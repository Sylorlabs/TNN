# VERDICT.md — T2-SPEEDINTEL (replacement crew)

**Verdict: REPRODUCED**

## 1. Frozen claims checklist (quoted verbatim from the frozen prereg — authoritative)

From `docs/lab/crossref/PREREG_TIER2.md`, T2-SPEEDINTEL section, at frozen pin
`7b2100d09911c5c10252c5756c7def288e70bd1f` (blob SHA `b1178370036bffbda6eb68ea0989c0e427dc31b7`):

> T2-SPEEDINTEL — speed-intelligence exchange rate: 2× is the knee (Type A)
>
> **Claims:** measured, frozen prereg, pure Zag, byte-identical: 1× deliberation starved (6/18 coding, 29/94 epistemic — ~2× cost per quality point vs the knee); 2× is the knee (18/18 coding, 59/94 epistemic); 4×/8× add nothing (18/18, 59/94, confirmed on a fresh battery); 2× + free-speed mechanisms reaches knee quality at ~2/3 the eval cost of naive 1× (65.1% fewer evals, 37.8% fewer compiler calls). Micah's ruling: 2× + free-speed = winner; 4×/8× dropped; quality-first, never trade quality for speed.
>
> **Method:** rerun the 1×/2×/4×/8× battery from committed sources in clean checkout (frozen prereg; crew freezes the pin); ≥3 byte-identical runs.
>
> **Rule:** REPRODUCED if the (6/18, 29/94) → (18/18, 59/94) → flat table reproduces cell-for-cell; NOT REPRODUCED if 4×/8× buys anything or 2× misses the knee.

**Decision rule applied:** REPRODUCED iff the (6/18, 29/94) → (18/18, 59/94) → flat table
reproduces cell-for-cell; NOT REPRODUCED iff 4×/8× buys anything or 2× misses the knee.

## 2. Measured table vs frozen table (cell-for-cell)

### Coding (battery_si.json, budgets 2/4/8/16 iters = 1×/2×/4×/8×, 3 reruns each)

| budget | Q_c frozen | Q_c measured | iters f/m | znc f/m | 1st-try | honest halt | canonical digest | reruns |
|---|---|---|---|---|---|---|---|---|
| 1× (2) | 6/18 | **6/18** | 32/32 | 25/25 | 6/18 | 2/2 | 009ecfed27255a63… match | IDENTICAL |
| 2× (4) | 18/18 | **18/18** | 46/46 | 27/27 | 6/18 | 2/2 | 9f1281364907d349… match | IDENTICAL |
| 4× (8) | 18/18 | **18/18** | 46/46 | 27/27 | 6/18 | 2/2 | 68fb53a6581b38b4… match | IDENTICAL |
| 8× (16) | 18/18 | **18/18** | 46/46 | 27/27 | 6/18 | 2/2 | d218ef3707fbe309… match | IDENTICAL |

