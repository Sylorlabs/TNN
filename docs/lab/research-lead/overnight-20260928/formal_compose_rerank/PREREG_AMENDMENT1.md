# PREREG_AMENDMENT1.md -- FORMAL-COMPOSE-RERANK battery fix + implementation bug fix

Date: 2026-10-03. Worker: FORMAL-COMPOSE-RERANK.
Amends: PREREG.md (frozen 2026-10-03, commit 4af524b81).
Status: FROZEN on commit. No further deviations without a new amendment.

## A1. Battery design flaw (found during debug runs 2026-10-03)

The frozen battery in PREREG.md section 3.2 has two edges that do not
test what the prereg claims on the REP arm:

1. B1c `e_add(13,6,2)`: On REP (fixed creation-order ranks), item 13
   has rank 9 and item 6 has rank 2. For `e_add(13,6)`: from=13
   (rank 9), to=6 (rank 2). Since rank(to)=2 < rank(from)=9, this is
   FAST-PATH on REP: the edge is written and IS readable (it lands in
   head 2, within item 13's interpreted prefix 0..8). So b1c=1 on REP,
   not b1c=0. The battery intended B1c to be cross-rank (slow path)
   on ALL arms, but on REP it is fast-path and readable. The frozen
   prediction `b1c=0` on REP is wrong for the frozen battery.

2. ADV1 `e_add(9,4,2)`: On REP, B1a `e_add(4,9,2)` is inert (does not
   commit a readable edge). So the DAG edge 4->9 does not exist on
   REP, and ADV1 `9->4` does NOT close a cycle on REP; it is a benign
   readable edge (rank 4 < rank 9). So a1=1 on REP, not a1=0. The
   battery intended ADV1 to be adversarial (cycle-closing) on ALL
   arms identically, but on REP it is benign because B1a never
   committed.

Debug runs confirmed: `b1_rep_bin` (old battery) gave
`b1a=0 b1b=0 b1c=1 a1=1 a2=0 a3=1` instead of the frozen
`b1a=0 b1b=0 b1c=0 a1=0 a2=0 a3=0`.

## A2. Battery fix (predictions for RERANK arm unchanged)

Replace in `b1_batt.zag` (and the standalone `b1_full_rep.zag`,
`b1_full_list.zag`):

- B1c: `e_add(13,6,2)` becomes `e_add(9,15,2)`. Creation ranks:
  item 9 rank 5, item 15 rank 11. Cross-rank (slow path) on ALL arms.
  Acyclic: item 15 does not reach item 9 (15->14->13, 15->13; no path
  to 9), so 9->15 cannot close a cycle. Check becomes
  `b1c=e_has(9,15,2)`.
- ADV1: `e_add(9,4,2)` becomes `e_add(7,9,2)`. The DAG contains the
  edge 9->7, so 7->9 closes the cycle 7->9->7 on ALL arms
  identically (the DAG edge 9->7 commits on all arms; it is fast-path
  everywhere). Check becomes `a1=a3=e_has(7,9,2)`.
- `es_raw(9,4,2)` becomes `es_raw(7,9,2)`.

The RERANK-arm rank trace (re-derived for the fixed battery):
after B1a {4:6,5:7,6:8}; after B1b {4:12,5:13,6:14,7:9,8:10,9:11};
after B1c {9:12,4:13,5:14,6:15}; after ADV1 {7:13,8:14,9:15,4:16,
5:17,6:18}; after ADV2 {12:9}; after ADV3a
{7:16,8:17,9:18,4:19,5:20,6:21}; after ADV3b {12:10}.
Final: maxrank=21, promotes=7, diverge=0, b1a=b1b=b1c=1,
a1=a2=a3=0, audit=0, vall=1, t1=12, t2=3.
These are the SAME values as the frozen PREREG.md section 3.2
predicts for the RERANK arm. The REP-arm prediction
`b1a=b1b=b1c=0 a1=a2=a3=0 audit=0 vall=1 t1=12 t2=0 maxrank=11
promotes=0 diverge=0` now holds for the fixed battery (verified).

## A3. LIST-arm audit prediction update: 3 becomes 4

PREREG.md section 3.2 predicts `audit=3` for LIST, with the parenthetical
"(items 4,9 on the 4<->9 cycle; item 12 on its self-loop)". That
parenthetical describes the OLD battery's cycle structure (ADV1=9->4
closing 4->9->4).

With the fixed battery (ADV1=7->9), the LIST-arm cycle structure is:
- Items 7, 8, 9 on the cycle 7->9->8->7 (ADV1 7->9 closes DAG 9->7;
  DAG 9->8 and 8->7 complete the triangle).
- Item 12 on its self-loop (ADV2 12->12).

`es_audit` counts ITEMS that can reach themselves. Fixed-battery LIST:
audit=4 (items 7, 8, 9, 12). The frozen `audit=3` is superseded by
`audit=4` for the fixed battery. All other LIST predictions unchanged:
`b1a=b1b=b1c=1 a1=a2=a3=1 vall=1 t1=12 t2=7 maxrank=11 promotes=0
diverge=0`.

Kill bar RR2 (section 4) references the LIST audit only as a
discriminator ("LIST audit>0"); the exact value 4 is now frozen here.

## A4. Implementation bug fix: es_relocate rank guard (2026-10-03)

During debug, B1b's `es_promote` hung in Phase 2 (`es_relocate`).
Root cause: `es_relocate` looped `y` over 0..23 and read
`es_head_at(st,y,old)` for UNREGISTERED items (rank -1), whose head
slots were never initialized to -1 by `es_item_new`. The uninitialized
head (0 from the zeroed allocation) was treated as record index 0,
corrupting lists and spinning `while(e>=0)` forever.

Fix (in `es_rerank.zag`): guard the per-y body with
`if(es_rank(st,y)>=0)`, matching the guard Phase 1 already has.
This is a correctness fix to the implementation; the mechanism,
predictions, and kill bars are unchanged. All other head readers
(`e_has`, `es_ndeps`, `es_dep_at`, `es_icount`, `es_ihas_to`,
`es_ioth`, Phase 1 scan) already guard on rank.

## A5. Frozen amended predictions (supersede PREREG.md 3.2)

- `rr_ex_bin` / `rr_xs_bin` B1 line:
  `B1 b1a=1 b1b=1 b1c=1 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=3`
  `B1D maxrank=21 promotes=7 diverge=0`
  plus `RR-EX prom0=0` / `RR-XS prom0=0`; E2E lines byte-identical
  to `formal_compose_e2e/ex_run_rep_1.txt` / `xs_run_rep_1.txt`.
- `b1_rep_bin`:
  `B1 b1a=0 b1b=0 b1c=0 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=0`
  `B1D maxrank=11 promotes=0 diverge=0`
- `b1_list_bin`:
  `B1 b1a=1 b1b=1 b1c=1 a1=1 a2=1 a3=1 audit=4 vall=1 t1=12 t2=7`
  `B1D maxrank=11 promotes=0 diverge=0`

Kill bars RR1-RR6 (PREREG.md section 4) stand, with the LIST audit
value updated per A3. No bar is weakened: RR1 still requires
RERANK b1*=1 vs REP b1*=0; RR2 still requires RERANK audit=0 vs
LIST audit>0.
