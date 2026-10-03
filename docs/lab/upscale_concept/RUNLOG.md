# RUNLOG — upscale concept probe → teach → re-probe (2026-09-26)

All runs: `src/uprobe_bin` (pure Zag, zero RNG). Every stage ran TWICE;
byte-identity verified with `diff -r` + sha256 on all outputs.

## 1. Fixture generation

`gen_fixtures.py` (deterministic; no RNG) wrote 56 PPMs + `fixtures/SHA256SUMS`.
Two fixture-design corrections were made during the EXPLORATORY phase
(before teach; probe-before used non-binding bars):

1. **Translational symmetry.** First fixtures SAD-tied at multiple offsets
   (checkerboard periods + hash grain conspired) → M2a ambiguous. Fix: +x//2
   non-periodic gradient in every synthetic image. Verified: unique peak
   (0,0), next-best SAD 778 vs 0.
2. **v_invent targeting.** First version perturbed block means (cross-caught by
   F2/F3). Fix: zero-mean per 2×2 block → targets F4 only. Amplitude raised
   30→60 (set A) / 25→50 (set B) after F4 missed ±30 stripes on textured
   images — the violator must be an unambiguous instance of fabricated detail.
   Causal order kept clean: bars are taught from TRUE PAIRS ONLY; violator
   design never fed back into bar values.

## 2. Probe-before (exploratory bars: on×4, bar3=2000, bar4=2000)

4 cases × 2 runs. All byte-identical. Result: correct ACCEPTed 4/4; all 16
violators REJECTed, each by its target feature (v_shift→F2, v_invent→F4,
v_object→F3, v_dims→F1). Machinery discriminates → proceed to teach.

## 3. Teach (TNN intake: survey → affinities → commit/revert → knowmap)

2 runs, byte-identical (`diff -r` clean).

| pair | m1 | peak | unique | resid×1000 | q×1000 |
|------|----|------|--------|------------|--------|
| 0 | 1 | (0,0) | 1 | 0 | 498 |
| 1 | 1 | (0,0) | 1 | 0 | 531 |
| 2 | 1 | (0,0) | 1 | 0 | 716 |
| 3 | 1 | (0,0) | 1 | 0 | 510 |

Affinities unanimous → **4/4 features COMMITTED, 0 reverted.**
Knowmap (`work/teach1/concept_knowmap.bin`, 8×i64 LE):
`[1,1,1,1, 2000, 1432, 4, 1]` — F4 bar **1432 = 2 × 716**, derived from measured
data, not crew-set. (F3's 2000 is the frozen prereg predicate.)

## 4. Probe-after (held-out; TAUGHT knowmap only)

4 held-out cases (incl. real GT crop) × 2 runs. All byte-identical.

| case | correct | v_shift | v_invent | v_object | v_dims |
|------|---------|---------|----------|----------|--------|
| 0 (heldout synth) | ACCEPT q=498 | REJECT F2 peak=(0,1) | REJECT F4 q=10696 | REJECT F3 r=7700 | REJECT F1 |
| 1 (heldout synth) | ACCEPT q=518 | REJECT F2 peak=(1,0) | REJECT F3+F4 r=2084 q=1496 | REJECT F3 r=11250 | REJECT F1 |
| 2 (heldout grain) | ACCEPT q=648 | REJECT F2 peak=(0,−1) | REJECT F4 q=3557 | REJECT F3 r=5126 | REJECT F1 |
| 3 (real GT crop) | ACCEPT q=868 | REJECT F2 peak=(−1,0) | REJECT F4 q=3514 | REJECT F3 r=5395 | REJECT F1 |

Injected shifts were (0,+2),(+2,0),(0,−2),(−2,0) hi-res px → measured low-res
peaks (0,1),(1,0),(0,−1),(−1,0): M2a not only rejects but **identifies** them.

## 5. Incidents

- `nio_open_root` on a nonexistent bars dir crashed the binary (rc=234) instead
  of a clean error. Root cause was a missing `prereg_bars/` dir (my omission),
  but the crash-on-missing-dir is a robustness bug in the substrate path —
  recorded, not fixed in this task's scope.
- A stale `uprobe_bin` from a failed first build caused one confusing crash;
  resolved by clean rebuild. Lesson: `rm -f` the binary before rebuilding
  after a compile error.

## Evidence locations (in repo commit)

- `src/uprobe.zag`, `src/build.sh`, `gen_fixtures.py`
- `fixtures/` (56 sealed PPMs + SHA256SUMS), `prereg_bars/exploratory_bars.bin`
- `evidence/teach_trace.txt`, `evidence/concept_knowmap.bin`
- `evidence/probe_before_case{0..3}.txt`, `evidence/probe_after_case{0..3}.txt`
  (verdict + measurement traces, run 1 of the byte-identical pair)
