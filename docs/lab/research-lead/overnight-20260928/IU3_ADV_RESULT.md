# IU3-ADV RESULT: H-INTENT-UNIFIED3 Red Team

## Verdict: H-INTENT-UNIFIED3 DOWNGRADED (not killed)

Two attacks succeeded. No frozen kill bar (K-IU3-1 through K-IU3-5)
was broken, so this is a downgrade, not a kill. The downgrade narrows
two repair claims:

1. "X-IU2-1 CLOSED" is now "closed only for collisions where both
   records are within the 16-input cap". The verbatim-conflict guard
   is blind to genuine training-data contradictions whenever the
   colliding input falls outside the record cap on one side
   (X-IU3-1a').
2. "bridge_learn crash fixed" is now "the reported 18-pair
   split-index crash is fixed; the split search retains a second
   fixed-size buffer that still panics" (X-IU3-2).

X-IU3-1b (agreement control), X-IU3-3 (evidence reproduction), and
X-IU3-4 (source audit) all passed for the repair.

## Methodology

Assume the repair claim is false. Preregister attacks with explicit
kill criteria before executing. Pure Zag, pinned toolchain
znc 2026.07.0-dev (edition 2026). No Python at any stage.

- Prereg: PREREG_IU3_ADV.md (commit a88de0031), frozen before any
  attack code.
- Amendment: PREREG_IU3_ADV_AMEND1.md records the X-IU3-1a setup
  void and the X-IU3-1a' recovery fixture. The frozen X-IU3-1a is
  scored VOID (setup), not failed; the timeline is recorded
  honestly in the amendment.
- Harness: iu3_adv.zag. Mechanism is lines 1..1311 of the repaired
  unified_learn.zag, verified byte-identical by diff; only main()
  and ADV helpers are new.
- Raw evidence: IU3_ADV_RAW.txt (md5
  5c971821f636f1ea9fdfb01ff2bdb162, 3 runs byte-identical).
  Note: the file contains non-UTF8 bytes because the X-IU3-2
  fixture trains on raw byte values 128..163 and the ROUTE echo
  prints them verbatim. This is the authoritative raw output.
- Commit order: prereg, then amendment, then harness plus raw plus
  this report. Only adversary-owned files staged.

## Attack X-IU3-1a': cap-times-verbatim composition (SUCCESS, DOWNGRADE)

### Fixture

Workspace W1. Train proc D with 17 reverse pairs, the colliding
input LAST (17th, therefore unrecorded):

"abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;
 vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;
 qrs>srq;tuv>vut;xab>bax"

Train bridge B with G1's exact known-good string (all 5 pairs
recorded):

"xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"

Control workspace W1c: train ONLY the 17-pair proc string.
Query "xab" on W1 and on W1c.

### Observed behavior (3/3 runs identical)

W1 learn trace:
- "INTENT WARN: record cap 16 reached; 17 training inputs, only
  first 16 recorded; em coverage incomplete" (R2 working)
- "ULEARN: direct discovery -> proc slot 0 (intent seq recorded,
  train_len=3)"
- "bridge: learned IF input[0]==120 THEN proc1 ELSE proc2"
- "ULEARN: bridge triggered -> rule 0 (intent seq recorded,
  train_len=-1)"

W1 query "xab":
- cand kind=proc slot=0 exact_match=0 len_match=1 train_len=3
  seq=0 cond_fire=0 score=10000
- cand kind=bridge slot=0 exact_match=1 len_match=0 train_len=-1
  seq=1 cond_fire=1 score=60000
- T DECIDE tag=A1a-xab kind=1 slot=0 gap=50000 answer=[xxx]
- "INTENT VERBATIM-CONFLICT" count in output: 0

W1c control query "xab":
- T DECIDE tag=A1a-CTRL-xab kind=0 slot=0 gap=0 answer=[bax]

### Kill criterion check

kind=1 (not -2): yes. No VERBATIM-CONFLICT line: yes. Control
answers "bax": yes. Trace shows proc exact_match=0 with bridge
exact_match=1: yes. All four conditions met.

