# PREREG.md -- IVWC-EXPAND2: Self-checking verifier and law-change limits

Frozen: 2026-10-03. This document fixes the experimental design and
the kill bars K1..K9. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. The prereg
commit must strictly precede the implementation commit
(prereg commit-order self-check). Amending a bar after results
invalidates the verdict.

## 1. Research questions

IVWC (baseline, BUILD-PASS) showed a learner can commit to a
composition plus its own confidence BEFORE any outcome signal,
receive pure environmental consequences, and self-evaluate better
than its raw estimate on sealed cases (113 vs 116). IVWC-EXPAND
showed the learner can REVISE the composition itself from physics
evidence and have further consequences validate the revision
(sealed 235 vs 223). Its secondary arm S2 left open the problem
this experiment attacks: the learner's own belief-based estimate of
its improvement did NOT track actual gain. Two questions remain:

(a) SELF-CHECKING: can the learner verify its own work BEFORE
execution? A learner-owned verifier, trained ONLY on train
consequences, emits a pre-execution PASS/FAIL verdict on each
sealed plan. The verdict must discriminate sealed outcomes better
than trivial baselines, with no harness-supplied verdict at any
step.

(b) LIMITS: where does internal verification break? A deterministic
law-change dial varies the sealed world's wall density
(15% -> 30% -> 45%) while the verifier stays frozen from train.
Carried verification (knowledge frozen from an older world) must
degrade and eventually stop beating the trivial baseline. The
fresh-consequence revision protocol from IVWC-EXPAND is re-run at
each shift level for contrast: per-case evidence is fresh even
under law change, so the experiment separates "verification from
stale carried knowledge" (expected to break) from "verification
from fresh consequences" (expected to survive).

## 2. Frozen design

World/beliefs/composition/consequences/revision: copied VERBATIM
from ivwc_expand/src/ivwc_expand.zag (frozen parameters CW=20,
EBUD=36, PLANMAX=64, NTRAIN=24, NSEAL=12, RECW=41, RECM=16,
RECC=24, EREC=128; LCG s=(s*25173+13849)%65536 with mod-65536
entry reduction; world seed 7919*cid+13; belief seed
104729*cid+7; belief noise 12% wall flip / 15% item drop / 18%
phantom) EXCEPT world_gen takes a wall-probability parameter wp
(walls form where lcg%100 < wp). At wp=15 the sealed worlds
(cid 100..111) are BIT-IDENTICAL to the IVWC-EXPAND sealed worlds,
so K7 is an exact replication check (expected sealed sums 223 and
235). Train always uses wp=15.

Learner self-check (LEARNER section; sees only consequence-derived
data, never world truth):
- verifier_train(bkt[24], eff[24], n, vb): per-bucket
  (bucket = planned-gather bucket 0..3 from learner_compose meta)
  sum and count of train actual_eff, bucket means (integer
  division; empty bucket -> mean -1), and threshold T = total
  train eff sum / n, all computed by the learner from consequences.
  vb layout: bsum@0, bcnt@16, bmean@32, T@48 (4-byte cells).
- verifier_check(vb, bucket): returns 1 (PASS) iff bcnt[bucket] > 0
  and bmean[bucket] >= T, else 0 (FAIL). Empty-bucket verdicts are
  FAIL by construction (conservative: no data, no pass).
- actual_eff = 100*collected/max(1,energy_used), as in IVWC-EXPAND.

Phases in main (batched, in this order):
1. TRAIN SETUP (wp=15): harness builds truth+beliefs, cid 0..23.
2. TRAIN COMMIT: learner_compose on train beliefs. In-program
   counter asserts world_execute not yet called (K1-train).
3. TRAIN CONSEQ: world_execute on train P1 -> consequences.
4. VERIFIER TRAIN (learner): build vb from train (bucket, eff)
   pairs; build vb_shuf from the same pairs under deterministic
   rotation by 7 (ablation arm input).
