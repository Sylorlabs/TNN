# Tier1 batch 2 findings (52 files, global indices 104–155)

Batch manifest: `batches/tier1_batch2.json` (corrected in place; "local" names now 0104_*–0155_*).
Local dir: `docs_local/`. Baseline: `BASELINE.md`. No "koryphaios"/"ghost" mentions in any file.
Files read: 52. NEW findings: 34 docs with new content (~17 NEW test results).

---

## NEW — big finds

### 1. FILE 41 — pre-v1 R5 results (PAM/senses ORIGINS, senses archaeology gold)
- Drive: `TNN/TNN/Research/tnn-pre-v1-r5-RESULTS.md` | size 5620 | modified 2026-08-23
- Verdict: **NEW** — pre-v1 R5 developmental results; first record in batch of the original
  sensory architectures (recurrent PAM + hybrid audio), training-mixture science, and an
  abandoned memory direction with stated reason.
- Findings:
  - Architecture ladder: flat fast/slow prototypes (poor transfer) → feature-local evidence
    → position-invariant lexical motifs (~76–79%) → contrastive raw-byte motif discovery
    → **hybrid audio PAM** ("retained stable global frequency identity while adding
    recurrent local temporal detail") → motif-gated temporal discourse workspace.
  - Abandoned: "A broad surprise-span memory was rejected: it improved some one-shot
    cases but regressed established meaning and consumed excessive compute."
  - Training mixture: `noisy → clean` won (Goldilocks 0.9580 @512 exposures, 0.97225 @1024);
    "video first" rejected ("not the winner" — delayed-language had best video 0.7050 but
    substantially worse fused meaning).
  - Architecture winner: recurrent PAM + hybrid audio (Goldilocks 0.9553; shallow PAM valid
    CAR alternative, ~5.8% fewer ops / ~10.7% less memory).
  - Multi-sentence reference: previous decoder 0.2000 → motif-gated workspace 1.0000.
  - Hard teenager boundary: `TEENAGER_ENGLISH=0`, `PRODUCTION_TNN_V1=NOT_PROMOTED`.
- Fills: senses/PAM/vision/audio origins (baseline item 4) and abandoned directions (item 2).
  Baseline has no pre-v1 developmental history.

### 2. FILE 46 — pre-v1 R6 RSI results (memory-scheme origins)
- Drive: `TNN/TNN/Research/tnn-pre-v1-r6-rsi-RESULTS.md` | size 5524 | modified 2026-08-23
- Verdict: **NEW** — promoted "Grounded Contrastive Schema Memory with support-gap
  recruitment and a protected fast path" (BOUNDED_SAR_RESEARCH_GATE PASS; production
  NOT_PROMOTED). The first schema branch was REJECTED for rewriting familiar structure
  (established exactness 0.9911 → 0.9291) — failure-triggered revision and rollback,
  preserved under `attempts/r6_unprotected_revision/`.
- "Support-gap recruitment: only the unsupported captured raw-byte span is eligible for
  one-shot growth; familiar grounded spans are not rewritten." — conceptual ancestor of
  today's deliberate memory ops / force-pin law.
- "This is a real negative result. The current learner does not yet know when additional
  teaching has stopped adding information." (delayed accuracy peaked at 2 examples.)
- Byte-identical pickle state persistence (SHA `49c6aa…53da` with PYTHONHASHSEED=0).
- Fills: baseline's "pre-v1 RSI self-architecture revision note" — now the actual
  mechanism, failure, and revision discipline.

### 3. FILE 28 — R33-N15 result: DEVELOPMENT GATE FAILED (strength-trial ancestor)
- Drive: `TNN/TNN/Research/R33_NATIVE_N15_PRESERVATION_ADDITIVE/RESULT.md` | size 6036
- Verdict: **NEW** — stability/plasticity microlearner, 2026-09-07 prereg (FILE 01, also NEW).
  Development gate FAILED (arm10 selected by fallback, deficit 11 > 4); confirmation forbidden.
  Honest-fail discipline: "They must never be rerun, retuned, or relabeled as confirmation."
