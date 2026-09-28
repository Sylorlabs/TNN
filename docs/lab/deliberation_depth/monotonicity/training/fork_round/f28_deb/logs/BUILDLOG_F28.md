# F28 DEB — build log

Fork 28, mechanism 28. Frozen authority: PREREG_FORKROUND.md §3 (F28) +
`ideas/fable_forks.md` Mechanism A (authoritative on mechanism detail).
Repo: sylorlabs/TNN, branch tnn-native-lab, frozen v2.
Coordinator: parent orchestrator. Date: 2026-09-24.

## Frozen inputs
- PREREG_FORKROUND.md FROZEN v2 (coordinator sign-off 2026-09-25).
- features.tsv SHA256 verified on disk:
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  (5240 cells) — matches the §2 pin (v2 typo fix).
- Toolchain (pinned only): ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1,
  SHA256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Harness modules: 7 files from `training/src/` copied into `src/`
  byte-identical (SHA-verified per file, 7/7 OK):
  R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag, dlb_util.zag,
  dlb_json.zag, dlb_cfg.zag, dlb_ledger.zag, dlb_delib.zag.

## Mechanism as frozen (§3 + ideas file)
- budget_0 = 1000
- budget_t = clamp(budget_{t-1} + margin_t*(1000/nh) − t*1000/64, 0, 1000)
- C = clamp(min(budget_t, clamp(margin_t*1000/nh, 0, 1000)), 0, 1000)
- All integer fixed-point (thousandths); integer division truncates toward zero.
- margin_t = per-depth margin observable = clamp(hist_m[t], 0, 1000), the
  frozen §4 feature-f1 observable (deliberation margin = leader score minus
  runner-up score). Margins are non-negative by construction.
- nh = per-item hypothesis count (it.nh): admit 9, revoke 6, logic 3,
  trap 2, cost 2, ceiling 2, redteam 3. (Ideas file: "nh = 64 (or the actual
  hypothesis pool size known at compile time)"; task brief resolves to the
  hypothesis count.)
- t ranges over deliberation rounds 1..t_eff ("for each depth t ≥ 1",
  raw transcript), t_eff = min(leg depth, st.rounds) — the M4
  effective-depth convention. Per-item cross-depth state is reconstructed
  from the deliberation margin history within each leg, so the per-leg
  driver is exact and stateless across legs (no on-disk state; A/B
  byte-identical trivially).
- Depth-charge coefficients (t*1000/64) are STRUCTURAL constants — never
  fitted, never increased. F28 has NO fittable parameters and NO training
  phase (prereg §5: non-training forks skip the training checkpoint; §5b
  TRAIN-COORD repair applies to F24–F27 only — coordinator-confirmed in
  the task brief: "it is structural"). No optimizer choice to record.

## Scaling analysis (pre-eval, from frozen features)
- Observed margin (f1) means: admit 938.5, revoke 740.7, logic 562.1,
  trap 572.1, cost 908.0, redteam 706.7, ceiling 697.4 (max 1000, zero zeros).
- Replenishment per round = margin_t*(1000/nh) ≥ 1*111 = 111 (admit, nh=9)
  and up to 1000*500 = 500000 (trap/cost/ceiling, nh=2).
- Charge per round = t*1000/64 ≤ 1000 (t=64).
- Since margins are in the hundreds, replenishment exceeds charge by 2–3
  orders of magnitude at every round: the budget pins at 1000 after the
  first round and never depletes. The head therefore reduces to
  C = clamp(margin_t*1000/nh, 0, 1000), which saturates at 1000 for
  margin_t ≥ nh — i.e. on essentially every released cell. This is the
  mechanism's honest structural behavior under the frozen formula, and it
  is what kill-bar (b) (clamp attractor, FM1) operationalizes. The eval
  measures it rather than asserting it.

## New sources (this fork)
- `src/deb.zag` — shared DEB head: deb_clamp, deb_budget, deb_conf.
  []u8 arenas + au_get64 LE accessors only; no `as []i32` casts
  (ZNC-2026-09-21-007); no fn named zalloc; no slice > 2^25 bytes;
  no bare `{...}` blocks; struct literals dot-prefixed.
- `src/policy.zag` — per-leg eval driver: frozen deliberation + M4
  release skeleton (release L_t iff L_t == L_1) + deb_conf head.
  gate01 accepted (0/1) and IGNORED — F28 has no gate. cert "deb-budget".
  TSV columns identical to mech.zag. Struct field reads through *DSt/*Item
  params only (ZNC-004/010-safe; mirrors f20's proven patterns).
- `src/probe.zag` — budget-pinning measurement probe sharing deb.zag
  (same budget the eval uses): per item emits
  id/depth/t_eff/nh/budget_final/margin_teff/rounds.

## Gates honored
- Pure Zag, zero RNG (fixed file order, integer arithmetic).
- A/B byte-identical builds: policy_f28_a/b cmp identical
  (SHA256 d3b6864aed1fed40cf89951fe59c9c90c4eba032c1492dd4c0f6370655d95d75).
- No training → no ×2 training determinism check needed (nothing to fit).
- No binaries or .zagd committed (build/ and *.zagd excluded from commits).

## Eval
- `run_eval.sh f28full <build/pol_a/policy_f28_a> 28 0` — 37 legs × A/B.
- `analysis/killbars_f28.py` — fork-round bars (B8 amended §4b), NEC m9
  deltas, F28 falsification triggers (a)/(b)/(c).
- Probe battery over all 37 legs → budget-pinning fractions per leg.
