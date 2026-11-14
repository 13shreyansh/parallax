"""Prepare diverse real pairs for a human. Never fill a human label automatically."""

import pathlib, json, csv

ROOT = pathlib.Path(__file__).resolve().parents[1]
articles = json.load(open(ROOT / "public/snapshot.json"))["articles"]
groups = []
for a in articles:
    fs = sorted(a["findings"], key=lambda f: f["fi"]["ordinal"])
    groups.append([fs[round(i * (len(fs) - 1) / 6)] for i in range(7)])
sample = [group[i] for i in range(7) for group in groups][:60]
with open(ROOT / "eval/annotation-queue.csv", "w") as out:
    w = csv.writer(out)
    w.writerow(
        [
            "fi_id",
            "qid",
            "fi_section",
            "fi_text",
            "fi_revision_url",
            "en_id",
            "en_text",
            "en_revision_url",
            "human_label",
            "annotator",
        ]
    )
    for f in sample:
        fi = f["fi"]
        en = f["matches"]["en"]
        w.writerow(
            [
                fi["id"],
                f["qid"],
                fi["section"],
                fi["text"],
                f"https://fi.wikipedia.org/w/index.php?oldid={fi['rev_id']}",
                en["id"],
                en["text"],
                f"https://en.wikipedia.org/w/index.php?oldid={en['rev_id']}",
                "",
                "",
            ]
        )
print(
    "Annotation queue:",
    len(sample),
    "pairs across",
    len(groups),
    "topics; all human labels blank",
)
