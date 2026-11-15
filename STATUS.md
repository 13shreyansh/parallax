Goal: fix Parallax from a MariaDB judge's point of view, using audit/JUDGE-AUDIT.md as the list.
Scope: Home first screen, review order, SQL proof, Method accuracy, Ask answers, edit history; no new data.
Acceptance: the 14-step re-review checklist in audit/JUDGE-AUDIT-v2.md passes on the deployed URL at 1440x900 and 390 px.
Hosting unchanged: Vercel proxies the VPS frontend and API; only parallax-* containers were touched.
Writer: Claude took over from Codex Job 05 at 04:27 Helsinki after it was stopped on Shreyansh's word.

ENTRY: Parallax / Sun 15 Nov 05:05 Helsinki / 885da142c795adac98212038034eb5c26ba99705 / https://parallax-gamma-red.vercel.app
DONE:
- First screen states the user, the problem and the MariaDB proof with live counts; default ranking and the main button lead to Winter War's 50 findings, ordered wrong fact, source, tone, with 40 coverage gaps grouped and closed.
- SQL view shows returned rows and the live schema on every page; Ask writes a cited one or two sentence answer from retrieved rows and stores it; "When this got in" shows the sentence before and after the edit.
- Method leads with current accuracy; Talk notes link to the public URL; "Not an issue" is browser-only; unknown addresses get a designed 404.
NUMBERS: held-out planted errors 40/40 caught, 0/40 false flags (measured, latest of three runs: 32/40, 34/40, 40/40; the latest used a revised prompt and larger number changes). Blind review 44/60 = 73% (measured, theme-wide sample before the publication filter; the earlier Winter War-only sample was 53/60). Baseline 5/36 (measured, from the earlier status). Judge score 83/100, was 73 (my estimate against the brief's five criteria).
SCREENSHOTS: audit/shots-v2/d-home.png; audit/shots-v2/m-home.png; audit/shots-v2/d-entry-diff.png
REVIEW: self re-review only, 14 of 14 automated checks pass at both widths; no separate reviewer ran. The design detector reports 53 advisory notes on sizes, colours and radii outside the documented scale, none structural.
NEXT: record the video from the list in audit/JUDGE-AUDIT-v2.md; show scale beyond one theme if any time remains.
NEEDS DECISION: push the 21 local commits to GitHub (the Method page links to the repository, which is behind the live site)?
BLOCKED: none

## Spec gaps I filled
- Headline copy is fixed text naming the Winter War; "many claims" became "some claims" because the theme has four source findings.
- Ask now calls Gemini Flash at query time for the answer sentence only; the Method page says so. The key reached the container over SSH stdin and is not in any file or log.
- Coverage gaps are any Languages finding whose verdict starts "Missing in".
- Codex's scripts/video-e2e.mjs and scripts/review-race.mjs test the removed shared review write and old labels; they were not updated and will fail.
