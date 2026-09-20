# Slice 19 — Mapping human output variation to state variables (Track 1)

## 1. Slice
Track 1, slice 19: catalog concrete human output-variation phenomena, map each to a
prereg-enumerated state variable (salience, budget, load, memory contents), and report
the unmapped remainder plainly — cases that are out of scope for Arm C or that falsify
the "humans vary via state, not dice" premise for those cases.

## 2. Falsifiable claim
For each of 7 common human output-variation classes, the class taken when a subject
re-expresses identical content is predicted by the **pre-output logged state**
(salience vector, budget, load, memory contents) at >60% class-conditional accuracy in
a forced-choice replication corpus (N=50 cases, state logged before each output). A
variation class whose distribution is invariant under ablation of all four variables
(χ² association p > 0.05) is declared **unmapped**. The premise survives iff at most
one of the 7 classes is unmapped and the unmapped case carries a dated
in-scope/out-of-scope ruling.

## 3. Design
Mapped phenomena → state variables. All reads are of state logged BEFORE the output
is produced; the router is a deterministic function of that state (slice 25, K5
arbitrariness bar: every variant pair must name its selecting variable).

- **Rephrasing the same point** (paraphrase, synonym choice, sentence shape) →
  memory contents: recent-expression history (avoid-repetition rule) + primed
  lexical frames; salience: the currently most-active frame wins. Repeating wording
  you just used is not "free choice" — it is history suppressing a frame.
- **Reordering points** (conclusion-first vs buildup) → salience: emission order =
  descending salience; salience ties fall back to ledger (insertion) order.
- **Emphasizing differently** (stress, hedged vs asserted) → salience: assert/hedge
  activation thresholds; load: under high load the hedging markers are the first
  things dropped.
- **Elaborating more/less** (explanation depth) → budget: depth = f(turn/time
  budget); load caps depth even when budget nominally allows it (fatigue is not
  just a low budget — the budget says "go", the load says "short version").
- **Choosing different examples** for the same point → memory contents:
  content-matched retrieval proposes candidates; salience picks the most active;
  expression history suppresses the example used last time.
- **Dropping/adding caveats under time pressure or fatigue** → budget (pressure)
  and load (fatigue) gate the elaboration and caveat stages independently — the
  two are distinguishable because a fresh-but-rushed human drops structure while
  a rested-but-tired human drops polish.
- **Performative variation** (trying a sharper tone to see how it lands — humans
  sometimes vary output to *change* their own state) → memory contents, via the
  closed loop: every output appends to expression history, so today's variation
  becomes tomorrow's logged state. output = f(input, full state), and the state
  lawfully evolves through its own outputs.

Zag-flavored router (deterministic; no RNG; slice-16 buckets S_mem/S_ctrl/S_hist
are the concrete storage of these four variables):

```
fn express(claim: Claim, st: *State) -> []u8 {
  // st logged pre-output: st.salience[], st.budget, st.load, st.mem, st.expr_hist
  let pts: []Point = claim.points_sorted_by_salience(st.salience); // reorder
  let depth: i32 = depth_from(st.budget, st.load);                 // elaborate
  let frames: []Frame = select_frames(pts, st.salience, st.mem, st.expr_hist); // rephrase
  st.expr_hist = st.expr_hist.push(frames);  // deliberate, audited memory write
  return render(pts[..depth], frames, st.salience);
}
```

## 4. Kill bar
1. Corpus: 50 documented same-content re-expression cases with the four variables
   logged before each output (salience proxies, budget, load, memory/expression-history).
2. Per class, ablate each variable in turn and re-simulate the router; a class is
   **unmapped** iff its distribution is invariant under ablation of ALL four
   (χ² p > 0.05 for every variable).
3. **KILL (premise):** ≥2 of the 7 classes unmapped → the mapping is killed;
   freeze and either amend the prereg with new state variables or hand the
   remainder to t4-curricula as an open gap.
4. **KILL (flagship):** rephrasing shows no association with memory contents
   (expression history) at p < 0.05 → the avoid-repetition loop is decorative and
   the single most human-recognizable variation class is unexplained.
5. **KILL (scope):** any MAY-vary output (expression/phrasing/path/ordering/
   elaboration) changes a MUST-NOT-vary artifact (verdict, memory decision,
   integrity refusal, ledger content) in any run → the router is mis-scoped;
   concept kill, mirroring slice 25's K2–K4.

## 5. Honesty notes
- The mapping is **unfalsifiable by construction unless state is logged before
  output and the prediction is tested by ablation**. Retro-attributing any
  observed variation to "salience must have differed" is motivated reasoning.
  The design's only honest reading is predictive, not explanatory.
- Neuroscience does not support the premise as a claim about humans: synaptic and
  sensory noise genuinely contributes to behavioral variation. "Humans vary via
  state, not dice" is an **engineering idealization**, not a fact. Arm C does not
  need humans to be deterministic — it needs TNN's logged state space rich enough
  that every target variation class is reachable as a lawful function.
- The "salience" here is a computed activation level, NOT the retired felt-intensity
  machinery (retired 2026-09-20) — do not let it smuggle the dead mechanism back in.
- **Unmapped remainder, reported plainly:**
  (a) **Mood/affect:** a global optimistic-vs-terse tone shift across a whole
  session maps to no listed variable — it is not load, not budget, not the
  salience of one item, not memory contents. A "global salience offset" would
  just be a fifth variable in disguise. Candidate for a prereg amendment or an
  explicit out-of-scope ruling.
  (b) **Paraphrase-without-cause:** humans sometimes reword with no detectable
  state change and no repetition-avoidance motive — pure aesthetic drift. If the
  flagship kill bar (4) fails, paraphrase joins this remainder and the premise
  takes its first real hit.
  (c) **Audience-model shifts for strangers:** whom the human addresses changes
  phrasing, but with a new interlocutor there is no stored interlocutor model in
  memory contents — the variation is driven by a social role stance, not a logged
  variable. (Known interlocutors are covered: phase 4 differentiation puts the
  model in memory contents.)
  (d) **Production noise:** slips of the tongue, typos, speech errors — output
  channel noise, not deliberate variation. Plausibly out of scope for Arm C:
  it is a defect class, not variation to preserve.
- I am NOT claiming the 7 classes are exhaustive or that human salience is measurable
  twice the same way — only that the router is a deterministic function of logged state.

## 6. Next build step
Build the minimal Zag router from §3 (salience-sorted ordering + budget/load-gated
depth + expression-history-driven paraphrase) against a 50-case human re-expression
corpus with pre-output state logging, then run the four-variable ablation. Single
most informative test: does expression history (memory contents) predict paraphrase
choice above chance — if yes, avoid-repetition is the load-bearing state variable
of the whole mapping; if no, the flagship class joins the unmapped remainder and
the premise fails its first honest test.
