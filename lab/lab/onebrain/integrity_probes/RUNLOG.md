# shared-state integrity-probe line — RUNLOG (resume, 2026-09-27)

## Inherited state (verified, not trusted)
- `atk.zag` (2151 lines): round-3 one-brain machinery + fault-injection probe fns
  (`fi_leader`, `fi_runnerup`, `fi_inject` with FI1..FI7) present. The `fi`
  parameter was NOT wired: `ob_subpasses` signature already took `fi:i32`
  but its caller at line 1948 passed only up to `trace` (build-broken), and
  `fi_inject` was called nowhere.
- `attack.zag`: byte-identical copy of `base.zag` (sha256 85e2b83c...), a
  leftover; removed at resume.
- `base.zag` + `base_bin` + `base_onebrain.txt`: round-3 frozen machinery.
- Baseline reproduction: rebuilt `base.zag` -> `base_rebuild`, ran `onebrain`
  over v6.tsv: VERDICT lines byte-identical to committed `base_onebrain.txt`,
  score 23/44 exactly. Baseline confirmed by rebuild, not by claim.
- Disk: home 99% full (~1.1G free). Workdir kept small; staging cleaned after commit.
- Language: neutral integrity-testing vocabulary throughout (per Micah's line brief).

## Wiring + measurement (completed)
- `fi` wired mechanically through main/run_full/solve_one/ob_deliberate/
  ob_subpasses; `fi_inject` phase-0 between sub-pass rounds, phase-1 between
  sub-passes and reintegration. Two latent defects in the inherited file
  repaired: `\"` escape sequences znc rejects (E0002) replaced with plain
  quotes in the 7 trace-print lines; the arity-mismatched ob_subpasses call
  completed. Build clean (`atk_bin`, warnings only).
- Determinism: every mode run twice, byte-identical (cmp). f0 control:
  23/44, zero winner changes vs the rebuilt baseline (only the mode label
  differs) — probe deltas are from the faults, not the wiring.
- Probe runs: f1 4/44, f2 23/44, f3 8/44, f4 23/44, f5 27/44, f6 27/44,
  f7 23/44. Raw trace outputs retained in ~/workspace/shared_state_adversary/
  (not committed; regenerable). Compact evidence committed as verdicts.tsv.
- z.ai relay: not used — verdicts are mechanistic and trace-grounded;
  no second opinion needed.
