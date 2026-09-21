# Encoder-Collision Forgery: Attacking the Canonical Encoder, Not the Fields (T3 gap-fill g10)

## 1. Slice
T3 gap-fill: canonical-encoder collision forgery — two semantically distinct ledger payloads canonicalizing to identical bytes (or identical bytes decoding to two semantics), so every hash check passes on a forged entry. This attacks the encoder layer that `04-ledger-forgery.md` assumes injective.

## 2. Falsifiable claim
At least one encoder-layer collision class — (a) normalization collapse, (b) same-bytes/two-readings under encoder or schema drift, (c) cross-build encoder divergence — lets an attacker commit a ledger entry whose canonical bytes verify under the hash chain while its decoded semantics differ from what was deliberated. The claim dies if a Zag canary harness (injectivity + round-trip + version-tagged decode + cross-build byte-compare over a fixed adversarial corpus) runs with zero collisions, zero round-trip losses, and zero divergence.

## 3. Design
Setup: the slice-15 layout `idx:u32|episode:u32|clock:u64|op:u8|prev_hash:32B|payload|entry_hash:32B` with `entry_hash = SHA256(canonical(payload) || prev_hash)`. Slice 04 attacks FIELDS assuming `canonical()` is injective and stable. I attack `canonical()` itself.

**(a) Normalization collapse (many payloads → one byte string).** Any lossy canonicalization step is a collision oracle: the attacker searches the preimage class of a target byte string for the most favorable semantics. Concrete shapes:
- Case/whitespace folding on a string field: `{op: PIN, target: "Core"}` vs `{op: PIN, target: "core"}` → identical bytes if the encoder folds case. The hash covers bytes the reader never distinguishes.
- Float truncation: strength `0.30000000000000004` vs `0.3` → both `"0.3"` under fixed-precision encoding. Deliberated value and audited value differ; hash green.
- Map key dedup under normalized ordering: `{"Slot A": PIN}` vs `{"slot a": KILL}` — if the encoder normalizes keys to sort them, both collapse to one entry and the surviving value is encoder-defined. Semantics silently rewritten.
- End-to-end walkthrough: deliberation records `{op: PIN, target: "Core"}` and commits `entry_hash = SHA256(canonical(payload) || prev_hash)`. The attacker later rewrites the payload bytes to `{op: PIN, target: "core"}` and rebuilds the chain forward. Every hash check passes — the bytes are exactly what the encoder would have produced — but the trail now attests a pin on "core" while the system acted on "Core". No field was smuggled past a check; the encoder erased the distinction the check would have needed.

**(b) Same bytes, two readings (decoder divergence).** Bytes B are fixed and hash-verified, but `decode(B)` depends on reader version:
- Union/tag drift: tag byte `0x02` = DEMOTE in encoder v1, KILL in v2 after the tag table is reordered. Ledger bytes unchanged, chain intact, a v2 auditor reads a kill where v1 wrote a demote.
- Field-width drift: a length prefix read as u16 by one build and u32 by another shifts every downstream field boundary. Slice 04's own warning applies: never assume offsets — but the parser itself must be pinned, parsing alone is not sufficient.
- Schema-evolution drift without a version bump: a builder adds an optional field defaulting to zero, and the canonical encoder omits default-valued fields. `{op: KILL, note: ""}` (field absent) vs `{op: KILL, note: <forged>}` (field present but zero-omitted) can canonicalize identically if the omission rule is value-based rather than presence-based. Presence must be encoded, never inferred.

**(c) Cross-build encoder divergence (one payload → many byte strings).** Same payload, different canonical bytes across builds: struct padding/field-order differences between znc versions, endianness of length prefixes, `[]u8` length-prefix width. Effect: byte-identical replay — the program's proof surface (PROGRAM_BRIEF law 2) — fails across builds; worse, a build-Y auditor recomputing different canonical bytes either false-rejects (denial of audit) or falls back to trusting stored bytes, letting 04's field checks run on attacker-favorable bytes. Not hypothetical: znc has a documented hot-path miscompile (ZNC-2026-09-19-001), arm64 syscall-lowering dropping the syscall number, and the 2^25 slice-indexing limit — the toolchain is proven capable of silently changing what bytes a program produces. Note the asymmetry with 04: field forgeries need the attacker to rewrite the chain; encoder collisions and divergences need only the encoder to be lossy or the build to differ — no chain rewrite required.

