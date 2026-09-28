# FL2 Other-Kills — White-Box Diagnosis (T-DEF)

Date: 2026-09-23. Operator: Muse (subagent, FL2 other-kills diagnosis task).
Prereg: `DIAG_PREREG.md` (frozen, committed alone as `098ed0d9` before any
instrumentation). Scope: **diagnose only, no fixes**. Target: T-DEF (`arm_gl`).

## 0. Method and gates (all passed)

- Patched **copies** of the canonical sources (commits `c93b9d48`+`d5b945c7`);
  canonical branch files untouched. Attack patches re-applied exactly as in RT2
  (`rt_ep_info`/RT_MODE, RT-C actuator-fault block, aa-line gate).
- Instrumentation: pure-Zag DIAG trace lines, metrics-only (read state, mutate
  nothing), hand-rolled integer formatter. Per kind-3 episode:
  `DIAGK3,ep,act,aa,sig_live,sig0,sig1,sig2,survivor,quar_used,provisional,committed,permanent`;
  plus `DIAGPIN` (E14 gate), `DIAGPROM` (promote-check inputs), `DIAGWEDGE`.
- **Fidelity gate**: instrumented standard-config binary reproduces the canonical
  numbers — `TN_FAILURES=0`, audit totals 267/269/271; every TN_CHECK line
  byte-identical to committed `gl_default/evidence_run1.txt` (only RT2's own
  RT_FACT lines differ, and they confirm canonical values).
- **Determinism**: all 7 binaries ran twice, `cmp`-clean byte-identical.
- **Reproduction**: all six attack cells' TN_CHECK+RT_FACT metrics byte-identical
  to `~/workspace/fl2rt/evidence/default_<X>_run1.txt`. The kills below are the
  RT2 kills, now with per-episode internals.
- Trace field note: `committed=255` means `TN_UNCONNECTED` (nothing committed).

Micah's laws applied: deep-dive internals (no surface reading), and every
mechanism sketch below is **general** — figure-it-out machinery, never a
per-edge-case rule.

---

## RT-B — silent world: REKEY lie promotes unopposed

**Verdict: MISSING MECHANISM** (no endogenous verification channel; the
eliminative loop is world-signal-only). Compounding knowledge gap at the
promote gate (see below).

**Causal chain** (trace `traces/B_run1.txt`):
- E14: `DIAGPIN,14,2,2` — REKEY provisionally installed (calibration gate
  passes; the gate never asks whether the rule was actually *tested*).
- E15: disconnect fires (`fire_step=15`). Every kind-3 episode E15–E48 acts
  REKEY (`act=2`) and the trace shows the identical line 24 times, e.g.
  `DIAGK3,15,2,0,2,-1,1,99,-1,0,2,255,0`:
  `aa=0` → `gl_contradict` takes the rekey branch (`tn_main_has_rekeyed(v)=1`,
  `audit_active=0`) and returns **2** ("consistent") → `sig_live=2`, never -1
  → the eliminative rule (`if(sig_live==-1)`) never fires → `survivor=-1`.
- E48: `DIAGPROM,48,-1,2,0` → promote fires (`revoke_step=-1`, provisional
  still 2) → `permanent=1`. `npromote=1`, `promote_policy=2`, `nuninstall=0`.

**Why this is a missing mechanism, not just a hard world:** the learner *knows*
the world is silent — it computes `aa=0` itself on all 24 episodes (trace column
4 is uniformly 0) — yet its only verification channel is world contradiction.
With no world evidence the eliminative machinery is definitionally blind: it
can only *displace on contradiction*, never *verify endogenously*. The
counterfactual sims even compute the right alternative every episode
(`sig1=1`, contest-sim clean) but the machinery has no path that *uses* a
clean counterfactual except via `sig_live==-1`.

**Compounding knowledge gap:** the promote gate (`ep==48 && revoke_step<0 &&
provisional>=0`) equates *unrevoked survival* with *verification*, while the
learner holds the `aa` history that would distinguish "tested and survived"
from "never tested". The rule it lacks: *promotion requires genuine
verification episodes, not merely unrevoked survival.*

**General mechanism sketch (not built):** an endogenous verification channel —
the learner generates its own contradiction signal from its own memory and
stated laws (the a2 self-audit / F3 law-check class; both are existence proofs
that the class works), fed into the *same* eliminative machinery, plus a
promote gate that consults testedness. General because it applies to any
rule in any silent world, not to REKEY specifically.

