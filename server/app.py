"""Read-only public query API. No arbitrary SQL, URLs, writes, or Wikipedia edits."""

import json, time, datetime, os, re, pathlib
from flask import Flask, request, jsonify
from server.db import connect, ALIGN_SQL, HISTORY_SQL, ASOF_SQL, ROOT

app = Flask(__name__)
snapshot = json.load(open(ROOT / "public/snapshot.json"))
TOPICS = {a["qid"]: a for a in snapshot["articles"]}


def clean(row):
    return {
        k: (v.isoformat(sep=" ") if isinstance(v, datetime.datetime) else v)
        for k, v in row.items()
    }


@app.after_request
def headers(r):
    r.headers["Cache-Control"] = "no-store"
    r.headers["X-Content-Type-Options"] = "nosniff"
    return r


@app.get("/health")
def health():
    try:
        with connect() as con:
            with con.cursor() as c:
                c.execute("SELECT VERSION() AS version")
                v = c.fetchone()["version"]
        return jsonify(
            ok=True,
            database=v,
            read_only_api=True,
            backend="MariaDB on build Mac through temporary tunnel",
        )
    except Exception:
        return jsonify(ok=False, error="The live database is unavailable."), 503


@app.get("/align")
def align():
    pid = request.args.get("id", "")
    lang = request.args.get("lang", "en")
    if lang not in ["en", "sv", "fi"] or not re.fullmatch(r"(fi|sv|en)-\d+-\d+", pid):
        return jsonify(error="Choose a stored passage and language."), 400
    with connect() as con:
        with con.cursor() as c:
            c.execute("SET SESSION max_statement_time=3")
            c.execute(
                "SELECT qid,VEC_ToText(embedding) AS embedding_json FROM passage WHERE id=%s",
                (pid,),
            )
            p = c.fetchone()
            if not p:
                return jsonify(error="Stored passage not found."), 404
            t = time.perf_counter()
            c.execute(ALIGN_SQL, (p["embedding_json"], p["qid"], lang))
            rows = c.fetchall()
            elapsed = (time.perf_counter() - t) * 1000
            c.execute("SELECT VERSION() AS v")
            v = c.fetchone()["v"]
    return jsonify(
        rows=rows,
        elapsed_ms=elapsed,
        database=v,
        sql=ALIGN_SQL,
        parameters={"passage_id": pid, "qid": p["qid"], "language": lang},
    )


def topic_version():
    a = TOPICS.get(request.args.get("qid"))
    lang = request.args.get("lang", "fi")
    if not a or lang not in ["fi", "en", "sv"]:
        return None
    return next(v for v in a["versions"] if v["lang"] == lang)


@app.get("/history")
def history():
    v = topic_version()
    if not v:
        return jsonify(error="Choose a stored topic and language."), 400
    with connect() as con:
        with con.cursor() as c:
            c.execute("SET SESSION max_statement_time=3")
            t = time.perf_counter()
            c.execute(HISTORY_SQL, (v["lang"], v["page_id"]))
            rows = c.fetchall()
            elapsed = (time.perf_counter() - t) * 1000
            c.execute(
                "SELECT COUNT(*) AS n FROM revision FOR SYSTEM_TIME ALL WHERE lang=%s AND page_id=%s",
                (v["lang"], v["page_id"]),
            )
            n = c.fetchone()["n"]
    return jsonify(
        rows=[clean(r) for r in rows], total=n, elapsed_ms=elapsed, sql=HISTORY_SQL
    )


@app.get("/asof")
def asof():
    v = topic_version()
    date = request.args.get("date", "")
    if not v:
        return jsonify(error="Choose a stored topic and language."), 400
    try:
        d = datetime.date.fromisoformat(date)
        assert datetime.date(2002, 1, 1) <= d <= datetime.date.today()
    except Exception:
        return jsonify(error="Choose a valid date from 2002 through today."), 400
    with connect() as con:
        with con.cursor() as c:
            c.execute("SET time_zone='+00:00'")
            c.execute("SET SESSION max_statement_time=3")
            t = time.perf_counter()
            c.execute(ASOF_SQL, (date + " 00:00:00", v["lang"], v["page_id"]))
            row = c.fetchone()
            elapsed = (time.perf_counter() - t) * 1000
    return jsonify(
        row=clean(row) if row else None,
        elapsed_ms=elapsed,
        sql=ASOF_SQL,
        as_of=date + " 00:00:00 UTC",
    )


@app.get("/probe")
def probe():
    # Deliberate mutations in an isolated response. Nothing is written to any table.
    from server.checks import check

    mutation = request.args.get("mutation", "day")
    if mutation not in ["day", "year", "name", "none"]:
        return jsonify(error="Unknown planted mutation."), 400
    with connect() as con:
        with con.cursor() as c:
            c.execute(
                "SELECT id,qid,VEC_ToText(embedding) AS embedding_json FROM passage WHERE qid='Q134949' AND lang='fi' ORDER BY ordinal LIMIT 1"
            )
            p = c.fetchone()
            c.execute(ALIGN_SQL, (p["embedding_json"], p["qid"], "en"))
            r = c.fetchone()
    original = r["text"]
    changed = original
    if mutation in ["day", "year"]:
        m = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b", original)
        if m:
            a, b = m.span(1 if mutation == "day" else 3)
            n = int(original[a:b])
            changed = (
                original[:a]
                + str(n + 1 if mutation == "year" or n < 27 else n - 1)
                + original[b:]
            )
    elif mutation == "name":
        changed = original.replace("Finland", "Sweden", 1)
    verdict = check(original, changed, 1.0)
    return jsonify(
        synthetic=True,
        mutation=mutation,
        original=original,
        changed=changed,
        changed_anything=changed != original,
        check=verdict,
        detected=verdict["kind"] in ["date-review", "numeric-review"],
        rev_id=r["rev_id"],
        lang="en",
        sql=ALIGN_SQL,
        scope="Rule-only comparison of a retrieved original against its deliberately altered copy; similarity fixed at 1. No Wikipedia edit or database write.",
    )


@app.errorhandler(Exception)
def failure(e):
    app.logger.error("Query failed: %s", type(e).__name__)
    return jsonify(
        error="The live query failed. Saved evidence is still available. Retry after the database reconnects."
    ), 503


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8808)), threads=4)
