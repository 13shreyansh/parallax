# Evaluation ledger

All runs in this ledger were performed during Junction on 14 November 2026, Helsinki time. Raw traces are committed. There are no human annotations or calibrated model judges. Synthetic mutation labels and weak automated retrieval proxies are identified separately.

## C-16 separate frozen family audit

See [C-16 report](c16/REPORT.md), [spec](c16/SPEC.md), [freeze manifest](c16/FROZEN.json) and [sealed final result](c16/final/FINAL.json). Product detector/model/thresholds were unchanged. New whole-family held-out measured paired tests caught 5/36 planted errors with 2/57 false flags on controlled equivalents. Held-out natural date proxy: vector 3/4 vs lexical 4/4. Combined metadata rename/reverse insertion changed 25/742 top-three rankings. All failures are published. Introduction of disagreement at revision X remains unproven. No new human labels or durable remote hosting are claimed. The earlier results below retain their original scope and history.

## What is being measured

The product produces review leads with exact evidence. It does not produce a validated neutrality score or general truth verdict. A flagged number can still describe a different scope. The evaluation isolates specific rules and checks the database's revision behavior; it does not establish real-world contradiction precision or recall.

The article split was frozen before classification work in `split.json`: four development topics and five initial held-out topics. The original brief had incorrect Wikidata IDs for several topics; the IDs were resolved from the actual supplied Parquet metadata before running the product. The final `split.json` records the real topics.

## v1 · conservative date/unit rules

Baseline: compare the sets of numeral strings in two sentences. Rules: full-date normalization, similar-passage checks and a small shared-unit set. Synthetic cases use actual English sentences paired with unchanged or deliberately modified copies. Similarity is fixed at 1 for edited copies; this is not an embedding pipeline test.

| Split | Method | Planted recall | False flags on negative controls |
|---|---|---:|---:|
| Dev, 51 cases | Naive numeral mismatch | 24/24 | 15/27 |
| Dev, 51 cases | Guarded rules v1 | 7/24 | 0/27 |
| Initial held-out, 77 cases | Naive numeral mismatch | 36/36 | 23/41 |
| Initial held-out, 77 cases | Guarded rules v1 | 16/36 | 0/41 |

Observed development failures: year changes were ignored because the rule demanded equal year sets; a changed date could be hidden by another date shared by both sentences. Preserve the baseline's recall while suppressing additional-context false positives was the next development hypothesis. Initial held-out results were already viewed at this point. They are not called untouched after v2.

Artifacts: `runs/v1/results.json`, `runs/v1/traces.json`, `runs/v1/checks.py`.

## v2 · compare full-date sets conservatively

Before changing the rule, reserved five fresh S-dataset articles in `split-v2.json`: Great Fire of Turku, Juho Kusti Paasikivi, Urho Kekkonen, Treaty of Fredrikshamn and Finnish famine of 1866–1868. Selection is deterministic by title. These are held-out articles, but they are still the same historical domain and constructed mutation task.

Change: allow year changes and single changed dates within otherwise matching date sets when cardinality is equal and similarity is at least 0.86. Unequal sets abstain to avoid treating added context as a contradiction. Name swaps were added as a deliberate unsupported failure mode. This changes the task mix, so v1 and v2 aggregate percentages are not a direct score comparison.

| Split | Cases | Method | Planted recall | False flags on negative controls |
|---|---:|---|---:|---:|
| Dev | 58 | Naive numeral mismatch | 24/31 | 15/27 |
| Dev | 58 | Guarded rules | 24/31 | 0/27 |
| Initial held-out, already seen | 85 | Naive numeral mismatch | 36/44 | 23/41 |
| Initial held-out, already seen | 85 | Guarded rules | 35/44 | 0/41 |
| Fresh held-out | 42 | Naive numeral mismatch | 18/20 | 13/22 |
| Fresh held-out | 42 | Guarded rules | 18/20 | 0/22 |

The fresh held-out result is **90% planted recall and 0% constructed-control false-positive rate**, 20 positives and 22 negatives. Both misses were country-name changes. This is not a real-world accuracy estimate. The cases reuse sentences for multiple variants, so case outcomes are correlated. The fresh set has only nine original date-bearing sentences across four contributing articles. Five articles were reserved; the famine article had no eligible full-date sentence and contributed no case. Do not treat 42 cases as 42 independent real claims.

Observed a development-article numeric false lead: a Finnish Civil War passage about 75% of deaths being Reds matched a Swedish passage about 64.6% of a different group being civilians. Similarity was 0.755. Raised the numeric gate from 0.72 to 0.86 and kept the cautionary scope language. The date-fixture results above do not measure this numeric-gate refinement. It removes that observed lead, but does not validate the remaining numeric detector.

Rule execution is local with no model/API inference charge. CPU time for v2 is in `public/evaluation.json`; medians are about 0.005 ms per case on this machine. This excludes ingestion, embedding, database retrieval, UI, network and hardware cost. No calibrated tone or contradiction LLM judge ran. The requested whole-article LLM baseline did not run; the measured baseline is the transparent numeral-set checker.

