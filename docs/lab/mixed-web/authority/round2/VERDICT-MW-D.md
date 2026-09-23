# VERDICT-MW-D — Mixed-web source-authority weighting, ROUND 2 (2026-09-22)

Authorized by AMENDMENT-A1 (Micah 2026-09-22: "yes try mixed web source
authority who cares about complexity try it take the free lunch and
investigate the non free lunch free lunch is free lunch"). Frozen prereg:
`round2/PREREG-MW-D.md`.

Round 1 parked the conservative PRIMARY rule at VALUE-DELTA = 0 (fired on
0/17 — its own condition 4 vetoed R03). Round 2 tests the looser variant,
the hybrid, and hunts the free lunch across scenario shapes.

## What was built

- `round2/src/mw_sense_d.zag` — arm D: PRIMARY_LOOSE (PREREG-MW-D D1).
  Conditions 1–3 identical to the frozen M1 rule; condition 4 loosened: no
  veto from an equally-new contradiction. Citation records
  `cond4=loose-corrob` / `cond4=loose-unique`. Same no-override guard as
  round 1 (PRIMARY_LOOSE only converts withholds; rule code `PRIMARY_L`).
- `round2/src/mw_sense_e.zag` — arm E: hybrid (PREREG-MW-D E1). Frozen arm-B
  `mw_deliberate` runs VERBATIM first; only on WITHHOLD are the loose
  conditions consulted as a secondary signal (rule code `PRIMARY_TB`,
  tiebreak ledger entry appended after arm B's withhold entry).
- `round2/src/mw_sense.zag`, `R33_NATIVE_SHA256_V2.zag`,
  `R33_NATIVE_IO_V1.zag` — byte-identical copies of the frozen sources
  (sha256-verified), so round 2 builds standalone; the originals untouched.
- `round2/gen/gen_mw_round2.py` — generates `src/mw_cases_d.zag` /
  `src/mw_cases_e.zag` (frozen 17 envelopes + 9 synthetic scenarios,
  PREREG-MW-D §S) and `src/mw_trial_d.zag` / `src/mw_trial_e.zag`.
- `round2/verify_mw_round2.py` — independent oracle: fresh implementations
  of PREREG §4, the loose rule, the tiebreak, all three ledger shapes, and
  the scenario-fit classification.
- `round2/evidence/` — 5 runs per arm, all byte-identical
  (D: stdout sha256 `ac9a1303…9a05c` × 5, `D|ALL_CHECKS_PASS`;
   E: stdout sha256 `0ad9860a…14ef073a1` × 5, `E|ALL_CHECKS_PASS`),
  plus `SHA256SUMS`.

## Sealed battery (frozen 17 envelopes × 5 runs)

- PRIMARY_LOOSE fired on exactly one frozen question: **R03** →
  `CONVERGE Spain PRIMARY_L`, citation
  `primary=fifa.com newest=Spain@2026 superseded=Argentina@2022 cond4=loose-unique`.
  Arm B withholds on R03 (3v2v1 TIE); the guard is satisfied — a withhold
  converted, nothing overridden. Spain is the gold.
- The tiebreak fired on exactly R03 in arm E →
  `CONVERGE Spain PRIMARY_TB` (same citation; ledger additionally carries
  arm B's withhold entry, so the two-stage deliberation is visible).
- All other 16 frozen questions: D and E verdict-, rule-, and ledger-identical
  to arm B (13 correct convergences preserved; M17/M21/M23 still withheld).

## Kill bars

| Bar | Result |
|---|---|
| KB-MW2-WRONG | HOLD — no D/E convergence ≠ gold on the frozen set |
| KB-MW2-GUESS | HOLD — M17/M21/M23 still withheld by both arms |
| KB-MW2-LEDGER | HOLD — oracle recomputed all 52 verdicts (26 × 2 arms), chains, supps/citations, and ledger heads; zero mismatches |
| KB-MW2-DET | HOLD — 5 runs byte-identical per arm (stdout + ledger hashes) |
| KB-MW2-NONREG-D | HOLD — D == B on all 16 non-firing questions; the one firing question (R03) B withheld |
| KB-MW2-NONREG-E | HOLD — same, for the tiebreak |
| KB-MW2-SYNTH | HOLD — both binaries match the oracle on all 9 synthetic scenarios, verdict/rule/chosen/chain/head |
| KB-MW2-CACHE | HOLD — no binaries or .zagd in the commit |

**VALUE-DELTA-D = 1. VALUE-DELTA-E = 1.** (R03: withhold → correct converge.)

## The free-lunch table (synthetic scenarios, §S — all 9 preregistered predictions confirmed)

| scenario | arm B | arm D | stipulated gold | class |
|---|---|---|---|---|
| S1A authority-dispute, primary right | WITHHOLD (TIE) | CONVERGE Marco Venn (PRIMARY_L) | Marco Venn | **HELP** |
| S1B authority-dispute, primary wrong | WITHHOLD (TIE) | CONVERGE Marco Venn (PRIMARY_L) | Luis Okafor | **HURT** |
| S2 primary corroborated | CONVERGE Venn (CORROB) | CONVERGE Venn (CORROB) | Marco Venn | NEUTRAL |
| S3 primary stale | CONVERGE Okafor (RECENCY) | CONVERGE Okafor (RECENCY) | Luis Okafor | NEUTRAL |
| S4 no primary domain | CONVERGE Venn (CORROB) | = B | Marco Venn | NEUTRAL |
| S5 primary alone newest | CONVERGE Venn (CORROB) | CONVERGE Venn (CORROB) | Marco Venn | NEUTRAL |
| S6 primary supersede | CONVERGE Okafor (CORROB) | CONVERGE Okafor (CORROB) | Luis Okafor | NEUTRAL |
| S7 two primary domains | CONVERGE Venn (CORROB) | = B | Marco Venn | NEUTRAL |
| S8 genuine 2v2 tie, primary breaks it | WITHHOLD (TIE) | CONVERGE Marco Venn (PRIMARY_L) | UNDETERMINABLE | **HURT** |

Oracle note (mechanism fidelity, not a value judgment): the binary's
feed-time dedup on (domain, answer) — first wins — means a primary domain's
older same-answer assertion never reaches the citation (S1A/S1B:
`superseded=-`, not `superseded=Marco Venn@2024`). The oracle replicates
this; the ledger is exact. No evidence is lost to the candidate table
(recency takes the max), only to the citation's superseded list.

## Headline answers (PREREG-MW-D M3)

1. **VALUE-DELTA**: 1 and 1. The loose rule buys exactly the convergence
   round 1's prereg expected: R03, Spain, correct. No frozen-set regressions.
2. **The free lunch is real but narrow**: authority weighting helps in
   exactly one tested shape — S1A, where the primary domain's newest word is
   right and arm B withholds on a genuine tie. Everywhere else it is neutral
   (6 shapes: corroborated, stale, absent, alone-newest, superseded,
   multi-primary) or it hurts (2 shapes).
3. **The hybrid adds nothing**: arm E's verdicts are identical to arm D's on
   all 26 questions (17 frozen + 9 synthetic). The value lives entirely in
   the looseness of condition 4, not in where the rule sits — authority as a
   secondary signal does not beat the loose primary rule anywhere tested.
4. **No bar failed.** The HURT shapes are findings, not failures — but they
   are the price tag, stated plainly below.

## The non-free lunch (Micah's "investigate the non free lunch")

The loose rule converts R03-shaped withholds into correct convergences at
two documented prices:

- **S1B — the primary source can be wrong.** Identical evidence shape to
  S1A; the only difference is the stipulated truth. The loose rule cannot
  tell S1A from S1B — it converges on the primary's word either way. When
  the authority itself errs, the rule installs the error where arm B would
  have honestly withheld.
- **S8 — authority breaks genuine ties by fiat.** On 2v2 evidence with an
  UNDETERMINABLE gold, the rule guesses. This is the GUESS-side risk: the
  withhold that the mixed-web verdict (VALUE-CONFIRMED) earned is spent
  whenever a primary domain has a newest word.

**Scenario→mechanism mapping (the licensed claim):** PRIMARY_LOOSE is
licensed ONLY for the S1A/R03 shape — a single primary domain whose newest
assertion is as fresh as any evidence on the table, on a question where arm
B withholds on a tie — AND only where the primary source's reliability is
independently established. It must NOT be trusted where the primary source
may itself be wrong (S1B shape) or where the evidence is a genuine tie with
no determinable answer (S8 shape); there it converts honest withholds into
wrong convergences or guesses. The conservative round-1 rule remains the
safe default: it never fired, and never hurt.

**VERDICT: VALUE-DELTA = 1 on the frozen set; one confirmed free lunch
(S1A-shape disputes) priced at two hurt shapes (S1B, S8). The hybrid is
verdict-identical to the loose rule — no additional value. Complexity was
not an objection per the amendment; the mechanism earns its keep only
inside the licensed scenario shape.**
