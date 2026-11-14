# NPOV Radar status

Owner: Codex, chat 01a1daa1-c19b-7813-9387-27ad33f7da3c. C-08 build DONE. Public video recording and final competition submission remain outside this build delivery.

Repository: https://github.com/13shreyansh/npov-radar, public, created with existing gh authentication. Source and final evaluation, design and runtime documentation pushed.
Frontend: https://npov-radar.vercel.app, Vercel project npov-radar in 13shreyanshs-projects.

Built: 9 themes / 27 live article versions / 2,308 multilingual sentence vectors / 12,944 real system-versioned revisions. Native MariaDB 13.0.2. Read-only API runs locally on 8808 through a temporary cloudflared tunnel, configured as RADAR_API_ORIGIN in Vercel. SQL socket is not exposed. Mac uptime is a live-query dependency. No other project modified.

Evaluation: v2 fresh article held-out synthetic tests catch 18/20 edits, no false flags on 22 controls. Country name swaps are missed. The first held-out set was seen before v2, retained as already seen. Cross-language date-overlap retrieval proxy: dev 7/7 vector and lexical; held-out 7/9 vector vs 8/9 lexical, no claimed vector win. Temporal metadata checks 9/9 after UTC correction. L: 1,000 of 568,416 records in a bounded vector ingestion/query probe; full scale not tested. No human labels or calibrated LLM judges. Curated Yle excerpt supports one start-date claim only.

Chief IAB functional verification passed at 17:39 Helsinki: exact revision links, Yle source, fresh SQL query, 2015 archive, synthetic detection and known miss; mobile 390px no page overflow; keyboard focus visible. Current wording/font and the five UI fixes were recaptured in IAB. Independent reviewer scored all five fixes resolved, no visible regressions from that batch, disposition ship for those fixes. Demo/pitch notes and runtime handoff are complete. Live API still requires this Mac and tunnel. No human expert labels or public video were fabricated.

Browser constraint: this chat lacks IAB. Do not use personal Chrome/Safari/Edge or any external browser workaround. Necessary authorized service connectors and secret-safe CLI are allowed. Ask Chief via bridge for exact browser UI steps.

## C-16 scoped improvement task

C-08 build remains DONE. C-16 MariaDB audit is DONE for the scoped implementation and publication. Independent spec/evidence-only review passed artifact consistency; production data publication and ten existing deployment regressions pass. A light post-publication IAB copy check was requested from Chief but no new IAB outcome is claimed here. Fixed detector/model/thresholds and product corpus are preserved. Frozen whole-family held-out measured pairs: 2/57 equivalent controls flagged, 5/36 planted errors caught. Natural held-out date proxy: vector 3/4, lexical 4/4. Combined rename/reverse insertion changes 25/742 top-three rankings. Temporal introduction remains unproven. Details and sealed failures in eval/c16/. No forms or Discord actions.
