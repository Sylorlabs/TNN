# PREREG: H-UNIFIED11 Red Team (U11-ADV) FROZEN

**Date:** 2026-09-29
**Lane:** H-UNIFIED11 independent red team (the ONE allowed red team per Micah 2026-09-29 directive; no successor will be spawned)
**Status:** FROZEN. Committed alone before any attack code, build, or run.
**Target:** H-UNIFIED11 builder result `fcbb8fac3` (builder prereg `b5a74dd9d`), claiming SURVIVES 31/31 via R12 (`world_init` initializes all 8 tombstone entries with s0=-1).
**Reference defect:** X-U10-2c (H-UNIFIED10 red team `f0593a0c7`): fresh zero-initialized tombstone entries `(0,0,0,0,0)` matched the all-zero episode `(0,0,0)>(0,0)`, causing a never-quarantined episode to be refused via UTOMBSTONE.

## Attack stance

Assume the R12 repair claim is false. Attack the repair, not the inherited mechanism. Four attacks, each with frozen kill/downgrade criteria below.

## Harness construction (frozen)

- Attack harness `u11_adv.zag` = lines 1..1620 of the frozen `unified11_learn.zag` blob at `fcbb8fac3` (everything before `fn main` at line 1621), verified byte-identical via `cmp`, plus an attack-only `fn main`. Zero mechanism lines edited.
- Toolchain: `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc` (`znc 2026.07.0-dev`), same as builder.
- 3/3 runs required byte-identical (`cmp`), exit 0. Analysis via shell tools only (grep/cmp/md5/diff/awk). No Python at any stage.
- Raw output persisted as `U11_ADV_RAW.txt`; report as `U11_ADV_RESULT.md`. Owned paths only: `u11_adversary/`.

## X-U11-1: Phantom tombstone re-test

**Goal:** verify the s0=-1 init actually prevents the (0,0,0)>(0,0) phantom, and try to construct a fresh world where a tombstone still matches incorrectly.

**Setup:** fresh world W via the mechanism's own `world_init`.

**Probes:**
- (a) White-box: `tomb_match(W,0,0,0,0,0)` on the fresh world must return 0 (no entry may match the all-zero signature).
- (b) Behavioral: `handle_caus_learn(W,"0,0,0>0,0")` must return 1 (stored); `get32(W,TOMB_N())` must be 0; zero `UTOMBSTONE` lines in the X-U11-1 section.
- (c) Static: every `z_alloc(65536)` site in the frozen source (13 sites, read-only verified pre-prereg) must be immediately followed by a `world_init` call on the same variable. Verified mechanically during the attack; any site bypassing `world_init` is a live phantom vector.

**KILL if:** (a) fails (tomb_match fires on a fresh world), or (b) fails (phantom refusal: nstored != 1, or TOMB_N != 0, or any UTOMBSTONE line in the section), or (c) fails (any world-creation site bypasses world_init).

**DOWNGRADE:** none predefined; any non-fatal anomaly is documented, not promoted.

## X-U11-2: Tombstone validity under stress

**Goal:** fill all 8 tombstones, verify the 9th contradiction flushes the oldest correctly, verify live tombstones still refuse, verify the flushed signature is NOT falsely refused.

**Setup:** fresh world W via `world_init`. Store base rule `handle_caus_learn(W,"7,0,0>0,1")` (expect 1). Then 9 distinct contradictions `7,0,0>0,2` through `7,0,0>0,10` (expect 0 each, each quarantined; same contradict-pattern as frozen K-U11-2).

**Expect:**
- (a) `get32(W,TOMB_N())==9` after the 9 contradictions.
- (b) `get32(W,TOMB_CUR())==1` (ring cursor wrapped: writes went to entries 0..7,0).
- (c) `tomb_get(W,0,0..4)==(7,0,0,0,10)` (9th signature overwrote entry 0); entries 1..7 hold signatures `7,0,0>0,3` through `7,0,0>0,9`; no entry holds `(7,0,0,0,2)` (flushed).
- (d) Replaying each live signature (`7,0,0>0,3` .. `7,0,0>0,10`): 0 stored, UTOMBSTONE refusal each, TOMB_N unchanged.
- (e) Replaying the flushed signature (`7,0,0>0,2`): NO UTOMBSTONE for it; treated as a fresh contradiction (0 stored, QCOUNT +1, TOMB_N 9 -> 10). This is the disclosed resurrection boundary (U10-ADV finding, carried forward in PREREG_UNIFIED11.md non-goals): expected behavior, not a kill.

