# REPORT: L2-L3 Adversarial World (RELAY)

Worker: Adversarial L2-L3 Worker (subagent, 2026-10-02).
Prereg: `l2_l3_adv/PREREG.md`, frozen alone at commit 4f87b09e6
before any implementation existed. No amendments.

## Verdict

**L2-L3-ADV-COMPLETE.** All six kill bars PASS, no falsifier fired,
3/3 byte-identical.

## What was built

A standalone pure-Zag experiment reusing the MEADOW learner
(`learner.zag`) byte-identical (sha256
338c462287661c13ea02e06fc0b8f57dda2f567c4db68c5ebc3d0b2b89117c6b,
verified with cmp) plus adversary-designed experiment side
(`world.zag`, `driver.zag`), assembled as
`cat learner.zag world.zag driver.zag > adv_full.zag` (807 lines) and
compiled with the pinned znc to `adv_bin`. The learner holds: X
episode recall with a learned replay length (L=4 from old 4-reading
protocol episodes), the L2 EXTEND standing rule (replay continues past
L while continuation slots are filled, up to 2 extra slots, firing on
structural preconditions, never researcher-selected per problem), Y
threshold decide on scalars, and the L3 greedy constructor over the
frozen op basis {CPY,ADD,SUB,MAX,MIN} on 6 registers (180
candidates/round, first-max tie-breaking, ascending threshold
sweeps). ADAPT_ON is a driver-set causal-control flag (the
composition_l2 adapt_on precedent), never written by the learner.

The hidden world rule (driver side only, designed by this worker
independently of the MEADOW builder): a relay link is STABLE iff the
overnight signal climb e5-e1 >= 5. The decisive reading e5 sits in
slot 5, unreachable without the L2 extension. A trap episode (id 8:
e5=8 yet UNSTABLE because e1=4) forces the second invented
instruction: e5 alone reaches only 7/8.

## Kill-bar results (from adv_run1.txt, reproduced in runs 2 and 3)

- K-CB-1 (both required): L2-ONLY 0/4, L3-ONLY 0/4, FULL 4/4. PASS.
- K-CB-2 (L2-only fails): Z-L2ONLY 0/4 with ADAPT-STAT ext=8.
  Adaptation genuinely fired (Z lines show 6-reading replays) but is
  insufficient without the novel intermediate. PASS.
- K-CB-3 (L3-only fails): Z-L3ONLY 0/4 with ext=0 and constructed M
  n=0. Construction trace: `C-ROUND 1 base=4 eval=180 stop`. The
  prereg's pairing proof holds: train projections pair
  stable/unstable episodes byte-identically on the first 4 readings,
  so no candidate can beat the 4/8 empty baseline. PASS.
- K-CB-4 (combined succeeds with provenance): Z-FULL 4/4,
  ADAPT-STAT-FULL ext=4352, M-STATE n=2 prog=0,0,5,2,0,1,... printed
  from learner state, and every Z line shows a 6-reading replayed
  sequence (adapted X' in the trace). The invented intermediate is
  M = [CPY R0,R5, SUB R0,R1] (R0 = e5, then R0 -= e1), t=5, train
  8/8. Construction trace matches the frozen hand derivation exactly:
  round 1 win=0,0,5 gain=3 score=7 t=5; round 2 win=2,0,1 gain=1
  score=8 t=5; round 3 stop. PASS.
- K-CB-5 (M not in source): all 11 frozen grep patterns return 0 hits
  on learner.zag (`e5-e1`, `CPY R0,R5`, `SUB R0,R1`, `0,0,5`,
  `2,0,1`, `021308`, `0,2,1,3,0,8`, `relay`, `threshold.*=.*5`,
  `_MODE`, case-insensitive `bridge`). PASS.
- K-CB-6 (determinism): adv_run1/2/3.txt sha256 identical
  (d161cbc7c3f4011fb4f9999dcfac540942c3439d7b53adc4693c2b097fd52217
  all three). PASS.

No falsifier fired: F-NO-CREATE, F-NO-EXTEND, F-L2-SUFFICIENT,
F-L3-SUFFICIENT, F-FRESH-PASS (Z-FRESH 0/4), F-OP-EXPAND, F-AUDIT,
F-NONDET, F-PYTHON all silent.

## Why this is L2 and L3 together

- L2: X's replay procedure was learned on 4-reading episodes (L=4).
  On 6-reading episodes the EXTEND standing rule adapts the procedure
  (X -> X') purely on the structural precondition of filled
  continuation slots. The ARM-L2-ONLY arm proves the adaptation is
  real (ext=8, 6-reading replays in the trace) and proves it is not
  enough (0/4).
- L3: M = [CPY R0,R5, SUB R0,R1] was not in source (K-CB-5 audit
  clean), was constructed after experience through the white-box
  greedy trace, and is causally necessary (removing M in ARM-L2-ONLY
  collapses Z to 0/4). The ARM-L3-ONLY arm proves the invention
  cannot happen without the adapted X' (pairing proof: 4-reading
  projections are label-uninformative, construction halts with n=0).

## Adversarial independence

The hidden rule (e5-e1 >= 5, a temporal difference), the episode
tables, the trap episode, the Y prior (t=5), and every hand-derived
expectation in the prereg were designed by this worker, not by the
MEADOW builder. The invented program is structurally distinct from
MEADOW's: SUB-based difference over (R5,R1) versus ADD-based sum
over (R4,R2). The learner mechanisms are unchanged: the same
byte-identical learner.zag produces a different invented
intermediate on the new world, which is the generalization under
test.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_l3_adv/`:

- PREREG.md (frozen, committed alone at 4f87b09e6)
- NAMECHECK.md (toolchain guard Step 0 record, development notes)
- REPORT.md (this file)
- learner.zag (byte-identical copy of l2_l3_combo/learner.zag;
  generic learner, never modified)
- world.zag (RELAY hidden rule + episode tables; experiment side only)
- driver.zag (four arms + kill-bar evaluation)
- adv_full.zag (assembled 807-line build input)
- adv_bin (compiled binary)
- adv_compile.txt (build log; exit 0)
- adv_run1.txt, adv_run2.txt, adv_run3.txt (3/3 byte-identical
  outputs)

## Non-claims and bounds

- One adversary-designed world family (RELAY signal stability). No
  generality claim beyond the four demonstrated arms.
- Does not claim Micah's full 12-criterion L3 bar; targets the six
  frozen combo bars.
- The op basis, register machine, greedy policy, and EXTEND rule are
  disclosed researcher-supplied generic machinery, reused
  byte-identical. The claims are: (a) EXTEND fires on structural
  preconditions without per-problem researcher selection; (b) M's
  final form is source-underdetermined and history-determined.
- Pure Zag, safebin toolchain, zero forbidden executables. Paper
  untouched. Nothing pushed. Commits local on tnn-native-lab.

## Display note (auditable, not a defect)

In ARM-L3-ONLY the Z lines show `true=` computed on the truncated
4-reading recall (sq[4]=sq[5]=0, so w_true gives 0), because the
driver prints the label of the sequence the learner actually saw.
Decisions are -1 regardless, so the arm scores 0/4 either way. The
kill bar depends only on the score.
