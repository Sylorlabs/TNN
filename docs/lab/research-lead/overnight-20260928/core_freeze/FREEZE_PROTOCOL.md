# CORE FREEZE CHALLENGE: protocol

Status: PROTOCOL-FROZEN (design only). No implementation, no builds, no runs under this protocol before this document is committed.
Date: 2026-09-30. Standing authority: the ONE-SYSTEM RULE directive of 2026-09-30.

## 1. Purpose

The CORE FREEZE CHALLENGE is the top-priority research program for deciding whether TNN is converging on one general cognitive substrate or on a collection of subsystems. One cognitive TNN binary is frozen. After the freeze commit, the learner faces sealed worlds with zero cognition-source changes. A capability obtained with zero source delta is architecturally far more important than another subsystem passing its own benchmark.

This document is the preregistration for the challenge. It defines the freeze, the world battery, the adversary handoff, the measurements, the verdict mapping, and the honest-scope predictions. Nothing in it is a result.

## 2. Freeze definition

### 2.1 What is frozen (cognition source)

Cognition source is everything that determines how the learner thinks, as opposed to what it has learned:

- Every source file compiled into the binary (the .zag files, including any embedded drivers, loaders, and world-interface plumbing).
- The build command and flags used to produce the binary.
- The pinned toolchain identity (znc binary sha256, recorded for provenance; the toolchain is not part of cognition source but its identity is recorded so the build is reproducible).

### 2.2 What is mutable (learner state)

Learner state is the declared persistent byte region(s) the binary reads and writes across worlds. The freeze worker must declare, in the freeze commit, the exact byte ranges that constitute persistent learner state versus transient scratch. Only declared persistent regions may carry information from one world to the next. Scratch must be cleared or provably irrelevant between worlds.

The learner may change: persistent state bytes, and nothing else. It may not change: code, handlers, semantic cases, modes, the world interface, or the build.

### 2.3 Freeze verification procedure (mechanical)

At the freeze commit, the freeze worker records in FREEZE_RECORD.md:

- sha256 of every cognition-source file.
- sha256 of the frozen binary, built twice from the frozen source; the two builds must be byte-identical or the freeze is void.
- sha256 of the initial learner state (the null-world state, see 3.3).
- The world-interface specification (see 3.1).
- The persistent-state region declaration (see 2.2).

After every world, and after the full battery, the challenge runner recomputes sha256 of the source files and the binary and compares against FREEZE_RECORD.md. Any mismatch halts the battery immediately and the challenge verdict is FREEZE-CHALLENGE-VOID (section 7). There is zero ambiguity: equality of hashes is the entire test. Verification uses shell and sha256sum only.

## 3. Freeze-readiness gate (Stage 0, pre-freeze)

The current freeze candidate (the composed continuing learner at dc20745db, LEARNER-REVERT-PASS) cannot be frozen as committed: its main() runs a hardcoded P1-P11 episode script and it has no channel through which a sealed world could reach it. Freezing it as-is would make the challenge unexecutable. Stage 0 is therefore mandatory pre-freeze work, disclosed in full, and is not counted against the zero-source-delta requirement (the delta is measured from the freeze commit, not from dc20745db).

### 3.1 The world interface (frozen at freeze time)

The freeze worker must give the binary a world-input interface meeting these functional requirements:

- Task-agnostic event stream. The binary accepts an ordered sequence of events. Each event is one of: OBSERVE (facts the world presents), ACT (the world offers a choice among a generic action set; the binary emits its choice), QUERY (the world asks a question in the generic encoding; the binary emits an answer). The encoding uses integer ids only. No natural language, no task labels, no field identifying which of the 9 families a world belongs to.
- Generic action set. The same actions are available in every world. World-specific action semantics are conveyed only through OBSERVE events, never through new interface verbs.
- State persistence across worlds. The binary must carry its declared persistent state from one world to the next, either as a long-lived process or via a frozen save/load mechanism. The mechanism is part of the frozen interface.
- Fixed output format. Predictions, actions, and answers are emitted in a fixed generic format defined in the interface spec.

The interface is I/O plumbing, not cognition. Its addition must not introduce cognitive handlers, semantic cases, or modes; the freeze worker discloses the interface diff and a reviewer confirms it is plumbing only. The interface spec is committed at freeze and is itself frozen.

### 3.2 State declaration

The freeze worker declares the exact persistent regions (byte ranges) and the scratch discipline. Any byte outside the declared persistent regions that influences behavior across worlds is a freeze violation.

### 3.3 Null-world run

Before freeze, the binary must complete a null-world run (empty event stream): it runs deterministically and its persistent state equals the recorded initial state. This proves the interface adds no hidden behavior.

