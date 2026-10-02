# Result: G0 Diagnostic on the Failing Unified Beam (R3 Arm 2)

Date: 2026-09-30. Worker: G0 Diagnostic Builder.
Status: FROZEN. Implementation and runs complete.

## 1. Provenance

- Prereg: PREREG_BEAM_G0.md, commit eb0ff7fdf (frozen before any
  implementation; commit-order self-check in section 7).
- Base: clean unified beam r3u.zag, commit fc03664f2
  (BEAM-UNIFIED-FAIL), sha256
  be9dba07c642573f518796d7b286e01d9493f8b310a13319455245d48aa07612.
- Instrumented copy: beam_g0/r3u_g0.zag (this commit). Frozen base
  untouched.
- Design: beam_next/BEAM_NEXT_DESIGN.md section 3, commit 446233dd5.
- Compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1 (pinned).

## 2. Build and run summary

- Control: unmodified r3u.zag compiled and run once. stdout md5
  6a8568a7232de691606e09712df0f17d, identical to the committed raw
  R3U_RAW_1/2/3.txt. Baseline reproduced; proceed.
- Instrumented build: r3u_g0.zag compiled clean (no new warnings
  attributable to the instrumentation; the two edits were a missing
  z_free definition copied from lifetime_race/race_tnn.zag line 17).
- Three instrumented runs. stdout md5 all three:
  6a8568a7232de691606e09712df0f17d. stderr empty all three runs.
- F-NOPERTURB holds: instrumented stdout byte-identical to the
  committed uninstrumented failing run. Diagnostic logs were read
  only after this check passed.
- Diagnostic log determinism: g0q_run1/2/3.log byte-identical,
  md5 632ea9f1487d87418581c0d250803475, 32322 lines each.
- Run artifacts: G0Q_RAW_1/2/3.txt, G0Q_RAW_1/2/3.err,
  g0q_run1/2/3.log, G0Q_CTL.txt, G0Q_CTL.err.

## 3. Q counts (A2-REUSE, rounds 0..24)

Q = (depth 3, operator histogram [2,1,1,0]), the species signature
occupied by the true target E = OR(AND(D,Y4), AND(NOT(D),Y5)).
Analysis by shell tools only (awk/grep); two independent formulations
agree.

- PROPOSED_Q = 4. All four Q-signature candidates appear in round 2
  (indices 42, 43, 44, 117; evidence accuracies 1, 1, 1, 9 of 64).
  No Q-signature candidate is proposed in any other round.
- MERGED_Q = 4. Round 2's merge loop (150 merge events) absorbed the
  Q species in a single event (M line "M 2 2 3 2 1 1 0" present
  exactly once). All four candidates shared that species key, so all
  four were absorbed together.
- RETAINED_Q = 0. None of the four candidates is in the final picked
  set of round 2 (P fates all 0), and no Q candidate appears retained
  in any round.
- PRUNED_Q = 0. No Q candidate lost its slot while its own species
  survived; every proposed Q candidate's species was absorbed.
- MERGED_AND_RETAINED = 0.

Per-candidate table: G0Q_QCANDS.txt.

## 4. Verdict

Per the frozen decision rule (prereg section 6):
PROPOSED_Q > 0 and MERGED_Q > 0 and RETAINED_Q == 0 resolves branch
(b). PRUNED_Q == 0 rules out branch (c) and the mixed case.
F-G0-INCONCLUSIVE does not fire (RETAINED_Q == 0).

**Verdict: G0-MERGED.**

## 5. Honest observations (do not move the bar)

- The absorbed Q candidates had low evidence accuracy (1, 1, 1, 9 of
  64): they were E-shaped structurally but not the true E
  behaviorally. The frozen rule classifies structurally, so the
  verdict stands as G0-MERGED. A future G2 builder should note that
  these particular candidates would likely also have lost a fair
  within-species retention fight; the diagnostic cannot separate
  "merged, then would have lost anyway" from "merged, then might
  have won" from this log alone.
- The Q species was absorbed in round 2, the earliest and heaviest
  merging round (150 events). Species small enough to be absorbed in
  round 2 are exactly the rare structural signatures.
- No Q-signature candidate was ever proposed in rounds 0-1 or 3-24.
  The generator proposes E-shaped structure only once, briefly, and
  the merge rule removes it the same round.

## 6. Kill bars

- K1 (prereg frozen before implementation): PASS. Prereg commit
  eb0ff7fdf strictly precedes the first commit containing
  r3u_g0.zag (this commit). See section 7.
- K2 (diagnostic runs): PASS. Control reproduced the committed raw;
  3/3 instrumented runs byte-identical to it; F-NOPERTURB verified
  before any log was read; the trichotomy resolved cleanly
  (G0-MERGED, no mixed outcome, no inconclusive).
- K3 (pure Zag, deterministic): PASS. Zag at every stage; shell
  tools only for verification and analysis. Zero Python at every
  stage from task start. 3/3 byte-identical instrumented stdout
  runs, zero stderr bytes, 3/3 byte-identical diagnostic logs.
  Loop documentation dash-clean (shell-verified).

## 7. Commit-order self-check

Prereg first commit: eb0ff7fdf (PREREG_BEAM_G0.md only).
Implementation/result commit: this commit (r3u_g0.zag, BUILD_G0.sh,
run artifacts, this file). The prereg commit is a strict ancestor of
this commit; no implementation file existed at eb0ff7fdf.

## 8. Honest scope

G0 is a diagnostic. Its output is data, not a mechanism. No L3 claim,
no Criterion 0 claim, no Q4 revival. The G0-MERGED verdict selects
the conditional G2 branch of the frozen design for a future builder
to preregister; it does not itself repair anything. Bounded-L2
diagnostic evidence only.

## 9. Recommended next step (for the parent, not decided here)

A G2 preregistration per BEAM_NEXT_DESIGN.md section 4 conditional
branch G2 (conditional: G0-MERGED), with the round-2 evidence-accuracy
caveat in section 5 above recorded as a pre-registered alternative
explanation to be killed by the G2 design.
