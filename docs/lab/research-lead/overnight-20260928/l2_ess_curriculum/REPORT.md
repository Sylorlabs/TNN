# REPORT.md -- L2-ESS-CURRICULUM (two-family test of H-OP-ESS)

**Verdict: H1 SURVIVES. H0 FALSIFIED (P2+P3+P5 jointly observed).**

## Kill bars (frozen PREREG.md, amendments A1-A5 transparent pre-results)

| Bar | Result | Evidence |
|-----|--------|----------|
| KB-FAM-A | PASS | k_fama=1 (UNGATED q0-6: ops 1,2,3,4,5,6,4; vals 42,11,32,60,77,91,11) |
| KB-FAM-B | PASS | k_famb=1 (UNGATED q7 val -2; q8 op4/v71; q9-14 val -2; q15 op2/v72; q16 op2/v73) |
| KB-P1 | PASS | k_p1=1; shell: q11-14 as(UNG)-as(STD)>=48 each; q7/q8 identical commits |
| KB-P2 | PASS | shell: UNGATED q11 MR-OP-TRY 2 + MR-OP-FAIL 2 vs STANDING MR-OP-STANDING-SKIP 2 (q11-14 all skip) |
| KB-P3 | PASS | k_p3=1; shell: q15 MR-OP-PROBATION 2, op==2 val==72; cell (op2,sig18) (0,4,1)->(8,2,0)->(16,1,0) |
| KB-P5 | PASS | k_p5=1 (GLOBAL q15 val=-2; STANDING q15 val==72) |
| KB-P4 | PASS | driver.zag grep: zero operator/form/trace-tag/standing-offset/threshold/signature literals |
| KB-F-A | NOT FIRED | RIVAL vs STANDING differ on q7 (RIVAL MR-RIVAL-SKIP 2; STANDING MR-OP-TRY 2) |
| KB-F-D | NOT FIRED | Every MR-OP-STANDING-SKIP paired with UNGATED MR-OP-FAIL (q4,q5,q9-14 spot-checked; zero OK-withheld) |
| KB-DET | PASS | 3/3 byte-identical sha256 `4887580841faf5b333eb08f65dd14bfe96fe2fb2a883f622db570ebb77c42add` |

## Design (Family B: genuinely different)

New source mX (dom 3, cap 3): entry rel 51, fold rels 52/53, value rel 54; facts 44-47 (values <256 per u8 fact fields). Disjoint relations/values from Family A. Signature (generic, T7): sig=em*16+nf*2+pat; Family A -> sig 6, Family B -> sig 18 (disjoint cells). Four arms: UNGATED (0), STANDING (1), GLOBAL (2), RIVAL (3).

## Key findings

1. **P2 (divergence)**: STANDING skips op 2 on q11-14 (saving >=48 ticks/query vs UNGATED) while UNGATED wastefully retries and fails. Identical commits on q7/q8 (no distortion).
2. **P3 (reversibility)**: (op2,sig18) struck after q7 (0,4,1); skipped q9-14; probation at q15 (QTOUCH=8) recovers to (8,2,0); q16 (16,1,0). Strike latency was 1 failure (SUC*2<FAIL), not 3 as mispredicted in A2/A4; phenomenon unchanged.
3. **P5 (context beats global)**: GLOBAL arm (per-op, no signature) wrongly skips op 2 on q15 (val -2); STANDING (per-(op,sig)) recovers via probation (val 72). Context-sensitivity demonstrated.
4. **F-A**: Rival (stateless "skip if no substitute candidate") differs from STANDING on q7, so STANDING is not reducible to the stateless rule.
5. **F-D**: Zero wrong skips; bound holds.

## Amendments (all pre-results, transparent)

- A1: Family B values 300-332 -> 245-254 (u8 fact field wrap).
- A2/A3/A4: q7 redesign (direct-execution interference; Form B s==v requirement; f_teach cap).
- A5: Corrected strike-latency prediction (1 failure, not 3).

## Artifacts

- `learner.zag`, `world.zag`, `driver.zag`, `ess_full.zag`, `ess_bin`
- `ess_run1/2/3.txt` (3/3 identical)
- PREREG.md (frozen + A1-A5), NAMECHECK.md

**H1 survives as ESS instance #5 (second-order, procedure-level). H0 ("operators should NOT have ESS") is falsified.**
