# F33 SRS — build & run log (2026-09-25)

## Pins
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Inputs: `training/features/features.tsv` (5,240 rows; sha256
  `4682190c…e65a897d` — prereg `…e65e897d` is a one-char typo, file is frozen/correct).
- Harness modules (7): copied byte-identical from frozen `training/src/`
  (R33_NATIVE_SHA256_V2/IO, dlb_util, dlb_json, dlb_cfg, dlb_ledger, dlb_delib).

## Sources
- `src/train_f33.zag` — single-pass trainer; emits `mt_f33_params.zag` +
  per-row training TSV. []u8 arenas + LE accessors; no `as []i32`; no `zalloc`;
  `_zag_arg` read unconditionally (no argc gate, ZNC-2026-09-21-007).
- `src/policy_f33.zag` — M4 release logic untouched; conf replaced by
  C*+Σδ−π; per-leg deterministic state `.f33state_{A,B}.tsv`; cert `f33-srs`.
- Two pre-build fixes: (1) trainer emitted conf with δ updated in the same
  step — reordered to emit-then-update per the frozen mechanism; (2) i32/i64
  coercions made explicit.
- `params/FROZEN_HYPERPARAMS.md` written before first run.

## Builds (A/B, separate clean trees)
- Trainer: both rc=0, 162,009 bytes, byte-identical.
- Policy: both rc=0, 176,319 bytes, byte-identical,
  sha256 `c2e2e908141373597226103900f3430a65b9951c533d618f3bbd36dadbee7a06`.

## Training (twice)
- `train_bin features.tsv mt_f33_params_{a,b}.zag logs/train_f33_{a,b}.tsv`,
  rc=0/0. Params byte-identical, logs byte-identical, nrel=4222.
- Independent Python replica (`analysis/replica_f33.py`) reproduces all 20
  key rows exactly (n,k,cstar,δ per d_idx).
- §5: 33/120 cells δ≠0 (27.5%≥10% ✓); cap binds 2/120 (1.7%<25% ✓);
  ledger moved on 7 keys ✓. Mechanism LIVE.

## Eval (37-leg battery, gate 0)
- Wrapper `build/run_eval_f33.sh` wipes `.f33state_{A,B}.tsv`, then frozen
  `run_eval.sh f33full <policy_bin> 33 0`.
- 37/37 legs PASS; A/B TSVs byte-identical; M4 refs copied; B9 5240/5240.
- Frozen `analyze.py` (mech 33 vs 4): V1=0 V2=174 Gviol=12.
- `killbars_f33.py`: B2/B3/B13 FAIL; falsifiers (a) clear (b) clear (c) clear-by-intent.
- `v2_decompose.py`: 174/174 V2 from π-drop (Δcum δ ≤ 0 on every pair).

## Verdict
KILLED — B2, B3, B13; failure mode (9) relief theater (new) + (1) contributory.
See VERDICT.md. No §6 horizon run.

## Artifacts
- `params/mt_f33_params{,_a,_b}.zag`, `logs/train_f33_{a,b}.tsv`,
  `logs/eval_f33full.log`, `analysis/{analyze_33_4.txt,killbars_f33.out,
  replica_f33.py,falsify_f33.py,killbars_f33.py,v2_decompose.py}`,
  `build/{trainbuild,polbuild}_{a,b}`, `build/policy_bin`, `build/run_eval_f33.sh`.
- Eval TSVs: `training/results_f33full/` (outside fork dir, per harness convention).
