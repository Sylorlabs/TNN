# REPORT: BP-7 (d_self dynamics, bar meta-parameter sensitivity, per-belief bars)

Worker: BELIEF-PROVENANCE-7 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_7/
Verdict: **BP-7-PASS** (all 3 preconditions, all 25 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method: frozen
prereg (committed as be9f3fea1 before any implementation),
one transparent amendment round after the first run exposed
three prereg errors (two arithmetic slips, one wrong block
assumption; documented in PREREG.md Section 5b), BP-6's
belief machinery reused verbatim plus the verbatim BP-4
R3-prime rule, zero new learner machinery, three world
arms, in-driver bars.

## 0. What was built

`bp7_learner.zag` is BP-6's `bp6_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files, `cmp` clean): the learner-owned u8 belief
table, R1-R7, eff(), b_retire, bp2_bar_after. No redesign.

`bp4_rules.zag` is BP-4's frozen R3-prime file reused
verbatim (SHA-256
7392299309082836bf376bb445492ef8d9fd75b3d857ad425b8ca74d7399e4d9,
re-verified): exactly one function, bp4_disconf_learn
(R3, then d_self -= 25 floored at 0 iff b_self >
b_ext at call time). Frozen FP4 code, not new
machinery.

`bp7_driver.zag` is the whole lane: three world arms
(DSELF/META/PBAR), bp7_absorb (the BP-6 absorb
renamed), the driver-side experimental parameterized
bar rule bp7_bar_param, the driver-side experimental
per-belief selection bp7_select_pbar, bp7_kill_self_prov,
the META event helper, commitment bookkeeping,
in-driver bars.

`bp7_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp7_learner.zag`
+ `bp4_rules.zag` + `bp7_driver.zag`. One `main`. Pinned znc by absolute path,
build exit 0 -> bp7_bin (411569 bytes); the A0102 warnings
are the benign ignored-return-value pattern pervasive in
the frozen block itself (same as BP-4/BP-5/BP-6).

Amendment round (disclosed): the first implementation run
went 23/26. Diagnosis: (1) K-MT-S5 was my arithmetic
slip: at e4 the S5 bar is already 50 (FPs never raised
it), so 100 >= 2*50 fires the lower a step earlier than
I hand-wrote; true final 48, not 49. The implementation
was faithful to the frozen rule (unit bars K-MT-U1..U4
all passed); the hand composition was wrong. (2)
K-PB-STREAK was my slip: bp2_form sets b_conf=1, so 40
R2s give conf 41, not 40 (same pattern as BP-6
PC-COMB-FORM). (3) K-PB-AVAIL exposed a wrong prereg
assumption about the block: ev_observe writes at most
one type-3 per fact (probe-verified 2026-10-03 in
/tmp/bp7probe: first contradict ret 0 + one type-3;
repeats ret 1, no new edge; a contradicted fact ignores
later matches too), so the world as built could not
deliver FP3 as a repeat contradict. World fix: mA
promotes 3 facts, one contradict each; PC-PB-FORM
updated (ext 1->2). PREREG.md Section 5b records all
three corrections with the re-derivations; S3/S5 share
the final 48, so their already-preregistered e1 values
were promoted to explicit bars K-MT-S3E1/K-MT-S5E1.
The lane was then re-run from scratch: 28/28.

## 1. Kill-bar results

Preconditions (3/3 PASS): PC-DS-FORM (m: sup 100,
ext 1, self 3, d 255; m2: 3/1; m3: 2/2; m4: 1/3),
PC-MT-FORM (mA sup 100 ext 2 self 2; mB sup 60),
PC-PB-FORM (mA sup 100 ext 2 self 1; mB/mX sup 50;
mO sup 100).

DSELF (d_self long trajectory), all PASS:
- K-DS-TRJ: after 10x bp4_disconf_learn: d_self=5,
  sup=0, disc=10, conf=0. The discount keeps
  deepening after support is gone (sup hit 0 at k=5,
  d_self still falling).
- K-DS-FLOOR: 11th application: d_self=0, no u8
  wraparound (the max(0,...) guard holds).
- K-DS-NOREC: 3x R2 after the floor: d_self stays 0
  while sup recovers 0->30 and conf=3. The frozen
  machinery has NO recovery path: the discount is a
  one-way ratchet.
- K-DS-EFF: bp2_eff=7 at sup 30 (undiscounted it
  would be 30). The ratchet has teeth on selection
  weight, not just on a stored number.
- K-DS-SEL: ext-majority m2 after 5x: d_self=255,
  sup=0, disc=5. Source-selectivity holds even as
  support is destroyed: the discount never fires
  without a self-majority.
- K-DS-BOUND: tied m3 (2/2) after 2x: d_self=255,
  sup=60. The strict > is load-bearing at the
  boundary.
- K-DS-FLIP: m4 after killing 2 self facts +
  relicense (sup 50, ext 1, self 1) + 2x: d_self=
  255, sup=10. The majority condition is evaluated
  live at each disconfirmation, not frozen at
  formation: losing the majority mid-trajectory
  stops the discount.

META (bar meta-parameter sensitivity), all PASS:
- K-MT-U1..U4: bp7_bar_param unit values 51/50/10/
  50 (raise, 1.5x-threshold lower, floor, zero-inc).
- K-MT-S1: 50 (frozen replication of BP-6's BA
  trajectory 50->51->51->51->51->50: the control
  holds).
- K-MT-S2: 52 (inc=3: upward drift; the raise step
  dominates).
- K-MT-S3: 48 (dec=3: downward drift).
- K-MT-S4: 47 (1.5x threshold: ratchets down every
  step, 51->50->49->48->47).
- K-MT-S5: 48 (inc=0: FPs never move the bar; the
  raise is load-bearing).
- K-MT-S6: 51 (dec=0: permanent ratchet, one FP is
  never forgiven).
- K-MT-S3E1/K-MT-S5E1: 51 vs 50 after e1: the inc
  step is what separates the two settings that share
  the final 48.
- K-MT-SEL: all 30 selections (5 events x 6
  settings) == mA: the outcome sequence is
  bar-independent, so the sweep is clean.

PBAR (per-belief bars), all PASS:
- K-PB-ISO: after mA's first FP: global bar 51
  excludes the innocent mB (R7({mB},51)=-3, eff 50
  < 51) while per-belief bars admit it
  (select_pbar({mB})==mB, pb[mB]=50). The FP penalty
  stays on the belief that earned it.
- K-PB-AVAIL: after mA's third FP: global bar 53
  abstains entirely (R7({mA,mB},53)=-3: 40 and 50
  both below) while per-belief selection still
  returns mB (mA excluded at pb 53, mB admitted at
  pb 50). Availability under population-wide bar
  inflation.
- K-PB-TEETH: mX's own FP raises pb[mX] to 51 and
  select_pbar({mX})==-3: the per-belief bar still
  punishes where earned.
- K-PB-STREAK: 40 world-driven TPs: pb[mO] 50->10,
  sup 255, conf 41, selected every step.
- K-PB-OVERFIT: after 12 disconfirmations (sup 15):
  select_pbar({mO})==mO (15>=10: selected on thin
  evidence) while bp2_select({mO},53)==-3 (the
  population-informed global bar refuses). The
  per-belief bar overfits to the local lucky
  streak: help and cost both measured, a
  discriminating pair each way.

K-DET: 3/3 runs byte-identical, SHA-256
e4dcfdd510433e39834e353595f3cc5a62aadfe74fefaeefc846942b5063a0e3.
K-HYG: pure Zag under safebin (`which python3`/`which
python` empty at build and run); zero em/en dash bytes
in all authored files and run outputs; 0 new edge types
(1/3/7/14 all pre-existing in the block; 7 is
block-written evidence); 0 new node types (tags 1/3/20
pre-existing); 0 modes, 0 bridges, 0 handlers;
xf_block.zag hash unchanged; bp7_learner.zag
byte-identical to bp6_learner.zag; bp4_rules.zag reused
verbatim; opaque identifiers. BP7-SUMMARY 28/28
in-driver; 30/30 with K-DET/K-HYG.

## 2. What this means

d_self is a one-way ratchet with live source gating.
The frozen R3-prime rule discounts only on
self-majority disconfirmation, floors cleanly at 0,
never recovers (confirmations do not touch it even
from the floor), and the majority test is re-evaluated
at each disconfirmation against current licensing, so
a belief that loses its self-majority mid-trajectory
stops discounting. The discount bites selection
weight (eff 30->7), not just a stored field. Whether
the architecture should have a learner-owned recovery
path is now a measured design question, not an
assumption: the current answer is that none exists.

The bar's meta-parameters all matter, and the frozen
setting sits in the balanced band. Every
meta-parameter moves the trajectory: inc sets the FP
response (0 = the bar never learns from false
positives), dec sets the forgiveness rate (0 = one FP
is never forgiven), the 2x threshold sets how easy a
true positive must be to earn a lowering (1.5x
ratchets down every step). Only the frozen (1,1,2x)
setting is neutral over a balanced FP/TP cycle; the
stable region is the inc/dec-balanced band around it.
The sweep also replicates BP-6's BA trajectory
exactly as its control arm.

Per-belief bars help and overfit, both measured. The
help: penalties stay local (isolation) and the system
keeps a usable candidate when the global bar inflates
past everything (availability). The cost: a locally
lucky belief drives its own bar to the floor and is
then selected on eff 15 where the population-informed
global bar refuses (overfit to a short streak). The
architectural difference under test is
credit-assignment scope: the global bar tracks the
selected belief's commitments; per-belief bars track
each belief's own outcomes. Adopting per-belief bars
is a parent-level design judgment with both sides now
measured.

A block semantics finding, probe-verified: evidence
edges are one-shot per fact for contradicts (first
contradict: ret 0 + one type-3; repeats: ret 1, no new
edge; contradicted facts ignore later matches), while
matches accumulate type-7s on never-contradicted
facts. The META arm's design (matches only on
never-contradicted facts) is consistent with this;
the PBAR world was corrected to one-contradict-per-fact.

