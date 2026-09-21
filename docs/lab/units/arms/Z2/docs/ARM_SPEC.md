# Z2 — Contract Chunks: build declaration

Arm: `z2` · Family: ECON · Round: r1 · Scale: 1x
Frozen spec: `units/PREREG_FREEZE.md` §3 row Z2 (commit `b0b9140c0eda`),
brief `units/arms/briefs/Z2.json` (verified byte-identical to the row —
no conflict, no paraphrase used).

## Mechanism (as built)

A chunk is an audited obligation between organs. Every deliberate ingest
issues a CONTRACT carried in the ADD ledger entry's aux fields (the frozen
opcode namespace has no CONTRACT opcode, so the obligation rides in
`a1..a4` — documented here, no namespace change):

- `a1` = consumer restriction mask (1=recall-only, 3=recall|compose,
  5=recall|quote; assigned deterministically as `chunk_index % 3`)
- `a2` = expiry, in ledger-op sequence numbers (deliberate, set at creation,
  visible in the ledger; no wall-clock anywhere)
- `a3` = MA4 value sign (+1/−1, derived deterministically from identity bits;
  stands in for the two organs' agreement and is auditable)
- `a4` = provider obligations bitmask (1 = byte-exact recall)

The contract is mirrored in per-slot arrays (`restr`, `exp`, `vsign`).
A **breach checker runs on the recall hot path** (`z_check`, called by
`z_recall` before any byte is returned): a consumer op outside the chunk's
restrictions, on an expired chunk, or on a tombstoned chunk is **refused
loudly** — REFUSE ledger entry with the reason in `d1`
(201=expired, 202=restriction breach, 203=tombstoned/unknown), nonzero
return, reason out-param. Never silent. Breach handling is preregistered:
refuse + log, never auto-repair.

Storage mechanics underneath are the B-64 grid (fixed 64-byte chunks,
arithmetic IDs `(corpus<<24)|idx`, id-derived slot placement), so the
standard battery measures the contract layer's cost, not a new engine.

## ID-arm classification: NON-ID (crew override, per ARM_INTERFACE.md §9)

The prereg provisionally lists z2 as an ID arm. The build honestly overrides
to non-ID: recall resolves IDs through pure arithmetic (`slot_hash(id)`)
plus the slot arrays every grid arm keeps; there is **no persistent
ID→storage mapping the arm maintains** — the contract table is indexed by
slot, derived from the ID, exactly like b64's slot arrays. Consequences,
as for b64: M1 swap probe `N/A (no ID layer)`, M7 `N/A (no ID layer)` with
the informational re-read-bytes footnote.

## Kill criteria (binding, from the frozen row)

1. **Breach-detection rate < 80% on the misuse battery → Z2 is theater → KILL.**
   Measured by mode `z2-misuse-1x` (9,000 misuse probes: forbidden purposes
   per class, expired-chunk recall, tombstone recall).
2. **> 30% of legitimate recall ops refused as breaches → restrictions
   unusable → kill the restriction half, keep obligations.**
   Measured by the same mode (165 legitimate probes: permitted purposes on
   live unexpired chunks; the legit phase runs before any misuse REFUSE
   entries so the battery's own logging cannot expire the legit sample).
3. **Hot-path characterization required (znc miscompile history).**
   Mode `z2-hotpath-1x` + `docs/HOTPATH.md`: 20,000 recalls through the
   checker, decision log sha256-hashed, in-process self-check re-run,
   checker-call counting, M8 frag/aslr determinism evidence.

## Standard-battery contract policy

All standard-battery recalls declare purpose RECALL, which every
restriction class permits; expiry window is 10^9 ledger ops (effectively
never within a trial). The contract layer is therefore always on but never
refuses a legitimate metric op by design — any refusal there would be a bug,
and the ledger would show it.

## Deviations from the frozen spec

None. The §3 row is implemented literally. Two build decisions made inside
the row's latitude, both documented here: (a) contract encoded in ADD aux
fields rather than a new opcode (frozen namespace untouched); (b) non-ID
classification override (allowed by §9, swap-probe honest).
