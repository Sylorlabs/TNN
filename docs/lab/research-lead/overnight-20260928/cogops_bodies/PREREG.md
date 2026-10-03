# PREREG: Cognitive Operation Body Learning (cogops_bodies)

Frozen before implementation. 2026-10-02.

## Question

Can the learner create or revise a cognitive operation BODY (the
instruction sequence executed by the interpreter), not just the control
parameters (applicability, composition, retirement) around it?
This is the SUF frontier left open by cogops_structures.

## Setup (unfrozen variant, pure Zag, pinned znc)

Base: the cogops 8-instruction interpreter (SET/COPY/ADD/EQ/JNZ/MATCH/
READF/YIELD), 5 innate op bodies, learner-owned appl/comp/tot/retired,
epsilon-greedy selector. Worlds: F (V-edge, 40%), N1 (D then V+R, 25%),
N2 (S then V, 15%), N3 (W-edge etype 5, F-shaped, 20%).

Planted facts:
- Op 0 (gather) starts BROKEN: its etype SET is 2, not 1. It fails on
  all F worlds until revised.
- N3 worlds are solvable by no innate body (etype 5 matches nothing).

## Learner-owned body machinery (all in learner state)

1. Snapshot archives: per-op sticky archives (20) of (graph, answer,
   ctx0, used_mask); per-ctx0 sticky archives (4). The consequence
   system already observes true answers post-hoc (as the existing
   credit rule does); archives reuse this for offline trials.
2. Repair: every 25 eps, for op o with tot uses>=20, tot mean<-300,
   >=6 archived snaps, budget left: exhaustive single-SET-imm
   (0..7) variant search scored by replay on o's modal-ctx0 snaps.
   Adopt iff best > champion+150 AND best >= 600 (x1000).
   On adopt: body replaced in place, op un-retired, origin=1.
3. Diverge: every 25 eps, for op o with appl(o,c)<-300 (n>=6) in ctx c
   but appl(o,c2)>500 (n>=15) elsewhere, empty slot, ctx snaps>=3:
   duplicate o's body to the slot, run the same search against
   ctx-c snaps, adopt on the same bar. origin=2, parent=o.
   On search failure the slot is freed.
4. Inline: every 25 eps from ep 150, for base pair (p,q) with
   comp_n>=20, comp mean>=800, both unretired, not yet inlined:
   splice p[0..first-YIELD) ++ q ++ p[fail-tail], with generic JNZ
   retargeting for jumps over the stripped region. Install in empty
   slot. origin=3. Live evaluation by the normal selector/credit
   machinery decides its fate.

Researcher-owned: the three operators, search order, bars, budgets
(3 repairs/op, 1 diverge/op, 2 inlines), the 8-instruction ISA.
Learner-owned: which variants win, which pairs inline, all slot
bodies after creation, all selection/retention.

No INVENT_MODE. No new mode/bridge/handler/semantic case.

## Kill bars (x1000 fixed point; 600 episodes/arm; 3/3 byte-identical)

- B1 REPAIR: op_origin[0]==1 AND late F success >= 75%.
- B2 REPAIR-CAUSAL: ablation (all body machinery off):
  late F success <= 10%.
- B3 DIVERGE: exists created op with origin==2 whose body differs
  from op 0 (>=1 byte) AND replay success on ctx0=0 snaps >= 850.
- B4 DIVERGE-USEFUL: treat late N3 success >= 70% AND
  (treat - ablation) >= 40 percentage points.
- B5 INLINE: exists created op with origin==3, solo-invoked >=5
  times, solo success >= 80%.
- B6 NO-BLOAT: created ops (origin 2/3) <= 2 AND no created op has
  parent == 3 (predict never duplicated or inlined).
- B7 DETERMINISM: 3 runs byte-identical (sha256).

OVERALL: B1..B7 all PASS -> COGOPS-BODIES-COMPLETE.

## Expected SUF bound

Honest expectation: L2 structural learning, not L3. The search and
splice operators are researcher-authored generic machinery; the
resulting bodies are learner-determined by experienced consequences
(which SET, which value, which pair, whether to adopt). The report
will state this boundary explicitly.
