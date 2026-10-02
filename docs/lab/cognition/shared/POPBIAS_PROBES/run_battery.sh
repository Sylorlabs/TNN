#!/bin/bash
# WS3-B battery harness.
# Usage: run_battery.sh <adapter_module> [outdir]
#   <adapter_module>: python module (dotted path, importable from cwd) exposing judge(probe).
# Runs the adapter twice over probes.jsonl, diffs for determinism, then scores.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ADAPTER="${1:?usage: run_battery.sh <adapter_module> [outdir]}"
OUT="${2:-$HERE/run_out}"
mkdir -p "$OUT"

run_once() {
  python3 - "$ADAPTER" "$HERE/probes.jsonl" "$1" <<'PYEOF'
import importlib, json, sys
mod = importlib.import_module(sys.argv[1])
rows = [json.loads(l) for l in open(sys.argv[2]) if l.strip()]
with open(sys.argv[3], "w") as f:
    for p in rows:
        r = mod.judge(p)
        f.write(json.dumps({"credence": r["credence"], "probe_id": p["probe_id"],
                            "verdict": r["verdict"]}, sort_keys=True) + "\n")
print("judged %d probes" % len(rows))
PYEOF
}

run_once "$OUT/verdicts_run1.jsonl"
run_once "$OUT/verdicts_run2.jsonl"
if ! cmp -s "$OUT/verdicts_run1.jsonl" "$OUT/verdicts_run2.jsonl"; then
  echo "PROCEDURE FAIL: adapter not deterministic (run1 != run2)"
  exit 2
fi
echo "determinism check: run1 == run2 (byte-identical)"
cp "$OUT/verdicts_run1.jsonl" "$OUT/verdicts.jsonl"
python3 "$HERE/scorer.py" "$OUT/verdicts.jsonl" | tee "$OUT/report.txt"
