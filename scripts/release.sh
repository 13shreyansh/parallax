#!/bin/sh
# Ship the committed tree to the VPS: build beside the live release, switch after health passes.
set -e
cd "$(dirname "$0")/.."
test -z "$(git status --porcelain -- package.json package-lock.json vite.config.js index.html src public-parallax pipeline service deploy)" || { echo "Commit before releasing."; exit 1; }
mkdir -p work/parallax
git rev-parse HEAD > work/parallax/deploy-commit.txt
COPYFILE_DISABLE=1 tar -czf /tmp/parallax-release-source.tgz --exclude='deploy/previous-assets' package.json package-lock.json vite.config.js index.html src public-parallax pipeline service deploy .dockerignore
scp -q /tmp/parallax-release-source.tgz root@72.61.22.106:/opt/parallax/release-source.tgz
ssh -o BatchMode=yes root@72.61.22.106 'tar -xzf /opt/parallax/release-source.tgz -C /opt/parallax/source'
ssh -o BatchMode=yes root@72.61.22.106 python3 /opt/parallax/source/deploy/release_remote.py "$(cat work/parallax/deploy-commit.txt)"
# Keep the live release and the one before it; older ones only hold memory.
ssh -o BatchMode=yes root@72.61.22.106 "docker ps --filter label=io.parallax.release --format '{{.CreatedAt}} {{.Names}}' | sort -r | tail -n +3 | awk '{print \$NF}' | xargs -r docker rm -f >/dev/null"
