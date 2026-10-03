# REDTEAM EXP1c wave-20260927-1721pdt: Independent Review

Reviewer: independent red-team (did not author the attempt).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Attempt commits reviewed:
- Freeze (reused): 8b456736b14a62b629c5cb7b152a10feba657907 (2026-09-27 18:28:26 UTC)
- Addendum: 763983e3a62b119edf5eb16a5e67307e0ef86798 (2026-09-28 00:33:41 UTC)
- Iteration 1: 5168f0448da4afd0d885e192a9ddc0efa835307c (2026-09-28 00:52:57 UTC)
Frozen prereg: docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md
World template: lab/invention/survival/src/world.zag, blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a at HEAD (matches addendum claim).
Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches frozen pin).

## Verdict: NOT CERTIFIABLE

The K1 KILL (the headline verdict) cannot be certified, and the run is
VOID as a test of H1/H2. Three independent grounds, any one of which is
sufficient:

1. The I arm as implemented is not the frozen I arm. It deviates from
   frozen M3 (scoring rule) and frozen M4 (reflex set) in ways the frozen
   text itself says void K1/K2. The measured 81-tick death is an
   implementation artifact (enumeration stall plus starvation), not a
   property of the frozen mechanism. (Findings F1-F5.)
2. The committed evidence package is internally inconsistent. The run
   file's machine-readable summary sections (MEDIANS, BARS, K7, ISTAT,
   ablation orig_ticks) contain corrupt values that contradict the TSV
   and the worker's note. The note's "both methods agree" and "medians
   are correct" claims are false for run mode, and the K7 PASS (file) vs
   VOID (note) contradiction is undisclosed. (Finding F6.)
3. The frozen section-7 bound is arithmetically impossible on its face
   (1134 minimum primitive-action ticks > 600), so the design cannot
   produce a post-enumeration phase; K7 VOID is structural. The worker
   reported this honestly, and the honest reporting is credited, but it
   confirms the run cannot test H1/H2 as designed. (Finding F9.)

What IS valid and is credited: commit ordering, M5 iteration-1 protocol,
pure-Zag sources, the vel=0 lo<hi family, mode_check gating in code,
byte-identical determinism (all five modes reproduce; rebuilt binary is
byte-identical to the committed binary), the TSV primary data, the
calibration gates C1/C2 as computed in Zag, no recycling from the voided
1421pdt attempt, and the honest section-7 NOT-MET.

## Checks that pass

C-ORDER: Freeze 8b456736b (18:28 UTC) strictly precedes addendum
763983e3a (00:33 UTC), which strictly precedes iteration 1 5168f0448
(00:52 UTC). Both are descendants of the freeze commit (verified via
merge-base --is-ancestor). The prereg commit-order self-check passes.

M5: Iteration 1 commit contains the variants source
(src/x1c_variants.zag, self-labeled "RETUNE ITERATION 1", const
X1C_ITER=1), the mode_check result (evidence/iter1_check.txt =
"CHECK_OK"), the calibration medians computed in Zag
(evidence/iter1_calibrate.txt), and SHA-256 hashes
(evidence/iter1_hashes.txt). No iteration 2 exists yet. The per-iteration
commit rule is satisfied.

PURE ZAG (item 7): the four sources are pure Zag. No Python files exist
anywhere under exp1c/. The probe scratch files mentioned in the worker's
note were removed before the commit (not present in 5168f0448). Evidence
files are byte-identical to fresh binary stdout (see REPRO). Shell use is
within the allowed scope (invoke compiler, redirect stdout, hash).

VEL=0 LO<HI: all 72 mote definitions (12 variants x 6) carry vel=0 and
satisfy lo<hi (verified in x1c_variants.zag; the in-Zag mode_check rule 1
lo>=hi and rule 8 vel!=0 both pass, CHECK_OK). The degenerate lo==hi
input is never used. This is the in-spec stationarity design per the
addendum's degenerate-input standing rule.

