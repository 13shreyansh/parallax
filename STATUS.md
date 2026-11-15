PARALLAX / 15 Nov 2026 08:45 Helsinki / CRACI feature branch / https://parallax-gamma-red.vercel.app
DONE:
- Added CRACI workflow for the existing build and regressions, plus pinned clean-environment dependencies.
- Verified an actual passing CRACI run and a deliberately failing unmerged regression control.
- Preserved the live application; this change affects source dependencies and CI only.
NUMBERS: dev measured 40 Python and 7 JavaScript tests passed; held-out not rerun; baseline measured application runtime unchanged.
SCREENSHOTS: pending final CI captures.
REVIEW: independent 6 Astra reran clean Python tests and build; final source/CI receipt closure pending.
NEXT: complete review and fast-forward the reviewed branch after its final CI run.
NEEDS DECISION: none
BLOCKED: none for implementation; final review pending.
