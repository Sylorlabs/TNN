# T — Episode-aligned chunks: Implementation Notes

## Design (struct-free)

The Zag compiler (znc) does not support `let s: StructType;` without an
initializer ("aggregate let needs an aggregate initializer"), and struct
literal syntax causes parse errors. The implementation therefore avoids
structs entirely.

Instead of a TEP struct, each mode function allocates its own local arrays:
- Episode table: five parallel []u8 arrays (eid, ebase, elen, ecorp, eflags),
  each cap*4 bytes, accessed via iput/iget.
- Metadata (n_ep, next_eid, etc.) as local i32 variables.
- Corpus buffers as local []u8.

Helper functions take explicit array parameters instead of *TEP.

## Episode model (from T.json and ALPHABET_S-X.md)

- Episode = maximal byte span ingested under one continuous ingestion intent.
- Opens on: (i) explicit audited EPISODE_BEGIN, (ii) quiescence gap > τ,
  (iii) source/file/socket/session switch.
- τ = 1,000,000 μs (1 second), frozen, judgment-set, not tuned.
- Episode is the chunk scope. Sub-episode recall is (episode_id, start, len).
- IDs stable; killed episodes tombstone (never reuse ID).

## M-harness mapping (literal reading, ambiguities logged)

- M1 (boundary): Whole-file ingest = one intent = one episode => 0%
  boundary by design (X precedent for whole-file-blob arms).
- M2 (recall): Episodes recalled by ID; (episode_id, start, len) for
  sub-episode spans.
- M3 (4000 slots): 4000 fresh ingest intents => 4000 episodes.
- M4/M6 (defects/revisions): Defects are byte-level; revisions create new
  episode IDs (tombstone old).
- M5 (memory): RSS + table bytes.
- M7 (reuse): Re-ingest creates new episodes (IDs stable, content may dedup).
- M8 (determinism): Byte-identical reruns required.

## Kill criteria (binding, from frozen row)

Any one kills:
(i) B2 within 2× of X's on either corpus;
(ii) >80% of battery recall queries address sub-episode spans;
(iii) determinism gate fails;
(iv) floor rule fires (S–W must beat X on B2, B4, B5, B9).

Note: B2/B4/B5/B9 are Crew-4 B-battery metrics, not M1–M9. The M harness
does not provide them. Criteria (i), (ii), (iv) cannot be determined from
M modes alone and are reported as UNRESOLVED unless frozen B-battery
evidence exists.
