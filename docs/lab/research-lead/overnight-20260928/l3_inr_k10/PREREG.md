# PREREG: L3-INR-K10 independent adversarial probe

Frozen: 2026-10-03. This prereg is committed BEFORE worlds are materialized
and before any arm runs. Predictions below are frozen; the verdict is read
off them after 3/3 byte-identical runs (seed 7).

## Context and non-goals

L3-INR-SEALED returned L3-KILLED (C409): the incomplete-disambiguation
trap showed the probe path materializes only the first disagreeing pair,
committing 12 edges at 4/6 heldout. Reclassification: L2+ (structural
learning with persistent state and revision, without reliable
hidden-instance generalization or transfer). The KILL is terminal and is
not revisited here. K10 maps the L2+ envelope: what CAN this architecture
do? Focus: the honest arms that passed, T4 (regime-change revision) and
T5a (probe resolution). Where is the boundary between L2+ success and
failure?

## Probe designs (materially different from S1-S5)

Opaque identifiers: fresh `w*` / `v*` names. Attributes verified
|Spearman|x1000 < 200 vs true order with the frozen spearman binary.
Budgets: T1/T5a/T4 per run_arm.sh (3000/3000/2000). Determinism: seed 7,
3/3 byte-identical digests over summary+trace.log+proto.log per sequence.

### P-C: probe-loop iteration (arm T5a on pc.world, fresh statedir)

True order: w0<w1<w2<w3<w4<w5<w6<w7<w8<w9.
Two gaps: u1 = adjacent pair (w4,w5) OMITTED from training (truth w4<w5);
u2 = adjacent pair (w6,w7) OMITTED (truth w6<w7). Bridges span both gaps:
(w3,w5),(w4,w6) for u1; (w5,w7),(w6,w8) for u2; plus (w4,w7) so no third
unconstrained pair arises. Jumps: (w0,w9). Negatives (5): (w7,w6,0) kills
the u2-reverse variant; (w1,w0,0),(w3,w2,0),(w9,w8,0),(w2,w1,0). Crucially
NO negative constrains u1's reverse, so the u1-false variant (adding
(w5,w4)) is training-consistent and survives the consequence filter.
PAIR listing order gives first-appearance ids: w5=0, w6=1, w4=2, w7=3,
w3=4, w8=5, w0=6, w1=7, w2=8, w9=9. Hence u1 is id-pair (0,2) with truth
REVERSED vs id order ((w5,w4) truth 0), and u2 is id-pair (1,3) with truth
forward ((w6,w7) truth 1).

Mechanism under test: probe_find scans (a,b) in id order. First
disagreeing pair is (0,2): variants {V1: u1-false+u2-true, V2:
u1-true+u2-true, E*} predict {1, 0, 0}. Probe (0,2) -> world truth 0.
hyps_filter keeps {V2, E*} (both predict 0): E* SURVIVES, nh=2, the loop
ITERATES (trace: PROBE_NEXT -> PROBE_SEND a second time),
PROBE_MATERIALIZE adds (2,0)=(w4,w5). Second probe: (1,3)=(w6,w7), truth 1,
E* eliminated, survivor {V2}, materialize (1,3), COMMIT.

Frozen predictions (P-C):
- HYP_KEPT 3 (V1, V2, E*); the two u2-reverse variants eliminated by
  (w7,w6,0).
- Exactly 2 PROBE_SEND events in trace.log: (0 2) with answer 0, then
  (1 3) with answer 1. PROBE_MATERIALIZE (w4,w5) then (w6,w7).
- TRAIN 18/18, HELD 6/6, EDGES 14, DEFER 0.
- K10-P1 verdict: PASS iff HELD 6/6 AND >=2 PROBE_SEND AND the second probe
  occurs after the first (loop iteration visible in trace).

Interpretation if PASS: the probe loop CAN iterate and resolve multiple
gaps. The S1 kill's boundary is precise: the loop stops when the first
discriminating probe's truth contradicts E* (answer 1 on a pair E*
predicts 0), eliminating the base hypothesis. When the first probe's truth
agrees with E* (answer 0), iteration continues. If FAIL: the loop never
iterates in practice, a tighter bound than S1 alone established.

### P-D: revision under id-permuted world (T1 on pd1.world -> T4 on pd2.world, shared statedir)

pd1.world: clean chain, true order v0<...<v9. TRAIN 18: 9 adjacents +
jumps (v0,v3),(v2,v5),(v4,v7),(v6,v9) + negatives
(v1,v0,0),(v3,v2,0),(v5,v4,0),(v7,v6,0),(v9,v0,0). Listing in name order ->
ids v0=0..v9=9. T1 commits chain (DEL removes jumps) to slot G.

