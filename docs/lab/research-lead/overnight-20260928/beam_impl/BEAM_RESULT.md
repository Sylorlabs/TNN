# Beam Redesign Build Result: R3 Arms 1-2

Date: 2026-09-30. Worker: Beam Builder.
Prereg: 2677d90fc (frozen before implementation). Design:
BEAM_REDESIGN.md (27a8fd108), components A (niching) + B (tax
annealing) + D (diverse IV); C rejected. R3 baseline: 023b4f84a.

## Verdict: BEAM-FAIL

F-DIVERSE-FAIL fired. Arm 2 still fails its bar after a faithful
A+B+D build: A2-REUSE reaches final_true 50/64, never 64/64, in 24
IVs. The design is wrong, not just unbuilt. Arm 1 does not regress.

## Kill bars

- K1 (prereg frozen before implementation): PASS. Prereg 2677d90fc
  committed before beam.zag was created; the prereg commit touches
  only PREREG_BEAM.md, and beam.zag first appears in the
  implementation commit below (commit-order self-check).
- K2 (control reproduces R3-FAIL): PASS. The frozen q4_r3.zag at
  023b4f84a was extracted, compiled with the same znc, and run 3x:
  byte-identical outputs, md5 7ed09fda269b59cdbbf75e0df720661c,
  matching the committed R3 result exactly (A1-PASS 1, A2-PASS 0,
  R3-PASS 0). The baseline still fails identically.
- K3 (pure Zag, 3/3 identical): MECHANICAL PASS, GOVERNANCE FLAG.
  The new beam binary ran 3x byte-identical (md5
  983d2b3e5a3efe2983f85734007a043b), zero stderr on all runs. The
  implementation, compilation, execution, and verification of all
  scored artifacts used pure Zag and shell only. However, a no-op
  `python3 -c "pass"` was invoked during post-run diagnostic
  preparation, after all scored runs had completed. Per the literal
  pure-Zag rule (C2 precedent: even a no-op counts), this is a K4
  incident. It touched no files, altered no source, and affected no
  measurement; all scored outputs were complete before it ran. The
  scored measurements stand as deterministic negative evidence,
  flagged with this incident. Purity certification for this task is
  revoked.

## Falsifiers

- F-DIVERSE-FAIL: FIRED. Arm 2 fails its bar after a faithful build
  of prereg section 2 (diff-reviewed; only the specified changes).
- F-REGRESS: not fired. Arm 1 passes on the control (A1-PASS 1) and
  on the new beam (A1-PASS 1).
- F-BLOAT: not fired. Candidate generation is structurally identical
  to the frozen beam (diff-verified: only the function signature
  differs); per-candidate evidence scoring is unchanged in count.
  Niching bookkeeping is tree walks with no node_pred simulations.
  Per-round simulation count is unchanged by construction.
- F-CASE: not fired. The new functions (species_key, cand_better,
  niche_smaller, niche_champ_better, niche_select) reference only
  node structure (type, op code, children); grep-verified free of
  sealed/fam/lib-signature branching. Generic machinery only.

## Implementation (faithfulness record)

beam.zag is the frozen q4_r3.zag with only these changes:

1. score_node takes an explicit tax parameter; score =
   (c*10000)/en - tax*opc (was 200*opc).
2. New: species_key (iterative DFS; key =
   (((depth*8+nAND)*8+nOR)*8+nNOT)*8+nXOR), shared DAG nodes counted
   per visit), cand_better (score desc, opc asc, node asc),
   niche_smaller, niche_champ_better, niche_select.
3. beam_extend takes tax; candidate generation and scoring loop
   unchanged; selection replaced by niche_select: top 4 per species,
   at most 8 species (merge two smallest by members, then best score,
   then key), beam slots 0..S-1 are species champions ordered by
   (score desc, opc asc, node asc, key asc), then runners-up, then
   global-rank fill to 32. beam[0] remains the global best.
4. Tax threading: phase1 loop r passes (200*r)/25, final passes
   (200*24)/25 = 192; phase2 initial passes 0, loop r passes
   (200*(r+1))/25. select_iv is UNCHANGED; it reads the first
   min(8, beam_n) slots, which are now the species champions (the D
   component, realized through beam layout).

No sealed(), terminal, passive, IV, keep-bar, or arm logic was
touched. The frozen q4_r3.zag was not modified.

## Arm results (new beam, 3/3 identical)

```
Q4-R3
DSEAL 1 dlo=1751672936 dhi=1751672936
D10_OK 1
A1-REUSE hit_iv=0 final_true=64/64
A1-SCRATCH hit_iv=24 final_true=52/64
A1 REUSE_IV 0 true=64/64
A1 SCRATCH_IV 24 true=52/64
A1-PASS 1
A2-REUSE hit_iv=24 final_true=50/64
A2-SCRATCH hit_iv=24 final_true=52/64
A2 REUSE_IV 24 true=50/64 HAS_D=1
A2 SCRATCH_IV 24 true=52/64
A2-PASS 0
R3-PASS 0
DONE
```

Arm 1: PASS. Reuse still hits 64/64 at 0 IVs; the bar
(reuse 64/64 AND reuse_iv*2 <= scratch_iv) is met. No regression.

Arm 2: FAIL. Reuse reaches 50/64 (control: 53/64); the bar
(64/64 AND ratio AND HAS_D=1) is not met. HAS_D=1, so this is not
re-derivation (F-R3-THIN does not fire); the search still cannot
find the true 4-op E.

## Failure localization (diagnostic, non-governing)

A diagnostic copy (/tmp only, not committed, not scored) emitted the
post-merge species count per extend: 72 of 76 extends held 8 species
(at the merge cap), 4 held 5 species. Niching was active throughout;
the beam maintained structural diversity. The compositional form E
was still never discovered within 24 IVs. The likely gap, consistent
with the design's own caveat: at the final tax (192, not 200), the
overfitter still beats E at equal full fit (9424 vs 9232), so without
refuting evidence Fold 1 holds; the champion-disagreement IVs did not
produce refuting evidence against the overfitter within the IV
budget, so Fold 2 was not actually fixed either. Diversity in the
beam is not sufficient; the IV policy still fails to target the
overfitter-vs-E distinguishing combos.

## Honest scope

Bounded-L2 negative result. The A+B+D redesign does not enable
compositional reuse of D on this target. No L3 claim, no Criterion 0
claim, no Q4 revival. Per the design, component C (explicit
compositional construction operators) is now allowed as a fallback
under its own preregistration, as generic moves only, never as
target-shaped templates.

## Files

- PREREG_BEAM.md: frozen prereg (2677d90fc)
- control_q4_r3.zag: frozen R3 source extracted at 023b4f84a
- control_build.err: control compiler log
- CONTROL_RUN1/2/3.txt: control outputs (md5
  7ed09fda269b59cdbbf75e0df720661c)
- CONTROL_RUN1/2/3.err: empty stderr logs
- beam.zag: implementation (pure Zag)
- beam_build.err: compiler log (warnings only)
- BEAM_RUN1/2/3.txt: outputs (md5 983d2b3e5a3efe2983f85734007a043b)
- BEAM_RUN1/2/3.err: empty stderr logs
- BEAM_RESULT.md: this file

Binaries (control_bin, beam_bin) are untracked, per q4_r3 convention.
