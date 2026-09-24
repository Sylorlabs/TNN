# H1EVO V2 — R3 namespace repair: EVIDENCE

Crew: V2 (R3 namespaces). Date: 2026-09-24. Frozen prereg: `~/workspace/h1evo/PREREG_H1EVO.md` (§5, method §2).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Pure Zag, zero RNG everywhere.

## Scope and verdict (read first)

Two hypotheses were tested head-to-head, **BOTH SURVIVE** every bar:

- **H-sep**: claim-route and commit-ring namespaces separated (ring moved to slots
  `[129,258)` of a doubled routes allocation; revoke/promote read only the claim region).
- **H-del**: the dead commit-ring write deleted outright (proven no-reader, see R3b(i) audit below).

**NO WINNER IS DECLARED.** Both hypotheses are behaviorally identical on every
instrument run (attack cells, ZD battery, LH 10x/100x — byte-identical outputs).
N-AUTH was not implemented (parked per prereg).

Baseline: `~/workspace/h1evo/v2_namespace/` is byte-identical to the frozen
`~/workspace/ob2_repairatk/vb/` (verified by `diff -r` 2026-09-24) and was never
modified. Control build `v0_build/`, H-sep `v2_hsep/`, H-del `v2_hdel/` were
copied from it. The lab checkout `~/workspace/selfpam_run/tnn-lab` was untouched.

## Source changes (all in `ob_arbiter.zag`; nothing else changed)

H-sep (`v2_hsep/ob_arbiter.zag`, SHA 719d674c…):
- `arb_new_routes()` allocates `ARB_ROUTES*4*2` bytes = 258 LE-i32 slots, zeroed to -1.
- Claim namespace: slots `[0,129)`, keyed by claim id (unchanged addressing).
- Commit ring: slots `[129,258)`, addressed `(ARB_RING_OFF + ep%ARB_ROUTES)*4`
  with `ARB_RING_OFF=129`. The ring stays write-only.
- `M_REVOKE`/`M_PROMOTE` keep reading `routes[pc*4]` via the provisional claim id
  in `ast` — they never consult the ring.

H-del (`v2_hdel/ob_arbiter.zag`, SHA 6c33046d…):
- The `M_COMMIT` routes write is deleted. Commit installation, auditing
  (`ARB_APPLIED`, `M_MEM_SAFETY`), pinning, and PAM rows are unchanged.

Both hypotheses:
- `M_PROPOSE_INSTALL` ingress bounds check: `a2<0 || a2>=ARB_ROUTES` →
  `ARB_DROP, M_PROPOSE_INSTALL, a2` (refusal family, ledgered); no state mutated,
  no PAM row burned, routes table never touched.

## R3′ attack results (`h3_atk.zag`, 3× byte-identical reruns each)

New repaired-behavior probe: cross-episode claim-0/commit-ep129 collision,
same-episode claim-5 collision, revoke-misroute leg, ingress bounds leg
(ids 200/-1/129 refused, 128 admitted), 300-commit no-panic profile,
16×4 mixed sweep with per-episode V0-vs-hypothesis decision comparison.

| cell | V0 (control) | H-sep | H-del |
|---|---|---|---|
| R3a′ cross-episode | KILLBAR=1 (route clobbered, wrong survivor promoted) | KILLBAR=0 HOLD | KILLBAR=0 HOLD |
| R3a′ same-episode | KILLBAR=1 (route clobbered) | KILLBAR=0 HOLD | KILLBAR=0 HOLD |
| R3a′ revoke-misroute | KILLBAR=1 (kill landed on pinned commit survivor, refused-pinned; intended target survived) | KILLBAR=0 HOLD | KILLBAR=0 HOLD |
| R3b′ bounds (200/-1/129) | **panic**: slice index out of bounds, exit=1 | KILLBAR=0 HOLD (all three are ledgered `ARB_DROP`s; id 128 still admits; no PAM rows burned) | KILLBAR=0 HOLD (identical) |
| R3c′ no-panic profile | n/a (panics) | KILLBAR=0 HOLD (64 admits / 236 backpressure drops, unchanged) | KILLBAR=0 HOLD (identical) |
| R3c′ 16×4 mixed sweep | n/a | KILLBAR=0 HOLD (agrees=64, diverges=0) | KILLBAR=0 HOLD (identical) |
| `OB_FAILURES` | — | 0 | 0 |

