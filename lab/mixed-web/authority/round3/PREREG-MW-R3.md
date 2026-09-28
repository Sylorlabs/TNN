# PREREG-MW-R3 — Source-authority RELIABILITY SWEEP (FROZEN 2026-09-22)

Authorized by AMENDMENT-A2 (Micah's 2026-09-22 "investigate the non free
lunch"). Round 2 (PREREG-MW-D / VERDICT-MW-D) found the free lunch
(PRIMARY_LOOSE converts S1A/R03-shaped withholds, VALUE-DELTA = 1) and priced
the non-free lunch qualitatively (S1B: primary wrong → installs error;
S8: genuine tie → fiat guess). The licensed claim was left conditional:
PRIMARY_LOOSE licensed ONLY for the S1A/R03 dispute shape AND only where
the primary source's reliability is independently established. This prereg
freezes the sweep that turns "independently established" into a number:
the reliability levels, the generative model, the value model, the
crossover method, the self-estimation stress, the S8 fiat-cost row, and the
kill bars. No tuning after results.

## R0. Arms and battery (frozen)

Arms (all frozen logic, no retuning):
- **B** — frozen `mw_deliberate` (PREREG §4) verbatim. No authority rule.
- **C** — conservative PRIMARY (PREREG-MW-C M1, the round-1 rule): fires
  only with the condition-4 veto intact. The "conservative round-1 rule"
  baseline for the value comparison.
- **D** — PRIMARY_LOOSE (PREREG-MW-D D1): conditions 1–3 identical, no
  condition-4 veto, no-override guard intact.

Battery: **220 synthetic envelopes**, fictional entities, stipulated golds,
in three blocks (§R1). The frozen 17 envelopes are not rerun (round 2
covers them). 5 byte-identical runs required per arm.

## R1. Envelope generative model (frozen)

All envelopes: temporal=1, question template
`Who won the 2026 {label} grand prix?` where `{label}` is the primary
domain's label. Deterministic name pools (cycled by envelope index j,
0-based within block):

- PRIMARIES: zorbian.com, quellar.org, myndax.net, velkora.io, dravnik.com,
  osselyn.org (labels: zorbian, quellar, myndax, velkora, dravnik, osselyn)
- PAIRS (A1 primary answer, A2 rival answer): (Marco Venn, Luis Okafor),
  (Petra Halvorsen, Dario Mensah), (Ines Kovac, Tomas Reyes),
  (Anya Petrova, Kwame Diallo), (Sofia Marchetti, Jonas Lindqvist),
  (Ravi Chandran, Elena Vasquez)
- RIVALS: racefeed.net, speedway.org, pitwall.io, apexwire.com,
  gridtalk.net, laptime.org
- Envelope j uses PRIMARIES[j mod 6], PAIRS[j mod 6],
  rival1=RIVALS[j mod 6], rival2=RIVALS[(j+1) mod 6],
  corr=RIVALS[(j+2) mod 6], rival3=RIVALS[(j+3) mod 6].

Shape invariants (checked per envelope by the oracle, §R5 KB-R3-SHAPE):
exactly one primary domain (D1.1), its newest answered assertion at the
global max recency 2026 ≥ 2000 (D1.2–D1.3), and arm B WITHHOLD/TIE.

### Block R — reliability sweep: 9 levels × 20 dispute envelopes = 180

Dispute-shape rows (S1 shape):
`(prim, A1, 2026), (prim, A1, 2024), (rival1, A2, 2026), (rival2, A2, 2026),
  (corr, A1, 2025)`.

Reliability levels (frozen): **0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90,
0.95, 0.99**. At level r, n_A(r) = round(20·r) envelopes are S1A-twins
(stipulated gold = A1, the primary's newest answer) and n_B(r) = 20 − n_A(r)
are S1B-twins (stipulated gold = A2). n_A: 6, 8, 10, 12, 14, 16, 18, 19, 20.
Twin placement (deterministic Bresenham interleave, frozen): envelope i
(0-based within level) is S1A iff (i·n_A) mod 20 < n_A.

Each Block-R envelope carries stipulated metadata `rel_ind = r`: the
primary source's reliability, INDEPENDENTLY ESTABLISHED (by construction:
the level is the independent reliability; the dispute rows carry no
reliability information). Qids: R30_00..R30_19, R40_00.., R50_00..,
R60_00.., R70_00.., R80_00.., R90_00.., R95_00.., R99_00...

