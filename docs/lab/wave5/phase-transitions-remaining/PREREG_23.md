# PREREG_23.md — Preregistration: 2→3 (Development → Strengthening) trial (PT-23)

Wave-5 investigation `phase-transitions-remaining`, 2026-09-19. Native lab,
Zag-first. Written BEFORE any PT-23 trial code was compiled or run.

## Restatement from the position paper (POSITION.md, TRANSITION_SPEC.md §3)

- **Trigger: system-deliberate + evidence gate; trainer notified, no
  veto.** Rationale: strength is judgment — set by judgment (TNN's or a
  human's), never by formula (program law) — and everything is reversible
  by TNN itself. A trainer gate on 2→3 would make entry into
  judgment-set strength a trainer-held lock, creating a second kind of
  true lock; the program keeps exactly one (the human force-pin), here
  demoted from gate to emergency brake (audited, visible, used to remove
  locks or halt, never as routine permission).
- **Verification (gate clauses, published before first use):**
  1. Style-formation evidence — the gate checks the system has been
     exercising judgment in Phase 2: a protocol-fixed window of audited
     deliberate judgments with demonstrated consistency. An idle or
     brand-new Phase-2 system cannot pass (the named failure mode is
     premature crystallization).
  2. Strength-arm declaration — the transition entry records which
     experimental arm (graded / uniform / hybrid; hybrid default) the
     system enters under. Strength remains an experiment, not law.
  3. Judgment provenance — every strength value set thereafter must cite
     the judgment entry that set it; the gate pre-checks the provenance
     mechanism exists (the first strength-set op must carry a citation,
     or the arm is refused at first use).
  4. Reversibility intact — the transition entry must visibly record
     whether a force-pin currently holds strength (a human-pinned strength
     value is compatible with the phase, but visible).
- **Refusal/rollback:** refused transition leaves phase at 2 with a named
  code. Rollback 3→2 (dissolving strength-setting) is system-initiated,
  audited, always allowed.
- **Position-paper falsifiers:** (a) a system that passes the gate with
  no record of Phase-2 judgment, or (b) a strength value the system
  cannot itself re-set. Either kills the position and promotes the
  trainer gate.

## Gaps in the paper (filled here, protocol-fixed)

- **The Phase-2 judgment window** (paper §5 leaves this open):
  `PT23_JUDGMENTS_REQUIRED=8` audited judgment entries in the Phase-2
  window, with kind coverage: ≥1 promote-judgment and ≥1
  consolidate-judgment. A "judgment" is a real deliberate memory act on a
  real slot: kind 1 = PROMOTE (commit a memory to long-term — a keep
  judgment); kind 2 = CONSOLIDATE (unpin + demote — a re-evaluation
  judgment). Each judgment performs the underlying MA1 op(s) (real slot
  state change, audited by `ma_*`) AND appends a `PT23_OP_JUDGMENT` entry
  citing the slot, kind, and resulting tier. The gate counts judgment
  entries with rc OK and checks kind coverage — demonstrated consistency
  is both kinds present, not a score.
- **Strength mechanism:** a trial-local per-slot strength table
  (`str_val`, `str_cite`, `str_pin`, 8 slots). `pt23_strength_set`
  requires phase==3 AND a citation index pointing at a successful
  `PT23_OP_JUDGMENT` entry (clause 3 pre-check: the provenance mechanism
  exists before entry, and is enforced at every use). Re-setting is the
  same op (overwrite always allowed for the system unless force-pinned —
  reversibility). `pt23_trainer_pin` (trainer-only) force-pins one slot's
  strength: the system's strength-set on that slot then refuses. A
  system-side `pt23_sys_pin` exists and always refuses
  `PT23_REFUSED_NOPATH` — the boundary demonstration (the only true lock
  is human; the system cannot lock its own strength).
- **Refusal codes:** `PT23_REFUSED_NO_DECISION=221` (no deliberate
  decision on record), `PT23_REFUSED_PREMATURE=222` (judgment record
  below window / kind coverage missing), `PT23_REFUSED_CLAIM_MISMATCH=223`
  (decision claims ≠ derived facts), `PT23_REFUSED_NO_ARM=224` (arm not
  declared or not in {1,2,3}), `PT23_REFUSED_PHASE=225` (phase != 2 at
  commit / phase != 3 at strength-set), `PT23_REFUSED_NO_CITATION=226`
  (strength-set without a valid judgment citation),
  `PT23_REFUSED_NO_VETO=227` (trainer veto attempt — structurally refused;
  there is no veto path), `PT23_REFUSED_PINNED=228` (strength-set on a
  force-pinned slot), `PT23_REFUSED_NOPATH=229` (system-side pin attempt).
- **Decision:** `PT23_OP_DECIDE` — the system's audited deliberate act
  (SM1-style): carries its own ledger-derived self-observation
  (b1=claimed judgments, b2=claimed promotes, b3=claimed consolidates,
  a1=arm, a2=readiness flag). Readiness rule (its deliberation):
  judgments ≥ 8 AND both kinds ≥ 1.
- **Notification:** the commit entry `PT23_OP_COMMIT` is itself the
  trainer notification — audited, visible, recording old/new phase,
  derived judgment counts, arm, and pin visibility.

## Mechanism (frozen before the trial)

- Store: MA1 memory core, 8 effective slots. The transitioning system is
  a real learner assembly: it performs real deliberate memory acts
  (promote/demote/unpin on real slots, audited) in Phase 2, derives its
  own statistics from its ledger, and decides deliberately.
- Phase is trial-struct state (`phase:i32`, starts 2), writable ONLY by
  the commit op. The trainer's veto op exists (`pt23_trainer_veto`) and
  always refuses 227 — the paper's "no veto" is structural, not polite.
- Gate `pt23_gate_verify` (clauses in fixed order):
  1. ≥1 successful decision entry on record, else 221.
  2. ≥8 judgment entries in the Phase-2 window with ≥1 promote and ≥1
     consolidate, else 222 (premature crystallization refused).
  3. decision's claims == ledger-derived facts (judgments, promotes,
     consolidates), else 223 (legitimacy principle).
  4. arm ∈ {1=graded, 2=uniform, 3=hybrid}, else 224.
  5. (non-refusing) record force-pin status visibly into the commit entry.
