# VERDICT — Arm Z2 (contract chunks), Track A closeout

**Date:** 2026-09-21
**Arm:** Z2 — Contract chunks (ECON family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PASS** (survives all binding criteria)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Breach-detection rate < 80% on the misuse battery — Z2 is theater; OR >30% of legitimate recall ops refused as breaches — restrictions unusable (kill the restriction half, keep obligations). Hot-path characterization required (znc miscompile history).

## Kill-criterion evaluation

### Clause 1 — Breach-detection rate < 80% on the misuse battery

Mode `z2-misuse-1x` (9,000 misuse probes: forbidden purposes per class,
expired-chunk recall, tombstone recall):

```
Z2MISUSE,100.0,0.0,9000,165,PASS,PASS
```

- Breach-detection rate = **100.0%** (9,000/9,000 misuse probes detected).
- Bar: < 80% kills. 100.0% ≥ 80%. **Clause does NOT fire.**

### Clause 2 — > 30% of legitimate recall ops refused as breaches

Same mode, 165 legitimate probes (permitted purposes on live unexpired
chunks; legit phase runs before any misuse REFUSE entries so the battery's
own logging cannot expire the legit sample):

- Legitimate-refusal rate = **0.0%** (0/165 refused).
- Bar: > 30% kills the restriction half. 0.0% ≤ 30%. **Clause does NOT fire.**

### Hot-path characterization (required, znc miscompile history)

Mode `z2-hotpath-1x` + `docs/HOTPATH.md`: 20,000 recalls through the
checker, decision log sha256-hashed
(`611a114be17c52d73005a174216601aa605b8a578eaceb6712e742bd90dbd1aa`),
in-process self-check re-run, checker-call counting, M8 frag/aslr
determinism evidence. Present and passing.

## Evidence trail

- Full 1x battery: `evidence/r1_1x/STATUS_all.txt` — 19 legs (m1–m7, m8
  variants, memctrl, z2-hotpath-1x, z2-misuse-1x) × 2 runs; every leg
  rc1=0 rc2=0, stdout byte-identical, fatal=0.
- Misuse battery stdout: `evidence/r1_1x/z2_misuse_stdout.txt`.
- Hot-path stdout: `evidence/r1_1x/z2_hotpath_stdout.txt`.
- M8 gate: `evidence/r1_1x/M8_GATE.txt`.
- Scorecard (metrics-v1): `evidence/r1_1x/scorecard_r1_1x.json`
  (m1 100.0/100.0 both corpora; m2 ETC=1; m3 survival 100.0; m4 100/100;
  m5/m6/m7/m9 recorded).
- Spec + kill semantics: `docs/ARM_SPEC.md`, `docs/BUILD_NOTES.md`,
  `docs/HOTPATH.md`.

## Notes

- Z2 is a non-ID arm by design (contract table indexed by slot, derived
  from the ID like b64): M1 swap probe N/A, M7 N/A — documented in
  ARM_SPEC.md, not a gap.
- 10x: NOT ATTEMPTED (per task rules, 10x follows 1x bars; 1x bars pass).

**Result: Z2 PASS — no binding kill criterion fires.**
