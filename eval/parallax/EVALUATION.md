# Parallax evaluation record

The first frozen v4 run caught **32/40 (80%)** planted errors and produced **0/40 false flags** on source-supported controls. All eight dropped-sentence cases were missed.

After an alignment regression fix, a second independently labeled set from disjoint article families caught **34/40 (85%)**, with **0/40 false flags**. It caught two of eight dropped sentences. Dates, numbers, loaded wording and unsupported-claim cases were 8/8 each in both runs. A third disjoint set, frozen after Winter War-only coverage development, caught **40/40 (100%)**, with **0/40 false flags**, meeting the numerical target on that controlled set. The third prompt clarifies coverage versus source verification; its larger numeric mutations avoid compatible rounding. This changed error severity limits comparison across rounds.

These are controlled copies of real passages, not full-article population accuracy. The second set uses 12 intact controls and 28 exact supported excerpts; eight dropped-sentence cases have original Finnish or Swedish counterparts. Source documents and native MariaDB vector retrieval are real. Most clean controls are single-language, so their false-flag rate does not estimate clean multilingual article-pair performance. Prompts were frozen before each measurement. Test schemas are separate from the product; only aggregate results are published in its database.

The first blind gpt-6-astra review confirmed **53/60 (88.3%)** randomly sampled Winter War flags. A later theme-wide sample confirmed **44/60 (73.3%)**, with 13 false and 3 uncertain, from 317 then-published flags. Uncertain counts as unconfirmed. Reviewers read complete peer articles and actual cited sources without detector verdicts, summaries or reasons.

The public list is subsequently restricted to independently confirmed findings. The above precision numbers describe the samples before that extra publication filter. They are not estimates of post-filter precision.

Frozen cases, prompt hashes and results are recorded in `FROZEN.json`, `RESULTS.json`, `FRESH-CONTROLS.json`, `FRESH-FROZEN.json`, `FRESH-RESULTS.json`, `THIRD-CONTROLS.json`, `THIRD-FROZEN.json`, `THIRD-RESULTS.json`, `BLIND-REAL.json` and `BLIND-FINAL.json`. Source and full-article caches remain private working artifacts.
