# PREREG: XP-COUNTMAP-1 (two-relation negative: formation without addressability)

Frozen 2026-10-03. To be committed alone before implementation.
Worker: XP-COUNTMAP-1. Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/xp_countmap1/ (files countmap1_*).
Non-ledger task (claim minting paused).

## Objective

COUNTMAP-SINGLETON (read-only source analysis of the XP-DAGFAN-4
frozen build) decomposed the singleton count MAP into four facts:
(A) the composition-layer lookup `xs5_find_countmap` is singleton
by construction (first live tag-20 INC-ok MAP wins, no relation
parameter); (B) formation is unbounded in principle
(`promote_graph` mints a fresh tag-20 MAP per verified trial with
no dedup); (C) pipeline order makes the singleton self-reinforcing
(`xs5_compose` runs before the trial layer, starving alternative
formation for already-covered counting); (D) the adaptation layer
cannot create count structures. Facts A-C were reasoned from code,
never executed as frozen kill-barred claims.

This experiment converts that code reading into a frozen negative
result: teach counting over rel 82 (forms MAP_Y as in XP-DAGFAN-4),
then teach counting over rel 85 with a verifying expected answer
so the trial layer mints a second live count MAP (MAP_V2), and
show that the composition layer still cannot address it. Banks
Facts A-C as an architecture fact future count-composition designs
must beat. Per the singleton recommendation, XP-COUNTMAP-2
(indexed lookup) is NOT run here.

## Frozen background (read-only, never modified)

- Build block: xdagfan4_block.zag from lane-xdagfan2-20261003
  (HEAD cea1856d2), 2648 lines, SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004,
  re-verified by sha256sum before freezing. Reused verbatim as
  countmap1_block.zag; no frozen name is redefined.
- Key frozen semantics (all line refs to the block):
  - `xs5_find_countmap` (:2134): scans node ids 2..1023, returns
    the first live tag-20 MAP whose field-20 graph contains an
    INC cell (tag 103). No relation parameter.
  - `xs5_agg_rel` (:2147): derives the world's single aggregation
    relation from the singleton's first type-1 provenance edge.
  - `xs5_agg_exec` (:2177): hard gate, returns -2 with no
    singleton; assembles the count template ephemerally per query
    via `t2_asm_count` over r_agg. The stored INC graph is never
    executed by the composition layer.
  - `xs5_compose` (:2208): tries every live nav-ok tag-20 MAP in
    id order as (NAV, AGG) over the ambient r_agg; count MAPs are
    never nav candidates (`cc_relseq` returns -1 on an INC-cell
    graph: the 102/101 alternation breaks at the first 103).
  - `t2_trial` count path (:635-647): iterates relations of the
    query subject via `t2_rels`, builds the maximal per-relation
    chain via `t2_chain`, assembles a count graph, promotes on
    verify. `promote_graph` (:533) mints a fresh tag-20 MAP per
    call with no dedup check and teaches the answer fact.
  - `ev_query_xs5` (:2423) stage order: activate, rebind_try,
    xs5_compose, mp_run/t2_trial, bootstrap_miss, xs5_select,
    miss_inquire.

## Design

All identifiers opaque (relation numbers only). Structural terms
only: "count structure", "nav structure". No domain labels.

Phase A, count training over rel 82 (replicates the xd4_train
shape from XP-DAGFAN-4 verbatim, the exact context in which MAP_Y
formed in the frozen runs):
teach (11,81,12), (12,81,13), (13,81,14);
ev_query_xs5(11,91,14) -> 14 (trial chain path promotes a chain
MAP; expected 14 ends the 3-link 81 walk);
teach (50,82,51), (51,82,52), (52,82,53);
ev_query_xs5(50,92,3) -> 3;
30 distractors: (5000+i, 60+(i%10), 6000+i) for i=0..29.
Predicted: TRAIN-Y reaches the trial count path (compose fails:
r_agg=-1, no count MAP yet), t2_rels(50)={82}, the 3-link 82-chain
verifies 3==3, trial promotes MAP_Y (count MAP over rel 82).
Stash my = xs5_find_countmap(W) (expect >= 0), aggA =
xs5_agg_rel(W) (expect 82), ncmA = exhaustive INC-ok count-MAP
scan (expect 1).

Phase B, second count over rel 85 (fresh subject, fresh rel):
teach (110,85,111), (111,85,112), (112,85,113), (113,85,114).
B1: c_pre = xs5_compose(W,110,117,4), direct call, predicted -2.
  r_agg is 82; every nav MAP holds an 81-relseq that cannot walk
  from 110 (no 81 facts at 110); the symmetric (AGG,NAV) try fails
  (no 82-chain from 110, len<2). No verify, no promotion.
B2: b = ev_query_xs5(W,110,117,4), predicted 4 via the trial
  layer. Pipeline: activate miss; rebind tried=0; xs5_compose
  fails (emits XS5-COMPOSE fail); trial chain path: path endpoints
  111/112/113/114, none == 4; sum path: 111 != 4; count path:
  t2_rels(110)={85}, 4-link 85-chain verifies 4==4, promotes
  MAP_V2 (count MAP over rel 85, provenance rel 85), answers 4.
  xs5_select never runs (trial answered).
