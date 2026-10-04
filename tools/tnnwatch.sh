#!/bin/bash
# TNN WATCHDOG (charter 96 hang detection / 153 watchdog recovery / 97 resource mgmt)
#
# WHY THIS EXISTS
#   Wave 2 aborted mid-experiment and left two Zag binaries running as orphans
#   (ppid=1): ./p5 for 2h28m and ./t2 for 2h13m, ~90% CPU each. Nobody would ever
#   collect them. On a 10-core box that is ~1.8 cores burned for 4+ hours, and it
#   was a direct contributor to later workers being unable to get CPU.
#
#   There was no timeout on any experiment run, so "LONG-RUNNING" and "DEAD" were
#   indistinguishable. That is precisely the failure the charter forbids.
#
# WHAT IT DOES
#   reg  <name> <secs> <cmd...>   run cmd under a hard wall-clock timeout.
#                                   On timeout: kill the whole process group and
#                                   record TIMEOUT (never silently extend).
#   reap                         kill any unregistered TNN-lane Zag binary that
#                                   has been running longer than the grace period.
#   status                       load, cores, RAM, disk, live runs, orphans.
#
# TIMEOUT SEMANTICS (charter 96/152)
#   A timeout is recorded as FAIL/TIMEOUT exactly as the prereg specified. It is
#   NEVER retried with a longer limit, because that would be moving a bar after
#   seeing the result.

set -u
WTROOT=/Users/Shared/micah/Documents/TNN/.worktrees
RUNDIR=/Users/Shared/micah/Documents/TNN/.runs
GRACE=${TNN_REAP_SECS:-900}      # orphans get 15 min before considered dead
mkdir -p "$RUNDIR"

# --------------------------------------------------------------------- reg --
cmd_reg() {
  local name="$1" secs="$2"; shift 2
  local log="$RUNDIR/$name.log"
  local meta="$RUNDIR/$name.meta"
  local start; start=$(date +%s)
  printf 'name=%s\nlimit=%s\nstart=%s\nstatus=RUNNING\n' "$name" "$secs" "$start" > "$meta"

  # setsid gives the child its own process group so a timeout kills the WHOLE
  # tree. Without this, killing the parent orphans the children - exactly the
  # bug this script exists to prevent.
  if command -v setsid >/dev/null 2>&1; then
    setsid "$@" > "$log" 2>&1 &
  else
    "$@" > "$log" 2>&1 &
  fi
  local pid=$!
  echo "$pid" > "$RUNDIR/$name.pid"

  local waited=0 rc=0 timedout=0
  while kill -0 "$pid" 2>/dev/null; do
    sleep 1
    waited=$((waited+1))
    if [ "$waited" -ge "$secs" ]; then timedout=1; break; fi
  done

  if [ "$timedout" = "1" ]; then
    kill -TERM -"$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null
    sleep 2
    kill -KILL -"$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null
    rc=124
    printf 'name=%s\nstatus=TIMEOUT\nlimit=%s\nelapsed=%s\n' "$name" "$secs" "$waited" > "$meta"
    echo "[watchdog] $name TIMEOUT after ${secs}s (killed process group $pid)" >&2
  else
    wait "$pid" 2>/dev/null; rc=$?
    printf 'name=%s\nstatus=DONE\nelapsed=%s\nrc=%s\n' "$name" "$waited" "$rc" > "$meta"
  fi

  # A run that produced NO output is not a result. This is the o_flush defect in
  # operational form: an empty log with rc=0 previously read as success.
  local bytes; bytes=$(wc -c < "$log" 2>/dev/null | tr -d ' ')
  if [ "${bytes:-0}" -eq 0 ]; then
    echo "[watchdog] $name PRODUCED ZERO BYTES - not a result (check _zag_print vs _zag_raw_syscall)" >&2
    printf 'name=%s\nstatus=EMPTY\nbytes=0\n' "$name" > "$meta"
  fi
  cat "$log"
  return $rc
}

# -------------------------------------------------------------------- reap --
cmd_reap() {
  local killed=0
  # Only binaries whose cwd is inside a TNN worktree or scratchpad are ours.
  for p in $(pgrep -f '^\./(p[0-9a-z_]+|lt[0-9]|c8t|smoke|probe|t2)$' 2>/dev/null); do
    local cwd; cwd=$(lsof -a -p "$p" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
    case "$cwd" in
      "$WTROOT"/*|*/opencode/*) ;;
      *) continue ;;
    esac
    # Respect the grace period.
    local et; et=$(ps -o etimes= -p "$p" 2>/dev/null | tr -d ' ')
    [ -n "${et:-}" ] || continue
    if [ "$et" -lt "$GRACE" ]; then
      echo "[watchdog] pid $p alive ${et}s (< grace ${GRACE}s), leaving alone"
      continue
    fi
    echo "[watchdog] reaping ORPHAN pid $p (${et}s) cwd=$cwd"
    kill -TERM "$p" 2>/dev/null; sleep 1; kill -KILL "$p" 2>/dev/null
    killed=$((killed+1))
  done
  echo "[watchdog] reaped=$killed"
}

# ------------------------------------------------------------------ status --
cmd_status() {
  echo "=== TNN WATCHDOG STATUS $(date '+%H:%M:%S') ==="
  echo "cores: $(sysctl -n hw.ncpu)   load: $(sysctl -n vm.loadavg | tr -d '{}' | cut -d, -f1-3)"
  echo "RAM free%: $(memory_pressure 2>/dev/null | sed -n 's/.*free percentage: //p')"
  df -h /Users/Shared | tail -1 | awk '{print "disk free: "$4"  used: "$5}'
  echo "--- registered runs ---"
  if ls "$RUNDIR"/*.meta >/dev/null 2>&1; then
    for m in "$RUNDIR"/*.meta; do
      printf '  %-28s %s\n' "$(basename "$m" .meta)" "$(tr '\n' ' ' < "$m")"
    done
  else
    echo "  (none)"
  fi
  echo "--- live TNN-lane processes ---"
  found=0
  for p in $(pgrep -f '^\./(p[0-9a-z_]+|lt[0-9]|c8t|smoke|probe|t2)$' 2>/dev/null); do
    cwd=$(lsof -a -p "$p" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
    case "$cwd" in
      "$WTROOT"/*|*/opencode/*) printf '  pid=%s etime=%s cwd=%s\n' "$p" "$(ps -o etime= -p $p|tr -d ' ')" "$cwd"; found=1 ;;
    esac
  done
  [ "$found" = "1" ] || echo "  (none)"
  echo "--- foreign load (NOT ours, informational) ---"
  ps -Ao pcpu,comm -r 2>/dev/null | head -5 | sed 's/^/  /'
}

case "${1:-status}" in
  reg)    shift; cmd_reg "$@" ;;
  reap)   cmd_reap ;;
  status) cmd_status ;;
  *)      echo "usage: tnnwatch.sh {reg NAME SECS CMD...|reap|status}" >&2; exit 2 ;;
esac
