# HTD-1 Red-Team Brief — The Debate Phase

**Role:** RED-TEAM debate worker. **Scope:** DEBATE phase only — no building.
**Date:** 2026-09-20. **Author:** red-team worker (subagent).

**Thesis:** HTD-1 is asking at least one of its two questions too early, and
the other in a form that invites vacuous wins. This brief argues the
premature-optimization case, the efficiency-without-a-workload case, proposes
program-level kill bars *for HTD-1 itself*, identifies ill-posed hypothesis
families, and gives an honest proceed/narrow/park verdict.

This is not an attempt to kill the program. Kill criteria are binding in this
program — and they bind the program's own questions too.

---

## 1. The premature-optimization case: generation tests on unsettled atoms

### The fact on the ground

The units program is mid-flight: 53 representation arms under a frozen prereg
(`docs/lab/units/PREREG_FREEZE.md`, signed), testing what the atoms of
knowledge even *are*. No section champions yet. Micah's standing question —
"what is a unit of knowledge, if not an LLM token?" — is **unanswered**.

Any generation-style test (AR vs diffusion-style vs all-at-once) is a test of
*how atoms are emitted*. Emission order, step cost, parallelism, and
context-coupling are all **atom-relative properties**. You cannot measure them
before the atoms exist.

### The dilemma — specific and, I claim, devastating

For any generation-style head-to-head run on proxy atoms, exactly one of two
things is true:

- **(a) The verdict is atom-relative.** "Parallel beats AR" holds for the
  proxy atoms used, but flips or voids when the winning arm yields different
  atoms (whole reasoning steps, deliberation traces, signed memory values —
  families with wildly different independence structure, granularity, and
  composition cost). The result proves something about the *proxy*, not about
  TNN's generation style. It will have to be re-run after the units program
  settles — meaning the HTD-1 generation track, run now, produces **throwaway
  evidence**. Worse: throwaway evidence with the *shape* of a verdict, which
  is how premature conclusions get smuggled into architecture decisions.
- **(b) The verdict is atom-invariant.** It holds across all plausible atom
  families — e.g., "ordering always costs at least X." Then it is so abstract
  it cannot answer Micah's actual question (what is TNN's generation style?),
  because generation style is a concrete architectural commitment about real
  atoms. An atom-invariant result is a theorem, not a design decision.

Either way, running the generation track now cannot produce an actionable
architectural verdict. That is the precise sense in which it is premature:
**the experiment's dependent variable (generation quality/cost) is undefined
until its independent variable (the atom ontology) is fixed.**

### Three concrete failure mechanisms

1. **Independence smuggling.** Parallel/all-at-once generation *presumes*
   atoms whose emission is mutually independent (or whose dependencies are
   known and cheap). But the independence structure of TNN's atoms is exactly
   what the 53 arms are measuring. Testing G-PA* now means *assuming the
   answer to a question the units program hasn't answered* — and the assumed
   answer is whichever atom family the proxy task happens to use.

2. **The decoder that doesn't exist.** TNN has cognition and no decoder. No
   settled commitment exists that TNN "generates" anything at all in the
   sense these tests assume — deliberation traces, hypothesis revision, and
   memory consolidation are not obviously emission processes. Testing
   generation styles is benchmarking a component the architecture hasn't
   decided to have. It is a spark-plug benchmark for an engine that might be
   electric.

3. **Granularity inversion.** If the winning atom turns out *coarse* (a whole
   deliberated judgment, a signed memory value), then "autoregressive vs
   parallel" collapses: emitting one coarse atom has no meaningful order
   question, and the interesting efficiency question moves *inside* the atom
   (how the judgment was formed), which is the deliberation-economy question,
   not a generation-style question. The generation track could be testing a
   distinction that the atom decision dissolves.

### What a generation test run now would actually prove

At best: "on proxy atoms of family F, with proxy task T, emission strategy S
wins on metric M." That sentence contains three proxies and zero commitments
TNN will keep. It proves nothing about TNN.

---

