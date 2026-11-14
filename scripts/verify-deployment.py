"""Verify the real deployed frontend -> proxy -> MariaDB flow, with no writes."""

import argparse, datetime, json, pathlib, requests

p = argparse.ArgumentParser()
p.add_argument("--url", default="https://npov-radar.vercel.app")
args = p.parse_args()
base = args.url.rstrip("/")
results = []


def get(path, validate):
    r = requests.get(base + path, timeout=25)
    j = r.json() if "json" in r.headers.get("Content-Type", "") else {}
    passed = validate(r, j)
    results.append(
        {
            "path": path,
            "status": r.status_code,
            "pass": bool(passed),
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    )
    print("PASS" if passed else "FAIL", path, r.status_code)


get("/", lambda r, j: r.status_code == 200 and "NPOV Radar" in r.text)
get(
    "/snapshot.json",
    lambda r, j: r.status_code == 200 and j.get("database", {}).get("passages", 0) > 0,
)
get(
    "/api/radar?mode=health",
    lambda r, j: r.status_code == 200
    and j.get("ok") is True
    and "MariaDB" in j.get("database", ""),
)
get(
    "/api/radar?mode=align&id=fi-1256-0&lang=en",
    lambda r, j: r.status_code == 200
    and len(j.get("rows", [])) == 3
    and all(x["rev_id"] > 0 for x in j["rows"]),
)
get(
    "/api/radar?mode=asof&qid=Q134949&lang=fi&date=2015-01-01",
    lambda r, j: r.status_code == 200
    and (j.get("row") or {}).get("rev_id") == 14547217,
)
get(
    "/api/radar?mode=asof&qid=Q134949&lang=fi&date=2026-10-02",
    lambda r, j: r.status_code == 200 and j.get("row") is None,
)
get(
    "/api/radar?mode=probe&mutation=day",
    lambda r, j: r.status_code == 200
    and j.get("synthetic") is True
    and j.get("detected") is True,
)
get(
    "/api/radar?mode=probe&mutation=name",
    lambda r, j: r.status_code == 200
    and j.get("synthetic") is True
    and j.get("detected") is False
    and j.get("changed_anything") is True,
)
get("/api/radar?mode=align&id=unknown&lang=en", lambda r, j: r.status_code == 400)
get("/api/radar?mode=arbitrary-sql", lambda r, j: r.status_code == 400)
root = pathlib.Path(__file__).resolve().parents[1]
(root / "eval/deployed-regression-checks.json").write_text(
    json.dumps(results, indent=2)
)
raise SystemExit(0 if all(x["pass"] for x in results) else 1)
