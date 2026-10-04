# C-W — Ambiguity decisions

Literal-prereg rule: implement the frozen reading, log the decision here, never
silently reinterpret. All decisions below were taken against the frozen
`ARM_INTERFACE.md`, `HARNESS_SPEC.md`, `ALPHABET_A-F.md` (Arm C), and
`briefs/C-W.json` as observed 2026-09-21.

## A1. ADD_UNIT per chunk vs one bulk SCAN_COMMIT for the scan

§6 defines both `ADD_UNIT` (d1 = chunk_index) and `SCAN_COMMIT` (bulk ingest,
"deterministic replay required"); the prereg mechanism says "one deterministic
scan". The ALPHABET buildability note records that per-cut entries were
proposed while bulk SCAN_COMMIT was the frozen-at-sign-off alternative.

**Decision:** per-chunk `ADD_UNIT` (d1 = chunk_index, d2 = 0), matching the
frozen B-64 validator's per-unit ADD pattern. Rationale: §5 says the audit
ledger records the exercised deliberate ops, and the arm's exercised op is the
per-chunk ingest; per-chunk entries keep M5's audit-entries/KB directly
comparable between C-W and B-64 (the bake-off's control comparison). A bulk
SCAN_COMMIT would make C-W's audit cost trivially ~0 and non-comparable.
Logged here; the alternative reading is recorded, not implemented.

## A2. Non-ID classification and M1/M7 consequences

`ARM_INTERFACE.md` §9 lists `cw` as provisionally non-ID. The arm's chunk IDs
are positional arithmetic `(corpus<<24)|index`; there is no ID→storage mapping
to attack or reuse.

**Decision:** M1 ID-swap probe N/A; M7 hit rate / reuse rate / dedup savings
reported `null` with `m7_na_reason` = "no ID layer: chunk IDs are positional,
lookup is by unit key"; M7 still reports the honest `m7_reread_bytes` over its
deterministic lookup sample plus the trainer-edit round. Implemented literally;
if the provisional classification is overturned, M1/M7 must be re-implemented.

## A3. Ledger sharding vs monolithic ledger

§6 fixes 64-byte entries but not the ledger's memory layout. `nio_alloc`
refuses slices over 2^25 bytes, so the honest per-chunk ledger (123 MB for
M1-prose) cannot be one slice.

**Decision:** 16 shards × 500,000 entries, logical order preserved (build note
in ARM_SPEC §5, not a prereg amendment; byte-identical rerun verified through
the M8 gate's ledger hash).

## A4. M8 store/ledger hashing without a monolithic image

The frozen M8 contract wants per-≤1 MB chunk hashes of the slot region and a
chain. Materialising the 171 MB image as one slice violates the 2^25 rule.

**Decision:** hash the 8 slot arrays directly in 1 MB logical chunks in the
contract's fixed array order (staging buffer; same chunk boundaries as a
materialised image would produce). Exact 1 MB concatenation boundaries are the
contract; array-ordered chunking satisfies them by construction.

## A5. M2 ledger sizing vs "size their ledgers to complete the trial"

A 50-episode worst case for t2_prose would need 82M entries (5.2 GB) — not
realisable. The validator itself undersizes M2's ledger (64 entries).

**Decision:** M2's ledger is sized at `4*n+4096` entries (covers the
mechanically-determined run: ETC=1 → 3 episodes ≈ 3n entries, plus margin).
Fill-drops are silent as in the validator; no LEDGER-BOUND fired in any run.
Ledgers for scored modes (M5, M8) are sized to hold every entry.

## A6. Scorecard assembler hardcodes `"arm": "b64"`

Frozen `scorecard_assemble.py` writes top-level `"arm": "b64"` regardless of
input fragments (and M1 probe text). The harness is frozen; not edited.

**Decision:** after assembly, apply a documented evidence-only correction of
the top-level `arm` field to `"cw"` in the shipped scorecard copy; the
per-mode fragments already emit `"arm":"cw"`. M1's probe text happens to be
correct (N/A for both arms).

## A7. `weaken` semantics

`WEAKEN` (0x04) is implemented as an audited annotation: it logs the op with
the trainer-supplied weight and does not alter stored bytes, pins, or eviction
order. This is the literal §6 reading (no behavioural clause is specified for
0x04 beyond the audit record).

## A8. Slot-table initialization vs allocator luck

znc does not reliably zero fresh heap (`AGENTS.md` ZNC lesson, confirmed by
another crew's M8 failure). `cw_init` left `flags`/`ids` uninitialized, so
slot placement could depend on heap garbage — which the M8 `frag`
perturbation deliberately reshuffles.

**Decision:** explicitly zero `flags`/`ids` and set `pidx` to −1 over all
`cap` slots at init. Determinism becomes structural. Post-fix output is
identical to pre-fix (the OS had been zeroing the large mmap'd arrays), so
this is a robustness fix, not a behaviour change.

## A9. Tenths arithmetic overflow in `probe_chunks`

`ok*1000/n` was computed in i32; for code's 2,446,768 chunks the product
overflows 2^31 and the metric went negative (−75.5). Prose (1,926,956) stayed
under the limit, hiding the bug on one leg.

**Decision:** widen to i64 before multiplying (all other `*1000` sites already
did). Pure bug fix; the corrected code leg reports 100.0/100.0 like prose.
