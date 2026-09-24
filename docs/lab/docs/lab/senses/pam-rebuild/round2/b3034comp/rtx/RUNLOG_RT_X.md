# RUNLOG_RT_X — B-3034-X red-team battery, execution record

Crew: RT-X. Date: 2026-09-24.
Prereg: PREREG_RT_X.md, frozen commit `0f8be190b7913e63e17175e2f38d938f257bdda7`
(committed ALONE before code).
Build: commit `ad7919c257a6a6e5436cef87ea1b1715f8523bce` (sources only;
verified byte-identical to the files the runs were built from:
`diff -r` clean, "COMMITTED BUILD == RUN BUILD").
Target: composition driver ad0e1ddd UNMODIFIED (SHA-256 verified pre-build,
prereg §9). Pure Zag, zero RNG (grep-clean).

## Source pins

| file | SHA-256 |
|------|---------|
| drive3034_ad0e1ddd.zag (pristine) | 1b1eb68ab4d0b704546b75ee0a6a7207cb7dcd59b6b6c53b5850d4b991e410b4 |
| b303134_common.zag (= ..._6e74ce54) | 79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218 |
| R33_NATIVE_IO_V1.zag | e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8 |
| src/rtx_x.zag | d1baa697202d6248da8e0e6fd8790fb2b42572fe9433a34965ba5c4eda6c90b1 |
| src/rtx_ablate_p1.zag | ce89f6ad5a6162af7fb85cc6e4376438b489ff09a55689aceebf6b948a1bdaab |
| src/rtx_ablate_p2.zag | bcb40deb4ce0079001bd700f04d1b25d8ca6b42562bf71d4d16cc4082645d1e7 |
| derived/drive3034_lib.zag | 5a41a7936b3b362eb117d91b95186fcd85907d8fa3bc1c1872a502e7b97751ed |
| derived/drive3034_ablate_p1.zag | 2a6c1bbb1323a921bd46dfef67ae96f92c932a04ceb7a77c0eb917f1344e984f |
| derived/drive3034_ablate_p2.zag | 9b01491a49ad587b56add771f22d9de120797daee0537caba473884383c084f2 |
| derived/b303134_common_ablate_p2.zag | c2147c29809c9af0b3c56ab4b875a0b2afed8c666ce8c5afce7d5c8761a4154b |

Derived diffs: `src/derived/DIFFS.md` (lib = one-line main rename; p1 = 5
line-level nops; p2 = import retarget + bind_ok→1). Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

## Run SHAs (3× byte-identical stdout)

| binary | run1 | run2 | run3 | SHA-256 (all three) |
|--------|------|------|------|---------------------|
| rtx_x | run1_x.txt | run2_x.txt | run3_x.txt | 2c427e8cddee44363efa86833da565aaecdb26a9cf44203eaaae1720b6cbb3b1 |
| rtx_ablate_p1 | run1_a1.txt | run2_a1.txt | run3_a1.txt | 039c70901f46af7460ff81382f62c9ed1f4c615659c2c9c5ecdd55a581b6eeeb |
| rtx_ablate_p2 | run1_a2.txt | run2_a2.txt | run3_a2.txt | bc852c6ca916e6732fba6c52f3b87f92443ee8a56b9f3641d86b021bb50162a2 |
| drive3034_pristine (15 modes) | — | — | — | 778aa6478b1e62c3be12f6179673a08fc756c18889e4486da7b681d2f4e175eb |

All four: 3/3 runs byte-identical.

## Per-class results vs bars

