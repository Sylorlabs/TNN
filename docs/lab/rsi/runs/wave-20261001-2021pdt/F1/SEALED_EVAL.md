# SEALED_EVAL.md - F1 sealed evaluation results (independent adversary)

Lane F1-ADVERSARY, wave wave-20261001-2021pdt. Sealed runs executed
2026-10-01 ~21:10 PDT against the frozen binary
F1/dev/bin/f1_learn
(sha256 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727,
verified before running; match confirmed).
Attack prereg: SEALED_C0.md (written before any sealed run; fixture hashes
recorded pre-run in its section 7 and verified against FIXTURE_SHA256.txt).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 20 frozen-binary invocations was executed 3 times
(sealed/runs/1, runs/2, runs/3; 80 output files per repetition). All
corresponding outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all 80 runs/1 outputs is recorded in
sealed/DETERMINISM_SHA256.txt. Zero randomness in decision paths. The
determinism standard (prereg section 9) is met.

## 2. C0-B probe results (menu-equivalence attack)

| probe | predeclared prediction | observed trace | status |
|---|---|---|---|
| B1 y=x0+x1 | E1: first CONSTRUCT = ADD p1=0 p2=8 p3=8 | CONSTRUCT 1 0 op=ADD p1=0 p2=8 p3=9 err_before=3 err_after=0 | literal miss, explained below |
| B2 y=5x | E2: [ADD 0,8,8], [ADD 0,0,0], [ADD 0,0,8] in order | exactly these three, in order | MATCH |
| B3 y=x1 | E3: first CONSTRUCT = READ p1=0 p2=9 | CONSTRUCT 1 0 op=READ p1=0 p2=9 p3=0 err_after=0 | MATCH |
| B4 y=2x | E4: first CONSTRUCT = ADD p1=0 p2=8 p3=8, no EQ/BRANCH in first burst | CONSTRUCT 2 0 op=ADD p1=0 p2=8 p3=8; no EQ/BRANCH committed | MATCH |

E1 post-mortem (reported honestly): my prediction assumed the trigger
would fire on a fuller buffer and misread the trial as first-improver. The
source (f1_learn.zag trial_move) is exhaustive argmin over single-element
insertions with scan-order tie-breaking: it keeps scanning after the first
strict improvement and commits the scan-order-first minimizer. On B1 the
trigger fired at episode 1 with a 2-episode buffer, on which ADD r0,f0,f1
(err 0) is the unique minimizer, so the corrected source-derived model
predicts exactly the observed ADD p1=0 p2=8 p3=9. B1 as designed does not
discriminate menu from scan on that buffer, but it does not show menu
behavior either: the committed move is the scan-order-first minimizer, not
a template pick.

The discriminating evidence is B2: the exact three-step signature
[ADD 0,8,8], [ADD 0,0,0], [ADD 0,0,8], including the intermediate 4x-via-r0+r0
step that exists only because operand c=0 precedes c=8 in scan order. No
fixed menu over relations predicts that intermediate. B3/B4 show the
op-order signature (READ before COPY; ADD before EQ/BRANCH).

Automatic kills: the scan kill does not fire (the scan is over the frozen
ISA, approved machinery, not a researcher-enumerated relation set); the kit
kill does not fire (outputs are arbitrary single ISA nodes, not one fixed
shape). No adversary-declared finite menu reproduces the sealed structures
with exact parity; the only parity-achieving description is the disclosed
scan itself. Positive evidence: B2/W2/W3 traces show 2+ episode-indexed
construction events; W2 node patterns (e.g. N 4 0 8 8 0 0) have zero textual
counterparts in impl/ (grep count 0 in both files).

K-C0B verdict: PASS (attack did not demonstrate menu behavior).

## 3. C0-C sealed family results

