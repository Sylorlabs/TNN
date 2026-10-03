# REPORT: COGOPS-LEARNOSC2 (outcome-record ablation)

Date: 2026-10-03. Worker: COGOPS-LEARNOSC-FOLLOWUP.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_learnosc2/`
Prereg: frozen commit d28d03584 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed). No
amendments after implementation began. One pre-commit
transcription fix to PREREG Section 7 (an S4 LSTATE-VFY line
carried a wrong prov field and a duplicated EP line from manual
copying) was corrected before the freeze commit and mechanically
re-verified byte-identical against the parent's frozen
c7_run1.txt. Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K9 all PASS)

The outcome record is necessary for the reuse advantage. With
the record intact (S9), re-presentation of goal 818 costs 2
passes via the stored response (how=2, OSC-REUSE). With only the
OUTC entry count word zeroed (S10 ABLATE-818), the identical
stage costs the full invention path: 4 passes, confirm pass,
src=0, and the emitted cycle is byte-identical to the one
invented in S3. Nothing else in learner state was touched
(specs, index, plans, bindings, world facts persist), so the
2-pass to 4-pass difference is attributable to the outcome
record alone. K5's causal story from the parent report is now
lesion evidence, not correlation.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S10: `Q id=S10 goal=818 how=1 passes=4` | byte-exact, exactly once | PASS |
| K2 | S10 OSC-CYCLE byte-identical to S3/S9's | 3/3 lines identical (`lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]`) | PASS |
| K3 | `OSC-CONFIRM goal=818 ok=1`, `SPECCHK goal=818 spec=1`, `OSC-STATE goal=818 lag=2 nph=2 src=0`; no OSC-REUSE in S10 | byte-exact; OSC-REUSE count 0 in S10 region | PASS |
| K4 | lines S1A..S9 byte-identical to parent c7_run1.txt; only differences: appended S10 stage + SUMMARY `plans_loaded=3` | prefix cmp-identical; diff shows exactly the 11-line S10 block and plans_loaded 2 to 3 | PASS |
| K5 | c8_base/world/learn cmp-identical to parent; c8_main differs only by outc_clear + S10 block; zero world literals in new code | all cmp/diff verified; new code holds only the 14500 structural offset and the S10 label | PASS |
| K6 | 3/3 byte-identical stdout, stderr empty | sha256 ae0ae3bf x3; .err 0 bytes | PASS |
| K7 | safebin, no python, pure Zag, pinned znc, no `while.*!(` | verified; learn is a byte copy of the parent | PASS |
| K8 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |
| K9 | scope honesty in this report | stated below | PASS |

Additionally, the full 90-line observed stdout is byte-identical
to PREREG Section 7 (mechanical cmp, not eyeballed).

## Causal reading

- Necessity: the lesion removes exactly one word of learner
  state (OUTC count at L+14500). The S10 stage otherwise
  mirrors S9 (same world, same episodes, same re-specialize,
  same goal). Reuse disappears; invention returns. The
  alternative hypotheses fail: specs still work (SPECCHK=1,
  SPEC/LSTATE lines healthy), the plan still loads
  (plans_loaded=3), the world is unchanged. The record drove
  the reuse.
- The fallback is exactly the invention path, not a degraded
  mode: 4 passes (vs 2), confirm pass predicts, src=0
  (re-invented, not replayed), and the reconstructed cycle is
  byte-identical to S3's. Cost accounting: 2 passes (record)
  < 4 passes (invention) < 16 (generic cap).
- What the lesion does NOT show (honest boundary): sufficiency
  (the record alone, without trajectory machinery, was not
  tested and is not claimed); learner-invented detection (the
  recurrence scan is untouched generic machinery); L3
  representational invention (no new representation, primitive,
  or procedure form; the 12-criterion bar is not claimed).

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `$HOME/safebin` verified directly: 49 entries,
no python3/python; the lane's safebin_setup script does not
exist in this checkout, same as the parent worker's finding).
`which python3` / `which python` return nothing; pinned znc
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure
Zag; shell only for znc/binary/git/assembly/byte
verification. Zero forbidden-executable invocations. New Zag
scanned for the `while.*!(` negated conjunction pattern:
clean. Git writes via /usr/bin/git absolute path, explicit
pathspecs, current branch only, nothing pushed.

Note: the parent's c7_build.sh carried a stale lane path
(`$HOME/workspace/tnn-rsi/...`); this lane exists in both
`tnn-rsi` and `tnn-rsi-gpi3` checkouts with identical content.
The c8_build.sh in this lane points at tnn-rsi-gpi3, the git
worktree used for all commits here.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_learnosc2/`:
PREREG.md (frozen, commit d28d03584), NAMECHECK.md (Step 0),
c8_base.zag (cmp-identical to c7_base.zag), c8_world.zag
(cmp-identical to c7_world.zag), c8_learn.zag (cmp-identical
to c7_learn.zag; learner code untouched), c8_main.zag (parent
plus outc_clear fn and the S10 stage; diff-verified), c8_build.sh,
c8_full.zag (assembled; exactly one `fn main`), c8_bin,
c8_compile.txt, c8_run1/2/3.txt (sha256 ae0ae3bf x3) + .err
(empty), REPORT.md (this file).

## Remaining follow-ups (for the parent, not decided here)

1. Learner-invented DETECTION (parent report follow-up 1):
   the recurrence scan remains generic machinery.
2. Lag above 3, 3+ node cycles (parent follow-up 2 / Option C):
   the driver still declines these by design.
3. Cross-goal analogy: whether a stored response can bootstrap
   handling of a structurally similar but new oscillation.
4. Sufficiency direction: the lesion shows necessity; a
   complementary experiment (record present, trajectory
   machinery impaired) is not yet designed.
5. C459 report recovery/cross-check (parent follow-up 5):
   still open.
