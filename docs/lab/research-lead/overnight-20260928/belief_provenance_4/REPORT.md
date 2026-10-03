# REPORT: BP-4 (FP1 graded flip point, FP4 learned source discount, FP5 independence discount)

Worker: BELIEF-PROVENANCE-4 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_4/
Verdict: **BP-4-PASS** (all 8 preconditions, all 16 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method: frozen
prereg (committed as 313211172 before any implementation),
BP-3's belief machinery reused verbatim plus exactly one
new learner rule (R3-prime, the FP4 d_self learning rule),
four independent worlds, in-driver bars.

## 0. What was built

`bp4_learner.zag` is BP-3's `bp3_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files): the learner-owned u8 belief table, R1-R7,
eff(), b_retire with kind-3 reason edges, the lg()
liveness-gating baseline. No redesign; the task's "build on
BP-3" is literal.

`bp4_rules.zag` is the single new learner rule this lane
adds: `bp4_disconf_learn`, the R3-prime d_self learning
rule (DESIGN.md 3.1, 6; frozen form disclosed in PREREG
Section 1). On a disconfirmation experience: apply R3,
then if the belief is self-majority-sourced (b_self >
b_ext), d_self -= 25 (floor 0). Confirmations never move
d_self.

`bp4_driver.zag` is the battery driver: `bp4_build` (the
BP-3 world replay at pm=0, no mz3), `bp4_set_prov_tag`
(disclosed P6 source-partition scripting: field16 2=TAUGHT
on the external MAP's facts, 6=DERIVED-FROM-STRUCTURE on
the self MAP's facts; the block never reads node field16
of tag-1 facts, verified by source audit), the FP1 step
runner, the FP4 treatment/control/post-choice legs, the
FP5 confirmation battery, in-driver bars.

`bp4_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp4_learner.zag`
+ `bp4_rules.zag` + `bp4_driver.zag`. One `main`. Pinned
znc by absolute path, build exit 0 -> bp4_bin (370481
bytes); the A0102 warnings are the benign
ignored-return-value pattern pervasive in the frozen block
itself (same as BP-3).

## 1. Kill-bar results

Preconditions (8/8 PASS): PC-F1-BUILD (singleton==mv2,
mv3 prov rel 87 with 4 live type-1 facts), PC-F1-IDX
(navx=27, mv2=194, mv3=274, matching BP-3's measured ids),
PC-F1-SUP0 (leader 140 after 2 confirms, rival 100),
PC-F4-T-BUILD / PC-F4-C-BUILD (same world shape on WT/WC),
PC-F4-T-TAG / PC-F4-C-TAG (mv2 licensing (live,ext,self)
= (L,L,0); mv3 = (4,0,4)), PC-F5-BUILD.

FP1 (graded flip point), all PASS:
- K-FP1-SEQ: b_sup[mv3] = (140,105,52,13,0) across the
  five steps, exactly the hand-derived R4 compounding
  fractions (140*3/4, 105*2/4 truncated, 52*1/4, retire).
- K-FP1-FLIP: R7 = (274,274,194,194,194); the flip from
  leader to rival occurs exactly at s2, the second
  tombstone.
- K-FP1-RETIRE: at s4, kind-3 reason-2 self-edge on mv3,
  b_sup=0.
- K-FP1-KILLCRIT: at s4, lg=274 (existence says use-it)
  while R7=194 (belief says refuse). The belief layer is
  not decorative here: the refusal is the persistent-state
  form of the sealed XHIER-COUNTMAP-FIX K3a finding.
- K-FP1-SHAPE: support declines strictly at every step
  (140>105>52>13>0: graded weakening), while selection
  flips in exactly one step, at the crossing point, not
  at a bar boundary (52>=50 at the flip step). Answer to
  the open question: graded weakening, sudden selection
  flip.

FP4 (learned source discount), all PASS:
- K-FP4-T-D: d_self[mv3]=205 after the failure experience
  (255-2*25). The discount is learned, not fixed.
- K-FP4-T-SUP: b_sup 100/100 at choice (equal, as
  DESIGN.md requires).
- K-FP4-T-EFF: eff = 100/80 (82000/1020=80, integer).
- K-FP4-T-SEL: R7 = 194 (mv2, the external-sourced
  belief). The learned discount flips selection.
- K-FP4-C-D: d_self[mv3]=255 in the control arm: no
  experience, no discount (no researcher bias leak).
- K-FP4-C-SEL: R7 = -3 (exact tie at 100/100: no
  systematic discount).
- K-FP4-EXT-INERT: two disconfirmations of the
  external-majority belief leave d_self=255 (b_sup
  100->60 as expected): the rule is source-selective.

FP5 (independence discount), all PASS:
- K-FP5-SUP: b_sup = 160/220 (6x INC_LO vs 6x INC_HI).
- K-FP5-DIFF: 220-160 = 60 = 6*(INC_HI-INC_LO), exactly.
- K-FP5-SEL: R7 = 274 (mv3, the independently-confirmed
  belief). Independent confirmations weigh more.
- K-FP5-CONF: b_conf = 7/7 (same confirmation count;
  only independence differs). The C211 Probe-R failure
  mode (repetition without independence going falsely
  confident) does not occur.

K-DET: 3/3 runs byte-identical, SHA-256
7da16a1755cab5f0bd1eeff978aeb82cf8e7d38a5ba5810d980e3c635c1f4969.
K-HYG: pure Zag under safebin (`which python3`/`which
python` empty at build and run); zero em/en dash bytes in
all authored files (the only dash bytes in the lane are
znc's own A0102 warning text inside the machine-generated
build log, disclosed here); 0 new edge types (only
1/14/3; the driver's link_edge calls are the frozen
type-14 world replay), 0 new node types, 0 modes, 0
bridges, 0 handlers; xf_block.zag hash unchanged;
bp4_learner.zag byte-identical to bp3_learner.zag; opaque
identifiers. BP4-SUMMARY 24/24 in-driver; 26/26 with
K-DET/K-HYG.

## 2. What this means

FP1 is confirmed as preregistered, and the open shape
question is answered: weakening is graded (every step
strictly lowers support by the exact R4 fraction) while
selection flips suddenly at the crossing step. The flip
is a relative-comparison event, not a bar event: at s2
eff=52 is still above BAR0=50, yet R7 moves to the rival
because 52<100. This is the graded replacement for the
XHIER-COUNTMAP-FIX binary fence behaving as designed.

FP4 is confirmed as preregistered: d_self moves only
through experienced disconfirmation of self-sourced
beliefs, by the disclosed rule, and the movement is
behaviorally load-bearing (it flips the choice at equal
b_sup). The two falsifiers from DESIGN.md are both
tested and both clear: the treatment arm shows the
discount (205<255), the control arm shows none (255, tie
abstention), and external-majority disconfirmation does
not move the self discount. What is learned is the
discount's value and its behavioral consequence; the
update form (step 25, self-majority condition) remains
researcher-chosen disclosed machinery, and its
sensitivity is future work.

FP5 is confirmed as preregistered: six confirmations from
disjoint licensing sets outweigh six from one set by
exactly the accumulated INC_HI/INC_LO difference (60),
with confirmation counts held equal. Repetition without
independence does not go falsely confident.

With FP1, FP4, FP5 sealed here, FP2/FP3 (BP-2), and
FP6/FP7 (BP-3), all 7 falsifiable predictions of the
BELIEF-PROVENANCE DESIGN.md Section 8 are now sealed.

## 3. One-system accounting

New learner machinery this lane: exactly one function,
`bp4_disconf_learn` (the R3-prime d_self learning rule,
~12 lines). Everything else is BP-3's belief layer
verbatim plus test-harness code. 0 new edge types
(1/14/3 only), 0 new node types, 0 modes, 0 bridges, 0
handlers, 0 semantic cases. Beliefs remain learner-state
records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the exact R4 step
values and the single-step flip location (FP1); the
d_self trajectory 255->230->205 under two
self-majority disconfirmations, its behavioral flip at
equal b_sup, its immobility without experience and under
external-majority disconfirmation (FP4); the exact
160/220 split and the independence-driven selection
(FP5); determinism; hygiene.

Reasoned: that the d_self step of 25 and the
self-majority condition are adequate forms (the lane
tests that learning happens at all, is
experience-gated, and is source-selective, not that the
form is optimal); that the driver-supplied indep flag
fairly models disjoint vs shared licensing sets; that
the candidate-set formulation is the operational
conflict definition (as in FP7); that the scripted
failure/recovery evidence fairly models a
self-amplification failure (disclosed as scripted; the
sealed quantities are the d_self trajectory and the
selection outcome).

## 5. Open questions (not claimed)

d_self form sensitivity (step size, majority condition,
floor); whether disconfirmation should also move d_self
upward after confirmed self-sourced successes (the
current rule only moves downward, per DESIGN.md);
bar-adjustment trajectories; B-FACT/B-META records;
multi-hop/cyclic propagation; combiner alternatives;
eviction interaction; constant sensitivity.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with the
  lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-1/BP-2/BP-3 REPORT.md files are
  untouched.
- All 7 belief-layer falsifiable predictions are now
  sealed: FP1/FP4/FP5 (this lane), FP2/FP3 (BP-2),
  FP6/FP7 (BP-3). Suggested next steps from the BP-3
  open list: R3/R5 dynamics beyond scripted evidence,
  bar-adjustment trajectories, B-FACT/B-META records,
  multi-hop/cyclic propagation fixpoints, combiner
  alternatives, eviction interaction.
- Style: no em/en dashes in authored files (hyphens
  only), opaque identifiers throughout.
