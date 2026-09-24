# AU-1 audit report — H-PAM-21: evidence-independence audit of the F5 quorum

Date: 2026-09-24. Crew: AU-1 (PAM round-2 swarm, evidence-independence audit).
Hypothesis: H-PAM-21 ("the quorum triple-counts one source"), full text in
`~/workspace/pam_hypotheses_native_B.md` §H-PAM-21. Backlog line 39 of
`~/workspace/hypothesis_backlog.md`.

Frozen mechanism under audit: `f5_full.zag` — predicate BLOCKED iff exemplar
(same family stem) with |dconf|<=150, |dmeas|<=2000; confirmation takes 3
temporal crops (conf∓10/meas∓200, center, conf±10/meas±200), each crop
reproduces the false signature iff exemplar (same stem) with |dconf|<=130,
|dmeas|<=950; WITHHOLD iff ≥2/3 crops reproduce, else CONFIRM+INSTALL.
Verdict under audit: SURVIVE (commits d156a60a prereg, 13b586dd evidence).

## Method (no new battery, no new mechanism code)

The committed run logs carry per-trial verdicts but not per-crop votes. The
votes are deterministic functions of the FROZEN inputs under the FROZEN rules,
so they were reconstructed by exact port of the decision logic:

- `fixtures_ledger.txt` — 300 NEAR battery input, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`
  (recomputed locally, matches the verdict's pinned SHA).
- `exemplars.tsv` — 6-row bank, SHA
  `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`
  (matches SHASUMS.txt, verified `sha256sum -c` OK).
- `ledger_d_withhold.txt` (backtest, 43 candidates) — local copy byte-identical
  to the blob committed on branch tnn-native-lab (verified via GitHub API).
- Reconstructed (blocked, quorum-verdict) validated against the committed
  run logs before any statistics were computed.

Validation gates: **300/300 NEAR percepts match run1.out** (SHA
d287b4ee67ca546ff4433fe245ad36fbd19f577b432939a15ef0d9ed13b78327);
**43/43 backtest candidates match bt1.out** (SHA
5c9eea9d8f5dbb84ea95d9c4b7ee9255ac355f95828bcb08ae41729a02a8b93f).
Both reconstructions byte-exact. Analysis scripts are deterministic Python
(no RNG); both were rerun and produced byte-identical outputs.

## Results — 300-battery panel (110 blocked NEAR percepts)

- Effective independent sample size: **n_eff = 1.2386** (mean pairwise
  Pearson rho = 0.7110; pairs: c1–c2 0.6094, c1–c3 0.5770, c2–c3 0.9467).
  H-PAM-21 predicted 1.0–1.2. Measured sits at the band's edge, squarely
  below the preregistered kill number of 1.5.
- Mutual information per crop pair: 0.3349 / 0.3072 / 0.8428 bits;
  normalized I/min(H): 0.4245 / 0.3894 / 0.8479 (near-max for the
  center–high pair).
- Vote-conditional agreement: P(c1=1|c2=1)=1.0000, P(c3=1|c2=1)=0.9500,
  P(c2=1|c3=1)=1.0000, P(c2=0|c3=0)=0.9434, P(c1=0|c2=0)=0.5200,
  P(c1=0|c3=0)=0.4906 — the "disagreement" is almost entirely one-sided
  permissiveness, not independent evidence.
- Vote patterns (110): 000:26, 100:24, 110:3, 111:57. Unanimous 83/110.
- **Structural collapse: the 110 triples are monotone nested (c3 ≤ c2 ≤ c1
  on every percept). A 2-of-3 majority of monotone votes is exactly the
  middle vote — so the quorum decision is byte-identical to the CENTER CROP
  alone on 110/110. The panel adds zero decision information over a single
  re-inspection.**

## Results — backtest panel (8 blocked TMB false accepts)

- All 8 triples are **111** (unanimous). Zero variance → effective-n = 1.0
  exactly, quorum == center crop 8/8. The preregistered kill bar
  (effective-n < 1.5 on the backtest battery) is met.

## Verdict

**H-PAM-21 CONFIRMED (TESTED-survived).** The quorum triple-counts a single
evidence source: n_eff ≈ 1.24 on the 300-battery (predicted 1.0–1.2),
1.0 on the backtest battery, and the 2/3 panel is decision-identical to one
center-crop re-inspection. The survival verdict's "predicate + independent
confirmation" justification is dead — what survived is predicate + a single
re-inspection, i.e. a coherence detector wearing a quorum's clothes.

Scope notes: (1) The numbers (8/8, 0/34, 20.0% delay) stand; the audit kills
the justification, not the bars — per the hypothesis's own steelman, the
surviving reframe is "redundant veto," not "independent witness." (2) The
monotone nesting is empirical on these frozen batteries (driven by battery
geometry: blocked percepts sit just above the exemplar measure window, so
the −200-meas crop is strictly more permissive); it is not proven as a
mechanism theorem — but it is proven on the evidence the verdict rests on.
(3) au1_votes.tsv is a deterministic reconstruction from frozen inputs,
validated vote-for-vote against the frozen logs; it is analysis, not new
evidence.

## Files

- `au1_effective_n.py` — 300-battery reconstruction + statistics (deterministic)
- `au1_backtest_panel.py` — backtest-panel reconstruction + statistics (deterministic)
- `au1_votes.tsv` — reconstructed per-crop vote matrix, 300 NEAR percepts
- `au1_report.txt` — 300-battery audit numbers (byte-identical rerun confirmed)
- `au1_backtest_report.txt` — backtest-panel audit numbers (byte-identical rerun confirmed)
- `SHASUMS.txt` — this directory's files
