# RUNLOG — NEC v3 Q3 Follow-up: B13 Scale Degradation (adopted m11)

## Protocol-ordering disclosure (READ FIRST)

The frozen task required a dated pre-run addendum BEFORE diagnosis and FIX runs.
Actual ordering on 2026-09-25 UTC:

1. **Exploratory work happened first**: pipeline validation, baseline B13 measurement
   (s1/s10/s100), D1/D2/D3 exploratory measurements, FIX-A/B/C/D input generation
   and initial runs, all before the addendum was committed.
2. `ADDENDUM_Q3_PRERUN.md` committed at `55cc07ef` (parent `1096c0e7b80a`).
3. All FIX-* battery A/B/C runs, gaming probes, m12 runs, and analyses in this
   log happened AFTER that commit.

The committed addendum states "diagnosis measured before FIX runs" but does NOT
sufficiently disclose that exploratory diagnosis preceded the addendum itself.
This RUNLOG corrects the record. The D1/D2/D3 numbers below are from the
exploratory phase (pre-addendum); they are reported as measured, with this
ordering caveat. No FIX input was generated after seeing its own output.

## Baseline (adopted m11, frozen driver, exact)

| Scale | B13 violations | Breakdown |
|-------|---------------|-----------|
| s1 | 6 | ceiling/O d1/d2/d4/d8/d16/d32 |
| s10 | 23 | ceiling/D=5, O=6, cost=5, redteam=2, revoke=5 |
| s100 | **24** | ceiling/D=6, O=6, cost=5, redteam=2, revoke=5 |

Correction: s100 is 24, not 23. The extra violation is ceiling/D d2
(G=-0.1106), missed in the first count because d2 has n<8 in some legs.

Rebuilt m11 reproduced all 37 historical legs byte-identically at s10/s100.

## Diagnosis

### D1 — pooled-ledger/prior washout: CONFIRMED (exploratory, pre-addendum)

Family-blind class bins converge toward the adversarially pooled empirical rate.
Key per-class empirical rates (s1):
- cls 5: 0.5152 (17/33), smoothed 0.5400
- cls 10: 0.6735 (33/49), smoothed 0.6843
- cls 15: 0.7756 (235/303), smoothed 0.7767
- cls 16: 0.6522 (75/115), smoothed 0.6573
- cls 17: 0.6591 (58/88), smoothed 0.6656
- cls 34: 0.9970 (985/988), smoothed 0.9969

Class 15 trajectory: ~0.9583 initially → 0.9993 at t≈150 → 0.8306 at t≈400 →
0.7781 at t≈3000 → 0.7756 asymptote. The honest-first cold ledger starts high;
the warm ledger washes out to the pooled rate.

O-family items sit in low-rate classes (explains baseline O violations).
The SCALE DEGRADATION (6→23→24) is driven by ceiling/D and cost/revoke/redteam
families whose warm-ledger rates fall below the G<-0.100 threshold as t grows.

### D2 — fixture composition shift: NOT CONFIRMED (exploratory, pre-addendum)

s10/s100 are exact sequential replications of the s1 distribution
(verified: first s100 pass through s1 pipeline reproduces B13=6 with the exact
same six O G values). Family/depth composition identical per pass.
Composition is NOT the driver.

### D3 — personal-cap ablation: CONFIRMED (exploratory, pre-addendum)

m9 (no personal cap) vs m11 (cap):
- s10: m11=23, m9=21 (cap contributes +2)
- s100: m11=24, m9=22 (cap contributes +2)
Two cap-attributable violations: redteam d2, d4. Without the cap K12 stays
wrongly confident at ≈0.996. The cap is load-bearing for red-team containment;
it is NOT removed.

## FIX-* battery (all post-addendum, 3× byte-identical A/B/C)

### FIX-A (per-class correct anchors to empirical 0.95)

| Scale | Baseline | FIX-A | B1 | B2 | B3 |
|-------|----------|-------|----|----|----|
| s1 | 6 | **0** | 0 | 0/0 | 2 |
| s10 | 23 | **0** | 0 | 0/0 | 2 |
| s100 | 24 | **0** | 0 | 0/0 | 2 |

MEETS TARGET: 0 ≤ 0 ≤ 0, B2=0, B3=2≤3, no broken passing bar.

