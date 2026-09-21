#!/bin/bash
# run_metric.sh — run one arm mode twice (fresh subdir per rerun), capturing
# stdout/stderr and the METRIC_JSON fragment, plus max RSS via /proc polling
# (no GNU time on this VM). Fails on: non-zero exit, FATAL line, stdout divergence.
# Usage: run_metric.sh <arm-bin> <mode> <corpus-root> <workdir> [extra args...]
set -u
BIN="$1"; MODE="$2"; CROOT="$3"; WORK="$4"; shift 4
EXTRA=("$@")
rm -rf "$WORK/run1" "$WORK/run2"
mkdir -p "$WORK/run1" "$WORK/run2"

run_with_rss() { # <tagdir> <cmd...>
    local tagdir="$1"; shift
    ( cd "$tagdir" && exec "$@" >stdout.txt 2>stderr.txt ) &
    local pid=$!
    local peak=0 v
    while kill -0 "$pid" 2>/dev/null; do
        v=$(awk '/^VmHWM:/{print $2}' "/proc/$pid/status" 2>/dev/null || true)
        case "$v" in ''|*[!0-9]*) ;; *) [ "$v" -gt "$peak" ] 2>/dev/null && peak="$v";; esac
        sleep 0.02
    done
    wait "$pid"; local rc=$?
    echo "$rc" >"$tagdir/rc.txt"
    echo "$peak" >"$tagdir/rss_kb.txt"
}

run_with_rss "$WORK/run1" "$BIN" "$MODE" "$CROOT" "${EXTRA[@]}"
run_with_rss "$WORK/run2" "$BIN" "$MODE" "$CROOT" "${EXTRA[@]}"

R1=$(cat "$WORK/run1/rc.txt"); R2=$(cat "$WORK/run2/rc.txt")
RSS1=$(cat "$WORK/run1/rss_kb.txt"); RSS2=$(cat "$WORK/run2/rss_kb.txt")
# METRIC_JSON fragment = last run's fragment line
grep -h '^METRIC_JSON ' "$WORK/run2/stdout.txt" > "$WORK/fragment.jsonl" || true
# FATAL line in either run = invalid trial
FATAL=0
grep -q 'FATAL' "$WORK/run1/stdout.txt" "$WORK/run2/stdout.txt" 2>/dev/null && FATAL=1
# determinism: diff stdout of the two runs
if diff -q "$WORK/run1/stdout.txt" "$WORK/run2/stdout.txt" >/dev/null 2>&1; then
    DET="IDENTICAL"
else
    DET="DIFFER"
fi
echo "mode=$MODE rc1=$R1 rc2=$R2 rss1_kb=$RSS1 rss2_kb=$RSS2 stdout=$DET fatal=$FATAL" > "$WORK/STATUS.txt"
cat "$WORK/STATUS.txt"
[ "$DET" = "IDENTICAL" ] || { echo "DOUBLE-RUN DIVERGENCE for $MODE" >&2; exit 1; }
[ "$FATAL" = "0" ] || { echo "FATAL in $MODE output" >&2; exit 1; }
[ "$R1" = "0" ] && [ "$R2" = "0" ] || exit 1
