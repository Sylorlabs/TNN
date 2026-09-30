# Morning Report: 2026-09-30

Checkpoint, not endpoint. All numbers from committed reports.

## 1. Capability Advances

**DDES (Difference-Driven Experiment Synthesis): BUILD-PASS.** Successor to H-CAUSALEXP-CONSTRUCT. Derives experiments from symbolic hypothesis difference via arrival-time analysis. 9/9 converge across Worlds A-E. Plans_built = 8 (exactly 1 per config). World C length 6 works with no bound consulted. World D emits OZ plan (variable choice works). World E returns NO-DISCRIMINATING-PLAN with 0 executions (honesty). All K-NX1 through K-NX8 pass. 3/3 byte-identical. This is a genuine advance: zero enumeration, zero bound, zero menu. Classification: Strong L2 (guided generation), NOT L3.

**Arena: 0.573 to 0.676.** Clean canonical remains 0.573 (39/68). Contaminated v3 measured 0.632 (43/68, C4 composition). v4 with conflict handling measured 0.676 (46/68, C6 0 to 1.000). The v4 work is clean: 7/7 kill bars pass, pure Zag, arena unmodified, 3/3 deterministic. But v4 builds on contaminated v3, so 0.676 is not canonical until clean refreeze reproduces composition. Still 0 on inquiry, causal, procedure, transfer, goal, language.

**I2 bounded learning-to-learn: BUILD-PASS 5/5.** Family A 13 examples. Family B with retained form_known 10, fresh 13, ablated 13. Real three-example benefit. Bounded L1/L2, not L3 (fixed-offset form is researcher-supplied).

**Invention economics principle: schemas amortize, instances do not.** Persisting a bare solution instance (macro) was ECON-NEGATIVE (net -2084 checks, worse at every scale). Retaining an offset-form schema was ECON-POSITIVE (+12 examples saved, 12 bytes storage, break-even at 0 percent probability). Design rule for the continuing learner: persist compressed schemas, not verbatim instances.

## 2. L3 Status and Semantic Authority

**No L3 anywhere.** All mechanisms are L2 or below.

- H-CAUSALEXP-CONSTRUCT: L3 claim KILLED. Survives as bounded L2. Researcher owns primitives, order, depth bound (MAXD=5 hardcoded), criterion, hypothesis space.
- DDES: Strong L2, NOT L3. Researcher owns action vocabulary, hypothesis format, analysis algorithm, schema set. Learner authors intervention decision, observed variable, plan length, full sequence. Zero learner-persistent state across worlds (confirmed by adversary K3).
- F2 autonomous scientist: BUILD-FAIL. Mechanism is L2 structural learning, not L3.
- F1 generic executable semantics: Still running. Adversarial prereg frozen (AX-GX1 probe-menu equivalence, AX-GX2 sealed nested-branch family to be designed after freeze, AX-GX3 source audit). This is the highest-priority frontier.
- F3 developmental language (DEVANG1): BUILD-FAIL. Implementation does not execute to completion (slice index out of bounds, memory corruption, lexicon overflow).

**Semantic authority:** The researcher retains semantic authority in every mechanism tested. No learner has invented or recruited a representation the researcher did not enumerate as the solution space.

## 3. Competitive Status

**TNN clean score: 0.573 (39/68).** This is the canonical score. C3 paraphrase, C5 correction, C14 restart at 1.000. Classification: bugfix and format robustness, not new cognition.

**Contaminated measurements (not canonical):** v3 0.632 (43/68, C4 composition, governance-contaminated by Python use). v4 0.676 (46/68, C6 conflict, clean 7/7 kill bars but built on v3). Do not promote until clean refreeze reproduces.

**LLM baseline: PATH-BLOCKED.** No authorized API credential. No spend authorization. Machine cannot run frontier-class local model. Estimated cost $10 to $20 for three runs plus blind control. **No TNN-beats-LLM claim is permitted.**

**Cost curves (measured):**
- v1: 0.352 score, 3220KB RSS, 16KB state
- v2: 0.573 score, 3224KB RSS, 16KB state
- v3-contaminated: 0.632 score, 3240KB RSS, 16KB state

Cost flat while score improves. Inference is local, deterministic, cheap. These are not competitive advantage claims until the LLM baseline runs.

## 4. Machine-Native Advantages Actually Measured

