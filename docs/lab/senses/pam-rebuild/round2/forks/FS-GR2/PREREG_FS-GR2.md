# FS-GR2 Preregistration — Frozen 2026-09-24

Gate-redesign iteration round 2 (PAM rebuild round 2). Micah's directive:
"iterate and test more, I bet we can find something way better." Round 1
(FS-GR1) fixed motiondir false-installs (7/630 → 1/630, UCB 2.2756% →
0.8936%) and timbredisc recall (25% → 100%), but motiondir control recall
fell 85.0% → 78.5%: the safety fix cost ~7 points of liveness. This round
builds RADICALLY DIFFERENT motiondir challenge designs from first
principles — not incremental tweaks of CH-MOT-3 — and red-teams every
candidate against the full battery plus hostile corpora.

This document freezes the battery, candidate specifications, bars, and
scoring BEFORE any round-2 mechanism is run. No mechanism edits after this
commit except documented build-defect repair (requires rerun from scratch).

## 1. Battery pin (frozen, do not redraw)

- Source: `round2/forks/FS-E2b/fixtures_e2b/` (12,000 fixtures + 12,000 truth sidecars).
- Adversarial manifest SHA-256: `f4f85194c4ee0cf157f7b155881a2c0797041beb5e2ee03bfb4ee7b70512e7a2`
- Control manifest SHA-256: `64798b244f90ddeaffe695ed4a43e361dbb397037da5595671c611cb01f6d22d`
- Manifest line counts: 10,000 adversarial, 2,000 control.
- File-level verification: recompute all 12,000 SHA-256 entries before any
  candidate run; require ok: 12000 bad: 0.
- MASTER=20260926. The battery is pinned by the two manifest SHAs. It must
  not be redrawn.

## 2. FS-GR1 baselines (carried; the bar to beat)

### Adversarial FI (Wilson 95% UCB) — FS-GR1 round-1 results

| Task | FI / n | FI rate | Wilson 95% UCB |
|---|---:|---:|---:|
| colordisc | 0/2330 | 0% | 0.1646% |
| colorconst | 0/1380 | 0% | 0.2776% |
| shapetrans | 0/2345 | 0% | 0.1636% |
| pitchdisc | 0/2330 | 0% | 0.1646% |
| timbredisc | 0/985 | 0% | 0.3885% |
| motiondir | 1/630 | 0.1587% | 0.8936% |
| pooled | 1/10000 | 0.01% | — |

### Control recall — FS-GR1 round-1 results

| Task | Recall |
|---|---:|
| colordisc | 94.3333% |
| colorconst | 98.4000% |
| shapetrans | 86.3333% |
| pitchdisc | 96.5000% |
| timbredisc | 100.0000% |
| motiondir | 78.5000% |
| pooled | 93.3500% |

Round-2 target: motiondir recall ≥ 85% with motiondir FI UCB ≤ 1%.

## 3. Design rationale (why these four, not tweaks)

FS-GR1's CH-MOT-3 kept formation's measurement (block-match SAD argmin on
the same central block) and added gates. The gates threw away the same
votes formation counted — hence the recall loss. FI requires the challenge
to AGREE with formation's WRONG claim; a challenge whose failure modes are
structurally uncorrelated with formation's block-match failures can resolve
more often (higher recall) while agreeing with a wrong formation claim more
rarely (low FI). The four candidates below change the measurement family,
the decision geometry, or the corroboration structure — never just the
thresholds.

Support rule FROZEN (from FS-E1b registry, unchanged): INSTALL iff
challenge outcome == formation claim and challenge != UNRESOLVED.
UNRESOLVED never installs. Only the motiondir challenge mechanism
(`mo_chal` + helpers in the copied sup source) is replaced per candidate;
the other five tasks' code paths are byte-identical to FS-GR1.

Formation stage: the FS-GR1 formation binary is UNCHANGED and was proven
byte-identical x2 in round 1. Candidates reuse FS-GR1's formation TSVs and
claim TSVs directly (documented reuse, not a rerun). Each candidate runs
the sup stage x2 (byte-identity), hash-chained ledgers, and scoring.

## 4. Candidate specifications (frozen)

Common: G buffer layout 50 frames of 32x32 u8 (frame t at bo + t*1024).
Lags t in {0,2,4,...,44} (23 lags) compare frame t -> frame t+2, EXCEPT
CH-MOT-6 which uses two interleaved lag sets. All integer arithmetic is
i64; overflow bounds are stated per candidate. Ties: first in row-major
(dx outer? — specified per candidate) enumeration order — deterministic.
No RNG anywhere.

### CH-MOT-4 "ZNCC-peak" — different similarity formulation

Zero-mean normalized cross-correlation replaces SAD. Correlation is
invariant to brightness/contrast scaling; its peak sharpness is a
principled informativeness measure (a genuine alignment produces a peak
well above the sidelobe floor).

