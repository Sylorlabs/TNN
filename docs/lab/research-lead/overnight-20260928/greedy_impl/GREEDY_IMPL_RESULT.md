# GREEDY Implementation Result: 2-Ply Plateau Lookahead (K=2)

Status: RESULT-COMMITTED. All runs complete. No further evaluation at
this commit.

Ancestry:
- Prereg: `a79f842e5` (PREREG-FROZEN, committed before any
  implementation; this result commit is its descendant).
- Design: `greedy_fix/GREEDY_FIX_DESIGN.md` (`3a0852278`),
  GREEDY-DESIGN-COMPLETE.
- Parent source: `bridge_fix_impl/bridge.zag` at `d920af162`
  (FIX-BUILT-PASS), SHA-256
  `d42c650a0e5d5e3573113524d17aabaee1afaf59c6351017bb37d8bf604e8dec`.
- T-ADV5 sealed protocol template: `tadv5_reeval/` (`83c02efff`),
  TADV5-ACCEPTABLE.

Scope: `docs/lab/research-lead/overnight-20260928/greedy_impl/` only.
Commits local. Nothing pushed.

## 1. K1: prereg frozen before implementation - PASS

`PREREG_GREEDY_IMPL.md` committed at `a79f842e5`. The source copy was
verified byte-identical to `d920af162` (SHA-256 match) after the prereg
commit and before any edit. No implementation, binary, or evaluation
existed at the prereg commit.

## 2. Implementation

`greedy.zag` = byte-identical copy of the `d920af162` bridge source,
then modified ONLY in the `construct_search` region:

- New helper `scan_moves`: the candidate enumeration extracted
  mechanically (byte-identical enumeration) with two added recording
  branches. Records the best strictly-positive move into `best[0..5]`
  and every admissible gain-exactly-0 move into `zbuf` in scan order.
- New `construct_search`: per iteration, computes `g1`/`m1` and `Z`,
  simulates each `z` in `Z` and measures the best follow-up gain
  `unlocked(z)` from the resulting state (same admissibility rules),
  applies the plateau move iff `Z` is nonempty and
  `unlocked(z*) > g1`, else the greedy move iff `g1 > 0`, else
  terminates. One `GREEDY` ledger line per iteration; the
  `BRIDGE MOVE` line for applied moves is unchanged in format.
- Unchanged: four operators, `novelty_generic`, VERIFY/refit, `teval`,
  family specs, menu adoption, cost units, all caps (8-node, EQCAPP=4,
  MOVEBUD=24, COSTCEIL=108). No op-code-specific logic anywhere in the
  rule. No new `setnode` sites. `construct_search` signature unchanged.

Seal check: `diff` of `greedy.zag` against
`d920af162:bridge.zag` shows changes confined to the
`construct_search`/`scan_moves` region (hunks at original lines
385-599 only). No other mechanism delta.

Build: repo `znc` only. `greedy.zag` -> `greedy_bin`: clean (only the
zagd-unavailable notice, same as the parent build). One analyzer
warning (A0102, discarded `scan_moves` return on a follow-up query) was
fixed by binding the result; the final build is warning-free apart
from the zagd notice.

## 3. K2a: frozen battery regression - PASS

Three runs of the frozen battery `main()`: 3/3 byte-identical
(SHA-256 `36f24db50c42acf02ca392214aadf69213d55a2a10539a69b30c629c53aa8175`),
zero stderr, exit 0.

- `K2 1`, `VERDICT BRIDGE-TESTED`.
- Per-family adopted/promoted/built/refit identical to FIX-BUILT-PASS
  on all 14 family runs (fresh G/H/K/T-ADV4 invented; fresh J
  HONESTFAIL with built=0; retained adopted/refit per the frozen
  `ra`/`rr` tables).
- Menu-family exact costs UNCHANGED: A=20, B=11, C=8, D=6, E=5.
- All invention-family costs within frozen bars (<= 108; G2 <= 30).

