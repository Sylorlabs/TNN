# Round 3 Verdict — head-to-head, frozen bars

Prereg: `PREREG_R3.md`, frozen+committed as `db591cb9` before any
implementation. Sources: `src/azgen_c1.zag`, `src/azgen_c3.zag`
(C2 void — no source). Implementers read the prereg first, ran BAR 0 on
pristine-azgen recompiles (both passed: committed baseline SHAs + all 11
PSNRs reproduced), byte-proofed every image (2 runs, SHA-256 identical),
and committed nothing. Scratch deleted by the implementers.

Baseline (generation PSNR dB): bridge 18.47, sky 22.75, fabric 21.47,
woodgrain 18.37, treebark 18.94, calmwaters 19.46, portrait 21.19,
car 22.92, building 14.96, cat 16.60, market 18.36.

## C1 — fit-licensed construction: FAILS BAR 1 (dead)

| image | base | C1 | Δ |
|---|---|---|---|
| bridge | 18.47 | 20.00 | +1.53 |
| sky | 22.75 | 26.27 | +3.52 |
| fabric | 21.47 | 21.47 | 0.00 |
| woodgrain | 18.37 | 18.86 | +0.49 |
| treebark | 18.94 | 21.26 | +2.32 |
| calmwaters | 19.46 | 20.06 | +0.60 |
| portrait | 21.19 | 22.63 | +1.44 |
| car | 22.92 | 24.12 | +1.20 |
| building | 14.96 | 14.60 | **−0.36** |
| cat | 16.60 | 17.08 | +0.48 |
| market | 18.36 | 19.38 | +1.02 |

Mean Δ +1.11 (≥+0.50 ✓), wins 10/11 (≥8 ✓), group means all ≥ 0 ✓ —
but building −0.36 dB < −0.15 dB single-image floor ✗. BAR 1 FAILS.
BAR 2 (originals) passed (+1.53, +3.52). Dead; no tuning per prereg.

Mechanism reading (from the trace): on bridge/sky/market the gate refused
*every* take → SHAPES reverted → LINES-on-raw-input + mean fill — that is
where the big gains come from. The gate worked as diagnosed (killing
overconfident stamps under ambiguity), but the frozen 4×/2× bars are not
sufficient on building: 20 licensed takes stamp texture that hurts.

## C2 — lineage-vouched cascade: VOID

Per-atom source-image provenance exists only in the human-readable
`TEACH_TRACE.txt`, never in the VOC2 binary format `g_vocab_load` reads
(3-way byte-exact audit: header + packed layout sums to exactly the file
size — zero room for per-atom metadata). The frozen battery never loads the
text trace. Prereg's void condition triggered; no workaround. A revival
would need a VOC3 vocab format — out of scope for this round.

## C3 — TNN-deliberated operator choice: PASSES BAR 1, BAR 2, BAR 3

| image | base | C3 | Δ |
|---|---|---|---|
| bridge | 18.47 | 19.74 | +1.27 |
| sky | 22.75 | 23.89 | +1.14 |
| fabric | 21.47 | 21.47 | 0.00 |
| woodgrain | 18.37 | 20.05 | +1.68 |
| treebark | 18.94 | 20.51 | +1.57 |
| calmwaters | 19.46 | 20.08 | +0.62 |
| portrait | 21.19 | 22.32 | +1.13 |
| car | 22.92 | 24.43 | +1.51 |
| building | 14.96 | 15.24 | +0.28 |
| cat | 16.60 | 17.19 | +0.59 |
| market | 18.36 | 19.07 | +0.71 |

Mean Δ **+0.955 dB** (≥+0.50 ✓), wins **11/11** (≥8 ✓), worst Δ 0.00
(fabric tie, not a loss) ✓, every category-group mean ≥ 0 ✓ →
**BAR 1 PASS**. BAR 2 (originals +1.27, +1.14) **PASS**.
BAR 3 (native choice): pooled operator shares PLANE 85.7%, MEAN 10.6%,
ATOM 3.7% — two operators each ≥5% with per-region evidence+choice+reason
traces → **PASS**.

Honest build note (pre-scoring, reported by implementer): a bridge smoke
run exposed two bugs — LS-plane denominators missing cross factors
(4×-steep planes) and operator-honest gain leaking into recursion. Both
fixed BEFORE any valid scoring; proven by a forced-ATOM probe reproducing
baseline bridge+sky byte-identically and an independent Python oracle
recomputing the LS-plane fit and 48/48 rendered pixels for two bridge
regions. No tuning after valid scoring; frozen thresholds untouched.

Mechanism reading: PLANE dominates (85.7%) and carries the gain — the
prereg's diagnosis that the plane was underused is confirmed. ATOM is
nearly dormant (3.7%) under the frozen gate; the stamp path barely earns
its keep. PLANE is a pure measured operator (no learned atoms) — the win
is deliberated construction, not vocabulary magic.

## Head-to-head

| arm | mean Δ | wins | worst Δ | BAR 1 | BAR 2 | BAR 3 | verdict |
|---|---|---|---|---|---|---|---|
| C1 | +1.11 | 10/11 | −0.36 (building) | FAIL | PASS | n/a | DEAD |
| C2 | — | — | — | — | — | — | VOID |
| C3 | +0.955 | 11/11 | 0.00 (fabric tie) | PASS | PASS | PASS | WINNER → red team |

## Next

Independent red team on C3 from committed source (below): close-call
inputs, category-shift traps, operator neutering (especially ATOM at
3.7% — does it affect output at all?). A z.ai second-opinion question on
this verdict is queued for the overnight relay. If C3 survives red team,
round 3 ships a genuine broad win: the first TNN-deliberated construction
operator in the upscale line.
