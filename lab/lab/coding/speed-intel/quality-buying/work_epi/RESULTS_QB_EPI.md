# QB-EPI — RESULTS (epistemic domain)

**Date:** 2026-09-22 · **Crew:** QB-EPI build crew · **Branch:** `tnn-native-lab`
**Frozen prereg:** `coding/speed-intel/quality-buying/PREREG_QB.md`
(commit `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b` — NOT amended)
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Battery (frozen, reused byte-identical from `work_a1r/epi/`):**
`b12_false.txt` + `b12_true.txt` + `c70.txt` = 94 items;
intended verdicts from `battery_a1r_items.json`
(falsehood→WITHHOLD, true→ENDORSE, weird-nonfactual→WITHHOLD).
**Build:** `delib_qb.zag` (modes d0–d5 via argv[2]), pure Zag, zero RNG in
any decision path. Substrate copies (`R33_NATIVE_IO_V1.zag`,
`R33_NATIVE_SHA256_V2.zag`) vendored next to the source so the build is
reproducible from this directory (`@import` resolves relative to cwd).

## 1. Per-arm results (3 reruns per cell; rep-1 values shown, all cells identical)

| arm | Q_e /94 | ΔQ vs D0 | false /12 | true /12 | weird /70 (fam tallies /10) | preds/item | Δcost (preds) | wall s | cpu s | determinism |
|-----|---------|----------|-----------|----------|------------------------------|------------|---------------|--------|-------|-------------|
| D0 (knee baseline) | **59/94** | — | 12 | 12 | 35 — joke 5, sarc 3, hyp 5, anal 3, poet 5, cf 9, impl 5 | 9.000 | — | 0.036 | 0.005 | IDENTICAL |
| D1 (conflict-driven) | 59/94 | +0 | 12 | 12 | 35 — same fams | 10.117 | +105 | 0.046 | 0.014 | IDENTICAL |
| D2 (3 critic rounds) | 12/94 | **−47** | 0 | 12 | 0 — all fams 0 | 12.000 | +282 | 0.074 | 0.008 | IDENTICAL |
| D3 (hypothesis competition) | 59/94 | +0 | 12 | 12 | 35 — same fams | 12.000 | +282 | 0.058 | 0.007 | IDENTICAL |
| D4 (one-brain phases) | 58/94 | **−1** | 12 | 12 | 34 — sarc 2 (rest same) | 12.000 | +282 | 0.050 | 0.007 | IDENTICAL |
| D5 (combined) | 59/94 | +0 | 12 | 12 | 35 — same fams | 17.117 | +763 | 0.046 | 0.016 | IDENTICAL |

Cost currency is pred-evals per prereg §5 (every predicate-function
evaluation = 1; every named deliberation step = 1). Wall/CPU are
sub-second for all arms and are not the binding cost.

## 2. Kill-bar verdicts

| bar | verdict |
|-----|---------|
| QB-DET (3 reruns, canonical logs byte-identical, zero RNG) | **PASS all cells** — 6/6 IDENTICAL |
| QB-CAL (D0 reproduces knee: 59/94 at 9.000 preds/item, A1R digest) | **PASS** — 59/94, 9.000/item, digest `57cefaa4…23bd650` matches the frozen A1R 2x digest exactly; verdict lines byte-identical to `out_b2_*.txt` |
| QB-QUALITY (arm scores iff Q_e > 59/94) | **no arm scores** — best non-baseline is 59/94 (D1/D3/D5 tie D0); D2 and D4 regress |
| QB-WORTH (marginal price per +1 item < 90 pred-evals) | **n/a** — no scoring arm; ΔQ ≤ 0 for every deeper arm, so no marginal price exists |
| QB-CEILING | **CEILING-CONFIRMED (epistemic domain)** — "the knee is the ceiling of deliberation; further quality must come from new mechanisms or new knowledge, not more compute." |

## 3. Quality-per-cost curve vs D0

ΔQ is flat at 0 (or negative) while Δcost grows monotonically:

