# Parallax — judge audit

Audited Sun 15 Nov 2026, 02:05–02:40 UTC, live at https://parallax-gamma-red.vercel.app (deployed commit `c71b70c`, read from the page's meta tag). Headless Chromium via Playwright at 1440x900 and 390x844. Read-only: all non-GET requests were blocked, so nothing was written to the demo data. 86 screenshots are in `mariadb/audit/shots/` (`d-` desktop, `m-` phone).

**Verdict: 73/100. A strong top-five entry that loses first place in its first ten seconds.** The engine is real and matches what the MariaDB booth asked for almost word for word. But the default screen ranks ten articles that all show zero issues, the main button opens an empty page, and MariaDB is invisible until a small button two clicks deep.

All numbers below are measured unless marked otherwise.

## 1. First impression

**First 5 seconds.** First paint at 0.18 s, list rows at 0.87–1.41 s (three desktop loads), 0.84 s on phone. Fast. The headline "The 10 articles that most need an expert" and the paragraph under it tell me who it is for (editors) and what it does. That part works.

Then I read the table. Ten rows, and every row says `0 0 0 0 0` under Issues, Source, Languages, Tone, Fact. The number one article "that most needs an expert" is *Lapplandsender*, a radio station I have never heard of, with zero issues. My honest reaction: "it found nothing". Nothing on the screen says MariaDB, vector search or system-versioned tables. (`d-load-2000ms.png`)

**After 60 seconds.** I click the only primary button, "Open the top article". I get "No open flags on this article", a link reading "Show all 0 claims", and a disabled "Show the SQL" button (`d-article-top-lapplandsender.png`). If I am a judge with twenty entries to see, I may stop here.

If I instead notice the example card on the right (8,260 vs 8,400 Swedish volunteers) and click through to Winter War, the product is suddenly impressive: three languages side by side, a revision timeline, a note for the Talk page, and real SQL with `VEC_DISTANCE_COSINE` and `FOR SYSTEM_TIME AS OF`. The good product is there, one lucky click away from the default path.

**What confused me:**
- Why are the top ten all zeros?
- What is "language distance 55", and why should an editor care about it if there are no issues?
- "38 flagged claims", "50 open issues" and "1 of 50" on the same screen.
- "Book, not checked" under nearly every claim.
- Is "Ask in any language" a question-answering tool? It returns passages, never an answer.

## 2. Scores

| Criterion | Score | Weighted |
|---|---|---|
| 1. Use of MariaDB RAG / system-versioned tables | 8 / 10 | 16 |
| 2. Implementation and scalability | 6.5 / 10 | 13 |
| 3. Usefulness for readers or editors | 7.5 / 10 | 15 |
| 4. Design and demo quality | 7 / 10 | 14 |
| 5. Originality | 7.5 / 10 | 15 |
| **Total** | | **73 / 100** |
| Bonus (SVT, or both tracks) | Qualifies: both tracks are combined in one view | |

**1. MariaDB use — 8.** Both tracks are real and combined: sentence alignment and source retrieval run on `VEC_DISTANCE_COSINE`, and the time bar runs `FOR SYSTEM_TIME AS OF` over 31,461 stored revisions. The SQL panel shows the live query and its timing (2–5 ms for alignment and history, 63–308 ms for search). Points lost: the panel shows no result rows, no schema and no evidence of a vector index; the "Closest source passage" tab returns "0 rows" on the default flag; and nothing on the first screen mentions MariaDB at all.

**2. Implementation — 6.5.** Live database, sub-second pages, a held-out evaluation and an honest "Where it fails" list. But it holds 22 articles in one theme, "Theme" is a static label rather than a selector, only 20% of cited sources were read, and nothing shows the small, medium and large datasets the brief names. The stated precision is 73.3% on a 60-flag sample, and the accuracy table's first column reads "Languages: 0 of 8 planted errors caught".

**3. Usefulness — 7.5.** This is exactly the booth's ask: a ranked list for a theme, cross-language discrepancies, claims not in their source, loaded wording, wrong dates, and a copy-ready Talk page note in the target language with the AI never editing. Points lost: 40 of Winter War's 50 flags are "Missing in Swedish/Finnish/English", which editors treat as normal coverage difference, and the valuable findings (date, number, source and tone errors) are buried at positions 4, 13, 20, 22 and 23. Only 7 of the 22 articles have any flag.

**4. Design and demo — 7.** Calm, legible, professional; works on a phone with no page overflow. Points lost on the first-run path described above, no landing framing, and several rough edges listed below.

**5. Originality — 7.5.** Most teams will build a chat-with-Wikipedia box. A claim-level review desk with source check, cross-language check, revision provenance ("when this got in") and a Talk page note is a distinct product. Cross-language comparison itself was suggested in the brief, so it is not a surprise to the judges.

