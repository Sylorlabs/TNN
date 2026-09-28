#!/usr/bin/env python3
"""Score v2 sub-battery runs against PREREG2 bars, mechanically.

Reads runs/sub_<s>_rep1.log PROBE lines + the test jsonl expectations.
Verdict semantics (frozen):
  expected=value        -> verdict must be VALUE:<probe_value>
  expected=contradiction -> verdict must be CONTRADICTION
  expected=hedged       -> verdict must be HEDGED
  expected=unknown       -> verdict must be UNKNOWN
Also reports:
  value_leaks: number of VALUE verdicts on non-value expects
    (contradiction / neg-only / hedge-only probes)
"""
import json, re, sys

s = sys.argv[1]
test = [json.loads(l) for l in open(f"inputs2/sub_{s}_test.jsonl") if l.strip()]
exp = {r["id"]: (r.get("expect", r["probe_value"]), r["probe_value"]) for r in test}

n = 0; correct = 0; leaks = 0; missed = []
for line in open(f"runs/sub_{s}_rep1.log"):
    if not line.startswith("PROBE "):
        continue
    m = re.match(r"PROBE id=(\d+) verdict=(\S+) expected=(\S+)", line)
    if not m:
        continue
    pid, verdict, _ = int(m.group(1)), m.group(2), m.group(3)
    want, pval = exp[pid]
    n += 1
    if want == "value":
        got = int(verdict.split(":")[1]) if verdict.startswith("VALUE:") else None
        ok = got == pval
    elif want == "contradiction":
        ok = verdict == "CONTRADICTION"
    elif want == "hedged":
        ok = verdict == "HEDGED"
    elif want == "unknown":
        ok = verdict == "UNKNOWN"
    else:
        raise AssertionError(f"unexpected expect label {want}")
    if ok:
        correct += 1
    else:
        missed.append((pid, want, verdict, pval))
    if verdict.startswith("VALUE:") and want != "value":
        leaks += 1

print(f"{s}: {correct}/{n} correct, value_leaks={leaks}")
for pid, want, verdict, pval in missed:
    print(f"  miss id={pid} want={want} got={verdict} probe_value={pval}")
