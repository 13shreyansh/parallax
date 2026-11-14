# Deployed workflow verification

Chief of Staff verified the deployed application through Codex's inbuilt browser on 14 November 2026 at 17:39 Helsinki. This is functional and layout verification, separate from evaluation accuracy. No personal browser, Wikipedia edit or competition submission was used.

- Winter War opened with FI/EN/SV evidence and exact revision links.
- Finnish War Introduction showed the exact Yle excerpt with "Supports start date only" and a scoped explanation.
- A fresh live MariaDB query returned three real English passage rows. One observed database time was 10.6 ms; that is not a latency distribution or end-to-end timing claim.
- Finnish War as of 2015-01-01 returned real revision 14331365 and original archive text.
- The planted day change was detected; the country-name swap visibly remained a known miss.
- At 390×844 mobile, document width was 383px with no document horizontal overflow. Horizontal article/passage rails and stacked evidence worked.
- Keyboard Tab from article search reached the first article button with a visible solid outline.

The initial screenshot session retained older "Different emphasis" / "Coverage gaps" wording and a static font asset. The final source uses "Related passages" / "Weak alignment" and a corrected self-hosted variable WOFF2. A fresh capture was requested before the finish review. Original functional evidence remains valid; no new accuracy claim follows from it.

Independent HTTP checks through the deployed Vercel proxy are in `deployed-http-checks.json`. They verify health, real SQL alignment, revision listing, point-in-time content, a deliberate history gap, and synthetic probes. Live API service depends on the build Mac and temporary tunnel. The saved evidence desk remains available when it disconnects.

The independent visual review requested five fixes: distinguish passage entries, reduce pre-evidence chrome, reveal selected queue position, enlarge exact-revision actions, and integrate the status with its heading. These were implemented in one batch. Post-fix desktop/mobile captures and the scoped reviewer verdict are recorded below. No backend or evaluation logic changed in this batch.

Final post-fix IAB captures show selected Winter War rank09, distinct English previews, more evidence in the opening desktop viewport, and integrated status/heading. Chief measured revision links at 12px/32px desktop and 13px/44px mobile, with no horizontal document overflow at 390px. The independent reviewer scored all five requested fixes resolved, no visible regressions from that batch, disposition `ship` for those five fixes only. The stale supplemental history image remains excluded from the typography verdict.
