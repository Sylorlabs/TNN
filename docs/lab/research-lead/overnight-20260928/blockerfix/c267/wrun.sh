#!/bin/bash
# B1 run wrapper. setsid does not exist on darwin/arm64, so every launch is
# detached with nohup+disown; otherwise the watchdog's poll loop dies with the
# launching shell and the run loses its timeout (brief 10.1 / 10.2).
# Usage: wrun.sh <name> <limit> <binary> [args...]
set -u
NAME="$1"; LIM="$2"; shift 2
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
cd "$(dirname "$0")"
D="$PWD"
nohup "$W" reg "$NAME" "$LIM" "$D/$@" >/dev/null 2>&1 </dev/null &
disown 2>/dev/null || true
exit 0