# H-CAUSAL-UNIFIED6 RED TEAM REPORT (X-CU6-1..X-CU6-4)

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED6 Red Team (independent subagent)
**Target:** H-CAUSAL-UNIFIED6 SURVIVES (5/5), result `438c3344a`.
**Prereg:** `PREREG_CU6_ADV.md` (commit `e74b3f0c8`, frozen alone
before any attack fixture, build, or run).
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python
in prereg, fixtures, builds, runs, analysis, or scratch.
**Verdict: H-CAUSAL-UNIFIED6 SURVIVES this red team.** All four
attacks fail to kill or downgrade. No KILL or DOWNGRADE criterion
fired.

## 1. Method

Attack harness `cu6_red_adv.zag` assembled from committed source
only: mechanism lines 1..2488 byte-verbatim from
`unified_causal6.zag` at git HEAD (cmp-verified against the
builder's own harness mechanism region; identical), plus adversary
helpers and a new main() with the frozen X-CU6-1..X-CU6-3
fixtures. All builds and runs from committed blobs via
`git show HEAD:...`, never the working tree.

## 2. X-CU6-1: three-outcome contradiction (HOLD)

Rationale: `conflict_adjudicate` refuses to carve when 3+ distinct
outcomes exist (messy=1), so a 3-outcome ST_CONFL entry is
permanent and the guard's third-outcome early-return is its only
protection. The builder never tested 3 outcomes.

Construction: builder K-CU6-1 fixture (flood, carve at (2,0,0),
re-conflict with (1,1,1)), then a third outcome `2,0,0,2>2,2,2`
absorbed into the ST_CONFL entry, then fresh general
`2,0,2,2>7,7,7`.

Raw (`CU6_ADV_RED_RAW_1.txt`, 3/3 byte-identical, MD5
`c245a241749c99cb82106d3e3c062382`):
- Adversary helper confirms 3 distinct live outcomes at (2,0,0).
- Query (2,0,0): `WITHHOLD (live-contradiction)`, r=0.
- Control (2,0,2): r=1 out=(7 7 7) via (exact-episode).

The guard's third-outcome path fires correctly. No shadow. HOLD.

## 3. X-CU6-2: tombstone chain (HOLD via legitimate adjudication)

Construction: X-CU6-1 steps 1-3, then two supporting (0,0,0)
episodes at (2,0,0) to force a re-carve attempt from the oldest
tombstone, then the general shadow.

Raw: the first supporting episode absorbed (CONFLICTED-ABSORB),
then `UNCONFLICT action 2 state (2 0 0) at seq 23: winner outcome
(0 0 0) support 3 vs loser (1 1 1) support 1; carved new entry 3
[s0=2&s1=0&s2=0] with 3 winner episode(s); 1 loser episode(s)
SUPERSEDED in conflicted entry 2 (ST_CONFL kept)`.

The contradiction was legitimately retired by adjudication (frozen
contest criterion: support>=2 and strict majority). Adversary
helper confirms zero live contradictions at (2,0,0) afterward.
Query (2,0,0): r=1 via (exact-episode) from the adjudicated entry.
The guard is correctly silent; this is a proper carve, not a
shadow. Control (2,0,2): r=1 out=(7 7 7).

Per the frozen prereg ("unless a legitimate adjudication retired
the contradiction (in which case the raw must show the carve and
the guard correctly silent)"), this is a HOLD. The mechanism
correctly distinguished adjudication from shadowing through a
tombstone chain.

## 4. X-CU6-3: untracked contradiction, contest capacity (HOLD)

Construction: 8 tracked contests opened at 8 distinct states
(contest capacity exhausted), then at (4,0,0) outcome (0,0,0) then
(1,1,1). Raw confirms: `ERROR: contest capacity (8) exhausted;
contradiction at state (4 0 0) has no contest slot; contradiction
UNTRACKED` and `ENTRY action 2 [any] CONFLICTED: contradiction
untracked (contest cap) at seq 18 (WITHHOLD)`.

- Adversary helper confirms a live contradiction at (4,0,0).
- Query (4,0,0): `WITHHOLD (live-contradiction)`, r=0.
- Control (4,0,2): r=1 out=(7 7 7) via (exact-episode).

The guard applies equally to untracked tombstones, confirming the
builder's disclosure. No shadow. HOLD.

## 5. X-CU6-4: regression (PASS)

From committed blobs at git HEAD:
- Builder adversary (K-CU6-1/K-CU6-2): rebuilt, rerun,
  byte-identical (cmp) to committed `CU6_ADV_RAW_1.txt`.
- Battery: rebuilt `cu6_test.zag`, rerun, byte-identical (cmp) to
  committed `CU6_TEST_RAW_1.txt` (16/16).
- Main: rebuilt `unified_causal6.zag`, rerun, byte-identical (cmp)
  to committed `CU6_MAIN_RAW_1.txt` (28/28).
- Diff `unified_causal5.zag` vs `unified_causal6.zag` (both from
  HEAD): exactly the frozen change set, 50 diff lines (40-line
  `live_contra_at` helper + 10-line predict guard, comments
  included). No other function text changed.

No silent changes. PASS.

## 6. Determinism

Attack harness: 3/3 byte-identical runs (MD5
`c245a241749c99cb82106d3e3c062382`).

## 7. Boundaries and non-claims

- The guard remains exact-state scoped by design; a contradiction
  at state S does not withhold queries at S' != S.
- The guard requires 2+ distinct live outcomes in a single
  ST_CONFL entry; split-across-entries contradictions were not
  observed (the absorb path funnels same-state contradictions into
  the oldest covering tombstone).
- 3+ outcome contradictions are permanently un-adjudicable
  (messy=1); the guard is their only protection, and it holds.
- This is bounded L2 mechanism red-teaming, not L3. No
  representational invention is claimed or tested.

## 8. Governance disclosures

- Preregistration strictly preceded all attack implementation and
  execution (commit `e74b3f0c8`, prereg committed alone).
- Pure Zag throughout: no Python in prereg, fixtures, builds,
  runs, analysis, harnesses, or scratch. File operations via shell
  only.
- All attack builds used mechanism source extracted from committed
  git blobs (`git show HEAD:...`), never the working tree.
- Only explicitly owned paths staged:
  `docs/lab/research-lead/overnight-20260928/causal_unified6_adversary/`.
- No binaries or generated artifacts committed (raw outputs are
  text; binaries and .zag-cache kept in /tmp).
- Commits are local; no push attempted or authorized.
- No frozen bar was weakened or retroactively changed. The X-CU6-2
  verdict applied the prereg's written "legitimate adjudication"
  clause verbatim; the raw shows the carve and the guard correctly
  silent.
- This document contains no em dashes.

## 9. Commit lineage

- `e74b3f0c8` PREREG H-CAUSAL-UNIFIED6 red team FROZEN (alone,
  before harness/builds/runs). X-CU6-1..4 with frozen kill
  criteria. Pure Zag.
- (this commit) `cu6_red_adv.zag` (attack harness: committed
  mechanism + adversary code), `CU6_ADV_RED_RAW_1/2/3.txt`
  (3/3 byte-identical attack runs), and this report.

## 10. Verdict

**H-CAUSAL-UNIFIED6 SURVIVES this red team.** X-CU6-1 (3+
outcomes), X-CU6-2 (tombstone chain), and X-CU6-3 (untracked
contradiction under contest-capacity pressure) all HOLD; X-CU6-4
regression PASSES with zero byte differences and a pure frozen
diff. The live-contradiction guard closes the demonstrated failure
class on every probed path, including the builder-untested
three-outcome and untracked-tombstone configurations.
Classification: bounded L2; nothing here is L3.
