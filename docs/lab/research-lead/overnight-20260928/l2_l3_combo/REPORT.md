# REPORT: L2-L3 Combination (MEADOW)

Worker: L2-L3 Combination Worker (subagent, 2026-10-02).
Prereg: `l2_l3_combo/PREREG.md`, frozen alone at commit fb1075ef0
before any implementation existed. No amendments.

## Verdict

**L2-L3-COMBO-COMPLETE.** All six kill bars PASS, no falsifier fired,
3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`) plus experiment side
(`world.zag`, `driver.zag`), assembled as
`cat learner.zag world.zag driver.zag > combo_full.zag` and compiled
with the pinned znc to `combo_bin`. The learner holds: X episode
recall with a learned replay length (L=4 from old 4-reading episodes),
the L2 EXTEND standing rule (replay continues past L while
continuation slots are filled, up to 2 extra slots, firing on
structural preconditions, never researcher-selected per problem), Y
threshold decide on scalars, and the L3 greedy constructor over the
frozen op basis {CPY,ADD,SUB,MAX,MIN} on 6 registers (180
candidates/round, first-max tie-breaking, ascending threshold
sweeps). ADAPT_ON is a driver-set causal-control flag (the
composition_l2 adapt_on precedent), never written by the learner.

The hidden world rule (driver side only): rich iff e2+e4 >= 10. The
decisive reading e4 sits in slot 4, unreachable without the L2
extension.

## Kill-bar results (from combo_run1.txt, reproduced in runs 2 and 3)

- K-CB-1 (both required): L2-ONLY 0/4, L3-ONLY 0/4, FULL 4/4. PASS.
- K-CB-2 (L2-only fails): Z-L2ONLY 0/4 with ADAPT-STAT ext=8.
  Adaptation genuinely fired (Z lines show 6-reading replays) but is
  insufficient without the novel intermediate. PASS.
- K-CB-3 (L3-only fails): Z-L3ONLY 0/4 with ext=0 and constructed M
  n=0. Construction trace: `C-ROUND 1 base=4 eval=180 stop`. The
  prereg's pairing proof holds: train projections pair rich/poor
  episodes byte-identically on the first 4 readings, so no candidate
  can beat the 4/8 empty baseline. PASS.
- K-CB-4 (combined succeeds with provenance): Z-FULL 4/4,
  ADAPT-STAT-FULL ext=4352, M-STATE n=2 prog=0,0,4,1,0,2,... printed
  from learner state, and every Z line shows a 6-reading replayed
  sequence (adapted X' in the trace). The invented intermediate is
  M = [CPY R0,R4, ADD R0,R2] (R0 = e4, then R0 += e2), t=10, train
  8/8. Construction trace matches the frozen hand derivation exactly:
  round 1 win=0,0,4 gain=3 score=7 t=1; round 2 win=1,0,2 gain=1
  score=8 t=10; round 3 stop. PASS.
- K-CB-5 (M not in source): all 11 frozen grep patterns return 0 hits
  on learner.zag (`e2+e4`, `CPY R0,R4`, `ADD R0,R2`, `0,0,4`,
  `1,0,2`, `107050`, `1,0,7,0,5,0`, `even`, `threshold.*=.*10`,
  `_MODE`, case-insensitive `bridge`). PASS.
- K-CB-6 (determinism): combo_run1/2/3.txt sha256 identical
  (dc0651ba7f965c5c8f9567d114675f30ce84c868050697abf88627667ee483f6).
  PASS.

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
- L3: M = [CPY R0,R4, ADD R0,R2] was not in source (K-CB-5 audit
  clean), was constructed after experience through the white-box
  greedy trace, and is causally necessary (removing M in ARM-L2-ONLY
  collapses Z to 0/4). The ARM-L3-ONLY arm proves the invention
  cannot happen without the adapted X' (pairing proof: 4-reading
  projections are label-uninformative, construction halts with n=0).

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_l3_combo/`:

- PREREG.md (frozen, committed alone at fb1075ef0)
- NAMECHECK.md (toolchain guard Step 0 record, development notes)
- REPORT.md (this file)
- learner.zag (generic learner: X recall + EXTEND, Y decide, L3
  constructor; 0 modes/handlers/semantic cases)
- world.zag (hidden rule + episode tables; experiment side only)
- driver.zag (four arms + kill-bar evaluation)
- combo_full.zag (assembled 803-line build input)
- combo_bin (compiled binary)
- combo_compile.txt (build log; exit 0)
- combo_run1.txt, combo_run2.txt, combo_run3.txt (3/3 byte-identical
  outputs)

## Non-claims and bounds

- One world family (MEADOW foraging aggregation). No generality claim
  beyond the four demonstrated arms.
- Does not claim Micah's full 12-criterion L3 bar; targets the six
  frozen combo bars.
- The hidden world rule was builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- The op basis, register machine, greedy policy, and EXTEND rule are
  disclosed researcher-supplied generic machinery. The claims are:
  (a) EXTEND fires on structural preconditions without per-problem
  researcher selection; (b) M's final form is source-underdetermined
  and history-determined.
- Pure Zag, safebin toolchain, zero forbidden executables. Paper
  untouched. Nothing pushed. Commits local on tnn-native-lab.