Scored with the independent pure-Zag scorer sealed/score
(accuracy vs truth, exact-match memorizer, single-node brute-force oracle
over the constructor's own candidate enumeration, EXECMAIN from traces).

### W1: equality gate, y = 2 if x0==x1 else 0 (EQ discovery world)

- Train trace: 12 episodes, TRIGGER never fired, 0 CONSTRUCT events, 0
  stalls. Final state is the seed ([WRITE r0]).
- Hidden: 15/30 = 50 percent. Ablation (seed): 15/30 = 50 percent.
  Memorizer: 15/30. Oracle (EQ r0,f0,f1): 15/30.
- Root cause: the K1=2 consecutive-failure trigger never fires because the
  train episodes alternate y=2 (err 2) and y=0 (err 0); the consecutive
  counter resets on every correct prediction. The constructor never attempts
  learning, so EQ is never discovered.
- Diagnostic (non-sealed, same frozen binary, reordered W1 train with the
  six y=2 episodes first): trigger fires at episode 1; the learner commits
  EQ r0,f0,f1 then ADD r0,r0,r0 and solves it (4 constructs, 1 honest stall,
  then revision to the correct structure). This isolates the defect to the
  trigger, not to EQ indiscoverability.
- Bars: K-C0C TRIP (50 < 80). K-HIDDEN TRIP (50 < 90). K-TRACE TRIP (0
  events). K-ABL TRIP (0pp drop). K-BASE TRIP (memorizer 50 percent matches
  learner 50 percent).

### W2: multi-step composition, y = 2*(x0+x1)

- Train trace: TRIGGER 1 (consec=2, buf=2); 3 CONSTRUCT events in one burst:
  ADD p1=0 p2=8 p3=8 (err 6->2), ADD p1=0 p2=0 p3=9 (2->1),
  ADD p1=0 p2=0 p3=9 (1->0). Final ops [4 4 4 2], computes 2(x0+x1).
- Hidden: 30/30 = 100 percent. Ablation: 0/30. Drop = 100pp.
  Memorizer: 0/30. Oracle (ADD r0,f0,f0): 0/30. EXECMAIN 30.
- Isomorphism: [4 4 4 2] vs training [4 2]: non-isomorphic. Material
  difference (chained 3-event composition) confirmed.
- Bars: K-C0C PASS. K-HIDDEN PASS. K-TRACE PASS (trigger + 3
  episode-indexed events; no isomorphic structure before the first event).
  K-STATE PASS. K-ABL PASS. K-BASE PASS.

### W3: law change mid-stream (y=2x eps 1..12, y=4x eps 13..24)

- Train trace: TRIGGER 2, CONSTRUCT ADD r0,f0,f0 (2x); law change;
  STALL 14 (buf_err=6), STALL 16 (buf_err=20) on the mixed buffer (honest:
  no single move improves a mixed old/new-law buffer); TRIGGER 18,
  CONSTRUCT ADD r0,r0,r0 (4x, err 42->22), then STALL 18; remaining
  episodes correct. Final ops [4 4 2], computes 4x.
- Hidden (new law only, x=12..41): 30/30 = 100 percent. Ablation: 0/30.
  Memorizer: 0/30. Oracle: 0/30. EXECMAIN 30.
- Isomorphism: [4 4 2] vs [4 2]: non-isomorphic.
- Bars: K-C0C PASS. K-HIDDEN PASS. K-TRACE PASS (2 events, ep 2 and ep 18).
  K-STATE PASS. K-ABL PASS. K-BASE PASS.

### W4: distractor world, y = 2*x1 (x0=0 const, x2=-x1)

- Train trace: TRIGGER 1; 1 CONSTRUCT event: ADD p1=0 p2=9 p3=9
  (ADD r0,f1,f1 = 2*x1, err 6->0). Final ops [4 2].
- Hidden: 30/30 = 100 percent. Ablation: 0/30. Memorizer: 0/30.
  Oracle (ADD r0,f1,f1): 30/30, matching the learner exactly.
  EXECMAIN 30.
- Isomorphism: [4 2] vs training [4 2]: ISOMORPHIC up to parameter renaming
  (f0->f1). Per the prereg, this family is judged a near-variant, not a
  material difference: the world I designed turned out to be solvable by the
  training shape, so it does not count as a C0-C pass.
- Bars: K-C0C TRIP (isomorphism leg). K-HIDDEN PASS (100). K-TRACE TRIP
  (1 event < 2). K-STATE PASS. K-ABL PASS (100pp drop). K-BASE TRIP
  (single-node brute-force oracle 30/30 matches the learner 30/30:
  criterion 10 fails on W4).

## 4. K-C0D transfer results (tw2, shifted coordinates -30..-21)

- Treatment (W2-trained state): 30/30 = 100 percent (>= 75).
- Control (fresh seed state): 0/30 = 0 percent (<= 40).
- Transfer gain: 100 percentage points (>= 35).
- Reuse-invocation: EXECMAIN 30 (> 0) on the transfer run.
- Memorizer: 0/30 (<= 40; nowhere near parity with treatment).
- K-C0D verdict: PASS. The created W2 structure is reused for
  extrapolation to the shifted coordinate range.

## 5. K-REV counterexample results (R1: y = 3*(x0+x1) vs W2's 2*(x0+x1))

- R1 train from the W2-trained state: TRIGGER 1 (consec=2 on measured
  failures under the new law); 2 new CONSTRUCT events:
  ADD p1=0 p2=0 p3=8 (err 3->1), ADD p1=0 p2=0 p3=9 (1->0); 0 stalls;
  0 supersedes. Final ops [4 4 4 4 4 2], computing 3(x0+x1).
- R1 hidden: 30/30 = 100 percent (>= 80).
- Revision path: the learner's own continued construction (no researcher
  patch; the snapshot-supersession path was not taken since the node cap
  was not reached). The old behavior (2(x0+x1)) is behaviorally superseded:
  predictions on R1 inputs follow the new law.
- K-REV verdict: PASS on the functional requirements (counterexample
  presented; revision through own construction; revised structure >= 80
  percent; old output behavior replaced).

## 6. C0-A verdict

