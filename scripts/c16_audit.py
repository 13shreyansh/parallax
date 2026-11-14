"""Freeze/score/replay a fixed C-16 audit, without changing delivered product tables."""

import os

os.environ["HF_HUB_OFFLINE"] = "1"
import argparse, pathlib, json, hashlib, datetime, sys, re, collections, importlib.metadata, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
AUDIT = ROOT / "eval/c16"
from server.checks import check, baseline, dates
from server.db import connect, ASOF_SQL


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 20):
            h.update(b)
    return h.hexdigest()


def frozen_files():
    return [
        "eval/c16/SPEC.md",
        "eval/c16/PLAN.json",
        "eval/c16/cases.json",
        "eval/c16/facts.json",
        "eval/c16/source-articles.json",
        "scripts/c16_prepare.py",
        "scripts/c16_audit.py",
        "server/checks.py",
        "server/db.py",
        "scripts/ingest.py",
    ]


def freeze():
    p = AUDIT / "FROZEN.json"
    if p.exists():
        raise SystemExit(
            "Already frozen; use a new audit version rather than replacing it."
        )
    weights = sorted((ROOT / "work/models").rglob("model.safetensors"))
    if not weights:
        weights = sorted((ROOT / "work/models").rglob("pytorch_model.bin"))
    assert weights, "Cached fixed model weights not found"
    j = {
        "audit_id": "c16-family-audit-v1",
        "frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "files": {name: sha(ROOT / name) for name in frozen_files()},
        "model": {
            "id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "weight_file": weights[0].name,
            "sha256": sha(weights[0]),
        },
        "packages": {
            n: importlib.metadata.version(n)
            for n in ["sentence-transformers", "torch", "numpy", "pyarrow", "PyMySQL"]
        },
        "policy": "Fixed product, single final scoring run; no human labels or calibrated model judge.",
    }
    p.write_text(json.dumps(j, indent=2) + "\n")
    print("Frozen", len(j["files"]), "files and cached model weights.")


def verify():
    j = json.load(open(AUDIT / "FROZEN.json"))
    for name, h in j["files"].items():
        assert sha(ROOT / name) == h, "Frozen input changed: " + name
    weights = sorted((ROOT / "work/models").rglob(j["model"]["weight_file"]))
    assert weights and sha(weights[0]) == j["model"]["sha256"]
    return j


