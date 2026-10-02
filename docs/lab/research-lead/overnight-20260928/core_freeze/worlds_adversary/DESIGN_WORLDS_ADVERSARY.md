# POST-FREEZE ADVERSARY WORLD DESIGN: W6 (active inquiry) and W9 (new representational structure)

Date: 2026-09-30. Adversary slot per FREEZE_PROTOCOL.md section 5.
Freeze: 87ac95d08 (source b761efd90cb1, binary 8733af3d2814).
Protocol: 66e3c3f38. Interface: stage0/INTERFACE.md. Regions: stage0/REGIONS.md.

Status: DESIGN ONLY. Sealed. Content revealed at run time. The worlds were
never executed against the frozen binary in this task.

## 1. Interface facts relied upon

From INTERFACE.md and REGIONS.md (interface-level evidence only; the
candidate's source was not read):

- Events are OBSERVE s r o (calls learn, emits OBSERVED), QUERY s r e
  (calls query, emits ANSWER s r v), ACT (emits CHOICE 0, fixed default).
- QUERY on an untaught (s, r) yields the not-found sentinel -2, unchanged
  by the interface ("that is existing cognitive semantics").
- The binary takes <world.txt> <state.bin>; the full 32768-byte W is
  written back after a successful stream, so state carries across separate
  invocations. Parse buffers never reach the state file.
- Fact store: 36 slots of 44 bytes at W[64..1648). DDES ledger slice
  W[16384..32768) is never written by the generic world driver.
- The output format is fixed; the only learner-to-world signals are the
  constant CHOICE 0 and reactive ANSWER values. No other byte crosses a
  process boundary.

## 2. Explicit assumptions and validity gates

- A1: On an untaught (s, r), QUERY returns -2 regardless of e (INTERFACE.md
  wording plus the ANSWER 2 10 -2 smoke case).
- A2: OBSERVE-taught triples persist across invocations via the state file
  (Stage 0 smoke tests).
- A3 (runner requirement R1): the challenge runner supports conditional
  phase release for W6: it reads the binary's stdout from one phase file
  and selects the next phase file by the responder contract in section 3.
  This is world-side logic, not interface machinery. Without R1, W6 cannot
  be run as designed.
- A4: Fact-store capacity suffices: W6 holds at most 8 live triples;
  W9 holds at most 28 (14 edges per tree, two trees). 36 slots total.
- A5: All ids below are fresh. The runner greps the frozen source for
  every id range; any match makes the world WORLD-INVALID per the
  protocol's anti-smuggling provisions (the world's fault, replaced per
  section 5).
- A6: Id ranges used here (20001-20115, 21001-21009, 22001-22003,
  22101, 23001-23004, 23101-23102) must be disjoint from every other
  world's ranges. The runner verifies disjointness before the battery.

Validity gate V0 (pre-registered): if on any untaught triple the binary's
ANSWER equals e (echo/default behavior) rather than -2, assumption A1 is
violated and W6 and W9 are ruled WORLD-INVALID, not failed. The
discriminating check is the control arm's first vault probe (QUERY
22001 22101 7 on an untaught triple): ANSWER 7 means echo (INVALID);
ANSWER -2 means the sentinel (proceed).

Conditional-validity clause C1: W6's treatment arm and W9's probe phases
are valid inquiry/representation measures only if the taught triples they
depend on are retained in the fact store at query time. The battery runs
W1-W9 sequentially with carried state; if W1-W5 pressure evicts the
reveal triple (W6) or edge triples (W9), the outcome is confounded by
capacity, not by inquiry or representation. The runner must verify
retention white-box (state-delta inspection) before scoring; on eviction
the world is reported CONFOUNDED, not failed.

## 3. W6: active inquiry

### 3.1 Functional spec (protocol)

The world withholds information provably unobtainable by passive
observation; only the learner's own actions can reveal it. A passive
control (same world, actions disabled) is run for comparison. Frozen bars:
information-seeking actions that measurably reduce uncertainty, not random
action; task success at least 80 percent while the passive control scores
at most chance plus 10 percentage points. Anti-smuggling: the generic
action set only; the inquiry strategy is learner-determined.