## 2. The efficiency-without-a-workload case

Micah's first question — "human brains took the free lunch; how far can
deliberate efficiency go?" — is the right question. Asked now, it has a
structural measurement problem: **efficiency is a ratio, and the denominator
(workload) doesn't exist yet.**

### The mechanism by which proxy-benchmark efficiency fails

1. **Relevance is workload-defined; sparsity presumes relevance.** Every
   E-SP* hypothesis ("wake only relevant parts") needs a relevance oracle: a
   function from (state, task) → which parts matter. On a proxy workload, the
   oracle is calibrated to the *proxy's* relevance distribution. Real
   deliberative work — multi-turn hypothesis revision, integrity checks,
   consolidation — has a different relevance distribution: parts that look
   irrelevant on a proxy (e.g., the audit-ledger writer, the provenance
   checker) are load-bearing on real work. Optimizing routing for the proxy
   then **silently degrades the real workload while reporting a win**. The
   failure mode is not "the win disappears" — it's "the win is real on the
   proxy and the architecture is corrupted for the actual job."

2. **Skipped work looks free.** A sparse system's headline number —
   fraction of substrate awake — is maximized by *not doing work*. Without a
   fixed, demanding workload, there is no way to distinguish "efficiently
   skipped" from "never attempted." Long-horizon coherence degradation from
   skipped deliberation only shows at scale (this program's own lesson from
   the felt-intensity trial: the harness, not the feeling, was broken — proxy
   setups hide structural failures). A micro-benchmark cannot see it.

3. **Wakeup-cost inversion.** On small proxies, the cost of deciding what to
   wake dominates; always-awake looks bad. At scale with hot state, the
   routing/decision overhead of fine-grained sparsity can exceed the savings.
   The crossover point is a property of the *workload*, so a proxy measured
   below the crossover "proves" sparsity wins, and the conclusion reverses on
   real work. This is not hypothetical — it is the standard shape of routing
   overhead curves.

4. **The moving-denominator trap.** "20% more efficient" on an undefined
   workload is not a claim; it's a slogan. Any efficiency hypothesis can win
   by redefining work downward (fewer deliberation steps = "leaner"). The
   program's own integrity work showed that techniques, not architecture,
   move behavior — an efficiency technique that reduces deliberation *is* a
   behavior change, and without a fixed quality bar on a fixed workload it
   will read as a pure win.

### What "the free lunch" actually requires

Brains' efficiency comes from two things TNN does not yet have: a **fixed
workload** (keeping a body alive in a world) and a **fixed substrate**
(neurons with known costs). TNN has neither fixed. Optimizing routing now is
designing a circulatory system before the body plan exists. The honest
sequence is: workload first (what real deliberative work looks like at
scale), cost model second (what counts as work — see §3, KB-HTD-1.5),
sparsity third.

---

## 3. Kill bars FOR HTD-1 ITSELF (program-level, numeric, firable)

Kill criteria bind the program's questions, not just its hypotheses. Each bar
below names its trigger, its measurement, and its consequence. All require
Micah's re-approval to amend, per standing law.

### KB-HTD-1.1 — Atom-independence gate (generation track)

**Bar:** The debate phase must produce at least one proxy generation task
whose definition does not depend on the choice among the 53 arms' atom
ontologies.
**Firing test:** Take the top two candidate proxy tasks. Re-run each task's
measurement definition across ≥3 materially different arm families (e.g.,
episodic-chunk atoms, deliberation-trace atoms, signed-value atoms). If for
*either* task the measurement is voided or its rank-ordering of generation
strategies flips in ≥1 family, the bar fails.
**Consequence:** Generation track (G-AR*, G-PA*) is **SUSPENDED** until the
units program names section champions. The debate output for the track is
archived, not discarded — it becomes the test plan for post-champion runs.

### KB-HTD-1.2 — Champion-availability gate (generation track)

**Bar:** No generation-style build begins before the units program reports
section champions (per PREREG_FREEZE verdict §7 analog).
**Consequence:** Automatic SUSPEND. This is a calendar-independent gate: it
fires on the state of the units program, not on a date.