5. SHIFT LOOP sh = 0..2, wp = 15/30/45, sealed cid 100..111,
   buffers reused across shifts:
   a. SEALED SETUP (this wp).
   b. SELFCHECK COMMIT (batched, all 12 before any sealed
      consequence of this shift): learner_compose on sealed
      beliefs. In-program counter asserts no world_execute since
      the previous phase boundary (K1-self[sh]).
   c. SELFCHECK VERDICT+CONSEQ: per case, verdict =
      verifier_check(frozen vb, bucket) BEFORE world_execute;
      then world_execute -> actual_eff. Metrics: n_pass,
      sum_eff_pass, n_fail, sum_eff_fail, accuracy acc =
      #(verdict == (eff >= T))/12, majority accuracy acc_maj =
      max(#(eff >= T), #(eff < T))/12. At sh=0 also the shuffled
      arm: verdicts from frozen vb_shuf -> acc_shuf.
   d. REVISION COMMIT1 (batched): learner_compose on sealed
      beliefs -> P1. In-program counter check (K1-rev[sh]).
   e. REVISION CONSEQ1: world_execute P1 -> C1 + evidence E1.
   f. REVISION REVISE+CONSEQ2: per case learner_revise with own
      evidence -> P2 -> world_execute -> C2; empty-evidence
      ablation -> P2_abl -> C2_abl. Metrics: sum_eff1,
      sum_eff2, sum_abl.

Secondary (reported, NOT frozen bars): per-case detail lines for
train and for each shift (selfcheck verdicts, revision effs);
bucket table and T; collected sums.

## 3. Frozen kill bars

- K1 (commit before signal, all phases): PASS iff all 7 in-program
  checks hold: world-call counter == 0 after TRAIN COMMIT;
  counter unchanged across each shift's SELFCHECK COMMIT and each
  shift's REVISION COMMIT1 (6 checks); AND the section-5 audits
  confirm code ordering (commit-phase learner_compose calls
  textually precede conseq-phase world_execute calls) and the
  learner section contains no world-truth tokens.
- K2 (consequence/evidence/verdict is not a disguised oracle):
  PASS iff the section-5 audits hold: no `expected|answer|key|
  target` tokens in src/ivwc_expand2.zag; no `correct|
  reference_plan|gold` tokens; every `==` in world_execute/w_step/
  w_left/w_right/w_gather compares against a physics constant,
  a map cell value, an action code, or a local flag; no reference
  plan exists; verifier inputs are (bucket, eff) pairs derived
  from executed consequences only; the threshold T is
  learner-computed from train consequences (no researcher-set
  constant anywhere in the verifier path).
- K3 (self-check discriminates, shift wp=15): PASS iff sealed
  n_pass > 0 and n_fail > 0 (both verdict classes non-empty) and
  sum_eff_pass * n_fail > sum_eff_fail * n_pass (strict; integer
  cross-multiplication for mean_pass > mean_fail).
- K4 (verifier beats the trivial baseline, shift wp=15): PASS iff
  sealed acc > acc_maj (strict), where the actual class of a case
  is (eff >= T) with the learner's own frozen T.
- K5 (determinism): PASS iff 3 runs produce byte-identical stdout
  (equal sha256).
- K6 (ablation: consequence CONTENT matters): PASS iff sealed
  acc_shuf < acc (strict) at wp=15, where acc_shuf uses the
  verifier trained on rotation-by-7 shuffled train pairs.
- K7 (revision replicates under stationarity, wp=15): PASS iff
  sealed sum(actual_eff_P2) > sum(actual_eff_P1) (strict). Because
  wp=15 sealed worlds are bit-identical to the IVWC-EXPAND sealed
  worlds and every function is copied verbatim, the expected
  values are 235 > 223; any deviation indicates an implementation
  divergence from the frozen predecessor.
- K8 (carried verification degrades under law change): PASS iff
  acc at wp=45 < acc at wp=15 (strict).
- K9 (break found): PASS iff acc at wp=45 <= acc_maj at wp=45
  (the frozen verifier no longer beats the trivial rule under
  strong law change).

Verdict: BUILD-PASS iff K1..K9 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar. VOID conditions: any
forbidden-interpreter invocation during the wave (PROCESS-FAIL per
governance), or any amendment to this prereg after implementation
begins.

## 4. What is NOT claimed

This is a mechanism test of self-checking and of verification
limits, not a composition-novelty claim and not an L3 claim. The
verifier is a deliberately simple fixed bucket table; the target
is the pre-execution self-verdict LOOP (train on consequences ->
frozen verdict -> sealed discrimination), not table novelty. The
NAV+GATHER composition and the revision rule are unchanged from
IVWC-EXPAND. No claim is made about cross-domain transfer or
representational invention. A K9 PASS establishes where THIS
verifier breaks (stale carried calibration under law change), not
that all self-checking must break there.

## 5. Frozen audit commands (run at report time, shell only)

A1 (K1 ordering): `grep -n "learner_compose(\|learner_revise(\|world_execute(" src/ivwc_expand2.zag`;
  every `learner_compose(` / `learner_revise(` call site inside a
  COMMIT-phase loop (phase comments `// Phase 2`, `// b.`,
  `// d.`) must have a smaller line number than every
  `world_execute(` call site inside the corresponding CONSEQ-phase
  loop (`// Phase 3`, `// c.`, `// e.`, `// f.`). Batched loops
  make this checkable per phase.
A2 (K1/K2 info hiding): `sed -n '/===== LEARNER =====/,/===== MAIN =====/p'
  src/ivwc_expand2.zag | grep -c "world_buf\|world_off"` must print
  0. (Consequence buffers cb/coff and evidence eb/eoff are
  consequence channels, as in the predecessors; only the truth
  buffers are banned from the learner section.)
A3 (K2 no oracle tokens): `grep -c -i -E "expected|answer|key|target"
  src/ivwc_expand2.zag` must print 0.
A4 (K2 no key comparison): `grep -n "correct\|reference_plan\|gold"
  src/ivwc_expand2.zag` must print nothing; every `==` in
  world_execute/w_step/w_left/w_right/w_gather compares against a
  physics constant (0/1/19/bounds), a map cell value, an action
  code, or a local flag; there is no reference-plan buffer;
  verifier_train/verifier_check take only (bucket, eff) arrays.
A5 (K5): three runs, `sha256sum` equality across
  runs/ivwc_expand2-run{1,2,3}.txt.

## 6. Design notes

Why the bars discriminate (each can fail):
- K3 fails if the verifier's buckets carry no sealed signal (empty
  class or wrong direction).
- K4 fails if the verifier cannot beat always predicting the
  majority class -- the honest trivial baseline for a PASS/FAIL
  self-check.
- K6 fails if shuffling train consequences does not hurt (then the
  table, not the content, would be doing the work).
- K7 fails on ANY divergence from the frozen predecessor
  (it is an exact replication probe, not just a direction check).
- K8 fails if law change does not degrade the frozen verifier
  (tie or improvement).
- K9 fails if the verifier remains super-majority under 45% wall
  density (a genuine robustness finding, reported as BUILD-FAIL).

Why wp=45 is expected to break the verifier: the verifier's bucket
means and T encode the wp=15 consequence regime (overconfident
beliefs, moderate collection). At wp=45 the corridor fragments,
plans bump far more, and actual_eff collapses across buckets while
T stays frozen high; verdicts calibrated to the old world
systematically misfire. The revision protocol, by contrast, uses
only per-case fresh evidence (bumps and misses remain truthful
physics under any wall density), so its sealed gain is expected to
stay positive -- the experiment thus separates stale-carried from
fresh-consequence verification. Both halves are reported whatever
the data says.
