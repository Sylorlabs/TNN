# REPORT.md -- H2 Completeness Repair (banded round-robin enumeration)

## Verdict: H2-COMPLETENESS-COMPLETE

Per the frozen prereg (PREREG.md, committed 1157eee96 before any
implementation edit), all bars T1..T7 pass. No kill bar moved. Cap stays
48. Depth stays 3. Zero new modes/bridges/handlers/semantic cases. The
D*B memory bound is preserved (bound proof updated for round-robin in
PREREG.md section 2b and in the `ir_frag_candidates` header).

## What was broken

REDTEAM2-H2H3 attack H2-B1 TRUNC-LOSS: KILL. `ir_frag_candidates`
enumerated fragments in flat (flen desc, map_id asc, start asc) order
and truncated at 48 per DFS level. In world B1 (8 decoy [9,9,9,9] MAPs
+ 3 true [1,1] MAPs, 6-link r1 goal 31..37), at DFS level 1 the decoys
enumerated 8 (flen 4) + 16 (flen 3) + 24 (flen 2) = 48 fragments before
the true (T,0,2) fragments at positions 49-50, so the genuine solution
was truncated away: RECOMB-FAIL when decoys were taught first, SOLVE
when trues were taught first. Teach order alone flipped the verdict on
identical knowledge.

## The repair: banded round-robin enumeration

Changed file: `h2c_patch.zag` only (the unfrozen fragment-recombination
patch). `h2c_base.zag` and all three drivers are byte-identical copies
of frozen inputs, verified by SHA-256 (see NAMECHECK.md).

The enumeration is now BANDED ROUND-ROBIN:

- Outer bands by decreasing fragment length (7..1), UNCHANGED: the
  fewer-fragments-preferred bias is preserved exactly.
- WITHIN each band, fragments are dealt round-robin across MAPs: round
  r hands every MAP (id ascending) its r-th satisfiable length-fl
  fragment (start ascending), until the 48 cap or until a full round
  yields no fragment.

Fair-share guarantee: within one band, with M MAPs holding satisfiable
fragments and R cap slots remaining, every MAP retains at least
floor(R/M) fragments, and any MAP with at most that many retains all of
them, regardless of teach order. For B1 level 1 (R=24 entering band
fl=2, M=11): every MAP keeps at least 2; the true MAPs have 1 flen-2
fragment each, so all true fragments survive in both teach orders.

The D*B bound is untouched: n still starts at 0, increments only at the
single write site, every loop (band, round, MAP, start) guards n<B, the
per-level regions [L*B,(L+1)*B) are still disjoint, and the buffer is
still D*B entries of 3 i32s. Only WHICH satisfiable fragments occupy
the B slots changed, never how many.

