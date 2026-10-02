# TNN-2 Freeze Interpretation Templates

**DRAFT - AWAITING ACTUAL SCORE.** This document contains no score. It contains interpretation templates for each possible outcome, grounded in the committed red-team findings. When the reconciled freeze commit lands, select the matching template. Do not quote the evaluator's inconsistent on-disk draft.

Date: 2026-10-01. Drafter session: 0d9ec9c1-8d17-4f1b-b941-3bb0696bec95.

## 0. Standing interpretation rules (apply to every scenario)

These rules are not scenario dependent. They come from Micah's explicit rulings and the committed analyses.

**Rule 1: FW1-FW9 are a regression battery, not a generality test.** Micah ruled that because TNN-2 was designed after seeing TNN-1's failures, the FW battery measures targeted repair, not broad generality. Any FW score, including 9/9, is evidence about whether the three diagnosed gaps were addressed within the known envelope. It is not evidence of L3 or of performance in genuinely new worlds.

**Rule 2: No FW score establishes C0-D.** The C0-D structural analysis (`8bfb80fdd`) verified from source that promoted graphs are never executed at query time. `promote_graph` (line 541) calls `ev_teach_in`, inserting an exact-match tag-1 fact that shadows the MAP. `ev_query` answers via `activate`, which filters tag 1 only. The next query on the same (s, r) is always an exact hit and never reaches the trial loop. A promoted graph executes exactly twice in its life: verification inside `t2_trial` and possible re-verification inside `t2_revise_graph`. Never to answer a query. The analysis concludes: "No FW1-FW9 score, even 9/9, can establish C0-D for construction, since the output is causally inert at query time regardless of score." Additionally, the graphs are value traces, not portable procedures: literals are embedded at assembly, the traversed relation lives only in DEP provenance, and the 4-op ISA has no relational-dereference operation. A chain graph built for one subject fails closed on a new subject (transfer probe P2 returned -999999).

**Rule 3: The red teams bound every interpretation.** All three mechanisms received ATTACK-SUCCESS. Construction is L2 (finite researcher-authored family, oracle verifier). Inquiry is a miss flag with a constant action (L3 hardcoded as action 30 / content -999 at lines 805-808; L6 absent, uncertainty never resolved). Revision is L1 (single-schema literal-patch; the learner chooses the cell and literal, the researcher chose the repair topology). The synthesis (`42b4dfa91`) names the shared cause: "enumerated-schema / filled-slot." The learner chose the operands, never the topology. TNN-2 moved the content of cognition into learner state but left the form in source code. The alternative-explanation attack (`ccee9e5e6`) gives the unified hypothesis: form from researcher, content from learner; TNN-2 is answer-fed, not answer-derived; the learner's degrees of freedom compress to indices and literals. The DOF map (`d2af26581`) found zero pure learner decisions in the cognition path: 0 learner, 5 mixed, ~240 researcher. The interaction analysis (`9009ff259`) found no closed feedback loops and no unsupervised learning loop at all.

**Rule 4: The honest summary line.** From the synthesis: "capability improved within the researcher-enumerated envelope; the envelope is unchanged in kind." Any score above 4/9 is a legitimate capability result on sealed worlds, valid for causal comparison against TNN-1. It measures capability within the envelope, not generality beyond it.

**Rule 5: The next test is the GW battery.** The post-freeze adversarial battery (GW1-GW8), authored after the freeze by an independent adversary, is the generality test. No freeze interpretation is complete without stating that the GW results are pending and that they, not the FW score, discriminate L3.

---

## Scenario 1: FW = 4/9 (same as TNN-1)

**Honest headline:** TNN-2 repaired none of TNN-1's diagnosed failures on the sealed regression battery; the three nominal mechanisms did not convert to capability on known worlds.

**What the score measures:** On the nine worlds TNN-2 was explicitly designed to address, it performs identically to the system it was built to surpass. The targeted repairs did not land as capability even within the researcher-enumerated envelope.