### KB-HTD-1.3 — Real-workload efficiency bar (efficiency track)

**Bar:** An efficiency hypothesis proceeds past pilot only if it beats the
always-awake baseline by **≥20% on total cost** on a **real workload** —
defined as ≥500 deliberative episodes of genuine TNN work (existing assets
count: MA-run logs, strength-trial traces, debate-trace corpora — real
deliberation, not a proxy task), with output quality held within **2%** of
baseline on the workload's native quality metric.
**Firing test:** Pilot runs on the real workload; if best hypothesis <20%
total-cost win or quality drops >2%, the track is **PARKED** (not killed —
parked pending a real scaled workload).
**Consequence:** PARKED. The 20% is deliberately high: below it, measurement
noise and audit-overhead accounting dominate, and the program has a history
of small proxy wins that didn't transfer.

### KB-HTD-1.4 — Transfer-void rule (efficiency track)

**Bar:** Any efficiency win claimed on workload family W must be re-measured
on a held-out workload family W' with different structure (different
deliberation depth, different memory churn).
**Firing test:** If the win on W' is <50% of the win on W (transfer gap
>50%), the claim is **VOID** and the hypothesis returns to pilot; two voids
= PARKED.
**Consequence:** Prevents proxy-shaped architectures (the §2 failure
mechanism) from advancing on a single workload's numbers.

### KB-HTD-1.5 — Full-cost accounting validity rule (efficiency track)

**Bar:** Every efficiency measurement must include **total cost** = compute +
memory-state updates + **audit/ledger write volume** + verification overhead.
**Firing test:** Any reported win computed without the ledger term is
**INVALID** — not a weak result, an invalid one, rejected at review.
**Rationale:** Per TNN law everything is audited and replayable. Sparse
routing that saves compute but doubles audit volume (finer-grained wake
events = finer-grained audit entries) is not a win; it's cost moved
off-book. This is the single most likely way E-SP*/E-LG* "wins" dishonestly.

### KB-HTD-1.6 — Cost-model-first rule (debate-phase gate)

**Bar:** Before any efficiency hypothesis is built, its proponents must state
in closed form: what counts as *work*, what counts as *overhead*, and what
the always-awake baseline costs on the chosen workload.
**Firing test:** No closed-form cost model by end of debate phase →
hypothesis is **PARKED** as untestable, not admitted to prereg.
**Rationale:** You cannot preregister kill bars for a hypothesis whose cost
function is prose.

### KB-HTD-1.7 — HTD-format credibility bar (meta)

**Bar:** If KB-HTD-1.1 fires (generation track suspended) AND KB-HTD-1.3
fires (efficiency track parked), HTD-1 as a flow is **SUSPENDED**, not
re-scoped into a third question.
**Rationale:** HTD-1 is the first htd flow; its credibility sets the format's
credibility. Reporting a vacuous verdict damages the format more than
suspending an untestable question. Per Micah's law: honest failure reported
as-is — and "not yet testable" is an honest result.

---

## 4. Ill-posed hypothesis families — and what would make them well-posed

