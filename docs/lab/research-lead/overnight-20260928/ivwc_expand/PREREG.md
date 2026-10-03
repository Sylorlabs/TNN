# PREREG.md -- IVWC-EXPAND: Multi-step Internal Verification via World Consequences

Frozen: 2026-10-02. This document fixes the experimental design and
the kill bars K1..K6. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. The prereg
commit must strictly precede the implementation commit
(prereg commit-order self-check). Amending a bar after results
invalidates the verdict.

## 1. Research question

IVWC (baseline, BUILD-PASS at C361) showed a learner can commit to a
composition output plus its own confidence BEFORE any outcome signal,
receive pure environmental consequences, update its own calibration
from those consequences, and predict sealed future performance better
than its raw estimate. This experiment asks the harder multi-step
question: can the learner commit to a composition, receive world
consequences, REVISE the composition itself from those consequences
(not just its confidence), and have the FURTHER consequences of the
revised composition validate the revision -- with no harness-supplied
expected answer at any step? This is Micah's priority #4 (reduce
dependence on harness-supplied expected answers) extended from
calibration to revision.

## 2. Frozen design

World: identical to the IVWC baseline (frozen parameters copied
verbatim): 1D corridor of 20 cells (0..19), ground truth = wall map
(20 bytes), item map (20 bytes), start cell; energy budget E=36.
Deterministic LCG `s = (s*25173 + 13849) % 65536` with state reduced
mod 65536 on entry (no i32 overflow). World seed `7919*cid + 13`,
belief seed `104729*cid + 7`. world_gen: cells 0 and 19 forced open;
other cells wall with probability 15%; open cells hold an item with
probability 25%; start = first open cell at or after `2 + lcg % 16`
(wraps). belief_gen (harness setup only, learner never sees truth
afterward): copy truth, wall belief flips 12% (never start), true
items dropped 15%, empty true-open cells gain phantom item beliefs
18%, start believed exactly. Train cases cid 0..23 (N_TRAIN=24);
sealed cases cid 100..111 (N_SEALED=12). Same case identities as the
baseline for comparability.

Learner composition (learner_compose, sees ONLY beliefs): the
baseline NAV+GATHER composition, reused unchanged. Visit
believed-item cells in increasing cell order; skip any whose
believed-open interval from the believed position holds a believed
wall; otherwise append unit moves toward it, then one GATHER.
Truncate to E=36 actions. Outputs: plan bytes (0=LEFT, 1=RIGHT,
2=GATHER; at most 64), g = planned gathers, L = plan length,
raw_conf = 100*g/max(1,L).

World consequences (world_execute, sees truth + plan only): steps
the plan through corridor physics exactly as the baseline. Each
action costs 1 energy. Consequence buffer: collected, energy_used,
bumps, wasted_gathers, final_pos, plan_len. NEW: a per-action
evidence log, 2 bytes per action (position byte, outcome byte),
outcome in {0=MOVE_OK, 1=BUMP_LEFT, 2=BUMP_RIGHT, 3=GATHER_HIT,
4=GATHER_MISS}. Evidence entries are physics outputs recorded during
stepping: a bump is a failed move (physics), a gather hit/miss is
item presence/absence (physics). There is NO key, NO expected plan,
NO reference output anywhere in the program. A "wrong" plan still
produces perfectly well-defined consequences and evidence.

Learner revision (learner_revise, sees ONLY its beliefs, its
committed plan P1, and the evidence log): copy beliefs, then apply
evidence. GATHER_MISS at cell p: the item belief at p is phantom, so
clear it (a miss is truthful: within one execution each cell is
gathered at most once, so a miss means the cell truly holds no
item). BUMP_LEFT at p (p>0): cell p-1 is truly a wall, so set the
wall belief (a bump is truthful: the move failed on physics).
BUMP_RIGHT at p (p<19): symmetric. Then learner_compose on the
revised beliefs yields the revised commitment P2 with its own
(g2, L2, raw_conf2). Revision inputs are (beliefs, P1, evidence)
only; no world truth reaches this function.

