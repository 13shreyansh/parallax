# Deployed taste gate

Served code: ba39c49307811b0b900edcd3e636aefaca72c87a. Screenshots below are in screenshots/parallax/. Every capture waits for actual content, fonts and settled layout. Public test writes are restored.

| Item | Result | Evidence |
|---|---|---|
|1 Professional product|Yes|01-home-distance-desktop.png|
|2 Real working video features|Yes|05-article-source-contradicted-desktop.png;08b-language-supporting-fix-desktop.png|
|3 Ordinary workspace entry|Yes, binding Parallax spec uses a public Wikipedia workspace directly, without an account selector|01-home-distance-desktop.png|
|4 Working controls/navigation|Yes|13-article-sql-desktop.png;15-article-dismissed-desktop.png; video-results.json|
|5 Real numbers|Yes|20-method-desktop.png; hosted.json contains direct SQL/API comparison|
|6 Binding screen design|Yes, with documented scope and loading-capture overrides|01-home-distance-desktop.png;24-article-sheet-phone.png|
|7 One primary action|Yes in actionable states; prescribed empty, dismissed, inline reason and closed five-column states have none|07-article-copied-desktop.png;15-article-dismissed-desktop.png;17-article-empty-rail-desktop.png|
|8 Plain editor language|Yes|05b-article-not-in-source-desktop.png;25-ask-phone.png|
|9 Five-second purpose|Yes: Wikipedia, Finnish/Swedish/English, source, editor and never edits appear above fold|01-home-distance-desktop.png|
|10 Calm layout|Yes|04-article-default-desktop.png|
|11 No default decorative styling|Yes|01-home-distance-desktop.png;20-method-desktop.png|
|12 Browser surfaces/no overflow|Yes at1440×900 and390×844|22-home-phone.png;23-article-phone.png|
|13 Complete deployed video flow|Yes, both widths, zero console errors|artifacts/e2e/video-results.json;07-article-copied-desktop.png|
|14 Visible evidence|Yes|05-article-source-contradicted-desktop.png;24b-source-passage-phone.png;27b-language-supporting-fix-phone.png|
|15 Responsive, settled flow|Yes; verified date queries3.5–8.83ms warm; reduced motion reaches end state immediately|10-article-past-desktop.png;data.json;extra-ui.json|
|Fresh data after tests|Yes:0 dismissals and0 copied-note counters after scoped cleanup|hosted.json;video-results.json|
|No visible internals|Yes; SQL only in its explicit drawer|13-article-sql-desktop.png;25-ask-phone.png|
|Loaded screenshots|Yes; loading screenshot03 intentionally omitted under the later loaded-content-only instruction|all listed PNGs|
|Mac independence|Yes; local API stopped, deployed VPS continues serving|hosted.json;01-home-distance-desktop.png|

Read receipts: artifacts/review/astra-final-read.json, artifacts/verification/review-race.json, fonts.json and contrast.json. Source Serif4 and Commissioner are verified custom web fonts; no platform fallback rendered the tested Russian quotation or interface text. Greyscale check:04b-article-greyscale-desktop.png.
