# GREEDY Integration Verification Result

Status: VERIFY-COMMITTED. Independent re-verification of the greedy K=2
plateau lookahead against the frozen bridge battery. No new mechanism
work at this commit.

Ancestry:
- Mechanism under test: `greedy_impl/greedy.zag` (commit `e96b998c7`,
  verdict GREEDY-PASS). Sources copied byte-identical into this
  directory (sha256 verified before build).
- Parent frozen battery: `bridge_fix_impl/` (commit `d920af162`,
  verdict FIX-BUILT-PASS). Raw parent run: `FIX_RUN1.txt`.
- T-ADV5 sealed protocol: `tadv5_reeval/` (commit `83c02efff`),
  verdict TADV5-ACCEPTABLE. Builder T-ADV5 run:
  `greedy_impl/GREEDY_TADV5_RUN1.txt`.

Scope: `docs/lab/research-lead/overnight-20260928/greedy_verify/`
only. Commits local. Nothing pushed.

## Step 0: standing-rules name-check

1. PURE ZAG ONLY. Applies. Every stage used shell, `znc`, `grep`,
   `diff`, `sha256sum`/`md5sum`, `awk`, `sed`, `wc` only. Zero Python
   at every stage including authoring, byte checks, and verification.
2. IMAGE JUDGE. Not relevant; no image work.
3. FORK TESTING. Applies. The greedy-fixed source is a fork of the
   frozen bridge learner; the frozen battery was run against this
   fork, and the per-fork verdict is reported below.
4. PURE-ZAG SCOPE. No fixture provisioning in this task.
5. SHELL-ONLY BYTE CHECKS. Applies. Dash checks used
   `worker_snippets/check_no_dash.sh` only.

## 1. K1: battery run complete - PASS

`greedy.zag` and `greedy_tadv5.zag` copied byte-identical from the
committed `e96b998c7` files (sha256 match, verified before build).
Built with the repo `znc` only:

- `greedy.zag` -> `greedy_verify_bin`: clean (zagd notice only).
- `greedy_tadv5.zag` -> `greedy_tadv5_verify_bin`: clean (zagd notice
  only).

Three frozen-battery runs: exit 0, zero stderr bytes, 3/3
byte-identical (md5 `ff0baa2475d812df1884535aee52de5c`). Three T-ADV5
runs: exit 0, zero stderr, 3/3 byte-identical (md5
`a729858a1999ff8817915423d797bb6c`).

## 2. K2: regression status determined - PASS (no regression)

### Battery reproduction

My verification runs are byte-identical to the builder's committed
runs (`diff VERIFY_RUN1.txt GREEDY_RUN1.txt`: zero differences; same
for T-ADV5). Independent re-execution reproduces the reported
evidence exactly.

### Move-trace identity against the frozen parent

`grep BRIDGE MOVE` md5 of my run matches the frozen parent
`bridge_fix_impl/FIX_RUN1.txt` exactly (`0d1eea4dbf887d3bd55a493a39853ac6`
both). Zero search decisions changed on the frozen battery.

### Verdict and family table

- `K2 1`, `VERDICT BRIDGE-TESTED`.
- Fresh families: G cost=62, H cost=94, K cost=68, J HONESTFAIL
  (cost=820), T-ADV4 cost=72. All invention-family costs within
  frozen bars (<= 108; G2 <= 30).
- Retained menu costs exact: A=20, B=11, C=8, D=6, E=5.
- `plateau=1` occurs 0 times on the battery: the lookahead never
  diverted a frozen-battery decision. Cost deltas are pure
  simulation overhead, as the builder's Amendment A1 anticipated.

### T-ADV5 STRONG PASS confirmed

- `GREEDY it=0 g1=1 nz=2 unlocked=10 plateau=1` (zero-gain LT@13010
  applied over the +1 EQ trap move), then `g1=10` LT@13020, then
  terminate.
- adopted=3, inv_promoted=1, cost=106 <= 108, nc=7 <= 8, eqnodes=0
  <= 4, `INV FIT exact=1`, heldout wrong=0.
- The trap flipped exactly as designed: EQ,EQ,HONESTFAIL became
  LT,LT,exact-fit. Cost headroom 2, as disclosed.

## 3. K3: purity, determinism, M1-M4 - PASS

- K4 pure-Zag: shell, `znc`, `grep`, `diff`, `sha256sum`/`md5sum`,
  `awk`, `sed`, `head`, `tail`, `wc` only. Zero Python at every
  stage. Dash check via the shell-only snippet: clean (exit 0).
- Determinism: both binaries 3/3 byte-identical, zero stderr.
- M1: zero `sig==1/3/4` hits outside comments; `node_count` and
  `build_tree` appear nowhere outside the carried-over REMOVED
  header comment. PASS.
- M2: `construct_search(st:[]u8, bs:[]u8, bo:[]u8, n:i32,
  cost:[]u8)` signature unchanged. PASS.
- M3: every `setnode(` call site lies inside `op_const_leaf`,
  `op_split_lt`, `op_split_eq`, or `op_prune` (line 200 is the
  definition itself). The Z-simulation restore uses direct `set32`
  field writes (the pre-existing pattern), not `setnode`. Zero
  `setnode(` calls in the `construct_search`/`scan_moves` region.
  PASS.
- M4: `teval` function body md5 `a64ef5684b6c162e52131a109d82728b`
  matches the `d920af162` parent version byte-for-byte; dispatch
  only on op codes 0..3. PASS.

## Verdict: GREEDY-REGRESSION-PASS

The greedy K=2 plateau lookahead introduces no regression on the
frozen bridge battery: all move traces byte-identical to the
FIX-BUILT-PASS parent, all verdicts and costs within frozen bars,
M1-M4 re-audit clean, and the T-ADV5 STRONG PASS independently
reproduced. The mechanism is behavior-preserving where 1-ply greedy
already worked and flips the T-ADV5 positive-gain trap as designed.

## Honest scope

This verification confirms the builder's reported evidence; it adds
no new claim. C0-C remains open (one post-freeze adversary family
solved by a generic search improvement, not by a new semantic case);
C0-D (cognitive reuse) remains open. No L3 claim and no Criterion 0
claim are made here. The disclosed boundaries stand: cost headroom
narrow on T-ADV5 (106/108); K=2 defeats 1-step traps only; T-ADV6
(3-threshold pattern) is the named next adversary.
