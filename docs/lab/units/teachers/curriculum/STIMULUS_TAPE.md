# STIMULUS TAPE — shared byte stream + STIMULUS_REF (TST-1 schema v1)

Implements prereg §4 B.4's `STIMULUS_REF` ("shared input by reference") for
Track B. This spec is normative for the harness, the teacher arms, and replay.

## §1 — The shared stimulus

The shared stimulus for one teaching session is **exactly one
slice's bytes, verbatim** — the `slice_bytes` bytes of the slice
named in `STIMULUS_REF`, in corpus order, unmodified. The tape carries these
bytes in its stimulus segment (framing per TST-1's length-prefixed events;
the stimulus segment itself is raw bytes, no escaping).

**§P span offsets are slice-relative**: `span_start`/`span_end` (and every
`aux_spans` / `grounding` span) are byte offsets with 0 = the slice's first
byte. Rationale (declared operationalization of an under-specified prereg
point): tapes are self-contained — replay needs the tape alone, never the
full corpus — and flaw/manifest coordinates stay valid across scale legs.

## §2 — STIMULUS_REF event (little-endian, length-prefixed per TST-1 framing)

| field | type | value |
|-------|------|-------|
| slice_id_len | u8 | length of slice_id |
| slice_id | bytes | e.g. `SHK-256K-0003` (ASCII) |
| corpus | u8 | 1 = shakespeare, 2 = sqlite |
| corpus_sha256 | 32 bytes | full corpus file SHA-256 (binds slice to corpus; pins in PROVENANCE.md) |
| byte_start | u64 | slice start offset in the corpus file |
| byte_end | u64 | slice end offset (exclusive) |
| slice_sha256 | 32 bytes | SHA-256 of exactly the stimulus bytes |
| inventory_sha256 | 32 bytes | G-V1 inventory hash for this slice |
| slice_bytes | u64 | == byte_end − byte_start (the size leg S) |
| size_leg | u8 | 1 = 64K, 2 = 256K, 3 = 1M |
| scale_leg | u8 | 1 = 1x, 2 = 10x |
| rep_index | u8 | 0 at 1x; 0..9 at 10x |
| held_out_start | u64 | the 90% boundary; invariant: `byte_end ≤ held_out_start` |
| flaw_slot_count | u8 | 12 (frozen, T-3) |

## §3 — Harness verification (declared, mandatory)

Before a session starts **and** before a replay:

1. `SHA-256(stimulus segment bytes) == slice_sha256`, else abort
   (`STIMULUS_MISMATCH` — the tape does not describe its own stimulus).
2. Recompute the G-V1 inventory hash from the stimulus bytes (deterministic
   procedure, OPERATIONALIZATION.md §2) and compare to `inventory_sha256`,
   else abort. (The committed inventory files are the answer key; this check
   proves the stimulus they were derived from is the stimulus on the tape.)
3. `byte_end ≤ held_out_start`, else abort (held-out exclusion is structural).

These checks make the tape self-certifying: an auditor holding only the tape
and this spec can verify the stimulus is exactly the slice the manifest
describes, without trusting the harness.

## §4 — Content addressing

Slices are content-addressed by SHA-256 throughout: manifests, tapes, and the
flaw-slot maps all key stimulus bytes by `slice_sha256`, never by filename or
path. Two harnesses with the same slice bytes agree on every downstream
artifact (replay rule, B.4: the tape IS the teacher for replay purposes).
