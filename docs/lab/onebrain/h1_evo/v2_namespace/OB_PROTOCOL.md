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

16 bytes: `{seq, mtype, arg1, arg2}`. `seq` is **arbiter-assigned at
receipt**: when the arbiter accepts an organ outbox, it re-stamps every
entry as `seq = (episode<<16)|arrival_index`. Organ-supplied order bits
are untrusted input and are ignored for dispatch (P5). Dispatch is FIFO
by arrival index. Zero RNG anywhere in routing.

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

### P1 — RETIRED 2026-09-24 (replaced by single FIFO dispatch)
The six-phase dispatch (`M_FORCE_PIN` → `M_DISCONNECT` → `M_REVOKE` →
`M_COMMIT` → `M_PROMOTE` → `M_PROPOSE_INSTALL`) is retired. The H1
P1/P1-alt fork test disqualified it: under reversed emission
(`M_PROMOTE` before `M_REVOKE` in one episode) the phase order applied
the promotion while P1-alt refused it — a precedence law hiding in the
clock (the C5 strongest objection, instantiated). The arbiter now makes
one FIFO pass in arrival order; P1-alt IS the dispatch.

- What P1 got right (preserved): revocation is a safety op and applies
  even if the install was withheld (P2); force-pin is external law (P0).
  What P1 got wrong (removed): deciding the A4 race by phase position
  instead of by the deliberation layer.
- The A4 race is now decided by the C3/C7 promotion-window predicate
  (below), a deliberation-layer window predicate per O-INV-2 — never by
  clock position.

### P1-alt — Arrival-order dispatch (canonical since 2026-09-24)
Within an episode the arbiter processes messages strictly FIFO by
arrival index. Fork-test evidence (`~/workspace/ob_p1fork/`): shipped
dispatch vs independent FIFO reimplementation are byte-identical under
natural AND reversed emission (task 1); the kill bar holds in every cell
(task 2); verdicts are emission-order independent (task 3).

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

### P5 — Deterministic ties (closed 2026-09-24)
Same episode → FIFO by arrival index. The arbiter assigns `seq` at
receipt (`(episode<<16)|arrival_index`); organ-supplied order bits are
ignored, closing the loud-organ back door (an organ can no longer win a
tie by choosing its own `order` bits). No randomness, no priority
jitter. Two runs from the same organ traces are byte-identical.

- O-4 content-hash fallback: genuine batch simultaneity (two messages
  with no arrival order between them) is unreachable in the
  single-threaded arbiter — there is one dispatch loop, arrival indices
  are dense and distinct, and no batch-enqueue API exists (O-INV-1 proof).
  O-4 (ascending SHA-256 over canonical entry bytes excluding `clock`
  and `prev_hash`) stands as the specified fallback for any future
  concurrent implementation; it is not implemented because it cannot
  trigger.
- Rationale: standing law — zero randomness in decision paths; the
  blindness axiom (O-AX) — the clock never sorts by meaning or by
  organ-assigned numbers.
- Alternative fork: none admitted while the law stands.

## C3/C7 — Deliberation-layer promotion-window predicate (2026-09-24)

Frozen C3 (revocation beats promotion) and C7 (corroborated
contradiction preempts promotion) are implemented as a **window
predicate in the deliberation layer** (`arb_revoke_blocks`, called from
the `M_PROMOTE` branch of `arb_handle_one`), per O-INV-2 — never as a
clock-order rule.

- When the arbiter handles `M_PROMOTE{policy}`, it applies the
  promotion-window predicate: a pending, unadjudicated `M_REVOKE` against
  the same claim in the episode window blocks `TN_OP_PROMOTE`.
  "Pending, unadjudicated" is decided by the dispatch cursor — a revoke
  queued at an index after the promote has not been processed yet, so it
  blocks; a revoke at an earlier index has been processed, and processing
  always adjudicates (the `M_REVOKE` branch logs a decision, applied or
  dropped, on every path), so it never blocks. This realizes the "queue
  plus arbiter log" check via the cursor: processed == adjudicated by
  construction. Per C3 ("contradiction evidence cleared / survivor
  re-selected"), a dropped revoke is adjudicated and does not block
  re-fire.
- On a block: the promotion is **refused**, ledgered as
  `ARB_REFUSED_CONTRADICTED` (code 204, MA1 refusal family, ≥ 101),
  **no state is mutated** (no memory op is issued), and the entry cites
  the blocking revoke's arbiter-assigned receipt seq
  (`(episode<<16)|arrival_index`).
- Re-fire: permitted only in a later episode, after the revocation has
  adjudicated; the adjudication is cited in the ledger trail
  ("deliberate audited repair", C7).
- Fork-test evidence: the reversed-emission twin (D1/E1) shows the
  ledgered 204 refusal with citation `(48<<16)|1`; the kill bar holds in
  every cell; a dropped revoke (policy mismatch) yields `ARB_DROP`, never
  204 (`test_dropped_revoke`).

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

### Cross-log total-order limitation (documented, not built)

Variant B does **not** build the unified §1.2 ledger. It retains two
separate trails: the arbiter audit log and the memory organ's audit log
(plus FL2/PAM local logs). These logs do **not** compose into one total
order:

- Each log has its own append clock (arbiter-log index vs MEM audit
  index); there is no cross-log clock and no hash chain linking them.
- A citation in one log (e.g. the C3/C7 refusal citing the revoke's
  receipt seq) cannot be mechanically ordered against an entry in the
  other log — the "which came first" question across logs has no
  ledger-defined answer.
- The O-INV-3 smuggle test and the O-4 tiebreak apply within each log's
  own append path (each path is single-threaded and proven so); they do
  not establish a cross-log order.

This is a known architecture gap (§8a of the ordering rule: "the
composition build must land the unified trail (or prove the arbiter log
+ organ logs compose into one total order, which reintroduces exactly
the clock problem this document solves)"). It is retained deliberately
per the repair scope: the unified ledger is future work, and the
limitation is recorded here so no consumer treats the two logs as one
ordered trail.
