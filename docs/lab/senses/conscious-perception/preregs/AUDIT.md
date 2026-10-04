# AUDIT — Full Autopilot Audit preregistration

**Frozen:** 2026-09-23 (PDT). No measurement below may be run before this
prereg is committed. **Question (Micah):** PAMs aren't the only suspect —
inventory EVERYTHING in the native lab that runs non-consciously or
disconnected from deliberation, and measure the bill: what does
consciousness cost per component, and what intelligence does it buy?

## 1. Definitions (frozen)

- **Autopilot:** a load-bearing path whose behavior is decided without any
  deliberation-path decision: fixed rules, timers, thresholds, or pipeline
  stages that execute regardless of what the system judges about the
  current situation. "Disconnected from deliberation" = the deliberative
  machinery cannot inspect, veto, or redirect the step.
- **Conscious version:** a variant where the same step is a deliberate
  act: attention control, a judgment, a verification step, or an explicit
  abstain — audited, with refusal codes, reversible where state changes.
- **The bill:** per-episode ops + wall time, autopilot vs conscious,
  byte-identical reruns (≥3), zero RNG in anything built here.
- **Intelligence gain:** a failure class the conscious version catches
  that the autopilot version does not — ideally a REAL failure from the
  lab's history (cited), else a constructed failure the prereg predicts.

## 2. Inventory method (frozen)

For each named area in scope (learners: prose-learning, wave3
hypothesis-driven-exploration, r27-consolidation, deliberate-recall,
trace-composition; memory ops: kb/, wave2/memoryagency install/revise/
delete/compact/promote; verification: self-test, wave5+ gates; generation:
imagination/, dialogue/; ingestion: mixed-web, info-source, youtube_ingest;
senses/PAMs: senses/, senses_unlimited/; recall: deliberate-recall;
reasoning control), read the design doc + the mechanism source and apply
the autopilot test:

1. Walk the load-bearing path (stimulus→sense→judgment→install, or
   need→recall→act, or op→ledger, etc.).
2. Mark every step: **A** (autopilot — runs regardless of judgment),
   **D** (deliberate — a judged, audited act), **H** (hybrid — advised
   by substrate, decided by learner).
3. A component "runs on autopilot" iff any load-bearing step is A and no
   D-step can veto or redirect it.

Components that are D-throughout are recorded as NEGATIVE controls
(already conscious — e.g. deliberate-recall's logic selection, HDE's
hypothesis-driven choice, MA1's op set). Anything unreachable (dead
workstreams, missing certrebuild) is named as a gap, not scored.

## 3. Measurement protocol (frozen)

Three evidence tiers, labeled on every table row:

- **Tier 1 — measured here:** both variants exist in runnable form (or the
  conscious variant is built by this audit). Rebuild from source with the
  pinned toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
  run ≥3 reps, byte-identical outputs (SHA256), wall time via
  perf_counter, ops from instrumented counters in the source or from
  algorithmic analysis of the hot loop (stated which). Zero-RNG static
  check (`grep -i rng` over new sources must be empty).
- **Tier 2 — committed evidence:** a frozen prereg + verdict + committed
  numbers already exist from a prior lab trial. Cite the commit; do NOT
  re-run the whole battery (re-verify reproducibility only if a runnable
  binary is present). Cost numbers are taken from the committed verdict
  and labeled as reported-then.
- **Tier 3 — estimate:** code-analysis estimate. Ops from the hot loop's
  asymptotic shape × measured per-op constants where available; wall time
  by proportional scaling from a measured sibling. Labeled ESTIMATE with
  the derivation shown. Never presented as measured.

**Fair-fight rule (Micah's standing bet: conscious helps WITH PROPER
TRAINING; tests must challenge it):** every conscious variant is also
scored on autopilot-favoring legs — raw throughput (items/episode),
latency floor, no-uncertainty cases where deliberation adds nothing but
latency, compute per episode. If autopilot wins anywhere, report the
mechanism (why), not just the timing.