MODE_CHECK GATING: mode_calibrate implements the in-code gate
(x1c_runner.zag lines 460-471): nonzero violation count prints
CHECK_FAIL plus CALIBRATE_REFUSED and returns without calibrating. The
evidence shows the positive case (iter1_check.txt = CHECK_OK;
iter1_calibrate.txt opens with CALIBRATE_BEGIN). The refusal path is
implemented but not demonstrated in evidence (expected, since a refusal
would produce no calibration file).

RECYCLING: clean. The 1421pdt record
(docs/lab/rsi/runs/wave-20260927-1421pdt/exp1c/) is byte-different from
all 1721pdt evidence; none of its planning numbers (510, 91, 649, 626)
appear in the 1721pdt evidence. Sources import only the frozen world
template and each other. The single "1421" string in x1c_variants.zag
line 12 is a code comment about the fixed label bug, not evidence reuse.

## Reproduction (independent)

Extracted bin/x1c_iter1 from commit 5168f0448 to /tmp (read-only) and
re-ran all five modes twice:
- check, variants, calibrate, bound, run: all byte-identical to the
  committed evidence files (diff clean on all five).
- run output SHA-256: 4aea7251fcf74d4702c8a0e9debbc7b9465fbd4e36740953ddaa6943c34272fa,
  matching the reported hash on both runs (determinism confirmed).
- Rebuilt the binary from the committed sources with the pinned
  toolchain: the rebuilt binary is BYTE-IDENTICAL to the committed
  binary (sha256 59df6901fcd1914f690043d44f20871d652f3541ba094fc8f0e64afaec332a07
  both). Source/binary consistency confirmed. The corrupt summary
  sections below are therefore produced by the committed source itself,
  not by a stale binary.

## Findings (void and major)

### F1. M3 scoring deviation: the I arm does not implement the frozen argmax. VOID for K1/K2.

Frozen M3 (and confound-list item 2): "scoring is deterministic argmax
over (mean experienced delta-energy + decaying B0)", with
B0(n) = B0/(1+n). Frozen M3: "The decay schedule is frozen text; any
implementation deviation voids K1/K2 for that arm."

Implemented (x1c_agents.zag lines 323-352): xi_eval computes a BINARY
bonus flag (bonus=1 if tried==0 or mean < B0/(1+n), else 0); xi_pick
ranks by key = 2*mean + bonus_flag (line 349). This is not
mean + B0/(1+n). Consequence: an untried sketch (intended score
0 + 40 = 40) ties a 30-times-tried sketch with mean 0 (key 1 vs key 1),
and the strict-greater tie-break keeps the lower index. The agent
repeats plan index 0 (L, LEFT) forever instead of enumerating.
Evidence: TOPSKETCH in iter1_run1.txt shows rank-0 plan L tried 30
times with all other 398 sketches at tried=0 for variants 1-8 and 10;
iter1_bound.txt shows n_distinct=1 for those runs. Enumeration stalls
at the first sketch. This is a direct implementation deviation from the
frozen scoring rule, and per the frozen text it voids K1/K2 for the I
arms.

### F2. M4 extra reflex: "mote-adjacent" preemption is not in the frozen list. VOID for K1/K2.

Frozen M4: "The implementation may contain exactly the following
preempting single-step reflexes, and no others: (a) storm-active flee;
(b) energy below 25 survival reflex; (c) void-adjacent step refusal
(H9)." And: "any implementation-added reflex not listed in this frozen
text voids the K1 and K2 gates for that run (the gate that was run was
not the gate that was frozen)."

Implemented (x1c_agents.zag lines 360-375, xi_preempt): preemption 2 is
"mote adjacent -> step onto it", which appears nowhere in M4. This is an
implementation-added preempting reflex. Per the frozen M4 law, K1 and K2
are VOID for every I-arm run. The gate that ran is not the gate that
was frozen.

### F3. M4(c) void-safety (H9) is missing from the implementation.

The taught H9 (kb_exp1c.txt lines 58-59): "If the step you are about to
take would land on a void cell: refuse that step." No void-refusal logic
exists anywhere in x1c_agents.zag or x1c_runner.zag (the only "void"
mentions in the agents file are comments; the runner only prints void
coordinates). The I arm's plan steps (raw LEFT/RIGHT actions) and its
mote-adjacent preemption (x_step_to, no void check) can step into voids
unrefused. The frozen M4(c) reflex is absent.