(znc counts here are Arm 1's exclusive count, as in the frozen table.)

### Epistemic (frozen 94-item battery, budgets 1/2/4/8, 3 reruns each)

| budget | total frozen | total measured | false/true | mean preds/item f/m | recon/vflips | reruns |
|---|---|---|---|---|---|---|
| 1× | 29/94 | **29/94** | 12/12, 12/12 | 3.000/3.000 | 0/0 | IDENTICAL |
| 2× | 59/94 | **59/94** | 12/12, 12/12 | 9.000/9.000 | 0/0 | IDENTICAL |
| 4× | 59/94 | **59/94** | 12/12, 12/12 | 9.319/9.319 | 0/0 | IDENTICAL |
| 8× | 59/94 | **59/94** | 12/12, 12/12 | 10.319/10.319 | 0/0 | IDENTICAL |

Per-family (weird-English /10) at 2×/4×/8×: joke 5, sarcasm 3, hypothetical 5,
analogy 3, counterfactual 9, poetry 5, implicature 5 — identical to frozen.
All 12 committed raw outputs (`epi/out_b*.txt`) reproduced **byte-identically**
with a fresh build.

### Epistemic — fresh disjoint battery (ADDENDUM SI-A1 resolution)

Generator re-run: deterministic, output **byte-identical** to the committed fresh
items (construction audit F 0/12, W 35/70 as committed).

| budget | total frozen | total measured | mean preds f/m | recon | reruns |
|---|---|---|---|---|---|
| 1× | 29/94 | **29/94** | 3.000/3.000 | 0 | IDENTICAL |
| 2× | 59/94 | **59/94** | 9.000/9.000 | 0 | IDENTICAL |
| 4× | 59/94 | **59/94** | 9.330/9.330 | 1 | IDENTICAL |
| 8× | 59/94 | **59/94** | 10.330/10.330 | 1 | IDENTICAL |

Resolution rule: gain(1×→2×)=31.9pp > 10pp ✓; gain(2×→4×)=0 ≤ 1pp ✓;
gain(4×→8×)=0 ≤ 1pp ✓ → **PLATEAU-CONFIRMED reproduces** exactly as frozen
(RESULTS_A1R.md).

### Exchange rate — Arm 4 (SI battery @ knee budget 4, inclusive znc counts, 3 reruns each)

| budget × mechanism | Q_c f/m | iters f/m | znc f/m | hyp-evals f/m | reruns |
|---|---|---|---|---|---|
| 1× baseline (budget 2) | 6/18 / **6/18** | 32/32 | 31/31 | 121/121 | IDENTICAL |
| knee baseline (budget 4) | 18/18 / **18/18** | 46/46 | 45/45 | 129/129 | IDENTICAL |
| knee + 3a prune | 18/18 / **18/18** | 46/46 | 45/45 | 43/43 **(−66.7%)** | IDENTICAL |
| knee + 3b branch-and-bound | 18/18 / **18/18** | 46/46 | 45/45 | 91/91 **(−29.5%)** | IDENTICAL |
| knee + 3c precheck | 18/18 / **18/18** | 46/46 | 28/28 **(−37.8%)** | 129/129 | IDENTICAL |
| knee + all winners | 18/18 / **18/18** | 46/46 | 28/28 **(−37.8%)** | 45/45 **(−65.1%)** | IDENTICAL |

Committed analyzer (`work_a4/analyze.py`) on my runs: 3a 28/28 diagnose winners
byte-identical; 3b 28/28; combo 25/25 evidence-matched + the same 3 characterized
PRECHECK divergences (S03→DUPFN, S05→TYPE, S06→TYPE scored NAME=7, trajectories
reconverge — identical to the frozen characterization); outcome equality vs
baseline IDENTICAL; precheck false-positive validation **0/51** on b4_c and b4_combo.
si4none sanity cell (manual, driver_si4 --mech none ×3): 18/18, 46 iters, 45 znc,
129 evals, IDENTICAL ×3, 28/28 diagnose winners identical to b4_none.

Gate battery 6/6 (REFUSE G1/G2/G4/G5 + 2× ALLOW) on all three rebuilt binaries:
work_a1/learner, work_a3/learner_si3, work_a4/bin/learner_si4.

## 3. Verdict justification

- The (6/18, 29/94) → (18/18, 59/94) → flat table reproduces **cell-for-cell**
  on coding and epistemic, including canonical digests (coding) and raw-output
  byte-identity (epistemic), all ≥3 runs byte-identical.
- 4×/8× buy nothing on either domain (frozen battery AND the fresh disjoint
  battery, whose generator is itself deterministic and reproduces its committed
  items byte-identically).
- 2× holds the knee on both domains: no NOT-REPRODUCED trigger fired.
- The exchange-rate claim holds: knee + all winners = 18/18 at 28 znc (−37.8%)
  and 45 hyp-evals (−65.1%), quality byte-identical, FP=0.

## 4. Method and environment deviations (declared, not hidden)

1. **No full git clone possible.** Large transfers (full clone, codeload tarball)
   stall/timeout on this VM (3 attempts, >180s each, no progress). Substituted:
   fetched the 27 needed committed files individually via the authenticated
   GitHub API at the frozen pin and verified **every file's blob SHA1 against
   the commit's recursive tree listing** (content-addressed integrity, 27/27).
   Frozen pin `7b2100d09911c5c10252c5756c7def288e70bd1f` verified to exist with
   the expected crossref commit message before any run.
2. **R33 substrate files were never committed.** `delib_si.zag`'s imports
   (`docs/lab/prose-learning/epistemic_wave/src/R33_NATIVE_IO_V1.zag`,
   `R33_NATIVE_SHA256_V2.zag`) resolve to a path absent at both the SI results
   commit (43eceed21) and the frozen pin (verified via API tree queries).
   Substituted the canonical in-lab copies: under `docs/lab/` all 41 copies of
   the IO file are one variant (a6b440d2) and all 37 copies of the SHA256 file
   are one variant (5dd858fa) — unambiguous. `delib_si.zag` uses only
   nio_alloc/nio_close/nio_open_child/nio_open_root/nio_read_exact from the IO
   file. Behavioral proof: all 12 committed `out_b*.txt` epistemic outputs
   reproduce **byte-identically** with the fresh build against the substituted
   files. The deliberation logic under test is the committed `delib_si.zag`
   verbatim; the R33 files are IO/SHA256 plumbing.
3. `work_a1r/delib_si.zag` was not re-fetched (blob SHA at the pin is identical
   to `work_a1/delib_si.zag`, 0c7be2e8d8); the verified work_a1 copy was used.
4. All builds used the pinned znc (`znc_linux_x86_64_abed8aa1`) with
   `--no-analyze --no-zagd` (no .zagd caches, no binaries committed).
   All drivers/scorers re-verified plumbing-only (no `re` import, no
   error-class keywords in drivers; scoring scripts use `re` only to parse the
   delib binary's own output format).
5. Zero RNG in all paths; scratch under `~/workspace/scratch-crossref/T2/`
   only (never /tmp). Predecessor's corrupt clone was removed and recorded in
   RUNLOG.md; nothing valid was inherited.

## 5. Frozen pins

- Cross-reference frozen pin: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (sylorlabs/TNN, branch tnn-native-lab)
- PREREG_TIER2.md blob at pin: `b1178370036bffbda6eb68ea0989c0e427dc31b7`
- SI frozen prereg commit (referenced by results): `43eceed2100c73b1b065f0685644d171a5837a4a`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 6. Files

- Run dir: `~/workspace/scratch-crossref/T2/SPEEDINTEL/crew/`
  (VERDICT.md, RUNLOG.md, fetch/getr33 scripts, runroot/ scratch tree)
- Full-tree manifest at pin: `~/workspace/scratch-crossref/T2/SPEEDINTEL/fulltree.json`
- Extracted prereg section: `~/workspace/scratch-crossref/T2/SPEEDINTEL/t2-speedintel-section.txt`