- Key diagnostic: "arm10's training-anchor loss is **0** while unseen old probes still degrade.
  The preservation mechanism is therefore succeeding on the protected training anchors
  without generalizing that guarantee across the broader old-behavior distribution."
- Arm taxonomy maps onto today's strength-trial arms: 1 shared rewrite / 4 strict
  preservation / 8 additive medium / 10 additive+preservation.
- Fills: design rationale for the graded/uniform/hybrid strength-trial design (baseline
  item 1).

### 4. FILE 32 — V91 semantic-KAT recovery B: recovery FAILED (blockers named)
- Drive: `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/reviews/RECOVERY_B_INDEPENDENT/README.md` | size 5955
- Verdict: **NEW** — final claim: "custody inputs only; actual generated outputs 0;
  admission CLOSED91; missing exact method/source inputs and full-condition reconstruction
  remain blockers." Required R23 source missing: `src/r23_experiments.py`, 63069 bytes,
  SHA `17eb325…e366d4b642`; "The author's reconstructed dataset still fails 0 of 16 row
  matches" — wait, 0-of-16 matches means all 16 FAILED to match.
- Extends baseline's "perceptual origins and trace-op semantics proven unrecoverable" with
  the actual V91 recovery verdict and missing-artifact identity.

### 5. FILE 38 — znc compiler bug #4: const recognition across import boundary
- Drive: `TNN/TNN/Research/R33_CONTINUING_LIFE_V1/NATIVE_SOURCE_PROJECTION_20260915/README.md` | size 5689
- Verdict: **NEW** — extends baseline's "three znc compiler bugs" to a fourth: "The native
  parser source explains the failure: `selfhost/parse.zag` registers const names in each
  Parser's separate `consts` list... An imported caller does not inherit that parser-local
  list." Direct V68 fails 7 checks, V73 fails 81; projected-source (dependency-before-caller
  ordering) closes qualification. Anchors Micah's dev paths: `/Users/Shared/micah/Documents/zag/znc`.

### 6. FILE 02 + FILE 18 — N17 continuity reviews V3/V4: REQUEST_CHANGES, R25 lineage terminal blocker
- Drive: `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/INDEPENDENT_REVIEW_V4.md` (7106) and `.../INDEPENDENT_REVIEW_V3.md` (6300)
- Verdict: **NEW** — R25 lineage is a *terminal* blocker: "All four required artifacts are
  still `MISSING`" (accepted R25 state, release manifest, accepted policy, root receipt);
  the R26→R27 continuity chain "cannot be closed." 33-row verifier matrix: 30 of 33 rows
  blocked/pending; fixtures SPECIFIED_NOT_FROZEN_NOT_EXECUTED. V3 adds F6: the whole-packet
  manifest was stale (five failed hashes, omitted Work Package A).
- Fills: design rationale for why R27 continuity was abandoned (baseline item 1); distinct
  from the already-known pre-git session-file hunt.

---

## NEW — R32 sequential-frontier (E51 line) test results never seen

All R32, frozen 2026-08-30/31, branch `r32-agent-sequential-frontier`, R27 canonical.
Baseline mentions only E45/E48.

- **FILE 19** — E51M result (6283): `CALIBRATION_DOSE_SIGNAL; NO EXACT RESCUE`. Full 12-arm
  dose×capacity grid; best no-unique 1,162/1,200 (2×,16 hinges); capacity 0→4 hinges
  improved both dimensions at every dose; non-monotonic beyond. Invalid-run disclosure:
  "run at GitHub Actions `33343784134` remains retired as an invalid
  seed-namespace-exhaustion run. Its grid is not evidence."
- **FILE 25** — E51V result (6118): `TRAJECTORY_OBJECTIVE_TRADEOFF` — 4,191/4,200 known,
  1,195/1,200 no-unique (one paired loss blocked rescue); "E51V strongly rejects the
  hypothesis that dynamic graph/connectivity machinery is already required for the residual
  R32 terminal problem."