### F4. M4(a) storm condition deviation.

Frozen M4(a) and taught H3 (kb_exp1c.txt line 47): "storm is active now"
(w_storm_active exists in the world template). Implemented
(x1c_agents.zag line 362): w_storm_within(w, 2), i.e. "storm within 2
ticks". Anticipatory flee is not the frozen "storm-active" reflex.
Minor next to F1-F3, but a further M4 deviation.

### F5. The 81-tick I-arm death is an implementation artifact, not a genuine property.

All Is/Ii arms die with cause=1 (world.zag: energy<=0, starvation),
e_end=0, at ticks 50/81/97, while P and R survive 1200/1200 in the same
worlds. The mechanism of death: F1's scoring stall pins the agent on
plan L (LEFT); EAT (index 2) is never selected; the agent walks left
until clamped at the boundary, never eating, and starves. The
energy<25 emergency preemption fires (TOPSKETCH tried counts show only
30 of 81 ticks were plan executions; the rest were preemptions) but
cannot save an agent that never eats. A trivial mote-seeking forage
survives all 1200 ticks in every variant. Under the frozen scoring, the
agent would enumerate through EAT and the other sketches. The measured
Is median of 81 is therefore not a measurement of the frozen I arm.
K1's "KILL" rests on this artifact and cannot be adopted. (K2's PASS is
likewise not a valid gate outcome, since K2 is void per F2; the
measurement 81 > 45 is factually correct from the TSV but the gate did
not run as frozen.)

### F6. Evidence integrity: corrupt summary sections and undisclosed contradictions.

The TSV section of iter1_run1.txt/iter1_run2.txt is sane and
reproducible (hand-verified medians: P=1200, Z=45, R=1200, Is=81,
Ii=81). But the program's own summary sections are corrupt:
- MEDIANS_BEGIN: P=2013, Z=2016, R=2019, Is=2022, Ii=2010 (garbage; true
  values 1200/45/1200/81/81). The "AGREE" flags are meaningless: both
  methods read the same corrupted buffer.
- BARS_BEGIN: K1 "median_Is=2022 median_R=2019 verdict=PASS". The
  verdict is WRONG (true medians give 81 <= 1200 = KILL). The committed
  evidence asserts K1 PASS while the worker's note asserts K1 KILL.
- K7_BEGIN: "post_enum_plans=73577 low_bonus_plans=73600 ...
  fraction_per_mille=1000 verdict=PASS". Impossible values
  (low_bonus > post_enum) and the wrong verdict; the code's intended
  path with zero post-enumeration plans is VOID (x1c_runner.zag
  lines 719-737).
- ISTAT_BEGIN: sequential garbage (3085, 3086, ... per row), not real
  statistics.
- ABLATION: orig_ticks garbage for variants 4-10 (2000, 2003, ...),
  disclosed in the note; but the note's "ablated_ticks and medians are
  correct" is false for MEDIANS_BEGIN, and the K6 "verdict=PASS" line in
  the file contradicts the note's "K6 FIRES".
The worker's note claims "Medians (both methods agree)" for the run.
That is false as a description of the committed run file: the two
methods agreed on garbage, and the reported medians (1200/45/1200/81/81)
were derived by hand from the TSV, not computed inside Zag. The frozen
item 7 requires medians computed inside Zag; the in-Zag run-mode median
path is corrupt. The note's Known-issues section discloses only the
ablation orig_ticks column and omits the MEDIANS/BARS/K7/ISTAT
corruption entirely. This is a material transparency failure in the
evidence package.

### F7. K7: VOID is the correct verdict, but the evidence contradicts itself and the instrumentation is inverted.

With zero post-enumeration plans (iter1_bound.txt: 0 of 24 runs
completed enumeration; enum_tick=-1 throughout), the choice question is
null, and per frozen K7 the run is VOID as a test of H1/H2. The worker's
note reaches VOID, which is correct. However: (a) the committed run
file asserts K7 PASS with impossible numbers (F6), an undisclosed
contradiction; (b) the K7 instrumentation itself is inverted relative
to the frozen text. Frozen K7 counts plans where the novelty bonus is
<10% of the winning score (learned credit dominates). The code
(x1c_agents.zag xi_act, post_low increment) counts plans where
mean < B0/(1+n), i.e. novelty DOMINATES, the opposite. Moot here
(enum_done never becomes 1), but the K7 bar as implemented does not
measure the frozen quantity.

