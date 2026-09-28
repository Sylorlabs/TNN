# STORAGE-COMPRESSION INVESTIGATION — Preregistration (FROZEN 2026-09-22)

**Order:** Micah, 2026-09-22, verbatim: "investigate if we can get methods to
make TNN use less — is there compression that makes TNN maybe slightly slower
or heck even free lunch for this? If compressed knowledge in a certain way has
same properties but takes slightly longer to use and costs barely anything,
its a win. Send Sol, Grok, and Muse."

**Freeze rule:** this document is committed BEFORE any scheme is implemented
or measured. Amendments after freeze require a new dated section; frozen
sections (§1–§8) are never edited in place. Consultant hypotheses arriving
after freeze are recorded verbatim in §9 (append-only) with attribution.

## §1. Baseline (CORRECTED — supersedes the 220-byte figure)

The frozen throughput instrument (`ops/throughput/thru_learner.zag`,
report commit `67bf4c4c`) stores per fact, by the driver's own `SCALE_MEM`
accounting (`bpf_slot=24`, `bpf_idx=4`, `bpf_audit=(ops_audit*64)/n`):

| Component | Bytes/fact | Layout (verified by code inspection) |
|---|---|---|
| Slot | 24 | id@0 i32, lifecycle@4 i32, strength@8 i32, clock@12 i32, value@16 i64 |
| Dense id→slot index | 4 | i32 per id, 0xFFFFFFFF = empty |
| Audit ledger | 64 | 16 × i32 per add: op,slot,rc,b1..b5,a1..a5,stage,d1,d2 |
| **Total** | **92** | |