Artifacts: `cases.json`, `traces.json`, `split-v2.json`, `public/evaluation.json`. All labels are `synthetic controlled edit` or `synthetic negative control` construction labels.

## Cross-language retrieval proxy

Find real Finnish passages with extracted full dates and at least one English passage in the same topic with exactly the same date set. Treat those English passages as weak relevance references. Query the actual MariaDB vector table for top 3 and compare with lexical Jaccard overlap over all same-topic English candidates.

| Split | Queries | MariaDB vector hit@3 | Lexical hit@3 |
|---|---:|---:|---:|
| Dev | 7 | 7/7 | 7/7 |
| Initial held-out topics | 9 | 7/9 | 8/9 |

**No vector improvement was observed.** This is a tiny, date-heavy, weakly labeled proxy, not a human semantic-relevance benchmark. Different events can share dates, and date numerals favor lexical matching. It does not test contradiction classification. The filtered query is a native cosine calculation over a small same-topic pool; no HNSW speedup is claimed for it.

Artifacts: `retrieval-results.json`, `retrieval-traces.json`. `annotation-queue.csv` contains 60 real pairs with blank human-label and annotator columns. An expert still needs to label them.

## Temporal database checks

For each of the nine selected Finnish articles, choose a genuine archived revision near 2014 and query its exact UTC timestamp using `FOR SYSTEM_TIME AS OF`. Compare the returned revision ID against the Parquet metadata, not against the application's own expected output.

Initial run: 0/9. Root cause was connection timezone defaulting to Helsinki when the expected timestamp was UTC. The online as-of route already set UTC, but the shared connection helper and history listing did not. Set UTC at connection creation. Final result: **9/9** matching archived revision IDs. This is a regression check on selected timestamps, not proof of every possible historical query.

A separate gap check at 2026-10-02 for Winter War returns no row. The October archive ends at its real coverage cutoff, while recently fetched revisions begin later. The importer originally bridged this gap; it was corrected before delivery. No fabricated timestamps are used. Same-second zero-validity older edits are skipped.

Artifacts: `temporal-results.json`, `data/history-coverage.json`.

## Database timings and scale

Product run: MariaDB 13.0.2, local macOS Unix socket, 2,308 passage vectors, 1,766 filtered alignment queries. Measured p50 **1.43 ms**, p95 **4.60 ms**. This includes Python-to-SQL retrieval but excludes embedding, ingestion, network and UI. Current worklist covers nine topics and 27 live versions, capped at 100 usable passages per language/article.

M: official release contains 862,076 revision rows. Actual imported rows: 12,944 across selected Finnish histories and recent FI/EN/SV API revisions. The whole M release was downloaded and checksum verified; the whole M history was not loaded into the application.

L: official metadata contains 568,416 rows. Actual probe loaded **1,000** native vectors from the first 1,000 Parquet rows, title plus first 400 characters. Model embedding took **1.49 s** and vector insertion **1.04 s**. Thirty native nearest-neighbor queries measured p50 **0.59 ms**, p95 **0.88 ms** locally. Query inputs are stored probe vectors; this is a load/query plumbing check, not a semantic-quality benchmark. Full L load, memory scaling and concurrency are unmeasured. The first rows are not a representative random sample.

M/L downloads were checked against the official SHA256SUMS. Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, 384 dimensions, max 128 tokens. Some selected sentences may still truncate. No embedding calibration study was performed.

Artifacts: `database-run.json`, `scale-results.json`.

## Source-check evidence

A source linked in the English Finnish War article, Yle's "Southern Towns Mark War of Finland Bicentennial", was retrieved successfully. A short exact excerpt supports 21 February 1808 as the start date. The source record stores URL, retrieval time and HTML hash. This curated example checks only that date. It does not verify every claim, all sources, or whole-article neutrality. Other source checks say cannot verify. No unsupported-source verdict was fabricated.

## Remaining failures and next decision

- Country-name swaps and general factual contradictions remain undetected.
- The model sometimes retrieves the wrong event or scope; numerical differences are insufficient without context.
- Low similarity can be a retrieval miss, rather than an omission. The UI preserves alternatives and uncertainty.
- Matching dates do not establish all-claim agreement. Source checks mostly abstain.
- Historical cross-language discrepancy onset is not established by viewing Finnish history.
- Human expert labels, an independent calibrated judge, numeric-scope evaluation and a stronger retrieval set are still needed.

Next evidence should be the 60 human labels and the actual retrieval misses, not a claim that vector search has already won. No human labels are available in this ledger.

C-16 publication checks: new evaluation JSON is byte-identical to the reviewed local publication, frontend JS/CSS hashes match the delivered build, README relative evidence links resolve, and all ten existing deployment regression checks pass with receipts saved separately in c16/. The sealed-final and reviewed-report overwrite guards refuse replacements. A new IAB copy check was requested, not claimed complete.
