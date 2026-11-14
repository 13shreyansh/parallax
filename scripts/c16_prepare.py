"""Prepare source-family evidence and controlled translations. Does not score the detector."""

import pathlib, json, re, hashlib, datetime
import pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "eval/c16"
plan = json.load(open(OUT / "PLAN.json"))
allgroups = {**plan["development"], **plan["heldout"]}
qidfamily = {q: f for f, qs in allgroups.items() for q in qs}
articles = []
for lang in ["fi", "en", "sv"]:
    articles.extend(
        [
            r
            for r in pq.read_table(
                ROOT / f"work/vector-starter/data/articles-{lang}.parquet"
            ).to_pylist()
            if r["wikidata_id"] in qidfamily
        ]
    )
assert len(articles) == len(qidfamily) * 3
json.dump(
    articles, open(OUT / "source-articles.json", "w"), ensure_ascii=False, indent=2
)
# These translations are audit-authored constructions, not native Wikipedia quotations or human labels.
facts = [
    (
        "war-start",
        "Q134949",
        "30 November 1939",
        "30. marraskuuta 1939",
        "30 november 1939",
        "The Winter War began on {d}.",
        "Talvisota alkoi {d}.",
        "Vinterkriget började den {d}.",
        "{d} was the start date of the Winter War.",
        "Talvisodan alkamispäivä oli {d}.",
        "Vinterkrigets startdatum var den {d}.",
    ),
    (
        "continuation-start",
        "Q122100",
        "25 June 1941",
        "25. kesäkuuta 1941",
        "25 juni 1941",
        "The Continuation War began on {d}.",
        "Jatkosota alkoi {d}.",
        "Fortsättningskriget började den {d}.",
        "The start date of the Continuation War was {d}.",
        "Jatkosodan alkamispäivä oli {d}.",
        "Fortsättningskrigets startdatum var den {d}.",
    ),
    (
        "academy-foundation",
        "Q414481",
        "26 March 1640",
        "26. maaliskuuta 1640",
        "26 mars 1640",
        "The Royal Academy of Turku was founded on {d}.",
        "Turun akatemia perustettiin {d}.",
        "Kungliga Akademien i Åbo grundades den {d}.",
        "On {d}, the Royal Academy of Turku was founded.",
        "{d} oli Turun akatemian perustamispäivä.",
        "Den {d} grundades Kungliga Akademien i Åbo.",
    ),
    (
        "tkk-foundation",
        "Q1646874",
        "1849",
        "1849",
        "1849",
        "Helsinki University of Technology was founded in {d}.",
        "Teknillinen korkeakoulu perustettiin vuonna {d}.",
        "Tekniska högskolan grundades år {d}.",
        "The founding year of Helsinki University of Technology was {d}.",
        "Teknillisen korkeakoulun perustamisvuosi oli {d}.",
        "Tekniska högskolans grundläggningsår var {d}.",
    ),
    (
        "tut-merger",
        "Q277664",
        "1 January 2019",
        "1. tammikuuta 2019",
        "1 januari 2019",
        "Tampere University of Technology merged with the University of Tampere on {d}.",
        "Tampereen teknillinen yliopisto yhdistyi Tampereen yliopiston kanssa {d}.",
        "Tammerfors tekniska universitet slogs samman med Tammerfors universitet den {d}.",
        "On {d}, Tampere University of Technology and the University of Tampere merged.",
        "{d} Tampereen teknillinen yliopisto ja Tampereen yliopisto yhdistyivät.",
        "Den {d} slogs Tammerfors tekniska universitet och Tammerfors universitet samman.",
    ),
    (
        "luoma-closure",
        "Q4411811",
        "27 March 2016",
        "27. maaliskuuta 2016",
        "27 mars 2016",
        "Luoma railway station closed on {d}.",
        "Luoman rautatieasema suljettiin {d}.",
        "Bobäcks hållplats stängdes den {d}.",
        "The closure date of Luoma railway station was {d}.",
        "Luoman rautatieaseman sulkemispäivä oli {d}.",
        "Bobäcks hållplats stängningsdatum var den {d}.",
    ),
    (
        "mankki-closure",
        "Q6750548",
        "27 March 2016",
        "27. maaliskuuta 2016",
        "27 mars 2016",
        "Mankki railway station closed on {d}.",
        "Mankin rautatieasema suljettiin {d}.",
        "Mankby hållplats stängdes den {d}.",
        "The closure date of Mankki railway station was {d}.",
        "Mankin rautatieaseman sulkemispäivä oli {d}.",
        "Mankby hållplats stängningsdatum var den {d}.",
    ),
    (
        "piikkio-last-train",
        "Q18661302",
        "26 May 1979",
        "26. toukokuuta 1979",
        "26 maj 1979",
        "The last train stopped at Piikkiö railway station on {d}.",
        "Viimeinen juna pysähtyi Piikkiön rautatieasemalla {d}.",
        "Det sista tåget stannade vid Pikis järnvägsstation den {d}.",
        "On {d}, the last train stopped at Piikkiö railway station.",
        "{d} viimeinen juna pysähtyi Piikkiön rautatieasemalla.",
        "Den {d} stannade det sista tåget vid Pikis järnvägsstation.",
    ),
]
cases = []
fact_records = []
for row in facts:
    fid, qid, *rest = row
    ds = rest[:3]
    templates = rest[3:6]
    rephrases = rest[6:9]
    source = next(a for a in articles if a["wikidata_id"] == qid and a["lang"] == "en")
    year = re.search(r"\d{4}", ds[0]).group()
    assert year in source["text"]
    lines = [line for line in source["text"].splitlines() if year in line]
    source_ref = {
        "lang": "en",
        "rev_id": source["rev_id"],
        "url": f"https://en.wikipedia.org/w/index.php?oldid={source['rev_id']}",
        "title": source["title"],
        "matching_source_paragraph": lines[0],
    }
    triples = {
        lang: t.format(d=d) for lang, t, d in zip(["en", "fi", "sv"], templates, ds)
    }
    rewrites = {
        lang: t.format(d=d) for lang, t, d in zip(["en", "fi", "sv"], rephrases, ds)
    }
    fact_records.append(
        {
            "fact_id": fid,
            "qid": qid,
            "family": qidfamily[qid],
            "source": source_ref,
            "claims": triples,
            "rephrases": rewrites,
            "construction_note": "Audit-authored translations, not human labels or quotations from FI/SV articles; source backs the tested value, not a general truth verdict.",
        }
    )
    for left, right in [("fi", "en"), ("fi", "sv"), ("sv", "en")]:
        for nuisance in ["base", "rephrase", "context_reorder"]:
            a = triples[left]
            b = rewrites[right] if nuisance == "rephrase" else triples[right]
            if nuisance == "context_reorder":
                a = "This statement concerns the stored article. " + a
                b = b + " This statement concerns the stored article."
            cases.append(
                {
                    "id": f"{fid}-{left}-{right}-{nuisance}",
                    "fact_id": fid,
                    "qid": qid,
                    "family": qidfamily[qid],
                    "split": "development"
                    if qid in plan["development"]["wartime_history"]
                    else "heldout",
                    "source": "S Wikipedia snapshot, controlled translation",
                    "slice": "translation_equivalent",
                    "nuisance": nuisance,
                    "langs": [left, right],
                    "a": a,
                    "b": b,
                    "expected_review": False,
                    "label_origin": "audit-authored controlled equivalent, no human validation",
                    "source_ref": source_ref,
                }
            )
        for mutation in ["year", "name"]:
            b = triples[right]
            if mutation == "year":
                b = b.replace(year, str(int(year) + 1), 1)
            else:
                # Deliberately swap the entity's name, preserving the date. Construction label only.
                names = {
                    "war-start": {
                        "en": "Winter War",
                        "fi": "Talvisota",
                        "sv": "Vinterkriget",
                    },
                    "continuation-start": {
                        "en": "Continuation War",
                        "fi": "Jatkosota",
                        "sv": "Fortsättningskriget",
                    },
                    "academy-foundation": {
                        "en": "Royal Academy of Turku",
                        "fi": "Turun akatemia",
                        "sv": "Kungliga Akademien i Åbo",
                    },
                    "tkk-foundation": {
                        "en": "Helsinki University of Technology",
                        "fi": "Teknillinen korkeakoulu",
                        "sv": "Tekniska högskolan",
                    },
                    "tut-merger": {
                        "en": "Tampere University of Technology",
                        "fi": "Tampereen teknillinen yliopisto",
                        "sv": "Tammerfors tekniska universitet",
                    },
                    "luoma-closure": {"en": "Luoma", "fi": "Luoman", "sv": "Bobäcks"},
                    "mankki-closure": {"en": "Mankki", "fi": "Mankin", "sv": "Mankby"},
                    "piikkio-last-train": {
                        "en": "Piikkiö",
                        "fi": "Piikkiön",
                        "sv": "Pikis",
                    },
                }
                assert names[fid][right] in b
                b = b.replace(names[fid][right], "Atlantis", 1)
            cases.append(
                {
                    "id": f"{fid}-{left}-{right}-changed-{mutation}",
                    "fact_id": fid,
                    "qid": qid,
                    "family": qidfamily[qid],
                    "split": "development"
                    if qid in plan["development"]["wartime_history"]
                    else "heldout",
                    "source": "S Wikipedia snapshot, controlled mutation",
                    "slice": "planted_error",
                    "nuisance": mutation,
                    "langs": [left, right],
                    "a": triples[left],
                    "b": b,
                    "expected_review": True,
                    "label_origin": "synthetic changed copy, no human label",
                    "source_ref": source_ref,
                }
            )
