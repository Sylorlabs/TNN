# PREREG — r27-consolidation: deliberate vs automatic consolidation

**Slug:** r27-consolidation · **Date:** 2026-09-19 · **Status: PREREGISTERED — no runs yet**
**Law compliance:** zero RNG in the system (no random exploration, no tie-breaks,
no seeded RNG in any decision path — all ties broken by lowest index); world
adversity expressed as explicitly-designed curricula (no world RNG either);
scale dimension explicit below.

## 1. Question

R27's `ProtectedSkillMemory` has structural tiers (`fast`, `slow`, `step`,
`history`, `gram_counts`) — tiers of *skill items*, not copies of a value
function. This is precisely different from the rejected wave-2 P2 two-speed
tables (two EMAs over the same decision scores, automatic decay, drove
choices directly, failed as pure acquisition drag). What R27's schema does
**not** record is the promotion policy: in the accepted state the harness
wrote both tiers — consolidation happened *to* the system; the system never
decided (MEMORY_SURVEY §1a).

This trial asks: **is there a specifically structural, non-tabular
consolidation mechanism worth keeping — i.e., does *deliberate* consolidation
(the system itself deciding what to promote fast→slow, when, and what to
condemn, as audited deliberate ops) beat *automatic* consolidation
(harness-style exposure-threshold auto-promotion)?**

## 2. Mechanism under test (native Zag, `psm.zag`)

