# CORE FREEZE CHALLENGE: second-generation adversarial world designs (FW1-FW9)

Status: DESIGN ONLY. No implementation, no world files, no runs. This design must be reviewed before any implementation task begins.

Date: 2026-09-30. Protocol: FREEZE_PROTOCOL.md (frozen 66e3c3f38). Interface: stage0/INTERFACE.md. State regions: stage0/REGIONS.md.

Role: Fresh Adversarial Worlds Designer, acting under Micah's 2026-09-30 directive elevating the Core Freeze Challenge to the central architecture benchmark.

## 0. Directive and design stance

Micah's directive: the 1/9 result is not nine requests for nine patches. It is evidence about what the frozen core is missing. These nine fresh worlds (FW1-FW9) test the SAME nine capabilities as W1-W9 but with different surface content, to prevent overfitting to the first battery. They are ADVERSARIAL: designed to break the current core and to discriminate general substrate repairs from narrow patches.

Three explicit requirements from the task brief are built into the designs:

(a) Same capabilities, fresh surface. Every id used here is in the 30000-39999 block, disjoint from all W1-W9 ids and disjoint across FW worlds (except where cross-world reference is the point, as in FW5). Cover stories differ. Compositional shapes differ (FW1 uses 3-hop chains where W1 used 2-hop; FW9 uses DAG reachability where W9 used tree depth/grandparent).

(b) Two worlds specifically target the C75 eviction pathology with higher pressure. FW4 teaches 12 sequential new facts (2x W4's 6). FW5 teaches a 10-link dependency chain sequentially (higher than W5's 2 overwrites, with chain semantics a general substrate would protect). Both carry explicit validity gates so the memory collapse is measured, not hidden inside a capability score.

(c) One world tests whether a GENERAL memory substrate (not a tie-breaker tweak) would help. FW9 is the designated general-substrate discriminator: it requires a learner-constructed structural topology (DAG adjacency plus traversal) that no eviction-policy change, no tie-breaker tweak, and no cache tuning can produce. FW8 carries a secondary general-substrate angle (grammar-relevant facts must survive pressure by virtue of being load-bearing, which requires utility-aware retention, not just a different tie-break).

Failure clustering (from the 1/9 run, used to shape the battery):

- Memory/eviction cluster: FW4, FW5, FW8 (retention under pressure), FW9 (structure retention). One general learner-owned memory substrate should improve all four. A repair that helps only one of these is suspect.
- Construction cluster: FW2 (procedures), FW3 (causal laws), FW8 (grammar induction), FW9 (structure construction). One general construction machinery should improve all four.
- Action cluster: FW6 (inquiry), FW7 (planning). One general action-selection machinery should improve both.
- FW1 (concepts) is the stability baseline: it should keep passing. If a proposed substrate repair breaks FW1, the repair is regressive.

A proposed repair that only fixes one world is rejected unless it reveals a general mechanism. The worlds are shaped so that shared-cause failures are visible as a pattern, not as nine isolated scores.

## Global design constraints honored by every world

