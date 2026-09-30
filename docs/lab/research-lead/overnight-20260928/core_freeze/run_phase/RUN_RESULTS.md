# CORE FREEZE CHALLENGE: Stage 2 Run Results

Date: 2026-09-30. Worker: Core Freeze Challenge Run-Phase Worker.
Status: FREEZE-RUN-COMPLETE.
Protocol: FREEZE_PROTOCOL.md (frozen 66e3c3f38). Freeze: 87ac95d08.

## Step 0 Name-Check

See NAMECHECK.md in this directory. The four standing-rules sections from
LOOP_STATE.md were identified before any run work began. Pure Zag/shell only;
no Python; shell-only dash checks; owned paths with explicit pathspecs;
frozen source/binary never modified; contaminated paper untouched.

## K1: Hash verifications

### Binary hash (8733af3d28148263f9ce41d979043379b9e6d637f09dcab42eff2374f3a59960)

Verified before every world via run_world.sh (exits 10/VOID on mismatch).
All nine worlds ran; no VOID triggered. Re-verified after the full battery:
MATCH.

### Source hash (b761efd90cb1b8f9fa31f319dfde8e98c52e3f4eacf5e826817adcf10d206249)

Re-verified after the full battery: MATCH. The frozen source was not modified.

### World file seals (all 15 verified before running)

Pre-freeze (design e806d634e):
- W1_world.txt: 9c8cdf421bb73bf58ec41a19cd9cf68e43d99d0e09851e0cebc201ddd4538325 MATCH
- W2_world.txt: 33958a4d0e01e7f9d02a9f1d5744247a0c7bdc82754a055191695f23699d7635 MATCH
- W3_world.txt: 01b4ee0d8095a073eb50113934b6ee377504c03d013280b470163ca73be9a662 MATCH
- W4_world.txt: 5d9bf895e8f5de74ef595441923c22f9f9daf0c9018ddb2a7a9605d05cdc7cb3 MATCH
- W5_world.txt: f926ec7bd6ee3d186cc00ef24a3653d5b3de2ad4b1bebeaeb7f8f6019e0e13e9 MATCH
- W7_world.txt: 27986463dcf9c26dd46f643b11e42c5b0af7ca618e2d8b9d34d244e9589aede8 MATCH
- W8_world.txt: 277320bec4c3150434d40d1e74c6b3049880a00b96cab9b52d882ffc04791deb MATCH

Adversary (design 6d185ebce):
- w6_phaseA.txt: 9c952dd06e7683f13d5cdb0d2659655bdaad315739bdb9af1b29559899446ef4 MATCH
- w6_phaseB.txt: 24f011f798817dfdfcb837b70ae8709a79af730d18c31eebd0167e316c715cb9 MATCH
- w6_controlA.txt: 4829f3e0636440fcc990be8ecab1ccee9e7df04a2a68daca951e9c2f333a3906 MATCH
- w6_controlB.txt: 011dc7e2698d069ea7004bc9f3f609c572095f21b9dc6dc77450b795ef5c7188 MATCH
- w6b_phaseA.txt: d09d81baaca118a4b8309ffbbbf441267d2a8161d23678ed5059a8bc0a4da905 MATCH
- w6b_phaseB.txt: 1221425f2bef89c01f9a2736906d154357cc510fad3da6e9822a5cb43bd8eaca MATCH
- w9_treeA.txt: 43351a79516062d2a17316cee5a37da44d4196b43859de9d7f377bea34c20779 MATCH
- w9_treeB.txt: 036ba3b0cce216895ac637fa352660ffbeb2215381ea5f2ad0c2ceb0827861fd MATCH

No SEAL-BROKEN. Battery proceeded.

### A5 source audit

Grep of frozen source for world id ranges. All adversary ids (20001-20115,
21001-21009, 22001-23004, 22101, 23101-23102) absent. All pre-freeze
distinctive ids (7001-7011, 8001-8005, 9001-9020, 9601-9606, 9700-9704,
9901-9910) absent. One numeric collision: integer 900 appears in source at
stage0/world_learn.zag lines 1082-1101 as a SUBJECT in the uncalled legacy
legacy_p1_p11() function (learn(W,900,1,2)). W1 uses 900 as a RELATION for
junk triples. Different argument position, different semantics, dead code
never executed by the world driver. Cleared: not smuggling.

### A6 disjointness

