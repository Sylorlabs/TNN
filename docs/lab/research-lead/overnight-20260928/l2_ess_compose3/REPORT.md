# REPORT: L2-ESS-COMPOSE3 (operator standing x [6,5,4,4] composition)

Verdict: **PASS** (all frozen kill bars hold; no falsifier fires).
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose3/`
Worker: L2-ESS-COMPOSE3 subagent (depth 2/2), 2026-10-03.
Non-ledger task (claim minting paused).
Prereg: PREREG.md (frozen alone at commit e63c1edd1, before implementation).
Binary: `f3_bin` (built from learner.zag + world_F.zag + driver_F3.zag
via pinned safebin znc 2026.07.0-dev; compile exit 0, A0102 warnings
only, same class as the chain4/ess builds).

## 1. What was built

The L2-ESS-COMPOSE standing learner, BYTE-IDENTICAL, on the
L2-COMPOSE-CHAIN4 [6,5,4,4] world. Zero learner source changes:
not one line, not one comment. This is the strongest test form
for the task's question: the exact frozen standing mechanism is
asked to scale to a 4-operator chain with no help.

- learner.zag: sha256-verified byte-identical copy of
  l2_ess_compose2's learner.zag
  (a7ac8a50848cd8f3ab958d844dd46f79f50eb7d9b33f93d7f127e4e9f11ff6ee),
  itself byte-identical to l2_ess_compose's. Its base is
  chain3's learner plus the purely additive standing
  integration; zero operator-semantic changes.
- world_F.zag: sha256-verified byte-identical copy of the
  l2_compose_chain4 lane's world_F.zag
  (9197c57320515f2a186a9bb752cc74ff7a46b27b4240ac1c4be3b7e5b6be58a2),
  itself byte-identical to chain3's world_E (the 44-fact
  world of the original [6,5,4] standing result).
- driver_F3.zag: new driver. Five arms, one binary, fresh
  16384B state each: UNGATED (mode 0), STANDING (mode 1),
  GLOBAL (mode 2, informational) on the F-world FULL sequence
  (QA + QD1..QD5 + four re-asks); PROB-UNG (mode 0) and PROB
  (mode 1) on the ESS probation world (reused verbatim:
  p_teach_initial / p_teach_recovery). d_teach_maps,
  d_runq, d_bar diff-verified byte-identical across the
  source drivers and reused verbatim; d_check_z4/z5/z6/z7
  copied verbatim from driver_F.zag. KB-SEAL clean (shell
  grep audit: 0 hits for operator/form names, standing
  offsets, trace tags, threshold/signature literals).

## 2. Kill-bar results

**KB-EFF (efficiency): PASS.** Tries QD1..QD5: UNGATED
6+11+16+22+30=85; STANDING 6+6+11+8+13=44. STANDING <
UNGATED and 85-44=41 >= 10. Per-query: QD1 6->6 (all
fresh), QD2 11->6 (phase-1 ops 1-5 skipped), QD3 16->11,
QD4 22->8, QD5 30->13. Savings concentrate where
history exists, and grow with chain depth: the 4-chain
saves 48%, vs 42% on [6,5,4] and 39% on [6,2,4].
Every predicted number (85, 44, 41, and the per-query
6/6/11/8/13) matches the prereg's hand-derived trace
exactly.

**KB-CORR (correctness): PASS.** QA/QD1..QD5
via/val/op/dec identical between arms; Z4/Z5/Z6/Z7
exact checks = 1 in both arms (d_check verifies every
descriptor field plus rel/fact rows, so rows are
field-identical); re-asks via/val/entered equal
(3/59, 4/63, 5/65, 6/65, entered=0). The [6,5,4,4]
chain is preserved exactly: INVERT Form A still fires
on Z5 in QD3 (op=4, via=5, val=65), INVERT Form B
still fires on Z6 in QD4 (op=4, via=6, val=65).

**KB-NOSKIP (no wrong skips): PASS.** 41 standing-skips
in ARM STANDING, every one paired with a same-query
same-phase same-source FAIL in ARM UNGATED (shell
cross-audit: zero unpaired skips, zero wrong skips):
QD2 5 (phase-1 ops 1-5), QD3 5 (phase-1 ops 1-5),
QD4 14 (phase-1 ops 1-5; Z4 ops 1-6; Z5 ops 1-3),
QD5 17 (phase-1 ops 1-6; Z4 ops 1-6; Z5 ops
1,2,3,5,6). The verifying operators are never skipped:
op6 QD1 phase-1, op5 QD2 Z4, op4 QD3 Z5, op4 QD4 Z6
all fire from fresh per-(src,sig) cells. The
twice-visited op4 on Z5 (QD4, QD5) is tried, not
skipped: its (4,4,6) cell carries SUC=8 from QD3, so
it is tried and correctly fails both times.

**KB-PROB (probation recovery): PASS.**
(a) PROB-UNG: PQ1..PQ7 val=-2, PQR op=2 val=62 (solver exists).
(b) PROB: PQ1..PQ7 val=-2, PQR op=2 val=62.
(c) PROB PQR trace: MR-OP-PROBATION 1 -> FAIL,
MR-OP-PROBATION 2 -> MR-OP-OK 2. The retired operator
recovers exactly when the world changes, on the
unchanged mechanism. No probation fires in the
F-world UNGATED/STANDING arms (max QTOUCH 5, as
predicted).

**KB-SEAL: PASS.** driver_F3.zag: zero operator/form
names, zero standing offsets, zero trace
tags/threshold/signature literals (shell grep, 0
hits on all patterns).

**KB-DET: PASS.** 3/3 byte-identical runs (sha256
2dd0e82d4f603e06015139dbfab0a007dff4e3a3933088552bc106613f01dfc2).

## 3. Informational: GLOBAL arm (mode 2)

Predicted qualitative outcome confirmed: QD1 op=6
val=59 tries=6; QD2 reroutes via op6 on Z4 (op=6,
val=63, tries=2; global cells do not distinguish
sources); QD3 val=-2 (op4 globally retired after
QD1, the INVERT link never fires, chain broken at
the third link); QD4 val=-2; QD5 val=-2; sum=17.
The context-vs-global conclusion transfers to the
4-chain: per-operator global retirement breaks the
chain at QD3 even though the mechanism routed around
the QD2 retirement via op6, while per-(op,src,sig)
standing preserves all four links. The (src,sig) key
is load-bearing on the 4-chain too. (GLOBAL shows
MR-COP-PROBATION tags as its shared cells heat up;
informational only, not a kill bar.)

## 4. Falsifiers

F-D (wrong skip): not fired (0 wrong skips in
cross-audit). F-EFF: not fired. F-CORR: not fired.
F-PROB: not fired. F-SEAL: not fired. F-DET: not
fired. In-binary FALSIFIERS = 0.

## 5. Interpretation: answers to the task's questions

**Does standing generalize to longer chains (4
operators)? Yes.** 85 -> 44 tries (48% fewer) with
zero solution changes, zero wrong skips, and
probation recovery, on the byte-identical frozen
mechanism. No [6,5,4,4]-specific adjustment was
needed.

**Is the efficiency gain similar or different?
Larger: 48% vs 42% ([6,5,4]) and 39% ([6,2,4]).**
The gain grows with chain depth because longer
chains revisit more (query, source) combinations
whose failures are already recorded: QD4 saves 14
tries and QD5 saves 17, both exceeding any single
query's savings on the 3-chains. Standing's value
scales with the amount of repeated structure, which
is exactly what longer composition chains produce.

**Does the src key correctly separate the two
INVERT applications (Form A on Z5, Form B on Z6)?
Yes.** Three pieces of evidence. First, the cell
trace: (4,4,6) records Form A's QD3 commit
(SUC=8), then QD4's and QD5's failed tries on Z5
(FAIL 0->4->8); (4,5,6) records Form B's QD4
commit (SUC=8) and is never touched by the Z5
failures. The two firings live in different cells
under the same signature (sig=6), separated by
src alone. Second, QD4 fires op4 on Z6 (tried from
the fresh (4,5,6) cell) immediately after failing
op4 on Z5 (the struck-then-tried (4,4,6) cell):
under a per-(op,sig) key the Z5 failure history
would have risked the Z6 firing. Third, the
verifying firings are never skipped while the
revisited op4-on-Z5 is tried-but-fails, which is
the exact behavior the key was designed for.

**Does [6,5,4,4] need a different standing design?
No.** The frozen mechanism sufficed with zero
source changes; the hand-derived trace predicted
every observed number, including all 41 skip
positions.

## 6. Disclosures and non-claims

- L2 evidence only (standing records reused across
  queries by fixed researcher-supplied gate/update
  formulas), not L3.
- One [6,5,4,4] chain on one shared family does not
  establish general standing composability at
  arbitrary depth; 5+ chains, the protected core,
  the continuing learner, scaling, and transfer are
  out of scope.
- The GLOBAL arm is informational, not a kill bar.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 semantic cases, 0 learner source
  changes, 0 world changes. Pure Zag, safebin
  toolchain, zero forbidden executables (Step 0
  verified at startup; `which python3` and `which
  python` empty under safebin PATH).
- No em/en dashes in loop documentation. Commits
  local with explicit pathspecs; nothing pushed. The
  compose, chain3b, chain4, ess_compose,
  ess_compose2, and builder lane directories were
  never modified.

## 7. Branch note

The shared main worktree (~/workspace/tnn-rsi) is
checked out on side branch lane-ma4b-20261003, not
tnn-native-lab. This worker operated in its own
worktree (~/workspace/lane-l2esscompose2-20261003,
branch lane-l2esscompose2-20261003, based on
tnn-native-lab) and landed commits on tnn-native-lab
via git plumbing (private index via GIT_INDEX_FILE,
read-tree + write-tree + commit-tree -p
tnn-native-lab HEAD + update-ref with old-value
check), per the shared-workspace git discipline.
Documented per the task's branch-issue instruction
(also in NAMECHECK.md).

## 8. Files

- learner.zag (byte-identical to l2_ess_compose2's),
  world_F.zag (byte-identical to l2_compose_chain4's),
  driver_F3.zag (new; 5 arms; KB-SEAL clean)
- f3_full.zag, f3_bin, f3_compile.txt,
  f3_run1/2/3.txt (3/3 byte-identical)
- PREREG.md (frozen alone at e63c1edd1), NAMECHECK.md
  (Step 0), REPORT.md (this file)

Commits: freeze e63c1edd1 (PREREG+NAMECHECK alone);
implementation + this report follow under explicit
pathspecs on tnn-native-lab, never pushed.
