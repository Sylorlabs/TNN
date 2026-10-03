# EXPLORE 02 — Adversarial probes against a self-chunking system

**Status: EXPLORATORY / NON-BINDING.** Designs + three executed pure-Zag probes.
Nothing here changes frozen bars. Each section names the exact frozen bar it would
amend if pursued. All probe code: pure Zag, zero RNG in any decision path, N=2 runs
byte-identical (logs beside the sources).

**Frozen context:** arm D (self-cut byte span + stable ID), arm K2 (64-bit FNV identity
with honest counted collisions, A-24), arm G1 (pressure-driven coarsening, A-16),
arm Y3 (temporal/versioned IDs, tombstones never reused, A-47), M-14 (freeze
distinguisher), R-2 (giant-span bar / L_max cap).

---

## Probe 1 — Pathological repetition (`probe_rep.zag`, `probe_rep_run1.log`)

**Attack family:** feed the exact R31 candidate enumeration (spans of length 2..8 at
every position, hashed, counted, promoted iff seen≥5) three degenerate streams:

| Stream | Unique spans (2..8) | Overflow events | Promoted (seen≥5) |
|---|---|---|---|
| `ab` × 10000 (period-2) | 14 | 0 | 14 |
| `x` × 20000 (constant) | 7 | 0 | 7 |
| `abcabc…` period-3, phase-shifted every 5000 B | 49 | 0 | 21 |

**Findings:**
1. Enumeration does NOT degenerate on these inputs: unique-span counts match the
   analytic prediction exactly (period-p stream → p distinct spans per length;
   constant → 1 per length). The 768-slot proposal table never overflows.
2. The `seen≥5` promotion bar correctly filters the 28 phase-boundary artifacts in
   stream C (49 observed, 21 promoted) — recurrence-gating works as an
   artifact filter. This is evidence *for* the recovered R31 promotion rule shape.
3. **The giant-span exploit is real and cheap:** under a *naive* compression-gain
   promotion (`gain=(n-1)*seen-(n+3)`, no L_max cap, no grounding dominance), a
   constant run of 20,000 bytes recruits a span of length **2** at gain-cap 1000 and
   length **7** at gain-cap 100000. I.e., without R-2's L_max cap and the
   grounding-dominates-compression rule, the chunker mints degenerate spans
   immediately. The reference docs rejected this exploit as a criterion; the probe
   quantifies *how fast* it fires without the bar.
4. Implication for the frozen design: R-2 (L_max cap + compression-term
   cap/weighting) is load-bearing, not decorative. Any future arm that re-weights
   compression upward must re-face this probe.

**Would amend:** R-2 (if the probe's gain-cap sweep were adopted as the L_max
calibration method).

## Probe 2 — Span collisions, tombstones, ghost IDs (`probe_id.zag`, `probe_id_run1.log`)

**Attack family:** adversarial inputs against the ID layer (13 checks, all PASS,
byte-identical across runs):

- (a) **Dedup-honest:** same bytes twice → same slot. PASS.
- (b) **Forced collision:** two *different* spans deliberately sharing one ID
  (simulates a 64-bit collision without needing to find one) → store chains the
  second span and disambiguates by content; resolution still finds live content;
  chain length ≥ 2 recorded. PASS. (This is the K2 "honest, counted collisions"
  mechanism, A-24, in miniature.)
- (c) **Revise-tombstone:** revising a span mints a new ID; the old ID is
  tombstoned; a later add is never issued the tombstoned ID. PASS × 4.
- (d) **Ghost-ID spoof:** an external reference presents a fully-tombstoned ID →
  resolves to TOMBSTONE (never live content); a never-issued ID → NOT-FOUND
  (never dangles); re-adding the *original bytes* after tombstoning mints a
  **fresh** ID (deterministic remix `id ^ attempt*0x9E3779B9` while the content-ID
  is tombstoned) and the tombstone survives the re-add. PASS × 4.

