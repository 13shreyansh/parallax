# Parallax — judge audit, second pass

Re-reviewed Sun 15 Nov 2026, 05:00 Helsinki, live at https://parallax-gamma-red.vercel.app, deployed commit `885da14` (the page's meta tag, the API health endpoint and local `HEAD` all report it). Headless Chromium via Playwright at 1440x900 and 390x844. Screenshots are in `mariadb/audit/shots-v2/`; the raw checklist results are in `shots-v2/checklist.json`.

**Verdict: 83/100, up from 73. It now reads as a first-place contender on the default path.** A judge who opens the link sees who it is for, one real finding with both quotes, and the MariaDB proof without clicking. The remaining gap to a safe first is scale: one theme, 22 articles, 20% of sources read.

All numbers are measured unless marked otherwise.

## What a judge sees now

**First 5 seconds.** "Three Wikipedias tell the Winter War differently. Parallax shows editors exactly where." Beside it, Swedish Wikipedia's 8,260 against its own cited source's 8,400, marked "Contradicted by its source". Below, one line: 6,747 claims and 20,963 source passages stored as MariaDB vectors, 31,461 revisions in system-versioned tables, every view shows its SQL. List rows appear in 1.5 s on desktop and 1.0 s on phone.

**After 60 seconds.** "Review Winter War, 50 findings" opens on a wrong date (29 vs 28 November), then numbers, then source and tone findings. The 40 "missing in a language" findings sit in one closed "Coverage gaps" group. "Show the SQL" shows the statement, the rows MariaDB returned and the live table definitions.

## Scores

| Criterion | First pass | Now | Why it moved |
|---|---|---|---|
| 1. MariaDB RAG / system-versioned tables | 8 | 9.5 | Proof is on the first screen; rows and schema are shown; Ask now generates a cited answer; history shows a before/after diff from the versioned table |
| 2. Implementation and scalability | 6.5 | 7 | Answers are stored in MariaDB; the dismissal hole is closed. Still one theme and 22 articles |
| 3. Usefulness for editors | 7.5 | 8.5 | Fixable errors come first; the Talk note links correctly; the edit that introduced a wording is shown |
| 4. Design and demo quality | 7 | 8.5 | Default path no longer dead-ends; counts agree; designed 404; the video is still to be recorded |
| 5. Originality | 7.5 | 8 | The before/after edit view and the cross-language answer are uncommon |
| **Total** | **73** | **83** | |

Bonus: both tracks are now combined visibly in two places (Ask, and "When this got in").

## The first-pass problems, one by one

| # | Problem | Status |
|---|---|---|
| 1 | Default ranking showed ten zero rows | Fixed. Default sort is findings; the distance sort also lists articles with findings first |
| 2 | Main button opened an empty page | Fixed. It opens Winter War; the empty article says "Show all 69 claims" and its SQL button works |
| 3 | MariaDB invisible on the first screen | Fixed. Proof strip with live counts, and "Show the SQL" on Home |
| 4 | Ask did not answer | Fixed. One or two sentences written only from retrieved rows, each statement linked to its passage, stored after first use. The brief's 2015 question now offers the article as of 31 Dec 2015 |
| 5 | Coverage gaps drowned real errors | Fixed. Wrong fact 4, Source 3, Tone 3 lead; 40 gaps are grouped and closed |
| 6 | Counts disagreed | Fixed. "50 findings" in the header, the tab and "1 of 50". The 317 is gone from the Method page |
| 7 | Headline contradicted an empty cell | Fixed in presentation. The cell now says "Covered in the Finnish article, but not as one matching sentence." The stored headline text is unchanged |
| 8 | Source check is thin | Not fixed; cannot be in this time. 20% of sources read, four source findings in the theme |
| 9 | Accuracy section undermined itself | Fixed. Leads with the blind review and the latest held-out run; 169 words, down from two dense paragraphs |
| 10 | SQL panel had no results | Fixed. Rows, shortened vector, no empty tabs, live schema with `vector(384)`, the vector index and `WITH SYSTEM VERSIONING` |
| 11 | Time travel showed no change | Fixed. Before/after sentences with changed words marked; wiki markup removed |
| 12 | Talk note linked to another site | Fixed. Links to the submitted URL. It still quotes Russian for some Swedish-gap findings |
| 13 | Chips worked backwards | Fixed |
| 14 | Unknown URLs returned JSON | Fixed. Designed page with a 404 status |
| 15 | Anyone could dismiss findings for everyone | Fixed. Dismissals stay in the reader's browser; the shared write endpoint refuses |
| 16–17 | Header overlap, layout jump | Fixed |
| 18 | Section titles clipped under the sticky header | Fixed for severity headings |
| 19 | Two tabs both labelled "Languages" | Not fixed |
| 20 | Generic explanation on some findings | Not fixed (stored text) |
| 21 | Duplicate history lines | Not fixed |
| 22 | "Not in its source" and "Contradicted" on one finding | Fixed |
| 23 | Shortcuts not discoverable | Not fixed |
| 24 | Rough "other close passages" | Not fixed; less visible now that an answer sits above them |
| 25 | Edge-state copy | Partly: unanswerable questions now say so plainly |
| 26 | Phone chips clipped, small links | Chips fixed; small inline links remain |
| 27 | No social preview | Fixed. Title, description, canonical and Open Graph tags with a 1200x630 image |
| 28 | "All claims" not virtualised | Not fixed |

