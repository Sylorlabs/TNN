# Ledger Invariance Under Expression Variation (Track 1, Slice 15)

## Slice
Track 1, slice 15: design ledger canonicalization under expression variation.

## Falsifiable claim
For any two runs fed identical (input, full logged state), differing only in forced
expression-variant selection, the canonical ledger is byte-identical in every field except
the `variant_id` field of the `VARIATION_CHOICE` entry; and any run replayed from
(input, logged full state) with no forced override reproduces the ENTIRE ledger
byte-identically, including the `VARIATION_CHOICE` entries. Kill if either fails.

## Design

**1. Canonical entry layout (16-word-inspired, fixed binary).** Every ledger entry is:
`idx:u32 | episode:u32 | clock:u64 | op:u8 | prev_hash:32B | payload:CANON | entry_hash:32B`
where `entry_hash = SHA256(prev_hash || canonical(idx||episode||clock||op||payload))`.
`payload` is a length-prefixed, key-sorted canonical encoding: keys are lexicographic,
integers big-endian, enums are u8 codes, hashes are raw 32B, strings (where permitted)
are length-prefried UTF-8. No maps with free ordering, no floats, no timestamps of
wall-clock time — only the deterministic `clock` tick counter. Integers and hashes only;
free text is banned outside a whitelist below.

**2. What is LOGGED (the invariant set).**
- `VERDICT` — verdict code enum (e.g. `CONFIRMED/REFUTED/UNDECIDED`), the rule-set version
  id, the evidence slot-ids it rested on. The prose explanation is NOT logged.
- `MEMORY_OP` — op enum (`ADD/KILL/PIN/PROMOTE/DEMOTE/STRENGTHEN/WEAKEN`), slot id,
  citation episode(s), acting authority (`TNN` vs `TRAINER_FORCE_PIN` + trainer id hash).
- `REFUSAL` — refusal code enum, violated rule id, hash of the triggering input block,
  the alternative action taken (enum, e.g. `HOLD/ESCALATE/ROLLBACK`).
- `STATE_HASH` — every K episodes (prereg: K=1 during trial): SHA256 of the canonical
  full-state snapshot per the Track-1 prereg state enumeration. Reproducibility anchor.
- `VARIATION_CHOICE` — `variant_id` (u16 index into the preregistered expression-variant
  table), `selector_hash` = SHA256(canonical of the state-feature vector that drove the
  choice), `policy_version` id, `forced_flag` (0 = lawful, 1 = test-harness override).
  The choice is deterministic and auditable, never hidden — but the surface phrasing it
  produced is not in the ledger at all.
- `GATE_EVENT` — staged-autonomy gate transitions (from MA1, 58/58: already ledgered;
  unchanged semantics, only now canonicalized under this layout).

**3. What is EXCLUDED (the variant set).**
- Surface phrasing/wording of any output, verdict explanation, or refusal message.
- Ordering of presented items: the ledger stores claim *sets* (canonically sorted);
  a presented order is a variation choice, logged as `VARIATION_CHOICE`, never as ledger
  content order.
- Elaboration depth: the content claim set is logged; the depth/rendering profile is a
  `VARIATION_CHOICE` (`variant_id`).
- Path taken to a conclusion: intermediate scratch reasoning is not ledgered; only the
  verdict + evidence refs + the variation choices made along the way.

**4. Replay check.** The replay harness takes (input, logged full state), re-executes,
recomputes `entry_hash` per entry, and byte-compares the full entry stream against the
recorded ledger. Pass = zero differing bytes. `STATE_HASH` entries let the harness
pinpoint the first divergent episode. A second harness mode forces a different
`variant_id` at chosen `VARIATION_CHOICE` points (`forced_flag=1`): the resulting ledger
must be byte-identical to the original in all fields except those `variant_id` fields.
Any other byte difference = invariance broken.

**5. Logging the variation decision itself.** The expression-variant table is preregistered
(policy version id). The selector is a pure function of (input hash, full-state hash):
no RNG, no hidden inputs. The `VARIATION_CHOICE` entry records the variant id AND the
`selector_hash` so an auditor can recompute: given logged state, the selector MUST
re-derive the same `variant_id` (this is the determinism proof; a mismatch is a
replay failure, not a ledger failure). Surface strings never enter `payload`.

## Kill bar
Preregistered: 200 paired runs (same input + logged state, forced differing variant).
Kill if ANY pair's ledgers differ in ANY byte outside the `variant_id` fields of their
`VARIATION_CHOICE` entries. Kill if ANY no-override replay of the 200 diverges by a
single byte. Kill if a byte-scan of any ledger finds free-text phrasing outside the
whitelisted fields (i.e., anything in `payload` that is not an enum, id, hash, or
length-prefixed canonical key). Kill if any `VARIATION_CHOICE` fails the
recompute-from-state check (selector hash does not re-derive the variant).

## Honesty notes
Weakest point: this design proves the ledger is invariant, not that the *excluded*
variation is harmless — a variant could legitimately omit a claim the auditor expected.
Mitigation is partial: the content claim *set* is logged, so omission is detectable as
a verdict/content divergence in a later audit, but this slice does not settle whether
elaboration depth can hide material content — that is a Track-1 sibling slice's problem
(content-vs-expression boundary). I am NOT claiming canonicalization is free: per-entry
SHA256 chaining and canonical key-sorting add per-entry overhead; at 1000x episode
targets (RC3 reached 100x) the ledger dominates I/O unless chunked (toolchain limit:
no slice > 2^25 bytes — chunked ledgers with hash-linked chunks, per validated
workaround). The `forced_flag=1` mode is a test-harness escape hatch: it must be
unavailable to TNN itself (constitution side, RC architecture: TNN controls reasoning,
0% of the ledger rules) or the ledger becomes self-editable. Integrity load-bearing
stays as established: eliminative verification and deliberative standards prevent
cheating; the ledger only proves (wave5/6 evidence, `docs/lab/wave5/`,
`docs/lab/wave6/`).

## Next build step
Build the canonical encoder + replay checker in Zag (one binary: encode, hash-chain,
verify, forced-variant mode) and run the 200-pair kill test on a minimal TNN harness
with two preregistered expression variants (e.g. terse vs elaborated rendering) over
a fixed (input, state) corpus: establish the byte-identical baseline before any
expression-variant selector is wired into the live system.
