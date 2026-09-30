# PREREG H-ROUTER9: survivor-contradiction gate for threshold compilation (FROZEN)

Status: FROZEN. Committed alone before any H-ROUTER9 implementation exists.
Parent: H-ROUTER8 KILLED by X-R8-3b (black-box threshold shadowing).
Lineage quarantine: H-ROUTER6/R7/R8 carry unresolved governance lineage;
H-ROUTER9 inherits the quarantine and is exploratory until adjudicated.
This prereg freezes the repair and its kill bars only.

## 1. Hypothesis

H-ROUTER8 is KILLED because `compile_thresholds` validates its clean
boundary against mask-3 source entries only, then `build_table_rest`
inserts the compiled threshold rules FIRST, silently shadowing any
surviving non-mask-3 entry whose condition overlaps the generalized
range with a different task. Gating compilation on a survivor
contradiction check (R9-1) closes X-R8-3b on BOTH threshold sides
([s1>=B]->M and [s1<B]->WITHHOLD) while preserving all R8 behavior
where no contradiction exists.

## 2. Repair (frozen R9-1, amended by A1)

New function `thresh_survivor_ok(W, s0v, B, M) -> i32`, called inside
`compile_thresholds` after the clean-boundary checks pass and before
any rule is added or any source compacted:

- For each entry e with ST_ACTIVE and FX_SET, for each episode k in
  0..en_neps(e): let f0=ep_s(e,0), f1=ep_s(e,1), f2=ep_s(e,2),
  t=ep_ns(e,0) (the TAUGHT task of that episode).
- If f0 == s0v: the threshold pair claims triple (f0,f1,f2) as
  M when f1 >= B, else TC_W().
- If t differs from the claimed task: the threshold would shadow
  DIRECT taught evidence. Emit THRESH-REFUSED naming s0v, the
  survivor entry, the episode triple, the taught task, and the
  contradicted claim; return 0.
- Return 1 if no episode contradicts.

On gate refusal (return 0): the whole threshold PAIR is refused.
No threshold rules are added, no sources are compacted (they stay
ACTIVE), and the existing "no clean threshold" path is skipped
(the THRESH-REFUSED line carries the reason). Routing falls back to
the surviving entry rules, which is sound.

On gate pass (return 1): compilation proceeds exactly as in H-ROUTER8,
including the THRESH-COMPILE and THRESHOLD-GENERALIZATION lines.

Scope freeze: induction, merge, table build, audits, and all fixtures
are untouched. Only `compile_thresholds` gains the gate call.

## 2b. Amendment A1 (2026-09-30 ~00:30 UTC, before implementation; reason recorded)

The prereg as first frozen specified a CONDITION-overlap gate (any
surviving entry whose mask condition overlaps the generalized range
with a different task refuses). Pre-implementation prototyping against
the honest curriculum showed that criterion refuses the honest
s0=1 and s0=2 thresholds: survivor H14 [any]->WITHHOLD (5 episodes,
all with s0 not in {1,2}) overlaps every threshold range by condition
alone. That refusal breaks frozen K-R9-3 (K-R4-4 falls to 0/10) and,
worse, would refuse essentially every threshold whenever the
induction's [any] default survives, destroying the mechanism's core
capability (family-boundary generalization, frozen since H-ROUTER2).

The X-R8-3b soundness hole is specifically DIRECT taught evidence at
the contradicted triple being silently shadowed (the (1,5,0)->W mark
absorbed into H1). The refined criterion above closes exactly that:
a threshold may generalize over triples no survivor has direct
evidence about (resolving generalization-vs-generalization by the
designed family/specificity policy), but it may never contradict a
taught episode. The kill bars in section 3 are unchanged: both
frozen fixtures refuse via the absorbed taught episodes
((1,5,0)->W in H1 for K-R9-1; (1,2,0)->PL in H1 for K-R9-2).

## 3. Frozen kill bars

New main sections (black-box via teach(), same helpers as builder):

