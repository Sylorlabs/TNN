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
