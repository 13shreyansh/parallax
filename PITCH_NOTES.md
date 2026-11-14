# Five-minute peer-review pitch

## 0:00–0:40 · The editor's job

The same history is written for different language audiences. An editor needs to distinguish a valid emphasis from a date or quantity that needs checking. The tool's job is to reduce reading effort while preserving the human's judgment. Show the first screen, choose Winter War, and read one related passage in each language.

## 0:40–1:40 · Evidence workflow

Show the exact revision links and alternative retrieved passages. Explain that "different emphasis" means a related passage was retrieved, not a factual-agreement verdict. Show the Finnish War source example. The Yle excerpt supports the start date only. Most source checks abstain. Prepare a review note and mark the passage reviewed locally. No posting or editing occurs.

## 1:40–2:30 · Why MariaDB matters

Open the SQL inspector and run the live vector query. Passage text, revision metadata and native 384-dimensional vectors sit in the same database. The query limits candidates by topic and language. The schema has a native vector index and native distance calculation. Do not promise exact nearest-neighbor ranking or invariance: the frozen C-16 combined rename/reorder check changed 25/742 top-three rankings.

Open revision history and time travel to 2015. The table is genuinely system-versioned. Archived revisions use real UTC timestamps, and missing periods are not bridged. We retain the text, not just a change count. This view does not prove when a discrepancy appeared, because complete cross-language historical alignment has not been built.

## 2:30–3:40 · Evaluation and known failure

Run the synthetic changed-day and country-name examples. State the labels came from controlled edits, not humans. Fresh article held-out: 18/20 errors found, 0/22 controls flagged; two name-swap misses. Initial held-out scores were viewed before v2, so a new article set was reserved. The ledger preserves both runs.

For retrieval, same-date overlap is only a weak proxy. Vector got 7/9 held-out targets; lexical got 8/9. No retrieval win is claimed. An independent archive metadata check passes 9/9 after fixing UTC handling. A 60-pair sheet is ready for an expert to label, but no human gold labels or calibrated model judges exist yet.

## 3:40–4:20 · Scale and deployment

S supplies the initial topics in three languages; live APIs refresh the chosen articles. M supplies Finnish histories. L has 568,416 rows; our actual bounded probe embeds and queries 1,000, not the whole dataset. 30 native L-probe queries were measured locally; those are not load-test or semantic-quality results. The app labels the limits.

Frontend is on Vercel. The read-only API currently reaches the isolated MariaDB on the build Mac through a temporary tunnel. The Mac must stay online for live queries. Saved SQL evidence remains inspectable. No Spread infrastructure or unrelated project was changed.

## 4:20–5:00 · What follows

The next useful milestone is a historian/editor annotating the 60 real pairs, then calibrating any contradiction or tone judge against those labels. Improve the observed retrieval misses before expanding the article set. Add cited-source fetching only with evidence and explicit abstention. Move the database to authorized durable hosting before wider use.

Close by returning to the editor's decision. The output is a reason to inspect an exact passage, not an automated verdict or edit.

Likely questions:

- Is this a bias score? No. Ranking is a disclosed heuristic using review count, then mean retrieved distance.
- Are the labels human? No. Synthetic construction labels and a small weak date-overlap retrieval proxy; the human sheet is blank.
- Does it find contradictions? It finds some date/unit review leads. It does not establish general factual contradiction or cite-source truth.
- What did you build beyond the starters? Claim-level cross-language retrieval, an editorial worklist, scoped source evidence, conservative checks and abstentions, review notes, the live synthetic error lab, and the combined revision workflow. The app was written during the event.

C-16 audit update: whole held-out education/railway families, measured paired tests caught 5/36 planted errors and falsely flagged 2/57 audit-authored equivalents. Held-out natural date proxy favored lexical 4/4 over vector 3/4. Introductory revision of disagreement remains unproven; never name a revision X. These new results do not turn the earlier English-copy 18/20 into cross-language accuracy.