Per lag, central 16x16 block (rows 8..23, cols 8..23) of frame t:
1. For each shift (dx,dy) in [-8,8]^2 (dy outer, dx inner, row-major):
   block A = frame t pixels; block B = frame t+2 pixels at (y+dy, x+dx).
   Integer means: ma = sum(A)/256, mb = sum(B)/256.
   N = sum((a-ma)*(b-mb)); Sa = sum((a-ma)^2); Sb = sum((b-mb)^2).
   If Sa <= 0 or Sb <= 0: score = -2147483648 (skip sentinel).
   Else D = isqrt(Sa*Sb) (integer Newton, floor); score = (N*1024)/D.
   Overflow: |a-ma| <= 255; |N| <= 256*255^2 = 16,646,400;
   N*1024 <= 1.71e10 < 2^63. Sa*Sb <= (1.66e7)^2 = 2.77e14 < 2^63. Clean.
2. (bx,by) = argmax score (first row-major on ties).
   Boundary rejection: |bx|=8 or |by|=8 -> skip lag (same wrap-latch
   rationale as CH-MOT-3: the 16px window cycle latches wraps at the
   search boundary).
3. Sharpness gate: s1 = best score; s2 = max score over shifts with
   max(|dx-bx|,|dy-by|) >= 2 (non-adjacent: excludes the peak's shoulders).
   Vote iff s1 >= 512 AND s1 - s2 >= 64, voting mot_quant(-bx,-by).
   Rationale (not tuned): s1 >= 512 = correlation >= 0.5 (positive
   alignment; random texture ~ 0); 64/1024 = 6.25% significance margin
   above the sidelobe floor. Else skip lag.
4. After all lags: V counted votes; V=0 -> UNRESOLVED. Strict majority
   (>50%): winner = argmax votes (lowest index on ties); if
   bestv*2 <= V -> UNRESOLVED; else winner.

### CH-MOT-5 "evidence accumulation" — different decision geometry

Uses the full SAD landscape per lag instead of a single argmin vote.
Abstention boundary is quadratic (margin^2 > total evidence), a
significance-style curve in (margin, evidence) space rather than a linear
majority rule.

Per lag, same block and ±8 search as CH-MOT-3; compute all 289 SADs:
1. Boundary rejection on argmin (bx,by): |bx|=8 or |by|=8 -> skip lag.
2. med = median of the 289 SADs (insertion sort, as in CH-MOT-3).
   For each shift: e = med - s; if e < 0 -> e = 0.
   j = mot_quant(-dx,-dy); D[j] += e.
   Overflow: med <= 256*255 = 65280; e <= 65280; per-lag sum <=
   289*65280 = 1.89e7; 23 lags -> D[j] <= 4.34e8 < 2^63. Clean.
3. After all lags: let D1 >= D2 be the top two direction evidences,
   E = sum_j D[j]. Resolve iff D1 > 0 AND (D1-D2)^2 > E; winner =
   argmax D (lowest index on ties). Else UNRESOLVED.
   Rationale: under the null (evidence spread across bins), D1-D2 ~
   sqrt(E); requiring margin^2 > E rejects null-like splits. A single
   noisy argmin cannot swing the outcome; coherent landscape-level
   support is required.

### CH-MOT-6 "temporal-quorum" — different corroboration structure

Two temporally interleaved witnesses, each with a LIBERAL per-witness bar
(plurality), combined by a STRICT corroboration requirement (agreement).
Novel liveness/safety trade: weaker per-witness, stronger quorum.

- Witness A: lags t in {0,2,...,44} (23 lags). Witness B: lags t in
  {1,3,...,43} (22 lags). Same central block, ±8 search, SAD argmin,
  boundary rejection, informativeness gate (s_best*5 < med*2) — as
  CH-MOT-3 — per lag per witness.
- Per witness: plurality winner (most votes; lowest index on ties);
  UNRESOLVED if zero counted votes. NO strict-majority per witness.
- Final: both witnesses resolve AND agree -> that direction;
  else UNRESOLVED.
- Rationale: frame-level sensor noise (+-3) and re-render noise are
  independent across frames, so the witnesses are independent samples of
  the same motion. Two independent noisy estimators agreeing on the same
  wrong direction is far rarer than one doing so — the safety that
  CH-MOT-3 bought with strict majority is bought here with corroboration,
  while each witness resolves more liberally (recovering recall).

### CH-MOT-7 "Lucas-Kanade" — different measurement family

Gradient-based normal-flow (structure tensor) instead of correlation
search. The aperture problem is handled FIRST-PRINCIPLES: the 2x2
structure tensor must be well-conditioned (both eigenvalues substantial)
for the displacement to be resolvable; ill-conditioned lags abstain by
construction rather than by an empirical gate.

Per lag t in {0,2,...,44}, central 16x16 block, frames t and t+2:
1. Per pixel (x,y) in block: Ix = (I(x+1,y,t)-I(x-1,y,t))/2;
   Iy = (I(x,y+1,t)-I(x,y-1,t))/2; It = I(x,y,t+2)-I(x,y,t).
   (x in 8..23 so x+-1 in 7..24, in-bounds.)
2. Sxx=sum Ix^2; Syy=sum Iy^2; Sxy=sum Ix*Iy; Sxt=sum Ix*It;
   Syt=sum Iy*It (256 px).
3. Aperture gate: tr = Sxx+Syy; if tr <= 0 -> skip.
   det = Sxx*Syy - Sxy*Sxy; if det <= 0 -> skip.
   If 16*det < tr*tr -> skip lag (minor eigenvalue < ~7% of major:
   motion unresolvable along the minor axis — pure aperture).
   Overflow: |Ix|<=127; Sxx <= 256*127^2 = 4.13e6;
   det <= (4.13e6)^2 = 1.71e13; tr^2 <= (8.26e6)^2 = 6.82e13 < 2^63.
   |Sxt| <= 256*127*255 = 8.29e6; |u_num| = |Syy*Sxt| <= 3.42e13;
   *256 <= 8.77e15 < 2^63. Clean.
4. u = -(Syy*Sxt - Sxy*Syt)*256/det; v = -(Sxx*Syt - Sxy*Sxt)*256/det
   (fixed-point x256; det > 0 by gate).
   qx = round(u/256), qy = round(v/256), round-half-away-from-zero,
   deterministic. Vote mot_quant(-qx,-qy) (negation: (u,v) is content
   displacement; the window moves opposite — same convention as
   block-match).
5. After all lags: strict majority (>50%) over counted votes;
   else UNRESOLVED.

## 5. Frozen bars (per candidate)

1. Motiondir control recall >= 85% (frozen 200-item subset).
2. Motiondir adversarial FI Wilson 95% UCB <= 1% (frozen 630-item subset;
   i.e. at most 1 FI).
3. Other-five-task no-regression vs FS-GR1 round-1: FI rate increase <=
   1pp per task; recall decrease <= 1pp per task. Floors: colordisc
   recall >= 93.3333%, colorconst >= 97.4000%, shapetrans >= 85.3333%,
   pitchdisc >= 95.5000%, timbredisc >= 99.0000%. FI ceiling 1.00% each.
   (Verified by byte-comparing the other five tasks' sup outputs against
   FS-GR1's committed evidence: the code paths are unchanged, so any
   difference is a build defect.)
4. Byte-identical determinism x2: sup raw output IDENTICAL across two
   full runs per candidate; hash chains verified line-by-line.
5. File-level battery verification before runs: 12000/12000 SHA-256 ok.

Champion selection (frozen): among candidates passing bars 1-4, rank by
motiondir recall DESC, then motiondir FI UCB ASC. If no candidate passes
bars 1+2 jointly, NO champion is named; the verdict reports the full
table and the Pareto frontier, and recommends the next iteration.

## 6. Red-teaming (frozen plan)

A dedicated red-team crew builds hostile motiondir corpora OUTSIDE the
frozen battery (frozen battery is never redrawn or augmented for bars):
- RT-A periodic textures: sine stripes at 6 orientations x 3 frequencies,
  checkerboards — multi-peak SAD/NCC ambiguity traps.
- RT-B near-flat + strong noise: argmin/argmax ~= noise traps.
- RT-C single-orientation ramps at 8 orientations: worst-case aperture.
- RT-D flicker stress: 50% flicker + moving blob (harder than family 2).
Fixtures use the frozen .r2fx layout (magic 1379026520); truth from the
generator; formation claims from the REAL FS-GR1 formation binary.
Per candidate, measure: (a) FI-like rate = challenge agrees with a WRONG
formation claim; (b) resolve rate. Also: every candidate must be run on
the 1 remaining FS-GR1 FI item — report whether it recurs.
Red-team corpora are diagnostic (not bars): a candidate that passes bars
but shows a systematic red-team break gets a documented finding and a
repair proposal, not a silent pass.

## 7. Scoring

- Run each candidate's sup binary on the frozen claim TSVs twice;
  byte-compare; assemble hash-chained ledgers; score with the frozen
  scorer definitions (FI = disposition INSTALL with formation claim !=
  truth; Recall = correct INSTALLs / n on controls).
- Write VERDICT_FS-GR2.md with every count/rate/UCB per candidate, the
  red-team findings, and FINAL champion/no-champion.
- Commit: prereg (this file), per-candidate sources, evidence TSVs/
  ledgers, red-team corpora + results, verdict. No binaries, no .zagd,
  no cache files.

## 8. Implementation constraints (frozen)

- Pure Zag for mechanisms; Python only for glue/analysis; zero RNG in
  any decision path.
- Pinned znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Work dirs: `senses/pam-rebuild/round2/work_fsgr2/<CAND>/` (working
  checkout, NOT the repo clone). No battery work in /tmp (512MB shared
  tmpfs).
- Copy FS-GR1 sources per candidate; replace ONLY the motiondir
  challenge; `reg_challenge(5)` returns the candidate's ID
  ("CH-MOT-4/5/6/7") for ledger traceability.
- Commit via `TMPDIR=~/workspace/tmp_commit python3
  ~/workspace/commit_racefree.py` (or commit_big_files.py for large
  evidence) with lab-relative paths
  `senses/pam-rebuild/round2/forks/FS-GR2/...`.
- If GitHub returns 429/403: stop GitHub work immediately, report
  partial progress, do not retry-loop.
- No redesigned mechanism run before this prereg is committed. No
  mechanism edits after except documented build-defect repair (requires
  full rerun from scratch).