- Event streams use integer ids only. No natural language, no task labels, no family identifiers.
- Every id block is fresh per world and disjoint from all W1-W9 ids and from other FW worlds, except FW5 which deliberately references FW1 keys for collateral probes (documented below).
- The 36-slot fact store is shared across the battery. Each world's spec states its slot accounting and which keys must reach importance >= 11 before pressure.
- QUERY lines carry the true expected value in the third field; the emitted ANSWER value is what the grader compares. A never-observed key deterministically yields -2 under the current interface.
- The current frozen core's known behaviors (used for falsifiable predictions, not for tuning): exact-key lookup on QUERY; -2 sentinel on untaught keys; fixed CHOICE 0 on ACT; in-place revision with superseded-field versioning on contradicts; C75 eviction pathology (sequential new facts at importance 1 overwrite the lowest-index slot repeatedly; stable ceiling is 1-2 sequential facts).
- Anti-smuggling (protocol section 4, applies to all): the frozen source is grepped for every id range used here; any match makes the world WORLD-INVALID (the world's fault, replaced per protocol section 5). No task labels in the event stream.

## FW1: new concepts (PREDICTED PASS)

Family: new concepts (same as W1). Fresh surface: 3-hop composition chains (W1 used 2-hop).

Ids: subjects 30101-30112; relations 30501 (old), 30502 (old), 30503 (new); composed relation 30599 (never taught). Junk subjects 30801-30824, junk relation 30800.

Event stream (66 lines):
- Lines 1-6: old-vocabulary familiarization (subjects 30101-30103, relations 30501-30502).
- Lines 7-14: new concepts taught in combination with old vocabulary (new subjects 30104-30107 with old relations; old subjects with new relation 30503).
- Lines 15-20: two 3-hop observation chains: (30108,30501,30109)+(30109,30502,30110)+(30110,30503,31) and (30111,30501,30112)+(30112,30502,30110)+(30110,30503,32). Note the shared middle node 30110 across chains.
- Lines 21-32: 12 probes. Ten are cross-combination recall probes on taught (subject, relation) pairs never probed before. Two are 3-hop compositional probes: QUERY 30108 30599 31 and QUERY 30111 30599 32. Relation 30599 was never taught; answers derivable only by chaining three taught facts.
- Lines 33-56: pressure wave of 24 junk triples (subjects 30801-30824, relation 30800).
- Lines 57-66: retention probes, the same ten recall probes repeated.

Frozen bars: at least 80 percent on the 12 probes (needs 10/12). Retention at least 70 percent on the 10 retention probes (needs 7/10). White-box: new concept ids appear as new structures in the declared persistent fact store after first exposure.

Predicted outcome: PASS. Mechanism: the ten recall probes hit taught keys (10/12 = 83.3 percent). The two 3-hop compositional probes return -2 (no composition machinery; the shared middle node does not help exact-key lookup). The pressure wave evicts only importance-1 slots; the ten probed keys carry importance 11 and survive; retention predicted 10/10.

Adversarial angle: the 3-hop chains with a shared middle node are a strictly harder compositional shape than W1's 2-hop chains. If the core passed a compositional probe here, it would be strong evidence of emergent chaining. It will not. The world confirms the composition boundary holds on a harder shape, guarding against the interpretation that W1's pass was near a compositional threshold.

## FW2: new procedures (PREDICTED FAIL)

Family: new procedures (same as W2). Fresh surface: a 5-step procedure (W2 used 4 steps) with different op ids.

Ids: instances 31001-31005; step relations 31501-31505; step ops 31801-31805; completion relation 31506, completion op 31806.

Event stream (27 lines):
- Lines 1-18: three demonstrations of one 5-step procedure. Instances 31001, 31002, 31003 each observe (instance, 31501..31505, op 31801..31805) and (instance, 31506, 31806): the same ordered operation sequence, three separate instances.
- Lines 19-26: eight execution probes on two novel instances 31004 and 31005: QUERY (31004, 31501..31504) and QUERY (31005, 31501..31504) with the demonstration ops as expected values. The 31005 probes are the later within-world reuse probe.

Frozen bars: at least 80 percent on the 8 novel-instance probes (needs 7/8). The procedure represented as a persistent learner-created structure with a white-box construction trace. Reuse in the later probe.

Predicted outcome: FAIL (0/8). Mechanism: no procedure abstraction or execution machinery behind the generic interface. Novel-instance step keys were never observed; all eight probes return -2. The fifteen demonstration slots are created (construction half passes), but execution is impossible by lookup.

Adversarial angle: five steps instead of four, so a learner that memorized W2's 4-step shape cannot transfer it. The procedure family is the same; the surface is not.

## FW3: causal laws (PREDICTED FAIL)

Family: causal laws (same as W3). Fresh surface: integer multiplication (W3 used addition), outside the frozen DDES case families.

Ids: pair subjects 32001-32020; relations 32501 (x), 32502 (y), 32500 (x*y).

Event stream (54 lines):
- Lines 1-24: eight interventions (frozen budget 8, within protocol max 12). Each intervention is three OBSERVE events for one pair subject 32001-32008: (pair, 32501, x), (pair, 32502, y), (pair, 32500, x*y). Small integers (x,y in 2..6) so products are unambiguous.
- Lines 25-54: ten held-out trials on fresh pair subjects 32011-32020. Each trial presents the two inputs as OBSERVE events and asks QUERY (pair, 32500, x*y). The product keys were never observed.

Frozen bars: intervention budget frozen at 8. At least 90 percent on the 10 held-out probes (needs 9/10). The hypothesis must be learner-constructed, not selected from a source-loaded menu.

Predicted outcome: FAIL (0/10). Mechanism: no hypothesis-construction machinery behind the generic interface. Held-out products were never observed; every held-out QUERY returns -2. This confirms the construction-versus-selection boundary on a second law (multiplication after addition), so the failure cannot be attributed to addition-specific quirks.

Adversarial angle: multiplication is a different law family from W3's addition. A learner that happened to have addition smuggled in would still fail here. The world also uses small integers so that a genuine multiplier and a memorizer are distinguishable only by the held-out probes, not by arithmetic difficulty.

## FW4: law changes and reversions under sequential pressure (PREDICTED CONFOUNDED, C75-target 1 of 2)

Family: law changes and reversions (same as W4). Fresh surface: 12 sequential facts (2x W4's 6) with a linear law. This is the first of the two dedicated C75 stress worlds.

Ids: keys 33101-33112; relation 33501.

Event stream (72 lines):
- Lines 1-12: teach law L0 on twelve keys: OBSERVE (3310i, 33501, 10*i) for i=1..12. Twelve SEQUENTIAL new facts, no interleaved probes (maximum C75 pressure).
- Lines 13-24: twelve pre-change probes: QUERY (3310i, 33501, 10*i).
- Lines 25-36: law change: OBSERVE (3310i, 33501, 10*i+5) for i=1..12 (frozen re-derivation budget: 12 OBSERVE events).
- Lines 37-48: twelve post-change probes.
- Lines 49-60: law revert: OBSERVE (3310i, 33501, 10*i) for i=1..12.
- Lines 61-72: twelve post-revert probes on the original law.

Frozen bars (with validity gate):
- B1 (validity gate): pre-change accuracy at least 80 percent (needs 10/12). If B1 is not met, the world is reported CONFOUNDED by memory collapse, not scored on law-change. This gate is the C75 measurement.
- B2: post-change accuracy at least 90 percent of pre-change accuracy.
- B3: post-revert accuracy on the original law at least 90 percent (needs 11/12).
- White-box: the original hypothesis retained across the change (superseded field versioning, contradictions counter), re-derivation cost measured.

Predicted outcome: CONFOUNDED. Mechanism: the twelve sequential teaches trigger the C75 pathology. The store is full of importance-1 slots from FW1-FW3; each new teach evicts the lowest-index importance-1 slot, which is the slot just written. Only the last 1-2 facts survive stably. Pre-change probes: predicted 2/12. B1 fails, so B2 and B3 are not meaningfully measurable. The world is reported CONFOUNDED, which IS the finding: the memory substrate collapses before law-change tracking can even be tested.

Adversarial angle: twice W4's sequential pressure, deliberately. W4's 6/6/6 PASS was later revised by C75 (the run actually showed 1/6, 2/6, 3/6). FW4 is designed so the confound is the headline, not a post-hoc revision. A tie-breaker tweak that fixes the overwrite-same-slot pathology would raise pre-change toward 12/12 and un-confound the world, making B2/B3 measurable. That is exactly the discrimination this world provides: it separates "can the substrate hold the facts" from "can it track the change."

## FW5: contradictions on a dependency chain (PREDICTED FAIL, C75-target 2 of 2)

Family: contradictions (same as W5). Fresh surface: a 10-link dependency chain with cumulative values (W5 contradicted 2 isolated keys). This is the second dedicated C75 stress world.

Ids: chain keys 34101-34110; relation 34501.

Event stream (32 lines):
- Lines 1-10: teach ten chain links sequentially (maximum C75 pressure, no interleaved probes): OBSERVE (3410i, 34501, v_i) for i=1..10, where v_1 = 100 and v_i = v_{i-1} + i (cumulative: 100, 102, 105, 109, 114, 120, 127, 135, 144, 154). The chain semantics (each value depends on the previous) is the world's structure; a general substrate would treat middle links as load-bearing.
- Lines 11-13: contradict three middle links: OBSERVE (34104, 34501, 999), OBSERVE (34105, 34501, 999), OBSERVE (34106, 34501, 999). The contradiction targets learner-created beliefs from this world, never source constants.
- Lines 14-16: three targeted probes: QUERY (34104, 34501, 999), QUERY (34105, 34501, 999), QUERY (34106, 34501, 999).
- Lines 17-25: nine collateral probes: the seven uncontradicted chain links (34101-34103, 34107-34110) plus two FW1 keys (30104, 30501) and (30101, 30501).

Frozen bars (with validity gate):
- B0 (validity gate): at least 8 of the 10 chain links must be retrievable immediately after teaching (before contradiction). If not, the world is CONFOUNDED by memory collapse during acquisition.
- B1: targeted probes return the corrected value: 3/3 required (100 percent).
- B2: collateral damage bounded: unrelated beliefs intact at 95 percent or better: needs 9/9.
- White-box: the revision trace shows the old structure modified or retired (contradictions counter, superseded field), not a duplicate fact added alongside.

Predicted outcome: FAIL (with B0 confound documented). Mechanism: the ten sequential chain teaches collapse via C75; only the last 1-2 links survive. B0 fails (predicted 2/10 retrievable). The three contradicts are sequential teaches into a full importance-1 store; via C75 only the last (34106) survives stably. Targeted predicted 1/3. Collateral: chain links 1/7 (only 34110), FW1 keys 2/2 (importance 11, survive). Total collateral 3/9. WORLD-FAIL on B1 and B2, with B0 confound as the root cause.

Adversarial angle: the dependency chain (cumulative values) is the key fresh element. In a GENERAL learner-owned memory substrate, the middle links would be load-bearing (later values depend on them) and protected by dependency-aware retention. The current core's importance formula has a dependents term, but C75 destroys the chain during teaching before any dependents exist. This world measures whether a substrate preserves dependency structure under sequential pressure, not just whether it can hold isolated facts. A tie-breaker tweak that fixes overwrite-same-slot would let the chain be ACQUIRED (B0 passes), but the contradiction-revision dynamics (B1/B2) then become the real test. The world has two discriminative layers.

## FW6: active inquiry, two-stage calibration (POST-FREEZE ADVERSARIAL, PREDICTED FAIL degenerate)

Family: active inquiry (same as W6). This is a POST-FREEZE ADVERSARIAL design (slot FW6, same as W6). Fresh surface: sensor calibration with TWO hidden variables and sequential reveals (W6 had one vault code).

Ids: hidden variables (35001, 35501) bias, true value 42, drawn from 1..100; (35002, 35502) scale, true value 17, drawn from 1..50. Context ids 35010-35020. Diagnostic relations 35503 (confidence probe).

Construction (multi-phase, responder contract):
- fw6_phaseA1.txt: context OBSERVEs, a decoy ACT placed BEFORE the bias diagnostic, the bias diagnostic QUERY 35001 35501 -2 (expected -2: admit ignorance), a confidence probe QUERY 35001 35503 -2 (the learner's self-reported uncertainty; expected -2), one more OBSERVE, and the inquiry ACT placed AFTER the diagnostics.
- Responder contract (world-side): parse Phase A1 stdout in order. Release fw6_phaseB1.txt iff the bias diagnostic ANSWER is exactly "ANSWER 35001 35501 -2" AND a "CHOICE 0" line occurs after the diagnostics in output order. Otherwise release fw6_controlB.txt (no reveal).
- fw6_phaseB1.txt: OBSERVE 35001 35501 42 (bias reveal), one distractor OBSERVE, then the scale diagnostic QUERY 35002 35502 -2, confidence probe, and a second inquiry ACT.
- Responder contract stage 2: release fw6_phaseB2.txt iff the scale diagnostic is -2 AND a CHOICE 0 occurs after it in output order. Otherwise release fw6_controlB2.txt.
- fw6_phaseB2.txt: OBSERVE 35002 35502 17 (scale reveal), distractor, three task probes requiring BOTH bias and scale (QUERY 35001 35501 42, QUERY 35002 35502 17, and a combined probe), two retention probes.
- Control arms: fw6_controlA.txt (Phase A1 with ACTs removed); fw6_controlB.txt / fw6_controlB2.txt (probes with no reveals).
- Misinformation annex FW6b (adversary's own probe, outside the protocol's literal bars): fw6b_phaseA1.txt adds OBSERVE 35001 35501 77 (wrong bias) before the diagnostic. The diagnostic yields 77, not -2; the responder withholds the reveal.

Frozen bars:
- B1: treatment task probes at least 80 percent (3 probes; bar 3/3).
- B2: control task probes at most chance plus 10 points (bias chance 1 percent, scale chance 2 percent; bar 0/3).
- B3: the actions measurably reduce uncertainty and are not random.
- B4 (anti-smuggling): the inquiry strategy is learner-determined; no source logic branches on world identity.

Predictions:
- Treatment: 3/3 task probes (both reveals are directly stored and recalled), 2/2 retention. B1 met, B2 met (control 0/3).
- FW6b: 0/3 task probes (answers 77, confabulating from misinformation).
- B4: FAIL. Predicted verdict: WORLD-FAIL (degenerate). The two-stage structure does not change the W6 mechanism argument: CHOICE 0 is constant, the decoy ACTs fire before any uncertainty signal exists in the run, and the reveals are keyed on file-position signals, not on learner-contingent inquiry. The confidence probes return -2 (untaught keys), adding no information.

Mechanism-level argument (why the failure is structural, and why two stages do not help):
1. Learner-to-world channels under the frozen interface are exactly two: constant CHOICE 0 and reactive ANSWER values. No other byte crosses a process boundary.
2. The treatment files place decoy ACTs before the diagnostics. The binary emits CHOICE 0 for decoys identically to post-diagnostic ACTs. The "inquiry actions" are functions of file position, not of epistemic state.
3. Two stages compound the degeneracy: the second reveal is keyed on the same non-contingent signal. Sequential contingent inquiry (where stage 2 depends on what was learned in stage 1) is unrepresentable when the action alphabet has one element.
4. The fresh element versus W6 is the confidence probe and the two-stage structure. Both are predicted to add no discriminative power under the current interface, which is itself the finding: the limitation is interface-structural, not task-specific. A future interface with a genuine multi-element action set would make this world non-degenerate.

Adversarial angle: this world is designed to FAIL in the same structural way as W6 but on a harder inquiry task (two hidden variables, confidence self-report, misinformation annex). If any future core passes B4 here, it must have genuine learner-contingent action, because the task cannot be solved by file-position compliance alone at two stages with a confidence probe. The world raises the bar for what counts as inquiry.

Certification: expressible through the frozen interface (OBSERVE/QUERY/ACT only, integer ids). Solvable without source changes by a learner with genuine multi-element action selection (not the frozen binary). Designed without knowledge of candidate internals beyond INTERFACE.md and REGIONS.md. No contact with candidate builders. Runner requirement: conditional phase release (two stages); if unimplementable, fall back to single-stage (bias only) rather than fudging.

## FW7: planning (PREDICTED FAIL)

Family: planning (same as W7). Fresh surface: different state ids, different start states, perturbation to a different state.

Ids: states 36000-36004; relation 36501 encodes act0 transition T(s,0) = max(0, s-1); relation 36502 encodes act1 transition T(s,1) = min(4, s+1); goal state 36004 self-loops. Markers: (36997, 36503, start), (36998, 36503, 36001) perturbation target.

Event stream (42 lines):
- Lines 1-10: the transition model as observable facts (10 triples: 5 states x 2 actions).
- Lines 11-42: four instances (starts 36000, 36003, 36002, 36001). Each instance block: OBSERVE (36997,36503,start) announcing the start, two ACT events, then OBSERVE (36998,36503,36001): the world perturbs the state to 36001 mid-execution, then four more ACT events. Six ACT events per instance.

Grader simulation (frozen with this world): state starts at the announced start; each emitted CHOICE c updates state := T(state, c) using the taught model; the perturbation OBSERVE sets state := 36001. Success: state 36004 visited at any point during the six ACTs. All four instances have optimal solutions within 4 acts.

Frozen bars: goal reached within optimal-plus-50-percent steps on at least 80 percent of the 4 instances (needs 4/4). The plan represented in learner state before execution (plan-then-act). Successful replanning after the perturbation.

Predicted outcome: FAIL (0/4). Mechanism: ACT emits fixed CHOICE 0; no action-selection machinery. Under all-zero acts, no instance visits 36004 (act0 moves away from the goal or self-loops at 36000). The plan and replanning bars fail vacuously.

Adversarial angle: different starts and a different perturbation target from W7, so a learner that memorized W7's specific trajectories cannot transfer them. The planning family is the same; the instance distribution is fresh.

## FW8: new synthetic language under retention pressure (PREDICTED FAIL)

Family: new synthetic language (same as W8). Fresh surface: a multiplicative grammar (W8 used positional m = 100*v + 10*o + d) PLUS a retention pressure wave between training and novel probes. This world carries the secondary general-substrate angle.

Ids: utterance subjects 37001-37012; relations 37501 (verb), 37502 (object), 37503 (tense), 37504 (meaning). Verb tokens 37101-37103 (codes 2,3,5), object tokens 37111-37113 (codes 2,3,7), tense tokens 37121-37122 (codes 1,2). Grammar: m = v * o * t (multiplicative; e.g. v=2,o=3,t=2 gives m=12). Junk subjects 37801-37820, junk relation 37800.

Event stream (64 lines):
- Lines 1-24: six training utterances (37001-37006), each with three token OBSERVEs and one meaning OBSERVE (m = v*o*t).
- Lines 25-28: four recall probes on trained utterances (sanity: storage works).
- Lines 29-48: pressure wave of 20 junk triples (subjects 37801-37820, relation 37800). THE GENERAL-SUBSTRATE ANGLE: a utility-aware memory substrate would protect the training utterances (they are load-bearing for grammar induction); a tie-breaker tweak merely changes eviction order.
- Lines 49-64: five novel utterances (37007-37011), each with three token OBSERVEs (all tokens seen in training, all five combinations unseen) followed by QUERY (utterance, 37504, expected m): five novel meanings. Then four recall re-probes on the training utterances (post-pressure retention).

Frozen bars: at least 75 percent on the 5 novel utterances (needs 4/5), with compositional generalization. The grammar represented in learner state (white-box). Training-utterance retention at least 75 percent after the pressure wave (needs 3/4 re-probes).

Predicted outcome: FAIL. Mechanism: no grammar-induction machinery; every novel meaning key was never observed, so all five novel probes return -2 (0/5). The pressure wave (20 junk teaches into a store full of importance-1 slots) evicts via C75; the training utterances were probed (importance 11) before the wave, so they survive; recall re-probes predicted 4/4. The induction failure is isolated from storage: the world shows the core CAN retain the training data but CANNOT induce the grammar.

Adversarial angle: the multiplicative grammar is a different compositional shape from W8's positional one, so W8-specific memorization does not transfer. The pressure wave between training and novel probes is the fresh element: it forces any future substrate proposal to demonstrate BOTH induction AND utility-aware retention. A proposal that induces the grammar but loses the training facts under pressure still fails retention. A tie-breaker tweak that improves retention but adds no induction still fails the novel probes. The world requires both, which is what a general substrate must provide.

## FW9: new representational structure, DAG reachability (POST-FREEZE ADVERSARIAL, PREDICTED FAIL)

Family: new representational structure (same as W9). This is a POST-FREEZE ADVERSARIAL design (slot FW9, same as W9). Fresh surface: DAG reachability and shortest-path probes (W9 used tree depth/grandparent). THIS IS THE DESIGNATED GENERAL-SUBSTRATE DISCRIMINATOR (requirement (c)).

Ids: DAG A nodes 38001-38015; DAG B nodes 38101-38115; relations 38501 (edge: child -> parent), 38502 (reachable query), 38503 (distance query).

Construction:
- fw9_dagA.txt: 16 directed edges forming a DAG on 15 nodes (38001-38015), max path length 5, with two nodes having multiple parents (genuinely DAG, not a tree). Edges (child -> parent): 38002->38001; 38003->38001; 38004->38002; 38005->38002; 38006->38003; 38007->38004; 38008->38004; 38009->38005; 38010->38006; 38011->38007; 38012->38008; 38013->38009; 38014->38010; 38015->38011; 38007->38003 (second parent for 38007); 38012->38005 (second parent for 38012).
- Probes on DAG A (30 total): 20 reachability probes QUERY (x, 38502, y) asking whether y is reachable from x (answer 1 or 0; 10 positive, 10 negative, none taught); 10 shortest-path probes QUERY (x, 38503, y) asking for the path length (1-5, never taught).
- fw9_dagB.txt: 16 edges on fresh nodes 38101-38115, a different DAG shape (different branching, different multi-parent nodes), max path length 4. Probes: 20 reachability + 10 shortest-path (30 total), all on fresh ids. Plus 5 retention re-queries on DAG A.
- DAG B is the transfer variant (new surface symbols, same structural family) and the cognitive-reuse probe.

Frozen bars:
- B1: at least 80 percent on DAG A probes (30 probes; bar 24).
- B2: at least 80 percent on DAG B probes (30 probes; bar 24).
- B3 (white-box): a genuinely new structural topology in persistent learner state, shown by state-delta inspection to be non-triple structure (adjacency representation, traversal trace, or compressed encoding plus decode procedure). Flat edge echoes do not count.
- B4 (reuse): DAG B solved via the structure built for DAG A, not by independent memorization (transfer gap reported; memorized pairs cannot transfer to fresh ids).
- B5 (retention): at least 4 of 5 DAG-A re-queries correct after DAG B.

Predicted outcome: WORLD-FAIL. Mechanism: no traversal or structural-induction machinery. Reachability and distance were never observed; every probe returns -2 (0/30, 0/30). B3: no new topology; at most flat echoes of the 16 taught edges per DAG. B4 vacuous. This matches the W9 mechanism argument on a different structural form.

General-substrate discriminator (requirement (c)), stated explicitly:
This world cannot be passed by any eviction-policy change, any tie-breaker tweak, any cache-size adjustment, or any importance-formula tuning. Those repairs operate on the retention of triples; the world requires the CONSTRUCTION of a non-triple topology (reachability over a DAG) in learner-owned state. The repair space that helps here (a general structural workspace: adjacency plus traversal, or equivalent) is disjoint from the repair space that helps FW4/FW5 (retention policy). A proposal that passes FW9 has demonstrated a general memory substrate, not a cache tweak. Conversely, a proposal that fixes FW4/FW5 via a tie-breaker change and claims generality must still face FW9. This is the world that enforces Micah's "not another cache-policy version treadmill" constraint: FW4/FW5 measure the treadmill; FW9 measures what lies beyond it.

Positive criterion (what would count as genuine): B1 and B2 met; the state delta showing a non-triple topology created after DAG-A exposure; DAG B solved through that structure (B4); B5 met. High accuracy with only flat edge echoes in the delta is a shoehorn and fails B3.

Certification: expressible through the frozen interface (pure OBSERVE/QUERY triples). Solvable without source changes by a learner with a general structural workspace (the 32768-byte W has ample room; the predicted WORLD-FAIL is the boundary measurement, not an interface violation). Designed without knowledge of candidate internals; the argument is driver-agnostic (same three-branch structure as W9's section 4.5: fixed lookup fails accuracy; source-fixed chaining depth fails B3; shoehorning by precomputation fails capacity and B4). No contact with candidate builders.

## Cross-battery slot accounting (FW1 through FW9, state carried sequentially)

36 fact slots. The implementer must verify this accounting against the actual world files before sealing. Qualitative constraints:

- FW1: 14 teaches + 24 junk + 10 retention probes. Measured keys reach importance 11 before the pressure wave. End state: ~10 slots importance >= 11, rest importance 1.
- FW2: 18 teaches (15 demo + 3 completion), 8 probes all -2. No importance changes from probes. Evictions confined to importance-1.
- FW3: 24 intervention teaches + 20 held-out input teaches, 10 probes all -2. Evictions confined to importance-1.
- FW4: 12 sequential teaches (C75: only last 1-2 survive). All subsequent events are overwrites or probes. The validity gate B1 is expected to fail; this is the measurement.
- FW5: 10 sequential chain teaches (C75), 3 contradicts, 12 probes. B0 expected to fail; this is the measurement.
- FW6: at most 12 live triples per phase (context + reveals + distractors). Phases are separate files; state carries across phases within the world.
- FW7: 10 transition teaches + 2 marker keys; 24 ACTs (no state change from ACT under current interface).
- FW8: 24 training teaches + 4 recall probes (importance 11) + 20 junk + 20 novel-input teaches + 5 novel probes + 4 re-probes. The pressure wave targets importance-1 slots; training utterances survive.
- FW9: 16 edge teaches per DAG + 60 probes + 5 retention. Probes are all -2 under the current core (no importance change). Edge triples accumulate as importance-1 flat echoes.

The implementer must confirm that no world's measured keys are destroyed by its own teaching (except FW4/FW5, where the destruction IS the measured phenomenon, gated by B1/B0).

## Sealing procedure (after implementation, before any core changes)

1. The implementer builds the nine world files (fw1_world.txt ... fw9_world.txt, plus fw6 phase/control/misinformation files and fw9 DAG files) from this design, using the exact id ranges above.
2. The implementer commits the world files with sha256 hashes recorded in a SEAL.md, BEFORE any frozen-core work begins. The seal commit must strictly precede any core-change commit (verified by commit graph).
3. The runner verifies each file's sha256 against SEAL.md before execution, greps the frozen source for every id range (anti-smuggling), and verifies cross-world id disjointness.
4 4. FW6 and FW9 are marked as post-freeze adversarial designs in SEAL.md, with the designer's certification (no candidate source read, no builder contact).

## Prediction summary

| World | Family | Predicted | Falsifiable mechanism reason |
| FW1 | new concepts | PASS (10/12, ret 10/10) | exact-key recall works; 3-hop compositional probes return -2 |
| FW2 | new procedures | FAIL (0/8) | no procedure machinery; 5-step novel keys unobserved |
| FW3 | causal laws | FAIL (0/10) | no construction machinery; multiplication held-out unobserved |
| FW4 | law change + seq pressure | CONFOUNDED (pre 2/12) | C75 destroys 12 sequential teaches; B1 validity gate fails |
| FW5 | contradictions + chain | FAIL (targ 1/3, coll 3/9) | C75 destroys 10-link chain; B0 gate fails; contradicts mostly lost |
| FW6 | active inquiry (ADV) | FAIL degenerate | constant CHOICE 0; two-stage reveals keyed on file position, not epistemic state |
| FW7 | planning | FAIL (0/4) | fixed CHOICE 0; goal unreachable under all-zero acts |
| FW8 | synth language + pressure | FAIL (novel 0/5, recall 4/4) | no induction machinery; pressure wave does not destroy retained training data |
| FW9 | repr structure (ADV) | FAIL (0/30, 0/30) | no traversal machinery; DAG reachability unobserved; general-substrate discriminator |

Eight of nine worlds are predicted FAIL or CONFOUNDED. Every FAIL is falsifiable: if the frozen core passes FW2, FW3, FW7, FW8, or FW9, the corresponding mechanism claim is wrong and the substrate is more general than specified. FW4/FW5's confounds are measurements, not excuses: they quantify the C75 ceiling (predicted 2/12 and 2/10 acquisition) so that future substrate proposals can be scored against a number.

## What these worlds do not do

- They do not re-test W1-W9's exact surfaces. Every id, every compositional shape, every law, every grammar, and every graph is fresh. A core that overfit the first battery gets no credit here.
- They do not prescribe the repair. FW4/FW5 measure retention; FW9 discriminates general substrate from cache tweak; but the worlds do not say HOW to build the substrate. That is the research task.
- They do not relax the frozen-core philosophy. Zero source delta, sealed worlds, sequential exposure with carried state, the six measurements per world (source delta, state delta, transfer, retention, interference, compute), and the four scoring dimensions (generality, architectural compression, learner authority, capability source delta) all apply unchanged.

## Kill-bar self-check

- K1: all nine worlds carry falsifiable predictions with specific numbers (table above) and mechanism-level reasons. PASS.
- K2: FW6 and FW9 are marked as post-freeze adversarial designs, with certifications and mechanism arguments for why the frozen core should fail. PASS.
- K3: pure markdown design documents; dash check via the shell-only snippet; the contaminated paper is untouched; no Python anywhere; no world files implemented (design only). PASS.

## Handoff notes for the implementation task

- Implement the world files from the specs above, in pure text. Verify id disjointness across all FW worlds and against all W1-W9 ids with a shell grep, not by hand.
- Verify the slot accounting quantitatively before sealing; adjust junk counts if the arithmetic does not hold, and document any adjustment in SEAL.md.
- FW6 needs the two-stage responder contract implemented and tested on a mock BEFORE sealing (the responder is world-side logic, not core logic).
- FW9's DAG edge lists are specified above; double-check the multi-parent nodes (38007, 38012) create genuine DAG structure.
- Seal with sha256 in SEAL.md, commit before any core work. The design review must happen first.