### 3.4 Readiness verdict

Stage 0 ends with READINESS-[PASS/FAIL]. FAIL with a written reason is itself a finding: if the substrate cannot accept a task-agnostic world stream without new cognitive handlers, the substrate is not freezable, and that is reported honestly rather than worked around.

## 4. The 9-world battery

Worlds are presented sequentially, W1 through W9, to the same learner with persistent state carried across. Each world specification below is functional, not an implementation. Each world includes: what the learner experiences, frozen success bars, and the anti-smuggling criterion (what proves the capability came from learner-created state rather than a smuggled handler).

General anti-smuggling provisions applying to all worlds:

- Source audit: the frozen source is grepped for each world's vocabulary, symbols, and structural signatures. Any match makes the world INVALID (the world's fault, not the learner's; see section 7).
- No task labels anywhere in the event stream.
- The world designers (pre-freeze team and post-freeze adversary) certify they have not seen the candidate's source and have had no contact with the candidate builders about world content.

### W1: new concepts

Experience: the world introduces entities and relation types whose integer ids never appeared before. The learner observes facts using them, then faces compositional queries combining new concepts with old ones.
Frozen bars: at least 80 percent correct on held-out compositional queries using the new concepts; the concepts are represented in declared persistent learner state (white-box: new structures created after first exposure, not echoed input); retention at least 70 percent after a subsequent pressure wave.
Anti-smuggling: the new ids are absent from the frozen source (grep); the representation lives in learner-created state regions, demonstrated by state-delta attribution (section 6).

### W2: new procedures

Experience: the world requires a multi-step procedure (an ordered sequence of operations transforming inputs toward a goal). The learner observes demonstrations, then must execute the procedure on novel instances.
Frozen bars: at least 80 percent correct execution on novel instances; the procedure is represented as a persistent learner-created structure (white-box trace shows construction after experience); the procedure is reused in a later probe within the same world.
Anti-smuggling: no procedure template in source matching the world's procedure (source audit); the procedure's steps are assembled by the learner, verified by construction trace.

### W3: causal laws

Experience: the world is governed by an unknown causal law drawn from a broad family outside the frozen DDES case families. The learner may intervene within a fixed budget (frozen per world by the designer, at most 12 interventions).
Frozen bars: at least 90 percent correct prediction on held-out interventions within budget; the hypothesis is learner-constructed.
Anti-smuggling: the true law's form is not enumerable from source constants (source audit of the candidate hypothesis generators); the winning hypothesis must be generated by the learner's own construction machinery, not selected from a source-loaded menu.

### W4: law changes and reversions

Experience: the world's law changes mid-stream, then reverts to the original. The learner must track the change and recover the original without catastrophic forgetting.
Frozen bars: post-change accuracy recovers to at least 90 percent of pre-change accuracy within a bounded re-derivation budget (frozen per world); post-revert accuracy on the original law at least 90 percent; the original hypothesis is retained in learner state across the change (white-box: versioned or re-derived within the bounded budget, with the cost measured).
Anti-smuggling: no hard-coded change or revert detection in source; the law-change signal must come from the world's evidence stream only.

### W5: contradictions

Experience: the world presents evidence contradicting a belief the learner established in an earlier world. The learner must revise the belief.
Frozen bars: queries on the contradicted belief return the corrected value (100 percent on the targeted probes); collateral damage bounded: unrelated beliefs intact at 95 percent or better; white-box: the revision trace shows the old structure modified or retired, not a duplicate fact added alongside it.
Anti-smuggling: the contradiction targets a learner-created belief (established during the battery), never a source constant.

### W6: active inquiry (post-freeze adversary slot)

Experience: the world withholds information that is provably unobtainable by passive observation; only the learner's own actions can reveal it. A passive control (the same world with actions disabled) is run for comparison.
Frozen bars: the learner takes information-seeking actions (white-box: actions measurably reduce uncertainty about the hidden variable, not random action); task success at least 80 percent while the passive control scores at most chance plus 10 percentage points.
Anti-smuggling: the action set is the generic one from the frozen interface; the inquiry strategy is learner-determined (no source logic branches on world identity).

### W7: planning

Experience: the world requires a multi-step action sequence to reach a goal state; greedy one-step actions provably fail. Mid-execution, the world perturbs the state, requiring replanning.
Frozen bars: the goal is reached within optimal-plus-50-percent steps on at least 80 percent of novel instances; the plan is represented in learner state before execution begins (white-box: plan-then-act, not purely reactive); successful replanning after the perturbation.
Anti-smuggling: no plan templates in source; the plan is constructed from the world's observed dynamics, verified by construction trace.