B3: c_post = xs5_compose(W,110,117,4), direct call, predicted -2.
  MAP_V2 now exists but the lookup still returns MAP_Y, r_agg is
  still 82, and MAP_V2 is not a nav candidate.

Query budget: 3 full ev_query_xs5 calls plus 2 direct
xs5_compose calls (no pipeline, no promotion on failure), within
the demonstrated safe range.

## Frozen predictions

- K1: after phase B, exactly 2 live tag-20 MAPs satisfy the frozen
  count-MAP predicate (live, tag 20, field-20 graph INC-ok, i.e.
  the `xs5_find_countmap` predicate applied exhaustively). The
  second (higher-id) count MAP's first type-1 provenance edge
  points to a fact with rel 85.
- K2: xs5_find_countmap(W) == my (the phase-A id). Lowest id wins;
  MAP_V2 is invisible to the lookup.
- K3: xs5_agg_rel(W) == 82 after phase B. The first-learned
  aggregation relation is not displaced.
- K4: c_pre == -2 and b == 4 and c_post == -2; the phase-B full
  query trace contains "XS5-COMPOSE fail" with no "XS5-COMPOSE ok"
  and no "XS5-TRY" (rebind tried=0), pinning the 4 to the trial
  layer. Formation without addressability, demonstrated.
- K5: 3/3 byte-identical whole-output runs; sha256 recorded.
- K6: pure Zag; safebin PATH from the first command; zero em/en
  dash bytes in lane docs (byte-verified); opaque identifiers
  only; frozen block reused verbatim (SHA re-verified pre/post);
  driver-only new code under the cm1_ prefix; 0 new node types,
  0 new edge types, 0 new opcodes, 0 new operators, 0 modes,
  bridges, handlers; Zag pitfalls honored (see NAMECHECK.md).

## Kill-bar discrimination (why each bar can fail)

- K1 fails if the trial layer does not mint MAP_V2 (stays 1) or
  mints duplicates on the single verifying query (>2); the
  provenance check fails if the second count MAP is an 82-count
  duplicate rather than a genuine 85-count structure.
- K2 fails if the lookup is relation-aware (returns MAP_V2).
- K3 fails if the second count MAP displaces r_agg to 85.
- K4 fails if composition answers the 85-count (addressable
  second count MAP) or if the trial layer fails to form/answer
  (no formation). Either direction kills the banked claim.
- K5/K6 are process bars: any nondeterminism or toolchain lapse
  voids the result.

Verdict XP-COUNTMAP-1-PASS iff K1-K6 all pass. VOID is terminal.

## Implementation plan (after prereg commit)

1. Copy the verified frozen build block to xp_countmap1/ as
   countmap1_block.zag; re-verify SHA256
   56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004.
2. Write countmap1_driver.zag (cm1_ prefix): cm1_train (phase A,
   xd4_train shape verbatim), cm1_phaseB (teaches, B1/B2/B3),
   cm1_h1 (K1-K4 assertions with exhaustive count-MAP scan and
   provenance-rel helpers), main() with one workspace. Pure Zag.
   No redefinition of any frozen name. Zag pitfalls honored.
3. Build: cat countmap1_block.zag countmap1_driver.zag >
   countmap1_full.zag. Compile with the pinned znc
   (src/tools/toolchain/znc_linux_x86_64_abed8aa1); run 3x;
   verify byte-identical; check kill bars; shell-verify trace
   markers and dash absence.
4. Write countmap1_REPORT.md. Commit with explicit pathspecs
   (lane directory only; never the ledger; never push).

## Constraints

Frozen read-only (the 2648-line build block; the
lane-xdagfan2-20261003 branch is not modified or merged). Pure
Zag (safebin PATH from the first command, no python; Step 0
recorded in NAMECHECK.md). Zero em/en dashes. Commits local
only, never pushed, explicit pathspecs, no reset, no amend of
shared history. No indexed-lookup patch (that is COUNTMAP-2,
explicitly held). Do not modify CLAIM_LEDGER.md. Zag pitfalls
honored.

## Battery well-formedness (disclosed pre-freeze work)

Before freezing, no driver code was written or prototyped. The
phase-A shapes are the committed XP-DAGFAN-4 xd4_train shapes;
phase B is a fresh rel/subject pair; the B1/B2/B3 trial-safety
analysis is derived from frozen operator semantics (t2_trial
search order, xs5_compose nav iteration, cc_relseq on INC-cell
graphs), not from execution. The frozen bars were not adjusted
to fit any outcome. Pre-freeze verification was limited to:
reading the COUNTMAP-SINGLETON REPORT.md, the XP-DAGFAN-4
REPORT/PREREG/driver/NAMECHECK, the frozen block source
(xs5_find_countmap, xs5_agg_rel, xs5_agg_exec, xs5_try_nav_agg,
xs5_compose, t2_trial, promote_graph, cc_relseq,
t2_try_verify, ev_query_xs5), and re-verifying the build-block
SHA (56b2e678...).