Cost ledger (search cost `scost`, total `cost`):

| family | FIX cost | GREEDY cost | delta | bar |
|---|---|---|---|---|
| FRESH G (6) | 62 | 62 | 0 | <= 108 |
| FRESH H (8) | 68 | 94 | +26 | <= 108 |
| FRESH K (10) | 68 | 68 | 0 | <= 108 |
| FRESH J (9) | 181 | 820 | +639 | none in battery; HONESTFAIL preserved |
| FRESH T-ADV4 (12) | 70 | 72 | +2 | <= 108 |
| RETAINED G (6) | 62 | 62 | 0 | <= 108 |
| RETAINED Gp (11) | 17 | 17 | 0 | <= 108 |
| RETAINED H (8) | 65 | 97 | +32 | <= 108 |
| RETAINED G2 (7) | 26 | 26 | 0 | <= 30 |

Amendment A1 (anticipated divergences, carried transparently per
prereg section 2.4):
- New `GREEDY` ledger lines appear in output (instrumentation,
  preregistered).
- `cost=` increases on H, T-ADV4, retained H, and J are pure
  lookahead simulation overhead: the `BRIDGE MOVE` traces are
  byte-identical to `FIX_RUN1.txt` (`diff` on all `BRIDGE MOVE` lines:
  zero differences), and `plateau=1` never fired on any battery family
  (0 occurrences). The lookahead changed no search decision on the
  frozen battery; it only paid for follow-up scans that confirmed the
  greedy choice. Ledger samples: H it=0 shows `nz=4 unlocked=1`
  (not > g1=1, no diversion); J it=1 shows `nz=18 unlocked=0`.
- Menu-family exact costs unchanged, as required (no
  `construct_search` on those paths).
- J remains HONESTFAIL (built=0); its +639 is honest search overhead
  with no battery cost bar. Noted as narrowed headroom, not hidden.

## 4. K2b: T-ADV5 sealed run - STRONG PASS

`greedy_tadv5.zag` = `greedy.zag` with `main()` replaced exactly as
`tadv5_reeval.zag` replaced it (family 13 dispatch + TADV5 harness).
Seal check: `diff` against `tadv5_reeval.zag` shows ONLY the
`construct_search`/`scan_moves` mechanism delta (218 changed lines,
all inside the original construct_search region).

Three runs: 3/3 byte-identical
(SHA-256 `a95917e1e2e8186d344b220c1dc892e4ebd64bb3eb1400757eb77ca4ef247fb3`),
zero stderr, exit 0.

Trace (the design prediction, confirmed exactly):

```
GREEDY it=0 g1=1 nz=2 unlocked=10 plateau=1
BRIDGE MOVE li=0 op=1 p=13010 gain=0 nc=4
GREEDY it=1 g1=10 nz=0 unlocked=0 plateau=0
BRIDGE MOVE li=3 op=1 p=13020 gain=10 nc=7
GREEDY it=2 g1=0 nz=0 unlocked=0 plateau=0
INV SEARCH fam=13 n=40 built=1 nodes=7 scost=52
INV FIT fam=13 exact=1
INV NOVEL fam=13 pass=1
INV EQN fam=13 eqnodes=0
INV PROMOTE fam=13 form=3 V=14
TR TADV5 fam=13 cost=106 adopted=3 V=14 refit=-1 inv_event=1 inv_promoted=1 uses3=1 strikes3=0
TADV5-NODES nc=7 eqnodes=0
TADV5-TREE ni=0 op=3 a=1 b=2 c=3
TADV5-TREE ni=1 op=1 a=13010 b=0 c=0
TADV5-TREE ni=2 op=0 a=1 b=0 c=0
TADV5-TREE ni=3 op=3 a=4 b=5 c=6
TADV5-TREE ni=4 op=1 a=13020 b=0 c=0
TADV5-TREE ni=5 op=0 a=0 b=0 c=0
TADV5-TREE ni=6 op=0 a=1 b=0 c=0
TADV5-HELDOUT wrong=0
```