**Findings — the important one:**
Pure content-addressed IDs ("same bytes → same ID", K1's core promise) are in
**direct tension** with "tombstoned IDs never reused" (arm D, A-47): re-adding
identical bytes after a tombstone re-issues the tombstoned ID unless the ID
carries a generation/nonce. The probe resolves it with a deterministic
tombstone-remix: content-hash stays the dedup key for *live* entries, but any
content-ID that is tombstoned anywhere forces a fresh remixed ID on re-add.
Consequence for the frozen design: **K1 (pure content hash) cannot satisfy A-47
alone** — the identity substrate needs the K3 hybrid direction (content +
generation/position) or an explicit generation stamp. This is a concrete,
pre-registered-tension input to the A-4 ID-width unification decision (Micah's).

**Would amend:** A-24 (adopt counted-collision chain rules as tested), A-47
(adopt tombstone-remix / never-resurrect semantics), A-4 (ID width must include a
generation component — evidence for the K3 hybrid side).

## Probe 3 — Memory-pressure ambush (`probe_pressure.zag`, `probe_pressure_run1.log`)

**Attack family:** 8 valuable spans (50 refs each) interleaved with an attacker
burst of 400 unique junk spans, **each referenced 61 times** — a use-count
inflation ambush gaming pure-LFU eviction (junk use 61 > valuable use 50).

| Policy | Valuable survival (8) | Junk residency | Evictions |
|---|---|---|---|
| Plain LFU, tie→earliest | **0** | 64 | 408 |
| Pinned (judgment-held) valuable | **8** | 56 | 408 |

**Findings:**
1. Pure use-count eviction is **fully gameable**: the attacker doesn't need more
   *distinct* junk than the store holds — it needs each junk span referenced just
   past the valuable count. 0/8 valuable chunks survive. This is the G1 threat
   model made quantitative, and it fires *below* any WARN/CRITICAL threshold that
   counts occupancy rather than reference inflation.
2. Judgment-held pinning (the force-pin-as-law direction) survives 8/8 with
   identical eviction cost (408). The defense costs nothing in this regime — the
   difference is purely *which* slots are evictable.
3. Implication for M-14 (freeze distinguisher): the "500-unit fresh sample; fresh
   recall ≥ 80%" leg must be run against an *inflating* adversary, not just a
   filling one — a filler only tests capacity, an inflator tests the eviction
   *policy*. Proposed amendment: the M-14 churn schedule's 3,000 fresh units
   should include an inflation leg (each fresh unit referenced past the current
   max use-count).

**Would amend:** A-16 (add use-inflation resistance to G1's bar set — e.g.,
"pinned-recall bar 1%" must hold under an inflation ambush, not just occupancy
pressure), M-14 (add inflation leg to the freeze distinguisher).

---

## Further attack designs (not yet built — proposed)

1. **Split/merge oscillation attack:** feed a stream engineered so the recovered
   split condition (`use_count ≥ 3 AND conflict ≥ learned_conflict AND utility ≤
   floor`) and merge condition alternate forever on the same span pair. Tests
   whether split/merge dynamics (B-T5) can be driven into a ledger-flooding
   oscillation. Would amend R-7/B-T5 (add oscillation-damping bar).
2. **Cross-TNN ID spoof (two-TNN merge):** present TNN-B with chunk IDs minted by
   TNN-A for different bytes (counter-ID remap attack, cf. arm M's kill bar).
   Tests the "≥1 dangling/misdirected pointer" kill condition at small scale.
   Would amend the M-arm kill bar's test protocol.
3. **Teacher-wire span smuggling:** a §P WORD_SPAN proposal whose bytes are valid
   but whose *grounding* is copied from an unrelated span (the R23 "no dictionary
   installed" boundary, inverted). Tests arm O's ingress gate beyond malformed
   proposals. Would amend T-3 (flaw manifest: add a cross-grounding flaw type).
4. **Audit-log flooding via micro-revisions:** 10,000 single-byte revisions each
   just under the M4 "20 revision episodes max" scope, testing whether the
   16-word ledger entries + Y6 refcount writes stay under the 10× arm-D ledger
   volume bar. Would amend M-25/A-50.

---

## Toolchain note (apparatus, not science)

Probes initially hit **ZNC-2026-09-19-001** (pinned znc miscompiles multi-store
`[]i32`/`[]i64` contexts — independently re-derived here: 3+ sequential i32
stores corrupt; `[]u8` stores are fully reliable, verified over 500 sequential
u8-backed i32 cells with negatives/extremes exact). All three probes were
rebuilt on `[]u8` storage with little-endian i32 cells (`a32_set`/`a32_get`) and
pass byte-identical. The workaround is documented in each probe's header. This
does not affect frozen bars — it is an apparatus note for the core/harness crews
building in `r0/impl/`: **prefer `[]u8`-backed cells over `[]i32` arrays until
the compiler is fixed.**

## Relation to frozen bars

| Probe / design | Frozen bar it would amend (if pursued) |
|---|---|
| Probe 1 gain-cap sweep | R-2 (L_max calibration method) |
| Probe 2 chain + tombstone-remix | A-24 (K2 chain rules), A-47 (never-resurrect), A-4 (generation in ID width) |
| Probe 3 inflation ambush | A-16 (G1 bars), M-14 (freeze distinguisher inflation leg) |
| Design 1 oscillation | B-T5 / R-7 (dynamics damping bar) |
| Design 2 cross-TNN spoof | M-arm kill bar test protocol |
| Design 3 wire smuggling | T-3 (flaw manifest composition) |
| Design 4 ledger flooding | M-25, A-50 (ledger volume bars) |
