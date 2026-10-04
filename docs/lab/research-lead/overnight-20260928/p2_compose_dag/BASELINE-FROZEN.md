# BASELINE-FROZEN — measured behaviour of the FROZEN COGOPS composer

Committed with PREREG.md, BEFORE the new engine is written.

## What this is

The object under test is `cogops_learnosc2/c8_learn.zag`, byte-identical
(`750cb01d086f…`), driven over this lane's world and goal records. Only
`nn <= 4` goals appear here, because the frozen arena is hard-dimensioned
at 4 needs (Section 2).

Arm: `f_base.zag = p2_base.zag + p2_world.zag + ref/c8_learn.zag +
p2_drv.zag + f_main.zag`, entry point `compose_iter`.

Output: `f_base_run1..3.txt`, sha256
`2d9fa604944ec5e6b9dfad55c178d829706da55baea448b8eaa969a796e30a33`, 3/3
byte-identical.

## Field meanings

`d1` is a digest of the emitted answer, `acc += 1002*len + sum(contents)`
summed over records. `eng`/`ref`/`rea` print `(need_index, record_length,
record_contents_sum)` per need, in need-index order, for: the engine's
answer (`eng`, normalised from plan order), an independent straight-line
reference under the strict reading (`ref`), and the same reference under
the produced-value reading (`rea`). `ra=0` means the reference REFUSED.

The reference shares only the record-accessor layer (`g_nneeds`,
`g_nlinks`, `link_w`, `need_nf`, `need_f`) with the engine. It has its
own ordering routine and its own execution loop and calls only the
frozen `ret_gen` / `vfy_gen` / `cnt_gen`.

## MEASURED (this is data, not prediction)

| id | goal | nn | nl | plan order | r1 | d1 | eq-strict | eq-adapt | verdict |
|----|------|----|----|-----------|----|----|-----------|-----------|---------|
| 1 | g901 | 2 | 1 | 0,1 | 2 | 4007 | 1 | 1 | correct under both readings |
| 2 | g902 | 3 | 2 | 0,1,2 | 2 | 6012 | 1 | 1 | correct |
| 6 | g906 | 3 | 2 | **1,0,2** | 2 | 43274 | 1 | 1 | correct; plan order non-canonical |
| 8 | gbro k=2 | 4 | 4 | **2,0,1,3** | 2 | 44238 | 1 | 1 | correct; plan order non-canonical |
| 9 | g909 | 4 | 4 | **1,0,2,3** | 2 | 94129 | 1 | **0** | **frozen = single-source reading** |
| 10 | g910 | 2 | 1 | 0,1 | 2 | 2003 | **0** | 1 | **frozen already = produced-value reading** |
| 11 | g911 | 2 | 1 | 0,1 | 2 | 1004 | 1 | 1 | identical under both; not discriminating |
| 16 | g916 | 1 | 0 | — | **0** | 0 | — | — | **declined** (unbindable need shape) |
| 17 | g917 | 3 | 2 | 0,1,2 | 2 | 41232 | 1 | **0** | **frozen answers; adapt refuses** |
| 18 | g918 | 2 | 1 | 0,1 | 2 | 40230 | 1 | 1 | correct; mixed version 2/0 |
| 19 | g919 | 3 | 2 | 1,2,0 | 2 | 42248 | n/a | n/a | iterated; pass cap 16 |

`r2 = 1` (plan loaded) for every id where `r1 = 2`; `plans_loaded`
increments once per goal. Totals: `pb=10 pl=10 tr=15 dc=2`.

## Findings from the frozen baseline (recorded before the new engine)

**F1 — NON-CANONICAL EMISSION ORDER (new).** `topo`/`topo_g` scan for a
zero-indegree node without breaking, so the LAST ready node wins. Plans
for the same goal are orderings, and the answer's record sequence is
plan-order-dependent. Measured `ord` values: id6 `1,0,2`; id8 `2,0,1,3`;
id9 `1,0,2,3`; id19 `1,2,0`. Consequences: (a) two structurally
equivalent compositions of the same goal do not produce comparable
answers; (b) equality testing on the raw record stream is order-sensitive
and reports false mismatches. This lane normalises to need-index order
before every comparison, and records the plan order explicitly.

**F2 — SINGLE-SOURCE OPERAND SET (new; confirmed at id9).** A need with
two incoming set-consuming links receives only the FIRST source. Measured:
need0 = 20 subjects, need1 = 6 subjects, need2 = 20 subjects (should be
26), need3 = 40 (should be 52). `fanin_src` returns on the first match.

**F3 — SILENTLY-DROPPED SET LINK (new; confirmed at id17).** A
set-consuming link into a need that has no set-shaped operand is ignored
entirely: the frozen engine answers `0` (a real number, confidently wrong)
where the invariant reading refuses the goal.

**F4 — NO INTERFACE-TYPE CHECK (new; confirmed at id11).** A
set-consuming link out of a scalar-producing need is executed by feeding
the scalar in as if it were a subject. No detection, no refusal; the
answer is `0`, indistinguishable from a legitimately empty result. Not
answer-discriminating by construction, so a new negative counter is
required.

**F5 — PRODUCED-VALUE INVARIANT ALREADY FROZEN (id10).**
`compose_iter` uses `apply_kind1_g`, which suppresses the scalar link when
the source produced nothing. `compose` (the non-iterated entry point)
uses `apply_kind1`, which does not. So the invariant exists in the frozen
code but only on one of the two entry points.

**F6 — HARD DIMENSIONING AT 4 (to be characterised next).** `W = 320`,
`OUTS = 640`, `SUBL = 512`, `ord = 16`, `dirty = 16`, `ind`/`placed = 16`,
`topo` and `topo_g` allocate `ind`/`placed` as `z_alloc(16)`, plan
entries are 56 bytes = 4 steps, the binding table is 8 entries, and
`execute_plan_iter` has a hard pass cap of 16. Every one of these is a
literal, not a parameter.

**F7 — ITERATION PASS CAP.** id19's self-linked walk reaches subject 1016
and stops at exactly 16 passes. A 20-step walk cannot be expressed.

## Why these are baselines, not results

Every number above comes from the FROZEN object. No new engine exists
yet. `build.sh` re-derives all of it from the committed sources.