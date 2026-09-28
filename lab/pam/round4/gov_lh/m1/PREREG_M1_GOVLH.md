# PREREG — M1 Threshold Adoption: Held-Out Wrongs at Long Horizon (PAM Round 4, Gov-LH Crew 4)

**Date:** 2026-09-24. **Crew:** Gov-LH Crew 4 (subagent).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Status:** FROZEN — committed alone
before any fixture generation, build output, or measurement exists.
This document is the single source of truth; the fixture generator
(`gen_m1_govlh.py`), the Zag instrument (`m1_govlh.zag`), and the scorer
(`score_m1_govlh.py`) all derive from it. No transcription — every family
rule, jitter constant, threshold, and reporting number below is extracted by
script from the cited frozen sources, never from memory.

## 0. Motivation (frozen evidence)

PAM Round 3 M1 verdict (`~/workspace/tnn-lab/pam/round3/m1/VERDICT_M1.md`):
the exact optimum bar **OPT = (ST=0, AT=0, CT=705, MT=3588)** yields
RK-3 = 910/1,102 = 82.58% ≥ 82% (kill line 904), with 0 false-PASS on the 12
TMB-5 wrongs and 0 false installs on the 9 CC1 pairs. Residuals:

- **R1:** the optimizer disabled the strong/agree arms; broad-wrong
  false-PASS explodes **7 → 712/1,109**. Safety-constrained variant
  **SAFE = (ST=1, AT=1, CT=705, MT=3588)** scores 671/1,102 = 60.89%.
- **R2:** six trials of headroom above the 82% line; the 3pp overfitting
  tolerance is nearly exhausted.
- **R3:** the W/P fixtures carry no strong/agree, so the bar was tuned
  against conf/margin only.

**Governance question for Micah (NOT resolved here):** adopt (0,0,705,3588)
as the bar, or hold it as a measurement only? This crew produces
decision-grade evidence: held-out wrong batteries at 10x/100x, the broad-
wrong explosion at scale, headroom in trials, and adversarial wrongs aimed
at the disabled arms. No kill bar is set by this prereg — the numbers are
reported with explicit pass/fail statements per §8, and the adoption call is
Micah's.

## 1. The bars (frozen)

A trial PASSES a bar iff all four hold:

    PASS(t; ST,AT,CT,MT) <=> conf(t) >= CT AND mrgF(t) >= MT
                            AND strong(t) >= ST AND agree(t) >= AT

| Bar  | ST | AT | CT  | MT   | Frozen meaning |
|------|----|----|-----|------|----------------|
| OPT  | 0  | 0  | 705 | 3588 | Round-3 exact optimum (arms disabled) |
| SAFE | 1  | 1  | 705 | 3588 | Safety-constrained: same CT/MT, arms ON |
| BASE | 1  | 1  | 700 | 0    | Round-3 baseline bar (reference only) |

## 2. Frozen data (read-only; scripts extract, never transcribe)

| # | Source (frozen) | sha256 |
|---|---|---|
| F | `~/workspace/tnn-lab/pam/round3/m1/m1_cases.txt` | `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611` |

Row kinds in F: `C` (1,102 correct, RK-3 denominator), `W` (12 TMB-5
calibration wrongs), `P` (18 rows = 9 CC1 wrong pairs), `B` (1,109 broad
wrongs, diagnostic-only in Round 3 — never constrained the §4/§5 search).

**"Held-out" definition (frozen here):** a wrong family is held-out iff no
member was in the calibration constraint sets (the 12 W wrongs + 9 P pairs).
The B set never constrained the search, so B-derived families are held-out
by this definition; the genuinely novel *profiles* are the SYNTH families
(§3). This caveat travels with every reported number.

## 3. Novel wrong families (frozen construction rules)

All families are derived deterministically by `gen_m1_govlh.py` from F
(real-data families) or from the frozen grid below (SYNTH families). Zero
RNG. Fixture line formats: `N|fam|conf|mrgF|strong|agree` with
fam ∈ {1,2,3,5}; `Q|pairid|conf|mrgF|strong|agree` for family 4 pairs.

- **N1 "1145-class" (contradiction shape: wrong despite full corroboration):**
  B rows with `strong=1 ∧ agree=1 ∧ conf ≥ 705 ∧ mrgF ≥ 3588`. Real wrongs
  OPT admits that carry the full (g)-check — the pointwise-unadjudicable
  class trial 1145 belongs to. (REAL)
- **N2 "single-arm exploit" (spoof geometry: one arm off):** B rows with
  `(strong=0 XOR agree=0) ∧ conf ≥ 705 ∧ mrgF ≥ 3588`. Real wrongs OPT
  admits that SAFE blocks via exactly one arm. (REAL)
- **N3 "boundary grid" (margin/conf profiles at the frontier):** the full
  cross product `conf ∈ {704,705,706,750,874,1000}` ×
  `mrgF ∈ {3587,3588,3589,5000,6600,10410}` × `strong ∈ {0,1}` ×
  `agree ∈ {0,1}` = 144 synthetic wrongs. Geometry probes of the bar: the
  (705, 3588) corner passes OPT by equality; (704,·) and (·,3587) probe the
  knife-edges. (SYNTH)
- **N4 "corroborated wrong pairs" (spoof geometry: pair install):** from the
  N3 points with `strong=1 ∧ agree=1` that PASS OPT at exact geometry,
  sorted by (conf, mrgF) ascending, paired consecutively
  ((0,1),(2,3),…) as `Q` rows. Tests pair-installs of confidently-wrong
  corroborated pairs — defeats both OPT and SAFE by construction, isolating
  the conf/margin-only protection. (SYNTH)
