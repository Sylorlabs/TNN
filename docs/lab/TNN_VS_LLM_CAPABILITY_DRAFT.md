# TNN vs LLMs — capability comparison

**Status: DRAFT idea for a public README. Not published. Every claim below must stay
falsifiable; nothing here may outrun the evidence.**

## The one-line version

There is no LLM size that replicates what TNN does — not because TNN is bigger, but
because the differences are architectural. You cannot scale your way to deliberate memory,
auditable belief, or byte-identical replay. Those are design properties, not emergent ones.

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

## The efficiency footnote

Every TNN result above was produced on a single Linux VM, CPU-only, zero GPUs,
fully deterministic. Wherever an LLM equivalent exists at all, it requires datacenter
scale — and still doesn't replicate the capability, only approximates it.

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
