# RESULT: L3C v2 Round-2 Independent Adversary Attack (pipeline step 10)

Date: 2026-09-30. Verdict: **L3C-V2-ADV2-SURVIVES-THIS-ROUND**.
Governing prereg: PREREG_L3C_V2_ADV2.md (commit c3fc2b964,
L3C-V2-ADV2-PREREG-FROZEN), committed alone before any attack file existed.
Precedence: prereg commit c3fc2b964 is an ancestor of this result commit
(verified with git merge-base --is-ancestor). No frozen bar was altered;
no slip was found.

## Method integrity

- The attack ran against a verbatim copy of the committed l3c_v2.zag
  (lines 1-771, everything before fn main); the copied prefix diffs EMPTY
  against the 20705ab5a blob (sha256
  4a039420c7830de103fd38585ddf74207c0fbb2ce200a5fc1af5adf02cfe1c50).
  The committed mechanism file was never modified.
- Pure Zag at every step: implementation, build, runs, analysis, byte
  checks. Zero Python. Shell-only check_no_dash.sh on every committed
  document. Pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Build exit 0 (only the expected A0102 ignored-observe-return notes).
  Binary runs exit 0. 3/3 runs byte-identical (sha256
  419ba587e828948de32cca76a667cade3de82d0b366405cc46bf0673e7d27bd5).

## Family RACE (sig 704): competing refines on sibling edges

All frozen predictions matched:

- Trace lines, in arrival order:
  "REFINE sig=704 edge=0 natoms=1 a0=(3,0,9)" then
  "REFINE sig=704 edge=1 natoms=1 a0=(3,0,9)". Exactly two REFINE lines.
- Edge 1's pre-refine record survived edge 0's refine: edge 1's refine
  fired on its 2nd contradiction, no 3rd record needed. The compaction in
  try_refine preserved the sibling edge's live record.
- built_delta=3, unresolved_delta=0, ambig_delta=0. Eval 6/6.
- Structure checks: CHK_RACE_defdisp PASS, CHK_RACE_labdisp PASS,
  CHK_RACE_d2atom PASS (D2 labeled atom (3,0,9)), CHK_RACE_d3atom PASS
  (D3 labeled atom (3,0,9)). No edge re-pointed twice; no double-build;
  no misrouted dispatch.

The serialization is coherent: one observe fires at most one refine, so
the race always resolves by arrival order of the second record, and the
loser's record is preserved rather than dropped.

## Family MIXED (sig 705): mixed-output check after a refine chain

All frozen predictions matched:

- Trace lines, in order:
  "REFINE sig=705 edge=7 natoms=1 a0=(3,0,9)",
  "REFINE sig=705 edge=9 natoms=1 a0=(2,0,2)",
  exactly one "REFINE_MIXED sig=705",
  "REFINE sig=705 edge=11 natoms=1 a0=(0,1,8)".
- M1 (mixed): no build, unresolved_delta=1 after the phase, records
  consumed, edge 11 NOT re-pointed.
- M2 (consistent contradictions, fresh feature f0): depth-4 extension
  built; disc2 selected (f0 GE 8) at level 3; edge 11 re-pointed at D4.
- Final: built_delta=4, unresolved_delta=1, ambig_delta=0. Eval 6/6.
- Structure checks: CHK_MIX_depth4 PASS (D4 is DISP), CHK_MIX_d4atom PASS
  (D4 labeled atom (0,1,8)), CHK_MIX_d4defterm PASS (D4 default edge
  targets TERM(3), the old leaf).

Recursion composes one level deeper than round-1 F1 (depth 4), and the
mixed-output guard fires correctly at depth 3 without corrupting the
pending refine.

## Kill bars (all satisfied)

- K1: prereg committed alone (c3fc2b964) before the attack file; result
  commit verified as its descendant. No bar weakened.
- K2: both families matched every frozen prediction 3/3; no break bar
  tripped (no dropped record, no double-build, no misrouted dispatch,
  no re-point on mixed outputs, no withhold on consistent contradictions,
  no silent misresolution). Verdict maps to
  L3C-V2-ADV2-SURVIVES-THIS-ROUND.
- K3: pure Zag, zero Python, no dashes (shell check), mechanism
  unmodified, prohibited paper untouched (verified empty diff).

## Recommendation

The v2 construction mechanism survives both attack fronts. The two
remaining untested dynamics named by round-1 (cross-edge race
serialization, post-chain mixed handling) now have exact-trace evidence
of coherent behavior. I recommend the v3 OR-vocabulary design question is
now warranted: F2's disjunction blind spot is the only confirmed
structural ceiling, and round-2 adds evidence that refinement races and
depth-4 composition are not the binding constraint. The honest ceiling
remains bounded L2; no L3 or Criterion-0 claim is affected by this round.
The v1 emergence claim stays retired.
