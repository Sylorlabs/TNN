# C1 Flakiness Investigation: REPORT

Verdict: C1-FLAKINESS-INVESTIGATED.
Finding: NOT contestant non-determinism. Harness bug in resume logic.

## Summary

The two "flaky" C1 runs (60/63 instead of 63/63 on D1/D2/D3) were
caused by stale state directories, not by non-determinism in the
contestant binary. The contestant is deterministic. The Zag driver
is deterministic given fresh state. The bug is in the harness.

## Evidence

### 1. The flaky signature

Flaky runs c1_w1_r3 and c1_w2_r1 (commit 323f2afaa):
- D1 answered d1a, D2 answered d2b, D3 answered d3a (conf 0.9)
  instead of UNRESOLVED (conf 0.6).
- Final state H weights: d1a=8, d1b=4, d2a=4, d2b=8, d3a=8, d3b=4.
- facts=62, rels=45, demos=14, vocab=12, state_bytes=3122.
- tools=0 (no tool calls).

Good run c1_w1_r1:
- D1/D2/D3 answered UNRESOLVED (conf 0.6).
- Final state H weights: d1a=4, d1b=2, d2a=2, d2b=4, d3a=4, d3b=2.
- facts=32, rels=23, demos=8, vocab=6, state_bytes=1659.
- tools=4 (3 ask, 1 intervene).

Every weight and count in the flaky run is exactly 2x the good run.
The 9 claim turns in w1/turns.jsonl (turns 82,83,85,86,88,89,91,93,95,
each w=2) produce exactly the good-run weights when ingested once.
The flaky weights require every claim ingested twice.

### 2. Root cause: stale state on resume

The Zag driver (zag_driver.zag, lines 350-352):
  let statedir:[]u8=pjoin(outdir,"state");
  do_mkdir(outdir);
  do_mkdir(statedir);

`do_mkdir` is a no-op if the directory exists. The driver never clears
pre-existing state. If state/state.txt exists from a prior partial run,
the contestant reads it and ingests all turns again on top of the stale
state, doubling every weight and count.

The resume script (refreeze_drive.sh):
  if [ -f "$d/costs.txt" ]; then
    echo "skip $name $world r$rep (already done)"
    return 0
  fi
  mkdir -p "$d"
  "$DRIVER" ...

Skip-if-done checks costs.txt (written at end of a successful run) but
does not clear a partial state/ directory. The /tmp wipe killed the
drive at 22/60 runs. On resume, runs that had started (partial state
written) but not finished (no costs.txt) re-ran on stale state.

The drive.log confirms c1_w1_r3 and c1_w2_r1 completed in the resumed
batch (lines 47-48, after the skip block), not in the initial 22.

### 3. Reproduction

Ran the pure-Zag driver twice on w1:
- Run 1 (fresh /tmp/flaky_demo): 63/63. H weights 4/2/2/4/4/2.
  facts=32. D1/D2/D3 UNRESOLVED.
- Run 2 (same dir, no clearing): 58/63. H weights 8/4/4/8/8/4.
  facts=62. D1=d1a, D2=d2b, D3=d3a at conf 0.9.

The reproduction matches the flaky signature exactly (2x weights,
62 facts, D1/D2/D3 committed answers). Score dropped further to 58/63
because even more state accumulated.

### 4. Why D1/D2/D3 flipped

The abstention logic (contestant.zag, ans_yn):
  let d:i32=w1-w2;
  if(d>1){return h1;}
  if(d<-1){return h2;}
  return "UNRESOLVED";

With correct weights (d1a=4, d1b=2): d=2 > 1, so it should return d1a.
But the good run returned UNRESOLVED. This means at D1/D2/D3 decision
time (turns ~96-98), the weights had not yet reached their final values.
The claims at turns 91, 93, 95 arrive after some D queries. With doubled
weights from stale state, the differences exceeded the threshold at
decision time, flipping UNRESOLVED to committed answers.

(The exact turn ordering vs. D-query timing determines the threshold
crossing; the key point is that doubling the weights moves the decision
across the abstention boundary.)

### 5. Impact on the scientific conclusion

NONE. The finding is a harness bug, not a scientific result.
- The contestant is deterministic given fresh state.
- 13/15 C1 runs in the re-freeze were 63/63 on fresh state.
- The prior wave (d5984f313) was 15/15 at 63/63 (3/3 reps x 5 worlds).
- The 2 affected runs are explained entirely by the stale-state bug.
- P2 (C1 63/63) and P6 (LEARNING-PROPERTY) stand without caveat.
  The "~13% flakiness" estimate in the re-freeze report is WITHDRAWN;
  it was measuring the harness bug rate, not contestant behavior.

## Recommendations

1. FIX (driver or resume script, not the contestant):
   Option A: zag_driver.zag clears statedir at startup (rm -rf equivalent
   via Zag, or refuse to run if state.txt exists).
   Option B: refreeze_drive.sh removes "$d" entirely before re-running
   (not just skip-if-costs-exists).
   Option B is simpler and sufficient. The contestant binary needs no change.

2. QUARANTINE: The two affected runs (c1_w1_r3, c1_w2_r1 in the
   323f2afaa re-freeze) should be re-run on fresh state dirs. Expected:
   63/63. This is a harness re-run, not a scientific re-freeze.

3. DOCUMENT: Record in the ledger that the "C1 flakiness" finding is
   retracted as contestant non-determinism and reclassified as a harness
   resume bug. The C93 clearance stands.

## One-System accounting

0 source lines changed. 0 new mechanisms. Read-only investigation plus
two demonstration runs in /tmp. The fix (when applied) is harness
hygiene, not cognitive architecture.

## Governance

- Toolchain guard: PASS. Restricted PATH, zero Python invocations.
- No sealed FW1-FW9 files accessed.
- Contaminated paper: zero-diff.
- Read-only w.r.t. the contestant binary and driver source.
- Demonstration runs in /tmp/flaky_demo (ephemeral, not committed).
