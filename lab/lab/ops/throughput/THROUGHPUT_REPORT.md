# TNN Throughput — the everything table

Date: 2026-09-22. Lab VM. Pinned znc (`znc_linux_x86_64_abed8aa1`).
Method: `ops/throughput/METHOD.md` (documented before measuring; timing-only
instruments, zero logic changes). 5 reps per measurement (8 for learner at
N≥24000 incl. CPU-clock reps); median + range reported.

## The everything table

| Direction | What | Measured | Workload it was measured on |
|---|---|---|---|
| **Input** | install (deliberate learning) | **~6.2 µs/fact CPU → ~162,000 facts/sec**, flat N=240→240,000; 4 ops/fact, 92 B/fact (driver's own accounting) | class-4 direct learner (`sc_teach_value`: slot+verify+audit), P=1, procedural integer facts |
| **Input** | chars/sec equivalent | **~3.2M chars/sec** (order-of-magnitude: 162K facts × ~5 tokens/fact × ~4 chars/token) | same as above |
| **Output** | utterance emission | **~507K chars/sec** median (range 342K–1.29M); **~65 µs per utterance** (range 26–96 µs) | 370-turn dialogue battery, avg 33 chars/utterance, 370/370 correct every rep |
| **Output** | end-to-end (hear→think→speak) | **~109K chars/sec** (range 87K–151K); **~0.30 ms per turn** (range 0.22–0.38 ms) | same battery |
| **Recall** | per-probe | **~0.3–1.0 µs/probe → ~1–3.2M probes/sec**, O(1) in N | read-only `sc_recall` sweeps, N=240→240,000 |
| **Deliberation** | episodes | **~3,300 episodes/sec** (~0.30 ms/turn; min 0.22 ms → 4,600/sec) | one dialogue turn = one episode (understand→resolve→retrieve→compose) on a 38-fact KB |

## Install anchor: re-verification of the 4.2 µs/fact figure

The remembered figure was 4.2 µs/fact (user CPU) → ~238,000 facts/sec.
Re-measured on the same learner lineage today:

- **CPU clock (contention-robust): 5.7–6.2 µs/fact, dead flat across
  N=240 → 240,000** (n=7: 5.74, 6.02, 6.19, 6.08, 6.16, 6.18, 6.14, 6.17).
  → **~162,000 facts/sec.**
- Wall clock under today's load (load avg 8–13 on 2 CPUs, other crews
  running image/audio/compile jobs): median 25–60 µs/fact, min-of-5 down to
  8.9–32 µs/fact.

Verdict: **same ballpark, 1.5× higher than remembered.** The gap is plausibly
VM/cache conditions (the original ran on a quieter box) plus ~3% from this
instrument's 6 clock_gettime calls per fact (documented in METHOD.md). The
4-ops/fact and 92-B/fact figures reproduce exactly (driver's own counters:
4.000–4.004). The "238,000 facts a second" headline becomes **~162,000** on
today's measurement — still ~800× a frontier LLM's ~200 tokens/sec serving
rate in raw facts, ~810K tokens/sec equivalent.

## What each number does and does not mean

**Install (~162K facts/sec).** This is *deliberate learning*: every fact goes
through slot write + verification + a 16-word audit entry. It is not
autocomplete and not a benchmark trick — it is the price of TNN's
truthfulness machinery (verify-before-install, audit-everything). It does not
mean TNN "reads" 3.2M chars/sec of arbitrary text; the char equivalence is an
order-of-magnitude translation so a human can feel the scale, nothing more.
TNN does not generate tokens at all.

**Emission (~507K chars/sec; ~65 µs/utterance).** This is the
deliberation→prose path: a resolved fact rendered into response bytes
(`emit_fact`'s prose templates plus short direct-write paths for yes/no,
comparisons, and contradiction notices). It is fast because composing from a
decided fact is mostly copying — the *thinking* is the expensive part, and
it's measured separately. It does not mean TNN writes essays at 500K
chars/sec; the workload is short factual answers (avg 33 chars). Longer
utterances would raise chars/sec (copy-dominated), not lower it.

**End-to-end (~109K chars/sec; ~0.30 ms/turn).** The full conversational
loop: hear an utterance, resolve referents, retrieve, compose, speak. At
~3,300 turns/sec, TNN holds a conversation roughly 100× faster than a human
can type. This was measured on a tiny 38-fact KB — retrieval cost grows with
KB organization, not raw size (recall is O(1)), but a real deployment's
deliberation would be deeper than this battery's single-fact answers.

**Recall (~1–3.2M probes/sec, O(1) in N).** Probing the KB is 5–20× cheaper
than installing into it, and flat from 240 to 240,000 facts. This is the
asymmetry the architecture wants: learning is the expensive, careful
operation; remembering is nearly free. It does not include the harness's
truth-derivation (~7 µs/probe in the eval sweep) — that's test scaffolding,
not TNN.

**The honest summary for Micah:** TNN learns deliberately at ~162K
facts/sec, remembers at ~1–3M probes/sec, and speaks at ~500K chars/sec once
it has decided what to say (~109K chars/sec including the thinking). The
bottleneck in "saying stuff" is deciding what to say, not saying it — which
is exactly the right shape for a system whose job is to be right, not fast.

## Files

- `ops/throughput/METHOD.md` — method (frozen before measuring)
- `ops/throughput/thru_learner.zag` — install/recall instrument
  (from `scale/fewshot/driver/fewshot_learner.zag`, timing-only diff)
- `ops/throughput/dlg_thru.zag` — deliberation/emission instrument
  (from `dialogue/dialogue.zag`, timing-only diff; `R33_NATIVE_*.zag`
  copied alongside for the `@import`)
- `ops/throughput/run_battery.sh`, `ops/throughput/analyze.py`
- `ops/throughput/runs/` — 32 raw logs + `ANALYSIS.txt`
- Binaries (`*_bin`) and `.zagd.semantic-ready` are build artifacts and are
  NOT committed.
