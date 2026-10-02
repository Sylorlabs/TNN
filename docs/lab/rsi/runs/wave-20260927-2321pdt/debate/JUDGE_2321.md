# Judge rulings: wave-20260927-2321pdt (five motions)

Role: independent judge. This judge read the advocate brief
(debate/ADVOCATE_2321.md), the skeptic report
(debate/SKEPTIC_2321.md), the independent red-team report
(exp1c/REDTEAM_EXP1C_2321.md, commit 3636d2fe4), the fork
battery report (forks/FORK_RESULTS_2321.md, commit 9926b0860),
the design-lane hunt (design_lane/HUNT_2321.md, commit
3dc45ca35), the interactive survey (INTERACTIVE_SURVEY_2321.md,
commit 9c6646c04), and the 2021pdt verdicts at the tail of
LOOP_STATE.md. Nothing else was read; nothing else was judged.

Binding precedent: the 2021pdt verdicts and judge rulings
e97d1b9c0. Judge-confirmed precedent: "a void test cannot kill
a hypothesis". K7 takes precedence over any K1 firing. The
section-7 redraft addendum d9e96ad91 is judge-legitimate. K4
CANNOT-CONFIRM and K5 INCOMPLETE are honestly reported per
frozen text. The K6 operationalization R3 was recorded as
reasonable; any future adoption must freeze the
operationalization first. The C3 "qualitatively distinct" claim
was struck in 2021pdt; the binding F10/R1 fix required the
in-Zag check.

Standing rules observed: pure Zag discipline (text debate, no
code, no Python), no em-dashes anywhere, nothing pushed, the
six governance rulings undecided and unrelitigated, all sealed
blind pairs untouched, Micah's frontier dirs untouched.

## Findings of fact the rulings rest on

The advocate and the skeptic agree, and the red team
independently verified, the following, and this judge takes
them as established:

