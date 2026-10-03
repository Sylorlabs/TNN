# Track 6 · Slice 01 — Scale-leg ladder: 1x → 10x → 100x → 1000x

## 1. Slice
Design the scale-leg ladder: define the scale unit precisely, exact per-leg
configuration, what is held constant across legs, and per-leg pass bars with
sequential gating (each leg passes before the next runs).

## 2. Falsifiable claim
With decision rules frozen and only capacity parameters following measured
per-leg laws, scaling the RC machinery 1x → 10x → 100x → 1000x in *episodes*
produces no behavioral divergence: each leg reproduces the 1x verdict profile
(40/40 checks, byte-identical checkpoint replay, zero integrity regressions
against the RC3 corpus and wave5/6 trap set), while runtime and audit bytes
grow within preregistered envelope laws. Scale is a capacity exercise, not a
behavioral one. Any *behavioral* divergence that survives the capacity-distinguisher
falsifies the hypothesis — the ladder, not the trial, dies.

## 3. Design
**Scale unit (three dimensions scale differently — only one is "x"):**
- `x` = episode count / 12. 1x = 12 episodes (RC1 pilot, `wave7/reasoning-control/PREREG.md`),
  10x = 120, 100x = 1200 (RC3 passed), 1000x = 12000. "x" is DURATION ONLY.
- Capacity parameters (`RC_SMAX`, `IL_CAP`, `RC_AUDIT_CAP`, ledger window) are NOT x;
  they follow measured per-leg laws (RC3 precedent: `RC_SMAX` = 150 × x,
  `IL_CAP` = 128 × x rounded to power of two, set in leg-local copies —
  `wave10/rc3/PREREG_RC3.md` §§87/155).
- Concurrent-hypothesis count and memory-slot count are a third, untested
  dimension: the ladder makes NO claim about them.

**Per-leg configuration (identical machine, native Zag on Linux):**
- Phases mirror RC3: Phase A (V=1), self-change event (V 1→2 with replay of
  the leg's own recorded episodes), Phase B (V=2, R=8), 400-episode (1x-relative:
  400 × x/100? NO — verification mini-phase fixed at 400 episodes for all legs;
  at 1x the mini-phase is the instrument run, not part of scaling).
- Pre-leg requirement: a 1/10 checkpointed mini must complete on the leg's exact
  binary (RC3 §193 fallback equivalence rule). No mini, no leg.
- All audit entries use the 16-word layout (stage@52, d1@56, d2@60).

**HELD CONSTANT across legs (standing law):**
- Decision rules frozen: V/R parameters, commit/refuse/rollback thresholds,
  eliminative-verification logic, force-pin law, constitutional gates
  (100% reasoning machinery / 0% constitution).
- The 40 `CL_CHECK` battery: same checks, same bars, same per-check verdict
  semantics. Pass = 40/40 at every leg.
- No-RNG law, byte-identical replay from full logged state, audit schema.
- Memory-op rate bands: ops-per-episode must stay inside the 1x 99% CI band —
  drift is behavioral evidence, not capacity noise.

**Sequential gating:** leg N+1 may not start until leg N's verdict sheet is
signed PASS. A skip attempt voids the whole ladder. The 1000x leg is
additionally gated exactly like S100 was (five-organ precedent): no execution
without written approval referencing the 100x PASS.

## 4. Kill bar
- **K1 behavior:** any leg fails any of the 40 checks, and the failure persists
  after the capacity-distinguisher (re-run the failing window at doubled
  capacities, same x; if failure vanishes → capacity cause, re-leg at same x
  with amended law — one dated amendment allowed per leg; if it persists →
  behavioral) → the scale-invariant-decision-rules hypothesis is KILLED.
- **K2 replay:** any byte mismatch replaying input + full logged state at a
  checkpoint → leg void; if unrepaired after one dated fix, hypothesis dead.
- **K3 integrity regression:** any wave5/6 trap previously passed now fails,
  or ledger-byte divergence vs the RC3 corpus → hypothesis dead (integrity
  does not degrade with scale — law 2 of the program).
- **K4 op-rate drift:** memory ops per episode outside the 1x 99% CI band at
  any leg → behavioral divergence presumed; K1 distinguisher applies.
- **K5 envelope breach:** runtime or audit bytes/episode exceed the leg's
  preregistered envelope (fitted at 1x–100x, linear-in-x upper bound × 1.5
  headroom) → leg configuration dead, re-leg allowed; two envelope failures
  at the same x → scale leg abandoned at that x (report, don't bend).

## 5. Honesty notes
- The capacity/behavior distinguisher is the load-bearing judgment call: a
  resource failure with a proven identical-decision trace is configuration, not
  falsification — but the proof (byte-identical decisions up to the failure
  point) must be produced, not asserted. This is where builders will be tempted
  to bend; the one-amendment-per-leg rule is the guardrail.
- 12000 episodes × audit bytes may hit the znc 2^25-byte slice indexing limit;
  chunking is validated (AGENTS.md) but a new chunk-boundary at 1000x could
  expose an untested edge — the 1/10 mini catches it, not the leg.
- The ladder tests duration scaling only. It says nothing about slot-count or
  concurrency scaling, and nothing about the five-organ S100 leg, which stays
  separately gated. Do not let a 1000x PASS here be quoted as "TNN scales 1000x"
  in any other dimension.
- I am not claiming decision rules are *proven* frozen at 1000x — that is the
  hypothesis under test. K1–K4 are the instruments that would kill it.

## 6. Next build step
Build the 1x→10x pre-leg mini harness first: a single Zag binary plus the
1/10 checkpointed mini runner with the capacity-distinguisher automated
(failing window auto re-run at 2× capacities, diff decision traces byte-wise),
before any 100x/1000x leg is scheduled.
