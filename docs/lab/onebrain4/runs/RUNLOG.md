# RUNLOG.md — One-Brain Round 4 Runner (frozen v7 battery)

**Run date:** 2026-09-27 (PDT). Runner executed the frozen 8×3 battery per PREREG4. No tuning, no .zag opened, no frozen files touched.

## Input verification (before any run)

| Artifact | Expected SHA-256 | Measured | Verdict |
|---|---|---|---|
| Binary `~/workspace/onebrain4/impl/onebrain_v4` | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` | ✅ MATCH |
| Problem set `~/workspace/onebrain4/prereg/v7.tsv` | task-stated `3f3b3d6c34364460fdd54303729033e02c2da8f5c9960ea1586a72efd95bda3a` | `3f3b3d6c34364460fdd54303729033e02c2da2f5c9960ea1586a72efd95bda3a` | ⚠️ differed from task text at one byte (`2f5c` vs `8f5c`); **FREEZE4.txt records `...da2f5c99...` — trusted FREEZE4.txt per task instruction, file re-verified against FREEZE4.txt → ✅ MATCH** |

Invocation per BUILD_LOG.md: `./impl/onebrain_v4 <mode> prereg/v7.tsv`, stdout captured to `runs_v7/<mode>_r<N>.out`, stderr to `.err` (all empty). 44 items/item-set confirmed in every output.

## Per-run SHAs and determinism (K4‴)

| Mode | r1 SHA-256 | r2 == r1 | r3 == r1 | Identical |
|---|---|---|---|---|
| single | `98c31283d14e0a3014396f00b82625bd4b70af040a7f27dea225ecff573d5895` | ✅ | ✅ | ✅ |
| onebrain | `4724e4c82a7c98892a50d2590e3eb203327993dd497073bbd94bee065ab6154d` | ✅ | ✅ | ✅ |
| nov4 | `8b8d27e7cadde1b36e0fdfbc37d25494ed8e45b977a8f83e7a3cf63a8edffe90` | ✅ | ✅ | ✅ |
| nG | `21483a898215c390c34b3675b295283c856bfc994ef4b7b88f9035dd90b21297` | ✅ | ✅ | ✅ |
| nov4nG | `ee4b792cf1f9021e3cb838afe800a0dcd8e0eb798b4025c531cf4071c793fdaf` | ✅ | ✅ | ✅ |
| ablate | `793ab0daf3fc8eb1a0799c6b5ea560236423440d3537501242a22f9003cf7a65` | ✅ | ✅ | ✅ |
| min | `6e844586d48e945e2a12972fbe210be680f22fda66fa5e1e28ca72564a3acefb` | ✅ | ✅ | ✅ |
| poison | `d695dff4eec55d757e5198d722a6222f935ade8925cc10fa988f8c61e73a9b65` | ✅ | ✅ | ✅ |

All 24 runs exited rc=0. All 3 reruns of every mode byte-identical (8 unique SHAs). **K4‴ PASSES — whole-round determinism holds.**

## Accuracy summary (exact match vs `expected_bid`, /44)

| Mode | V4 | Reint | Score | Δ vs single |
|---|---|---|---|---|
| single | off | off | **12** | — |
| onebrain | on | on | **30** | +18 |
| nov4 | off | on | **35** | +23 |
| nG | on | off | **16** | +4 |
| nov4nG | off | off | **24** | +12 |
| ablate | on | on | **26** | +14 |
| min | on | on | **30** | +18 |
| poison (diagnostic) | on | on | **17** (of 44; 23 items = NO_VERDICT, winner=-1) | +5 |

Key per-item facts (see `winner_table.md` for the full 44×8 table):
- q01–q08 (V4-binding H2 forget-hurt): single/nov4/nov4nG hit expected 15/16; onebrain/nG/min/ablate move to 19 (V4 harm direction) on all 8.
- q09–q19 (reintegration-room): single at 13 (wrong) on all 11; reintegration modes recover expected on 8 of 11.
- q21–q28, q33–q36: reintegration modes score expected; single at 17/19 (one-bid misses).
- q29, q32, q31 (support-quality): mixed — reintegration fixes some, V4 re-breaks others.
- q37–q40 anchors: all modes agree (correct).
- q41–q44 withhold (expected 23): all modes answer 19 (wrong) — 0/4 for every mode.

## Kill-bar adjudication (H1‴ claims)

| Bar | Rule | Numbers | Verdict |
|---|---|---|---|
| K1‴ | nov4 ≤ nov4nG kills Claim 1 (reintegration-alone) | nov4=35, nov4nG=24 → margin **+11** | ✅ **NOT TRIGGERED** — Claim 1 survives |
| K2‴ | onebrain − nov4 ≥ +2 kills Claim 2 (V4-neutral-or-harmful) | onebrain−nov4 = 30−35 = **−5** | ✅ **NOT TRIGGERED** — Claim 2 survives (V4 cost 5 net items) |
| K3‴ | onebrain ≤ single kills Claim 3 (lineage replication) | onebrain=30 > single=12 → **+18** | ✅ **NOT TRIGGERED** — Claim 3 survives |
| K4‴ | any rerun pair differs | all 24 runs byte-identical | ✅ **PASSES** |
| K5‴ | RNG in decision paths | reruns byte-identical; zero `rand`/`rng`/`seed` markers in any output/err; stderr all empty | ✅ **no RNG evidence** |
| K6‴ | min does not fan out on fork-worthy items | min forked **41/44** items (fork=1); non-fork = q38, q39, q40 (anchors) only | ✅ **NOT TRIGGERED** — min fans out |

No kill bar triggered; no bar voided the round. Per PREREG4 §8 step 5, red team now owns confound review before any claim is declared.

## Notes for the red team (observed, not adjudicated)

1. **single fork=0 on all 44 items** — even though PREREG4 §7 states 36 fork-target items were verified pre-freeze as fork-worthy in single mode. The `fork=` field in single-mode VERDICT lines reads 0 everywhere; min (same machinery family) forks on 41. Whether single genuinely never forked or the flag is mode-conditional in the trace is a trace-semantics question worth checking.
2. **poison** yields NO_VERDICT (winner=-1) on 23/44 and scored 17/44 on the remainder; q41–q44 withhold items answered 19 everywhere.
3. The v7.tsv hash discrepancy: the task text's hash (`...da8f5c...`) differs from FREEZE4.txt's (`...da2f5c...`) by one hex pair; the task instruction said to trust FREEZE4.txt, and the file matches FREEZE4.txt exactly.
4. nov4nG (24) outscores single (12) by +12 despite both being V4-off/reintegration-off per PREREG4 §3 — the fork/close machinery apparently still runs in nov4nG ("fork/close still run"), and differs from single on q09–q14, q15–q17, q19–q20. Not a kill-bar issue, but the margin between the two "neither" arms belongs in the confound review.

## Deliverables in this dir

- This RUNLOG.md
- `winner_table.md` — 44-row per-problem winner table (8 modes), bold = matches expected
- 24 raw outputs: `<mode>_r{1,2,3}.out` (+ empty `.err` files)
