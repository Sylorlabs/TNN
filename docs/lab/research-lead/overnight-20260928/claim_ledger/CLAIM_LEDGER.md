# Claim Ledger

Maintained by the Claim Ledger Worker. One row per major claim or verdict
from the 2026-09-29/30 research window. Each row records the claim, its
disposition, the evidence commit, and the date.

Disposition key:
- STANDS: claim accepted on its frozen bar; evidence committed.
- SURVIVES-AS-L2: bounded L2 subsystem; L3 construction claim KILLED.
- L3-KILLED: the L3 construction/invention claim is dead; bounded value may remain.
- BUILD-PASS: builder met all frozen kill bars (not yet a canon verdict; 11-step pipeline still required for SURVIVES).
- BUILD-FAIL: builder did not meet a frozen kill bar; mechanism rejected on this bar.
- PATH-BLOCKED: work cannot proceed; blocker named.
- ECON-MIXED: economic test had both positive and negative sub-results.
- STEP-COMPLETE: integration step finished.
- STEP-BLOCKED: integration step cannot proceed as specified; blocker named.
- KILLED: claim dead; do not repeat.
- MEASURED-CONTAMINATED: number is a real measurement but governance-contaminated; not canonical.
- ADVANTAGE-MAPPED: analysis committed; claims triaged into confirmed/killed/unmeasured.

No em dashes. Pure documentation; zero implementation.

## Entries

### 1. H-CAUSALEXP-CONSTRUCT L3 construction claim

- Claim: active causal experiment construction is L3 cognitive structure invention.
- Disposition: SURVIVES-AS-L2 / L3-KILLED.
- Evidence: `45db44fab` (FINAL_VERDICT.md, 11-step pipeline completed).
- Date: 2026-09-30.
- Notes: Bounded L2. Mechanism enumerates 1364 sequences from a fixed
  4-action vocabulary with hardcoded MAXD=5; researcher owns primitives,
  order, depth bound, criterion, hypothesis space. Surviving value:
  disagreement filter is correctness-critical (4/4 to 0/4), simulation
  cuts real actions 35x to 254x, memorization 0/2 on novel worlds vs
  mechanism 4/4.

### 2. DDES (Difference-Driven Experiment Synthesis)

- Claim: successor builder derives experiments from hypothesis structure
  with zero enumeration, zero bound, zero menu.
- Disposition: BUILD-PASS (Strong L2, NOT L3).
- Evidence: `56db8d606` (implementation; prereg strictly precedes).
- Date: 2026-09-30.
- Notes: 9/9 converge (Worlds A-E); plans_built = 8 (exactly 1 per
  config); 3/3 byte-identical. World C length 6 works (no bound); World D
  OZ plan (variable choice); World E NO-PLAN with 0 executions
  (honesty). All K-NX1 through K-NX8 PASS. Researcher still owns action
  vocabulary, hypothesis format, analysis algorithm, schema set.

### 3. F2 autonomous scientist (autosci v1)

- Claim: autonomous experiment construction achieves goals with random
  control 0/20 on both worlds.
- Disposition: BUILD-FAIL (K-AS5 failed; weak goal).
- Evidence: `4ebde580a` (report; prereg `2a87efa77`).
- Date: 2026-09-30.
- Notes: World A 2 experiments, goal achieved, random 0/20. World B
  contextual law identified, goal achieved, but random control scored
  1/20. Transient Y=1 goal had about 5 percent random base rate; too
  weak. No seed-shopping. Mechanism classified L2 structural learning,
  not L3. Retry underway with harder sustained goal.

### 4. C2 machine-native epistemic bookkeeping advantage

- Claim: the C2 epistemic engine demonstrates a TNN machine-native
  advantage.
- Disposition: KILLED (database-native, not TNN-native).
- Evidence: `48f9765b5` (machine-native audit); `d874c0de4` (database baseline).
- Date: 2026-09-30.
- Notes: All 7 C2 query types implemented in 288 lines of SQLite, faster
  (Q1 65 microseconds, Q6 0.8 ms), with ACID. Nothing requires TNN's
  architecture. Restart recovery is table stakes for deterministic
  programs. If C2 passes, the fair claim is "epistemic bookkeeping at
  1000-entity scale can be implemented in pure Zag" only.

### 5. Arena clean canonical score

- Claim: 0.573 (39/68) is the clean canonical arena score.
- Disposition: STANDS.
- Evidence: `0c5b6c631` (clean arena score).
- Date: 2026-09-30.
- Notes: C3 paraphrase, C5 correction, C14 restart at 1.000.
  Classification: bugfix and format robustness, not new cognition.

### 6. Arena composition v3 score 0.632 (43/68)

- Claim: composition mechanism lifts arena to 0.632.
- Disposition: MEASURED-CONTAMINATED (not canonical).
- Evidence: `0f6f1790d` (implementation/report).
- Date: 2026-09-30.
- Notes: C4 0 to 1.000 (4/4), no regressions, generic relation store
  plus two-hop inference. Prereg bundled into coordinator commit
  `bbcd6eca8` after lock collision; worker used python3 -c during
  analysis. Disclosure does not cure Python use. Treat as real
  measurement from a governance-contaminated wave; clean canonical
  remains 0.573 until clean refreeze and rerun.

### 7. Arena conflict v4 score 0.676 (46/68)

