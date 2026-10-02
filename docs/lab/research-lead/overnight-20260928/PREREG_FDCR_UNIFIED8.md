# PREREG H-FDCR-UNIFIED8: Lifetime Per-Distinct-Subject Overflow Counters

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED8 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED7 SURVIVES (47/47). Prereg `855322a77`,
  Amendment 1 `42cbe6396`, result `18dd712a3`. Red team DOWNGRADED
  (2 downgrade findings, no kill): X-FU7-2/B2b (same-tier double
  count) and X-FU7-3/C3b (cross-tier double count).
**Hypothesis:** Both downgrade findings close at the mechanism level
  with lifetime per-distinct-subject tracking. NOADD_DROP_OVERFLOW
  then genuinely counts distinct subjects dropped beyond the 64-name
  capacity (lifetime), and the two tiers stay mutually exclusive: each
  distinct subject contributes exactly once to exactly one tier.

## The downgrade findings (from X-FU7 red team, FU7_ADV_RESULT.md)

- **B-FU7-1 (same-tier double count, X-FU7-2/B2b):** A subject
  overflow-named, then membered and R3-cleared, then re-recorded via
  the merge path (`con_merge_into` -> `noadd_record` -> NOADD table
  full -> `noadd_drop_record`), is re-admitted to the freed
  overflow-name slot and re-increments NOADD_DROP_OVERFLOW. 65
  increments for 64 distinct subjects. The counter counts
  overflow-name admissions, not distinct subjects.
- **B-FU7-2 (cross-tier double count, X-FU7-3/C3b):** A subject whose
  drop incremented only the event tier (both name lists full), later
  re-dropped after a clear freed an overflow slot, is named and
  counted in the overflow tier while its event-tier increment
  persists. The subject is counted in both tiers at once.

## Repairs (frozen)

**R8a: Lifetime overflow-counted subject list.**
New memory: NOADD_DROP_OVL=3192 (128 entries of 4-byte subject string
offsets; ends 3704). Records every subject ever counted in
NOADD_DROP_OVERFLOW, by string offset. Strings are append-only
(`con_intern` only advances ST_STR), so offsets are stable for the
world lifetime. `noadd_drop_init` zeroes the list. The 3192..4095
region is verified free (only the FU7 memory-map comment mentions
it; WORK=4096 is a size constant, not a scratch user).

