# HARDENING_VERDICT.md — PAMs v2 follow-up item 4

Prereg: `PREREG_V2-IE_AMEND1.md` (committed alone as `f61da3af`, before any
fork was built). Battery: six hardening forks (H1–H6) × four frozen red-team
streams × 3 runs. All gates, the scorer (`rt_score.zag`), and the ledger
verifier (`tools/lverify.zag`) are pure Zag; Python was used only for
build glue, the deterministic attestation-sidecar generator
(`tools/make_gatt.py`), and analysis. Zero RNG. All 24 (fork, stream) cells
are byte-identical across the 3 runs (digests in
`evidence/DISPOSITION_DIGESTS.md`); all 24 audit ledgers verify under the
pure-Zag chain check (`evidence/LEDGER_DIGESTS.md`).

## Head-to-head results (rt_score, frozen streams)

I = installs, C = correct installs, F = false installs, W = withholds,
R = revise_installs. n: clean 288, withhold 288, install 44, decoy 52.

| fork | stream   | I | C | F | W | R |
|------|----------|---|---|---|---|---|
| H1   | clean    | 39| 26| 13|151| 0 |
| H1   | withhold |  0|  0|  0|288| 0 |
| H1   | install  | 34| 23| 11|  2| 0 |
| H1   | decoy    | 42| 23| 19|  3| 0 |
| H2   | clean    | 26| 16| 10|147|11 |
| H2   | withhold |  0|  0|  0|288| 0 |
| H2   | install  |  8|  4|  4|  1| 1 |
| H2   | decoy    | 11|  4|  7|  7| 1 |
| H3   | clean    | 16| 10|  6|157| 1 |
| H3   | withhold |  0|  0|  0|288| 0 |
| H3   | install  |  8|  4|  4|  3| 1 |
| H3   | decoy    | 11|  4|  7|  9| 1 |
| H4   | clean    | 22| 13|  9|149| 7 |
| H4   | withhold |  0|  0|  0|288| 0 |
| H4   | install  |  8|  4|  4|  3| 1 |
| H4   | decoy    | 13|  4|  9|  9| 3 |
| H5   | clean    |  8|  6|  2|228| 0 |
| H5   | withhold |  0|  0|  0|288| 0 |
| H5   | install  |  6|  3|  3| 33| 1 |
| H5   | decoy    |  6|  3|  3| 41| 1 |
| H6   | clean    |  2|  2|  0|234| 0 |
| H6   | withhold |  0|  0|  0|288| 0 |
| H6   | install  |  4|  3|  1| 35| 1 |
| H6   | decoy    |  4|  3|  1| 43| 1 |

Score-file digests (rt_score output hash per cell) are listed in §6.

## Kill-bar verdicts

- KB-H1 (0 false on clean): H6 PASS (2 installs, both correct). All others FAIL.
- KB-H2 (withhold stream: 0 installs): ALL PASS (all forks emit byte-identical
  all-WITHHELD dispositions on the 288 UNRESOLVED records).
- KB-H3 (decoy stream: 0 false): ALL FAIL (best: H6, 1 false).
- KB-H4 (install stream: 0 false): ALL FAIL (best: H6, 1 false).
- KB-H5 (must not collapse to 0 installs): ALL PASS (every fork installs on
  clean/install/decoy).

**No fork passes all kill bars.** Per the amendment, the follow-up item closes
with the honest verdict: **no hardened fork achieves the bar on these streams.**

## What the battery proved

1. **T1 (record-channel forgery) is solved by R2+R3.** The 8 spoofed decoy
   records (seqs 5,11,17,23,29,35,41,47 — identified by byte-exact
   re-derivation of the harness constructor, not heuristics) install freely
   without authentication: H1 installs all 8. H2/H3/H4 — authentication that
   guards only the adjudication/revision path — still install 2–3 spoofed
   records through the unguarded provisional/first-install path (H4 even
   REVISE-installs one). H5/H6, which require attested agreement on EVERY
   install path (R3), install **zero** spoofed records. Authentication must
   cover all install paths, not just revision.
