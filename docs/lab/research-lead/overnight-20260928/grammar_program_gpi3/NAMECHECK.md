# NAMECHECK.md -- GPI-3 Conjunctive Constraint-Family Generality Probe Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Result: safebin populated with the allowed tools. `which python3`
and `which python` with PATH=$HOME/safebin returned NOTHING
(empty output, exit 1 for both). All subsequent work runs with
PATH=$HOME/safebin exported in every shell command.

NOTE: the pinned compiler required by the task is
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`. `which znc`
resolved to a PATH-installed znc (2026.07.0-dev); the build
uses the pinned binary path explicitly, never the safebin
symlink.

No forbidden executable invoked at any point. Pure Zag via the
pinned znc. Shell used only for: safebin setup, file moves,
concatenation, znc invocation, binary runs, sha256sum, read-only
greps, dash-byte checks, and git ops.

## Step 1: Task identity

GPI-3 worker (subagent, 2026-10-02). Mission: THIRD GENERALITY
PROBE for the GPI-1 intermediate machinery (GPI-1 ledger C303,
dir
docs/lab/research-lead/overnight-20260928/grammar_program_intermediate/;
GPI-2 ledger C311, dir
docs/lab/research-lead/overnight-20260928/grammar_program_gpi2/).
GPI-1 proved the learner creates a construction-plan
intermediate (SEQ/PAIR/NEST vocabulary) mediating a learned
single-delimiter depth-budget constraint and an executable
MAP-chain program, then reuses and revises it (L2-COMPLETE).
GPI-2 proved the SAME machinery, vocabulary frozen,
generalizes to multi-type stack-discipline well-formedness with
no depth budget (L2-COMPLETE, GENERALIZES, C0-C partial).

GPI-3 tests whether generality COMPOSES: the CONJUNCTIVE family
(multi-type stack discipline AND depth budget simultaneously).
The learner must extract BOTH dimensions from one probe campaign
(type alphabet plus matching rule AND scalar depth bound, depth
probes built from the LEARNED type bindings), build one plan
whose per-node bindings carry the type dimension while the
restored assembler-side check enforces the budget dimension,
assemble, execute, and obtain world acceptance. Then: reuse the
core on a second target, revise under a budget-dimension world
change (Dmax 3->2; the old program is now REJECTED by the new
world, sharper than GPI-1), show the no-plan direct path fails,
show a fresh learner fails, and show wrong constraints refused
on EACH dimension separately. Load-bearing question: does the
fixed vocabulary plus plan machinery handle the conjunction,
or does it break? Both outcomes are publishable. If it breaks,
the report characterizes EXACTLY which enforcement piece or
builder assumption fails, with a minimal failing case.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. Standalone
  learner-mechanism experiment; frozen TNN core not used. Work
  confined to docs/lab/research-lead/overnight-20260928/
  grammar_program_gpi3/ with explicit pathspecs, on branch
  tnn-native-lab.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with
  check_no_dash.sh).
- Paper untouched (TNN_RESEARCH_PAPER_20260929.md never
  opened). Nothing pushed. Commits local only on
  tnn-native-lab. Commit messages append "Local only, never
  pushed."
- Commit order: prereg (this dir's PREREG.md) committed ALONE
  with this NAMECHECK.md before any implementation file exists.
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
- Vocabulary freeze: SEQ/PAIR/NEST node kinds (0,1,2), node
  field layout, region offsets, and node execution semantics
  are unchanged from GPI-1/GPI-2. Adding a node kind to make
  the family pass is forbidden and is itself a frozen bar
  (K12, grep audit). The restored assembler depth check and
  the fact-store compaction are disclosed non-vocabulary
  machinery (Section 5 of the prereg), not node semantics.
