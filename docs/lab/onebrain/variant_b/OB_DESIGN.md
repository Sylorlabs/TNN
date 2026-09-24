# ONE-BRAIN variant B — design (OB_DESIGN.md)

## What variant B is

Three organs, each with **local state**, composed by **messages** through
a small arbiter. The fork from variant A: no shared ledger. One part's
failure is known to the others only through what it emits; the arbiter's
precedence order (OB_PROTOCOL.md) is the entire integration contract.

```
            +-----------------+
            |   FL2 organ     |  local: main/quarantine/scratch/
            | (eliminative    |  counterfactual arenas, local TN log
            |  learner)       |  emits: PROPOSE/DISCONNECT/REVOKE/
            +--------+--------+         COMMIT/PROMOTE
                     | M_* messages
            +--------v--------+
            |    ARBITER      |  precedence P0..P5; routing table
            | (message order) |  claim -> mem slot; own audit log
            +---+---------+---+
                |         |
   M_ADMIT_REQ  |         |  M_MEM_OP / M_FORCE_PIN
   M_PAM_VERDICT|         |  M_MEM_RESULT / M_MEM_SAFETY
            +---v---+ +---v-------------+
            | PAM   | | deliberate      |
            | organ | | memory organ    |
            +-------+ +-----------------+
            local observation rows +    local slots, staged autonomy,
            local disposition ledger    signed trust, audit ledger
```

## Organ contracts

**ob_tn.zag** — byte-for-byte copy of the canonical `gl_substrate.zag`
(`cmp` verified). Not modified, not forked.

**ob_fl2.zag — the FL2 organ.** Ports `gl_learner.zag`'s arm_gl with its
state made local: main/quarantine/scratch/counterfactual arenas, a local
TN-style event log, and the exact `f3_survivor` selector from
`forks/g8_fl2_variants/nevercontradicted/f3_lawcheck.zag`
(the failed action is never its own survivor). Emits install/revoke/
promote/disconnect as `M_*` intents; applies its own decisions (provisional
flags, quarantine, disconnect, E29 correction) locally. Its local log is
its published trace — in a deployed variant B this would be a message
stream; the trial harness passes the buffer, and each organ's state is
touched only through that organ's own handler functions.

**ob_pam.zag — the PAM organ.** Local observation rows (12 words:
judgments, confidences, independence, spans, intervention outcomes,
episode) and a local disposition ledger (M8: audit property only, never
installation authority). Admission rule, frozen constants, two modes
(see OB_PROTOCOL.md): FRESH = M1∧M3∧M4; REVISE = FRESH ∧ M9/cf1
corroboration. Emits binary admit/withhold + frozen reason codes.

**ob_mem.zag — the deliberate-memory organ.** Local slot table (flat
arrays: live, signed value, pin, region, tier, step), staged autonomy
(NONE→PIN→FULL), per-feature signed trust accumulator (MA4: ±evidence,
clamped ±256, init +64; declared value = trust/64, may be negative),
force-pin as `MA_PIN_FORCE=2` (learner KILL/UNPIN refuse it; only the
external overseer clears it), CORE slot unkillable, checkpoint/rollback,
replay-to-exact-state across interleaved rollback, clean-refusal check.
Every path — success and refusal — is audited in the organ-local ledger.
Its own deliberate safety policy (`mm_safety_policy`) announces
`M_MEM_SAFETY` ops (e.g. pinning a committed survivor while uncertain,
subject to the frozen pin budget of 16); announcements are applied
through the normal op path so refusals stay possible and audited.

**ob_arbiter.zag — the arbiter.** Owns the message queue, the routing
table (claim episode → mem slot), the provisional-claim register, and its
own audit log. Processes each episode's queue in precedence phases
P0..P5, FIFO within a phase. Applies PAM verdicts, routes admitted
installs to the memory organ, applies revokes/promotes, enforces P4
(refusals terminal). Reads the FL2 organ's local log as its published
trace to derive the PAM claim observation (see below).

**ob_common.zag** — shared constants (message types, PAM reasons, memory
op codes live in ob_mem.zag), the 16-byte message envelope helpers, byte
arena helpers, and the `OB_CHECK` printer.

## Provisional mappings (hypotheses, not frozen)

These exist so the composition loop runs end to end. No trial verdicts
rest on them; the frozen H1 prereg replaces each with a specified rule.

1. **Claim-observation derivation** (`arb_pam_claim`): the PAM
   observation for an install intent is derived from the FL2 organ's
   trace: judgment = the proposed policy on both channels; confidence =
   250 × calibration score (4/4 → 1000 ≥ 700 bar); independent source;
   disjoint spans by construction; interventions = the organ's
   counterfactual sims (provisionally: all flip / shift 3.5σ). Quirk:
   derived confidence is ~always 1000, so REVISE corroboration needs
   priors with confidence ≥ 950 — an artifact of this mapping, flagged
   for the prereg.
2. **Fresh-vs-revise routing**: `M_PROPOSE_INSTALL` → FRESH;
   `M_COMMIT` → REVISE (conservative; the alternative fork gates commits
   as FRESH — see OB_PROTOCOL.md).
3. **FL2 provisional vs MEM installed**: the organ's provisional/
   committed flags track its own decisions (intent layer); the MEM organ
   tracks what the arbiter actually landed (application layer). No
   verdict feedback flows back to the FL2 organ — organs communicate
   forward only. A feedback variant is a named fork for the prereg.
4. **Brain staging**: the composition harness advances the memory
   organ's staged autonomy to FULL (trainer-gated in reality); the
   staging mechanism itself is unit-tested, not bypassed.

## The variant-B cold-start finding

Committed by the composition smoke (not a trial verdict): on the lying
stream, the REKEY install is admitted at E14 (FRESH bars pass — the
contradiction has not arrived yet, exactly the known FL2 E15–E29
"acts the lie" window), revoked at E29, and the CONTEST survivor is
WITHHELD/UNCORROBORATED in REVISE mode — the system ends with no
install, awaiting corroboration. A learner that has never installed
anything can install (FRESH), but a *replacement* must earn
corroboration. Whether this is the right conservatism, and whether
variant A behaves the same, is for the frozen trial.

## Determinism

Zero RNG in every decision path. All state transitions are pure
functions of prior state + the episode's messages. Two-run byte identity
is asserted by the runner for every unit test.

## What is NOT in this build (by the user's gate)

No integration trial / curriculum run. No verdicts about one-brain
composition. The frozen prereg is awaited; when it arrives, the trial
harness (not the organs) is what gets built next.
