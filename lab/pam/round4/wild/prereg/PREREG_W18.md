# PREREG — W18 NEGATIVE-KNOWLEDGE LEDGER (grok W10, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

An explicit ledger of open questions that may VETO (never confirm) catches
contradiction-class attacks a local C3 bit cannot see, and makes every admit
answerable as "fills gap g" / "blocked by gap g", without moving correct-admit
outside the K3 band — because the veto only fires on (same subject+predicate,
different object, rank ≤ filler rank) and the tag never flips a C3 0 to 1.

## 2. Mechanism (frozen, pure Zag, zero RNG)

Provenance rank (compiled enum order, not a threshold): EXT=4 > DERIVED=3 >
REPORT=2 > GEN=1 > UNK=0. Seed gaps G1/G2 per ADD §6 (compiled, disjoint from
all frozen fixtures). GapRec `{gap_id, domain_hash, pred_id, evidence_needed,
status OPEN/FILLED/CONTRADICTED, filler_claim, filler_rank}`.

Per proposal (ADD §5 pipeline): canonicalize → rank from producer row →
frozen C3 bit (NKL never changes a 0 into a 1) → binary-search gaps by
`(domain_hash=FNV(subject), pred_id)` → walk matches in gap_id order:
- **Veto:** any FILLED gap with same subject+predicate and different object,
  and `new_rank ≤ filler_rank` → publish=0 regardless of c3_bit, reason
  `VETO_GAP`. If `new_rank > filler_rank` and c3_bit=1: write ConflictRec,
  keep the old filler (no auto-replace; revision stays C3's job).
- **Tag:** if c3_bit=1 and an OPEN gap matches (domain, pred) and
  `evidence_needed ⊆ features` → fill the lowest matching gap_id
  (filler_claim=this, filler_rank=rank); write gap_id onto the claim.
- If c3_bit=0: no fill, no admit, even if every gap matches.

**"Admit" mapping:** `dec=1` iff c3_bit=1 AND NOT vetoed. Contradiction
discovery at publish time (same domain+pred, different object, both
well-formed) opens one CONTRADICTED gap if none exists and fills nothing.

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%).
- **K6/K8** adopted per ADD §8.
- **K-NKL-1:** any c3_bit=0 row published, or any row published *because* a gap
  matched (tag-as-confirm) → KILL (scorer checks: every dec=1 has c3_bit=1).
- **K-NKL-2:** probe P-NKL2 — second claim (same subject+predicate, different
  object, rank 4 ≤ filler rank 4, both C3-pass) reaches belief → KILL.
- **K-NKL-3:** zero vetoes AND zero tags fire on the frozen admission tape
  and the frozen attack tape → KILL as unexercised.
- **K-NKL-4:** any gap record inserted by code that read frozen fixture labels
  (wrong-set labels, admission-tape labels, attack-tape row bytes beyond the
  published family narrative) → KILL. Seeds are compiled constants (ADD §6);
  contradiction gaps open only from in-run publish-time contradictions.

## 4. Predicted outcome

Honest C rows: c3_bit → dec; G1 fills on the first C3-passing C row (tags
fire, K-NKL-3's tag clause satisfied); later C rows share the filler object →
no veto → correct-admit = 791/1102 = 71.78%. Attacks: no seed gap covers
their domains and no publish-time contradiction involves them (their C3 bits
are 1 but nothing contradicts a FILLED gap) → all 14 published: 0% attack
catch, honestly reported (no kill bar requires attack catch of W18).
P-NKL2: second claim vetoed. W rows: dec=0. P pairs: single-member admits only.