## Re-review checklist results

Run on the deployed URL at both widths. All pass.

| # | Check | 1440 | 390 | Evidence |
|---|---|---|---|---|
| 1 | Home in under 2 s, findings first | Pass | Pass | 1,500 ms and 959 ms; findings column 50, 16, 8, 3, 1, 1, 1, 0, 0, 0 |
| 2 | First screen names the user, the problem and MariaDB | Pass | Pass | On phone the proof strip is one scroll down |
| 3 | Main button leads with a wrong fact or source error | Pass | Pass | First group "Wrong fact 4" |
| 4 | One count of findings | Pass | Pass | "50 findings", tab 50, "1 of 50" |
| 5 | A chip shows only that check | Pass | Pass | Wrong fact: 3 rows; again: 9 rows |
| 6 | First five headlines never credit an empty language | Pass | — | Checked on desktop |
| 7 | SQL on every page, rows shown, no empty tab | Pass | Pass | Home, article, empty article and Ask |
| 8 | Before/after diff, no markup | Pass | Pass | "stress" removed, "lie" added; 0 markup tokens in the 2015 view |
| 9 | Note links to the submitted URL | Pass | — | Clipboard read on desktop |
| 10 | Suggested questions and the brief's question | Pass | Pass | Three suggested questions and "When did the Winter War start?" give cited answers; the 2015 question gives the revision link |
| 11 | Method: current number first, short | Pass | Pass | 44 of 60, then 40 of 40; 169 words |
| 12 | Designed 404 | Pass | Pass | Status 404 |
| 13 | Clean console, no overflow, no overlapping headers | Pass | Pass | Only the 404 page's own status is logged |
| 14 | Ten-second test with a new reader | Not run | Not run | Needs a person |

## What is true about accuracy

- **Planted errors:** three frozen runs caught 32/40, 34/40 and 40/40, each with 0/40 false flags. The latest used a revised prompt for dropped sentences and larger number changes, so it is not a like-for-like gain. Every earlier miss was a dropped sentence.
- **Blind review:** 44 of 60 (73%) on the theme-wide sample is current. 53 of 60 (88%) was the earlier Winter War-only sample. STATUS.md had still quoted 53/60.
- **What is shown:** only findings the blind review individually confirmed; 80 today.

## What still costs points

1. **Scale.** One theme, 22 articles, and only 7 of them have findings. Nothing on screen shows the medium or large dataset. This is the biggest remaining gap on criterion 2.
2. **Source coverage.** "Book, not checked" is still everywhere. Say it aloud in the video as a task for editors rather than leaving a judge to notice.
3. **Answer wording.** Answers are grounded but sometimes clumsy. "When did the Winter War start?" cites "November 1939" from the Mannerheim Line article first, though a passage with 30 November is also cited. Pick demo questions from the ones verified above.
4. **A live dependency.** The first answer to a new question takes 2–4 s and needs the Gemini API. If it fails, the page shows passages only.
5. **The headline is fixed text.** It names the Winter War whatever the database holds. True today.

## For the video

Use these, all verified on the live site:
- Home: the 8,260 vs 8,400 finding, then "Show the SQL" and the Schema tab.
- Winter War: 29 vs 28 November; 3,000 vs 1,558 tanks.
- The tone finding: "continued to stress" became "continued to lie" on 16 Oct 2023, shown before and after.
- Ask: "Was Finland allied with Germany?" for a two-sentence answer citing the Finnish and Swedish articles.
- "Copy note for editors", then say it never edits Wikipedia.

Avoid the Language distance sort and the "other close passages" list.

## What I did not check

- Safari, Firefox and a real phone; everything above is headless Chromium.
- Behaviour with many judges at once. Stored answers help, but I ran no load test.
- The Codex end-to-end scripts (`scripts/video-e2e.mjs`, `scripts/review-race.mjs`). They test the shared "Not an issue" write, which I removed on purpose, and the old labels, so they will fail if re-run. I did not update them.
- The design detector reports 53 advisory notes, all font sizes, colours and radii outside the documented scale; 18 are in styles I added. No structural findings. I left them.
- The GitHub repository is 21 commits behind the live site (Codex's unpushed work and mine); I have not pushed.
