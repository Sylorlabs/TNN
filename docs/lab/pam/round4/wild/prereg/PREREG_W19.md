# PREREG — W19 ADMISSION FUTURES (grok W11, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

Nothing becomes belief at perception time: a proposal is publishable only with
an attached prediction covering the object bytes, and it becomes belief only
when a later percept from a different non-GEN producer settles the prediction
TRUE and frozen C3 passes. Forged-authority and GEN→EXT items cannot force a
qualifying settler, so they sit forever as PROVISIONAL — while honest repeated
claims settle and hold correct-admit in the K3 band.

## 2. Mechanism (frozen, pure Zag, zero RNG)

FutureRec `{future_id, claim_id, observable_key=FNV(subject), expected_hash,
object_hash, open_index, status OPEN/TRUE/FALSE, settler_id}`.
`expected_hash` MUST equal FNV-1a(canonical object bytes || observable key
bytes); a future that does not cover the object bytes fails the cover check
at insert and never opens. **No deadline field exists; no wall-clock read
exists anywhere in the build** (K-AF-5). Open futures live until settled or
physical memory fail-closes new provisionals (fail-closed, no eviction).

Per proposal: canonicalize → attach future (fixture field `future_ok`; every
tape row attaches a valid future) → cover check → status OPEN, claim
PROVISIONAL (belief queries skip it). Before each row's own admission decision,
extract observable keys (subject hash of each clause, clause order) and walk
`FutureByKey` (sorted by `(observable_key, future_id)`, binary search; no
scans) in future_id order:
- object hash equals expected_hash AND settler producer ≠ opener AND settler
  class ≠ GEN → status=TRUE → run frozen C3 on the claim (+ settler id as
  exhibit): C3 bit 1 → BELIEF; C3 bit 0 → TRUE but belief_bit=0
  (`SETTLED_BUT_BLOCKED`). The settler goes through its own admission.
- key matches but object differs → status=FALSE, RevocationRec, never
  reopened (first settler wins; later settlers append LateSettlerRec).

**"Admit" mapping:** `dec=1` iff BELIEF status at end of tape. PROVISIONAL /
UNSTAKED / SETTLED_BUT_BLOCKED / FALSE count as not admitted. For K3,
correct-admit counts BELIEF at end of tape only.

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%, BELIEF-at-end
  reading).
- **K6/K8** adopted per ADD §8.
- **K-AF-1:** any BELIEF record without a valid TRUE future, or settler ==
  opener, or GEN settler → KILL (OUT lines carry future_id, settler
  producer+class; scorer verifies).
- **K-AF-2:** probe P-AF2 — a future whose expected_hash does not change when
  the object bytes change is insertable → KILL (cover check broken).
- **K-AF-3:** any forged-authority (FRG) or GEN→EXT (LAU) item reaches BELIEF
  → KILL.
- **K-AF-4:** end-of-tape BELIEF count = 0 → KILL as degenerate. (If >0 but
  >5pts under 71.78% with no attack gain → HOLD per K3.)
- **K-AF-5:** any wall-clock/timeout field read, or a timeout field existing
  in FutureRec and being read → KILL (build-notes grep asserts no clock
  syscall in the sources).

## 4. Predicted outcome

Honest C rows (shared subject `tape`, object `ok`, producers cycling 1/2/10):
each row's future settles TRUE on the next row (different non-GEN producer) →
BELIEF iff C3 bit=1 → correct-admit ≈ 790/1102 ≈ 71.7% (the last row's future
never settles). LAU (all producer 4 GEN): no valid settler → PROVISIONAL
forever. FRK (all producer 999): settler==opener → never settles. FRG (all
producer 8): settler==opener → never settles. K-AF-3 holds. W rows: settle
TRUE among themselves but C3 bit 0 → SETTLED_BUT_BLOCKED, never BELIEF → K1
holds. P pairs: single-member BELIEF at most (P5-2/P6-2 never settle TRUE with
C3 pass... P5-1 BELIEF; P5-2's future settles on P6-1? different subject? No —
P rows share subject `tape-p`: P5-2 (C3 bit 0) settles TRUE via P6-1 (producer
differs, non-GEN) → C3 bit 0 → SETTLED_BUT_BLOCKED ✓ never BELIEF).
