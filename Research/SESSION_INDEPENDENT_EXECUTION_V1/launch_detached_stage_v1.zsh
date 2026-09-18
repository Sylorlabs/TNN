#!/bin/zsh
set -eu

if (( $# < 2 )); then
  print -u2 -- 'usage: launch_detached_stage_v1.zsh STAGE_ID SCRIPT [args...]'
  exit 64
fi

STAGE_ID=$1
SCRIPT=$2
shift 2

case "$STAGE_ID" in
  (*[!A-Za-z0-9._-]*)
    print -u2 -- 'stage id must contain only A-Z a-z 0-9 . _ -'
    exit 65
    ;;
esac

if [[ ! -f "$SCRIPT" ]]; then
  print -u2 -- "stage script not found: $SCRIPT"
  exit 66
fi

BASE=${TNN_DETACHED_RUN_ROOT:-"$PWD/Research/DETACHED_RUNS"}
HERE=${0:A:h}
WORKER="$HERE/detached_worker_v1.zsh"
if [[ ! -f "$WORKER" ]]; then
  print -u2 -- "worker missing: $WORKER"
  exit 67
fi

stamp=$(date -u '+%Y%m%dT%H%M%SZ')
RUN_DIR="$BASE/${stamp}-${STAGE_ID}"
mkdir -p "$RUN_DIR"
script_abs=${SCRIPT:A}
worker_abs=${WORKER:A}

{
  print -- "stage_id=$STAGE_ID"
  print -- "script=$script_abs"
  print -- "worker=$worker_abs"
  print -- "launch_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  print -- "cwd=$PWD"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$script_abs" "$worker_abs"
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$script_abs" "$worker_abs"
  fi
} > "$RUN_DIR/LAUNCH.txt"

{
  print -- "script=$script_abs"
  print -- "argc=$#"
  i=1
  for arg in "$@"; do
    print -r -- "arg[$i]=${(qqq)arg}"
    (( i = i + 1 ))
  done
} > "$RUN_DIR/ARGUMENTS.txt"

nohup zsh "$worker_abs" "$RUN_DIR" "$STAGE_ID" "$script_abs" "$@" > "$RUN_DIR/worker.out" 2>&1 &
pid=$!
print -- "$pid" > "$RUN_DIR/worker.pid"
print -- "DETACHED_STAGE_V1_LAUNCHED,$STAGE_ID,$pid,$RUN_DIR"
