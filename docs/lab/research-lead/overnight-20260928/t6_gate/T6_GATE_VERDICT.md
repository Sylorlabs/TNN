# T6 Gate Verification: T6-GATE-READY

Date: 2026-09-30.
Checker: T6 Unblocker.
Gate source: PREREG_BATTERY_V2.md section 3.7 and section 5 (commit d2a69d512).

## Frozen gate text (verbatim from the prereg)

"T6 evaluation launches only after ALL of: (i) freeze commits of every
hypothesis evaluated under v2 (B, C2, and D's K4-clean rerun commit) are
in ancestry; (ii) the Battery v2 prereg is frozen; (iii) the sealed T6
spec commit strictly follows (i) and (ii). A and C are falsified under
v1 and do not gate T6."

Section 5 K2: "no v2 evaluation launches until D's clean rerun commit
and B's freeze commit are in ancestry."

Section 5 K1: the battery v2 prereg freeze commit must strictly precede
every v2 implementation or evaluation commit.

## Ancestry verification

All checked with `git merge-base --is-ancestor <commit> HEAD` on
branch tnn-native-lab (HEAD 4ecbc2c6d at check time). All present:

| Commit | Role | In ancestry |
|--------|------|-------------|
| 69730b4ab | B freeze (hyp_b implementation + B-TESTED result) | YES |
| 9e2fbd134 | B prereg (frozen before B implementation) | YES |
| f313372d7 | C2 v2 implementation + results (C2-F5 FIRES) | YES |
| 9bc64e4cf | C2 v2 prereg amendment (frozen before v2 code) | YES |
| cdffdcca9 | C2 K4-clean rerun result (byte-identical to f313372d7) | YES |
| d01f4cb8a | C2 clean rerun prereg (frozen before build/run) | YES |
| 2500fd02b | D K4-clean rerun commit (D-V2-FAIL) | YES |
| 2a32cb75e | D v2 prereg (frozen before implementation) | YES |
| d2a69d512 | Battery v2 prereg freeze | YES |
| 7c34fe1d1 | GENEXEC2-P build (conformance PASS) | YES |
| f26f432dc | T6 sealed spec DRAFT (T6-DRAFT-COMPLETE, not sealed) | YES |

## Ordering verification

All required strict precedences hold (verified by ancestor checks,
each pair distinct commits):

- d2a69d512 strictly precedes f313372d7 (battery prereg before C2 v2
  implementation: K1 satisfied).
- d2a69d512 strictly precedes 2500fd02b (battery prereg before D v2
  rerun evaluation: K1 satisfied).
- 9bc64e4cf strictly precedes f313372d7 (C2 v2 amendment before v2
  code: K2 checklist satisfied).
- 2a32cb75e strictly precedes 2500fd02b (D prereg before D rerun:
  commit-order rule satisfied).
- d01f4cb8a strictly precedes cdffdcca9 (C2 clean prereg before clean
  runs: commit-order rule satisfied).
- 9e2fbd134 strictly precedes 69730b4ab (B prereg before B
  implementation: commit-order rule satisfied).

## K4 status check (parent instruction)

- D (2500fd02b): K4-CLEAN. Worker report states zero Python at every
  stage. PASS.
- C2: original v2 wave (f313372d7) K4-VIOLATED (disclosed
  `python3 -c "pass"` invocation; amendment 286c8e681). Purity-repaired
  by K4-clean byte-identical rerun cdffdcca9 plus transparent addendum
  (C2_K4_AMENDMENT_ADDENDUM.md). Measurements are canonical.
- B (69730b4ab): K4-VIOLATED WITH DISCLOSURE. The result document states
  the worker invoked python3 twice (one prereg byte-check, one dummy
  compile-probe file generation); disclosure does not cure use. Builder
  verdict was BUILD-FAIL (K3 not met: T2 induction absent; K4 violated).
  The battery itself stands as B-TESTED: six tasks plus two transfer
  runs executed per the frozen protocol, 3/3 byte-identical runs,
  mechanism and harness pure Zag.

Note: the frozen gate text requires only that B's freeze commit be in
ancestry; it does not require a B clean rerun. B's capability
measurements (the content T6 discriminates on) are deterministic and
byte-identical. A B K4-clean rerun would strengthen the chain and is
recommended, but it is not a gate blocker under the frozen text.

## Gate status

**T6-GATE-READY.**

- Clause (i): satisfied. B freeze, C2 freeze, and D K4-clean rerun
  commits are all in ancestry.
- Clause (ii): satisfied. Battery v2 prereg d2a69d512 is frozen and in
  ancestry; its K1/K2/K3 kill bars hold.
- Clause (iii): actionable. No sealed T6 spec commit exists yet (only
  the draft f26f432dc). The sealed spec commit must be created strictly
  after all freeze commits; any new seal commit on current HEAD
  satisfies this automatically.

## Recommended next step

A sealer worker may now create the sealed T6 spec commit from
T6_SPEC_DRAFT.md (resolving any open decisions), strictly after the
freeze commits above, before any T6 evaluation runs.

## Kill bars

- K1 (ancestry verified): PASS.
- K2 (gate status determined): PASS. T6-GATE-READY.
- K3 (zero Python): PASS. Shell, git, grep, sed only. No em or en dash
  bytes in this document (shell-verified before commit).
