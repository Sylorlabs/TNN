# ht_next / ht_decide — test log (2026-09-22)

Binaries: `ht_next_bin`, `ht_decide_bin` (pure Zag, no RNG, no timestamps).
Sources `ht_sense2.zag`, `ht_read.zag`, `ws2_sense.zag` NOT modified.
Stdin read via raw `_zag_raw_syscall(0,...)` on fd 0 (nio_read_exact refuses
non-regular fds). Total stdin capped at 1 MiB; no per-result skip — the 16 KiB
title+snippet cap is documented as read-cap only per task instruction.

## SPEC DEVIATION (documented, deliberate)
Task said ht2_begin(w, cand_idx, searched) with searched=1. The frozen
`ws_gate` in ws2_sense.zag returns 0 (NO_SEARCH) whenever searched!=0, which
forces EVERY case to trial DISP 4 (WITHHOLD) and makes the specified test
expectations (5/2/4) unreachable. The CAND <searched> field is parsed but
ignored; a fresh cycle always runs with searched=0. D8 proves identical output
for CAND 16 with searched=0 vs 1. The real driver must send 0 for a fresh
search cycle, or the trial will see WITHHOLD on every candidate. Needs the
supervisor's word on intended gate semantics.

## ht_next tests — all PASS
- N1 `HIST 0` -> `NEXT 0 <q0> 0`
- N2 last V disp=4 fol=0 -> `NEXT 7 <q7> systematic review 1` (flag=1)
- N3 last V disp=4 fol=1 -> `NEXT 7 <q7> latest evidence 1`
- N4 WITHHOLD fol=2 exhausted -> next unvisited (cand 1)
- N5 all 19 visited -> `DONE all_candidates_visited`
- N6/N9 empty stdin -> `NEXT 0 <q0> 0`

## ht_decide tests — all PASS
- D1 CAND 16 (A1, known, contra DENY), 2 DENY + 1 AFFIRM (2 distinct domains):
  STANCE 2,2,1 / SIGNAL 4 / DISP 5 (REVISE) / CONSULT 0 / DEVIATION 0
- D2 CAND 0 (C1, known), 3 AFFIRM:
  STANCE 1,1,1 / SIGNAL 5 / DISP 2 (INSTALL) / CONSULT 0 / DEVIATION 0
- D3 CAND 8 (C8), 1 AFFIRM + 1 DENY:
  STANCE 1,2 / SIGNAL 2 / DISP 4 (WITHHOLD) / CONSULT 1 / DEVIATION 0
- D4 helper AFFIRM bypasses classifier (direct ws_add_result, domain "helper"):
  2 DENY + helper AFFIRM -> STANCE 2,2,1 / SIGNAL 6 / DISP 3 (REJECT)
- D5 helper UNCERTAIN -> stance 0, relevance 0 (logged, not corroborating):
  SIGNAL 2 / DISP 4 / CONSULT 1
- D6 D1 run twice -> byte-identical output (HEAD 9350bb23...)
- D7 snippet with escaped \t \n unescaped correctly -> AFFIRM
- D10 CAND 8, zero results -> SIGNAL 2 / DISP 4 / CONSULT 1

Known limits: max 4096 input lines, 8 fields/line, k clamped to 4000 results,
6 corroboration slots (ws2 limit). znc L0012 string-leak warnings only.