- **FILE 34** — E51Y result (5829): `VALID NATIVE NEGATIVE — FIVE_WAY_CONTINUATION_VALUE_MIS-CALIBRATED`.
  Continuation arms over-continue/stop wrongly (local-384: -169,578 utility vs 529,800
  terminal-only control; 274/1,200 no-unique wrong). Terminal learner reproduced at
  4,200/4,200 + 1,200/1,200 before CONTINUE training.
- **FILE 00** — E51Z result (7161): `VALID DIAGNOSTIC — MIXED_STOPPING_FAILURE`.
  "the strict E51Y no-unique zero-wrong gate is structurally impossible for at least
  seven fresh no-unique trajectories under the frozen E51X terminal learner and E51Y
  resource transition geometry." Also: E51Y's scalar utility target explicitly conflicts
  with success-preservation on 2,328 reachable states.
- **FILE 43** — E51P result (5596): `VALID NATIVE NEGATIVE` — 32-cell expert:
  "4,200 ; 1,170" (known/no-unique). Causal fact: "context-dependent local feature weights
  are materially more expressive than global calibration or one scalar local offset."
- **FILE 47** — E49 (5505, frozen 2026-08-28): `EXECUTED_VALID_NATIVE_NEGATIVE —
  NO_TESTED_GROUNDED_QUADRATIC_RESCUE`. The quadratic feature "reduced no-unique UNKNOWN
  by 600 and added 600 wrong commitments relative to the matched joint batch control."
- **FILE 36** — E51AJ analysis README (5737): `REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE`,
  "retention direction: `MIXED_OR_UNREPLICATED_RETENTION_DIRECTION`."

## NEW — results cited inside preregs (never in baseline)

- **FILE 04** E51G prereg (7013): cites E51F (terminal states exactly distinguishable on
  fresh validation) and E51E baseline (1,125/1,200 no-unique reachability).
