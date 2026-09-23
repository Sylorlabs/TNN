# E-SP Relevance-Calibration Research Plan

**Crew:** E-SP-R. **Status:** DESIGN (not frozen — this plan is the design
deliverable; the labeling prereg is a separate dated amendment, approved per
standing law, before any labeling run).
**Authority:** HTD-1 frozen prereg §3c, §1 KB-HTD-1.3–1.6; debate briefs
`eff-sparse.md` (shared bars) and `redteam.md` (§2.1 circularity objection).
**Anti-scope:** No routing architectures, no wake/sleep mechanisms, no gate
design. This program produces *labeled data and an oracle scorecard* — nothing
that wakes or sleeps anything. No mechanism advances to an architecture claim
without clearing KB-HTD-1.3. No git commits from this crew.

## 0. Why this research exists

The red-team verdict on E-SP\* was precise: sparse routing presumes a
relevance oracle — a function from (state, task) → which parts matter — and
on a proxy workload that oracle is circular (relevance is workload-defined;
deliberation *is* TNN's relevance judgment, so a gate is deliberation gating
deliberation). The rescope answer is not to argue the circle away but to
*measure through it*: define relevance ground truth **counterfactually** on
real deliberative work, by replaying real episodes with partitions removed
and observing what changes. If no oracle can predict those counterfactual
labels better than chance, relevance is not definable this way — and that
negative result is a result: E-SP stays parked, honestly.

## 1. The research question, stated falsifiably

**Q:** Can relevance ground truth be defined on real deliberative corpora
such that an oracle, given only pre-episode state and task, predicts which
state partitions mattered to episode outcomes?

**Falsifiable form.** Let NECESSARY(P,E) ∈ {0,1} be the counterfactual label
(§2.5): partition P mattered to episode E iff deterministically replaying E
with P ablated changes E's scored outcome or any ledgered deliberate
decision. An oracle ŷ(S_E, I_E) → subset of partitions is tested against
these labels on held-out episodes. Then:

- **DEFINABLE** iff the best non-trivial oracle (§3.3) achieves macro-averaged
  MCC ≥ **0.30** AND necessity-recall ≥ **0.90** on held-out episodes, in
  **≥2 workload families** (§2.1).
- **NOT DEFINABLE** iff no oracle exceeds MCC **0.10** on held-out episodes
  (the chance zone) in any family.
- **Gray zone** (0.10 < MCC < 0.30, or recall bar missed): verdict
  INCONCLUSIVE — E-SP stays parked; the report states exactly what would
  change the verdict (more families, better features, different partitioning).

The negative result is binding: NOT DEFINABLE → E-SP1…E-SP6 stay parked as
research, no architecture candidacy, and the report is the deliverable. There
is no re-entry on the same corpora with the same oracle families.

### Why MCC and why these numbers