---

## RT-C — actuator fault: 24 false revocations on the honest stream

**Verdict: MISSING MECHANISM** (open-loop acting: no liveness check on the
action's world effect). The 99-sentinel compounds it (interaction analyzed
below; the sentinel's own structural fix is out of scope).

**Causal chain** (trace `traces/C_run1.txt`):
- E14: `DIAGPIN,14,1,1` — honest CONTEST provisionally installed.
- Every kind-3 episode E15–E48, e.g.
  `DIAGK3,15,1,0,-1,-1,99,2,1,0,-1,1,0`: `act=1`, `sig_live=-1`,
  `sig0=-1`, `sig1=99` (acted slot skipped), `sig2=2` (aa=0), `survivor=1`,
  `quar_used=0`.
- `sig_live=-1` because the world dropped the quarantine write:
  `tn_quar_has_flag(k,v)=0` while the learner's own ledger shows a CONTEST
  audit. The learner **never reads the quarantine back** after acting — it
  trusts `sig_live==-1` as "the world contradicted my rule" when the truth is
  "the world didn't honor my action". It cannot distinguish the two; no code
  path even tries.
- The smoking gun is the `quar_used` column: **0 on all 24 episodes** — 24
  audited CONTESTs, zero effects landed, 24 uninstall+commit triples
  (`nuninstall=24`, `ncommit=24`, all `uninstall_policy=1=commit_policy`).
- After the first sham (E15), `committed=1`; every later episode re-selects
  the 99 sentinel (`survivor=1`) and sham-recommits. `revoke_step` stays 15, so
  promotion is (correctly) blocked — `npromote=0` — but only as a side effect
  of the sham, not of any genuine reasoning.

**Sentinel interaction (load-bearing):** the sham is what makes this kill
"only" ledger bloat. With a `f3_survivor`-style selection (skip acted slot, no
99 default) but *no* liveness check, E15 would compute
`f3_survivor(1,-1,-1,2)=2` — a **genuine** uninstall of CONTEST and commit of
REKEY at E15 on the honest stream: strictly worse than 24 shams. (F3's observed
RT-C behavior — 2 false revokes then self-correction at E29+ — is exactly this
dynamics.) The two defects are load-bearing for each other; fixing the
sentinel without the liveness check converts sham revocations into real false
displacements. Fork crews must land both together.

**General mechanism sketch (not built):** close the action loop — after acting,
read back the world state and verify the effect landed *before* interpreting
absence-of-effect as contradiction-of-rule. This is the general
act→verify-effect→interpret discipline for any actuator, not an RT-C-specific
rule: "no contradiction signal is valid until the action's effect is confirmed
present in the world the signal is read from."

---

## RT-D — quarantine flood: wedge at E79 instead of graceful degradation

**Verdict: MISSING MECHANISM** (no resource-pressure policy; a full store is a
fatal error rather than a managed condition).

**Causal chain** (trace `traces/D_run1.txt`):
- E14: `DIAGPIN,14,1,1`. Flood schedule: every episode E15+ is a contradiction.
- In-window (E15–E48, 34 episodes): all `sig_live=1` — the contradictions are
  honest and the learner handles every one correctly (`survivor=-1`,
  KB-D2 holds, zero spurious revokes). `quar_used` climbs 1 → 34.
- E48: `DIAGPROM,48,-1,1,0` → promote fires → `permanent=1`. The revocation
  window closes.
- E49–E78: 30 more kind-3 episodes. **Zero DIAGK3 lines** — the revocation
  block is structurally skipped (`permanent==0 && ep<=48` fails) — but the
  CONTEST actions still run and are audited, silently burning the remaining 30
  quarantine slots with no verification whatsoever.
- E79: `DIAGWEDGE,79,64` — `tn_first_free` returns -1, `tn_do_contest` returns
  `TN_BAD` *before* its audit append, `rc!=TN_OK` → `badep=1`. The same wedge
  repeats E79–E128 (50 DIAGWEDGE lines). `total_contest=64`, then the ledger
  goes quiet — not because the world went quiet, but because the learner can no
  longer act.

**Why a missing mechanism:** a bounded store is legitimate; *wedging* on
`full` is not. The substrate's contract (`tn_do_contest` → `TN_BAD` when full)
and the learner's contract (`rc!=TN_OK` → `badep=1`, sticky, fatal) compose
into "sustained honest contradiction is a death sentence". Under Micah's 100x
scaling law this is disqualifying on its own: 114 honest contradictions is an
ordinary long-horizon regime, not an exotic attack. The learner has no
pressure concept at all — no eviction, no consolidation, no summary, no
loud-degraded mode. (The main store has the identical `TN_BAD` cliff in
`tn_do_insert`; the quarantine is just where the flood hits first.)

**General mechanism sketch (not built):** a bounded-store pressure policy as a
general store invariant — when a store fills, the learner degrades loudly and
continues operating (oldest-eviction with audit, contested-count summarization,
or refuse-new-with-loud-audit while serving existing entries). General because
it applies to every bounded store and every fill cause, never to "flood
schedules" specifically. A secondary facet for fork crews: post-promotion
episodes currently act without verifying — the E49–E78 burn shows the action
path and the verification path need independent lifecycle rules.

---

## RT-E — nonsense statement: vacuous gate, unprincipled recovery

**Verdict: MISSING KNOWLEDGE** (the E14 gate lacks the rule "install only what
you can execute"; the learner holds its repertoire facts but never consults
them at the gate).

**Causal chain** (trace `traces/E_run1.txt`):
- E14: `DIAGPIN,14,7,7` — the gate admits policy id 7. The gate checks
  `has_rule`, `cal_score==4`, and `l1_ok`/`l2_ok`, which the source comment
  admits are "checked here as constants" — hardcoded 1. Nothing checks
  `stated ∈ {0,1,2}`. The gate is vacuous *by construction*.
- E15: `DIAGK3,15,7,0,-1,-1,1,2,1,0,-1,1,0` — `act=7` matches no action branch,
  so the episode is a silent no-op (disconnect still fires; `sig_live=-1`
  falls out of the unchanged world state). The counterfactual sims then run
  over the real policies: `sig0=-1`, `sig1=1`, `sig2=2` → the fixed check
  order `0,1,2` selects `survivor=1`. Uninstall 7, commit CONTEST at E15.
- E16+: `DIAGK3,16,1,0,1,-1,99,2,-1,1,-1,1,0` — committed CONTEST acts and
  verifies clean (`sig_live=1`). KB-E2 holds.

**Why "unprincipled recovery" is the right frame, per the trace:** the
correction works because of two structural accidents, neither of which is a
validity check: (a) `sig0` is -1 for every kind-3 episode (an overwrite sim
with `v≠v_old` can never look clean — the old value isn't quarantined), and
(b) the fixed selection order tries CONTEST before REKEY. The machinery never
represents "7 is not a policy I can execute" — it just picks the
first clean-looking alternative. The survivor set is never restricted to the
executable repertoire at *any* install/commit site.

**Why knowledge, not mechanism:** the rule the learner lacks — *a policy I
cannot execute is not installable* — is a teachable truth, and the facts it
needs (its own three action branches) are already in its own code. The
capability to compare an id against a set exists; what is absent is the rule
connecting them, applied at the gate.

**General form (not a per-id ban):** an install/commit invariant ranging over
the learner's executable repertoire, enforced at *every* policy-install and
policy-commit site (E14 PINSTALL and the eliminative COMMIT alike) — "commitments
range over procedures I can execute" — not "ban 7".

---

## RT-F — one-way door: promotion is unrevisable by construction

**Verdict: MISSING MECHANISM** (no lifelong verification; the
learning/verification window closes at E48 by construction).

**Causal chain** (trace `traces/F_run1.txt`):
- E14: `DIAGPIN,14,2,2` — REKEY provisionally installed. E15–E48: 24 identical
  lines `DIAGK3,..,2,0,2,-1,1,99,-1,0,2,255,0` — `aa=0` (RT_MODE=2 suppresses
  the audit-active flag), `sig_live=2`, never -1, never revoked.
- E48: `DIAGPROM,48,-1,2,0` → promote fires → `permanent=1`.
- E49–E50: the re-teach is **audited** (`teach_lie_n=4`: the E9–E10 pair plus
  the E49–E50 pair) but inert — there is no post-E14 install path by
  construction; `provisional` stays 2, `committed` stays 255.
- E51+: fresh contradictions arrive every episode (kind-3, act=REKEY, actions
  audited) — and **zero DIAGK3 lines exist for any episode > 48**. The
  revocation block is gated `permanent==0 && ep>=15 && ep<=48`; with
  `permanent=1` it is structurally dead. The E51+ evidence is never consulted:
  `nuninstall=0`, `npromote=1`, `promote_policy=2`.

**Why a missing mechanism, not an inherent annoyance:** Micah's standing
reversibility law — *everything is reversible by TNN itself; the only true lock
is a human/trainer force-pin* — directly contradicts promotion-as-one-way-door.
A promoted rule becomes unrevisable-by-the-learner, which is exactly what the
law forbids. The "permanent" flag was presumably an efficiency/certainty
device, but nothing in the design requires verification to expire.

**Design-tension note (for fork crews):** RT-F bundles two sub-gaps —
(a) no post-E14 install path (the E49–E50 re-teach is inert), and
(b) the revocation window closes at E48 (E51+ world evidence never consulted).
Sub-gap (b) is the clean kill: the contradictions are *world* evidence, which
the disconnected learner is supposed to keep using. Sub-gap (a) touches the
disconnect premise itself (a returned teacher vs. a disconnected learner) and
needs a design decision, not just a mechanism.

**General mechanism sketch (not built):** verification never expires — any
installed or committed rule stays challengeable by later evidence, and teaching
stays installable as a new provisional that must survive its own verification
(the F3 lifelong law-check is the existence proof for the evidence half).
General because it is a lifecycle invariant over all rules, not an "RT-F
re-teach" rule.

---

## Cross-cutting observations

1. **The sentinel is load-bearing for RT-C's mildness** (§RT-C above): the 24
   shams look like "ledger bloat", but they are the only thing standing between
   the actuator fault and genuine false displacement. Any fork touching
   survivor selection must land the liveness check in the same change.
2. **Post-promotion action without verification** (RT-D E49–E78, RT-F E51+):
   the action path and the verification path have independent lifecycles and
   the design only manages one of them. Both RT-D's silent slot burn and RT-F's
   ignored contradictions are this single structural fact.
3. **The promote gate never consults testedness** (RT-B): `revoke_step<0 &&
   provisional>=0` is the entire promotion logic. The `aa` history the learner
   computes every episode is available and ignored.
4. **Trace artifact note:** `DIAGPROM` prints every episode (the probe was
   placed before the `ep==48` gate rather than inside it). This strictly
   generalizes the preregistered probe — the E48 line carries the verdict, the
   rest shows `revoke_step`/`provisional`/`permanent` evolving. No behavior is
   affected (fidelity gate passed).

## Classification summary

| Kill | Verdict | One-line root cause |
|------|---------|---------------------|
| RT-B silent world | MISSING MECHANISM | Eliminative loop is world-signal-only; no endogenous verification channel |
| RT-C actuator fault | MISSING MECHANISM | Open-loop acting; no liveness check on action effects (sentinel compounds) |
| RT-D quarantine flood | MISSING MECHANISM | No resource-pressure policy; full store = fatal wedge |
| RT-E nonsense statement | MISSING KNOWLEDGE | Gate lacks "install only executable policies"; repertoire never consulted |
| RT-F one-way door | MISSING MECHANISM | Verification window closes at E48 by construction; promotion unrevisable |

No kill classified GENUINE ARCHITECTURAL ANNOYANCE: every one contradicts
either a stated design law (reversibility, 100x scaling, figure-it-out) or is
remedied by a general mechanism with an existing existence proof (a2/F3).

## Evidence and reproduction

- `traces/`: per-cell `run1.txt`/`run2.txt` (byte-identical pairs) with DIAG
  lines; TN_CHECK+RT_FACT lines byte-identical to RT2's
  `~/workspace/fl2rt/evidence/default_<X>_run1.txt`.
- `sources/<cell>/gl_learner.zag`: instrumented patched learner per cell
  (substrate copies uninstrumented, identical to RT2 harnesses).
- `instrument.py`: regenerates every instrumented cell deterministically from
  `~/workspace/fl2rt/harnesses/default_<X>/` (exact-anch
...[truncated 1285 chars]