- **FILE 10** E51M prereg (6611): cites E51K ("rank-preserving scalar calibration errors
  are already present on development worlds" — bottleneck not fresh-world transfer) and
  E51L (top-commit sign supervision moved frontier but couldn't fit harmful-commit side).
- **FILE 13** E51P prereg (6483): cites E51O — "learner-recruited local regions carry real
  but weak calibration signal": 8→64 cells moved 4174/1163 to 4175/1166 then saturated.
- **FILE 22** E51U prereg (6216): cites E51R/S ("much longer optimization... gives only
  small capability movement") and E51T ("96→192 sweeps does not create a capability
  superset: gained 5 trajectories and lost 5 others while aggregate reachability remained
  unchanged" — "residual decision boundary is therefore unstable under additional linear
  coordinate fitting").
- **FILE 26** E51E prereg (6103): cites E51D frozen-terminal reachability veto — "599/4,200
  known episodes... never expose a correct terminal commit at any feasible stopping time,
  and 179/183 no-unique episodes never expose UNKNOWN."
- **FILE 27** E51X prereg (6039): cites E51W — 96- and 192-sweep arms "preserved 4,200 /
  4,200 known reachability and reached 1,198 / 1,200 no-unique UNKNOWN reachability."
- **FILE 37** E51L prereg (5697): cites E51I ("every known validation episode already
  contains a stopping state where the correct commit action is top-ranked... one global
  commit shift cannot jointly expose all known decisions and all no-unique UNKNOWN
  decisions") and E51J.
- **FILE 40** E51R prereg (5649): cites E51P result (4,200/4,200 + 1,170/1,200) and E51Q
  ("found 26 blocked no-unique trajectories, no exact learner-state aliases, and no
  feasible uniform score shift").
- **FILE 42** E51AC prereg (5618): cites E51AA ("mature report geometry has a
  resource-feasible action-support ceiling") and E51AB ("replacing the mature terminal
  controller with direct candidate-return heads is destructive... only 3,324 / 4,200").
- **FILE 44** E51C prereg (5558): cites E51B ("reduced no-unique wrong commitments by 68
  in the primary M0 model and 72 in M1" but net utility failed).
- **FILE 45** E51S prereg (5556): cites E51R (12→24→48 sweeps: no-unique 1,165→1,166→1,166;
  48-sweep still accepted strict development-loss improvements at the ceiling).
- **FILE 49** E51J prereg (5402): cites E51I — "one global commit shift cannot satisfy both
  sides: all-known reachability required a uniform integer shift of at least +57, while
  all-no-unique UNKNOWN reachability required at most -631."
- **FILE 05** E51V prereg (6941), **FILE 39** E51N native README (5659, replication reducer
  design: pareto_pass rule, 2-of-3 replica gate, frozen arm schedule 0=BASE..4=D2C4):
  NEW one-liners.

## NEW — R33 engineering design rationale

- **FILE 08** R33_MASTER_PLAN (6772): the 18-stage R33 program's priority order, the
  no-repeat/freshness protocol ("E51M/N already tested calibration dose/capacity; E51AD
  already tested a preservation-constrained router; AH/AI/AJ already tested related
  residual/replay designs"), and stopping/promotion rules. Quote: "A new seed number is
  not by itself independent evidence." Baseline knows the 5-organ architecture, not this plan.
- **FILE 09** R33-B001-C03 prereg (6667): durable generic-transaction collector + native
  replay design (21 groups incl. crash hooks `os._exit(73)`, ENOSPC, hash corruption).
- **FILE 16** R33-N03 prereg (6356): native opaque-snapshot journal engineering primary —
  58 planned native child processes; BUILD02 changes from BUILD01.
- **FILE 03** R33-N12 result (7028): PASS — 9,723 completed-child checks, 0 failures;
  numeric-view engineering (11 dtypes, NaN payloads, first/last scalar bit probes;
  fresh-process replay byte-identical). Baseline has no N12.
- **FILE 14** N13A postrun review (6392) + **FILE 24** N13A result (6158): N13A
  `CONFIRM_BOUNDED_ENGINEERING_PASS`; N13 remains `FAIL_CONSUMED` at inventory-write
  (409,862,144 bytes) vs N13A 313,180,160 bytes — "bounded regression comparison only."
- **FILE 20** V92 README (6278): V92 state-image qual — 339 selftest PASS, exact
  245,472-byte V4 image (33 learner sections), 12 separate-process image/packet modes;
  "No V4 implementation defect was found."
- **FILE 29** R33-N07 result (5983): bounded authenticated-control engineering PASS
  (642 child + 368 parent checks); preregistered negative witness — "An authentic MAC
  chain alone does not tell this implementation that a newer suffix once existed
  elsewhere" → next layer needs an "independently protected high-water authority outside
  learner rollback." Directly relevant to force-pin authority work.
- **FILE 30** E51N prereg (5973): E51M's integrity failed — "could not assign 2,440 of
  29,160 requested fresh worlds... E51M's printed dose/capacity measurements are therefore
  non-authoritative"; domain-separated RNG repair design. (Note: FILE 30 was frozen the
  same day as the E51M rerun in FILE 19 — the rerun, not the E51N plan, is the current
  E51M authority.)
- **FILE 23** E48 prereg (6195, frozen 2026-08-23): `WITHDRAWN_BEFORE_SOURCE_OR_EXECUTION`
  — post-E47 audit showed it would "remeasure the already-established E46 order effect";
  "The active E48 preregistration is the matched online versus batch 2×2 discriminator."
  Also records E46 ("large presentation-order abstention/known-resolution tradeoff") and
  E47 results.
- **FILE 21** N19 review V2 (6227): N19 `REQUEST_CHANGES` — host ABI unqualified
  (capability-safe macOS/APFS contract missing), no runtime evidence, macOS release/SDK
  unfrozen. Documents why N19 never executed.
- **FILE 31** N19 Lane-C review (5968): `PASS_BOUNDED_NATIVE_ENGINEERING` for V6/runtime +
  V3/direct-child supervisor snapshot (lane-scoped, not a global pass). BUILD_08 "remains
  rejected historical evidence."
- **FILE 48** N19 PROCESS_GAPS review (5468): companion bounded PASS + honest custody
  incident (worker deleted C during concurrent review; six reviewer-baselined sources
  restored exactly).
- **FILE 50** N19 supplement review (5352): staging/amendment interpretation; broad
  all-Research preservation "remains qualified," not claimed — honest scoping.
- **FILE 51** N19 review V1 (5315): `REQUEST_CHANGES` — telemetry schema/emitter mismatch
  (16-column output vs 14 declared fields) plus ABI blockers. Companion to FILE 21.

## CONFIRMS (one line each)

- FILE 01 (0105, 7154): N15 preregistration — actually NEW (see above under #3); listed here in error → treated as NEW.
- FILE 07 (0111, 6851) N12 preregistration: CONFIRMS the N12 PASS in FILE 03 (same 160-byte rows, 7,089 REDUCE descriptors).
- FILE 11 (0115, 6578) N14 preregistration: CONFIRMS baseline's N14 S1 PASS envelope
  (8 packets, 12 metadata fields, 14 malformed refusals, `sn_observe`).
- FILE 12 (0116, 6575) N14 postrun review: CONFIRMS bounded engineering pass; wrapper
  `/usr/bin/date` path defect preserved (do-not-backfill).
- FILE 15 (0119, 6356) B001-C01 preregistration: CONFIRMS baseline's B001 context (native
  component regression, 77 scalars/40 vectors, 65,536-codeword PCM oracle).
- FILE 17 (0121, 6337) N06 preregistration: CONFIRMS baseline's N06 S0 PASS envelope
  (377,264 observer values, 636 metadata fields, 12-field metadata, TNNRAW01).
- FILE 33 (0137, 5921): duplicate copy of FILE 20's V92 README inside the
  R33_CLOSEOUT_20260915T174458Z snapshot — CONFIRMS (identical content).
- FILE 35 (0139, 5744) E51W prereg: restates the E51V result numbers already in FILE 25;
  prereg only — CONFIRMS.

SUPERSEDED: none (no doc is overtaken by another in the same batch).
NOISE: none.

---

## Dates / people anchors

- 2026-08-23: R5 results, R6 RSI results, E48 withdrawal prereg, E49 prereg — the oldest
  strata in this batch (pre-v1 → R32 transition era).
- 2026-08-30/31: E51G/V/AF/M/P/U/E/X/W/C/R/S/L/J/AC/Y/Z preregistrations frozen and most
  results executed — the R32 sequential-frontier sprint.
- 2026-09-06: N03 admission, N12/N13A/N14 primaries executed; 2026-09-07: N14/N15
  preregs; 2026-09-09: N17 reviews V3/V4, N19 reviews V1/V2; 2026-09-15: V92/N19
  recoveries, source-projection closeout.
- Machine paths: `/Users/Shared/micah/Documents/zag/znc` (pinned compiler),
  `/Users/Shared/micah/Documents/TNN/TNN` (workspace) — Micah's local dev machine.
- "Owner: main agent, sole registry writer and launcher" — process archaeology: a single
  main agent ran the R33 native campaign with strict single-writer allocation
  ("Allocation is single-writer; no subagent launches experiments").

## Contradictions with baseline

- **Mild tension, not a contradiction:** E51N prereg (FILE 30) declares E51M's printed
  measurements "non-authoritative and must not influence learner selection" — but it was
  frozen 2026-08-30, the same day the E51M *rerun* (FILE 19, GHA 33364230156) repaired the
  namespace exhaustion and re-established authority. Both docs agree the *first* E51M run
  is invalid; current E51M authority is FILE 19's rerun. Flagged so the sweep doesn't
  propagate "E51M invalid" as a blanket verdict.
- No other contradictions found. The R32 line being absent from the baseline's wave list
  is a gap, not a conflict (the R33 master plan treats R32 as historical ledgers).
