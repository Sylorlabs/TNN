# REPORT.md - DEVANG6 Lane Report to Coordinator

Lane worker DEVANG, wave wave-20261002-1121pdt, queue item 4.
Branch: lane-devang-20261002-1121pdt. All commits local, never pushed.

## Numbers first

- K_ABL (recalibrated, gap >= 4): PASS. Learner 12/12, ablation 5/12, gap 7.
  K1 gap 2 >= 2. The recalibration is validated on a fresh draw.
- K_SEG: 12/12. PASS.
- K_SEAL: 9/20 < 12/20. FAIL. This kills the build.
- K_DISC: 6/6 (premise 2/6). PASS.
- K_SAME / K_AUD / K10 / K11 / K_C0 / K8: PASS.
- Verdict: BUILD-FAIL (K_SEAL), classified MECHANISM RESULT.

## Candidates

DEVANG6 proposed no new mechanism (by design; this was a measurement wave).
The candidate under test was the RECALIBRATED K_ABL bar itself: KEEP. It is
purpose-fit (the gap measures what the ablation removes), stricter than the
old bar against vacuous front-ends (fails gap-1 where old bar passed), set
with an anti-fit margin (4 vs observed 6), and it passed on fresh data with
slack (7 >= 4). The old bar would also have passed this draw (5/12), so the
recalibration manufactured nothing.

The FINREG/POSSEG mechanism (inherited byte-identical from DEVANG5):
DISCARD as a sealed-generalization solution. It does not robustly clear
12/20 on fresh vocabulary (draws: 12, 14, 9) and never beats fixed-3 on any
C-family (12v14, 14v14, 9v11). Kill evidence: K_SEAL 9/20 on C-tripleprime,
which included an intentional prefix-ambiguity stress.

## Commit ids

76361ff85 (Step 0) -> bda385c32 (prereg ALONE) -> c72b40a54 (E-prime
baseline) -> f541f16e3 (implementation) -> 1e852dbb2 (sealed package) ->
[this commit] (eval, red team, debate, verdict, report, build log).
Commit-order self-check: PASS (prereg strictly first).

## Red-team findings

Six attacks, all fail to kill:
- A (retrieve/replay): fails; FIN_* from learner's own segmentations,
  E-prime fresh tuples 6/6, ablation gap 7.
- B (impossibility proof): holds in-scope; escape hatch is the L3 criterion.
- C ("bar chosen to pass"): fails; four honesty arguments + fresh-data pass
  with slack + old bar would also pass.
- D (metric gaming): fails; floorcheck incident was a compiler bug caught by
  the lemma, fixed and re-measured; the kill is reported honestly.
- E (K_SEAL miscalibration): fails to overturn; real capability gap, though
  draw variance (12,14,9) is a noted caveat.
- F (E-prime memorization): fails; binary predates the tuples.

Debate (advocate/skeptic/judge) upheld: recalibration validated, BUILD-FAIL
stands, kill classified as mechanism result.

## Incidents

FOURTH pinned-znc miscompile found and documented: `!(A && B)` in a while
condition miscompiles (verified via isolated repros; De Morgan form works).
It corrupted only floorcheck.zag (new code); grep-verified absent from
devang6.zag, genseal6.zag, scoree.zag. Caught by the fixed-3 lemma
contradiction, fixed, re-measured (true floor 7/12, consistent with ablation
5/12). Recorded in ~/AGENTS.md as mandatory workaround. Governance note:
four independent miscompile patterns now documented; toolchain fitness for
sealed evaluation deserves review.

## Queued next

1. Multi-draw K_SEAL calibration (12/20 near observed mean; noisy).
2. Independent-adversary replication of K_SEG/K_SEAL/K_ABL.
3. Attack the C-family deficit (learner never beats fixed-3 on novel vocab).
4. znc toolchain fitness review (governance).
