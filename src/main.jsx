import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Search,
  ArrowUpRight,
  ChevronRight,
  Database,
  History,
  Check,
  Copy,
  ArrowLeft,
  Filter,
  BookOpen,
  Radio,
  Info,
  RefreshCw,
  CheckCheck,
  ExternalLink,
} from "lucide-react";
import "./style.css";
const formatDate = (s) =>
  new Date(s).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
const labels = {
  "numeric-review": "Check the numbers",
  "date-review": "Check the dates",
  coverage: "Weak alignment",
  emphasis: "Related passages",
  aligned: "Matching dates",
};
const revisionURL = (lang, rev) =>
  `https://${lang}.wikipedia.org/w/index.php?oldid=${rev}`;
function App() {
  const [data, setData] = useState(null),
    [error, setError] = useState(""),
    [topic, setTopic] = useState("Q134949"),
    [selected, setSelected] = useState(""),
    [search, setSearch] = useState(""),
    [filter, setFilter] = useState("all"),
    [view, setView] = useState("worklist"),
    [live, setLive] = useState("checking"),
    [query, setQuery] = useState(null),
    [busy, setBusy] = useState(""),
    [history, setHistory] = useState(null),
    [asof, setAsof] = useState("2015-01-01"),
    [point, setPoint] = useState(null),
    [probe, setProbe] = useState(null),
    [note, setNote] = useState(false),
    [copied, setCopied] = useState(false),
    [evals, setEvals] = useState(null),
    [reviewed, setReviewed] = useState(() => {
      try {
        return JSON.parse(localStorage.getItem("npov-reviewed") || "[]");
      } catch {
        return [];
      }
    });
  useEffect(() => {
    fetch("/snapshot.json")
      .then((r) => {
        if (!r.ok)
          throw Error(
            "The saved worklist could not load. Reload to try again.",
          );
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message));
    fetch("/evaluation.json")
      .then((r) => (r.ok ? r.json() : null))
      .then(setEvals)
      .catch(() => {});
    fetch("/api/radar?mode=health", { signal: AbortSignal.timeout(10000) })
      .then((r) => {
        if (!r.ok) throw Error();
        return r.json();
      })
      .then((j) => setLive(j.ok ? "connected" : "snapshot"))
      .catch(() => setLive("snapshot"));
  }, []);
  useEffect(() => {
    localStorage.setItem("npov-reviewed", JSON.stringify(reviewed));
  }, [reviewed]);
  if (error)
    return (
      <main className="load">
        <h1>Worklist unavailable</h1>
        <p role="alert">{error}</p>
        <button onClick={() => location.reload()}>Reload worklist</button>
      </main>
    );
  if (!data)
    return (
      <main className="load">
        <div className="radar-logo" />
        <h1>Opening the evidence desk</h1>
        <p>Loading the saved MariaDB query results…</p>
      </main>
    );
  const article =
    data.articles.find((a) => a.qid === topic) || data.articles[0];
  const list = data.articles.filter((a) =>
    (a.title + " " + a.fi_title).toLowerCase().includes(search.toLowerCase()),
  );
  const visible = article.findings.filter(
    (f) =>
      filter === "all" ||
      (filter === "review"
        ? f.flags.some((x) => ["date-review", "numeric-review"].includes(x))
        : filter === "coverage"
          ? f.flags.includes("coverage")
          : f.matches.en?.check.kind === "aligned" ||
            f.matches.sv?.check.kind === "aligned"),
  );
  const finding = visible.find((f) => f.id === selected) || visible[0];
  const selectArticle = (a) => {
    setTopic(a.qid);
    setSelected("");
    setNote(false);
    setQuery(null);
    setHistory(null);
    setPoint(null);
    setFilter("all");
  };
  async function run(mode, params = {}) {
    setBusy(mode);
    try {
      const r = await fetch(
        "/api/radar?" +
          new URLSearchParams({ mode, qid: article.qid, ...params }),
        { signal: AbortSignal.timeout(15000) },
      );
      const j = await r.json();
      if (!r.ok)
        throw Error(
          j.error ||
            "The live database is unavailable. Saved evidence is still available.",
        );
      setLive("connected");
      if (mode === "align") setQuery(j);
      if (mode === "history") {
        setHistory(j);
        setTimeout(
          () =>
            document
              .querySelector(".history-panel")
              ?.scrollIntoView({ behavior: "smooth", block: "start" }),
          50,
        );
      }
      if (mode === "asof") setPoint(j);
      if (mode === "probe") setProbe(j);
    } catch (e) {
      const j = { error: e.message };
      if (mode === "align") setQuery(j);
      if (mode === "history") {
        try {
          const saved = await fetch("/history-snapshot.json").then((r) =>
            r.json(),
          );
          setHistory({ ...saved[article.qid], offline: true });
        } catch {
          setHistory(j);
        }
      }
      if (mode === "asof") setPoint(j);
      if (mode === "probe") setProbe(j);
      setLive("snapshot");
    } finally {
      setBusy("");
    }
  }
  const reviewKind = (f) =>
    f.flags.includes("date-review")
      ? "date-review"
      : f.flags.includes("numeric-review")
        ? "numeric-review"
        : f.flags.includes("coverage")
          ? "coverage"
          : Object.values(f.matches).some((m) => m.check.kind === "aligned")
            ? "aligned"
            : "emphasis";
  const noteText = finding
    ? `Review request: ${article.title}\n\nFinnish revision ${finding.fi.rev_id}: ${finding.fi.text}\n\n${Object.entries(
        finding.matches,
      )
        .map(
          ([lang, m]) =>
            `${lang.toUpperCase()} revision ${m.rev_id}: ${m.text}\n${m.check.reason}`,
        )
        .join(
          "\n\n",
        )}\n\nPlease check the cited sources and whether these passages describe the same event and scope. This is an automated review lead, not a confirmed error. No edit has been made.`
    : "";
  return (
    <>
      <header>
        <a className="brand" href="/" aria-label="NPOV Radar home">
          <span className="radar-logo" />
          <span>
            NPOV<span className="brand-light"> Radar</span>
          </span>
        </a>
        <nav aria-label="Main navigation">
          {[
            ["worklist", "Editor worklist"],
            ["method", "Method & evaluation"],
          ].map(([v, l]) => (
            <button
              key={v}
              className={view === v ? "nav-active" : ""}
              onClick={() => setView(v)}
            >
              {l}
            </button>
          ))}
        </nav>
        <a
          className="repo-link"
          href="https://github.com/13shreyansh/npov-radar"
          target="_blank"
          rel="noreferrer"
        >
          Project code <ArrowUpRight size={15} />
        </a>
      </header>
      <div className="statusline">
        <span>
          <span
            className={"status-dot " + (live === "connected" ? "green" : "")}
          />
          {live === "connected"
            ? "MariaDB live connection"
            : live === "checking"
              ? "Checking live database…"
              : "Saved MariaDB results · live API unavailable"}
        </span>
        <span>
          Finland’s history <span className="separator">/</span> FI · EN · SV{" "}
          <span className="separator">/</span> {data.database.topics} topics
        </span>
      </div>
      {view === "method" ? (
        <main className="method">
          <button className="text-button" onClick={() => setView("worklist")}>
            <ArrowLeft size={16} /> Back to the worklist
          </button>
          <h1>Evidence before edits.</h1>
          <p className="large-copy">
            Semantic distance helps choose where to look. It cannot tell you
            which language is right.
          </p>
          <section>
            <h2>What the worklist does</h2>
            <p>
              We match Finnish passages to their nearest English and Swedish
              passages within the same Wikidata topic. MariaDB computes cosine
              distance over 384-dimensional multilingual sentence vectors. Exact
              dates and a small set of numeric units get deterministic checks. A
              mismatch becomes a review lead, never an automatic contradiction
              verdict.
            </p>
            <p>
              The queue sorts by numeric/date review count, then mean retrieved
              distance. This is a heuristic review priority, not a validated
              NPOV score. Coverage gaps may also be retrieval failures. All
              source checks currently abstain unless a verified cited-source
              excerpt is available.
            </p>
          </section>
          <section className="probe-panel">
            <h2>Try a planted error</h2>
            <p>
              Retrieve a real Winter War passage with MariaDB, then alter its
              copy. This synthetic test never changes Wikipedia or the stored
              evidence.
            </p>
            <div className="actions">
              <button
                className="primary"
                disabled={!!busy}
                onClick={() => run("probe", { mutation: "day" })}
              >
                {busy === "probe" ? "Running live test…" : "Change a day"}
              </button>
              <button
                className="subtle-button"
                disabled={!!busy}
                onClick={() => run("probe", { mutation: "name" })}
              >
                Swap a country name
              </button>
              <button
                className="subtle-button"
                disabled={!!busy}
                onClick={() => run("probe", { mutation: "none" })}
              >
                Unchanged control
              </button>
            </div>
            {probe && (
              <div role="status">
                {probe.error ? (
                  <p className="error">{probe.error}</p>
                ) : (
                  <>
                    <span className="tag">
                      Synthetic test ·{" "}
                      {probe.detected
                        ? "Review lead detected"
                        : probe.mutation === "none"
                          ? "No flag on unchanged text"
                          : "Known limitation: change missed"}
                    </span>
                    <h3>Real retrieved passage</h3>
                    <blockquote>{probe.original}</blockquote>
                    <a
                      href={revisionURL("en", probe.rev_id)}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Exact Wikipedia revision <ArrowUpRight size={12} />
                    </a>
                    <h3>Deliberately altered copy</h3>
                    <blockquote className="planted">{probe.changed}</blockquote>
                    <p>{probe.check.reason}</p>
                    <p>{probe.scope}</p>
                  </>
                )}
              </div>
            )}
          </section>
          <section>
            <h2>What actually ran</h2>
            <dl className="facts">
              <div>
                <dt>Database</dt>
                <dd>MariaDB {data.database.version}</dd>
              </div>
              <div>
                <dt>Passages in vector table</dt>
                <dd>{data.database.passages.toLocaleString()}</dd>
              </div>
              <div>
                <dt>Real revision rows</dt>
                <dd>{data.database.revisions.toLocaleString()}</dd>
              </div>
              <div>
                <dt>Alignment SQL queries</dt>
                <dd>{data.database.query_count.toLocaleString()}</dd>
              </div>
              <div>
                <dt>Local query p50 / p95</dt>
                <dd>
                  {data.database.query_p50_ms.toFixed(1)} /{" "}
                  {data.database.query_p95_ms.toFixed(1)} ms
                </dd>
              </div>
              <div>
                <dt>Saved results generated</dt>
                <dd>{data.built_at.replace("T", " ").replace("Z", " UTC")}</dd>
              </div>
            </dl>
            <p>
              Query timing excludes model loading, embedding, ingestion, network
              and browser time. The online API queries the same MariaDB instance
              on the build Mac through a temporary tunnel. It depends on that
              Mac staying online. Saved results remain readable if it goes
              offline.
            </p>
          </section>
          <section>
            <h2>Evaluation, with its limits</h2>
            {evals ? (
              <>
                <p>{evals.summary}</p>
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>Split / synthetic cases</th>
                        <th>Method</th>
                        <th>Error recall</th>
                        <th>False-positive rate</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evals.rows.map((r, i) => (
                        <tr key={i}>
                          <td>
                            {r.split} · {r.n}
                          </td>
                          <td>{r.method}</td>
                          <td>{r.recall}</td>
                          <td>{r.fpr}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <p>{evals.limitations}</p>
                <a
                  href="https://github.com/13shreyansh/npov-radar/blob/main/eval/LEDGER.md"
                  target="_blank"
                  rel="noreferrer"
                >
                  Read the evaluation ledger <ArrowUpRight size={14} />
                </a>
              </>
            ) : (
              <p>
                Evaluation is not yet published. No accuracy claim is available.
              </p>
            )}
          </section>
          <section>
            <h2>Boundaries that matter</h2>
            <ul>
              <li>
                Different audience emphasis is legitimate. Unequal article
                lengths and lexical tone do not prove bias.
              </li>
              <li>
                The sentence model truncates at 128 tokens. We cap passage
                length, but some Finnish text can still truncate.
              </li>
              <li>
                The Finnish historical import is incomplete relative to all of
                Wikipedia. Other languages have only a few recently fetched
                revisions.
              </li>
              <li>
                The history view shows real revision content. It does not
                establish when an editorial discrepancy began.
              </li>
              <li>
                No human gold labels or calibrated LLM judges are available.
                Synthetic tests measure only the implemented rules.
              </li>
              <li>No edits are sent to Wikipedia.</li>
            </ul>
          </section>
          <section>
            <h2>Data and licenses</h2>
            <p>
              Wikipedia and its contributors supply the article text and
              revisions under CC BY-SA 4.0. Data comes from the MariaDB
              Foundation’s S, M and L releases and the Wikipedia API. The new
              project code is MIT. The licenses remain separate.
            </p>
            <a
              href="https://github.com/MariaDB/mariadb-wikipedia-datasets"
              target="_blank"
              rel="noreferrer"
            >
              Official datasets <ArrowUpRight size={14} />
            </a>
          </section>
        </main>
      ) : (
        <>
          <section className="intro">
            <div>
              <h1>A clearer place to start editing.</h1>
              <p>
                Compare Finnish, English and Swedish accounts of Finland’s
                history.
                <br className="desktop-break" /> Find the passages worth a human
                review. Follow the evidence.
              </p>
            </div>
            <div className="human-rule">
              <BookOpen size={19} />
              <span>
                You decide what needs changing.
                <br />
                <strong>Radar never edits Wikipedia.</strong>
              </span>
            </div>
          </section>
          <main className="desk">
            <aside className="worklist">
              <div className="queue-heading">
                <h2>Your review queue</h2>
                <span>{data.articles.length} articles</span>
              </div>
              <p className="queue-help">
                Ranked by review leads, then language distance.
              </p>
              <label className="search">
                <Search size={16} />
                <input
                  aria-label="Find an article"
                  placeholder="Find an article…"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </label>
              <div className="queue">
                {list.length ? (
                  list.map((a, i) => (
                    <button
                      key={a.qid}
                      className={
                        "article-row " +
                        (article.qid === a.qid ? "selected" : "")
                      }
                      onClick={() => selectArticle(a)}
                      aria-label={`Review ${a.title}`}
                      aria-pressed={article.qid === a.qid}
                    >
                      <span className="rank">
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <span className="article-row-content">
                        <strong>{a.title}</strong>
                        <span>{a.fi_title}</span>
                        <span className="row-meta">
                          {a.review_count
                            ? `${a.review_count} number/date leads`
                            : "Coverage & emphasis"}
                          <span className="mini-distance">
                            {a.distance.toFixed(2)} distance
                          </span>
                        </span>
                      </span>
                      <ChevronRight size={17} />
                    </button>
                  ))
                ) : (
                  <p className="empty">
                    No articles match “{search}”. Try an English or Finnish
                    title.
                  </p>
                )}
              </div>
              <div className="queue-foot">
                <Info size={15} />
                <p>
                  Distance measures wording and coverage, not neutrality. A flag
                  is a place to look, not a verdict.
                </p>
              </div>
              <div className="language-key">
                <span>
                  FI <small>Finnish</small>
                </span>
                <span>
                  EN <small>English</small>
                </span>
                <span>
                  SV <small>Swedish</small>
                </span>
              </div>
            </aside>
            <section className="workspace">
              <div className="article-heading">
                <div>
                  <h2>{article.title}</h2>
                  <p>
                    {article.fi_title}{" "}
                    <span>
                      · {article.passage_count} Finnish passages checked
                    </span>
                  </p>
                </div>
                <button
                  className="subtle-button"
                  onClick={() => {
                    setView("method");
                  }}
                >
                  <Info size={16} /> How to read this
                </button>
              </div>
              <div className="workspace-tabs">
                <button className="active">
                  <BookOpen size={16} /> Compare passages
                </button>
                <button
                  onClick={() => {
                    run("history", { lang: "fi" });
                  }}
                >
                  <History size={16} /> Revision history
                </button>
                <span>Same topic · {article.qid}</span>
              </div>
              <div className="filters" aria-label="Filter passages">
                <Filter size={14} />
                {[
                  ["all", "All passages"],
                  ["review", "Numbers & dates"],
                  ["coverage", "Weak matches"],
                  ["aligned", "Matching dates"],
                ].map(([v, l]) => (
                  <button
                    className={filter === v ? "active" : ""}
                    key={v}
                    onClick={() => {
                      setFilter(v);
                      setSelected("");
                      setNote(false);
                    }}
                  >
                    {l}
                  </button>
                ))}
                <span>{visible.length} results</span>
              </div>
              <div className="comparison-area">
                <div className="passage-list" aria-label="Passages">
                  {visible.length ? (
                    visible.map((f, i) => (
                      <button
                        key={f.id}
                        onClick={() => {
                          setSelected(f.id);
                          setQuery(null);
                          setNote(false);
                        }}
                        className={
                          "passage-link " +
                          (finding?.id === f.id ? "active" : "")
                        }
                      >
                        <span className={"kind-dot " + reviewKind(f)} />
                        <span>
                          <strong>{f.fi.section}</strong>
                          <small>{labels[reviewKind(f)]}</small>
                        </span>
                        <ChevronRight size={14} />
                      </button>
                    ))
                  ) : (
                    <p className="empty">
                      No passages match this filter. Try “All passages”.
                    </p>
                  )}
                </div>
                {finding ? (
                  <div className="evidence">
                    <div className="finding-title">
                      <span className={"tag " + reviewKind(finding)}>
                        {labels[reviewKind(finding)]}
                      </span>
                      <button
                        className="text-button"
                        onClick={() =>
                          setReviewed((s) =>
                            s.includes(finding.id)
                              ? s.filter((x) => x !== finding.id)
                              : [...s, finding.id],
                          )
                        }
                      >
                        {reviewed.includes(finding.id) ? (
                          <CheckCheck size={15} />
                        ) : (
                          <Check size={15} />
                        )}{" "}
                        {reviewed.includes(finding.id)
                          ? "Reviewed on this device"
                          : "Mark reviewed"}
                      </button>
                    </div>
                    <h3>{finding.fi.section}</h3>
                    <p className="finding-explanation">
                      {reviewKind(finding) === "emphasis"
                        ? "Related text was retrieved. These passages may agree or emphasize different things; no factual verdict has been established."
                        : reviewKind(finding) === "coverage"
                          ? "The model did not retrieve a close match in at least one language. Check the alternatives before treating this as an omission."
                          : reviewKind(finding) === "aligned"
                            ? "The extracted full dates match in at least one language pair. This is evidence for those dates, not verification of the whole passage."
                            : "The checks found a difference worth reviewing. Confirm the event, unit, rounding and source before proposing any correction."}
                    </p>
                    <div className="evidence-columns">
                      {["fi", "en", "sv"].map((lang) => {
                        const p =
                          lang === "fi" ? finding.fi : finding.matches[lang];
                        const v = article.versions.find((v) => v.lang === lang);
                        return (
                          <article className="quote-column" key={lang}>
                            <div className="quote-header">
                              <span className="lang">{lang.toUpperCase()}</span>
                              <strong>
                                {lang === "fi"
                                  ? "Finnish"
                                  : lang === "en"
                                    ? "English"
                                    : "Swedish"}
                              </strong>
                              {lang !== "fi" && p && (
                                <span
                                  className="similarity"
                                  title="Cosine similarity is not confidence"
                                >
                                  {Math.round((1 - p.distance) * 100)}% similar
                                </span>
                              )}
                            </div>
                            <blockquote lang={lang}>
                              {p?.text || "No passage retrieved."}
                            </blockquote>
                            {p?.check && (
                              <p className={"pair-check " + p.check.kind}>
                                {p.check.reason}
                              </p>
                            )}
                            <div className="provenance">
                              <span>{v?.title}</span>
                              <span>
                                Revised {formatDate(v?.date_modified)}
                              </span>
                              <a
                                href={revisionURL(lang, p?.rev_id || v?.rev_id)}
                                target="_blank"
                                rel="noreferrer"
                              >
                                Revision {p?.rev_id || v?.rev_id}{" "}
                                <ArrowUpRight size={12} />
                              </a>
                            </div>
                            {lang !== "fi" && p?.alternatives?.length > 0 && (
                              <details>
                                <summary>Other retrieved passages</summary>
                                {p.alternatives.map((a) => (
                                  <p key={a.id} lang={lang}>
                                    {a.text}
                                    <small>
                                      Similarity{" "}
                                      {Math.round((1 - a.distance) * 100)}%
                                    </small>
                                  </p>
                                ))}
                              </details>
                            )}
                          </article>
                        );
                      })}
                    </div>
                    <div className="source-check">
                      <div className="source-icon">
                        <Search size={18} />
                      </div>
                      <div>
                        <h4>
                          Cited-source support{" "}
                          <span className="neutral-tag">
                            {finding.source.status === "supports-date"
                              ? "Supports start date only"
                              : "Cannot verify"}
                          </span>
                        </h4>
                        <p>{finding.source.reason}</p>
                        {finding.source.quote && (
                          <div className="source-excerpt">
                            <blockquote>"{finding.source.quote}"</blockquote>
                            <a
                              href={finding.source.url}
                              target="_blank"
                              rel="noreferrer"
                            >
                              {finding.source.publisher} ·{" "}
                              {finding.source.title} <ArrowUpRight size={12} />
                            </a>
                            <p>
                              Curated source check · exact excerpt · other
                              claims remain unverified.
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                    {finding.tone.length > 0 && (
                      <div className="tone-note">
                        <Info size={16} />
                        <p>
                          Lexical tone cue: {finding.tone.join(", ")}. This may
                          be an attributed quotation. Read the context before
                          calling the wording loaded.
                        </p>
                      </div>
                    )}
                    <div className="actions">
                      <button
                        className="primary"
                        onClick={() => setNote(!note)}
                      >
                        <Copy size={16} /> Prepare a review note
                      </button>
                      <a
                        className="subtle-button"
                        href={`https://fi.wikipedia.org/w/index.php?curid=${finding.fi.page_id}&action=edit`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Open Wikipedia editor <ExternalLink size={14} />
                      </a>
                    </div>
                    {note && (
                      <section className="review-note">
                        <h4>A starting point for your talk-page note</h4>
                        <p>
                          Check and adapt this before posting. Radar does not
                          send it anywhere.
                        </p>
                        <textarea
                          aria-label="Review note"
                          value={noteText}
                          readOnly
                          rows={10}
                        />
                        <button
                          className="subtle-button"
                          onClick={async () => {
                            try {
                              await navigator.clipboard.writeText(noteText);
                              setCopied(true);
                            } catch {
                              setCopied(false);
                            }
                          }}
                        >
                          {copied ? <Check size={14} /> : <Copy size={14} />}{" "}
                          {copied ? "Copied" : "Copy note"}
                        </button>
                      </section>
                    )}
                    <details className="sql-panel">
                      <summary>
                        <Database size={16} /> Inspect the MariaDB query{" "}
                        <span>Native vector search</span>
                      </summary>
                      <p>
                        The saved alignment above came from this SQL. Run it
                        again to inspect a fresh database response.
                      </p>
                      <pre>{data.sql.alignment}</pre>
                      <button
                        className="subtle-button"
                        disabled={!!busy}
                        onClick={() =>
                          run("align", { id: finding.id, lang: "en" })
                        }
                      >
                        <RefreshCw size={14} />
                        {busy === "align"
                          ? "Running query…"
                          : "Run live alignment query"}
                      </button>
                      {query && (
                        <div className="query-result" role="status">
                          {query.error ? (
                            <p className="error">{query.error}</p>
                          ) : (
                            <>
                              <p>
                                <Check size={14} /> MariaDB {query.database} ·{" "}
                                {query.elapsed_ms.toFixed(1)} ms ·{" "}
                                {query.rows.length} rows
                              </p>
                              {query.rows.map((r) => (
                                <div key={r.id}>
                                  <strong>
                                    {r.id} · distance {r.distance.toFixed(4)}
                                  </strong>
                                  <p>{r.text}</p>
                                </div>
                              ))}
                            </>
                          )}
                        </div>
                      )}
                    </details>
                  </div>
                ) : (
                  <div className="empty">
                    Select a different filter to compare passages.
                  </div>
                )}
              </div>
              {(history || busy === "history") && (
                <section className="history-panel">
                  <h3>
                    <History size={20} /> What did this article say then?
                  </h3>
                  <p>
                    MariaDB system-versioned rows use Wikipedia’s original
                    revision times. This view shows text history, not proof of
                    when a discrepancy began.
                  </p>
                  {busy === "history" ? (
                    <p role="status">Querying revision history…</p>
                  ) : history.error ? (
                    <p className="error">{history.error}</p>
                  ) : (
                    <>
                      <p>
                        {history.offline
                          ? "Saved temporal SQL results. Live time travel is unavailable. "
                          : ""}
                        {history.total.toLocaleString()} stored Finnish
                        revisions. Most recent entries below.
                      </p>
                      <form
                        onSubmit={(e) => {
                          e.preventDefault();
                          run("asof", { lang: "fi", date: asof });
                        }}
                      >
                        <label>
                          Article as of{" "}
                          <input
                            type="date"
                            value={asof}
                            min="2002-01-01"
                            max={data.built_at.slice(0, 10)}
                            onChange={(e) => setAsof(e.target.value)}
                            required
                          />
                        </label>
                        <button className="primary" disabled={!!busy}>
                          {busy === "asof"
                            ? "Querying…"
                            : "Travel to this date"}
                        </button>
                      </form>
                      {point && (
                        <div className="historical-result" role="status">
                          {point.error ? (
                            <p className="error">{point.error}</p>
                          ) : point.row ? (
                            <>
                              <h4>
                                {point.row.title} · revision {point.row.rev_id}
                              </h4>
                              <p>
                                Saved on {point.row.revised_at} UTC ·{" "}
                                {point.elapsed_ms.toFixed(1)} ms query
                              </p>
                              <pre>{point.row.text.slice(0, 5000)}</pre>
                              <a
                                href={revisionURL("fi", point.row.rev_id)}
                                target="_blank"
                                rel="noreferrer"
                              >
                                Read this revision on Wikipedia{" "}
                                <ArrowUpRight size={14} />
                              </a>
                            </>
                          ) : (
                            <p>No stored revision was valid at that time.</p>
                          )}
                        </div>
                      )}
                      <div className="history-list">
                        {history.rows.slice(0, 8).map((r) => (
                          <a
                            href={revisionURL("fi", r.rev_id)}
                            key={r.rev_id}
                            target="_blank"
                            rel="noreferrer"
                          >
                            <time>{r.revised_at}</time>
                            <span>Revision {r.rev_id}</span>
                            <small>
                              {r.characters.toLocaleString()} characters
                            </small>
                            <ArrowUpRight size={13} />
                          </a>
                        ))}
                      </div>
                      <details>
                        <summary>Executed temporal SQL</summary>
                        <pre>{history.sql}</pre>
                      </details>
                    </>
                  )}
                </section>
              )}
            </section>
          </main>
        </>
      )}
      <footer>
        <span>
          NPOV Radar <span className="separator">/</span> Built at Junction 2026
          by The CS Guy
        </span>
        <span>
          Wikipedia text © its contributors · CC BY-SA 4.0{" "}
          <a
            href="https://github.com/13shreyansh/npov-radar/blob/main/DATA_LICENSE.md"
            target="_blank"
            rel="noreferrer"
          >
            Attribution <ArrowUpRight size={12} />
          </a>
        </span>
      </footer>
    </>
  );
}
createRoot(document.getElementById("root")).render(<App />);
