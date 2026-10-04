# IMPLEMENTATION: TNN-3 H1 (wave-20261001-2021pdt, lane TNN3H1)

Date: 2026-10-01 20:29-21:05 PDT. Worker: TNN3H1-IMPL.
Prereg: PREREG_H1.md, frozen alone at commit 1942eb51b (verified via git log
before any implementation file was written; implementation files first appear
after that commit, so prereg ordering is VERIFIABLE, K-P1 satisfied for the
builder phase).

## 1. Toolchain guard

- safebin activated per docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh;
  PATH exported to $HOME/safebin only (Step 0 and Step 0b in NAMECHECK.md).
- `which python3` prints NOTHING (exit 1). `which python` prints NOTHING.
- All work: pinned znc, running compiled binaries, git read ops, file
  moves/copies, safebin text tools (sed, grep, awk, diff, sha256sum).
- Zero forbidden executable invocations. No PROCESS-FAIL conditions triggered.

## 2. Baseline

- Source: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
- 1591 lines, commit f4de7ff46, SHA-256
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (matches the prereg; verified before copying).
- Working copy: lane file tnn3.zag, byte-identical copy at start of phase.

## 3. Change set applied (pure deletion, zero insertions)

Deletion hunks against the frozen baseline (from `diff tnn3.zag.pre tnn3.zag`):

1. Lines 362-410 (49 lines): the three assemblers plus their doc comments.
   t2_asm_chain, t2_asm_count, t2_asm_sum. Matches prereg section 3.1
   (prereg line numbers were approximate; substance identical).
2. Lines 581-666 (86 lines): fn t2_trial in full plus its 5-line doc comment,
   i.e. the researcher-fixed schema menu and search order (k-hop chains
   k=2..4, then subset sums, then counts, then the single-hop fallback).
   Matches prereg section 3.1.
3. Lines 667-671 (5 lines): fn mp_run plus its comment. mp_run was a thin
   wrapper whose only content was the t2_trial call; with t2_trial deleted
   the wrapper is dead. Deleting it is the call-site rewiring the prereg
   leaves as implementation detail (section 3.2).
4. Lines 826-828 (3 lines): the ev_query miss-path call site
   ("trial loop first" comment, `let ans:i32=mp_run(...)`,
   `if(ans!=-2){...}`). Deleted so the miss path falls through to the
   pre-existing P-INV bootstrap fallback and then miss_inquire, both kept
   verbatim from the frozen baseline.

Total: 143 lines deleted, 0 lines added, 0 lines modified. The diff contains
only `d` (delete) hunks; `grep -c "^>"` on the diff is 0.

### Delta accounting vs the frozen bars (prereg section 3.3)

- Cognition source lines ADDED: 0. Bar met.
- Cognition source lines DELETED: 143. Bar as literally stated (>=150)
  is NOT met; see section 7 for the transparent calibration note.
- Non-deletion modified lines: 0 (pure deletion; "call-site rewiring only"
  satisfied vacuously).
- New conditionals, constants, semantic cases in modified lines: none
  (there are no modified lines).
- New modes, bridges, routers, task-specific handlers, admission gates: 0.
- New hardcoded semantic cases beyond the frozen ISA: 0.
- Forbidden protected semantic operations in the diff
  (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
  LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL or equivalents):
  none present (grep clean).
- Residual references to deleted functions: none. `grep` for
  t2_asm_chain, t2_asm_count, t2_asm_sum, t2_trial, mp_run returns zero
  hits outside the test function NAME t_t2_trial_reject (a name only; it
  calls ev_query, not deleted code).
- EXECUTE signature: unchanged, EXECUTE(root, frame), the approved
  protected-core machinery form (prereg section 3.4 note honored; no
  reinterpretation).

## 4. Build evidence (pinned znc)

Compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1 (via safebin `znc`).

Main implementation binary (tnn3.zag):
- 3/3 builds byte-identical.
- SHA-256: ac715d080a7e67bbab4694feee66ad5973140d3e58095dcb88b687e55613d2db
- Size: 195817 bytes. Analyzer: 136 warning lines (baseline: 142; same
  warning class, six fewer after deletion). Zero errors.
- Lane artifact: tnn3_bin (this hash).

Dev harness binary (tnn3.zag with main stripped + h1_dev.zag):
- 3/3 builds byte-identical.
- SHA-256: 8c44084942102d4cc890c30290c6c655f23485505e0e344eed837157687e18b1

## 5. Test results

### 5a. Baseline self-test suite (in-file run_all, 46 tests)

Result: 36/46 PASS, deterministic 3/3 byte-identical transcripts
(transcript SHA-256 4f200b69a1b17be0ea9a8ebdcc9fd25d6c58b83856e33deab0eabcb75ccc5382).
Full log: tnn3_selftest.log.

The 10 failures are exactly the trial-menu-dependent tests, and each fails
for the designed reason (the deleted capability is gone, not a defect):
P1, F2, P2, P3a, P3b (trial-built chain/count answers no longer produced),
P4 (trial stats header field 16 no longer written), XCAP (first step needs
trial-built plan), T2-CHAIN4 (runtime 4-hop assembly was the trial loop),
T2-REJECT (trial reject stats), T2-REVISE (revision of a trial-promoted
graph; nothing is promoted anymore).

