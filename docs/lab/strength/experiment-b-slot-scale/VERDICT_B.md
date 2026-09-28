# VERDICT B — Slot scale: 14 / 28 / 56 / 140 user slots

**Question (Micah, 2026-09-25):** "How expensive is it to scale up slots and
have you tried it?" Nobody had. The strength core ran 14 user slots since
birth; this is the first variation of strength-store slot capacity.

**Law context:** recycle fork at `5610c1215d7f` (hole-1 trainer-gated
st_kill, hole-2 delete-never-recycles, high-water erase pricing, F4b
single-use cites, B2 arm, P2+P3). Cite-mode switch (W/G/H) ported in via
`merge_citemode.py`; W is default and the W path of `st_cite_consumed` is
the base-commit body verbatim. Base-vs-merged W-mode law equivalence proven
byte-identical (FUNC/14, re-verified after every driver rebuild).

**Scale verdict: PASS — no degradation on any metric, 14 → 140 slots.**
Memory grows strictly linearly (+31 bytes/slot); add/cite/destroy/checker
per-op costs are flat; the F6 global-citation wedge cliff scales linearly
with capacity (same law, more slots — predictable, not a rot).

## 1. Memory (BYTES leg, audit_cap=32768 fixed)

| user slots | slot_cap | total alloc (B) | Δ vs 14 | largest single alloc |
|---:|---:|---:|---:|---:|
| 14 | 16 | 2,753,008 | — | 688,128 |
| 28 | 30 | 2,753,442 | +434 | 688,128 |
| 56 | 58 | 2,754,310 | +1,302 | 688,128 |
| 140 | 142 | 2,756,914 | +3,906 | 688,128 |

Growth is exactly **+31 bytes per user slot** (the 13 slot arrays:
1+4+1+1+1+4+1+1+4+1+4+4+4). The audit ledger dominates (4 × 688,128 =
2,752,512 B, chunked under the znc 2^25 ceiling by construction).
Largest single allocation 688,128 B « 33,554,432 B ceiling (`ceil_ok=1`
all configs). **Memory: no degradation — strictly linear, audit-dominated.**

## 2. Per-op cost (COST leg; CPU-time medians, 21 batches, 2 rounds)

Method note: wall clock measured scheduler noise on this shared VM
(real=72s vs user=3.2s on the first attempt), so the cost clock is
CLOCK_PROCESS_CPUTIME_ID. Timing is cost measurement only, never mixed
into functional evidence. Medians in ns (r1 / r2):

| op | 14 | 28 | 56 | 140 | 140÷14 |
|---|---:|---:|---:|---:|---:|
| add_empty | 1,859 / 2,979 | 2,032 / 1,877 | 1,947 / 1,936 | 2,263 / 1,880 | ~1.1× |
| add_fullscan (refused) | 2,111 / 3,038 | 2,209 / 2,710 | 2,527 / 2,275 | 2,545 / 2,764 | ~1.2× |
| cite | 5,926 / 6,004 | 5,982 / 5,819 | 6,240 / 6,047 | 6,013 / 6,450 | ~1.0× |
| priced destroy | 43,397 / 44,338 | 47,048 / 45,580 | 44,965 / 44,681 | 44,316 / 45,876 | ~1.0× |
| checker (323-entry ledger) | 29.7ms / 29.3ms | 30.2ms / 29.4ms | 29.8ms / 28.6ms | 29.8ms / 28.7ms | ~1.0× |

**Per-op: no degradation.** add_empty ≈ 2µs, cite ≈ 6µs, priced
destroy ≈ 45µs, all flat 14→140. add_fullscan's 1.2× is the honest
linear term (a refused ADD scans all slots: 142 trivial iterations at
140 slots). The checker is flat across slot counts on the identical
323-entry ledger — the slot-array scan is negligible next to ledger
verification at these scales.

## 3. Checker vs ledger size (CKL leg; honest curricula, 5 passes × 21 rounds)