- S-R9A "THRESHOLD-SHADOW REPAIR" replays X-R8-3b verbatim, 7 marks:
  (0,5,0)->W "a;b;c;d;e"; (0,6,0)->PL "a;b;c;d;e;f";
  (1,5,0)->W "a>b;c;d;e>f;g>h;i>j"; (1,3,0)->PL "a>b;c>d;e>f";
  (1,4,0)->PL "a>b;c>d;e>f;g>h"; (2,3,0)->CL "1,1,1>1,0;2,2,2>2,0;3,3,3>3,0";
  (1,1,0)->W "a>b".
- S-R9B "THRESHOLD-SHADOW T2" exercises the [s1<B]->WITHHOLD side, 7 marks:
  (0,2,0)->PL "a;b"; (0,3,0)->W "a;b;c"; (1,2,0)->PL "a>b;c>d";
  (1,4,0)->PL "a>b;c>d;e>f;g>h"; (1,5,0)->PL "a>b;c>d;e>f;g>h;i>j";
  (2,4,0)->CL "1,1,1>1,0;2,2,2>2,0;3,3,3>3,0;4,4,4>4,0";
  (1,1,0)->W "a>b".

K-R9-1 (X-R8-3b closure): in S-R9A, exactly the s0=1 threshold pair is
refused: one THRESH-REFUSED line for s0=1, zero THRESH-COMPILE lines
for s0=1; route3 probes (1,5,0)=10, (1,1,0)=10, (1,3,0)=11,
(1,4,0)=11; audit_replay 7/7. KILL iff any probe is wrong, replay is
below 7/7, or any s0=1 THRESH-COMPILE line appears.

K-R9-2 (T2-side closure): in S-R9B, the s0=1 threshold pair is refused:
one THRESH-REFUSED line for s0=1, zero THRESH-COMPILE lines for s0=1;
route3 probes (1,2,0)=11, (1,1,0)=10, (1,4,0)=11, (1,5,0)=11;
audit_replay 7/7. KILL iff any probe is wrong, replay is below 7/7,
or any s0=1 THRESH-COMPILE line appears.

K-R9-3 (builder regression): every pre-existing automated bar passes
unchanged: K-R5-1, K-R5-2a, K-R5-2b, K-R5-2c, K-R4-1, K-R4-2, K-R4-3,
K-R4-4, K-R4-5, K-R6-1, K-R6-2, K-R7-1, K-R7-2, K-R8-1. Zero
THRESH-REFUSED lines appear in any pre-existing fixture section; the
honest-curriculum THRESH-COMPILE lines still fire. Any refusal inside
a pre-existing fixture is a bar failure pending investigation, not a
pass. KILL iff any listed bar fails or any unexpected refusal appears.

K-R9-4 (clean boundary still compiles): the honest curriculum emits
THRESH-COMPILE for the s0=1 family exactly as under H-ROUTER8, and
K-R4-4 holds 10/10 (already entailed by K-R9-3; listed separately as
the anti-overrefusal check). KILL iff the honest threshold stops
compiling.

K-R9-5 (determinism): 3/3 runs byte-identical, exit 0. KILL iff any
run differs.

Verdict: H-ROUTER9 SURVIVES iff K-R9-1 through K-R9-5 all PASS.
Otherwise H-ROUTER9 is KILLED. DOWNGRADE is not available: the repair
claims closure, so a missed contradiction is a kill.

## 4. Governance

Pure Zag throughout: no Python anywhere including scratch, builds,
verification, and analysis. Prereg committed alone before
implementation; implementation is a byte-verbatim copy of
router8_learn.zag at its builder result commit plus exactly the frozen
R9-1 edits (diff-audited). Only owned paths staged:
PREREG_ROUTER9.md, router9_learn.zag, ROUTER9_RAW_OUTPUT.txt,
ROUTER9_RESULT.md. No binaries committed. No em dashes (byte-checked).
Commits local only; no push authorized.