The file header sentence the red-team killed ("discovery is by
constraint satisfaction only") now reads "discovery is by constraint
satisfaction over a teach-order-fair candidate set", citing the B1
repair.

Design alternative rejected (frozen in PREREG.md section 5): global
round-robin (interleave across MAPs ignoring flen) loses the global
flen-desc priority and would have changed A1's arm from a 1-fragment to
a 2-fragment solution and A3's Z2 reuse from a whole-MAP fragment to two
fragments. Banded round-robin keeps the stated length bias and only
reorders within bands.

## Test results (all 3/3 byte-identical, exit 0)

Binaries (pinned `~/safebin/znc`, warnings only):
`h2c_bin` (frag_on=1), `h2c_nc_bin` (frag_on=0), `h2c_b1_bin` (B1
driver), `h2c_stress_bin` (stress driver).

### T1/T2: B1 re-test, both teach orders (the KILL)

- B1a (decoys taught first): SOLVES. Level-1 probe n=48 with the true
  fragments inside the cap (previously at positions 49-50, dropped).
  `RECOMB-FRAGS n=3 (m=383,s=0,l=2) (m=396,s=0,l=2) (m=409,s=0,l=2)`
  = exactly (T1,0,2)+(T2,0,2)+(T3,0,2); `B1 Z ans=37`.
- B1c (trues taught first): still SOLVES. `RECOMB-FRAGS n=3
  (m=23,s=0,l=2) (m=36,s=0,l=2) (m=49,s=0,l=2)` = (T1,0,2)+(T2,0,2)+
  (T3,0,2); `B1 Z ans=37`.
- Teach order no longer flips the verdict. The driver's legacy
  "UNEXPECTED-SOLVE" label on B1a is the old driver's expectation text;
  the outcome (SOLVE) is the repaired behavior this prereg barred.

B1 transcript SHA-256 (3/3 identical):
9f4d5311fceac0792dd9a3d59b220708980d9b9c6be74f59e1f1aef1eff81802.
B2 arms (not in the battery, informational): both still promote their
teach-order forms, n=2, unchanged from redteam2. B4: still clean
RECOMB-FAIL, ans=-2, exit 0 (depth bound intact).

### T3/T4/T5: H2 fix battery, no regression

`h2c_run1/2/3.txt` are BYTE-IDENTICAL to the fixer's frozen
`h2f_run1/2/3.txt` (SHA-256
63bff44157c500a02b5feec4f34340880adcaf2bc9cd6bc16debc492894c4a21,
the fixer's own transcript hash). Verdicts unchanged:

- A1 SPURIOUS: BOUND. `RECOMB-FRAGS n=1 (m=91,s=0,l=3)`, `Z ans=37`
  (verifier limitation documented OPEN by the fixer; untouched).
- A2 DUP-ABL: BOUND. `RECOMB-FRAGS n=2 (m=91,s=0,l=3)
  (m=68,s=0,l=3)`, `Z ans=37`.
- A3 SINGLE: BOUND. Z via `(m=45,s=0,l=3)+(m=68,s=0,l=3)`, Z2 via
  whole-MAP fragment `(m=165,s=0,l=6)`, `Z2 ans=47`.
- A4c CONTROL: BOUND. `RECOMB-FAIL`, `Z ans=-2`.
- A5 THREEFRAG: SURVIVE. `RECOMB-FRAGS n=3 (m=45,s=0,l=3)
  (m=68,s=0,l=3) (m=45,s=1,l=3)`, `Z ans=40`.

The nc control binary's transcripts are likewise BYTE-IDENTICAL to the
fixer's frozen `h2f_nc_run1/2/3.txt` (SHA-256
c0c7b619d8a35d4a4c154091d8b3ea027df1312233b610c4f2db12ca797d70f2).

### T6: 100-fragment stress test

`h2c_stress_run1/2/3.txt` BYTE-IDENTICAL to the fixer's frozen
`h2f_stress_run1/2/3.txt` (SHA-256
76a95db1f296864ea75802bfcd176f17b72f9f91d89dc23c05a0238b19cbb6ad).
`CANDCOUNT s=31 n0=48 cap=48`, `RECOMB-FRAGS n=3 (m=45,s=0,l=4)
(m=68,s=0,l=4) (m=91,s=0,l=4)`, `Z ans=43`, exit 0. Terminates cleanly.

### T7: determinism

Every binary ran 3x; all run sets 3/3 byte-identical by cmp/sha256sum.

## Architecture accounting

- Cognition lines changed: `ir_frag_candidates` rewritten (banded
  round-robin) plus one header sentence; the rest of the patch is
  byte-identical to the fixer's `h2f_patch.zag`.
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
  No new opcodes; protected-core ISA untouched.
- Cap (48), depth (3), D*B buffer layout, satisfiability test,
  used-triple exclusion, DFS, verifier, query protocol: all unchanged.
- The enumeration change is a fairness repair to the search, not a new
  subsystem: no router, mode flag, or task-specific gate was added.

## Residual limitation (honest, frozen in PREREG.md)

Bands still drain in flen-desc order, so a band that alone fills the 48
cap still excludes shorter bands (the intended fewer-fragments bias).
What this repair removes is the within-band teach-order unfairness that
B1 killed: no MAP's fragments can be starved by enumeration order alone
within a band. Full order-independence would need goal-derived
relevance ranking: a redesign, noted as follow-up, not claimed here.

## Reproduction

All files under
`docs/lab/research-lead/overnight-20260928/h2_completeness/`:

- `PREREG.md`, `NAMECHECK.md`, `REPORT.md` (this file).
- `h2c_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6):
  frozen base, unmodified.
- `h2c_patch.zag`: repaired patch (banded round-robin).
- `h2c_patch_nc.zag`: one-line frag_on=0 variant.
- `h2c_driver.zag`, `h2c_stress_driver.zag`, `h2c_b1_driver.zag`:
  byte-identical driver copies (hashes in NAMECHECK.md).
- `h2c_full.zag`, `h2c_full_nc.zag`, `h2c_full_b1.zag`,
  `h2c_stress_full.zag`: assemblies (concatenation).
- `h2c_bin`, `h2c_nc_bin`, `h2c_b1_bin`, `h2c_stress_bin`: binaries
  (pinned znc; warnings only; build log `h2c_build.log`).
- `h2c_run1/2/3.txt`, `h2c_nc_run1/2/3.txt`, `h2c_b1_run1/2/3.txt`,
  `h2c_stress_run1/2/3.txt`: 3/3 byte-identical run outputs.

Builds: `znc h2c_full.zag -o h2c_bin` etc. Runs: `./h2c_bin >
h2c_runN.txt` etc. Pure Zag; safebin toolchain guard Step 0 in
NAMECHECK.md (no python3/python in worker PATH). Paper untouched.
Nothing pushed. Commits local on branch tnn-native-lab with explicit
pathspecs.

## Open items for the parent (not decided here)

1. Goal-derived relevance ranking (the stronger completeness
   direction the red-team listed) remains a redesign follow-up; this
   repair deliberately stays at fair-share enumeration.
2. H2-B2 (order-form tie-break) and H2-B4 (depth-4) are BOUND and were
   not addressed; both re-verified unchanged on the repaired binary.