**Defense/test: the canonicalization canary.** A Zag test harness, separate from every AI decision path; corpus fixed and versioned, zero RNG anywhere:
1. Adversarial corpus C (checked in): string edge cases (case pairs, leading/trailing/zero-width whitespace, NFC/NFD pairs, empty vs blank), float boundary pairs (`0.1+0.2` vs `0.3`, `-0.0` vs `+0.0`, precision neighbors), map key near-collisions, every union variant, max-length and empty fields. Deterministic expansion: mutate each field of each item through its fixed edge-value list → pair set P of semantically distinct payloads.
2. Injectivity: for all distinct `(x,y)` in P, assert `canonical(x) != canonical(y)`. Any equality is a found collision.
3. Round-trip: for all x in C, assert `decode(canonical(x)) == x` semantically. Lossy normalization fails here first.
4. Version-tagged decode: the ledger header pins `ENCODER_ID = SHA256(encoder source || schema definition)`; `decode()` takes `(bytes, encoder_id)` and rejects unknown ids. Same-bytes/two-readings then requires a second pinned id, and adding one is a rule change needing Micah's dated re-approval.
5. Cross-build byte-compare: build the encoder on every supported target (x86_64/arm64 × znc versions in use); byte-compare `canonical(C)` across all builds; any divergence fails the build. The pinned ENCODER_ID in step 4 must cover the exact znc version and target triple, not just the encoder source — otherwise two "same-source" builds silently diverge and step 4's pinning is theater.

```zag
fn canary(corpus: []Payload, enc: Encoder) -> CanaryReport {
    // injectivity over deterministically expanded pairs (no RNG)
    let pairs: []Pair = expand_pairs(corpus);
    for p in pairs {
        if enc.canon(p.a) == enc.canon(p.b) { return fail("COLLISION", p); }
    }
    // round-trip: canonicalization must be information-preserving
    for x in corpus {
        if !sem_equal(enc.decode(enc.canon(x)), x) { return fail("LOSSY", x); }
    }
    // decoder pinning: unknown encoder ids rejected
    if enc.id() != LEDGER_PINNED_ENCODER_ID { return fail("UNPINNED_ENCODER"); }
    return pass();
}
// cross-build gate (CI): for each target t, bytes_t = canon_all(corpus); assert all bytes_t equal.
```
6. Negative control: the canary must be validated against a deliberately broken encoder (case-folding string fields, 6-digit float truncation, value-based field omission) and MUST fire on it. A canary that passes a broken encoder is theater — the harness is only trusted after it has killed at least one planted collision of each class (a), (b), and (c).

## 4. Kill bar
Red-team claim dies if the Zag canary — injectivity over ≥500 deterministically expanded distinct-semantic pairs, round-trip over the full versioned corpus, decoder rejection of all unpinned encoder ids, cross-build byte-compare clean on ≥2 targets — reports zero collisions, zero round-trip losses, zero divergence. Blue-team (encoder) kill, prereg-style: ANY single colliding distinct-semantic pair, any round-trip loss, any unpinned-id acceptance, or any cross-build byte divergence = encoder REJECTED; no ledger entries may be committed under it and the Arm C trial does not proceed on that encoder. Fires once; no threshold, no averaging. A fired kill is itself recorded as a ledger GATE_EVENT under the pinned encoder — the rejection of a bad encoder must be as auditable as the entries it would have produced.

## 5. Honesty notes
Weakest point is corpus completeness: injectivity over a finite corpus does not prove injectivity over the schema — the canary is only as adversarial as its author, and the Unicode/float edge spaces are effectively infinite, so this is a tripwire, not a proof. The deterministic pair expansion in §3 is a deliberate choice: it keeps the harness inside the no-RNG law, at the cost of never surprising itself — a fenced, seeded adversarial generator (fixed seed, checked-in output) would widen coverage without putting randomness in any decision path, and is worth considering once the baseline canary passes. Same-bytes/two-readings is bounded by known reader versions; a deliberately malicious encoder (supply chain) is out of scope — under the RC architecture TNN holds 0% of ledger rules, so the constitution side must authenticate the encoder build. Cross-build testing covers only builds actually run. I am NOT claiming the SHA256 chain is broken (it is not — 04's analysis stands), NOT covering field-layer forgeries (04's territory: forced_flag, stale selector_hash, table swap), and NOT claiming this replaces 04's per-choice-point re-derivation fix, which still needs its own build. Evidence leaned on: `wave5/ledger-gating/` (ledger as proof surface), slice 04 of `wave11/t3-integrity-redteam/findings/`, PROGRAM_BRIEF laws 1–2.

## 6. Next build step
Build the minimal canonical encoder for the slice-15 entry layout in Zag plus the versioned adversarial corpus and the injectivity + round-trip canary, and run it before any ledger entry is committed or any Arm C trial harness wires the selector in: if the canary finds even one collision or round-trip loss, the encoder spec is not trial-ready — and every field-layer defense in 04 would be guarding bytes that can lie.
Concretely: encoder v0 covers exactly the slice-15 field types (u8/u16/u32/u64, 32B hashes, length-prefixed byte strings, the op enum); the corpus ships with ≥40 hand-built adversarial pairs plus the deterministic edge-value expansion; the CI job runs the canary and the cross-build byte-compare on every commit touching the encoder.
Success looks like: a boring encoder — fixed field order, no normalization, presence-encoded optionals, pinned id — that the canary cannot break.
