# NAMECHECK.md -- L2 Substitute Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python; echo "guard-check-done"
```

Result: setup printed `SAFEBIN-READY: /home/hatch/safebin (36 tools,
no python)` and `znc: OK
(/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`.
`which python3` and `which python` with PATH=$HOME/safebin returned
NOTHING (empty output before `guard-check-done`). All subsequent
work runs with PATH=$HOME/safebin exported in every shell command.

No forbidden executable invoked at any point. Pure Zag via the
pinned znc. Shell used only for: safebin setup, file concatenation,
znc invocation, binary runs, sha256sum, read-only greps, dash-byte
checks, and git ops.

## Step 1: Task identity

L2 Substitute Worker (subagent, 2026-10-02). Mission: prove the L2
SUBSTITUTE operator within-domain (chain family). Scenario: MAP m
([1,1,1], 1->2->3->4) learned; MAP n ([2,2], 2->5->3) learned
independently before the world change, covering the same endpoints
as m's middle segment via different relations/facts; world change
kills fact 1 (the middle hop license (2,1,3)); the learner detects
the stale segment (m_exec licensing check fires at hop 1),
searches its piece inventory in node-id order, substitutes n for
the dead segment (m2 = [1] ++ [2,2] ++ [1] = [1,2,2,1], facts
[0,3,4,2], 1->2->5->3->4), verifies m2 by real execution to
terminal 4, promotes m2 with type-16 adapted-from edges to m and
n, retires stale m, writes LINK14 answer provenance and type-15
co-use edges on episode success, and answers queries through m2.
Zero new edge types, zero new opcodes, zero modes/bridges/handlers.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Frozen TNN core not
  used; standalone learner-mechanism experiment.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with
  worker_snippets/check_no_dash.sh).
- Paper untouched. Nothing pushed. Commits local only on
  tnn-native-lab. Commit messages append "Local only, never
  pushed."
- Commit order: prereg (this dir's PREREG.md) committed ALONE with
  this NAMECHECK.md before any implementation file exists.
- Compiler lessons honored: u8-backed cells with get32/set32
  only (no `as *i32` slice construction); no `_zag_print`
  anywhere (one preallocated 64KB buffer, single raw-syscall
  write loop, stdout bytes verified); no `as []f64`/`as []i64`;
  sub-conditions hoisted, if-nesting kept at 4 or fewer with all
  call results hoisted into locals before conditions (build clean,
  zero E0204);
  far under the 1024-node workspace budget (16 MAP slots,
  32 fact slots, 64 edge slots); MAP inventory taught via
  direct m_teach calls (no rebind assemblies).
- SUB_ON/ET_ON are driver-set causal-control flags (the
  composition_l2 adapt_on precedent), never written by the
  learner.

## Step 3: Development notes

1. First build reproduced the frozen hand derivation with one
   correction: FULL adapt counters came out S=8 E=3, not the
   hand-derived S=9. Root cause: the frozen first-match rule stops
   the piece search at the first MATCH, so the distractor MAP d is
   never examined in FULL (my hand count had examined it). The
   implementation follows the frozen counting rules exactly; the
   hand derivation double-counted. Recorded transparently in
   PREREG_AMENDMENT2.md (5x products 45 -> 40; the 5x ratio
   threshold itself unchanged; measured 76 and 72 clear both).
   No other deviation: SUB-STALE m=0 hop=1 fact=1; MATCH on MAP1
   (2->3, facts 3,4 live); SUB-BUILD rels=1,2,2,1 facts=0,3,4,2;
   SUB-VERIFY term=4; SUB-PROMOTE m2=3; SUB-T16 3->0 and 3->1;
   SUB-RETIRE m=0; ANS via=3 val=4; post-query ans=4 via=3 with
   m0live=0. NO-SUB: ET-TRUNC t=3 from=0, ET-EXTEND e=4 from=2,
   ET-EXTEND e=5 from=3, ans=-2, t16=3. ABLATE-N: RB-CAND
   sequence L=1 term=2,11 / L=2 term=5,13,12 / L=3 term=3,14 /
   L=4 term=4 exactly as derived; RB-BUILD m3=3 native; ADAPT
   S=76 E=10; ans=4; t16=0. ABLATE-M: stale@hop0, no candidate,
   rebuild dead-ends at 12, ans=-2, t16=0, nm=3. FRESH: RB-BUILD
   m3=0 native; ADAPT S=72 E=9; ans=4 via=0; t16=0.
2. Build: `cat learner.zag world.zag driver.zag > sub_full.zag`
   (1220 lines), then `znc sub_full.zag -o sub_bin`. Build exit 0.
   Only diagnostics: the benign zagd-unavailable notice, one
   unused-local warning (wv), and ignored-return-value notes;
   zero errors, zero E0204. Fourth-defect pattern `while.*!(`
   grep-clean; `as *i32` grep-clean.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 125 lines, 0 NUL bytes, ends with
   L2-SUBSTITUTE-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32`
   slice construction. If-nesting kept at 4 or fewer with all
   call results hoisted into locals before conditions.
5. K9 audit: all 8 frozen patterns return 0 hits on learner.zag.
   One self-inflicted near-miss fixed pre-verdict: the header
   comment said "0 bridges", tripping the case-insensitive
   `bridge` pattern; rephrased (comment only, no behavior
   change), rebuilt, re-ran 3x.
6. Amendments: AMENDMENT1 (operator firing semantics,
   pre-implementation); AMENDMENT2 (FULL A_SEARCH 9 -> 8,
   post-first-build pre-verdict, arithmetic correction only).
   No kill bar weakened; no threshold moved.

## Step 4: Determinism

- No RNG anywhere. Node-id order in every scan; first-match
  candidate rule; ascending fact-id scans; iterative deepening
  L=1..4 in the rebuild fallback.
- sub_run1/2/3.txt sha256 identical:
  198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261
  (all three). K8 PASS.
- Binary sha256:
  9f9a4cd1af7644f34441aa6c18f7d7a1875c05e841b72d20f956e16b902f91a1
