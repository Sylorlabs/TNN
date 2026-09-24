# VERDICT — g1 archived rival-filler precedence, production build

**Date:** 2026-09-24. **Prereg:** `PREREG_G1.md` (frozen before the build ran).
**Binary:** `g1_bin`, built from `g1.zag` with the pinned znc toolchain
(`znc_linux_x86_64_abed8aa1`); imports `R33_NATIVE_IO_V1.zag` +
`R33_NATIVE_SHA256_V2.zag` (copies vendored in this dir).

## Verdict: PASS — all 8 kill bars hold

| ID | Bar | Result |
|----|-----|--------|
| K1 | F1_sydney + pinset v1 → WITHHOLD\|ARCHVETO, 2 reps byte-identical | PASS — `V\|g1\|WITHHOLD\|ARCHVETO\|4\|-1` (t1d=4 canberra, no runner-up), rep1==rep2 |
| K2 | 12/12 honest → PASS, no veto, 2 reps byte-identical | PASS — 12/12 `V\|g1\|PASS\|NONE\|0\|0` |
| K3 | T4_supersede + pinset v2 (era-2) → PASS | PASS — era-split lets the honest capital move through |
| K4 | T4_supersede + pinset v1 (stale) → WITHHOLD\|ARCHVETO | PASS — the pin-discipline cost, quantified and expected |
| K5 | Determinism: every case ×2 byte-identical | PASS — 22/22 rows rep1==rep2 on full stdout |
| K6 | Zero RNG in the decision path | PASS — grep audit: no rng/random/seed/clock in `g1.zag`; only syscalls are open/read/close on the fixed pin file; `ns_sha256` is a pure function |
| K7 | Tampered pin → WITHHOLD\|PINFAIL everywhere, never PASS | PASS — one flipped digest hex digit rejects the whole set; 3/3 claims PINFAIL |
| K8 | Parity with probed `beyond.zag` g1 rows | PASS — F1_sydney ARCHVETO / T4 INSTALL / F_H_WIRE INSTALL / 0 honest ARCHVETO rows, decisions match on all |

Extension probes: G1-FORM2 ("The capital of Australia is Sydney.") → ARCHVETO
(both surface forms covered); G1-MERCURY → PASS (multi-template inventory);
G1-NONCLASS → PASS (closed-class scoping; no template = no veto).

## What the build adds over the probe

1. **Versioned, content-addressed pins.** Every REC carries sha256 over
   canonical bytes `template|filler|era|domains`; ENDSET digests the whole set.
   The loader re-verifies all digests before accepting — independently
   recomputed in Zag (the digests were generated in Python; agreement is itself
   a cross-implementation check).
2. **Fail-closed pin discipline** (K7): broken pins → WITHHOLD|PINFAIL, never
   silent pass-through.
3. **Era-split roll governance** (`PIN_ROLL_LOG.md`): v1 → v2 adds era-2
   without rewriting era-1; two-generation confirmation required before any
   roll that moves a dominant filler.
4. **Frozen normalization before parse**: the probe parsed already-normalized
   sentences; the production stage normalizes the raw claim itself
   (lowercase ASCII, punct→space, controls dropped — byte-identical to the
   probe's `normalize`). Caught during build: without this, template lookup
   silently misses ("capital of Australia." ≠ "capital of australia").
5. **Standalone stage**: veto-only pre-filter (`tentative` must be INSTALL;
   g1 can only downgrade, never upgrade).

## Battery log

`BATTERY_LOG.txt` — 22/22 rows, 0 failures.

## Accepted residuals (unchanged from round 2)

S3 (no prior filler) silent; S1 (archived filler IS the falsehood) certifies;
S2 new events silent; impatient-only (patient pre-dating attacker wins, forced
into the harder S3 game); live archive APIs stay out of the decision path.