**Where it ranks.** In a typical strong field I would place it third to fifth as it stands: technically among the best, but a judge following the default path sees zeros and an empty page. **What makes it a clear first:** the first screen must show the ten most serious findings (not ten zeros), state the MariaDB use in one line, and the search box must give one grounded, cited sentence as an answer. All three are small changes on top of what exists.

## 3. Problems found

### Blockers

**1. Default ranking shows ten articles with zero issues.** Home, `d-load-2000ms.png`, `m-home.png`. The default sort is language distance; the top ten by distance all have 0 flags. A judge concludes the tool found nothing. *Fix:* default to "Number of issues" (Winter War 50, Continuation War 16, Mannerheim Cross 8). Better: rank by a blend, and never show an article with no findings above one with findings.

**2. "Open the top article" opens an empty page.** `d-article-top-lapplandsender.png`. Lapplandsender shows "No open flags", "Show all 0 claims" (the tab beside it says "All claims 69"), and "Show the SQL" is disabled. *Fix:* point the button at the top article by issues, fix the "0 claims" count, and keep the SQL button enabled.

**3. MariaDB is invisible on the first screen.** Home. No mention of MariaDB, vectors or versioned tables until "Show the SQL" inside an article. For a MariaDB-judged prize this costs most of criterion 1 for any judge who does not dig. *Fix:* a one-line proof strip on home ("6,747 claims as MariaDB vectors · 31,461 revisions in system-versioned tables · every view shows its SQL") and a "Show the SQL" button on the home list too.