Verified: all distinctive subject/relation id blocks are disjoint across
worlds except intentional reuse (W5 targets W1/W4 beliefs by design; W9
tree B includes 5 tree-A retention probes by design). Small integers used
as object values overlap but are not vocabulary.

## K2: World execution

All nine worlds executed in protocol order W1-W9 with persistent state
carried across (S0 null -> S1 -> S2 -> S3 -> S4 -> S5 -> S5a -> S6 -> S7 ->
S8 -> S8a -> S9). Each world was one process invocation per file via the
frozen save/load mechanism. State snapshots saved before/after each world.

### V0 validity gate: PASS

Standalone probe QUERY 22001 22101 7 on untaught triple returned
ANSWER 22001 22101 -2 (sentinel, not echo). W6 and W9 are valid worlds,
not INVALID. The control arm's first vault probe confirmed the same.

### C1 conditional-validity: CONFOUNDED for W6-treatment and W9

White-box state inspection shows the eviction pathology (see below)
destroyed the triples the bars depend on:
- W6 reveal triple (22001,22101,7): taught in phase B, immediately evicted
  (EVICT 22001 22101 in phase B output). Only 1/5 treatment probes correct.
- W9 edge triples: 1 of 28 survived in S9 (only the last-taught edge
  (20115,21001)). The 27 others were evicted.
Per C1, W6-treatment and W9 outcomes are CONFOUNDED by capacity/state
management, not clean measures of inquiry or representation.

## Per-world results

| World | Predicted | Observed | Verdict | Confirms/Revises |
| W1 new concepts | PASS 10/12, ret 10/10 | 10/12, ret 10/10 | WORLD-PASS | CONFIRMS. The 2 two-hop probes returned -2 as predicted, documenting the composition boundary inside a passing world. |
| W2 new procedures | FAIL 0/8 | 0/8 (all -2) | WORLD-FAIL | CONFIRMS. No procedure abstraction; novel-instance keys never observed. |
| W3 causal laws | FAIL 0/10 | 0/10 (all -2) | WORLD-FAIL | CONFIRMS. No hypothesis construction; held-out sums unobserved. |
| W4 law change/revert | PASS 6/6,6/6,6/6 | 1/6 pre, 2/6 post, 3/6 revert | WORLD-FAIL | REVISES. The prediction assumed 6 teaches would occupy 6 slots. The eviction tie-breaker (lowest index) caused sequential teaches to overwrite the same slot. The world did not test reversion; it tested the eviction pathology. |
| W5 contradictions | PASS 2/2, 6/6 | 1/2 targeted, 4/6 collateral | WORLD-FAIL | REVISES (cascade). W4's keys never stabilized, so W5's contradiction targets were absent. The 1/2 and 4/6 reflect eviction noise, not belief revision. |
| W6 active inquiry | FAIL (B4 attribution) | Treatment 1/5 (0/3 vault); Control 0/5 | WORLD-FAIL* | CONFIRMS the adversary's structural argument and ADDS the C1 confound. *See B4 dual reading below. |
| W7 planning | FAIL 0/4 | 0/4 (all CHOICE 0) | WORLD-FAIL | CONFIRMS. No action-selection machinery; goal unreachable under all-zero acts per the frozen grader. |
| W8 synth language | FAIL 0/5 novel, 4/4 recall | 0/9 (0/5 novel, 0/4 recall) | WORLD-FAIL | CONFIRMS FAIL but REVISES the recall prediction: the 4 recall probes failed because training triples were evicted, not because storage works. |
| W9 new representation | FAIL 0/28, 0/26 | 0/28 tree A, 0/31 tree B | WORLD-FAIL | CONFIRMS. No traversal machinery; all probes -2. C1 CONFOUNDED (27/28 edges evicted), so the white-box B3 test was not clean. |

Challenge-level: FREEZE-CHALLENGE-COMPLETE (all nine worlds executed,
source delta zero throughout, measurements delivered, boundary analysis
below). Learner profile: 1/9 WORLD-PASS (W1 only).

## The eviction-pathology finding

The battery's most important discovery is not in the predicted
pass/fail table. It is a state-management flaw in the frozen substrate
that the world designers did not anticipate.

