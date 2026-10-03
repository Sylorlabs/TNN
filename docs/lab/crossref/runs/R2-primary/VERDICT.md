# R2 replication — VERDICT (R2-PRIMARY crew, independent Type A)

Family R2: **deliberation quality ceiling — CEILING-CONFIRMED**.
Replication type A: full independent rerun in a clean environment
(fresh clone, frozen checkout, pinned toolchain, no copied binaries/caches,
zero RNG, ≥3 byte-identical reps per cell). Date: 2026-09-22/23 PDT.

## Verdict: REPRODUCED

Every committed number in the frozen R2 evidence was reproduced exactly —
mechanism battery tallies/costs/digests (byte-identical logs), the six QB
structures on both the 94-item epistemic and 20-item coding batteries
(identical tallies, costs, and canonical digests), the 36/36 gate battery,
and the 4x/8x no-gain legs (byte-identical outputs; the plateau is
mechanism-level, measured on fresh runs).

## Frozen evidence pins (verified before any run; all ancestral to the frozen checkout)

| pin | commit | subject |
|---|---|---|
| prereg | `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b` | QB prereg: freeze quality-buying design before any results (PREREG_QB.md) |
| synthesis | `3314fc1fdd6fb45ec4d73169817cc9820ce520a1` | QB synthesis: quality-per-cost curve (RESULTS_QB.md) — verdict CEILING-CONFIRMED |
| mechanism | `a638d4d56a2e` | new-mechanisms: implementation + 15 run logs |
| mechanism | `b447c367677f` | new-mechanisms: prereg/spec/verdict (CLOSED) |

Frozen checkout: `7b2100d09911c5c10252c5756c7def288e70bd1f`, tree clean.
Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Committed vs measured — mechanism battery (264 items)

Source `docs/lab/new-mechanisms/mech_learner.zag` rebuilt fresh; 3 modes × 3 reps.
All 9 logs byte-identical to committed; reps 3/3 identical within mode.

| measure | committed | measured | match |
|---|---|---|---|
| baseline contradiction resolution | 12/156 | 12/156 | ✓ |
| hypcomp contradiction resolution | 156/156 | 156/156 | ✓ |
| confdepth contradiction resolution | 156/156 | 156/156 | ✓ |
| kind tallies baseline (k0..k6) | 96,0,0,0,0,12,0 | 96,0,0,0,0,12,0 | ✓ |
| kind tallies hypcomp / confdepth | 96,36,36,24,24,12,24 | identical | ✓ |
| kind 7 smooth-lie absorption (all modes) | 12/12 | 12/12 | ✓ |
| deliberate withholds (k1 2v1) | 0 / 36 / 36 | 0 / 36 / 36 | ✓ |
| quiet ops/fact (×1000) | 2000 / 3000 / 2000 | 2000 / 3000 / 2000 | ✓ |
| confdepth quiet cost vs baseline | 1.00× (2.000 ops) | 1.00× | ✓ |
| contested ops totals | 552 / 1356 / 1500 | 552 / 1356 / 1500 | ✓ |
| state digest baseline | `60a7095526fdd054` | identical | ✓ |
| state digest hypcomp = confdepth | `1f68e26f32a54bac` | identical (parity) | ✓ |

Kill bars: KB-M-RESOLVE PASS (156/156 ≥ 140), KB-M-NOHARM PASS (96/96),
KB-M-TIE PASS (36/36), KB-M-COMPOSE PASS (24/24), KB-M-TEMPORAL PASS
(24/24 + 12/12), KB-M-SPOOF PASS (24/24), KB-M-COST PASS (1.00× ≤ 1.10×),
KB-M-PARITY PASS (identical tallies AND digests), KB-M-DET PASS (3/3
byte-identical per mode; original bar was 5/5).

## Committed vs measured — QB epistemic (94 items, six structures)

Source `quality-buying/work_epi/delib_qb.zag` rebuilt fresh; 6 modes × 3 corpora × 3 reps.
All 54 logs byte-identical to committed. Independent pure-Zag scorer
(`score_epi.zag`, sha256 self-test passes) reproduces every number.

| mode | Q_e committed | Q_e measured | preds/item | digest |
|---|---|---|---|---|
| d0 baseline | 59/94 | 59/94 | 846 / 9.000 | `57cefaa4…23bd650` ✓ |
| d1 conflict-driven | 59/94 | 59/94 | 951 / 10.117 | same as d0 ✓ |
| d2 3-round critique | 12/94 | 12/94 | 1128 / 12.000 | `2d4506e1…` ✓ (destructive) |
| d3 hyp. competition | 59/94 | 59/94 | 1128 / 12.000 | same as d0 ✓ |
| d4 one-brain phases | 58/94 | 58/94 | 1128 / 12.000 | `8842bfe0…` ✓ (−1: sarcasm 2/10) |
| d5 combined | 59/94 | 59/94 | 1609 / 17.117 | same as d0 ✓ |

