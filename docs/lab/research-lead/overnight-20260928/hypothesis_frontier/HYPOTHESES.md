# Live Hypothesis Frontier

Worker: Hypothesis Generator. Constitution Section 20.
Date: 2026-10-01. Branch: tnn-native-lab. Local only, nothing pushed.

## Frontier status

18 live hypotheses. Sources: the 10-priority wave results (C181-C188, C189 pending), the governance wave-2 gaps, and the TNN Autonomous Research Constitution (2026-10-01).

### Completed-wave results feeding this frontier

- C181 learner-verification: reliability replaces expected for revision (V4 PASS); honest withholding (V1/V3a); cannot bootstrap cross-subject acceptance without generalization. V2 invalid, V3b unclear.
- C182 adaptive-threshold: T adapts to experienced noise (partial yes to "when enough evidence"). The how-to-adapt stays researcher-owned.
- C183 provenance-learning: source reliability from consequences; ranking reverses A to B. Disagreement rule still researcher-set.
- C184 mini-lifetime: 3 arms, no resets; transfer preserved in integration; withholding only in Arm C; no regressions.
- C185 substrate-expansion: one substrate drives 5 behaviors; per-behavior ablations all PASS; shared fields proven.
- C186 persistent-connections: rebind writes LINK edges; C exploits at 11x speedup; ablation causal. Link-priority rule researcher-authored.
- C187 utility-integration: Test 6 complete (U not redundant); predictive utility kills wrong-but-frequent.
- C188 rebind-hardening: 4 worlds graceful; scale cost real (21 vs 4 verifies at 15 MAPs); 100-MAP infeasible; no adaptation.
- C189 protect-how: 3-tier eviction saves generative structure (8/8 cells vs 0/8). Policy researcher-authored.

### Persistent gaps (standing)

1. Learner fills slots and creates simple structures, but does not create new slots, fields, or mechanisms.
2. Scale: O(n) rebind scan plus 1024-node workspace makes 100-MAP fixtures infeasible.
3. Update rules, disagreement rules, priority rules, eviction tiers, threshold formulas: all researcher-owned.
4. Threshold=3 replaced by adaptive T, but the adaptation rule itself is researcher-set.

---

## P0: Critical bottlenecks

### H-SCALE-1: What blocks 100 MAPs, scan cost or allocation pressure?

Question: Is the rebind-hardening 100-MAP infeasibility caused by O(n) scan cost, by 1024-node workspace allocation/eviction pressure during fixture construction, or by their interaction?

Why it matters: C188 documents scale cost (21 vs 4 verifies at 15 MAPs) and calls 100-MAP infeasible as a harness limitation. If the blocker is fixture construction (allocation pressure), the mechanism may scale fine in a larger workspace and the fix is infrastructure (Constitution 17). If the blocker is scan cost, the mechanism itself needs sublinear indexing. These demand completely different next builds. Information gain is maximal because it decides between two architectures.

Experiment: Build the 100-MAP fixture incrementally in a workspace enlarged only for construction (then measured at standard size), timing fixture build vs query scan separately. Compare: (a) construction time per MAP as n grows, (b) per-query scan verifies as n grows with distractors matched/mismatched.

Falsifier: If per-query scan verifies grow sublinearly with n while construction alone stalls, the blocker is infrastructure, not the rebind mechanism. If scan verifies grow linearly with n and construction is flat, the blocker is the scan. If both grow, the interaction hypothesis wins.

Priority: P0.

### H-VER-1: Can learner-owned verification drive withholding, not just revision?

Question: C181 showed reliability replacing expected for revision acceptance (V4 PASS) and honest withholding when no predictor exists (V1/V3a). Can the learner withhold based on low predicted reliability without a researcher-set threshold, and does that withholding improve later accuracy per unit compute?

Why it matters: Micah Priority 1 named four tasks: acceptance, rejection, withholding, revision. Only revision is demonstrated. H2-v2 showed frozen TNN-2 cannot withhold without expected. If learner-owned withholding works, expected-answer verification is replaceable across all four tasks, which removes the last researcher crutch in the verification path.

Experiment: Two-arm lifetime: treatment withholds when predictor reliability falls below a learner-maintained confidence bound (updated from prediction errors); control uses fixed threshold from C181. Worlds: (a) stable, (b) noisy, (c) deceptive candidates. Measure: withhold rate, false accepts, false rejects, verifies per correct answer.

Falsifier: If the learner-maintained bound collapses to a fixed value equivalent to the researcher threshold across all worlds, the "learner-owned" claim is vacuous. If treatment withholds on problems the control solves (excess false withholds > 2x), the mechanism is worse than the crutch.

Priority: P0.

### H-ADAPT-1: Can TNN adapt MAPs beyond exact plen matching?

Question: C188 showed plen matching is all-or-nothing: partial applicability and extend/truncate correctly fall back to trial but never adapt. Can the learner construct an adapted variant (prefix reuse, extension, truncation) cheaper than fresh trial, or is exact-shape rebinding the ceiling of the current mechanism?

Why it matters: Micah Priority 3 explicitly demands "adaptation rather than exact reuse." All graceful fallbacks so far mean the reuse machinery contributes nothing when shapes differ. If adaptation is impossible without new machinery, that defines the next construction target (Constitution 9: invention when existing structure is inadequate).

Experiment: Worlds where B needs plen-5 but A holds plen-4 (extend by one) and plen-6 (truncate by one), with the missing/extra step inferable from B's own data. Treatment: attempt adaptation via prefix extraction plus one trial step. Control: fresh trial. Measure verifies and whether the adapted MAP is promoted and later reused.

Falsifier: If adapted MAPs verify correctly but cost more than fresh trial (no savings), adaptation exists but is useless. If no adapted MAP ever verifies across 3/3 runs in three distinct shape-mismatch families, exact-shape rebinding is the mechanism ceiling.

Priority: P0.

### H-INDEX-1: Can the consequence substrate support sublinear retrieval?

Question: Can an index structure (keyed by plen, by endpoint literal, or by learned LINK topology from C186) be built on the shared substrate so that rebind candidate retrieval grows sublinearly in the number of MAPs, replacing the current O(n) id-order scan?

Why it matters: Constitution 17 requires sublinear indexing; H-SCALE-1 will show whether scan cost is the binding constraint. C185 proved one substrate can drive five behaviors; a sixth consumer (retrieval indexing) would be the strongest One-System test yet. C186's LINK edges are a natural index substrate: newest-first linked MAPs already form a priority structure.

Experiment: Build treatment with a plen-keyed candidate shortlist plus LINK-edge priority (C186), control with id-order scan. Scale MAPs 10/20/40 (within workspace limits). Measure verifies per query vs n. Ablation: remove the index, keep LINK edges; remove LINK edges, keep plen key.

Falsifier: If verifies per query grow linearly in both arms (index provides no scaling benefit), sublinear retrieval needs a different architecture. If the index arm is slower at small n and only wins at large n, record the crossover point; if crossover exceeds feasible workspace size, the win is theoretical only.

Priority: P0.

### H-INTEG-1: Does reliability plus substrate plus verification beat expected-answer verification in a noisy multi-source lifetime?

Question: Combine C181 (learner verification), C183 (source reliability), C185 (substrate): does a treatment where source reliability scores feed the substrate, which gates verification candidates, outperform expected-answer verification on accuracy per verify in a lifetime with degrading sources, deceptive candidates, and interference?

Why it matters: Governance wave-2 named this the top integration gap. Each mechanism works in isolation; the constitution (Section 12) demands consequence re-entry across behaviors from one substrate. If the integrated treatment beats both the frozen baseline and each mechanism alone, that is the first demonstration of compounding learner-owned machinery. If it does not, the mechanisms interfere and integration needs redesign.

Experiment: Three arms over a 500+ event lifetime with source degradation mid-run: (a) frozen TNN-2, (b) expected-answer verification, (c) integrated (reliability-gated substrate verification). Measure: accuracy, verifies per correct answer, false accepts, source-switch latency after degradation.

Falsifier: If arm (c) matches arm (b) on accuracy but costs more verifies, integration adds complexity without benefit. If arm (c) is worse than arm (b) on any metric, the mechanisms interfere and the integration hypothesis is rejected pending redesign.

Priority: P0.

---

## P1: High information gain

### H-PREDOPT-1: Can the learner choose not to predict?

Question: Constitution Sections 1 and 13 require prediction-optional cognition. In tasks where retrieval or deduction suffices (known fact lookup, logically implied conclusions), does the current prediction-before-outcome machinery waste compute, and can the learner select the cheaper cognitive process based on its own state?

Why it matters: C181 wired prediction into verification everywhere. If prediction is scored even when the answer is already known, the architecture reproduces the "predict everything" limitation the constitution explicitly forbids. Demonstrating process selection (retrieve vs deduce vs predict) is a prerequisite for the north star's "chooses appropriate cognitive operations."

Experiment: Worlds with (a) directly known facts, (b) logically implied facts (chain deduction), (c) genuinely uncertain outcomes. Instrument: does the learner invoke prediction machinery in (a) and (b)? Treatment: a confidence/knowledge check gates prediction (skip when a verified fact or valid deduction exists). Measure verifies and compute per correct answer in both arms.

Falsifier: If the gated treatment saves no compute (prediction was already cheap or rarely invoked), prediction-optional is a non-problem in this architecture. If gating breaks accuracy in (c), the knowledge check is unreliable and process selection needs better state signals.

Priority: P1.

### H-COMP-1: Do separately learned capabilities compose without paired examples?

Question: Constitution Section 8: if TNN separately learns capability X and capability Y, can it solve a task requiring X+Y with no paired training examples, no task-specific handler, and no explicit "combine" hint?

Why it matters: This is the compositionality test the constitution calls "a key measure of genuine understanding." Rebinding (C188) reuses one structure; composition requires two independent structures to cooperate on a novel goal. No current result tests this. A pass would be the strongest generality evidence to date; a clean fail defines the construction grammar's composition ceiling.

Experiment: Teach procedure family X (e.g., chain traversal) and fact family Y (e.g., guarded lookup) in separate phases with interference between. Then pose Z requiring X's traversal over Y's guarded facts. No Z examples. Measure: solved without trial-from-scratch, verifies vs fresh control, whether the solution references both X and Y structures (white-box check).

Falsifier: If the treatment always falls back to full trial (cost equals fresh control), composition does not occur and the two capabilities are isolated silos. If it solves Z only when X and Y share surface form (ids, literals), the result is pattern matching, not composition.

