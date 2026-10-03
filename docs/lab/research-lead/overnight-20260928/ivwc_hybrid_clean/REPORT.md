# REPORT.md -- IVWC-HYBRID-CLEAN: clean reproduction of IVWC-HYBRID-VERDICT

## Verdict: CLEAN REPRODUCTION CONFIRMED -- BUILD-PASS (K1-K10), PROCESS-FAIL LIFTED

Zero python3/python in this entire session (safebin PATH for every
build/run/audit; Step 0 attested in NAMECHECK.md). The committed
source (`5ad68a24e`) was rebuilt with the pinned znc and re-run 3x:

- Source sha256:
  `2af399624ced0da22ce5d6744efc43b565200a8ecaddeaefdc08de561464c8e8`
  (1216 lines, byte-verified against the committed blob).
- Rebuilt binary sha256:
  `6773ffab36b990abe780bb099ed2f1e477173830fd2509d81bb97ea23d6c523a`
  -- byte-identical to the committed binary (same sha256).
- 3/3 runs byte-identical stdout, sha256
  `eee1fcd97432078ce9945552222cd580cdc06dedc32294a21a5976bae73d95f4`
  -- the exact sha256 recorded in the verdict REPORT, and
  `cmp`-equal to the committed `ivwc_hybrid_verdict-run1.txt`.
- Run stderr: empty (0 bytes) all 3 runs; the binary writes nothing
  to stderr. Build stderr held only the standard zagd-unavailable
  informational notice.

No source was changed, no prediction was moved. Every frozen
prediction from `ivwc_hybrid_verdict/PREREG.md` -- all twelve arm
accuracies, all five error sets, all six bar values -- reproduces
exactly, including the preregistered limit (K10).

## Arm accuracies (from the clean re-runs; identical to the verdict run)

| arm | @15 (wp=15) | @30 (wp=30) | @45 (wp=45) |
|---|---|---|---|
| A1 UCB x V_T (anchor) | 11 {s=3} | 9 {s=0,s=6,s=7} | 10 {s=0,s=4} |
| A2 UCB x V_N (anchor) | 10 {s=0,s=3} | 7 | 9 {s=0,s=4,s=5} |
| A3 D1b x V_T (anchor) | 8 | 10 | 12 |
| A4 D1b x V_N (anchor) | 11 {s=5} | 11 {s=2} | 12 |
| A5 D2b x V_T (anchor) | 6 | 8 | 10 |
| A6 D2b x V_N (anchor) | 8 | 8 | 10 |
| A7a UCB x V_HA (KEY) | **11 {s=3}** | **9 {s=0,s=6,s=7}** | **9 {s=0,s=4,s=5}** |
| A7b UCB x V_HB | 11 {s=3} | 9 {s=0,s=6,s=7} | 10 {s=0,s=4} |
| A8a D1b x V_HA (KEY) | **11 {s=5}** | **12** | **12** |
| A8b D1b x V_HB | 11 {s=5} | 12 | 12 |
| A9a D2b x V_HA | 9 | 9 | 10 |
| A9b D2b x V_HB | 9 | 9 | 10 |
| anchors OF / X3 / HYB / MG | 10 / 9 / 9 / 10 | 8 / 9 / 8 / 8 | 8 / 10 / 9 / 10 |

BARS lines (clean re-run): sh=0 TVucb=13 Tfixed=12 ThyA=13 ThyB=13
Tpred=28; sh=1 TVucb=20 Tfixed=12 ThyA=20 ThyB=20 Tpred=35; sh=2
TVucb=13 Tfixed=12 ThyA=6 ThyB=13 Tpred=21. TFIXED=12, CVAL=15.

## Kill-bar re-verification (K1-K10)

