# REPORT: Cognitive Operation Body Learning (cogops_bodies)

**Verdict: COGOPS-BODIES-COMPLETE** (B1-B7 all PASS).
Prereg `a27dea64b` strictly precedes implementation. 3/3 byte-identical,
sha256 `fd0ad2ed0760c6836a1f71a710bac171de1d27015285be215b0254bfb00a384f`.

## Question

cogops_structures showed selection, composition, and retirement of
cognitive ops can be learner-owned, but op BODIES were researcher
bootstrap. Can the learner revise or create an operation body?

## What was built

`cb.zag` (~800 lines, pure Zag, pinned znc): the cogops 8-instruction
interpreter (SET/COPY/ADD/EQ/JNZ/MATCH/READF/YIELD) extended with three
consequence-driven body operators, all in learner state:

1. **REPAIR**: per-op sticky snapshot archives (graph, answer, ctx0);
   every 25 eps, if a body's replay score on its modal ctx is <400,
   exhaustive single-SET-imm (0..7) variant search; adopt iff
   best > champ+150 and best >= 600. On adopt the body is replaced
   in place, the op is un-retired, appl is reset (new body, fresh
   evaluation), origin=1.
2. **DIVERGE**: if op o is useless in ctx c (appl<200) but works
   elsewhere (appl>500), duplicate its body to an empty slot and run
   the same search against ctx-c snapshots; adopt on the same bar
   (origin=2), else free the slot.
3. **INLINE**: if base pair (p,q) has comp>=800 (n>=20), splice
   p[0..first-YIELD) ++ q ++ p[fail-tail] with generic JNZ
   retargeting into an empty slot (origin=3). Live selector/credit
   machinery decides its fate.

Worlds: F 40%, N1 25%, N2 15%, N3 20% (W-edge etype 5, F-shaped).
Planted: op 0 (gather) starts broken (etype SET=2, not 1); no innate
body matches etype 5. 600 episodes/arm. No INVENT_MODE, 0
modes/bridges/handlers/semantic cases.

## Results (treat arm)

- `REPAIR op=0 champ=0 best=1000 set#0 imm=1`: the exact planted bug
  (first SET, imm 2->1), found by blind search, adopted on replay
  consequences. Late F success: **134/134 (100%)**.
- `DIVERGE op=0 ->slot=5 ctx=0 champ=0 best=1000`: the duplicate was
  specialized to etype 5. Replay on N3 snaps: 1000. Body differs
  from op 0 (white-box). Late N3 success: **55/55 (100%)**.
- `INLINE pair=1,2 ->slot=6 len=208`: follow+complete spliced (26
  instructions, JNZ retargeted +32->+160). First-op share on late N1:
  **95/104 (91%)**. Solo invocations: 108/108.
- Efficiency: late N1 mean steps **114 vs 233** ablation (the inline
  nearly halves the 2-op sequence into 1 call).
- Solo: o0=191/191, o5=73/73, o6=108/108. Every created body works
  standalone and persists to episode 600.

## Ablation (all body machinery off)

- Late F: **0/134** (B2 PASS, repair is causal).
- Late N3: **0/55** (B4 gap = 100pp >= 40).
- No repair/diverge/inline events; origins all 0.

## Kill bars

- B1 REPAIR (origin[0]==1, F>=75%): **1** (100%).
- B2 REPAIR-CAUSAL (ablation F<=10%): **1** (0%).
- B3 DIVERGE (origin-2 body differs, replay>=850): **1** (1000).
- B4 DIVERGE-USEFUL (N3>=70%, gap>=40pp): **1** (100%, 100pp).
- B5 INLINE (origin-3 solo>=5, >=80%): **1** (108/108).
- B6 NO-BLOAT (<=2 created, parent!=3): **1**.
- B7 DETERMINISM: **1** (sha256 match x3).

## Two bugs found and fixed during development (transparent)

1. **OOB reward hack**: the first search run "repaired" op 2 via a
   variant whose broken sentinel comparison let it read `g_field(-1)`
   (adjacent log memory holding 0) and score 1000 on replay. Fixed by
   bounds-checking `g_field` (sentinel -999 on OOB), a principled
   interpreter soundness fix; correct bodies unaffected.
2. **Stale reputation**: the repaired op 0 was never re-selected
   (selector remembered its failures). Fixed by resetting appl on
   repair adopt (new body, fresh evaluation). This also unblocked
   DIVERGE, which needs post-repair N3 trials.

## SUF analysis (honest)

This is **L2 structural learning, not L3**. The search operator
(single-SET-imm enumeration), the splice operator (with JNZ fixup),
the trigger conditions, and the adopt bars are researcher-authored
generic machinery. What is learner-determined: which SET, which imm
value, which ctx to specialize for, which pair to inline, whether
each creation survives (live consequences), and the final byte
content of every created body (no created body existed in source).
The learner did not invent the *idea* of revising bodies. The
boundary is the same as the invention H1/H2/H3 workers': operators
researcher-owned, resulting forms consequence-determined.

What is genuinely new vs cogops_structures: bodies are no longer
immutable bootstrap. They are revised in place (repair), duplicated
and specialized (diverge), and composed into novel composites
(inline), all driven by experienced consequences with no task label
and no INVENT_MODE.

## Follow-ups

- Multi-point search (iterated single-point) for compound body bugs.
- Body revision for the *retired* harmful op (can predict's body be
  rehabilitated, or is retirement the right fate?).
- Inline of 3-op sequences; inline where the pair's order is wrong.
- Merge the replay archive into the tag-61 consequence substrate
  (currently a separate store; compression opportunity).
