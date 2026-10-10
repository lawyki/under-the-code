#!/bin/sh
# Runs every suite in sequence (they share port 8123); logs to out/<suite>.log.
cd "$(dirname "$0")"
rc=0
for s in invariants traces parity marks ui; do
  node "$s.mjs" "$@" > "out/$s.log" 2>&1 || rc=1
  grep '^SUMMARY' "out/$s.log"
done
exit $rc
