# AMENDMENT-A3 — the conservative rule fires on corroborated disputes; add the uncorroborated block

Date: 2026-09-22. Status: FROZEN before Block-U/G2 generation and runs.
Parent: PREREG-MW-R3 (commit 1b762445637650a90e82dfc0b204029938480c4c).

## A3.1 What the sealed battery just proved (measured, oracle-confirmed)

On the 220 sealed envelopes (Blocks R/G/S), arm C (conservative PRIMARY,
frozen round-1 binary) CONVERGED on **all 220** — 200/200 disputes and 20/20
S8 ties — via the `cond4=corrob` disjunct. The independent oracle,
reimplemented faithfully from the frozen `mw_sense_c.zag`
(`mw_primary_cond4`: corroboration checked FIRST and takes precedence; the
equally-new-contradiction veto applies ONLY when no corroboration exists),
agrees with the binary on all 220 cells, citations and ledger heads
included. The mechanism is correct per its frozen spec.

The error was in PREREG-MW-R3 §R2/KB-R3-CONS, which predicted "arm C
withholds on all 220". That prediction generalized round 1's R03 veto
(no corroboration + equally-new contradiction → withhold) to ALL disputes.
The frozen M1 rule is the disjunction **corrob OR unique**, and the sealed
envelopes all carry corroboration (the `corr` corroborator on disputes,
`rival2` on S8 ties). **KB-R3-CONS as written is void and replaced below.**
No mechanism was changed; only the prereg's expectation is corrected.

## A3.2 Consequences (measured)

1. **On corroborated disputes (Blocks R/G) and corroborated ties (Block S),
   arm C and arm D are verdict-identical**: both CONVERGE on the primary's
   newest answer on all 220 envelopes. Measured D-minus-C value delta =
   **+0.00/case at every reliability level**. The loose rule adds nothing
   over the conservative rule on these shapes — the conservative rule
   already converges there.
2. **The fiat-tie risk is NOT unique to the loose rule.** On Block S, arm C
   also fiat-breaks every tie: 20/20 convergences, 10/20 wrong guesses vs
   latent truth (50%), 100% false-confidence — identical to arm D. Round 2's
   "the conservative rule never hurts" holds only for the frozen-17 shapes,
   not for corroborated ties.
3. **The loose rule's marginal value over the conservative rule lives ONLY
   on the UNCORROBORATED dispute shape** (the R03 shape): the primary's
   newest answer has no corroboration from any other domain but faces
   equally-new contradiction. There — and only there — C withholds (veto)
   while D converges. Round 2's license ("S1A/R03 shape") is refined: on the
   corroborated S1A shape the conservative rule suffices; the loose rule is
   needed only for the uncorroborated shape.

## A3.3 New frozen blocks: U (uncorroborated reliability sweep) and G2

**Block U** — 9 reliability levels × 20 envelopes = 180 envelopes.
Rows (U1 shape; A1 = primary's newest answer, A2/A3 = split equally-new
contradiction, no corroborator anywhere):

- (prim, A1, 2026), (prim, A1, 2024), (rival1, A2, 2026), (rival2, A3, 2026)

Levels, S1A counts, and Bresenham interleave are IDENTICAL to Block R
(§R1): levels 0.30…0.99, n_A = 6,8,10,12,14,16,18,19,20, twin S1A iff
(i·n_A) mod 20 < n_A. Stipulated gold: S1A → A1 (primary right),
S1B → A2 (primary wrong; rival1 right). Names rotate over the same six
fictional leagues; rival2's name pool supplies A3.

Oracle-confirmed expectations (independent reimplementation, 2026-09-22):
arm B WITHHOLD/TIE on all 180 (1v1v1 tie defeats RECENCY/MAJORITY/CORROB);
arm C WITHHOLD/TIE on all 180 (cond4: no corroboration → equally-new
contradiction vetoes); arm D CONVERGE on the primary's newest answer,
rule PRIMARY_L, basis `loose-unique`, on all 180 (D1 has no veto; the
no-override guard passes because B withholds).

**Block G2** — 20 uncorroborated-dispute (U1) envelopes, 50/50 S1A/S1B mix
(Bresenham with n_A=10), NO independent reliability. Same twin-identity
gate analysis as Block G (§R3), applied to the licensed shape.

Total trial: 220 + 180 + 20 = **420 envelopes** × 3 arms × 5 runs.

## A3.4 Frozen predictions for Block U

- Arm D value vs arm C (the true margin of loosening):
  E_r = (n_A − n_B)/20 = **2r−1** per case:
  −0.40, −0.20, 0.00, +0.20, +0.40, +0.60, +0.80, +0.90, +1.00.
- Symmetric crossover: **r* = 0.50** (linear interpolation).
- Asymmetric wrong-install cost k (relative to C's withhold baseline 0):
  r*(1)=0.50, r*(2)=0.667, r*(3)=0.75, r*(5)=0.833.
- Licensed-value curve (fire only if independently-established rel ≥ t):
  t=0.50:+0.557, 0.60:+0.650, 0.70:+0.740, 0.80:+0.825, 0.90:+0.900,
  0.95:+0.950 per case over levels ≥ t.
- Block G2: twin-identity holds (r̂ constant across identical-rows groups);
  no dispute-internal gate achieves positive EV (admits all-or-nothing).

## A3.5 Kill bars (revised)

- **KB-R3-CONS (replaces §R7.4):** arm C's measured verdicts on all 420
  envelopes are fully explained by the frozen-M1 oracle (KB-R3-ORACLE);
  the verifier REPORTS C's convergence count per block. No unexplained
  fire or withhold.
- **KB-R3-U-SHAPE:** arm B WITHHOLDs on all 200 Block-U/G2 envelopes
  (shape validity for the no-override guard).
- **KB-R3-U-ORACLE:** the independent oracle reproduces every arm's
  verdict/chosen/rule/citation/chain/ledger-head on all 420 × 3 cells.
- **KB-R3-U-VALUE:** measured Block-U E_r matches 2r−1 at all 9 levels;
  measured crossover r* = 0.50 ± 0.025.
- All other bars (DET, MIX, SHAPE, NONREG) extend to 420 envelopes unchanged.

## A3.6 What this amendment does NOT change

The mechanisms (frozen `mw_deliberate`, M1, D1+D2), the value accounting,
the 220 sealed envelopes, their evidence, or the Block-R/G/S verdicts are
untouched. This amendment corrects a prereg expectation, records two
measured mechanism findings, and adds the discriminating blocks the
licensing question requires. Nothing here is tuned to make a bar pass.