Phases in main (batched, in this order):
1. SETUP: generate truth+beliefs for 24 train cases.
2. COMMIT1 (train): learner_compose on train beliefs -> P1/meta1.
   In-program counter asserts no world_execute call has happened yet
   (K1a).
3. CONSEQ1 (train): world_execute on committed P1 plans ->
   consequences C1 + evidence E1.
4. REVISE (train): learner_revise on (beliefs, P1, E1) -> P2/meta2.
   In-program counter asserts world_execute was not called during
   this phase (K1b). In-program check that at least one train case
   has P2 != P1 (K3).
5. CONSEQ2 (train): world_execute on P2 plans (fresh episode on the
   same truth; the simulator keeps no cross-episode state) -> C2.
6. SEALED SETUP: fresh truth+beliefs for 12 sealed cases.
7. SEALED COMMIT1: learner_compose on sealed beliefs (all 12 before
   any sealed consequence).
8. SEALED CONSEQ1: world_execute on sealed P1 -> C1/E1.
9. SEALED REVISE+CONSEQ2: per sealed case: learner_revise with its
   own evidence -> P2, world_execute -> C2; ablation arm:
   learner_revise with an EMPTY evidence log -> P2_abl (honest
   null-revision: with no evidence the beliefs are unchanged, so
   P2_abl is byte-identical to P1), world_execute -> C2_abl.

Secondary (reported, NOT frozen bars): S1 shuffled-evidence arm --
sealed revision using another sealed case's evidence (deterministic
rotation by 5), to show the content of the evidence matters, not
just the act of revising. S2 gain prediction -- the learner's own
estimate of its improvement, pred_gain = raw_conf2 - raw_conf1, vs
the actual gain act_gain = actual_eff2 - actual_eff1, reported as
sealed sum|pred_gain - act_gain| vs sealed sum|act_gain|, where
actual_eff = 100*collected/max(1,energy_used). S3 collected sums.

## 3. Frozen kill bars

- K1 (commit before signal, both steps): PASS iff (a) the in-program
  world-call counter equals 0 immediately after the train COMMIT1
  phase, (b) the in-program counter is unchanged across the train
  REVISE phase (no world_execute during revision), AND the
  section-5 audits confirm code ordering (all train learner_compose
  calls precede all train world_execute calls of CONSEQ1; all train
  learner_revise calls precede all train world_execute calls of
  CONSEQ2) and the learner code section contains no world-truth
  tokens.
- K2 (consequence/evidence is not a disguised answer check): PASS
  iff the section-5 audits hold: no `expected|answer|key|target`
  tokens in src/ivwc_expand.zag; world_execute/w_step perform no
  plan-to-key comparison (their only comparisons are physics:
  bounds, wall presence, item presence, action dispatch); evidence
  entries are (position, outcome) pairs recorded from physics
  stepping; no `correct|reference_plan|gold` tokens; there is no
  correct-plan buffer in the program; learner_revise's inputs are
  (beliefs, P1, evidence) only.
- K3 (revision acts on consequences): PASS iff the in-program check
  finds at least one train case whose revised plan P2 differs from
  P1 (length or any plan byte).
- K4 (revised commitment validated by further consequences): PASS
  iff sealed sum(actual_eff_P2) > sealed sum(actual_eff_P1)
  (strict, integer), where actual_eff = 100*collected /
  max(1,energy_used) measured from executing each plan on the
  identical sealed physics. Efficiency (not raw collected) is the
  frozen metric because the revision's truthful evidence provably
  makes per-case eff2 >= eff1 (phantom/wall corrections can only
  remove wasted actions and never remove a truly-collected item;
  see section 6), so the bar reduces to "at least one sealed case
  revises", which the evidence rates make near-certain; collected
  sums are reported as secondary S3.
- K5 (determinism): PASS iff 3 runs produce byte-identical stdout
  (equal sha256).