| slots | episodes | ledger entries | checker median |
|---:|---:|---:|---:|
| 14 | 50 | 163 | 11.4 ms |
| 14 | 100 | 323 | 28.6 ms |
| 14 | 200 | 693 | 102.4 ms |
| 14 | 400 | 1,383 | 332.7 ms |
| 140 | 50 | 163 | 11.0 ms |
| 140 | 100 | 323 | 29.4 ms |
| 140 | 200 | 693 | 101.0 ms |
| 140 | 400 | 1,383 | 327.9 ms |

Two clean findings. **Slot count contributes nothing**: at fixed ledger
size, 14 vs 140 slots agree to within 3% on all four ledger sizes — the
slot-array scan is unmeasurable next to verification work. **Ledger size
is the cost driver, and it is superlinear**: 163→1,383 entries (8.5×)
takes checker time 11.4→332.7 ms (29×), i.e. roughly n^1.6 — consistent
with the per-destruction evidence-window scans inside `ck_verify`.
Caveat: absolute ms drift ~1.5× between sessions on this shared VM (an
ad-hoc 14/50 run measured 7.4 ms vs the battery's 11.4 ms); the
within-battery ratios above are the reliable signal.

## 4. Ledger growth (FUNC leg, 400 episodes, byte-identical ×2)

| slots | ok destroys | audit entries | entries/episode | ledger bytes/episode |
|---:|---:|---:|---:|---:|
| 14 | 196 | 1,383 | 3.45 | ~290 |
| 28 | 196 | 1,383 | 3.45 | ~290 |
| 56 | 176 | 1,283 | 3.20 | ~269 |
| 140 | 140 | 1,103 | 2.75 | ~231 |

(~3.4 entries/episode; 84 bytes/entry. The per-episode dip at high slot
counts is workload, not scaling: the fixed 400-episode rotation visits
each slot less often, so fewer destroys happen. ckfail=0, replay clean,
refusals-hygiene clean on all 8 runs.)

## 5. F6 global-citation wedge (G mode; P = finite salient pool)

Blind rotating cites over a finite pool; each slot sustains exactly P/4
priced destructions, then one 121-consumed refusal clogs it forever;
after all slots clog, ADD→REFUSED_FULL wedges the store. Measured
(12/12 cells byte-identical ×2, checker clean throughout):

| slots | P=8: ok / wedge@ | P=16: ok / wedge@ | P=32: ok / wedge@ |
|---:|---:|---:|---:|
| 14 | 28 / 42 | 56 / 70 | 112 / 126 |
| 28 | 56 / 84 | 112 / 140 | 224 / 252 |
| 56 | 112 / 168 | 224 / 280 | 448 / 504 |
| 140 | 280 / 420 | 560 / 700 | 1,120 / 1,260 |

Law: **ok destructions before clog = slots × P/4**; refusals = exactly
one 121 per slot; first refusal at iteration P/4 (2/4/8); full wedge at
slots×(P/4+1). The 14/P=8 cell reproduces the F6 core's own measurement
(28 ok, 14×121, wedge@42) exactly — the ported G branch is faithful.
**Wedge: no rot — the cliff scales linearly with capacity.** It is the
same law at every scale; G mode remains a deliberate adversarial
instrument, not the default (W).

## 6. Hygiene

- Functional runs byte-identical ×2: BYTES (4), FUNC (4), WEDGE (12),
  all `cmp`-clean.
- W-mode base-vs-merged equivalence: byte-identical (×3, after every
  driver rebuild).
- Checker clean at every scale: ckfail=0 on all 44 functional runs.
- Zero RNG anywhere; pure Zag; deterministic given state.
- No allocation ≥ 33,554,432 bytes on any run.

## Bottom line

The strength store's first capacity variation shows **no scale-rot from
slots**: memory +31 B/slot, per-op costs flat to 140 slots, checker cost
independent of slot count, and the adversarial citation wedge scaling
linearly with capacity as the law predicts. The honest binding cost at
scale is **ledger length** (checker ~n^1.6 in entries), not slots — worth
knowing, but it is a property of the verification law, not of capacity.

Evidence: `evidence/{bytes,func,cost,wedge,ckl}/` (raw logs, checksummed
in CHECKSUMS.md). Code: `code/` (driver, merged core+checker, merge and
build scripts). Method: RUNLOG.md.