**What it does NOT measure:** It does not measure whether TNN-2 is worse than TNN-1 in any general sense. The FW battery is nine specific worlds. A 4/9 could mask real architectural advances that these worlds do not reward (for example, persistent provenance and genuine rejection traces are real structural learning even when they do not change a world score). It also does not measure generality; that was never the FW battery's job.

**Red-team findings that bound interpretation:** The construction red team found the trial loop searches exactly three researcher-authored linear families with the verifier receiving the expected answer from the environment. If the FW worlds that TNN-1 failed require structures outside those families (deeper chains beyond depth 4, branching, non-linear composition), TNN-2 cannot pass them by construction, and the 4/9 is predicted rather than surprising. The inquiry red team found the guide action is constant 30 regardless of uncertainty; any FW world requiring discriminating inquiry cannot be passed by a constant. The revision red team found a single repair topology; any FW world requiring a structurally different repair cannot be passed.

**What the next test should be:** The GW battery remains the generality test, but a 4/9 on the regression battery lowers the prior on GW performance. Before running GW, the per-world failure analysis should check whether each FW failure maps to a known red-team limitation (unrepresentable structure, constant inquiry, single-schema repair). If all failures map cleanly, the GW battery is expected to fail in the same clustered ways, and the value of running it is confirmation of the clustering rather than discovery. Run it anyway: the clustering prediction itself needs sealed confirmation.

---

## Scenario 2: FW = 5/9 through 8/9 (improvement over TNN-1)

**Honest headline:** TNN-2 repaired some of TNN-1's diagnosed failures; capability improved within the researcher-enumerated envelope, and the envelope is unchanged in kind.

**What the score measures:** A genuine capability gain on sealed worlds, valid for causal comparison against TNN-1's 4/9. The worlds that flipped from fail to pass are worlds where the nominal mechanisms (runtime graph construction, miss-triggered inquiry linkage, topology-changing revision) were sufficient. Each flipped world should be named, and the mechanism credited should be the one whose kill bar that world exercises. This is legitimate evidence that the TNN-1 root-cause diagnosis was correct and that the TNN-2 repairs addressed it where the envelope permitted.

**What it does NOT measure:** Generality, L3, or C0-D. Per Rule 1, the FW battery is a regression battery: TNN-2 was designed after seeing these failure modes. An improvement to 7/9 shows the repairs work on known-shaped problems. It does not show the learner can handle shapes the researcher did not enumerate. Per Rule 2, no score establishes reuse: the promoted graphs that produced the flipped worlds are causally inert at query time (shadowed by memoized facts, value-bound traces). The capability gain is real, and it is L2.

**Red-team findings that bound interpretation:** The specific worlds that flipped must be checked against the red-team limitations. The synthesis predicts the flipped worlds are exactly those whose required structures fall inside the three linear families, whose inquiry needs are satisfiable by a constant action, and whose repairs match the single tombstone/insert-literal/rewire topology. Any flipped world that appears to require more than this deserves close scrutiny: either the red-team analysis missed a capability (possible; the red teams were source audits, and behavior can surprise source reading), or the world's scoring does not actually exercise what it appears to exercise (for example, a world scored as "revision" that is passable by retrieval of a revised fact rather than by structural repair). The per-world analysis must distinguish these.

**What the next test should be:** The GW battery, with the specific prediction that worlds requiring structures outside the enumerated families, discriminating inquiry, or non-single-schema repairs will fail. The FW improvement sets up a sharp GW test: if GW worlds inside the envelope pass and worlds outside it fail, the "envelope unchanged in kind" hypothesis is confirmed by the system's own behavior. The most informative GW worlds are the near-miss variants: structures one step outside each family boundary (5-hop chains, branching graphs, relational rather than value-bound procedures).

---

## Scenario 3: FW = 9/9 (perfect on the regression battery)

**Honest headline:** TNN-2 passes every world it was designed to pass; this is a complete targeted-repair success and zero evidence of L3.

**What the score measures:** That the three diagnosed TNN-1 gaps are fully addressed within the known envelope. Every failure mode the researchers identified has a working repair on sealed data. This is the strongest possible regression result and it validates the diagnosis-to-repair pipeline as a methodology.