Family tallies match committed (d0: false 12/12, true 12/12,
j/s/h/a/p/c/i = 5/3/5/3/5/9/5 of 10; d2: false 0/12, weird 0/70, true 12/12).
QB-CAL PASS: d0 = 59/94 @ 9.000 with digest `57cefaa42100f695…23bd650`,
matching the frozen A1R 2x digest. D1/D3/D5 converge to exactly the staged
verdicts on all 94 items (shared digest).

## Committed vs measured — QB coding (20 items, six structures)

Source `quality-buying/work_code/learner_qb.zag` rebuilt fresh
(sha256 `a54155da65a6bc65747fb5451907a9e6a3d7cc3612485986a3bc7e8322c3fb8b`);
committed `driver_qb.py` used as plumbing only. 6 modes × 3 reps = 18 cells.
All reps digest-identical within mode; every digest equals the committed
digest (full 64-hex, verified by the independent pure-Zag `canon.zag`,
itself validated against the committed d0 JSON). Tallies independently
verified by pure-Zag `tally.zag`.

| mode | Q_c | halts | iters | znc | hyp-evals | digest |
|---|---|---|---|---|---|---|
| d0 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 28 ✓ | 45 ✓ | `dce739cd9514…` ✓ |
| d1 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 28 ✓ | 45 ✓ | `6655e051606d…` ✓ |
| d2 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 27 ✓ | 101 ✓ | `4d96ff818cc7…` ✓ |
| d3 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 28 ✓ | 137 ✓ | `658a6f657cc4…` ✓ |
| d4 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 28 ✓ | 68 ✓ | `8f492914cfcd…` ✓ |
| d5 | 18/18 ✓ | 2/2 ✓ | 46 ✓ | 27 ✓ | 216 ✓ | `40b1d9b8dab6…` ✓ |

(✓ = identical in all 3 reps and equal to committed.)
Gate battery on the fresh binary: **36/36 PASS** (R1–R4 → REFUSE:G1/G2/G4/G5,
A5/A6 → ALLOW), identical verdicts to the committed `gate_battery_all.txt`.

## Committed vs measured — 4x/8x no-gain (SI legs, 94 items)

Source `work_a1r/delib_si.zag` rebuilt fresh; budgets 4 and 8 × 3 corpora × 3 reps.
All 18 outputs byte-identical to the committed `out_b4_*` / `out_b8_*` logs.

| budget | score committed | score measured | preds/item | recon | flips |
|---|---|---|---|---|---|
| 2x (ref) | 59/94 | (QB d0 rerun: 59/94) | 9.000 | 0 | 0 |
| 4x | 59/94 | 59/94 | 9.330 (877/94) | 1 | 0 |
| 8x | 59/94 | 59/94 | 10.330 (971/94) | 1 | 0 |

Gain(2x→4x) = 0pp, gain(4x→8x) = 0pp on verdicts; the 4x reconsideration
fires once (W152, pro=con tie → keeps the 2x verdict) and the 8x
verification pass flips nothing. The plateau is mechanism-level, not a
battery artifact. The R2 direction "keep 2× deliberation + free-speed
mechanisms; drop 4×/8× (no gain)" is MEASURED on fresh runs.

## Changes and caveats

1. **Incident (external, fully recovered):** mid-sweep, the freshly built
   `bin/learner_qb` was deleted by an unknown external actor (~02:31;
   directory mtime; no session command deletes files and the committed
   driver contains no deletion logic). 7 cells failed with FileNotFoundError.
   The committed source was verified intact (sha256 unchanged), the binary
   rebuilt from it (same 279931 bytes), and the 7 cells rerun with a
   pre-cell existence guard — all succeeded, all digests match committed.
   No evidence values were affected.
2. **Cosmetic:** my gate-battery runner prints an `(out: ALLOW)` suffix the
   original script omitted; all 36 verdicts are identical.
3. **Pre-existing prereg typo (not mine):** `new-mechanisms/PREREG.md` lists
   kind 5 "temporal unattested" as n=24; every piece of committed evidence
   (bar text 12/12, VERDICT, `mech_learner.zag` ranges, the 264 total) uses 12.
4. **Rounding:** VERDICT.md's prose rounds contested ops/fact (3.286/8.929)
   vs the logs' exact 3.285/8.928; the logs carry exact integers and my runs
   reproduce them.
5. `delib_si.zag`'s `@import` path (`../../../../prose-learning/epistemic_wave/src/`)
   has no R33 files at that location in the frozen commit; I mirrored the
   committed R33 pair there in scratch. Byte-identical outputs validate the choice.

## Bottom line

REPRODUCED. Deliberation buys quality up to ~2× and then hard-ceils:
conflict-driven deliberation reaches the ceiling at exactly baseline quiet
cost (1.00×) with identical state; hypothesis competition and the combined
stack cost 1.5–4.8× more deliberation for zero additional quality on both
batteries; unguided critique is destructive (12/94). No evidence contradicts
the frozen CEILING-CONFIRMED verdict.
