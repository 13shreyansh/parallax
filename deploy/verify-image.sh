#!/bin/sh
set -eu
# Regression: runtime imports must work as the image's unprivileged user on a read-only filesystem.
docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=32m --network none --entrypoint python parallax-api:current -c 'import service.app; from pipeline.common import WORK; assert str(WORK).startswith("/tmp/"); assert service.app.app.name == "service.app"'
