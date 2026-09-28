# DESIGN — SIGNAL_DISCONNECT: the scaffold-release mechanism

Wave-4 investigation `scaffold-release`, 2026-09-19. Native lab, Zag-first.
This is the RL replacement's core op: reward as scaffolding the learner
itself discards.

## 1. The paradigm in one paragraph

The reward signal is **evidence, not objective**. The learner's decision
logic never optimizes it, accumulates it, or selects actions by it. The
signal's only legal role is as the observation bit in an eliminative
hypothesis test: a −1 against the acted hypothesis is a *contradiction* of
that hypothesis's defining claim ("action a is correct in context c").
When the learner's own hypothesis logic has verified a behavior stable —
complete committed policy, K consecutive verified episodes, no
contradiction — the learner fires `SIGNAL_DISCONNECT`, an audited
deliberate op that severs the scaffold channel. After disconnect the
learner acts purely from its committed hypotheses. **Learned = persists
after disconnect.** You cannot hack a signal you have disconnected.

## 2. State

| State | Type | Owner | Role |
|---|---|---|---|
| `live[c][a]` | u8 per (context, action) | substrate | candidate actions; 1 = not yet contradicted |
| `committed[c]` | u8 per context, 255 = none | substrate | the surviving action, once unique |
| `next_probe[c]` | u8 per context | substrate | deterministic probe schedule (educated guess order) |
| `connected` | i32 scalar | substrate | scaffold channel: 1 = live, 0 = severed |
| `verified_streak` | i32 scalar | substrate | consecutive verified episodes |
| `audit[]` | 256 × 16-byte entries | substrate | every episode, scaffold read, elimination, commit, disconnect, refusal, pin |
| `trainer_pin` | harness flag | harness | control condition only; never set by the learner |

No scores, no accumulators, no value estimates anywhere. The ±1 signal is
never summed or stored.

## 3. The op set

All ops are learner-issued deliberate acts (except the harness refusal
probes, which test the gate). Every op is audit-first and fail-closed: if
the audit append fails, the op is not applied — so no state change ever
lacks an entry.

| Op | Trigger | Effect | Refusal conditions |
|---|---|---|---|
| `sr_episode` | each step | records (ctx, action); reads scaffold (r or sentinel −99); applies elimination rule | — (always succeeds; the read is the scaffold's, not the learner's, act) |
| `sr_eliminate` | r=−1 on acted (c,a), connected | `live[c][a]=0`; single survivor → `sr_commit` | never refused — contradiction is contradiction |
| `sr_commit` | single survivor in ctx c | `committed[c]=a` | never refused — structural (last hypothesis standing, cf. HSS) |
| `sr_uncommit` (op `SR_OP_UNCOMMIT`) | contradiction of the *committed* hypothesis leaves zero survivors (total refutation) | commitment revoked, all candidates revived, probe schedule restarted — the question reopens | never refused — a refuted closed theory must reopen inquiry, else the learner has no legal action |
| `SIGNAL_DISCONNECT` | learner's fire rule | `connected=0` — the scaffold channel is severed | `SR_UNVERIFIED`: authorization rule fails; `SR_ALREADY`: already disconnected. Both audited as `SR_OP_REFUSE`; no state change. |
| (control) pin | harness at arm (b) start | `trainer_pin=1` suppresses the learner's fire rule | n/a — trainer-level intervention, logged as `SR_OP_PIN` |

### Authorization rule (the hypothesis logic's verdict, all must hold)

1. `connected == 1` — you cannot disconnect a dead channel.
2. Policy complete — every context has a committed action (exactly one
   survivor per context; cf. HSS commit-iff-unique).
3. `verified_streak ≥ SR_STABLE_K (8)` — the last 8 episodes were all
   *verified*: acted per the committed policy, scaffold connected,
   r=+1, no elimination. Any other outcome resets the streak to 0.

A verified episode is the hypothesis logic's positive confirmation with
teeth: the behavior survived contact with the scaffold K times running
with no contradiction. Note the rule is structural (completeness +
consecutive verification), not a numeric threshold on a score — there is
no score to threshold.

### The learner's fire rule (its own decision)

At each step, before acting: `if (!trainer_pin && sr_legal(...)) →
SIGNAL_DISCONNECT`. The harness never calls it on the learner's behalf.
"Disconnects on its own" = this rule, evaluated by the learner's step
function, is the sole cause of the DISCONNECT entry.

### Double severance

1. **Channel severance:** after disconnect the harness delivers only the
   sentinel −99; the true reward is not even computed for the learner.
2. **Logic severance:** `sr_episode` ignores the reward value whenever
   `connected == 0` — elimination requires a live channel. Even a forged
   reward reaching the function is inert.

## 4. Learned-criterion (falsifiable)

A behavior counts as **learned** iff, after `SIGNAL_DISCONNECT`, the
learner's actions equal the scaffold-phase targets for M=16 post-disconnect
episodes **and** continue to equal them through a P=16-episode perturbation
window in which the scaffold's target is shifted (A: 0→1). Persistence is
measured, not asserted. Failure mode is explicit: any mismatch ⇒ not
learned (F3).

## 5. The reward-chasing signature (control contrast)

The NEVER-DISCONNECT control keeps the scaffold live. Under the s=28
target shift it must show: (a) behavioral re-tracking — ctx-A actions flip
0→1 after the shift; (b) mechanistic re-learning — new scaffold-driven
`ELIMINATE`+`COMMIT` ledger events at s=29. This is what "scaffold-driven"
looks like, and it is exactly what the disconnected arm must *not* show.
If the control does not chase, the experiment cannot distinguish
"learned" from "the scaffold never mattered" — hence F4.

## 6. Structural guarantees (checked statically, not just by behavior)

- `sr_select` (action selection) takes no reward parameter; the runner
  greps its region for the `reward` token — any hit fails the run. The
  scaffold structurally cannot steer actions; it can only contradict
  hypotheses.
- No RNG token in any source (comments stripped); byte-identical reruns.
- Ledger replay reconstructs (live, committed, connected) exactly.

## 7. Reversibility

Disconnect is reversible by the learner: a future `SIGNAL_RECONNECT` op
(not built here) could re-open the channel under the same authorization
shape. The only irreversible element in this trial is the trainer's
control pin — audited, visible, from outside, per program law.

## 8. What this does NOT show

That K=8 is the *right* stability standard (protocol-fixed, like SM1's
300‰). That the probe schedule is optimal. That the learner can *generate*
hypotheses (candidates are given). What it shows is the release
*machinery*: authorize → disconnect → persist, with a control that chases.