### Block G — self-estimation stress: 20 dispute envelopes

Same S1 rows and name pools. True mix fixed at 50/50: n_A = 10, same
Bresenham interleave. `rel_ind = UNKNOWN` (not independently established).
Qids: G_00..G_19. The oracle computes two dispute-internal estimators per
envelope (§R3) and the gate analysis is performed on them.

### Block S — S8 fiat-cost row: 20 tie envelopes

Genuine-2v2 rows:
`(prim, A1, 2026), (rival1, A2, 2026), (rival2, A1, 2026), (rival3, A2, 2026)`.
Stipulated gold: UNDETERMINABLE (per Micah's skepticism rule:
undeterminable claims are excluded from true/false scoring — Block S
contributes 0 to net value and is reported as a separate fiat-cost row).
Latent truth (modeling device ONLY, for the wrong-guess rate): A1 iff
(i mod 2 == 0), else A2 — deterministic 50/50, independent of the fiat
pick. Qids: S8_00..S8_19.

## R2. Value model and crossover (frozen)

Per dispute envelope (Blocks R, G), arm-D value vs the conservative
baseline:
- **+1** if D CONVERGE and chosen == stipulated gold (win arm C withholds on);
- **−1** if D CONVERGE and chosen ≠ stipulated gold (installed error);
- **0** if D WITHHOLD.
Arm C is expected to withhold on all 220 envelopes (KB-R3-CONS verifies —
the baseline value is measured, not assumed), so the value delta at level r
is E_r = (Σ V over the level's 20 envelopes) / 20.

Preregistered prediction: D fires PRIMARY_LOOSE on every dispute envelope
(shape invariant) and converges on the primary's newest answer A1, so
E_r = (n_A(r) − n_B(r)) / 20 = 2r − 1 up to the n_A rounding:
-0.40, -0.20, 0.00, +0.20, +0.40, +0.60, +0.80, +0.90, +1.00.

**Crossover** (frozen method): predicted r* = 0.50 (E = 2r−1 = 0).
Measured r* = linear interpolation between the adjacent levels straddling
E_r = 0. Reported as one number with this method stated.

**Sensitivity** (secondary, arithmetic on the measured ±1 rates — no new
runs): if a wrong convergence costs k× a correct convergence gains,
E(k,r) = r − k(1−r) and the crossover is r*(k) = k/(1+k). Reported for
k ∈ {1, 2, 3, 5} → {0.50, 0.667, 0.75, 0.833}, so Micah can set the
threshold from his own false-install cost judgment.

**Licensed-value curve** (frozen): for gate thresholds
t ∈ {0.50, 0.60, 0.70, 0.80, 0.90, 0.95}, licensed EV(t) = mean of E_r over
levels r ≥ t (the gate "fire PRIMARY_LOOSE only where independently
established reliability ≥ t", applied analytically to the measured E_r).

## R3. Self-estimation stress (frozen)

Question: does the S1A win survive when the primary's reliability is
estimated FROM THE SAME DISPUTE rather than independently established?

Preregistered estimators (oracle-computed from dispute-internal rows only):
- r̂_max = (distinct non-primary domains at global max recency asserting
  the primary's newest answer) / (distinct domains at global max recency).
  On the S1 rows: 0/3 = 0.0.
- r̂_all = (distinct domains, any recency, whose newest assertion equals the
  primary's newest answer) / (distinct domains). On the S1 rows: 2/4 = 0.5.

Twin-identity check (frozen): the oracle verifies r̂_max and r̂_all are
EQUAL across every S1A/S1B twin pair (twins share byte-identical rows —
any dispute-internal estimator is twin-identical by construction).

Gate analysis (frozen): for thresholds t ∈ {0.30, 0.50, 0.70, 0.90}, the
gate "fire only if r̂ ≥ t" is applied to Block G; reported per estimator:
admitted S1A count, admitted S1B count, and arm-D value on the admitted
set. Preregistered prediction: no threshold separates the twins — the gate
either blocks both (win destroyed) or admits both (unlicensed gamble at the
block's base rate). Positive control: Block R at r = 0.95 with
rel_ind = 0.95 (independently established) — the gate admits all 20 and the
win is licensed at EV +0.90/case.

## R4. S8 fiat-cost row (frozen)

Arm D is expected to CONVERGE A1 PRIMARY_L (cond4=loose-corrob) on all 20
Block-S envelopes — fiat-breaking a genuine tie. Measured:
- **wrong-guess rate** = #{D chosen ≠ latent truth} / 20, predicted 10/20
  = 50% (latent truths are 50/50 independent of the pick, §R1);
- **false-confidence rate** = #{D CONVERGE recorded with a PRIMARY_L
  citation and no uncertainty marking} / 20, predicted 20/20 = 100% (every
  fiat guess is ledgered indistinguishably from a knowledge-backed S1A
  convergence apart from the rule code).
Arm C and arm B are expected to WITHHOLD on all 20 (verified by binary for
C, by oracle for B). No reliability level is varied for Block S: the
envelopes are reliability-independent by construction, so the fiat-cost row
is reported once. Standing distinction: if a primary source has privileged
access to the truth on the question, the case is NOT S8-shaped — it is an
S1 dispute shape and belongs in Block R. S8 as defined here has no
privileged access, so no reliability level can rescue fiat-breaking.

## R5. Kill bars (frozen)

- KB-R3-DET: 5 runs byte-identical per arm (stdout sha256 × 5; B, C, D).
- KB-R3-ORACLE: the independent oracle recomputes every verdict, chosen
  answer, rule code, candidate chain, citation/supp, and ledger head from
  the envelopes → any mismatch on any of the 220 × 3 arm-envelope cells
  FAILs.
- KB-R3-MIX: per level, the generator manifest's S1A/S1B counts equal the
  preregistered n_A(r)/n_B(r) exactly, and twin positions match the
  Bresenham formula (oracle-checked from the envelope data).
- KB-R3-CONS: arm C (binary-verified) WITHHOLDs on all 220 envelopes —
  the conservative baseline is 0 by measurement.
- KB-R3-SHAPE: oracle derive_b (frozen PREREG §4) WITHHOLDs on all 220
  envelopes — the loose rule is the only thing that can converge.
- KB-R3-CACHE: no binaries or .zagd in the commit.

A HURT finding (S1B −1s, S8 fiat guesses) is a priced finding, not a bar
failure — but a WRONG-bar-style surprise (D converging ≠ A1 on a dispute
envelope, C or B converging anywhere, oracle mismatch) fails the
corresponding bar above.

## R6. Oracle independence (frozen)

`verify_mw_round3.py` is written fresh: it imports ONLY the envelope data
(rows, questions, stipulated golds, levels, latent truths) from the
generator module — never its mechanism functions. It reimplements
separately: derive_b (PREREG §4), the loose rule (PREREG-MW-D D1), the
conservative rule (PREREG-MW-C M1 with the condition-4 veto), the citation
builders, the hash-chained ledger-head recomputation, the r̂ estimators,
the value table, the crossover interpolation, and the gate analyses. The
check binary-head == recomputed-head is what carries the guarantee.

## R7. Headline questions and honest reporting

1. **Reliability × value table**: level | n_A/n_B | measured E_r |
   predicted 2r−1 | match. Any deviation is reported as a mechanism
   finding, not smoothed over.
2. **Crossover**: one number r* with the §R2 interpolation method stated,
   plus the analytic 0.50 and the sensitivity table r*(k).
3. **Self-estimation verdict**: does the win survive without independently
   established reliability — yes (mechanically) but unlicensed, or no.
   Stated plainly either way.
4. **S8**: wrong-guess rate, false-confidence rate, and the verdict on
   whether any reliability level makes fiat-breaking defensible.
5. **Licensing recommendation**: license / park / license-with-threshold-X,
   with the residual risk in one sentence. The decision rule is
   preregistered: license-with-threshold-X requires (a) crossover confirmed
   at 0.50, (b) the self-estimation stress confirming independence is
   load-bearing, (c) S8 fiat-breaking never licensed; X is set with margin
   above the crossover per the §R2 sensitivity table.
6. If any kill bar fails: report the failure plainly with the mechanism's
   name on it.

## R8. What this does not claim

Reliability here is STIPULATED per level, not measured from any real
source — the sweep maps the decision rule "if reliability r, then expected
value E_r", it does not establish any real source's r. Licensing a real
source requires actually establishing its reliability on held-out questions
first; this trial gives the threshold to check it against, not the
reliability itself. The ±1 value model is preregistered symmetric; the
§R2 sensitivity table carries the asymmetric-cost reading. Synthetic
dispute shapes use fictional entities — they map where the mechanism wins
and loses, they do not prove real-world efficacy.

**FROZEN 2026-09-22.**
