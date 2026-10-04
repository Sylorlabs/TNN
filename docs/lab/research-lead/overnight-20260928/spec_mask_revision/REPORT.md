# REPORT: Specialize Mask Revision (SHIFT)

Worker: Specialize Mask Revision Worker (subagent, 2026-10-02).
Prereg: `spec_mask_revision/PREREG.md`, frozen alone at commit
cda792126 before any implementation existed. No amendments: the
first full build reproduced every frozen hand-derived expectation
with zero source changes after the initial (pre-run) removal of one
unused driver local.

## Verdict

**SPEC-MASK-REVISION-COMPLETE.** All seven kill bars PASS, no
falsifier fired, 3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`) plus experiment side
(`world.zag`, `driver.zag`), assembled as
`cat learner.zag world.zag driver.zag > rv_full.zag` (1010 lines)
and compiled with the pinned znc to `rv_bin`. The learner holds: X
episode recall with a learned replay length (L=6) and per-kind
informative slot masks, the L2 SPECIALIZE standing rule (unchanged
in mechanism from l2_l3_spec), Y threshold decide on scalars (t=6),
and the greedy constructor over the frozen op basis
{CPY,ADD,SUB,MAX,MIN} on 2 registers with first-2 loading. The one
new mechanism is `x_revise_masks`: a consolidation function with a
consolidation pointer REV_PTR that recomputes the per-kind variance
masks over the not-yet-consolidated episode window [REV_PTR, XN),
overwrites a kind's mask iff the window holds at least one episode
of that kind, then advances REV_PTR. The first call (after phase-0)
is the initial learn; later calls are revisions. The consolidation
timing is driver-scheduled (disclosed experimental control, the
frozen-timing precedent); the recomputation is generic learner
machinery with no world knowledge.

The hidden world (driver side only): phase 1 is the ORCHARD world
(TRUE1: PICK iff the kind's signal pair sums >= 10, kind 1 on
(d,e), kind 2 on (b,c)). Phase 2 moves the informative slots
(TRUE2: kind 1 on (b,c), kind 2 on (d,e); old slots zero).

## Kill-bar results (from rv_run1.txt, reproduced in runs 2 and 3)

- K-RV-1 (masks learned): post-phase-0 `LEARN-MASKS k1=48 k2=12
  revptr=4`. PASS.
- K-RV-2 (work initially): Z-PHASE1 4/4; M1 n=1, t=6,
  prog=1,0,1,0,0,0,... (M = [ADD R0,R1]); construction trace
  matches the frozen hand derivation exactly (`C-ROUND 1 base=6
  eval=20 win=1,0,1 gain=2 score=8 t=6`; `C-ROUND 2 base=8 eval=20
  stop`); T-AGREE y=6 m=6. PASS.
- K-RV-3 (world change breaks them): Z-STALE-KEEP exactly 2/4 (Z
  lines show stale replays `seq=0,0`, s=0, both picks missed: the
  always-skip baseline) AND STALE-REBUILD construction halts with
  n=0 (`C-ROUND 1 base=4 eval=20 stop`: every phase-2 train
  episode replays (0,0) through the stale masks, so no candidate
  beats the 4/8 empty baseline) AND Z-STALE-REBUILD 0/4 (dec=-1,
  M absent). The break is at the mask level, not in M: the
  information-starvation proof. PASS.
- K-RV-4 (learner revises masks): `REVISE MASKS k1=12 k2=48
  revptr=24`. The masks SWAP 48<->12 from the phase-2 window
  (episodes 16..23 = ids 21..28) through the generic variance
  criterion. PASS.
- K-RV-5 (revised work): Z-REVISE 4/4 with M1 reused (M slot still
  n=1, gen=1, t=6, prog=1,0,1,... printed from learner state in
  `M-STATE-POST-REVISE`); every Z line shows a 2-reading revised
  replay ([5,8],[3,2],[7,6],[2,3], s=13/5/13/5, dec=1/0/1/0, all
  ok). PASS.
- K-RV-6 (provenance): `CONSOLIDATE-1 MASKS k1=48 k2=12` in all
  four arms (revision is stable when the world is stable: no
  spurious mask change, F-SPURIOUS silent) AND ADAPT-STAT-REVISE
  spec=344 (specialization fired in the revise trace) AND the
  frozen 13-pattern grep audit on learner.zag returns 0 hits on
  every pattern. PASS.
- K-RV-7 (determinism): rv_run1/2/3.txt sha256 identical
  (82fab4f577319d2d58858a7556b23448bb47c6296b207e366216b9df2a27a6a4).
  PASS.

No falsifier fired: F-NO-LEARN, F-NO-BASE, F-NO-BREAK,
F-NO-REVISE, F-NO-RECOVER, F-SPURIOUS, F-OP-EXPAND, F-AUDIT,
F-NONDET, F-PYTHON all silent.

## Why this is mask revision

- The masks are learner state, not researcher parameters: they are
  computed by the generic variance criterion over experienced
  episodes, and the revision call recomputes them over new
  experience through the consolidation pointer. The driver
  schedules WHEN; the learner computes WHAT. The trigger is
  disclosed as experimental control; autonomous change detection
  is explicitly not claimed.
- The world change is adversarial to the old structure in a
  precise sense: the old masks deliver (0,0) on every new
  episode, so the stale pipeline collapses to the always-skip
  baseline (2/4) and re-construction provably halts (n=0). The
  masks are the broken component, and revising them is the
  sufficient repair.
- The invented intermediate M = [ADD R0,R1] survives the world
  change untouched: revision restores 4/4 with M1 reused, no
  re-construction. SPECIALIZE re-canonicalizes the new signal
  pair into (R0,R1), so the L3 intermediate is reusable across the
  slot move. Revision at the L2 level composes with a standing L3
  invention.
- Stability control: re-consolidation after phase-1 leaves the
  masks 48/12, so the mechanism does not spuriously rewrite
  working structure when the world is stable.

## Files

All under `docs/lab/research-lead/overnight-20260928/spec_mask_revision/`:

- PREREG.md (frozen, committed alone at cda792126; no amendments)
- NAMECHECK.md (toolchain guard Step 0 record, development notes)
- REPORT.md (this file)
- learner.zag (generic learner: X recall + SPECIALIZE +
  x_revise_masks, Y decide, L3 constructor; 0 modes/handlers/
  semantic cases)
- world.zag (hidden rules TRUE1/TRUE2 + episode tables;
  experiment side only)
- driver.zag (four arms + kill-bar evaluation)
- rv_full.zag (assembled 1010-line build input)
- rv_bin (compiled binary)
- rv_compile.txt (build log; exit 0; benign zagd notice plus
  three A0101 off-by-one heuristic warnings, all provably
  in-bounds: max store index 8+31*7+6=231, max mask offset 405,
  all inside their buffers)
- rv_run1.txt, rv_run2.txt, rv_run3.txt (3/3 byte-identical
  outputs, 190 lines, 0 NUL bytes)

## Non-claims and bounds

- One world family (kind-tagged aggregation with a slot move). No
  generality claim beyond the four demonstrated arms.
- Does not claim Micah's full 12-criterion L3 bar; targets the
  seven frozen revision bars.
- The hidden world rules were builder-designed, not
  adversary-designed. Sealed-adversary generality is open future
  work.
- The revision trigger is driver-scheduled (disclosed). Autonomous
  change detection is explicitly not tested here.
- The op basis, 2-register first-2 consumer, greedy policy,
  variance mask criterion, consolidation pointer, SPECIALIZE
  rule, and consolidation timing are disclosed researcher-supplied
  generic machinery. The claim is: x_revise_masks recomputes
  per-kind informative masks from post-change experience through
  the generic window mechanism, with no world knowledge in the
  learner.
- Pure Zag, safebin toolchain, zero forbidden executables. Paper
  untouched. Nothing pushed. Commits local on tnn-native-lab.
