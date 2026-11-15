# Parallax evaluation record

The first frozen v4 run caught **32/40 (80%)** planted errors and produced **0/40 false flags** on source-supported controls. All eight dropped-sentence cases were missed.

After an alignment regression fix, a second independently labeled set from disjoint article families caught **34/40 (85%)**, with **0/40 false flags**. It caught two of eight dropped sentences. Dates, numbers, loaded wording and unsupported-claim cases were8/8 each in both runs. The90% recall target has not yet been reached.

These are controlled copies of real passages, not full-article population accuracy. The second set uses12 intact controls and28 exact supported excerpts; eight dropped-sentence cases have original Finnish or Swedish counterparts. Source documents and native MariaDB vector retrieval are real. Most clean controls are single-language, so their false-flag rate does not estimate clean multilingual article-pair performance. Prompts were frozen before each measurement. Test schemas are separate from the product; only aggregate results are published in its database.

The first blind gpt-6-astra review confirmed **53/60 (88.3%)** randomly sampled Winter War flags. A later theme-wide sample confirmed **44/60 (73.3%)**, with13 false and3 uncertain, from317 then-published flags. Uncertain counts as unconfirmed. Reviewers read complete peer articles and actual cited sources without detector verdicts, summaries or reasons.

The public list is subsequently restricted to independently confirmed findings. The above precision numbers describe the samples before that extra publication filter. They are not estimates of post-filter precision.

Frozen cases, prompt hashes and results are recorded in `FROZEN.json`, `RESULTS.json`, `FRESH-CONTROLS.json`, `FRESH-FROZEN.json`, `FRESH-RESULTS.json`, `BLIND-REAL.json` and `BLIND-FINAL.json`. Source and full-article caches remain private working artifacts.
