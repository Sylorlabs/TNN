# REPORT.md -- H-CATFORGET-1: Catastrophic Forgetting under Interference

Worker: Catastrophic Forgetting Worker (H-CATFORGET-1), 2026-10-02.
Verdict: CATFORGET-COMPLETE (R1=1, R2=1, R3=1, R4=1, R5=1 on all
3 seeds).
Determinism: 3/3 byte-identical (sha256
3572d18999898f2e4d7b6cb5ab08cf83469c78c47bdd539c9308212ae0b67dc8).

## 1. What was built

`catforget.zag`: a standalone pure-Zag interference battery. One
persistent learner per arm runs three phases with no reset:

- Phase 1 (200 episodes): master task A, the follow->complete
  composition on N1 worlds ((Q)-[D]->(E2), (E2)-[V]->V2,
  (E2)-[R]->K, answer V2+K).
- Phase 2 (300 episodes): interfering task B on the same tables.
- Phase 3 (100 episodes): re-test A with learning frozen (harness
  skips all writes; selection code identical, so this is not a
  learner mode). Retention = Phase-3 A success rate.

Learner machinery (generic): graph store, 4-instruction interpreter
(MATCH/ADD/ANSWER/SETCUR) executing 5 learner-owned byte-array op
bodies (gather, follow, complete, followT, readU), epsilon-greedy
bandit scoring appl + comp, generic consequence credit, consequence
ring. The interpreter never branches on op id; the selector never
branches on op id. Zero modes, bridges, handlers, semantic cases.

Arms (2x2) x 3 seeds (111, 222, 333), one binary, fixed order:
- FULL-SIM: comp consulted; B = F worlds ((Q)-[V]->ans), which write
  the SAME appl cell (gather,1) that Phase 1 teaches as -1000:
  maximally similar interference.
- SEV-SIM: comp recorded but severed from scoring (the C220
  contrast); B = F.
- FULL-DIFF: comp consulted; B = U worlds ((Q)-[T]->(E4),
  (E4)-[U]->W), touching only appl rows 3,4 and comp pairs among
  {3,4}: disjoint substrate.
- SEV-DIFF: comp severed; B = U.

## 2. Results

Retention table (Phase-3 A success %, learning frozen):

| seed | FULL-SIM | SEV-SIM | FULL-DIFF | SEV-DIFF |
|------|----------|---------|-----------|----------|
| 111  | 100      | 0       | 100       | 100      |
| 222  | 100      | 0       | 100       | 100      |
| 333  | 100      | 0       | 100       | 100      |

Preregistered bars (all required on all 3 seeds):
- R1 mastery: late-Phase-1 N1 success = 100% in all 4 arms
  (bar >= 90%); comp(1,2) = 1000 in FULL arms (bar >= 900). PASS.
- R2 shielding: FULL-SIM retention = 100% (bar >= 90%). PASS.
- R3 catastrophic forgetting: SEV-SIM retention = 0% (bar <= 30%).
  PASS.
- R4 link effect: FULL-SIM minus SEV-SIM = 100pp (bar >= 50pp).
  PASS.
- R5 gradient: FULL-DIFF = 100% and SEV-DIFF = 100% (bar >= 90%);
  SEV-DIFF minus SEV-SIM = 100pp (bar >= 50pp). PASS.

Verdict: CATFORGET-COMPLETE.

## 3. Mechanism (white-box, x1000 fixed point)

Phase 1 teaches: appl(gather,1) = -1000 (gather answers wrong at E2),
appl(complete,1) = +1000, appl(follow,2) = 945..960,
comp(follow,complete) = 1000. Late-Phase-1 success 100% in every arm,
including SEV (which masters A via appl alone).

Phase 2 (SIM arms) corrupts the shared cell directly: appl(gather,1)
inverts from -1000 to +875..+929 (300 F episodes of +1 against the
Phase-1 -1000 history), while appl(complete,1) degrades to 654..732
(complete is tried first in each F episode and fails, recording 0s).
comp(1,2) stays exactly 1000: F episodes are single-op, so no pairs
are written. appl(follow,2) is untouched (F never sees ctx=2).

Phase 3 at E2 (ctx=1, the ambiguous shared context):
- FULL: score(complete) = appl + comp = ~700 + 1000;
  score(gather) = ~900 + (-1000). The composition link routes around
  the corrupted cell. Retention 100%.
- SEV: score = appl only; gather (~900) beats complete (~700);
  gather answers V2 instead of V2+K; every episode fails.
  Retention 0%.

The sharpest detail: in SEV-SIM, comp(1,2) = 1000 is present in
learner state (recorded during Phase 1) but severed from scoring.
The link exists; only its functional role is removed, and A is
entirely forgotten. This isolates the C220 hypothesis to the
decision-loop role of structural connections, not their mere
presence.

DIFF arms: Phase-2 U episodes touch only disjoint cells
(appl(gather,1) stays -1000, comp(1,2) stays 1000), so both FULL-DIFF
and SEV-DIFF retain A at 100%. Similarity, not mere continued
training, drives forgetting: SEV-DIFF minus SEV-SIM = 100pp.

## 4. Architecture audit (One-System Rule)

- New file: catforget.zag only (~470 lines).
- Cognition lines added: ~470, all in the standalone file.
- New modes / bridges / handlers / semantic cases: 0.
- New hardcoded op sequences in learner code: 0.
- Learner-state structures: 5 op bodies, appl 5x32, comp 5x5,
  consequence ring (24x2). The phase loop and Phase-3 freeze are
  harness-level.
- Capability-source delta: the follow->complete composition and all
  retention behavior exist only in learner tables; source holds only
  generic machinery.

## 5. Limitations and next steps

- Op bodies are innate bootstrap (fixed byte arrays); only
  applicability, composition links, and their use are learned. Same
  honest bound as C220.
- Interference here is one similar task and one disjoint task; a
  graded similarity ladder (partial cell overlap) would map the
  gradient more finely.
- Retention is measured immediately after interference; delayed
  re-test after further unrelated training would test durability.
- The corruption vector is a single shared (op, ctx) cell with
  directly contradicting rewards; real interference is messier.
- Suggested ledger entry: C22x catforget, CATFORGET-COMPLETE
  (preregistered, 3/3 byte-identical): phased interference battery;
  composition links shield A under similar interference
  (FULL-SIM 100% vs SEV-SIM 0% retention); unrelated interference
  harmless in both arms (100%/100%); severed-but-present link
  (comp(1,2)=1000 recorded, not consulted) still forgets.
