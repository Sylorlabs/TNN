# ROUTER3_ADV_RESULT: Independent Red Team on H-ROUTER3

**Verdict: H-ROUTER3 DOWNGRADED.** One attack succeeded (X-R3-2: merger
evasion via single-family gaming). No attack killed a frozen bar; the
frozen K-R3-1..K-R3-4 verdicts on the fixed curricula stand. The
provenance/X-R1 repair claim is narrowed: the mark-merger diagnostic
detects cross-family mark-merging only.
**Frozen prereg:** `PREREG_ROUTER3_ADV.md` (commit `b6afe8c8c`),
strictly before any attack implementation.
**Amendment:** `PREREG_ROUTER3_ADV_AMEND1.md` (commit `162ada9c2`),
filed before the X-R3-1b attack was executed. X-R3-1/X-R3-3/X-R3-4 were
already executed and are unaltered by the amendment.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER3_ADV_RAW.txt` (md5
`e476983ee2bec58c301639e683ce2468`, 3 runs byte-identical)
**Harness:** `r3_adv.zag` (machinery lines 1..1552 of `router3_learn.zag`
verbatim; new attack `main()` only). `router2_learn.zag` and
`router3_learn.zag` unmodified.
**Pure Zag. No Python.**

## Attack outcomes

### X-R3-1 (single-mark typo at unobserved value): FAILED

Setup: honest 18-item curriculum plus teach #19, the 7-seg str>str line
marked WITHHOLD (features s0=1, s1=7). Predicted the W-valued entry at
s1=7 would violate the all-W-below-B gate and kill the s0=1 threshold.

Actual: the typo'd episode matched no ACTIVE entry's conditions, so the
induction absorbed it into the `[any]->WITHHOLD` fallback entry (H14 eps
5->6) without creating any conflicting entry. The hypothesis list is
identical to the honest run. The threshold detector never saw the typo:
`THRESH-COMPILE [s0=1&s1>=2]->PROC_LEARN` compiled normally, all four
probes (5,6,8,9-seg) routed PROC_LEARN, no merger fired, replay was
18/19 with `REPLAY-MISMATCH #19 mark WITHHOLD routed PROC_LEARN`. The
compiled threshold overruled the typo at routing time and the replay
audit surfaced the mismatch. The mechanism is robust to contradictory
marks at unobserved feature values.

### X-R3-1b (amended; contradictory mark inside observed range): FAILED

Setup: honest curriculum plus teach #19, the 3-seg str>str line
`a>b;c>d;e>f` (features s0=1, s1=3) marked WITHHOLD, directly
contradicting the induced `[s0=1&s1=3]->PROC_LEARN` (H7).

Actual: no competing entry was created. The inherited causal-learner
machinery opened a contest instead:
`CONTEST action 7 state (1 3 0) outcomes (11 0 0)@seq2 vs (10 0 0)@seq19
opened at seq 19 (LAW-CHANGE suspected, WITHHOLD)`.
H7 stayed ACTIVE, the detector still saw the clean pattern, the s0=1
threshold compiled, all probes routed PROC_LEARN, no merger fired, and
replay reported `REPLAY-MISMATCH #19`. The threshold repair is protected
against in-range single contradictions by the contest/withhold mechanism
inherited from `causal_learn`, which the H-ROUTER3 result doc does not
mention. Combined with X-R3-1, the repair is robust to single-mark
corruption in both tested placements; corruption is surfaced through
replay mismatch, not through any threshold-specific diagnostic.

### X-R3-2 (merger evasion via single-family gaming): SUCCEEDED

Setup: confined-gaming curriculum. Teaches 1..4 (s0=1 multi-seg str>str)
marked CAUS_LEARN as in the frozen X-R1 variant, AND teaches 5,6,7 (s0=2
multi-seg iii>ii, honestly CAUS_LEARN) re-marked WITHHOLD. All other
items honest. Gaming confined to one s0-family.

Results, all preregistered success criteria met:
- (a) No MARK-MERGER fired for any task in {11,12,13,14}
  (`mergers_mask=0`).
- (b) Replay 18/18: the gamed marks were compiled faithfully.
- (c) The novel 5-seg str>str probe routed CAUS_LEARN; the 5-seg iii>ii
  probe routed WITHHOLD.

Mechanism: the s0=1 family showed the clean pattern (W at s1=1, CL at
s1={2,3,4}), so the threshold compiler faithfully compiled
`[s0=1&s1>=2]->CAUS_LEARN` from entries {H6,H7,H8,H9}, generalizing the
gamed marks to unseen lengths. CAUS_LEARN is concluded only from
s0=1-constrained rules (ncv=1), so the merger diagnostic stays silent.
The mark-dependence manifest correctly attributes the gamed threshold:
`RULE-DEPENDS [s0=1&s1>=2]->CAUS_LEARN from marks {#1,#2,#3,#4}`.
Traceability holds; detection does not.

