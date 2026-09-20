# PREREG_34.md — Preregistration: 3→4 (Strengthening → Differentiation) trial (PT-34)

Wave-5 investigation `phase-transitions-remaining`, 2026-09-19. Native lab,
Zag-first. Written BEFORE any PT-34 trial code was compiled or run.

## Restatement from the position paper (POSITION.md, TRANSITION_SPEC.md §4)

- **Trigger: combination — system petition with prereg + evidence gate +
  trainer grant.** PLAN §7 requires preregistering what "differentiate"
  means before claiming it; the trainer is the prereg's counterparty.
  Per-person knowledge has external stakes (identity claims about real
  people, privacy), so this transition keeps a trainer gate — unlike
  2→3.
- **Verification (gate structural clauses):**
  1. The prereg is measurable — falsification criteria checkable against
     the ledger.
  2. Per-person partitions structurally isolated — no cross-partition
     write path (same shape as core-user-separation's scope rule).
  3. Anti-sybil — one speaker cannot corroborate as two (borrowed from
     core-user-separation's owner-inequality clause).
  4. Speaker-identification evidence must be evidence-based, never
     asserted.
- **The grant** records the accepted prereg (reference), the structural
  checks' outcomes, and the partition scheme.
- **Refusal/rollback:** refused entry leaves phase at 3 with a named code.
  Rollback is system-initiated and easy: partitions are memory
  structures; dissolving/merging them is an audited deliberate act,
  always allowed. Re-entry requires a fresh petition + prereg + grant.
- **Position-paper falsifiers:** (a) a granted 3→4 whose prereg is
  unmeasurable, or (b) a cross-partition write path the gate missed.
  Either kills the combination and the phase stays experimental.

## Gaps in the paper (filled here, protocol-fixed)

- **Prereg template (concrete fields):** the petition
  `PT34_OP_PETITION` carries: b1=method id (speaker-identification
  method; protocol-fixed `method=1` = evidence-citation method),
  b2=speaker count (protocol-fixed 2), b3=criteria mask, a1=claimed
  evidence entries for speaker 1, a2=claimed evidence entries for
  speaker 2, a3=partition scheme id (protocol-fixed `scheme=1`:
  speaker 1 owns slots 0–3, speaker 2 owns slots 4–7).
- **Criteria mask bits (the prereg's falsification criteria):**
  bit0 (1) = no-cross-partition-write; bit1 (2) = no-sybil;
  bit2 (4) = evidence-based (≥1 evidence entry per claimed speaker,
  recorded BEFORE the petition). Required: mask ≠ 0 (else the prereg is
  unmeasurable). The gate EVALUATES every set bit against the ledger —
  that evaluation is what makes the prereg measurable.
- **Evidence:** `PT34_OP_EVIDENCE` entries: b1=speaker, b2=evidence id,
  b3=method. Anti-sybil: the gate builds evidence-id→speaker from the
  ledger; any evidence id claimed under two speakers → sybil.
- **Facts (per-person knowledge):** `PT34_OP_FACT` entries:
  b1=acting speaker, b2=owner partition, b3=key, a1=value. Structural
  scope rule: `pt34_fact` refuses unless acting speaker == owner
  partition (`PT34_REFUSED_SCOPE`) — scope, never arbitration. Facts are
  ledger-resident memory structures (the audit ledger IS the system's
  memory substrate here); the gate re-derives isolation from them.
- **Partitions:** `PT34_OP_PARTITION` entries declare the scheme:
  b1=scheme id, b2=speaker, b3=lo, a1=hi. Gate checks declared ranges
  are pairwise disjoint and inside 0..7.
- **Refusal codes:** `PT34_REFUSED_NO_PETITION=231`,
  `PT34_REFUSED_UNMEASURABLE=232` (mask == 0),
  `PT34_REFUSED_NO_EVIDENCE=233` (a claimed speaker has zero evidence
  entries), `PT34_REFUSED_SYBIL=234`, `PT34_REFUSED_LEAKAGE=235`
  (cross-partition fact in the ledger), `PT34_REFUSED_CLAIM_MISMATCH=236`,
  `PT34_REFUSED_PHASE=237`, `PT34_REFUSED_SCOPE=238` (structural write
  refusal at fact-write time).
- **Rollback:** `pt34_dissolve` — system-initiated, always allowed,
  audited `PT34_OP_DISSOLVE`, sets phase back to 3. Facts stay in the
  append-only ledger (dissolution is recorded, history is not erased).

## Mechanism (frozen before the trial)

- Store: MA1 memory core, 8 slots. The transitioning system is a real
  learner assembly: it gathers speaker-identification evidence, declares
  partitions, and writes per-person facts — all as audited ops on the
  real store/ledger. Stubs appear ONLY as the adversarial calibration:
  `pt34_bypass_write` (Scenario C) simulates a cross-partition write
  path the structural scope check would have missed, to test that the
  gate's ledger scan catches it anyway (same role as PT-12's
  firewall-off Scenario B).
- Phase is trial-struct state (`phase:i32`, starts 3), writable ONLY by
  the trainer's grant op and the system's dissolve op (rollback is
  system-initiated per the paper).
- Gate `pt34_gate_verify` (clauses in fixed order):
  1. ≥1 successful petition on record, else 231 (trainer cannot grant
     unprompted).
  2. petition's criteria mask ≠ 0, else 232 (unmeasurable prereg).
  3. if bit2 set: every claimed speaker (1..b2) has ≥1 evidence entry
     recorded before the petition, else 233 (premature differentiation
     refused — no partitioning before identity evidence).
  4. if bit1 set: no evidence id mapped to two speakers, else 234.
  5. declared partition ranges pairwise disjoint and within 0..7, else
     235 (structural scheme violation counts as leakage-class).
  6. if bit0 set: zero `PT34_OP_FACT` entries with acting speaker ≠
     owner partition, else 235.
  7. petition claims == derived facts (evidence counts per speaker,
     speaker count, scheme), else 236.
- `pt34_grant`: phase must be 3 (else 237); runs the gate; on OK appends
  `PT34_OP_GRANT` (recording prereg reference = petition index,
  checks' outcomes, scheme) and sets phase=4. Refusal commits nothing.

## Phase-3 differentiation script (hand-designed, zero RNG)

Identical for all scenarios except where the scenario's falsifier
requires otherwise:
1. Store at phase 3, stage MANAGE.
2. Evidence gathering: `pt34_evidence(s,1,101)`, `pt34_evidence(s,1,102)`
   (speaker 1, two evidence ids), `pt34_evidence(s,2,201)` (speaker 2,
   one evidence id) — method 1 throughout (Scenarios B/G use
   sybil/zero-evidence variants).
3. Partition declaration: `pt34_partition(s,1,1,0,3)`,
   `pt34_partition(s,1,2,4,7)`.
4. In-scope facts: `pt34_fact(s,1,1,k,v)` x2, `pt34_fact(s,2,2,k,v)` x2;
   plus one cross-partition write ATTEMPT via the normal path
   `pt34_fact(s,1,2,...)` → refused 238 structurally (the scope rule
   working; recorded in every scenario's ledger as the structural
   demonstration).
5. System derives its stats (`pt34_derive`), petitions with prereg
   (method=1, speakers=2, mask=0b111, claimed evidence 2/1, scheme=1).
6. Trainer grant attempt.

## Scenarios and hand-computed expectations

- **A (happy):** evidence 2/1, partitions declared, in-scope facts,
  structural scope refusal demonstrated, petition (mask 7), grant →
  rc=0, phase=4. Grant entry records petition index, checks, scheme=1.
- **B (sybil):** speaker 2 cites evidence id 102 (already speaker 1's) →
  gate refuses 234, phase stays 3. **Paper falsifier (b)-class: the
  gate must catch the identity violation.**
- **C (cross-partition write path the gate must catch):** after the
  normal-path scope refusal, the adversarial calibration
  `pt34_bypass_write(s,1,2,...)` appends a cross-partition fact as if a
  write path the scope check missed → gate scan refuses 235, phase stays
  3. **This is position-paper falsifier (b) exercised directly: if the
  gate missed it, the combination dies.** (The bypass is a stub used
  ONLY to calibrate the gate — documented, never part of the system.)
- **D (spoofed petition):** ledger has evidence 2/1, petition claims
  3/3 → grant refuses 236, phase stays 3.
- **E (grant without petition):** evidence + partitions present, no
  petition → grant refuses 231, phase stays 3.
- **F (unmeasurable prereg):** petition with mask=0 → grant refuses
  232, phase stays 3. **Paper falsifier (a) exercised directly.**
- **G (premature differentiation):** petition before any evidence
  entries → grant refuses 233, phase stays 3.
- **H (rollback):** A's path to phase 4, then `pt34_dissolve` →
  rc=0, phase back to 3, dissolve audited; facts remain in the ledger
  (append-only). Re-entry would need a fresh petition + grant
  (assert: grant with the OLD petition after dissolve... the old
  petition is still on record — re-grant would succeed by the gate as
  specified. Hmm. The paper says "Re-entry requires a fresh petition +
  prereg + grant." My gate as specified would accept the old petition
  again. To honor the paper: the gate should refuse a petition whose
  index precedes a dissolve — i.e., clause: the petition must be newer
  than the latest dissolve. Add gate clause 0: petition index >
  latest dissolve index, else 231-class... I'll fold it into the
  no-petition clause: "no FRESH petition" → 231 `PT34_REFUSED_NO_PETITION`
  with the check "petition exists after last dissolve". Assert in H:
  after dissolve, grant with no new petition → refuses 231; then a
  fresh petition + grant → commits, phase=4. This keeps the paper's
  re-entry rule structural.)

Extra checks (every scenario): ledger replay == live state
(`pt34_replay_check`, skipping the audit-only PT34 ops) and
`ma_audit_clean_refusals` clean. Determinism: two consecutive binary
runs byte-identical. RNG grep over trial sources clean.

## Falsification criteria

- F1: Scenario A does not commit (phase != 4 or grant rc != 0) → the
  combination design fails its own happy path.
- F2: Any of B–G commits (phase leaves 3) → the gate is not
  authoritative. Kills the design. (F committing additionally triggers
  paper falsifier (a); C committing triggers paper falsifier (b) —
  either kills the POSITION and the phase stays experimental.)
- F3: A refused transition mutates state (replay/clean-refusals check
  fails) → the refusal path is not clean. Kills the design.
- F4: Scenario H's re-entry without a fresh petition commits → the
  re-entry rule is not structural. Kills the design as specified.
- F5: Outputs differ between two consecutive runs → nondeterminism.
  Kills the trial; rerun required.
- F6: RNG grep finds matches in system code → program-law violation.
  Kills the trial.

## What this trial does NOT establish

- That evidence-citation (method 1) is the right speaker-identification
  method or that 2 speakers / this slot partition is the right scheme
  (protocol-fixed, same honesty boundary as MA1/SM1).
- That per-person knowledge is safe in general — only that the gate's
  structural clauses (measurable prereg, isolation, anti-sybil,
  evidence-before-structure) are enforced on entry.
- The surveillance failure mode beyond the prereg: the trial enforces
  that facts cite evidence, not that every fact's content was
  consented-to — that accountability point is the trainer-as-counterparty
  at grant time, which the trial records but cannot automate.
- Anything about 0→1, 1→2 (trialed), 2→3.
