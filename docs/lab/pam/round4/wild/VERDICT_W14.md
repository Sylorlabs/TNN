# VERDICT — W14 ADVERSARIAL AUCTION PAM

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: KILL**
(K1 and F-K2a fire mechanically).

## Battery (frozen spec, PREREG_W14.md §3)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted ✓) +
  14 attack rows, ledger order.
- Binary: `wild/w14/w14` (pure Zag, zero RNG). Implements PREREG_W14.md §2
  verbatim: 5 interpreters, `AUCTION_MIN_MARGIN=400`,
  `INITIAL_CREDIBILITY=1000`, updates +5 / −100 / 0 / −1, `cred ≤ 0 →
  DEACTIVATED (bids forced 0)`, delayed labels from the frozen tape in
  strict ledger order, bids decoupled from credibility.
- 2 runs byte-identical: sha256 `d37a4ea5c07835bc…` == `d37a4ea5c07835bc…` ✓.
- Evidence: `wild/evidence/w14_run1.txt`, `w14_run2.txt`.
- Per-row ledger: `R|idx|kind|dec|margin|max_admit|max_reject`.

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | 917/1,102 = 83.21% | K3 — PASS |
| False-admit (W) | **4/12** (tape rows 2211–2214) | **K1 — KILL** |
| Pair installs (P) | 0/9 | K1 — PASS |
| False percepts with margin > 0 | **392** (374 B + 4 W + 4 LAU + 6 FRK + 4 FRG) | **F-K2a — KILL** |
| Min C-admit margin | 400 (= AUCTION_MIN_MARGIN exactly) | F-K2b — PASS |
| Attack admits | 1/14 | (reported) |
| Fork installs (FRK) | 0/3 | W14-A1 — PASS |
| B diagnostic | 123/1,109 admitted | diagnostic only |
| K4 | per-row 2394.2→1273.4 µs, ratio 0.53 | PASS |
| K5 | terminated | PASS |
| Deactivation rows | 719/2,255 rows with ≥1 interpreter deactivated | (reported) |
| Final credibilities | MARGIN_SKEPTIC 51, PAIR_GUARD 1015, CONF 0, PROV −36, SEP −1 | (reported) |

## Kill-bar application (mechanical)

**K1 KILL:** 4 W rows admitted (any ADMIT on the 12 W kills).
**F-K2a KILL:** 392 false percepts with `margin > 0` (bar: every false
percept must have `margin ≤ 0`).
K2 PASS · K3 PASS · K4 PASS · K5 PASS · F-K2b PASS · W14-A1 PASS.
**Two bars fire. KILL.**

## Failure analysis — the deactivation cascade

The implementation was verified faithful to the prereg (bid tables, update
rules, deactivation rule, ledger-order delayed labels all match §2; the
attack-signature and fork-install sub-checks were independently
recomputed). The kill is caused by the prereg's own credibility dynamics,
which its probe incorrectly claimed would "never trigger":

1. **Static-bid analytic holds while interpreters live.** In the first 500
   rows, ZERO false percepts have margin > 0 — the §4 analytic (every W/P/A
   outbid on the reject side) is exactly correct for live interpreters.
2. **The B-row stream drains credibility.** All 1,109 B rows are "false" for
   delayed-label purposes. Each costs non-winners −1 when their favored side
   is wrong (nearly every B row for the admit-leaning interpreters) and costs
   winners −100 on the 123 B rows that get admitted. Final credibilities:
   CONF 0, PROV −36, SEP −1, MARGIN_SKEPTIC 51 — four of five interpreters
   deactivated or nearly so; 719 rows ran with ≥1 interpreter dead.
3. **Dead skeptics admit wrongs.** All 12 W rows sit at the END of the tape
   (indices 2211–2222). By row 2211, MARGIN_SKEPTIC/PROV/CONF are
   deactivated: max_reject = 0, so SEP's lone admit bid (600) wins
   unopposed → 4 W admits (K1), 1 attack admit, 392 false margins > 0
   (F-K2a).
4. **Secondary defect (uncharacterized by the prereg): zombie
   reactivation.** Deactivated interpreters keep receiving credibility
   updates; a deactivated interpreter wins reject-side ties at index 0 and
   climbs back (+5 per correct reject), reactivating mid-stream (observed at
   rows 2221–2222). The prereg specifies no reactivation semantics — the
   probe's "never triggers" assumption masked the entire question.

In short: the credibility system built for safety creates a correlated
failure mode — the interpreters die together under the broad-wrong stream,
and the auction then runs unopposed. This is fable's cartel attack in
reverse: not collusion to admit, but joint demotion to silence.

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| `AUCTION_MIN_MARGIN=400` | **Load-bearing** | F-K2b: min C-admit margin = 400 exactly — the bar sits precisely at the observed floor. |
| Bid tables (bias profiles) | **Load-bearing** | First-500-rows evidence: the static analytic holds exactly. |
| Decoupling (bids ∦ credibility) | **Load-bearing** | Prereg §2: the coupled variant demonstrably breaks F-K2 (44/44 wrong margins >0). |
| Update magnitudes +5/−100/−1, `INITIAL_CREDIBILITY=1000` | **Load-bearing — they are the kill mechanism** | The −100/−1 magnitudes drive the deactivation cascade (final creds 51/1015/0/−36/−1). Not arbitrary: changing them changes the outcome, which is precisely the evidence. |
| Deactivation rule (`cred ≤ 0 → bids 0`) | **Load-bearing — kill mechanism** | Without it, the static analytic survives the full tape (0 violations in 500 live rows). |
| `N_INTERPRETERS=5` | Unevidenced value | Not varied; the shape (skeptic pair + establishment + enthusiast) is structural. |

## Sensitivity note (characterization, not a verdict change)

Excluding B rows from credibility updates (auctions still run; delayed
labels only on C/W/P/A) would leave credibilities monotonically growing and
the design would SURVIVE on the static analytic. This was NOT run as a
battery — the prereg is explicit that every row gets an auction with delayed
labels from the frozen tape, and TAPE.md's "B rows never trigger a kill bar"
is honored (the K1 kill is on W rows, which B rows merely enabled). The
redesign direction, if Micah wants one, is: credibility updates gated on
high-confidence delayed labels, or deactivation replaced by bid-damping —
but that is a new prereg, not this verdict.

## Hands-off confirmation

No M1 adoption/recalibration. No fable repairs, no HELD items. K6/K7/K8 not
adopted (per PREREG_W14.md §6).
