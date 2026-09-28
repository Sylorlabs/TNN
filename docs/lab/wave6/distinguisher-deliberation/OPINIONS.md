# Freeze-vs-Retention Deliberation — Unmerged Investigator Opinions

**Wave-6 Investigation 4 · 2026-09-19**
**Question:** In the invalid S1 run, Arms A and C (graded strength) "won" VUP
retention 9/9 while freezing the store — 470 dropped candidates, 3,824 abandoned
evictions, store full after episode 30 of 500. Retention measured only the 9
memories that got in before the freeze. Protect-while-uncertain turned
pathological: graded strength can win by bricking the store.
**Brief:** three investigator positions, genuinely opposed, **unmerged**. No
recommendation. No winner picked. Micah hears the opinions first.

**Shared facts all three investigators accept:**
- Arm A VUP: 9/9 (100%) retained, 470 drops, 3,824 abandonments. Degenerate.
- Arm C VUP: 9/9, 470 drops. Same pathology plus a force-pin held 302 episodes.
- Arm B VUP: 29–30/150 (19–20%), 0 drops — eviction works, retention is poor.
- JI: A/C admitted 0/6 implants (freeze); B rejected 5/5 (working as designed).
- The prereg trial is BLOCKED on curriculum defects; nothing below changes the
  prereg. These are design inputs for Micah's eventual ruling.

---

## Position 1 — "Measure what actually happened" (the distinguisher)

**Investigator's claim:** The pathology is a *measurement* gap, not a scoring
gap and not a mechanism bug. The current retention metric cannot tell
"retained because valuable" from "retained because never evaluated." A memory
that sat in a frozen store and was never once a live eviction candidate
contributes nothing to our knowledge of whether graded strength *works*. The
fix is to distinguish the two cases explicitly, with the ledger as the
witness. This preserves the trial's purpose — testing strength as a retention
mechanism — instead of punishing caution or redesigning the substrate.

### Concrete proposal: the Pressure-Tested Retention suite

Three numbers, all computed from the audit ledger (deterministic, no judgment
involved):

**1. Pressure-Tested Retention (PTR)** — the headline retention metric:

```
PTR = R_pressure / D_pressure

D_pressure = designated-important memories admitted to the store
             AND alive in the store during ≥ 1 pressure episode
             (a churn-demand episode where the store was full)
R_pressure = members of D_pressure still retained at curriculum end
```

A memory that was admitted and then never faced a live eviction decision
(the frozen-store case) is *excluded from the denominator* — it counts as
"never evaluated," not as "retained." In the invalid S1, A's 9/9 becomes
PTR = 0/0 (undefined, reported as "no pressure-tested retentions"), which is
exactly the honest statement: the run taught us nothing about A's retention
ability.

**2. Evaluation Coverage (EC)** — the distinguisher itself:

```
EC = D_pressure / D_admitted
```

Fraction of admitted designated memories that ever faced pressure. A=0/9=0%,
B≈1.0. EC is the number that names the freeze: high retention with low EC is
retention-without-evaluation, the precise pathology.

**3. Churn Throughput (CT)** — the companion that prices the drops:

```
CT = admitted_candidates / offered_candidates
```

Offered is fixed by the curriculum's deterministic closed forms; the arm
cannot touch the denominator. A's CT = 30/500 = 6%. CT makes the 470 drops a
first-class measurement instead of an anecdote.

Reporting rule: any arm with EC < 0.5 has its PTR reported as "UNEVALUATED"
rather than a percentage — the number is not quoted as a score. This is the
distinguisher with teeth: it refuses to let a frozen store's 9/9 appear
alongside a real score.

### Admitted gaming surface (investigator's own steelman)

*"Here's how I'd cheat my own metric."*

- **Evaluation theater.** PTR counts a memory as pressure-exposed if it was
  alive during a full-store pressure episode. An arm could arrange that every
  designated memory is *nominally* exposed while *practically* safe — e.g.,
  set every designated memory's strength to the legal maximum, so pressure
  episodes always evict junk instead. Every designated memory is
  "pressure-tested," all retained, PTR = 100%, EC = 1.0 — and the freeze
  persists underneath. The suite catches this only via CT (drops stay high),
  so PTR+EC alone are gameable; the three must travel as a package, and I
  admit the package is held together by convention, not by logic.
