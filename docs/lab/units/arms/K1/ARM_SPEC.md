# ARM K1 — Full SHA-256 Identity: Specification

**Date:** 2026-09-21
**Implementer:** Track A crew K1
**Status:** Implementation complete; 1× battery in progress

## 0. Authority (corrections acknowledged)

1. **2026-09-21:** The phrase "random stable IDs" was wrong and is void. K1 is **Full SHA-256 identity**.
   The ID of a span is `SHA-256(content)`, computed natively. Equal bytes → equal IDs → deduplication.
2. **2026-09-21:** Prior coordinator paraphrases of this arm are void. Authority is, in order:
   1. `units/arms/briefs/K1.json` (verbatim §3 mechanism + kill criteria),
   2. byte-verified verbatim rows from the frozen documents,
   3. nothing else previously written by the coordinator.
3. The brief was inspected on 2026-09-21 and matched the verbatim row exactly.

## 1. Mechanism (frozen)

**Family:** IDENT.

- `ID(span) = SHA-256(byte content)`, computed with the native substrate
  `R33_NATIVE_SHA256_V2.zag`. No new crypto code.
- The 256-bit digest is stored as `u64[4]` and compared as **four integer words** —
  never slice `==`.
- **Dedup table:** fixed-capacity open-addressing hash table keyed on the digest quad,
  sized at **2× expected unique spans**.
  - On `add`: compute digest, linear-probe deterministically from `digest[0] mod capacity`.
  - Hit → full payload-byte confirmation, then `OP_DEDUP_HIT` (refcount++, audited —
    reuse is visible work, not a silent shortcut); the existing slot is returned.
  - Miss → new record appended.
- Identical spans anywhere — across tilings, streams, time — are **one record**.
- **Collision handling (no randomness):** on digest equality, full bytes are compared
  deterministically (explicit byte loop over the append-only payload store). A true
  digest collision chains by **insertion order** (logged) in a slot-linked list; the ID
  stays the digest, disambiguated by chain position. The chain path is exercised with
  synthetic forced collisions (deterministic vectors, preregistered — not random).
- **Revision:** a revised span's content hashes differently, so its identity **dies by
  definition** — honest, not a bug. Lineage is preserved by
  `OP_REVISE_LINK(old_id → new_id, reason, cite_ep)`; recall follows revision links
  (append-only chain) to the live ID. References never dangle; history is never rewritten.
- **Position-blindness (acknowledged weakness):** "the" at line 10 and "the" at line 10,000
  are one chunk. Role and context come from **links** (occurrence records with
  corpus/offset/role/flags/boundary metadata), never from the ID.

## 2. Segmentation (this implementation)

Whitespace-delimited byte tokens. Separators are bytes `0x09`–`0x0D` and `0x20`
(TAB, LF, VT, FF, CR, SPACE) — matching Python `bytes.split()` behavior.

- Follows the alphabet's repeated-word and isolated-word examples ("the" at line 10 vs
  line 10,000; single-word recall disambiguation).
- Boundary metadata (offset, length, role flags) is recorded per occurrence so
  tokenization is auditable and replayable.
- *Note:* the frozen brief does not name a segmentation; this choice is documented here
  as an implementation decision, not a frozen rule.

## 3. Opcodes

Frozen audit namespace `0x01`–`0x13` per `ARM_INTERFACE.md` §6, plus K1-local extensions
(the frozen K1 mechanism text mandates both; the opcode namespace reservation is
reported as an ambiguity in §7):

| Opcode | Value | Meaning |
|---|---|---|
| `OP_DEDUP_HIT` | 20 | Repeat span: refcount++, existing slot returned |
| `OP_REVISE_LINK` | 21 | Append-only `old_id → new_id` revision link |

Audit entries are 16 little-endian u32 words; `stage@52 = 1`, `d1@56`, `d2@60`.

## 4. Storage architecture (build notes)

- **Chunked fixed-capacity stores** (no slice may exceed 2^25 bytes — znc toolchain limit):
  - Table: 96-byte entries, 131,072 entries/chunk, ≤ 8 chunks.
  - Payload: append-only, 16 MiB/chunk, ≤ 4 chunks.
  - Occurrences: 64-byte entries, 480,000 entries/chunk, ≤ 8 chunks.
  - Ledger: 64-byte entries, 524,288 entries/chunk, ≤ 8 chunks.
- Chunking preserves logical semantics; equivalence is proven by byte-identical reruns.
- Payload store is append-only. Revision links are append-only.
- Allocation trace records operation kinds and sizes only (never addresses).

## 5. Trial modes (this binary, `argv[1]`)

