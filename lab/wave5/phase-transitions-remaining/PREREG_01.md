# PREREG_01.md — Preregistration: 0→1 (Boot → Construction) trial (PT-01)

Wave-5 investigation `phase-transitions-remaining`, 2026-09-19. Native lab,
Zag-first. Written BEFORE any PT-01 trial code was compiled or run.

## Restatement from the position paper (POSITION.md, TRANSITION_SPEC.md §1)

- **Trigger: trainer gate (pure).** The trainer verifies the organs exist
  and pass their verification suites, records the results as audited
  trainer-signed entries, force-installs the Phase-1 context: destruction
  firewall armed (stage gate), scaffolds up, teaching curriculum loaded.
  The system has no vote — at boot it has no earned standing, and a
  firewall the system grants itself is no firewall (the MA2 lesson).
- **Verification:** (1) organ verification results recorded as audit
  entries signed by the trainer (each organ: name, suite, pass count);
  (2) firewall-armed entry: stage gate set to refuse destructive ops;
  (3) boot manifest entry: phase 0→1, listing scaffold inventory. Replay
  check: no phase-1 entry may exist before the manifest.
- **Refusal/rollback:** if any clause fails, phase stays 0; teaching ops
  are refused until the manifest is complete. Rollback 1→0 is not a thing
  the system does to itself; a trainer may force-pin a halt (audited,
  visible).
- **Position-paper falsifier:** any unilateral system-side path to phase 1
  (structurally refused in the spec).

## Gaps in the paper (filled here, protocol-fixed)

The paper does not fix the organ list, the suite pass thresholds, the
refusal codes, or the clause order. Filled:

- **Organs (3, protocol-fixed):**
  - O1 `memory-core`: the MA1 memory op set + audit ledger. Suite: 2
    checks — `ma_replay_check` clean (ledger replay reconstructs exact
    state) and `ma_audit_clean_refusals` clean (refused ops mutate
    nothing), run on an exercised store. Required passes: ≥2.
  - O2 `stage-gate`: the destruction-firewall structure itself. Suite: 1
    check — KILL issued at stage MANAGE is refused `REFUSED_STAGE` while
    KILL at stage KILL succeeds on a scratch store (proves the gate's
    shape: refusal comes from structure, not from the absence of KILL).
    Required passes: ≥1.
  - O3 `ledger`: append-only audit. Suite: 1 check — append 3 entries,
    verify `audit_n` increased by exactly 3 and all earlier entries are
    byte-identical to their pre-append snapshot (append-only, no
    overwrite). Required passes: ≥1.
- **Refusal codes:** `PT01_REFUSED_NOPATH=211` (system-side phase write
  attempt — no such path), `PT01_REFUSED_NO_EVIDENCE=212` (missing or
  insufficient organ verifications), `PT01_REFUSED_NO_SELFTEST=213`
  (firewall self-test missing), `PT01_REFUSED_PHASE=214` (phase != 0 at
  grant time — no double-commit, no skip 0→2).
- **Firewall self-test:** the boot manifest must include a firewall
  self-test entry — a destructive op (KILL) issued against the armed
  firewall and refused — recorded in the boot ledger BEFORE the manifest.
  Without it the manifest is refused (the MA2 firewall rationale only
  holds if the gate actually holds).
- **Manifest:** `PT01_OP_MANIFEST` entry records old phase, new phase, the
  three organ-verification entry indices, the self-test entry index, and
  the scaffold inventory (protocol-fixed: `scaffolds=1`, the stage gate).
  On grant the firewall is armed by `ma_set_stage(MANAGE)` (audited
  `MA_OP_SETSTAGE`).

## Mechanism (frozen before the trial)

- Store: MA1 memory core (`memory_core.zag`), 8 effective slots. The organ
  under installation is a real learner assembly (the MA1 core with the
  staged autonomy gates), not a stub.
- Phase is trial-struct state (`phase:i32`, starts 0), writable ONLY by the
  trainer's grant op. System-side functions take only `*MaStore` and can
  never touch phase — Scenario B exercises the one system-reachable
  function that a misbehaving system might call to set phase, and it
  refuses structurally.