| Family | Verdict | Why ill-posed | What makes it well-posed |
|---|---|---|---|
| **G-AR*** (autoregressive generation) | ILL-POSED now | Presumes a linear emission order over atoms; if atoms are deliberation traces (branching, parallel), "AR" has no referent. Order is atom-relative. | Atoms defined AND emission order is an architectural question (e.g., sequence-constrained output). Needs KB-HTD-1.1 to pass. |
| **G-PA*** (parallel / all-at-once) | ILL-POSED now (most) | Presumes atom independence — the exact property the 53 arms are measuring. Tests the answer by assuming it. Mirror image of G-AR*'s flaw. | Measured independence structure of the champion atoms first; parallelism tested *against that structure*, not assumed. |
| **G-CO*** (constitution/deliberation-gated generation) | NARROWABLE now | Best-positioned: it tests against *settled* law (constitution, audit, deliberative standards) rather than unsettled atoms. Ill-posed only if it smuggles an atom assumption inside the gate. | Restrict to: "given a fixed candidate output, what must deliberation verify before release?" — no claim about how the candidate was produced. |
| **E-SP*** (sparse routing / wake-only-relevant) | ILL-POSED now | Relevance oracle is workload-defined; on a proxy the oracle is circular (§2.1). | Relevance ground truth from a real workload first ("relevance calibration" research, no architecture claims until then); full-cost accounting per KB-HTD-1.5. |
| **E-DE*** (deliberation economy — how much deliberation per decision) | PROCEED NARROWED | The most load-bearing question: TNN deliberates everything by architecture, so deliberation cost is the real budget. Ill-posed only if "deliberation unit cost" is measured in proxy compute instead of end-to-end cost (audit + state) on real runs. | Cost measured end-to-end on real deliberative corpora (existing MA/strength-trial logs); closed-form cost model per KB-HTD-1.6. |
| **E-LG*** (ledger economy) | DANGEROUS as framed | The ledger is append-only and byte-identical **by law**. "Economizing" it trades integrity for bytes unless proven otherwise. Highest catastrophic-failure surface of any family. | Integrity gate first: 100% replay-to-exact-state on every run, zero tolerance; only then is a byte/compute saving admissible as "efficiency." Any E-LG* hypothesis without the integrity gate is not an efficiency hypothesis — it's a corruption vector. |

---

## 5. Honest verdict: proceed / narrow / park

### PROCEED NOW (does not depend on unsettled atoms)

1. **The metrics spec** — the debate worker on metrics is doing the most
   important work in HTD-1: closed-form cost models, what counts as work,
   full-cost accounting incl. the ledger term (KB-HTD-1.5). This is load-
   bearing for every future htd flow, not just this one.
2. **E-DE* narrowed to cost-model + measurement work on existing real
   corpora** — MA-run logs, strength-trial traces, debate traces are *real
   deliberative work already in hand*. "How much does deliberation cost,
   end-to-end, on work we actually did?" is answerable today and needed
   before any sparsity claim.
3. **The kill-bar framework itself** (§3) — program-level bars are the
   deliverable that keeps HTD-1 honest whether its questions are ready or not.

### NARROW (testable sub-question only)

4. **E-SP* → "relevance calibration" only.** No routing architectures, no
   wake/sleep mechanisms. One question: can we define relevance ground truth
   on real deliberative corpora such that a sparsity oracle trained on it
   predicts which state mattered to outcomes? If yes, sparsity becomes
   testable later. If no, E-SP* stays parked — and that's a result.
5. **G-CO* → output-gating only.** "What must deliberation verify before a
   candidate output is released?" — testable against settled constitutional
   law, atom-agnostic. The generation-style comparison is stripped out.

### PARK (until preconditions hold)

6. **G-AR* vs G-PA* head-to-head — PARKED.** This is the flagship comparison
   and the most premature. Precondition: units champions named (KB-HTD-1.2)
   AND an atom-independent task definition exists (KB-HTD-1.1). The debate
   output becomes the parked test plan; nothing is lost except the illusion
   of progress.
7. **Any efficiency architecture claim that cannot clear KB-HTD-1.3** on a
   real workload — PARKED, not killed. The 20% bar and the transfer-void rule
   exist because this program has already learned (felt-intensity trial, RNG
   verdict) that proxy wins don't transfer and honest failures are the norm,
   not the exception.
8. **E-LG* as "savings" — PARKED pending the integrity gate.** Ledger work
   may proceed only as integrity research (can we prove cheaper encodings
   preserve replay-to-exact-state?), never as cost-cutting.

### The one-line version

**Measure cost now (metrics + deliberation economy on real corpora), calibrate
relevance as research, and park the generation-style showdown until the atoms
it's about exist.** HTD-1's honest output may be "one question answered, one
question parked" — and under this program's laws, that is a pass, not a
failure.
