# Throughput measurement — METHOD

Date: 2026-09-22. VM: lab VM (~/workspace/tnn-lab). Toolchain: pinned
`toolchain/bin/znc_linux_x86_64_abed8aa1`, `--no-analyze` (same as BUILD.md).

This is measurement, not a hypothesis trial: no prereg, but the method is
documented here BEFORE measuring and kept stable across all runs below.

## Instruments

Both instruments are timing-only copies of proven lab machinery. No learning,
deliberation, or emission logic is changed — only wall-clock reads added.

### 1. thru_learner.zag (install + recall)

Source: byte-copy of `scale/fewshot/driver/fewshot_learner.zag`
(championship class-4 direct-learning lineage — the same learner core as
`scale/driver/scale_learner.zag`, which produced the remembered 4.2 µs/fact
figure: identical `t5_verify`/`t5_add` field writes, return codes, audit
contents, and 16-word audit layout).

Timing-only changes:
- `sc_run_pass` takes three extra `*i64` accumulators and times, per fact,
  (a) truth derivation (harness-side: `sc_fact_truth` + `sc_supplied`,
  wall clock), (b) `sc_teach_value` (the learner's install path: slot write
  + verify + audit; wall clock), and (c) the install path on the process
  CPU clock (`clock_gettime(CLOCK_PROCESS_CPUTIME_ID)` = user+sys CPU
  actually consumed — robust under VM contention, and the same "user CPU"
  basis as the remembered 4.2 µs/fact figure). Cost: 6 extra clock_gettime
  syscalls per fact (~150ns, ~3% at 4 µs/fact; documented, not hidden).
- Prints `THRU_INSTALL,pass=<p>,facts=<n>,ns_teach_total=<t>,ns_teach_cpu_total=<c>,ns_truth_total=<u>`
  per pass.
- Recall microbenchmark: the original fixed 2000-sweep version is kept in
  spirit but made adaptive — `sweeps = clamp(2_000_000 / n, 1, 20000)` —
  targeting ~2M read-only `sc_recall` probes per measurement (the fixed
  version would take ~2.4 min/rep at N=240k). Prints
  `THRU_RECALL,recalls=<r>,ns_total=<t>,sweeps=<s>`.
- The mastery eval sweep (`sc_run_eval`, one full read-only sweep with
  harness truth derivation per probe) is timed as a realistic recall
  workload: `THRU_EVALSWEEP,probes=<n>,ns_total=<t>`.
- Clock: `clock_gettime(CLOCK_MONOTONIC)` via raw syscall 228, wall-clock,
  harness-side only, never part of deterministic state (same convention as
  the original `SCALE_RECALL_TIMING` line).

Workload: `thru_learner train <N> 24 <N/24> 1 <rep> ~/workspace/scale/corpus/texts`,
N ∈ {240, 2400, 24000, 240000} (3 orders of magnitude), 3 reps each.
Per-pass timing excludes the fixed one-time corpus init (~1.4s) and store
init. P=1 (single pass; the remembered figure is marginal per-fact).

### 2. dlg_thru.zag (deliberation + utterance emission)

Source: byte-copy of `dialogue/dialogue.zag` (2026-09-22 dialogue trial:
370 turns, 99.7% pass — TNN's real deliberation-to-utterance path:
gazetteer scan → sentence processing → retrieval → `emit_fact` prose
rendering into the response buffer).

Timing-only changes:
- `now_ns()` helper added (`clock_gettime(CLOCK_MONOTONIC)`, raw syscall 228).
- `do_turn` gains two extra `*i64` accumulator params (one call site, in
  main): all 4 `emit_fact` call sites are wrapped so emission time is
  accumulated even on the correction branch's early return.
- main wraps each `do_turn` call (one full deliberation episode:
  understand utterance → resolve → retrieve → compose response) and
  accumulates response bytes (`g32(resp,0)` per turn).
- Prints `THRU_TURNS,turns=<t>,ns_total=<n>,chars_total=<c>` and
  `THRU_EMIT,emits=<e>,ns_total=<n>`.

Workload: `dialogue/battery.txt` (370 user turns, 8 categories), run with
cwd=`dialogue/` (reads kb.txt, gaz.txt, battery.txt), 3 reps.

## Metrics

- Install: `ns_teach_total / facts` → µs/fact; facts/sec = 1e9 / ns_per_fact.
  Headline = teach path only (truth derivation reported separately).
- Recall: `ns_total / recalls` (microbenchmark) → ns/probe, probes/sec;
  `THRU_EVALSWEEP` gives the realistic single-sweep per-probe cost.
- Deliberation: `ns_total / turns` → ms/turn; episodes/sec = turns / (ns/1e9).
- Emission: `ns_total / emits` → µs/utterance;
  chars/sec (emission) = chars_total / emit_s;
  chars/sec (end-to-end) = chars_total / turn_s.
- Aggregation: median of 3 reps + range (min–max). No min-of-N cherry-picking.

## Honesty scope

- "Facts" are procedural integer facts (92 B/fact, ~4 ops/fact per the
  driver's own SCALE_OPS accounting — re-verified, not assumed), not prose.
- Wall-clock on a shared VM; ranges shown, not hidden.
- Install measures deliberate learning (slot+verify+audit), not autocomplete.
  TNN does not generate tokens; token/char equivalences are order-of-magnitude
  translations, labeled as such.
