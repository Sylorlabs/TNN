# PAM Survivors — Governance Gaps (2026-09-25)

Everything below is awaiting Micah's signature. **No values invented.**
Preregistered test values are recorded as test values, not as defaults.

## Composition-level (B-3034X3)

- `QCAP=40`, `K_PIN=3`, `TOL_C=10`, `TOL_M=50` — test values; governance undecided (prereg §6).
- Gap seal (`th_mix(toyhash3(id,epoch,7919),t_g)`) — test value; governance gap-seal rule needed.
- `MAX_AGE=64` (+ `GCAP/LCAP/SCAP=64`) — test values.
- Sink `conf>=95` threshold — carried scope note (B-3034COMP §6); false G never promotes so the call site is unreachable there.
- Q0 liveness is SCOPE-CARRY; R0 carried with the construction proof (frozen C-R0: no reset symbol in API).

## Per-arm gaps

- **H-PAM-35**: CAP_NONCE/dom 7/8/sink structure are mechanism design, not governance-signed. Harness owns the private-construction barrier (Zag cannot make construction private).
- **H-PAM-36**: fresh-seed distribution/commitment policy is governance (unsigned). An attacker who learns the fresh world seed re-opens M-36.
- **H-PAM-33**: ENDORSE_KEY custody + endorsed-channel roster are governance (unsigned). Escape-(i) must be enforced externally.
- **H-PAM-30/34**: thresholds/tolerances are test values; sink conf>=95 gate value unsigned.
- **H-8**: force-pin policy for promoting the tripwire into any admission path is unsigned. Hybrid trust locus: TMB-5 scenes; 120 out-of-repertoire B/C spoofs committed-install UNCOVERED.

## WILD gaps (test values, not signed)

- W1: VOTE_THRESHOLD=650 load-bearing; DELIBERATION_BUDGET=8 arbitrary (flagged).
- W2: Advocate conf>=700 arbitrary-ish; both-must-agree load-bearing.
- W4: CAP=64 per-miss bound (existence load-bearing, value arbitrary); epoch cap 3 arbitrary.
- W6: N=3 unevidenced; predicate constants 3588/705 tuning.
- W7: suspicion threshold 600 (existence load-bearing, value calibration).
- W9: FIDELITY_THRESHOLD=0.55 load-bearing AND brittle (viable band 10,979–11,109).
- W11: L=6 chain cap arbitrary; CALIB_REG exact-match is a deployment constant; allowlist membership is registry-defined.
- W12: B=24814 value arbitrary (mechanism load-bearing). No MAX_AGE/gap-seal/sink parameters exist in any W1–W12 design.
- **W12 K1 premise failure**: K1-as-written trips on frozen-bar items [1124, 1126]; the old verdict recommends amending K1's premise to item-level accounting. **Needs Micah's word.**
- **W20 prereg inconsistency**: PREREG_W20 §2 R-AUTH `declprov≠class` clause conflicts with frozen K-ETB-4; the kill bar was given precedence by the implementer. **Needs a frozen-prereg amendment — Micah's word.**

## CU gaps

- All cutoffs are preregistered test values: WORTH speed <=12x, intro >=0.85, agreement >=0.90 (grok), P-HYB cost <=1.3x, ATTACKWIN +15 pts, C3xM1 bar >= max-2pts = 80.58%.
- Combined C3×M1 adoption HOLD (AUDIT-1 57.71%) remains open for Micah's word.
- F-A1 (500 new traps) and F-A5 (10k temporal stream) not run (preregistered omission; fixture-generation project in C3 track).
- `cu_query` maxrec=2048 is a flagged arbitrary HARNESS cap, not a mechanism limit.