- EXP1c iteration 3 sources are new this wave (first committed
  at 7fbd485b6), pure Zag, compiled with the pinned znc
  (SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
  and every committed artifact was reproduced byte-identically
  by the red team from committed sources.
- M3 is verbatim (score = mean experienced delta-energy +
  B0/(1+n), integer division, strict-greater deterministic
  argmax; B0=40 for arms 3 and 5, B0=120 for arms 4 and 6; no
  per-composition bonuses). M4 is exhaustive and exclusive
  (exactly the three frozen reflexes; the P-arm storm
  anticipation is inherited taught content).
- Medians hand-verified from run1.tsv: P=1200, R=1200, Z=50,
  I-survive=266, I-invent=269, I-survive-abl=1200,
  I-invent-abl=1200. K1 fires literally (266 <= 1200); K2
  survives (266 > 50); K3 ok (1200 not < 960); K6 fires
  literally on both ablation arms (1200 >= 266; 1200 >= 269).
- K7 fails: I-survive 0/13, I-invent 0/94, both below 0.50.
  Completed enumerations are 2/12 (I-survive, variants 2 and
  5) and 5/12 (I-invent, variants 2, 5, 6, 8, 11), not "5/12
  in each arm". The red team's "7 runs completed enumeration"
  is the sum 2+5 and is consistent.
- C3 gate numbers are correct: calibrator medians 1200 >= 720;
  d01=7 (variants 0,1,3,4,6,7,10), d02=12, d12=12 at the
  frozen dXY >= 1 threshold. All 12 f2 vector differences
  (vs f0 and vs f1) are e_end-only; ticks are identical at
  1200 for all three calibrators in all 12 variants.
- x1c_evidence.zag was edited at milestone 3 (0563e0cce, a
  30-line diff on top of the milestone-1 version) after the
  run data were visible at milestone 2 (26669a08d). The two
  fixes were disclosed, the diff is minimal and verified,
  and the note is byte-identical to the fixed generator's
  stdout. The record does not state what the pre-fix
  instrument emitted.
- The committed evidence note prints literal KILL labels for
  K1 ("K1 (median I-survive <= median R kills H1):
  I-survive=266 R=1200 KILL") and K6, and the milestone-3
  commit message repeats "K1 KILL ... K6 KILL"; the note never
  states that K7 voids them. The note does not print the
  addendum's explicit max-enum_tick comparison line (maximum
  1183 is derivable from the per-run rows).
- Fork battery: 56 named entries, 54 PASS, 0 FAIL, 2
  UNTESTABLE, 44 unique commits recomputed from this wave's
  own verdict table. Harness rebuilt pure-Zag byte-identical
  to the frozen instrument. Local HEAD moved mid-run from the
  task-pinned baf48e474 to 9c6646c04; pinning made the
  results inert to the move; 9c6646c04 was not tested.
- The last fresh tnn_chat FIT re-run was at 2021pdt (commit
  927b3f3f7) with staleness reset to 0 of 8. This wave did
  not re-run FIT. The fork report's claim of staleness
  "5 of 8" is arithmetically wrong; one wave has elapsed
  without a re-run, so staleness is 1 of 8.
- HUNT_2321.md recommends the EXP2-K4 redesign with a 3-wave
  auto-retire expiry clause ("if no curator path (his
  decision) exists within 3 waves of the redesigned prereg
  being draftable, RETIRE the lane"). It reserves that the
  final retire/keep call is his.
- The interactive survey covers fc1a43b8c..baf48e474 with full
  hit accounting and zero genuine interactive hits.

## M1: EXP1c iteration 3. AMEND.

The advocate moves entering iteration 3 as VOID as a test of
H1/H2 (K7), with K1/K6 as certified measurements and C3
certified PASS. The skeptic sustains the VOID but raises
three blocking items (A1, A2) and three caveats (A3, A4, A5).
This judge sustains A1 and A2 and adopts A3, A4, A5. The
motion passes only with the amended wording below, which is
binding verbatim for the wave's verdict entry.

(a) Verdict entry wording. Both sides agree on VOID framing;
the skeptic's A1 shows the archive still carries literal
KILL labels whose own definitions say "kills H1". The
precedent must be quoted verbatim in the verdict line so no
future adoption read can cite the note's KILL labels as
adopted kills. The amended verdict entry reads:

"EXP1c iteration 3: VOID as a test of H1/H2 (K7 fails: 0/13
and 0/94 learned-credit fractions, both below 0.50).
Judge-confirmed precedent: a void test cannot kill a
hypothesis. K7 takes precedence over any K1 firing. The
evidence note's and the milestone-3 commit message's literal
KILL labels for K1 and K6 are not adopted; K1 (266 <= 1200)
and K6 (1200 >= 266; 1200 >= 269) are certified as correct
literal computations recorded as measurements from a voided
run. K2 survives (266 > 50); K3 ok (1200 not < 960); C1
PASS; C2 PASS; C3 PASS on the specified gate (three
calibrator medians 1200 >= 720; pairwise vector-distinctness
d01=7, d02=12, d12=12 at dXY >= 1), with the composition
caveat in this ruling's item (b); K4 CANNOT-CONFIRM (no
audit attempted; with K7 VOID there is no learned strategy
to audit); K5 INCOMPLETE (no independent auditor;
implementer cannot self-certify). No DEAD label attaches to
H1. Completed enumerations are 2/12 (I-survive) and 5/12
(I-invent); the run records that the design failed to reach
its own choice phase, nothing about learned behavior.
Nothing is adopted."

(b) C3 PASS stands as certified on the specified gate, and
the "genuinely different decision rule" gloss is struck.
The skeptic's A2 is sustained on the measured evidence: all
12 f2 differences are e_end-only, ticks are identical at
1200 across all calibrators and all 12 variants, and the
dXY >= 1 threshold is a hair trigger that any non-identical
implementation satisfies via energy residuals alone. The
2021pdt verdict struck the "qualitatively distinct" claim
from the record; this wave's equivalent gloss ("genuinely a
different decision rule") rests on code reading, not on the
measured gate, and its reintroduction would certify on
thinner measured grounds than the claim the binding fix was
meant to secure. The amended certification wording reads:

