# REPORT: L2-ESS-COMPOSE2 (operator standing x [6,2,4] composition)

Verdict: **PASS** (all frozen kill bars hold; no falsifier fires).
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose2/`
Worker: L2-ESS-COMPOSE2 subagent (depth 2/2), 2026-10-03.
Non-ledger task (claim minting paused).
Prereg: PREREG.md (frozen alone at commit bf7e8c2c6, before implementation).
Binary: `h2_bin` (built from learner.zag + world_H.zag + driver_H2.zag
via pinned safebin znc 2026.07.0-dev; compile exit 0, A0102 warnings
only, same class as the chain3b builds).

## 1. What was built

The L2-ESS-COMPOSE standing learner, BYTE-IDENTICAL, on the
L2-COMPOSE-CHAIN3B [6,2,4] world. Zero learner source changes:
not one line, not one comment. This is the strongest test form
for the task's question: the exact frozen standing mechanism is
asked to transfer to a different operator triple with no help.

- learner.zag: sha256-verified byte-identical copy of
  l2_ess_compose's learner.zag
  (a7ac8a50848cd8f3ab958d844dd46f79f50eb7d9b33f93d7f127e4e9f11ff6ee).
  Its base is chain3's learner plus the purely additive standing
  integration (diff vs chain3b's learner.zag shows only the
  standing block and gating insertions; zero operator-semantic
  changes).
- world_H.zag: sha256-verified byte-identical copy of the
  l2_compose_chain3b lane's world_H.zag
  (f76b290f8aad163bf16627d792683340cd571cc56e058e4901a93e7cb71d10d0).
  The chain3b lane is not merged into tnn-native-lab, so the
  copy is recorded here (NAMECHECK.md).
- driver_H2.zag: new driver. Five arms, one binary, fresh
  16384B state each: UNGATED (mode 0), STANDING (mode 1),
  GLOBAL (mode 2, informational) on the H-world FULL sequence
  (QA + QD1..QD4 + three re-asks); PROB-UNG (mode 0) and PROB
  (mode 1) on the ESS probation world (reused verbatim:
  p_teach_initial / p_teach_recovery). d_teach_maps is
  diff-verified byte-identical between the ESS driver and
  driver_H.zag and is reused verbatim. KB-SEAL clean (shell
  grep audit: 0 hits for trace tags, operator/form names,
  standing offsets).

## 2. Kill-bar results

**KB-EFF (efficiency): PASS.** Tries QD1..QD4: UNGATED
6+8+16+24=54; STANDING 6+3+10+14=33. STANDING < UNGATED
and 54-33=21 >= 10. Per-query: QD1 6->6 (all fresh),
QD2 8->3 (phase-1 ops 1-5 skipped), QD3 16->10, QD4
24->14. Savings concentrate where history exists, as in
[6,5,4]. Every predicted number (54, 33, 21, and the
per-query 6/3/10/14) matches the prereg's hand-derived
trace exactly.

**KB-CORR (correctness): PASS.** QA/QD1/QD2/QD3 via/val/op
identical (1/51, 3/59/6, 4/67/2, 5/68/4); QD4 val=-2 op=-1
both; Z1/Z2/Z3 exact checks = 1 both arms, rows field-equal;
re-asks via/val equal (3/59, 4/67, 5/68). The [6,2,4]
chain is preserved exactly: SUBSTITUTE still fires on Z1
in QD2 (MR-COP-OK 2 after MR-COMP-SRC id=3), INVERT Form B
still fires on Z2 in QD3 (MR-COP-OK 4 after MR-COMP-SRC
id=4).

**KB-NOSKIP (no wrong skips): PASS.** 21 standing-skips in
ARM STANDING, every one paired with a same-query same-phase
FAIL in ARM UNGATED (shell cross-audit: zero unpaired
skips): QD2 5 phase-1 (ops 1-5), QD3 5 phase-1 + 1 on Z1
(op1), QD4 5 phase-1 + 5 on Z1 (ops 1,3,4,5,6). Zero
OK-withheld; F-D does not fire. The verifying operators
are never skipped: op2's (2,3,6) cell carries SUC=8 from
QD2 so it is tried (and correctly fails) on Z1 in QD3;
op4's (4,4,6) cell is fresh per (src,sig) so it fires on
Z2 in QD3.

**KB-PROB (probation recovery): PASS.**
(a) PROB-UNG: PQ1..PQ7 val=-2, PQR op=2 val=62 (solver exists).
(b) PROB: PQ1..PQ7 val=-2, PQR op=2 val=62.
(c) PROB PQR trace: MR-OP-PROBATION 1 (fail),
MR-OP-PROBATION 2 -> ANS term=24 val=62 -> MR-OP-OK 2.
PQ1 update shows (op,0,20)=(0,4,1); PQ2..PQ7 all skipped
(QTOUCH 2..7); PQR hits QTOUCH=8 -> probation -> verify
-> commit. The retired operator recovers exactly when the
world changes, on the unchanged mechanism.

**KB-SEAL: PASS.** driver_H2.zag: zero trace tags, zero
operator/form names, zero standing offsets (shell grep, 0
hits on all patterns).

**KB-DET: PASS.** 3/3 byte-identical runs (sha256
909a58f16407bc88aa526376a1caf963a6d7210eaf5f312fd666c89eabbdd3d7).

## 3. Informational: GLOBAL arm (mode 2)

Predicted qualitative outcome confirmed: QD2 reroutes via
op6 on Z1 (op=6, val=67, tries=2: global cells do not
distinguish sources, so op2 is globally struck but op6's
global SUC lets it fire, the same [6,6,4]-style reroute the
ABLATE-SUB arm found); QD3 then fails (val=-2, op=-1,
tries=3): op4 is globally retired after the QD1/QD2
failures and the INVERT link never fires, so the chain
breaks at QD3; QD4 val=-2 (tries=1, one probation try).
The context-vs-global conclusion transfers to [6,2,4]:
per-operator global retirement breaks the chain even
though the mechanism routed around the QD2 retirement via
op6, while per-(op,src,sig) standing preserves it. The
(src,sig) key is load-bearing on this triple too.

## 4. Falsifiers

F-D (wrong skip): not fired. F-EFF: not fired. F-CORR:
not fired. F-PROB: not fired. F-SEAL: not fired. F-DET:
not fired.

## 5. Interpretation: answers to the task's questions

**Does the standing mechanism generalize beyond [6,5,4]?
Yes.** 54 -> 33 tries (39% fewer, cf. 57 -> 33 / 42% on
[6,5,4]) with zero solution changes, zero wrong skips,
and probation recovery, on the byte-identical frozen
mechanism. No [6,2,4]-specific adjustment was needed.

**Is the per-(op,src,sig) key sufficient for [6,2,4]'s
different discriminator pattern? Yes.** Two pieces of
evidence. First, SUBSTITUTE's de-mismatch lifecycle is
handled by src separation: op2's QD2-phase-1 failure on
taught (2,1,4), its QD2-phase-2 success on Z1 (2,3,6),
and its QD3-phase-2 failure on Z1 are recorded in
distinct cells, so QD3 tries op2 on Z1 (SUC=8, not
struck) and correctly fails it, with no wrong skip and
no wrong commit. Second, the load-bearing moment the
prereg identified: in QD3, phase 2 visits Z1 then Z2
under the SAME signature (sig=6). op4 fails on Z1,
striking (4,3,6) via the post-source update; (4,4,6)
stays fresh, so op4 fires on Z2. Under a per-(op,sig)
key the Z1 failure would have struck the shared cell
and broken the chain. The src in the key carries the
[6,2,4] chain exactly where the design said it must.

**Does [6,2,4] need a different standing design? No.**
The frozen mechanism sufficed with zero source changes;
the hand-derived trace predicted every observed number.

## 6. Disclosures and non-claims

- L2 evidence only (standing records reused across
  queries by fixed researcher-supplied gate/update
  formulas), not L3.
- One [6,2,4] chain on one fresh family does not
  establish general standing composability; 4+ chains,
  the protected core, the continuing learner, scaling,
  and transfer are out of scope.
- The GLOBAL arm is informational, not a kill bar.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 semantic cases, 0 learner source
  changes. Pure Zag, safebin toolchain, zero forbidden
  executables (Step 0 verified at startup; `which
  python3` empty under safebin PATH).
- No em/en dashes in loop documentation. Commits
  local with explicit pathspecs; nothing pushed. The
  compose, chain3b, ess_compose, and builder lane
  directories were never modified.

## 7. Branch note

The shared main worktree (~/workspace/tnn-rsi) is
checked out on side branch lane-ma4b-20261003, not
tnn-native-lab. This worker operated in its own worktree
(~/workspace/lane-l2esscompose2-20261003, branch
lane-l2esscompose2-20261003, based on tnn-native-lab) and
landed commits on tnn-native-lab via git plumbing
(write-tree + commit-tree -p HEAD + update-ref with
old-value check), per the shared-workspace git
discipline. Documented per the task's branch-issue
instruction (also in NAMECHECK.md).

## 8. Files

- learner.zag (byte-identical to l2_ess_compose's),
  world_H.zag (byte-identical to l2_compose_chain3b's),
  driver_H2.zag (new; 5 arms; KB-SEAL clean)
- full.zag, h2_bin, h2_compile.txt,
  run1/2/3.txt (3/3 byte-identical)
- PREREG.md (frozen alone at bf7e8c2c6), NAMECHECK.md
  (Step 0), REPORT.md (this file)

Commits: freeze bf7e8c2c6 (PREREG+NAMECHECK alone);
implementation + this report follow under explicit
pathspecs on tnn-native-lab, never pushed.
