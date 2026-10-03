# TNN vs LLMs — capability comparison

**Status: DRAFT idea for a public README. Not published. Every claim below must stay
falsifiable; nothing here may outrun the evidence.**

## The one-line version

There is no LLM size that replicates what TNN does — not because TNN is bigger, but
because the differences are architectural. You cannot scale your way to deliberate memory,
auditable belief, or byte-identical replay. Those are design properties, not emergent ones.

## Parameters buy nothing (2026-09-21, measured)

Two scaling programs, same null result — and the null is the finding:

| Axis | Range tested | Result |
|---|---|---|
| Data | 240 → 6,585,360 facts | mastery 1.0 throughout; exactly 4 ops/fact, 92 B/fact, linear cost |
| Parameters (capacity knobs) | 0.25× → 8× slots, buffers, depth, redundancy | **16 of 19 configs byte-identical learners** — zero behavioral difference, only cost |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** on the Data row — "mastery 1.0 throughout" is the measured value; the bar behind it (KB-SCALING, trip iff mastery drops >2pp) has infinite slack: measured drop 0.00pp, and it tolerates 125,137 wrong facts at N=6,585,360 before tripping. "1.0" is exact to the battery's resolution; the bar could not have failed short of six figures of wrong facts. (T2)

Above the minimum capacity that fits the facts, bigger tables change nothing.
Below it, degradation is exactly proportional and graceful — what fits stays perfect.
**Capability is set by mechanisms and information sources, not buffer sizes.**
What *did* buy capability: new mechanisms (conflict-driven deliberation: 156/156
contradictions resolved at baseline cost on quiet facts) and new information
(the live web-search sense). Evidence: `docs/lab/scale/params/`, `docs/lab/new-mechanisms/`,
`docs/lab/senses/web-search/v2/`.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** on "degradation is exactly proportional and graceful" — qualified: the flaw battery behind reduced-config readings samples ids in [0, n/4) only, blind to capacity loss beyond 4×; per the audit the reduced-config 96/96 is a coverage artifact and must be marked DEGRADED. "Graceful" describes the probed quarter of the id range, not the full store. (H2)

## How to read this

This is not a benchmark shootout. It is a capability map: for each thing TNN demonstrably
does, what is the LLM equivalent, and what size LLM does it take to replicate it?

| TNN capability (measured) | LLM equivalent | What size LLM replicates it? |
|---|---|---|
| Deliberate memory: every stored item explicitly committed, refused, or rolled back (58/58 checks) | None. Weights are not decisions; RAG is a bolt-on database, not belief | **No size.** No LLM deliberates over what to remember |
| Byte-exact recall: 100/100 over 6,144 stored chunks | Hallucination rate falls with scale but never reaches zero; exact recall is unguaranteed at every size | **No size** guarantees it |
| Corruption detection: 64/64 tampered memories caught and killed | No integrity machinery; prompt injection and data poisoning are open problems at frontier scale | **No size** |
| Deliberate belief revision: 18/18 false claims revised on world evidence, 6/6 true claims untouched (180/180 at 10x) | Fine-tuning / RLHF: approximate, causes collateral changes; machine unlearning is an unsolved research problem | **No size** revises deliberately |
| Byte-identical replay: same input + same logged state → identical output, always | Stochastic by design; temperature 0 reduces variation but guarantees nothing across runs or hardware | **No size** |
| Deliberative refusal: 100% over 2,595 genuinely attractive temptations, at 10x and 100x horizons | Refusal is trained behavior, statistically enforced; jailbreaks persist at frontier scale | Frontier scale gets close, never 100%, never architectural |
| Audit trail: every belief carries its ledger entry; full replay to exact state | No provenance: no LLM can show you *why* it believes something | **No size** |
| Long-horizon stability: no degradation at 100x the training horizon | Context degradation is the signature LLM weakness (lost-in-the-middle, drift, collapse) | Larger windows delay it; **no size** eliminates it |
| Learning from a single evidence confrontation, no reward signal | LLMs learn via gradient updates over massive data; one-shot deliberate revision is not a thing | **No size** |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** on "no degradation at 100x" — qualified: the scale-program evidence behind this row rests on KB-SCALING (trip iff mastery drop >2pp; measured 0.00pp; tolerates 125,137 wrong facts at N=6,585,360) and KB-FORGET (trip iff last−first decile gap >3pp; measured 0.00pp; tolerates ~187,700 forgotten early facts), both with infinite slack. "No degradation" means none detectable within the battery's resolution, not absolute absence. (T2, T3)