## 3. One-system accounting

New learner machinery this lane: ZERO functions.
bp4_disconf_learn is frozen BP-4 code reused verbatim;
bp7_bar_param and the per-belief bars
(bp7_select_pbar, the pb array) are driver-side
experimental code explicitly not adopted into the
belief layer; the META sweep and PBAR comparison are
evidence for keeping or changing the frozen rules,
not changes. 0 new edge types, 0 new node types, 0
modes, 0 bridges, 0 handlers, 0 semantic cases.
Beliefs remain learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the full d_self
trajectory to the floor (255->5 at k=10, 0 at k=11,
no wraparound), the absence of any recovery path
(d_self stays 0 through 3 confirmations), the eff
teeth (7 vs 30), source-selectivity at support 0,
the strict-majority boundary, the live majority
re-evaluation after relicensing; six bar
meta-parameter settings on one world-driven evidence
stream with exact trajectories (50/52/48/47/48/51)
and e1 discrimination of the colliding pair; the
per-belief help pair (isolation, availability), the
teeth check, the 40-TP streak to MIN_BAR, and the
overfit divergence pair at eff 15.

Reasoned: that the inc/dec-balanced band around the
frozen setting is the stable region (follows from
the drift directions, not from a longer-horizon
stability proof); that per-belief adoption is a
design judgment (both sides measured, not decided
here); that a d_self recovery rule would be new
learner machinery (tested absent, not implemented).

## 5. Open questions (not claimed)

A learner-owned d_self recovery rule (measured
absent; whether one should exist is a design
decision); per-belief bar adoption (help and cost
measured; decision left to the parent); the bar
meta-parameter choice (sensitivity mapped; the
frozen setting is the neutral one, not proven
optimal); eviction-sync design (still needs the
parent ruling: persist vs tombstone vs R4-retire);
multi-channel absorption; cycles larger than 5 or
with heterogeneous edge structure.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with
  the lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-2 through BP-6 REPORT.md files
  are untouched. The 7 sealed predictions stay sealed;
  this lane adds open-dynamics evidence only.
- The amendment round is disclosed in full in
  PREREG.md Section 5b: two of my arithmetic slips
  and one wrong block assumption, each re-derived,
  none of the implementation rules changed to chase
  a bar.
- Suggested next from the remaining open list:
  eviction-sync design decision (still needs your
  ruling); multi-channel absorption; whether to
  adopt per-belief bars (evidence above); whether
  d_self needs a recovery path (evidence above).
- Style: no em/en dashes in authored files (hyphens
  only), opaque identifiers throughout.
