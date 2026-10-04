# BASELINE-FROZEN — P2 OPERAND-SET

Characterisation of the substrate **before** any hypothesis code exists. No
implementation of the hypothesis is in this commit; the only `.zag` files here
are byte-identical copies of other lanes' frozen sources.

Commit order: `d69a87017` = PREREG alone. This file and the copies = the next
commit. All implementation lands after both.

## Digests pinned at this commit

| file | sha256 | provenance |
|------|--------|------------|
| `os_learn.zag` | `d4ef0cb8c4daccb48a180feedc10d147497c20e6c0b867b16dfd93dca83393ef` | byte-identical to `../p2_compose_dag/p2_learn.zag` (COMPOSE-DAG re-dimensioned engine, itself pinned to the frozen COGOPS core `750cb01d086f`) |
| `os_base.zag` | `c6092cdbc2c8993ff28193ae91026ceb5cdc51c93874877faac509b8b9ee19f0` | byte-identical to `../p2_compose_dag/p2_base.zag` |
| `os_drv.zag` | `1cfdb19226ebc1c2b2e9bde697f7acce04919c3a3f4e6c165a12247779e0dffd` | byte-identical to `../p2_compose_dag/p2_drv.zag` (independent reference evaluator + memo helpers) |
| `os_world.zag` | `b73ed8d19d0cdd2749793f5140b341abf83cc4ffe8b30eefe61c1dd8b8fb4017` | byte-identical to `../p2_compose_dag/p2_world.zag` (177 facts) |
| `ref/c8_base.zag` | — | `cmp`-identical to `../p2_compose_dag/ref/c8_base.zag` |
| `ref/c8_learn.zag` | — | `cmp`-identical |
| `ref/c8_world.zag` | — | `cmp`-identical |
| `ref/c8_main.zag` | — | `cmp`-identical |

Kill bar **C2** verified at this commit: `os_base.zag + ref/c8_world.zag +
ref/c8_learn.zag + ref/c8_main.zag` builds with the pinned compiler and
reproduces `../cogops_learnosc2/c8_run1.txt` **byte-identically**
(`ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7`,
3344 bytes), 2/2 identical, stderr empty, exactly one `fn main(`.

This re-confirms that blocker **B13** stays resolved and that the frozen
COGOPS substrate is reproducible on this host through the single
`_zag_print` writer substitution that `os_base.zag` already carries.

## The substrate's accepted-need repertoire at this commit

Exactly three forms, all researcher-written, all keyed by the need's field
vector in `shape_desc`:

| family | shape | fields | procedure |
|--------|-------|--------|-----------|
| 0 | `nf = 2` | `[rel, obj]` | `ret_gen` / `ret_spec` (RETRIEVE), set output |
| 1 | `nf = 1 + 3*ns` | `[ns, (subj,obj,val)*ns]` | `vfy_gen` / `vfy_spec` (VERIFY), set operand at slot 1, set output |
| 2 | `nf = 3`, `f1 == 1` | `[rel, 1, ?]` | `cnt_gen` / `cnt_spec` (distinct COUNT), scalar output |

Nothing else binds. COMPOSE-DAG's ids 14, 15, 16 decline for exactly this
reason. Link kinds 1, 2, 3 only.

## What this lane will add, and where

One accepted need shape (`nf = 2 + 3*ns`, the family-1 shape with one extra
leading integer) and one reduction over the assembled operand set. The
reduction is written once and reached from two provenance switches. The full
delta against `os_learn.zag` is published in `DIFF-oslearn-vs-p2learn.txt`
(kill bar C3); nothing else in the frozen engine changes.