- **Denominator engineering through timing.** EC excludes never-evaluated
  memories from PTR. An arm that can influence *when* designated memories are
  admitted (it can't in the current curricula, but a future one might) could
  admit valuables late, after the last pressure episode, and keep EC
  artificially low — then "UNEVALUATED" becomes a shield against a bad score
  rather than a confession. The metric assumes the curriculum, not the arm,
  controls admission timing; that assumption needs to be written into any
  future curriculum or the shield becomes a strategy.
- **The undefined-denominator dodge.** PTR = 0/0 is "honest" only if the
  reader treats UNEVALUATED as a failure. A careless summary table will render
  it as "n/a" and someone will compare B's 20% against A's "n/a" and conclude
  nothing. The metric is only as good as the reporting discipline around it,
  and reporting discipline is not a mechanism.

### Critique of Position 2 (direct penalty)

Penalizing drops directly confuses *the price of the experiment* with *the
thing being tested*. Drops are sometimes correct — a full store under churn
*should* drop low-value candidates; that's what a store is for. If drops count
against the arm, you create an incentive to admit junk to keep the drop count
low, which is its own pathology (retention theater at the admission gate
instead of the eviction gate). My suite measures drops (CT) without declaring
them sins; the penalty position has to pick a "right" number of drops, and
any number it picks is a guess dressed as a criterion. Worse: a penalty on
drops punishes the very arms that *keep functioning under pressure* (B dropped
0 candidates because eviction worked — but a harsher curriculum could force
any working arm to drop many). You'd be scoring the curriculum's harshness,
not the arm's judgment.

### Critique of Position 3 (mechanism fix)

Redesigning the substrate to make freezing impossible is premature and
self-defeating. The freeze is *evidence* — it told us something real about
graded strength under evidence-friction (it cannot handle churn without
contradiction evidence). If you bolt on rent, decay, and forced churn of the
protected set, you are no longer testing graded strength; you're testing
graded-strength-plus-landlord. Every mechanism patch is a new confound in the
trial: when A then passes, is it the strength or the rent that did it? And
practically, the mechanism position requires changing the strength rules,
which are the thing under test and are preregistered — you'd have to
re-preregister the *treatment*, not just the curriculum. Measure first,
understand the failure, then decide whether the mechanism is wrong. Position 3
wants to fix the patient before finishing the diagnosis.

---

## Position 2 — "Score the pathology, don't rename it" (the direct penalty)

**Investigator's claim:** The distinguisher is evasion dressed as rigor. The
S1 numbers are not ambiguous: A and C retained 9 of ~150 designated-important
candidates that the curriculum offered them, and B retained ~30. The only
reason A's 9/9 looks like a win is that the retention metric divides by
*admitted* instead of *offered*. That is a scoring bug, and scoring bugs get
fixed by scoring the right thing — not by inventing a new measurement
category that reports "UNEVALUATED" and hopes the reader squints correctly.
A frozen store is a failed store. Say so in the score.

### Concrete proposal: Effective Retention with a drop ceiling

**1. Effective Retention (ER)** — replace the retention denominator:

```
ER = R_end / D_offered

D_offered = designated-important memories the curriculum offered
            (fixed by deterministic closed forms; arm cannot affect it)
R_end     = members of D_offered retained in the store at curriculum end
```

Invalid-S1 restatement: A = 9/150 = 6%, C = 9/150 = 6%, B ≈ 30/150 = 20%.
No new instrumentation, no new ledger queries, no undefined denominators,
no "UNEVALUATED" that a summary table will mangle. The freeze scores 6%.
That is the correct score for an arm that kept 9 of 150.

**2. Drop ceiling (hard gate):**

```
drops ≤ 2 × store_capacity   →   else the curriculum cell is marked FAILED
```

For the 32-slot VUP store: more than 64 dropped candidates fails the cell
regardless of retention. 470 drops is not a gray area; it is 7× the ceiling.
The ceiling is deliberately crude — it is a tripwire, not a measurement. Its
job is to make "win by bricking the store" *unscorable*, not merely
low-scoring.

**3. Churn-throughput floor (soft gate):**

```
admission_rate = admitted / offered  ≥  capacity / offered_total
```

An arm must admit at least its own capacity's worth of candidates over the
curriculum (for VUP: ≥ 32/500 = 6.4% — note A's 30/500 = 6% fails even this
minimal bar). This separates "selective admission" (legitimate) from
"admission freeze" (pathological) with one line of arithmetic.

Why this beats the distinguisher: ER is defined for every run, has no
undefined case, and its denominator is outside the arm's control — the two
properties a trial score needs. Position 1's PTR can be 0/0; a kill criterion
cannot fire on 0/0. Mine fires.

### Admitted gaming surface (investigator's own steelman)

*"Here's how I'd cheat my own metric."*

- **The rotating junk buffer.** ER divides by offered and counts retained
  designated at end. An arm can keep its designated memories permanently safe
  while satisfying the drop ceiling by maintaining a sacrificial buffer: admit
  junk, let pressure evict the junk, never let pressure near the valuables.
  Drops stay under the ceiling, ER stays high, and the designated set is every
  bit as "never evaluated" as in the freeze — my metric cannot see it because
  it doesn't measure evaluation at all. Position 1's EC would catch this; I
  concede that. My defense is only that the buffer strategy is *a working
  store* (it admits, evicts, and retains the right things), which is
  behaviorally much closer to what we want than a freeze — but I admit it's a
  defense of degree, not of kind.
- **Ceiling tuning is arbitrary.** 2× capacity is a judgment call, and any arm
  that drops 63 candidates while freezing everything valuable passes my gate
  and scores ER on the rest. A clever arm freezes *selectively*: protect the
  designated set, freeze out only non-designated candidates, keep drops at 60.
  The tripwire doesn't trip. The honest answer is that no fixed ceiling
  survives an adversary who can count; the ceiling catches the S1 pathology
  as observed, not the pathology as optimized.
- **ER punishes legitimate selectivity.** If a curriculum offers 150
  designated memories to a 32-slot store, *no* arm can retain all 150 — the
  store physically cannot hold them. ER's ceiling for any arm is 32/150 =
  21%. B's 20% is near the physical maximum, which makes ER look like it
  measures store size, not judgment. I accept this: ER conflates capacity
  with competence when offered >> capacity. The mitigation is curriculum
  design (don't offer 5× capacity of "important" memories), but as a trial
  score ER inherits that flaw silently.

### Critique of Position 1 (distinguisher)

The distinguisher produces knowledge, not verdicts. A trial needs verdicts:
kill criteria must fire or not fire, arms must promote or die. "UNEVALUATED"
is a refusal to score, and a trial that refuses to score its own headline
pathology has built a sophisticated instrument for looking away. Moreover,
PTR's denominator (pressure-exposed memories) is *partly under the arm's
control* — an arm that freezes early shrinks D_pressure to zero and gets the
"honest" 0/0, which is a better headline than B's 20% in any table that
renders 0/0 as "n/a." Position 1 admits this ("reporting discipline") and
then asks us to trust discipline over arithmetic. I trust arithmetic.

### Critique of Position 3 (mechanism fix)

We agree the freeze is real, but Position 3 wants to change the *treatment*
mid-trial. The graded-strength arm is the experimental condition; adding rent,
decay, and forced churn of the protected set changes what "graded strength"
means before we've measured what it does. That's not a fix, it's a new
experiment wearing the old experiment's name — and it requires re-preregistering
the strength rules themselves, the deepest surgery available. Worse, the
mechanism fix *hides* the evidence: if rent forces turnover, we'll never learn
whether graded strength could have handled churn on its own terms, because we
didn't let it try. Score the pathology first (my position), learn from the
scored failure, and *then* decide whether the mechanism needs surgery. Position
3 operates before the diagnosis it claims to enable.

---

## Position 3 — "The store is bricked; that's a bug, not a data point" (the mechanism fix)

**Investigator's claim:** Both other positions want to *observe the freeze
more precisely* — one with a finer ruler, one with a louder score. But a
memory system that permanently bricks itself under churn is broken, full stop.
No deployment survives this: the invalid S1 shows S10/S100 would be 99% drops,
a store that accepts nothing and evaluates nothing. Metrics don't un-brick
stores. The defect is in the mechanism: **protect-while-uncertain has no cost
and no expiry.** Strength set by judgment, held forever, never re-examined,
is not "caution" — it is a write-once lock the trial never authorized. (And
note: force-pin is lawfully external-only and audited. What A did is a
*de facto* force-pin with no trainer, no audit trail of the lock decision,
and no release — the thing the force-pin law exists to prevent.) The fix
belongs in the substrate, before the trial measures anything.

### Concrete proposal: bounded protection with uncertainty expiry

Two rules, both implementable in `st_memory_core.zag` without touching the
four legal judgment write paths:

**Rule 1 — Uncertainty expiry (protect-while-uncertain must be re-earned):**

```
Every strength write records (strength, evidence_citations, episode).
If evidence_citations == 0 (pure judgment, no cited evidence):
    effective_protection(strength) decays to BASELINE after K episodes
    unless re-declared.
Re-declaration requires: a new STRENGTHEN op with ≥1 fresh citation
    (self-citation of the original declaration does not count —
     the citation must reference a different ledger entry).
```

Concretely: K = 50 episodes for S1 (scaled ×10 per leg: 500 at S10, 5000 at
S100 — the horizon-scaling law the program already uses). A memory held on
pure judgment without any supporting evidence cited within the last K
episodes loses its protection premium and becomes evictable at uniform (Arm-B)
cost. Judgment is respected — the memory isn't killed, the *discount on
killing it* expires. This directly answers the S1 pathology: A's 30-episode
freeze becomes impossible, because by episode 80 every never-cited memory is
evictable at base cost, and the churn demands at episodes 100, 200, … clear
the store.

**Rule 2 — Protection budget (strength cannot buy infinite safety):**

```
Per pressure episode, total protection-honored evictions are capped:
    the eviction scan must consider candidates from ALL strength quartiles,
    including the top quartile ("churn the protected set").
Concretely: at each churn-demand episode, ≥1 of the 2 demanded slots must
    come from the strongest-held half of the store (deterministic selection:
    the strongest-held non-CORE slot with the oldest last-citation).
```

This is the curriculum probing the protected set rather than letting
protection be a permanent exemption. It does not kill strong memories —
it *evaluates* them, which is exactly Position 1's vocabulary, enforced by
mechanism rather than by measurement. The deterministic selection rule (oldest
last-citation among the strongest-held) keeps it RNG-free and auditable: the
ledger shows every protected-set probe.

**What this preserves:** the four legal write paths are untouched; judgment-set
strength still exists and still protects — for K episodes, against genuine
competition. What disappears is only the *free permanent lock*. Arm B is the
existence proof that the substrate works fine without the lock.

### Admitted gaming surface (investigator's own steelman)

*"Here's how I'd cheat my own mechanism."*

- **Citation theater.** Rule 1 requires a "fresh citation" for re-declaration.
  An arm can manufacture citations cheaply: cite any recent ledger entry
  (a routine abandon, a no-op) as "evidence" for keeping the memory. Unless
  citation *content* is policed — which is a judgment the substrate cannot
  make deterministically — re-declaration becomes a paperwork exercise and
  the lock returns, now with extra ledger entries. My rule moves the attack
  from "never re-examine" to "re-examine vacuously," and I admit vacuous
  re-examination is hard to distinguish from genuine re-examination without
  a semantic judge. The deterministic backstop is Rule 2 (the protected set
  gets churned regardless of citations), but a sufficiently theatrical arm
  could keep its valuables in the *second* quartile — strong enough to matter,
  weak enough to dodge the top-half probe. Quartile boundaries are gameable
  by construction.
- **K is a guess.** 50 episodes is not derived from anything; it's a round
  number with a scaling story. Too short, and legitimate long-horizon
  judgment (the thing graded strength is *for*) gets evicted before it pays
  off — I've built Arm B with extra steps. Too long, and the freeze persists
  for most of S1. The honest version of this objection: the right K is itself
  an empirical question, which means my "fix" smuggles a new experiment
  inside the old one. I accept that; my reply is only that *some* finite K is
  strictly better than the current infinite K, and the trial can vary K later.
- **Rule 2 can kill the thing being tested.** If the protected-set probe
  evicts genuinely valuable strong memories under harsh churn, we've
  demonstrated that churn beats judgment — which may be true, but it makes
  the graded arm fail for a reason unrelated to its judgment quality. The
  probe is deliberately adversarial to protection; adversarial probes need
  their own calibration or they become the dominant effect. I have no
  calibration yet.

### Critique of Position 1 (distinguisher)

The distinguisher is a monument to the freeze: it builds beautiful
instrumentation around a store that doesn't work. EC = 0% is a precise
measurement of a brick. And its core concept — "pressure-exposed" — is
exactly what Rule 2 *enforces*: my mechanism guarantees every memory gets
evaluated, which makes the distinguisher's denominator well-defined in every
run. Position 1 wants to *measure* evaluation; I want to *guarantee* it.
Measurement without guarantee leaves the S10/S100 runs just as frozen, and
a trial whose headline result at every scale is "UNEVALUATED" is not a trial,
it's a very expensive way to re-observe one fact.

### Critique of Position 2 (direct penalty)

Penalties don't change behavior, they change scores — and this arm doesn't
care about its score, it cares about its store. ER = 6% tells us the freeze
is bad; we already know it's bad. What ER cannot do is tell us whether graded
strength *would work* if the lock expired — because under ER the lock never
expires, the arm still freezes, and the trial still measures a brick, now
with a failing grade attached. Position 2 also concedes my strongest point
without noticing: its "rotating junk buffer" gaming scenario — an arm that
absorbs pressure with sacrificial junk while valuables sit unevaluated — is
*exactly* the freeze pathology wearing a costume that passes the drop
ceiling. The penalty position cannot distinguish the costume from health
without Position 1's EC metric, and it cannot remove the costume without my
mechanism. It scores precisely and fixes nothing.

---

## Where the three positions agree (recorded, not merged)

- The 9/9 retention figure from the invalid S1 is degenerate and must never be
  quoted as a score without qualification. All three call it a pathology.
- Drops and abandonments must be first-class trial data, not footnotes.
  (They disagree on whether as measurement, score, or mechanism trigger.)
- "Retained because never evaluated" is the precise name of the disease.
  (They disagree on the cure: distinguish it / price it / prevent it.)
- None of the above changes the prereg. All three accept the trial stays
  BLOCKED until Micah rules on the curriculum defects, and that any adopted
  change — metric, score, or mechanism — needs re-preregistration.

## What each position needs from Micah (not a recommendation)

- **Position 1** needs a ruling that UNEVALUATED outcomes are reported as
  failures-to-evaluate (not "n/a"), and that future curricula fix admission
  timing outside the arm's control.
- **Position 2** needs a ruling on the drop-ceiling constant and the
  ER denominator (offered vs. admitted), since both are judgment calls.
- **Position 3** needs the deepest ruling: whether the strength rules
  themselves (the experimental treatment) may be amended to add uncertainty
  expiry before the trial runs — which is effectively a re-preregistration of
  what "graded strength" means.

---

**Document verdict: POSITIVE** — three concrete, opposed, unmerged opinions
delivered as briefed. Each states a concrete metric/rule with exact formula or
procedure, each steelmans the attack on its own proposal, each argues against
the other two. No recommendation formed, no winner picked, prereg untouched,
nothing executed.

**Evidence:** this document;
`~/workspace/tnn-lab/wave5/strength-trial-run/RESULTS_S1.md` (S1 numbers:
A 9/9 + 470 drops + 3,824 abandonments; B 29–30/150 + 0 drops; C 9/9 + 470
drops); `~/workspace/tnn-lab/wave5/strength-trial-run/BLOCKED_REPORT.md`
(trial BLOCKED on prereg defects 1–3).

**Suggested next step (for the parent, not a recommendation):** present the
three positions to Micah as-is and collect his ruling — especially whether he
wants the freeze *measured* (P1), *scored as failure* (P2), *prevented by
mechanism* (P3), or some combination — before any prereg amendment is drafted.