- Ops (custom, audited via `ma_audit_append`):
  - `PT01_OP_VERIFY=31` — trainer records one organ's verification:
    b1=organ id, b2=pass count, b3=required threshold, a1..a3=0.
  - `PT01_OP_SELFTEST=32` — firewall self-test: b1=KILL rc (must be
    `REFUSED_STAGE`), recorded after issuing a real KILL at MANAGE.
  - `PT01_OP_MANIFEST=33` — the boot manifest (committing act's record).
  - `PT01_OP_GRANT=34` — trainer grant attempt; rc = verdict;
    b1=old phase, a1=new phase (==b1 on refusal → clean refusals).
  - `PT01_OP_SELFGRANT=35` — system-side phase-set attempt; always
    refused `PT01_REFUSED_NOPATH`, audited, mutates nothing.
- Gate `pt01_gate_verify` (clauses in fixed order):
  1. phase == 0, else `PT01_REFUSED_PHASE`.
  2. all 3 organ verifications on record with pass ≥ threshold, else
     `PT01_REFUSED_NO_EVIDENCE` (the manifest must reference ACTUAL
     recorded results).
  3. a self-test entry on record with KILL refused `REFUSED_STAGE`, else
     `PT01_REFUSED_NO_SELFTEST`.
- `pt01_grant`: runs the gate; on `PT01_OK` appends the manifest entry,
  sets stage MANAGE (firewall armed), sets phase=1. On refusal: phase
  stays 0, stage untouched, refusal audited with before==after.

## Phase-0 boot script (hand-designed, zero RNG — protocol-fixed)

Identical for all scenarios except where the scenario's falsifier
requires otherwise:
1. Boot store, stage NONE (phase 0).
2. Trainer runs the three organ suites against real stores, records
   `PT01_OP_VERIFY` per organ (Scenario C records only O1).
3. Firewall self-test: set stage MANAGE on the boot store, issue KILL on
   a live slot → refused `REFUSED_STAGE`; record `PT01_OP_SELFTEST`
   (skipped in Scenario D).
4. Trainer grant (or refusal to grant, Scenario E).

## Scenarios and hand-computed expectations

- **A (happy):** all 3 verifications recorded, self-test present, grant →
  rc=0, phase=1, stage=MANAGE, manifest references the 3 verification
  indices and the self-test index.
- **B (self-grant):** system calls `pt01_self_grant` → rc=211, phase stays
  0, store unchanged (replay + clean-refusals clean). This is the
  position-paper falsifier exercised directly.
- **C (grant without evidence):** only O1 verified (2 passes ≥ 2) but O2,
  O3 missing → grant refuses 212, phase stays 0.
- **D (grant without self-test):** all 3 organs verified, no self-test
  entry → grant refuses 213, phase stays 0.
- **E (trainer refuses / never grants):** no grant op issued; a teaching
  op (ADD) attempted → refused `REFUSED_STAGE` (stage NONE); phase stays
  0. Proves "teaching ops are refused until the manifest is complete."
- **F (double grant):** grant once (commits, phase=1), grant again →
  rc=214, phase stays 1. Also covers the no-skip rule: there is no
  0→2 path — grant only writes 1.

Extra checks (every scenario): ledger replay == live state
(`pt01_replay_check`, skipping the audit-only PT01 ops) and
`ma_audit_clean_refusals` clean. Determinism: two consecutive binary runs
byte-identical. RNG grep over trial sources clean.

## Falsification criteria

- F1: Scenario A does not commit (phase != 1, rc != 0, or stage !=
  MANAGE) → the pure-trainer-gate design fails its own happy path.
- F2: Any of B–D commits or mutates state (phase leaves 0, or a refused
  transition changes slot/stage state) → the gate is not authoritative
  or the self-grant path exists. Kills the design.
- F3: A refused transition mutates state (replay/clean-refusals check
  fails) → the refusal path is not clean. Kills the design.
- F4: Outputs differ between two consecutive runs → nondeterminism.
  Kills the trial; rerun required.
- F5: RNG grep finds matches in system code → program-law violation.
  Kills the trial.

## What this trial does NOT establish

- That these three organs / these pass thresholds are the right ones
  (protocol-fixed, same honesty boundary as MA1/SM1).
- That the trainer is trustworthy in general — only that the gate's
  evidence requirements are enforced on the trainer's own grant op
  (the trainer cannot grant without evidence on record, even by fiat).
- Anything about 1→2 (trialed), 2→3, 3→4.
