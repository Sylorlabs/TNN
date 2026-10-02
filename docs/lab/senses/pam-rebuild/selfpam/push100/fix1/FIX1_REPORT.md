# FIX1 — broad fix for the candidate gate's order-blindness (push-to-100%, round 3)

**Date:** 2026-09-27 | **Crew:** fix crew (self-PAM push-to-100% round 3)
**Corpus:** frozen CELL-A 1,200-pair corpus (`~/workspace/selfpam_consumer/pairs_full/`,
1200/1200 `.pair` SHAs verified OK against committed `MANIFEST.r2p.sha256`)
**Regression list:** round-1 autopsy `push100/round1/miss_table.tsv` (101 rows)
**Scope:** candidate-experimental only. The §8 draft is untouched; `span_seq/8`
is a PROPOSED revised §8 value, not an enacted one (see §6).

## 1. The problem (recap)

The candidate gate (id 2) judged each span with `span_sum(evidence)/8` — a raw
byte sum, blind to byte order. Of the 101 pairs it admitted (withheld
1099/1200 = 91.58% vs the reference gate's 1200/1200), the round-1 autopsy
(`push100/round1/MISS_AUTOPSY.md`, commits add55081e7 + 01e30c9201) confirmed
**all 101 are genuine should-withhold misses; zero correct admits**, in two
mechanism classes:

- **Class A (100, motiondir/reversed, seq 1000–1198 even):** exact
  byte-permutations — F is the frame-reversed video, G is forward; sorted
  bytes identical on all 100, so the sums collide exactly and the gate admits.
- **Class B (1, seq 135, colordisc, truth=SAME, "illuminant-drift"):** an EXACT
  byte-sum collision — the warm illuminant maps (48,167,159)→(137,155,82)
  with per-pixel channel sum preserved (374=374; gains +89/−12/−77 net to zero
  after rounding); total sums exactly equal (2,872,404 → jf=jg=359050). The
  ÷8 tolerance is NOT the cause — tightening it would not fix this pair.

## 2. What changed

**`selfpam/src/g1_candidate.zag`** (mirrored byte-identically into
`round2/forks/R2-3/src/g1_candidate.zag`; `codec.zag`'s `span_sum` UNTOUCHED —
still the §8-drafted SPAN-SUM value used by `corr.zag` and the cc1_guard tests):

- NEW `span_seq(ev)`: position-weighted sum **Σ (i+1)·b_i mod 2^31** over the
  evidence bytes (i64 accumulator; corpus max span 86,408 bytes → accumulator
  ≈ 9.5e11, enormous i64 headroom). Swapping bytes at positions i,j changes
  the sum by exactly **(i−j)·(y−x)** — nonzero unless the swapped bytes are
  identical — so pure permutations are provably visible.
- NEW `span_fnv(ev)`: FNV-1a 32-bit digest (same per-step masking as the
  codec's `fact_jcode`), for the comparison variant.
- `sp_gate_judge` now wires three selectable variants:
  - **id 2** `selfpam-fact-gate` — PRIMARY: `span_seq(evidence)/8`
    (same sum-measurement family and /8 tolerance shape as before;
    small benign byte differences → small measurement differences).
  - **id 3** `selfpam-sum-gate` — LEGACY: `span_sum(evidence)/8`, the
    pre-fix1 id-2 law, kept measurable as a control.
  - **id 4** `selfpam-fnv-gate` — COMPARISON: `span_fnv(evidence)`, exact
    comparison (tolerance 0): withhold iff digests differ.

**`round2/forks/R2-3/src/sense.zag`**: gate-id range 0..2 → 0..4.
**`round2/forks/R2-3/src/r2p_gates.zag`**: id 3/4 branches delegating to
`sp_gate_*`. Ids 0/1 behavior unchanged.

Governance: amendment 2026-09-27-A froze `g1_candidate.zag` semantics behind
"any future change needs its own amendment" — the required draft amendment
is `selfpam/amendments/AMENDMENT_2026-09-27_G1_FIX1.md` (DRAFT, awaiting
coordinator disposition); a dated staleness banner was added to
`G1_REGISTRATION.md`. Revert SHAs are recorded in the amendment.

## 3. Why this is a broad fix, not a bridge to the corpus

1. **No task/index/content branching anywhere.** `span_seq`/`span_fnv` take
   only the evidence bytes; `sp_gate_judge`'s id-2/3/4 branches ignore the
   `task` parameter entirely. The red-team probe proves it: identical bytes
   judged under task 0 vs task 5 give identical judgments on all three ids
   (`T1_task_independent=1`), using synthetic blobs that never touch the
   corpus.
2. **One mechanism fixed two unrelated miss classes.** The same change fixed
   all 100 Class-A order-only motiondir pairs AND the Class-B illuminant-drift
   exact-sum collision (different task, different cause, different byte
   relationship — permutation vs distinct-content) — because both were
   instances of aggregate-measurement blindness, not corpus patterns.
3. **The separation is content-agnostic math, with huge margin.** Class A:
   min |ΔW| = 10,144,128 across the 100 reversed pairs (median 666M). Class B:
   |ΔW| = 637,440 (verified empirically from the actual bytes: span_seq(F)=
   901,501,636 vs span_seq(G)=902,139,076, while span_sum(F)=span_sum(G)=
   2,872,404 exactly). All are millions of times outside the ±8 quantization
   window — a different measurement regime, not a tuned threshold.

## 4. Measurement results

Built EXACTLY per `BUILD_RECORD_G1_ID2.md`'s procedure (pinned znc
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
SHA-verified before compiling; vendoring check passed; build log with all
staged SHAs in `build_fix1.log`). Binary
`fd13d2eb9ca8a1677420b6f8f2a47f6be5cf46fa54f988d68d6f97b3667560ca`
(build scratch, not committed). ~19 s per 1,200-pair run.

| Variant | Gate id | Withheld | Rate | Errors | Overlap | ×3 byte-identical | Chain verified |
|---|---|---|---|---|---|---|---|
| span_seq/8 (primary) | 2 | 1200/1200 | **100.00%** | 0 | 0 | yes | yes (×3) |
| span_sum/8 (legacy) | 3 | 1099/1200 | 91.58% | 0 | 0 | yes | yes (×3) |
| FNV-1a exact | 4 | 1200/1200 | **100.00%** | 0 | 0 | yes | yes (×3) |
| reference (regression) | 0 | 1200/1200 | — | 0 | 0 | byte-identical to committed R2-3 evidence | yes |
| broken (regression) | 1 | 0/1200 | — | 0 | 1200 | byte-identical to committed R2-3 evidence | yes |

- **Misses fixed:** 101/101 (the full autopsy regression list: all 100
  Class-A reversed pairs + the Class-B seq-135 collision) now withhold
  under both id 2 and id 4.
- **Regressions:** 0 — all 1,099 previously-withheld pairs still withhold
  under id 2 and id 4.
- **Legacy control:** id 3's admitted set is EXACTLY the autopsy's 101
  (seq 135 + 1000–1198 even) — the old law reproduced to the pair, proving
  the instrument change is isolated to the candidate measurement.
- Reports + ledgers: `push100/fix1/reports/`, `push100/fix1/ledgers/`.
- Numbers: `push100/fix1/numbers_fix1.json` (schema v1, for consolidation
  into `push100/NUMBERS.json`).

## 5. Red-team results (full report: `REDTEAM_FIX1.md`)

An independent-eyes pass inside the crew attacked the fix three ways, with a
Zag probe (`probe_fix1.zag`, output in `probe_output.txt`) whose every value
was cross-checked against an independent Python reimplementation (exact match):

1. **Subset-sum / quantization attack — SUCCEEDS mathematically, MISSES as
   an attack.** An adjacent swap with Δ=−1 collides after /8 when it doesn't
   cross a bucket boundary (probe T3: 5592321 → 5592320, same judgment,
   admitted). So the /8 window is real. But the byte-difference it hides is
   perceptually nil (two adjacent near-identical bytes) — no reference
   judge would disagree on such a pair either, so it produces no
   reference-withholds/candidate-admits miss. The 100 natural reversed pairs
   sit ≥10M away from the window, not near it.
2. **Byte-tweaks preserving BOTH sums — SUCCEEDS, honestly reported.** The
   measurement imposes only 2 linear constraints; a 4-byte tweak
   (+1/−1/+1/−1 at positions 20/30/60/50) preserves both sums exactly (probe
   T4), and a two-swap construction with **±255 byte changes** achieves
   exact Δ=0 on both sums (probe T7: Δ=(0−200)(255−0)+(1−201)(0−255)=0).
   Conclusion: `span_seq/8` is NOT tamper-evident against a byte-level
   adversary — but the gate's threat model is natural corpus pairs, not an
   adversary with write access to the evidence bytes. The FNV variant (id 4)
   raises the bar to a ~2^32 second-preimage search (FNV-1a is
   non-cryptographic — stated honestly, not oversold).
3. **Generality — HOLDS.** Pure function of evidence bytes; task-independent
   (T1); synthetic-blob reversal control (T5) withholds under id 2 while
   id 3 admits — the same mechanism works on never-seen bytes. One mechanism
   fixed both autopsy classes (permutation AND exact-sum-collision) with no
   per-index, per-task, or per-cause logic anywhere.

## 6. The §8 proposal (PROPOSED — not enacted) — REVISED after expansion results

The §8 draft defines meas=SPAN-SUM with tolerance 8 and is UNSIGNED
(awaiting Micah). It was NOT edited and nothing here claims enactment.

The round-2 adversarial expansion corpus (frozen 2026-09-27, 352 pairs,
`push100/expansion/`, committed BEFORE any gate measurement) changes the
recommendation. The original fix1 proposal — `span_seq/8` as the revised §8
value — does not survive the expansion evidence. What follows is the
revised, evidence-led proposal.

### The trade-off table (measured, not hypothesized)

| | id 3: span_sum/8 (legacy) | id 2: span_seq/8 (fix1 primary) | id 4: FNV-1a exact digest |
|---|---|---|---|
| Frozen corpus, 1,200 (naturalistic) | 91.58% withhold | 100% | 100% |
| Expansion DIFFERENT, 312 (adversarial) | 0% (0/312) | 66.7% (208/312) | 100% (312/312) |
| Expansion misses | 312 | 104 (48 fshuffle + 32 pxperm + 24 wsumcol) | 0 |
| calib 7a: 20 byte-identical must-admit | 20/20 admit | 20/20 admit | 20/20 admit |
| calib 7b: 20 single-byte ±1 probes | 14/20 admit (tolerant) | 0/20 admit (strict) | 0/20 admit (strict) |
| Exact-collision resistance | none | weak — 3 exact-blindness mechanisms (§8) | strong (non-cryptographic) |
| Tolerance semantics | yes | effectively no (see below) | no (by design) |

Two findings matter most:

1. **The weighted sum is exactly blind to three constructed classes**
   (§8): equal-mass block permutations (fshuffle, 48/48), channel-
   complementary pixel permutations (pxperm colordisc/colorconst, 32/32),
   and arithmetic-progression 3-cycles (wsumcol, 24/24 — family 8). These
   are exact collisions (ΔW = 0), not quantization near-misses. The
   linearity of Σ(i+1)·bᵢ is the root cause in all three.

2. **The calibration refutes the tolerance story for `span_seq/8`.** A
   single-byte ±1 change at position i shifts the weighted sum by ±(i+1);
   for i ≥ 7 that is ≥ 8 and ALWAYS flips the /8 judgment. Measured: 0/20
   admits on the ±1 probes — identical strictness to FNV, without FNV's
   collision resistance. Only the legacy plain sum is genuinely tolerant
   (14/20 admits). So `span_seq/8` sits in the worst middle: strict like a
   digest, fragile like a sum.

### Revised recommendation

The evidence favors **the exact-digest variant (id 4, FNV-1a) as the
revised §8 measurement value** — 100% on the frozen corpus, 312/312 on the
adversarial expansion, 20/20 must-admit controls. The cost is explicit:
zero tolerance — ANY byte difference in the evidence withholds, including
the ±1 probes the plain sum would admit (14/20).

This is a semantic choice for the program, not a technical inevitability:

- **Exact digest** = the gate asks "is the evidence byte-identical?"
  Strict, collision-resistant (non-crypto), no calibration knob.
- **Sum family** = the gate asks "is the evidence approximately equal?"
  Tolerant (`span_sum/8`), but blind to every order-only difference by
  construction.

The weighted middle (`span_seq/8`) is not recommended: it buys neither
tolerance nor collision resistance.

Caveats: FNV-1a is non-cryptographic; if §8 wants tamper-evidence against
a deliberate forger, the codec already ships `fact_evhash` (SHA-256) — a
design decision for the program, not the fix crew. The draft amendment
`AMENDMENT_2026-09-27_G1_FIX1.md` (which proposed `span_seq/8`) is
superseded on the recommendation by this section; the amendment file is
left standing as the dated record.

Whether the program adopts any of this is Micah's call through the normal
amendment process.

## 7. Honest residual ceiling (revised after expansion)

- **Frozen corpus (1,200):** 100% under id 2 and id 4 — zero misses remain.
  All 1,099 prior withholds retained, 101/101 prior misses fixed, zero
  regressions.
- **Adversarial expansion (352):** id 4 (FNV) 312/312 DIFFERENT withhold,
  20/20 must-admit — clean. id 2 (`span_seq/8`) misses 104/312 by three
  exact-collision mechanisms (48 fshuffle + 32 pxperm + 24 wsumcol). id 3
  (legacy) misses 312/312 — fully order-blind, as designed.
- **Autopsy reconciliation — RESOLVED.** The round-1 autopsy confirmed
  101/101 genuine misses, zero correct admits; the preliminary
  "possibly correct admit" hypothesis for the truth=SAME pair is refuted
  (generator-certified fooled F, reference withholds, no truth-based
  carve-outs in the program's bar). The regression target is therefore
  clean, and this fix meets it exactly.
- **Natural (non-adversarial) future pairs:** the exact collisions require
  constructed equal-mass / channel-complementary / arithmetic-progression
  arrangements — they do not occur by chance, but the claim is now bounded:
  unmeasured outside these two frozen corpora. A motivated constructor
  defeats the weighted sum at will (three corpus families prove it).
- **Byte-level adversary:** `span_seq/8` is exactly forgeable (three
  expansion families plus red-team T4/T7); FNV-1a raises the bar
  substantially but is non-cryptographic. Tamper-evidence needs a
  cryptographic digest (`fact_evhash`/SHA-256 exists in the codec) — out of
  scope for this fix, and a design decision for the program, not the fix
  crew.

## 8. Adversarial expansion corpus (round 2) — primary fails, digest holds

Corpus: `push100/expansion/` — 352 pairs, 8 families, frozen 2026-09-27
BEFORE any gate measurement (commit `794021e7`, manifest SHA-256
`cedf7551cf41fdf7abc619df0ab3a0842b973c25fb2fd6e13055e57a34c58dba`,
verified `sha256sum -c` clean on extraction). Family specs in
`expansion/FAMILIES.md`.

Measurement driver: `fix1/xp_measure.zag` — pure-Zag, calls the real
`sp_gate_judge` (fixed `g1_candidate.zag`, SHA-256
`b7f9622a834bdc8a06235eb6846ce1d351db155df9d35890b6451a19c90a48d1`)
for ids 2/3/4 over each pair's F/G blobs; withhold iff judgments differ.
Binary SHA-256
`43afb5ac08910487f7bb6522e68b02efd0bfe4116df0df8fc6c1a1d75d4780c1`
(scratch, not committed). Per-pair judgments: `fix1/xp_results.txt`
(SHA-256 `0f0198e5816a05d12a3b5b61988db7b30157b44cefd58fbe72d06436cf2413c5`);
pair list: `fix1/xp_manifest.txt`. 352/352 pairs processed, 0 errors.

### 8a. Per-family withhold rates (truth=DIFFERENT families — should withhold)

| Family | n | Attack | id 2 (span_seq/8) | id 3 (span_sum/8) | id 4 (FNV-1a) |
|---|---|---|---|---|---|
| audiorev | 48 | audio time-reversal | 48/48 | 0/48 | 48/48 |
| blkswap | 48 | half-block swap | 48/48 | 0/48 | 48/48 |
| cycshift | 48 | rotation by len//3 | 48/48 | 0/48 | 48/48 |
| fshuffle | 48 | deranged frame permutation | **0/48** | 0/48 | 48/48 |
| pxperm | 48 | in-frame pixel permutation | **16/48** | 0/48 | 48/48 |
| sumswap | 48 | single 2-byte swap | 48/48 | 0/48 | 48/48 |
| wsumcol | 24 | constructed weighted-sum collision | **0/24** | 0/24 | 24/24 |
| **total** | **312** | | **208/312 (66.7%)** | **0/312** | **312/312 (100%)** |

### 8b. Calibration family (truth=SAME — keeps the false-withhold bar honest)

| Probe | n | id 2 admit | id 3 admit | id 4 admit |
|---|---|---|---|---|
| 7a: byte-identical (must-admit) | 20 | 20/20 | 20/20 | 20/20 |
| 7b: single byte ±1 | 20 | **0/20** | 14/20 | **0/20** |

The 7a controls pass on all variants (identical bytes ⇒ identical
judgments/digests). The 7b probes are the honest surprise: `span_seq/8`
admits 0/20 — it is NOT tolerance-calibrated. A ±1 byte change at position
i shifts the weighted sum by ±(i+1); for i ≥ 7 that is ≥ 8 and always flips
the /8 judgment. Only the legacy plain sum shows real tolerance (14/20;
flips only on crossing a multiple of 8). The weighted variant is exactly
as strict as FNV on small perturbations, without FNV's collision
resistance.

### 8c. The three exact-blindness mechanisms of the linear weighted sum

All three give ΔW = 0 EXACTLY (not mod 2³¹, not post-quantization) —
verified byte-level against the corpus, proofs below.

**M1 — Equal-mass block permutation (fshuffle, 48/48 blind).**
All 8 frames of every fshuffle pair carry byte sum 7532 (verified). Write
W = Σₖ (384·k·Mₖ) + internalₖ, where Mₖ is the byte sum of the frame at
position k and internalₖ moves with its frame. Under any frame
permutation with all Mₖ = M: Σₖ 384·k·M = 384·M·Σₖk — independent of the
permutation. The linear position weight cannot see permutations of
equal-mass blocks. (Generalizes the round-1 Class-A reversal.)

**M2 — Channel-complementary 2-valued pixel permutation (pxperm
colordisc/colorconst, 32/32 blind; shapetrans 16/16 separate).**
The split fields contain exactly two pixel values, (200,30,30) ×64 and
(30,30,200) ×64 (verified; G channel constant). A pixel changing
A→B at pixel position p contributes
Δ = (3p+1)(−170) + (3p+3)(170) = 340 — position-independent. Each B→A swap
contributes −340. The permutation preserves pixel counts, so A→B and B→A
swaps pair up and ΔW = 0 exactly. The structured 8-frame shapetrans fields
have no such complementarity and separate 16/16.

**M3 — Arithmetic-progression 3-cycles (wsumcol, 24/24 blind — family 8).**
As proven in `expansion/FAMILIES.md`: positions (p0, p0+d, p0+2d) with
values (x,z,y), 2y = x+z, 3-cycled. ΔW = d(x+z−2y) = 0 exactly; the plain
sum is preserved because it is a permutation. 12 bytes change value per
pair (e.g. 16→116). The fix1 primary was KNOWN to miss these by
construction — confirmed empirically 24/24 admit under id 2 and id 3,
24/24 withhold under id 4.

### 8d. What this means

The expansion corpus was built to attack the ORIGINAL sum gate, but two
of its families (fshuffle, pxperm-2val) defeat the weighted fix as well,
and family 8 was built specifically against it. The primary variant's
honest scorecard:

- Frozen naturalistic corpus: 100% (fix verified, §4).
- Adversarial expansion: 66.7% — 104 misses by three exact-collision
  mechanisms, all rooted in the linearity of Σ(i+1)·bᵢ.
- Tolerance calibration: 0/20 — no tolerance benefit over exact comparison.

The comparison variant (FNV-1a exact digest) scores 100% / 100% / 20/20
must-admit, at the price of zero tolerance (0/20 on ±1 probes — by
design). It resists all three corpus mechanisms and both red-team
constructions (T4, T7). It is non-cryptographic; deliberate forgery by a
byte-level adversary who can compute FNV-1a is not ruled out — but unlike
the weighted sum, no exact-collision CLASS is known.

This is why §6's recommendation was revised: the §8 measurement value
should be the exact digest, not the weighted sum. The weighted sum was a
good fix for the naturalistic corpus and a poor choice for an adversarial
one — and the calibration shows it does not even purchase tolerance.
