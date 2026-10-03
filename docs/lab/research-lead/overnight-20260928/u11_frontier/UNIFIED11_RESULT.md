# H-UNIFIED11 RESULT (R12): phantom tombstone init fix

**Date:** 2026-09-29
**Lane:** H-UNIFIED11 frontier researcher (repair of H-UNIFIED10 after red-team DOWNGRADE)
**Target:** H-UNIFIED10 DOWNGRADED on X-U10-2c (phantom zero-episode
  tombstone), builder prereg `64db99d58`, builder result `86a759d1b`,
  red-team prereg `b89469cb8`, red-team result `f0593a0c7`.
**Builder prereg:** `b5a74dd9d` ("Prereg H-UNIFIED11 FROZEN (alone, before
  implementation): R12 phantom tombstone init fix. K-U11-1..5 frozen.
  Pure Zag."), committed alone before any implementation, build, or run.
  Verified: `b5a74dd9d` is a strict ancestor of this result commit via
  `git merge-base --is-ancestor`.
**Verdict: SURVIVES.** All five frozen kill bars PASS (31/31 in-harness
  checks, 3/3 deterministic). The X-U10-2c defect is closed by the exact
  fix the red team recommended; the DOWNGRADE is lifted by clean re-freeze
  and re-run, per the red team's own condition.

## The repair (R12)

`fn world_init(W:[]u8)void` centralizes fresh-world initialization: the
existing `set32(W, ST_STR(), STR0())` pointer init plus initialization of
all 8 tombstone entries with `s0=-1` (the existing invalid sentinel,
already used by `tomb_clear`). All 12 world-creation sites in `main()`
(W, W5, W6 x2 scopes, W9a, W9b, W9c, W9d, W10a, W10b, W10c, W7) now call
`world_init`; the new test world WZ does too. `tomb_match` needed no
validity-flag change: sentinel entries never match a real episode
signature, consistent with the pre-existing `tomb_clear` contract.

## Build and determinism

- Toolchain: pinned `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`,
  `znc 2026.07.0-dev (edition 2026)`. Build: warnings only (non-strict
  analyzer notes, same class as the U10 builder). Binary 218062 bytes
  (main).
- Runs: 3/3 byte-identical (`cmp` clean), exit 0 all runs, zero stderr.
  Raw md5: `55f716a6a33c0655b662c4b9d4bb359e` (all three runs; identical
  across a rebuild after /tmp was wiped mid-task).
- In-harness checks: **31 PASS, 0 FAIL** (`=== RESULT: 31/31 ===`,
  `H-UNIFIED11 SURVIVES`, zero FAIL lines).
- No Python at any stage. Built and run in /tmp only; no binaries
  committed.

## Kill-bar results (frozen)

### K-U11-1: phantom tombstone closed (D1 repair) - PASS

Fresh world WZ via `world_init`. `handle_caus_learn(WZ,"0,0,0>0,0")`
returned 1 (stored); raw trace `causal: new rule R0 IF s0==0 AND a==0
THEN s1:=0`, ULEARN `1 stored, 0 corroborated, 0 quarantined, 0
tombstoned`; TOMB_N()==0; `cpredict(WZ,CBASE(),0,0,0)` returned 1
predicting (0,0); no `UTOMBSTONE` line in the K-U11-1 window. The
all-zero episode now commits as fresh knowledge, exactly as X-U10-2c
required.

### K-U11-2: genuine tombstone still refuses (R11b preserved) - PASS

Same WZ: `"5,0,0>0,1"` stored (1); `"5,0,0>0,9"` quarantined (0,
QCOUNT delta=1, TOMB_N delta=1, UCOHERE QUARANTINE trace); replay of
`"5,0,0>0,9"` refused (0, QCOUNT delta=0, TOMB_N delta=0,
`UTOMBSTONE: episode (5,0,0)->(0,9)` trace, per-call ULEARN
`tombstoned=1`). The real tombstone path is unaffected by the sentinel
init.

### K-U11-3: preserved H-UNIFIED10 behavior (regression) - PASS

All 29 inherited checks PASS. Raw diff vs UNIFIED10_RAW_OUTPUT.txt
contains ONLY the disclosed deltas: (a) banner line (R12 tag added),
(b) final verdict line (H-UNIFIED11), (c) the new K-U11-1/K-U11-2
sections (16 added lines, before RESULT), (d) RESULT count line
(31/31). Every inherited line is byte-identical. Verified by grep before
freezing that no inherited fixture uses the all-zero episode, so the
sentinel init cannot change any inherited observable.

### K-U11-4: determinism - PASS

3/3 runs byte-identical, exit 0, zero FAIL lines.

### K-U11-5: diff purity - PASS

`unified11_learn.zag` is the U10 source at `86a759d1b` copied verbatim
(cmp-verified) plus exactly the frozen R12 change set: (i) `world_init`
function (inserted before `fn main`; mechanism lines 1..1602 unchanged),
(ii) 12 call-site swaps, (iii) header/banner/verdict renames,
(iv) K-U11-1/K-U11-2 fixtures. No behavioral change outside world init.

## Boundaries carried forward (unchanged)

- s0=-1 sentinel collision is a pre-existing design assumption
  (tomb_clear already used it); R12 makes fresh state consistent with
  it. An episode with literal s0=-1 would collide with the invalid
  sentinel. No new exposure.
- B-U10-1 (tombstone over-withholding), B-U10-2 (stream-injected merit,
  out of scope), 8-entry tombstone capacity, recency edge at exactly
  CSEQ == bseq+32, luses=1 unprotected: all unchanged.
- Classification: bounded L2. This is a one-defect implementation repair,
  not L3.

## Lineage

- Builder prereg: `b5a74dd9d` (committed alone before implementation,
  build, or execution; em-dash scan clean: 0).
- Target under test: `86a759d1b` (H-UNIFIED10 builder result).
- Red team that motivated this repair: `f0593a0c7` (U10-ADV, DOWNGRADED).
- Raw output: `UNIFIED11_RAW_OUTPUT.txt` (md5
  `55f716a6a33c0655b662c4b9d4bb359e`).
- No pushes; commits local only.

## Governance notes

- A mid-task `/tmp` wipe destroyed the first build directory and its
  three run outputs after they had been verified (31/31, md5
  55f716a6a...). Rebuilt from the unchanged frozen source and reran 3x:
  identical md5, confirming cross-rebuild determinism. Raw output was
  then persisted into the repo directory before committing.
- This result is the builder's verdict under the frozen prereg; it is
  NOT a canonical governance acceptance. The red team's condition for
  lifting the DOWNGRADE (clean re-freeze and re-run) is met by the
  prereg+build+run chain above; an independent red team should still
  attack H-UNIFIED11.
