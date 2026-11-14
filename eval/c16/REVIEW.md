# C-16 independent evidence review

**Verdict: PASS for the consistency of the scoped C-16 evidence and its reported negative results.** This does not certify historical truth, translation equivalence, model independence or general product accuracy. No material numerical correction to the C-16 claims is required.

## Evidence checks

I read only the request, specification and allowlisted artifacts. I recomputed SHA-256 for all ten allowlisted frozen files and all six sealed outputs: every hash matches. FINAL.json correctly links the current FROZEN.json and detector hashes. Recorded selection, freeze, scoring and seal times are ordered consistently. Local manifests establish internal integrity, not an externally witnessed chronology.

I reapplied the unchanged checker to all 246 observations using their recorded similarities; verdicts, review decisions, weak-alignment flags, baseline decisions and pass flags all match. Both paths contain the same 123 cases. All 34 aggregate slices and the 70-entry failure list recompute exactly; the 70 failures concern 41 distinct cases across two paths.

| Family | Equivalent controls | False flags, either path | Planted errors | Measured caught | Rule-only caught |
|---|---:|---:|---:|---:|---:|
| Education institutions, held out | 30 | 2 | 18 | 1 | 6 |
| Railway sites, held out | 27 | 0 | 18 | 4 | 9 |
| Wartime history, development | 18 | 0 | 12 | 4 | 6 |

Thus held-out results are **2/57 false flags**, **5/36 planted errors caught** with recorded embeddings, and **15/36 caught** at similarity 1. The held-out name slice is 0/18 caught on both paths; changed years are 5/18 measured and 15/18 rule-only. All weak-alignment counts are zero; these are separately represented, not counted as factual accusations.

Source slices recompute: controlled translations have 0/72 false flags; numeric formatting has 2/3; mutations have 9/48 measured and 21/48 rule-only detections, including development. Across all topics, FI–EN, FI–SV and SV–EN have respectively 1/25, 1/25 and 0/25 equivalent-control false flags. Base, rephrase and neutral-clause reorder each have 0/24 false flags per path. These slice denominators overlap and must not be added as independent samples.

The declared development and held-out topic sets are disjoint; no held-out QID appears in the plan's previously-seen exclusion list. All ten topics have exactly FI/EN/SV source versions with consistent family membership. Controlled cases cover eight topics plus an additional percentage construction on one of them: eight facts each generate 15 correlated cases, and the percentage generates three. The plan's historical exclusion completeness and pre-reading selection procedure cannot be independently established from these artifacts alone.

I recreated the original chunker output from the sealed source articles: **1,711 passages, 742 Finnish queries**. Recomputing the exact date-set proxy yields exactly the ten recorded natural queries and reference sets. Lexical top-three lists and both hit flags match. Development is vector 6/6 versus lexical 6/6; education is 1/2 versus 2/2; railway is 2/2 versus 2/2. Held-out totals therefore favor lexical **4/4 over vector 3/4**. There are **732 unscored queries**. Q211855, Q1646874, Q277664 and Q18661302 have zero scorable queries; all three family slices are nonempty. This is a date-overlap proxy, not semantic relevance gold. The earlier saved retrieval summary likewise favors lexical 8/9 over vector 7/9; its raw retrieval traces are outside this allowlist, so that older total was checked against its saved summary only.

Metadata comparison covers every Finnish query: **25/742** rankings change, including **24 membership changes** and **two first-result changes**. All 25 occur in wartime history (25/383); education is 0/221 and railway 0/138. The paired rephrase records match their controlled traces, including recorded similarities: **0/24 decision flips per path**. These are narrow construction/plumbing checks. The five-case post-seal exploration does not replace the final failures or establish a causal explanation or validated repair.

## Source examples and refused judgments

All eight cited fact paragraphs occur in the named English source article with matching revision metadata. The academy's quoted paragraph supports only 1640; the full frozen English article separately states 26 March 1640. The Piikkiö source uses “May 26, 1979”; the constructed control rewrites it to a form the checker parses. This illustrates why these paired constructions cannot establish natural-text coverage.

The percentage source says “Close to 50%”; the constructions retain approximation and write 50,0 versus 50. Reapplying the checker reproduces the two false flags: its unit values are strings “50.0” and “50”, despite numerical equality. Measured similarities are about 0.943 and 0.962, above the gate. All 24 name mutations actually replace the subject name with Atlantis while preserving the date; these are real text mutations, but only synthetic construction labels. Matching dates often return aligned despite that semantic change. No human translation certification or historical adjudication is justified.

The nine temporal records total 12,944 revision rows. Every topic has only three EN and three SV revisions; all 2015 EN/SV counterparts are null. No bounded complete multilingual before/after claim comparison or established disagreement is supplied. **Introduction revision must remain null/unproven.** A text-changing revision alone cannot identify disagreement onset.

I refuse claims of human labels, calibrated judge agreement, publisher independence, exclusion from model training, general accuracy, full-scale quality, compliance, durable hosting or broad paraphrase/entity-renaming robustness. The measured pair test omits retrieval; the metadata test preserves passage text and embeddings. The old 18/20 English-copy result is a separate historical task, not validated by C-16 or by the allowlisted v1 results, which describe a different earlier run.

## Corrections and provenance limits

No change to sealed scores or raw traces is required. For citation precision, a future annotation should identify the academy's full-date paragraph; keep the sealed source reference unchanged. Keep the lexical win, low error recall, correlated constructions, unscored-query count and Mac/tunnel dependency visible.

The unchanged-baseline and no-post-score-tuning statements are consistent with the supplied records but are not independently proven against commit 7f98b50: baseline checkout/history is not allowlisted. I verified frozen code hashes, not the actual cached weight file, tokenizer/configuration, package installation, recorded embedding dot products or live MariaDB execution. The weight hash is recorded in the manifest; the weight file is outside the supplied artifact allowlist. The runner uses persistent audit tables with CREATE IF NOT EXISTS and INSERT IGNORE, so fresh table state is not certified by a row digest. These limits do not change the trace arithmetic; they limit execution/reproduction certification. The report appropriately preserves the temporary Mac/tunnel dependency; I did not recheck hosting or the UI.

Reviewer provenance: fresh model-agent consistency review with no builder conversation, browser, other chat history, human expert labels or calibrated translation judge. Exact runtime model identity is not exposed to this review; no independent-model-family claim is made. Only this REVIEW.md was written; product and sealed audit files were left unchanged.