"C3 PASS is certified on the specified gate only: the three
calibrator medians sit at 1200 (>= 720) and the pairwise
outcome-vector differences are d01=7, d02=12, d12=12 at the
frozen dXY >= 1 threshold. The 'genuinely a different
decision rule' gloss is struck as unsupported by
measurement. Recorded composition: every one of the 12 f2
vector differences (vs f0 and vs f1) is e_end-only; ticks
are identical at 1200 for all three calibrators in all 12
variants. The gate's dXY >= 1 threshold is a hair trigger
that any non-identical implementation satisfies through
energy residuals alone, so it does not establish
qualitative distinctness; the calibrators sit at the 1200
ceiling and the calibration discriminates nothing about
survival. Code-level f2 differences (open-loop patrol with
no target seeking; storms send it home to wait; an
energy-below-25 survival branch; an ACTIVE-mote-only eating
filter) are documented from source reading, and the e_end
gaps may be driven by the eating filter as much as by the
patrol rule. The binding F10/R1 in-Zag check is implemented
and passes as specified; the substantive distinctness
claim is not certified."

(c) The forward rule on the verdict emitter is warranted.
The skeptic's A3 is sustained as a forward requirement: the
evidence generator is the verdict instrument, and a
post-data edit to it is exactly where verdict-shopping
would occur. The 2021pdt tolerance covered agent/run
sources, not the verdict emitter. This judge sets the
binding forward requirement:

"The evidence (verdict) generator is frozen at milestone 1.
Any edit to it after data visibility invalidates the
milestone chain and requires a re-freeze and a full re-run
before the note may be regenerated; the record must state
what the pre-fix instrument emitted (crash vs wrong output
vs wrong verdicts). Disclosure, minimal diffs, and
byte-identical reproduction remain required but do not
substitute for the freeze."

This wave enters under the current tolerant standard
(disclosure, minimal diff, byte-identical reproduction,
independent hand recomputation all verified and holding);
the rule binds future waves.

(d) The K6 ablation interpretation carries the skeptic's
caveat. The advocate's "genuine intervention" claim is
accepted as to intervention; the skeptic's A4 is sustained
as to what the intervention measures. The amended K6
wording reads:

"K6 fires literally and is certified as a correct
computation. Interpretation caveat: the ablation excludes
COMBINE-containing sketches, which changes both the
invention channel and the exploration-risk profile (the I
arms die exploring COMBINE sketches with n_replans in the
hundreds; the ablation explores a smaller, safer 258-sketch
pool and never dies). The survival gains 266->1200 and
269->1200 are fully explained by the exploration-risk
change and cannot be separated from it; ticks-survived
cannot distinguish 'invention does not help' from
'exploration is lethal'. The ablation median saturates at
the 1200 ceiling and quantifies no invention effect. The
firings are recorded as measurements from a voided run and
may never be read as evidence about invention. The
binding 2021pdt rule is re-entered: any future adoption
must freeze the K6 operationalization first."

K7's evidentiary base carries the A5 correction already in
item (a)'s wording: 2/12 and 5/12, never "5/12 in each
arm", and the narrow interpretation.

M1 therefore enters as AMENDed: VOID as a test of H1/H2,
nothing adopted, with the four amended texts above binding
on the wave's verdict entry.

## M2: fork battery. AMEND.

The advocate moves CONFIRM [clean]. The skeptic sustains B1
(pinning) and B2 (staleness, headline) as caveats, with B1
requiring the pin in the verdict line. This judge agrees on
both, and additionally adjudicates the FIT staleness count:
the fork worker's "5 of 8" is wrong. The loop record shows
the last fresh FIT re-run at 2021pdt (commit 927b3f3f7) with
staleness reset to 0 of 8, and this wave did not re-run it,
so staleness is 1 of 8. The 5-of-8 claim does not enter the
record. The amended verdict line reads:

