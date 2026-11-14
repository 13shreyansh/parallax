# Human annotation queue

`annotation-queue.csv` contains 60 actual MariaDB-retrieved FI/EN pairs, spread across all nine topics and spaced across the stored passage ordinals. Section names and exact revision links provide context. The sampling is for diagnosis, not a representative real-world estimate.

The `human_label` and `annotator` columns are intentionally blank. No human has supplied these labels. Suggested categories after review are agree, omit, contradict, emphasis, and cannot verify. Different emphasis is valid. A single nearest passage cannot establish an omission; inspect the target article before applying that label. Use cited sources to establish a factual contradiction. If the context or source is missing, cannot verify is useful.

Do not merge these future human annotations with the synthetic fixture labels. Preserve annotator, date and criteria version, and record any disagreements. The current evaluation ledger has no human-ground-truth accuracy claim.