**KILL if:** the 9th contradiction does not overwrite entry 0, or any live signature (d) fails to refuse its replay via UTOMBSTONE, or the flushed signature is still refused via UTOMBSTONE (stale entry / false refusal), or TOMB_N miscounts at any step.

**DOWNGRADE if:** ring discipline holds but per-call ULEARN accounting disagrees with the cumulative counters (accounting anomaly without integrity loss).

## X-U11-3: s0=-1 sentinel collision

**Goal:** test whether the sentinel can collide with real data or be evaded. Pre-prereg read-only fact: `field_kind` accepts digits and commas only; byte 45 ('-') fails the shape gate, so the stream parser cannot produce negative values. The builder discloses the collision as a pre-existing design assumption (PREREG_UNIFIED11.md non-goals).

**Probes (fresh world W via world_init):**
- (a) Stream attack: `handle_caus_learn(W,"-1,0,0>0,0")` must yield 0 stored, a USHAPE skip, TOMB_N unchanged, no crash.
- (b) Operator attack: `handle_caus_revise(W,"!-1,0,0>0,0")` must yield 0 stored, a USHAPE skip, no tombstone write.
- (c) White-box shape-of-exposure: `tomb_match(W,-1,0,0,0,0)` on the fresh world is expected to return 1. This documents the exact shape of the disclosed exposure (sentinel entries match a hypothetical (-1,0,0)>(0,0)); it is not reachable via (a)/(b).
- (d) Clear integrity: quarantine a real episode (`9,0,0>0,5` after storing `9,0,0>0,1`), clear it via `tomb_clear` on its exact signature, then verify `tomb_match` for that signature is 0 and that re-presenting a coherent episode with the same signature is not falsely refused.

**KILL if:** any reachable path (stream or operator) commits, quarantines, or tombstone-matches an episode carrying a negative field (i.e., (a) or (b) stores or writes a tombstone, or (d) shows a cleared entry causing false refusal of a real episode).

**HOLDS (no kill, no downgrade) if:** only (c) holds while (a), (b), (d) behave as expected. Then the builder's disclosure ("exposure predates R12 and is unchanged by it") is empirically accurate.

## X-U11-4: Regression

**Goal:** verify all 31 builder checks reproduce byte-identical and the U10->U11 diff contains only R12.

**Probes:**
- (a) Rebuild `unified11_learn.zag` from the frozen blob at `fcbb8fac3`; run the production main 3x; require byte-identical (`cmp`) to committed `UNIFIED11_RAW_OUTPUT.txt` (md5 `55f716a6a33c0655b662c4b9d4bb359e`), exit 0 all runs, zero FAIL lines.
- (b) Diff frozen U10 blob (`86a759d1b:unified10_learn.zag`) vs frozen U11 blob (`fcbb8fac3:unified11_learn.zag`); require every hunk to fall in the disclosed R12 categories: header comment, `world_init` function, banner/verdict renames, 13 call-site swaps (12 in main + WZ), K-U11-1/K-U11-2 fixtures. No other behavioral changes.

**KILL if:** (a) fails (raw output not byte-identical, exit != 0, any FAIL), or (b) shows any behavioral change outside the disclosed R12 set.

## Verdict rule

- KILLED if any X-U11-1..X-U11-4 fires its KILL criterion.
- DOWNGRADED if any fires its DOWNGRADE criterion and none fires KILL.
- SURVIVES otherwise.
- This is a red-team verdict, not canonical acceptance. Per Micah 2026-09-29: no successor is spawned from this red team; the UNIFIED lane freezes after this unless knowledge integrity is at risk, the continuing learner is blocked, or competitive evaluation exposes the problem.

## Governance

- Prereg committed alone before any attack code, build, or run.
- Pure Zag throughout (harness, builds, runs). Shell text tools only for analysis. No Python at any stage, including scratch and verification. Disclosure does not cure; therefore there is nothing to disclose.
- No em dashes in documentation (byte-checked before commit).
- Only owned paths staged: `docs/lab/research-lead/overnight-20260928/u11_adversary/`.
- No binaries committed; builds and runs in /tmp only.