Mechanism: learn() on a full store calls evict_c(), which returns the
lowest-importance valid slot with ties broken by lowest index. A newly
taught slot has importance 1 (correct=0, wrong=0, dependents=0,
contradictions=0). When the store is full of importance-1 slots, the
tie-breaker picks the lowest-index slot. The new fact is written there.
On the NEXT teach, evict_c scans again from index 0; the just-written
slot (still importance 1, at the low index) is picked again. The
sequential teaches overwrite the same slot instead of spreading across
available low-importance slots.

Observed signature (in binary stdout):
```
OBSERVED 9601 610 10
EVICT 9601 610        <- the just-taught key, evicted by the next learn()
OBSERVED 9602 610 20
```

Impact:
- W4: 6 sequential teaches collapsed to 1-2 surviving keys. The
  reversion bars could not be tested.
- W5: contradiction targets were absent; collateral keys were evicted.
- W6: the reveal triple was evicted; context triples were evicted.
- W8: training utterances were evicted; recall failed.
- W9: 27 of 28 edge triples were evicted.
- W1 survived only because its 10 probed keys were taught early (before
  the store filled) and earned importance 11 via probes.

This is a property of the frozen binary, not a world-design error. It
revises the W4/W5 predictions (which assumed stable multi-slot
occupancy) and confounds W6/W9 per C1. It also sets a ceiling on the
continuing-learner program: a substrate that cannot stably hold 6 new
facts in sequence cannot accumulate experience across worlds.

## W6 B4 dual reading (protocol-interpretation call for the research director)

The adversary's design documents two readings. Both are recorded here
without deciding between them.

Adversary FAIL reading: B4 requires the inquiry strategy to be
learner-determined. The binary's only action signal is the constant
CHOICE 0, emitted wherever the world file places an ACT line. The decoy
ACT in phase A fires before any uncertainty signal could exist in that
run; the post-diagnostic ACT fires identically. The "inquiry action" is
a function of file position, not epistemic state. A one-element constant
action set cannot encode selection among inquiries. The reveal was keyed
on output, but the output was keyed on author-placed signals. This is the
measured form of protocol prediction 8.4. Verdict: WORLD-FAIL on B4
attribution, by design. The world exposes the false positive.

Literalist PASS reading: B1-B3 are the numeric bars. B1 (treatment 80%)
was not met here due to the C1 eviction confound, but in a counterfactual
with stable storage the treatment would score 3/3 (direct recall of the
revealed triple) while the control scores 0/3. B4's "learner-determined"
is satisfied in the thin sense: the fixed default CHOICE 0 does not
branch on world identity (no source logic conditions on W6). The
responder contract is world-side logic, not a learner handler. On this
reading the numbers pass and the attribution criterion is met
vacuously. Verdict: WORLD-PASS (or CONFOUNDED, given the eviction).

The false-positive analysis: scoring the literalist reading as a pass
would credit compliant plumbing (emit constant, store revealed triple)
as active inquiry. The treatment's success would measure the responder's
generosity, never the learner's inquiry, because no binary through this
interface can make its action contingent on its uncertainty (the only
learner-to-world channels are the constant CHOICE and reactive ANSWERs).

This is a protocol-interpretation call. The runner does not decide it.
Flagged for the research director.

## Measurements (protocol section 6)

CAPABILITY SOURCE DELTA: zero at every check (binary and source hashes
recomputed before each world and after the battery; all MATCH). The
challenge is not void.

