# PREREG_SEALED.md -- Sealed Strong Composition (Micah Priority 4)

Committed BEFORE any implementation. Frozen kill bars below govern the
verdict. Broken prereg or weakened bar after results = fresh prereg.

## Task

Learn skill X independently. Learn domain Y independently. Later receive
novel goal Z requiring both. No paired X+Y examples. No explicit
combination hint. No task label.

- X = formal scalar operation, induced from scalar (in,out) examples as an
  executable 2-node graph: IN -> ADD(k). Induction hypothesis family:
  out = in + k, k taken from the first example, verified on the rest.
  Fails closed on non-constant examples.
- Y = sequence domain: register sequences, indexed read, length, build.
  Sequences are never transformed during Phase 2.
- Z (sealed) = new sequence S* plus target T* where T*[i] = X(S*[i]).
  Presented as unlabeled data plus a target. No mention of X or Y.

## Mechanism under test

`sc_solve`: generic candidate enumeration over LEARNED structures only.
Families: COPY (any registered sequence of matching length) and ELTWISE
(any learned scalar proc applied elementwise to any registered sequence
of matching length). Candidates verified elementwise against the target.
First verified candidate wins. No labels, no hint, no "combine" call.
On success a new executable Z record is created (ELTWISE with proc=X)
with provenance links to the selected proc and to the sequence domain.
Z is later applied directly to a fresh sequence (Z2 reuse).

Researcher-authored: induction family {out = in + k}, candidate families
COPY/ELTWISE, candidate order, driver world. Learner-owned: k values,
which proc, which sequence, Z record, provenance links.

## Arms (one binary, fresh workspace per arm, fixed order)

- TREAT: X1(add7), X2(add2) taught; SA,SB,SC,SD taught; gap; sealed Z;
  then Z2 reuse via direct Z apply.
- ABL-X: scalar proc records deleted after training; sealed Z must fail.
- ABL-Y: sequence domain disabled after training (no sequence registration
  or traversal); sealed Z must fail.
- FRESH: no training; sealed Z must fail.
- NO-COMPOSE: training intact; ELTWISE family disabled; sealed Z must fail.

## Frozen kill bars

1. TREAT solves Z: produced sequence equals target elementwise, selected
   proc is X1 (k=7), selected sequence is S*.
2. TREAT creates Z record with provenance links to X1 and the Y domain.
3. TREAT Z2: direct Z apply on unseen S2* yields the correct target with
   exactly 1 verify and no search.
4. ABL-X: Z unsolved (ans = -2).
5. ABL-Y: Z unsolved (ans = -2).
6. FRESH: Z unsolved (ans = -2).
7. NO-COMPOSE: Z unsolved (ans = -2). Proves the ELTWISE mechanism causal.
8. No paired X+Y examples: machine check. An eltwise-execution counter is
   zero at the end of Phase 2 in every arm that reaches Phase 3.
9. Determinism: 3 runs of the binary, byte-identical transcripts (cmp).
10. Induction fails closed: non-constant gap examples produce no proc.

Verdict on all bars passed: COMPOSITION-SEALED-COMPLETE with causal
reuse proof. If bar 1 fails: COMPOSITION-SEALED-FAIL. No rescue, no
re-interpretation.

## Standing constraints

Pure Zag. Safebin PATH from worker startup. `which python3` and
`which python` return nothing. Frozen source read-only. Unfrozen only.
Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
No em/en dashes in loop documentation.
