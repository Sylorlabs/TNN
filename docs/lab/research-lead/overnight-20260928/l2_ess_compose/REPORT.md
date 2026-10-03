# REPORT: L2-ESS-COMPOSE (operator standing in the composition learner)

Verdict: **PASS** (all frozen kill bars hold; no falsifier fires).
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose/`
Worker: L2-ESS-COMPOSE subagent (depth 2/2), 2026-10-03.
Non-ledger task (claim minting paused).
Prereg: PREREG.md (frozen at commit a2c91db49, before implementation).
Binary: `esc_bin` (built from learner.zag + world_E.zag + driver.zag
via pinned safebin znc 2026.07.0-dev). world_E.zag reused byte-identical
from l2_compose_chain3 (sha256 9197c573...).

## 1. What was built

The chain3 [6,5,4] composition learner plus operator standing records.
Zero operator-semantic changes. Additions only:

- Cell table: 6 ops x 16 MAP ids x 32 sigs x 4B [SUC,FAIL,STRK,QTOUCH]
  at 1412+(((op-1)*16+src)*32+sig)*4. The source id is part of the key
  (composition tries one operator against several sources in a query;
  per-(op,sig) alone would let Z4 failures strike Z5's cell).
- Gate (st_standing_eval): mode 0 = immediate try (byte-identical
  trace); mode 1 = (op,src,sig) cells; mode 2 = (op,0,0) global cells.
  struck = (STRK>=3) OR (SUC*2<FAIL); probation at QTOUCH>=8.
- Context signature st_sig = em*16+nf*2+pat (ESS formula; em from a
  live (s,d_entry) fact, nf = d_nf clamped, pat = d_entry==0).
- Updates (st_standing_upd, learner-side only): after phase 1 keyed
  (s,agg_src); after each Z source keyed (s,zsrc). Commit ->
  SUC+8/STRK=0/FAIL/=2; tried-not-committed -> FAIL+4/STRK+1.
- Gating at all 12 enumeration blocks (6 phase-1 MR-OP, 6 phase-2
  MR-COP) with TRIEDMASK_P1/P2 and phase-appropriate tags.
- Driver: mr_standing_arm(st, mode) per arm only (KB-SEAL clean).

Five arms, one binary, fresh 16384B state each: UNGATED (mode 0),
STANDING (mode 1), GLOBAL (mode 2, informational) on the E-world FULL
sequence; PROB-UNG (mode 0) and PROB (mode 1) on the 12-fact probation
world (PQ1..PQ7 strike queries, recovery teach, PQR).

## 2. Kill-bar results

**KB-EFF (efficiency): PASS.** Tries QD1..QD4: UNGATED 6+11+16+24=57;
STANDING 6+6+11+10=33. STANDING < UNGATED and 57-33=24 >= 10.
Per-query: QD1 6->6 (all fresh), QD2 11->6 (phase-1 ops 1-5 skipped),
QD3 16->11, QD4 24->10. Savings concentrate where history exists.

**KB-CORR (correctness): PASS.** QA/QD1/QD2/QD3 via/val/op identical
(3/59/6, 4/63/5, 5/65/4); QD4 val=-2 op=-1 both; d_check_z4/z5/z6 = 1
both; QD1-B/QD2-B/QD3-B via/val equal (3/59, 4/63, 5/65). The [6,5,4]
chain is preserved exactly.

**KB-NOSKIP (no wrong skips): PASS.** 24 standing-skips in ARM
STANDING, every one paired with a same-query same-phase FAIL in ARM
UNGATED (QD2: 5 phase-1; QD3: 5 phase-1; QD4: 5 phase-1 + 9 phase-2).
Zero OK-withheld; F-D does not fire. The verifying operators (op 5 on
QD2/Z4, op 4 on QD3/Z5) are never skipped: their phase-2 cells are
fresh per (src,sig).

**KB-PROB (probation recovery): PASS.**
(a) PROB-UNG: PQ1..PQ7 val=-2, PQR op=2 val=62 (solver exists).
(b) PROB: PQ1..PQ7 val=-2, PQR op=2 val=62.
(c) PROB PQR trace: MR-OP-PROBATION 1 (fail), MR-OP-PROBATION 2 ->
ANS term=24 val=62 via=1 -> MR-OP-OK 2. PQ1 update shows
(op,0,20)=(0,4,1); PQ2..PQ7 all skipped (QTOUCH 2..7); PQR hits
QTOUCH=8 -> probation -> verify -> commit. The retired operator
recovers exactly when the world changes.

**KB-SEAL: PASS.** driver.zag: zero operator/form names, zero
standing offsets, zero trace tags/threshold/signature literals.

**KB-DET: PASS.** 3/3 byte-identical runs (sha256
d985a4c1f6b49cc34c1427d46659d2cb54613bf4b0727bfe399d4ff39094bdb7).

## 3. Informational: GLOBAL arm (mode 2)

Predicted: QD2 fails (op 5 over-retired). Observed: QD2 SOLVED by op 6
(val=63, op=6, tries included in sum=17) via a genuine alternative
path: CONCRETIZE on Z4 finds the mP' pattern's folds (22,23) novel
against Z4's (26,27) folds (phase-1 OLD-FOLDS became VERIFY-OK).
QD3 then fails (val=-2): op 4 is globally struck after QD1 and never
recovers; QD4 val=-2. So the context-vs-global conclusion stands
(and is stronger): per-operator retirement breaks the [6,5,4] chain
at QD3 even though the system routed around the QD2 retirement via
op 6. The (src,sig) key is load-bearing.

## 4. Falsifiers

F-D (wrong skip): not fired. F-EFF: not fired. F-PROB: not fired.

## 5. Interpretation

Operator standing transfers to the composition setting with the one
refinement the setting demands: the source id in the cell key. The
[6,5,4] chain gets 42% fewer tries (57->33) with zero solution
changes, zero wrong skips, and probation recovery on a world change.
The GLOBAL arm confirms ESS P5 (context beats global) in composition:
global retirement breaks the chain; contextual standing preserves it.

## 6. Files

- learner.zag (standing integration; base = chain3 learner)
- world_E.zag (byte-identical to chain3)
- driver.zag (5 arms; KB-SEAL clean)
- full.zag, esc_bin, run1/2/3.txt (3/3 identical)
- PREREG.md (frozen), NAMECHECK.md (Step 0)

Commits: freeze a2c91db49 (PREREG+NAMECHECK alone); implementation +
this report follow under explicit pathspecs on tnn-native-lab, never
pushed.
