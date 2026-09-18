#!/bin/zsh
set -u

if (( $# < 3 )); then
  print -u2 -- 'usage: detached_worker_v1.zsh RUN_DIR STAGE_ID SCRIPT [args...]'
  exit 64
fi

RUN_DIR=$1
STAGE_ID=$2
SCRIPT=$3
shift 3
mkdir -p "$RUN_DIR" || exit 65

status="$RUN_DIR/STATUS.json"
log="$RUN_DIR/stage.log"
started=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
pid=$$

json_escape() {
  print -rn -- "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

write_status() {
  local phase=$1
  local code=${2:-null}
  local finished_raw=${3:-}
  local esc_stage esc_script finished_json
  esc_stage=$(json_escape "$STAGE_ID")
  esc_script=$(json_escape "$SCRIPT")
  finished_json=null
  if [[ -n "$finished_raw" ]]; then
    finished_json="\"$(json_escape "$finished_raw")\""
  fi
  cat > "$status.tmp" <<EOF_STATUS
{
  "schema_version": 1,
  "stage_id": "$esc_stage",
  "phase": "$phase",
  "pid": $pid,
  "script": "$esc_script",
  "started_utc": "$started",
  "finished_utc": $finished_json,
  "exit_code": $code
}
EOF_STATUS
  mv "$status.tmp" "$status"
}

write_status RUNNING null
rc=1
finished=''
{
  print -- "DETACHED_STAGE_V1_BEGIN,$STAGE_ID,$started,$pid"
  zsh "$SCRIPT" "$@"
  rc=$?
  finished=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  print -- "DETACHED_STAGE_V1_END,$STAGE_ID,$finished,$rc"
} >> "$log" 2>&1

if [[ -z "$finished" ]]; then
  finished=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
fi
if (( rc == 0 )); then
  write_status SUCCEEDED "$rc" "$finished"
else
  write_status FAILED "$rc" "$finished"
fi
exit $rc