LEARNER STATE DELTA (bytes changed, via cmp -l):
- S0->S1 (W1): 430 bytes. 36/36 slots valid; tick 64.
- S1->S2 (W2): 7 bytes. (W2's 15 teaches churned the same low-index slot.)
- S2->S3 (W3): 9 bytes. (W3's 44 teaches churned similarly.)
- S3->S4 (W4): 36 bytes.
- S4->S5 (W5): 36 bytes.
- S5->S5a (W6 phase A): 41 bytes.
- S5a->S6 (W6 phase B): 6 bytes.
- S6->S7 (W7): 9 bytes.
- S7->S8 (W8): 11 bytes.
- S8->S8a (W9 tree A): 14 bytes.
- S8a->S9 (W9 tree B): 12 bytes.
The small deltas after W1 reflect the eviction pathology: new teaches
overwrite one slot rather than occupying new ones. Cumulative state
utilization: 36/36 fact slots valid throughout (after W1); the DDES
ledger slice W[16384..32768) was never written (as declared).

TRANSFER: W9 tree B is the transfer variant (fresh ids 20101-20115, same
structural family as tree A). Transfer gap is vacuous: both scored 0.
No other world shipped a held-out surface variant.

RETENTION: cross-world retention was destroyed by the eviction
pathology, not by interference between learnable content. W1's 10
importance-11 keys survived the full battery (spot-checked: 7001/501 and
101/201 still answer correctly in S9). All later worlds' keys were
churned. The INTERFERENCE measurement is therefore dominated by the
eviction policy, not by representational interference.

COMPUTE (wall-clock per world, informational):
- W1: 58 ms, 64 events. W2: ~50 ms, 23 events. W3: ~50 ms, 54 events.
- W4: ~80 ms, 36 events. W5: ~60 ms, 10 events. W6: phase A ~30 ms,
  phase B ~40 ms, control ~70 ms total. W7: ~40 ms, 42 events.
- W8: ~60 ms, 44 events. W9: tree A ~100 ms, tree B ~120 ms.

## Scoring (protocol section 9, per world)

- W1: GENERALITY 0 (no transfer variant; composition probes failed).
  ARCHITECTURAL COMPRESSION 1 (existing regions reused, no new formats).
  LEARNER AUTHORITY 1 (learner-created persistent state owns the
  semantics for the 10 recalled keys). CAPABILITY SOURCE DELTA 2 (zero).
- W2: GENERALITY 0. COMPRESSION 1. AUTHORITY 0 (no persistent new
  semantics; behavior is lookup failure). DELTA 2.
- W3: GENERALITY 0. COMPRESSION 1. AUTHORITY 0. DELTA 2.
- W4: GENERALITY 0. COMPRESSION 1. AUTHORITY 0 (no stable revision;
  the versioning machinery was not exercised). DELTA 2.
- W5: GENERALITY 0. COMPRESSION 1. AUTHORITY 0. DELTA 2.
- W6: GENERALITY 0. COMPRESSION 1. AUTHORITY 0 (adversary reading) or 1
  (literalist reading, thin). DELTA 2.
- W7: GENERALITY 0. COMPRESSION 1. AUTHORITY 0. DELTA 2.
- W8: GENERALITY 0. COMPRESSION 1. AUTHORITY 0. DELTA 2.
- W9: GENERALITY 0. COMPRESSION 1. AUTHORITY 0. DELTA 2.

## K3: Process

Pure markdown and POSIX shell. No Python invoked at any point. Dash
check via worker_snippets/check_no_dash.sh (run before commit).
Contaminated paper
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
untouched (verified zero diff). Frozen source and binary unmodified
(hashes re-verified after battery). Commits local, owned paths only,
explicit pathspecs.

## Boundary analysis (protocol section 8)

Predicted failures and what actually happened:
1. Stage 0 freezability: passed (READINESS-PASS); the interface is
   plumbing, confirmed by the run (no cognitive handlers fired).
2. W9 fragmented state (predicted FAIL): confirmed 0/28, 0/31, but
   CONFOUNDED by eviction per C1. The representation boundary was not
   cleanly measured.
3. W3 researcher menus (predicted FAIL): confirmed 0/10. The
   construction-vs-selection boundary stands.
4. W6 fixed intervention grammar (predicted FAIL or degenerate):
   confirmed degenerate; the B4 dual reading is the honest output.
5. W8 no linguistic substrate (predicted FAIL): confirmed 0/9. The
   recall sub-prediction (4/4) was wrong due to eviction.
6. W7 no planner (predicted FAIL): confirmed 0/4.

Unpredicted finding: the eviction tie-breaker pathology. This was not
in the protocol's predicted failure list. It dominates W4, W5, W6, W8,
and W9, and it revises the W4/W5 predictions. It is the strongest
remaining reason the substrate cannot serve as a continuing learner:
not a missing cognitive capability, but a state-management flaw that
prevents stable accumulation of experience.

If the candidate had passed W2, W3, W7, or W8, the corresponding
mechanism claim would have been revised. It passed none of them. The
one passing world (W1) passed on faithful exact-key memory, with the
composition boundary documented inside the pass.

## Artifacts in this directory

- NAMECHECK.md (Step 0)
- RUN_RESULTS.md (this file)
- run_world.sh, score_probes.sh (harness; shell only)
- battery/ (world outputs W1.out..W9treeB.out, state snapshots
  state_S0.bin..state_S9.bin, scores)
