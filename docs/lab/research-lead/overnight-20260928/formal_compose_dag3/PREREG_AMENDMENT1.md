# PREREG_AMENDMENT1.md -- FORMAL-COMPOSE-DAG3

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG3. Parent commit:
c956d17f1 (frozen PREREG.md). Task type: NON-LEDGER.

This amendment documents five exact-prediction mismatches
found when the frozen battery ran, with root causes. It
corrects the section-4 prediction table only. NO kill bar
changes: every value pinned by DAG1-DAG6 matched the frozen
predictions exactly. No implementation file was modified;
`es_rerank.zag` remains byte-identical to the parent lane
(sha256 8a6de72312d0375bb32d76292dbf97cbb46c8b27d1ce5207a499799b1b051c1c).
No re-run is required: the amendment changes predictions,
not code or battery.

## A1. RERANK D3A maxrank: predicted 5, actual 8

Root cause: prereg arithmetic error, not a mechanism
deviation. `es_item_new` updates maxrank-seen at
registration time (`if(rk>mr){ set32(st,2088,rk); }` in
es_rerank.zag). Registering items 4..12 assigns ranks 0..8,
so maxrank-seen is already 8 before the first promotion;
the stage-1 promotions only reach rank 5 and never raise it.
The frozen rank trace itself (section 3.1) is confirmed
digit-for-digit: promotes=4, all four diamond edges
readable, and D3B's maxrank=9 (item 4 promoted to rank 9)
matches the prediction, which is only consistent with the
derived trace. Corrected prediction: D3A maxrank=8.

## A2. LIST D3C t1: predicted 10, actual 11

Root cause: prereg arithmetic error. Stage 3 writes SEVEN
type-1 edges (4->8, 4->9, 8->7, 9->7, 10->11, 11->10,
12->4), all readable on the unconstrained LIST store, so
t1 = 4 (diamond) + 7 = 11. (On RERANK, 11->10 is inert, so
t1=10 there, as predicted.) Corrected prediction: LIST D3C
t1=11.

## A3. LIST D3D t1: predicted 20, actual 22

Same arithmetic error: 11 + 10 (chain) + 1 (13->23) = 22.
Corrected prediction: LIST D3D t1=22.

## A4. LIST D3D audit=18 (predicted 19) and maxrank=1
## (predicted 19): latent layout bug in es_list_rr.zag

Root cause: a genuine latent bug in the DISCRIMINATOR store
`es_list_rr.zag` (copied byte-identical from the parent
lane), not in the mechanism under test. Its layout says
`1984: registered[24], u8` with flags at `1984+1+it`, and
`2008: registration counter, i32`. For it=23 the flag byte
IS st+2008, the low byte of the counter. Registering item
23 (which the D3 battery does in stage 4; the parent
battery never registered past item 15, so the bug never
fired there) clobbers the counter: counter 19 -> low byte
set to 1 -> incremented to 2, hence maxrank = 2-1 = 1.
The audit's registration check for u=23 then reads the
counter low byte (2, not 1) and skips u=23, hence
audit=18 instead of 19.

Deliberately NOT fixed: the file is the parent lane's
frozen discriminator design; the bug affects only LIST
diagnostics (maxrank) and the exact audit count, while the
arm's frozen purpose -- VOID-discrimination -- is intact
(audit=18 > 0 proves the adversarial probes genuinely
close cycles; all adversarial attaches readable). Fixing
the harness to hit prettier numbers would be cosmetic;
the honest record is kept here. Flagged as a known issue
for the parent lane. Corrected predictions: LIST D3D
audit=18, maxrank=1.

## Corrected exact-prediction table (section 4)

d3_rerank_bin: unchanged except D3A maxrank=8:
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=1 audit=0 promotes=4 maxrank=8
D3B adv1=0 adv2=0 dia=1 inv=1 audit=0 promotes=6 maxrank=9
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=0 inv=1 audit=0 promotes=11 maxrank=10 t1=10 t2=0
D3D chain=10 cyc=0 inv=1 audit=0 promotes=12 maxrank=30 diverge=0 t1=20 t2=0
```
d3_rep_bin: unchanged (all predictions matched).
d3_list_bin: D3C t1=11; D3D t1=22, audit=18, maxrank=1:
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=0 audit=0 promotes=0 maxrank=8
D3B adv1=1 adv2=1 dia=1 inv=0 audit=4 promotes=0 maxrank=8
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=1 inv=0 audit=8 promotes=0 maxrank=8 t1=11 t2=2
D3D chain=10 cyc=1 inv=0 audit=18 promotes=0 maxrank=1 diverge=0 t1=22 t2=2
```

## Kill-bar impact: none

DAG1: RERANK D3A dab=dac=dbd=dcd=1 (actual 1,1,1,1);
REP all 0; LIST all 1. Unchanged, PASS.
DAG2: RERANK adv1=adv2=0, cyc=0 (D3C, D3D), audit=0 all
lines; LIST adv1=adv2=1 audit=4 (D3B), cyc=1 (D3C, D3D).
Unchanged, PASS.
DAG3: RERANK inv=1 all four lines; REP inv=1 all four
lines. Unchanged, PASS.
DAG4: RERANK D3C fo1=fo2=fi1=fi2=1, ext1=ext2=1, t1=10,
t2=0, promotes=11, maxrank=10. Unchanged, PASS.
DAG5: RERANK D3D chain=10, cyc=0, promotes=12,
maxrank=30, diverge=0, t1=20, t2=0. Unchanged, PASS.
DAG6: 3/3 byte-identical per binary, stderr empty on all
9 runs, no analyzer warning classes. Unchanged, PASS.
