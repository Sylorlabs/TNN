# AMENDMENT_2026-09-20_schema — dated schema amendments (step 1b)

**Date:** 2026-09-20. **Status:** PROPOSED — pending Micah's re-approval per
program law (rule changes need re-approval) and overseer-channel review.
Filed per PREREG_STATE_SCHEMA.md §9 (amendment process, 16 §3c). The build in
this step implements the amended schema; if Micah rejects, the build is
reverted to the frozen prereg text and re-run.

## Amendment A — H.cid: hypothesis creation id logged (schema correction)

**What:** each hypothesis record gains `H[j].cid : u64` (creation id,
monotonic, never reused). Schema v1 layout: H block becomes
16 × (cid, status, ev1, ev2, verdict_ep) = 640 bytes at offset 1224;
total STATE_E v1 = **2432 bytes** (was 2304); logged field count **273**
(was 257). All downstream offsets shift accordingly (see s1b_codec.zag,
which is authoritative).

**Why:** the frozen prereg (§1.2) requires creation ids "monotonic u32, never
reused" and the evolution law (§3 rule 3) eliminates the "smallest-id live"
hypothesis — but the frozen §2 table serialized no creation id, making the
never-reused invariant and the tie-break rule uncheckable from the record.
A schema that cannot check its own law is a logging gap (Class A by the
step's own taxonomy). This is a genuine prereg-intended variable (it was
enumerated in §1.2), not a post-hoc patch — the 25/K1 reprieve-clause guard
is satisfied.

**Retroactive re-validation:** the full evidence suite (replay 1000/1000 ×2
build hashes, perm 600/600, difftest, conform) was run against the amended
schema; the frozen-prereg legs predate the build (no prior approved legs
exist for step 1b — the prereg was committed before any code), so there is
nothing to re-run. FIELD_COUNT,273 is asserted in every transcript.

## Amendment B — K.rctr: refinement-round counter logged (schema v2)

**What:** `K.rctr : u64` appended at offset 2432; schema v2 (0x02) total =
**2440 bytes**; logged field count **274**. Decoder rejects unknown versions.

**Why:** this is the §1.11 planned discovery amendment. The v1 schema
deliberately left K.rctr unlogged as the planted missing variable for the
differential-replay experiment (16 §6). The experiment exposed it in all 5
batches (first alarms at pairs 7/10/13/16/19 of 460; hunt FOUND rctr 5/5;
16-K1 did NOT fire — see run_difftest.txt). Per 16 §3c, the discovered
variable is now added to the schema by dated amendment.

**Retroactive re-validation (16 §3c):** the prior approved legs were re-run
with the expanded S: the full replay suite under v2 = **1000/1000**
(run_diffk2.txt), and the differential-replay sweep under v2 shows **0
alarms** across 5×460 pairs (divergence now attributable to the logged
rctr difference — 16-K2 did NOT fire). Old results reproduce
byte-identically under the expanded schema (v1 transcripts are unchanged;
v2 adds only the rctr field).

## Review checklist for Micah
- [ ] Amendment A (H.cid) approved as a genuine prereg-intended variable
- [ ] Amendment B (K.rctr) approved post-discovery
- [ ] v1 = 2432 B / 273 fields, v2 = 2440 B / 274 fields accepted as the
      K5 (arbitrariness) measurement basis going forward
