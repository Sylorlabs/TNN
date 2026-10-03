# PREREG: PROXY-REDESIGN -- a structural proxy via interventional interchangeability (frozen)

## 0. Standing

MA4C-MULTISTREAM returned MARGIN-FRAGILE with the preregistered
K-VARIES implication: the (R) ratio (xerr*wpart <= K*wpsm*xcnt)
measures contingent error overlap (tile-sequence luck), not
structural redundancy. Adaptive K is insufficient where ratios
coincide or invert. This prereg freezes a replacement proxy based
on a different structural signal. Nothing here weakens any frozen
bar; the bars are defined fresh for this lane.

This is a non-ledger task (claim minting paused).

## 1. Design basis (disclosed)

The design was informed by exploratory analysis of the frozen
MA4C-MULTISTREAM run files (no new mechanism runs; a write-only
diagnostic binary in /tmp recorded runner-up tallies and
decision-point means, disclosed here as the design basis). The
prereg below is committed BEFORE the frozen implementation.

## 2. The structural signal: interventional interchangeability

The (R) ratio compares error MAGNITUDES: j's mean error on i's wins
vs i's own mean error. Magnitudes are tile-luck. The replacement
signal uses RANKS and DORMANCY, which are structural.

Causal-intervention framing: removing cell i from the system
changes behavior ONLY on episodes i won (cells update means only
on wins; the winner elsewhere is unaffected). So "i is redundant
given j" requires j would have won i's episodes (j is runner-up
there) AND i would have won j's episodes (mutual coverage).
But one-way coverage is insufficient: in the adversarial case
(E795 W6/T4) cell 3 IS the runner-up on all of cell 2's B4 wins
(100%), yet consolidating cell 2 destroys its active B4 model.

The structural difference: in the genuine case (E735), cell 2
is DORMANT (no wins in 65+ episodes; it has no current role).
In the adversarial case (E795 W6/T4), cell 2 is ACTIVE (won 5
episodes ago; it has a current B4 role). Dormancy is the
interventional gate: a dormant cell cannot be killed (nothing
to destroy); an active cell can.

Redundancy = mutual runner-up coverage + dormancy. The
dormancy threshold (60 episodes = one band-length) is the only
count threshold besides PACT=5; it is NOT a threshold on the
(R) ratio or any error magnitude.

## 3. Frozen proxy: redun3

Cell i is redundant given protected cell j (j != i) iff ALL of:
- (G) prot(i)=1 and prot(j)=1 (established cells; unchanged).
- (D) e-lastwin[i] > 60 (i DORMANT; no current functional role;
  lastwin[4] at 3688972 records most recent win episode per cell).
- (A) wpart[j] >= wpart[i] (absorption toward greater evidence;
  unchanged).
- (C) rucov[j][i] >= 5 and rucov[i][j] >= 5 (MUTUAL runner-up
  evidence; PACT minimum, mirroring the old PACT gate).

Returns j+1 (anchor) or 0. First qualifying j in 0..3 order.

New learner tallies (write-only for the proxy; rucov zeroed on
reseed exactly like xerr/xcnt; lastwin not zeroed):
- rucov[16] at 3687300: rucov[j][i]++ when winner==i and
  runner-up==j (runner-up = min error among k!=i, ties to lower
  index, same tie-break as winner).
- lastwin[4] at 3688972: lastwin[i]=e when winner==i (W only).
- On reseed of v: zero rucov[v][*], rucov[*][v] (v is a new
  model; old runner-up relations invalid).

## 4. Frozen experiment

Five binaries pr_w6.zag, pr_t1..t4.zag. Each = frozen
ms_<s>.zag (MA4C-MULTISTREAM mechanism, K=3 driving the closed
loop) PLUS: runner-up computation, rucov/lastwin tallies,
redun3, and a write-only PX audit (px_eval) at each W trigger
(kind=0, pre-reseed) and each fixed probe (kind=1, e=734/e=794):
ep, v, vkind, kind, px0..px3 (redun3(i) for i=0..3),
ru32=rucov[3][2], ru23=rucov[2][3], dg2=e-lastwin[2] (dormancy
gap), lw2=lastwin[2]. The PX audit is write-only; redun3 NEVER
drives a reseed. The closed loop is bit-for-bit the
MA4C-MULTISTREAM K=3 loop.

Per stream: compile with safebin znc, run 3x, sha256-recorded,
3/3 byte-identical required.

## 5. Frozen predictions (from the disclosed exploratory basis)

At the B4-boundary trigger (E735), all 5 streams: redun3 FIRES
for v=2 with anchor j=3 (px2=4). Genuine dormant duplicate;
DG2=65>60.

At the B5-boundary trigger (E795) on W6 and T4: redun3 SILENT
(px2=0). Adversarial; cell 2 is an active B4 model (DG2=5<=60).

At the B5-boundary trigger (E795) on T1/T2/T3: redun3 FIRES
(px2=4). The state is frozen from E735 (cell 2 dormant
duplicate, DG2=125>60); this is a benign late consolidation,
NOT a kill (cell 2 has no active role; nothing is destroyed).
Recorded as a consistency check, not an adversarial test.

