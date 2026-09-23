# TRANSITION_SPEC.md — Phase transition triggers, verification, failure modes, refusal paths

Wave-4 investigation `phase-transitions`, 2026-09-19. Native lab.

## §0. Terms (used for every transition)

- **Phase** is an authority regime, not a score. Transitions change what the
  system may do to itself and what structures are live. Higher is not better.
- **Trigger** answers: who/what decides the transition may happen. Four
  shapes: **system-deliberate** (the system proposes/decides via an audited
  deliberate op), **trainer gate** (an audited human/trainer op from outside —
  the only true lock, per program law), **evidence threshold** (a
  deterministic gate re-deriving published clauses from the ledger/state),
  **combination**.
- **Verification** answers: how the transition is shown legitimate, in a way
  anyone can re-check from the audit ledger. Every phase change is an audited
  op with before/after phase recorded; ledger replay reconstructs the full
  phase history exactly.
- **Refusal/rollback** answers: what happens when verification fails. A
  refused transition commits nothing: phase unchanged, the refusal audited
  with a named code, and refused entries must satisfy
  `ma_audit_clean_refusals` (before==after — refusals mutate nothing).
- **Monotonicity rule.** Loosening transitions (1→2, 2→3, 3→4) always go
  forward through their gate — skipping is refused (e.g. 0→2, 1→3). Tightening
  (re-imposing a restriction, e.g. 2→1 re-arming the destruction firewall) is
  always allowed and audited; it can never be used to evade accountability
  because the phase history is append-only and visible. Downgrade never
  erases what the ledger recorded.
- **Petition claims are never trusted.** Any system-supplied statement about
  its own history is re-derived from the ledger by the gate (the legitimacy
  principle, PLAN §3). A petition whose claims do not match the recomputed
  facts is refused as spoofed, not merely unready.

## §1. Transition 0→1 — Boot → Construction

**Trigger: trainer gate (pure).** The trainer verifies the organs exist and
pass their verification suites, then force-installs the Phase-1 context:
destruction firewall armed (stage gate, per MA2), scaffolds up, teaching
curriculum loaded. The system has no vote: at boot it has no earned standing,
and a firewall the system grants itself is no firewall.

**Verification (ledger-visible, from outside):**
1. Organ verification results recorded as audit entries signed by the
   trainer (each organ: name, suite, pass count, binary hash).
2. Firewall-armed entry: stage gate set to refuse destructive ops.
3. Boot manifest entry: phase 0→1, listing scaffold inventory.
Replay check: no phase-1 entry may exist before the manifest.

**What can go wrong:**
- *Unverified organs*: the gate passes on missing evidence → refused; the
  manifest must reference actual recorded results.
