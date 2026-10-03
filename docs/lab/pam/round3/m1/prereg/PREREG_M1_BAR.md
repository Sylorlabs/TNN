# PREREG — M1 Bar Calibration (PAM Round 3, Crew 7)

**Date:** 2026-09-24. **Crew:** M1 bar-calibration crew (subagent).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Status:** FROZEN — committed alone
before any fixture generation, build output, or search result exists.
This document is the single source of truth; the fixture generator
(`gen_m1.py`), the Zag grid search (`m1_grid.zag`), and the scorer
(`score_m1.py`) all derive from it. No transcription — every fixture row,
threshold axis, and kill number below is extracted by script from the cited
frozen sources, never from memory.

## 0. Motivation (frozen evidence)

Fable-5.1 audit Q6 (`~/workspace/tmp_commit/pam_r3/fable_audit_out.txt`):
trial 1145 was WRONG yet strictly dominated its CORRECT incumbent on every
logged axis (conf=874, margin=10410, strong=1, agree=1) — and the current bar
lets it through. H6 no-provisional stops *unconfirmed* wrongs but not
*confidently-wrong corroborated* pairs. The 85% RK-3 bar is a target, not a
mechanism. M1 recalibrates the bar itself.

## 1. The bar

A trial PASSES the bar iff all four hold:

    PASS(t)  <=>  conf(t) >= CT  AND  mrgF(t) >= MT  AND  strong(t) >= ST  AND  agree(t) >= AT

## 2. Frozen data (read-only; scripts extract, never transcribe)

| # | Source (frozen) | sha256 | Extraction rule |
|---|---|---|---|
| D | `~/workspace/pam_round2/o1_delivery/sweep.jsonl` (11,840 rows; the frozen R2-4 evidence, sha pinned by the O1 prereg) | `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2` | RK-3 battery denominator: trials with `judgment==truth` AND `conf>=700`. Count = **1,102**. Axes per trial: `(conf, mrgF, strong, agree)`. |
| W | `~/workspace/pam_round2/d1_stack/rec_install.records` (D1 battery Leg 2 source) | `c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad` | 12 sustained TMB-5 cross-span wrongs = seq 24–35 (RICH judgments, truth DARK/BRIGHT, conf 764–832). Axes: `(conf, mrgF := meas)` per the D1 prereg's frozen `mrgF := measure` substitution (record format carries no margin). |
| P | `~/workspace/pam_round2/cc1_guard/prereg/gen_guard.py` (CC1 guard fixtures) | `49eef7b169790207dd53b140a3586144fe34a8b99a134e18d2244702ae2c214b` | 9 wrong pairs: cells `CC1`, `CC1-V1` … `CC1-V8`. Wrong members = trials idx 2,3 of each cell (jcode=2 ≠ truth=3). Tuple fields `(tcode, prog, jcode, conf, pred, meas, mrgF, truth, jG, confG, seq, span_a, span_b)`. Axes per member: `(conf, mrgF)`. Pair data: CC1/V1/V2/V3/V7/V8 (718,382)+(704,358); V4 (850,382)+(840,358); V5 (718,6600)+(704,6603); V6 (718,6600)+(704,358). |
| B | same sweep.jsonl as D | same | Diagnostic-only broad-wrong set: trials with `judgment!=truth` AND `conf>=700`. Count = **1,109**. NEVER constrains the search; reported as a safety diagnostic. |

**Worst-case convention (frozen here, not post-hoc):** the W and P record
formats log no `strong`/`agree`. Both are treated as 1 (satisfied) for every
W/P trial. This is the adversarial assumption: the conf/margin arms alone
must block the wrongs. If the true values were 0, the bar would be strictly
safer — the assumption can only make the optimized bar more conservative,
never less.

## 3. Search space (frozen)

- CT ∈ {0, 1, …, 1000} (integer confidence threshold)
- MT ∈ {0, 1, …, 20000} (integer margin threshold)
- ST ∈ {0, 1}, AT ∈ {0, 1} (strong/agree arms; 0 = arm disabled)

## 4. Objective (frozen)

Maximize **true-PASS** = |{ t ∈ D : PASS(t) }| / 1102.

RK-3 % for M1 is defined as this true-PASS rate: the fraction of the frozen
RK-3 denominator (1,102 correct conf≥700 trials) that the bar admits. This is
the bar-fronted form of the program's RK-3 metric (104/1,102 frozen).

## 5. Constraints (frozen; both must hold with zero violations)

- **C1:** zero false-PASS on the 12 TMB-5 wrongs: ∀w ∈ W, ¬PASS(w).
- **C2:** zero false installs on the 9 CC1 wrong-pairs: ∀ pairs (a,b) ∈ P,
  ¬(PASS(a) ∧ PASS(b)) — a pair installs only if BOTH members pass.

