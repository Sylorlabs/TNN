# Job-3 bar-check results (score_job3.py, deterministic)

rundir: runs/run1

[PASS] genA G1==0
[PASS] genA G3==1
[PASS] genB G1==0
[PASS] genB G3==1
[PASS] genC G1==0
[PASS] genC G3==1
[PASS] memA G1==0
[PASS] memA G3==1
[PASS] memB G1==0
[PASS] memB G3==1
[PASS] memC G1==0
[PASS] memC G3==1
[PASS] genA G2p==360 — got 360
[PASS] memA G2p==360 — got 360
[PASS] genB G2p==0 — got 0
[PASS] memB G2p==0 — got 0
[PASS] genC G2p==0 — got 0
[PASS] memC G2p==0 — got 0
[PASS] genA P0 48/48
[PASS] genA P2 120/120
[PASS] genA P3 8/8
[PASS] genB P0 48/48
[PASS] genB P2 120/120
[PASS] genB P3 8/8
[PASS] genC P0 48/48
[PASS] genC P2 120/120
[PASS] genC P3 8/8
[PASS] memA P0==[0,0,0,8,8,0] — got [0, 0, 0, 8, 8, 0]
[PASS] memA P0 total 16/48
[PASS] memA (3,4)==3/4 on lengths {3,4,5} — hit idx [273, 274, 275] lens [3, 4, 5]
[PASS] memA (4,3)==0/4
[PASS] memA P2 accidents exactly {(5,3,312),(5,4,316)} — got [(5, 3, 312), (5, 4, 316)]
[PASS] memA P2 total 5/120
[PASS] memA P3 0/8
[PASS] memB P0==[0,0,0,2,2,0] — got [0, 0, 0, 2, 2, 0]
[PASS] memB P0 hits exactly length-2 probes of rules 3,4 — hits {0: [], 1: [], 2: [], 3: [128, 132], 4: [136, 140], 5: []}
[PASS] memB P2 accidents exactly ((5, 3, 312), (5, 4, 316)) — got [(5, 3, 312), (5, 4, 316)]
[PASS] memB P2 total 2/120
[PASS] memB P3==6/8, misses exactly [400,404] (length-2 vacuous) — got 6/8, misses [400, 404]
[PASS] memC P0==[0,0,0,2,2,0] — got [0, 0, 0, 2, 2, 0]
[PASS] memC P0 hits exactly length-2 probes of rules 3,4 — hits {0: [], 1: [], 2: [], 3: [128, 132], 4: [136, 140], 5: []}
[PASS] memC P2 accidents exactly ((5, 3, 312), (5, 4, 316)) — got [(5, 3, 312), (5, 4, 316)]
[PASS] memC P2 total 2/120
[PASS] memC P3==6/8, misses exactly [400,404] (length-2 vacuous) — got 6/8, misses [400, 404]

OVERALL: ALL CHECKS PASS
