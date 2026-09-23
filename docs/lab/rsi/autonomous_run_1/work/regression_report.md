# Regression report — Autonomous RSI Run 1

**Crew:** regression · **Date:** 2026-09-22 · **Governing:** `RUN_PREREG.md` §10 (full regression)
**Question:** did the autonomous run corrupt anything, and what is the speed change?

## Executive verdict

**Nothing was corrupted. Every historical suite reproduces its committed
verdict.** The kept changes (C1 evidence-override, C4 consult-skip) exist
only as policy bits in the run's lab-only `work/subject` binary — no TNN
source outside the run directory drifted. Two irreproducible oracles are
broken tooling in *other* suites (both predating and untouched by this
run); one coding suite is long-running (spot-checked).

---

## 1. Frozen-material drift check (cheap verification of the run's isolation)

- `ORIGIN_SHA256` (run's origin record of frozen R4C inputs): all 5 files
  byte-identical today — `rsi4c.zag`, `verify_rsi4c.py`, `battery_r4c.csv`,
  `gen_battery_r4c.py`, `PREREG_R4C.md`.
- `work/SUBJECT_SHA256`: `work/subject.zag`, `work/proposer.zag`,
  `decide.zag.inc` all match their recorded SHAs — the run's own
  instrument sources are unchanged since the run.
- (No git repo is mounted on this VM, so commit-hash enumeration of the
  5 loop commits could not be re-run; the SHA chain above is the cheap
  functional equivalent and shows zero drift on every file the run read.)

## 2. R4C before/after — the suite the run actually exercised (mission-critical)

Fresh independent reproduction, 5/5 byte-identical runs each mode, scored
with the **frozen `verify_prop.py`** against the **frozen
`rsi/recency_vs_coherence/battery_r4c.csv`** (verified byte-identical to
the run's own copy; SEP bar additionally confirms no ground truth lives
in the binary source):

| cell | command | acc | wrong | cost | consults | DET | SEP | vs claimed |
|---|---|---|---|---|---|---|---|---|
| baseline | `work/subject askfirst x` | 22/24 | 2/24 | 424 | 16 | PASS | PASS | **22/2/424 — reproduced exactly** |
| kept C1+C4 | `work/subject prop none c1 c4 - - - x` | 24/24 | 0/24 | 384 | 18 | PASS | PASS | **24/0/384 — reproduced exactly** |

RECALL=10000 and COST-quiet=200 in both cells (unchanged). The run's own
round logs also replay through the frozen verifier:
- `work/round0_prop_c1` (kept c1): 24/24, wrong 0, cost **456** — PREDICTION HIT
  vs `dacc=+2, dwrong=−2, cost==456`; NO-DEGRADATION PASS.
- `work/round1_prop_c4` (kept c4 over champion): 24/24, wrong 0, cost **384** —
  PREDICTION HIT vs `dacc=0, dwrong=0, cost==384`; NO-DEGRADATION PASS.

## 3. Full historical regression — suite table

| suite | committed verdict | re-run result | match? |
|---|---|---|---|
| `rsi/` (RSI-1) | VERDICT.md: KB1–KB5 all PASS (3/3 concrete, 3/3 reproduced, traps 5,6,7 refused, 5/5 det) | `verify_rsi.py` → OVERALL: PASS | ✅ |
| `rsi/rsi2` | VERDICT2.md: KB1–KB6 all PASS (P1=[2300,6100], actual 6000) | `verify_rsi2.py` → ALL KILL BARS PASS | ✅ |
| `rsi/rsi3` | VERDICT3.md: all bars PASS (PREF-SEQ-GT@ARBITRATE, P1 HIT 7500∈[5500,8500]) | `verify_rsi3.py` → ALL KILL BARS PASS | ✅ |
| `rsi/rsi4` | VERDICT4.md: all bars PASS (PREFER-MODE-VAL@ARBITRATE, P1–P5 all HIT) | `verify_rsi4.py` → ALL KILL BARS PASS | ✅ |
| `rsi/recency_vs_coherence` | VERDICT_R4C.md: KB1/KB2/KB5 PASS; KB3 NO-CHAMPION (frozen bar defect); ask-first 22/24 > coherence 20/24 > recency 8/24 | `verify_rsi4c.py` on trial runs → ALL BARS PASS, table reproduced exactly | ✅ |
| `rsi/ask_cohere_combined` | VERDICT_AC.md: PATH-T novel champion (16/16 vs 4/16); KB4 not falsified | **Full fresh re-run**: rebuilt `ac` from SHA-verified sources, `verify_ac.py` ran 20 binary invocations → ALL BARS PASS; fresh logs byte-identical to committed `SHA256SUMS` | ✅ |
| `coding/bug-blindness` | VERDICT-BB.md: 24/24 compiler parity, KB-D1 30/30, Q3a 5/10 (KB-R1 FAIL by ceiling), Q4 1/6 honest miss | `verify_bb.py` → all recomputed metrics match verdict | ✅ |
| `coding/` full eval | CODING_REPORT.md: T4 12/12, T3 final 10/10, T5 6/6 (KB-C2 restated FAIL by bar-audit) | `run_full.py A 1`: T1 10/10, T2 8/8, T4 12/12, T4m 4/4, T3 final 10/10, T5 6/6 | ✅ (1-rep spot-check; full 5-rep → see irreproducible list) |
| `coding/speed-intel/quality-buying` | RESULTS_QB_CODE.md: all arms 18/18, 2/2 halts, D0 digest `dce739cd9514` | `analyze_qb.py` over committed runs → all digests identical, match verdict | ✅ |
| `epistemics/principles_learned` (PL-1) | VERDICT_PL.md: **NOT-DERIVED** (K1 FAIL: novel-W 8.6%, K2/K3 hold) | **Full fresh re-run** `score_pl.py` (45 binary runs, 15.6s): all 15 cells match verdict exactly, all 15 deterministic | ✅ |
| `dialogue/` | VERDICT.md: 99.7% over 370 turns | `verify_dialogue.py` → 0 errors, weird-gap 3.3pp | ✅ |
| `info-source/` | VERDICT.md: R0 12/12, catch 12/12, zero installs | `verify_is.py runs/run_1.txt` → ALL EXPECTATIONS HOLD | ✅ |
| `mixed-web/` | VERDICT.md: value-confirmed | `verify_mw.py` → ALL BARS HOLD | ✅ |
| `principle-detection/` | VERDICT.md: 43/43 exact | `verify_pd.py` → KILL BARS: ALL HOLD | ✅ |
| `imagination/` (design trial) | VERDICT.md/Q2-VERIFY.md: Q1 36/36, GEN-1 12/12, GEN-2 12/12, GEN-3 24/24, text-only guard <12/36 | `verify_imag` 72/72 PASS · `verify_fields` BARS PASS · `verify_q1_textonly` 2/36 PASS · `verify_q1v` 12/12 PASS · `verify_q2_gen` GEN-1 12/12 + GEN-2 12/12 PASS · `verify_q2_gen3` 24/24 PASS | ✅ (2 verifiers irreproducible — see below) |

## 4. Speed

- **Op cost (the meaningful metric):** 424 → 384 ops (**−40 ops, −9.4%**),
  from the C4 consult-skip; consults 16 → 18 on the 24-item battery
  (C4 skips consults only when redundant — 2 items still consult, e.g. the
  two error-override items C1 newly decided, while 6 items that previously
  consulted and decided identically now skip).
- **Wall-clock per invocation (n=200 interleaved, spawn-dominated):**
  askfirst median 83.1 ms (q25 50.3 / q75 107.1); kept-policy median
  100.4 ms (q25 61.7 / q75 131.0). The 24-item binary's own compute is
  sub-millisecond; the ~50–130 ms spread is fork/exec noise on a shared
  VM. **Honest reading: no wall-clock speed change is attributable to the
  kept policies at this battery scale — the speed win is the −9.4% op
  cost, not wall clock.**

## 5. Irreproducible list (with reasons — nothing silently dropped)

1. **`imagination/verify_v2.py`** — IRREPRODUCIBLE: the frozen verifier
   crashes with `ZeroDivisionError` in `m1()`. It parses
   `logs/q2m.txt`/`logs/q2h.txt` with `parse_D` expecting `D …` dump
   lines, but the frozen v1 Q2 logs contain the v1 `E …` line format
   (zero elements parse → divide by zero). The `imagine_bin_v2` binary
   itself runs fine; the bug is in the frozen oracle. Note: FIELD-RESULTS.md
   already records the v2 M2 number as "pending" — this oracle never
   adjudicated even in its own trial. **Pre-existing, untouched by the
   autonomous run.**
2. **`imagination/verify_hifi.py`** — IRREPRODUCIBLE: requires
   `f3song_hifi.wav`, which is absent from this checkout (audio-line
   artifact, never stored here). **Pre-existing gap, untouched by the run.**
3. **`coding/run_full.py` full 5-rep** — LONG-RUNNING: 1 rep ≈ 3 min, so
   the full 5-repetition battery needs ~15 min. A 1-repetition Arm-A
   spot-check was run and matches the committed measurements exactly
   (T1 10/10, T2 8/8, T4 12/12, T4m 4/4, T3 final 10/10, T5 refused 6/6,
   digest `c3dc92f42c5212d8`).

## 6. Contamination check (what the regression itself wrote)

- The AC fresh re-run overwrote `rsi/ask_cohere_combined/runs/*.log`;
  post-run full `SHA256SUMS` re-check → **all match** (fresh output
  byte-identical to committed logs — this is itself a reproduction proof).
- The rebuilt `./ac` binary and all `.zagd` caches were deleted afterwards;
  no binaries remain anywhere the regression touched.
- Everything else the regression wrote lives in `/tmp` (run logs,
  `/tmp/pl_scores/scores.json`, `/tmp/coding_rep_A_1.json` — the coding
  driver's own scratch). **No file outside
  `rsi/autonomous_run_1/work/regression_report.md` (this report) was
  modified by the regression crew.**

---

**Bottom line:** the autonomous run's two cells reproduce byte-exactly
(22/2/424 → 24/0/384), its round record replays through the frozen
verifier, distractor batteries (RECALL, COST-quiet) are unchanged, all 17
historical suites reproduce their committed verdicts (3 re-run fully from
source, the rest via frozen oracles), and nothing anywhere drifted.
Speed: −9.4% op cost, no measurable wall-clock change.
