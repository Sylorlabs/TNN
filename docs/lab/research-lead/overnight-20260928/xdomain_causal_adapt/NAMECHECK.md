# NAMECHECK.md -- XDOMAIN-CAUSAL-ADAPT Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python
```

Result: setup printed `SAFEBIN-READY: /home/hatch/safebin (36 tools,
no python)` and `znc: OK
(/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`.
`which python3` and `which python` with PATH=$HOME/safebin returned
NOTHING (exit 1, empty output). All subsequent work runs with
`export PATH="$HOME/safebin"` in every shell command.

No forbidden executable invoked at any point. Pure Zag via the
pinned znc. Shell used only for: safebin setup, file writes/moves,
concatenation, znc invocation, binary runs, sha256sum, and git ops.

Worker branch note: the task named branch `tnn-native-lab`; that
branch is checked out by the shared worktree at
`/home/hatch/workspace/tnn-rsi-gpi3` (recent WATCHDOG ledger commits
C356/C357 present). All lane work happens in that worktree, commits
use explicit pathspec limited to this lane directory, nothing is
pushed.

## Step 1: Task identity

Cross-Domain Adaptive Composition worker (subagent, 2026-10-02).
Mission: causal model -> intervention with REQUIRED adaptation.
A causal model X learned in a source context (variables a,b,c, full
observability) must be ADAPTED (not copied) to select an intervention
in a target context with different variable names (p,q,r,d,s),
different arity (5 observed + 1 hidden vs 3), and partial
observability (hidden mediator h). Direct literal reuse must fail
(K2); adaptation must produce the optimal intervention (K3) and beat
both direct copy and learning from scratch (K4).

## Step 2: Toolchain verification

- `znc` resolves via safebin to the pinned Linux binary; `znc --help`
  runs before first compile to confirm CLI.
- No python3/python in PATH (Step 0). All scientific computation in
  Zag (.zag sources compiled by znc to a native binary).
- Determinism: no RNG anywhere in the experiment; fixed probe values;
  explicit enumeration of presentation orders. 3/3 byte-identical
  runs verified by sha256sum.

## Step 3: Known znc defect workarounds applied

Per AGENTS.md toolchain lessons: (1) no `as *i32` + slice
construction inside functions: all i32 state lives in []u8 cells via
get32/set32 little-endian helpers; (2) no `_zag_print` for dynamic
content: single preallocated output buffer with cursor-returning emit
helpers, one `_zag_raw_syscall(1,1,ptr,len)` write at end; (3) no
7-deep nested ifs with !=/<= + call: conditions kept flat, flags
hoisted, nesting <= 3; (4) no `!(A && B)` in while conditions:
De Morgan rewrites; (5) no `.len` trust on cast slices: no f64/i64
slice casts used at all. Every binary's stdout bytes verified before
trusting it.
