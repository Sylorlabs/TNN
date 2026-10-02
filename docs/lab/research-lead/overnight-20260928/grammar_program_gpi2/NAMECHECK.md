# NAMECHECK.md -- GPI-2 Second Constraint-Family Generality Probe Worker

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
pinned znc. Shell used only for: safebin setup, file moves,
concatenation, znc invocation, binary runs, sha256sum, read-only
greps, dash-byte checks, and git ops.

## Step 1: Task identity

GPI-2 worker (subagent, 2026-10-02). Mission: SECOND
CONSTRAINT-FAMILY GENERALITY PROBE for the GPI-1 intermediate
machinery (ledger C303; dir
docs/lab/research-lead/overnight-20260928/grammar_program_intermediate/;
prereg 5293381da; impl 9ee033542). GPI-1 proved the learner creates
a construction-plan intermediate (SEQ/PAIR/NEST vocabulary)
mediating a learned single-delimiter depth-budget constraint and an
executable MAP-chain program, then reuses and revises it; honest
verdict L2-COMPLETE, L3 not claimed, C0-C failed (single family).

GPI-2 tests whether the SAME intermediate machinery, with the node
vocabulary FROZEN, generalizes to a structurally different
constraint family: MULTI-TYPE STACK-DISCIPLINE WELL-FORMEDNESS
(three delimiter types (), [], {} where every close must match the
most recent open TYPE; no depth budget). The learner must extract
the type alphabet plus the matching rule from world probes (not
handed), build a construction plan using ONLY SEQ/PAIR/NEST,
assemble and execute a MAP-chain program, and get world
acceptance. Load-bearing question: does the fixed vocabulary plus
plan machinery handle the new family, or does it break? Both
outcomes are publishable. If it breaks, the report characterizes
EXACTLY which vocabulary piece or builder assumption fails, with a
minimal failing case; that characterization IS the result (the
invention gap the L3 track must close). The family is not contorted
to fit the vocabulary; the vocabulary is not extended to fit the
family.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Standalone
  learner-mechanism experiment; frozen TNN core not used. Work
  confined to docs/lab/research-lead/overnight-20260928/
  grammar_program_gpi2/ with explicit pathspecs.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with
  worker_snippets/check_no_dash.sh).
- Paper untouched
  (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
  never opened). Nothing pushed. Commits local only on
  tnn-native-lab. Commit messages append "Local only, never
  pushed."
- Commit order: prereg (this dir's PREREG.md) committed ALONE with
  this NAMECHECK.md before any implementation file exists.
  Self-check recorded in REPORT.md (K13).
- Compiler lessons honored: u8-backed cells with get32/set32
  only (no `as *i32` slice construction); no `_zag_print`
  anywhere (one preallocated 64KB buffer, single raw-syscall
  write loop, stdout bytes verified); no `as []f64`/`as []i64`;
  sub-conditions hoisted, if-nesting kept at 3 or fewer with all
  call results hoisted into locals before conditions;
  no `!(... && ...)` in any `while` condition (De Morgan form
  used; grep-verified on new Zag: `grep -n 'while.*!('` must
  return nothing).
- Sealed-world rule: no sealed assets are used here; the world
  side is experiment-local and fully disclosed in the prereg.
  The driver never inspects world truth except through w_check
  outcomes; kill-bar expectations reference only probe outcomes
  and learner state.
- Vocabulary freeze: SEQ/PAIR/NEST node kinds (0,1,2), node field
  layout, and node execution semantics are unchanged from GPI-1.
  Adding a node kind to make the family pass is forbidden and is
  itself a frozen bar (K11, grep audit).