"CONFIRM the fork battery as a process confirmation
(toolchain and extraction stability only) at the pinned
run-start HEAD baf48e474: 56 named entries, 54 PASS, 0
FAIL, 2 UNTESTABLE (44 unique commits; the two
UNTESTABLEs are the expected rh-pull-1-head and
rh-pull-2-head, non-TNN research-doc trees, pinned
toolchain path absent, fourteen waves running). The
mid-run local HEAD move to 9c6646c04 was inert under
pinned-commit extraction; 9c6646c04 was not tested by this
battery and is left for the next wave's enumeration. The
headline count 56 named must travel with the 44-unique-commit
count. tnn_chat FIT: not re-run this wave; staleness is
1 of 8 (last fresh re-run at 2021pdt, staleness reset to
0 of 8; the fork report's 5-of-8 claim is corrected)."

The HEAD-race open question banked at 2021pdt repeats; it is
banked again, unchanged.

## M3: design lane NULLs. AMEND.

The advocate moves confirmation of the NULLs with the
EXP2-K4 redesign-or-retire recommendation. The skeptic's C1
(blocking) is sustained: the 3-wave auto-retire expiry is a
governance pre-decision smuggled into a design
recommendation. The recommendation reserves the final
retire/keep call to Micah, but retiring the lane on his
silence decides it for him; silence is not a decision, and
the advocate's "nothing here decides or pre-decides any of
his six rulings" is false as written. The skeptic's C2 is
sustained as a substantive objection: mechanical selection
over a self-authored, spec-informed problem set does not
produce spec-blindness, and the redesign asks Micah to waive
or redefine blocker 2, which is the status quo, not a
technical resolution.

The NULLs themselves are honestly surveyed and pass. The
recommendation language is amended to read:

"EXP2-K4: HELD, with a redesign-or-retire recommendation
(not a decision). The technical track (loop-owned
failure-trace corpus in pure Zag) is loop-executable. The
3-wave auto-retire expiry clause is struck as a loop
pre-commitment; it is converted to an explicit question to
Micah: does he approve a wave-counted expiry, or prefer an
alternative such as a standing written-HELD cadence? The
lane is not retired on his silence. The adoption of the
redesign (amending F1/F2 of the draft prereg), the F2
spec-blindness question, the acceptance of self-generated
failures as 'real deliberation failures' under the 0221pdt
forward requirement (a), and the final retire/keep call are
his decisions. The record states plainly: 'mechanical
selection attestation' over a self-authored, spec-informed
problem set does not establish spec-blindness; the
redesign does not resolve blocker 2 technically and asks
him to waive or redefine it. The redesign is not
self-executing: its validity as a K4 corpus needs the
judge's acceptance. B1 mechanism: NULL. COMP2-P11: HELD
(ruling 6 still OPEN). Trades: HELD. Sensory: NULL under
standing stand-downs. Nothing manufactured."

## M4: interactive survey NONE. CONFIRM.

The method, the merge range, and the full false-positive
accounting are verified as documented; zero genuine
interactive hits; the previously surveyed Micah REPLs are
correctly left as read-only closed frontier. Verdict: NONE,
pinned to fc1a43b8c..baf48e474.

## M5: commit-order self-check. CONFIRM, VALID.

The chain d9e96ad91 < 7fbd485b6 < 26669a08d < 0563e0cce is
strict and merge-base verified; the frozen prereg 8b456736b
strictly precedes every wave commit; the section-7 redraft
addendum was committed alone before any EXP1c
implementation file existed. The standing caveat is
restated, not implied: commit order evidences commit order
only, never run order and never content identity. It does
not show that the evidence generator was frozen before
data visibility (x1c_evidence.zag was edited at milestone
3 after the run data were visible; see M1(c)), nor that
calibration ran before the full runs.

## Binding forward requirements set by this judge

1. The evidence (verdict) generator is frozen at milestone
   1; any post-data edit invalidates the milestone chain and
   requires a re-freeze and a full re-run, with the record
   stating what the pre-fix instrument emitted. (M1(c))
2. Future evidence notes print the addendum's explicit
   max-enum_tick comparison against the corrected minimum.
   (O1, closed)
3. Any future adoption must freeze the K6 operationalization
   first; K6 firings from this wave may never be read as
   evidence about invention. (M1(d))
4. Fork-battery verdict lines are pinned to the run-start
   commit; headline named counts travel with the
   unique-commit count; FIT staleness is counted from the
   last fresh re-run. (M2)
5. No loop pre-commitment may retire a lane on Micah's
   silence; the EXP2-K4 redesign stays a recommendation with
   its expiry converted to an explicit question to him.
   (M3)

## Nothing touched

The six governance rulings remain OPEN and undecided. All
sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD,
S13, S14, whirlpool-planform) are untouched. Micah's
frontier dirs are untouched. Nothing is pushed. This
ruling file is uncommitted, left for the coordinator.
