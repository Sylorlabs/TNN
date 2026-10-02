# NAMECHECK.md -- Grammar-Program-Intermediate Worker

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

Grammar-Program-Intermediate Worker (subagent, 2026-10-02). Mission:
grammar constraints to program construction REQUIRING A NEW
INTERMEDIATE REPRESENTATION (L2/L3 boundary probe, on Micah's
high-value list, not yet done). Prior H1/H2 grammar to construction
work proved exact reuse; it is NOT redone here. This experiment:
X = a learned grammar constraint structure (balanced delimiters,
max nesting depth D, extracted by the learner from world probes,
not handed by the researcher). Target: construct an executable
MAP-chain program satisfying the constraint where no existing MAP
encodes a construction plan. The learner must CREATE an intermediate
construction plan (ordered decomposition with per-part depth budgets
propagated from the constraint), USE it to assemble the program,
EXECUTE the program, and have the world accept or reject it. The
intermediate must then be REUSED on a second target and REVISED
after a constraint change (D 3 to 4), with white-box traces of
creation, reuse, and revision. Honest L2 vs L3 assessment against
Micah's invention criteria; no finite operator menu widened.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Standalone
  learner-mechanism experiment; frozen TNN core not used.
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
  sub-conditions hoisted, if-nesting kept at 3 or fewer with all
  call results hoisted into locals before conditions;
  no `!(... && ...)` in any `while` condition (De Morgan form
  used; grep-verified on new Zag).
- Sealed-world rule: no sealed assets are used here; the world
  side is experiment-local and fully disclosed in the prereg.
