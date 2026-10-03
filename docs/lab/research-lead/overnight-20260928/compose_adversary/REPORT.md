# COMPOSE-ADVERSARY: Sealed World Design Report

Date: 2026-10-03. Worker: COMPOSE-ADVERSARY (non-ledger task).
Lane: `docs/lab/research-lead/overnight-20260928/compose_adversary/`

## What this lane is

Sealed worlds testing the three composition hypotheses against the
"complementary, not ranked" verdict from the A vs B vs C comparison:

- **A (COMPOSE-BACKCHAIN-1):** lazy chronological backtracking, interleaved execution. Memoryless.
- **B (COMPOSE-SUSPEND-1):** SUSPEND (ASSEMBLE/EVALUATE/WIDEN/REBIND/REVISE). Efficient on fan-in.
- **C (COMPOSE-LEARNCOMPOSE-1):** A's substrate + 16-entry composition memory; retrieve by similarity; injective contract matching; frozen revision ops (R1 SUBST_FAILED, R2 TRUNCATE, R3 SUBST, R4 APPEND); succ/fail + NEGREC. Only mechanism with a learning curve and cross-shape transfer.

I design worlds only. I do not modify builders' frozen code, and I have not
executed any mechanism on the sealed worlds. First mechanism execution on
these worlds happens in the parent's independent sealed evaluation.

## Governance

1. **Prereg before implementation.** PREREG.md (kill bars, predictions,
   protocol) was committed as `57e2492b5` before any `.zag` world code existed.
2. **Pure Zag, safebin mandatory.** All computation in this lane is Zag
   compiled with the pinned znc under `PATH=$HOME/safebin`. One toolchain
   incident is disclosed in NAMECHECK.md (a stray `python3` token in a shell
   command; it did not resolve under safebin, executed nothing, and touched
   no artifact; all research logic remains pure Zag).
3. **Sealing.** Builders never saw these worlds. Worlds were validated only
   by an independent witness checker (pure-Zag substrate reimplementation,
   no mechanism code). No bar was tuned to mechanism output. The worlds are
   transcribed exactly from the frozen prereg; a witness FAIL would have
   meant fixing the transcription, never retuning a prediction.

## The 14 world families

All worlds use opaque kinds 1/2, stay within the 64-fact store and map
ids 0..15, and carry a witness program in PREREG Section 4 whose value
defines the expected answer.

**Falsify A: F-A1 CHAIN15 (w_adv_chain15).** A 15-link chain. A's frames
grow as the sum of partial permutations of 15 (the CHAIN10 datapoint was
986,410 frames for 9 links); the 1.2M occ arena exhausts, and `occ_new`
returning -1 is misread as "producer exhausted", killing the search. This
is resource explosion *within* A's depth bound, not a depth-cap artifact.
Prediction: all three FAIL (A explodes; B's depth<6 caps chains at 6;
C's cold-start inherits A's search). If A survives this, its frame growth
is better than the white-box model predicts and the kill bar K-ADV-A1
would need re-examination.

**Falsify B: F-B1 CHAIN7 (w_adv_chain7).** A 7-link chain. B's `alts`
expands sub-needs only when `depth<6`, so the longest chain B can build is
6 links; no WIDEN application bridges the 7th. Prediction: A PASS, C PASS,
B FAIL (B's first predicted failure on a pure chain, its home territory).

**Falsify B: F-B2 SUBCAP (w_adv_subcap).** Root COUNT over C1(W3(W2(s))),
plus 11 decoy WALKs where only W2 feeds W3. Traced through B's `alts`:
the depth-1 sub-need buffer (cap 128) fills entirely with W1-rooted chains
during the first producer's turn, so the W3-rooted correct program is never
interned and never proposed to REBIND. This is a *capacity* falsification,
not a depth one: B has the right MAPs and the right depth, but its fixed
assembly buffer starves the correct composition. Prediction: A PASS,
C PASS, B FAIL. If B passes, the trace is wrong about buffer fill order
and the white-box model needs revision.

**Falsify C: F-C1 TRAP1 (w_adv_teach -> w_adv_trap1).** The retrieval
misfire trap. TEACH stores a 2-chain [X,Y] as memory E1. TRAP1's 16-map
inventory has a code multiset that is a superset of E1's, so similarity
fires at sim 2 (not sim 3: the WALK codes differ, so per-map equality
fails on the WALK slot). The adapted [X,Y] executes to -2; R1 tries 11
WALK + 3 COUNT substitutes (all fail); R4 appends one MAP at the frontier
(root end), which cannot help because the missing piece is a *prefix*;
cold-start then duplicates A's full search. By construction, C_TRIES =
misfire tries (>0) + A_TRIES, so **C_TRIES > A_TRIES strictly** (hard
efficiency bar K-ADV-E1, void if M1 fails). Prediction: all three solve
with ANS=5, C with SIM=2 and MODE=REVISE. This is C's predicted failure
mode made structural: C can never be *wrong* where A succeeds (it verifies
before counting), so its failure is pure wasted work, and here the waste
is guaranteed by the mechanism's own revision-operator geometry (no
prepend/insert exists). If C_TRIES <= A_TRIES, something in the misfire
accounting is misunderstood.