### Causal interpretation

The guard's precondition (both top-two candidates em=1) is a
property of the intent RECORD, not of the training data. The proc
genuinely learned "xab>bax" (the control proves it reverses the
colliding input), so the training data genuinely contradicts
itself on "xab". But the 17th pair was truncated from the record,
so em=0 on the proc side, the guard never fires, and the bridge's
em term (40000) plus condition heuristic (20000) silently resolve
the conflict: kind=1, answer "xxx", gap 50000, no diagnostic. This
is the exact X-IU2-1 failure mode, persisting for out-of-cap
collisions. The learn-time WARN is emitted (R2 works as
documented) but does not restore query-time protection.

The repair doc's boundary note says "Near-ties (em=1 vs em=0 with
cf/lm deciding) are unchanged". This case is not a near-tie in any
substantive sense: the evidence is verbatim in the training data
and the em=0 is purely an artifact of the record cap. The repair's
headline claim, "No heuristic term may silently resolve a
verbatim-vs-verbatim conflict", is falsified for out-of-cap
collisions. Verdict contribution: DOWNGRADE (claim narrowing).

### The voided frozen fixture (honesty record)

The frozen X-IU3-1a used colliding input "qab" with bridge string
"qab>zzz;qcd>zzz;abc>ccc;def>ccc;abcde>eeeee". That bridge string
returned rc=-1 ("ULEARN FAIL: no program and no bridge"):
its non-'q' side {abc>ccc, def>ccc, abcde>eeeee} admits no single
program, while G1's {abc>ccc, def>fff, abcde>eeeee} yields "repeat
last input char". Per the prereg's setup-void clause the fixture
was voided, diagnosed, and replaced by X-IU3-1a' (amendment
committed). The void is scored as VOID, not as a repair failure.

## Attack X-IU3-1b: agreement control (PASSED for the repair)

### Fixture

Workspace W2. Two reverse procs that agree verbatim on the query:
A = "qab>baq;xcd>dcx" (slot 0), E = "qab>baq;wxy>yxw" (slot 1).
Query "qab".

### Observed behavior

- Both candidates: exact_match=1, score=50000.
- T DECIDE tag=A1b-qab kind=-2 slot=-1 gap=0.
- "INTENT VERBATIM-CONFLICT" count: 0.

The guard stayed silent on agreement (both answers "baq") and the
pre-existing qscore-tie rule produced the withhold. This is exactly
the repair's specified agree-refinement behavior. No over-broad
withholding. Scored as a control pass for the repair.

## Attack X-IU3-2: distinct-value table overflow (SUCCESS, DOWNGRADE)

### Fixture

129-pair training string built in Zag code (no literals beyond the
generator): byte values v in 33..163 excluding 59 (';') and 62
('>'), input bytes [v,'a','b'], output "xxx" for the first 120
pairs and "yyy" for the last 9. That is 129 distinct first-byte
values at split position 0. Direct discovery must fail (as in the
G3 fixture) so the split search runs; the setup check is the
"bridge: direct failed, inducing condition..." emit line.

### Observed behavior (3/3 runs identical, exit code 1)

- "ADV-BIGLINE pairs=129 bytes=1031"
- "ROUTE [...] -> PROC_LEARN (2+ segs, str>str)"
- "bridge: direct failed, inducing condition..."
- "panic: slice index out of bounds"

### Root cause

bridge_learn's split search collects distinct byte values at each
candidate position into `dvals:[]u8=z_alloc(128)`
(unified_learn.zag:503; intent_learn.zag:468). A byte holds 256
distinct values, and ndv increments once per distinct value with
no bound check: `dvals[ndv]=v as u8`. With 129 distinct values at
position 0, the 129th write targets dvals[128] and panics. R3
sized s1idx/s2idx by npairs but left the adjacent distinct-value
table fixed. The bug predates IU3 and is inherited identically by
both files; the finding is that the repair's crash hardening
covered the reported vector, not the buffer class. Verdict
contribution: DOWNGRADE (claim narrowing). The 18-pair K-IU3-3
fixture still passes (verified in X-IU3-3).