- D1: +105 preds, +0 items — conflict classification + deep specificity
  resolution on 11 conflicted items (10 falsehoods + W152); every deep
  resolution agrees with the staged verdict.
- D3: +282 preds, +0 items — the separately-written competition path
  (S_W = 4·kf+3·ab+2·matchers vs S_E = 4·kt+cm2+quiet-prior) agrees with
  the staged pipeline on all 94 items.
- D5: +763 preds, +0 items — the most expensive arm buys nothing; its d3
  final stage silently reverts every flip its d2/d4 stages made (see §4).
- D2: +282 preds, **−47 items** — deeper deliberation that destroys quality.
- D4: +282 preds, **−1 item**.

No arm has a finite marginal price per +1 item (there is no +1).

## 4. Mechanism notes — every verdict change vs D0

**D1 — 0 flips.** 11 items classified conflicted (pro≥1 AND con≥1): 10
falsehoods (kf + CM2 assertion-form, e.g. F901 "…triangle has 4 sides."
has " is "+digit) and W152 (sarcasm matcher + CM2). Deep specificity
resolution (kf=kt=4 > ab=3 > matcher=2 > cm2=1; cross-side tie keeps
staged) resolves all 11 pro-side → WITHHOLD, identical to staged.
Reason codes in log: `conf=1|pmax=1|cmax=5|win=0` (falsehoods),
`conf=1|pmax=3|cmax=5|win=0` (W152). Conflict-driven deliberation is
real machinery that changes nothing here: the conflicts are all
style-vs-world-knowledge, and world knowledge always wins.

