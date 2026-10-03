# PREREG: Matched-RNG follow-up to COGOPS-ADAPTIVEPLEN K4 FAIL

Frozen before implementation. 2026-10-03. Worker: COGOPS-ADAPTIVEPLEN-RNG.
Non-ledger task (claim minting paused).

## Question

COGOPS-ADAPTIVEPLEN reported verdict INCOMPLETE: K1-K3, K5-K12 PASS,
K4 FAIL (informative). The K4 bar (A-FULL revise_trials <
create_trials) failed: adaptive revise cost 284 trials plus one
failed 368-trial attempt (best=0, no adopt) vs fixed-3's 188.

Hypothesized mechanism: the adaptive ramp leaves the revise search
under-pressured -- plen is still 1 during revise-search (it becomes 2
only after revise-compression), vs 3 for fixed. Weaker pressure
retains longer variants, diluting the targeted single-slot etype fix
(imm 5->6) across more slots; the first attempt exhausted the
30-generation budget without sampling it.

Preregistered confound: the two arms shared RNG seeds at arm start
but diverged in RNG consumption before revise, so the 284-vs-188 gap
mixes treatment (plen value) with RNG path. The second attempt at
the same plen=1 succeeded in 284, so the first-attempt failure may be
partly RNG-path artifact.

This lane runs the proposed matched-RNG follow-up: paired revise
searches at fixed plen=1 vs plen=3 from the same seed body and the
same RNG state, to discriminate treatment effect from RNG-path
artifact and to test the hypothesized mechanism.

## Design (pure Zag, pinned znc, safebin)

Base: ap.zag from cogops_adaptiveplen (commits c06ee6d01 /
0086f982d / 702e15b97; cited, not re-derived). The ONLY new code is
a matched-RNG driver plus reporting-only instrumentation. No change
to the interpreter, worlds, graded replay, constructor operators,
composite fitness, plen_of, compression, or adopt bars.

### Paired design

N=8 RNG pairs (k=0..7). Within pair k, two revise-search runs:

- P1: plen fixed = 1 during the revise search. Implemented as
  pmode==3 with learner cell 2370 preset to 1. (plen_adapt no-ops:
  it returns immediately when cell 2370 != 0. The inversion
  diagnostic counts but changes nothing.) This reproduces the
  adaptive arm's exact revise-phase state (pmode 3, plen 1).
- P3: plen fixed = 3 during the revise search. Implemented as
  pmode==2 (plen_of returns 3; PARSIMONY-exact). This reproduces
  the fixed arm's revise-phase state.

Pair seeds (deterministic, documented):
- env_seed(k)   = 123456789 + k*104729   (rng_env, cell 238)
- learn_seed(k) = 987654321 + k*7919     (rng_learn, cell 239)

Within a pair, P1 and P3 start the revise search with IDENTICAL
RNG stream states, identical learner state, and identical seed
body. The ONLY difference between arms is the plen coefficient in
the composite fitness. Any systematic cost difference across the 8
pairs is therefore a treatment effect, not an RNG-path artifact.

### Setup per run (identical within pair)

1. Fresh S (16384 B), BC (4096 B). Seeds as above.
2. build_bodies (innate op bodies; slot-5 pointer 512).
3. Policy init to 1s (cells 2200/2208/2272/2280), as in lb_arm.
4. Shift flag on: cell 2293 = 1 (post-shift N3 world, etype 6).
5. 40 post-shift episodes: run_ep(S,BC,400+e,0) for e=0..39.
   Fills snapshot rings, shapes policy/IMMC identically in both
   arms. No create/revise calls during setup.
6. Install seed body at BC 512: the exact pre-shift-optimal
   6-instruction body (pre-revise state in the original run):
   SET R0,5 / MATCH R7,R0->R1 / SET R4,1 / READF R1,R4->R5 /
   SET R6,2 / YIELD R6,R5. Cell 815 (slot-5 length) = 48.
7. bias_imm_from_snaps(S); collect_sources(S); policy_seed(S,BC).
8. Sanity: cur = graded_replay(seed body); expected 100 in every
   run (matches the original REVISE-TRIED cur=100: the unfixed
   body replays 100 post-shift).

### Revise search (the treatment)

Identical to try_revise's search phase, minus the plen update
(this lane holds plen FIXED to isolate the coefficient):

- construct_init_rev(S,BC) (seed body + 7 mutated copies)
- construct_gens(S,BC,30,arm=1,xfer=1) (30-generation budget,
  12 offspring/generation, graft enabled iff ns>0)
- Adopt rule (unchanged): bi=best_passer_idx(S); adopt iff bi>=0
  and best > cur+150. trials = cell 858.

### Reporting-only instrumentation

