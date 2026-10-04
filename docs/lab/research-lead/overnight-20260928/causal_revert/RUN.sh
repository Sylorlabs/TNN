#!/bin/sh
# RUN.sh -- run the causal-revert binary 3 times; check byte-identical determinism.
# Usage: ./RUN.sh   (run from the causal_revert/ directory)
set -e
./BUILD.sh
./causal_revert_bin > RUN1.txt 2> RUN1.err; echo "exit=$? run=1"
./causal_revert_bin > RUN2.txt 2> RUN2.err; echo "exit=$? run=2"
./causal_revert_bin > RUN3.txt 2> RUN3.err; echo "exit=$? run=3"
md5sum RUN1.txt RUN2.txt RUN3.txt
if cmp -s RUN1.txt RUN2.txt && cmp -s RUN1.txt RUN3.txt; then
  echo "DETERMINISM-OK 3/3 byte-identical"
else
  echo "DETERMINISM-FAIL runs differ" >&2
  exit 1
fi
