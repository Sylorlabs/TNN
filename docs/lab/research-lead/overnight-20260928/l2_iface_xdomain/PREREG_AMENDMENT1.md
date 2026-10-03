# PREREG AMENDMENT 1 (pre-verdict, arithmetic only)

Date: 2026-10-02. Filed BEFORE any post-fix verification run.
Parent: PREREG.md (committed alone at 968e3c3ab).

## What changes

- FULL-Q2 frozen S: 484 -> 482.
- Trial T4 frozen component: 114 -> 112.
- No other frozen value changes. No code behavior changes
  implied by this amendment (the two code fixes below are
  separate and were already identified as bugs against the
  frozen design).

## Why (transparent derivation)

PREREG.md section 4 derived T4 as "77 + VALs 18+19 = 114",
where 77 was written as "13+14+15+16+17 walk". That 77
double-counts the entry scan: the 13 is scan1(50,17)
(entry probe, fid12 hit at i=12), and the foldwalk proper
is 14+15+16+17 = 62 (scan_nv(74)=14, scan_nv(75)=15,
scan1(76,15)=16, scan1(77,16)=17). The addends check is
scan_val(75,2)=18 + scan_val(77,2)=19 = 37.

Correct T4: 13 (entry) + 62 (walk) + 37 (addends) = 112.

(T3 is unaffected: 13 + 62 + 20 = 95, which the prereg
already states as 95; only its "77 walk" label was sloppy.)

Correct FULL-Q2: pipeline 1 + naive find_gen 1 + naive
entry 20 + adapt find_gen 1 + candidates 20 + trials
(50+50+95+112 = 307) + ia_exec 132 = 482.

Note: tick_exec writes the E counter (st[1300]), not the S
counter (st[1296]), so ia_exec contributes 13 (entry loop)
+ 62 (walk) + 37 (addends) + 20 (repv) = 132 to S, with no
extra 1. Q2B/Q2C = 2 + 132 = 134 confirms the 132.

## What does NOT change

- The algorithm, the tick model, and all other frozen
  S/E values (QA 24/1, Q2B 134/1, Q2C 134/1, Q2D 84/1,
  ABLATE QA 3/0, ABLATE Q2 3/0) are untouched.
- F-COUNT still fires on any deviation from the (amended)
  frozen values. This amendment narrows no bar; it corrects
  the prereg's arithmetic to match the frozen design.

## Code fixes applied alongside (not part of this amendment)

1. ia_query: added saw_adapt flag; when the pipeline
   dispatches to an adapter MAP (pm != 1), naive + adapt
   are skipped. Fixes Q2D fall-through re-adapt (was 396).
2. ia_driver run_arm: ABLATE-X kill (st[528+1]=0) moved
   before QA, matching the frozen "kill before QA" spec.
3. ia_driver ck_count FULL-Q2 expectation updated 484->482
   per this amendment.