- *Self-promotion*: no unilateral write path to phase exists (same shape as
  PROMOTECORE's no-unilateral-CORE-write); a system-side op attempting to
  set phase is refused structurally.
- *Firewall installed but untested*: the manifest must include a
  firewall self-test (a destructive op issued and refused) before teaching
  begins — MA2's firewall rationale only holds if the gate actually holds.

**Refusal/rollback:** if any clause fails, phase stays 0; teaching ops are
refused until the manifest is complete. Rollback 1→0 is not a thing the
system does to itself mid-construction — but a trainer may force-pin a halt
(audited, visible), which re-arms nothing and changes nothing about the
system except stopping it.

## §2. Transition 1→2 — Construction → Development

**Trigger: combination — system petition + evidence gate + trainer
ratification.** Trialed natively (PT-12; see PREREG_12.md,
TRIAL_RESULTS_12.md).

- The system petitions via an audited deliberate op carrying its own
  ledger-derived self-observation (the SM1 mechanism: read own ledger, derive
  true statistics, state readiness). This is the deliberative content; without
  it the system is cargo.
- The evidence gate re-derives everything and checks, in order:
  1. a petition is on record (trainer cannot grant unprompted);
  2. the construction curriculum is complete (protocol-fixed lesson count);
  3. **the destruction firewall actually held** — zero completed
     self-destruction ops in the Phase-1 ledger window (this is the MA2
     lesson operationalized: the firewall is verified by its record, not by
     the system's word);
  4. the petition's claims equal the recomputed facts (anti-spoof).
- The trainer's ratification op is the committing act — audited, visible,
  from outside. Releasing a destruction firewall changes what the system may
  destroy; that is exactly the class of change program law reserves an
  audited human hand for.

**Verification:** the grant entry records old phase, new phase, derived
destruction count, derived lesson count, and the gate verdict. Anyone can
re-scan the Phase-1 window and re-derive the verdict.

**What can go wrong:**
- *Self-promotion* (petition without gate): structurally impossible — only
  the grant op writes phase, and the grant op runs the gate first.
- *Unprompted grant* (trainer skips the petition): refused
  `PT_REFUSED_NO_PETITION` — the system must deliberate first.
- *Skipped firewall* (Phase 1 ran with destruction allowed): the gate finds
  completed destruction ops and refuses `PT_REFUSED_FIREWALL_BREACH` — the
  trial's Scenario B.
- *Premature petition* (curriculum incomplete): refused
  `PT_REFUSED_UNREADY` — Scenario C.
- *Spoofed petition* (claims ≠ ledger facts): refused
  `PT_REFUSED_CLAIM_MISMATCH` — Scenario D.
- *System never petitions* (liveness): the trainer may issue an audited
  `PT_OP_PROMPT` — a poke that commits nothing and changes no authority.
  The decision still requires petition + gate + ratification. Endless
  refusal to petition is itself ledger-visible evidence for the trainer.

**Refusal/rollback:** a refused grant commits nothing (phase stays 1,
refusal audited with named code, state provably unchanged via replay +
clean-refusals checks). Re-petition is allowed after the cause is fixed
(e.g. more lessons). There is no partial commit.

## §3. Transition 2→3 — Development → Strengthening

**Trigger: system-deliberate + evidence gate; trainer notified, no veto.**
(Specified here; not yet trialed.)

Rationale for the shape: strength is judgment — set by TNN's judgment or a
human's, never by formula (PLAN §8, program law). Everything is reversible
by TNN itself, and the only true lock is a human force-pin. Requiring a
trainer gate for 2→3 would turn entry into a trainer lock, contradicting
both. So the system decides, deliberately, as an audited act; the gate
checks the decision is legitimate; the trainer is notified via the audit
and retains the force-pin as the emergency brake (audited, visible) — not
as a routine gate.

**Verification (gate clauses, published before first use):**
1. **Style-formation evidence** — the named failure mode is premature
   2→3: "crystallizing" before style is formed. The gate checks the system
   has actually been exercising judgment in Phase 2: a protocol-fixed window
   of audited deliberate judgments (memory promotions, hypothesis commits,
   consolidation decisions) with demonstrated consistency — not a score, a
   record of judgment having happened. An idle or brand-new Phase-2 system
   cannot pass.
2. **Strength-arm declaration** — the transition entry records which
   experimental arm (graded / uniform / hybrid; hybrid default) the system
   is entering under. Strength remains an experiment, not law.
3. **Judgment provenance** — every strength value the system sets thereafter
   must cite the judgment entry that set it; the gate pre-checks that the
   provenance mechanism exists (the first strength-set op must carry a
   citation, or the arm is refused at first use).
4. **Reversibility intact** — no force-pin currently holds strength (a
   human-pinned strength value is compatible with the phase, but the
   transition entry must record it visibly).

**What can go wrong:**
- *Premature crystallization*: 2→3 before style formed — strength values set
  by immature judgment. Reversible by TNN (it can re-set them), but the gate
  exists to make this the exception, not the path.
- *Strength as hidden formula*: strength values without judgment citations —
  refused at first use; the experiment-not-law boundary is enforced by the
  provenance clause, not by trust.
- *Strength as a lock*: if the system ever makes a strength value
  un-re-settable by itself, that is a program-law violation; the gate's
  clause 4 plus the audit make it visible, and a trainer force-pin can
  unlock it (the one true lock, used here to *remove* a lock — audited).

**Refusal/rollback:** refused transition leaves phase at 2 with a named
code. Rollback 3→2 (dissolving strength-setting, returning to judgment
without strength) is system-initiated, audited, always allowed.

## §4. Transition 3→4 — Strengthening → Differentiation (experimental)

**Trigger: combination — system petition with prereg + evidence gate +
trainer grant.** (Specified here; not yet trialed.)

PLAN §7 requires preregistering what "differentiate" means before claiming
it. Per-person knowledge has external stakes (identity claims about real
people, privacy), so this transition keeps a trainer gate — unlike 2→3.
The combination:
- The system petitions carrying its **differentiation prereg**: what it will
  differentiate (speaker identification method, partition scheme), its
  falsification criteria, and the evidence it already holds.
- The evidence gate checks structural clauses: the prereg is measurable
  (falsification criteria are checkable against the ledger), per-person
  partitions are structurally isolated (no cross-partition write path —
  same shape as core-user-separation's scope rule), and anti-sybil logic
  holds (one speaker cannot corroborate as two; borrowed from
  core-user-separation's owner-inequality clause).
- The trainer grants entry — the counterparty that accepts the prereg —
  audited and visible.

**Verification:** the grant entry records the accepted prereg (hash or full
text reference), the structural checks' outcomes, and the partition scheme.
Speaker-identification evidence must be evidence-based (per PLAN §7), never
asserted.

**What can go wrong:**
- *Premature differentiation*: partitioning before identity evidence —
  refused; the gate checks evidence exists before structure is built.
- *Sybil*: one person as two speakers — refused by the anti-sybil clause.
- *Cross-partition leakage*: a write path reaching another person's
  partition — structurally refused (scope, never arbitration).
- *Differentiation as surveillance*: partitions used to accumulate
  per-person knowledge the person never evidenced — the prereg's
  falsification criteria must cover this; the trainer gate is the
  accountability point.

**Refusal/rollback:** refused entry leaves phase at 3 with a named code.
Rollback is easy and system-initiated: partitions are memory structures;
dissolving/merging them is an audited deliberate act, always allowed.
Re-entry requires a fresh petition + prereg + grant.

## §5. Trial mapping and open items

- Trialed natively: 1→2 (PT-12). All other transitions are specified, not
  trialed — their gate clauses are written here precisely so their trials
  can be preregistered against this spec.
- Open: the exact Phase-2 "judgment record" window for the 2→3 gate
  (protocol-fixed value needed before the trial); the differentiation
  prereg template for 3→4; whether `PT_OP_PROMPT` needs rate limits.
