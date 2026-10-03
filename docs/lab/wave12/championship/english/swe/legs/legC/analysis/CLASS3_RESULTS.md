# SWE-ENGLISH class-3 + direct-§B.7 results

Source model: swe-1-6-slow:free ONLY (frozen corpus english-championship-v1).
§B.7 is value-agnostic: the flaw battery (slice schedule, flaw kinds, sealed
scorer) is byte-identical to the muse championship; no content adaptation was made.

legB direct §B.7: 5/5 byte-identical
legB slice 0: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 1: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 2: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 3: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 4: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 5: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 6: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB slice 7: hits=12/12 nears=0 misses=0 pass=1 [PASS]
legB direct §B.7 total: 96/96, slices passing: 8/8
legB teach: eps=240 withheld=0 rev=12 store_n=240

legC teacher leg: 5/5 byte-identical
cross-leg invariant HOLD: SWEC_TEACH_DIGEST == SWEB_TEACH_DIGEST
legC slice 0: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 1: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 2: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 3: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 4: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 5: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 6: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0
legC slice 7: hits=12/12 pass=1 adopts=20 mh=24/24 tw=0 fps=0 leak=0

legC teacher: teach_eps=240 withheld=0 rev=12/12 store_n=240
legC mastery: fm=192/192 = 1.0000
legC revisability: rev=12/12 = 1.0000
legC integrity: blocked_ok=1 fp_ok=1 tw_ok=1 leak_ok=1 slices_ok=1 -> 1.0000
legC retention: fm=192 sum_mh=192 -> 1.0000
legC cost: esc=0 eps=536 ops=457 -> 0.9214
legC class-3 composite: 0.9921
legC §B.7 (taught): total_hits=96/96 slices_pass=8/8
legC adopted=160/192 teacher_gap=32 withheld=0
legC: no kill clauses tripped (all gates mechanical PASS)