Labels are sparse (most partitions don't matter per episode), so accuracy is
meaningless and F1 is threshold-fragile; MCC is the honest single number for
imbalanced binary agreement (0 = chance, 1 = perfect). 0.30 is a moderate,
nontrivial bar: a token-overlap gate on a lookup workload should clear it
easily if relevance is really predictable; a gate that only works on proxies
will not. The **necessity-recall ≥ 0.90** bar is the research-phase analog of
SH-RECALL: deployment is safety-critical — skipping a necessary partition
loses an answer — so an oracle that is precise but blind is not "definable
enough." Both bars must hold; missing either is not DEFINABLE.

## 2. Method: instrument, ablate, replay, label

### 2.1 Workload families (real deliberative corpora)

A corpus qualifies for labeling only if all four hold:

1. **Real deliberative work** — genuine TNN episodes (memory operations,
   deliberative refusal, revision, integrity checks, consolidation), not
   synthetic tasks.
2. **Native scored outcome per episode** — the workload's *own* quality
   metric (not wall-clock, not op counts). Examples:
   - debate traces (`tnn-lab/wave8/debate/out_*.txt`, `TR_*` records):
     spectator-side choice / assertion-revision correctness per the debate
     prereg's native scoring;
   - strength-trial cell logs (`tnn-lab/wave5/strength-trial-run/evidence/cell_*.log`):
     the trial's own pass/fail checks (`CL_CHECK` lines) per cell-episode;
   - MA trial evidence (`tnn-lab/wave2/memoryagency/trial/EVIDENCE_*`):
     memory-op check outcomes (kill/pin/promote decisions + checks);
   - long-horizon runs (`tnn-lab/wave2/longhorizon/variants/LH-*`):
     regime-switch decisions over update windows (episodes = windows).
3. **Replayable** — binary or rebuildable Zag source + logged initial state +
   input log reproduces the original trace **byte-identically** (standing
   law). Non-replayable corpora are documented, never labeled.
4. **Partitionable** — a per-corpus partition declaration (§2.3) is possible.

The labeling set needs **≥500 episodes** (KB-HTD-1.3's number; the research
uses the same bar so the promotion gate needs no re-measurement of scale).
Recommended first set: debate traces + strength-trial cells (largest,
cleanest episode structure), MA evidence second, LH windows third. The R3
crew's frozen real-workload corpus is the authoritative episode list; this
research does not invent its own.

### 2.2 Episode

An **episode** E = (I, S, T, O, Q) where I is the episode input bytes, S is
the start state (partitioned), T is the executed trace (deliberate ops with
a partition-touch log), O is the ledgered outcome (decision/commit/answer),
and Q(E) is the native score. Episode boundaries come from the workload's
own structure (debate session, trial cell, MA trial, LH window) — the
research never re-segments.

### 2.3 Partition declarations (per corpus, frozen before labeling)

Partitions are **not invented by the researcher**. Each corpus gets a frozen
partition declaration naming the partition ID scheme, analogous to E-DE4's
relevance-partition declarations. Criteria: stable IDs across episodes (same
ID = same logical content group); **independently ablatable** (withholding
P is well-defined); coarse enough to be a real intervention (memory
contexts/slot-groups, not single chunks; not the whole store). Natural
candidates: TNN's deliberately-managed memory contexts (the 16/16
context-switch partitions); debate memory partitions + world-record
partitions; strength-trial store partitions per the trial's own layout.
The declaration is part of the labeling prereg amendment.

### 2.4 Instrumentation: the trace schema

Existing logs are evidence, not labels. A small Zag instrumentation
prototype (allowed under design-first; the *plan* is still the deliverable)
re-runs each qualifying trial with a trace emitter producing, per episode:

```
EPISODE <episode-id> <input-sha256> <start-state-sha256>
PART_TOUCH <episode-id> <partition-id> <read|write|revise|kill|cite> <count>
OUTCOME <episode-id> <outcome-bytes-sha256> <native-score>
EPISODE_END <episode-id> <end-state-sha256>
```

Requirements: emission is ledger-visible and deterministic; the
instrumented replay of the corpus must reproduce the *original uninstrumented
trace* byte-identically apart from the new trace records (V0 gate, §2.6) —
instrumentation must not perturb deliberation.

### 2.5 The ablate-and-replay protocol (exact procedure)

For each episode E in the labeling set:

1. **Control replay.** Replay E with no ablation from (I, S). Must reproduce
   (T, O, Q) byte-identically. Failure → episode excluded, harness
   investigated (standing law: determinism failure = disqualified, no appeal).
2. **Ablation runs.** For each partition P in the ablation set (§2.7),
   replay E from (I, S with P tombstoned): partition ID preserved, all reads
   return ABSENT deterministically, writes to P are dropped-and-ledgered.
   (Tombstone, not renumbering: slot/ID shifts are a harness artifact and
   are banned — V1 checks this.)
3. **Outcome comparison.** Record O_P, Q_P. Label:
   **NECESSARY(P,E) = 1** iff Q_P ≠ Q at the native scoring granularity, OR
   any ledgered deliberate decision in O differs (kill/promote/revise/refuse/
   commit/cite sets differ). Byte differences confined to scratch or audit
   records that change no decision and no score → NECESSARY = 0 (artifacts,
   not relevance).
   Also record CONSULTED(P,E) = 1 iff the control trace's touch log shows ≥1
   read/write/revise/kill/cite on P.

Determinism is what makes the causal identification clean: reruns are
byte-identical, so the *only* source of outcome difference between control
and ablation run is the ablation itself. There is no noise floor to argue
about.

