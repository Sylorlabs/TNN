# H-FDCR-UNIFIED8 RESULT: SURVIVES 51/51 (lifetime per-distinct-subject overflow counters)

**Date:** 2026-09-29 (UTC 2026-09-30)
**Researcher:** H-FDCR-UNIFIED8 Frontier Researcher (independent subagent)
**Verdict:** SURVIVES. All frozen kill bars K-FU8-1 through K-FU8-5 pass.
**Prereg:** `039d6fcaa` (committed alone, before any implementation edit).
**Lineage:** `unified_fdcr7.zag` (result `18dd712a3`) copied verbatim
  (cmp-verified), plus exactly the frozen R8a-R8g changes.
  `unified_fdcr7.zag` untouched.

## What was repaired

H-FDCR-UNIFIED7 was DOWNGRADED (not killed) by the X-FU7 red team
for two double-count findings:

- **B-FU7-1 (X-FU7-2/B2b):** an overflow-named subject, membered and
  R3-cleared, then re-recorded via the merge path, was re-admitted
  and re-incremented NOADD_DROP_OVERFLOW (65 increments for 64
  distinct subjects).
- **B-FU7-2 (X-FU7-3/C3b):** a subject counted in the event tier
  (both name lists full), later re-dropped after a clear freed a
  slot, was counted in the overflow tier while its event increment
  persisted (counted in both tiers).

Repair: two lifetime lists in the verified-free 3192..4095 region.

- **R8a:** NOADD_DROP_OVL=3192, 128 entries of 4-byte subject string
  offsets (ends 3704). Every subject ever counted in
  NOADD_DROP_OVERFLOW is recorded here. Strings are append-only, so
  offsets are stable.
- **R8b:** NOADD_DROP_EVL=3704, 48 entries of 8 bytes (subject string
  offset + that subject's event count; ends 4088). Records subjects
  whose drops incremented NOADD_DROP_OVERFLOW2. Free: 4088..4095.
- **R8c:** re-admission of a lifetime-counted subject after R3 clear
  restores the overflow-name entry without re-incrementing
  NOADD_DROP_OVERFLOW (closes B-FU7-1).
- **R8d:** an event-tier subject re-dropped when a slot frees is
  transferred: removed from the event list, NOADD_DROP_OVERFLOW2
  decremented by its event count, named, and counted exactly once in
  NOADD_DROP_OVERFLOW (closes B-FU7-2).
- **R8e:** new subjects get lifetime bookkeeping; documented residual
  boundaries if the lifetime lists themselves fill (128 distinct
  overflow subjects with clear cycles; 48 distinct event subjects).
- **R8f:** invariant: a subject is in at most one lifetime list at a
  time; each distinct subject contributes exactly once to exactly
  one tier, lifetime.
- **R8g:** PART I tests (I-T1..I-T4). PART A-H untouched.
  `noadd_vote_lost` and both NOTE wordings unchanged (the NOTE text
  "distinct subject(s) beyond name capacity" is now genuinely true).

## Frozen kill bars vs observed

- **K-FU8-1 (same-tier double count closed):** exact X-FU7-2/B2b
  replay. Observed: total=129, overflow=64 (not 65), ov2=0,
  vote_lost(e1)=1, vote_lost(s8)=0, raw contains
  "CONCEPT-MERGE 1 into 0". PASS.
- **K-FU8-2 (cross-tier double count closed):** exact X-FU7-3/C3b
  replay. Observed: total=130, overflow=65, ov2=0 (not ov2=1),
  vote_lost(h1)=1. PASS.
- **K-FU8-3 (multi-event transfer):** h1 dropped 3x as events
  (total=131, ov=64, ov2=3), g65 cleared, h1 re-dropped. Observed:
  total=132, overflow=65, ov2=0. All three events transferred; h1
  counted once as a distinct subject. PASS.
- **K-FU8-4 (regression):** all 47 existing named checks (PART A
  through PART H) pass unchanged. PASS.
- **K-FU8-5 (determinism):** 3/3 runs byte-identical, md5
  `6ae1d1e5716e09d0a07beb3dee420d68`. PASS.

New test I-T4 (transferred subject re-drop is a no-op): PASS.
Total: **51/51**, zero FAIL, zero VOID, exit code 0.

## Causal interpretation

The red team's two findings shared one root cause: the counters had
no memory of which distinct subjects they had counted, only of
which subjects were currently named. R3 clearing (correctly)
removes a membered subject from the live name lists, but the
counters kept no lifetime identity, so re-admission and
event-to-named promotion double-counted. The repair separates
live definite-loss naming (still clears on membership, so members
are not falsely reported as lost votes) from lifetime
counted-subject identity (never clears). The two tiers are now
mutually exclusive per subject across clear/re-drop cycles.

## Boundaries (residual, documented)

- Beyond 128 distinct overflow-counted subjects with clear cycles,
  the lifetime overflow list fills and a re-admission may recount
  (old behavior returns; the counter is no longer guaranteed
  distinct).
- Beyond 48 distinct event-tier subjects, the event list fills and
  a later event-to-overflow transfer is impossible (the subject
  stays counted as events).
- Both bounds are far above the tested regime (64/64 name lists)
  and fail loudly by construction (documented, not silent).

## Governance disclosures

- Pure Zag throughout: no Python in implementation, fixtures,
  builds, runs, greps, md5, cmp, or diff.
- Prereg `039d6fcaa` committed alone before any implementation
  edit, build, or run. No bar was weakened or altered after
  results.
- Only owned paths staged/committed (pathspec-restricted
  `git add`). No binaries committed (builds in /tmp/fu8 only).
- The single em dash in `unified_fdcr8.zag` (line 1 header comment)
  is pre-existing from the verbatim FU7 copy; zero em dashes added
  by this work.
- Red-team downgrade findings B-FU7-1 and B-FU7-2 are CLOSED at the
  mechanism level by R8c and R8d respectively. H-FDCR-UNIFIED7's
  DOWNGRADED status stands as history; H-FDCR-UNIFIED8 SURVIVES on
  its own frozen bars.

## Evidence

- Raw deterministic output (3/3 byte-identical):
  `FDCR_UNIFIED8_RAW.txt`, md5
  `6ae1d1e5716e09d0a07beb3dee420d68`.
- Source: `unified_fdcr8.zag`.
- Prereg: `PREREG_FDCR_UNIFIED8.md`.
- Toolchain: `znc 2026.07.0-dev (edition 2026)`.
