# ARM SPEC — T: Episode-aligned chunks

## Authority
1. `units/arms/briefs/T.json` (authoritative)
2. Frozen row (2026-09-21 verbatim):
   > `| T — Episode-aligned chunks | STRUCT | Mechanism: Chunks = episodes; segmentation follows the episode clock (τ quiescence gap). | Binding kill criterion: Any one: (i) B2 within 2× of X's on either corpus; (ii) >80% of battery recall queries address sub-episode spans (the "unit of experience" claim falsified); (iii) determinism gate fails; (iv) floor rule fires. |`
3. `units/ALPHABET_S-X.md` (episode definition)

## Mechanism
- **Chunks = episodes.** Segmentation follows the episode clock (τ quiescence gap).
- **Episode**: maximal byte span ingested under one continuous ingestion intent.
- **Episode opens** on: (i) audited `EPISODE_BEGIN`, (ii) quiescence gap > τ, (iii) source/file/socket/session switch.
- **τ = 1,000,000 μs** (1 second). Frozen, judgment-set, not tuned.
- **Episode is chunk scope.** Sub-episode recall uses `(episode_id, start, len)`.
- **IDs stable**; killed episodes tombstone (never reuse ID).
- **Whole-file ingest** = one continuous intent = one episode (0% boundary by design; X precedent for whole-file-blob arms).

## Implementation (struct-free)
- znc compiler bugs force struct-free design:
  - `let s:StructType;` requires aggregate initializer (no working literal syntax)
  - Function signatures with spaces fail: `fn f(s:[]u8)[]u8` works, `fn f(s: []u8) []u8` fails
  - `@import` breaks `.len` in main file (treated as "dead computation")
- Workaround: inline substrate functions, use `_zag_print` (not `print`), substrate-style signatures.
- Each mode allocates local arrays; helpers take explicit parameters.
- Episode table: parallel []u8 arrays (eid, base, len) with iput32/iget32.

## M-Harness Mapping
- **M1**: 1 episode, 0 boundaries (by design). Prose: 5,638,480 bytes. Code: 9,515,341 bytes.
- **M2**: 1000 recalls via (episode_id=1,start,len), 1000 hits.
- **M3**: 4000 episodes (fresh intents), IDs 1..4000, all verified.
- **M4**: Defect injected (byte flip), detected via recall, repaired, re-verified.
- **M5**: Table 48,000 bytes + data 6,086,480 bytes = 6,134,480 total.
- **M6**: Episode 1 tombstoned, episode 2 alive, ID 1 never reused.
- **M7**: Re-ingest creates 2 episodes, distinct IDs, same content length.
- **M8**: Determinism — M1+M3 sequence byte-identical across 10 runs.
- **M9**: N/A (learning-curve shape; T is STRUCT, not learning arm).

## Kill Criteria Status
- (i) B2 within 2× of X: **UNRESOLVED** (no B-battery evidence; M modes do not establish B2)
- (ii) >80% sub-episode queries: **UNRESOLVED** (refers to B-battery; M2 uses sub-episode spans by design for ID-arm recall)
- (iii) Determinism gate fails: **NOT FIRED** (M8 10x byte-identical)
- (iv) Floor rule (B2/B4/B5/B9 vs X): **UNRESOLVED** (no X B-battery evidence)

## Ambiguities (from harness/AMBIGUITIES.md)
- **A7**: M7 C′ edit bytes proposed, not frozen. Using literal re-ingest.
- **A8**: 5,000 lookup schedule proposed, not frozen. M2 uses 1000 recalls.
- **A15**: ID-arm M1 swap procedure proposed, not frozen. M1 reports 0 boundaries by design.
- **A17**: M8 combined M1+M3 vs separate unresolved. Using combined (validator interpretation).

## Verdict
**PASS** — Arm builds, all M1-M8 modes pass, M8 determinism holds 10x. No binding kill criterion fires with available evidence. B-battery criteria (i), (ii), (iv) unresolved pending Crew-4 B-battery/X evidence.
