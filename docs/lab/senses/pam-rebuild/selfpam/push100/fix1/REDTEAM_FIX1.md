# REDTEAM_FIX1 — adversarial review of the span_seq/8 candidate gate

**Date:** 2026-09-27 | **Crew:** fix crew, adversarial pass
**Regression target:** round-1 autopsy `push100/round1/miss_table.tsv`
(101 genuine should-withhold misses, 2 mechanism classes; zero correct admits)
**Method:** a dedicated Zag probe (`probe_fix1.zag`) exercising
`sp_gate_judge` on synthetic blobs (no corpus bytes), every asserted
judgment cross-checked against an independent Python reimplementation —
exact agreement on all tests. Probe binary
`2c8275e3dafec50912f756271f78962670a20be909ab06e43e179f5c891db40f`
(scratch, not committed). Output: `probe_output.txt`.

## Attack 1 — subset-sum / quantization attack (the /8 window)

**Goal:** find byte-differences that change the weighted sum by less than 8
(or cross no /8 bucket boundary) and are admitted by id 2 while a reference
judge would withhold.

**T3 (adjacent unequal-byte swap, Δ=−1):** blob where positions 1999/2000
hold `c8` vs `c7`. Weighted sums 5592321 → 5592320; judgments identical
(699040); **admitted**. The /8 window is real: a Δ of −1 that doesn't cross
a bucket boundary is invisible to id 2.

**But:** the hidden difference is two adjacent near-identical bytes —
perceptually nil. No plausible reference judge would withhold on such a
pair, so this produces NO reference-withholds/candidate-admits miss. The
100 natural Class-A reversed pairs sit ≥10,144,128 away from the window —
a million-fold margin, not a tuned threshold. The Class-B pair sits 637,440
away.

