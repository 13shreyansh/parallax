# C-16 family audit

The delivered C-08 system is unchanged. This separate audit froze source families, cases, code and cached model weights before one final scoring run. [Specification](SPEC.md), [freeze manifest](FROZEN.json), [sealed result](final/FINAL.json), [output hashes](final/SEALED.json). No tuning followed the scores.

## What is new and what is not

Six topics in education institutions and railway sites were held out as whole topic families. Their FI/EN/SV versions stay together. Development uses four wartime topics. Both use the supplied S snapshot. Earlier article-level holdouts and confirmation topics are already seen and excluded from this new holdout. All sources are Wikipedia; families can share historical context. The split does not prove publisher independence or exclusion from pretrained model data.

Controlled translations and mutations were authored for this audit. They are not natural FI/SV quotations, human labels, or a calibrated translation gold set. Source-backed values are linked in [facts](facts.json) and [cases](cases.json). Each fact generates correlated language/nuisance variants. Reported fractions describe these constructions only.

## Translation-equivalent false-positive slice

A false positive here means a date/unit review flag on a constructed meaning-equivalent pair. Weak alignment is counted separately, not treated as a factual accusation. The measured-pair path computes actual model cosine similarity; it does not include retrieval or cited-source verification. The rule-only stress path fixes similarity at 1 and is not end-to-end.

| Path | Family | Equivalent pairs | False review flags | Planted errors | Caught |
|---|---|---:|---:|---:|---:|
| measured_pair_embedding | education_institutions | 30 | 2 | 18 | 1 |
| measured_pair_embedding | railway_sites | 27 | 0 | 18 | 4 |
| measured_pair_embedding | wartime_history | 18 | 0 | 12 | 4 |
| rule_only_similarity_1 | education_institutions | 30 | 2 | 18 | 6 |
| rule_only_similarity_1 | railway_sites | 27 | 0 | 18 | 9 |
| rule_only_similarity_1 | wartime_history | 18 | 0 | 12 | 6 |

**Held-out measured pairs: 2/57 false positives and 5/36 planted errors caught.** The rule-only stress caught 15/36 with the same 2/57 false positives. Low false positives coexist with poor error recall. The earlier 18/20 English-copy result remains historical evidence for a different, easier constructed task; it does not transfer to these cross-language pairs.

Both false positives involve the same approximate budget percentage written as `50,0 prosenttia` versus `50 percent` or `50 procent`. Numeric values are equal, but the unchanged checker compares numeric strings. Subject-name swaps are missed. Bare-year changes are also missed. Other changed full dates are missed when cross-language cosine similarity falls below the fixed 0.86 gate.

[All controlled traces](final/controlled-traces.json) retain text, language pair, source, family, construction label, measured cosine, verdict and baseline result. FINAL.json also splits by source type, language pair and nuisance. Its 70 failed path/case observations span two scoring paths over 123 correlated cases; they are not 70 independent factual claims.

## Natural retrieval by whole family

This uses real MariaDB native vectors for 1,711 audit passages in isolated `npov_c16_audit` tables. The product tables and corpus were not changed. Relevance is still only exact full-date overlap between original FI and EN passages in the same topic. That proxy can match different events and favors date numerals.

| Family | Scorable queries | Vector hit@3 | Lexical hit@3 |
|---|---:|---:|---:|
| wartime_history | 6 | 6/6 | 6/6 |
| education_institutions | 2 | 1/2 | 2/2 |
| railway_sites | 2 | 2/2 | 2/2 |

Held-out families together: vector **3/4**, lexical **4/4**. Only 10 of 742 Finnish query passages had a usable date-overlap reference; 732 are unscored, not successful. Four topics have zero scorable proxy queries: Q211855, Q1646874, Q277664 and Q18661302. Their retrieval quality is unmeasured by this proxy. Per-topic sample sizes are too small for general quality claims. The earlier deployed-corpus test also favored lexical, **8/9 versus vector 7/9**. No vector benchmark win is claimed. [Natural traces](final/natural-retrieval-traces.json).

## Nuisance checks and failures

- Combined display-title anonymization and reverse candidate insertion changed **25/742** top-three rankings. This test changes two factors together and cannot isolate which caused a change. Display titles are not embedded; this is retrieval/database plumbing, not semantic robustness to entity renaming. Of the 25, 24 change candidate membership and two change the first result. [Raw comparisons](final/metadata-nuisance-traces.json).
  The family split is wartime 25/383 changed rankings, education 0/221 and railway 0/138. These denominators concern query rankings, not translation accuracy.
- Meaning-preserving rephrases caused **0/24** review-decision flips per paired scoring path. These are equivalent controls with mostly no review flags, not a broad paraphrase robustness benchmark. [Rephrase traces](final/rephrase-traces.json).
- Neutral-clause reordering is split separately in FINAL.json. It is a controlled wording nuisance, not evidence of general document-order invariance.

After sealing, a read-only [exploratory diagnosis](post-seal-nuisance-diagnosis.json) inspected five failed rankings using an added ID sort key and an index-ignored query. Those query shapes agreed in that small sample. This changes multiple query conditions, so it does not establish a complete root cause or a validated fix. The 25 failures remain in the final audit. The product does not guarantee exact nearest-neighbor rank or invariant top-three output.

## Disagreement introduction remains unproven

`introduction_revision` is **null** for every inspected product topic. Real SQL shows long Finnish history but only a few recent English/Swedish revisions; at 2015 the required counterpart evidence is missing. Current date/unit leads are not established factual contradictions. No continuous before/after multilingual claim comparison or validated disagreement relation is available.

A revision changing text is not proof that it introduced a disagreement. A claim first observed in the available window is not proof of its first introduction. The system therefore does **not** display or claim "disagreement introduced at revision X". The existing temporal view remains useful for examining exact archived content. [Coverage and comparison evidence](final/temporal-onset.json).

## Freeze, reproduction and reviewer scope

```sh
.venv/bin/python scripts/c16_audit.py replay --out work/c16-replay
```

The runner verifies frozen inputs and cached weights and refuses to overwrite the final output. A replay requires the same local model/dependencies, an authorized MariaDB service and the delivered `npov` schema with its article/revision import for the temporal evidence; index build/traversal and hardware can produce different ranks. It is not a guarantee of bit-identical fresh database reconstruction. The sealed files preserve this observed final run.

The [independent model-agent review](REVIEW.md) received only the specification, allowlisted evidence and README, with no builder conversation. It passed scoped artifact consistency and verified hashes and fractions, while refusing to independently certify baseline-commit equivalence, actual model weights/embeddings or live SQL execution. [Provenance](reviewer-provenance.json) records this scope. A [citation clarification](CITATION_NOTES.md) locates the academy full-date paragraph without changing frozen evidence. It is not a human historian or calibrated translation judge. Source fact truth, broad translation quality, model training exclusions, general accuracy, novelty, compliance and durable hosting remain unsupported unless separate evidence exists.

## Runtime and remaining limits

The public site still relies on the build Mac and temporary tunnel for live SQL. Saved evidence remains readable offline. This audit adds no remote database hosting, Wikipedia edits, public video or final submission. Full S/M/L scale and human expert labels remain absent. New failures are published rather than hidden by changing thresholds.