### 2.6 Labeling validity gates (the method grades itself)

- **V0 (replay sanity):** control replay byte-identical to the instrumented
  original on 100% of labeling-set episodes. Any failure → episode excluded;
  systematic failure → corpus disqualified.
- **V1 (harness artifact check):** for a preregistered sample, ablate
  partitions with CONSULTED = 0. Outcome must be byte-identical to control
  in ≥99% of cases. Any divergence is a harness bug (tombstone leaking into
  deliberation paths, e.g. ID-shift or ABSENT-handling asymmetry) → labeling
  **suspended** until the harness is fixed. This is the control that keeps
  ablation honest.
- **V2 (intervention-artifact rate):** fraction of NECESSARY = 1 labels with
  CONSULTED = 0 must be ≤5%. Above that, the ablation intervention is
  changing outcomes through non-deliberative paths (absence-triggered
  fallback/refusal machinery firing on the *fact of absence* rather than on
  missing content) → labels measure the intervention, not relevance →
  labeling suspended, method revised. This is the quantitative form of the
  "mattered" skepticism in §6.
- **V3 (realization stability, if bandwidth):** re-label a sample with an
  alternate ablation realization (empty-partition vs tombstone); label
  agreement must be ≥95%.

V1/V2 failing suspends *labeling*, not the research question — the report
says the method failed its own validity gates, which is itself a finding
(and E-SP stays parked).

### 2.7 Ablation set (what gets ablated per episode)

Default: **all** declared partitions, per episode. For corpora with >200
partitions per episode, fallback: all CONSULTED partitions + a frozen
deterministic systematic sample of non-consulted partitions (every k-th by
partition ID, k frozen in the labeling prereg — no randomness anywhere, and
the selection rule is replayable). Labeling cost is one-time research cost,
not deployment cost; it is bounded by workdir discipline (`~/workspace`,
never `/tmp`) but is not subject to FULL COST accounting (no efficiency
claim is made from labeling runs).

## 3. The oracle

### 3.1 Interface

- **Input:** (S_E, I_E) — the start-state snapshot (per-partition content
  digests SHA-256, slot counts, recency metadata) and the episode input
  bytes + frozen task-class tag. **Nothing from T or O.** Any feature
  computed from the trace or outcome disqualifies the run (leakage = the
  circularity objection made real; checked by feature provenance audit).
- **Output:** a predicted-relevant partition set (a subset of declared
  partition IDs); scored oracles may additionally emit a ranking, evaluated
  at the frozen operating threshold.

### 3.2 What the oracle predicts

The target variable is **NECESSARY(P,E)** — counterfactual necessity, not
consultation. Rationale: a gate's job is to skip what needn't be woken; a
partition consulted-but-redundant is safe to skip, a partition necessary is
not. The corpus also yields the measured consultation ⊃ necessity gap, which
is reported as the *headroom estimate* for sparsity on that workload — but
headroom is not a win; no gate is built or claimed here.

### 3.3 Oracle families (all evaluated; "best" selected by frozen rule)

- **O-CHANCE** — deterministic hash-based random subset at the corpus base
  necessity rate. The chance baseline every oracle must beat.
- **O-ALL** — all partitions. The trivial precision/recall baseline (recall
  1.0, precision = base rate). Never eligible for "best."
- **O-TOUCH** — partitions consulted in the K most recent episodes of the
  same task class (K frozen). Tests whether relevance is just recency.
- **O-SIGNATURE** — E-SP1-style token-overlap gate (query-term hashes ∩
  per-partition signature). **This is the same oracle family as the
  CORPUS-QA-60 proxy pilots** — the bridge that lets pilot data and real
  corpora be scored on one metric (§4).
- **O-MASK** — per-task-class learned masks trained on labeled folds
  (E-SP5 analog), only if bandwidth allows. Trained strictly on training
  folds.

Frozen selection rule for "best non-trivial oracle": highest held-out
macro-MCC among O-TOUCH / O-SIGNATURE / O-MASK, subject to necessity-recall
≥ 0.90. O-CHANCE and O-ALL are reported, never selected.

### 3.4 Calibration metric and held-out protocol

