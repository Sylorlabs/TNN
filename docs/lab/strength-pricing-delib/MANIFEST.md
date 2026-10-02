# MANIFEST.md — Arm E: DELIBERATIVE DESTRUCTION-PRICING

## Source files (committed)

- `strength_core.zag` — arm-E mechanism: ST_OP_DELIBERATE (22),
  ST_PRICE_DELIB (5), ST_REFUSED_NODELIB (122), deliberation policy,
  personality scopes, st_deliberate / st_deliberate_dryrun, kill-check
  hooks (122 fail-closed, P3 baseline suppressed under DELIB).
- `strength_checker.zag` — independent deliberation verification:
  ck_verify_deliberate (recomputes price+reasons+personality from the
  ledger prefix at each record), ck_verify_delib_binding (every priced
  destruction binds a valid in-window record).
- `price_trial.zag` — measurement driver: E1/E2 ATTACK (E A1–A8 + PE1–PE11),
  HONEST (price histogram), STRESS; fixed A–D paths unchanged.
- `price_rt_e.zag` — blind red-team driver source (binary in blind/arm_E/).
- `gen_drivers.py` — sibling's driver generator (unchanged, kept for
  provenance).
- `substrate/` — R33 native substrate (unchanged mirror).

## Docs (committed)

- `DESIGN.md` — the deliberation law, personalities, refusal law.
- `VERDICT.md` — head-to-head, attack/stress results, plain-English verdict.
- `blind/brief_E.md` — blind red-team brief (observable law only).
- `MANIFEST.md` — this file.

## Evidence (committed, in evidence/)

- `run1_E1_ATTACK.txt`, `run2_E1_ATTACK.txt` — byte-identical (cmp).
- `run1_E2_ATTACK.txt`, `run2_E2_ATTACK.txt` — byte-identical.
- `run1_E1_HONEST.txt`, `run2_E1_HONEST.txt` — byte-identical.
- `run1_E2_HONEST.txt`, `run2_E2_HONEST.txt` — byte-identical.
- `run1_E1_STRESS.txt`, `run2_E1_STRESS.txt` — byte-identical.
- `run1_E2_STRESS.txt`, `run2_E2_STRESS.txt` — byte-identical.

## Blind drop (binary in blind/arm_E/, NOT committed to the repo)

- `price_arm_E_rt_bin` — SHA-256
  2a8d1751d182a722a470e660d4f05fa2b755a304e2004082a6543304c35cc427
- `price_trial_E_bin` — SHA-256
  b4658997ba9b669cdadd1ab22777ac032e4c8910a78ee69c3a3e46da96ab2dd8
  (measurement instrument, not blind).

Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
Branch: tnn-native-lab (never main). Zero RNG; pure Zag.