Bar check (frozen, from `tadv5_reeval/PREREG_TADV5_REEVAL.md` 3.1):
- adopted=3, promoted=1: yes.
- cost=106 <= 108: yes (headroom 2; narrowed as the design disclosed).
- node count 7 <= 8: yes.
- EQ nodes 0 <= 4: yes.
- Exact fit on the 40-point buffer: yes (`INV FIT exact=1`).
- 2-threshold form with an LT separating the zero-block as a region:
  yes. The tree is `IF(x<13010, 1, IF(x<13020, 0, 1))`: node 3 is an
  IF on LT(13020) whose then-branch is CONST(0), covering exactly the
  [13010,13020) zero-block. Zero EQ nodes, so no EQ memorization.
- Falsifiers: F-DECEPT-COST no (106 <= 108); F-DECEPT-DEGENERATE no;
  F-DECEPT-NODECAP no; F-DECEPT-MEMORIZE no; F-DECEPT-WRONG no
  (held-out wrong=0); F-DECEPT-PREEMPT no (inventor fired,
  adopted=3).

The trap flipped exactly as predicted: EQ,EQ,HONESTFAIL became
LT,LT,exact-fit. Iteration 0 took the zero-gain LT@13010 because it
unlocked +10, strictly beating the +1 EQ trap move.

## 5. K3: purity, determinism, M1-M4 - PASS

- K4 pure-Zag: every stage used shell, `znc`, `grep`, `diff`,
  `sha256sum`/`md5sum`, `sed`, `awk`, `head`, `tail`, `wc` only. Zero
  Python at every stage including scratch, diagnostics, byte checks,
  and verification. The earlier `python3 -c "pass"` failure pattern
  from the C2 wave was not repeated.
- Determinism: both binaries 3/3 byte-identical, zero stderr.
- Dash check: `worker_snippets/check_no_dash.sh` passes on all loop
  docs in this directory; zero em/en-dash bytes.
- M1: zero `sig==1/3/4` hits; `node_count`/`build_tree` appear only in
  the carried-over REMOVED header comment.
- M2: `construct_search(st:[]u8, bs:[]u8, bo:[]u8, n:i32, cost:[]u8)`
  signature unchanged; no diagnosis enum.
- M3: every `setnode` call site lies inside `op_const_leaf`,
  `op_split_lt`, `op_split_eq`, or `op_prune`. The Z-simulation
  restore uses direct `set32` field writes (the pre-existing pattern),
  not `setnode`.
- M4: `teval` byte-identical to the `d920af162` version (md5
  `a64ef5684b6c162e52131a109d82728b` both); dispatches only on op
  codes 0..3.

## 6. Verdict: GREEDY-PASS

K1 PASS (prereg `a79f842e5` strictly precedes implementation).
K2 PASS (battery regression PASS with Amendment A1; T-ADV5
STRONG PASS). K3 PASS (pure Zag, 3/3 identical, M1-M4 PASS, dash-clean).

## 7. Honest scope and boundary

- This is one more C0-C data point for the fixed protocol: an
  independent post-freeze adversary family (T-ADV5) is now solved by a
  generic search improvement, not by a new researcher-authored semantic
  case. C0-C is not closed and C0-D (cognitive reuse) remains open. No
  L3 claim and no Criterion 0 claim are made here.
- The frozen battery shows the lookahead is behavior-preserving where
  1-ply greedy already worked (zero diverted decisions, identical move
  traces); its price is measured simulation overhead, all within bars.
- Cost headroom is now narrow on T-ADV5 (106/108). The design's honest
  boundary stands: K=2 defeats 1-step traps; a 2-step trap (two
  consecutive zero-gain moves before payoff) still defeats it. T-ADV6
  (3-threshold non-monotonic pattern) is the named next adversary.
- The J-family search cost (780, total 820) has no battery bar but is
  recorded as the mechanism's worst-case overhead on an unfittable
  buffer.
