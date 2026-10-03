# REPORT.md -- COMPOSE-SEALED-EVAL: sealed evaluation verdict

Date: 2026-10-03. Worker: COMPOSE-SEALED-EVAL. Lane:
`docs/lab/research-lead/overnight-20260928/compose_sealed_eval/`.
Branch: `tnn-native-lab`. Task type: NON-LEDGER (claim minting
paused).

This report executes the adversary's frozen PREREG.md
(`../compose_adversary/PREREG.md`) sections 5 (bars) and 6
(protocol). The evaluator did NOT read the adversary's
REPORT.md, the witness checker, or any builder REPORT.md.

## 1. Verdict

**7 of 18 HARD bars HOLD, 10 FAIL, 1 VOID. 0 panics.**

The sealed battery substantially falsifies the adversary's
predictions. The three mechanisms' actual behavior on sealed
worlds differs from prediction in three major ways:

1. **B (SUSPEND) fails every axis world and every
   falsification world except CYC2.** B solves only TFANIN,
   TCHAIN, and CYC2 (via WIDEN). On all other 11 problems B
   returns -999 with ASMSTEPS=255: the 256-thunk table fills
   during symbolic assembly, so the root application can never
   be interned. The predicted B failures (CHAIN7, SUBCAP) hold,
   but the predicted B passes (CHAIN5, FANOUT5, FANIN5, DAG10,
   PARTIAL, TRAP1, TRAP2) all fail for the same
   table-exhaustion reason.
2. **A (BACKCHAIN) fails SUBCAP, TRAP1, and TRAP2** (all
   -999), contrary to prediction. A solves CHAIN7, TFANIN,
   TCHAIN, and all five axis worlds.
3. **C (LEARN-COMPOSE) does not retrieve on TRAP1/TRAP2**
   (SIM=-1, MODE=0 COLD), contrary to the designed SIM=2
   misfire. C's cold-start is byte-for-byte A's behavior
   (identical TRIES on every cold problem), confirming C1.
   C DOES retrieve (SIM=2, MODE=2 REVISE) on TFANIN and
   TCHAIN.

Additionally, **CYC3 does not discriminate 3-hop traversal**:
all three mechanisms return 502, the 1-hop value, because the
world's 2-cycle (502<->503) makes the 3-hop value equal the
1-hop value. K-ADV-D2 fails for all three.

## 2. Execution record

- Protocol: adversary PREREG section 6, executed verbatim.
  EVAL_EXEC.md (this lane) was committed before any sealed
  execution.
- Concat (copies, verified byte-identical to lane originals):
  A = bc_base+bc_thunk+bc_search+adv_worlds+eval_main_a;
  B = sus_base+sus_thunk+sus_asm+sus_rev+adv_worlds+eval_main_b;
  C = lc_base+lc_thunk+lc_search+lc_mem+lc_rev+lc_rep+
      adv_worlds+eval_main_c.
  (lc_rep included per section 6's explicit note; it defines
  do_prob and no main. All concats have exactly one main.)
- Toolchain: safebin znc, byte-identical (cmp) to the pinned
  builder binary
  $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1.
  `which python3` / `which python` return nothing in safebin
  PATH. Pure Zag throughout.
- Process grouping: per section 6 via the adversary's frozen
  templates. Verified no `global` state in any mechanism
  source; `z_alloc` is `_zag_malloc` (independent malloc per
  arena); A/S reallocated fresh per problem; C's M persists
  across SEQ1 (TEACH->TRAP1->TRAP2) and SEQ2
  (TEACH-D->T-FANIN->T-CHAIN), fresh elsewhere. MEM field
  confirms: SEQ1 MEM stays 1 across all three problems; SEQ2
  MEM stays 1; fresh-M problems show MEM=0 on failure.
- Determinism: each binary run 3 times. **3/3 byte-identical
  stdout on all three binaries (cmp).** Empty stderr on all 9
  runs. All 9 runs exit 0. No panics.
- Sealed worlds and mechanism sources were not modified.

## 3. Raw results (run1; runs 2,3 byte-identical)

### A (BACKCHAIN)

