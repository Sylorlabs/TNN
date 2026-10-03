# PREREG: MA4C-MULTISTREAM -- multi-stream validation of the K=3 proxy (frozen)

## 0. Standing

MA4c is PROXY-LEARNER-DRIVEN on one W6 stream with an honest
boundary: K=3 is exploratory (unique integer separating measured
ratios 2.94 vs 3.42; E735 margin 1.9%), multi-stream validation
required. This prereg freezes that validation. Nothing here weakens
any frozen bar; the bars are defined fresh for this lane.

## 1. Frozen design

Five W streams: W6 (Bernoulli seed 20261026, the MA4c baseline) and
S1..S4 (seeds 20261027, 20261028, 20261029, 20261030). Streams differ
ONLY in the W Bernoulli seed literal in gen(); tiles, bands,
shuffles, X/Y/Z seeds, and every line of mechanism logic are frozen
as ma4c.zag.

One binary per stream: `ms_<s>.zag` = ma4c.zag plus the write-only
MS audit (spec in NAMECHECK.md design record) plus fixed-episode
write-only probes at 0-indexed e=734 and e=794. The five sources
differ ONLY in the W seed literal and the banner stream tag
(verified by diff). K=3 drives the real victim rule in all five;
no K sweep in the mechanism.

MS audit record per W trigger (kind=0, pre-reseed) and per probe
(kind=1): printed episode (1-indexed), v, vkind, kind, N=nvalid,
VI/J=min-ratio pair, NUM/DEN (i64), PCT=100*NUM/DEN (i64; INF when
DEN=0<NUM), K1..K5 bits (1 iff some valid pair has NUM <= K*DEN,
the exact proxy firing condition).

## 2. Experimental protocol (frozen)

Per stream: compile ms_<s>.zag with safebin znc, run 3x,
sha256-recorded, 3/3 byte-identical required. Extract TRIGW, PROXYC,
REDSEEDW, DECLW, MS lines. X/Y/Z must be byte-identical across all
five streams (W seed cannot affect them); W tiles must be identical
(same shuffles).

## 3. Mechanism-derived predictions (frozen)

- X/Y/Z sections byte-identical across all five streams; W tile
  values identical; only W Bernoulli bits differ.
- ms_w6: non-MS, non-banner lines byte-identical to frozen ma4c
  run1.txt (audit neutrality); MS at E735 (kind=0): N>=1, VI=2, J=3,
  PCT in [290,300], K3=1; MS at E795 (kind=0): VI=2, J=3, PCT in
  [335,350], K3=0. (Reproduces the W6 diagnostic: 2.94 / 3.42.)
- Trigger timing is a seed-sensitive race (design record); S1..S4
  may show extra, missing, or shifted boundary triggers. B5/B6
  handle this without reinterpretation.

## 4. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this PREREG.md (+NAMECHECK.md Step 0)
  is committed strictly before any ms_*.zag implementation file.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical per stream
  (5 sha256 recorded).
- B4 AUDIT-NEUTRALITY: PASS iff ms_w6 output minus MS lines minus
  the banner line is byte-identical to frozen ma4c run1.txt (cmp
  after filtering). Proves the MS audit is write-only and the
  tested mechanism is the frozen K=3 proxy.
- B5 SCENARIO-VALIDITY (per new stream): PASS iff the closed-loop
  run shows a W trigger with printed episode in [733,741]
  (B4-boundary) AND a W trigger with printed episode in [793,801]
  (B5-boundary). A stream failing B5 does not present the designed
  two-case discrimination; it is excluded from B6/B8 and reported
  as a scenario-presentation finding, not a proxy finding.
- B6 K3-DISCRIMINATION (PRIMARY, per B5-passing stream): PASS iff
  (i) at the B4-boundary trigger the MS kind=0 entry shows K3=1,
  PROXYC shows >=1 nonzero C, and TRIGW shows the R-path
  (":NR" suffix, vkind=1) with the reseed proceeding; AND (ii) at
  the B5-boundary trigger the MS kind=0 entry shows K3=0, PROXYC
  shows all C=0, and TRIGW shows declined (":D", DECLW increments).
- B7 OPAQUE-IDS: PASS iff case-insensitive grep for the frozen
  29-word list returns empty in all ms_*.zag.
- B8 MARGIN-QUANTIFICATION (measurement bar): PASS iff REPORT.md
  tabulates, per B5-passing stream, GEN_PCT and ADV_PCT (MS
  min-pair PCTs at the two boundary triggers), both margins vs 300,
  and the separating-K set {K in 1..5 : K-bit=1 at B4 trigger AND
  K-bit=0 at B5 trigger}; plus the fixed-probe PCTs at e=734/794
  for all streams.
- B9 K3-STABILITY (kill bar): PASS iff B6 PASS on ALL B5-passing
  new streams (S1..S4).

Headline verdict:
- K3-ROBUST iff B9 PASS with B1..B8 PASS: K=3 discriminates the
  genuine/adversarial cases on every testable stream; the 1.9%
  W6 margin is stable under Bernoulli resampling.
- MARGIN-FRAGILE iff B9 FAILS: the report names each failing
  stream, which side flipped (genuine silent or adversarial
  fired), the measured PCTs, and the separating-K sets. The
  report must diagnose, not reinterpret the bar.
- K-VARIES (preregistered implication): if the separating-K sets
  of the B5-passing streams have empty intersection (no single
  integer K separates on all streams), a frozen universal integer
  K is disclaimed: the proxy design must make K adaptive
  (set from experience) or replace the fixed-K form with a
  margin-aware rule. A stream-varying optimal K is evidence
  against a constant, not a tuning exercise.

If B6 FAILS with the apparatus bars PASS, the headline is
MARGIN-FRAGILE (or K-VARIES per the sets), never a weakened bar.

## 5. Honest boundaries (frozen)

- Streams resample Bernoulli noise only; the tile/band scenario
  design is frozen. This tests margin stability under noise, not
  generality across tile designs (a separate experiment).
- Four new streams is a small sample: K3-ROBUST bounds fragility,
  it does not prove universality.
- The trigger race is a second, distinct fragility (design
  record); B5 isolates it from the proxy-margin question.
- What is measured are cell-mean tallies, as MA1-4. Not strategy
  invention, not L3. The proxy is tally-driven, not invented.

## 6. Artifacts planned

- `ms_w6.zag`, `ms_s1.zag` .. `ms_s4.zag`, five binaries,
  15 run files (3 per stream, sha256 recorded)
- `REPORT.md`, `NAMECHECK.md` (build record)
