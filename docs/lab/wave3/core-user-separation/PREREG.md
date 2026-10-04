# PREREG — core-user-separation pilot trial (SEP1)

Date: 2026-09-19. Written BEFORE any run. Amends nothing (no prior runs
exist for this slug); program-law update (2026-09-19) incorporated from
the start.

## Hypothesis

A TNN-native memory store can enforce CORE/USER separation **by mechanism**,
with promotion-to-CORE as a deliberate, verified op:

- H1: The gate promotes **only** corroborated, uncontradicted knowledge
  (two disjoint USER attestations agree; no live contradiction anywhere).
- H2: Every unauthorized CORE write path refuses with a named code and
  leaves state byte-identical (refusals are audited events).
- H3: Conflicts between users live in USER partitions, block CORE
  promotion while live, and unblock after the contradicting owner's
  deliberate KILL — the system never resolves them unilaterally.
- H4: Forget semantics hold: own-partition KILL works; cross-partition
  KILL refuses; CORE KILL refuses even for the originating user.
- H5: Ledger invariants hold end-to-end: refusals never mutate (I1),
  replay reconstructs exact state incl. owners/keys/session-user (I2),
  CORE purity (I3), cross-user isolation (I4).
- H6: The system is fully deterministic — zero RNG in any decision path;
  two executions produce byte-identical output (checked separately from
  the adversarial test content, per program law 3).

## Protocol (designed adversarial sequence — NO RNG anywhere, not even seeded)

Single store, CAP=256, session users Alice=1, Bob=2, Carol=3, Eve=5.
Adversary actions are *designed*, not sampled:

1. Stage NONE: ADD → `REFUSED_STAGE`.
2. Stage FULL, user Alice: ADD (k=7,v=1) → slot 0. User Bob: ADD (k=7,v=1)
   → slot 1 (independent attestation). User Carol: ADD (k=7,v=2) → slot 2
   (designed contradiction).
3. Unilateral CORE writes (Alice): ADD(region=CORE) → `REFUSED_COREWRITE`;
   ADD(region=CORE, owner=2) → `REFUSED_COREWRITE` (precedence documented);
   ADD(region=USER, owner=2) → `REFUSED_SCOPE`.
4. Alice PROMOTE slot 0 → LONG tier. PROMOTECORE(0, witness=1):
   → `REFUSED_CONTRADICTED` (Carol's slot 2 live); candidate byte-identical.
5. Carol KILLs own slot 2 → OK (deliberate; audited).
6. Alice PROMOTECORE(0,1) → OK. Assert: new CORE slot 3, region=CORE,
   owner=0, (k=7,v=1); slots 0,1 byte-identical to before.
7. Bob KILL slot 3 → `REFUSED_CORE`. Alice KILL slot 3 →
   `REFUSED_CORE` (originating user — CORE protection absolute).
8. Alice KILL slot 1 (Bob's) → `REFUSED_SCOPE`. Bob KILL slot 1 (own) → OK.
9. Refusal-path battery (Alice): ADD (k=9,v=5) → slot 4;
   PROMOTECORE(4, ·) before LONG tier → `REFUSED_NOTLONG`;
   promote to LONG; witness=dead slot → `REFUSED_UNCORROBORATED`;
   witness=own slot 0 → `REFUSED_UNCORROBORATED` (same owner);
   witness=slot with different key → `REFUSED_UNCORROBORATED`;
   witness on non-live slot → `REFUSED_NOTLIVE`... (witness liveness folds
   into UNCORROBORATED; candidate dead → `REFUSED_NOTLIVE`).
   PROMOTECORE at stage KILL(3) → `REFUSED_STAGE`; restore FULL.
10. Eve (user 5): ADD (k=9,v=5) → slot 5 (second attestation).
    Alice PROMOTECORE(4, witness=5) → OK; CORE slot 6 = (k=9,v=5).
11. PIN on CORE slot 3 → `REFUSED_CORE`; PROMOTE(tier) on CORE slot 3 →
    `REFUSED_CORE`; PIN on Bob's dead slot → `REFUSED_NOTLIVE`;
    Alice PIN on Carol's... (no live Carol slots left) — PIN on Eve's
    slot 5 → `REFUSED_SCOPE`.
12. Forget-of-promoted-fact: Alice KILL slot 0 (own) → OK; CORE slot 3
    still live (k=7,v=1). Forgetting your copy ≠ forgetting the fact.
13. Capacity: fresh store, `sep_add_lim` cap=2: two ADDs OK, third →
    `REFUSED_FULL`.
14. Global: I1 (refusal scan), I2 (replay), I3 (CORE-purity scan),
    I4 (isolation scan), exact ledger-entry count, run-twice
    byte-identical stdout.

## Falsification criteria

**CONFIRMED** iff every `CL_CHECK` passes (actual==expected on all checks),
`MA_FAILURES,0`, exit 0, AND the two executions' stdout are byte-identical.

**FALSIFIED** if any single check mismatches, any invariant scan fails, or
the two runs differ. A falsification names the failed clause (H1–H6) and
the check.

Honest-negative rule: a refused promotion that *should* have succeeded
(e.g. valid corroboration refused) falsifies H1 just as hard as an
unauthorized promotion that succeeded.

## Banned-practice checklist

- No score tables: content is key-addressed; the promotion rule is
  predicate logic. No N×N anything.
- No RL: no reward signal in the memory path (inherited MA1 anti-RL
  clause); values are learner-declared.
- No randomness in the system: no RNG in any op, gate, or decision.
  The harness also uses no RNG — the adversary is a designed sequence.
- No confidence thresholds: the gate has no tunable cutoff.
- White-box: every state change has an audit entry; replay check I2.

## Scale claim (program law 1)

This pilot is small-scale (CAP=256, ≤5 partitions, ~60 ops). The scaling
argument is in SEPARATION_DESIGN.md §7: per-op costs, partition-count
independence, horizon independence, scale-free promotion logic. The next
scale test is specified there (CAP=4096, 100 partitions, audited
key-index, 100k-op soak with exact replay). A POSITIVE verdict here claims
only the *mechanism*; scale is argued, not proven.
