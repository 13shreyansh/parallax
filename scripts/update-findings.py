import sys, pathlib, json, re, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server.db import connect
from server.checks import check, dates, MONTHS

source_html = (ROOT / "work/source-yle.html").read_text()
source_quote = "The war began on February 21, 1808"
assert source_quote in source_html, "Source excerpt changed; abstain and inspect it."
m = re.search(r"([A-Za-z]+) (\d{1,2}), (\d{4})", source_quote)
source_date = (
    f"{int(m.group(3)):04}-{MONTHS[m.group(1).lower()]:02}-{int(m.group(2)):02}"
)

j = json.load(open(ROOT / "public/snapshot.json"))
c = connect().cursor()
source = {
    "status": "supports-date",
    "reason": "The Yle report cited in this article supports the start date, 21 February 1808. This check does not verify the rest of the passage.",
    "quote": "The war began on February 21, 1808",
    "url": "https://yle.fi/a/3-5823726",
    "title": "Southern Towns Mark War of Finland Bicentennial",
    "publisher": "Yle News",
    "source_published": "2008-02-21",
    "fetched_at": datetime.datetime.fromtimestamp(
        (ROOT / "work/source-yle.html").stat().st_mtime, datetime.timezone.utc
    ).isoformat(),
    "html_sha256": hashlib.sha256(
        (ROOT / "work/source-yle.html").read_bytes()
    ).hexdigest(),
    "scope": "English start date only",
    "method": "Exact source excerpt and deterministic date comparison. Curated example, not an automatic all-source audit.",
}
for a in j["articles"]:
    for f in a["findings"]:
        f["flags"] = []
        for lang, m in f["matches"].items():
            m["check"] = check(f["fi"]["text"], m["text"], 1 - m["distance"])
            if m["check"]["kind"] not in ["aligned", "emphasis"]:
                f["flags"].append(m["check"]["kind"])
        if a["qid"] == "Q736268" and "21 February 1808" in f["matches"].get(
            "en", {}
        ).get("text", ""):
            claim_dates = dates(f["matches"]["en"]["text"])
            if claim_dates and min(claim_dates) == source_date:
                f["source"] = {**source, "checked_start_date": source_date}
        c.execute(
            "REPLACE INTO finding VALUES (%s,%s,%s)",
            (f["id"], a["qid"], json.dumps(f, ensure_ascii=False)),
        )
    a["review_count"] = sum(
        any(x in ["date-review", "numeric-review"] for x in f["flags"])
        for f in a["findings"]
    )
    a["findings"].sort(
        key=lambda f: (
            -sum(x in ["date-review", "numeric-review"] for x in f["flags"]),
            -bool(f["tone"]),
            f["fi"]["ordinal"],
        )
    )
j["articles"].sort(key=lambda a: (-a["review_count"], -a["distance"]))
json.dump(j, open(ROOT / "public/snapshot.json", "w"), ensure_ascii=False)
json.dump(
    source, open(ROOT / "data/source-evidence.json", "w"), ensure_ascii=False, indent=2
)
print([(a["title"], a["review_count"]) for a in j["articles"]])