## 6. Exact search algorithm (frozen; the Zag program implements this verbatim)

For each (ST, AT) ∈ {0,1}²:

1. Armed set D' = { t ∈ D : strong(t) ≥ ST ∧ agree(t) ≥ AT }.
2. Candidate MTs = sorted-unique( {0} ∪ { mrgF(w)+1 : w ∈ W }
   ∪ { min(mrgF(a),mrgF(b))+1 : (a,b) ∈ P } ∪ { mrgF(t) : t ∈ D' } ).
3. For each MT: CT*(MT) = max( {0}
   ∪ { conf(w)+1 : w ∈ W, mrgF(w) ≥ MT }
   ∪ { min(conf(a),conf(b))+1 : (a,b) ∈ P, min(mrgF(a),mrgF(b)) ≥ MT } ).
   A wrong blocked by the margin arm (mrgF < MT) needs no conf arm, and a
   pair is blocked iff its weaker member is blocked — hence the min() forms.
4. tp(MT) = |{ t ∈ D' : conf(t) ≥ CT*(MT) ∧ mrgF(t) ≥ MT }|.

Global optimum = argmax over the 4 × |candidates| evaluations.

**Exactness argument (frozen):** for fixed MT, tp is monotone non-increasing
in CT, so the smallest feasible CT maximizes tp on that MT-slice; CT*(MT) is
exactly that smallest feasible CT (any smaller CT admits a wrong or a full
pair). Both feasibility and tp are constant for MT between consecutive
candidate values (they change only at mrgF+1 / mrgF values), so the sweep
covers every distinct slice. The sweep therefore returns the true global
optimum of §4 under §5 — no heuristic, no sampling.

**Tie-break (frozen, deterministic total order):** (1) larger tp;
(2) larger MT (more conservative margin among equal-throughput optima —
defense-first); (3) smaller CT; (4) larger ST+AT. First by this order wins;
the Zag program implements the comparison verbatim.

## 7. Baseline "current bar" (frozen definition)

(CT=700, MT=0, ST=1, AT=1): pass iff conf ≥ 700 ∧ strong=1 ∧ agree=1 — the
conf≥700 high-conf admission (O1 prereg §2.2) over the (g) disjoint-span
check (agree/strong both 1). Trial 1145 (874, 10410, 1, 1) passes it, as the
audit states. Reported for comparison: true-PASS, C1 violations, C2
violations, B false-PASS.

## 8. Kill bar (frozen, verbatim from fable audit Q6)

**KB-M1: KILL the recalibration iff the optimized bar yields RK-3 < 82%**,
i.e. true-PASS < 904/1,102. (82% = the 85% program target minus the 3pp
frozen-data overfitting tolerance.) If killed, the current bar stands and
M1 is dead; if not killed, the optimized thresholds ship WITH the §9
diagnostics attached.

## 9. Diagnostics (reported, never kill — frozen list)

- D1: per-constraint verification: C1 false-PASS count (must be 0), C2
  false-install pair count (must be 0), each computed independently by
  `score_m1.py` from the Zag output.
- D2: broad-wrong false-PASS: |{ t ∈ B : PASS(t) }| / 1109 under the
  optimized bar vs the baseline bar.
- D3: trial-1145 disposition under the optimized bar (passes / blocked).
- D4: baseline-bar numbers (§7) vs optimized-bar numbers, all four metrics.

## 10. Determinism & toolchain (frozen)

- Pure Zag for the instrument (`m1_grid.zag`); zero RNG anywhere.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Fixture `m1_cases.txt` derived deterministically by `gen_m1.py` (glue, never
  the instrument) from the §2 sources; line format
  `K|…` with K ∈ {C, W, P, B}: `C|conf|mrgF|strong|agree` (1,102),
  `W|conf|mrgF|1|1` (12), `P|pairid|conf|mrgF|1|1` (18),
  `B|conf|mrgF|strong|agree` (1,109). Fixture sha256 recorded in the runlog
  before any build.
- 3 runs; sha256(stdout) must match byte-identically across all three, else
  VOID. `score_m1.py` independently recomputes every reported number from the
  fixture + thresholds (Python mirror of §6, never the instrument).
- znc build notes honored: []u8 arenas with explicit LE accessors for all
  indexed tables (never `as []i32`); no slice > 2^25 bytes.

## 11. Commit plan (frozen)

1. This prereg — committed ALONE, before any fixture/build/output exists.
2. Then: `gen_m1.py` + `m1_cases.txt` + `m1_grid.zag` + `R33_NATIVE_IO_V1.zag`
   + build + `evidence/` (run1/2/3.txt, DIGESTS.txt) + `RUNLOG_M1.md` +
   `score_m1.py` + `VERDICT_M1.md` — committed after the runs, never any
   binaries or `.zagd` files.