Boundary: the vector needs 129 or more pairs with 129 or more
distinct byte values at a single position, all extractable, and
failed direct discovery. Narrow but constructible, deterministic,
and 3/3 reproducible.

## Attack X-IU3-3: evidence reproduction (PASSED for the repair)

Rebuilt iu3_fix.zag, intent_learn.zag, and unified_learn.zag from
the committed sources with the pinned toolchain. Ran each binary 3
times. All runs byte-identical within each binary, and each
matches its committed raw file:

- iu3_fix: c5c4ecc9cdcf6210ab6f630778515fd0 (matches
  IU3_FIX_RAW.txt, including the md5 quoted in the repair report)
- intent_learn: 98315faec8faea24e75533892c0b240d (matches
  IU3_INTENT_REG_RAW.txt)
- unified_learn: 904de9f83a2873c7a8862b71804a9065 (matches
  IU3_UNIFIED_REG_RAW.txt)

Frozen K-IU3-5 (determinism) holds, and the 8/8 plus 10/10 plus
20/20 evidence reproduces exactly. No silent change.

## Attack X-IU3-4: source audit (PASSED for the repair)

(a) All 8 intent functions (intent_record_inputs,
intent_record_proc, intent_record_br, intent_exact_match,
intent_qscore, intent_winner, intent_trace_emit, intent_init) are
byte-identical between intent_learn.zag and unified_learn.zag
(X-IU4 faithfulness invariant holds).
(b) No test-answer literals ("qab", "xab", "tuv", "wqx", "baq",
"zzz", "xxx", "ccc", "ddd") appear in the mechanism regions of
either file (everything above main()).
(c) ce[] is assigned for every candidate in both the proc loop and
the bridge loop of intent_winner, in both files.
(d) The guard dispatches proc_apply versus bridge_apply by kind
for both top and second, in both files.
(e) WARN counts on the X-IU3-1a' fixture: exactly 2 (one per
17-pair learn), 0 for the in-cap 5-pair bridge learn. The frozen
G2 WARN behavior is unchanged (reproduced in X-IU3-3).

## Classification

Bounded L2 integration infrastructure, unchanged. The findings
narrow the repair's claims; they do not promote or demote the
mechanism's level. No representational invention is involved on
either side.

## Boundaries (consolidated)

- In-cap verbatim collisions still withhold (G1 reproduced
  byte-identically in X-IU3-3).
- The guard's agree-refinement behaves as specified (X-IU3-1b).
- The 16-input cap, the tie rule, and the WARN are unchanged and
  reproduced.
- Finding 1 needs the collision to straddle the cap on exactly one
  side. Finding 2 needs 129+ distinct byte values at one split
  position with failed direct discovery.

## Governance

Pure Zag throughout. No Python used at any stage: no generators,
no verifiers, no analysis scripts, no scratch tooling. Prereg
(a88de0031) strictly precedes attack code; the fixture amendment
is recorded transparently with its honest timeline. Only
adversary-owned files staged and committed: PREREG_IU3_ADV.md,
PREREG_IU3_ADV_AMEND1.md, iu3_adv.zag, IU3_ADV_RAW.txt, and this
report. No other agent's files touched. No em dashes in new
documentation.

## Recommended repairs (for the next hypothesis)

- R4 (X-IU3-1a'): make conflict detection robust to the record
  cap, e.g. record a truncated-evidence flag per record and
  withhold (or emit an explicit conflict-possible diagnostic) when
  a verbatim candidate on one side meets a truncated record on the
  other whose learned procedure answers differently; at minimum,
  scope the "no silent resolution" claim to in-cap collisions in
  the paper.
- R5 (X-IU3-2): size dvals by the byte range (256) or by npairs,
  and audit bridge_learn for any remaining fixed-size buffers
  (the WORK/PAIRBASE overlap beyond 128 pairs is a further latent
  capacity boundary worth a principled sizing argument).
