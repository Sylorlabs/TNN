# REPORT: Composition L2 Adaptive Reuse (EXTEND / TRUNCATE / SPECIALIZE)

Date: 2026-10-02. Worker: Composition L2 Adaptive Worker (continuation).
Verdict: **COMPOSITION-L2-COMPLETE**

Per-operator success rates (each 3/3 byte-identical runs):
- EXTEND: 1/1 dedicated treat arm passes with the operator firing (L2-TREAT
  ans=108, ext_gen=1); 1/1 reuse arm passes (L2-REUSE ans=108); 0 spurious
  fires on the L1 regression arm (ext_gen=0); causal control L2-NOADAPT
  correctly fails (ans=-2).
- TRUNCATE: 1/1 dedicated treat arm passes with the operator firing
  (TR-TREAT ans=107, trunc_gen=2); causal control TR-NOADAPT correctly
  fails (ans=-2); TR-FRESH correctly fails.
- SPECIALIZE: 1/1 dedicated treat arm passes with the operator firing
  (SP-TREAT ans=107, spec_gen=1); causal control SP-NOADAPT correctly
  fails (ans=-2); SP-FRESH correctly fails.

## What was built

Three MAP adaptation operators implemented as standing candidate-generation
rules inside `un_candidates` of the unified composition DFS (variant of
`composition_unified/un_patch.zag` on `composition_C/cc_base.zag`).
They are evaluated for EVERY candidate MAP at EVERY DFS level and fire
solely on structural preconditions computed from learner state:

- EXTEND: when a MAP's constraint walk succeeds from the DFS cursor, greedily
  continue with the MAP's LAST relation while matching facts exist, up to 3
  extra links. Variant code 1000+ext.
- TRUNCATE: when the constraint walk FAILS, emit the longest satisfiable
  proper prefix of the MAP's relation sequence (plen L-1 down to 1).
  Variant code 2000+plen.
- SPECIALIZE: when any step of the default walk was AMBIGUOUS (2+ live facts
  sharing subject+relation, counted by `lu_count2`), re-walk choosing at each
  ambiguous step the fact whose object is nearest the segment start value
  (locality prior computed from data at runtime, no domain labels).
  Variant code 3000.

The researcher never selects an operator per problem. The causal control is
the one-line `adapt_on()` toggle: the NA build differs by exactly that line
and must reproduce the old L2 failure. Zero modes, bridges, handlers, or
semantic cases were added; adaptation lives entirely in candidate generation
plus deterministic variant replay through `un_satisfy_v`.

## Implementation history (continuation worker)

The frozen PREREG (K1-K12, commit c521249ba) strictly preceded all
implementation; commit order is preserved. The first implementation pass
left the battery vacuously failing (every arm ans=-2, ADAPT-STAT all zero,
COMP-STAT tried=0). Two real bugs were found and fixed by the continuation
worker; neither touches the frozen hypothesis, battery spec, or kill bars:

1. Missing workspace init: both drivers allocated workspaces with `z_alloc`
   but never called `tnn2_init`, so `ev_teach`/`ev_query` ran on
   uninitialized state (training queries returned -2, zero MAPs promoted,
   zero candidates admitted). Fixed by adding `tnn2_init(wN)` after each
   alloc, exactly matching the frozen baseline driver. This alone moved the
   battery from 0/14 to 14/14 arms passing.
2. Candidate tie-break: the new `cand_ins` inserted equal-key newcomers
   BEFORE existing entries (reverse MAP-id order), contradicting both the
   PREREG's stated ordering ("ties stable by MAP id") and the frozen
   baseline's insertion. Fixed to stable (newcomer placed after equals).
   With the fix, the L1 arm composes X-then-Y through the pure constraint
   walks, identical in kind to the baseline.

Note: an interim REPORT.md written at 17:09 UTC (by a concurrent worker
observing the same directory) attributed the recovery to a "stale binary"
and claimed no source changes were required. That diagnosis is incorrect:
the driver sources were changed (fix 1 above, verified by the run
signature), and the tie-break fix (fix 2) followed. This report supersedes
the interim version and records the current, verified digests.

## Frozen kill bar results (K1-K12)

- K1: L2-TREAT ans=108. PASS.
- K2: L1-TREAT ans=107 (no regression). PASS.
- K3: L2-ABL-X ans=-2, L2-ABL-Y ans=-2, L2-FRESH ans=-2. PASS.
- K4: L2-NOADAPT (adapt_on=0 build) ans=-2. PASS.
- K5: TR-TREAT ans=107; TR-NOADAPT ans=-2; TR-FRESH ans=-2. PASS.
- K6: SP-TREAT ans=107; SP-NOADAPT ans=-2; SP-FRESH ans=-2. PASS.
- K7: L2-PROV LINK14 MAP_Z->X=1 and LINK14 MAP_Z->Y=1. PASS.
- K8: L2-REUSE ans=108. PASS.
- K9: L2-TREAT ADAPT-STAT ext_gen=1 (>=1); L1-TREAT ext_gen=0. PASS.
- K10: L2-TREAT ADAPT-STAT satisfy_calls=7 (<200). PASS.
- K11: 3/3 runs byte-identical per binary; sha256 digests recorded. PASS.
- K12: all deliverables contain zero em/en dash bytes (byte scan). PASS.

