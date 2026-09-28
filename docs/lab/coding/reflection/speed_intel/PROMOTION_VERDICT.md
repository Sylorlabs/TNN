# SPEED-WINNER PROMOTION — VERDICT

**Date:** 2026-09-22 · **Authority:** Micah — "Take the free lunch."
**Frozen prereg:** `coding/reflection/speed_intel/PROMOTION_PREREG.md`
(commit `f5154e8c6c7c050388d03b3580f9d17cd6f2858b`, committed BEFORE any
mainline change).
**Source evidence:** prereg `43eceed2100c73b1b065f0685644d171a5837a4a`,
synthesis `3314fc1fdd6fb45ec4d73169817cc9820ce520a1`.
**Pinned toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Verdict: PROMOTE — all five items, all prereg PASS conditions met

## 1. What changed (mainline files)

| # | File | Change |
|---|---|---|
| P1 | `coding/reflection/loop/driver.py` | `--budget` default 6 → **4** (Arm 1 knee) |
| P2 | `coding/reflection/loop/learner.zag` | `diagnose` default path = Arm 4 combo: dead-branch pruning (3a) FIRST, then one-brain branch-and-bound (3b) over the pruned survivor set (`bnb_stop`); winners proven byte-identical to full evaluation. `diagnose argv[9]`: absent/`"ab"` → combo; `"classic"` → old full-evaluation path (escape hatch). `precheck` mode added. |
| P3 | `coding/reflection/loop/driver.py` | Fail-fast precheck routing always-on: before each znc, ask the learner `precheck <spec> <src>`; `PRECHECK FAIL` → route to `diagnose` as evtype=PRECHECK with the learner's reason text VERBATIM, skipping znc. Sentinel-style first-line routing only — the INTERFACE.md grep law verified CLEAN. `--no-precheck` escape hatch. |
| P4 | `coding/reflection/kb/src/kb_install.zag` | Builds the inverted index (purely additive; kb.dat byte-identical, sha256-verified). argv[3] = index path, default `<kbdat>.idx`. |
| P4 | `coding/reflection/kb/src/kb_main.zag` | Indexed recall is the DEFAULT: auto-loads `<kbpath>.idx` when present and magic-valid, else silent flat fallback (proven results-identical). Explicit `flat` mode retained as escape hatch. |
| P4 | `coding/reflection/kb/bin/run_recall.py` | Installs with index by default, recalls in auto mode; `--flat` flag. |
| P5 | `prose-learning/epistemic_wave/speechact_exp/delib_sa.zag` | NO code change: arm=2 (full pipeline) confirmed as the effective mainline default — it IS the 2× knee. 4×/8× reconsideration+verification NOT promoted (Arm 1: 0 fired, 0 flips, ΔQ=0). |
| — | `coding/reflection/loop/INTERFACE.md` | Documents the new defaults: budget 4, combo diagnose + trace conventions, `evals`, `precheck` mode, PRECHECK evidence, driver contract, escape hatches, determinism at budget 4. |

NOT promoted (per prereg): Arm 2b memoization (FAIL), 2c fast paths (FAIL).

## 2. Before/after quality tables (must be — and are — identical)

### Coding (SI battery, 20 items: 18 fixable + X3/X4 unfixable), ×3 reruns

| condition | budget | pass | honest halts | iters | znc | hyp-evals |
|---|---|---|---|---|---|---|
| Old defaults (pre-port control) | 6 | 18/18 | 2/2 | 46 | 45 | 129 |
| **New defaults (combo + precheck)** | **4** | **18/18** | **2/2** | 46 | **28 (−37.8%)** | **45 (−65.1%)** |
| Classic escape hatch (post-port) | 6 | 18/18 | 2/2 | 46 | 45 | 129 |

Determinism: byte-identical canonical logs 3/3 in both conditions
(control `72468b38…`, new `6e6ee2ca…`). Precheck false positives: **0/17**
(all 17 unique precheck-FAIL sources confirmed real compile failures offline).
Zero RNG. INTERFACE.md grep law: CLEAN.

### KB (24-spec battery), ×3 runs each

| condition | selections | compile | test pass | gates |
|---|---|---|---|---|
| Flat baseline (pre-port) | 24/24 | 24/24 | 23/24 | 6/6 |
| **Indexed default (post-port)** | **24/24 byte-identical** | 24/24 | 23/24 | 6/6 |

(The single test FAIL is `o2`, a frozen mainline selection quirk — E-STRREV
over E-SORT — reproduced byte-identically post-port.) kb.dat byte-identical
(`1531fda8…`). Probes/query: 348.0 → 278.5 (**−69.5**); index build 39,870
one-time term comparisons (8,253-byte index); honest break-even **574 queries**.

### Epistemic (frozen 94-item set, arm=2), ×3 reruns

| rep | total | per-family |
|---|---|---|
| 1/2/3 | **59/94** | 12/12 false, 12/12 true, 5/10 joke, 3/10 sarc, 5/10 hyp, 3/10 anal, 9/10 counterfactual, 5/10 poetry, 5/10 implicature |

Byte-identical stdout ×3; matches the frozen RESULTS_SI.md table cell-for-cell
AND the committed arm-2 scored evidence. No code change was needed.

## 3. Measured wall-clock savings (end-to-end, single-threaded)

- **Coding loop, SI battery:** old 66.5/69.7/56.5s (mean 64.2) → new
  53.6/48.9/51.9s (mean 51.5) = **≈ −20%**. (Less than the −37.8% znc saving
  because the loop is dominated by learner-binary invocations, not znc alone.
  Honest note, not a kill: cost-per-quality-point improved at every step.)
- **KB recall, 24-spec battery:** no realized wall-clock saving at 24-query
  scale (56–70s either way; dominated by 72 znc compile+run invocations).
  The win is per-query probe reduction paying back after 574 queries —
  frozen in the prereg, not a kill condition.
- **Epistemic:** sub-second per 94-item run either way (deliberation is free
  relative to the coding loop).

## 4. Rollback procedure

1. **Runtime (no code change):** loop: `--no-precheck --mask classic --budget 6`;
   KB: `flat` mode / `--flat`; epistemic: unchanged (no code change).
2. **Code:** `git revert` this promotion commit (the frozen prereg commit
   `f5154e8c` stands).
3. After rollback, re-run the SI battery control once to confirm 18/18.

## 5. Judgment calls and caveats (all additive, none quality-bearing)

- **Mask remap:** the ported learner maps `s_eq(mask,"classic")` → old path,
  else combo. (si4 used substring tests; "classic" contains "a".) Only
  non-comment change vs the proven si4 code.
- **KB auto-mode** validates the full 7-byte `KBIDX1` magic + bounds guards
  (stricter than SI's); failures route to flat fallback, never changing results.
- **Classic-path trace order:** S03/S09 log DUPFN trace lines before NAME
  (si4's baseline branch order, inherited verbatim). Class/strategy/score/
  hashes/outcomes 20/20 identical — decision-neutral.
- Run evidence: `speed_intel/work_promo_{loop,kb,epi}/` (text logs, metrics,
  digests; binaries and .zagd caches excluded from the commit).

## 6. Kill-criteria check

No quality delta on any frozen battery · no determinism break · no RNG ·
grep law holds · realized savings measured (coding −20% wall-clock; KB
per-query −69.5 probes with frozen break-even). **No kill triggered.**