- **Primary metric:** Matthews correlation coefficient between predicted set
  and NECESSARY labels, computed per episode and **macro-averaged** over
  episodes (episodes have different partition counts; pooled MCC would let
  large episodes dominate). 
- **Secondary:** necessity-recall (the safety number), precision, AUROC for
  scored oracles, and the consultation-vs-necessity gap per family.
- **Held-out protocol:** 5-fold cross-validation by episode, folds frozen in
  the labeling prereg, stratified by task class where declared. Oracle
  fitting/training on 4 folds, evaluation on the 5th. The DEFINABLE /
  NOT DEFINABLE bars (§1) are evaluated on held-out folds only.
- **Anti-leakage:** feature provenance audit — every oracle input feature
  must be derivable from (S_E, I_E) with the trace and outcome cryptographically
  excluded (features computed by a separate frozen pass over start-state
  snapshots, before traces are opened). Violation → run discarded.

## 4. CORPUS-QA-60 proxy pilot feeding protocol

The E-SP proxy pilots (wake fraction ≤30%, miss ≤5%, overhead <25% of gross
saved, net ops <90% of B0, S10 gate ≤12× S1) run in parallel. Their data
enters this research as **workload family P (proxy)** — nothing more:

1. **Same labeling method applies.** Partitions = the frozen corpus
   partition map (pg100 work-partitions, sqlite amalgamation-file
   partitions); "deliberation" = the QA answering run; outcome = answer
   correctness vs frozen ground truth; ablate-and-replay = withhold a corpus
   partition, re-answer, compare. The pilot's gate *is* an O-SIGNATURE-class
   oracle, so its wake sets are oracle predictions scored by the §3.4 metric
   on family P.
2. **What pilot numbers may be used for:** oracle-calibration evidence only.
   Wake fractions, miss rates, S1/S10 numbers describe how well an oracle
   family predicts counterfactual necessity on family P. 
3. **What pilot numbers may NOT be used for:** any routing-architecture
   claim. Citing a pilot win as evidence that a wake/sleep mechanism works
   is INVALID per §3c — the pilot measures an oracle family on a proxy, not
   a deployed gate on real work. The per-hypothesis bars remain the pilot
   scorecard; they do not promote anything.
4. **Transfer measurement.** Oracles calibrated on family P are evaluated on
   the real families (and vice versa); the transfer gap is reported as a
   number. Per the KB-HTD-1.4 logic, a proxy-only win transfers nowhere —
   if O-SIGNATURE is DEFINABLE on family P but NOT DEFINABLE on real
   families, the verdict is NOT DEFINABLE for TNN's purposes, and the gap
   itself is the finding (it quantifies the red-team's §2.1 objection).

## 5. Promotion checklist: E-SP research → architecture candidacy

No wake/sleep mechanism advances without **all** of the following (the
KB-HTD-1.3 gate restated as a checklist):

1. [ ] Research verdict **DEFINABLE** on the frozen real-workload corpus
    (macro-MCC ≥ 0.30, necessity-recall ≥ 0.90, held-out, ≥2 families) —
    documented in the research report.
2. [ ] Implementable oracle: prediction cost measured in native ops; gate +
    dispatch + commit < 25% of gross saved (the SH-OVERHEAD analog, computed
    in FULL COST).
3. [ ] **KB-HTD-1.3 firing test passed:** ≥20% total-cost win vs always-awake
    on ≥500 real deliberative episodes, output quality within 2% of baseline
    on the workload's native metric — preregistered before building,
    head-to-head, reported as it resolves.
4. [ ] **KB-HTD-1.4 transfer:** re-measured on held-out W' (different
    deliberation depth, different memory churn); transfer gap ≤50% or the
    claim is VOID; two voids = PARKED.
5. [ ] **KB-HTD-1.5 full-cost accounting:** total cost = compute +
    memory-state updates + audit/ledger write volume + verification overhead.
    Any win reported without the ledger term is INVALID.
6. [ ] **KB-HTD-1.6:** closed-form cost model frozen by the referee crew
    (`htd-1/contracts/COST_MODEL_FROZEN.md`) before any efficiency build.
7. [ ] Zero randomness in any decision path; byte-identical reruns from the
    same input + logged state (SH-DET standing law).
