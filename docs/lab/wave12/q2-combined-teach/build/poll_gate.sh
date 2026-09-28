#!/bin/bash
# TOGETHER 6-corpus gate poll (replaces the 9-corpus /tmp/together_poll.sh).
# Gate (Micah's order 2026-09-21 14:35 PDT — GLM sources FORGOTTEN):
#   sol, grok-4.6, step-3.7-flash, swe-1-6-slow, hy3, muse-native.
# 5/6 are frozen as DATA. The only open item is hy3's corpus (capacity retry
# running in the hy3 team's background process). This poll watches the
# tnn-native-lab branch for hy3's DATA commit and logs a GATE MET line.
# Log: ~/workspace/tnn-lab/wave12/q2-combined-teach/build/poll_gate.log
GH=~/workspace/skills/github/bin/gh-api
LOG=~/workspace/tnn-lab/wave12/q2-combined-teach/build/poll_gate.log
echo "$(date -u +%FT%TZ) poll start: 6-corpus gate, 5/6 frozen, watching hy3" >> "$LOG"
while true; do
  if $GH GET "/repos/sylorlabs/TNN/commits?sha=tnn-native-lab&per_page=40" 2>/dev/null \
    | grep -qi "hy3.*corpus\|corpus.*hy3\|q2-distillation-hy3.*DATA\|DATA.*hy3"; then
    echo "$(date -u +%FT%TZ) GATE MET? hy3 corpus commit detected on tnn-native-lab — verify DATA commit, then run the 6-source pipeline" >> "$LOG"
    sleep 3600
  else
    echo "$(date -u +%FT%TZ) waiting: hy3 corpus not yet on tnn-native-lab (5/6 frozen)" >> "$LOG"
    sleep 300
  fi
done