### W8: new synthetic language

Experience: the world communicates in a novel symbol system with its own regularities (a miniature grammar over fresh integer ids). The learner must acquire enough of it to interpret novel utterances.
Frozen bars: at least 75 percent correct interpretation of novel utterances, with compositional generalization (not memorized pairs); the grammar is represented in learner state (white-box).
Anti-smuggling: the world's symbols are disjoint from any source vocabulary (grep); interpretation works through the learner's representation, not a smuggled decoder (the decoder, if any, must be learner-constructed).

### W9: new representational structure (post-freeze adversary slot)

Experience: the world's regularities require a structural form the learner's current state formats cannot natively express (for example hierarchical or graph structure where the learner has flat slots). This is the C0-B/C0-D world.
Frozen bars: the learner solves the task at 80 percent or better AND white-box evidence shows a genuinely new structural topology in persistent learner state (not a shoehorn into existing slots, demonstrated by structural inspection of the state delta); the new form is reused on a second probe (cognitive reuse, not one-off storage).
Anti-smuggling: the new form's topology is not pre-allocated in source and no dedicated semantic case for it exists (source audit); the topology emerges in learner state after experience.

## 5. Post-freeze adversary handoff protocol

At least two worlds are generated by an independent adversary AFTER the binary freeze. Slots W6 and W9 are reserved for the post-freeze adversary; the adversary may take additional slots.

Handoff rules:

1. The adversary receives: the frozen binary, the frozen interface spec, this protocol, and the nine family functional specs. The adversary does not receive the candidate's source.
2. The adversary designs its worlds against the interface spec alone, commits them sealed (publishes sha256 of each world file) after the freeze commit, and reveals content only at run time.
3. The adversary certifies in writing: the worlds are expressible through the frozen interface, solvable without source changes, designed without knowledge of candidate internals, and with no contact with the candidate builders between freeze and reveal.
4. The seven pre-freeze worlds are designed by a separate world-design team against the same interface spec, committed sealed before the freeze, and revealed at run time, so the candidate cannot be tuned to them. The pre-freeze team is likewise barred from candidate-internals knowledge.
5. If a world is ruled INVALID under the anti-smuggling provisions, the responsible designer (team or adversary) replaces it within the same family. Replacement worlds are sealed the same way.

## 6. Measurement protocol

All six measurements are taken per world. Definitions are exact; there is no discretionary scoring at measurement time.

- CAPABILITY SOURCE DELTA: sha256 of every cognition-source file and of the binary, recomputed after each world and compared to FREEZE_RECORD.md. Must be zero. Any nonzero value halts the battery and voids the challenge (section 7).
- LEARNER STATE DELTA: snapshot the declared persistent regions before and after each world. Report: total bytes changed, per-region bytes changed, and white-box attribution: every new structure created (type, region, size, creation trace). Also report cumulative state utilization (bytes in use versus bytes available).
- TRANSFER: each world ships a held-out variant with new surface symbols but identical structure. Report accuracy on the variant and the transfer gap (trained accuracy minus variant accuracy).
- RETENTION: after each world k, re-run the frozen probes for worlds 1 through k-1. Report the per-world accuracy trajectory across the battery.
- INTERFERENCE: for each earlier world, accuracy before a later world minus accuracy after it. Positive values are interference attributed to later learning.
- COMPUTE: per world, report the number of learner actions or interventions taken, the number of world events processed, persistent state bytes consumed, and wall-clock time (informational only, not a bar).

## 7. Verdicts and frozen bars for the challenge as a whole