| PROB | ANS | TRIES | WIDEN | ANSMATCH |
|------|-----|-------|-------|----------|
| CHAIN15 | -999 | 18 | 1 | PASS |
| CHAIN7 | 4 | 36 | 0 | PASS |
| SUBCAP | -999 | 34 | 1 | FAIL |
| TRAP1 | -999 | 201 | 1 | FAIL |
| TRAP2 | -999 | 29 | 1 | FAIL |
| TFANIN | 5 | 4 | 0 | PASS |
| TCHAIN | 3 | 5 | 0 | PASS |
| CYC2 | -999 | 1 | 1 | PASS |
| CYC3 | 502 | 1 | 0 | FAIL |
| CHAIN5 | 6 | 21 | 0 | PASS |
| FANOUT5 | 10 | 45 | 0 | PASS |
| FANIN5 | 12 | 101 | 0 | PASS |
| DAG10 | 10 | 46 | 0 | PASS |
| PARTIAL | 10 | 59 | 0 | PASS |

### B (SUSPEND)

| PROB | ANS | ASMSTEPS | WIDEN | ANSMATCH |
|------|-----|----------|-------|----------|
| CHAIN15 | -999 | 255 | 1 | PASS |
| CHAIN7 | -999 | 255 | 1 | PASS |
| SUBCAP | -999 | 255 | 1 | PASS |
| TRAP1 | -999 | 255 | 1 | FAIL |
| TRAP2 | -999 | 255 | 1 | FAIL |
| TFANIN | 5 | 6 | 0 | PASS |
| TCHAIN | 3 | 5 | 0 | PASS |
| CYC2 | 503 | 1 | 1 | PASS |
| CYC3 | 502 | 1 | 0 | FAIL |
| CHAIN5 | -999 | 255 | 1 | FAIL |
| FANOUT5 | -999 | 255 | 1 | FAIL |
| FANIN5 | -999 | 255 | 1 | FAIL |
| DAG10 | -999 | 255 | 1 | FAIL |
| PARTIAL | -999 | 255 | 1 | FAIL |

(B also reports SEARCHRUNS=1, VIOL=0 on all problems;
EXECTOT=1 except TFANIN=4, TCHAIN=5, FANOUT5=255, DAG10=255.)

### C (LEARN-COMPOSE)

| PROB | ANS | TRIES | WIDEN | MODE | SIM | NEGREC | MEM | ANSMATCH |
|------|-----|-------|-------|------|-----|--------|-----|----------|
| TEACH | 3 | 3 | 0 | 0 | -1 | 0 | 1 | PASS |
| TRAP1 | -2 | 201 | 1 | 0 | -1 | 0 | 1 | FAIL |
| TRAP2 | -2 | 29 | 1 | 0 | -1 | 0 | 1 | FAIL |
| TEACHD | 5 | 7 | 0 | 0 | -1 | 0 | 1 | PASS |
| TFANIN | 5 | 3 | 0 | 2 | 2 | 0 | 1 | PASS |
| TCHAIN | 3 | 2 | 0 | 2 | 2 | 0 | 1 | PASS |
| CHAIN15 | -2 | 18 | 1 | 0 | -1 | 0 | 0 | PASS |
| CHAIN7 | 4 | 36 | 0 | 0 | -1 | 0 | 1 | PASS |
| SUBCAP | -2 | 34 | 1 | 0 | -1 | 0 | 0 | FAIL |
| CYC2 | -2 | 1 | 1 | 0 | -1 | 0 | 0 | PASS |
| CYC3 | 502 | 1 | 1 | 0 | -1 | 0 | 1 | FAIL |
| CHAIN5 | 6 | 21 | 0 | 0 | -1 | 0 | 1 | PASS |
| FANOUT5 | 10 | 45 | 0 | 0 | -1 | 0 | 1 | PASS |
| FANIN5 | 12 | 101 | 0 | 0 | -1 | 0 | 1 | PASS |
| DAG10 | 10 | 46 | 0 | 0 | -1 | 0 | 1 | PASS |
| PARTIAL | 10 | 59 | 0 | 0 | -1 | 0 | 1 | PASS |