Inside construct_gens, at the end of each generation, emit (only
when driver flag cell 2399 == 1; no behavioral effect):

- GEN g sumlen=<sum of member nin> bestraw=<max raw replay>
  fixcount=<members containing a SET R0,6 instruction
  (op==1, a==0, imm==6): the single-slot etype fix>

Analysis derives per run: trials-to-adopt, adopted (0/1),
first-passer generation, mean population length over
generations, fix-presence trajectory.

### RNG-match self-check (binary-enforced)

The driver records rng cells 238/239 at revise start for P1
(cells 2400/2401) and requires P3's values to be identical;
any mismatch emits RNG-MISMATCH and voids that pair. Expected:
8/8 RNG-MATCH=1 (setup is deterministic and identical).

## Metrics

Per arm-run:
- cost = trials if adopted, else 369 (one more than the maximum
  possible 8+30*12=368; no-adopt is strictly worse than any adopt)
- adopted (0/1), trials, best, firstpass (first generation with a
  raw>=850 member; 31 if none), meanlen (mean over generations of
  mean member length in instructions)

Paired comparisons (P1 vs P3 within each of the 8 pairs).

## Kill bars (checked from run logs; MR3/MR4 by build.sh)

- MR1 REPLICATE (primary): P1 cost > P3 cost in >= 6 of 8 pairs
  (paired sign) AND mean(P1 cost)/mean(P3 cost) >= 1.25. Both
  conditions required for PASS.
- MR2 MECHANISM: (a) meanlen(P1) > meanlen(P3) in >= 6 of 8 pairs
  (P1 retains longer variants: the under-pressure signature);
  AND (b) firstpass(P1) > firstpass(P3) in >= 6 of 8 pairs
  (the fix is found later under weaker pressure). Both required.
- MR3 DETERMINISM: 3/3 runs byte-identical (sha256 recorded).
- MR4 GUARDS: build.sh asserts: zero `python`, zero `as *i32`,
  zero `_MODE` tokens, interpreter dispatch exactly opcodes 1..8,
  zero `while.*!(` patterns, single main.
- MR5 SETUP-SANITY: 8/8 pairs RNG-MATCH=1 (binary self-check);
  AND seed-body cur replay == 100 in all 16 arm-runs.

OVERALL verdict mapping (all bars checked as frozen):
- MR1 PASS + MR2 PASS (+MR3/MR4/MR5 PASS): K4 FAIL REPLICATES as
  a TREATMENT EFFECT; mechanism confirmed (under-pressured
  revise search at plen=1). -> BUILD-PASS.
- MR1 PASS + MR2 FAIL: the gap replicates but the hypothesized
  mechanism is NOT confirmed (some other plen-1 effect).
  -> INCOMPLETE (mechanism open).
- MR1 FAIL: the gap does NOT replicate under matched RNG; the
  original K4 FAIL is attributed to RNG-path artifact (with the
  N=8 power caveat stated). -> INCOMPLETE (negative result).
- MR3 or MR4 or MR5 FAIL: PROCESS-FAIL (rerun cleanly).

## Tradeoff analysis (preregistered, reported regardless of verdict)

- Per-pair table: P1 vs P3 trials, adopted, best, firstpass,
  meanlen, fixcount trajectory summary.
- Sign counts and mean cost ratio for MR1; sign counts for MR2a/b.
- No-adopt event counts per arm (the original's failed 368-trial
  attempt is the phenomenon of interest: does it recur more under
  P1?).
- Whether the fix (SET R0,6) is sampled but loses composite
  selection under P1 (exploratory mechanism detail).

## Honest boundary (preregistered)

Expected level: L2 structural learning, not L3. Same
researcher-owned/learner-owned split as COGOPS-ADAPTIVEPLEN; this
lane adds no new learning claim, only a causal discrimination.

What this experiment does NOT do:
- It tests fixed plen=1 vs fixed plen=3, not the full adaptive
  0->1->2 trajectory. The plen=1 value is exactly the adaptive
  arm's revise-phase state, so this isolates the hypothesized
  mechanism, but a full-trajectory replication is a separate
  (larger) experiment.
- The starting state is synthetic (40 post-shift episodes, not
  the original 474-episode history). Absolute trial counts are
  expected to differ from the original; the inference is on the
  RELATIVE paired difference, which is what the confound
  threatened.
- N=8 pairs gives modest power. A null result (MR1 FAIL) is
  reported as "fails to replicate under matched RNG" with the
  power caveat, not as proof of no effect.
- Within-search RNG paths still diverge between arms (treatment
  changes the search path, hence subsequent draws). The matched
  design controls the RNG state AT revise start; averaging over
  8 pairs controls within-search luck. This is the standard
  paired-trial rationale, stated here so it is not mistaken for
  a stronger claim.
