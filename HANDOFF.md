# NPOV Radar handoff

Owner: Codex, C-08. Chat 01a1daa1-c19b-7813-9387-27ad33f7da3c.

Live: https://npov-radar.vercel.app
Public repository: https://github.com/13shreyansh/npov-radar
Workspace: /Users/shreyansh/Documents/ChatGPT/Junction/mariadb
Vercel project: npov-radar, team 13shreyanshs-projects.

## Current runtime

MariaDB 13.0.2 runs from work/runtime/mariadb/13.0.2_1, data in work/db, socket work/mariadb.sock. Only Unix socket access; no database TCP port exposed. The local OS user authenticates through the socket. No project password was created.

The read-only API is `python -m server.app`, bound to 127.0.0.1:8808 with waitress. Cloudflared exposes that HTTP API via a temporary quick tunnel. Its current URL is in work/tunnel.log and Vercel RADAR_API_ORIGIN. The URL is public and contains no credential. Never point RADAR_API_ORIGIN to MariaDB's SQL port.

All three processes must remain running, and the Mac must remain awake and connected, for live queries. This is a hackathon hosting limitation. There is no durable remote MariaDB hosting provisioned. No Spread VPS or other project's infrastructure was changed.

## Restart only this project's processes

Check work/mariadb.pid and whether the socket exists before starting a duplicate database. Use `scripts/start-db.sh` from this workspace if it stopped. Then:

```sh
.venv/bin/python -m server.app
cloudflared tunnel --url http://127.0.0.1:8808 --no-autoupdate
```

Use the installed cloudflared at /Users/shreyansh/.local/bin/cloudflared if it is not on PATH. Keep logs under work/. A new quick tunnel gets a new URL. Update only this Vercel project's RADAR_API_ORIGIN using existing authorized credentials, then redeploy. Do not write tokens in bridge files or logs. Do not modify any other project's processes.

Health: https://npov-radar.vercel.app/api/radar?mode=health
Meaningful checks: align id=fi-1256-0 lang=en; history qid=Q134949 lang=fi; asof date=2015-01-01 should return revision 14547217; asof 2026-10-02 should return no row because archive coverage ended and live coverage has not begun. The planted day probe detects the error; the name probe intentionally demonstrates a miss.

Saved passage evidence, source metadata, evaluation and revision listings remain available if the backend disconnects. Live time travel and probes then show an unavailable message. No stored synthetic revision is presented as Wikipedia.

## Evidence and limits

9 topics, 27 live article versions, 2,308 passage vectors, 12,944 genuine revision rows. S/M/L downloaded; M/L checksums verified. L probe loads only 1,000 of 568,416 rows.

Fresh held-out synthetic rules: 18/20 planted edits caught, 0/22 controls flagged. Name swaps missed. Initial held-out was seen before v2, so a fresh article set was reserved. Similarity fixed at 1 isolates rules. This is not measured real-world contradiction accuracy or human labeling.

Cross-language date-overlap proxy: vector 7/9 held-out, lexical 8/9. No vector win claimed. Temporal selected archive checks 9/9 after UTC fix. The app has no calibrated LLM judge and no whole-article LLM baseline. `eval/annotation-queue.csv` has blank human-label fields on purpose.

No confirmed factual contradiction is claimed in the current real sample. The numerical detector's observed scope false lead was suppressed. "Weak alignment" and "Related passages" avoid unsupported omission/emphasis labels. The curated Yle check supports only the Finnish War start date. All other source checks mostly abstain.

## Delivery and next work

README.md describes the actual system and reproduction. eval/LEDGER.md and traces preserve results. DEMO_SCRIPT.md is a 1:55 recording script. PITCH_NOTES.md covers five minutes. Code is MIT; Wikipedia text/embeddings retain CC BY-SA 4.0; other source copyright is preserved.

No video was recorded or published and no final entry form was submitted. Shreyansh still needs the public video and final competition submission. Human expert labeling and durable database hosting remain future work. Deadline is Sunday 15 November 2026 10:00 Helsinki; build target was feature complete by 04:00 and polished by 08:00.

Browser instruction: use only Codex IAB for web/account UI. IAB is unavailable in this project chat. Chief of Staff has working IAB and can handle the exact requested browser checks. Necessary authorized connectors and secret-safe CLI work are allowed. Do not use personal Chrome, Safari, Edge, or an external browser workaround.

An idle-sleep assertion is attached to the current API process using `caffeinate -i -w <api-pid>`, without changing power settings. Its PID is in work/awake.pid. It ends when that API process ends. It does not keep a closed laptop online or guarantee network availability.