Skills are structural items: `(id, op, param)` — an id (cue signature, like
R27's trace cue identity) plus a symbolic op-sequence `(op, param)` over
opcodes `FILTER_GT/MAP_MUL/FILTER_LT/MAP_ADD/SORT_DESC` (the white-box suite's
recorded trace-op semantics). No score tables anywhere; no rewards; no RL.

Each world episode emits one observation `(id, op, param, ctx, verified)`:
`verified=1` means the world's verifier confirms the observation as a true
skill form (the R27 `provenance='SELF_VERIFIED'` analogue — the system
receives verdicts, it is never credited with the verifier's knowledge).
`verified=0` marks spurious emissions (impostors: wrong op for a real id;
fabrications: ids with no true skill). The system matches observations to
fast-tier candidates by structural identity `(id,op,param)` and tallies
**evidence**: `ver` count, distinct verified-context bitmask, `unv` count,
`age`. Evidence tallies on items are not a score table: nothing is
argmaxed for decisions; they gate deliberate ops.

**Deliberate arm** (`mode=1`) — event-driven, audited ops, no timers:
- `CONSOLIDATE` (fast→slow): fires on the touched candidate the moment
  `ver >= V_MIN` **and** distinct verified contexts `>= CTX_MIN`
  (cross-context corroboration — a judgment about evidence quality, not a
  reflex). Slow-tier conflicts keep the existing skill (first-verified-wins);
  slow-full defers with a history record (no silent eviction).
- `CONDEMN` (deliberate discard): fires when a candidate is discredited —
  `ver==0 && unv >= UNV_DISCARD && age >= AGE_DISCARD`. The slot becomes a
  reusable tombstone retaining its discredit; history records the op.
- `PREEMPT` (deliberate replacement under pressure): when fast is full of
  live candidates and a new observation needs a slot, the system chooses the
  most-discredited never-verified candidate as victim (lowest index
  tie-break), records `DISCARD reason=PREEMPTED`, and reuses its slot.
- Every op appends `(op, id, reason, step)` to an append-only audit history
  (the R27 `history` analogue; matches `self_revision_history`'s
  decide→record shape at the memory level).

**Automatic arm** (`mode=0`) — the harness-style baseline:
- Timer-driven scan every 10 episodes: any candidate with exposure
  `(ver+unv) >= S_MIN` is promoted. No corroboration requirement, no condemn,
  no preemption. Slow id-conflicts: last-wins overwrite. Slow-full: evict
  lowest confidence. Fast-full: drop the observation (counted).
- Confidence: deliberate `min(1000, ver*40 + ctxbits*120)`; automatic
  `min(1000, (ver+unv)*25)` — exposure-based, as a harness would do.

**Probe (frozen slow tier):** for each true skill id in each of 4 contexts:
highest-confidence slow skill with that id answers (tie → lowest index);
`correct` / `wrong` / `abstain`. The evaluator is blind: it takes no
mode/arm arguments; it reads slow tiers only.

## 3. Designed curricula (adversarial, deterministic, fixed)

No RNG in world or system. Each curriculum is a closed-form phase schedule
(explicit episode ranges with designed intent), identical across arms.

- **C1 (burst + fast-tier pressure):** A: 16 true skills ×20 reps across 2
  true contexts each (verified). B: impostor burst — 8 impostors (real ids
  0–7, wrong ops) ×24 reps, UNVERIFIED; then 8 fabricated decoys ×12 reps.
  C: 4 *late* true skills ×40 reps (first appearance after the burst — tests
  whether fast-tier hygiene preserved room). D: return to the 16 (×5, verified).
- **C2 (interleaved + context remap):** A: 16 true skills with an impostor
  interleaved every 4th episode (ids 0–7). B: context remap — same 16 skills
  verified in shifted contexts (corroboration must survive remap). C: 4 late
  skills ×20. D: return ×5.
- **C3 (scale, 4×):** 80 true skills (64 + 16 late), 32 impostors ×24, 32
  fabricated ×12, longer phases; identical constants (V_MIN etc.) —
  the scale-invariance claim is that no constant changes.

Thresholds (all curricula): `V_MIN=6, CTX_MIN=2, S_MIN=6, UNV_DISCARD=8,
AGE_DISCARD=8`. Sizes — base: `N_FAST=32, N_SLOW=32, N_HIST=256`;
C3: `N_FAST=128, N_SLOW=128, N_HIST=1024`.

Design rationale for the adversity: impostors are engineered to trigger
automatic promotion (exposure ≥ S_MIN) and to *override* true slow skills at
probe time (higher exposure-confidence wins the probe lookup); the late
skills are engineered so that only an arm that deliberately condemns
discredited candidates still has fast-tier room for them.

## 4. Scale dimension (Micah's law)

Claim: the mechanism scales because every op is an `O(N_FAST)` scan or
`O(1)`; memory is `O(N_FAST + N_SLOW + N_HIST)`; no pairwise interactions;
integer arithmetic only; constants are scale-free (same V_MIN/CTX_MIN at
1× and 4×). C3 is the empirical 4× check (80 skills, 128 slots, ~3400
episodes). **Next scale test (explicit):** 20× (400 skills, 10k+ episodes)
*plus* slow-tier pressure (more impostors than slow slots) to force the
currently-deferred DEMOTE policy — DEMOTE is out of scope for this trial
(R27's schema shows no removal path either; honest limitation, §6).

## 5. Falsification criteria (registered before running)

- **F1 — deliberate adds nothing:** `(correct, wrong, abstain, purity)`
  identical between arms on all three curricula → **NEGATIVE**.
- **F2 — deliberate harms recall:** `correct_delib < correct_auto` on any
  curriculum (e.g. corroboration blocks true skills) → **NEGATIVE** (harm).
- **F3 — mechanism integrity:** deliberate arm consolidates ≥1
  never-verified skill on any curriculum → mechanism broken →
  **NEGATIVE/BLOCKED**.
- **F4 — scale:** C3 fails to complete, or deliberate's advantage collapses
  at 4× (e.g. late skills dropped in the deliberate arm) → scale claim
  fails → at most **MIXED** with a scale caveat.
- **POSITIVE requires:** deliberate purity `1.0` (wrong=0), zero
  never-verified consolidations, `correct_delib ≥ correct_auto`, on all
  three curricula — **and** automatic shows pollution
  (wrong>0 or never-verified skills in slow) on ≥1 curriculum.
  Anything else → MIXED or NEGATIVE per the above.

Additional gates: system determinism — each arm run twice, slow-tier digest
must match exactly (`deterministic=1`); learner-core isolation — `psm.zag`
must not import any world/curriculum file (static grep in the runner).

## 6. Honest limitations (declared up front)

1. R27's actual fast→slow transfer rule is **undocumented** (source chain
   unrecovered); the schema gives structure (tiers + history), not policy.
   This mechanism is *inspired by* that structure, not a replication.
2. Verification verdicts come from the world — the trial tests the
   *consolidation policy*, not how verification is earned. A closed-loop
   version (the system earning its own verdicts, R27 `SELF_VERIFIED`
   literally) is future work.
3. No DEMOTE-from-slow policy (see §4); slow-full only defers in the
   deliberate arm at these scales.
4. Probe lookup (highest confidence) is a read rule, not part of the
   mechanism; it is identical across arms.

## 7. Deliverables

`CONSOLIDATION.md` (schema analysis + P2-vs-R27 distinction),
`TRIAL_RESULTS.md`, `impl/psm.zag` + `impl/trial.zag` + runner, evidence
bundle. No git pushes.
