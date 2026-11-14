# Independent evidence review request

Read only SPEC.md and the evidence named here. Do not read the builder conversation, bridge history or other chat summaries. Do not edit product code or sealed evidence. No browser is needed; use only local artifacts. Do not spawn other agents.

Claim document: ../../README.md, REPORT.md and ../../public/evaluation.json.

Frozen inputs: PLAN.json, FROZEN.json, facts.json, cases.json, source-articles.json, ../../scripts/c16_audit.py, ../../scripts/c16_prepare.py, ../../server/checks.py, ../../server/db.py, ../../scripts/ingest.py.

Sealed evidence: final/FINAL.json, final/SEALED.json, final/controlled-traces.json, final/natural-retrieval-traces.json, final/metadata-nuisance-traces.json, final/rephrase-traces.json, final/temporal-onset.json. Post-seal exploratory evidence: post-seal-nuisance-diagnosis.json. Earlier baseline evidence: ../retrieval-results.json and ../runs/v1/results.json.

Check file hashes and recompute the reported fractions from raw traces. Check family membership separation, prior-seen exclusions, correlated-case limits, source/family slices and nuisance denominators. Inspect source-backed fact examples, especially the decimal-format false-positive slice and name mutations. Distinguish constructed translation assumptions from validated human equivalence. Check whether the temporal evidence justifies any introduction revision and refuse such a claim if not. Distinguish code/plumbing invariance from semantic robustness. Check which retrieval baseline won and whether audit results are overgeneralized. Do not claim human labels, a calibrated judge, publisher independence, unseen model training data, compliance, general accuracy or durable hosting without actual evidence.

Return a concise report with verdict, evidence checks, unsupported/refused judgments, material corrections required and provenance limits. An honest negative result can pass an evidence audit. Your role is a fresh model-agent consistency review, not a human historian, independent-model-family experiment or translation certification. Record exact model identity only if exposed by your runtime; otherwise say it is not exposed. Keep raw final outputs unchanged.