## The efficiency footnote

Every TNN result above was produced on a single Linux VM, CPU-only, zero GPUs,
fully deterministic. Wherever an LLM equivalent exists at all, it requires datacenter
scale — and still doesn't replicate the capability, only approximates it.

## The catch — no free lunch still stands

TNN running 100% on 8GB of RAM is real, but nothing is free. The prices TNN pays:

1. **Deliberation costs per thought.** Every memory act goes through inspect / propose /
   commit / refuse, plus ledger writes. An LLM forward pass is cheap matrix math; TNN pays
   deliberation overhead on everything it learns. We already measured O(n²) free-slot
   scanning at 10x scale — deliberate systems have per-operation costs that thoughtless
   systems don't.
2. **Breadth is the bill.** TNN learns deeply, but each item costs a deliberation. LLMs
   amortize one giant run across the whole internet, shallowly. For TNN to reach that
   breadth it must perform billions of deliberate learning acts. Whether that's tractable
   is the program's central open bet — the scale legs exist to test exactly this.
3. **Design cost upfront.** Every TNN capability was deliberately built. LLMs get
   capabilities as free (if unreliable) side effects of scale. TNN pays engineering for
   everything.
4. **Determinism isn't free.** Byte-identical replay means logging complete internal
   state; ledgers grow (16MB × 10 runs in the M8 battery). LLMs pay no such storage tax.
5. **Some machinery may be ornamental.** The felt-intensity trial failed honestly —
   15,000+ valid readings changed nothing. No-free-lunch means some organs might not earn
   their keep, and the kill bars exist to find out.

One line: **TNN trades compute-per-thought for thought-per-compute.** Whether
deep-and-expensive beats shallow-and-cheap at world scale is unproven — that's what the
scale legs are for.

## Learning, head to head

| To... | LLM | TNN |
|---|---|---|
| Learn one new thing reliably | Fine-tuning run: curated data, multiple epochs, hyperparameter tuning, regression evals; collateral changes | One deliberate act: inspect → hypothesize → commit, ledgered |
| Fix one wrong belief | Machine unlearning is an unsolved problem; patches shift other behavior unpredictably | Deliberate revision, first-class: 180/180 false claims revised, 0 true ones touched |
| Learn from a single example | Few-shot is prompting, not learning — nothing is retained past the context window | Single evidence confrontation → committed memory |
| Know what changed after learning | Nobody can enumerate what a fine-tune changed | The ledger lists every commit with its evidence and episode |
| Learn without forgetting | Catastrophic forgetting — the reason continual learning is a whole field | Strength-gated deliberate retention; revision is explicit, never silent erosion (our churn-freeze finding is the honest version of this problem, under test) |
| Learn from few exposures | Data-hungry by construction: patterns need thousands to millions of exposures across epochs | Adapts at the frozen threshold from few exposures |

## The honest reverse

A comparison that only runs one way is advertising, not evidence. What LLMs do that
TNN does not — yet:

- **Broad world knowledge:** frontier LLMs carry fluent knowledge across nearly every domain. TNN's knowledge is what it has deliberately learned so far: narrow and young.
- **Open-ended fluency:** LLMs generate fluent text on arbitrary topics out of the box. TNN is building the cognitive architecture first; fluency is downstream.
- **Few-shot task generalization:** LLMs adapt to novel tasks from a few examples. TNN's generalization across tasks is unproven.

TNN's bet is that these are the *easy* direction: once the architecture for deliberate,
revisable, auditable knowledge exists, breadth follows. The LLM bet is the reverse —
that scale will eventually produce deliberation — and the table above is the evidence
it hasn't.

## The claim this document makes

Not "TNN beats LLMs." The claim is narrower and checkable: **there exists a set of
cognitive capabilities — deliberate memory, revision, audit, replay, refusal — that are
properties of architecture, not of scale, and TNN demonstrates them while no LLM at any
size does.** Everything else is future work, on both sides.