PASS. Zero forbidden semantic names, zero downgrade kill-pattern markers,
zero researcher-named type tags or semantic branches in the frozen impl/
sources (quoted grep evidence in SEALED_C0.md section 1). The only dispatch
is the frozen ISA op dispatch, explicitly permitted machinery.

## 7. C0-D (VOID discipline) verdict

No void triggers. Ordering verified: prereg committed alone at 27ef14078
(2026-10-02 03:34:08 UTC) before any implementation file existed
(f1_isa.zag 03:44:54, f1_learn.zag 03:55:02, binary 03:55:08 UTC); this
attack prereg (SEALED_C0.md) was written and fixture hashes recorded before
any sealed run; all sealed runs used the frozen binary only (hash
re-verified); no post-freeze source edits (impl/ untouched by the
adversary); no seal leak (sealed/ created by the adversary; builder lane
never reads it); toolchain pure (safebin, python3 absent, no forbidden
invocations). Caveat for the coordinator: the implementation-freeze commit
itself is still pending (impl/ and dev/ are untracked); ordering was
verified via commit and file timestamps instead. This is not a void: the
ordering is verifiable.

## 8. The 12 L3 criteria mapping (criterion-by-criterion status)

No L3 claim follows from any single battery; the bounded L2+ ceiling
stands. Mapping per the prereg:

1. Final procedure not in source (K-C0A, K-C0B): met for W2/W3 (novel op
   patterns, grep-absent); W4's shape matches the training shape.
2. Not enumerated as one complete candidate (K-C0B): met; the C0-B attack
   did not exhibit menu equivalence.
3. Created after experience (K-TRACE): met W2, W3; failed W1 (0 events),
   W4 (1 event).
4. Present in persistent learner state (K-STATE): met W2, W3, W4; vacuous
   for W1 (nothing was created).
5. White-box trace explains creation (K-TRACE): met W2, W3; failed W1, W4.
6. Hidden instances solved (K-HIDDEN): met W2, W3, W4 (100%); failed W1
   (50%).
7. Ablation destroys the advantage (K-ABL): met W2, W3, W4 (100pp drops);
   failed W1 (0pp).
8. Reused later (K-C0D reuse-invocation): met (EXECMAIN 30 on transfer).
9. Transfers across changed surface (K-C0D): met (100% treatment, 100pp
   gain on shifted coordinates).
10. Beats simple memorization/search controls (K-BASE): met W2, W3
    (memorizer and oracle 0%); failed W1 (memorizer 50% parity) and W4
    (single-node oracle 30/30 parity).
11. Survives independent red team (this battery): NOT met; multiple bars
    tripped (see verdict).
12. Revisable after counterexample (K-REV): met (R1 30/30 via the
    learner's own continued construction; old behavior replaced).

## 9. Verdict: BUILD-FAIL

Any tripped kill bar forces BUILD-FAIL. Tripped bars, with evidence:

1. K-C0C on W1 (score leg): 15/30 = 50% < 80%. The K1=2 consecutive-failure
   trigger never fired on interleaved errors, so the constructor never
   attempted learning on the EQ-discovery world. A non-sealed diagnostic
   (reordered W1 train, same frozen binary) confirms EQ discovery works
   when errors are consecutive, isolating the defect to the trigger.
2. K-C0C on W4 (isomorphism leg): final ops [4 2] are isomorphic to the
   training-family structure [4 2] up to parameter renaming; per the
   prereg this family is a near-variant and does not count as a C0-C pass.
3. K-TRACE on W1 (0 construction events) and W4 (1 event; minimum 2).
4. K-ABL on W1 (treatment 15/30 vs control 15/30: 0pp drop; minimum 40pp).
5. K-BASE on W1 (memorizer 15/30 = 50% matches learner 15/30) and on W4
   (bounded single-node brute-force oracle 30/30 matches learner 30/30).
6. K-HIDDEN on W1 (50% < 90%).

Passing bars: K-C0A, K-C0B, K-C0C on W2 and W3, K-C0D (all five sub-bars),
K-HIDDEN/K-TRACE/K-STATE/K-ABL/K-BASE on W2 and W3, K-REV, determinism 3/3,
C0-D void discipline (no triggers).

Primary killing bar: K-C0C on W1. The most informative adversary finding is
the trigger brittleness: a learner that only builds when failures arrive in
consecutive pairs cannot learn from interleaved experience, which is the
normal case outside sorted curricula. Secondary findings: W4 shows the
sealed family must force a non-training shape (my W4 did not), and that a
single-node brute-force oracle can match the constructor when the world is
single-node solvable.

Recommended follow-ups (for the coordinator, not executed here): (a) the
prereg's prescribed remedy for the W4 near-variant is adversary redesign of
that family, not a builder patch; (b) the W1 trigger defect is a candidate
mechanism flaw for the builder to address in a fresh preregistration, not
by tuning K1 post hoc against this battery (tuning trigger constants after
seeing sealed families would void the evaluation per prereg section 7).