**What it does NOT measure:** Everything the red teams found. A 9/9 is fully compatible with every ATTACK-SUCCESS verdict, and the interpretation must say so explicitly:

- Construction 9/9 is compatible with a finite researcher-authored family searched in a fixed order against an environment-supplied answer. The construction red team (`340e94e3e`) found exactly this: three linear assemblers, hard bounds (depth 4, 96 paths, 12 values), the sum branch dead in production, DEC never emitted, and the verifier accepting the first candidate matching the QUERY event's `expected`. A 9/9 means the nine worlds' answers were all reachable within this family. It does not mean the learner can construct structures outside it.
- Inquiry 9/9 is compatible with a constant action. The inquiry red team (`4e329c772`) found guide action 30 and content -999 are researcher constants at lines 805-808, with no production path that resolves uncertainty or supersedes stale guides. A 9/9 means no world required the guide to vary with the uncertainty, required uncertainty resolution, or punished stale guides. It does not mean the system performs discriminating inquiry.
- Revision 9/9 is compatible with a single repair schema. The revision red team (`687ba0219`) found exactly one topology (find BRANCHEQ-guarded SETREG, tombstone, insert observed-literal SETREG, rewire), with `t2_trial` never invoked on the revision path and corrected content memorized from the observed value. A 9/9 means all nine worlds' repairs matched this schema. It does not mean the learner can perform structurally different repairs.

**Why 9/9 does not establish L3:** L3 requires the learner to invent or recruit representations the researcher did not enumerate as the solution space (C0-B), to do so across multiple unforeseen forms (C0-C), with semantics in learner-created state (C0-A) and demonstrated cognitive reuse (C0-D). The red teams show C0-A fails (procedures are source code; the H3 probe `94cecdba4` confirmed no policy write path exists in production), C0-B fails (three fixed assemblers; fixed 2-node guide schema; single repair topology), C0-C fails (no sealed world in FW1-FW9 was authored to require an unforeseen form; the battery predates the freeze), and C0-D fails structurally (Rule 2). A 9/9 changes none of these findings because none of these findings is about the score. They are about the source.

**What the next test should be:** The GW battery is now the entire game. A 9/9 on FW plus the red-team verdicts makes a crisp, falsifiable prediction: GW worlds that stay inside the enumerated envelope will pass, and GW worlds that step outside it will fail in the clustered ways the synthesis names. If a GW world outside the envelope passes, that is the most important result of the cycle: it would be evidence against the synthesis, and the red-team findings would need revision. The interpretation of a 9/9 must therefore be written as a bet on the GW outcome, not as a victory statement.

---

## Scenario 4: W score diverges from FW score

The W battery (W1-W9) is the supplementary old-world battery. TNN-1 scored 4/9 on W (passing W1, W2, W4, W5). The W score measures retention and non-regression on the worlds the previous generation handled, plus any transfer the new mechanisms provide.

**If W < 4/9 (regression):** Honest headline: TNN-2 lost capability TNN-1 had; the new mechanisms interfere with or displace old competence. What it measures: a genuine regression tax. The per-world analysis must identify which previously passing worlds now fail and trace the causal path (for example, a promoted graph shadowing a fact that the old retrieval path would have answered correctly, or a revision corrupting a previously stable structure). What it does not measure: it does not erase the FW gains, but it changes their price. A system that gains 3 FW worlds and loses 2 W worlds has not unambiguously improved. The next test is a retention-focused analysis: do the W failures share a cause (interference from the new machinery), and would that cause also threaten GW performance? The interaction analysis (`9009ff259`) found no closed feedback loops and write-only accumulation of guides and uncertainties; unbounded accumulation is a candidate mechanism for slow interference-driven regression.

**If W = 4/9 (same):** Honest headline: TNN-2 retained TNN-1's old-world capability while changing the FW score by whatever it changed. What it measures: no regression tax on the old battery. The new machinery did not displace the old competence. This is the expected outcome if the new mechanisms are strictly additive (new code paths that trigger only on miss). What it does not measure: transfer. Identical W performance is retention, not reuse. C0-D requires the invented structures to improve performance somewhere; holding W flat while FW moves is consistent with the structures being causally inert (Rule 2).

