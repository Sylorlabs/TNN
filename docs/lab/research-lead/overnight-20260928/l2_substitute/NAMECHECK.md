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
  sub-conditions hoisted, if-nesting kept at 3 or fewer;
  far under the 1024-node workspace budget (16 MAP slots,
  32 fact slots, 64 edge slots); MAP inventory taught via
  direct m_teach calls (no rebind assemblies).
- SUB_ON/ET_ON are driver-set causal-control flags (the
  composition_l2 adapt_on precedent), never written by the
  learner.

## Step 3: Development notes

(To be filled after the build: first-build fidelity to the frozen
hand derivation, build invocation, stdout verification, audit
results.)

## Step 4: Determinism

- No RNG anywhere. Node-id order in every scan; first-match
  candidate rule; ascending fact-id scans; iterative deepening
  L=1..4 in the rebuild fallback.
- sub_run1/2/3.txt sha256 digests recorded here after the runs.
