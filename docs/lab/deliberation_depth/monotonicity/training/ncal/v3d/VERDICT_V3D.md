# VERDICT — NEC v3d: m20 vs Design S head-to-head

- **Date:** 2026-09-25 (PDT).
- **Prereg:** `PREREG_NCAL_V3D_H2H_FROZEN.md` (`695997f5`) + Amendment A1
  (`4df783f9`). **Runlog:** `RUNLOG_V3D.md`.
  **Decision table:** `DECISION_TABLE_V3D.md` (no aggregate score, per prereg).
- **Contenders:** variant 20 (adopted m20: personal-only, d1prior=0.95,
  per-item min latch) vs variant 26 (Design S: released-conditioned exact
  (f1,f5,depth) schema, 312 L1 cells, L1→L4 backoff), same frozen binary,
  identical inputs, 3× byte-identical runs throughout.

## Recommendation

**Adopt Design S + FIX1** (FIX1 applies now per Micah's ~11:50 UTC ruling
and Amendment A1; FIX-A pure-Zag port likewise dispatched).

## Why — dimension by dimension

**SPEED: tie.** The sequential medians and the drift-cancelling
interleaved medians contradict each other (v26 12–19% slower vs 23%
faster) — textbook machine noise on a shared 2-core VM. The reliable
number is the mechanistic bound: S's schema lookup adds ≤312 integer
comparisons on an item's FIRST observation only, against a ~30 µs/row
baseline — under 1%, unresolvable. There is no speed cost to the schema.

**COST: m20, by a small fixed margin.** S carries a 20,520 B static
schema (~+126 KB resident code pages at small scale, ~0 at s10+) and
+1.6–2% audit bytes (7-char `1000000` confs vs 6-char `950000`). The
ledger is identical (88 B/item), the projection walls are equal within
noise, and the schema cost is FIXED — at 1M items it is 0.02% of the
ledger. This margin is real but negligible at scale.

**CATCHES: S, uniformly.** No blowout — but also no counter-evidence
anywhere:
- 17 red-team batteries: binary catches IDENTICAL (zero asymmetric rows),
  yet S's mean|err| is lower on 16/17 (−1% to −17%). Better calibration,
  not luck — the schema seeds are per-class honest values where m20 can
  only emit its constant.
- T1 (latch dynamics): tie — both follow stated rules exactly (150/150),
  both crater honestly, zero sparing, same B13 cost.
- T3 (unseen classes): S wins 0.3812 vs 0.4700, PASS vs FAIL, by honest
  mechanism — trace-verified L3 backoff (0.802) on every unseen class,
  against m20's 0.95-on-unseen. This is the forward-looking metric: the
  knowledge-first future Micah ordered is ABOUT unseen classes, and S is
  the only contender whose machinery treats "I haven't seen this" as a
  distinct, honest state.

## The judgment

The cost margin for m20 is fixed and tiny; the catches margin for S is
mechanism-explained and points at the future. A constant can never learn
that it hasn't seen something — S's backoff hierarchy is exactly the
machinery the unseen-class calibration work needs. Speed is a tie, so it
doesn't arbitrate. **S wins the dimensions that can grow; m20 wins the
dimensions that are already floored.**

## Residuals (what S does NOT fix — carried openly)

1. **RT-B latch inversion (B5 ≈ −0.10):** both contenders carry it; S's
   trace shows the identical inversion shape as m20's. The schema changes
   the seed, not the latch. Still needs its own fix.
2. **RT-F 63-byte ID cap:** both miss the same 30 rows pre-FIX1. FIX1 is
   dispatched and applies to the adopted mechanism now (Amendment A1) —
   it flips both to catch, tie preserved.
3. **No new binary catches:** S catches nothing on the red-team batteries
   that m20 misses. Its advantage is calibration + unseen-class honesty,
   not trap-breaking.
4. **The schema is hand-built knowledge** (312+246+7 cells). The bytes are
   cheap; the knowledge-engineering is the real price. The knowledge-first
   line (TNN learning schemas itself, not hand-building them) is where
   this cost goes to zero — and S is the machinery that can USE learned
   schemas, which m20's constant cannot.

## What adoption commits Micah to

1. **S + FIX1 as the NEC production rule** (variant 26 semantics on the
   fixed id-compare).
2. **The schema as a living artifact:** versioned, audited, and
   eventually LEARNED rather than hand-built (knowledge-first line).
3. **m20 kept as the simplicity baseline** — the constant+latch remains
   the fallback and the cross-check, not deleted.
4. **The open residuals stay open:** RT-B inversion needs its own fix;
   RT-F is closed by FIX1; T3's remaining 0.38 is the honest-backoff
   floor, improvable only by real knowledge (the ceiling-composition v2
   already dispatched).

## Evidence

- `RUNLOG_V3D.md` (§0 gate, §2 speed, §3 cost, §4 catches, §5 SHA logs)
- `DECISION_TABLE_V3D.md` (per-dimension margins, no aggregate score)
- `work/speed/` (6 legs ×3, interleaved validation, S2 trace)
- `work/cost/` (RSS, output bytes, C5 projection)
- `work/catches/` (46 legs ×3, bars, asymmetry, t1_h2h, t3_h2h, traces)
- Scripts: `crew_speed.sh`, `crew_cost.sh`, `crew_cost_resume.sh`,
  `crew_catches.sh`, `crew_catches_resume.sh`,
  `analysis/{t3_h2h,asymmetry,t1_h2h,rss_one,rss_harness}.py`
