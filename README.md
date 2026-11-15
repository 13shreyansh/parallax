# Parallax

Live: https://parallax-gamma-red.vercel.app

A review desk for Wikipedia editors. Parallax compares claims in Finnish, Swedish and English with their own cited sources and with the other language versions. It flags passages for a person to review and prepares a neutral Talk-page note. It never edits Wikipedia.

The active theme contains 22 sponsor-linked topics on Finland in the Second World War. Winter War also has German and Russian comparison columns. Product findings come from real current Wikipedia revisions and fetched sources; planted errors are kept in an isolated evaluation database.

## How it works

- Sponsor S provides article/Wikidata links; M supplies Finnish history. Wikipedia APIs supply current cited wikitext and available revisions.
- Each claim keeps its section, revision and citation links. Readable cited pages are extracted, chunked, embedded with multilingual MiniLM and stored in native MariaDB VECTOR columns.
- MariaDB cosine retrieval selects source passages and cross-language claims. Gemini 3.8 Flash nominates candidates; Gemini 4 Argon confirms them against the actual source and peer articles. Literal evidence gates reject invented quotes.
- Unreachable URLs are retried through Internet Archive and Context.dev. Books and unreachable sources remain explicitly unchecked.
- Revision history lives in MariaDB system-versioned tables. Entry dates describe exact wording, with historical source support explicitly unknown.

## Hosting

The new `parallax` Vercel project routes the frontend and public API to the isolated VPS service at `https://parallax.72.61.22.106.sslip.io`. MariaDB 11.8 has networking disabled; the API connects through a private socket. Read and review-write accounts are separate. API writes use `/tmp`; persistent database data uses named volumes. The old `npov-radar` Vercel project remains untouched.

## Development

```sh
npm ci
npm run build
.venv/bin/python -m unittest discover -s tests
```

Pipeline entry points live in `pipeline/`; the hosted API is `service/app.py`; deployment files are in `deploy/`. Local data, model caches and credentials are ignored. Never place keys in source files or public assets. `DESIGN-DIRECTION.md` is the binding UI specification.

## Measurement

Three disjoint controlled held-out runs caught **32/40 (80%)**, **34/40 (85%)**, then **40/40 (100%)** planted errors, each with **0/40 false flags**. The third uses a coverage prompt developed only on Winter War copies and larger numeric perturbations. These are controlled passage tests, not full-article population accuracy; clean controls mostly do not measure multilingual false flags.

A blind gpt-6-astra review confirmed **44/60 (73.3%)** sampled flags from the then-published theme population. The public list was subsequently restricted to independently confirmed findings; 73.3% describes the pre-curation sample, not post-filter precision. It currently has 80 published flags, 50 on Winter War. See [the evaluation record](eval/parallax/EVALUATION.md) for frozen cases, prompt hashes, earlier measurements and limitations.

The browser acceptance test runs against the deployed URL at 1440×900 and 390×844, checks real source evidence, language fixes, temporal queries, clipboard equality and persisted editor reviews, then restores its own writes. Run `node scripts/video-e2e.mjs`. Screenshots are saved to `screenshots/parallax/` and `artifacts/e2e/`.

Wikipedia text is attributed and linked to its revision under CC BY-SA 4.0. Source excerpts retain their source links.