**D2 — 47 flips, all in the wrong direction (WITHHOLD→ENDORSE, all
intended WITHHOLD).** Round-1 challenges: `ch0=1` (kf) on all 12
falsehoods, `ch0=2/3/4/5/6/7/8` (the single fired matcher) on 35 weird
items. Every flipped item had exactly ONE fired nonfactual bit, so the
frozen mechanical validity rule ("names ≥1 fired evidence bit whose
removal changes the verdict") admits the challenge, and the verdict
flips. Rounds 2–3 pass (`ch1=0|ch2=0`): against the flipped ENDORSE
verdict, bit-removal can never change the outcome, so no further valid
challenge exists — the damage is done in round 1 and is irreversible
within the 3-round budget. Items with ≥2 fired bits (none on this
battery — max is 1) and items with 0 fired bits (the 12 true controls,
which survive: 12/12) are untouched. Finding: critique governed only by
the mechanical validity rule attacks precisely the thin-but-correct
evidence — single-bit items are where the pipeline is most often right
(47/47 of the flips were correct→wrong). "No free-form second-guessing"
turns out to also mean "no judgment about whether the challenge is
sensible."

**D3 — 0 flips.** The competition path is genuinely separately written
(weighted evidence sums, not the staged rule's disjunction), yet
S_W > 0 ⟺ staged WITHHOLD on this battery, and S_E > S_W never occurs
(it would need kt=1 co-firing with a lone matcher — absent here). Same
ledger, same verdicts: the ledger is the binding constraint, not the
decision procedure.

**D4 — 1 flip: W152 WITHHOLD→ENDORSE (wrong).**
`W152|…|arg=3|syn=1` — "Wonderful, the alarm is set for 6 AM on a
Saturday." The challenger disputes the lone sarcasm matcher (arg=3);
synthesis upholds it because the withhold case is style-only (kf=ab=0)
and a con marker is present (cm2=1: " is " + digit "6"). The upheld
challenge is wrong: CM2 (assertion-form + digit) is a structural
heuristic, not counter-evidence, and the synthesis rule over-trusts it.
Notably W152 is exactly the "rare conflicted item" class the prereg
named as the realistic best case — the deeper arm got the best-case
item wrong, not right.

**D5 — 0 net flips, but 48 internal flips reverted.** Stage trace
(`v1|v4|v2|flips|sw|se`):
- F901: `v1=0|v4=0|v2=1|flips=1|sw=4|se=1` — d2 flips the kf item to
  ENDORSE; d3 (sw=4 > se=1) restores WITHHOLD.
- W152: `v1=0|v4=1|v2=1|flips=0|sw=2|se=1` — d4 upholds the challenge
  (ENDORSE); d2 passes; d3 (sw=2 > se=1) restores WITHHOLD.
- All 35 d2-flipped weird items show the same rescue pattern
  (`v2=1`, final WITHHOLD via sw>se).
D5 is a working demonstration of composition-as-stabilizer: the
competition stage vetoes every destructive flip from the earlier
stages, at 17.117 preds/item — nearly 2× the knee cost for the knee
verdicts.

## 5. Honest limits

1. Prereg §7 stands: the 35/70 weird-English misses fire no nonfactual
   predicate by construction; their ledgers are indistinguishable from
   true controls to any deterministic function of the ledger, and §4
   forbids new predicates. No deliberation structure tested here can
   recover them — confirmed empirically: three different structures
   (D1/D3/D5) converge exactly to the staged verdicts.
2. D2's destructiveness is a property of the FROZEN challenge-validity
   rule as written, not of critique in general. A validity rule that
   required the challenger to supply positive counter-evidence (as D4's
   synthesis does) would not flip single-bit items — but D4 shows even
   that rule misfires on the best-case item.
3. Single-threaded substrate: D4's "sub-deliberations" are sequential
   phases; the measured cost is pred-evals, not wall-clock parallelism.
4. The reading choices frozen for this build (prereg ambiguities):
   (a) D2 "the staged pipeline's verdict" = the verdict currently under
   challenge; (b) reinterpretation ≡ removal (no new predicates may give
   it other content); (c) repeat challenges across rounds are permitted
   (rounds are independent trials); (d) D4 synthesis upholds iff the
   disputed bit is style-level AND kf=ab=0 AND ≥1 con marker present;
   (e) D5 = sequential pipeline d1→d4→d2→d3 with d3 as final decider;
   (f) cost = 1 per predicate evaluation + 1 per named deliberation step
   (d0 9; d1 10/11; d2 12; d3 12; d4 12; d5 17/18 per item).
5. This verdict covers the EPISTEMIC domain only; the coding crew reports
   separately (prereg §7.1: coding cells test non-regression + cost).

## 6. Build & reproduction

- Source: `delib_qb.zag` (this dir); build from this dir so `@import`
  resolves the vendored substrate copies:
  `znc_linux_x86_64_abed8aa1 delib_qb.zag -o delib_qb --no-zagd`
- Run (battery stays frozen in `work_a1r/epi/`, never copied):
  `cd ../reflection/speed_intel/work_a1r && <bindir>/delib_qb epi dK <file>`
  (K = 0..5; files `b12_false.txt`, `b12_true.txt`, `c70.txt`).
- Score: `python3 score_qb_epi.py` (from this dir) → `sweep_qb_epi.json`;
  raw logs in `logs/` (3 reps × 6 modes × 3 files).
- Calibration: `logs/out_d0_*_r1.txt` are byte-identical to
  `work_a1r/epi/out_b2_*.txt`; d0 digest
  `57cefaa42100f695d76d906ac7de9a348f55979f466086c83c1a8874e23bd650`
  equals the frozen A1R 2x digest.

## 7. Bottom line

Micah asked whether qualitatively deeper deliberation — a different
kind of compute, not more iterations — can buy quality past the knee.
On the epistemic battery the answer is **no**: four deeper structures
(conflict-driven specificity, multi-round critique, hypothesis
competition, one-brain challenge/synthesis, and all four combined)
produce zero net gains at 1.1–1.9× the knee cost, and two of them
actively destroy quality (D2: −47, D4: −1). The knee is not a budget
artifact — it is the ceiling of what this ledger can decide.
**CEILING-CONFIRMED** for the epistemic domain. Further quality must
come from new mechanisms or new knowledge, not from deliberation
structure.