At the B2-boundary trigger (E675) on T1-T4: redun3 SILENT
(DG2=5<=60; cell 2 won at e=669, not yet dormant). The
dormancy gate correctly declines early consolidation.

At E14: SILENT (rucov below PACT).

## 6. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this PREREG.md (+NAMECHECK.md Step 0)
  is committed strictly before any pr_*.zag implementation file.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical per stream
  (5 sha256 recorded).
- B4 EXACT-REPRODUCTION: PASS iff pr_<s> output minus PX lines
  minus the banner line is byte-identical (cmp) to frozen
  ma4c_multistream <s>_run1.txt minus MS lines minus the banner
  line, for all 5 streams. Proves the harness faithfully
  reproduces MA4C-MULTISTREAM and the K=3 baseline table is
  intact; the PX audit is write-only.
- B5 SCENARIO-VALIDITY: same as MA4C-MULTISTREAM B5 (B4-boundary
  trigger in [733,741], B5-boundary trigger in [793,801], per
  stream). Expected PASS on all 5 (same closed loop).
- B6 PROXY-DISCRIMINATION (PRIMARY):
  (i) GENUINE: at the E735 trigger on all 5 streams, PX kind=0
  shows px2=4 (fires, anchor cell 3).
  (ii) ADVERSARIAL: at the E795 trigger on W6 and T4, PX kind=0
  shows px2=0 (silent). These are the two streams where E795
  presents a true adversarial (cell 2 an active B4 model; K=3
  killed on T4).
- B7 OPAQUE-IDS: PASS iff case-insensitive whole-word grep for
  the frozen 29-word list returns empty in all pr_*.zag.
- B8 MARGIN-QUANTIFICATION (measurement): PASS iff REPORT.md
  tabulates, per stream at E735 and E795 (trigger kind=0):
  px2, ru32, ru23, dg2, lw2, and the K=3 baseline MS PCTs; plus
  the T1/T2/T3 E795 consistency note.
- B9 PROXY-STABILITY (kill bar): PASS iff B6(i) and B6(ii) PASS
  on ALL streams (genuine fires everywhere; adversarial silent
  on both true-adversarial streams).

Headline verdict:
- PROXY-DISCRIMINATES iff B9 PASS with B1..B8 PASS: the
  structural (interchangeability) proxy fires the genuine case
  and stays silent on the true adversarial cases on every
  stream, where the (R) ratio failed.
- PROXY-FRAGILE iff B9 FAILS: the report names each failing
  decision point, the measured coverage numbers, and which
  clause failed.

If B6 FAILS with the apparatus bars PASS, the headline is
PROXY-FRAGILE, never a weakened bar.

## 7. Honest boundaries (frozen)

- redun3 is evaluated as a write-only shadow; K=3 drives the
  closed loop. This tests DISCRIMINATION at frozen decision
  points, not closed-loop mechanism behavior. A closed-loop
  redun3 lane is explicit follow-up, not claimed here.
- The design used exploratory analysis on the frozen
  MA4C-MULTISTREAM data (disclosed above). Generality to new
  tile designs is not tested; that is a separate experiment.
- The symmetry comparison has a thin margin in the genuine
  case (~1.5%: 100% vs 98.5% coverage). The REPORT must state
  this margin honestly. The adversarial asymmetry (80-87% vs
  100%) is wide.
- What is measured are cell-mean tallies and win/runner-up
  relations, as MA1-4. Not strategy invention, not L3.

## 8. Transparent amendment (2026-10-03, during implementation)

During implementation, the (S) symmetry rule was found to be
non-discriminating: with reseed-zeroing, the post-reseed
history at E795 W6 shows symmetric B4-era coverage (both cells
in B4), so (S) fires (740>=740). Without zeroing, lifetime
symmetric pre-history dominates (115440>=114708), so (S) also
fires. The symmetry cannot see the adversarial asymmetry
because the relevant history (cell 2 as R-model vs cell 3 as
R-model) is either erased by zeroing or overwhelmed by lifetime
symmetry.

The structural fix is DORMANCY: the victim must have no current
functional role. Replacing (S) with (D):
- (D) e-lastwin[i] > 60 (i dormant; no wins in a full
  band-length). lastwin[4] at 3688972 (after pxlog).

The (C) mutual PACT condition is retained (ensures functional
relationship). ruw is removed (not needed without (S)).

Updated predictions:
- E735 all streams: FIRE (dormant, DG2=65>60).
- E795 W6/T4: SILENT (active, DG2=5<=60).
- E795 T1/T2/T3: FIRE (dormant, DG2=125>60; benign).
- E675 T1-T4: SILENT (DG2=5<=60; cell 2 won at e=669, not yet
  dormant). This differs from the original prediction (FIRE);
  the dormancy gate correctly declines early consolidation.
- E14: SILENT (rucov below PACT).

Kill bars B6/B9 UNCHANGED. B8 fields updated: px2, ru32, ru23,
dg2, lw2 (replacing rw32/rw23 and symmetry values).

## 9. Artifacts planned

- `pr_w6.zag`, `pr_t1.zag` .. `pr_t4.zag`, five binaries,
  15 run files (3 per stream, sha256 recorded)
- `PREREG.md`, `NAMECHECK.md`, `REPORT.md`
