# Slice 13 — Memory-decision invariance (Track 1: state-dependent deterministic variation)

## 1. Slice
Firewall guaranteeing the variation function cannot influence deliberate memory operations
(kill/pin/promote/demote/strengthen/weaken): memory judgments stay pure functions of
(evidence, existing judgments, constitution) while expression/phrasing/path vary lawfully.

## 2. Falsifiable claim
For every episode in the differential suite, replaying the episode with all expression-state
variables perturbed (phrasing history, wording counters, style registers, elaboration-depth
cursor, path-choice memo) while holding evidence, memory store, judgments, and constitution
byte-identical produces byte-identical memory-op sequences AND byte-identical ledger
contents. If any perturbation class changes any memory decision, the firewall has leaked
and the design is dead.

## 3. Design

**Module boundary.** Two Zag modules, one-way visibility:
- `mem_judge.zag` — owns kill/pin/promote/demote/strengthen/weaken. Its `mem_decide`
  takes exactly one struct: `JudgeInput { evidence, judgments, constitution }`. It does
  NOT `@import` the variation module and does not name any expression-state type; the
  compile gate greps the import graph and fails the build on any edge `mem_judge ->
  vary_expr`.
- `vary_expr.zag` — owns expression, phrasing, path, ordering, elaboration. It receives
  the concluded verdicts and raw memory decisions as READ-ONLY output and renders text.
  It may never emit a `MemOp` and may never call `mem_decide` (its module does not import
  the memory-op constructor; ops are constructed only inside `mem_judge`).

**Allowed call graph (and nothing else):**
```
judge_loop → mem_decide(JudgeInput) → MemOp[] → ledger_append (judge path only)
judge_loop → conclude(verdicts, MemOp[]) → render(VaryState, conclusions) → text
```
Forbidden edges: `mem_decide` reading any `VaryState` field; `render` writing to the
store, ledger, or judgments; any variation-state hash used as a tie-breaker inside the
judge path. Tie-breaks inside `mem_decide` are lawful and deterministic by construction:
fixed priority order (slot id → evidence priority → episode index), never expression state.

**Why type-level, not discipline-level:** per Micah's no-RNG law and the MA1 audit
(`docs/lab/wave4/...` on branch `tnn-native-lab`), deliberate ops already replay to exact
state from logged state. The firewall extends that: the replay function for `mem_decide`
requires ONLY `JudgeInput` bytes, so expression-state perturbation cannot be an input by
construction. Strength judgments follow the standing ruling: strength set by judgment
(Micah 2026-09-20: overwriting a strong memory costs the full erase price, no cheap-edit
path) — the price schedule lives in the constitution struct, inside the firewall.

**Leakage audit (continuous, in CI):** differential suite — 200 curriculum episodes × 8
perturbation classes (wipe phrasing history; max out wording counters; flip style
registers; pin elaboration cursor at min/max; scramble path-choice memo; reorder
equivalent phrasings; swap elaboration depth; null the conversation register). Each run:
replay episode with perturbed `VaryState`, identical `JudgeInput`; compare `MemOp[]`
sequence op-by-op (code, slot, strength value) and ledger bytes. Instrumentation adds a
read-watch: any read of a `VaryState`-tagged word by code in the judge call graph is
logged; nonzero reads = leak even if outputs happened to match.

## 4. Kill bar
Preregistered, binding: the design is killed if ANY of the following fires —
(a) ≥1 episode in the 200-episode × 8-class differential suite (1,600 replays) yields a
`MemOp` sequence differing in op code, target slot, or strength value from the baseline;
(b) ≥1 replay yields ledger bytes differing from baseline (ledger contents MUST NOT
vary); (c) the read-watch logs any `VaryState` read inside the judge call graph on any
replay; (d) the compile gate finds an import edge `mem_judge -> vary_expr`. Zero
tolerance: one leaked decision kills the firewall, not the threshold.

## 5. Honesty notes
- This firewall proves *non-influence of the variation function*, not *correctness* of
  memory judgments: a wrong-but-invariant judgment passes. Judgment quality is judged
  by other slices (adversarial curricula, trap suites).
- The exact leakage condition is observational: if a leak exists that never fires on the
  1,600 replays, the differential test misses it; the read-watch and the compile gate
  are the structural backstops, and I am NOT claiming the perturbation set is exhaustive
  (a novel expression-state channel added later must extend the 8 classes — Track 1 rule).
- Human trainer force-pin is the one lawful irreversible op (standing law); it enters via
  the constitution struct, inside the firewall — a force-pin must never be derivable from
  expression state either.
- I am not claiming the judge path is free of ALL state-dependence: lawful dependence on
  full internal judgment state is the point of the program; the claim is only that the
  *variation function's* state is excluded.
- Weakest point: the boundary is only as strong as the module system — a builder who
  merges the modules or passes `VaryState` "for logging" reopens the hole; the compile
  gate is load-bearing, review it like a lock.

## 6. Next build step
Implement the two-module split with the compile-time import gate and the read-watch,
then run the 200×8 differential suite against the current memory curriculum; the single
most informative outcome is the first nonzero read-watch hit or the first op divergence,
because it names the exact channel the firewall must close.
