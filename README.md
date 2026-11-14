# Parallax

A review desk for Wikipedia editors. Parallax compares claims in Finnish, Swedish and English with their own cited sources and with the other language versions. It flags passages for a person to review and prepares a neutral Talk-page note. It never edits Wikipedia.

The active theme contains 22 sponsor-linked topics on Finland in the Second World War. Winter War also has German and Russian comparison columns. Product findings come from real current Wikipedia revisions and fetched sources; planted errors are kept in an isolated evaluation database.

## How it works

- Sponsor S provides article/Wikidata links; M supplies Finnish history. Wikipedia APIs supply current cited wikitext and available revisions.
- Each claim keeps its section, revision and citation links. Readable cited pages are extracted, chunked, embedded with multilingual MiniLM and stored in native MariaDB VECTOR columns.
- MariaDB cosine retrieval selects source passages and cross-language claims. Gemini 3.8 Flash nominates candidates; Gemini 4 Argon confirms them against the actual source and peer articles. Literal evidence gates reject invented quotes.
- Unreachable URLs are retried through Internet Archive and Context.dev. Books and unreachable sources remain explicitly unchecked.
- Revision history lives in MariaDB system-versioned tables. Entry dates describe exact wording, with historical source support explicitly unknown.

## Hosting

The new `parallax` Vercel project serves the frontend and a token-authenticated proxy to the isolated VPS API at `https://parallax.72.61.22.106.sslip.io`. MariaDB 11.8 has networking disabled; the API connects through a private socket. Read and review-write accounts are separate. API writes use `/tmp`; persistent database data uses named volumes. The old `npov-radar` Vercel project remains untouched.

## Development

```sh
npm ci
npm run build
.venv/bin/python -m unittest discover -s tests
```

Pipeline entry points live in `pipeline/`; the hosted API is `service/app.py`; deployment files are in `deploy/`. Local data, model caches and credentials are ignored. Never place keys in source files or public assets. `DESIGN-DIRECTION.md` is the binding UI specification.

## Measurement

The first frozen v4 held-out run caught 32 of 40 planted errors (80%), with 0 false flags on 40 clean controls. Date, number, loaded wording and unsupported-claim cases scored 8/8 each; dropped sentences scored 0/8. These are controlled real-passage tests, not full-article population accuracy. Blind precision on real findings is pending. See `eval/parallax/RESULTS.json` and `STATUS.md` for the current measured results and limitations.

Wikipedia text is attributed and linked to its revision under CC BY-SA 4.0. Source excerpts retain their source links.
