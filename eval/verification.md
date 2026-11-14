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