SHAs (run1; runs 2,3 byte-identical):
- V0 `h3_1.txt`: `ee16d2471ff613849561f939a2b163b0eaabda66dc00e059c61ba9127736a22e` (exit=1)
- H-sep `h3_1.txt`: `aa9f4e1997fcf89c8b92fb9fb13e4c16cb8ada75b7b5b50e2693ef0d0eb8d63a` (exit=0)
- H-del `h3_1.txt`: `aa9f4e1997fcf89c8b92fb9fb13e4c16cb8ada75b7b5b50e2693ef0d0eb8d63a` (exit=0)

H-sep and H-del attack outputs are **byte-identical**. V0 breaks on all three
R3a legs and panics on R3b — the probe discriminates the repair.

Probe-design note: the first same-episode leg read the route post-clobber and
passed vacuously on V0; it was rewritten to capture the route pre-commit and
assert no-clobber explicitly (V0 then correctly KILLBAR=1).

## R3b(i) read audit (the proof behind H-del)

Every `routes` access in `ob_arbiter.zag`, both variants:
1. `M_REVOKE`: read `routes[pc*4]`, `pc` from `ast` (set only by successful
   `M_PROPOSE_INSTALL`); clears the same slot after a successful kill.
2. `M_COMMIT` (V0/H-sep only): write to episode-keyed slot — **no reader in the
   codebase consults an episode-keyed slot** (revoke/promote key off `ast` only).
3. `M_PROMOTE`: read `routes[pc*4]`, `pc` from `ast`.
4. `M_PROPOSE_INSTALL`: write `routes[a2*4]`; now ingress-bounds-guarded.

`ast` is set solely by successful `M_PROPOSE_INSTALL`, so after the ingress
guard all claim-id route reads are in-bounds. The commit-ring write's only
observable effect was clobbering claim routes and misrouting revokes/promotes —
a genuinely dead write. Deleting it (H-del) removes the shared namespace.

## ZD battery (byte-identical vs V0 except on preregistered attack inputs)

`ob_test_fl2`, `ob_test_pam`, `ob_test_mem`, `ob_test_arbiter`, `r1_atk`
(R1a known defect KILLBAR=1 / R1b novel-admit KILLBAR=0 / R1c KILLBAR=0),
`r2_atk` (R2a–d all KILLBAR=0): every binary exited 0 with `OB_FAILURES,0`;
**3× byte-identical per binary; entire stdout byte-identical across
V0/H-sep/H-del** (e.g. `zd_ob_test_arbiter_1.txt` =
`de350664875173d566fc2cbd02e923b2670bb7f01fc5b6866ad65b656664cef3` in all three).
M_COMMIT admission (R1b novel admit) is unaffected by either repair.

## Long horizon (`h3_lh.zag`: 3000 eps = 10x, 30000 eps = 100x of the R3c sweep)

Deterministic 4-episode blocks `[PROPOSE{11,(41k)%129}, COMMIT{1,30+(k%5)},
REVOKE{11}, PROMOTE{11}]`. Stride 41 forces a real V0 commit-ring/claim collision
at blocks k≡7 (mod 129) — inside the PAM admit window. Two instruments: per-episode
cumulative decision tallies (`LHE`, arbiter-log deltas via cursor, exact past the
1024-entry cap) and a per-block revoke oracle (`LHO`: expected slot from the
mem-audit ADD vs the slot the revoke actually killed + rc).

| horizon | V0 | H-sep | H-del |
|---|---|---|---|
| 10x (3000 eps), 3× | byte-identical `c0a7e6be…`; oracle: **1 misrouted revoke** (block 7: expected slot 1, killed slot 9, rc=102 MA_REFUSED_PINNED) | byte-identical `b35c12e4…`; **0 misroutes** | byte-identical `b35c12e4…` = H-sep SHA; **0 misroutes** |
| 100x (30000 eps), 3× | byte-identical `7c1f3018…`; same single block-7 misroute — **no new failure mode at 100x** | byte-identical `d208afad…`; **0 misroutes** | byte-identical `d208afad…` = H-sep SHA; **0 misroutes** |

