"""Download official releases. Third-party text is CC BY-SA 4.0, never MIT."""

import requests, pathlib, concurrent.futures, hashlib

root = pathlib.Path("work/official")
root.mkdir(exist_ok=True)


def fetch(job):
    size, name = job
    dest = root / size / name
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        return str(dest) + " cached"
    u = f"https://github.com/MariaDB/mariadb-wikipedia-datasets/releases/download/{size}-2026-10/{name}"
    with requests.get(u, stream=True, timeout=90) as r:
        r.raise_for_status()
        with open(str(dest) + ".part", "wb") as f:
            for b in r.iter_content(1 << 20):
                f.write(b)
    pathlib.Path(str(dest) + ".part").rename(dest)
    return str(dest) + " " + str(dest.stat().st_size)


jobs = [("m", "SHA256SUMS"), ("l", "SHA256SUMS"), ("l", "articles-fi.parquet")] + [
    ("m", f"versions-{n:02d}.parquet") for n in range(1, 17)
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for r in ex.map(fetch, jobs):
        print(r, flush=True)
for size in ["m", "l"]:
    for line in (root / size / "SHA256SUMS").read_text().splitlines():
        parts = line.split()
        if len(parts) == 2:
            p = root / size / parts[1].lstrip("*")
            if p.exists():
                assert hashlib.sha256(p.read_bytes()).hexdigest() == parts[0], str(p)
print("Downloaded files match official SHA256SUMS")