- K1 (diet / commit order): PASS. Re-audited on the rebuilt source
  (same bytes as the committed source): A1 phase order
  671<684<701<769<827<854<923 (train COMMIT 671 < train PREFF 684 <
  train CONSEQ 701 < learner BAR 769 < sealed COMMIT 827 < learner
  BARS 854 < SCORING 923 -- strict increase). A2: 0
  world_buf/world_off tokens in learner decision fns
  (lc_blocked/lc_leg/learner_compose/learner_compose_rev/
  learner_compose_nn/belief_execute/gather_cells/verifier_*,
  source lines 240-578; the 26 whole-file hits are all in the
  world/harness fns, lines 1-239). A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x3
  (1 def + 2 call sites). A6: WC-FINAL=60 (24 train + 36 sealed,
  from run output). A7: 0 `learner_`/`belief_` tokens after the
  SCORING marker (line 923). A8: 0 `oracle` tokens. In-program
  K1=1.
- K2 (determinism): PASS. 3/3 byte-identical stdout (sha256
  `eee1fcd9...95f4` x3), and each run is `cmp`-equal to the
  committed verdict run.
- K3 (anchor @15): PASS. K3of15=10, K3x315=9.
- K4 (anchor @45): PASS. K4of45=8, K4x345=10.
- K5 (PRIMARY): PASS. K5ha8a15=11, K5he=1, K5hs=5; independent
  per-case check on the clean run: A8a@15 errors exactly {s=5}.
- K6: PASS. K6a315=8.
- K7: PASS. K7ha7a15=11, K7he=1, K7hs=3; A7a@15 errors exactly
  {s=3}.
- K8: PASS. K8ha9a15=9, K8hlt=1 (9 < 11).
- K9: PASS. K9ha8a30=12, K9he=0.
- K10: PASS (preregistered limit confirmed). K10ha7a45=9,
  K10he=3, K10hs=5; A7a@45 errors exactly {s=0,s=4,s=5}.

Preregistered secondary findings (all re-confirmed in the clean
runs): S1 ThyB = 13/20/13 (BARS line, == TVucb); S2 A7b == A1
(11/9/10, error sets {s=3}/{s=0,s=6,s=7}/{s=0,s=4}); S3 A8b:
11/12 {s=5}, 12/12, 12/12; S4 A9b: 9/12, 9/12, 10/12; S5 A9a:
9/12, 9/12, 10/12.

## What this establishes

1. The IVWC-HYBRID-VERDICT BUILD-PASS (K1-K10) is reproducible from
   the committed source with zero forbidden-interpreter
   involvement: the PROCESS-FAIL is lifted and the results are
   promoted from exploratory to clean.
2. The verdict's scientific content is unchanged (it was never in
   doubt): the preff-scoped hybrid bar V_HA un-blocks D1b (11/12
   @15 ceiling; 12/12 @30, beating V_N) and recovers V_T's UCB
   adaptation @15 (11/12) and @30 (9/12), with the preregistered
   @45 limit (9/12 = V_N < V_T's 10/12); V_HB gets the full
   best-of-both (UCB 11/9/10; D1b 11/12, 12/12, 12/12).
3. Byte-level provenance chain: prereg `99c5691da` -> implementation
   `5ad68a24e` -> this clean reproduction (source sha256
   `2af39962...`, binary sha256 `6773ffab...`, stdout sha256
   `eee1fcd9...`, all three cross-verified against the committed
   artifacts).

## Notes

- The reproducible build artifact (`bin/`) is deliberately NOT
  committed in this lane, per Micah's 2026-10-03 guidance
  (everything except reproducible cache/build artifacts). Rebuild
  with the pinned znc:
  `znc src/ivwc_hybrid_verdict.zag -o bin/ivwc_hybrid_verdict`
  from `docs/lab/research-lead/overnight-20260928/ivwc_hybrid_verdict/`
  under the safebin PATH.
- The `ivwc_hybrid_verdict/` lane was not modified by this
  reproduction; its PROCESS-FAIL'd history stands as the audit
  record.
- Non-ledger task. Commits local on `tnn-native-lab`, explicit
  pathspecs confined to `ivwc_hybrid_clean/`.
