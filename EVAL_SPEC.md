# Evaluation specification

The tool helps editors locate evidence worth reviewing. A semantic distance is not a bias score. Different audience emphasis is valid unless specific facts conflict. Retrieval and checking are separate steps.

Freeze article split before tuning: dev Q134949 Winter War, Q122100 Continuation War, Q211855 Finnish Civil War, Q185489 Simo Häyhä. Held-out topics will be selected from the supplied set before classification code is tuned and recorded in eval/split.json.

No human labels are available at start. Agent-authored annotations must be identified as such. Planted edits have synthetic ground truth, never human ground truth. Do not report calibrated model accuracy or real-world contradiction precision from these fixtures.

Compare a naive number-set mismatch baseline with a guarded entity/date check, and compare lexical retrieval with multilingual vector retrieval. Keep raw per-case outputs. Hold out entire articles, not sentences from the same articles. Include agreement, different context, missing evidence and formatting-only changes.

Success criteria: real MariaDB VEC_DISTANCE_COSINE queries retrieve exact source text and revision provenance; real FOR SYSTEM_TIME queries return the correct stored historical revision; planted date/number errors detected with fewer false flags on negative controls than naive mismatch baseline. Report recall, false-positive rate, sample sizes, query latency and known failures. Source support requires an exact accessible source excerpt; otherwise cannot verify. Never auto-edit Wikipedia.

Scale: inspect S, M and L schema/metadata and measure only the actual loaded subsets. Full-dataset scale is unproven until run. Do not claim starter benchmark numbers as ours.