### 3.2 Construction

Hidden variable: the vault code, (22001, 22101). True value 7, drawn from
{1..20} (chance 5 percent; control bar: at most 15 percent).

Treatment arm:
- w6_phaseA.txt (7 lines): context OBSERVEs, a decoy ACT placed BEFORE
  the diagnostic query, the diagnostic QUERY 22001 22101 -2 (expected -2:
  the learner should admit ignorance), one more OBSERVE, and the inquiry
  ACT placed AFTER the diagnostic.
- Responder contract (world-side): parse the Phase A stdout in order. Let
  D be the ANSWER line for (22001, 22101). Release w6_phaseB.txt iff D is
  exactly "ANSWER 22001 22101 -2" AND a "CHOICE 0" line occurs after D in
  output order. Otherwise release w6_controlB.txt (no reveal).
- w6_phaseB.txt (7 lines): OBSERVE 22001 22101 7 (the reveal), one
  distractor OBSERVE, three task probes QUERY 22001 22101 7, two retention
  probes.

Control arm (passive, actions disabled):
- w6_controlA.txt: identical to Phase A with both ACT lines removed.
- The responder finds no CHOICE line and releases w6_controlB.txt: the
  same five probes with no reveal OBSERVE.

Diagnostic annex W6b (misinformation variant, clearly marked as the
adversary's own probe, outside the protocol's literal bars):
- w6b_phaseA.txt: as Phase A, plus OBSERVE 22001 22101 13 (wrong code)
  before the diagnostic. The diagnostic therefore yields "ANSWER
  22001 22101 13", not -2. The responder withholds the reveal and
  releases w6b_phaseB.txt (task probes only, expected 7).

### 3.3 Frozen bars for this world

- B1: treatment task probes at least 80 percent (3 probes; bar 3/3).
- B2: control task probes at most 15 percent (3 probes; chance 5 percent).
- B3: the actions measurably reduce uncertainty and are not random.
- B4 (anti-smuggling): the inquiry strategy is learner-determined; no
  source logic branches on world identity.

### 3.4 Predictions

- Treatment: 3/3 task probes (the reveal triple is directly stored and
  recalled), 2/2 retention. B1 met, B2 met (control 0/3: all -2).
- W6b: 0/2 task probes (answers 13, confabulating from misinformation).
- B4: FAIL. Predicted verdict: WORLD-FAIL (degenerate). B1-B3 are met on
  the numbers; the world fails on attribution, by design.

### 3.5 Mechanism-level argument (why the failure is structural)

1. Learner-to-world channels under the frozen interface are exactly two:
   (i) CHOICE 0, a constant emitted wherever the world file places an ACT
   line; (ii) ANSWER values, reactive responses to world-posed queries
   (section 1). No other byte crosses a process boundary.
2. The treatment file places a decoy ACT before the diagnostic query. The
   binary will emit CHOICE 0 for the decoy identically to the
   post-diagnostic ACT: the action fires before any uncertainty signal
   could exist in that run. This is observed data, not a hypothesis. The
   binary's "inquiry action" is therefore not a function of its epistemic
   state but of file position.
