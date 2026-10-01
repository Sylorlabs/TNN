# TNN-2 Cycle Governance Audit

**Auditor:** TNN-2 Cycle Governance Auditor (subagent).
**Date:** 2026-10-01 UTC.
**Scope:** TNN-2 cycle: prereg (`7c1e30522`) -> build (`f4de7ff46`) ->
repro (`fdf1fa626`) -> freeze prereg (`ce1a7c5f8`) -> shim (`23c2c0206`)
-> freeze eval (in progress, uncommitted at audit time).
**Method:** safebin-only verification; independent re-checks of hashes,
byte-identity, commit ordering, and source scans; review of each
worker's NAMECHECK.md Step 0 and kill-bar evidence.
**Verdict: GOVERNANCE-AUDIT-PASS** (one open caveat, not a violation;
see item 9).

## 1. Prereg commit-order: PASS

- TNN-2 prereg `7c1e30522` committed 2026-09-30 21:20:50 -0700.
- TNN-2 build `f4de7ff46` committed 2026-10-01 04:43:54 +0000
  (21:43:54 -0700). Strictly after the prereg.
- `git merge-base --is-ancestor 7c1e30522 HEAD` true at build start
  (HEAD was the prereg commit itself); re-verified by the auditor
  via `git rev-list --reverse 7c1e30522..23c2c0206`, which orders
  `f4de7ff46`, `fdf1fa626`, `ce1a7c5f8`, `23c2c0206` strictly.
- Freeze prereg `ce1a7c5f8` committed 2026-09-30 21:45:59 -0700.
- Shim `23c2c0206` committed 2026-10-01 04:47:00 +0000 (21:47:00 -0700).
  Strictly after the freeze prereg; `git merge-base --is-ancestor`
  verified by the shim worker before implementation.
- The freeze prereg correctly references the already-completed build
  and repro commits as frozen inputs; no rule requires the freeze
  prereg to precede the build it freezes.

## 2. Kill bars and falsifiers: PASS

- K-T2-1 through K-T2-8: all reported PASS in
  `tnn2_build/TNN2_BUILD_REPORT.md` with per-bar evidence.
  Auditor independently re-verified:
  - K-T2-1 ordering (git ancestry, see item 1);
  - K-T2-2: `execute` byte-identical to frozen base (cmp, see item 3);
  - K-T2-3: removed template names have zero code hits (repro
    spot-check confirms; auditors saw comment-only `exec_plan`
    references).
- No kill bar was weakened or retroactively altered. The K-T2-5
  wording permitting the hardcoded 0 fallback "only for the
  empty-policy edge case" is in the frozen prereg text itself,
  not an amendment.
- Falsifiers F-T2-1..F-T2-4: none triggered per build report;
  auditor's ISA scan (item 3) and scope scan (item 7) found no
  counter-evidence.
- K-FZ2-1..K-FZ2-5 (freeze cycle): K-FZ2-1 ordering verified (see
  item 1); K-FZ2-2 before-hash verification confirmed by shim
  report and eval NAMECHECK (4/4 hashes via sha256sum before any
  world exposure); K-FZ2-3 zero-cognition attested in shim report;
  K-FZ2-5 seal: eval NAMECHECK records 16/16 FW world files
  re-verified against SEAL.md from seal commit `396895595`.
  K-FZ2-2 after-verification and K-FZ2-4 determinism are the
  evaluator's own bars and are pending its completion (see item 9
  caveat).
- F-FZ2-1..F-FZ2-3: none triggered.

## 3. ISA freeze: PASS

- `fn execute` in `tnn2_build/tnn2.zag` is byte-identical to the
  frozen TNN-1 ACT-remediated base (`d3895083c9f8...`), verified
  by cmp on the extracted function bodies. The 4-op ISA
  (MOVE/BRANCHEQ/INC/DEC, tags 101-104) is unchanged.
- No new opcodes, modes, bridges, handlers, or semantic cases.
  Auditor grep for MODE/bridge/handler hits only:
  - a comment restating the ISA freeze;
  - a comment restating no-new-modes in the inquiry integration;
  - `t_r_pact5`, an existing ACT-suite test name, not new machinery.
- Function count: base 169, TNN-2 168 (net deletion; fixed templates
  removed, no subsystem accumulation).
- Node types: originals only (1,2,3,4,20,21,30); T_PLAN/T_STEP
  removed. Matches the build report's F-T2-1 evidence.

## 4. Pure Zag: PASS

- Builder, reproducer, shim builder, and evaluator all record
  Step 0 safebin activation with `which python3 python` empty and
  zero forbidden invocations.
- The two documentation-only preregs (`tnn2_prereg`,
  `core_freeze_tnn2`) noted `/usr/bin/python3` present as an
  unremovable system binary with documented non-use and performed
  no research computation, scoring, or analysis. No violation of
  the pure-Zag research-computation rule.
- Auditor scan of all TNN-2 cycle directories (including
  `core_freeze_tnn2_eval/`) found no Python/C/JS/Rust usage; the
  only `python` matches are toolchain-guard records in NAMECHECK
  files.
- Eval battery scripts are POSIX shell plus safebin tools
  (sha256sum, grep, awk, cmp, cp); scorers are Zag
  (`grade_plan.zag`, `probe_score.zag`). Shell used only for
  orchestration, per standing rules.

## 5. Safebin: PASS

- TNN-2 build: NAMECHECK.md Step 0 records safebin setup,
  restricted PATH, `which python3` exit 127.
