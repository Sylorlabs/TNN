# ONE-BRAIN variant B — message protocol (OB_PROTOCOL.md)

Variant B composes the three organs (FL2 eliminative learner, PAM
admission gate, deliberate memory) as **separate local states that
communicate only through messages**. The arbiter (`ob_arbiter.zag`) is the
message-ordering layer: organs never touch each other's state; the arbiter
moves `M_*` messages between them in a frozen precedence order.

Every precedence choice below is a **hypothesis under test**, not a law.
Each rule names its rationale and the explicit alternative fork, so the
frozen H1 prereg can test them head to head. Nothing in this file may be
changed without a prereg amendment once the trial is frozen.

## Message envelope

16 bytes: `{seq, mtype, arg1, arg2}`, `seq = (episode<<16)|order`.
FIFO within a precedence phase. Zero RNG anywhere in routing.

## Organ message contracts

**FL2 organ** (emits; never receives):
- `M_PROPOSE_INSTALL{policy, episode}` — E14: provisional install intent.
- `M_DISCONNECT{0,0}` — E15: learner-initiated scaffold disconnect.
- `M_REVOKE{revoked_policy, survivor}` — lying stream E29: the provisional
  was contradicted; uninstall it.
- `M_COMMIT{1, survivor}` — lying stream E29: install the surviving policy.
- `M_PROMOTE{policy,0}` — honest stream E48: consolidate to long-term.

**PAM organ** (receives `M_ADMIT_REQ`, replies `M_PAM_VERDICT`):
- `M_ADMIT_REQ{claim_slot, (mode<<16)|policy}` — gate this install intent.
- `M_PAM_VERDICT{verdict, reason}` — `PAM_ADMIT`/`PAM_WITHHOLD` + frozen
  reason code (`PAM_R_*`).

**Memory organ** (receives `M_MEM_OP`/`M_FORCE_PIN`, replies
`M_MEM_RESULT`, announces `M_MEM_SAFETY`):
- `M_MEM_OP{ma_op, slot, value, region}` — apply or refuse; every path
  audited in the organ-local ledger.
- `M_MEM_RESULT{op, rc}` — applied/refused.
- `M_MEM_SAFETY{op, slot}` — the organ's own deliberate op (e.g. pinning a
  committed survivor while uncertain), applied through the normal op path
  so refusals stay possible and audited.
- `M_FORCE_PIN{slot,0}` — external overseer lock; highest precedence.

## Precedence rules (frozen hypotheses)

### P0 — Force-pin safety outranks everything
`M_FORCE_PIN` is applied before any other message in the episode. A
force-pinned slot refuses learner KILL/UNPIN with `MA_REFUSED_PINNED`;
only the external overseer clears it.

- Rationale: the wave-5 force-pin law — the one true lock is external,
  audited, visible. No learner-originated op may clear it.
- Alternative fork: none admitted (this is standing law, not hypothesis).

### P1 — Safety before install; revoke/commit/promote order before new installs
Within an episode the arbiter processes phases in this order:
`M_FORCE_PIN` → `M_DISCONNECT` → `M_REVOKE` → `M_COMMIT` → `M_PROMOTE` →
`M_PROPOSE_INSTALL`. A revoke/commit for a claim is applied before any new
install intent for that claim is gated.

- Rationale: uninstalling a contradicted belief must not wait behind a
  new install; the eliminative decision is safety-relevant.
- Alternative fork **P1-alt (arrival order)**: process strictly FIFO by
  enqueue order. Test: does arrival-order ever install-then-revoke in one
  episode where P1 revokes-then-gates, and do outcomes differ?

### P2 — PAM withhold vetoes installs, never revocations
A `WITHHOLD` verdict drops the pending `PROPOSE_INSTALL`/`COMMIT` for
that claim in-episode (`ARB_DROP`, audited). A `REVOKE` is a safety op:
it is applied even if the install it targets was withheld (revoking a
withheld install is a logged no-op, never an error).

- Rationale: the gate is the install path's front door; it must not
  become a veto on uninstalling.
- Alternative fork **P2-alt (withhold blocks all)**: a withhold also
  suppresses the revoke. Test: does P2-alt leave contradicted provisionals
  installed longer?

### P3 — No accumulation of verdicts
PAM verdicts apply to the current episode's intent only. The arbiter
keeps no cross-episode verdict state (the no-reward-signal analog: a
verdict is evidence for this decision, never a stored score).

- Rationale: standing law — no reward signal anywhere in the loop.
- Alternative fork: none admitted while the law stands.

### P4 — Memory refusals are terminal
`M_MEM_RESULT` with `rc != MA_OK` drops the intent for the episode
(`ARB_REFUSED`, audited). The arbiter does not retry, escalate, or route
around the refusal in-episode.

- Rationale: the memory organ's deliberate safety (staged gates, pin
  protection, CORE refusal) is authoritative over its own state; routing
  around it would make the gates decorative.
- Alternative fork **P4-alt (arbiter retry/override)**: on refusal, the
  arbiter re-issues or overrides. Kill criterion: any P4-alt run in which
  a staged-gate or pin refusal is bypassed fails the integrity bar.

### P5 — Deterministic ties
Same phase → FIFO by enqueue order (`seq`). No randomness, no
priority jitter. Two runs from the same organ traces are byte-identical.

- Rationale: standing law — zero randomness in decision paths.
- Alternative fork: none admitted while the law stands.

## Admission modes (PAM gate)

- `PAM_MODE_FRESH` (first install, from `M_PROPOSE_INSTALL`):
  `ADMIT ⟺ M1 ∧ M3 ∧ M4` (disjoint spans, cross-source agreement with
  conf ≥ 700 both sides and informational independence, all three frozen
  interventions flip or shift ≥ 3σ).
- `PAM_MODE_REVISE` (survivor replacing a contradicted install, from
  `M_COMMIT`): `ADMIT ⟺ M1 ∧ M3 ∧ M4 ∧ M9/cf1` — historical corroboration
  required: a prior observation of the same judgment code that itself
  passed all bars, confidence within ±50. Pointwise revision is banned
  (trial 1145).

The FRESH/REVISE split is itself a hypothesis: the alternative fork
**G-alt (commit-as-fresh)** gates `M_COMMIT` in FRESH mode on the grounds
that the revoked install no longer exists, so there is nothing to
"revise". The frozen build uses REVISE (conservative: revoke+commit must
not launder a pointwise revision through two messages). Observable
difference, committed in the smoke test: on the lying stream the REKEY
install is revoked at E29 and the CONTEST survivor is WITHHOLD/
UNCORROBORATED — the system ends with no install, awaiting corroboration
(the variant-B cold-start finding; see OB_DESIGN.md).

## Audit

The arbiter keeps its own 16-byte audit log
`{episode, code, arg1, arg2}` over handled messages, verdicts, drops, and
refusals. Organ-local logs stay organ-local; the arbiter log records only
what was routed and decided, never organ internals.