**Confirmed (measured):**
- W1: Zero marginal inference cost ($0.00/run)
- W2: Determinism (3/3 byte-identical, md5-verified). Strongest non-cost win.
- W3: Local execution (no network, no API keys)
- W4: State efficiency (16KB for 53 exposures)
- W5: Latency (microseconds vs seconds estimated)

**Killed:**
- "Machine-native" epistemic bookkeeping: **KILLED.** SQLite implements all 7 C2 query types in 288 lines, faster (Q1 65 microseconds, Q6 0.8 ms), with ACID. This is database-native, not TNN-native. A rational user needing this uses SQLite. The label does not survive.

**Unmeasured:** TNN-beats-LLM on any capability. Superiority of white-box traceability over LLMs.

**Honest envelope:** A deterministic, local, zero-marginal-cost persistent knowledge appliance. One-shot fact learning, corrections retained, conflicts tracked explicitly, 2-hop compositional queries, byte-identical restart, 16KB state, microseconds per query, no network. Narrow but real: "deterministic personal knowledge base with conflict tracking." Mostly research, with this narrow product-shaped core.

## 5. Integration and Causal Downstream Benefits

**Step A: COMPLETE.** Five stale single-pass discovery copies retired with SUPERSEDED headers (not moved, history preserved). Gap G9 closed.

**Step B: BLOCKED.** Cannot port full causal machinery into unified learner. Architectural incompatibility: unified has 2 variables and per-episode interface; causal_learn has 3 variables, episodes/entities/contests, 8940-byte workspace, batch interface. Porting would invalidate the 14/14 or break all unified tests. Options: accept simplified store, redesign unified for 3 variables (major breaking change), or keep separate components.

**Step C: COMPLETE.** F-LEAK was already repaired by H-FLEAKFIX, verified working.

**Status:** "One continuing learner" is FALSE at present. Components are stranded, not a system. No single binary runs the full curriculum. The causal machinery (14/14 validated) remains outside the unified learner.

## 6. Killed Ideas

- **H-CAUSALEXP-CONSTRUCT L3 claim:** KILLED. Bounded enumeration (1364 sequences, MAXD=5 hardcoded). Survives as L2.
- **C2 machine-native advantage:** KILLED. Database-native. SQLite does it better.
- **Persisting bare solution instances:** ECON-NEGATIVE. Net -2084 checks. Anti-economical.
- **F3 DEVANG1 v1:** BUILD-FAIL. Does not execute (memory corruption, overflow).
- **F2 autoscientist v1:** BUILD-FAIL. Weak goal (5 percent random base rate).
- **DDES promotion:** BLOCKED. Adversary found t*=0 soundness hole (silent wrong convergence on 0-delay rules). BUILD-PASS stands (no frozen world had t*=0), but promotion requires repair.

## 7. Single Biggest Blocker

**The LLM baseline is PATH-BLOCKED.** This prevents any competitive claim. We have measured TNN costs ($0, microseconds, 16KB) and TNN scores (0.573 clean), but the LLM side is estimate only. Without a serious baseline on the frozen protocol, we cannot answer "why would a rational user choose TNN over an LLM" with data. The user must supply a key and authorize capped spend, or explicitly keep it blocked.

Secondarily: six arena capabilities remain at zero (inquiry, causal, procedure, transfer, goal, language). This is why a rational user picks the LLM today: it can do the task.

## 8. Highest-Information Next Frontier

**F1 generic executable semantics.** This is the user's stated highest priority: learner-authored representation semantics. The builder is running. The adversarial prereg is frozen (AX-GX1, AX-GX3). AX-GX2 (sealed nested-branch family) must be designed only after the implementation freeze. When F1 reports, immediately verify freeze, design AX-GX2, and run all three attacks. The C0-B gap (54 fixed probes, "first useful probe" selection, fixed branch template) is the key risk.

Second: **DDES repair.** The t*=0 soundness hole has a documented repair sketch (force >=1 W before observation). Repair, re-run sealed World F, verify no regression on K-NX1..K-NX8. This unblocks a genuine Strong L2 advance.

Third: **Integration decision.** Step B is blocked. The user must choose: accept the simplified 2-variable store, authorize a major 3-variable redesign, or keep components separate honestly.

---

**Active workers:** 10. F1 builder, F3 (failed, needs replacement), C1 race, C2 stress, DDES repair, arena inquiry (C8 prereg frozen), schema persistence, Integration Step C (complete), claim ledger (complete), morning report (this).

**Commits stay local.** Nothing pushed. LLM baseline PENDING user authorization.