def main(out):
    frozen = verify()
    out.mkdir(parents=True, exist_ok=True)
    if (out / "FINAL.json").exists():
        raise SystemExit("Refusing to overwrite sealed FINAL.json")
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from scripts.ingest import chunks

    plan = json.load(open(AUDIT / "PLAN.json"))
    cases = json.load(open(AUDIT / "cases.json"))
    articles = json.load(open(AUDIT / "source-articles.json"))
    families = {
        q: f for f, qs in {**plan["development"], **plan["heldout"]}.items() for q in qs
    }
    model = SentenceTransformer(
        frozen["model"]["id"],
        cache_folder=str(ROOT / "work/models"),
        device="mps",
        local_files_only=True,
    )
    strings = sorted({c[k] for c in cases for k in ["a", "b"]})
    vecs = model.encode(
        strings, normalize_embeddings=True, batch_size=64, show_progress_bar=False
    )
    lookup = dict(zip(strings, vecs))
    traces = []
    for c in cases:
        sim = float(np.dot(lookup[c["a"]], lookup[c["b"]]))
        for mode, s in [
            ("rule_only_similarity_1", 1.0),
            ("measured_pair_embedding", sim),
        ]:
            verdict = check(c["a"], c["b"], s)
            pred = verdict["kind"] in ["date-review", "numeric-review"]
            traces.append(
                {
                    **c,
                    "path": mode,
                    "similarity": s,
                    "prediction_review": pred,
                    "weak_alignment": verdict["kind"] == "coverage",
                    "pass": pred == c["expected_review"],
                    "verdict": verdict,
                    "baseline_review": baseline(c["a"], c["b"]),
                }
            )
    groups = collections.defaultdict(list)
    for t in traces:
        for group in [
            ("overall", t["split"]),
            ("family", t["family"]),
            ("source", t["source"]),
            ("language_pair", "-".join(t["langs"])),
            ("nuisance", t["nuisance"]),
        ]:
            groups[(t["path"], *group)].append(t)
    summary = []
    for (mode, axis, value), ts in sorted(groups.items()):
        neg = [t for t in ts if not t["expected_review"]]
        pos = [t for t in ts if t["expected_review"]]
        summary.append(
            {
                "path": mode,
                "axis": axis,
                "value": value,
                "n": len(ts),
                "equivalents": len(neg),
                "false_positives": sum(t["prediction_review"] for t in neg),
                "planted": len(pos),
                "caught": sum(t["prediction_review"] for t in pos),
                "weak_alignments": sum(t["weak_alignment"] for t in ts),
            }
        )
    # Real native SQL on isolated audit tables. No product database rows are changed.
    con = connect(None)
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS npov_c16_audit CHARACTER SET utf8mb4")
    con.close()
    con = connect("npov_c16_audit")
    cur = con.cursor()
    for name in ["candidate_original", "candidate_renamed_reversed"]:
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {name}(id VARCHAR(64) CHARACTER SET ascii PRIMARY KEY,qid VARCHAR(24),lang CHAR(2),title VARCHAR(255),text TEXT,embedding VECTOR(384) NOT NULL,KEY(qid,lang),VECTOR INDEX(embedding) M=16 DISTANCE=cosine)"""
        )
    ps = []
    for a in articles:
        for i, (sec, text) in enumerate(chunks(a["text"])):
            ps.append(
                {
                    "id": f"{a['lang']}-{a['page_id']}-{i}",
                    "qid": a["wikidata_id"],
                    "lang": a["lang"],
                    "title": a["title"],
                    "text": text,
                    "section": sec,
                    "rev_id": a["rev_id"],
                }
            )
    em = model.encode(
        [p["text"] for p in ps],
        normalize_embeddings=True,
        batch_size=64,
        show_progress_bar=False,
    )
    for idx, table in enumerate(["candidate_original", "candidate_renamed_reversed"]):
        ordered = list(zip(ps, em))
        ordered = ordered if idx == 0 else list(reversed(ordered))
        for p, v in ordered:
            cur.execute(
                f"INSERT IGNORE INTO {table} VALUES(%s,%s,%s,%s,%s,%s)",
                (
                    p["id"],
                    p["qid"],
                    p["lang"],
                    p["title"] if idx == 0 else "Anonymous entry",
                    p["text"],
                    np.asarray(v, dtype="<f4").tobytes(),
                ),
            )

    def tokens(s):
        return set(re.findall(r"\w+", s.lower()))

    natural = []
    nuisance = []
    for p, v in zip(ps, em):
        if p["lang"] != "fi":
            continue
        answers = []
        for table in ["candidate_original", "candidate_renamed_reversed"]:
            cur.execute(
                f"SELECT id,text,VEC_DISTANCE_COSINE(embedding,VEC_FromText(%s)) AS distance FROM {table} WHERE qid=%s AND lang=%s ORDER BY distance LIMIT 3",
                (json.dumps(v.tolist()), p["qid"], "en"),
            )
            answers.append(cur.fetchall())
        nuisance.append(
            {
                "id": p["id"],
                "family": families[p["qid"]],
                "original_ids": [x["id"] for x in answers[0]],
                "renamed_reversed_ids": [x["id"] for x in answers[1]],
                "pass": [x["id"] for x in answers[0]] == [x["id"] for x in answers[1]],
                "scope": "Display-title metadata rename plus reverse insertion order; passage embedding unchanged.",
            }
        )
        d = dates(p["text"])
        targets = [t for t in ps if t["qid"] == p["qid"] and t["lang"] == "en"]
        refs = [t["id"] for t in targets if d and dates(t["text"]) == d]
        if not refs:
            continue
        lex = sorted(
            targets,
            key=lambda t: len(tokens(p["text"]) & tokens(t["text"]))
            / (len(tokens(p["text"]) | tokens(t["text"])) or 1),
            reverse=True,
        )[:3]
        natural.append(
            {
                "id": p["id"],
                "qid": p["qid"],
                "family": families[p["qid"]],
                "source": "S snapshot original Wikipedia excerpts",
                "query": p["text"],
                "reference_ids": refs,
                "vector": answers[0],
                "lexical": [{"id": x["id"], "text": x["text"]} for x in lex],
                "vector_hit": bool(set(refs) & {x["id"] for x in answers[0]}),
                "lexical_hit": bool(set(refs) & {x["id"] for x in lex}),
            }
        )
    retrieval = []
    for fam in families.values():
        if any(r["family"] == fam for r in retrieval):
            continue
        rs = [t for t in natural if t["family"] == fam]
        retrieval.append(
            {
                "family": fam,
                "n": len(rs),
                "vector_hit_at_3": sum(t["vector_hit"] for t in rs),
                "lexical_hit_at_3": sum(t["lexical_hit"] for t in rs),
            }
        )
    # Paired rephrase invariance, not broader semantic accuracy.
    byid = {(t["id"], t["path"]): t for t in traces}
    rephrase = []
    for t in traces:
        if t["nuisance"] != "rephrase":
            continue
        base = byid[(t["id"].removesuffix("rephrase") + "base", t["path"])]
        rephrase.append(
            {
                "id": t["id"],
                "path": t["path"],
                "family": t["family"],
                "base_review": base["prediction_review"],
                "rephrase_review": t["prediction_review"],
                "pass": base["prediction_review"] == t["prediction_review"],
                "base_similarity": base["similarity"],
                "rephrase_similarity": t["similarity"],
            }
        )
    temporal = []
    with connect() as prod:
        with prod.cursor() as c:
            for a in json.load(open(ROOT / "public/snapshot.json"))["articles"]:
                coverage = []
                asof = []
                for version in a["versions"]:
                    c.execute(
                        "SELECT COUNT(*) AS n,MIN(row_start) AS first_revision,MAX(row_start) AS last_revision FROM revision FOR SYSTEM_TIME ALL WHERE lang=%s AND page_id=%s",
                        (version["lang"], version["page_id"]),
                    )
                    r = c.fetchone()
                    coverage.append(
                        {
                            "lang": version["lang"],
                            **{
                                k: str(v) if hasattr(v, "isoformat") else v
                                for k, v in r.items()
                            },
                        }
                    )
                    c.execute(
                        ASOF_SQL,
                        ("2015-01-01 00:00:00", version["lang"], version["page_id"]),
                    )
                    r = c.fetchone()
                    asof.append(
                        {
                            "lang": version["lang"],
                            "revision": r["rev_id"] if r else None,
                        }
                    )
                temporal.append(
                    {
                        "qid": a["qid"],
                        "coverage": coverage,
                        "comparison_2015_utc": asof,
                        "status": "unproven",
                        "introduction_revision": None,
                        "reason": "No established factual disagreement and no continuous aligned multilingual history. Single-language content changes cannot identify cross-language disagreement onset.",
                    }
                )
    for name, obj in [
        ("controlled-traces.json", traces),
        ("natural-retrieval-traces.json", natural),
        ("metadata-nuisance-traces.json", nuisance),
        ("rephrase-traces.json", rephrase),
        ("temporal-onset.json", temporal),
    ]:
        json.dump(obj, open(out / name, "w"), ensure_ascii=False, indent=2)
    result = {
        "audit_id": frozen["audit_id"],
        "scored_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "freeze_sha256": sha(AUDIT / "FROZEN.json"),
        "product_detector_sha256": sha(ROOT / "server/checks.py"),
        "controlled_slices": summary,
        "natural_retrieval_by_family": retrieval,
        "metadata_rename_reorder": {
            "n": len(nuisance),
            "failed": sum(not t["pass"] for t in nuisance),
        },
        "rephrase_by_path": [
            {
                "path": mode,
                "n": sum(t["path"] == mode for t in rephrase),
                "flipped": sum(t["path"] == mode and not t["pass"] for t in rephrase),
            }
            for mode in ["rule_only_similarity_1", "measured_pair_embedding"]
        ],
        "natural_query_pool": sum(p["lang"] == "fi" for p in ps),
        "natural_scorable_date_proxy": len(natural),
        "audit_vector_rows": len(ps),
        "temporal_status": "unproven",
        "temporal_introduction_revision": None,
        "failures": [
            {
                "id": t["id"],
                "path": t["path"],
                "family": t["family"],
                "slice": t["slice"],
                "nuisance": t["nuisance"],
                "predicted": t["prediction_review"],
                "expected": t["expected_review"],
            }
            for t in traces
            if not t["pass"]
        ],
        "limits": [
            "Controlled translations are audit-authored and not human validated.",
            "Family-heldout does not mean publisher-independent or absent from pretrained model data.",
            "Natural relevance is only a full-date-overlap proxy; unscorable queries are excluded and counted.",
            "Paired tests omit retrieval and source verification; rule-only similarity=1 is a stress input.",
            "Metadata rename/reorder preserves passage embeddings by design.",
            "Product remains on build Mac and temporary tunnel.",
            "Previous product retrieval result favored lexical: 8/9 vs vector 7/9.",
        ],
    }
    json.dump(result, open(out / "FINAL.json", "w"), ensure_ascii=False, indent=2)
    files = {p.name: sha(p) for p in sorted(out.glob("*.json"))}
    json.dump(
        {
            "sealed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "files": files,
        },
        open(out / "SEALED.json", "w"),
        indent=2,
    )
    print(
        json.dumps(
            {
                "controlled_cases": len(cases),
                "vector_rows": len(ps),
                "retrieval": retrieval,
                "metadata": result["metadata_rename_reorder"],
                "failures": len(result["failures"]),
                "onset": "unproven",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["freeze", "final", "replay"])
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.mode == "freeze":
        freeze()
    else:
        if args.mode == "replay" and not args.out:
            ap.error("Replay requires a separate --out directory")
        if args.mode == "final" and args.out:
            ap.error("Final output path is fixed")
        main(pathlib.Path(args.out).resolve() if args.out else AUDIT / "final")
