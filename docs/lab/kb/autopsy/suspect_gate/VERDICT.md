# VERDICT — KB4 SUSPECT-gate trial (PACKAGE 1)

**Frozen prereg:** `kb/autopsy/PREREG_FROZEN_SUSPECT_GATE.md` (FROZEN
2026-09-22, Micah's signature: "go ahead and run test accordingly").
Freeze commit: `50ba82a8f5b9b312eba3bbb5c7c839ea3e6b66e9`
(tnn-native-lab). Split manifest independently recomputed from truth.json:
byte-identical (93 calibration / 92 test).

**What ran:** pure-Zag three-state gate (`suspect_gate.zag`, zero RNG) on
the frozen KB4 batches (A: 924 lines / 184 adversarial fixtures; B: 925 /
185). Channel = 6-entry per-class P(truth preserved | class) from
CALIBRATION truth only (human-verification stand-in). Thresholds frozen a
priori: τ_hi=0.9, τ_lo=0.1. Three repetitions, SHA256 byte-identical
within each sense (A: `0f5ae350…`, B: `4b421a35…`). Ledger hash chain
verified line-by-line against an independent Python recomputation
(fields, decisions, prevhash links, SUMMARY, chain head — all match).

## The channel, honestly

Calibration-only estimates (per-mille):

| class | preserved/total | p_c | band |
|---|---|---|---|
| colordisc | 26/30 | 0.867 | SUSPECT |
| colorconst | 20/20 | 1.000 | HIGH (≥0.9) |
| shapetrans | 22/45 | 0.489 | SUSPECT |
| pitchdisc | 12/30 | 0.400 | SUSPECT |
| timbredisc | 8/30 | 0.267 | SUSPECT |
| motiondir | 4/30 | 0.133 | SUSPECT |

Only **colorconst** clears a threshold. Every other class SUSPECTs every
fixture, match or differ. (For reference, the full-data oracle values from
the why-swarm were the complement's mirror — e.g. motiondir 0.90 changed =
0.10 preserved — but the freeze mandates calibration-only, and
calibration says otherwise. That gap is itself a finding: the channel is
data-starved.)

## Bars (TEST split, pooled A+B, n=184)

| Bar | Result | Bar | Met? |
|---|---|---|---|
| B1 false-install rate on INSTALL decisions | 3/15 = **20.0%** | ≤ 10% | NO |
| B2 SUSPECT correct-abstention | 76/164 = **46.3%** | ≥ 80% | NO |
| B3 silent poison (unverified INSTALLs) | **0** | = 0 | YES |
| B4 true INSTALLs on adversarial fixtures | **12** | ≥ 40 | NO |

**Verdict: MARGINAL** (B3 = 0, not all four met). Per-sense: A —
B1 0.0%, B2 47.6%, B4 9; B — B1 50.0%, B2 45.1%, B4 3. SUSPECT rate 89.1%
both senses.

## Confusion: gate decisions vs truth (test, pooled)

| gate \ truth | adv correct (99) | adv wrong (85) |
|---|---|---|
| INSTALL (15) | 12 | 3 |
| WITHHOLD (5) | 4 | 1 |
| SUSPECT (164) | 83 | 81 |

Per class (test): colorconst 20 → 15 INSTALL (12 true / 3 false), 5
WITHHOLD, 0 SUSPECT. All other classes → 100% SUSPECT (164 fixtures).

## Diagnostics (frozen)

- **Withheld-true rate:** 4/99 = **4.0%**. All four are colorconst
  differ+high-p → WITHHOLD where the sense had *self-corrected* (wrong on
  primary, right on adversarial, truth preserved). The channel is
  world-side: it cannot see sense-side self-correction, so it reads every
  differ on a preserved-truth class as fooling.
- **SUSPECT rate:** 164/184 = **89.1%**.
- **Resolution latency:** channel compute per fixture is O(1) — one
  6-entry lookup + ≤2 integer comparisons, no iteration, no search.
  Measured end-to-end: ~7–17 ms per adversarial fixture wall-clock
  (1.2–3.1 s per full batch run), dominated by the SHA256 hash-chained
  ledger writes, not the decision. **Fraction never resolved: 89.1%** —
  SUSPECT is terminal in this trial; live SUSPECTs would route to human
  verification per standing law (not exercised here).
- B2 diagnostic (strict parenthetical): differ-and-adv-correct SUSPECTs =
  41/164 = **25.0%**; differ-fraction among SUSPECTs = 87/164 = 53.0%.

## The honest answer

**Does SUSPECT resolve the false-install ceiling?** Structurally, yes;
empirically, not yet. The gate does exactly what the autopsy asked for:
it stops gambling on unresolvable cases — 89% of adversarial fixtures
are now flagged SUSPECT instead of being force-installed or
force-withheld, and the silent-poison failure mode is **structurally
zero** (every INSTALL is channel-verified; the ledger proves it). The old
gate's 41–46% failure came from being *forced to bet*; the new gate
refuses the bet.

**At what cost?** Three costs, all measured:

1. **The channel verifies almost nothing.** Calibration-only data puts
   one of six classes above τ_hi and none below τ_lo, so 89% of fixtures
   SUSPECT. The abstention is honest, but at 89% the human-verification
   backup (standing law) becomes the primary path — which does not
   scale. The missing ~1 bit is still missing on five classes.
2. **Verified ≠ correct.** B1 fails at 20%: all 3 false installs are
   M2 consistent-error cases — judgment wrong on *both* variants, truth
   preserved, channel says "preserved" and the gate installs. The
   channel verifies *truth-preservation*, not *judgment correctness*;
   that is the exact residual risk the freeze said B1 would measure,
   and it measured it.
3. **The channel eats self-corrections.** The 4 withheld-true cases are
   the sense getting it right on the adversarial variant after being
   wrong on primary — differ+high-p reads them as "fooled" and withholds
   truth. A cross-time consistency signal could separate self-correction
   from fooling; the frozen design has none.

**On B2 (46% vs 80%):** the bar's operationalization punishes abstentions
where a blind gamble would have been right — which is most match-cases
(P(adv correct|match) ≈ 0.57). By the autopsy-§6 philosophy
("correct-SUSPECT counts as a positive") those abstentions are the *right*
move under unresolvable uncertainty; by B2's scoring they are failures.
This tension needs Micah's ruling before the bar is reused: is a
"would-have-been-right-by-luck" abstention a failure of the gate, or the
gate doing its job?

## Repair cycle (MARGINAL → next)

1. **More informative channel.** Five of six classes sit in the SUSPECT
   band. Options the freeze anticipated: more calibration fixtures per
   class, finer perturbation classes, or the more-info channel shootout
   already dispatched (causal perturbation / cross-time consistency /
   multi-source / consultant-invented) to find what delivers the missing
   bit.
2. **B2 bar ruling.** Decide whether correct-abstention (as
   operationalized) or correct-SUSPECT (autopsy §6 philosophy) is the
   scoring rule. They disagree by construction.
3. **Primary-correctness signal for verified classes.** B1's 20% is all
   M2 — the why-swarm's residual falsifier #1. The channel needs a
   companion signal for "was the primary judgment itself right," or
   match+high-p INSTALL stays a gamble on the sense's consistency.
4. **Self-correction vs fooling.** The 4 withheld-true cases are a
   cross-time consistency question the frozen channel cannot ask.

## Reproducibility

- Gate source: `suspect_gate.zag` (+ `R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag` substrate copies). Build:
  `znc_linux_x86_64_abed8aa1 suspect_gate.zag -o suspect_gate --no-analyze`
  (run from this directory; @imports resolve relative to cwd).
- Inputs: `classmap.txt` (370 stim→class), `segments_A/B.txt` (frozen
  block layout), `channel.txt` (6 per-mille values; see
  `channel_table.json` for exact rationals + quantization check).
- Runs: `./suspect_gate . batch_{A,B}.txt segments_{A,B}.txt classmap.txt
  channel.txt {A,B}` — batches are the frozen
  `prose-learning/epistemic_wave/kb4_rerun/batch_{A,B}.txt` (copies
  included for convenience; byte-identical to frozen).
- 3 reps SHA256-identical per sense; scores identical across reps
  (asserted in `score_run.py`).
- Never committed: binaries, `.zagd` caches.

*All numbers above are from TEST-split scoring only. Calibration truth
was used solely as the channel's training set (committed as
`channel_table.json`); test truth never entered any gate or channel
binary.*
