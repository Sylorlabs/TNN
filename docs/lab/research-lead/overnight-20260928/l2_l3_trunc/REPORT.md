# REPORT: L2-L3 Truncate Combination (STUBBLE)

Worker: L2-L3 Truncate Worker (subagent, 2026-10-02).
Prereg: `l2_l3_trunc/PREREG.md`, frozen alone at commit fc2417e3c
before any implementation existed. No amendments.

## Verdict

**L2-L3-TRUNC-COMPLETE.** All six kill bars PASS, no falsifier fired,
3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`) plus experiment side
(`world.zag`, `driver.zag`), assembled as
`cat learner.zag world.zag driver.zag > trunc_full.zag` and compiled
with the pinned znc to `trunc_bin`. The learner holds: X episode
recall with a learned replay length (L=6 from old 6-reading episodes,
consolidated once and not re-learned), the L2 TRUNCATE standing rule
(replay stops at the first unfilled slot within 0..L-1, firing on
structural preconditions, never researcher-selected per problem), a
fixed 4-register recency window (keep-last loading: the consumer's
working memory holds the last up to 4 replayed readings), Y threshold
decide on scalars, and the L3 greedy constructor over the frozen op
basis {CPY,ADD,SUB,MAX,MIN} on 4 registers (80 candidates/round,
first-max tie-breaking, ascending threshold sweeps). ADAPT_ON is a
driver-set causal-control flag (the composition_l2 adapt_on
precedent), never written by the learner.

The hidden world rule (driver side only): KEEP iff e1+e2 >= 12. The
decisive reading e1 sits in slot 1, displaced from the recency window
without TRUNCATE (the untruncated 6-slot replay's tail is
[e2,e3,255,255]).

## Kill-bar results (from trunc_run1.txt, reproduced in runs 2 and 3)

- K-CB-1 (both required): L2-ONLY 0/4, L3-ONLY 0/4, FULL 4/4. PASS.
- K-CB-2 (L2-only fails): Z-L2ONLY 0/4 with ADAPT-STAT trunc=8.
  Adaptation genuinely fired (Z lines show 4-reading replays) but is
  insufficient without the novel intermediate. PASS.
- K-CB-3 (L3-only fails): Z-L3ONLY 0/4 with trunc=0 and constructed
  M n=0. Construction trace: `C-ROUND 1 base=4 eval=80 stop`. The
  prereg's pairing proof holds: the untruncated recency window shows
  (e2,e3,255,255) with (e2,e3) byte-identical across the keep/drop
  split, so every candidate in every round scores at most the 4/8
  empty baseline. PASS.
- K-CB-4 (combined succeeds with provenance): Z-FULL 4/4,
  ADAPT-STAT-FULL trunc=1952, M-STATE n=2 prog=0,0,1,1,0,2,...
  printed from learner state, and every Z line shows a 4-reading
  replayed sequence (adapted X' in the trace). The invented
  intermediate is M = [CPY R0,R1, ADD R0,R2] (R0 = e1, then R0 +=
  e2), t=12, train 8/8. Construction trace matches the frozen hand
  derivation exactly: round 1 win=0,0,1 gain=3 score=7 t=3; round 2
  win=1,0,2 gain=1 score=8 t=12; round 3 stop. PASS.
- K-CB-5 (M not in source): all 10 frozen grep patterns return 0
  hits on learner.zag (`e1+e2`, `CPY R0,R1`, `ADD R0,R2`,
  `0,0,1,1,0,2`, `3761`, `3,7,6,1`, `stubble`, `threshold.*=.*12`,
  `_MODE`, case-insensitive `bridge`). PASS.
- K-CB-6 (determinism): trunc_run1/2/3.txt sha256 identical
  (2d9908601667d6bff4eb2f18a1e263b02fdb3cea7e4fea2d53e128fe9aebab65).
  PASS.

No falsifier fired: F-NO-CREATE, F-NO-TRUNC, F-L2-SUFFICIENT,
F-L3-SUFFICIENT, F-FRESH-PASS (Z-FRESH 0/4), F-OP-EXPAND, F-AUDIT,
F-NONDET, F-PYTHON all silent.

## Why this is L2 and L3 together

- L2: X's replay procedure was consolidated on 6-reading episodes
  (L=6). On 4-reading episodes the TRUNCATE standing rule adapts the
  procedure (X -> X') purely on the structural precondition of
  unfilled slots. The ARM-L2-ONLY arm proves the adaptation is real
  (trunc=8, 4-reading replays in the trace) and proves it is not
  enough (0/4).
- L3: M = [CPY R0,R1, ADD R0,R2] was not in source (K-CB-5 audit
  clean), was constructed after experience through the white-box
  greedy trace, and is causally necessary (removing M in ARM-L2-ONLY
  collapses Z to 0/4). The ARM-L3-ONLY arm proves the invention
  cannot happen without the adapted X' (pairing proof: the
  untruncated recency window is label-uninformative, construction
  halts with n=0).

## Design note (disclosed in prereg section 9)

With a first-6 register loading, trailing constant slots (255 vs 0)
are provably ignorable by the greedy search (any program touching
only constant registers constant-folds to one that does not), so
TRUNCATE could not be load-bearing there. The fixed-capacity recency
window is the disclosed consumer-side constraint that makes X's
over-long replay displace informative readings, which is what
TRUNCATE repairs. The invented M has the same CPY-then-ADD shape as
MEADOW's but over different registers (R1,R2 vs R4,R2) and a
different threshold (12 vs 10), confirming the construction is
history-determined rather than shape-copied.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_l3_trunc/`:

- PREREG.md (frozen, committed alone at fc2417e3c)
- NAMECHECK.md (toolchain guard Step 0 record, development notes)
- REPORT.md (this file)
- learner.zag (generic learner: X recall + TRUNCATE, 4-register
  recency window, Y decide, L3 constructor; 0 modes/handlers/
  semantic cases)
- world.zag (hidden rule + episode tables; experiment side only)
- driver.zag (four arms + kill-bar evaluation)
- trunc_full.zag (assembled 822-line build input)
- trunc_bin (compiled binary)
- trunc_compile.txt (build log; exit 0)
- trunc_run1.txt, trunc_run2.txt, trunc_run3.txt (3/3 byte-identical
  outputs)

## Non-claims and bounds

- One world family (STUBBLE short-episode keeping). No generality
  claim beyond the four demonstrated arms.
- Does not claim Micah's full 12-criterion L3 bar; targets the six
  frozen combo bars.
- The hidden world rule was builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- The op basis, recency window, greedy policy, and TRUNCATE rule are
  disclosed researcher-supplied generic machinery. The claims are:
  (a) TRUNCATE fires on structural preconditions without per-problem
  researcher selection; (b) M's final form is source-underdetermined
  and history-determined.
- Pure Zag, safebin toolchain, zero forbidden executables. Paper
  untouched. Nothing pushed. Commits local on tnn-native-lab.
