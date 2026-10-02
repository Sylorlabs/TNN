# REPEXPAND-1 Simple-Baseline Comparison: Report

Date: 2026-09-30. Pure Zag. No Python at any stage.
Prereg frozen at `dc74cb523` (amended transparently at `9ef37be36`,
pre-implementation) BEFORE any baseline code existed. No amendments
after implementation.

## Verdict: BASELINE-MATCHES

No simple baseline beats or ties the COUPLED node on the frozen
generalization test. The task is not solvable by memorization,
nearest-neighbor copying, or exhaustive search of the frozen base
language L. This is a baseline-comparison verdict under the frozen
K-BL-4 rule, not a promotion. REPEXPAND-1 remains BUILD-PASS
(independently reproduced), NOT SURVIVES.

## What was built

`rxbase.zag`: the three frozen baselines, reimplemented from the
frozen world spec (PREREG_REPEXPAND.md at `cb3523684`), not from the
builder's source. All baselines observe the 6 TRAIN episodes under the
same sequential reveal protocol the learner had (answer revealed after
each prediction attempt), then run frozen on HIDDEN, EXTENDED, and
TRANSFER.

- B1 MEM: stores (n -> (s1,l1,s2,l2)) on first observation; predicts
  the stored tuple for a seen n, failure otherwise. No generalization.
- B2 NN: same table; predicts the stored tuple of the closest seen n
  (tie: smaller n), copying lengths verbatim, never scaling.
- B3 LEXH: all 604 canonical L-expressions (512 singles + 92 diagonal
  ALTs) with L prediction semantics from the frozen prereg, scored
  (a) on E_1..E_12 to verify the impossibility number, and (b) as an
  oracle ceiling on the 17 experiment episodes.

## Bar-by-bar

**K-BL-1 (build/run): PASS.** Built with the frozen toolchain
(`znc 2026.07.0-dev`), native binary, exit code 0 on all three runs,
stderr 0 bytes on all three runs.

**K-BL-2 (determinism): PASS.** 3 consecutive runs byte-identical
(shell cmp), md5 `70236a308f4675c130b8a87eb5f85bfc`.

**K-BL-3 (complete report): PASS.** BX-EP lines for all 34
baseline-episode runs, BX-SUM lines for every baseline x phase,
BX-LEXH lines for both checks, and the BX-VERDICT line, all in
`RXBASE_RAW.txt`.

**K-BL-4 (verdict rule): BASELINE-MATCHES.** Frozen rule: BASELINE-BEATS
iff any baseline scores >= 4/4 on HIDDEN or the LEXH verification finds
max604 != 3. Observed: B1 HIDDEN 0/4, B2 HIDDEN 0/4, B3-oracle HIDDEN
0/4, max604 = 3. No trigger fires.

**K-BL-5 (purity): PASS.** Implementation, compile, and runs in pure
Zag (shell only for compile/cmp/md5/rm). Byte scan: zero em dash
bytes in all authored docs in this directory.

## Exact numbers

| baseline | TRAIN /6 | HIDDEN /4 | EXTENDED /3 | TRANSFER /4 | total /17 |
|---|---|---|---|---|---|
| B1 MEM | 0 | 0 | 0 | 1 | 1 |
| B2 NN | 0 | 0 | 0 | 1 | 1 |
| B3 LEXH (oracle best) | 3 | 0 | 0 | 0 | 3 |
| COUPLED node v1 (ref) | 3 | 4 | 4 | 4 | 14 |

Node reference: TRAIN 3/6 (first three episodes failed before node
creation at ep2), HIDDEN 4/4 (n=9,11,15,17), EXTENDED 3/3
(n=13,20,30), TRANSFER 4/4. The node total on the same 17 episodes is
14/17; the strongest template baseline reaches 3/17.

B3 details:
- Check (a): max over the 604 L-expressions on E_1..E_12 = 3,
  attained first by cand 548 (ALT3 branches 1,2,3). This reproduces
  the builder's max604=3 exactly, computed here directly from episode
  semantics rather than the builder's shortcut.
- Check (b): oracle ceiling on the 17 episodes = 3/17, attained first
  by cand 569 (ALT3 branches 2,3,4): TRAIN 3/6, HIDDEN 0/4, EXTENDED
  0/3, TRANSFER 0/4. HIDDEN and EXTENDED n values (9,11,13,15,17,20,
  30) all exceed the branch cap of 8, so no branch ever fires there;
  TRANSFER is unreachable via spec '$' and symbols x/y, which L
  cannot emit (fixed symbols 'a','b').

## Reading the TRANSFER 1/4 for B1/B2

The single TRANSFER point for B1 and B2 is T1 (spec='$', n=4,
a^4 b^4): n=4 was seen in TRAIN and the stored tuple happens to
match. T3 (n=3 seen) fails on the symbol mismatch: the stored tuple
is (a,3,b,3), the actual content is (x,3,y,3). Exact-key memorization
cannot cross the alphabet change; the node binds symbol slots to head
positions and scores T3 and T4 exactly. This is a miss, not near
generalization: both baselines score 0/4 on every phase that requires
an unseen n.

## What this does and does not show

- It shows the v1 generalization claim (HIDDEN 4/4, EXTENDED 3/3,
  TRANSFER 4/4 on n values never seen, beyond every frozen constant,
  across changed spec byte and alphabet) is not reachable by storing
  seen pairs, copying the nearest seen pair, or any of the 604 frozen
  template expressions even when the template is chosen with full
  test knowledge.
- It independently confirms the builder's in-program ablation
  (growth-disabled bestL: HIDDEN 0/4) and the impossibility number
  (max604=3).
- It does not test the CONTRADICTION/REVISE arc, the "disguised menu"
  objection, OOD cases beyond the frozen sets, or the transfer of a
  revised node. Those belong to later pipeline steps and the
  independent adversary.

## Commits (branch tnn-native-lab, local only)

- Prereg frozen alone: `dc74cb523` (strictly before implementation).
- Transparent pre-implementation amendment: `9ef37be36` (corrected
  non-frozen TRAIN predictions 6/6 to 0/6 under the sequential
  protocol; bars, definitions, verdict rule unchanged).
- Implementation + raw evidence + this report: committed together
  after the frozen 3/3 run (see commit hash in the parent log).

Raw evidence: `RXBASE_RAW.txt`,
md5 `70236a308f4675c130b8a87eb5f85bfc`.
Program verdict line:
`BX-VERDICT BASELINE-MATCHES b1_hidden=0/4 b2_hidden=0/4 b3_hidden=0/4 max604=3`
