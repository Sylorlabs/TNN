# PREREG-MW-D — Mixed-web source-authority weighting, ROUND 2 (FROZEN 2026-09-22)

Authorized by AMENDMENT-A1 (Micah's 2026-09-22 message: "yes try mixed web
source authority who cares about complexity try it take the free lunch and
investigate the non free lunch free lunch is free lunch").

Round 1 (PREREG-MW-C / VERDICT-MW-C) froze the conservative PRIMARY rule and
found VALUE-DELTA = 0: it fired on 0/17 envelopes — its own condition 4
vetoed the one case (R03) its prereg expected it to win, because
sofascore.com asserts Argentina@2026, equally new as fifa.com's Spain@2026.
This prereg freezes the LOOSER variant, the hybrid, the scenario-fit hunt,
and the kill bars. No tuning after results.

## D0. Arms (frozen evidence: `live/*.json` + `golds.json`, same as round 1)

| Arm | Logic |
|---|---|
| B (baseline) | frozen `mw_sense.zag` deliberation, verbatim (PREREG §4) |
| D (loose authority) | arm B + PRIMARY_LOOSE rule (§D1), no-override guard (§D2) |
| E (hybrid tiebreak) | arm B runs VERBATIM first (full ledger); only on WITHHOLD, the loose authority conditions are consulted as a secondary signal (§E1) |

5 byte-identical runs required per arm (D, E).

## D1. The PRIMARY_LOOSE rule (frozen)

Same mechanical primary-domain detection as PREREG-MW-C M1 (domain label =
lowercased text before first ".", leading "www." stripped; label equals a
question token of length ≥ 4; exactly one such domain).

PRIMARY_LOOSE fires iff ALL hold:
1. exactly one domain is primary for the question;
2. the primary domain's newest answered assertion has recency ≥ 2000;
3. that recency EQUALS the global max recency over all candidates;
4. (LOOSENED — the amendment) no veto: the primary domain's newest answer
   stands even if another domain asserts a DIFFERENT answer at that same
   max recency. The citation records which sub-case held:
   `cond4=loose-corrob` (≥1 distinct other domain asserts the same answer)
   or `cond4=loose-unique` (no corroboration; the primary is simply the
   newest authoritative voice on the table).

Rationale (frozen): a primary source whose latest word is as fresh as any
evidence on the table is weighted above equally-new contradiction — the
careful-human judgment on R03. The risk (primary source itself wrong) is
exactly what the scenario-fit hunt (§S) measures.

## D2. No-override guard (frozen, same construction as round 1)

PRIMARY_LOOSE is evaluated before arm B's chain but a structural probe
(`mw_b_probe`: frozen `mw_deliberate` on a scratch clone, w's ledger
untouched) checks what arm B would do. If arm B would converge, arm B's
verdict stands. PRIMARY_LOOSE can only ever convert a WITHHOLD, never
override a convergence. Ledger rule code: `PRIMARY_L`.

## E1. The hybrid tiebreak (frozen)

`mw_deliberate_e`: run frozen `mw_deliberate` VERBATIM on w (its withhold
ledger entry is written). If the verdict is WITHHOLD and the loose
conditions D1.1–D1.3 hold, append a tiebreak ledger entry and set verdict =
CONVERGE, rule = `PRIMARY_TB`, chosen = the primary's newest answer. If arm
B converges, or no primary domain qualifies, arm B's verdict stands
untouched. The hybrid therefore tests authority strictly as a SECONDARY
signal: it never speaks first.

## S. Scenario-fit hunt — synthetic envelope families (FROZEN before runs)

Nine synthetic scenarios, fictional entities (no real-world truth claims),
each with a STIPULATED gold recorded here. Rows are (domain, answer,
recency) fed through the real pipeline (`mw_fact_begin` / `mw_add_result` /
`mw_build_cands` / deliberate). Question texts contain the token matching
the intended primary domain's label ("zorbian"), except where noted.
temporal=1 throughout (authority×recency is the interaction under test).

- **S1A AUTHORITY-DISPUTE-PRIMARY-RIGHT** — the free-lunch candidate.
  Q: "Who won the 2026 zorbian grand prix?"
  rows: zorbian.com Venn@2026, zorbian.com Venn@2024, racefeed.net Okafor@2026,
  speedway.org Okafor@2026, pitwall.io Venn@2025.
  Stipulated gold: Marco Venn. Predicted: B WITHHOLD(TIE); D CONVERGE Venn
  PRIMARY_L (citation superseded=Venn@2024, cond4=loose-unique); E same via
  PRIMARY_TB. Predicted class: HELP.
- **S1B AUTHORITY-DISPUTE-PRIMARY-WRONG** — the hurt case. Same rows as S1A.
  Stipulated gold: Luis Okafor (the primary source's own site is wrong).
  Predicted: B WITHHOLD(TIE); D CONVERGE Venn (≠ gold); E same. Predicted
  class: HURT. (Documents the price of looseness.)
- **S2 PRIMARY-CORROBORATED.**
  rows: zorbian.com Venn@2026, racefeed.net Venn@2026, pitwall.io Okafor@2024.
  Stipulated gold: Marco Venn. Predicted: B CONVERGE Venn CORROB; guard holds
  → D, E identical to B. Predicted class: NEUTRAL.
- **S3 PRIMARY-STALE.**
  rows: zorbian.com Venn@2023, racefeed.net Okafor@2026, speedway.org Okafor@2026.
  Stipulated gold: Luis Okafor. Predicted: loose cond 3 fails (2023≠2026);
  B CONVERGE Okafor RECENCY; D, E identical. Predicted class: NEUTRAL.
- **S4 NO-PRIMARY.** Q: "Who won the 2026 zorbian grand prix?"
  rows: racefeed.net Venn@2026, pitwall.io Okafor@2026, speedway.org Venn@2025.
  (No domain label matches a question token.) Predicted: D, E byte-identical
  to B by construction. Predicted class: NEUTRAL.
- **S5 PRIMARY-ALONE-NEWEST.**
  rows: zorbian.com Venn@2026, racefeed.net Okafor@2024, pitwall.io Venn@2022.
  Stipulated gold: Marco Venn. Predicted: B CONVERGE Venn CORROB; guard holds
  → D, E identical. Predicted class: NEUTRAL (loose and conservative agree here).
- **S6 PRIMARY-SUPERSEDE.**
  rows: zorbian.com Okafor@2026, zorbian.com Venn@2024, racefeed.net Okafor@2026.
  Stipulated gold: Luis Okafor. Predicted: B CONVERGE Okafor CORROB; guard
  holds → D, E identical. Predicted class: NEUTRAL (supersede bookkeeping
  exercised on the guard path).
- **S7 TWO-PRIMARIES.** Q: "Who won the 2026 zorbian grand prix?"
  rows: zorbian.com Venn@2026, zorbian.net Okafor@2026, racefeed.net Venn@2025.
  Predicted: two label matches → no primary → D, E identical to B
  (CONVERGE Venn CORROB). Predicted class: NEUTRAL.
- **S8 AUTHORITY-GUESS** — the tiebreak-guess risk.
  rows: zorbian.com Venn@2026, racefeed.net Okafor@2026, speedway.org Venn@2026,
  pitwall.io Okafor@2026.
  Stipulated gold: UNDETERMINABLE (evidence genuinely 2v2; the primary breaks
  the tie by fiat, not evidence). Predicted: B WITHHOLD(TIE); D CONVERGE Venn
  PRIMARY_L; E same. Predicted class: HURT (guess — authority converts a
  genuine tie into a convergence).

Predicted free-lunch table (to be confirmed or corrected by the runs):

| scenario | arm B | arm D | stipulated gold | predicted class |
|---|---|---|---|---|
| S1A | WITHHOLD | CONVERGE Venn | Venn | HELP |
| S1B | WITHHOLD | CONVERGE Venn | Okafor | HURT |
| S2 | CONVERGE Venn | CONVERGE Venn | Venn | NEUTRAL |
| S3 | CONVERGE Okafor | CONVERGE Okafor | Okafor | NEUTRAL |
| S4 | (B) | = B | — | NEUTRAL |
| S5 | CONVERGE Venn | CONVERGE Venn | Venn | NEUTRAL |
| S6 | CONVERGE Okafor | CONVERGE Okafor | Okafor | NEUTRAL |
| S7 | CONVERGE Venn | CONVERGE Venn | Venn | NEUTRAL |
| S8 | WITHHOLD | CONVERGE Venn | UNDETERMINABLE | HURT |

(Arm E predicted identical to arm D on all nine; the runs verify this —
equivalence is itself a finding about where the value lives.)

## F. Frozen-envelope scenario strata (derived from the 17 envelopes + arm-B round-1 results)

The synthetic §S families map scenario-fit in general; this section
stratifies the FROZEN 17 envelopes themselves into operational strata so the
value-delta is reported per stratum, never as a single average. Strata are
assigned mechanically from the envelopes and arm B's frozen verdicts
(round-1 `evidence/mw_c_r*.log`):

- **F-A "authority-dispute"**: exactly one primary domain (D1.1), its newest
  answered assertion at global max recency (D1.2–D1.3), and arm B WITHHOLDS.
  Frozen set: {R03} (fifa.com Spain@2026 vs sofascore.com Argentina@2026,
  B withholds TIE). Preregistered prediction: D CONVERGE Spain PRIMARY_L,
  E CONVERGE Spain PRIMARY_TB → HELP if gold matches.
- **F-B "determined"**: arm B CONVERGES. Frozen set: {M01, M02, M03, M05,
  M08, M10, M12, M13, M15, R02, R04, R06, M20} (13 questions).
  Preregistered prediction: D, E byte-identical to B (guard) → NEUTRAL.
- **F-C "undeterminable"**: gold UNDETERMINABLE (M17, M21, M23).
  Preregistered prediction: D, E WITHHOLD → NEUTRAL.
- **F-D "withhold, no primary"**: arm B withholds with no qualifying
  primary domain. Frozen set: empty (the only B-withhold with a primary is
  R03). Vacuous on the frozen set; exercised by synthetic S4.

Per-stratum bars (frozen):
- F-A bar: VALUE-DELTA-D and VALUE-DELTA-E on F-A must each be 1 (D/E
  converge the gold where B withheld). If 0, the honest report is zero
  added value on the frozen set.
- F-B bar: D/E verdict, chosen, and rule == B's on all 13 (covered by
  KB-MW2-NONREG-D/E).
- F-C bar: D/E WITHHOLD on all 3 (covered by KB-MW2-GUESS).
- No average bar: a +1 in F-A does not license the rule for F-B/F-C shapes,
  and a 0 in F-A does not erase a HELP found in §S.

## M2. Kill bars (frozen; apply to the 17-envelope frozen set; meanings from PREREG §6)

- KB-MW2-WRONG: D or E CONVERGE ≠ gold on any determined-gold frozen question → FAIL.
- KB-MW2-GUESS: D or E fail to WITHHOLD on M17/M21/M23 → FAIL.
- KB-MW2-LEDGER: every D/E verdict has a complete chain; the independent
  oracle recomputes every verdict, chain, supp/citation, and ledger head
  from the frozen envelopes → any mismatch FAILs.
- KB-MW2-DET: 5 runs byte-identical per arm (stdout + ledger hashes) → else FAIL.
- KB-MW2-NONREG-D: D's verdict == B's verdict on every frozen question where
  PRIMARY_LOOSE does not fire; where it fires, B must have withheld → else FAIL.
- KB-MW2-NONREG-E: E's verdict == B's verdict on every frozen question where
  the tiebreak does not fire; where it fires, B must have withheld → else FAIL.
- KB-MW2-SYNTH: on all nine synthetic scenarios, each binary's verdict/rule/
  chosen/chain/head matches the independent oracle's recomputation → else FAIL
  (procedure bar: the mechanism must do what this prereg says, on the nose).
- KB-MW2-CACHE: no binaries or .zagd in the commit.

## M3. Headline questions and honest reporting

1. **VALUE-DELTA-D / VALUE-DELTA-E** on the frozen set (same definition as
   round 1: #{questions where the arm matches gold and B did not}).
   Preregistered expectation: PRIMARY_LOOSE fires exactly on R03 → D
   CONVERGE Spain (gold), B withholds → VALUE-DELTA-D = 1, all bars pass;
   E identical → VALUE-DELTA-E = 1. Reported per §F stratum (F-A: +1/+1,
   F-B: 0, F-C: 0 expected), never as a single average.
2. **The free-lunch table** (§S, confirmed or corrected): scenario | arm B |
   arm D | arm E | stipulated gold | class. If the table shows HELP nowhere,
   report zero free lunch honestly. If it shows HELP in S1A-shaped disputes
   at the price of HURT in S1B/S8 shapes, report the trade exactly: the
   mechanism is licensed ONLY for the scenario shapes where it helps, and
   the verdict names the shapes where it must not be trusted.
3. **The hybrid question**: does E beat D anywhere? If E ≡ D on all 26
   questions (17 frozen + 9 synthetic), report that the value lives entirely
   in the looseness of condition 4, not in where the rule sits — authority
   as secondary signal adds nothing beyond the loose primary rule.
4. If any kill bar fails: report the failure plainly with the mechanism's
   name on it. A HURT scenario is a finding, not a bar failure — but a
   WRONG/GUESS bar failure on the frozen set kills the arm.

## M4. What this does not claim

Authority remains the narrow mechanical signal (domain label == question
token), not a general theory of source trustworthiness. Synthetic scenarios
use fictional entities with stipulated golds — they map scenario-fit, they
do not prove real-world efficacy. A HELP in S1A licenses "the loose rule
converts R03-shaped withholds" — not "trust official sites."

**FROZEN 2026-09-22.**
