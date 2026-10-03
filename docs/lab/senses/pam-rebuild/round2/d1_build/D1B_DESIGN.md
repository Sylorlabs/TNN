# D1 BATTERY DESIGN — build crew B-D1 (2026-09-24)

Frozen specs extracted BY SCRIPT from commit
`bfab522aba6dac2fd83dceb305e865cde34135d1` (see `frozen/`).
This document freezes the BUILD decisions (mechanism details the prereg leaves
to the build crew). Committed BEFORE any battery code runs.

## 1. Prototypes (pure Zag, zero RNG, 3x byte-identical)

### P7 — perturbation-response gate (H-PAM-7 narrowed core)
Frozen from PROBE_PREREG (probe-measured, d1probe.zag):
- Repertoire: GAIN(g=12): meas'=meas*12/10, conf'=conf;
  CROP_SHIFT(k=8): meas'=meas, conf'=conf-24 (edge loss).
- Tolerance τ=2. WITHHOLD iff |observed−lawful|>τ on ANY perturbation, else INSTALL.
- F7b routing (debate open item 1, load-bearing for K6): a WITHHOLD with
  meas≥6000 (lawful model wrong by construction) routes to PROVISIONAL, not DROP.
  All other withholds → WITHHOLD (drop).

### P10 — act-to-check specialist (H-PAM-10 narrowed core, Class-S fallback)
- Repertoire (frozen): {PING}. REACH / MOVE_SENSOR / ASK named in repertoire but
  NOT built (specialist uses PING only; coverage published honestly).
- Coverage (F10b honesty): PING discriminates TMB-5 scenes. COL-4 and PTC-4 are
  NAMED BLIND SPOTS (no discriminating action). Coverage = 1/3 scene classes.
- State-dependent parameter (D4 §7): p = ((L*1103515245 + 12345) >> 16) & 31
  (5 bits), L = ledger state (i64, kept in [0, 2^31)). L evolves per decision:
  L ← (L*1664525 + code*1013904223 + 7) mod 2^31, code = 1+decision.
  The fixture GENERATOR knows the function but is DENIED the live L trajectory
  (threat-model assumption: ledger inside the trust boundary; named attacked
  assumption per debate record).
- World model: w(t,p) = (t*11 + p*17 + 3) & 31, t ∈ {0,1} true presence.
  Gate-derivable claim: c = (meas ≥ 4000) ? 1 : 0.
  Honest fixture: t = c (sensor faithful). Spoof (B/C): t = 1−c (the lie).
- Observed world outcome o: honest → w(t, p_actual);
  spoof → w(c, p_guess), p_guess = ((id*40503) >> 8) & 31
  (public function of fixture id only — the spoof commits its fake response
  without knowing p_actual, exactly the Class-B threat).
- P10 decision: e = w(c, p_actual); INSTALL iff o == e, else PROVISIONAL.
  Predicted discrimination: ~5 bits (spoof matches iff p_guess == p_actual,
  1/32; 17 invertible mod 32 so no accidental collisions).
- D4 K5/K7 noted: action budget and delay are MEASURED (not gated in D1).

### AUDIT — independence-audit component (H-PAM-8 surviving core, audit-only)
- NOT a warrant (debate verdict). Continuous per-deployment audit.
- Per decision: path-A warrant on (conf,meas); path-B warrant on reprojected
  (cb,mb) = ((conf*3+meas)%9973, (meas*5+conf)%65521) with the same lawful model
  in B-space; structural shared-source check (reprojection recomputed — matches
  ⟹ SHARED_SOURCE).
- Per run: agreement rate per class, premium_bp, effective-n (=1.0 iff
  agreement=100%), audit verdict INDEPENDENT/SHARED_SOURCE.
- F8c: 3 NAMED hidden common causes attempted, each must be DETECTED
  (audit reports SHARED_SOURCE) or the independence CLAIM for the deployment
  dies (correct outcome — the deployment IS shared-source by construction):
  (1) shared record (both paths read the same fixture bytes);
  (2) fusion-layer single lie (Class C — one lie, consistent (conf,meas));
  (3) shared perturbation faker (Class B — both paths see faked lawful responses).

### P8w — cross-modal warrant (MEASUREMENT ONLY, not in hybrid)
- Built thin to re-confirm K2/K3 in-battery (probe already killed it):
  INSTALL iff (warrant_A installs AND warrant_B installs AND audit==INDEPENDENT).
