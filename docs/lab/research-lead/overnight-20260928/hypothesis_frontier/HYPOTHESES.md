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
