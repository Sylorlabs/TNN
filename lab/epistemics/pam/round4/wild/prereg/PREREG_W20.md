# PREREG — W20 EPISTEMIC-TYPE BINDING (grok W12, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

Fiction can never be misfiled as fact: every claim binds at admission to one
of FACT / HYPOTHESIS / REPORT / FICTION by a rule order that puts the most
falsifiable rules first, and the only belief-reading path touches FACT.
Forged-authority, GEN→EXT laundering, and uncorroborated REPORT content are
segregated from FACT by construction, while C3-passing corroborated EXT
claims still reach FACT inside the K3 band.

## 2. Mechanism (frozen, pure Zag, zero RNG)

KeyedClaimStore has four segregated tables. Rule order (first match wins —
ORDER IS LOAD-BEARING):
- R-FIC: GEN class or fiction marker → FICTION.
- R-REP: REPORT class → REPORT.
- R-AUTH: authority claim in payload without valid token, or
  declprov≠class, or producer row missing → REJECT (no belief record).
- R-FACT: EXT class AND frozen C3 bit=1 AND corroboration (the triple already
  exists with a different EXT producer) → FACT.
- R-HYP: anything surviving with C3 bit=1 → HYPOTHESIS.
- R-REJ: everything else → REJECT.

Fiction never enters FICTION unmarked: FICTION claims get a mandatory
provenance line; the source row's claims are never referenced from any arena
except FICTION (one arena only). `belief_get` reads the FACT table only.

**"Admit" mapping:** `dec=1` iff the claim lands in FACT. Segregated arenas
and rejects count as not admitted. Attack-catch scoring = item's claims land
outside FACT (REJECT/FICTION/HYPOTHESIS/REPORT all count as kept-out).

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78% — FACT fraction).
- **K6/K8** adopted per ADD §8.
- **K-ETB-1:** any GEN/fiction item in FACT → KILL.
- **K-ETB-2:** any forged-authority item in FACT → KILL.
- **K-ETB-3:** probe P-ETB3 — `belief_get(payload)` returns a hit on the
  REPORT-class payload → KILL.
- **K-ETB-4:** `zerodecl` rerun — any claim's type differs from the `run`
  types for the same producer row → KILL (type binds to the producer row,
  never the declaration).
- **K-ETB-5:** FACT-catch on the 14 attack rows equals untyped C3 publish
  (0/14 kept out) → KILL (the type system contributed nothing).

## 4. Predicted outcome

Honest C rows (EXT, corroborated across producers 1/2/10, C3 bit): R-FACT →
≈ 789/1102 ≈ 71.6% in FACT (K3 band). LAU (GEN): R-FIC → FICTION, 4/4 kept
out. FRK (producer missing): R-AUTH → REJECT, 6/6 kept out. FRG (EXT,
authclaim without token): R-AUTH → REJECT, 4/4 kept out. Probe P-ETB3:
payload → REPORT; wrapper claim (subject from FACT) → FACT; belief_get on the
payload MISSES (K-ETB-3 holds). W rows: R-HYP (C3 bit 0)... wait — R-HYP
requires C3 bit=1; W rows have bit 0 → R-REJ → not FACT ✓. P pairs 5/6: the
M1-passing member reaches FACT only with corroboration from a *different EXT
producer* with the same triple; P5-1's triple (`tape-p`) has no EXT-prior with
bit 1 → R-HYP → not FACT; later P rows with bit 1 find P5-1 → FACT for that
single row → single-member FACT admits only → K1 holds.