- Claim: conflict handling (C6) added to arena contestant.
- Disposition: BUILD-PASS (7/7 kill bars).
- Evidence: `9211de19e` (prereg `5a4245a22` frozen before implementation).
- Date: 2026-09-30.
- Notes: C6 0.000 to 1.000 (3/3); total 43/68 to 46/68. No regression.
  Pure Zag, zero Python, arena unmodified, 3/3 deterministic. Honest
  scope: both conflicting values retained and reported explicitly; does
  not resolve source reliability or perform belief revision. Still 0 on
  inquiry, causal, procedure, transfer, goal, language.

### 8. LLM baseline

- Claim: serious LLM baseline on the frozen arena protocol.
- Disposition: PATH-BLOCKED.
- Evidence: `690dfff84` (pathfinder report).
- Date: 2026-09-30.
- Notes: Blockers: (1) no authorized LLM API credential, (2) no
  authorization to spend money or create an external provider account,
  (3) machine cannot run a serious frontier-class local model. Estimated
  cost 10 to 20 dollars for three runs plus blind control. No
  TNN-beats-LLM claim permitted until this runs.

### 9. Invention economics

- Claim: persistence policy test (when should a learner persist vs
  relearn).
- Disposition: ECON-MIXED (K1-K9 pass; pure Zag; 3/3 byte-identical).
- Evidence: `9ac23932b` (result; prereg `2557d3106`).
- Date: 2026-09-30.
- Notes: Persisted intervention macro ECON-NEGATIVE (net -2084 checks;
  reuse anti-economical). Retained offset-form schema ECON-POSITIVE
  (+12 examples, 12 bytes storage, break-even p_star = 0 percent).
  Principle: schemas amortize; bare instances do not.

### 10. Integration Step A

- Claim: retire five stale single-pass discovery copies (gap G9).
- Disposition: STEP-COMPLETE.
- Evidence: `b1819d4da` (RETIREMENT_RECORD.md).
- Date: 2026-09-30.
- Notes: Headers, not moves; history preserved. All five carry
  committed SUPERSEDED headers; H-GENBIAS fix confirmed absent from all
  five and present in both canonical copies.

### 11. Integration Step B

- Claim: port full causal machinery into the unified learner (gap G2).
- Disposition: STEP-BLOCKED (architectural incompatibility).
- Evidence: `9848741e3` (BLOCKED_REPORT.md).
- Date: 2026-09-30.
- Notes: Unified has 2 variables and per-episode interface; causal_learn
  has 3 variables, episodes/entities/contests, 8940-byte workspace, batch
  interface. Porting as specified would invalidate the 14/14 or break
  all unified tests. Options: accept simplified store, redesign unified
  for 3 variables, or keep separate components.

### 12. Integration Scout inventory

- Claim: thirteen integration gaps identified with ordered plan A-J.
- Disposition: STANDS.
- Evidence: `e6f140b64` (INVENTORY.md).
- Date: 2026-09-30.
- Notes: Highest leverage: no single binary runs the full curriculum;
  causal machinery stranded; FDCR unintegrated; routing researcher-authored.

### 13. I2 bounded learning-to-learn

- Claim: retained-form learning-to-learn benefit on family B.
- Disposition: BUILD-PASS 5/5 (bounded L1/L2, not L3).
- Evidence: `b7047b6e6` (result; prereg `4b4c8c345`).
- Date: 2026-09-30.
- Notes: Family A 13 examples; family B with retained form_known 10,
  fresh 13, ablated 13. Real three-example benefit. Fixed-offset
  hypothesis form is researcher-supplied. Worker accidentally swept
  concurrent OOD files, then reset and recommitted owned files only.

### 14. Cost curves

- Claim: score rises while cost stays flat across versions.
- Disposition: STANDS.
- Evidence: `1945c5e34` (COSTS.md).
- Date: 2026-09-30.
- Notes: v1 0.352 / 3220KB RSS; v2 0.573 / 3224KB; v3-contaminated
  0.632 / 3240KB. State constant at 16KB. Not competitive advantage
  claims until a serious LLM baseline runs.

### 15. Genuine advantage mapping

- Claim: map where TNN actually wins, measured.
- Disposition: ADVANTAGE-MAPPED.
- Evidence: `27fdc65f9` (SCOUT.md).
- Date: 2026-09-30.
- Notes: Confirmed W1-W5 (zero marginal cost, determinism, locality,
  16KB state, microsecond latency). Killed: machine-native epistemic
  advantage. Unmeasured: TNN-beats-LLM. False at present:
  one-continuing-learner. Verdict: mostly research with a narrow
  product-shaped core ("deterministic personal knowledge base with
  conflict tracking").

## Pending (not yet verdicts)

- F1 generic executable semantics: builder running; adversarial prereg
  frozen (AX-GX1/GX2/GX3); AX-GX2 to be designed only after freeze.
- F2 retry (autosci2): builder running; harder sustained World B goal required.
- F3 developmental semantic language: builder running.
- C1 lifetime-learning race: builder running.
- C2 machine-native stress test: builder running (results pending).
- DDES adversary: running; attacks on 56db8d606.
- Arena inquiry worker: running; targets C8.
- Schema persistence worker: running; tests the schemas-amortize principle.
- Database baseline worker: completed; genuine advantage scout replaced it.
- Integration Step C (F-LEAK repair): running.
- LLM baseline: awaits user key + spend authorization.

## Files

- [CLAIM_LEDGER.md](sandbox://workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/claim_ledger/CLAIM_LEDGER.md)
