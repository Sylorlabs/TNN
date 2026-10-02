# H-UNIFIED11 Red Team (U11-ADV): RESULT

**Date:** 2026-09-29
**Adversary prereg:** `5d94f7765` (committed alone before any attack code, build, or run)
**Target:** H-UNIFIED11 builder result `fcbb8fac3` (builder prereg `b5a74dd9d`), SURVIVES 31/31 via R12
**Verdict: SURVIVES.** No kill criterion fired, no downgrade criterion fired. All four frozen attacks hold.

This is a red-team verdict, not canonical acceptance. Per Micah 2026-09-29, no successor is spawned; the UNIFIED lane freezes after this red team unless knowledge integrity is at risk, the continuing learner is blocked, or competitive evaluation exposes the problem.

## Method

Attack harness `u11_adv.zag` = lines 1..1620 of the frozen `unified11_learn.zag` blob at `fcbb8fac3` (everything before `fn main` at line 1621), verified byte-identical via `cmp` against the working tree, plus an attack-only `fn main`. Zero mechanism lines edited. Toolchain `znc 2026.07.0-dev`, same as builder. Runs: 3/3 byte-identical (`cmp`), exit 0, zero stderr. Raw md5 `6a76de4b5a1275a7f1bdf3ccb30e5377` (`U11_ADV_RAW.txt`). Analysis via shell tools only (grep/cmp/md5/diff). No Python at any stage.

## X-U11-1: Phantom tombstone re-test - HOLDS

- (a) White-box: `tomb_match(W,0,0,0,0,0)==0` on a fresh `world_init` world. PASS.
- (b) Behavioral: `handle_caus_learn(W,"0,0,0>0,0")` returned 1 (stored); `TOMB_N()==0`; zero `UTOMBSTONE` lines in the X-U11-1 section (shell-verified). PASS. The exact X-U10-2c scenario is closed.
- (c) Static: all 13 `z_alloc(65536)` sites in the frozen source are each immediately followed by a `world_init` call on the same variable (13/13, line-paired and recorded). No world-creation site bypasses the init. PASS.

No kill: no phantom refusal, no white-box match, no uncovered site.

## X-U11-2: Tombstone validity under stress - HOLDS

Base rule `7,0,0>0,1` stored; 9 distinct contradictions `7,0,0>0,2`..`7,0,0>0,10`:

- (a) All 9 returned 0; `TOMB_N()==9`; `TOMB_CUR()==1` (ring wrapped: writes went to entries 0..7,0). PASS.
- (b) `tomb_get` entry audit: entry 0 holds the 9th signature `(7,0,0,0,10)`; entries 1..7 hold signatures 3..9; `tomb_match(W,7,0,0,0,2)==0` (flushed signature gone from every entry). PASS. The 9th contradiction correctly overwrote the oldest entry.
- (c) Replaying each live signature (8 replays): all returned 0, `TOMB_N` and `QCOUNT` unchanged, exactly 8 `UTOMBSTONE` lines in the section (shell-verified). PASS. Every live tombstone still refuses.
- (d) Replaying the flushed signature `7,0,0>0,2`: 0 stored, `QCOUNT` +1, `TOMB_N` 9->10, zero `UTOMBSTONE` for `(7,0,0)->(0,2)` (shell-verified). PASS. The flushed evidence was treated as a fresh contradiction (re-quarantined), which is exactly the disclosed resurrection boundary from U10-ADV carried forward in PREREG_UNIFIED11.md non-goals. Not a kill.

No kill: ring discipline exact, no stale-entry false refusal, counters exact at every step.

## X-U11-3: s0=-1 sentinel collision - HOLDS

- (a) Stream: `route_line("-1,0,0>0,0")` returned 0 (WITHHOLD, "single pair/episode: learning needs 2+ segs", shell-verified in trace); direct `handle_caus_learn(W,"-1,0,0>0,0")` hit the handler shape gate (`USHAPE` skip, shell-verified), returned 0, `TOMB_N` unchanged. PASS.
- (b) Operator: `handle_caus_revise(W,"!-1,0,0>0,0")` hit the shape gate (`USHAPE` skip), returned 0, no tombstone write. PASS.
- (c) White-box shape-of-exposure: `tomb_match(W,-1,0,0,0,0)==1` on the fresh world, as expected. This confirms the exact shape of the disclosed exposure: sentinel entries would match a hypothetical `(-1,0,0)>(0,0)` signature. Probes (a) and (b) show that signature is unreachable through either the stream parser or the operator parser, because `field_kind` accepts digits and commas only (byte 45 fails the shape gate at both layers). The builder's disclosure ("exposure predates R12 and is unchanged by it") is empirically accurate. Not a kill, not a downgrade.
- (d) Clear integrity: stored `9,0,0>0,1`; quarantined `9,0,0>0,5` (`tomb_match==1` before clear); `tomb_clear` on the exact signature; `tomb_match==0` after; entry scan shows exactly one entry with `(s0==-1, ns1==5)` (the cleared one; fresh entries are `(-1,0,0,0,0)`). PASS. Cleared entries cannot falsely refuse real episodes.

No kill: no reachable path commits, quarantines, or matches a negative-field episode; no false refusal from cleared entries.

## X-U11-4: Regression - HOLDS

- (a) Rebuilt `unified11_learn.zag` from the frozen blob at `fcbb8fac3`; production main ran 3x byte-identical (`cmp`), exit 0, zero stderr, zero FAIL lines; output byte-identical (`cmp`) to committed `UNIFIED11_RAW_OUTPUT.txt`, md5 `55f716a6a33c0655b662c4b9d4bb359e` (matches the builder's frozen hash). Binary 218062 bytes (matches builder). PASS.
- (b) Diff of frozen blobs (`86a759d1b` U10 vs `fcbb8fac3` U11): 18 hunks, 16 removed lines, 72 added lines. Every removed line falls in a disclosed R12 category: v10 header comment, banner emit, the 12 `set32(Wx, ST_STR(), STR0())` call sites, 2 verdict renames. Every added line falls in a disclosed R12 category: v11 header, `world_init` function + comment, banner/verdict renames, 13 `world_init` call sites, K-U11-1/K-U11-2 fixtures. Zero behavioral changes outside R12. PASS.

## Residual observations (no kill/downgrade criteria; documented per prereg)

1. The 8-entry tombstone capacity and the flushed-evidence resurrection behavior are unchanged from H-UNIFIED10 and remain disclosed design boundaries (X-U11-2d reproduced the documented behavior exactly).
2. The `s0=-1` sentinel remains a validity-by-convention scheme with no validity flag; the parser's digit-only gate is what makes it safe. Any future path that writes non-digit-parsed values into tombstone fields or episode signatures would need to re-audit this assumption.
3. `world_init` does not reset `TOMB_CUR`/`TOMB_N`; this is correct only because every call site uses a fresh `z_alloc` (zeroed) world, which the 13/13 site audit confirms. A future world-reuse path would need to extend `world_init`.

## Commits (tnn-native-lab, local only)

- `5d94f7765` adversary prereg (alone)
- This result commit: report + raw evidence (`U11_ADV_RESULT.md`, `U11_ADV_RAW.txt`), owned `u11_adversary/` paths only

## Governance

- Prereg `5d94f7765` strictly precedes all attack code, builds, and runs (no pre-prereg builds or runs of any kind).
- Pure Zag throughout (harness, builds, runs). Shell text tools only for analysis. Zero Python.
- No em dashes in documentation (byte-checked).
- No binaries committed; builds and runs in /tmp only.
- Harness mechanism region cmp-verified byte-identical to the frozen blob; zero mechanism lines edited.