2. **R1 (prog=PASS) is necessary but weak alone** (H1: 13 clean false).
3. **Provisional installs are the main false-install vector on clean data.**
   H5's 2 clean false installs are both first-observation provisionals;
   H6's no-provisional rule (withhold until a corroborated second observation
   within tolerance) eliminates them: 0 false on clean.
4. **The remaining failures are one mechanism: sustained, attested,
   mutually-corroborating, confident cross-span error (T2).** The install
   stream's TMB-5 trials 24–35 are twelve consecutive RICH judgments (truth
   DARK/BRIGHT), conf 764–832, G-span agreeing on 9 of 12 — including the two
   trials H6 installs (seq 24 unconfirmed → seq 25 permanent, |Δmeas|=27 ≤
   tol). Gate-visible features of this wrong cluster overlap correct installs
   on every stream (clean: wrong conf 763–832 vs correct 777–955; the decoy
   stream has attested wrong trials up to conf 951). No confidence threshold,
   margin, corroboration count, or attestation check separates them without
   also killing correct installs or collapsing to zero installs. This error
   class is observationally identical to correct operation; defeating it needs
   a better front-end, not a stricter gate.

## Recommendation

- **Adopt H6's rule set** (R1 prog gate, R2 channel attestation on every
  install path, R3 attested-agreement bar, R4 corroboration+margin for
  revision, no provisional installs) as the hardened baseline: it is the
  only fork with 0 false installs on clean data, 0 spoofed installs, and
  non-degenerate install counts, and it dominates H5 on every stream.
- **Do not chase the 0-false bar on the install/decoy streams by tuning the
  gate.** The residual false installs are systematic front-end confusion,
  not a gate defect; any truth-free rule that kills them on these streams
  would be overfit to the red-team fixtures.
- **Next red-team target: the TMB front-end**, not the gate. Twelve
  consecutive confident cross-span RICH errors on DARK/BRIGHT fixtures is a
  sensor/judgment failure the gate cannot see.

## §6 score digests (rt_score output hash per cell)

- H1: clean b2955c91bb0b3ff7fc7e016a64921fc5574bed1bab0b5b14f126f183656bdaad / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install c674cde41745b7a75d0bb63af34ab0dbbbc7bd66529560dcfa762731ecd74396 / decoy 2cb9ba5480a9bb9964a1572c8c11d231b5ad7af8f7d9603284c45a6ee83534f5
- H2: clean 96ea5325d95348dde8cb9209c436f9c3600630e109abe9447a1677edf05d5453 / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install 181f671b8fe817ba9bada7b64edbd9f4c214f9a40b929fb03c99fbc5f632aac7 / decoy 7a23a21b2331d69f8b3017719154facdc07291347e51bdeadc5d7c1e45678cd1
- H3: clean 96cfa01ed67a6a5f2bbd5bbcb5b2db063e64b57b3c164e2a027c3a3a60c71706 / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install d260e87f6fa596b26d642576be9ccaa13179ba24aea7df60beec180d09efdebd / decoy fdb225d2197dbb5daf05c11752acea4a66c63814ce26e75faf90e42d9075f5ac
- H4: clean e5017373ef54ec1a998e2028f1d0fd2aec64456c15d498ffa7f16cfb03a3925b / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install d260e87f6fa596b26d642576be9ccaa13179ba24aea7df60beec180d09efdebd / decoy b29d6f52fec025e86ec44764028f895e1ea17af6af81fc60551caac939faeaa4
- H5: clean 233efbed5b90da91aefceea0b5af79948c7d9868d8c5d6a4a769af18cb1e9c37 / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install 51b7b71a0266ddf8fda66d2d616862f8aba2e396a37208afd3ac301eb04b07a0 / decoy 90c64a83fca5a982e17cd96281f29a76b4f78111e66425a9dcc119722053965a
- H6: clean 17c092c26ae88ce366774d171f0fa444b533ab3d0848d5b40fb85c081a88425a / withhold 7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616 / install 34bc8f5c32fa43f1457a1be5b4503e2359625d700a4e41d414bff9ff8819a95c / decoy 9f417a8e7f259bd1da0b981961e6071457fc8c60a3c93a2d75413b4924c57c6e

(Full hashes in `evidence/DISPOSITION_DIGESTS.md`; per-family score files in
`evidence/score_h*_*.txt`; r1 dispositions and ledgers alongside.)
