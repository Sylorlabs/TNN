# H1EVO crew status (2026-09-24)

## C12 (C1/C2) — COMPLETE 2026-09-24 20:41 UTC
- C1: rule-A (pin mass=0) and rule-B (deliberate pins only) BOTH SURVIVE C1a'/C1b'.
  Rule separation confirmed via deliberate-pin probe (mode 3): rule-A refuses,
  rule-B promotes with pin deciding. Auto-pins refused under both.
- C2: breakers (a) carryover, (b) escalation budget, (c) rising discount ALL
  SURVIVE C2a'/C2b'. Resolution: (a) ep2/r1, (b) ep3/r3 (routes to review),
  (c) ep2/r2. LH 10x/100x prefix-consistent, zero false quarantines.
- LH caught a real defect: gate inherited organ pin-budget (MM_MAX_PIN=16)
  refusal → legit promotions refused under sustained auto-pinning (storage
  gating truth). Budget check removed from GATE only; organ law untouched.
- ZD: ob_test_mem/pam/arbiter/fl2 all OB_FAILURES=0 vs untouched sources.
- 15/15 modes 3x byte-identical, zero RNG.
- Evidence: ~/workspace/h1evo/c12_gate/evidence/ (strip .zag-cache/ *_bin before commit)

## V1 (R1 novelty) — RUNNING (948fcb07)
## L14 (L1-L4 ledger) — RUNNING (97f48dd7)
## V2 (R3 namespaces) — RUNNING (40580b08)

## V1 (R1 novelty) — COMPLETE 2026-09-24 20:49 UTC
- H-organ (PAM owns novelty via PAM_CONTRA register + pam_is_novel) and
  H-arbiter (arbiter-side register): BOTH SURVIVE R1a'/R1b'/R1c' (killbars 0,
  OB_FAILURES=0, 3x byte-identical).
- Build bug caught: novelty query must precede arb_pam_claim's row append
  (first build withheld novel r1b) — fixed/verified.
- ZD: 4 unit suites + R2a-d byte-identical vs V0 (V0 arbiter SHA matches
  frozen de35066487...). test_commit_pin seeded priors route REVISE but
  corroborate → verdict/audit bytes unchanged.
- LH 10x/100x (300/3000 eps): no panic; 3x identical per horizon;
  cross-horizon prefix identical. Delta vs V0 surgically confined: exactly 7
  pre-saturation drifted contradicted recommits (V0 admits, H-* withhold).
- Hypotheses byte-identical to each other everywhere → separation is
  architectural (organ autonomy vs router-held state), not empirical.
- Caveat: one H-arbiter 100x run had torn stdout framing (transient I/O
  artifact, decision bytes identical).
- Evidence: ~/workspace/h1evo/v1_novel/ (EVIDENCE.md)

## V2 (R3 namespaces) — COMPLETE 2026-09-24 21:05 UTC
- H-sep (separate claim/commit-ring namespaces) and H-del (dead commit-ring write deleted): BOTH SURVIVE all R3' bars.
- Attack (h3_atk, 3x byte-identical): all six cells HOLD on both (killbars 0, OB_FAILURES=0, exit 0); V0 breaks on all three R3a legs (killbars 1) and panics on R3b (claim 200, exit=1).
- H-sep and H-del outputs byte-identical on every instrument (attack, ZD, LH 10x/100x).
- ZD: 4 unit suites + R1a-d + R2a-d byte-identical vs V0 (3x each).
- LH 10x/100x (3000/30000 eps, 3x each, prefix-consistent): no panics; per-block revoke oracle shows V0 misroutes exactly the predicted collision block (k=7: killed slot 9 not 1, rc=102) at both horizons, hypotheses zero misroutes.
- Probe bug caught: first same-episode leg read the route post-clobber (vacuous on V0); rewritten to capture pre-commit route + assert no-clobber.
- Backlog: H-OB-81 (ARB_APPLIED(MA_OP_ADD) logs input slot -1, not installed slot — pre-existing V0 audit-fidelity gap). H-OB-79/80 still open. N-AUTH parked. NO WINNER DECLARED.
- Evidence: ~/workspace/h1evo/v2_namespace/EVIDENCE.md (sources: v2_hsep/, v2_hdel/; baseline v2_namespace/ pristine)

## V2 (R3 namespaces) — COMPLETE 2026-09-24 21:04 UTC
- H-sep (doubled routes table: claim namespace [0,129), commit ring
  [129,258) at (129+ep%129)*4) and H-del (dead commit-ring write deleted
  after read-audit proved no episode-keyed reader): BOTH SURVIVE R3a'/R3b'/R3c'.
- V0 control confirmed broken: all three R3a legs misroute + R3b panics on
  id 200 (probe discriminates the repair; a probe bug was caught and fixed).
- ZD: 4 unit suites + R1a-c + R2a-d all OB_FAILURES=0, stdout byte-identical
  across V0/H-sep/H-del. M_COMMIT admission unaffected.
- LH 10x/100x (3000/30000 eps): no panics; prefixes identical; H-sep ≡ H-del
  byte-identical at both horizons. V0 misroutes exactly the predicted k=7
  collision block at both horizons (no new failure mode at 100x).
- Hypotheses byte-identical everywhere → separator-vs-deleter is
  architectural, not empirical.
- New backlog H-OB-81: ARB_APPLIED(MA_OP_ADD) logs input slot -1, not the
  installed slot (pre-existing V0 audit-fidelity gap).
- Evidence: ~/workspace/h1evo/v2_namespace/ (EVIDENCE.md)

## L14 (L1-L4 ledger) — COMPLETE 2026-09-24 21:13 UTC
- L1' exact-byte hashing (raw unescaped runtime bytes): 39 checks pass.
- L2' checkpoint-identity binding (MEM header 12->20B, mm_checkpoint returns
  id — preregistered breaking change): forged sidecar refused (MA_REFUSED_CKPT
  =107); replay converges. 37 checks pass.
- L3' guarded clock (hdr@16; legacy hdr@4 inert): strictly-forward accepted,
  zero/negative/backward rejected, all attempts logged. 33 checks pass.
- L4' governance triage: priority lane (tail 4 queue slots drain first),
  arbiter-audit reservation (960+64, explicit overflow counter), PAM obs
  reservation (56+8), disposition ledger as 256-ring with counted evictions.
  All partitions of existing capacity, not new caps. 82 checks pass.
- ZD: 4 suites + R2a-d byte-identical vs V0. LH 10x/100x prefix-consistent.
- Original L1-L4 attacks vs hardened code: all dead (divergences verified as
  the repair working or the preregistered API change).
- Findings: (1) midpoint-replay contract requires tail rollbacks cite tail
  checkpoints (driver-side, fixed); (2) rollbacks restore checkpointed
  governance state incl. pins (filed H-OB-82).
- Backlog H-OB-81..H-OB-85 filed.
- Evidence: ~/workspace/h1evo/ledger_l14/ (FINAL_REPORT.md, VERDICT.md,
  SHA_MANIFEST.txt)

## V3 INTEGRATOR — DISPATCHED 2026-09-24 ~21:15 UTC
Task: assemble V3 (architectural choices justified), reconcile L14's
mm_checkpoint API change, verify ALL kill bars on V3, run full V0/V1/V2/V3 x
1x/10x/100x comparison matrix, produce COMPARISON_MATRIX.md, commit to
origin/tnn-native-lab under docs/lab/onebrain/h1_evo/. NO WINNER DECLARED.