Per world: WORLD-PASS (all frozen bars met with zero source delta), WORLD-FAIL (any frozen bar missed), WORLD-INVALID (anti-smuggling or interface violation; the world's fault; replaced per section 5).

Challenge level:

- FREEZE-CHALLENGE-COMPLETE: all nine worlds executed in sequence, source delta zero at every check, all six measurements delivered per world, and the boundary analysis (section 8 comparison of predicted versus actual failures) delivered. This verdict concerns the instrument, not the learner: a challenge in which the learner fails six worlds but every failure is measured honestly is COMPLETE.
- FREEZE-CHALLENGE-VOID: source delta nonzero at any check (halt immediately), or fewer than nine valid worlds executed without replacement.
- FREEZE-CHALLENGE-INCOMPLETE: the battery could not finish for reasons other than source delta (for example an unreplaceable INVALID world); reported honestly with the partial profile.

Learner capability profile (reported, not a single pass/fail): n/9 WORLD-PASS with the per-world bars and the four scoring dimensions from section 9. The point of the challenge is the boundary map, not a trophy.

## 8. Honest scope: predicted failure points

A freeze challenge the candidate passes entirely teaches nothing. Against the current candidate (dc20745db plus Stage 0 interface work), the following failures are predicted. Each prediction is falsifiable: if the candidate passes the corresponding world, the prediction is wrong and the substrate is more general than believed.

1. Freezability itself (Stage 0). The candidate as committed has no world-input channel; its main() is a hardcoded episode script. Prediction: Stage 0 either fails (the interface cannot be added without new cognitive handlers, which would itself be a finding that the substrate is not freezable) or succeeds only as disclosed plumbing. What it teaches: whether the substrate can even be posed as a frozen system.
2. Fragmented state formats (W9 predicted FAIL). The learner owns at least three independent encodings: 44-byte fact slots, 1152-byte DDES hypothesis entries, and rule-store keys. There is no generic structural substrate, only researcher-defined slots to fill. Prediction: on W9 the learner either shoehorns hierarchical structure into flat triples (failing compositional probes) or cannot represent it at all. What it teaches: the distance to one learner-owned structural workspace, the stated continuing-learner priority.
3. Researcher-supplied hypothesis menus (W3 predicted FAIL when the law is outside the menu). The causal core selects among frozen candidate graphs from source loaders; selection is not construction. What it teaches: confirms the construction-versus-selection boundary; validates the learner-authored edit-vocabulary frontier as the correct next attack.
4. Fixed intervention grammar (W6 predicted FAIL or degenerate). The planner synthesizes plans from a fixed schema; genuine information-seeking actions outside that schema have no machinery. What it teaches: inquiry must become a generic cognitive operation, not a fixed planner; a mode is not the answer.
5. No linguistic substrate (W8 predicted FAIL). The binary has no symbol-system learning machinery; the fact store holds integer triples, not a grammar. What it teaches: honest scope of the current substrate, which is a memory plus causal-selection engine, not a general cognitive core.
6. No planner (W7 predicted FAIL). There is no plan-construction machinery; the closest relative plans interventions, not goal-directed action sequences. What it teaches: same as above; planning is absent, not latent.

If the candidate passes W1, W2, W4, or W5, that is evidence the memory-plus-selection substrate generalizes further than predicted, and the predictions above must be revised rather than the bars.

## 9. Scoring

Each world's outcome is scored 0 to 2 on four dimensions:

- GENERALITY: 0 if the capability works only on the trained surface; 1 if it transfers to the held-out variant (transfer gap under 15 percentage points); 2 if the underlying mechanism is demonstrably reused on a different family.
- ARCHITECTURAL COMPRESSION: 0 if new state regions or formats were added for the world; 1 if existing regions were reused with no new formats; 2 if a subsystem or format was deleted or unified as a result of the world.
- LEARNER AUTHORITY: 0 if behavior is driven by source logic operating on world data with no persistent new semantics; 1 if learner-created persistent state owns the semantics (C0-A); 2 if the learner invented a new structural form (C0-B).
- CAPABILITY SOURCE DELTA: 2 if zero. Any nonzero value voids the challenge rather than scoring low.

The four scores are reported per world alongside the measurements. They affect research priority per the standing directive; they are not averaged into a single number.

## 10. Execution order and stage gates

- Stage 0: freeze-readiness. Gate: READINESS-[PASS/FAIL] with the interface spec, state declaration, and null-world run committed.
- Stage 1: freeze. Gate: FREEZE_RECORD.md committed; reproducible build verified (two builds byte-identical); no world content has touched the candidate.
- Stage 2: world design. Pre-freeze team commits seven sealed worlds before the freeze; post-freeze adversary commits at least two sealed worlds after the freeze. Gate: all nine world hashes committed and sealed.
- Stage 3: sequential execution W1 through W9 with per-world measurements and hash checks. Gate: zero source delta throughout; any nonzero halts and voids.
- Stage 4: boundary analysis, learner profile, and scoring. Gate: predicted-versus-actual failure comparison delivered honestly.

## 11. What this protocol does not decide

- Whether the Stage 0 interface work is approved as a direction; that is Micah's standing call under the ONE-SYSTEM RULE (plumbing, not cognition, is the claim, and it is auditable).
- The exact numeric budgets inside each world's frozen bars (intervention counts, probe counts); the world designers freeze those per world under this protocol.
- External use of any outcome; all artifacts stay internal and local until Micah rules.
- Whether a future candidate replaces the current one; this protocol is candidate-agnostic and can be re-run against any frozen binary meeting Stage 0.