### F8. K6: fires literally on equality, but the ablation is a no-op and the file disagrees.

The file header states the rule: "fires iff median(ablated I-survive)
>= median(original I-survive)". True medians: 81 >= 81, so the literal
rule fires on equality, as the worker's note claims. But:
(a) the committed file's K6 line says "verdict=PASS" (computed from
garbage median_orig_Is=2022), contradicting the note's FIRES;
(b) the ablation replaced 0 TAKE/DROP/COMBINE actions in all 24 traces
(the I arm died before ever composing), so it is a no-op ablation. A
no-op ablation "not reducing survival" is vacuous as killing evidence
for the invention claim. The worker discloses the replaced=0 fact, to
their credit, but presenting "K6 FIRES" as an independent kill overstates
it. The TSV orig_ticks corruption for variants 4-10 does not change the
hand-derived medians (both 81), but it does corrupt the file's own K6
computation.

### F9. Section-7 frozen arithmetic is impossible on its face; the worker's NOT-MET is honest.

Frozen section 7 claims 399 sketches "provably complete before tick 600".
Minimum primitive-action cost: 7 length-1 plans (7 ticks) + 49 length-2
(98) + 343 length-3 (1029) = 1134 ticks, plus 399 replan overheads.
1134 > 600 under one action per tick, so the frozen claim is false on
its own terms; no implementation can satisfy it. The worker's bound mode
faithfully implements "at most one plan try per replan" (x1c_runner.zag
mode_bound) and reports NOT-MET (0/24 complete), and the note states the
arithmetic inconsistency plainly without weakening the requirement. This
is the correct honest-negative handling, and it is credited. Structural
consequence: the design can never reach a post-enumeration phase, so K7
VOID is inevitable for any faithful implementation.

### F10. C3 "qualitatively distinct" is not satisfied.

Frozen C3: ">= 3 qualitatively distinct scripted strategies each
reaching median >= 720/1200". The in-Zag C3 counts medians only
(p_ward=1200, forage=1200, cachefarm=1200 = 3). But p_ward and forage
produce BYTE-IDENTICAL traces: same ticks (1200) and same e_end in all
12 variants (e.g. variant 0: 145/145; variant 3: 181/181). Two
behaviorally identical strategies do not demonstrate the strategy
diversity C3 is meant to validate; the genuinely distinct survivors are
forage/p_ward (one behavioral cluster) and cachefarm: 2, not 3. (R is
likewise near-identical to P: e_end matches in 11 of 12 variants.) The
C3 PASS as computed does not meet the frozen "qualitatively distinct"
qualifier. C1 and C2 themselves are unaffected (correct in-Zag medians,
reproducible).

### F11. The _zag_malloc claim is unproven and does not explain the corruption.

The note attributes corruption to "toolchain _zag_malloc returning
overlapping blocks on successive calls", claiming a fix via
single-allocation arena partitioning. But main() (x1c_runner.zag)
performs exactly ONE _zag_malloc call and carves fixed arenas; the
corruption persists in the committed binary built from the committed
source. The cited mechanism (successive calls) cannot produce the
observed corruption under a single call unless the Zag runtime allocates
internally, which the worker does not demonstrate. The corruption
pattern (deterministic sequential values in ISTAT; specific Q_RES words
for variants 4-10) looks like a deterministic codegen or source-level
bug, not allocator nondeterminism. The claim therefore papers over an
undiagnosed defect. It does not affect the TSV hashes (the TSV is
correct and reproduces byte-identically), but it is not a diagnosed
root cause and cannot certify the summary sections.

## Verdict mapping recommendation: VOID (not DEAD)

