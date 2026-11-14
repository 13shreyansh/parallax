#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export DYLD_LIBRARY_PATH="$(find "$PWD/work/runtime" -type d -name lib | paste -sd: -)"
exec "$PWD/work/runtime/mariadb/13.0.2_1/bin/mariadbd" --no-defaults --basedir="$PWD/work/runtime/mariadb/13.0.2_1" --datadir="$PWD/work/db" --socket="$PWD/work/mariadb.sock" --pid-file="$PWD/work/mariadb.pid" --skip-networking --innodb-buffer-pool-size=256M --log-error="$PWD/work/database.log"