3. Hence the reveal, though keyed on output, is keyed on a signal the
   world file's author placed. A one-element constant action set cannot
   encode selection among inquiries, and a static stream cannot carry
   uncertainty-contingent action. No binary through this interface can
   satisfy B4 in the Level-D sense ("learner must act to obtain missing
   information" where the act is the learner's own). Any W6 world under
   this interface is degenerate: it measures at most the responder's
   generosity, never the learner's inquiry.
4. The one genuinely learner-contingent gate is the -2 versus
   confabulation distinction measured by W6b: whether the reveal fires
   depends on the learner's stored state (ignorant versus misinformed).
   That measures calibration, not active inquiry, and it is the only
   part of this world attributable to the learner rather than the file
   author.
5. The literalist counter-reading (WORLD-PASS: B1-B3 met, the fixed
   default is "the learner's strategy" and does not branch on world
   identity) is documented here as the exact false positive this world
   is built to expose. Scoring that reading as a pass would credit
   compliant plumbing as inquiry. The adversary recommends the B4 FAIL
   reading. This is the measured form of protocol prediction 8.4 ("W6
   predicted FAIL or degenerate").

### 3.6 W6 certification

Expressible through the frozen interface: yes, all files use only
OBSERVE/QUERY/ACT with integer ids. Solvable without source changes: the
treatment arm is solvable by the frozen binary as built (predicted 3/3);
the predicted WORLD-FAIL rests on the anti-smuggling attribution
criterion, which is the boundary measurement the protocol calls for, not
an interface violation. Designed without knowledge of candidate internals:
no candidate source was read; every mechanism claim rests on INTERFACE.md,
REGIONS.md, and FREEZE_RECORD.md. No contact with candidate builders.

## 4. W9: new representational structure

### 4.1 Functional spec (protocol)

The world's regularities require a structural form the learner's current
state formats cannot natively express. Frozen bars: the learner solves
the task at 80 percent or better AND white-box evidence shows a genuinely
new structural topology in persistent learner state (not a shoehorn into
existing slots, shown by structural inspection of the state delta); the
new form is reused on a second probe. Anti-smuggling: the topology is not
pre-allocated in source and no dedicated semantic case exists.

### 4.2 Construction

Two rooted trees are taught as flat parent edges (child 21001 parent).
Probes ask for functional properties that require traversal: depth
(21007, single-valued per node) and grandparent (21009, single-valued
per node). Neither property is taught; neither is one lookup away from
the taught triples. Ids are fresh per A5.

Tree A (w9_treeA.txt, 42 lines): 15 nodes (20001-20015), 14 edges, max
depth 6. Probes: 15 depth, 13 grandparent (28 total).
Tree B (w9_treeB.txt, 45 lines): 15 nodes (20101-20115), 14 edges, a
different branching shape, max depth 4. Probes: 15 depth, 11 grandparent,
plus 5 retention re-queries of tree A (31 total).

Tree shapes (edges child -> parent):
- A: 20002->20001; 20003,20007,20008->20002; 20004,20009,20010->20003;
  20005,20011,20012->20004; 20006,20013,20014->20005; 20015->20006.
- B: 20102,20103,20104->20101; 20105,20106->20102; 20107->20103;
  20108,20109->20104; 20110->20105; 20111,20112->20107; 20113->20109;
  20114->20110; 20115->20113.

Tree B is the transfer variant (new surface symbols, same structural
family) and simultaneously the cognitive-reuse probe: a genuine traversal
structure must apply to new ids without re-derivation from scratch.

### 4.3 Frozen bars for this world

- B1: at least 80 percent on tree A probes (28 probes; bar 23).
- B2: at least 80 percent on tree B probes (26 probes; bar 21).
- B3: white-box: a genuinely new structural topology in persistent W,
  shown by state-delta inspection to be non-triple structure (not flat
  edge echoes).
- B4: reuse: tree B solved via the structure built for tree A, not by
  independent memorization (transfer gap reported; memorized pairs would
  not transfer to fresh ids).
- B5: retention: at least 4 of 5 tree-A re-queries correct after tree B.

### 4.4 Predictions

- Tree A: 0/28 (every probe untaught; predicted ANSWER -2 throughout).
- Tree B: 0/26. Retention: 0/5. B1, B2, B5 missed.
- B3: no new topology in the state delta; at most flat echoes of the 14
  taught edges per tree. B4 vacuous.
- Predicted verdict: WORLD-FAIL on accuracy and on white-box.

### 4.5 Mechanism-level argument (three branches, driver-agnostic)

The argument does not depend on the query driver's internals, which the
adversary has not seen.

1. Branch 1, fixed lookup: depth and grandparent are never observed, so
   every probe misses and returns -2. Accuracy FAIL (predicted).
2. Branch 2, fixed chaining to a source-fixed depth k: probes beyond k
   fail; and even full accuracy would fail B3, because a source-fixed
   chaining bound is source logic, not learner-created topology.
3. Branch 3, shoehorning by precomputation: deriving all depth and
   grandparent facts would need 28 extra triples per tree against 36
   total slots shared with the 14 taught edges and all earlier worlds;
   and precomputed pairs cannot transfer to tree B's fresh ids without
   the general procedure the world demands (B4 kills the shoehorn even
   if capacity allowed).
4. Therefore passing requires a learner-constructed traversal or
   compression structure in persistent W plus reuse on tree B: exactly
   the C0-B/C0-D target. The frozen candidate owns three researcher-fixed
   encodings (44-byte fact slots; the DDES ledger slice the generic
   driver never writes; rule-store keys). There is no generic structural
   substrate, only slots to fill. This is the measured form of protocol
   prediction 8.2 ("W9 predicted FAIL").

### 4.6 Positive criterion (what would count as genuine)

A WORLD-PASS would require: B1 and B2 met; the state delta showing a
non-triple topology (for example a parent-pointer array, a traversal
trace, or a compressed encoding plus a decode procedure) created after
the tree-A exposure; tree B solved through that structure (B4); and B5
met. Anything less, including high accuracy with only flat edge echoes
in the delta, is a shoehorn and fails B3.

### 4.7 W9 certification

Expressible through the frozen interface: yes, pure OBSERVE/QUERY
triples. Solvable without source changes: a learner with a general
structural workspace could construct the traversal in the 32768-byte W
without any source change; the predicted WORLD-FAIL is the boundary
measurement the protocol calls for (section 8.2), not an interface
violation. Designed without knowledge of candidate internals: the
three-branch argument is deliberately driver-agnostic. No contact with
candidate builders.

## 5. Sealed hashes (sha256, committed after freeze 87ac95d08)

- w6_phaseA.txt: 9c952dd06e7683f13d5cdb0d2659655bdaad315739bdb9af1b29559899446ef4
- w6_phaseB.txt: 24f011f798817dfdfcb837b70ae8709a79af730d18c31eebd0167e316c715cb9
- w6_controlA.txt: 4829f3e0636440fcc990be8ecab1ccee9e7df04a2a68daca951e9c2f333a3906
- w6_controlB.txt: 011dc7e2698d069ea7004bc9f3f609c572095f21b9dc6dc77450b795ef5c7188
- w6b_phaseA.txt: d09d81baaca118a4b8309ffbbbf441267d2a8161d23678ed5059a8bc0a4da905
- w6b_phaseB.txt: 1221425f2bef89c01f9a2736906d154357cc510fad3da6e9822a5cb43bd8eaca
- w9_treeA.txt: 43351a79516062d2a17316cee5a37da44d4196b43859de9d7f377bea34c20779
- w9_treeB.txt: 036ba3b0cce216895ac637fa352660ffbeb2215381ea5f2ad0c2ceb0827861fd

Line counts: w6_phaseA 7, w6_phaseB 7, w6_controlA 5, w6_controlB 5,
w6b_phaseA 7, w6b_phaseB 3, w9_treeA 42, w9_treeB 45.

## 6. Kill-bar self-check

- K1: both worlds specified as sealed event streams with protocol success
  criteria. PASS: W6 has B1-B4 with the responder contract and the
  passive control; W9 has B1-B5 with the transfer/reuse and white-box
  criteria.
- K2: each world carries a mechanism-level argument for why the frozen
  binary should fail. PASS: W6 section 3.5 (interface cannot carry
  Level-D inquiry; the decoy-ACT non-contingency proof; predicted
  WORLD-FAIL on B4 attribution). W9 section 4.5 (driver-agnostic three
  branches; predicted WORLD-FAIL on accuracy and white-box).
- K3: pure text/markdown, dash-clean, contaminated paper untouched,
  worlds never executed against the binary. PASS (verified at commit
  time; the worlds were authored by hand, never run).

## 7. What this design does not decide

- Whether runner requirement R1 (conditional phase release) is
  implementable in Stage 3; if not, W6 must be redesigned or dropped,
  not fudged.
- Whether the literalist or the adversary reading of W6's B4 governs;
  that is a protocol-interpretation call for the research director.
  Both readings are recorded above with the false-positive analysis.
- The numeric fate of the conditional-validity clause C1; the runner
  reports retention white-box before scoring.
- Anything about W1-W5, W7, W8, which belong to the pre-freeze team.