(MODE: 0=COLD, 2=REVISE. SIM=-1 means retrieve() found no
entry with sim>=2; lc_cold ran.)

## 4. Bar-by-bar adjudication (PREREG section 5)

HARD bars. ANS=-999 (A/B) and ANS=-2 (C) both count as
FAIL-to-solve per the prereg.

- K-ADV-A1 (CHAIN15: A!=4, B!=4, C!=4): A=-999, B=-999,
  C=-2. **HOLD.**
- K-ADV-B1 (CHAIN7: A=4, B!=4, C=4): A=4, B=-999, C=4.
  **HOLD.**
- K-ADV-B2 (SUBCAP: A=4, B!=4, C=4): A=-999, B=-999, C=-2.
  **FAIL** (A and C do not solve; B!=4 holds).
- K-ADV-C1 (TRAP1: A=5, B=5, C=5): A=-999, B=-999, C=-2.
  **FAIL** (none solve).
- K-ADV-C2 (TRAP2: A=5, C=5): A=-999, C=-2. **FAIL.**
- K-ADV-T1 (T-FANIN: A=5, B=5, C=5): 5, 5, 5. **HOLD.**
- K-ADV-T2 (T-CHAIN: A=3, B=3, C=3): 3, 3, 3. **HOLD.**
- K-ADV-D1 (CYC2: A!=503, B=503, C!=503): A=-999, B=503,
  C=-2. **HOLD.**
- K-ADV-D2 (CYC3: A!=502, B!=502, C!=502): A=502, B=502,
  C=502. **FAIL** (all return the 1-hop value; see section 5).
- K-ADV-X1 (CHAIN5 =6): A=6, B=-999, C=6. **FAIL** (B).
- K-ADV-X2 (FANOUT5 =10): A=10, B=-999, C=10. **FAIL** (B).
- K-ADV-X3 (FANIN5 =12): A=12, B=-999, C=12. **FAIL** (B).
- K-ADV-X4 (DAG10 =10): A=10, B=-999, C=10. **FAIL** (B).
- K-ADV-X5 (PARTIAL =10): A=10, B=-999, C=10. **FAIL** (B).
- K-ADV-M1 (TRAP1: C_SIM=2, C_MODE=2): SIM=-1, MODE=0.
  **FAIL** (retrieval did not fire).
- K-ADV-M2 (CYC2: B_WIDEN=1): WIDEN=1. **HOLD.**
- K-ADV-M3 (TFANIN+TCHAIN: C_SIM=2, C_MODE=2): TFANIN
  SIM=2/MODE=2, TCHAIN SIM=2/MODE=2. **HOLD.**
- K-ADV-E1 (TRAP1: C_TRIES > A_TRIES): **VOID** per the
  prereg void rule (K-ADV-M1 failed; the structural guarantee
  assumed the misfire path, which did not occur).

SOFT bars:

- S-ADV-E2 (TRAP2: C_TRIES < A_TRIES): C=29, A=29. Not met
  (equal, not strictly less). Informative only.
- S-ADV-E3 (TRIES recorded): met; full table in section 3.

**Tally: 7 HOLD, 10 FAIL, 1 VOID, 0 panics.**

## 5. Observations (evidence-grounded)

