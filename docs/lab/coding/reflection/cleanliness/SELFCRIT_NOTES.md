# CLN-1 self-critique probe (amended design: the actual learner, not an authored judge)

**Question:** can the current mainline learner itself distinguish clean from dirty
code, or does it merely produce relatively clean code without explicit
cleanliness knowledge?

**Method (deterministic, no RNG):**
- `work/dirty_inject.py` injects two semantics-preserving dirt items into TNN's
  own passing sources: an uncalled fn `tnn_unused_probe` and an unused local
  `tnn_unused_local`. Applied to CLN-G2, CLN-G4, CLN-T2 (all M1=2 clean).
- Dirtied variants verified: compile with pinned znc, byte-match frozen test
  outputs, checker M1 drops 2 → 1 (2 dead-code instances). Dirt is real and measurable.
- Probe A (direct): `learner diagnose` (the actual deliberative classifier) on
  clean vs dirty with IDENTICAL TEST-pass evidence envelopes.
- Probe B (loop): `driver.py --budget 4` repair loop on the dirtied seeds.

**Results:**
- Probe B: all 3 dirtied seeds `outcome=pass`, `iters_used=1`, `evtype=NONE` —
  the loop compiles, tests pass, accepts the dirty source UNCHANGED. `diagnose`
  is never invoked on passing code. (report: `work/selfcrit/driver_dirty_run.json`)
- Probe A (G2, G4): DIAG classification lines byte-identical for clean vs dirty:
  `DIAG class=OUTPUT_FORMAT strategy=halt-no-patch score=7 evals=3
  trace=FORMAT+7:equal-modulo-trailing-ws;`
  The `@@SRC@@` sections echo each input back UNCHANGED — zero cleaning performed
  on the dirty variant. (raw: `work/selfcrit/diag_{clean,dirty}_{g2,g4}.txt`)

**Verdict:** the current mainline learner has NO explicit cleanliness judgment.
Its interface (teach/gen/repair/gate/delib/diagnose/precheck) contains no
ranking or cleanliness action; its failure taxonomy (SYNTAX NAME ARITY TYPE
DUPFN GEN_FAILURE RUNTIME OUTPUT_FORMAT LOGIC_VALUE LOGIC_OTHER UNKNOWN)
contains no cleanliness class; and its deliberation treats a dirty-but-passing
program as equivalent to the clean original. It produces relatively clean code
as a byproduct of its generation patterns, but it cannot tell clean from dirty.
Self-critique score: 0/2 probes show any cleanliness discrimination.