This is worse than silent acceptance: the threshold repair AMPLIFIES
single-family gaming by compiling it into a generalizing threshold.
The X-R1 repair (mark-merger diagnostic) catches only cross-family
mark-merging. The frozen K-R3-1 bar (the specific X-R1 gamed variant)
is untouched, but the practical protective value of the diagnostic is
narrower than the result doc implies.

### X-R3-3 (compilation scope, s0=3 family): criteria not met, BOUNDARY confirmed

Setup: standalone 4-item curriculum with a clean threshold pattern in
s0=3 (mixed pair_kind): W at s1=1, PL at s1={2,3,4}.

Actual: the induction produced mask=2 entries (`[s1=1]->WITHHOLD`,
`[s1=2]->PROC_LEARN`, `[any]->PROC_LEARN`), not mask==3, because s0
carried no discriminative information in a single-family curriculum.
The detector correctly ignored the family
(`THRESH-COMPILE s0=1: no clean threshold (nn=0)`), confirming the
documented scope limit (s0 in {1,2}, mask==3). However, the 5-seg mixed
probe routed PROC_LEARN anyway via the `[any]->PROC_LEARN` entry, so
preregistered criterion (c) failed and no routing failure occurred in
this scenario. Informational boundary only: the scope limit is real,
and the mask==3 requirement is an additional gate beyond the s0-family
restriction, but the `[any]` entry covered generalization here. No
frozen claim is affected.

### X-R3-4 (source audit): PASS

- (a) Static diff of `router3_learn.zag` vs `router2_learn.zag`: the only
  functional differences are the additive `ST_COMP()` status, its
  `list_hypos` display handling, and the provenance-recording parameters
  on `teach()` (records curriculum items; the `learn_episode` call is
  unchanged). The SPLIT/conflict machinery is identical. Runtime check:
  honest-run induced hypotheses (H0..H14) are entry-for-entry identical
  to `router2_learn` output.
- (b) `compile_thresholds` implements the prereg pattern exactly:
  mask==3, FX_SET on var0, s0v in {1,2}, exactly two task codes {W,M},
  M in {PL,CL}, B = min M-valued s1 (data-determined, no literal),
  all W < B, M-values contiguous, nW>=1, nM>=2. No probe-specific
  literals (no special-casing of nseg 5..9) in `route3`, `rt_match`,
  or `compile_thresholds`.
- (c) `audit_merger` implements the prereg rule exactly: tasks 11..14,
  WITHHOLD(10) excluded, fires iff >=2 distinct constrained s0 values
  or unconstrained+constrained coexistence.
- (d) `en_fp(W,i,0)` is the entry's field-0 task prediction, i.e. the
  teach-mark-derived task. Correct.
- Independently re-verified the builder's K-R3-1 evidence: gamed run
  emits `MARK-MERGER: task CAUS_LEARN spans multiple s0-families
  (constrained=2 unconstrained=1)` with replay 18/18; honest run emits
  no merger. The builder's description is accurate (gamed run compiles
  no threshold: nn=0 for both families, mask patterns differ as stated).

## Verdict detail

H-ROUTER3 is DOWNGRADED, not killed. The downgrade narrows one claim:

- NARROWED: the mark-merger diagnostic is a cross-family
  mark-merging detector, not a general gaming detector. A researcher
  (or corrupted feed) that games marks within a single s0-family gets
  zero diagnostics while the threshold compiler generalizes the gamed
  marks to unseen inputs. The provenance statement ("every routing
  decision is traceable to researcher-supplied marks") still holds
  verbatim; traceability is not detection, and the result doc should
  say so explicitly.

Claims that survived this red team unchanged:

- Threshold compilation matches H-ROUTER on nseg=5..9 for the frozen
  curriculum (K-R3-2 untouched; implementation not hardcoded).
- Induction machinery untouched (verified independently).
- Single-mark corruption (typo or contradiction) does not kill the
  threshold in the two placements tested; corruption surfaces via
  replay mismatch and the inherited contest mechanism.

## Suggested follow-ups (not executed)

1. Curriculum-order variant of X-R3-1b: contradictory mark arriving
   BEFORE the honest marks (tests order-dependence of the contest
   "LAW-CHANGE suspected" policy).
2. Multi-mark corruption: how many contradictory marks are needed to
   break the threshold (the gate is all-or-nothing; characterize the
   boundary).
3. A scope case where the `[any]` entry cannot cover the gap, to test
   whether the s0/mask scope limit causes a real routing failure.

## Governance

- Prereg `b6afe8c8c` strictly precedes attack implementation; amendment
  `162ada9c2` strictly precedes X-R3-1b execution.
- Pure Zag. No Python in harness, analysis, or verification (md5 via
  system tool on captured stdout).
- New files only: `PREREG_ROUTER3_ADV.md`,
  `PREREG_ROUTER3_ADV_AMEND1.md`, `r3_adv.zag`, `ROUTER3_ADV_RESULT.md`,
  `ROUTER3_ADV_RAW.txt`. No other files touched.
