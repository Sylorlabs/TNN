# Slice 16: Curriculum interference and forgetting (Track 4)
## 1. Slice
Three curricula — CODE (crisp formal reasoning), ENGLISH (expression,
ambiguity, narrative), MESSY-REALITY (noisy, partial, adversarial
observation) — run interleaved in one learner: measure cross-curriculum
interference and define what "catastrophic forgetting" means in a
deliberate-memory system, where forgetting is a deliberate op with an audit
trail, not gradient overwrite.
## 2. Falsifiable claim
Under interleaved training, each curriculum's battery score degrades by <5
points relative to its isolated-training baseline at every checkpoint; any
larger degradation is always accompanied by ledger-visible deliberate-kill
signatures whose burst rate predicts the drop before it lands; and any check
dropping >10 points is restored to within 5 points of baseline by deliberate
rehearsal within 2 cycles, with no prereg changes. If interleaving causes a
>10-point cross-curriculum delta that rehearsal cannot restore within 2 cycles
— or degradation with no ledger signature at all — the interleaving design is killed.

## 3. Design

**Measurement protocol.** Each curriculum gets a 24-check battery, run at full
logged state every checkpoint (prereg: every 200 episodes). B_code: type
inference, invariant proof, injected spec-violation detection, loop-invariant
completion. B_eng: paraphrase preserving truth-conditions, garden-path
disambiguation, register choice, summary without invention. B_messy:
hidden-variable inference from partial observation, holding conclusions under
sustained noise, rejecting planted misleading data, and acting under
underspecification with an uncertainty flag. Baselines (each curriculum alone,
same episode count) give B_code_base(t), B_eng_base(t), B_messy_base(t); the
interleaved run gives S_code(t), S_eng(t), S_messy(t). Cross-curriculum
deltas: D_code(t) = B_code_base(t) − S_code(t), likewise D_eng, D_messy — these
answer "does learning English degrade code skill?" Asymmetric probes measure
directionality: English-then-code quiz (did narrative training erode formal
invariant discipline?), code-then-messy quiz (did crisp reasoning breed
overconfidence under noise?). Plot D_X(t) against each curriculum's active
training windows; a D_code spike during English-heavy windows is directional
evidence of interference.

**What catastrophic forgetting looks like here.** Memories are never
gradient-overwritten; every removal is a deliberate kill op on the append-only
audit ledger (MA1: 58/58, replay to exact state). Forgetting is always
attributable to an actor, a reason, and an episode. *Bad* forgetting — the
deliberate-memory analogue of catastrophic forgetting — has this ledger
signature, computed per partition: (a) cross-curriculum kills: a kill on a
memory whose judgment-strength was set by curriculum A, issued during
curriculum B/C training — K_rate(B→A) — vs self-maintenance K_rate(A→A);
(b) silent kills: kills lacking a deliberative-standard citation (RC gates
require recorded reasons; a kill with no evidence-refutation entry is the
exact signature of unmanaged erosion); (c) burst pattern: >8 kills per 200
episodes with no compensating adds — net shrinkage of a core partition;
(d) law violations: any kill of a CORE-adjacent or force-pinned memory without
a force-pin audit entry — a law breach, not a metric breach; halts the trial.
Monitor pseudocode (Zag-flavored):
```
# for each kill entry e in the ledger
if e.target == SHARED: flag LAW_CHECK(e)
if e.target != e.curriculum and reason(e) == NONE: bad_sig += 1
if kill_rate(e.target, win) > 8 and net_growth(e.target, win) < 0: burst += 1
```
A D_X(t) spike counts as explained only if a bad-signature burst in partition
X precedes it within one checkpoint window — bursts must LEAD drops to be
predictive, not merely forensic.

**Mitigation curriculum.** (i) Partition the store: three context partitions
(pattern from the 11/11 context-switching result), one per curriculum, plus a
SHARED partition for CORE-adjacent invariants; no curriculum's training
episode may kill into another's partition, and any kill touching SHARED needs a
petition+deterministic-evidence gate (wave9 pattern, 40/40). (ii) Deliberate
rehearsal: each curriculum's 24 battery exemplars are pinned; every 400
episodes the learner replays and re-judges them, and any kill request on a
rehearsal member is auto-routed to the gate. (iii) Replacement debt: a kill
that drops a battery check increments a debt counter; the learner must add a
revised memory and re-pass the check, or the gate blocks further kills in that
partition — forgetting becomes budgeted and audited, never a leak.

## 4. Kill bar

Interleaving is KILLED if any fire: (1) any D_X(t) > 10 points after two
completed rehearsal cycles — knowledge genuinely unrecoverable by deliberate
means; (2) any D_X(t) > 10 points with NO preceding bad-forgetting ledger
signature — degradation that is not deliberate forgetting is unobservable
erosion, violating the white-box law; this kills interleaving harder than a
plain metric failure, because the architecture cannot see its own loss;
(3) any kill of a CORE-adjacent or force-pinned memory without a force-pin
audit entry (law violation; halts and invalidates the run). Interleaving
SURVIVES if all D_X(t) ≤ 5 points at every checkpoint, or if transient dips
fully recover within 2 rehearsal cycles with a matching ledger signature
(the 5–10 point recovered zone is logged as interference-not-catastrophe).

## 5. Honesty notes

Weakest point: I assume degradation is always legible in the ledger — but a
learner could "kill by neglect": never rehearse, never kill, just stop using a
memory so the reasoning path that needs it decays. RC3's 100x runs showed
path-level decay is possible without any ledger entry. My cross-partition
kill-rate metric would show nothing while scores drop; that is exactly
kill-condition (2), and I have no design for it yet — it may be the most likely
way interleaving dies. Second weakness: batteries are proxies — a code battery
may miss crispness erosion that shows up as style drift, and the known
sensor-deceivable hole means checks cannot see whether evidence was genuine.
Third: rehearsal is not free — it costs episodes and store slots, and the
budget case is not made here. I am NOT claiming English and code are
fundamentally separable — interference may be structural (shared machinery),
in which case partitioning is a bandage and the honest verdict is that one
learner cannot hold all three at full crispness. The 5/10-point thresholds are
not principled; they are prereg-staked tripwires, revisable only by Micah
before the build.

## 6. Next build step

Build the ledger-instrumented kill-rate monitor on the existing audit trail
(per-partition K_rate counters, cross-partition kill flagging, reason-citation
checks, SHARED-partition law checks), then run a 600-episode code→messy
interference probe to learn whether D_code(t) moves at all and whether kill
bursts lead or lag the score drop — lead/lag decides whether the ledger
signature is predictive or merely forensic. Evidence to build on:
`docs/lab/wave5/` (MA1, 58/58), `docs/lab/wave6/` (RC gates, ledger replay),
`docs/lab/wave9/` (petition+gate, 40/40), `docs/lab/wave10/` (RC3 100x paths).
