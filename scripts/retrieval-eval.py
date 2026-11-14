"""Date-overlap retrieval proxy, not human semantic relevance labels."""

import sys, pathlib, json, time, re, statistics

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server.db import connect, ALIGN_SQL, ASOF_SQL
from server.checks import dates
import numpy as np

ps = json.load(open(ROOT / "data/passages.json"))
emb = np.load(ROOT / "work/embeddings.npy")
split = json.load(open(ROOT / "eval/split.json"))
con = connect()
c = con.cursor()
traces = []


def tokens(s):
    return set(re.findall(r"\w+", s.lower()))


for i, p in enumerate(ps):
    if p["lang"] != "fi" or not dates(p["text"]):
        continue
    targets = [t for t in ps if t["qid"] == p["qid"] and t["lang"] == "en"]
    d = dates(p["text"])
    refs = [t["id"] for t in targets if dates(t["text"]) == d]
    if not refs:
        continue
    c.execute(ALIGN_SQL, (json.dumps(emb[i].tolist()), p["qid"], "en"))
    retrieved = c.fetchall()
    lex = sorted(
        targets,
        key=lambda t: len(tokens(p["text"]) & tokens(t["text"]))
        / (len(tokens(p["text"]) | tokens(t["text"])) or 1),
        reverse=True,
    )[:3]
    traces.append(
        {
            "id": p["id"],
            "qid": p["qid"],
            "split": "dev" if p["qid"] in split["dev"] else "initial held-out",
            "fi": p["text"],
            "dates": sorted(d),
            "reference_ids": refs,
            "vector": [
                {"id": r["id"], "text": r["text"], "distance": float(r["distance"])}
                for r in retrieved
            ],
            "lexical": [{"id": r["id"], "text": r["text"]} for r in lex],
            "vector_hit": bool(set(refs) & {r["id"] for r in retrieved}),
            "lexical_hit": bool(set(refs) & {r["id"] for r in lex}),
        }
    )
rows = []
for s in ["dev", "initial held-out"]:
    rs = [r for r in traces if r["split"] == s]
    rows.append(
        {
            "split": s,
            "n": len(rs),
            "vector_hit_at_3": sum(r["vector_hit"] for r in rs),
            "lexical_hit_at_3": sum(r["lexical_hit"] for r in rs),
        }
    )
# Genuine temporal verification against archived fixture metadata, not the app's own response.
import pyarrow.parquet as pq

fixtures = []
for p in sorted((ROOT / "work/official/m").glob("*.parquet")):
    t = pq.read_table(
        p,
        columns=["page_id", "title", "rev_id", "timestamp"],
        filters=[
            (
                "page_id",
                "in",
                [
                    a["page_id"]
                    for a in json.load(open(ROOT / "work/current-articles.json"))
                    if a["lang"] == "fi"
                ],
            )
        ],
    ).to_pylist()
    for pid in sorted({r["page_id"] for r in t}):
        vs = sorted(
            [r for r in t if r["page_id"] == pid], key=lambda r: str(r["timestamp"])
        )
        r = next((r for r in vs if str(r["timestamp"]) > "2014-01-01"), vs[0])
        ts = (
            str(r["timestamp"]).replace("T", " ").replace("Z", "").replace("+00:00", "")
        )
        c.execute(ASOF_SQL, (ts, "fi", pid))
        got = c.fetchone()
        fixtures.append(
            {
                "page_id": pid,
                "asof": ts,
                "expected_rev": r["rev_id"],
                "actual_rev": got["rev_id"] if got else None,
                "pass": bool(got and got["rev_id"] == r["rev_id"]),
            }
        )
json.dump(
    {
        "description": "Weak relevance proxy: an English passage containing exactly the same extracted full dates as the Finnish query is considered relevant. Equal dates can describe different events. Not human labels or contradiction accuracy. All query candidates are restricted to the same article topic.",
        "rows": rows,
    },
    open(ROOT / "eval/retrieval-results.json", "w"),
    indent=2,
)
json.dump(
    traces, open(ROOT / "eval/retrieval-traces.json", "w"), ensure_ascii=False, indent=2
)
json.dump(fixtures, open(ROOT / "eval/temporal-results.json", "w"), indent=2)
print(json.dumps(rows))
print("Temporal archive checks", sum(f["pass"] for f in fixtures), "/", len(fixtures))
# Human annotation is exported separately; labels stay blank.
import runpy

runpy.run_path(str(ROOT / "scripts/export-annotation.py"))
