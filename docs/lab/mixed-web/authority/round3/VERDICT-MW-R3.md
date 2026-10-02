# VERDICT-MW-R3 — source-authority reliability sweep

Date: 2026-09-22. Prereg: PREREG-MW-R3 + AMENDMENT-A2 (frozen, commit
1b76244) + AMENDMENT-A3 (frozen before new blocks, commit bf623df).
Evidence: 420 synthetic envelopes × 3 arms × 5 runs = 6,300 cells,
all byte-identical within arm; independent oracle recomputed every
decision, citation, candidate chain, and SHA-256 ledger head.
Verdict: **LICENSE WITH THRESHOLD** (narrowed shape + independent
reliability gate). Details below.

## 1. What we tested

The question: when a primary source's newest answer faces equally-new
contradiction, is it worth letting the loose authority rule
(PRIMARY_LOOSE) converge where the conservative round-1 rule withholds?
We varied the primary source's reliability across 9 levels (30%→99% of
cases where the primary is right) and measured expected value, separately
for two dispute shapes:

- **Corroborated dispute** (Block R, 180 envelopes): someone else backs
  the primary's answer.
- **Uncorroborated dispute** (Block U, 180 envelopes): nobody backs the
  primary's answer; two rivals contradict it with equally-fresh evidence.
  This is the round-1 R03 shape — the only place the two rules disagree.

Plus: 40 envelopes with no reliability given (can the rule judge
reliability from the dispute itself?), and 20 genuine 2v2 ties (what does
fiat-breaking cost?).

## 2. The headline correction (AMENDMENT-A3, measured)

The sealed battery proved the prereg's expectation wrong: **the
conservative rule already converges on corroborated disputes.** Its
frozen rule is "corroboration OR uncontradicted" — corroboration wins even
against equally-new contradiction. The binary (frozen round-1 artifact) is
correct; the prereg's prediction was wrong. Consequences:

| Shape | Deliberate (B) | Conservative (C) | Loose (D) |
|---|---|---|---|
| Corroborated dispute | withholds | **converges** | converges (identical) |
| Uncorroborated dispute | withholds | withholds (veto) | **converges** |
| Genuine 2v2 tie | withholds | **converges (fiat)** | **converges (fiat)** |

- On corroborated disputes, loose and conservative are **verdict-identical
  on all 180 envelopes**: the loose rule adds literally nothing there
  (measured value delta +0.00 at every reliability level).
- On genuine ties, **both** rules fiat-break: 20/20 convergences, 10/20
  wrong guesses (50%), 100% false-confidence — for EACH rule. The tie
  risk is not unique to loosening.

## 3. Reliability × value: loose vs conservative (Block U — the real margin)

Value per case: correct convergence +1, wrong convergence −1, withhold 0.
The conservative rule withholds on all of Block U (value 0), so the
table below IS the loose rule's marginal value over the status quo.

| Primary reliability | Primary right / wrong | Expected value of loosening |
|---|---|---|
| 0.30 | 6 / 14 | **−0.40** |
| 0.40 | 8 / 12 | **−0.20** |
| 0.50 | 10 / 10 | **0.00** |
| 0.60 | 12 / 8 | **+0.20** |
| 0.70 | 14 / 6 | **+0.40** |
| 0.80 | 16 / 4 | **+0.60** |
| 0.90 | 18 / 2 | **+0.80** |
| 0.95 | 19 / 1 | **+0.90** |
| 0.99 | 20 / 0 | **+1.00** |

All 9 levels matched the predicted 2r−1 exactly. Measured crossover
(linear interpolation between the 0.40 and 0.50 levels): **r* = 0.50**.
Below 50% reliability, loosening destroys value; above, it creates it.

## 4. When a wrong install costs more than a right one earns

If installing a falsehood costs k× what a correct convergence earns:

| Wrong-install cost k | Minimum reliability to break even |
|---|---|
| 1 (symmetric) | **0.50** |
| 2 | **0.667** |
| 3 | **0.75** |
| 5 | **0.833** |

Rule: fire only if independently-established reliability ≥ k/(k+1).

If the rule fires only when reliability is independently established at
or above a threshold t, the expected value per case over the qualifying
levels is: t=0.50 → +0.557; t=0.60 → +0.650; t=0.70 → +0.740;
t=0.80 → +0.825; t=0.90 → +0.900; t=0.95 → +0.950.

## 5. Can the rule judge reliability from the dispute itself? No.

Two dispute-internal estimators were tested on 40 envelopes with no
reliability given. Both are **twin-identical**: envelopes with
byte-identical rows but opposite truth get identical scores, by
construction (the rows carry no information about who is right).
The strict estimator admits nothing (value 0); the lenient one admits
everything-or-nothing (value 0). **No self-estimated reliability can ever
gate this rule into positive value.** The reliability gate MUST come from
outside the dispute — track record, not the case at hand. This held on
both the corroborated and uncorroborated shapes.

## 6. The tie problem (both rules)

On 20 genuine 2v2 ties: the loose rule converged 20/20, guessed wrong
10/20 (50%), and was 100% falsely confident. The conservative rule did
exactly the same (20/20, 10/20, 100%). Neither rule may fire on a
genuine tie; both currently do when the primary's answer has a
corroborator. **Tie shapes are parked for both rules** pending a
tie-shape guard (withhold on 2v2 splits).

## 7. Recommendation: LICENSE WITH THRESHOLD

1. **License PRIMARY_LOOSE only for the uncorroborated-dispute shape**
   (primary's newest answer has zero corroboration, faces equally-new
   contradiction, deliberate withholds) — this is the ONLY shape where it
   changes anything versus the conservative rule. Round 2's license is
   narrowed: on the corroborated shape the conservative rule already
   converges, so the loose rule is redundant there, not licensed-there.
2. **Gate it on independently-established primary reliability**
   r ≥ k/(k+1) (k = wrong-install cost multiple). Symmetric costs: r ≥ 0.50.
   Never on self-estimated reliability — proven worthless (§5).
3. **Park tie shapes for BOTH rules** until a tie guard exists (§6).

## 8. Residual risk

The license is only as good as the reliability estimate's independence —
if the "track record" is contaminated by the dispute at hand, the
twin-identity result proves no in-case signal can rescue the decision;
and until the tie guard exists, both rules will confidently install
falsehoods on corroborated 2v2 ties half the time.

## 9. Evidence and reproduction

- Envelopes, generator, oracle: `mixed-web/authority/round3/`
  (`gen/gen_mw_round3.py`, `verify_mw_round3.py`, `manifest_r3.txt`).
- Evidence: `mixed-web/authority/round3/evidence/` (15 logs + SHA256SUMS);
  5/5 runs byte-identical per arm; all self-checks pass.
- Kill bars: DET, ORACLE (1,260 cells × decisions/citations/chains/heads),
  MIX, CONS (corrected), SHAPE, U-SHAPE, U-ORACLE, U-VALUE — **all hold**.
- Pure Zag, zero RNG in every decision path; no binaries or caches committed.