- **N5 "double-arm exploit" (adversarial: the discarded class):** B rows
  with `strong=0 ∧ agree=0 ∧ conf ≥ 705 ∧ mrgF ≥ 3588` (REAL) **plus**
  synthetic engineered points
  `conf ∈ {874,1000} × mrgF ∈ {6600,10410}` at `strong=0, agree=0`
  (4 SYNTH rows: high-conf, high-margin, both arms off — the exact class the
  optimum discards protection against).

**Partition property (frozen check):** at exact geometry (no jitter), N1 ∪
N2 ∪ N5-REAL = { B rows : PASS(B; OPT) }, disjoint. The scorer asserts this
equality; if it fails, the run is VOID.

## 4. Long-horizon scale & deterministic jitter (frozen)

Scales **S ∈ {1, 10, 100}**. Each fixture row r is evaluated S times
(replicas k = 0 … S−1) with deterministic per-replica jitter:

    jit_c(r,k) = 0                                           if k = 0
               = ((k·2654435761 + r·40503) mod 7) − 3        otherwise
    jit_m(r,k) = 0                                           if k = 0
               = ((k·40503 + r·2654435761) mod 7) − 3        otherwise
    conf'(r,k) = conf(r) + jit_c(r,k)
    mrgF'(r,k) = mrgF(r) + jit_m(r,k)

All arithmetic i64, non-negative operands (products fit: max ≈ 1.1e13).
**S=1 anchor:** k=0 only, zero jitter — the instrument must reproduce the
Round-3 numbers exactly (opt_true_pass=910, diag_b_fp=712, base_b_fp=7,
W FP=0, P installs=0, safe_true_pass=671); else VOID.

The jitter simulates deployment remeasurement (±3 units): it probes
knife-edge passes (conf=705, mrgF=3588 exactly) and wrong-side flips, with
zero RNG and byte-identical reruns.

## 5. Measurements (frozen; the Zag instrument reports all of them)

For each S ∈ {1,10,100}, under OPT and SAFE (BASE only where noted):

- **M1 held-out false-PASS:** per family (W, P, B, N1, N2, N3, N4, N5):
  counts of rows/replicas passing; for P and N4, pair-install counts
  (both members pass). W and P at S=1 must be 0 (anchor).
- **M2 broad-wrong at scale:** B false-PASS counts and rates under
  OPT / SAFE / BASE; decomposition of the OPT count into N1+N2+N5-REAL
  (partition check §3); the OPT−SAFE gap = wrongs admitted *only* because
  ST=AT=0 (the structural cost).
- **M3 headroom:**
  - H-trial(S) = tp_OPT(S) − ceil(0.82 × 1102 × S), tp over S×1102 C replicas.
  - H-absorb = max k ∈ ℕ with 910/(1102+k) ≥ 0.82 (additional bar-failing
    correct trials absorbable before the 82% line breaks).
  - H-knife = #{C rows passing OPT with conf = 705} and #{… with mrgF = 3588}
    (passes flippable by 1-unit remeasurement).
  - H-jitter(S) = #{(passing C row, replica k≥1) that FAIL}
    (fragile true passes); #{(blocked wrong row in N1∪N2∪N3∪N5, k≥1) that PASS}
    (wrong-side flips — the dangerous direction).
- **M4 adversarial:** N5 false-PASS under OPT vs SAFE at each S
  (expectation under the bar geometry: OPT admits all, SAFE blocks all —
  reported, not assumed).

## 6. Determinism & toolchain (frozen)

- Pure Zag for the instrument (`m1_govlh.zag`); zero RNG anywhere
  (the jitter is a closed-form function of (r,k)).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Fixture `m1_govlh_cases.txt` derived deterministically by
  `gen_m1_govlh.py` (glue, never the instrument) from the §2 source;
  fixture sha256 recorded in the runlog before any build.
- **3 runs** (task minimum is 2); sha256(stdout) must match byte-identically
  across all three, else VOID. `score_m1_govlh.py` independently recomputes
  every reported number from the fixture + §1 bars + §4 jitter (Python
  mirror of §§3–5, never the instrument), including the S=1 anchor
  reproduction and the §3 partition equality.
- znc build notes honored: []u8 arenas with explicit LE accessors for all
  indexed tables (never `as []i32`); no slice > 2^25 bytes; arena sizing for
  ≤ 4096 fixture rows (rows stored once; replicas evaluated in an inner
  loop — no storage blowup).

## 7. Commit plan (frozen)

1. This prereg — committed ALONE, before any fixture/build/output exists,
   to branch `tnn-native-lab` at
   `docs/lab/pam/round4/gov_lh/m1/PREREG_M1_GOVLH.md`.
2. Then: `gen_m1_govlh.py` + `m1_govlh_cases.txt` + `m1_govlh.zag` +
   build + `evidence/` (run1/2/3.txt, DIGESTS.txt) + `RUNLOG_M1_GOVLH.md` +
   `score_m1_govlh.py` + `VERDICT_M1_GOVLH.md` — committed after the runs,
   never any binaries, `.zagd`, or `.zag-cache`.

## 8. Reporting standards (frozen; measurement, not kill)

- **HELD-OUT CLEARANCE:** stated as CLEAR iff OPT shows 0 false-PASS on every
  novel family (N1–N5) at every scale; otherwise the counts, rates, and the
  OPT−SAFE gap are reported per family — the evidence Micah needs for the
  adoption question.
- **STRUCTURAL vs ARTIFACT:** the 7→712/1109 explosion is STRUCTURAL iff the
  OPT−SAFE gap on B persists at the same rate at 10x/100x with the N1/N2/N5
  partition intact; else ARTIFACT with the scale at which it breaks.
- The verdict **recommends nothing about adoption** — it reports the four
  legs and states plainly what OPT protects against and what it abandons.