Priority: P1.

### H-L2L-1: Does examples-to-criterion decrease with lifetime experience?

Question: Constitution Section 16: does the integrated learner (Arm C from C184, or H-INTEG-1's arm c) require fewer examples or less search to reach criterion on later unfamiliar problems than the frozen baseline, with causal ablation proving prior learning produced the improvement?

Why it matters: "The older TNN becomes, the better it should become at learning" is the constitution's learning-to-learn target. Current transfer results (C184, C186) show cheaper retrieval, not faster learning of genuinely new structure. This is the difference between a cache and a improving learner.

Experiment: Lifetime with 4 sequential novel problem families. Measure examples-to-criterion (trials to first verified MAP) per family for: (a) frozen, (b) integrated learner with full history, (c) integrated learner with history ablated (connections/records deleted between families). The (b) vs (c) gap is the causal learning-to-learn effect.

Falsifier: If (b) matches (c), history provides no learning speedup and all transfer is retrieval, not improved learning. If (b) beats (a) but matches (c), the gain is architecture, not experience.

Priority: P1.

### H-PERSIST-1: Do A-B links survive 1000+ event lifetimes and get exploited spontaneously?

Question: C186 built persistent A-B links and showed C exploits them at 11x speedup, but at small scale with the exploitation phase scripted. In a 1000+ event lifetime with heavy interference, do the LINK edges survive eviction, and does a later problem spontaneously retrieve them without a scripted exploitation phase?

Why it matters: Governance named P2-deep (1000+ events, spontaneous formation) a top gap. The constitution's north star requires old information to become useful months later via learner-reconnected structure. If LINK edges are evicted under pressure or never spontaneously retrieved, persistent connections are a lab artifact.

Experiment: Lifetime: A learned, B rebinds (LINK written), 1000 interference events, then C presented with no retrieval hint. Measure: LINK edge survival count, whether C's solution path traverses LINK edges (white-box), verifies for C vs fresh control. Ablation: delete LINK edges before C.

Falsifier: If zero LINK edges survive 1000 events, the protection story (C189) must extend to connection edges or the mechanism is not lifetime-viable. If edges survive but C never traverses them spontaneously, retrieval is the bottleneck, not persistence.

Priority: P1.

### H-SUB6-1: Can the substrate drive revision strategy as a sixth behavior?

Question: C185 drove five behaviors from one substrate. Can revision strategy selection (which revision operator to try first: supersede, refine, split, abandon) be driven by the same STRATEGY/PURSUIT records, with an ablation showing the shared records causally matter?

Why it matters: Constitution Section 12 lists revision strategy as a target consequence consumer. Six behaviors from one substrate strengthens the One-System claim; failure bounds it at five and suggests revision needs private machinery.

Experiment: Worlds requiring different revision operators (contradiction vs refinement vs obsolescence). Treatment: revision operator order ranked by substrate success history. Control/ablation: fixed operator order with substrate reads gated off. Measure: trials to successful revision per world type.

Falsifier: If the ablation arm matches the full arm, substrate records do not inform revision and the behavior is not substrate-driven. If the treatment helps in one world type only, revision strategy is partially substrate-driven and the boundary needs mapping.

Priority: P1.

### H-UTILRET-1: Does predictive utility correctly order retention under 3-tier eviction?

Question: Combine C187 (predictive utility: U is prediction score) with C189 (3-tier eviction: derived answers first, generative last). Does predictive U correctly rank generative structures above stale-but-frequent cached answers inside the eviction tiers, and does the combination preserve both mechanisms' guarantees?

Why it matters: C189's tiers are researcher-authored categories; C187's U is learner-scored value. If U can drive tier assignment (high-U generative structures protected, low-U derived answers sacrificed first), the eviction policy moves toward learner-owned. If they conflict, integration needs a resolution rule.

Experiment: Lifetime with generative MAPs plus frequently-queried-but-stale cached answers. Arms: (a) C189 tiers alone, (b) C187 predictive U alone, (c) U-driven tier assignment. Measure: generative cell survival, stale answer reclamation rate, re-derivation cost in phase 5.

Falsifier: If arm (c) sacrifices generative structures that arm (a) preserves, U-driven tiers are unsafe and the researcher-authored categories are load-bearing. If (c) matches (a) on survival but costs more compute, the integration is correct but not yet cheaper.

Priority: P1.

### H-THRESH-1: Does the adaptive threshold need regime-change forgetting?

Question: C182's follow-up noted E decays slowly, so very old noise keeps T elevated until sustained stability arrives. Does adding a regime-change detector (reset or fast-decay E when the world demonstrably shifts) improve adaptation speed without hurting stability, and can the detector itself be learner-driven?

Why it matters: C182 gave a partial yes to "when enough evidence." Stale elevation is the known failure mode. If a learner-driven regime signal fixes it, the threshold mechanism becomes fully adaptive; if only a researcher-set schedule works, part of the mechanism stays researcher-owned permanently.

Experiment: Changing worlds with long stable phases punctuated by shifts (the C182 changing environment extended). Arms: (a) C182 as-is, (b) E fast-decay on detected shift (researcher-set detector), (c) shift detected from prediction-error bursts (learner-driven). Measure: trials to re-converge after shift, false resets during stable phases.

Falsifier: If (c) false-resets during stable noise (worse than (a)), learner-driven regime detection is unreliable and the concept needs better signals. If (b) beats (a) but (c) matches (a), the improvement is available but not learner-ownable with current machinery.

Priority: P1.

---

## P2: Medium priority, high upside

### H-FORMAL-1: Do formal errors become impossible after mastery?

Question: Constitution Section 7: once TNN has complete, actively used knowledge of a formal system (e.g., the chain grammar's syntax), do syntax-level errors become architecturally avoidable, or do they persist at the same rate?

Why it matters: This separates pattern familiarity from operational understanding. Current work never tests whether learned knowledge constrains generation. A pass is evidence of "true understanding having consequences"; a fail with complete knowledge present indicts the generation path.

Experiment: Teach the chain construction grammar to criterion (verified MAPs across families). Then require constructing novel chains under time/compute pressure. Measure: fraction of generated candidates that are syntactically invalid, before vs after mastery, vs a control that never reached criterion.

Falsifier: If invalid-candidate rate is unchanged after demonstrated mastery (criterion-tested knowledge present), generation does not consult learned formal knowledge and the understanding/consequences link is missing. If the rate drops only under no pressure, the constraint is compute-dependent.

Priority: P2.

### H-COMPRESS-1: Can the 5-behavior substrate lose 500 lines and keep all behaviors?

Question: Constitution Section 4: a version deleting 500 cognition lines while retaining capability beats one adding 2000 for a new battery. Can the C185 substrate (~250 new lines plus base) be compressed (fewer branches, unified record paths) while all five per-behavior ablations still PASS?

Why it matters: Architecture compression is a first-class metric. Current trajectory adds lines per behavior. A successful compression with retained ablations proves the behaviors share real structure rather than five adjacent implementations.

Experiment: Rewrite the substrate machinery minimizing lines (target: 30 percent reduction), keeping the tag-904 ablation bitmask protocol identical. Re-run all five B1-B5 batteries 3/3. All must PASS with identical verdicts.

Falsifier: If any battery flips to FAIL, the removed lines were load-bearing and the compression hypothesis is rejected for that cut; record which behavior broke to map the true sharing structure. If compression succeeds trivially (dead code only), the original was uncompressed, which is itself a finding about builder discipline.

Priority: P2.

### H-SLOT-1: Can the learner create a new record slot?

Question: The standing SUF gap: the learner fills researcher-defined slots and creates simple structures (LINK edges, MAP graphs) but never creates a new field, slot, or record type. Can a mechanism be built where the learner allocates a genuinely new slot (new tag or new field semantics) because its existing slots are inadequate, and then uses it?

Why it matters: This is the sharpest form of the "learner fills slot vs learner creates slot" gap. All current learner-owned values live in researcher-authored containers. A positive result moves SUF from values-and-links to schema, which is the largest remaining step toward L3-adjacent structural authority.

Experiment: Construct a world where existing substrate fields cannot represent the needed distinction (e.g., two independent reliability dimensions forced into one score field, causing demonstrable interference). Provide a generic ALLOC primitive (already in the protected ISA class). Test whether the learner allocates and consistently uses a new slot. Measure: interference resolved, new slot read/write consistency, reuse across problems.

Falsifier: If the learner never allocates despite measurable interference, slot creation is beyond current machinery and the gap is confirmed as architectural. If it allocates but never reads the slot, allocation without use is not slot creation.

Priority: P2.

### H-PROVUTIL-1: Should per-source reliability feed predictive utility?

Question: Merge C183 (per-source reliability) with C187 (predictive utility): when a structure's predictions are scored, should the update magnitude depend on the source reliability of the evidence behind the structure, so that predictions from degraded sources move U less?

Why it matters: Currently U updates (+1/-1) are source-blind and reliability scores live in a separate record family. The constitution (Section 6) wants source history plus outcomes to inform confidence. A merger tests whether the two learner-owned value systems compose or double-count.

Experiment: Worlds where a high-U structure's supporting source degrades. Arms: (a) C187 as-is, (b) reliability-weighted U updates. Measure: trials for U to demote the structure after source degradation, false demotions when the source is reliable but the world is noisy.

Falsifier: If (b) demotes slower than (a) with no accuracy benefit, weighting adds lag without value. If (b) false-demotes reliable-source structures during noise, the weighting confuses source reliability with world noise.

Priority: P2.

### H-NEGTR-1: Does the consequence substrate prevent negative transfer better than verification alone?

Question: C188's W4 (negative transfer) showed graceful fallback (reject misleading MAP, trial succeeds) but at a cost. Does substrate-driven search-order (C185 B5) or abandonment (B2b) reduce the cost of negative transfer by deprioritizing previously-harmful structures?

Why it matters: Negative transfer is the tax on all reuse machinery. If the consequence substrate learns "this helper hurt last time" and avoids it, reuse becomes safer with experience, which is a learning-to-learn effect specific to transfer.

Experiment: Worlds with a misleading structurally-similar MAP (C188 W4 family). Arms: (a) rebind alone, (b) rebind plus substrate search-order/abandonment with cross-problem memory. Measure: verifies wasted on the misleading MAP before correct solution, across repeated exposures (does the waste decrease?).

Falsifier: If the waste does not decrease across exposures in arm (b), the substrate does not learn transfer-specific avoidance. If arm (b) avoids the misleading MAP but also avoids the helpful one (over-general avoidance), the discrimination is too coarse.

Priority: P2.

### H-XDOMAIN-1: Can an arithmetic structure spontaneously help planning?

Question: Constitution Section 11 names the canonical cross-domain hope: an arithmetic structure later helping planning. Can a chain-counting or ordering structure learned in a numeric domain be retrieved and rebound for a planning-like sequencing problem with no shared surface form?

Why it matters: All demonstrated transfer (C184, C186, C188) is within the chain family. Cross-domain transfer with no shared surface is the stated north-star test ("connect old and new structures, reuse those connections spontaneously"). A clean negative result here bounds every transfer claim to date as same-family.

Experiment: Teach numeric ordering chains; much later, pose a sequencing problem with different literals, different relations, but isomorphic order structure. No hints. Measure: spontaneous retrieval (does the numeric MAP get rebound?), verifies vs fresh control, white-box check that the reused structure is the numeric one.

Falsifier: If retrieval never selects the numeric MAP across 3/3 runs in three isomorphic-but-surface-different families, cross-domain spontaneous reuse does not occur and the transfer story is family-bounded. If it works only with shared literals, the result is surface matching.

Priority: P2.

---

## Bottleneck clustering (Constitution 23)

Three failures share one architectural cause:

- H-SCALE-1 (100-MAP infeasible), H-INDEX-1 (linear scan), H-PERSIST-1 (LINK survival at scale), H-PREDOPT-1 (prediction invoked wastefully).

Shared cause hypothesis: the architecture has no cost-aware retrieval layer; every cognitive operation scans flat structures at full price. The general fix is not five patches but one: a learner-maintained, consequence-ranked retrieval substrate (H-INDEX-1) that process selection (H-PREDOPT-1), transfer (H-PERSIST-1), and scaling (H-SCALE-1) all consume. If H-INDEX-1 fails, the fallback cluster is: hierarchical memory, generative compression, and reconstructibility (Constitution 17), each needing its own hypothesis.

Treadmill warning: exact-plen rebinding has now accumulated graceful-fallback results across C188 (H3/H4), the rebind adversary (W6 order-dependence), and H-ADAPT-1's motivation. That is three adjacent "correct fallback" results. Per Section 23, freeze the fallback lineage: H-ADAPT-1 is the last fallback characterization; next work must be adaptation machinery or a structurally different retrieval approach, not another fallback world.

## Promotion log

Auto-promote rule (Constitution: "if undecided you must test and if it turns into no brainer auto promote"): no promotions this cycle. All 18 hypotheses require experiments before promotion. The only no-brainer carried forward is the standing one: keep the swarm at 10 workers with 7+ executable, which the parent already enforces.

## Next-wave worker mapping (suggested)

- 3 frontier builders: H-INDEX-1, H-VER-1, H-ADAPT-1.
- 2 adversaries: H-SCALE-1 (distinguish scan vs allocation), H-NEGTR-1.
- 2 integration: H-INTEG-1, H-UTILRET-1.
- 1 lifetime: H-L2L-1 or H-PERSIST-1.
- 1 hypothesis generator (this lane, continuous).
- 1 governance (ledger, SUF tracking).

Total: 10. Replacement order per Micah: BUILD, RUN, ABLATE, ADVERSARY, INTEGRATE, ANALYZE.

---

## Frontier status update: 2026-10-02 (Governance Wave 3)

### Tested since 2026-10-01

| Hypothesis | Status | Evidence |
|---|---|---|
| H-PREDOPT-1 | TESTED (partial) | C190: 86% prediction waste measured; state-driven selection works. Micah correction: 7-type taxonomy is researcher-authored; must remove labels next. |
| H-COMP-1 | TESTED (negative) | C191: clean negative; composition architecturally absent. A/B/C hypotheses NOT yet tested. |
| H-L2L-1 | TESTED (positive, bounded) | C192: 6x Family-2 cost reduction; ablation proves LINK strategy causal. Families structurally identical; cross-family still open. |
| H-INDEX-1 | TESTED (positive) | C193: 140x scan reduction at 100 MAPs; learner-maintained; verifies identical. Plen buckets risk becoming researcher taxonomy (Micah note). |
| H-INTEG-1 | TESTED (positive) | C194: integrated 3/3 vs 2/3 each alone; C183 private store deleted. First net-negative integration. |
| H-VER-1 | TESTED (positive, bounded) | C195: adaptive WT wins on regime change (111 vs 104); loses stationary. Reliability score does most work; threshold secondary. |
| H-PERSIST-1 | TESTED (positive, pending commit) | p2_lifetime REPORT: links survive 960 interference events; C and D cost 1 try vs 11 control; D links to B (node-id ordering). Ablation batch pending. Worker active, uncommitted. |
| H-FORMAL-1 | IN PROGRESS | formal_errors worker active (run outputs exist, no REPORT.md yet). |

### Still live (untested)

H-SCALE-1, H-ADAPT-1, H-SUB6-1, H-UTILRET-1, H-THRESH-1, H-COMPRESS-1, H-SLOT-1, H-PROVUTIL-1, H-NEGTR-1, H-XDOMAIN-1.

### New hypotheses from this wave

- **H-COMP-0 (P0):** C191 proves the trial/MAP divide blocks all composition. Before testing A/B/C, test whether ANY mechanism can make trial consume MAPs (not raw facts). If trial cannot be bridged to MAPs, composition needs a new execution path, not a better rebind. Falsifier: a MAP-consuming trial variant costs more than fresh trial with zero reuse.
- **H-PREDOPT-2 (P0):** Per Micah's correction, test unlabeled process selection: present goal/situation with no TYPE label; TNN must determine the cognitive operation sequence from its own state (knowledge, missing pieces, constraints, uncertainty, consequences). Falsifier: selection accuracy at chance without labels, or labels prove necessary.
- **H-SEQ-1 (P1):** Test multi-operation sequences (RECALL to DERIVE to VERIFY to ACT). Single-operation selection (C190) is insufficient for general intelligence. Falsifier: TNN cannot chain two different operations without researcher sequencing.
- **H-EMERGKEY-1 (P1):** Per Micah Section 6, test whether index keys can emerge from learned structure and access/consequence history rather than researcher plen buckets. Falsifier: emergent keys perform worse than plen buckets at all scales.
- **H-L2L-2 (P0):** Strong learning-to-learn per Micah Section 5: Family A (chains) to structurally different Family B (not just new literals). Ablation of learned meta-structure must remove the advantage. Falsifier: no transfer across structurally different families.

### Treadmill check (Constitution 23)

The exact-plen fallback lineage now has 4 adjacent "correct fallback" results (C188 H3/H4, C191 C1/C3 pattern). H-ADAPT-1 remains the last allowed characterization; next work on this lineage must be adaptation machinery or a different approach, not another fallback measurement.

No em dashes used (verified).

---

## Frontier status update: 2026-10-02 (Composition consolidation)

Canonical consolidation: `docs/lab/research-lead/overnight-20260928/composition_canonical/CONSOLIDATION.md`.
Verdict: COMPOSITION-CANONICAL-COMPLETE.

### Tested since the Wave 3 update

| Hypothesis | Status | Evidence |
|---|---|---|
| H-COMPGEN-1 | TESTED | H1 (typed contracts) + H2 (value composition) solve 4 domain pairs with unmodified mechanism logic (commits `99bf95ed7`, `0e63486c5`, `0c6cfa780`, `81b984bdc`, `141db015a`). H3's 2-mode structure-derived execution retired on structural grounds (cannot express value aggregation; mode extension is the finite-menu treadmill). H3 wiring discovery preserved as pluggable search option. Survivor set for value-handoff composition: H1+H2. |
| H-COMPCROSS-1 | TESTED (positive, bounded) | H1/H2 bridge 4 family pairs at Level 1 exact reuse: navigation x aggregation, arithmetic x alloc, causal x intervention, grammar x construction. Family-bounded falsifier not triggered. Boundary is planning, not family distance (see H-PLANCOMP-1). |
| H-XDOMAIN-1 | TESTED (mixed) | SUM to ALLOC (integer division): yes, H1/H2 PASS (`0c6cfa780`, artifacts in `xdomain_arith_plan/superseded_prereg1/`). SUM to PLAN (genuine goal-directed action sequences): no; H1/H2/H3/XIO all fail, clean negative (PREREG2 `91e84ee0d`, current `xdomain_arith_plan/REPORT.md`). The hypothesis as stated is confirmed for arithmetic value handoff and falsified for planning composition. |
| H-COMP-1 | SUPERSEDED | C191's "composition architecturally absent" verdict is superseded for value-handoff composition: H1/H2 demonstrate X+Y->Z across 4 pairs. Still open for planning composition (H-PLANCOMP-1) and for Levels 2/3. |

### Correction recorded

The `xdomain_h3_arith` / `h3_generality` "three-way comparison on the
same pair" (H1 PASS, H2 PASS, H3 FAIL) was invalid: H1/H2's figures
are from the PREREG1 world (SUM to ALLOC, Z=(101,93)->3) while H3 was
tested on the PREREG2 world (SUM to PLAN, Z=(103,93)->203). Different
Y domains, different sealed goals. Corrected record: on SUM to ALLOC,
H1 PASS / H2 PASS / H3 UNTESTED; on SUM to PLAN, all FAIL. H3's
retirement stands on the independent structural argument (2-mode
dispatch cannot express value aggregation), not on the invalid
comparison. Full correction in CONSOLIDATION.md Section 5.

### Architectural lesson (candidate constitutional principle)

Composition should depend on learned behavior contracts, not on
structural heuristics about how procedures compute. H1 observes WHAT
procedures consume/produce; H2 executes and observes results; both
are representation-agnostic. H3 inspected structure to select
execution method and failed at the first computation type outside
its heuristic. Structure underdetermines computation.

### New hypothesis from this consolidation

- **H-PLANCOMP-1 (P0):** Can any mechanism compose a computed value
  into a goal-directed planning procedure? PREREG2 shows H1/H2/H3/XIO
  all fail SUM to PLAN (plan(sum(s)) with parameterized action
  sequences). The failure is architectural and shared: every current
  mechanism is a novel-chain constructor. Falsifier: a mechanism that
  solves SUM to PLAN at cost below fresh trial with X/Y ablations
  causal and no planning-specific template. If three structurally
  distinct approaches fail, planning composition needs a new
  architectural primitive, not a better chain constructor.

No em dashes used (verified).

---

## Saturation wave 2026-10-02: 19 new hypotheses (Micah 10 priorities)

Status of prior hypotheses updated in the status table below. New IDs:

### P0: Composition is a core frontier

### H-COMPGEN-1: Which composition mechanism generalizes furthest, and can the three collapse into one operation?

Question: A, B, and C independently demonstrated X+Y->Z in the chain family. Which mechanism survives fresh post-freeze domains (misleading fragments, multiple valid compositions, branch topology, incorrect expected targets), does one subsume the others, and can their useful principles collapse into ONE general composition operation rather than three engines?

Why it matters: Micah Priority 1 forbids permanently integrating three separate composition engines. Three positive results in one battery is fork success, not architecture. If contracts, co-use history, and constraints share a common substrate (e.g. structure satisfying parts of a new goal), keeping three mechanisms is the same menu-expansion failure mode the constitution forbids.

Experiment: Adversarial comparison battery on fresh sealed worlds unseen during development: (a) misleading fragments that look composable but are not, (b) multiple valid compositions with different costs, (c) branch (non-chain) topologies, (d) wrong expected targets that must be rejected. Run A, B, C mechanisms plus a candidate collapsed mechanism on all four. Score: solves, false compositions, cost vs fresh rediscovery.

Falsifier: If all three mechanisms fail on branch topologies, composition is chain-bounded and no collapse is possible without new machinery. If the collapsed candidate matches or beats all three on every fixture with fewer cognition lines, the three-engine design is superseded.

Priority: P0.

### H-COMPNOEXP-1: Does composition work without expected-answer supervision?

Question: A, B, C all used the expected output as the search target. Can X+Y->Z be driven by an internal goal-satisfaction criterion (goal state entailment, learner-owned verification) so that composition succeeds where no researcher expected value exists?

Why it matters: Expected-answer verification is the last researcher crutch in the composition path. Composition that cannot proceed without the answer is assembly, not intelligence. This is the C181/C199 lesson applied to the composition frontier.

Experiment: Composition battery where goals are states to reach or properties to satisfy, never expected structures. Treatment composes using learner-owned verification (C181 machinery) as the acceptance test. Controls: expected-guided (prior positive), fresh trial. Ablation: remove learner verification, keep composition.

Falsifier: If treatment composes only when the goal state is isomorphic to an expected literal (verification is a rename of supervision), nothing changed. If ablation shows verification contributed nothing (search found Z first), composition does not use it.

Priority: P0.

### H-COMPK-1: Do compositions scale to 3, 4, 5+ learned structures?

Question: All positive composition results combine exactly two fragments. Can TNN compose three, four, or five previously learned structures into one executable Z, with ablation of each fragment showing causal contribution?

Why it matters: Two-fragment composition might be a special case (one boundary to bridge). Multi-fragment composition tests whether the mechanism is a general operation or a two-body trick. Micah Priority 1 names 3, 4, 5+ explicitly.

Experiment: Chain worlds requiring K fragments (K=3,4,5) learned independently. Treatment: composition; controls: fresh trial, leave-one-fragment-out (K ablations each). Measure: solves, cost vs fresh, per-fragment ablation loss, later reuse of the K-composite.

Falsifier: If cost grows superlinearly in K and exceeds fresh trial at K=3, the mechanism is a pairwise trick. If K-composites never persist or reuse, multi-composition produces disposable structures.

Priority: P0.

### H-COMPCROSS-1: Do structures from radically different domains compose?

Question: Can X from one structure family (e.g. arithmetic procedure graphs) compose with Y from a radically different family (e.g. causal experiment sequences) into a Z neither family produces alone?

Why it matters: Chain-family composition is bounded L2. Cross-domain composition is the test Micah Priority 1 and 4 demand: programming plus audio knowledge, formal language plus algorithm, causal knowledge plus planning. If composition only works inside one family, the "knowledge composes" claim is family assembly.

Experiment: Teach procedure-graph X in a numeric domain and sequence-graph Y in a planning-ish domain, independently. Pose goal Z requiring both: e.g. construct a plan whose steps are computed by the numeric procedure. No paired examples, no hint, no label. Treatment vs fresh control, X ablation, Y ablation.

Falsifier: If composition never bridges families across 3/3 runs in three family pairs, composition is family-bounded. If it works only when surface literals overlap, the bridge is surface matching.

Priority: P0.

### H-PARTADAPT-1: Can partial applicability be adapted during composition?

Question: H-ADAPT-1 asks whether single MAPs adapt across shape mismatch. In composition, can a fragment that partially satisfies a sub-goal be adapted (prefix reuse, extension, truncation) rather than rejected whole?

Why it matters: Exact-shape composition plus exact-shape rebinding both hit the same ceiling: anything mismatched falls back to trial. If fragments adapt inside composition, the reuse machinery contributes where shapes differ. Otherwise composition inherits the C188 ceiling.

Experiment: Composition worlds where X fits sub-goal 1 exactly but Y needs one-step extension for sub-goal 2, the missing step inferable from Y's own data. Treatment: adapt Y inside composition; control: fresh trial for sub-goal 2. Measure verifies, whether the adapted Y persists and reuses.

Falsifier: If adapted fragments cost more than fresh trial or never verify across three mismatch families, partial applicability is a fallback-only story.

Priority: P0.

### P0: Formal knowledge must constrain behavior

### H-GRAMIND-1: Can TNN induce grammar/semantics from examples so learned constraints become causally active in construction?

Question: C205 showed researcher-authored grammar restriction turns 0/11 into 11/11. Can the learner instead induce the grammar (allowable forms, type constraints) from positive and negative examples, store it in learner-owned state, and have it actively constrain generation so invalid structures become impossible or explicitly rejected?

Why it matters: Micah Priority 2: do not permanently hardcode grammar restriction. Induce it from examples, then ablate the learned constraint and verify errors return. This is the sharpest test of "formal understanding constrains behavior" as learner-owned knowledge rather than researcher whitelist.

Experiment: Teach the EXL tiny language (or a fresh compact formal language) via examples only: valid and invalid constructions with outcomes. Treatment: learner induces a constraint structure; later novel construction tasks. Controls: researcher-whitelist (C205 treatment), no-constraint base. Ablation: delete the induced constraint, keep everything else; errors must return. Long-term: extend toward Zag syntax.

Falsifier: If induced constraints never reach whitelist performance across 3/3 runs in three languages, induction fails. If ablation does not restore errors, the constraint was not causal. If the induction procedure enumerates researcher-listed rule forms, the learning is template fitting.

Priority: P0.

### H-GENREENTRY-1: Do consequences re-enter candidate generation and search order?

Question: C206 found consequences do not re-enter generation: base repeated 4/4 errors despite 16 prior rejections. Can rejection consequences alter future candidate generation and search ordering so previously rejected forms are not regenerated?

Why it matters: This is the architectural gap behind F1/F2. A system that remembers outcomes but generates candidates as if nothing happened has memory without learning. The consequence loop (Constitution: outcome to retention to changed decision) is broken at the generation step.

Experiment: Worlds with repeated construction opportunities in a constrained grammar. Treatment: rejection consequence records feed a generation-order penalty (via the shared substrate). Control: C206 base. Measure: repeat-error rate over trials, verifies to first valid, whether search order visibly shifts after rejections.

Falsifier: If repeat errors persist at base rates after 20+ rejection records, consequences do not constrain generation. If order shifts but errors stay, ordering without form-avoidance is insufficient.

Priority: P0.

### P0: Scaling

### H-INDEXADV-1: Can the general index invariant survive adversarial corruption?

Question: C203 broke the plen-bucket index with a single cycle (no liveness/type/cycle check, buffer overflow). Can a GENERAL invariant (structural liveness checks, bounded candidate buffers, cycle detection on every index mutation path) be built so no fixture-specific fix is needed again?

Why it matters: Micah Priority 6: fix the general invariant, not just that fixture. An index that crashes on corrupt state is not a scaling solution; it is a happy-path demo. Every index mutation (insert, link, evict, slot-reuse) must preserve the invariant.

Experiment: Adversarial index battery: cycles injected at insert, bucket corruption, slot reuse after eviction, concurrent mutation during scan. Treatment: invariant-hardened index. Control: C193 index. Measure: crashes (must be zero), retrieval correctness, scan visits unchanged on intact state. Red team designs post-freeze corruption fixtures.

Falsifier: If any corruption fixture crashes or silently returns wrong candidates, the invariant is incomplete. If hardening costs more than the index saves below 100 MAPs, record crossover.

Priority: P0.

### H-TRIALMEM-1: Can trial reclaim rejected candidates structurally?

Question: C205/C206 noted trial leaks ~13 nodes per candidate including rejected ones, plus superlinear full edge scans. Can the learner reclaim dead candidate structure and index live structure so construction cost stays sublinear in trial history?

Why it matters: Generation without reclamation is a memory leak wearing a lab coat. Long lifetimes require structure-level reclamation (Constitution 17). This is the memory half of the scaling story; indexing is the retrieval half.

Experiment: Long construction lifetime (hundreds of candidates, most rejected). Treatment: structural reclamation of dead candidates plus live-structure indexing. Control: C206 base. Measure: workspace occupancy over time, per-candidate allocation cost trend, slowdown factor over 100/500/1000 candidates.

Falsifier: If occupancy still grows linearly with rejected candidates, reclamation fails. If reclamation corrupts live structures (post-reclamation queries return wrong results), it is unsafe.

Priority: P0.

### P1: Cognitive operations as learner-owned structures

### H-OPSTRUCT-1: Can cognitive operations be represented as learner-owned executable structures with learned applicability, consequence records, composition, revision, and retirement?

Question: C197/C200 select operations from consequence history, but the operation set and preconditions are researcher-authored. Can operations themselves become learner-owned executable graphs whose applicability is learned from history, whose records live on the shared substrate, and which compose with each other, revise, and retire?

Why it matters: Micah Priority 3. Researcher-authored ops with learned selection is still a menu. The north star: the learner discovers useful cognitive sequences itself. Avoid recreating modes as RETRIEVE_OP/REASON_OP/PREDICT_OP/INVENT_OP with a smarter router.

Experiment: Operation records as executable structures: each op has applicability conditions learned from consequence records, cost estimates from history, and composition edges to successor ops. Worlds requiring multi-step cognition. Treatment: op structures editable by the learner (revise applicability after failures, retire ops with sustained negative utility). Control: C200 fixed op set. Measure: novel op sequences discovered, dead-op retirement events, composition of two ops into a compound op that reuses.

Falsifier: If the learner never revises an applicability condition or retires an op across 3/3 lifetimes, ops are frozen entries. If op composition never yields a reused compound op, composition of cognition is absent.

Priority: P1.

### P1: Consequence-taught adaptive policy

### H-INTEGPOL-1: Can consequences teach TNN the costs of false trust, unnecessary withholding, wrong prediction, and missed opportunity?

Question: C203 showed the integrated AND gate withholds on a perfect predictor when the source is adversarial (0% answered) while prediction-only scores 100%. Can consequence records teach the decision policy the four costs (false trust, unnecessary withholding, wrong prediction, missed opportunity) so the policy adapts to context instead of using a hardcoded AND/OR?

Why it matters: Micah Priority 7: do not patch the AND gate with a new hardcoded OR/AND switch. The policy must learn from consequences which error is expensive in the current context. This merges utility (C187), reliability (C183/C194), withholding (C195), and operation selection (C200) into one adaptive policy.

Experiment: Context-varying lifetime: phases where (a) sources are honest (withholding is pure cost), (b) sources adversarial (trust is pure cost), (c) predictors unreliable (prediction cost). Treatment: policy parameters (trust/withhold/predict weights) updated from tagged consequence records. Control: C194 AND gate. Measure: accuracy per phase, answer rate, adaptation lag after phase change. Ablation: freeze weights at phase-a values.

Falsifier: If treatment never beats the AND gate in any phase, consequence teaching fails. If weights oscillate without settling, the teaching signal is too noisy to be a policy.

Priority: P1.

### P1: Meta-learning applicability

### H-APPLIC-1: Can the learner judge "does it apply HERE" with no researcher domain labels?

Question: C203 proved irrelevant plen-3 history causes a 4x slowdown on plen-5 Family 2. Can the learner maintain applicability judgments (this old structure applies here / is irrelevant / is misleading) that accelerate related domains, stay neutral on irrelevant ones, and reject misleading ones, with NO researcher-supplied domain labels?

Why it matters: Micah Priority 5. Learning-to-learn that cannot detect irrelevance is a liability at scale: every old structure becomes a tax. Applicability must be learner-owned and label-free, derived from structural match evidence and consequence history.

Experiment: Mixed lifetime: Family B episodes interleaved with structurally related, structurally unrelated, and adversarially misleading families. Treatment: applicability tags learned per MAP/family from structural-match records and outcome consequences. Control: C198 machinery without applicability. Measure: cost on related (must accelerate), unrelated (must be neutral vs fresh), misleading (must reject faster than control). Ablation: delete applicability tags.

Falsifier: If unrelated-family cost stays above fresh (neutrality fails), applicability is not learned. If the learner needs surface similarity to judge applicability, it is label-free only in name.

Priority: P1.

### P1: Invention (three structurally different hypotheses)

### H-INVENT-MUT-1: Mutation: do new forms arise from structure mutation under inadequacy pressure?

Question: When existing structures provably fail a goal (inadequacy detected via repeated consequence failure), can the learner generate mutated variants of its own structures (edge rewiring, node substitution, subgraph splicing) and does a useful mutant ever survive internal evaluation, persist, and reuse?

Why it matters: Micah Priority 8 requires existing structures inadequate as the trigger. Mutation is the simplest structurally different invention hypothesis: variation on what exists, selected by learner-owned evaluation.

Experiment: Worlds where all learned structures fail a novel goal but a one-mutation variant succeeds. Treatment: mutation generator over learner structures with internal evaluation (consequence-predicted utility) before execution. Controls: fresh trial, exact-reuse only. Track: mutants generated, mutants passing internal eval, mutants executed successfully, mutants persisting and reusing later.

Falsifier: If no mutant ever passes internal eval and executes successfully across 3/3 runs in three inadequacy families, mutation does not produce invention. If mutants succeed but never reuse, they are disposable repairs.

Priority: P1.

### H-INVENT-REC-1: Recombination: do new forms arise from cross-family structure splicing?

Question: Can the learner splice subgraphs from structures of different families (inadequate individually) into a novel form that neither family contains, evaluated internally, persisted, and reused?

Why it matters: Second structurally different invention hypothesis. Recombination differs from mutation: the new form's parts come from unrelated structures, so the result is not a variant of any one parent. This tests whether TNN can be combinatorially creative rather than locally adaptive.

Experiment: Goal requiring part of arithmetic-chain structure plus part of planning-sequence structure, where no single parent suffices. Treatment: subgraph splicing across families with internal eval. Controls: mutation-only (H-INVENT-MUT-1 arm), fresh trial. Measure: spliced forms created, internally accepted, executed, persisted, reused, transferred to a new surface.

Falsifier: If spliced forms never outperform mutation-only across three cross-family worlds, recombination adds nothing. If every "splice" is actually one parent plus cosmetic graft, it is mutation in disguise.

Priority: P1.

### H-INVENT-CON-1: Constraint-driven: do new forms emerge from constraint satisfaction search over structure space?

Question: Can the learner express a goal as constraints on structure (form requirements, type requirements, cost bounds) and search structure space for a form satisfying them, producing a form no existing structure resembles?

Why it matters: Third structurally different invention hypothesis. Constraint search differs from mutation (no parent required) and recombination (no parts required): the form is specified by requirements, not derived from parents. This is the C199 constraint idea turned inward on structure creation.

Experiment: Inadequacy worlds where the needed form is not a mutant or splice of anything known (verified by distance: no parent within K edits). Treatment: constraint extraction from goal plus structure-space search. Controls: mutation arm, recombination arm. Measure: forms created, constraint satisfaction verified, persistence, reuse, transfer. Crucial check: the final form must be source-underdetermined (no researcher-enumerated candidate family contains it).

Falsifier: If constraint search never produces a form beyond K edits of a parent, it collapses to mutation. If forms are produced but never reused, they are one-off solutions.

Priority: P1.

### P1: Belief and logic

### H-BELIEF-1: Does TNN form rational beliefs from available evidence (provisional, uncertain, revised)?

Question: Given weak evidence, does TNN hold a provisional belief (acted on cautiously); given contrary evidence, does it become uncertain rather than flipping or freezing; given strong independent evidence, does it revise with an explanation trace?

Why it matters: Micah Priority 9. Belief formation is scored against available evidence, not omniscience. The current machinery (reliability scores, thresholds) adjusts numbers; belief requires the learner to hold a stance toward a proposition and change it for stated reasons.

Experiment: Evidence-ladder worlds: proposition P with (a) one weak source, (b) two contradicting sources, (c) three independent strong sources, (d) a later retraction. Treatment: belief records with evidence links and stance values. Measure: stance trajectory vs evidence, explanation quality (can TNN state why it believes P?), revision latency after retraction, action calibration (cautious action under weak evidence).

Falsifier: If stances do not track evidence strength (e.g. full commitment on one weak source), belief is absent. If revision after retraction requires researcher intervention, the mechanism is not learner-driven.

Priority: P1.

### H-LOGIC-1: When known facts entail X, does TNN derive X without prediction?

Question: In exact logical situations where premises entail a conclusion, does the learner DERIVE the conclusion (C190/C197 have DERIVE) rather than route through prediction machinery, and does it do so faster and more reliably than prediction-based paths?

Why it matters: Micah Priority 9 and the constitution: prediction is one optional process. Forcing prediction into exact knowledge is waste and error. This tests whether the operation selector distinguishes entailed from uncertain.

Experiment: Entailment worlds: premises that logically determine answers (deductive chains, constraint propagation) mixed with genuinely uncertain worlds. Treatment: unlabeled selector (C197) over operation set including DERIVE and PREDICT. Measure: on entailment worlds, DERIVE usage rate, correctness, cost vs PREDICT path; on uncertain worlds, PREDICT usage rate. Control: prediction-forced baseline.

Falsifier: If DERIVE is not preferentially selected on entailment worlds (usage at chance), the selector cannot tell entailment from uncertainty. If DERIVE is selected but wrong more often than prediction, the DERIVE machinery is broken.

Priority: P1.

### P1: Strong composition sealed tests

### H-COMPREVISE-1: Can composite structures be revised and reused later?

Question: A, B, C showed Z persists and reuses once. Can a composite Z later be REVISED (counterexample arrives, Z must change while keeping its fragment provenance) and can the revised Z reuse in a new context?

Why it matters: Micah Priority 1 and 4: persistence without revision is fossilization. The continuing learner must revise composites the way it revises beliefs. Revision of a composite tests whether the composition's internal structure (X part, Y part, bridge) is learner-legible.

Experiment: Composition battery, then a counterexample invalidating the X-derived part of Z. Treatment: revise Z's X-part via re-composition or adaptation, keep Y-part. Controls: rebuild from scratch, keep broken Z. Measure: revision cost vs rebuild, whether revised Z verifies, later reuse of revised Z, provenance integrity after revision.

Falsifier: If revision always costs as much as rebuild, composites are write-once. If revision corrupts the intact part, the composite is not modular.

Priority: P1.

### H-XYSKILL-1: Sealed X-skill plus Y-domain to novel Z (Micah core example battery)

Question: In sealed worlds: learn skill X independently (e.g. a construction procedure), learn domain Y independently (e.g. audio fact structures), then receive novel goal Z requiring both (e.g. construct an audio system). No paired examples, no combination hint, no task label. Does causal reuse of both competencies occur?

Why it matters: Micah Priority 4. This is the canonical strong-composition test, harder than chain batteries: the competencies live in different representational neighborhoods and Z is not a longer chain. Eventual instances: programming plus audio, formal language plus algorithm, causal knowledge plus planning.

Experiment: Three sealed domain pairs designed post-freeze by an independent adversary. Treatment: full learner with composition machinery. Controls: X-only learner, Y-only learner, fresh learner. Require: both X and Y ablation loss, Z executable, no paired examples in training, no task label at goal time.

Falsifier: If treatment fails all three pairs while X-only or Y-only succeed on their parts, cross-competency composition is absent. If Z succeeds but ablation shows only one competency was used, it is single-skill transfer.

Priority: P1.

---

## Frontier status update: 2026-10-02 (Governance saturation wave)

### Tested since the 2026-10-02 governance wave-3 update

| Hypothesis | Status | Evidence |
|---|---|---|
| H-COMP-1 | TESTED (positive, bounded) | C201/C202/C199: A, B, C all positive in chain family. Causal ablations pass. Researcher search machinery + expected-answer verification retained in all three. |
| H-PERSIST-1 | TESTED (positive, bounded) | C207: links survive 1000+ events (census 2->3->4->5) but speedup conditional on persistent competitors; distractors were evicted. Partial completion (2/3 treatment). |
| H-FORMAL-1 | TESTED (positive, bounded) | C205: mastery 10/10 both arms; construction 0/11 base vs 11/11 grammar-restricted. Restriction researcher-authored. C206: F1 4/4 base errors vs 0/4 treatment; F2 same; F3 both lost 8/8 nodes under pressure. |
| H-NEGTR-1 | TESTED (negative) | C203: irrelevant plen-3 history causes 4x slowdown (40 vs 10) on plen-5 Family 2. Consequence substrate does NOT prevent negative transfer without applicability judgments. |
| H-INDEX-1 | TESTED (positive, bounded) | C193 positive; C203 BREAKS it: cycle in bucket list crashes (no liveness/type/cycle check, buffer overflow). 140x claim valid only on intact happy-path state. |
| H-INTEG-1 | TESTED (positive, bounded) | C194 positive; C203 TRADEOFF: perfect predictor + adversarial source gives 100% prediction-only vs 0% answered for integrated AND gate. Integration avoids false trust but can be too conservative. |
| H-PREDOPT-2 | TESTED (positive) | C197: unlabeled selection 19/19 correct, emergent sequences; fresh ablation returns to 3 ops. Op set still researcher-authored. |
| H-SUB6-1 | TESTED (positive) | C200: substrate-driven operation selection 7/7 vs 3/7 control; 6th/7th substrate behavior. Signature bits + score formula researcher-authored. |
| H-THRESH-1 | TESTED (partial) | C195: adaptive WT wins on regime change 111 vs 104; loses stationary. Values learner-owned; update formula + clamp researcher-owned. |
| H-SEQ-1 | TESTED (partial) | C197 emergent sequences GATHER->DERIVE->VERIFY->EXEC, RETRIEVE->REBIND->CROSSCHECK observed; sequencing researcher-free but op definitions researcher-authored. |
| H-L2L-2 | TESTED (partial) | C198: cross-regime temporal-noise transfer (T=5 from noisy A); 0 wrong commits vs 3 for others. Cross-paradigm transfer still untested. |
| H-SCALE-1 | RE-RUNNING CLEAN | C204 (11adcb0ea) PROCESS-FAIL for canonical (Python violation). Clean safebin reproduction in progress (scaling_clean worker; byte-identical source rebuild verified via cmp/sha256sum). |
| H-COMP-0 | SUPERSEDED | A/B/C all consumed MAPs via composition machinery; the bridge question is answered positively for chains. Replaced by H-COMPGEN-1. |

### Live frontier (open hypotheses)

Untested: H-SCALE-1, H-ADAPT-1, H-UTILRET-1, H-COMPRESS-1, H-SLOT-1, H-PROVUTIL-1, H-XDOMAIN-1, H-COMP-0(s), H-EMERGKEY-1, H-COMPGEN-1, H-COMPNOEXP-1, H-COMPK-1, H-COMPCROSS-1, H-PARTADAPT-1, H-GRAMIND-1, H-GENREENTRY-1, H-INDEXADV-1, H-TRIALMEM-1, H-OPSTRUCT-1, H-INTEGPOL-1, H-APPLIC-1, H-INVENT-MUT-1, H-INVENT-REC-1, H-INVENT-CON-1, H-BELIEF-1, H-LOGIC-1, H-COMPREVISE-1, H-XYSKILL-1.
Partially tested but open: H-VER-1, H-INDEX-1, H-INTEG-1, H-PREDOPT-1, H-COMP-1, H-L2L-1, H-PERSIST-1, H-THRESH-1, H-FORMAL-1, H-NEGTR-1, H-PREDOPT-2, H-SEQ-1, H-L2L-2.
Total live: 41. Requirement: 20+. Met with margin.

### Treadmill check (Constitution 23)

New treadmill risk: composition A/B/C are three adjacent positive results on the same chain battery. Per Section 23, freeze the "another composition mechanism on chains" lineage: H-COMPGEN-1 is the last allowed chain-family characterization; next composition work must be adversarial generalization (H-COMPCROSS-1, H-COMPNOEXP-1, H-COMPK-1), cross-domain, or the collapse experiment, not a fourth mechanism on chains.

The exact-plen fallback lineage stays frozen per the prior update. The scaling numbers lineage (100/500/1000 MAP claims) is frozen until the clean rerun lands; no new scale claims may cite C204 measurements as canonical.

### Compression note

C194 deleted one private store (net-negative integration). C201/C202/C199 add three parallel composition mechanisms (~250 lines each estimated). Net direction is wrong until H-COMPGEN-1 collapses them. Compression ledger addendum follows in the next governance commit.

### Saturation worker mapping (no fixed cap; maximize useful throughput)

Active: composition_compare (H-COMPGEN-1), scaling_clean (H-SCALE-1 clean rerun), plus 12 more lanes per Micah priorities: grammar_induction (H-GRAMIND-1), index_hardening (H-INDEXADV-1), belief_formation (H-BELIEF-1), logic_vs_prediction (H-LOGIC-1), meta_learning (H-APPLIC-1), cognitive_ops (H-OPSTRUCT-1), integration_policy (H-INTEGPOL-1), strong_composition_sealed (H-XYSKILL-1), cross_domain_composition (H-COMPCROSS-1), invention_1/2/3 (H-INVENT-MUT-1, H-INVENT-REC-1, H-INVENT-CON-1).

No em dashes used (verified).

---

## Status update: 2026-10-02, composition comparison landed (C208)

| Hypothesis | Status | Evidence |
|---|---|---|
| H-COMPGEN-1 | TESTED (positive, bounded) | C208: C subsumes A/B on arity; collapse to one operation via C's DFS with pluggable applicability predicates. All fail T4 (atomic MAPs), T5 (expected required), 4+ (cap). |
| H-COMPK-1 | TESTED (partial) | C208 T1: 3-structure composition works (C only). 4/5 fail on caps, not architecture. A/B are pair-bound by design. |
| H-COMPCROSS-1 | TESTED (positive, bounded) | C208 T3: all three pass cross-domain (chain + single-hop). Heterogeneity is not the blocker; decomposition is. |
| H-PARTADAPT-1 | TESTED (negative) | C208 T4: all fail. MAPs are atomic units; no prefix use. Decomposable MAPs are the next architecture target. |
| H-COMPNOEXP-1 | TESTED (negative) | C208 T5: all fail without expected. Learner verification (C181) replacing expected is the open experiment. |

Live count unchanged (41). The composition-collapse recommendation from C208 is now the highest-priority integration task: build the single DFS composition op, port contract/co-use/relsew as applicability predicates, remove or learner-control the segment cap, then attack MAP decomposability (T4) and expected-free verification (T5).

No em dashes used (verified).

---

## Status update: 2026-10-02, scaling clean + logic-vs-predict landed (C209, C210)

| Hypothesis | Status | Evidence |
|---|---|---|
| H-SCALE-1 | TESTED (positive, clean) | C209: pure-Zag safebin reproduction of C204, zero Python, 3/3 byte-identical (eee373a2). 140x/693x/1393x canonical now. PROCESS-PASS. H-SCALE-1 moves from exploratory-only to canonical evidence. |
| H-LOGIC-1 | TESTED (positive) | C210: state-driven dispatch never predicts on exact knowledge even with competing weak predictor; derives entailed values exactly; predicts only under uncertainty; withholds honestly on empty. Prediction-first pollutes state with false PRED nodes. 0 new semantic cases. |

New treadmill note: the scaling-number lineage is unfrozen from PROCESS-FAIL but remains exploratory (no frozen prereg). Further scale claims should move to frozen preregistration per the 11-step pipeline before canonical promotion beyond reproduction.

No em dashes used (verified).

---

## Status update: 2026-10-02, frontier generation wave (16 new hypotheses)

Worker: Frontier Generation Worker (frontier_gen_20261002). Branch: tnn-native-lab. Local only, nothing pushed.

### Latest results mined

1. composition_xdomain REPORT (COMPOSITION-XDOMAIN-COMPLETE): all three mechanisms (A, B, C) fail cross-domain cleanly, 3/3 byte-identical per mechanism. Diagnosis: "every existing mechanism implements composition as navigation concatenation; cross-domain needs function composition over typed values." X = navigation (chain-following, output a literal retrieved by walking facts); Y = aggregation (count queries via INC cells tag 103 plus MOV epilogue, output computed arithmetically, no output literal in the fact store). Z = chain-then-count: X's output node (34) is Y's input subject; Y's output (2) is a number, not a walkable node. Count MAPs (plen=-1, contract=-1, relseq=[]) are real, competent, reusable-via-trial, but every mechanism's admission filter renders them invisible.
2. grammar_induction REPORT (GRAMMAR-INDUCTION-COMPLETE): INDUCE arm 11/11 valid; HARDCODE arm 11/11 valid; causal ablation.
3. Invention: H-MUT-1/H-MUT-2 PASS; INVENTION-RECOMBINE-COMPLETE ("Fragment recombination strictly generalizes whole-MAP chaining (when frag_on=1, whole MAPs are just (m,0,len) fragments, so C is a special case)"; "if fragment recombination subsumes Composition C (it does, as a special case), the whole-MAP path could be deleted, yielding net-negative lines. This is flagged for the integration worker, not done here."); INVENTION-CONSTRAINT-COMPLETE (TREAT constructs all 3, K1 PASS). All PASS at L2, honestly bounded.
4. cogops_structures REPORT: composition links shield applicability. Ablation (comp links recorded but not used): treat late N 96.6% vs ablation 58.1%, gap 38.5pp (bar >=30pp). Appl-only learner collapses to a stable bad equilibrium: late F 24% (treat 100%), late N2 15% (treat 98%).
5. integration_adaptive REPORT (INTEGRATION-ADAPTIVE-COMPLETE): "K1: adaptive total beats both fixed gates on every seed"; the policy "contains no threshold constant and no AND/OR combination of signals."
6. C209: scaling canonical, pure-Zag safebin, 3/3 byte-identical (eee373a2): 140x/693x/1393x at 1000 MAPs.
7. belief_formation REPORT (BELIEF-FORMATION-COMPLETE): "Rationality 3/3 phases relative to evidence at time. Both ablations pass."
8. meta_applicability REPORT: Verdict FAIL (K7, correctness). TREAT C-P5 trial fails with WRONG answer (ans=-2, trial=11) on the 21st problem. "The base TNN-2 trial cannot solve the 21st problem correctly, indicating a scaling limitation in the base (not the APPL gate, which correctly set gate=0)." APPL mechanism demonstrated: K1, K4, K5 PASS; K2, K3, K6 partial.
9. composition_sealed REPORT (COMPOSITION-SEALED-COMPLETE with causal reuse proof): skill X (scalar transform) plus domain Y (sequences) compose to sealed novel Z with no paired examples, no combination hint, no task label. "Ablating X or Y destroys Z. All ten frozen kill bars passed. 3/3 byte-identical."

### New hypotheses, ranked by expected information gain (#1 highest)

### H-COLLAPSE-1: Delete Composition C's whole-MAP path into fragment recombination (rank #1)

Question: The recombination report proves fragment recombination strictly generalizes whole-MAP chaining (with frag_on=1, whole MAPs are just (m,0,len) fragments, so C is a special case) and flags that the whole-MAP path could be deleted for net-negative lines, but the integration was never done. Can Composition C be deleted entirely and reimplemented as fragment recombination restricted to (m,0,len) fragments, with zero capability loss?

Mechanism sketch: Replace cc_dfs with ir_frag_dfs parameterized to whole-MAP fragments; port C's applicability predicates (contract, co-use, relseq) to fragment-level predicates; delete the duplicated DFS structure. The single composition operation becomes the recombination operator in its (m,0,len) special case.

Expected result: Every C-positive battery (chain composition batteries, C208 T1 3-fragment composition, sealed composition) still passes; cognition lines strictly decrease by the size of the deleted whole-MAP path; zero new semantic cases, modes, or bridges.

Simplest baseline: Keep both paths (current state: two parallel DFS implementations).

Falsifier: Any C-positive battery flips to FAIL under the collapsed implementation, or the line count does not decrease (the "duplication" was load-bearing after all).

Likely failure mode: Fragment DFS admission semantics differ at the (m,0,len) boundary (e.g. count MAPs with plen=-1 and empty relseq break the fragment mapping), so collapse works on chains but silently changes behavior on irregular MAPs.

Priority: P0.

### H-XIO-1: Learner-built typed I/O adapters rescue cross-domain composition (rank #2)

Question: The xdomain diagnosis is exact: all three mechanisms implement composition as navigation concatenation, but Z (chain-then-count) needs function composition over typed values. X's output node (34) is Y's input subject; Y's output (2) is a number, not a walkable node. Count MAPs (plen=-1, contract=-1, relseq=[]) are real and competent but invisible to every admission filter. Can the learner construct interface adapters (typed I/O bridge structures) that make Y's MAPs admissible and bind X's output value as Y's input?

Mechanism sketch: When admission rejects a MAP with empty relseq that has verified trial history, the learner builds an adapter: a small executable structure declaring the MAP's input type (subject node) and output type (number, produced by INC cells tag 103 plus MOV epilogue), plus a value-binding edge from the upstream fragment's output. Adapters are learner-owned structures subject to revision and retirement, never researcher bridges.

Expected result: Z query (31,93)->2 solves via X-then-Y with a learner-constructed adapter; ablations of adapter, X MAPs, and Y MAPs each destroy Z; the adapter reuses on a second cross-domain goal with fresh literals.

Simplest baseline: Direct navigation concatenation (current behavior) = 0/3 on Z in all arms.

Falsifier: Learner-constructed adapters never verify across 3/3 runs in three X/Y family pairs; only researcher hand-coded type mappings work.

Likely failure mode: The learner has no type vocabulary (numbers vs node literals are not distinguished in learner state), so adapter construction has nothing to build on; typed values must be induced first, making this hypothesis premature without a type-induction precursor.

Priority: P0.

### H-DECOMP-1: Store MAPs as fragment-addressable structures (rank #3)

Question: C208 T4 and H-PARTADAPT-1 failed cleanly: MAPs are atomic units, no prefix use. The named next architecture target is decomposable MAPs. Can MAPs be stored with learner-created segment boundaries so that rebind and composition address (m,start,len) directly instead of whole MAP ids?

Mechanism sketch: At episode success, the learner writes segment-boundary marks (reusing the type-15 LINK edge machinery from mechanism B) at points where sub-sequences independently verified. The MAP store becomes fragment-addressable; rebind and composition take (m,start,len) arguments. The collapsed recombination operator (H-COLLAPSE-1) consumes fragments natively.

Expected result: Prefix reuse works (a plen-4 MAP contributes its plen-3 prefix to a plen-3 subgoal); T4-style fixtures pass; partial-applicability adaptation (H-PARTADAPT-1) flips to positive.

Simplest baseline: Atomic whole-MAP rebinding = 0 on all prefix fixtures.

Falsifier: Fragment-addressable storage costs more than fresh trial (boundary maintenance overhead dominates), or learner-placed segment boundaries never align with reuse needs across 3/3 mismatch families.

Likely failure mode: Boundary placement is the hard part; wrong boundaries make fragments useless and the mechanism degrades to whole-MAP rebinding with overhead, or boundaries proliferate and the index story (H-INDEX-1) regresses.

Priority: P0.

### H-COMPVER-1: C181 learner verification replaces expected answers in composition (rank #4)

Question: H-COMPNOEXP-1 failed (C208 T5: all mechanisms fail without expected). The named open experiment is learner verification (C181) replacing expected. Can composition search accept Z candidates via reliability-gated learner verification instead of matching a researcher-supplied expected literal?

Mechanism sketch: Composition proposes Z candidates; acceptance uses C181 machinery (predicted reliability from consequence history, honest withholding when no predictor exists) against goal properties to satisfy, never an expected structure. Withholding fires on uncomposable goals instead of emitting garbage.

Expected result: Composition succeeds on goals where no researcher expected value exists; false-composition rate drops vs the expected-free baseline; ablating verification returns the T5 failure.

Simplest baseline: Expected-guided composition (current positive) and fresh trial.

Falsifier: Treatment composes only when the goal state is isomorphic to an expected literal (verification is supervision renamed), or ablating verification changes nothing (search found Z first anyway).

Likely failure mode: Reliability scores are trained on trial outcomes, not composition outcomes, so the verifier cannot discriminate good from bad compositions; the search accepts wrong Z or withholds on everything.

Priority: P0.

### H-CAP-1: Lift the segment cap; test 4/5-fragment composition (rank #5)

Question: C208 T1: 3-structure composition works (C only); 4/5 fail on caps, not architecture. Is the segment cap a harness artifact or load-bearing?

Mechanism sketch: Remove the cap in the collapsed composition op, or make the cap a learner-owned parameter adjusted from consequence records (composition success/failure vs segment count). Run K=3,4,5 fragment worlds with per-fragment ablations.

Expected result: 4- and 5-fragment compositions succeed with causal per-fragment ablation loss; cost grows sub-quadratically in K; the K-composite persists and reuses.

Simplest baseline: Capped composition = hard fail at K>=4 by construction.

Falsifier: Uncapped cost grows superlinearly and exceeds fresh trial at K=4 (the cap was load-bearing, masking blowup).

Likely failure mode: Search combinatorics explode; uncapped composition is correct but useless, and the real need is consequence-ranked candidate ordering, not cap removal.

Priority: P0.

### H-SHIELD-1: What exactly shields applicability when composition links are used (rank #6)

Question: The cogops ablation is the most surprising recent finding: with comp links recorded but not used, late N drops 96.6% to 58.1% and the appl-only learner collapses into a stable bad equilibrium (F 24%, N2 15%). Is the shielding carried by the edge structure or by the composition episode's consequence records?

Mechanism sketch: Four-way dissociation: (a) full treat, (b) comp links deleted but consequence records kept, (c) consequence records deleted but edges kept, (d) harness-written comp links with no composition episode ever run. The shielding carrier is whichever single deletion reproduces the collapse.

Expected result: Deleting the episode's consequence records reproduces the collapse even with edges intact (shielding is episodic, not structural); harness-written links do not shield.

Simplest baseline: Current treat vs full ablation (already measured: 38.5pp gap).

Falsifier: Harness-written links shield equally well (shielding is structural), or no single deletion reproduces the collapse (the effect is irreducibly entangled).

Likely failure mode: Links and records are written by the same code path, so clean dissociation is impossible and the mechanism stays a black-box correlation; the honest result is "entangled, needs a rewrite to separate."

Priority: P1.

### H-QUAR-1: Learner quarantine of corrupted base evidence (rank #7)

Question: Meta-applicability FAILED K7 because base TNN-2 trial produced a WRONG answer (ans=-2, trial=11) on the 21st problem; the APPL gate correctly set gate=0 but the run still burned. Can the learner detect the corruption signature (sudden clustered failures on previously-mastered problems, contradicting long mastery history) and quarantine those evidence records instead of revising good structures?

Mechanism sketch: Per-family mastery records (verified-solve history). A corruption detector fires when failures cluster on mastered problems at a rate incompatible with the mastery history. Quarantined records are excluded from revision, reliability, and utility updates, and the corruption is flagged in learner state.

Expected result: With a corrupted base injected, the quarantine learner preserves mastered structures and flags the corruption; the control revises good structures (measurable negative learning: post-corruption competence drop).

Simplest baseline: No quarantine (current) = base bug poisons learner state.

Falsifier: Quarantine never fires on real injected corruption across 3/3 runs, or fires on genuine world change (false quarantine worse than no quarantine on H-THRESH-1 regime-change worlds).

Likely failure mode: "Base bug" vs "world changed" is genuinely hard to distinguish from inside; the signature overlaps regime change, and the detector either never fires or fires on every shift.

Priority: P1.

### H-GRAMZAG-1: Induced grammar transfers to Zag syntax itself (rank #8)

Question: Grammar induction reached 11/11 on a tiny language with causal ablation. The untested transfer is grammar->Zag: can the same induction machinery induce constraints on real Zag syntax (the researcher's own language) from valid/invalid program fragments, and do the induced constraints actively block invalid construction?

Mechanism sketch: Feed the H-GRAMIND-1 induction machinery a corpus of valid/invalid Zag fragments; the learner induces Zag-syntax constraints into learner-owned state; test on a novel Zag program-construction task, measuring invalid-attempt rejection pre-execution.

Expected result: Induced Zag constraints reach near-whitelist performance; ablation (delete induced constraints) restores construction errors; the constraint transfers to Zag constructs absent from the training corpus.

Simplest baseline: Researcher-whitelist of Zag syntax (C205-style) vs no constraint.

Falsifier: Induction never reaches whitelist performance on Zag across 3/3 runs, or the induced constraint is never consulted during generation (performance comes from elsewhere).

Likely failure mode: Real Zag syntax has irregularities the tiny-language induction cannot capture; the experiment reveals the induction machinery's complexity ceiling, which bounds H-GRAMIND-1 honestly.

Priority: P1.

### H-DECEPT-1: Belief machinery detects source defection (rank #9)

Question: Belief formation is 3/3 rational relative to evidence at time. The untested transfer is belief->deception: a source builds high reliability over many episodes, then defects (the C203 adversarial-source scenario that broke the integrated AND gate). Do belief-stance trajectories detect defection faster than scalar reliability scores?

Mechanism sketch: Sources reliable for N episodes then defect; treatment uses H-BELIEF-1 stance records (stance values with evidence links, revision traces) to detect defection; control uses raw reliability scores / the adaptive policy. Measure false trusts post-defection and detection latency.

Expected result: Belief treatment detects defection in fewer episodes because stance trajectories encode the shape of evidence history (sudden contradiction of a long-supported stance), not just a scalar average.

Simplest baseline: Reliability-score-only detection (C183/C194 machinery).

Falsifier: Belief treatment detects no faster than scalar reliability across 3/3 defection schedules; stance trajectories add no signal.

Likely failure mode: Belief stances are derived from the same reliability scores, so no independent signal exists and deception detection reduces to threshold tuning; the honest result bounds belief machinery to honest-but-noisy worlds.

Priority: P1.

### H-INVNCH-1: Recombination invention outside the chain family (rank #10)

Question: Invention H1/H2/H3 all PASS at L2, honestly bounded, but inside the chain family. The untested transfer is invention->non-chain: does the recombination operator (ir_frag_dfs) produce novel, verifying, persisting forms on non-chain structures (numeric procedure graphs with INC cells, count MAPs with plen=-1)?

Mechanism sketch: Inadequacy worlds in non-chain domains where no existing structure suffices (verified by distance: no parent within K edits); run the recombination operator over non-chain fragments; track internal acceptance, execution success, persistence, reuse, and transfer to a new surface.

Expected result: Recombination produces a novel non-chain form that verifies, persists, and reuses; the final form is source-underdetermined (no researcher-enumerated candidate family contains it).

Simplest baseline: Fresh trial in the non-chain domain; chain-family recombination (current positive).

Falsifier: Recombination never produces a verifying non-chain form across 3/3 non-chain inadequacy families.

Likely failure mode: The fragment representation (m,start,len) assumes sequential structure; non-chain graphs are not fragment-addressable, so the operator cannot represent candidates at all; this would show the invention operators are chain-shaped and need a graph-native redesign.

Priority: P1.

### H-POLXFER-1: Does the consequence-taught policy transfer across contexts (rank #11)

Question: The adaptive policy beats both fixed gates on every seed with no threshold constant and no AND/OR combination. Is the learned policy reusable knowledge or context-fitted weights? Teach in context A (honest sources), move to context B (adversarial) with the policy intact vs reset.

Mechanism sketch: Two-phase lifetime; treatment carries the taught policy into phase B; control resets to the untrained policy at the phase boundary; a third arm carries the policy but freezes it (no further teaching). Measure adaptation speed and accuracy-per-cost in phase B.

Expected result: Carried unfrozen policy adapts faster than reset (policy structure transfers); carried frozen policy beats reset early but loses late (teaching still needed).

Simplest baseline: Reset policy at phase boundary (re-learn from scratch).

Falsifier: Carried policy performs no better than reset, or worse (negative policy transfer: phase A's cost structure must be unlearned first).

Likely failure mode: The policy encodes phase A's cost structure; in phase B it must unlearn before relearning, making transfer slower than fresh learning; the honest result bounds the policy to single-context lifetimes.

Priority: P1.

### H-SEAL2-1: Second adversarial seal on composition (rank #12)

Question: Sealed composition passed all ten kill bars with causal reuse proof (scalar transform X plus sequences Y to Z). Was the first seal accidentally easy? An independent adversary designs a second sealed battery post-freeze: new X/Y pairs, new Z goals, new surface forms.

Mechanism sketch: Freeze the current composition machinery; the adversary (who did not build it) designs three new X/Y/Z sealed worlds with a preregistered solvability check (a human-composed solution must exist and be executable); run 3/3 byte-identical; diagnose failures to the exact line.

Expected result: Either a second pass (generality evidence beyond the first seal) or a clean diagnostic failure naming the next mechanism gap.

Simplest baseline: The first seal (already passed).

Falsifier: The second seal fails in a way showing the first seal's X/Y were accidentally composable (shared surface structure the machinery exploited), downgrading the first pass to family-bounded.

Likely failure mode: The adversary designs a seal that is impossible in principle, producing an uninformative fail; seal validity needs its own preregistered solvability criterion or the exercise wastes a wave.

Priority: P1.

### H-INVLIVE-1: Hardened index invariants under learner-driven mutation (rank #13)

Question: H-INDEXADV-1 hardened the index against harness-injected corruption (cycles, bucket corruption, slot reuse). But the learner itself mutates the index on every insert/link/evict/slot-reuse path. Do the general invariants hold on the learner's own mutation paths under memory pressure?

Mechanism sketch: Long lifetime (500+ events) with eviction pressure forcing repeated learner-driven evict/reinsert cycles; assert the invariants (liveness, type checks, cycle detection, bounded buffers) on every mutation path; zero crashes and retrieval correctness required throughout.

Expected result: Zero crashes; invariant checks fire and recover on learner-generated edge cases; retrieval correctness maintained.

Simplest baseline: Harness-corruption battery (H-INDEXADV-1, already passed).

Falsifier: Any learner-driven mutation crashes or silently corrupts retrieval (the invariant is incomplete on the learner's own paths).

Likely failure mode: Learner mutation paths are a strict subset of harness-tested paths, so this passes trivially and adds no information; still worth one run as a guard before canonical promotion.

Priority: P2.

### H-SCALEADV-1: 1393x under adversarial query distributions (rank #14)

Question: C209 made 140x/693x/1393x canonical at 1000 MAPs on the standard workload. Is the reduction architectural or workload-dependent? An adversary designs worst-case queries post-freeze: largest-bucket hits, adversarial plen distributions, adversarial literal choices.

Mechanism sketch: Frozen index; two workloads (standard, adversarial); scale 100/500/1000 MAPs; measure verifies per query vs n for both; the claim holds if the adversarial curve stays sublinear.

Expected result: Graceful degradation (still strongly sublinear) rather than collapse to linear scan.

Simplest baseline: Standard workload (1393x at 1000 MAPs).

Falsifier: Adversarial queries collapse retrieval to linear scan (the 1393x is workload-dependent, and the honest claim must carry the workload restriction).

Likely failure mode: The index's worst case is genuinely linear and the adversary finds it immediately; still informative because it bounds the claim honestly, but it is a negative result on a canonical number.

Priority: P2.

### H-BASECERT-1: Pre-registered base-trial certification (rank #15)

Question: The K7 failure burned a full mechanism run on a base limitation: base TNN-2 trial could not solve problem 21 (ans=-2 vs trial=11). Should every meta-level experiment preregister a base-trial certification battery (all fixture problems solvable by base alone, 3/3 byte-identical) whose failure invalidates the fixture, not the mechanism?

Mechanism sketch: Governance experiment: take the next three meta-level preregs, add a certification gate (base-only 3/3 on every fixture problem before the mechanism run); measure certification catches vs wasted runs vs added cost.

Expected result: Certification catches base limitations before they burn mechanism runs; K7-style misattribution becomes impossible.

Simplest baseline: Current practice (no certification; K7 failed the mechanism for a base bug).

Falsifier: Certification passes but the base still fails mid-run on problems outside the certification set (certification is not predictive of base competence).

Likely failure mode: Certification doubles experiment cost (every fixture needs a base-only 3/3 run first); the governance overhead exceeds the waste it prevents, and workers skip it under time pressure.

Priority: P2.

### H-CATFORGET-1: Structure-type survival census under interference (rank #16)

Question: Composition LINK edges shield applicability, but what about the other learner-owned state types: reliability scores, utility values, induced grammar constraints, belief stances, threshold state? A 1000+ event interference lifetime with a census of each type before and after gives an empirical survival ranking.

Mechanism sketch: Lifetime with heavy interference; census LINK edges, reliability scores, utility values, grammar constraints, belief stances, and threshold state before/after; measure survival rate and post-interference competence attributable to each type (per-type ablation).

Expected result: A survival ranking that tells builders which learner-owned state is interference-robust and which needs protection; extends C189's 3-tier eviction with empirical data.

Simplest baseline: No-interference control (all types survive by construction).

Falsifier: All types survive equally (interference does not differentiate) or none survive (the lifetime is too hostile to be informative).

Likely failure mode: Survival correlates trivially with recency/frequency (LRU-like), adding nothing beyond standard caching theory; the census then just re-derives recency.

Priority: P2.

### Live frontier after this wave

Prior live: 41. New: 16 (all untested). Total live: 57. Requirement: 20+. Met with margin.

New untested: H-COLLAPSE-1, H-XIO-1, H-DECOMP-1, H-COMPVER-1, H-CAP-1, H-SHIELD-1, H-QUAR-1, H-GRAMZAG-1, H-DECEPT-1, H-INVNCH-1, H-POLXFER-1, H-SEAL2-1, H-INVLIVE-1, H-SCALEADV-1, H-BASECERT-1, H-CATFORGET-1.

### Treadmill check (Constitution 23)

H-COMPVER-1 is the repair follow-up to the H-COMPNOEXP-1 negative (T5): this is the one allowed retry with a structurally different acceptance mechanism (learner verification instead of expected matching), not a re-run of the failed design. H-CAP-1 re-opens the K-scaling question C208 closed on caps: allowed because the cap was a harness parameter, not a tested architectural limit. H-SEAL2-1 is the second seal: allowed because the adversary and worlds are fresh, not a re-run of the first seal.

No em dashes used (verified).
