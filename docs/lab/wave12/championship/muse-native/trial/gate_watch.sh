#!/usr/bin/env bash
# Gate watcher for CREW MUSE-TNN: poll until all 40 raw batches exist,
# then run the mechanical freeze. Polls 90s, timeout ~4h.
RAW=~/workspace/championship/muse_team/raw
deadline=$(( $(date +%s) + 4*3600 ))
while [ $(date +%s) -lt $deadline ]; do
  n=0
  for tag in dump teach; do
    for bi in $(seq -w 0 19); do
      [ -f "$RAW/${tag}_batch${bi}.txt" ] && n=$((n+1))
    done
  done
  echo "$(date -u +%H:%M:%SZ) gate: $n/40 batches present"
  if [ "$n" -eq 40 ]; then
    python3 ~/workspace/championship/muse_team/freeze_corpus.py
    code=$?
    if [ $code -eq 0 ]; then
      echo "GATE CLEAR — corpus frozen"
      exit 0
    elif [ $code -eq 2 ]; then
      echo "parse failures — continuing to poll for corrected files"
    else
      echo "unexpected freeze exit $code — continuing to poll"
    fi
  fi
  sleep 90
done
echo "TIMEOUT: gate never cleared within 4h"
exit 3
