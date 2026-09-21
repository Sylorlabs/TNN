# Z7 battery status — r1 / 1x, 2026-09-21

Every leg rerun (rc1=0 rc2=0, stdout byte-identical between reruns, fatal=0).
M8 gate required to pass before any PASS verdict: `M8GATE PASS`
(5 perturbations × 2 reruns, artifacts byte-identical).

| leg | rc1/rc2 | stdout | notes |
|---|---|---|---|
| m1-1x-prose | 0/0 | IDENTICAL | 100.0/100.0, 84731 units, tierbad=0 |
| m1-1x-code | 0/0 | IDENTICAL | 100.0/100.0, 148678 units, tierbad=0 |
| m2-t1-prose | 0/0 | IDENTICAL | ETC=1, final 100.0/100.0, tierbad=0 |
| m2-t1-code | 0/0 | IDENTICAL | ETC=1, final 100.0/100.0, tierbad=0 |
| m2-t2-prose | 0/0 | IDENTICAL | ETC=1, final 100.0/100.0, tierbad=0 |
| m2-t2-code | 0/0 | IDENTICAL | ETC=1, final 100.0/100.0, tierbad=0 |
| m2-t3-1x | 0/0 | IDENTICAL | ETC=1, final 100.0/100.0, tierbad=0 |
| m3-1x | 0/0 | IDENTICAL | survival 100.0, fresh 100.0, CLEAR, 8050 mgmt, 50/50 weaken |
| m4-1x-prose | 0/0 | IDENTICAL | rev 100.0/100.0, kill 0.0, 1 episode |
| m4-1x-code | 0/0 | IDENTICAL | rev 100.0/100.0, kill 0.0, 1 episode |
| m5-1x | 0/0 | IDENTICAL | 1.811x memory/source-byte (bar FAIL), 16.19 audit/kb (bar FAIL) |
| m5-baseline | 0/0 | IDENTICAL | RSS baseline |
| m6-p2c-1x | 0/0 | IDENTICAL | recall 100.0, boundary 100.0, revision 100.0, tax 0.0, tierbad=0 |
| m6-c2p-1x | 0/0 | IDENTICAL | recall 100.0, boundary 100.0, revision 100.0, tax 0.0, tierbad=0 |
| memctrl-p2c-1x | 0/0 | IDENTICAL | drop 54.8 (≥15 gate PASS) |
| memctrl-c2p-1x | 0/0 | IDENTICAL | (control) |
| m7-1x | 0/0 | IDENTICAL | N/A (non-ID arm), re-read 319937 bytes |
| spoof-1x | 0/0 | IDENTICAL | **PROVISIONAL (A-57)**; see SPOOF_STATUS.md |
| M8 gate | — | — | **M8GATE PASS** (clean/frag/aslr/starve/freelist, all rc=0) |

M5 memory bars: FAIL is an honest datum, not a binding kill criterion for Z7
(the binding criteria are §3's two death clauses; neither fires). The 1.81x
and 16.19/kb values are validator-architecture-wide properties (b64-family
slot+ledger accounting), not a Z7 regression.

Full scorecard: `scorecard_z7_r1_1x.json`. M8 log: `M8_GATE.txt`.