| Mode | Trial | Corpus |
|---|---|---|
| `m1-1x-prose` / `m1-1x-code` | M1 span recall | prose.bin / code.bin |
| `m2-t1-prose` / `m2-t1-code` | M2 transfer T1 | t1_prose.bin / t1_code.bin |
| `m2-t2-prose` / `m2-t2-code` | M2 transfer T2 | t2_prose.bin / t2_code.bin |
| `m2-t3-1x` | M2 transfer T3 | t3.bin |
| `m3-1x` | M3 churn | prose+code+churn_fresh |
| `m4-1x-prose` / `m4-1x-code` | M4 defect repair | prose.bin / code.bin |
| `m5-baseline` / `m5-1x` | M5 resource pressure | prose+churn_fresh |
| `m6-p2c-1x` / `m6-c2p-1x` | M6 transfer p2c/c2p | prose.bin / code.bin |
| `m7-1x` | M7 adversarial probe | prose.bin |
| `m8-1x` | M8 combined M1+M3 | prose+code+churn_fresh |
| `k1-dedup-1x` | Kill (i): payload savings vs sequential IDs | all r1 corpora |
| `k1-chain-1x` | Kill (ii): revision chain length + latency | synthetic 100-batch schedule |
| `k1-role-1x` | Kill (iii): wrong-role recall rate | synthetic role fixture |
| `k1-selftest` | 9 mechanism self-checks | synthetic |

Every mode emits: human-readable `M<n>,...` lines, then **one compact JSON metrics object**
(`schema: "metrics-v1"`) as the final line.

## 6. Kill criteria (frozen — any one kills K1)

1. **Dedup failure:** payload savings < 15% on corpus A vs sequential IDs at equal recall
   accuracy → the caching claim dies. Measured by `k1-dedup-1x`.
2. **Churn swamp:** on corpus C, mean revision-link chain length > 8 **and** recall latency
   > 2× the no-revision baseline → the revision-link mechanism dies. Measured by `k1-chain-1x`.
3. **Disambiguation failure:** > 5% of single-span recalls return a contextually wrong
   occurrence (right bytes, wrong role) → K1 dies as a **standalone** scheme (survives only
   as a K3 component). Measured by `k1-role-1x`.

If any fires: issue a public death certificate immediately; do not soften it.

## 7. Ambiguities (reported, not resolved unilaterally)

1. **Corpus A/B/C mapping.** The frozen brief names corpora A, B, C; the harness provides
   `prose.bin`, `code.bin`, `t1_*`, `t2_*`, `t3.bin`, `churn_fresh.bin`. Working mapping:
   A = prose (+code for the code leg), C ≈ churn schedule. The exact authoritative mapping
   and the corpus-C 100-patch schedule were not found; `k1-chain-1x` uses a deterministic
   local 100-batch revision schedule (documented, not authoritative).
2. **Annotated role ground truth.** Kill (iii) requires annotated corpus-A role truth and a
   query schedule; not found. `k1-role-1x` uses a deterministic local role fixture
   (documented, not authoritative).
3. **Opcode namespace.** The frozen opcode list ends at `0x13`; K1's mandated
   `OP_DEDUP_HIT` / `OP_REVISE_LINK` use local values 20/21. No conflict with frozen
   assignments was found, but formal reservation is pending.
4. **Segmentation.** Not named in the frozen brief; whitespace tokens documented in §2.
5. **M4 immutable-content identity.** Whether "immutable content" permits the
   revision-link repair path or demands literal same-ID preservation is unresolved;
   the implementation repairs via revision links (identity dies, lineage preserved).
6. **M8 combined instance.** Follows the M8 validator; the separate-vs-combined
   ambiguity is unresolved and reported.
7. **10× promotion.** Exact 1× replication/promotion bars beyond the general rule not
   found. 10× runs only after 1× bars pass, with approval.

## 8. Determinism & honesty rules (standing)

- Pure Zag. Zero randomness in any decision path. Byte-identical reruns required:
  every 1× leg runs twice; outputs must be byte-identical.
- Real mechanisms, not stubs. Honest failures unchanged.
- An unavailable or failing required run is `ATTEMPTED — FAILED`.
- Frozen kill criteria bind; no appeals.
- No frozen rule/schedule/metric/kill-criterion changes without approval.
- Outcome-changing ambiguity → reported, never silently resolved.

## 9. IO & allocator hazards (build lessons)

- This znc build: casting a slice directly to `i64` does **not** yield its data pointer.
  All raw syscalls use `_zag_slice_ptr(slice) as i64`.
- `nio_free` only what `nio_alloc` / `_zag_i64_to_str` returned. Never free:
  string literals, `_zag_arg` results, `read_bin` sub-slice returns, or any derived slice.
- `_zag_strcmp` returns 1 on equality.
- Never slice-`==` for digest/content comparisons (four-word integer compare; explicit
  byte loops).
- Bare `@import` only. No slice larger than 2^25 bytes (chunk everything).