**4. "Ask" does not answer.** `d-search-0-result.png`, `d-search-10.png` to `d-search-15.png`. The booth said the RAG track "moves the needle a lot". The search returns the closest stored passages with no answer sentence.
- "What did Wikipedia say about the Mannerheim Line in 2015, and what changed since?" (the brief's own example) returns "Nothing in these articles is close to that", although Mannerheim Line is in the database.
- "När slutade vinterkriget?" is one of the site's own suggested questions. The Finnish and Swedish rows shown are irrelevant; only the English row contains the answer.
- "Kuinka monta sotilasta kaatui talvisodassa?" returns a claim about parishes, and its close passages include a US Army text about Hitler's 1941 campaign.

*Fix:* add one generated sentence above the passages, built only from the retrieved rows, each clause linked to its revision, with "the versions disagree" stated when they do. Cache it. Replace the suggested questions with three that work well, and handle the "in 2015 … what changed" pattern by routing to the article's time view.

### Major

**5. Coverage gaps drown the real errors.** Winter War, `d-article-winterwar-2500ms.png`. 40 of 50 flags are "Missing in X", listed in article order. The first three a judge sees are all "Missing in Swedish". *Fix:* order flags by severity (Wrong fact, Source, Tone first), and collapse "Missing in X" into a single "Coverage gaps (40)" group that is closed by default.

**6. Counts disagree.** Same screen. "38 flagged claims", "50 open issues", chips summing to 50, "1 of 50". The method page says 80 open flags and also "317 published theme flags". *Fix:* one noun and one number everywhere, with one line explaining the 317 → 80 curation.

**7. The explanation contradicts the evidence.** `d-article-winterwar-2500ms.png`. The headline says "The English (and Finnish) articles detail Boris Yartsev's…" while the Finnish cell directly below says "No matching passage found in this version". Two different empty messages ("No matching passage found in this version" and "Not in the Swedish article") sit side by side with no explanation of the difference. *Fix:* show the Finnish sentence the model relied on, or drop "(and Finnish)"; explain the two states in a tooltip or use one message.

**8. The source check is thin.** Everywhere. "Book, not checked" appears under nearly every claim. The whole theme has four Source flags (three on Winter War, one on Lapland War). The booth named unsupported claims as a core goal. *Fix:* cannot be fixed in five hours; reframe it. Lead the demo with the three good Source findings, and change the label to "Cited to a book — needs a human with the book", which turns a gap into an editor task.

**9. The accuracy section undermines itself.** Method, `d-method-accuracy.png`. The first data column reads "Languages 0 of 8" and the total "32 of 40", followed by two dense paragraphs of caveats that even a careful reader cannot parse ("pre-curation population", "coverage clarification"). *Fix:* show the latest run first (40 of 40 caught, 0 of 40 false flags), then one plain sentence: "A blind review confirmed 44 of 60 random flags (73%); only reviewed flags are shown." Move the history of earlier runs behind "Read the evaluation record".

**10. The SQL panel is proof without results.** `d-article-sql.png`, `m-search-sql.png`. It shows a query and "3 rows · 3.23 ms" above a large empty box. The second tab says "0 rows" on the default flag. The search query prints several hundred floats. No schema, no index. *Fix:* render the returned rows (lang, distance, text) under the query; abbreviate the vector literal to `VEC_FromText('[…384 floats…]')`; add a "Schema" tab with the `CREATE TABLE … VECTOR(…) … WITH SYSTEM VERSIONING` statements; hide a tab that has no rows.

**11. Time travel shows the past but not the change.** `d-article-asof-2015.png`, `d-article-day-before.png`. Old revisions show raw wiki markup ("===Negotiations===", "assets.]]"). The side panel keeps describing today's flag while the page shows 2015, which needs a grey notice to explain. There is no before/after diff, so "what changed since" is never answered directly. *Fix:* strip markup from historical text; in "When this got in", show the sentence the day before and the day after with the changed words marked. That one diff is the SVT money shot.

**12. The Talk page note points at a different site.** Clipboard text from "Copy note for editors". It links to `parallax-13shreyanshs-projects.vercel.app`, not the submitted URL. For a "Missing in Swedish" flag it quotes English and Russian, while Russian is hidden in the default three-language view. *Fix:* use the canonical URL; quote the languages the flag is about.

**13. Filter chips work backwards.** Article toolbar, `d-article-note-source.png`. Clicking "Source 3" hides the Source flags (URL becomes `checks=lang,tone,fact`) instead of showing only them. A judge who clicks "Wrong fact" to see the wrong facts sees everything except them. *Fix:* click selects only that check; click again returns to all.

**14. Unknown URLs return raw JSON.** `d-404.png`. `/nonexistent`, `/robots.txt` and `/favicon.ico` return 403 with `{"error":"Access denied"}`. *Fix:* SPA fallback to a "Page not found — back to the list" screen.

**15. Anyone can dismiss flags on the public demo.** Method, "Where it fails". "Not an issue" needs no login. One curious judge or rival can empty the list before the next judge arrives. Not exercised in this audit. *Fix:* for judging, make dismissals per-browser (local) or auto-restore on a timer.

### Minor

16. Home table header: "Source" and "Languages" labels overlap at 1440 px (`d-load-2000ms.png`).
17. Home layout jumps left when the example card loads; the skeleton is centred, the content is not (`d-load-500ms.png` vs `d-load-2000ms.png`).
18. Section titles are half hidden under the sticky column header when scrolled (`d-flag-06-Languages.png`).
19. Flags with two findings show two tabs both labelled "Languages" (`d-flag-06-Languages.png`).
20. Some flags carry a generic explanation: "The English article includes this claim. It is not in the Swedish article."
21. History list shows "12 Feb 2021 wording changed" then "12 Feb 2021 wording added" for the same claim.
22. The home example is labelled both "Not in its source" and "Source: Contradicted".
23. Keyboard shortcuts `/`, `j`, `k`, `s` work but are not discoverable; arrow keys and `?` do nothing.
24. Search "Other close passages" start and end mid-word, include Markdown link debris, repeat the same passage twice, and show bare domains as titles.
25. Edge states: `?theme=foo` says "The 0 articles in this theme, ranked"; a future date shows a bare "Try again"; an empty question says "Your question was not saved".
26. Phone: the check chips row is clipped at "Wrong fac…" (`m-article.png`); several links are 16–20 px tall, under the 44 px touch floor.
27. No social preview image or description tags; a shared link will be bare.
28. "All claims" renders about 14,700 DOM nodes on a 280,000 px page with no virtualisation. Fine now; it will not scale to the large dataset.

No console errors or page overflow were found on the normal paths at either width.

## 4. Can a judge see the MariaDB use?

**Yes if they look, no if they don't.** What exists is convincing: real `VEC_DISTANCE_COSINE` self-join alignment, a `source_chunk` vector retrieval, `FOR SYSTEM_TIME AS OF TIMESTAMP '…'` across five language tables, each with a measured time and a copy button. It is the best kind of proof because it is the actual query behind the view.

But it sits behind one outlined button on the article toolbar, is disabled on the article the main CTA opens, shows no rows, and is absent from home. A judge on the default path sees zero MariaDB. The method page explains it in prose but shows no SQL. Bring the proof to the first screen and show the returned rows, and criterion 1 goes from 8 to 9.5.

## 5. Top 10 improvements, ranked by points per hour

Time estimates are my guesses.

| # | Change | Time | Fixes |
|---|---|---|---|
| 1 | Default sort to issues; "Open the top article" opens Winter War; fix "Show all 0 claims" | 15 min | 1, 2 |
| 2 | Order flags by severity; collapse "Missing in X" into one closed group | 45 min | 5 |
| 3 | Home hero: one-line problem, one-line MariaDB proof strip, CTA (outline below) | 45 min | 3 |
| 4 | SQL panel: show result rows, shorten the vector literal, hide empty tabs, enable everywhere, add to home | 60 min | 10 |
| 5 | Ask: one grounded answer sentence with citations above the passages; three suggested questions that work | 60–90 min | 4 |
| 6 | Method: latest accuracy first, one plain sentence, cut the caveat paragraphs | 20 min | 9 |
| 7 | One count everywhere; fix the "(and Finnish)" contradiction; chips select instead of hide | 40 min | 6, 7, 13 |
| 8 | "When this got in": before/after sentence diff; strip wiki markup from old revisions | 45 min | 11 |
| 9 | Canonical URL in the Talk note; 404 page; header overlap; layout jump | 30 min | 12, 14, 16, 17 |
| 10 | Protect the demo from public dismissals during judging | 15 min | 15 |

Items 1–4 are about three hours and move the score the most. If time runs short, do 1, 3, 2, 4 in that order and put item 5's effort into the video instead.

### Proposed first screen (keep it one screen, above the list, not a separate marketing page)

- **Headline:** "Three Wikipedias tell the Winter War differently. Parallax shows editors exactly where."
- **Problem, one sentence:** "The Finnish, Swedish and English articles disagree on dates, numbers and tone, and many claims are not in the source they cite. No editor can read all three."
- **Proof, one live finding:** the existing card — Swedish Wikipedia says 8,260; its own cited source says 8,400 — with both quotes.
- **MariaDB strip:** "6,747 claims stored as MariaDB vectors · 31,461 revisions in system-versioned tables · every view shows its SQL".
- **Promise:** "It never edits Wikipedia. It flags, shows the evidence, and writes the Talk page note."
- **CTA:** "Review Winter War — 50 findings", with a secondary "Show the SQL".
- Below: the ranked list, sorted by issues.

### The 2:00 video

- **0:00–0:15 Problem.** Same event, three Wikipedias, three stories. Show 28 vs 29 November side by side.
- **0:15–0:35 The list.** "For a theme, the ten articles an expert should fix first" — the booth's exact words. Click Winter War.
- **0:35–1:05 Three findings, ten seconds each.** A wrong fact (3,000 vs 1,558 tanks), a source contradiction (8,260 vs 8,400), loaded wording ("continued to lie") with the neutral rewrite.
- **1:05–1:25 Time travel.** "When did this get in?" Click the marker, show the day before, open the SQL: `FOR SYSTEM_TIME AS OF`.
- **1:25–1:40 Vectors.** Show the `VEC_DISTANCE_COSINE` query and its rows; switch on German and Russian.
- **1:40–1:52 The editor's action.** Copy the note, show it in Swedish, "AI never edits".
- **1:52–2:00 Close.** Numbers and the URL. Say "MariaDB" aloud at least three times in the video.

Do not show the default distance sort, Lapplandsender, the search box (unless item 5 ships) or the accuracy table as it stands.

## 6. How to review it after fixes

Run at 1440x900 and 390 px on the deployed URL, in a fresh private window.

1. Home shows real content in under 2 s, and no row in the top ten shows all zeros.
2. Without scrolling, the first screen names the user, the problem and MariaDB.
3. The main button opens an article whose first visible flag is a wrong fact or source error, not "Missing in…".
4. On that article, every count of flags uses one number.
5. Clicking a check chip shows only that check.
6. Read the first five flags: the headline never names a language whose cell is empty.
7. "Show the SQL" is enabled on every page, shows returned rows, and no tab says "0 rows".
8. "Show the day before it entered" shows clean text with the changed words marked, and no `===` or `]]`.
9. "Copy note for editors" pastes a note that links to the submitted URL.
10. Ask the three suggested questions plus "When did the Winter War start?" and the brief's "what did Wikipedia say … in 2015, and what changed since?". Each gives a cited answer or a useful redirect.
11. Method page: the first accuracy number a reader sees is the best current one, and the section reads in under 20 seconds.
12. `/nonexistent` shows a designed page, not JSON.
13. Console is clean; no horizontal scroll at 390 px; no overlapping header labels at 1440 px.
14. Hand the URL to someone who has never seen it. After 10 seconds, ask what it does and which database it uses.

## What I did not check

- "Not an issue" and the notes-copied counter, because writes were blocked to keep the demo data clean.
- Phone language tabs and the phone date picker while the flag sheet is open; my taps there were intercepted by the sheet, so that path is unverified rather than known broken.
- Whether Escape closes the SQL panel after opening it with the `s` key; it closed when opened by click.
- The content of the linked GitHub evaluation record (the link returns 200).
- All 22 articles; I opened Winter War, Continuation War, Mannerheim Cross, Driftwood theory and Lapplandsender.