8. [ ] Miss rate ≤5% on the real workload's native outcome (no skipped
    necessary partition changes an outcome — the deployment form of the
    recall bar).
9. [ ] No architecture claim rests on CORPUS-QA-60 pilot data alone (§4.3).
10. [ ] Any change to rules, metrics, thresholds, or scope carries a dated,
    Micah-approved amendment (standing law).

If the research verdict is NOT DEFINABLE or INCONCLUSIVE, items 2–10 are
moot: E-SP stays parked, and the research report — including the honest
negative — is the deliverable.

## 6. Steelman: the strongest objection to this method

**The objection.** Ablate-and-replay measures relevance in a world where
everything is awake, but a wake gate operates in a world it itself changes —
*relevance labels are regime-relative, and the oracle's predictions shift the
regime they were trained on.* Three concrete forms:

1. **Opportunistic consultation.** Under always-awake deliberation, the
   system reads partitions *because they are there*, not because it needs
   them. Necessity labels correctly mark these redundant — but the oracle,
   trained to predict necessity, will then license skipping them, and the
   deliberation that runs under sparsity is a *different deliberation* whose
   necessity structure was never measured. The labels describe the full
   regime; the gate deploys into the sparse regime. Nothing in this research
   measures whether necessity is stable across that transition.
2. **Compensatory deliberation.** A partition labeled unnecessary under
   full-awake deliberation might become necessary under sparse deliberation
   (the system leans harder on what remains), or a necessary partition's
   content might be reconstructible from others only when those others are
   awake. Necessity is a property of (partition, episode, *regime*), and we
   measure only one regime.
3. **The oracle's own circularity, one level up.** The best features for
   predicting necessity may themselves be products of prior full
   deliberation (e.g., signatures built at consolidation time by an awake
   system). An oracle that is "definable" only because the always-awake
   regime pre-computed its features has not escaped the circle — it has
   moved the full-awake cost into consolidation and called the gate cheap.

**Why the research is still worth running — and what it does not claim.**
The objection is correct that this research cannot license a gate; that is
exactly why §5 exists. The research answers the narrower, prior question:
*is there any stable signal at all* — can pre-episode state predict
counterfactual necessity better than chance on real work? If the answer is
no, the regime-relativity objection is moot and E-SP parks honestly. If the
answer is yes, the regime-transition question becomes the *next* preregistered
study (gate-in-the-loop replay: re-run episodes under oracle-predicted wake
sets and re-label necessity in the sparse regime — a separate prereg, not
part of this program), and the KB-HTD-1.3 firing test (§5.3) is the gate
that finally decides, measured with the gate in the loop on 500 real
episodes. This research is the filter that keeps an undefinable idea from
ever reaching that expensive test — not a shortcut past it. The V2 validity
gate (§2.6) is the in-method tripwire for the crudest form of the objection
(intervention artifacts); the subtler regime form is acknowledged as beyond
this method's reach, and the plan says so rather than hand-waving.

## 7. Dependencies, deliverables, open questions

**Depends on:** R2 (determinism harness, R=5, SHA-256) for V0; R3 (frozen
real-workload corpus episode list; frozen CORPUS-QA-60 + partition map) for
the labeling set; R1 (closed-form cost model) only at promotion phase (§5.6),
not for research. E-SP proxy pilots feed family P data in parallel.

**Deliverables:** (1) this plan; (2) the labeling prereg amendment (dated,
Micah-approved): corpus list, partition declarations, oracle families,
folds, metric, bars; (3) the instrumented trace corpora + label tables
(under `htd-1/builds/esp-research/`, workdirs under `~/workspace`); (4) the
oracle scorecard with the DEFINABLE / NOT DEFINABLE / INCONCLUSIVE verdict;
(5) the research report committed under `docs/lab/htd-1/` per §8 of the
frozen prereg.

**Open questions for the coordinator / Micah:**
1. First label set: debate + strength-trial first, MA second — confirm, or
   reorder?
2. Is O-MASK (learned oracle) in scope for this phase, or deferred?
3. The MCC 0.30 / recall 0.90 / chance-zone 0.10 thresholds are proposed
   here and frozen at the labeling-prereg amendment — amendable by dated
   Micah amendment per standing law.
