# G1 Build Log — Symmetry Group Percept (SGP)

## Frozen Prereg

Committed alone 2026-09-22: `6a156c796a48676e6c7d0c38256e8b7c8b236de3`
Parent: `f3656c8aad14`
File: `docs/lab/senses/pam-rebuild/forks/G1/PREREG_G1.md`

## Source

`sense.zag` (~1,225 lines, pure Zag, zero RNG):
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` (imports)
- Six task kernels: colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir
- 512-bit percept: 256b generator codes + 256b fixed-point coords
- Hash-chained ledger, first-per-class anchors, 1%-variance contract (≤5 bits)
- CLI: approach, task, judgment, confidence, ops, percept (128 hex), disposition, variance, anchor, ledger_hash

## Build

```bash
cd ~/workspace/tnn-lab/senses/pam-rebuild/forks/G1/src
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  sense.zag --no-zagd --no-analyze --no-foreground-cache \
  -o ~/workspace/tmp_g1build/sense
```
Output: 155,071 byte native binary. Zero RNG in any decision path (verified by code inspection; no `_zag_random` or equivalent calls).

## Bugs Fixed During Build

1. **Ledger hash off-by-one**: `hp < lp - 70` → `hp + 70 <= lp` (bound check).
2. **Timbre normalization**: divided by 10^12 → 10^6 (integer overflow in profile computation).
3. **Shape symmetry denominator**: total-pixels → IoU over shape union (prereg said "per-mille self-match", total-pixels made all transforms score ~950+).
4. **Shape rotation rounding**: truncating → round-half-away-from-zero via `rdiv1000()` (minimal improvement).

## Bugs NOT Fixed (Frozen Design)

1. **Shape mask**: "threshold at mean" captures photo background, not shape. On 90 real fixtures, mask is background 80%+ of time. Prereg-frozen; cannot change to fixed threshold.
2. **Shape score thresholds**: 850/880 don't match IoU distribution (circle full=859, triangle full=570). Prereg-frozen.
3. **Motiondir**: centroid of changed pixels fails on photographic backgrounds (systematically wrong directions). Copied from Approach A (which also gets 41.7%).

## Test Results

### B1: Mean viability 62.9% (PASS ≥60%)
- colordisc: 68.3% (60 fixtures)
- colorconst: 57.5% (40)
- shapetrans: 33.3% (90) — chance, mask broken
- pitchdisc: 85.0% (60)
- timbredisc: 100% (60)
- motiondir: 33.3% (60) — chance, tracker broken

### B2: Head-to-head 66.3% agreement (445 fixtures, G1 vs A)
Both run on identical fixtures (370 primary + 75 G1-adv).

### B3: Ops/bytes
- colordisc: 16,384 ops
- colorconst: 16,384 ops
- shapetrans: 29,952 ops
- pitchdisc: 2,671,680 ops (DFT)
- timbredisc: 1,335,968 ops (DFT)
- motiondir: 28,674 ops
- Binary: 155,071 bytes
- Percept: 64 bytes (512 bits) vs MB raw input

### B4: Contract changes 84% of adversarial decisions (PASS ≥10%)
- 63/75 differ between contract and ablated (confidence≥500)
- False installs: 41 (ablated) → 6 (contract). Contract helps, but not enough.

### B5: Adversarial false-install 54.5% per-install (FAIL ≤5%, KILL)
- 6 false installs out of 11 installs (75 G1-adv fixtures)
- Per-fixture: 8% (6/75)
- Root cause: 5-bit Hamming threshold too loose. CHROMA_3 (0x43) vs CHROMA_4 (0x44) differ by 3 bits. Different generators look "matching" to the contract.

### B6: Three byte-identical runs (PASS)
- Runs 1, 2, 3: 445 fixtures each, 0 errors
- All outputs byte-identical. All ledgers verify (hash chain + disposition replay). Zero problems.

### Retrieval: 57.8% (FAIL ≥80%, KILL)
- Method: exact generator-code agreement vs class anchors.
- Tried: full-percept slots (57.1%), generator-only (57.8%), code-classes (40.8%), symmetry-only (42.6%).
- Root cause: percepts mix symmetry structure (PAIR_MATCH, ROT_90) with instance parameters (CHROMA_5, SPECT_3). Exact matching fails on parameters; coarse matching loses discrimination.

## Kill Verdict: G1 KILLED

**Kill bars hit:**
- B5: 54.5% false-install > 5% → KILL
- Retrieval: 57.8% < 80% → KILL

**What died:** The Symmetry Group Percept as a unified perceptual organ.

**Why:**
1. The 1%-variance contract (frozen) is not strict enough. The Hamming distance on raw code bits doesn't reflect semantic distance. Two different hues are 3 bits apart; the contract sees them as "matching."
2. The percept design (frozen) conflates group structure with instance data. Retrieval can't work when "CHROMA_5" and "CHROMA_3" are different codes — the group alignment has nothing to align.
3. The frozen shape mask and motion tracker don't work on real photographic data. The symmetry idea is sound, but the frozen segmentation/tracking mechanisms are not.

**What survived (honest):**
- B1 62.9%: The symmetry approach works for audio (pitch 85%, timbre 100%) and decently for color (68%, 58%).
- B4: The contract DOES change decisions (84%) and DOES reduce false installs (41→6). It's just not strict enough.
- B6: Determinism is perfect. Zero RNG, byte-identical reruns, verified ledgers.

**The honest lesson:** Strict symmetry matching does NOT destroy recall (B1 passes). But the frozen 5-bit threshold is too loose to prevent false installs, and the percept's mixing of structure/parameters breaks retrieval. The IDEA (group-theoretic percepts) is elegant and works where the symmetries are clean (audio). The FROZEN IMPLEMENTATION (masks, thresholds, code design) fails on real visual data.