**Dominance worlds (one mechanism clearly wins):**

- **D-B1 CYCLE-2HOP (w_adv_cycle, query 2-hop).** Two hops through one
  WALK on a cyclic relation. A's and C's (need,producer) pair guard blocks
  MAP reuse, but B's `widen_pass` skips the loop guard, so WIDEN bridges
  the cycle. Prediction: B uniquely PASSes (WIDEN=1, bar K-ADV-M2), A and
  C FAIL. An emergent B capability its builders did not design for.
- **D-C1 TRANSFER (w_adv_teachd -> w_adv_tfanin -> w_adv_tchain).**
  A diamond memory transfers to a 2-leg fan-in (DROP_UNMAPPED rewires the
  unmapped X legs to CONST) and to a 2-chain (unmapped G dropped, last
  instruction Wp wins). Prediction: C solves both with SIM=2,
  MODE=REVISE (bar K-ADV-M3); A and B solve from scratch. C's dominance
  is *efficiency of reuse*, not unique solvability.
- **D-C2 TRAP2 (w_adv_teach -> w_adv_trap2).** Same inventory shape as
  TRAP1, but the correct program [W1,X,Y] is one substitution from the
  stored [Z,X,Y]: R1's SUBST_FAILED (Z->W1) repairs it. Prediction: C
  solves with C_TRIES < A_TRIES (soft bar S-ADV-E2). TRAP1/TRAP2 together
  map C's revision boundary: 1-edit misfires are repaired, 2-edit
  (missing-prefix) misfires are not.

**Shared failure: S-ALL1 CYCLE-3HOP (w_adv_cycle, query 3-hop).** Three
hops; B's one-step widen cannot bridge two reuses, A/C's pair guard blocks
all reuse. Prediction: all three FAIL. No iterate-with-halt exists in any
mechanism, so this is a genuine capability gap, not a tuning artifact.

**Axis coverage (all predicted PASS for all three):** X-CHAIN5, X-FANOUT5
(5 consumers + 4-ADD2 tree), X-FANIN5 (5 legs, 2/3/1/4/2 facts), X-DAG10
(2-chain into shared X into two diamonds into ADD2; B's max depth 5,
verified), X-PARTIAL (5-leg fan-in, 2 legs factless; answer = sum of the
3 live legs = 10; tests partial applicability, not all-or-nothing).

## On the "complementary, not ranked" verdict

The sealed set was designed to stress this verdict from both sides:

- **For complementarity:** D-B1 (only B solves), D-C1 (only C transfers),
  F-B1/F-B2 (B fails where A/C pass), F-C1 (C wastes tries where A/B do
  not). Each mechanism has a region where it is strictly the best or
  strictly the worst.
- **Against complementarity:** S-ALL1 is the world where all three fail
  identically, and F-A1 is the world where all three fail for *different*
  structural reasons. If the sealed results show one mechanism passing
  everything while another fails its home territory, the verdict needs
  revision.

The honest outcome this design is hunting for is not "C wins" but the
shape of the boundary: exactly which structural features (chain length,
buffer pressure, retrieval similarity, cycles) flip each mechanism.

## Files

- `PREREG.md` -- frozen preregistration (kill bars, predictions, protocol).
- `NAMECHECK.md` -- toolchain guard record + incident disclosure.
- `adv_worlds.zag` -- the 16 sealed world builders (`w_adv_*`).
- `adv_sub.zag` -- independent witness substrate (no mechanism code).
- `adv_witness.zag` -- per-world witness checks against PREREG exp values.
- `adv_wit_full.zag`, `adv_wit_bin`, `adv_wit_compile.txt`,
  `adv_wit_run1.txt` -- witness build artifacts; 16/16 PASS, 0 failures.
- `eval_templates/eval_main_a.zag`, `eval_main_b.zag`,
  `eval_main_c.zag` -- sealed-evaluation mains for the parent. Concat
  orders and process grouping are in PREREG Section 6; all three
  templates were syntax-verified by compiling against the frozen
  mechanism sources (compile only; the resulting binaries were not run
  and were deleted).

## Open questions for the evaluator

1. TRAP1's C_TRIES > A_TRIES bar is structural, but its *magnitude* is
   not predicted; a very large ratio would suggest the misfire path is
   worse than the white-box trace implies.
2. SUBCAP's predicted B failure depends on sub-buffer fill order; if B
   passes, the interesting result is *why* (which the trace got wrong).
3. CYCLE-2HOP is B's only predicted unique win; if B fails it, the
   widen_pass loop-guard reading is wrong, which also affects B's
   Q1b-style rebind results.
4. CHAIN15 runtime for A: the occ arena fill is bounded (1.2M frames),
   but wall-clock was not modeled; the evaluator should record it.