**T6 (modular wrap):** the mod 2^31 cannot hide a small swap (additive
accumulator; mod only folds overflow, can't cancel a ±1 difference).

**Verdict: mathematical success, attack failure.** The residual risk is
natural pairs whose F/G differ ONLY by permutations with |Δ|<8 that a
reference judge would still call different — implausible, and absent from
the 1,200-pair corpus (100% withhold).

## Attack 2 — byte-tweaks preserving BOTH span_sum and span_seq

**Goal:** keep both the plain sum AND the weighted sum identical under a
perceptually real byte change — the full dual-sum collision.

**T4 (four tweaks, ±1 byte changes):** positions 20/30/60/50, changes
+1/−1/+1/−1 → plain sum Δ=0 AND weighted sum Δ=0 (verified by the Python
oracle too). **Both id 2 and id 3 admit; FNV (id 4) withholds.**

**T7 (two-swap construction, ±255 byte changes):** positions 0/200 and
1/201, swaps of 0↔255. Δ = (0−200)(255−0) + (1−201)(0−255) = 0 **exactly** —
plain and weighted sums both preserved under large local byte changes.
**Ids 2 and 3 admit; FNV withholds.**

**Verdict: succeeds.** The measurement imposes only 2 linear constraints on
N bytes; the solution space is (N−2)-dimensional. `span_seq/8` is NOT
tamper-evident against a byte-level adversary. This is an honest ceiling,
not a disqualifier: the gate's threat model is natural corpus pairs (F and
G are independent measurements of a claim's subject), not an adversary with
write access to the evidence bytes. Against that threat model the fix holds
100% on the frozen corpus. The FNV variant raises the adversarial bar to a
~2^32 second-preimage search; FNV-1a is non-cryptographic and is not claimed
to be otherwise.

## Attack 3 — generality (is the fix broad?)

- **T1 (task-independence):** identical bytes under task 0 vs task 5 give
  identical judgments on ids 2, 3, AND 4. No task/content branching anywhere
  in the measurement path.
- **T5 (order-blindness control):** full reversal of a fresh synthetic blob
  (10,000 bytes) → id 2 withholds (weighted sums differ hugely),
  id 3 admits (sums collide). The mechanism that fixed the 100 Class-A
  corpus pairs works on never-seen synthetic bytes.
- **T2 (identical input):** same blob → admit on all ids. Sanity.
- **Corpus-level:** one mechanism fixed Class A (permutation, motiondir) AND
  Class B (exact-sum collision on distinct content, colordisc) — different
  tasks, different miss causes, different byte relationships. No per-index,
  per-task, or per-cause logic.

**Verdict: holds.** The fix is a general measurement property
(order-sensitivity), not a corpus-pattern bridge.

## Class-B separation — explicit empirical verification (per autopsy note)

The autopsy requires the replacement judgment to separate seq 135
empirically, not by assumption. From the actual pair bytes (independent
Python computation, matching the instrument's ledger judgments exactly):

- `span_sum(F) = span_sum(G) = 2,872,404` — EXACT collision confirmed
  (matches the autopsy's byte anatomy: warm illuminant preserves per-pixel
  channel sum 374). Legacy id 3: jf=jg=359050 → ADMIT (miss reproduced).
- `span_seq(F) = 901,501,636`, `span_seq(G) = 902,139,076`,
  |ΔW| = 637,440 — the pixel byte values genuinely differ at the same
  positions, so position weighting sees them. Primary id 2:
  jf=112,687,704 vs jg=112,767,384 → WITHHOLD (ledger wh=1).
- FNV id 4: digests differ → WITHHOLD (ledger wh=1).

The ÷8 tolerance was never load-bearing for this pair: the sums are exactly
equal, and the weighted sums differ by 637,440 — nearly 80,000× the
tolerance window.

## Honest residual ceiling

- **This frozen corpus:** 100% — no misses remain under id 2 or id 4; the
  full 101-row autopsy regression list separates.
- **Adversarial expansion (round 2, 352 frozen pairs):** id 2 misses
  104/312 DIFFERENT pairs by three exact-collision mechanisms (see
  "Frozen adversarial instances" below); id 4 holds 312/312. The weighted
  sum's "does not happen by chance" claim is now bounded: unmeasured
  outside the two frozen corpora, and a motivated constructor defeats it
  at will.
- **Byte-level adversary:** `span_seq/8` forgeable (attacks 1–2 plus three
  corpus families); FNV raises the bar substantially but is
  non-cryptographic. A cryptographic digest would be needed for a
  tamper-evidence claim — out of scope for this fix.

## Frozen adversarial instances (expansion corpus, round 2)

The synthetic probe attacks above are now joined by FROZEN, committed
instances — `push100/expansion/` (commit `794021e7`, frozen before any gate
measurement). The fix1 driver `fix1/xp_measure.zag` (real `sp_gate_judge`,
fixed candidate) confirms the variant's behavior on each:

- **Family 8 (`wsumcol`, 24 pairs) — SUCCEEDED against the primary by
  construction.** 3-cycles at arithmetic-progression positions with
  midpoint values (2y = x+z) give ΔW = d(x+z−2y) = 0 EXACTLY, so both the
  plain and the weighted sums collide exactly while 12 bytes change value.
  Confirmed: id 2 admits 24/24, id 3 admits 24/24, id 4 withholds 24/24.
  Full proof in `expansion/FAMILIES.md`.
- **`fshuffle` (48 pairs) — equal-mass block permutation.** All 8 frames
  carry byte sum 7532; the linear position weight cannot see permutations
  of equal-mass blocks (Σₖ 384·k·M is permutation-invariant when all
  Mₖ = M). Confirmed: id 2 admits 48/48, id 4 withholds 48/48.
- **`pxperm` colordisc/colorconst (32 pairs) — channel-complementary
  2-valued permutation.** Pixel values (200,30,30)/(30,30,200): each swap
  contributes a position-independent Δ = ±340, pairing to exactly 0.
  Confirmed: id 2 admits 32/32 (shapetrans 16/16 separate), id 4 withholds
  48/48.
- **Calibration (`calib`, 40 pairs):** 7a byte-identical 20/20 admit on all
  variants; 7b single-byte ±1 probes — id 2 admits **0/20**, id 3 admits
  14/20, id 4 admits 0/20. The weighted variant has no tolerance benefit
  over exact comparison (a ±1 change at position i ≥ 7 always flips /8).

Verdict: the red team's "forgeable" verdict on `span_seq/8` is confirmed
by frozen corpus evidence, not just synthetic probes. The FNV variant
withstands every constructed instance (312/312 DIFFERENT withhold).
- **Autopsy reconciliation — RESOLVED.** The round-1 autopsy confirmed
  101/101 genuine should-withhold misses with zero correct admits; the
  preliminary "possibly correct admit" hypothesis for the truth=SAME pair
  is refuted. The regression target is clean and fully met.
