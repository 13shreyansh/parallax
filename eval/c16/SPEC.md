# C-16 frozen audit specification

Audit an unchanged product, baseline commit 7f98b50. The product detector, thresholds and model must retain their baseline file hashes. Do not tune after seeing final results. C-08 remains delivered; C-16 is a separate improvement task.

## Families and evidence

PLAN.json selects development wartime history and six previously unaudited topics in two held-out entity families, education institutions and railway sites. Every language version of a topic stays in the same family. All original S snapshot articles for these ten topics are source-articles.json. Family names are builder-authored groupings, not expert taxonomy. They can share historical context, and all are Wikipedia. This is not publisher-independent evaluation or proof of exclusion from pretrained model data.

Prior article-level held-outs and prior confirmation families are marked seen and excluded from the new heldout. All six new topics were selected by title metadata before their texts were opened for this audit. Both development and heldout retrieval use the same S snapshot source and original chunking, so the source-version policy is consistent within this audit. The deployed live corpus is not replaced.

## Measurements decided before scoring

1. Translation-equivalent controls: cases.json contains audit-authored FI/EN/SV translations of source-backed facts, meaning-preserving rephrases, neutral-clause reordering and decimal-format equivalents. These are construction labels, not human labels or natural Wikipedia translation-alignment gold. Report date/unit review false positives over all equivalent controls, separately by family, source type, language pair and nuisance. Also report weak alignments, which are abstentions rather than factual accusations.
2. Planted errors: controlled changed years and actual subject-name swaps, never real Wikipedia revisions. Report errors detected/missed per family and mutation, with unchanged controls. A bare year may be missed. These are not general contradiction accuracy claims.
3. Separate rule stress from measured embeddings: use similarity fixed at 1 only in the explicitly named rule-only stress slice. Separately encode each pair with the unchanged multilingual model and apply its actual cosine similarity. Neither paired slice includes retrieval. Low false positives can coexist with poor recall and must not be celebrated alone.
4. Natural retrieval: import original S passages into isolated npov_c16_audit tables, use real MariaDB native vectors and same-topic language filters. For FI queries with exact full-date-overlap EN references, compare vector top3 with lexical Jaccard top3. This is a weak date-overlap proxy, not semantic relevance gold. Report unscorable queries and zero-size family slices. Publish losses, ties and wins without changing the fixed algorithm.
5. Rename/reorder: create an isolated candidate copy with anonymous display titles and reverse insertion order. Requery every FI passage and compare top3 IDs against the original isolated table. This is a database/plumbing invariance check; titles are not embedded by the delivered pipeline, so it is not evidence of semantic robustness to renaming entities inside claims.
6. Rephrase: report whether false-positive decisions change on the pre-authored paraphrases relative to their base equivalents, separately for measured embeddings and rule-only stress. Keep raw cosine similarities. Do not infer general paraphrase robustness from a few controlled templates.
7. Temporal introduction: query real revision coverage and a 2015 multilingual comparison from the delivered versioned table. An introduction revision requires a justified before/after claim comparison across languages, appropriate event/scope, continuous or bounded complete revision evidence, and an established disagreement. Text changing in one revision is insufficient. If these prerequisites are absent, publish status unproven with a null introduction revision. Do not invent a revision X.

## Freeze and reporting

Before scoring, FROZEN.json hashes the spec, family plan, cases, source articles, source facts, runner, preparation code, original checks, chunker, database helper and cached model weights. The runner verifies these hashes and refuses to overwrite FINAL.json. Final results are sealed before any independent reviewer sees them. A replay must use a different explicit output directory and cannot replace the final evidence. No product fix is permitted under this audit ID.

Publish FINAL.json, controlled and natural per-case traces, nuisance failures and temporal evidence. REPORT.md must give numerators/denominators, distinguish old results from C-16, list failures and constraints, and preserve the original lexical baseline win and Mac/tunnel dependency. A new result is not a sponsor/model/compliance guarantee.

The independent reviewer gets only this spec and the named evidence/README, with no builder conversation. It must refuse unsupported equivalence, accuracy, onset, scale, independence, calibration or hosting claims. Record reviewer provenance honestly: model agent, no human expert labels, no calibrated judge agreement, no invented independent model family. A label-free review may validate evidence consistency, not historical truth.