Frozen mapping: "Any kill bar firing means DEAD with killing evidence.
K3 or K7 failure means VOID." Both conditions nominally occur (K1 fires
on the TSV medians; K7 fails). The honest resolution:
- K7 failure makes the run VOID as a test of H1/H2 by the frozen text's
  own definition ("the design failed, not the agent"; "a validity gate,
  not a kill"). A void test cannot kill a hypothesis.
- K1/K2 are independently VOID for the I arms per the frozen M3 text
  ("any implementation deviation voids K1/K2 for that arm") and the
  frozen M4 law (extra reflex), given findings F1, F2, F4.
- The K1 measurement (median_Is 81 <= median_R 1200) is recorded as a
  measurement of the as-built (deviating) implementation, but it is NOT
  adopted as a kill of H1. The 81-tick death is an implementation
  artifact (F5).
- K6's literal firing is vacuous (no-op ablation, F8) and is not
  independent killing evidence.
Recommended recorded verdict: **VOID as a test of H1/H2** (K7 fails;
section-7 bound arithmetically unsatisfiable; I-arm implementation not
faithful to frozen M1-M4). The "DEAD" label must not be attached to H1
on this evidence.

## What the worker got right (credited)

- Commit ordering, M5 per-iteration commits, and the pre-run addendum
  discipline are exemplary.
- The section-7 NOT-MET is reported without flinching, with the
  arithmetic inconsistency stated plainly. This is exactly the honesty
  the loop asks for.
- Determinism is real: two byte-identical 144,000-tick runs, and the
  source rebuilds to a byte-identical binary.
- No recycling: everything is new this wave; the voided 1421pdt record
  is referenced only as planning data, never as evidence.
- The ablation no-op (replaced=0) is disclosed rather than hidden.

## Required before any future certification of an EXP1c iteration

1. Implement the frozen scoring verbatim: rank by
   mean_delta_energy + B0/(1+n) with the frozen integer division, so
   untried sketches strictly outrank tried ones and enumeration
   actually proceeds in lex order.
2. Implement EXACTLY the three M4 reflexes: storm-ACTIVE (use
   w_storm_active), energy<25 survival reflex, H9 void-step refusal;
   remove the mote-adjacent preemption or obtain a frozen amendment.
3. Fix or root-cause the summary-section corruption (MEDIANS, BARS, K7,
   ISTAT, ablation orig_ticks); do not ship hand-derived medians
   described as "both methods agree".
4. Repair or amend the section-7 bound: as frozen, it is unsatisfiable
   (1134 > 600). Either the horizon, the plan space, or the tick bound
   needs a frozen redraft before K7 can be meaningful.
5. Make C3 check behavioral distinctness, not just median counts, or
   field a third genuinely distinct surviving strategy.
6. Correct the K7 instrumentation to the frozen quantity (bonus < 10%
   of winning score), not its inverse.

## Line and section references

- Frozen M3 scoring / void rule: PREREG_EXP1c_FROZEN.md sections 3
  (M3), 9 (confound 2).
- Frozen M4 exhaustive reflex list and void law: PREREG_EXP1c_FROZEN.md
  section 3 (M4).
- Frozen K7 and verdict mapping: PREREG_EXP1c_FROZEN.md section 6.
- Frozen section 7 arithmetic: PREREG_EXP1c_FROZEN.md section 7.
- Frozen item 7 pure-Zag: PREREG_EXP1c_FROZEN.md sections 9 (confound
  7), 10.
- Scoring implementation: x1c_agents.zag lines 323-352
  (xi_eval/xi_pick; key at line 349).
- Preemptions: x1c_agents.zag lines 360-375 (xi_preempt).
- Taught H3/H9: lab/invention/survival/kb/kb_exp1c.txt lines 47-49,
  58-59.
- Death causes: lab/invention/survival/src/world.zag (cause 1 =
  energy<=0 starvation; cause 2 = void fall).
- Median/K7/ablation/bound printing: x1c_runner.zag lines 656-737
  (MEDIANS/BARS/K7), 738-775 (ablation/K6), 780-910 (bound).
- Calibrate gate: x1c_runner.zag lines 460-471.
- Worker note: evidence/iter1_note.md. Corrupt run file:
  evidence/iter1_run1.txt (MEDIANS_BEGIN, BARS_BEGIN, K7_BEGIN,
  ISTAT_BEGIN, ABLATION_BEGIN).
