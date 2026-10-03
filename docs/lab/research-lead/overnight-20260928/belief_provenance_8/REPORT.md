# REPORT: BP-8 (multi-channel absorption, 12-cycle, heterogeneous cycles)

Worker: BELIEF-PROVENANCE-8 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_8/
Verdict: **BP-8-PASS** (all 3 preconditions, all 18 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method:
frozen prereg (committed before any implementation),
one transparent amendment after the first run exposed
one prereg composition slip (documented in PREREG.md
Section 5b; no frozen rule changed), BP-7's belief
machinery reused verbatim plus the verbatim BP-7
absorb body, zero new learner machinery, three world
arms, in-driver bars.

## 0. What was built

`bp8_learner.zag` is BP-7's `bp7_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files, `cmp` clean): the learner-owned u8 belief
table, R1-R7, eff(), b_retire, bp2_bar_after. No redesign.

`bp8_driver.zag` is the whole lane: three world arms
(MCH/CY12/HET), bp8_absorb (the BP-7 absorb body
verbatim, renamed), bp8_allsup (all-sup test helper),
bp8_selfcnt, world builders per arm, in-driver bars.

`bp8_full.zag` = block lines 1..2668 of BP-7's
bp7_full.zag (the patched block, verbatim, SHA-256
172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) +
`bp8_learner.zag` + `bp8_driver.zag`. One `main`.
Pinned znc by absolute path (safebin znc is a symlink
to it, identical SHA-256), build exit 0 -> bp8_bin
(376036 bytes); the A0102 warnings are the benign
ignored-return-value pattern pervasive in the frozen
block itself (same as BP-4 through BP-7).

Amendment round (disclosed): the first implementation
run went 20/21. Diagnosis: K-CY12-RAISE was my
composition slip, not an implementation error. The
prereg said z4 "stays 100" at the raise 1-hop, but the
FULL sweep had already set every node to 40
(K-CY12-FULL/K-CY12-FIX passed) and nothing touches
z4 before the raise 1-hop, so the frozen rules give
z4=40. The implementation was faithful (CY12-RAISED
emitted z6=80; R6(z5) set z5=80). Corrected bar:
z6==80 && z5==80 && z4==40; the discriminating
content is preserved (a transitive one-application
propagation would have set z4=80). PREREG.md Section
5b records the correction with the re-derivation;
Section 3's hand-derivation updated to match. The
lane was then re-run from scratch: 21/21.

## 1. Kill-bar results

Preconditions (3/3 PASS): PC-MCH-FORM (mS: sup 100
ext 1 self 0; mR: sup 100 ext 0 self 1; mM: sup 100
ext 1 self 1), PC-CY12-FORM (all 12 sup 100),
PC-HET-FORM (all 6 sup 100).

MCH (multi-channel absorption), all PASS:
- K-MCH-RETS: ra==1 (match) && rb==0 (first
  contradict): the block evidence codes.
- K-MCH-SAME: same fact, match then contradict:
  n7==1 && n3==1 && sup==90 && conf==0 && disc==1.
  Both channels absorb; the R3 zeroes the conf the
  R2 just set, pinning the frozen R2-then-R3
  application order (R3-then-R2 would give 90/1/0).
- K-MCH-ORD: contradict then match: n7==0 &&
  n3==1 && sup==80 && disc==1 && conf==0. The block
  drops a match that arrives after a contradict on
  the same fact, so absorption is order-sensitive at
  the evidence layer: only the contradict absorbs.
  (The match's raw ret was emitted not barred:
  probe P7 showed it is 1 graph-licensed vs 0
  graph-less; the absorb-relevant invariant n7==0
  holds in both.)
- K-MCH-SAT: two type-7s on fM1: n7==2 &&
  conf==2 && sup==110. The two edges collapse to
  ONE R2 (conf 2, not 3): per-channel
  single-application saturation, measured.
- K-MCH-MULTI: then one type-3 on fM2: n3==1 &&
  sup==90 && conf==0 && disc==1.
- K-MCH-BLIND: sup/conf/disc equal for mS and mM
  (90/0/1 both). Same-fact and multi-fact delivery
  net identically: the layer is fact-blind given
  the same channel multiset.

CY12 (12-cycle, homogeneous type-14), all PASS:
- K-CY12-WEAK: z6=40 after 3x R3.
- K-CY12-1HOP: R6(z5)=40, ret 40; z4 and z11 stay
  100. One hop only.
- K-CY12-FULL: one backward R6 sweep: all 12 are
  40. The min converges around the full ring.
- K-CY12-FIX: re-application: all 12 still 40
  (fixpoint, no oscillation at 12 nodes).
- K-CY12-RAISE: 2x R2(z6,1) -> 80; R6(z5)=80;
  z4 stays 40. The raise also moves exactly one
  hop per application.
- K-CY12-RAISEFULL: backward sweep: all 12 are 80.
  Snap-up generalizes to 12 nodes.

HET (6-cycle, heterogeneous edges
v1-14->v2-14->v3-1->v4-14->v5-3->v6-14->v1),
all PASS:
- K-HET-WEAK: v4=40 after 3x R3.
- K-HET-BLOCK: R6(v3) ret==255, v3 stays 100,
  v4 stays 40. The type-1 edge blocks the 1-hop
  that CY5/CY12 showed: R6 is a no-op where no
  type-14 successor exists.
- K-HET-ERASE: R6(v4) ret==100, v4 back to 100.
  The isolated weakening is reabsorbed from the
  healthy type-14 successor; in the homogeneous
  ring the weakened node kept 40 through the sweep
  because its successor was weakened first, which
  cannot happen across the type-1 edge.
- K-HET-FULL: full sweep: all 6 are 100.
- K-HET-FIX: re-application: all 6 still 100.
- K-HET-T3: after 3x R3(v6) (w6pre=40):
  R6(v5) ret==255, v5 stays 100 (the type-3 edge
  carries nothing), R6(v6) -> v6=100. A weakening
  behind a type-3 edge is likewise reabsorbed.

K-DET: 3/3 runs byte-identical, SHA-256
fa9caf0f7a3c025cf72d6e83ef143252699aa1bc58ff4c4575705a3b02ce2bae.
K-HYG: pure Zag under safebin (`which python3`/`which
python` empty at build and run); zero em/en dash bytes
in all authored files and run outputs; 0 new edge types
(1/3/7/14 all pre-existing; the HET ring reuses
pre-existing kinds 1 and 3 between composites); 0 new
node types (tags 1/3/20 pre-existing); 0 modes, 0
bridges, 0 handlers; block SHA-256 unchanged;
bp8_learner.zag byte-identical to bp7_learner.zag;
opaque identifiers. BP8-SUMMARY 21/21 in-driver;
23/23 with K-DET/K-HYG.

## 2. What this means

Absorption is per-channel, not per-edge and not
per-fact. The frozen absorb applies at most one R2
and one R3 per call however many new edges the
watermarks saw, and the driver calls it once per
fact, so the belief record cannot tell whether a
confirm+contradict arrived on one fact or two.
Three consequences measured: (1) same-fact
match+contradict nets 90/0/1 with the frozen
R2-then-R3 order pinned by the counters; (2) the
block makes absorption order-sensitive one level
down: contradict-then-match delivers only the
contradict (the later match is dropped on the
original fact); (3) two type-7s saturate to one R2.
Whether per-channel saturation is the right
convention is not decided here; the frozen behavior
is measured, not endorsed.

The cycle fixpoint generalizes to larger homogeneous
cycles and does NOT generalize to heterogeneous
ones, and the reason is the same in both cases: R6
is edge-typed. On 12 type-14 nodes the BP-6 results
replicate exactly (min-convergence via one backward
sweep, idempotent fixpoint, one-hop raise, full-ring
snap-up). On the mixed ring the "cycle" as a
graph-theoretic object is not what converges: each
R6 application reads only type-14 successors, so a
type-1 or type-3 edge cuts the ring into type-14
reachability components. A weakening isolated by
such a cut cannot spread and is reabsorbed the
moment R6 touches the weakened node itself (it
recombines from healthy type-14 successors). The
honest statement: convergence holds per type-14
component; heterogeneous edges do not break the
fixpoint property (re-application stays idempotent),
they change what it converges to.

## 3. One-system accounting

New learner machinery this lane: ZERO functions.
bp8_absorb is the BP-7 absorb body verbatim
(renamed); bp8_allsup is a test-harness counting
helper. R2/R3/R6/R7 and the bar rule are untouched.
0 new edge types, 0 new node types, 0 modes, 0
bridges, 0 handlers, 0 semantic cases. Beliefs remain
learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the exact
absorption nets for same-fact (90/0/1), reversed
order (80/1/0 with n7==0), saturated multi-edge
(conf 2 not 3), multi-fact (90/0/1), and the
same-fact/multi-fact net equality; the 12-cycle
weak/1-hop/full/fix/raise/raise-full values
(40/40/all-40/all-40/80/all-80); the heterogeneous
ring block (ret 255), erase (ret 100), full sweep
(all 100), fixpoint, and type-3 no-op plus
reabsorption.

Reasoned: that per-channel saturation is the
correct reading of the frozen absorb (it is what
the code does; whether it should is out of scope);
that R6's type-14 restriction is the architectural
reason for the HET result (follows from the frozen
R6 source, which matches only kind-14 edges);
that convergence holds per type-14 reachability
component in general (tested on one 6-ring with one
type-1 and one type-3 edge, not on all topologies).

## 5. Open questions (not claimed)

Whether absorption should be per-edge rather than
per-channel (saturation measured, not judged);
whether R6 should follow non-14 edges (measured as
type-restricted); recovery paths for reabsorbed
weakenings; eviction-sync design (still needs the
parent ruling: persist vs tombstone vs R4-retire);
per-belief bar adoption (BP-7 evidence stands);
d_self recovery (BP-7 evidence stands).

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with
  the lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-2 through BP-7 REPORT.md files
  are untouched. The 7 sealed predictions stay sealed;
  this lane adds open-dynamics evidence only.
- The amendment round is disclosed in full in
  PREREG.md Section 5b: one composition slip of mine
  (z4=40 not 100 at the raise 1-hop), re-derived from
  the frozen rules; no implementation rule changed to
  chase the bar.
- Suggested nexts from the remaining open list:
  eviction-sync design decision (still needs your
  ruling); whether to adopt per-belief bars; whether
  d_self needs a recovery path; per-edge vs
  per-channel absorption (now measured); R6 edge
  typing (now measured).
- Style: no em/en dashes in authored files (hyphens
  only), opaque identifiers throughout.
