# RUN REPORT — Wave 9 trust-tiers AMENDED REDESIGN rerun

**Date:** 2026-09-20 (PDT) · **Worker role:** REDESIGN (implement amended scheme + rerun; no result interpretation beyond the verdict rule).
**Law:** `AMENDMENT_REDESIGN_2026-09-20.md` (pre-run commit `9a5687eb`, branch `tnn-native-lab`).

## Implementation (native Zag, `substrate/trust_tiers.zag`)

Amendment items implemented (§1–§9):
- **H1 (§5.6):** new audit ops 67–71 (`T0_T1_HOLD`, `HOLD_RELEASED_T0_CONFIRM`, `HOLD_BROKEN_BY_DISTRUST`, `HOLD_TIMEOUT_ESCALATE`, `GATE_HELD`); per-slot hold state (`hold_state/branch/ep/claimed/resolution/resolve_ep`); trigger (T1-alone leg + T0-cites-held [a] or T0-silent [b]); three resolution paths checked in order every episode (T0-confirm → all-leg-sources-distrusted → W=25 timeout → freeze + `TRAINER_ESCALATE`); `GATE_HELD` for gate ops on held memories; arm-T-only (T-NC keeps its 0/36 A5 ablation signal per §7).
- **A.3:** freeze-lapse clock resets only on contradiction citations (`ek==TT_KIND_CONTRA`) by named sources.
- **A.2:** `ST_T01_WINDOW` — {T0,T1} citations per target in the campaign window.
- **A.5:** absolute ep on every `TT_OP_*` audit; added `ST_REV` revision events; fixed three `COLLUSION_SUSPECT` call sites that packed claim into the ep field (one pre-existing, two new) — found by the new chronological checker, fixed, binary rebuilt, full pipeline re-run.
- **M1/M2:** campaign constants, selector parsing, schedules (M1: T0 lag 2/5/8, T1-first genuine shift; M2: T0 suppressed, spoofed T1 + T3 colluders), metrics, taxonomy.
- Zero RNG in AI decision paths (static grep clean); arm-B gate region untouched (code-level tier purity verified).

Two implementation defects caught and fixed before evidence:
1. H1 trigger initially lacked the arm-T guard and fired on T-NC (would have destroyed the 396/432 ceiling). Fixed.
2. A.5 packed-ep on `COLLUSION_SUSPECT` (see above). Fixed; all evidence below is from the final binary.

## Build

```bash
cd ~/workspace/tnn-lab/wave9/trust-tiers/substrate
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 trust_tiers.zag \
  --no-zagd --no-analyze --no-foreground-cache -o trust_tiers.bin
```
Compiled clean. Binary `trust_tiers.bin` (306434 bytes). NOT committed (per instruction).

### Source SHAs (pre-build, final binary)

- `trust_tiers.zag`          `9e95d533403ab5c1a863de025753659d16e56301e55a14f0294569e7c5fb497d`
- `st_memory_core.zag`       `474ac0bb2417f26e531450a4fa406662aa733138eeaf622f454222509834da8d` (verbatim)
- `cl/common.zag`            `8aec83cb4feb83a20bc91c8179d7055d691c155414a359f7014386271aa6168b`
- `R33_NATIVE_IO_V1.zag`     `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `R33_NATIVE_SHA256_V2.zag` `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- `run_gate.sh`              `d50ecb6a082f38af69541f302c76bc6ac6a3f58209109d4f9d831b694d9fd870`
- `run_matrix_s1.sh`         `94b4681134caa799555484d64c5688404b249ccd72beabe985b18556158a2765`
- `run_matrix_s10.sh`        `91fbe7de3c3e27e314db63f84a8344961d2ee107e8793348d4258083c3483116`
- `run_matrix_m1m2.sh`       `8744718ed3c32cc47e07518e68d150f5c6a387187aa62f4df8b081427235073f`
- `check_bars.sh`            `ce5c85114dabe853f1d7a7de99846b4d291dfcd52923f69c17a2f037ee4e999e`

## Static gates (before battery)

- Invalid selectors: empty→64, bad campaign→65, N_A0→66. M1/M2 selectors accepted.
- RNG grep: none in decision paths. Arm-B region: no tier reads.

## Pre-run gate (`run_gate.sh`) — PASS (final binary)

- (i) A5/T: 36/36 cells — `T0_T1_HOLD` at (ep−astart)≤1 branch a → `HOLD_BROKEN_BY_DISTRUST` → zero target revisions.
- (ii) A4/T: 36/36 cells — no hold, `ST_REV_LATENCY` ≤ 6.
- (iii) M2/T: 36/36 cells — hold branch b → `HOLD_TIMEOUT_ESCALATE` at hold+25 + `TRAINER_ESCALATE` → zero revisions, DEGRADED_GRACEFUL.
- All 108 cells × 2 runs paired byte-identical. Evidence: `evidence/gate/` + `cells.sha256`.

## Battery (final binary)

| Matrix | Command | Cells | Executions | Divergences | Evidence |
|---|---|---|---|---|---|
| S1 (full original: 3 arms × 8 camps × 3 var × 12 inst) | `run_matrix_s1.sh` | 792 | 1,584 | 0 | `evidence/s1/` |
| M1/M2 (3 arms × 2 camps × 3 var × 12 inst) | `run_matrix_m1m2.sh` | 216 | 432 | 0 | `evidence/mm/` |
| S10 (conditional; S1 had 0 divergences) | `run_matrix_s10.sh` | 12 | 24 | 0 | `evidence/s10/` |

Manifests: `cells.sha256` in each dir, all `sha256sum -c` clean (1584/1584, 432/432, 24/24).

## Checker

`check_bars.sh` (extended: §11 H1 audit assertions, §12 absolute-ep ordering, §13 BLIND scoping, §14 FP budget on attack-free baselines) — rc=0, all sections green. Full output: `/tmp/check_out.txt` (rerun: `./check_bars.sh`).

## Artifacts & cleanup

- Superseded evidence retained under `evidence/archive/` (original REDESIGN; pre-A.5-fix amended run). Final evidence in `evidence/{gate,s1,mm,s10}/`.
- Binaries (`.bin`) and `.zagd` cache files excluded from the commit. `REPAIR_IN_PROGRESS.md` removed only in the final commit.
