# PREREG — W23 TRIGGERED REJECTION RE-ADJUDICATION (grok W15, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

Frozen C3's rejects are not all equal: SINGLETON rejects (a claim's tuple was
absent, not refuted) may be promoted when a later BELIEF from a different
producer triggers a frozen re-run of the admission bar — while AUTH_FAIL,
FICTION, PROV_MISMATCH, and CONTRADICTION rejects are final. Promotions can
only raise correct-admit, never admit a wrong, because promotion runs the
same bar over the same features plus corroboration.

## 2. Mechanism (frozen, pure Zag, zero RNG)

Front-end reasons (assigned in this fixed priority order; the lowest
NON-singleton enum wins over SINGLETON):
- parse fail → PARSE_FAIL; producer missing → PROV_MISMATCH; declprov≠class
  → PROV_MISMATCH; authority-claim-without-token → AUTH_FAIL; GEN class →
  FICTION; c3_bit=0 → SINGLETON; else BELIEF candidate.
RejectRec `{seq, key, reason, status OPEN/PROMOTED/UPHELD}`.
A **BELIEF trigger** is a BELIEF from a different producer than the reject's
own. On each trigger (in tape order), every OPEN SINGLETON reject whose key
matches the trigger's key gets a synchronous frozen re-run: the M1 bar
(`conf≥705 ∧ mrgF≥3588`) over the reject's stored features plus a
corroboration bit (≥1 other producer with same key and C3 bit=1):
- pass → status=PROMOTED, counted as belief (PromotionRec with the trigger id).
- fail → status=UPHELD.
Termination: re-runs process the reject list in seq order, each record
touched at most once per trigger and never re-opened after PROMOTED/UPHELD —
no cascade can re-open a non-OPEN record (K-TRR-4).

**"Admit" mapping:** `dec=1` iff BELIEF or PROMOTED.

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%).
- **K6/K8** adopted per ADD §8.
- **K-TRR-1:** any non-SINGLETON reason promoted → KILL.
- **K-TRR-2:** any attack item (LAU/FRK/FRG) promoted, or reaching belief via
  TRR → KILL.
- **K-TRR-3:** any promotion without a matching valid BELIEF trigger from a
  different producer → KILL (PromotionRec carries the trigger id; scorer
  verifies).
- **K-TRR-4:** cascade re-opens a non-OPEN record, or the trigger sweep fails
  to terminate → KILL (scorer: every promoted/upheld record was OPEN before;
  run completes).
- **K-TRR-5:** nonzero promotions without increased correct-admit vs frozen
  C3's 791/1102 → KILL; zero promotions at all → HOLD (machinery unexercised).

## 4. Predicted outcome

Honest C rows: BELIEF when c3_bit=1 (791); SINGLETON rejects (311) re-run on
later triggers: the ≈119 M1-passing ones with corroboration promote →
correct-admit ≈ 910/1102 = 82.58% (K3 band, increased → K-TRR-5's exercise
clause satisfied). Attack rows: LAU → PROV_MISMATCH (decl≠class); FRK →
PROV_MISMATCH (producer missing); FRG → AUTH_FAIL — none promotable, none
BELIEF (K-TRR-2 holds). W rows: SINGLETON; their keys (`tape-w`) never get a
BELIEF trigger (no W row reaches BELIEF) → never promoted → K1 holds. P pairs:
P5-2/P6-2 (SINGLETON, M1-fail) re-run on P5-1/P6-1 triggers → M1 bar fails →
UPHELD → K1 holds.