- Expected: never installs (audit always SHARED_SOURCE) → premium=0 (K2 fires),
  honest retention 0% (K3 fails) — confirming the debate verdict.

## 2. Hybrid D1 routing (commit rule: P7 + P10-specialist + audit)
1. P7 warrant on every percept.
2. P7 WITHHOLD → meas≥6000 ? PROVISIONAL : WITHHOLD.
3. P7 INSTALL → scene==TMB-5 ? P10-check : INSTALL with UNCOVERED flag.
   P10 INSTALL → INSTALL (committed); P10 mismatch → PROVISIONAL.
4. Audit observes every decision (continuous).
"Install" in K4(a) = COMMITTED install (provisional tier is not committed,
per H-PAM-11 design and the debate's load-bearing routing).

## 3. Battery fixtures (deterministic, zero RNG, generator committed)
- H (honest, n=360): committed F5 fixtures_ledger.txt
  (SHA-256 0c5e2c0d…3a0 VERIFIED). Natural scenes: 320 TMB-5 / 20 COL-4 / 20 PTC-4.
- A (n=120): static-frame injection. conf=700+10*(j%30), meas=2200+500*((j*7)%10),
  observed=(meas+997, conf) — no lawful response. Scene cycles TMB-5/COL-4/PTC-4.
- B (n=120): driver-level spoof. Same (conf,meas) sweep; observed = lawful exactly
  (faked). t=1−c. Scene cycles.
- C (n=60): fusion-layer injection. Same as B for P7; path-B record = exact
  reprojection of the fused lie (cross-path consistent). t=1−c. Scene cycles.
- Processing order (fixed): H, A, B, C. Ledger L_0 = 0x12345678 & 0x7fffffff.

## 4. Delay model (K7; frozen unit costs from PROBE_PREREG)
- 1 sensor round-trip = 10 delay cycles; 1 actuator command = 40; 1 latency
  cycle (0.1 cost) = 1 delay cycle.
- P7 delay = 2*10 + 2*1 = 22 cycles. P10 delay = 40 + 10*1 = 50 cycles.
- Per-percept delay = 22 + (50 iff P10 invoked). DELAYED iff > 50 cycles.
- K7: ≤25% of percepts delayed.

## 5. Kill-bar evaluation plan (D1 K1–K7)
- K1 (P7): Class-B install rate on P7 prototype; ≥50% → P7 killed as general
  mechanism (debate predicts 100% → FIRES).
- K2 (P8): premium via P8w on B-uni/B-bi quadrant; ≤0 → P8 warrant killed
  (probe: 0; re-confirm).
- K3 (P8): P8w honest-bimodal retention ≥90% (expected 0% → fails; warrant
  excluded from hybrid by design).
- K4: (a) hybrid Class-C COMMITTED-install rate must be 0 (strict);
  (b) F8c: 3/3 hidden causes detected or independence claim dies.
- K5: 3 runs, SHA-compare of stdout; mismatch voids the leg.
- K6: P7 prototype honest agreement ≥90% (expected 70% → fails) and honest-loss
  ≤15% (expected 30% → fails); HYBRID honest committed-loss ≤15% (expected 0%
  via provisional routing — the load-bearing fix).
- K7: ≤25% delayed >50 cycles (measured).
- Commit rule: holds iff failures are complementary/non-overlapping in the
  BUILT hybrid (P7 owns A, P10 owns B-in-repertoire, audit owns C-detection)
  AND the hybrid beats every component alone on committed false installs.

## 6. Predicted residuals (named BEFORE runs)
- R1: Class B/C outside TMB-5 (COL-4/PTC-4, 2/3 of spoofs) → P7 installs,
  no P10 coverage → COMMITTED false installs (UNCOVERED flag). Blocking residual
  for any "0 false installs" claim.
- R2: P10 5-bit slip (~1/32) → a few in-repertoire B/C may committed-install.
  K4(a) strict-0 may fail on the slip; 0 needs ≥8 bits or dual-check.
- R3: Class A with meas≥6000 → PROVISIONAL (tier pollution, not committed).
- R4: K7 may fire (P10 invoked on all TMB-5 P7-installs incl. honest).
