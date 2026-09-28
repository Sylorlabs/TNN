#!/usr/bin/env bash
# V-QUAR CI check: no direct Q access outside the sanctioned paths.
# The raw readers qraw_read_path/qraw_read_file may be called ONLY from:
#   * read_file / read_path (the instrumented wrappers in qa_audit.inc)
#   * qread_claim           (the single Q accessor, MERGE binary only)
#   * qraw_read_path itself (its internal split calls qraw_read_file)
# Their definitions ("fn qraw_read_file(") are excluded. Anything else -> FAIL.
# Additionally: qread_claim/cmd_merge exist only in merge; qp_quarantine
# exists only in train.
set -u
cd "$(dirname "$0")"
fail=0
for src in webg_prod.zag webg_train.zag webg_merge.zag; do
  bad=$(awk '
    /^fn /{ fn=$2; sub(/\(.*/,"",fn) }
    /qraw_read_(path|file)\(/ && $0 !~ /^fn / {
      if (fn != "read_file" && fn != "read_path" && fn != "qread_claim" \
          && fn != "qraw_read_path" && fn != "qraw_read_file")
        print FILENAME":"FNR": in fn "fn": "$0
    }' "$src")
  if [ -n "$bad" ]; then
    echo "FAIL: $src has raw-reader call sites outside wrappers/accessor:"
    echo "$bad"
    fail=1
  fi
  n=$(grep -c "fn qread_claim" "$src" || true)
  case "$src" in
    webg_merge.zag) [ "$n" = "1" ] || { echo "FAIL: $src qread_claim count=$n (need 1)"; fail=1; } ;;
    *) [ "$n" = "0" ] || { echo "FAIL: $src defines qread_claim (only merge may)"; fail=1; } ;;
  esac
  nq=$(grep -c "fn qp_quarantine" "$src" || true)
  case "$src" in
    webg_train.zag) [ "$nq" = "1" ] || { echo "FAIL: $src qp_quarantine count=$nq (need 1)"; fail=1; } ;;
    *) [ "$nq" = "0" ] || { echo "FAIL: $src defines qp_quarantine (only train may)"; fail=1; } ;;
  esac
  nm=$(grep -c "fn cmd_merge" "$src" || true)
  case "$src" in
    webg_merge.zag) [ "$nm" = "1" ] || { echo "FAIL: $src cmd_merge count=$nm (need 1)"; fail=1; } ;;
    *) [ "$nm" = "0" ] || { echo "FAIL: $src defines cmd_merge (only merge may)"; fail=1; } ;;
  esac
done
if [ "$fail" = "0" ]; then
  echo "OK: no direct Q access; single accessor confined to merge binary"
fi
exit "$fail"