- No panics in any of the 18 runs (all exit 0).
- 10x `LHE` lines == first 3000 `LHE` lines of the 100x run, per variant (prefix-consistent).
- Final tallies tell the same story as the oracle: V0
  `admits,withholds,drops,refused,applied,contra,prom,rev = 64,0,800,1,111,0,0,32`
  vs hypotheses `64,0,800,0,112,0,0,32` — V0's one refused misrouted kill.
- (Collision-block math correction: solutions of `37k≡1 (mod 129)` are
  k=7,136,265… — an earlier note said 14/21/28, which was wrong. Only k=7 falls
  inside the PAM admit window, so exactly one misroute is observable per run.)

## Static checks

- `grep -rni "rng|rand|seed"` over both hypotheses' sources: only "zero RNG"
  comments. No RNG mechanism anywhere in new/changed code.
- No `as []i32 / []u32 / []u16` indexed tables in new/changed code (ZNC-2026-09-21-007
  honored; `[]u8` arenas + LE accessors throughout).
- House rules honored: no `};`, `.*` only on pointers, no `nio_free` of `_zag_arg`,
  no slice > 2^25, `@import` bare, no `try` identifier.
- Toolchain pitfalls note: `(ARB_RING_OFF+ep%ARB_ROUTES)*4` relies on `%` binding
  tighter than `+`; verified empirically — the no-clobber cell and the 16×4
  forced-collision sweep (which targets exactly the slots a mis-parenthesized
  form would hit) both hold.

## Backlog

- **H-OB-81** (new, filed 2026-09-24): `ARB_APPLIED(MA_OP_ADD)` audit entries
  record the *input* slot (-1) rather than the *installed* memory slot, so the
  arbiter audit alone cannot answer "which slot did this op install" — probes
  must cross-reference the memory audit (found while building the h3 oracle;
  pre-existing in V0, not introduced by either hypothesis, not a kill bar here).
- H-OB-79 (M_COMMIT-never-sets-ast seam) and H-OB-80 (ast gap) untouched, still open.
- N-AUTH: not implemented (parked per prereg).

## Evidence inventory

- Attack: `v0_build/h3_{1,2,3}.txt`, `v2_hsep/h3_{1,2,3}.txt`, `v2_hdel/h3_{1,2,3}.txt`
  (probe source `h3_atk.zag`, identical in all three dirs).
- ZD: `{v0_build,v2_hsep,v2_hdel}/zd_{ob_test_fl2,ob_test_pam,ob_test_mem,ob_test_arbiter,r1_atk,r2_atk}_{1,2,3}.txt`.
- LH: `{v0_build,v2_hsep,v2_hdel}/lh10_{1,2,3}.txt` (3000 eps),
  `{v0_build,v2_hsep,v2_hdel}/lh100_{1,2,3}.txt` (30000 eps); probe `h3_lh.zag`.
- Frozen R3 verdict reproduction: `v0_build/r3_1.txt` (R3a KILLBAR=1, R3b panic — unchanged).
- Sources: `v2_hsep/ob_arbiter.zag`, `v2_hdel/ob_arbiter.zag` (diffs vs
  `v2_namespace/ob_arbiter.zag`, itself byte-identical to the frozen baseline).
- Binaries kept alongside sources (small); `.zag-cache/` and `*.zagd` are build
  scratch, not evidence. Debug scratch (`dbg.zag`) removed.

## Bottom line

Both H-sep and H-del repair R3: every attack cell holds, the ZD battery is
untouched, and the long-horizon oracle shows zero misrouted revokes at 10x and
100x — while V0 breaks on every R3a leg, panics on R3b, and misroutes exactly
the predicted collision block at both horizons. The two hypotheses are
byte-identical in behavior on all instruments. **No winner declared** — that
decision belongs to Micah/the integrator, with H-OB-79/80/81 as open backlog.