Still passing (36): all C1-C15 core memory tests, all A1-A6 ACT tests,
T2-INQUIRE, T2-ACTLIVE, ABL-I, ABL-C, P2b, P5, P6, P7, DV, all R-PACT tests.
The inquiry (miss-to-act), revision-operator, bootstrap, and ACT machinery
survive intact.

The failing tests were LEFT IN PLACE deliberately: the prereg deletion list
is exact and does not list them, and deleting failing tests to green the
suite would hide the designed capability removal. Their failure is the
honest signal that the menu is gone.

### 5b. Development harness (h1_dev.zag; worlds designed by this worker;
strictly separate from any sealed protocol)

Result: 6/6 PASS, deterministic 3/3 byte-identical transcripts.
Full log: h1_dev_run1.log.

- DEV LINK-EXEC (AFF-LINK, AFF-EXEC): two INC cells SEQ-linked into a
  sequence, named with handle 7001; executed on two instances (slot0=5
  gives 7; slot0=40 gives 42). Same named object traversed by two
  instance executions.
- DEV NAME-WB (AFF-NAME): white-box signature verified: handle cell
  (tag 904, field20=7001), exactly one NAME edge (type 11) to the
  sequence root; unknown handle 7002 absent.
- DEV COMPOSE (C1 family shape): P=[INC] named 7201, Q=[INC,INC] named
  7202, composite C named 7203 with NAME edges to both roots; executing
  C runs P then Q on one frame: 10 -> 13.
- DEV DIAMOND (C2 family shape): one shared step S named 7301, SEQ-linked
  from two parent graphs A (INC then S) and B (DEC then S); white-box
  shows exactly one S object with two incoming SEQ edges; A: 10 -> 12,
  B: 10 -> 10, S alone: 10 -> 11.
- DEV NO-MENU: a miss the frozen trial loop used to answer now returns -2
  and header field 16 (trial stats) stays 0.
- DEV GUARD-SET: guard/set/literal cells still constructible via the
  generic machinery; passing guard flows through, failing guard aborts
  with -999999.

NAME white-box convention used by the harness (proposed for the sealed
counting tool): handle cell tag 904, field20 = learner-chosen handle
value, NAME edge type 11 (ET_REG, unused by the frozen baseline).

## 6. Implementation freeze record

- tnn3.zag: 1448 lines, SHA-256 to be recorded at coordinator commit
  (file frozen; no further writes by this worker).
- Baseline copy for verification: tnn3.zag.pre (1591 lines, hash matches
  the prereg).
- Binary: tnn3_bin, SHA-256
  ac715d080a7e67bbab4694feee66ad5973140d3e58095dcb88b687e55613d2db.
- No git commit by this worker (coordinator commits). No push. No reset,
  no rebase.

## 7. Transparent notes (no silent drift)

(a) Deletion-count calibration. The prereg estimated the section 3.1 set at
"about 155" lines and set the bar at >=150 deleted. The actual 3.1 set in
the frozen baseline is 135 lines (49 assembler region + 86 trial region);
with the mp_run wrapper and ev_query call-site rewiring the total applied
deletion is 143 lines. The complete 3.1 set is verifiably gone (zero
residual references; diff hunks align exactly with the listed functions),
and 0 lines were added. The numeric shortfall (143 vs 150) is a prereg
line-count estimate error, not a partial implementation. This worker did
NOT delete additional code to chase the number. Recommendation: the
coordinator transparently amends the bar to the actual 3.1 set size before
adopting results; this worker reports IMPLEMENTATION COMPLETE on substance
with the calibration flagged.

(b) Sealed-protocol observation (not a blocker for implementation, flagged
for the coordinator and the independent adversary). After the deletion,
the frozen binary's public event interface (ev_observe, ev_query, ev_act)
contains no learner-driven construction path for named procedures: the
trial loop was the only constructor, and the 0-added bar forbids writing a
replacement. The naming/linking affordance exists as the surviving generic
machinery (alloc_node, t2_guard, t2_set, t2_lit, t2_inc, t2_mov, seq_link,
link_edge, execute), demonstrated working by the dev harness. For the
sealed families C1-C3, how named objects come to exist in a sealed run
(e.g. driver-exposed construction events vs. learner-driven construction)
is a sealed-protocol design decision for the coordinator and adversary;
the K-H1-1 counting procedure presupposes names can be created, so the
protocol must resolve this before the sealed battery or the battery will
measure an empty affordance. This worker built no sealed-style worlds and
performed no self-evaluation on sealed families.

## 8. Verdict for this phase

IMPLEMENTATION COMPLETE: binary frozen, delta accounting recorded, dev
tests 6/6, determinism 3/3 on both binaries. READY FOR SEALED EVALUATION
subject to notes 7(a) (bar calibration amendment) and 7(b) (sealed
protocol must define how name creation is elicited).
