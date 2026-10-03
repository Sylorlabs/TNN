# PREREG H-UNIFIED11 (R12): phantom tombstone init fix

**Date:** 2026-09-29
**Lane:** H-UNIFIED11 frontier researcher (repair of H-UNIFIED10 after red-team DOWNGRADE)
**Status:** FROZEN. Committed alone before any implementation, build, or run.

## Target

H-UNIFIED10 SURVIVES (29/29), prereg `64db99d58`, result `86a759d58` family
(builder result `86a759d1b`).
Red team DOWNGRADED (X-U10-2c defect confirmed, no kill), adversary prereg
`b89469cb8`, adversary result `f0593a0c7`.

## The defect to repair

### D1: X-U10-2c phantom zero-episode tombstone (R11b implementation defect)

Red team: on a fresh world, `handle_caus_learn(W, "0,0,0>0,0")` returned
nstored==0 with a `UTOMBSTONE` refusal, though the episode is well-formed
(3-int > 2-int), coherent on an empty store, and was never quarantined.

Root cause: the 8-entry tombstone table (TOMB_BASE()=1744) lives in
zero-initialized world memory (`z_alloc` zeroes all bytes). `tomb_match`
has no validity flag, so the 8 fresh `(0,0,0,0,0)` entries are live and
entry 0 matches the all-zero episode. `tomb_clear` already uses `s0=-1`
as the invalid sentinel, but fresh entries are never initialized to it.

Severity (per red team): narrow but real. Only the all-zero episode is
affected, and only until 8 genuine quarantines overwrite the phantom
entries. No data loss (refusal, not corruption). The main R11b mechanism
works.

## The repair (R12)

### R12a: world-init centralizes tombstone sentinel init (closes D1)

Add `fn world_init(W:[]u8)void`: sets `set32(W, ST_STR(), STR0())` (the
existing world pointer init) AND initializes all 8 tombstone entries with
`s0=-1` (the existing invalid sentinel, already used by `tomb_clear`).
No validity-flag change to `tomb_match` is needed: sentinel entries
`(s0=-1,...)` never match a real episode signature, consistent with the
existing `tomb_clear` contract.

Replace all 12 world-creation sites in `main()` (W, W5, two W6 scopes,
W9a, W9b, W9c, W9d, W10a, W10b, W10c, W7) from
`set32(Wx, ST_STR(), STR0());` to `world_init(Wx);`. New test world WZ
also uses `world_init`.

This is the exact fix the red team recommended (adversary result section
"Recommended follow-ups" item 1). The DOWNGRADE lifts only on a clean
re-freeze and re-run, which this prereg governs.

## Frozen kill bars

### K-U11-1: phantom tombstone closed (D1 repair)

Setup: fresh world WZ via `world_init`. `handle_caus_learn(WZ,
"0,0,0>0,0")`.

Expect: returns 1 (stored). TOMB_N()==0 (no quarantine occurred).
`cpredict(WZ,CBASE(),0,0,0)` returns 1 predicting (0,0). No `UTOMBSTONE`
trace in the K-U11-1 output window.

Kill if: nstored != 1, or TOMB_N() != 0, or a UTOMBSTONE line appears in
the K-U11-1 section, or the prediction fails.

### K-U11-2: genuine tombstone still refuses (R11b preserved)

Setup: same WZ (now holds "0,0,0>0,0" -> (0,0)). `handle_caus_learn(WZ,
"5,0,0>0,1")` (new s0=5, coherent, stored). `handle_caus_learn(WZ,
"5,0,0>0,9")` (contradicts the s0=5 rule: quarantined + tombstoned).
`handle_caus_learn(WZ, "5,0,0>0,9")` again.

Expect: first returns 1; second returns 0 with QCOUNT delta=1 and
TOMB_N delta=1; third returns 0 with QCOUNT delta=0 and TOMB_N delta=0
(UTOMBSTONE refusal path does not increment TOMB_N; it is counted only
in the per-call ULEARN "tombstoned" field).

Kill if: the replay is stored, or the quarantine counters are wrong, or
the second presentation is quarantined again instead of refused.

### K-U11-3: preserved H-UNIFIED10 behavior (regression)

All 29 H-UNIFIED10 checks PASS. Total ntest/npass becomes 31/31 with the
two new bars. Full raw output is byte-identical to
UNIFIED10_RAW_OUTPUT.txt modulo: (a) the banner line (R12 tag added),
(b) the final verdict line (H-UNIFIED11), (c) the new K-U11-1/K-U11-2
sections (before the RESULT line), (d) the RESULT count line (31/31).

Kill if: any of the 29 inherited checks FAIL, or output diverges beyond
the disclosed deltas.

Note: no inherited fixture uses the all-zero episode (verified by grep
before freezing), so the sentinel init cannot change any inherited
observable.

### K-U11-4: determinism

3/3 runs byte-identical (cmp), exit 0, zero FAIL lines.

Kill if: any run differs, or exit != 0, or any FAIL line.

### K-U11-5: diff purity

`unified11_learn.zag` is `unified10_learn.zag` (at `86a759d1b`) copied
verbatim (cmp-verified) plus exactly the frozen R12 change set:
(i) `world_init` function (before `fn main`, mechanism lines 1..1602
unchanged so adversary harnesses keep working), (ii) 12 call-site swaps,
(iii) banner/verdict renames, (iv) K-U11-1/K-U11-2 fixtures.

Kill if: the diff contains any behavioral change outside R12.

## Explicit non-goals (disclosed boundaries)

- The s0=-1 sentinel is a pre-existing design assumption (tomb_clear
  already used it). R12 makes fresh state consistent with it. An episode
  with literal s0=-1 would collide with the invalid sentinel; this
  exposure predates R12 and is unchanged by it.
- B-U10-1 (tombstone over-withholding, episode-indexed precision cost),
  B-U10-2 (stream-injected merit, out of scope), the 8-entry tombstone
  capacity, the recency edge at exactly CSEQ == bseq+32, and luses=1
  unprotected are all carried forward unchanged.
- Classification remains bounded L2. This is a one-defect implementation
  repair, not L3.

## Governance

- Prereg committed alone before any implementation, build, or run.
- `unified11_learn.zag` = committed `unified10_learn.zag` copied verbatim
  (cmp-verified), plus exactly the frozen R12 change set.
- Pure Zag throughout. No Python at any stage.
- No em dashes in loop documentation (byte-verified before commit).
- Only owned paths staged: `u11_frontier/` directory.
- 3/3 deterministic runs required.
- Builds and runs in /tmp/u11 only; no binaries committed.

## Verdict rule

SURVIVES if K-U11-1..K-U11-5 all PASS.
DOWNGRADED if K-U11-1 or K-U11-2 FAIL but K-U11-3 and K-U11-4 PASS
(mechanism works, repair incomplete).
KILLED if K-U11-3 FAILS (regression: broke H-UNIFIED10) or K-U11-4 FAILS
(non-deterministic) or DCOUNT>0 or silent eviction in any bar.
