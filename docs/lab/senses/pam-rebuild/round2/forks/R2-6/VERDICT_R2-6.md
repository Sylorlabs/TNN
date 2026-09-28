# VERDICT R2-6 — Disjoint-corroboration PASS (HC-3/B)

**Final verdict: DEAD.** The DESIGN_R26.md "ALIVE (mechanism proven, engineering
incomplete)" claim was unverified, and on verification it does not survive:
its headline numbers do not reproduce, and the frozen build cannot be evaluated
against its own frozen prereg — while on the fixtures it CAN run, the kill-bar
analogs fail structurally. Full numbers in `evidence/METRICS.md`.

## What was done (2026-09-23, completion crew)

1. Read the frozen prereg (`preregs/PREREG_R2-6.md`), the unverified
   `DESIGN_R26.md`, and all five sources (built unchanged — no source edits).
2. Built `sense_r26` + `memgate_r26` with the pinned znc toolchain
   (sha256 `427e2dd9…` / `0314033…`, see `evidence/BUILD_INFO.txt`).
3. Ran the prereg's evaluation as far as the frozen build permits: 925 trials
   (370 primary + 370 noise + 185 adversarial) from the round-1 harness formats
   the binary consumes. Ran the sense sweep **3×**; outputs byte-identical
   (sha256 `af5dc8321851…`); memgate ledger independently verified 925/925.
   Approach A head-to-head run on identical fixtures.
4. Scored every bar that is evaluable; documented the rest as unevaluable.

## Load-bearing finding: the frozen evaluation cannot be executed on the frozen build

`sense_r26` exits `error=bad-size` on every R2A `.r2fx` F-span, all six tasks
(empirically demonstrated, see `evidence/R2FX_INCOMPAT.txt`):

- colordisc/colorconst need 128×64 RGB + header; R2A gives 6,144 / 13,824 raw
  bytes (patch pairs / no dims, no header).
- shapetrans needs 96×96 RGB + header; R2A gives 9,216 raw bytes (96×96×1).
- pitchdisc/timbredisc need `[sr][cnt]` + i16 with assumed tone/gap layout;
  R2A gives headerless i16 with a different tone layout.
- motiondir needs `[8,64,64]` + 98,304 RGB bytes; R2A gives 51,200 raw bytes
  (8×80×80×1 grayscale).

A translator would have to invent pixels or re-lay measurements — i.e.
redesign the measurement front-ends — a post-results build change, barred by
the frozen prereg ("No retroactive bar changes after results"). Therefore
**RK-1 (≤0.03/10,000), the frozen B4 (≥10% of R2A adversarial), the frozen B5
(≤3% on R2A), and the frozen RK-2/3/5 are unsatisfiable by this build.**
A fork whose prereg kill criteria cannot be run fails its prereg.

## Measured kill-bar analogs (harness 925 — fail structurally)

- **RK-2: 5/9 = 55.6% wrong-high-conf installed (bar ≤1%).** The timbredisc
  judgment vocabulary is only BRIGHT/DARK (frozen code, `sense_r26.zag:1814`),
  so every RICH truth is judged BRIGHT at high confidence and corroborates —
  systematic false installs, not fixture luck.
- **RK-3: 0/141 = 0% correct-high-conf PASS-and-install (bar ≥85%).** The
  memgate keeps one provisional/permanent slot per task (frozen code); once a
  wrong PASS installs provisionally, every later correct PASS is
  CONFLICT_WITHHELD forever. Structurally unreachable on interleaved streams.
- **RK-5: 3/9 = 33.3% wrong-high-conf → FAIL/UNRESOLVED (bar ≥90%).** Same
  timbredisc systematic PASSes as RK-2.
- **B5 analog: 37/925 = 4.0% false installs (bar ≤3%).** DESIGN itself admitted
  13.2% in its "simplified" run — it declared ALIVE while conceding a kill-bar
  failure.

## DESIGN_R26.md numbers: refuted, not merely unverified

Rerun on the only fixture set the frozen build consumes (370 primary):

| Task | DESIGN claim | Measured | Verdict |
|---|---|---|---|
| colordisc | 100% | 78.3% (47/60) | refuted |
| colorconst | 86.7% | 90.0% (36/40) | close |
| shapetrans | 45.0% | 40.0% (36/90) | close |
| pitchdisc | 100% | 100% (60/60) | confirmed |
| timbredisc | 50.0% | 50.0% (30/60) | confirmed |
| motiondir | 85.0% | 78.3% (47/60) | refuted |
| overall | 77.8% (280/360) | 69.2% (256/370) | refuted |

The 13-trial colordisc gap cannot be explained by the 370-vs-360 denominator.
B4 analog measured 34.1% changed / 60→37 false installs vs DESIGN's 21.7% /
27→7 — different experiment, not a reproduction.

## What passes (recorded honestly)

- B6: 3 byte-identical runs; hash-chained ledger verified 925/925. PASS.
- B1 analog: 69.2% ≥ 60% on harness primary. PASS (as an analog, not the
  frozen bar).
- B4 analog: contract changes 34.1% of adversarial decisions (≥10%) and
  reduces false installs 60→37. PASS (analog).
- RK-4 analog: 309 contractless installs ≥100. RK-6 analog: 0 escalations,
  p95 ops 24.6% of Approach A (≤40%). PASS (analogs).
- B2/B3 head-to-head vs Approach A (identical fixtures): R26 69.2% vs A 74.1%
  (Δ −4.9pp); R26 costs 24.6% of A's ops. The convergence claim (HC-3 vs HC-1)
  is therefore: same-or-lower compute, but LOWER accuracy and no R2-4
  head-to-head was possible on the frozen suite — informational, and it does
  not support convergence.

## Verdict rationale

DEAD per the frozen kill criteria, on two independent grounds:
1. **Unevaluability:** the frozen R2A evaluation cannot run on the frozen
   build (fixture-format incompatibility, all six tasks); the prereg's kill
   criteria are unsatisfiable. No retroactive rescoping is permitted.
2. **Structural kill-bar failures on measurement:** RK-2, RK-3, RK-5 and the
   B5 analog fail as code properties (timbredisc judgment vocabulary;
   single-slot gate), not as fixture accidents — they would fail on any
   fixture suite.

The DESIGN_R26.md "ALIVE" claim is withdrawn: unverified at commit, refuted on
rerun, and self-contradictory (it admitted B5 13.2% > 3% while declaring
ALIVE). What survives as ideas for future work — the disjoint-corroboration
PASS rule and the hash-chained memgate — would need a fresh build against a
fixture suite it can actually consume, under a new prereg. That is new work,
not a rescue of this fork.

B7: PENDING-MICAH (no sensory artifacts produced).

## Evidence

`evidence/`: `sense_raw_run{1,2,3}.log` (byte-identical ×3),
`records.txt`, `dispositions.txt`, `ledger.txt` (+ independent verification),
`sweep.jsonl`, `metrics.json`, `byte_identity.json`, `ledger_verify.json`,
`approach_a.json`, `eval_r26.py` (harness), `METRICS.md`, `BUILD_INFO.txt`,
`R2FX_INCOMPAT.txt`.