SHA-256:
- s1: `ee4fbafd74c823c4f2e8a1270f322070928eaae059bb7dab866d484e0605364d` (A)
- s10: `873e67f40aaa27ba0b33743672cfa0aad9a445c209e4e14f23bfbbf5411dcadc`
- s100: `d86bcb5268df1e24a37c2b5709abb598ba07a8946cb1a3d2f73ea3601ce2acd7`

Bug found and fixed: initial interleaver grouped anchors by class (class-17
anchors arrived too late), giving a spurious s10 B13=10. Corrected to per-class
uniform spreading across the entire input. All reported numbers use the
corrected interleaver.

Gaming probes (all PASS):
- GP-1 held-out honesty: mean|conf−1.0| = 0.0185 ≤ 0.10 (306 held-out IDs,
  1528 released cells, appended after warm ledger)
- GP-2 wrong-item overconfidence: mean conf(wrong) = 0.0917 ≤ 0.50 (n=4620)
- GP-3 cap integrity: K12 (redteam wrong) conf at d2+ = 0.000 exactly
  (d1 = 0.9967, expected — cap binds only after first observation)

### FIX-B (1:1 honest replication): MISSES

| s1 | s10 | s100 |
|----|-----|------|
| 5 | 11 | 12 |

1:1 is insufficient to counteract the pooled rate. B3=2 (held).

### FIX-C (matched correct traps): MISSES, worst at scale

| s1 | s10 | s100 |
|----|-----|------|
| 5 | 18 | 18 |

Traps in matched (f1,f5) do not raise the pooled rate enough. B3=2 (held).

### FIX-D (thin wrongs to 5%): B13=0 BUT B3 FAILS

| s1 | s10 | s100 | B3 (s10/s100) |
|----|-----|------|---------------|
| 0 | 0 | 0 | 6 / 5 |

B13 target met (0 ≤ 0 ≤ 0) but B3 = 6 (s10) / 5 (s100), exceeding the ≤3 bar.
Thinning wrongs distorts the monotonicity the B3 bar measures. DISQUALIFIED.
(Risk was disclosed in addendum; confirmed.)

### m12 (PRIOR-WASHOUT mechanism: shrinkage prior (emp+p0)/2): MISSES

| s1 | s10 | s100 |
|----|-----|------|
| 3 | 11 | TBD |

Predicted miss confirmed: convex averaging cannot raise class 15 above ≈0.863.
A principled scale-invariant prior alone does not meet the target.

## Infrastructure notes

- `nec_scale_big.zag`: capacity-only changes vs frozen m11 (personal-table
  10k/100k/510k, input buffers 8MB/16MB/33.5MB). Verified byte-identical to
  frozen m11 on standard s1/s10/s100 inputs.
- s100 max_items raised 450k→510k (510000×64=32.6MB < 2^25) to admit FIX-B s100's
  500500 distinct IDs. Re-verified byte-identical after the change.
- Fixture family aliases compacted `anchor/calib/trapu` → `a/c/t` to keep s100
  inputs under the 2^25 slice limit. Documented; equivalence checked.
- FIX-B s100 IDs compacted `#s100rNNN` → `#rNNN` (identity relationships preserved).
- `/tmp` ENOSPC incident: FIX-A s100 run C truncated at 12MB when /tmp hit 100%.
  Scratch moved to `~/workspace/ncal-q3/scratch/`. C rerun matched A/B byte-for-byte.
  The earlier "C mismatch" was truncation, not nondeterminism.
- Python (`fixbuild.py`, `convert.py`, `q3bars.py`) is analysis/scratch tooling.
  The "Pure Zag final mechanisms/fixtures" requirement is NOT yet satisfied for
  FIX-A — the fixture generator must be ported to pure Zag before adoption.

## Verdict (pending VERDICT_Q3.md)

- D1 CONFIRMED, D2 NOT CONFIRMED, D3 CONFIRMED.
- FIX-A is the ONLY candidate meeting the B13 target with all bars held.
- FIX-B/C miss on B13. FIX-D meets B13 but breaks B3. m12 (shrinkage prior) misses.
- Per the decision rule: **FIXTURE** (FIX-A meets target).
- NOT adoption-eligible yet: pure-Zag fixture port, full white-box audit (§2 T1-T4),
  and committed evidence remain.