**Correction:** earlier briefings and the README ("So what's the catch:
STORAGE", commit `f3656c8`) stated ~220 bytes/fact (~92 slot + ~128 audit).
That was a misreading: the audit's "16 words" are 16 × i32 = 64 B, not
16 × 8 B, and the driver's 92 B figure was already the all-in total, not the
slot alone. Evidence: `sc_audit_append` writes 16 `sc_s32` (lines 820–838);
`sc_add` writes the 24 B slot (lines 906–911); `SCALE_MEM` prints 24+4+64=92
(lines 1174–1181). The past-RAM prereg independently confirms the same
structure (4096×24 B slot chunks, 4 B index, 16384×64 B audit chunks, all in
process heap, zero persistence). The audit ledger is 69.6% of the cost —
still the biggest component, still the prime target.

Measured performance at baseline (frozen): install ~6.2 µs/fact (process CPU
clock), recall 1–3.2M probes/sec O(1), deliberation ~3,300 episodes/sec
(separate instrument `dlg_thru.zag` with its own structures — applicability
of slot-layout schemes to it is reported honestly, not assumed).

## §2. Free-lunch candidates (from code inspection — to be verified by measurement)

These are candidate pure-waste removals. Each must still satisfy §5.

- **FL1 — slot id field (4 B):** written at line 907, never read anywhere in
  the instrument (no `sc_g32(ch,o)` read exists; `sc_recall` reads only o+16).
  The id→slot mapping already lives in the dense index; the slot's id copy is
  redundant for addressability.
- **FL2 — audit zero-words (36 B):** for op=1 (deliberate add), 9 of 16 words
  are always zero (b3,b4,b5,a3,a4,a5,stage,d1,d2). A per-op compact encoding
  (op,slot,id,v_lo,v_hi = 5 words = 20 B) preserves every information bit of
  the add record while cutting the audit entry 64→20 B.
- **FL3 — constant slot fields (8 B):** strength is always 1000 and lifecycle
  always 1 at install in this instrument (lines 908–909). Sparse/default
  encoding (store only deviations) costs nothing when constant.
- **FL4 — clock redundancy:** `sc_episode` runs once per pass (line 1011), so
  in single-pass runs all N slots carry an identical clock value (4 B × N of
  the same number). Per-chunk or delta encoding removes it.

If all four verify: 24→12 B slot, 4 B index, 64→20 B audit = **36 B/fact**
(60.9% reduction) with identical information content.

## §3. Hypothesis families under test

- (a) **Audit-ledger compaction** — per-op compact encodings (FL2 and
  generalizations to other op types). Replay/tamper-evidence preserved by
  construction (same fields, denser packing; hash chain over compact bytes).
- (b) **String interning / dictionary encoding** — applies to text-valued
  facts. NOTE: the frozen instrument stores i64 values; this family is
  prototyped on a string-valued variant and reported separately, not mixed
  into the headline 92 B figure.
- (c) **Delta encoding** — clock/id deltas across sequential slots (FL4 and
  generalizations).
- (d) **Cold-fact consolidation** — archive rarely-touched facts into denser
  form with a measured recall penalty. NOTE: the instrument has no per-slot
  access tracking; this prototypes the tracking the consolidation organ
  would need. Scoped honestly: a prototype, not the organ.
- (e) **Columnar / sparse slot layouts** — struct-of-arrays refinements,
  sparse overrides for near-constant fields (FL3 generalization).
- (f) **Consultant-invented** — anything from Sol, Grok-4.6, or native Muse
  consultants not covered above, recorded verbatim in §9 with kill bars.

## §4. Metrics (the tradeoff curve is the deliverable)

Per scheme, per N in {240K (anchor), 1M}: bytes/fact (driver accounting AND
RSS-vs-N slope), install µs/fact (CLOCK_PROCESS_CPUTIME_ID, same basis as
the 6.2 µs figure), recall probes/sec (microbenchmark + eval sweep),
deliberation episodes/sec where applicable. The deliverable is
**bytes saved per microsecond of slowdown** per scheme, plus the free-lunch
verdict (bytes AND time saved = unconditional win).

## §5. Kill bars (frozen)

- **KB-CORRECT:** every scheme must reproduce the byte-identical recall
  digest (FNV-1a over (id, recalled value) for all ids) and pass the 96-probe
  flaw battery 96/96. Any scheme that changes recall results is dead.
- **KB-ADDR:** facts stay explicit, individually addressable via id→slot,
  revisable, deletable, countable. Any scheme that merges facts into an
  unaddressable blob is dead.
- **KB-DET:** ≥3 runs per (scheme, N), byte-identical digests across runs,
  zero RNG anywhere, pure Zag for TNN-side mechanisms.
- **KB-WIN:** earns a README-update recommendation iff total bytes/fact cut
  ≥20% with install slowdown ≤10% AND recall slowdown ≤10%; OR any cut with
  zero slowdown on both (free lunch) wins unconditionally.
- **KB-HONEST:** family (b) and (d) results are reported on their own basis,
  never folded into the headline instrument figure.

## §6. Method

Fork `thru_learner.zag` per scheme (layout/timing changes only; the
verify/teach/eval semantics in `sc_verify`, `sc_teach_value`, `sc_flaw` are
untouched). Build with the pinned toolchain
(`toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze`). The 240K anchor
must reproduce ~6.2 µs/fact and the frozen digest before larger N are
trusted. Work in `~/workspace/tnn-lab/ops/storage-compression/`; scratch in
`~/workspace/tmp_commit`; never `/tmp` (shared 512 MB tmpfs is full). Do not
disturb the running past-RAM or PAM-rebuild coordinators.

## §7. Constraints (non-negotiable, Micah's standing laws)

Facts stay explicit, countable, individually addressable, revisable,
deletable. Zero RNG in any decision path. Deterministic: identical
state+input reruns byte-identically. Pure Zag for TNN-side mechanisms. TNN
stays one unified brain. Knowledge-first: outside consultants build
hypotheses/tests, never crew-authored architecture for invention claims.

## §8. Deliverables

Committed under `docs/lab/ops/storage-compression/`: this prereg (alone,
first), consultant hypotheses (§9, verbatim), per-scheme evidence (hashes,
digests, measurements), and a final verdict: winner(s), the bytes-vs-speed
tradeoff table, the free-lunch verdict, and proposed README replacement text
(the README itself is NOT modified by this investigation).

## §9. Consultant hypotheses (append-only — filled after freeze)