- TNN-2 repro: Step 0 records safebin, pinned znc hash verified
  (`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- Shim: Step 0 records the full safebin setup sequence.
- Evaluator: Step 0 records safebin setup for all work.
- This audit: Step 0 recorded in `tnn2_governance/NAMECHECK.md`.

## 6. Hash integrity: PASS

Auditor re-verified on disk with sha256sum; all match frozen values:

| Artifact | Frozen | On-disk | Result |
|---|---|---|---|
| `tnn2_build/tnn2.zag` | `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` | same | PASS |
| `tnn2_build/tnn2_bin` | `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b` | same | PASS |
| `core_freeze_tnn2_shim/freeze_shim2.zag` | `33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8` | same | PASS |
| `core_freeze_tnn2_shim/freeze_shim2_bin` | `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954` | same | PASS |

- Shim construction claim independently re-verified by the auditor:
  `tnn2.zag` minus line 1357 (`fn main()i32 { return run_all(); }`)
  is byte-identical to the first 1590 lines of `freeze_shim2.zag`;
  remaining 161 lines are the appended driver. 1590 + 161 = 1751.
  All TNN-2 cognition lines preserved byte-identical.

## 7. Scope discipline: PASS

- Added functions in `tnn2.zag` vs base: `t2_*` trial/constructor
  family (19), `miss_inquire`, `promote_graph`,
  `revise_on_contradict`, `t2_revise_graph`, five `t_t2_*` tests,
  `tnn2_init` (rename of `tnn1_init`). Every addition maps to one
  of the three preregistered changes.
- Removed functions: the fixed plan templates, `exec_plan`, their
  helper vocabulary, `exact_lu` (only caller removed),
  `promote_map` (superseded by `promote_graph`, which keeps the
  frozen MAP node layout), SK_*/TM_* constants, T_PLAN/T_STEP.
  All removals were required by K-T2-2/K-T2-3.
- `promote_graph` keeps the frozen MAP node layout per the build
  report; not a new semantic case.
- Test-count wording note (not a violation): the prereg cites
  "existing TNN-1 test suite (35/35) plus the ACT suite (24/24)"
  while the build reports 41 test groups copied with assertions
  verbatim (15 CLA-2 core + 6 ACT + 14 cognition + 6 ACT-remediation
  groups). The 24 ACT items are assertions within 6 groups; the
  assertions are recorded as verbatim copies with only the init
  call renamed. No scope creep found.
- The five new tests (T2-CHAIN4, T2-REJECT, T2-INQUIRE, T2-ACTLIVE,
  T2-REVISE) are required by K-T2-3 through K-T2-6, not
  unpreregistered features.

## 8. Verdict discipline: PASS

- TNN-2 build: `TNN2-BUILD-PASS` only. Report explicitly states
  "(SURVIVES requires the 11-step pipeline; not claimed.)"
- TNN-2 repro: `TNN2-REPRO-PASS` only, scoped to pipeline step 4,
  with the remaining steps listed as open.
- Auditor scan of all TNN-2 cycle documentation found no
  `SURVIVES`, premature L3, or Criterion 0 claims.
- Compression failure recorded honestly: 1591 lines vs the frozen
  1200-line ceiling, reported as a separate un-waived axis per
  Micah's ruling.

## 9. Contamination: PASS (with caveat)

- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: zero
  uncommitted diff; `git log 7c1e30522..HEAD` shows no commits
  touching it in the TNN-2 cycle. Verified untouched.
- Sealed FW assets: seal commit `396895595` exists
  (2026-09-30 18:20:31 +0000, 16 world files + FW6 responder).
  `git diff 396895595..HEAD` on `freeze_worlds_v2/` is empty:
  no post-seal modifications. No commit in the TNN-2 cycle
  touches the sealed worlds.
- The only accessor of sealed worlds is the authorized
  CORE-FREEZE-TNN2 evaluator, via the battery scripts that
  verify the binary hash before every world (VOID exit 10 on
  mismatch). Evaluator runs read world files; they do not modify
  them.
- **Caveat:** at audit time the freeze evaluation was still
  running and its report uncommitted (`FREEZE_REPORT.md` draft
  present: FW battery runs in progress, old-world battery
  pending, K-FZ2-4 determinism self-marked PENDING). This audit
  therefore covers the cycle through the shim and the eval's
  setup/governance; the evaluator's final K-FZ2-2-after,
  K-FZ2-4, and K-FZ2-5 confirmation are its own bars to close on
  completion. This is not a governance violation: evaluation
  assets were frozen before world exposure, and no cognition
  edits occurred after exposure.

## Findings

No violations found. Minor record-keeping note in item 7
(test-count wording). Open caveat in item 9 (evaluation in
progress; evaluator must close its own K-FZ2 bars and commit).

## Verdict

**GOVERNANCE-AUDIT-PASS**

The TNN-2 cycle (prereg, build, independent reproduction, freeze
prereg, driver shim) is governance-compliant: commit ordering
holds, all applicable kill bars are satisfied with evidence, no
bar was weakened or altered after the fact, the ISA remains
frozen, the toolchain was pure Zag under safebin at every step,
all frozen hashes verify, builders stayed within prereg scope,
verdicts are correctly limited to BUILD-PASS/REPRO-PASS with no
L3 or SURVIVES claims, and neither the contaminated paper nor the
sealed FW assets were touched outside the authorized evaluator.