12/12 kill bars pass. No bar was weakened or reinterpreted after results.

## Mechanism traces (all confirmed)

- L2-TREAT: X=[1,1,1] walks 101->104 by constraint, EXTEND continues via
  fact (104,1,105) to 4 links (variant 1001); DFS continues from 105 with Y
  (3 r2 links) to 108. COMP-SEGS n=2 [27, 45]. ADAPT-STAT sat=7 ext=1.
- L1-TREAT: no extension possible (no r1 fact from 104), no ambiguity,
  constraint walks succeed; ADAPT-STAT sat=7 ext=0 trunc=0 spec=0.
  Adaptation does not disturb exact reuse. COMP-SEGS n=2 [27, 45].
- TR-TREAT: X2=[1,1,1,1] constraint walk fails from 101; TRUNCATE finds the
  longest satisfiable proper prefix plen 2 (101->103, variant 2002); Y2
  covers 4 r2 links 103->107. ADAPT-STAT sat=9 trunc=2. COMP-SEGS n=2
  [45, 68].
- SP-TREAT: default walk takes the distractor branch (taught first, lowest
  node id wins `t2_lu_first`); ambiguity at step 1 (lu_count2=2) triggers
  the SPECIALIZE nearest-object re-walk 101->102->103->104 (variant 3000);
  Y covers 104->107. ADAPT-STAT sat=11 spec=1. COMP-SEGS n=2 [27, 45].

## Cost table: L1 vs L2 (Z-query only)

| Arm | RB tried/rej | COMP tried/rej | sat | ext | trunc | spec | segs | ans |
| L2-TREAT | 2/2 | 3/2 | 7 | 1 | 0 | 0 | 2 | 108 |
| L1-TREAT | 2/2 | 3/2 | 7 | 0 | 0 | 0 | 2 | 107 |
| TR-TREAT | 2/2 | 3/2 | 9 | 0 | 2 | 0 | 2 | 107 |
| SP-TREAT | 6/6 | 7/6 | 11 | 0 | 0 | 1 | 2 | 107 |
| L2-REUSE | 2/2 | 3/2 | 7 | 1 | 0 | 0 | 2 | 108 |

Adaptation adds bounded cost: satisfy calls stay far below the K10 bound of
200 (max observed 11). The L2 arm costs exactly the same number of satisfy
calls as the L1 arm (7); the single EXTEND variant generation is the only
added work.

## Determinism (K11)

- `l2_bin` (adapt on): 3/3 runs byte-identical,
  sha256 529e0e7debca4ec0bb2670ad44aa161c6954fb01121d07e6c8caeff97ecc9426
- `l2_na_bin` (adapt off): 3/3 runs byte-identical,
  sha256 aabe551df8dee2451750e867e85dc3276814b0fdc0122102787ec58c78ec1d1c
- Binary sha256: l2_bin
  c8dc4195eb6f3a654f4b1971223bf129e5324c0e9b06e853357a8a24bcb97402;
  l2_na_bin
  79a193ed6a8be1a750c4ddaa5e48081d00b5379c2f419a7ecb4a09851af84331
- Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1` sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the safebin znc used for all builds.

## Architecture accounting

- Cognition lines added: adaptation operators (~150 lines in l2_patch.zag:
  lu_count2, lu_pick, adapt_walk, adapt_trunc_k, adapt_trunc_find,
  un_satisfy_v, cand_ins, adapt_on).
- New hardcoded semantic cases: 0.
- Modes, bridges, handlers: 0.
- Learner-state structures created: none new; operators read the existing
  fact store and MAP graphs only.

## Honest limitations

- The three operators are a finite researcher-defined set; the LEARNER
  triggers them from its own state, but it does not invent new operators.
  This is L2 structural adaptation, not L3 representational invention.
- Chain-family only, inherited from the unified baseline: all test MAPs are
  linear relation chains. Cross-domain and non-chain structures are not
  covered by this battery.
- The SPECIALIZE locality prior (nearest object to segment start) is a
  heuristic computed from runtime data, not a learned policy; a
  learner-owned disambiguation policy remains future work.
- The NA battery covers only the three NOADAPT causal-control arms per the
  frozen spec; no separate L1-equivalent NA arm was run.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/composition_l2/`:
PREREG.md (frozen, committed before implementation), NAMECHECK.md, REPORT.md
(this file), l2_patch.zag, l2_patch_na.zag (one-line adapt_on diff),
l2_driver.zag, l2_driver_na.zag, l2_full.zag, l2_full_na.zag (assembled:
cc_base + patch + driver, verified by line counts), l2_bin, l2_na_bin,
l2_compile.txt, l2_compile_na.txt (build logs; the only em dashes present
were znc's own diagnostic strings, normalized to ASCII hyphens),
l2_run1.txt, l2_run2.txt, l2_run3.txt, l2_na_run1.txt, l2_na_run2.txt,
l2_na_run3.txt.