# Same approximate percentage, different decimal conventions. This is the important unit-format negative control.
qid = "Q277664"
source = next(a for a in articles if a["wikidata_id"] == qid and a["lang"] == "en")
assert "50%" in source["text"]
base = {
    "en": "About 50 percent of the university budget was external funding.",
    "fi": "Noin 50,0 prosenttia yliopiston budjetista oli ulkoista rahoitusta.",
    "sv": "Ungefär 50 procent av universitetets budget var extern finansiering.",
}
for left, right in [("fi", "en"), ("fi", "sv"), ("sv", "en")]:
    cases.append(
        {
            "id": f"budget-percent-{left}-{right}",
            "fact_id": "budget-percent",
            "qid": qid,
            "family": "education_institutions",
            "split": "heldout",
            "source": "S Wikipedia snapshot, controlled numeric formatting",
            "slice": "translation_equivalent",
            "nuisance": "decimal_format",
            "langs": [left, right],
            "a": base[left],
            "b": base[right],
            "expected_review": False,
            "label_origin": "audit-authored numerical equivalent, no human validation",
            "source_ref": {
                "url": f"https://en.wikipedia.org/w/index.php?oldid={source['rev_id']}",
                "matching_source_paragraph": next(
                    l for l in source["text"].splitlines() if "50%" in l
                ),
            },
        }
    )
json.dump(fact_records, open(OUT / "facts.json", "w"), ensure_ascii=False, indent=2)
json.dump(cases, open(OUT / "cases.json", "w"), ensure_ascii=False, indent=2)
print(
    "Prepared",
    len(articles),
    "source versions and",
    len(cases),
    "controlled cases. No scoring run.",
)
