# SPEED-WINNER PROMOTION — FROZEN PREREGISTRATION

**Date frozen:** 2026-09-22 · **Authority:** Micah — "Take the free lunch."
(speed winners → main defaults)
**Branch:** `tnn-native-lab` · **Dir:** `coding/reflection/speed_intel/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 0. What this promotes (frozen evidence)

Source prereg: `43eceed2100c73b1b065f0685644d171a5837a4a`;
synthesis: `3314fc1fdd6fb45ec4d73169817cc9820ce520a1`.
Five items become MAINLINE defaults (not variants):

| # | Promotion | Source file (mainline) | Change |
|---|---|---|---|
| P1 | 2× deliberation budget as default | `coding/reflection/loop/driver.py` | `--budget` default 6 → **4** (Arm 1 knee: 18/18 coding, 59/94 epistemic; 4×/8× add nothing) |
| P2 | Dead-branch pruning (3a) + one-brain branch-and-bound (3b) always-on | `coding/reflection/loop/learner.zag` `diagnose` | Port the Arm 4 combo path (`speed_intel/work_a4/learner_si4.zag`, mask "ab" behavior: prune first, then B&B over the pruned survivor set via `bnb_stop`) as the default diagnose path. Diagnose winners proven byte-identical to full evaluation (28/28). |
| P3 | Fail-fast compiler prechecks (3c) always-on | `coding/reflection/loop/driver.py` | Port precheck routing from `speed_intel/work_a4/driver_si4.py`: before each znc invocation ask the learner `precheck <spec> <src>`; `PRECHECK FAIL` → route to `diagnose` as evtype=PRECHECK with the learner's reason text VERBATIM, skipping znc; `PRECHECK OK` → compile. Sentinel-style first-line routing only — the driver classifies nothing (INTERFACE.md grep law must still hold). |
| P4 | Indexed KB recall as default | `coding/reflection/kb/src/kb_install.zag`, `coding/reflection/kb/src/kb_main.zag` | Port index build (from `speed_intel/work_a2/kb_install_si.zag`; kb.dat stays byte-identical) and indexed recall (from `speed_intel/work_a2/kb_main_si.zag`). `kb_install <txt> <kbdat> [idxpath]` (default `<kbdat>.idx`); `kb_main` auto-uses `<kbpath>.idx` when present and loadable, else flat fallback (results proven 24/24 byte-identical either way). Explicit `flat` escape hatch retained. Honest break-even: 574 queries (39,870-comparison one-time build; −69.5 probes/query). |
| P5 | Epistemic 2× confirmed as the mainline default | `prose-learning/epistemic_wave/speechact_exp/delib_sa.zag` | NO code change expected: arm=2 (full pipeline) is already the 2× knee. Confirm the default invocation path uses arm=2 and document it. 4×/8× reconsideration+verification are NOT promoted (Arm 1: 0 recon fired, 0 vflips, ΔQ=0). |

Explicitly NOT promoted: Arm 2b memoization (FAIL), 2c fast paths (FAIL),
epistemic 4×/8× (no gain), any 4×/8× budget.

## 1. Escape hatches (reversibility without code revert)

- Driver: `--no-precheck` disables P3; `--budget` remains overridable.
- Learner `diagnose argv[9]`: absent or `"ab"` → combo default; `"classic"` →
  the old full-evaluation path (used for the regression control below).
- KB: `kb_main ... flat` forces flat recall.
These are the runtime rollback path; the code rollback path is §6.

## 2. Regression batteries (frozen)

- **Coding:** `coding/reflection/speed_intel/work_a1/battery_si.json`
  (20 items: 18 fixable + X3/X4 unfixable). Control FIRST (before porting):
  old defaults (`--budget 6`, classic path, no precheck) ×3 reruns.
  Then new defaults (`--budget 4`, combo + precheck) ×3 reruns.
- **KB:** `coding/reflection/kb/tests/specs.txt` 24-spec battery via
  `kb/bin/run_recall.py`: flat (pre-promotion binaries) vs indexed
  (post-promotion, default path) — 24/24 family selections must be
  byte-identical; record probes/query before/after.
- **Epistemic:** frozen 94-item set via `delib_sa.zag` arm=2, ×3 reruns.

## 3. Metrics and verdict rules

Per condition: pass rate, honest-halt rate (coding 2/2), iterations, znc
invocations, hyp-evals (coding), probes/query (KB), wall-clock, and the
sha256 of the canonical (timing-free) log.

- **PASS (promote):** coding 18/18 + 2/2 halts in BOTH conditions
  (identical quality tables); KB 24/24 selections byte-identical;
  epistemic 59/94; 3 reruns byte-identical canonical logs in every
  condition; zero RNG in the promotion path (pure Zag reasoning/verifying;
  Python glue only); INTERFACE.md grep law still holds for the driver.
- **FAIL (do not promote):** any quality delta between conditions, any
  determinism break, any RNG in a decision path. Roll back per §6.

Wall-clock: measure end-to-end wall-clock for the standard batteries,
old vs new defaults, and report realized savings (no parallelism claims —
single-threaded substrate).

## 4. Determinism and purity

- Zero RNG anywhere in TNN decision paths (standing law).
- All reasoning/verifying in pure Zag; Python only glue.
- 3 reruns per condition, byte-identical canonical logs.
- Binaries and `.zagd` caches are NEVER committed.

## 5. Deliverables

- This prereg (frozen, committed before work).
- Ported mainline sources + updated `loop/INTERFACE.md` (new defaults
  documented) + `kb` docs touched only where behavior changed.
- `PROMOTION_VERDICT.md`: what changed, before/after quality tables
  (must be identical), measured wall-clock savings, rollback procedure.
- Run logs/digests under `speed_intel/work_promo_{loop,kb,epi}/`.
- One commit on `tnn-native-lab` (prereg separate from the promotion
  commit), via `~/workspace/commit_racefree.py` with
  `TMPDIR=~/workspace/tmp_commit`.

## 6. Rollback procedure

1. Runtime: `--no-precheck` + `diagnose ... classic` + `--budget 6`
   (loop); `flat` KB mode; epistemic unchanged (no code change).
2. Code: `git revert` the promotion commit (prereg commit stands).
3. After rollback, re-run the control battery once to confirm 18/18.

## 7. Kill criteria

Promotion is KILLED (not amended) if: quality tables differ in either
direction on the frozen batteries; determinism breaks; the INTERFACE.md
grep law is violated; or wall-clock shows no realized saving AND the
port adds maintenance surface. A PARTIAL never ends a track — a failed
single mechanism (P2/P3/P4 independently) is dropped while the rest
promote, with the drop documented in the verdict.