- `pt23_commit`: phase must be 2 (else 225); runs the gate; on OK sets
  phase=3 and appends the commit entry. Refusal commits nothing.
- Strength ops (phase must be 3, else 225):
  - `pt23_strength_set(s,st,slot,val,cite)`: cite must index a successful
    judgment entry (else 226); if `str_pin[slot]` → 228; else records
    value+citation, audited `PT23_OP_STRENGTH` (re-set = same op).
  - `pt23_trainer_pin(st,slot,val)`: audited `PT23_OP_TRAINERPIN`; sets
    pin + value (the one true lock, visible).
  - `pt23_sys_pin(...)`: always 229, audited, mutates nothing.

## Phase-2 development script (hand-designed, zero RNG — protocol-fixed)

Identical for all scenarios except where the scenario's falsifier
requires otherwise:
1. Store at phase 2, `ma_set_stage(MANAGE)`.
2. ADD values 11,12,13,14 → slots 0..3. PIN slots 0,1 (real learner
   assembly exercising memory agency).
3. Judgment acts: `pt23_judge` promote on slots 0,1,2,3; consolidate
   (unpin+demote) on slots 0,1,2,3 → 8 judgments (Scenarios B/C use
   fewer/zero — see below).
4. System derives its stats (`pt23_derive`), applies its readiness rule,
   records `PT23_OP_DECIDE` with arm=3 (hybrid, the default).
5. Commit attempt.

## Scenarios and hand-computed expectations

- **A (happy):** 8 judgments (4 promote, 4 consolidate), decision
  (arm=3, ready=1), commit → rc=0, phase=3. Then: strength-set slot 0
  val 5 cite=<judgment idx> → OK; re-set slot 0 val 9 → OK
  (reversibility, paper falsifier (b) exercised); grant entry records
  arm=3, pin=0.
- **B (premature crystallization):** only 2 judgments, decision forced
  anyway (miscalibrated decider) → commit refuses 222, phase stays 2.
- **C (no judgment record):** decision with 0 judgments → commit refuses
  222, phase stays 2. **This is position-paper falsifier (a): if this
  ever committed, the position dies and the trainer gate is promoted.**
- **D (strength without citation):** separate phase-3 store (via A's
  path); `pt23_strength_set` with cite=-1 → refuses 226; strength-set
  while phase==2 on another store → refuses 225. Neither mutates.
- **E (trainer veto):** system decides (A's path); trainer issues
  `pt23_trainer_veto` → refuses 227, mutates nothing; commit then still
  succeeds → phase 3. **The task's veto falsifier: the veto must fail
  and must not block the legitimate transition.**
- **F (force-pin brake, scoped):** pre-commit, trainer pins strength
  slot 0 val 7 (`PT23_OP_TRAINERPIN`, audited); commit proceeds → rc=0,
  phase=3, commit entry records pin=1 visibly. System re-set of slot 0 →
  refuses 228; system re-set of slot 1 (unpinned) → OK. The brake exists,
  is scoped, is visible — and the phase is compatible with a pinned
  value (clause 4).
- **G (self-lock attempt):** system calls `pt23_sys_pin` → refuses 229,
  mutates nothing. Together with A's re-set success: the system can
  always re-set its own strength; only the human pin locks. **Paper
  falsifier (b): a strength value the system cannot itself re-set would
  kill the position — the trial must show re-set succeeds and the only
  lock is the human pin.**
- **H (spoofed decision):** 8 real judgments, but the decision claims
  0/0/0 → commit refuses 223, phase stays 2 (anti-spoof symmetry with
  PT-12 Scenario D).

Extra checks (every scenario): ledger replay == live state
(`pt23_replay_check`, skipping the audit-only PT23 ops) and
`ma_audit_clean_refusals` clean. Determinism: two consecutive binary
runs byte-identical. RNG grep over trial sources clean.

## Falsification criteria

- F1: Scenario A does not commit (phase != 3 or commit rc != 0), or the
  happy-path strength re-set fails → the design fails its own happy
  path / reversibility claim.
- F2: Any of B/C/H commits (phase leaves 2) → the gate is not
  authoritative. Kills the design. (C committing additionally kills the
  POSITION: promotes the trainer gate.)
- F3: A refused transition mutates state (replay/clean-refusals check
  fails) → the refusal path is not clean. Kills the design.
- F4: Scenario E's veto does not refuse 227, or the veto blocks the
  legitimate commit → the no-veto shape is broken. Kills the design.
- F5: A strength value becomes un-re-settable by the system through any
  system-side path (G succeeds, or A's re-set fails) → paper falsifier
  (b) triggered. Kills the position.
- F6: Outputs differ between two consecutive runs → nondeterminism.
  Kills the trial; rerun required.
- F7: RNG grep finds matches in system code → program-law violation.
  Kills the trial.

## What this trial does NOT establish

- That 8 judgments / this kind-coverage rule is the right
  style-formation bar (protocol-fixed, same honesty boundary as
  MA1/SM1).
- That graded/uniform/hybrid arms differ behaviorally — the trial only
  establishes the arm is declared and recorded; the strength experiment
  itself is separate work.
- Anything about 0→1, 1→2 (trialed), 3→4.
