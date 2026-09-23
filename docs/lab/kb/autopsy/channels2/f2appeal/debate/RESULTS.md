# F2 appeal battery — RESULTS (post-result debate input)

Mechanical verdict rule (§6): RECOVERY fires iff bits > 0.15 AND false-install < 0.15
on pooled TEST (per-sense reported; either sense counts), 2× byte-identical, 0 cross-check errors.

## Two-run integrity
- G0 gate: PASS — 370/370 frozen judgment+confidence reproductions, pass1==pass2 byte-identical.
- All 14 members: run1/run2 verdict files byte-identical; generation SHA256 manifests byte-identical; 0 voided members.
- Scorer: pure-Zag counts vs independent Python recompute — 0 mismatches across all 14 members.
- H(Y) prior on TEST: 0.9958 bits.

## R1 — noise-amplitude sweep (C3 idea, 7 levels; 184 TEST rows/member)
| Level | Amplitude | pooled bits | false-install | A bits | B bits |
|---|---|---|---|---|---|
| L0 | ±50 pcm / ±1 img | 0.0184 | 0.453 | 0.0132 | 0.0228 |
| L1 | ±100 / ±2 | 0.0144 | 0.449 | 0.0266 | 0.0093 |
| L2 | ±200 / ±4 | 0.0246 | 0.443 | 0.0266 | 0.0258 |
| L3 | ±300 / ±8 | 0.0215 | 0.439 | 0.0541 | 0.0100 |
| L4 | ±600 / ±16 | 0.0296 | 0.420 | 0.0252 | 0.0314 |
| L5 | ±1200 / ±32 | 0.0006 | 0.456 | 0.0010 | 0.0033 |
| L6 | ±2400 / ±64 | 0.0044 | 0.447 | 0.0010 | 0.0165 |
NULL at every level. No amplitude separates fooled from correct judgments; L5–L6 collapse toward 0 bits as predicted (near-universal WITHHOLD).

## R2 — multi-draw majority (N=5; 184 TEST rows/member)
| Config | pooled bits | false-install | A bits | B bits |
|---|---|---|---|---|
| L3 (majority of 5 @ ±300/±8) | 0.0173 | 0.442 | 0.0402 | 0.0100 |
| L5 (majority of 5 @ ±1200/±32) | 0.0000 | 0.463 | 0.0010 | 0.0001 |
NULL. L5 majority is a near-constant function (bits = 0.0000), as the PRO camp's mechanics predicted.

## R3 — alternative transforms (C2 idea, new T family)
F3 validity gates (≥95% calibration legibility), identical both runs:
- vflip: A PASS 48/48; B VOID 37/48 (0.7708) — vertical flip breaks sense-B legibility.
- signflip: A PASS 30/30; B PASS 30/30.
- fshift: A VOID 4/15; B VOID 6/15 — half-frame shift destroys legibility both senses.
Involution T(T(x))==x byte-verified on every applicable fixture, 0 failures.

| Transform | pooled bits | false-install | A bits | B bits | valid cells |
|---|---|---|---|---|---|
| vflip | 0.0203 | 0.511 | 0.0000 | 0.0374 (VOID cell) | (A,vflip) only |
| signflip | 0.0000 | 0.283 | 0.0000 | 0.0000 | (A,sf), (B,sf) |
| fshift | 0.0002 | 0.643 | 0.0348 (VOID) | 0.0258 (VOID) | none |
On every VALID (sense, transform) cell the C2-redux agreement is perfect: J(T(x))==L(J(x))
everywhere measured → 0.0000 bits (A,vflip; A,signflip; B,signflip). The DPI identity
extends to the new transform family. VOID cells excluded per the frozen rule.

## R4 — structured noise (184 TEST rows/member)
| Variant | pooled bits | false-install | A bits | B bits |
|---|---|---|---|---|
| V1 block/frame-correlated | 0.0102 | 0.443 | 0.0541 | 0.0012 |
| V2 ternary {-A,0,+A} | 0.0167 | 0.436 | 0.0340 | 0.0076 |
NULL both variants.

## Bottom line
14/14 members NULL. Maximum pooled bits 0.0296 (R1-L4); maximum per-sense bits 0.0541
(R1-L3 sense A) — 2.8× below the 0.15 bar. False-installs range 0.267–0.714, all far
above the < 0.15 requirement (lowest: R3 signflip at 0.283, with bits at 0.0000).
The frozen mechanical rule (§6) yields: **WRAPS**. No RECOVERY fired.
