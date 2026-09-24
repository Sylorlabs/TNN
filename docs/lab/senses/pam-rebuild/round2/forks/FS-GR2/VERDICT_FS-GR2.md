# VERDICT_FS-GR2.md — Gate-redesign iteration round 2

**Date:** 2026-09-24
**Prereg:** `PREREG_FS-GR2.md` (commit `61aef566`, frozen before any round-2 mechanism ran)
**Status:** COMPLETE — all four frozen candidates built, run on the frozen battery, scored, red-teamed.

## 1. Frozen-battery results

| candidate | challenge | motiondir recall (n=200) | motiondir FI (n=630) | FI Wilson 95% UCB | bar: recall ≥85% | bar: UCB ≤1% |
|---|---|---|---|---|---|---|
| FS-GR1 (baseline) | CH-MOT-3 | 157/200 = 78.5% | 1/630 | 0.894% | — | — |
| CH-MOT-4 | ZNCC-peak | 146/200 = **73.0%** | **0/630** | **0.606%** | ✗ | ✓ |
| CH-MOT-5 | evidence accumulation | 116/200 = **58.0%** | **19/630** | **4.66%** | ✗ | ✗ |
| CH-MOT-6 | temporal-quorum | 153/200 = **76.5%** | **2/630** | **1.15%** | ✗ | ✗ |
| CH-MOT-7 | Lucas–Kanade | 50/200 = **25.0%** | **4/630** | **1.62%** | ✗ | ✗ |

Integrity checks (all candidates): battery file-level SHA-256 **12000/12000 ok** before running;
supervisor output byte-identical across two full runs (r1 == r2); hash chains verify by
independent recomputation; other five tasks' outputs **byte-identical** to FS-GR1's committed
raws (no-regression PASS for all four). No candidate touched anything outside the motiondir path.

## 2. Champion

**NONE.** Per the frozen §7 rule: no candidate jointly passes the recall and FI bars, so no
champion is named. The mechanical ranking never activates.

## 3. Pareto frontier (recall maximized, FI minimized)

Including the FS-GR1 baseline:

- **FS-GR1 (78.5%, 1 FI)** — highest recall on the frontier.
- **CH-MOT-4 (73.0%, 0 FI)** — the only point with zero FI; buys perfect safety for 5.5pp recall.

CH-MOT-6 (76.5%, 2 FI) is **strictly dominated by FS-GR1** (worse on both axes).
CH-MOT-5 and CH-MOT-7 are dominated by every other point.

## 4. Red-team (hostile corpora RT-A..RT-D, 288 fixtures; diagnostic, not bars)

| candidate | FI-like | key pattern |
|---|---|---|
| MOT-4 | **0** | total withhold on stripes/ramps; 39/40 correct installs on flat noise; conservative-true on flicker |
| MOT-5 | 10 | systematic diagonal→cardinal snap on coarse (L=16) stripes; reverse-installs on aperture-maximal ramps |
| MOT-6 | 10 | scattered higher error floor on periodic stimuli; shares genuine trap fixture rtC_0010 with MOT-5 |
| MOT-7 | 2 | zero utility on weak motion: 0/40 installs on flat noise while formation was 39/40 correct |

FS-GR1 FI-item recurrence (`e2b_adv_motiondir_34236`, formation claimed W, truth SE):
**MOT-5 RECURS, MOT-6 RECURS, MOT-4 withholds, MOT-7 correctly disagrees/withholds.**

## 5. Per-candidate diagnosis

- **MOT-4 (ZNCC-peak):** the uncorrelated-measurement thesis held on the *safety* axis —
  a different similarity formulation fails in different places than formation, so it never
  agrees-with-wrong (0/630 FI, red-team clean). But the sharpness gate (corr ≥ 0.5, 6.25%
  sidelobe margin) is too strict: resolve rate only 76–77%, and the withholds cost 5.5pp
  recall vs FS-GR1. Safety without liveness.
- **MOT-5 (evidence accumulation):** the quadratic abstention boundary `margin² > E` did not
  abstain — it resolved wrong with high confidence (99–100% resolve rate, 19 FI, several
  exact-reverse installs). Accumulating the full landscape *amplified* the correlated error
  instead of hedging it. Worst of both worlds.
- **MOT-6 (temporal-quorum):** liberal per-witness plurality + strict agreement sounded safer,
  but plurality is plurality — the witnesses share the same measurement family as formation,
  so their errors correlate and agreement does not buy what independence would. Dominated by
  FS-GR1 on both axes.
- **MOT-7 (Lucas–Kanade):** per-lag LK without a coarse-to-fine pyramid cannot handle the
  fixtures' ~4px/2-frame displacements (verified by independent Python reimplementation —
  not a code bug). Flow collapses toward STILL (106/200 ctrl outcomes voted STILL, 22 truly
  were). Mechanism wrong for this regime, not merely mis-tuned.

## 6. Round lesson

The round-2 thesis was: *a challenge with structurally uncorrelated failure modes can
resolve more often while agreeing-wrongly more rarely.* The evidence says the thesis is
**half-right**: MOT-4 proves uncorrelated measurement buys real safety (0 FI, red-team
clean). But none of the four bought *liveness*: every abstention mechanism tried so far
(strict majority, sharpness gate, quadratic boundary, cross-witness agreement, aperture
eigenvalue gate) taxes recall harder than it pays in FI reduction. The safety/liveness
tradeoff is not an artifact of one correlated measurement path — it survives across four
independent mechanism families. The next round must attack the *voting/abstention geometry*,
not the measurement family: the open question is a rule that withholds exactly on the
fixtures formation gets wrong, rather than withholding broadly.

## 7. Evidence committed (this commit)

- `src/fsg2_mot{4,5,6,7}_sup.zag` — candidate supervisor sources (diff-scoped to the
  motiondir challenge path + challenge ID; everything else byte-identical to FS-GR1)
- `evidence/eval/mot{N}/` — adv/ctrl raw outputs r1+r2, hash-chained ledgers, worker score scripts
- `evidence/redteam/` — hostile corpora RT-A..RT-D (288 `.r2fx` + `.truth` + manifest with
  generation seeds), `gen_redteam.py`, `score_redteam.py`, `score_redteam.json`, raw outputs
- Binaries, `.zagd`, and `.zag-cache/` are NOT committed (per standing rule).

## 8. Round-3 hypotheses (proposed, not launched — needs its own prereg)

1. **MOT-4 gate relaxation:** sweep the ZNCC sharpness gate (corr threshold, sidelobe margin)
   as a *parameter study*, not a mechanism change — the safety came from ZNCC, the recall
   loss from the gate. (Note: this edges toward "tuning"; prereg must pin the sweep grid.)
2. **ZNCC + formation hybrid vote:** challenge resolves by ZNCC-peak, but the *vote* is
   formation's SAD-argmin direction — decouple measurement (safety) from direction
   estimation (liveness).
3. **Disagreement-triggered escalation:** run the cheap formation-correlated challenge first;
   escalate to ZNCC-peak only when it disagrees with formation — spend the conservative
   gate exactly where it pays.
4. **Coarse-to-fine LK:** the honest LK repair (image pyramid) — tests whether the gradient
   family was wrong or just under-built.