1. **B's thunk table is the binding constraint, and it binds
   far earlier than the adversary's B2 analysis.** On all 11
   B failures, ASMSTEPS=255: the 256-entry thunk table fills
   during phase-0 symbolic assembly. The assembly enumerates
   WALK-chain permutations (depth-first, producer-id order)
   and interns each; once the table is full, the root COUNT
   application cannot be interned (th_new returns -2), so no
   candidate can match exp and WIDEN cannot synthesize the
   missing root. This defeats B even on CHAIN5 (5 links,
   within B's stated 6-link depth bound) and on all fan-out /
   fan-in / DAG / partial worlds. B's only sealed solves are
   the 3-map TFANIN/TCHAIN (table never fills) and CYC2 via
   the one-shot WIDEN (B5), which does not enforce the loop
   guard. The builders' BUILD-PASS battery evidently never
   presented B with an inventory large enough to saturate the
   table during assembly.
2. **A fails the three distractor-heavy 3-structure worlds.**
   SUBCAP, TRAP1, TRAP2 all return -999 after WIDEN fires.
   (A's WIDEN is one-shot kind-relaxation; it does not
   recover these.) A solves all five axis worlds and CHAIN7.
3. **C never retrieves on SEQ1.** TRAP1 and TRAP2 run
   MODE=0 COLD with SIM=-1: retrieve() found no memory entry
   with sim>=2 despite TEACH storing one (MEM=1 persists
   across SEQ1). Consequently C's TRIES are identical to A's
   on every cold problem (CHAIN15: 18/18, CHAIN7: 36/36,
   SUBCAP: 34/34, TRAP1: 201/201, TRAP2: 29/29, CYC2: 1/1,
   CYC3: 1/1, CHAIN5: 21/21, FANOUT5: 45/45, FANIN5: 101/101,
   DAG10: 46/46, PARTIAL: 59/59), confirming C1 (cold-start
   IS A's solve verbatim). On SEQ2, retrieval works as
   designed: TFANIN and TCHAIN both retrieve at SIM=2 and run
   MODE=2 REVISE, solving with TRIES 3 and 2 (vs A's 4 and 5).
4. **CYC3 cannot test 3-hop traversal.** The world's facts
   (501->502->503->502) form a 2-cycle, so the 3-hop value
   (502) equals the 1-hop value. All three mechanisms return
   502 with TRIES=1 via the single Wc application. K-ADV-D2
   is unmeasurable on this world, not merely failed.
5. **No mechanism returns a wrong answer on any world.**
   Every ANS is either exp or a fail sentinel (-999/-2). The
   CYC3 502s are correct answers to the query as posed.

## 6. Blindness and integrity

- The evaluator read the adversary PREREG.md (required: bars
  in section 5, protocol in section 6). The evaluator did NOT
  read `../compose_adversary/REPORT.md`, `adv_witness.zag`,
  `adv_wit_bin`, `adv_wit_full.zag`, `adv_wit_compile.txt`,
  `adv_wit_run1.txt`, or any builder REPORT.md.
- Sealed worlds and frozen mechanism sources were copied,
  never modified (all copies verified byte-identical via
  cmp/sha256).
- Execution was mechanical: concat, compile, run 3x, cmp,
  report fields, check bars.
- Toolchain incident (self-disclosed): during diagnostic
  setup the evaluator typed a `python3 -c` probe; it failed
  with "command not found" (python3 does not resolve in
  safebin PATH; verified via `which`). No Python process
  ever executed; the file transformation was performed by
  `awk`. The sealed evaluation itself used only safebin tools
  (znc, sh, awk, cmp, etc.). The diagnostic binary was killed
  and its outputs deleted; it did not contribute to results.

## 7. Files (this lane)

- `EVAL_EXEC.md`: pre-execution protocol record (frozen).
- `eval/`: copied frozen sources, concats
  (`eval_a.zag`, `eval_b.zag`, `eval_c.zag`), binaries,
  `sources.sha256`, compile logs.
- `runs/`: all 9 run outputs (`{a,b,c}_run{1,2,3}.txt`),
  empty `.err` files, `score.sh`.
- `REPORT.md`: this file.

## 8. Recommended follow-ups (for the parent)

- B's assembly table-exhaustion is a general architectural
  finding (candidate enumeration saturates a fixed 256-entry
  table before the root is built), not a world-specific
  quirk. It falsifies B's claimed 6-link chain capacity on
  any inventory with >=5 permutable producers.
- C's SEQ1 non-retrieval vs SEQ2 retrieval is a precise
  boundary worth root-causing (the stored TEACH entry was
  not retrieved at sim>=2 on TRAP1).
- CYC3 needs a redesigned world (e.g., a 3-cycle or a
  3-hop value distinct from all shorter-hop values) before
  K-ADV-D2 can be measured.
- A/B/C on SUBCAP/TRAP1/TRAP2 merit builder-side
  root-cause analysis; the sealed eval's job stops at the
  verdict above.
