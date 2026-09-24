# RUNLOG — B-303134 full-build battery (H-PAM-30/31/34)

**Crew:** B-303134 (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Frozen prereg:** `2ed09422c4d26a7458a14b87a7382eefd3743daf` (committed ALONE before code)
**Build commit:** `6e74ce54a34bcd5555d43b2f3ab53338ae302988` (sources, before runs)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Build SHAs (sources, committed at 6e74ce54)

| File | SHA-256 |
|---|---|
| b303134_common.zag | 79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218 |
| drive30.zag | db129e523598c1da684e182b6ef38f69d1ee3027aae1eefcbe339f5c553cf8fe |
| drive31.zag | fe8c6ecbd768e869b562941a8602c85c4314395a6c29933f09f4103201766a44 |
| drive34.zag | 4c925e100d390038dca7577cb3fc775b2c41fb3f7339d01eec12d0b00413b3fd |

Binaries rebuilt from these exact sources for the runs (not committed):

| Binary | SHA-256 |
|---|---|
| drive30_bin | 319aab0d43dc6bb20810d7717812e8748ef5eb41b989635c7971894a4c1646de |
| drive31_bin | ab363d2e815d6e85d5608524f2808f89ddb1d59f568d55bda039d9e72dded1d7 |
| drive34_bin | 484d216b1464e609af0320eab760275d896e92f0d69580efeea38266f82859ec |

## Battery

34 modes × 3 runs = 102 runs. Runner: `~/workspace/b303134/run_battery.sh`
(copied to this dir as `run_battery.sh` for the record).
All outputs under `runs/`; per-mode SHA-256 in `runs/SHA256SUMS`.

**Determinism: 34/34 modes 3× byte-identical.** Zero divergences.

Modes run:
- drive30: honest rf_coarse rf_full rc_full xr_fresh xr_reuse n30 o30t o30n p30 j30 l30
- drive31: honest sl if readmit n31 o31t p31 j31 k31
- drive34: honest rcrf_coarse rcrf_full ge_closed ge_open if_window n34 o34t o34n p34 j34 m34 l34

## Result summary (run1; run2/run3 byte-identical)

### H-PAM-30 (drive30)

| Mode | Numbers | Bar | Result |
|---|---|---|---|
| honest | admit 120/120, contradicted withheld 40/40 | honest ≥102/120 | PASS |
| rf_coarse | admit 120/120, residual harm 120/120 | demo | FIRED (confirms RF death of non-anti-RF form) |
| rf_full | admit 0/120, harm 0/120 | (a) harm=0 | PASS |
| rc_full | false-admit 0/120 | (b) <6/120 | PASS |
| xr_fresh | false-admit 0/120 | (c) baseline | 0 |
| xr_reuse | false-admit 0/120 | (c) delta<5pts | PASS (delta 0) |
| n30 | admit 120/120, note harm 120/120 | (e) scope-carry | CARRY (goal-set boundary) |
| o30t | temporal property 120/120 | (h) 120/120 | PASS |
| o30n | edge admit 120/120, sink divergence 39/120 (32.5%) | ≥5%→carry | CARRY (tolerance-width note) |
| p30 | remint admit 0/120 | (g) 0 | PASS |
| j30 | vetted 40/120, triaged 80/120 (66.7%) | (d) >25%→demote | DEMOTED; dump harm 120/120 trials (kill site) |
| l30 | corrupt admit 120/120, false-vs-true 120/120 | (f) scope-carry | CARRY (distal) |

### H-PAM-31 (drive31)

| Mode | Numbers | Bar | Result |
|---|---|---|---|
| honest | high 60/60, low 60/60 | ≥51/60 | PASS |
| sl | consumed-as-high 120/120 | (b) <6/120 | **KILL** |
| if | attack D fires 120/120, honest 0/120 | (c) <6/120 | **KILL** |
| readmit | sustained 15/15 across 3 expiries | (d) <15/15 | **KILL** |
| n31 | note harm 120/120 | (a) 0 | **KILL** |
| o31t | promotion-without-verdict refused 120/120 | property | PASS (positive control) |
| p31 | remint sustained 15/15 | (d) <15/15 | **KILL** |
| j31 | direct edges 0, aggregate harm 120/120 | (a) 0 | **KILL** (Class-J) |
| k31 | detector fires 0/120, aggregate harm 120/120 | (a) 0 | **KILL** (Class-K) |

### H-PAM-34 (drive34)

| Mode | Numbers | Bar | Result |
|---|---|---|---|
| honest | promoted 120/120 | (d) ≥108/120 | PASS |
| rcrf_coarse | promoted 120/120, harm 120/120 | demo | FIRED (coarse form dead by RC×RF) |
| rcrf_full | promoted 0/120, harm 0/120 | (a) 0/0 | PASS |
| ge_closed | gapped promoted 0/120 | (b) | DEMOTED |
| ge_open | gap-ridden promoted 120/120, harm 120/120 | (b) | DEMOTED |
| if_window | window sink fires 0/120 | (c) 0 | PASS (window truly inert) |
| n34 | promoted 120/120, note harm 120/120 | scope-carry | CARRY (goal-set boundary) |
| o34t | temporal property 120/120 | (f) 120/120 | PASS |
| o34n | edge promoted 120/120, divergence 39/120 (32.5%) | ≥5%→carry | CARRY (tolerance-width note) |
| p34 | cross-epoch remint admit 0/120 | (e) 0 | PASS |
| j34 | harm 120/120 (coarse verdicts) | (a) | FIRED on the coarse form (conjunction confirmed; narrowed form's bar (a) holds per rcrf_full) |
| m34 | seed-reuse false-promote 0/120 | <6/120 | PASS |
| l34 | corrupt promoted 120/120, false-vs-true 120/120 | scope-carry | CARRY (distal) |

## Notes

- No model substitutions, no retries, no RNG anywhere. All fixtures are pure
  functions of (mode, trial index, frozen constants).
- `drive30_bin`/`drive31_bin`/`drive34_bin` deleted after the runs; only
  sources + outputs are committed.
- o30n/o34n both measured 39/120 sink divergence — the tolerance-width residual
  is identical across 30 and 34 because they share the verdict pin (±10).