pd2.world: MILD block-rotation regime change (same magnitude class as S2,
which passed): true order v0<v1<v2<v3<v6<v4<v5<v7<v8<v9. TRAIN 18:
adjacents minus gaps (v6,v4),(v4,v5),(v5,v7) [6] + jumps
(v0,v3),(v2,v4),(v3,v5),(v6,v7),(v4,v8) + long (v0,v9),(v1,v8) [13 pos] +
negatives (v5,v6,0) [toxic vs pd1's (v5,v6) edge],(v4,v3,0),(v9,v0,0),
(v8,v2,0),(v7,v4,0). Adversarial dimension (NEW vs S2): PAIR listing order
is PERMUTED -> first-appearance ids v8=0,v9=1,v7=2,v0=3,v1=4,v2=5,v3=6,
v6=7,v4=8,v5=9, fully deranged vs pd1's v0=0..v9=9.

Mechanism under test: T4 MONITOR re-tests pd2's first 6 training pairs
against slot G (pd1 ids); (v7,v8,1)->ids(2,0): G predicts 0, truth 1 ->
REJECT -> REGIME_CHANGE. Toxic purge then compares G edges (pd1 ids)
against pd2 training (pd2 ids) with NO remapping: G edges
(0,1)..(8,9); pd2 negatives (9,7,0),(8,6,0),(1,3,0),(0,5,0),(2,8,0) ->
ZERO matches -> ZERO DEL_EDGE_TOXIC. Stale pd1 edges persist in the wrong
id space; ADD's cycle guard rejects most true pd2 positives (stale chain
covers them positionally); DEL hill-climbs from a partial score.

Frozen predictions (P-D):
- T1(pd1): TRAIN 18/18, HELD 6/6, EDGES 9 -> PASS (baseline).
- T4(pd2): REGIME_CHANGE detected (trace); ZERO DEL_EDGE_TOXIC events;
  TRAIN <18/18; HELD <5/6 -> revision FAILS (predicted FAIL = successful
  adversarial probe).
- K10-P2 verdict: PROBE-SUCCESS iff T4 TRAIN<18 OR HELD<5/6 AND zero
  DEL_EDGE_TOXIC in trace.

Interpretation: sealed-battery finding #3 becomes an ACTIVE failure.
Revision works only when the revision world's PAIR listing preserves the
original id assignment; entity identity is positional, not by name. This
is the L2+ revision boundary.

### P-E: full-reversal revision, aligned ids (T1 on pd1.world -> T4 on pe2.world, shared statedir)

pe2.world: FULL ORDER REVERSAL of pd1: true order v9<...<v0. TRAIN 18:
9 negatives (v0,v1,0)..(v8,v9,0) + 9 positives
(v1,v0,1)..(v9,v8,1). Listing order SAME name sequence as pd1 ->
ids v0=0..v9=9 ALIGNED.

Mechanism under test: MONITOR first pair (v0,v1,0)->(0,1): G predicts 1,
truth 0 -> REGIME_CHANGE. Purge: all 9 G edges (0,1)..(8,9) exactly match
pe2 negatives -> 9 DEL_EDGE_TOXIC -> E empty. ADD seeds 9 reversed
adjacents; DEL keeps all; nu=0 -> COMMIT to G2.

Frozen predictions (P-E):
- T1(pd1): TRAIN 18/18, HELD 6/6, EDGES 9 -> PASS (baseline, same as P-D).
- T4(pe2): REGIME_CHANGE on 1st monitored pair; exactly 9 DEL_EDGE_TOXIC;
  TRAIN 18/18, HELD 6/6, EDGES 9 -> PASS.
- K10-P3 verdict: PASS iff TRAIN 18/18 AND HELD 6/6 AND 9 toxic purges.

Interpretation if PASS: revision handles ARBITRARY regime magnitude
(full reversal) given id alignment. Combined with P-D: the revision
boundary is EXACTLY id-alignment, not change magnitude. Positive L2+
envelope evidence: purge+rebuild is a capable structural-revision
operator within its precondition.

## Kill bars (characterization bars, not L3 bars)

- K10-P1-PASS: pc.world T5a: HELD 6/6, >=2 PROBE_SEND, loop iteration in trace.
- K10-P2-PROBE-SUCCESS (predicted): pd2 T4: (TRAIN<18 OR HELD<5/6) AND 0 DEL_EDGE_TOXIC.
- K10-P3-PASS: pe2 T4: TRAIN 18/18 AND HELD 6/6 AND 9 DEL_EDGE_TOXIC.
- K10-DET: all sequences 3/3 byte-identical (sha256 of
  summary+trace.log+proto.log identical across runs 1/2/3).

## Governance

- The L3-KILL verdict (C409) is terminal; nothing here revisits it.
- No L3 claim is made under any outcome. PASS outcomes characterize L2+
  capability; they do not promote the architecture.
- Frozen implementation never modified (read-only). Learner never opens a
  world file (two-process protocol via frozen run_arm.sh).
- Commits local, never push, explicit pathspecs.
