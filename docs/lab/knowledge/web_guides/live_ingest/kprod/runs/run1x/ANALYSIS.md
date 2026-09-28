# KPROD analysis — 1x mode
outdir: run1x
battery: battery1x
KP1 inputs: K hk installs 12/12, sk installs 0/12
pass-agreement K verdict classes identical: True

## Kill bars
- KP1: PASS — K hk 12/12 INSTALL; K sk 0 installs (bar: 12/12, 0)
- KP2: PASS — K fn PENDING 8/8, INSTALL 0 (bar: 8/8, 0); N fn INSTALL 8/8 (frozen documents the closed hole)
- KP3: PASS — K sk installs 0; pf re-ingest installs 0 (bar: 0, 0)
- KP4: PASS — PROMOTED 4/4; pn-b INSTALL>12 True; RESOLVED_FALSE 8/8; pf re-ingest WITHHOLD True; AUTO_FALSE 4/4; AUTO_PROMOTED 4/4; pc-b INSTALL>12 True; pn-05..08 held True; pc pendings cleared True; done=True void=None
- KP5: PASS — hn K withhold 8/8, N withhold 8/8 (bar 8/8 both); admission audit: 32 K PENDING entries, 0 without N INSTALL
- KP6: PASS — pass1==pass2 byte-identical
- KP7: PASS — pass1: verdict_cmp IDENTICAL, installed.txt IDENTICAL; pass2: verdict_cmp IDENTICAL, installed.txt IDENTICAL

verdict: PASS (7/7 bars pass)
