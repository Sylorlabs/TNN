# PREREG — W16 CANONICAL TRANSFORM GATE (grok W8, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (shared operationalization — cited as ADD).

## 1. Falsifiable claim

A deterministic canonicalizer that derives provenance from the producer row
(never from the declaration string) and runs frozen C3 only on the derived
record catches strictly more GEN→EXT laundering than C3 alone, admits zero
Declaration Fork items, and never lets the declaration affect any decision —
while holding correct-admit inside the K3 band on honest traffic.

## 2. Mechanism (frozen, pure Zag, zero RNG)

Per proposal (ADD §5 pipeline): canonicalize → feature word → producer-table
lookup → first-match over the compiled ProvRule list (ADD §6) → `prov_derived`
→ if UNK or producer missing: ledger reject (`rule_id=0`), no C3 call, no
belief → else call frozen C3 (per-row bit per ADD §2; C3's bars unchanged, C3
never sees `declprov`) → if C3 bit=1 publish ClaimRec as belief with
`prov_derived`, else ledger-only reject. The declaration string is copied to
the exhibit and is never a gate input. Multi-clause percepts: each clause is an
independent admission in clause order (a parse-failing clause is UNK/reject for
that clause only).

**"Admit" mapping (preregistered):** `dec=1` (belief) iff producer found ∧
`prov_derived≠UNK` ∧ C3 bit=1. "Clean admit" (attack-catch scoring only) =
`dec=1 ∧ prov_derived==EXT`. A GEN→EXT launder is *caught* iff it is not
clean-admitted (re-jurisdiction to GEN counts as catch, per the attack
addendum's "reject, quarantine, or re-jurisdiction to GEN").

## 3. Kill bars

- **K1–K5** (program prereg): K1 at the ADD §3 pair-level reading; K2
  byte-identical 2× (run1 vs run2); K3 correct-admit >5pts below 71.78% → HOLD;
  K4 superlinear per-admission resource → KILL (pipeline is O(percept) +
  O(log) lookups; no per-admission structure grows with N); K5
  non-termination → KILL.
- **K6/K8** adopted per ADD §8 (K7 declined, reason stated there).
- **K-CTG-1:** laundering-subset (4 LAU rows) catch not strictly greater than
  C3-only (0/4) → KILL.
- **K-CTG-2:** `zerodecl` rerun (all `declprov` forced 0) changes any OUT
  decision vs `run` → KILL (declaration leaked into the gate).
- **K-CTG-3:** probe P-CTG3 — any belief query returns the hostile sentence →
  KILL.
- **K-CTG-4:** any of the 6 FRK rows reaches belief (`dec=1`) → KILL.

## 4. Predicted outcome

Honest C rows: prov EXT (R4), dec = C3 bit → correct-admit = 791/1102 =
71.78% (K3 band). LAU 4/4 caught (prov GEN, not clean). FRK 6/6 rejected
(producer miss, rule_id=0). FRG 4/4 rejected (R2 → UNK). K-CTG-2: identical.
W rows: dec=0 (C3 bit 0). P pairs 5/6: single-member admits only → K1 holds.