**R8b: Lifetime event-tier subject list.**
New memory: NOADD_DROP_EVL=3704 (48 entries of 8 bytes: subject
string offset + that subject's event count; ends 4088). Records
subjects whose drops incremented NOADD_DROP_OVERFLOW2. Free:
4088..4095 (8 bytes).

**R8c: Re-admission without re-count (closes B-FU7-1).**
In `noadd_drop_record`, after the existing main-list and
overflow-name-list content dedups: if the subject content is in the
lifetime overflow list (previously counted, cleared via R3, now
re-admitted): if a free overflow-name slot exists, restore the name
entry but do NOT increment NOADD_DROP_OVERFLOW; if no free slot,
return without incrementing NOADD_DROP_OVERFLOW2 either (the subject
is already counted in the overflow tier; the total-events counter
still records the event).

**R8d: Event-to-overflow transfer (closes B-FU7-2).**
In `noadd_drop_record`, if the subject content is in the lifetime
event list: if a free overflow-name slot exists, remove it from the
event list, decrement NOADD_DROP_OVERFLOW2 by its recorded event
count, add it to the lifetime overflow list, name it in the overflow
list, and increment NOADD_DROP_OVERFLOW exactly once. If no free
slot, increment its event count and NOADD_DROP_OVERFLOW2 (unchanged
behavior).

**R8e: New distinct subjects and documented fallbacks.**
A newly overflow-named subject is added to the lifetime overflow
list; a new event-tier subject is added to the lifetime event list
with count 1. If the lifetime overflow list is full (beyond 128
distinct overflow subjects with clear cycles), the counter
increments without lifetime tracking (old behavior; documented
residual boundary). If the lifetime event list is full (beyond 48
distinct event subjects), the event counter increments without
tracking (transfer impossible later; documented residual boundary).

**R8f: Invariant.**
A subject is in at most one lifetime list at a time: transfer moves
it from the event list to the overflow list; re-admission never adds
to the event list. Each distinct subject therefore contributes
exactly once to exactly one tier, lifetime.

**R8g: PART I tests** (I-T1..I-T4) appended after PART H. PART H and
earlier tests untouched. `noadd_vote_lost` and both NOTE wordings
unchanged (the NOTE text "distinct subject(s) beyond name capacity"
becomes genuinely true).

## Frozen kill bars

**K-FU8-1 (same-tier double count closed):** Exact replay of the
X-FU7-2/B2b adversary fixture: `fu7_pet40_world`, teach f1..f64 then
e1..e64 (total=128, ov=64, ov2=0); `T e1 | is_a | animal` members e1
(cleared: vote_lost(e1)=0, total=128, ov=64); `T e1 | is_a | pet`
extends animal to 2 features (no drop); `T s1 | is_a | animal`
extends pet, firing `con_merge_into(pet, animal)` ("CONCEPT-MERGE 1
into 0"), pet full so e1 is merge-overflow re-recorded.
Requires: total=129, noadd_drop_overflow()==64 (NOT 65),
noadd_vote_lost("e1")==1, noadd_vote_lost("s8")==0, raw contains
"CONCEPT-MERGE 1 into 0". (Under FU7: overflow==65.)

**K-FU8-2 (cross-tier double count closed):** Exact replay of the
X-FU7-3/C3b adversary fixture: `fu7_pet40_world`, teach g1..g128
(total=128, ov=64, ov2=0); `T h1 | is_a | pet` (total=129, ov=64,
ov2=1, vote_lost(h1)=0); `T g65 | is_a | animal` members g65
(cleared: vote_lost(g65)=0); `T h1 | is_a | pet` re-drop.
Requires: total=130, noadd_drop_overflow()==65,
noadd_drop_overflow2()==0 (NOT ov=65 AND ov2=1),
noadd_vote_lost("h1")==1. (Under FU7: ov==65, ov2==1.)

**K-FU8-3 (multi-event transfer):** `fu7_pet40_world`, teach g1..g128
(total=128, ov=64, ov2=0); `T h1 | is_a | pet` three times
(total=131, ov=64, ov2=3); `T g65 | is_a | animal` members g65
(cleared); `T h1 | is_a | pet` re-drop.
Requires: total=132, noadd_drop_overflow()==65,
noadd_drop_overflow2()==0 (all 3 events transferred; h1 counted
once as a distinct subject).

**K-FU8-4 (regression):** All 47 existing named checks (PART A
through PART H, G-T1..G-T2, H-T1..H-T5) pass unchanged. Rationale:
the repair only activates on clear+re-record cycles (R8c) and
event-to-named transfers (R8d); no existing test exercises either
path (H-T4's cleared subject x is main-named, never overflow- or
event-counted, and is never re-dropped).

**K-FU8-5 (determinism):** Every new fixture run 3/3 byte-identical.

Verdict rule: all of K-FU8-1..K-FU8-5 PASS -> SURVIVES; any FAIL ->
KILLED (the repair claims to close the findings, so a failure is a
kill, not a downgrade).

## Governance

- This prereg is committed ALONE before any implementation edit,
  build, or run.
- Pure Zag throughout: fixtures, implementation, builds, runs,
  greps, md5, cmp, diff. Zero Python at any stage.
- `unified_fdcr8.zag` = `unified_fdcr7.zag` (result `18dd712a3`)
  copied verbatim (cmp-verified) plus exactly the frozen R8a-R8g
  changes. `unified_fdcr7.zag` untouched.
- Only owned paths staged/committed (pathspec-restricted).
- No binaries committed (builds in /tmp/fu8 only).
- No em dashes in loop documentation (byte-verified).