## 4. Component list (frozen scope)

| # | Component | Path | Expected class |
|---|---|---|---|
| C1 | Consolidation (fast→slow promotion) | wave3/r27-consolidation/impl/psm.zag | autopilot arm EXISTS (harness-style baseline) vs deliberate arm — Tier 1 |
| C2 | PAM sense pipeline (pre-attentive stages) | senses/, senses_unlimited/ | autopilot — Tier 1 (minimal experiment built here) + Tier 3 for full pipeline |
| C3 | KB install gate (judgment→install) | kb/autopsy (KB4) | Tier 2 (KB4 autopsy: deliberative gate vs round-1 rule) |
| C4 | Ingestion sense→install (info-source) | info-source/src | Tier 2 (three-arm: facts-only vs corroboration-gated) |
| C5 | Ingestion sense→install (mixed-web, youtube_ingest) | mixed-web/src, senses/youtube_ingest | Tier 3 |
| C6 | Imagination generation pipeline | imagination/ | Tier 2 (RT4 pipeline red-team + assembly fix) |
| C7 | Dialogue generation (morphology/composition) | dialogue/dialogue.zag | Tier 3 |
| C8 | Self-test verification (orchestrator) | self-test/selftest.zag | Tier 2 (orchestration overhead measured) |
| C9 | Curiosity substrate | wave3/curiosity-substrate | NEGATIVE (advisor-only by design) + real failure citation (R34 LCG, remediated) |
| C10 | Exploration choice (HDE) | wave3/hypothesis-driven-exploration | NEGATIVE (hypothesis-driven by design) |
| C11 | Recall selection | wave3/deliberate-recall | NEGATIVE (logic selection by design) |
| C12 | Trace composition | wave3/trace-composition/comp.zag | NEGATIVE (structural preconditions) |
| C13 | Memory ops install/revise/delete/promote | wave2/memoryagency/trial/memory_core.zag | NEGATIVE (deliberate op set); autopilot ancestor = R27 harness-written tiers (C1 covers the delta) |
| C14 | Compaction | wave2 (MEMORY_SAFETY.md) | inventory only — no compact op found in MA1 set; Tier 3/none |
| C15 | Structural revision | wave3/native-structural-revision | NEGATIVE (proposal→measured→PROMOTE) |
| C16 | wave5 ledger gates | wave5/ledger-gating | Tier 3 (external adjudication — autopilot? deliberate?) |

## 5. Verdict rules (frozen)

- **conscious-ify:** conscious variant catches a real failure class at a
  cost ≤ 10× autopilot per episode (or any cost if the failure class is
  integrity-critical: silent corruption, false installs).
- **keep autopilot:** conscious variant catches nothing the autopilot
  misses on the frozen battery, or costs > 10× with no integrity gain.
- **needs experiment:** mechanism unclear, or Micah's "test both" rule
  applies and no frozen battery exists yet.

## 6. Commit plan

Evidence → `~/workspace/conscious_perception/evidence/`; committed to
`tnn-native-lab` under `docs/lab/senses/conscious-perception/` via
`~/workspace/commit_big_files.py` (lab-relative paths, no binaries,
no `.zagd`; TMPDIR=~/workspace/tmp_commit). Prereg committed BEFORE any
Tier-1 measurement result is written up.

## 7. Honest limits

- Full-pipeline PAM cost (C2) cannot be measured here without the
  production sense harness; the minimal experiment measures the gate
  delta only — the full-pipeline number stays Tier 3.
- 1GB-ingestion red-team/audit is in flight (dispatched 2026-09-23); this
  audit cites only committed findings, not interim claims.
- `certrebuild` named in the task brief was not found in the lab tree —
  recorded as a gap (C-g1). Reasoning-control internals beyond RC1/RC2
  were not reached — recorded as a gap (C-g2).