**If W > 4/9 (improvement):** Honest headline: TNN-2 improved on old worlds it was not specifically designed to address; this is the most interesting W outcome. What it measures: possible transfer or positive side effects of the new mechanisms. Each newly passing W world must be analyzed for the causal path: did a promoted graph, a guide, or a revision actually contribute, or did the world become passable through an incidental change (for example, a larger workspace, a changed eviction order, or a fact taught as a side effect of promotion)? The C0-D analysis requires white-box evidence that a MAP was read during the query; in the frozen build, no production path outside revision reads MAPs, so a transfer claim needs extraordinary evidence. What it does not measure: it does not by itself establish C0-D, but it is the outcome most worth investigating for C0-D-shaped evidence. The next test is a targeted ablation: remove the promoted graphs (or the guides, or the revisions) and check whether the W gain disappears. If the gain survives ablation of the new structures, it was incidental. If it disappears, there is a genuine reuse path the source audit missed, and the C0-D analysis needs updating.

---

## 5. The C0-D caveat (standalone statement)

For use whenever any freeze score is reported, in any scenario:

"No score on FW1-FW9 or W1-W9 establishes cognitive reuse (C0-D) for TNN-2's constructed graphs. Structural analysis of the frozen build (`8bfb80fdd`) verified that every promoted graph is shadowed at promotion time by an exact-match fact (`promote_graph` line 541 calls `ev_teach_in`), that the query path (`ev_query` via `activate`) can only read tag-1 facts and structurally excludes tag-20 MAP nodes, and that the graphs themselves are value traces bound to their original subjects (literals embedded at assembly; the 4-op ISA has no relational dereference; cross-subject execution fails closed). The promoted graphs are therefore causally inert at query time regardless of the score. Demonstrating C0-D requires a battery in which a constructed structure is executed to answer a later query on new inputs, with white-box evidence that the MAP was read during that query. The GW battery should include such worlds; the FW and W batteries do not."

---

## 6. Scorecard template (fill when the reconciled commit lands)

- FW score: ___/9. Passing worlds: ___. Failing worlds: ___.
- W score: ___/9. Passing worlds: ___. Failing worlds: ___.
- Determinism: three byte-identical runs confirmed (yes/no).
- Frozen hashes re-verified post-eval (yes/no): TNN-2 source `a29972ca...`, binary `6044f91f...`, shim source `33795c19...`, shim binary `9217054c...`.
- Seal integrity: verified `0c97a669a` (16 files, hashes match, no contamination).
- Comparison vs TNN-1: FW 4/9 (FW1, FW2, FW4, FW5); W 4/9 (W1, W2, W4, W5).
- Template selected: Scenario ___.
- Per-world mechanism attribution: for each flipped world, name the mechanism and check it against the red-team bounds.
- GW prediction recorded: ___.

## 7. What the next test must be

The post-freeze adversarial battery (GW1-GW8), authored after the TNN-2 freeze by an independent adversary who saw the public architecture claims but not the builder fixtures. Requirements from the TNN-3 prerequisites analysis (`f795807cc`): worlds must not be trivial FW variants; must attack unfamiliar graph structures, deeper or different composition, structurally different revisions, successive revision and reversion, ambiguous repairs, state-dependent informative actions, locally attractive wrong questions, cross-domain reuse, interference and memory pressure, and abstractions not anticipated by the arithmetic examples. Must not require new ISA opcodes. TNN-2 remains untouched. Worlds sealed before evaluation.

The GW battery is the test that discriminates the synthesis hypothesis ("capability improved within the researcher-enumerated envelope; the envelope is unchanged in kind"). The FW interpretation in every scenario above is written as a prediction about GW. If GW confirms the prediction, the red-team clustering stands and TNN-3 design proceeds from H1/H2/H3. If GW disconfirms it (an outside-envelope world passes), the most valuable outcome of the cycle has occurred: the synthesis is wrong in an interesting way, and the analysis must be redone from the passing world outward.

---

*End of draft. No score is recorded here. No score is predicted here. Select the matching scenario template when the reconciled freeze commit lands.*