| class | gate_install | protocol_install | harm_install | bar | predicted | observed |
|-------|--------------|------------------|--------------|-----|-----------|----------|
| X1 VACUOUS-K | promote 120/120 | mon refuse 120/120 (reason K-distinct) | — | KILL | 120/120 kill | KILL ✓ |
| X2 VACUOUS-TICK | promote 120/120 | mon refuse 120/120 (reason temporal) | — | KILL | 120/120 kill | KILL ✓ |
| X3a GAP-ABSENT | twin identical 120/120; gapped promote 60/60 | mon (ge_closed) refuse 60/60 gapped | — | KILL | 120/120; 60/60 | KILL ✓ |
| X3b gap-swap | inexpressible (proxy 0/120) | — | — | STRUCTURAL-KILL | structural | HOLDS ✓ |
| X4 EPOCH-DRIFT | promote 120/120 (oracle stale-true) | mon refuse 120/120 (reason epoch-drift) | false-at-e2 120/120 | KILL | 120/120 kill | KILL ✓ |
| X5 DEAD-ACT-SINK | 1020 promoted, 0 with extra≠0, 0 sink fires | — | — | interpretive KILL | 0 fires | KILL ✓ |
| X6 ABLATION | p1: 15/15 modes byte-identical to pristine; p2: 14/15, j_tag only moves (0→120) | — | — | KILL | identical / j_tag moves | KILL ✓ |
| S0 sanity | promote 0/120 | — | — | sanity HOLDS | 0/120 | HOLDS ✓ |
| OLD15 replay | all 15 at frozen rates | — | — | sanity | prior rates | prior rates ✓ |

Notes:
- X1/X2/X4 gate calls are oracle-true honest fixtures (verdict_bit=1 on the
  driver's observable world); the kills come from the protocol/harm installs
  the driver cannot see — exactly the conjunctions B-3034COMP never tested.
- X4's driver-visible calls are byte-identical to X1's (prereg A3, by
  construction: same H(j) bytes); the 120/120 harm fires on the epoch-indexed
  world the driver never observes.
- X5 per-mode: X1 120, honest 120, rf/rc/xr/j_dump 0, n_goal 120, o_temporal
  120, o_numeric 120, j_agg 60, k_blind 120, l_distal 120, ge_gap 120;
  p_remint/j_tag N/A (no pipeline calls). Per-mode promote counts match the
  OLD15 replay section exactly (transcription cross-check).
- X6 p1 proves the 34-half's K-loop, continuity, tick compares, and in-loop
  maxv test contribute NOTHING to any of the 15 modes' outputs: the battery
  measured verdict_bit + the maxv==3 gate + the forge fiat. p2 confirms
  bind_ok is the only load-bearing check in j_tag's path.
- X3b structural verification (script, committed source): pipeline has
  exactly 9 parameters — one (label,conf,meas,extra) percept tuple, one
  seed, three scalar knobs (maxv, forge, corrupt); the while(e<3) body
  references no identifiers outside the outer args and loop locals (it
  re-feeds identical args). Three distinct per-epoch byte vectors plus three
  per-epoch principal verdict objects are INEXPRESSIBLE. Sequential calls
  cannot substitute (no cross-call state; each call re-derives h0 from its
  own args — F1). The proxy (single shot, e2 false label) promotes 0/120:
  the proxy is a renamed false snapshot, not the gap-swap.
- OLD15 section of rtx_x is byte-identical to the pristine binary's 15 mode
  outputs (15/15 modes): the main-rename lib's pipeline IS the committed
  pipeline. The X-classes therefore ran against ad0e1ddd unmodified.
- SCOPE-BUG-S6 line (own line, not an X-bar): o_numeric sink_divergence
  39/120 recomputed here from driver-visible outputs (edge_promoted=120/120
  in the OLD15 replay). §6 must not outvote X1–X6.
- Sanity "classes are new": X1's 120 promoted ids use honest G, forge=0,
  maxv=3 — they satisfy none of J–P's refusal predicates (J: extra≠0/splice;
  P: oracle-false; O: forge fiat; K: aggregate; N/L: note/world). Quiet old
  bars beside firing X* bars confirm the original matrix cannot see these
  conjunctions. X2 uses forge=0 (not O-as-run). X4 is not P/S0: the oracle
  accepts (120/120 promote) while S0's false content promotes 0/120.

## Machine verdict (§8 rule)

X1∧X2∧X4 kill ✓, X3a kills ✓, X3b structural-kills ✓, X6 kills ✓,
S0 holds at 0/120 ✓, no prediction missed → no bar void. Print:

- VERDICT_X: TESTED-killed
- VERDICT_34: MECHANISM-ABSENT
- VERDICT_C3034: DEMOTED (to a single verdict_bit call)

See VERDICT_RT_X.md for the final adjudication.