- K6 (ablation): PASS iff sealed sum(actual_eff_P2) >
  sealed sum(actual_eff_P2_abl) (strict, integer). Declared openly
  here (not discovered post-hoc): the empty-evidence ablation's
  revised plan equals P1 by construction (no evidence -> beliefs
  unchanged -> identical recomposition), so K6 tests the same
  integer inequality as K4 through the necessity-of-feedback
  framing; the independent evidence that evidence CONTENT matters
  is the secondary shuffled arm S1.

Verdict: BUILD-PASS iff K1..K6 all PASS. Any FAIL yields BUILD-FAIL
naming the failed bar. VOID conditions: any forbidden-interpreter
invocation during the wave (PROCESS-FAIL per governance), or any
amendment to this prereg after implementation begins.

## 4. What is NOT claimed

This is a mechanism test of multi-step internal verification, not a
composition-novelty claim and not an L3 claim. The NAV+GATHER
composition and the revision rule are deliberately simple and
learner-side-fixed; the target of the experiment is the commit ->
consequence -> revised-commit -> further-consequence loop with no
harness-supplied expected answers. No claim is made about
cross-domain transfer or representational invention.

## 5. Frozen audit commands (run at report time, shell only)

A1a (K1 commit-1 ordering): `grep -n "learner_compose(\|learner_revise(\|world_execute(" src/ivwc_expand.zag`;
  the last `learner_compose(` line inside the train COMMIT1 phase
  must have a smaller line number than the first `world_execute(`
  line inside the train CONSEQ1 phase (phase comments
  `// Phase 2: train COMMIT1` / `// Phase 3: train CONSEQ1` delimit).
A1b (K1 revision ordering): the last `learner_revise(` line inside
  the train REVISE phase must have a smaller line number than the
  first `world_execute(` line inside the train CONSEQ2 phase (phase
  comments `// Phase 4: train REVISE` / `// Phase 5: train CONSEQ2`
  delimit).
A2 (K1/K2 info hiding): extract the LEARNER section (between the
  `// ===== LEARNER =====` and `// ===== MAIN =====` markers) and
  confirm zero occurrences of `world_buf` / `world_off`:
  `sed -n '/===== LEARNER =====/,/===== MAIN =====/p'
  src/ivwc_expand.zag | grep -c "world_buf\|world_off"` must print 0.
  (The evidence buffer `eb`/`eoff` is a consequence channel, like
  the baseline's consequence buffer; only the truth buffers are
  banned from the learner section.)
A3 (K2 no answer tokens): `grep -c -i -E "expected|answer|key|target"
  src/ivwc_expand.zag` must print 0. (The words appear in this
  PREREG.md and in REPORT.md discussion only, never in the program.)
A4 (K2 no key comparison): `grep -n "correct\|reference_plan\|gold"
  src/ivwc_expand.zag` must print nothing; every `==` in
  world_execute/w_step/w_left/w_right/w_gather compares against a
  physics constant (0/1/19/bounds), a map cell value, or an action
  code; there is no correct-plan buffer in the program.
A5 (K5): three runs, `sha256sum` equality.

## 6. Design note: why K4 is safe by construction

The revision only ever (a) clears an item belief where a gather
MISSED, and within one execution each cell is gathered at most once,
so a miss means the cell truly holds no item; (b) sets a wall belief
where a move BUMPED, and a bump means the adjacent cell is truly a
wall (or the corridor edge, which is guarded). Both corrections are
truthful: P2's believed-item set is P1's minus proven phantoms, and
P2 additionally avoids proven walls. learner_compose visits
believed items in increasing cell order, so P2's plan is P1's plan
with wasted actions removed: L2 <= L1, and every true item P1
collected is still targeted and reached by P2 (a shorter prefix to
each common cell under the same E=36 truncation), so
collected2 >= collected1 per case. Hence per-case
actual_eff2 = 100*collected2/max(1,L2) >= 100*collected1/max(1,L1)
= actual_eff1, with strict inequality for the sealed sum iff at
least one sealed case revises. With 12%/18% belief noise, the
probability that zero of 12 sealed cases produce any bump or
phantom gather is negligible, so the strict bar is safe without
being tuned to any seed.
