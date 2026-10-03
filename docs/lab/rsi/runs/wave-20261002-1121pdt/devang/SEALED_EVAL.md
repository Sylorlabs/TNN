# SEALED_EVAL.md - DEVANG6 Sealed Evaluation

Wave: wave-20261002-1121pdt. Lane: DEVANG (queue item 4).
Prereg: PREREG_DEVANG6.md (commit bda385c32, frozen before implementation).
Mechanism: devang6.zag (commit f541f16e3). Sealed package: commit 1e852dbb2.

## Sealed package integrity (verified pre-run)

SHA256SUMS committed in sealed6/ before any sealed execution:
- sealed_b6.txt: db1b02c7...
- sealed_b6_key.txt: 964b71a3...
- sealed_c6.txt: d30ef174...

All sealed runs: 3/3 byte-identical, zero stderr. Hashes re-verified before each run.
Sealed inputs/keys never read directly; only mechanical aggregate scorers used.

## Per-bar results

### K_SEG (Family B-tripleprime, learner): 12/12. PASS (>= 10/12).

### K_ABL leg 1 (recalibrated): gap = 7 >= 4. PASS.
- Learner K_SEG: 12/12.
- Ablation (segb-abl, fixed-3): 5/12.
- Gap: 12 - 5 = 7, bar >= 4. Passes with 3 points of slack.
- Fairness floor (spec guard, not a bar): 7/12 B-utterances contain a word of
  length != 3 (see incident note below). Floor >= 4 satisfied.

### K_ABL leg 2 (Family A dev, carried): gap = 2 >= 2. PASS.
- Learner K1: 10/10. Ablation K1: 8/10. Gap 10 - 8 = 2.

### K_DISC (Family E-prime, frozen devang4 baseline): PASS.
- Baseline premise: 2/6 (frozen devang4 binary, 3/3 byte-identical, sha
  50c16fe0...). Premise <= 2/6 holds.
- Learner: 6/6. 6/6 vs 2/6, premise satisfied, bar (>= 5/6 with premise) PASS.

### K_SEAL (Family C-tripleprime, learner): 9/20. FAIL (bar >= 12/20).
- Learner: 9/20. Controls: c0 5/20, c2 (fixed-3) 11/20, c1 7/20, c3 7/20.
- 9 < 12. K_SEAL FAILS. This is the killing bar; verdict BUILD-FAIL.

### K_SEG (Family A dev, regression): 10/10 K1; K2..K7,K9 7/7; test 20/20. PASS.
### K_C0 (Family A dev): 35pp / 7 words. PASS.
### K8 (Family A dev): exactly 15pp. PASS.
### K_SAME: PASS. devang6.zag differs from devang5.zag by exactly 2 comment
lines (banner); compiled binary sha256
a11bd3506987a83ee2f502a78e9af686e92b6cf53ff89d4b950e5dbb3d1e03df,
byte-identical to the frozen DEVANG5 binary. Family A dev output byte-identical.
### K_AUD / K10 / K11: PASS (carry-forward). Comments-only diff vs devang5.zag,
which passed these audits in DEVANG5. Single _zag_print is the emit passthrough
(sanctioned pattern); no dynamic-content _zag_print; no as *i32 slices in
functions; no negated-conjunction while conditions (grep verified).

## Incident: floorcheck miscompile (resolved, did not affect sealed results)

During evaluation, a contradiction appeared: floorcheck reported FLOOR 12/12
(all B-utterances contain a non-3-char word), which by the fixed-3 lemma implies
the ablation should score 0/12, but the ablation measured 5/12.

Root cause: a FOURTH pinned-znc miscompile. The pattern
`while(arrow<ke-2 && !(fk[arrow]==61 && fk[arrow]==62))` miscompiles: the scan
ran past the match (returned 9 instead of 7 on a known input). Isolated repros
confirmed: the De Morgan form `(fk[arrow]!=61 || fk[arrow+1]!=62)` returns the
correct 7; a hoisted-flag version returns 7; the `!(X && Y)` form fails
regardless of && operand order.

The pattern appeared ONLY in floorcheck.zag (grep verified absent from
devang6.zag, genseal6.zag, scoree.zag). Sealed results are unaffected.

Fix: rewrote both instances via De Morgan; verified 2/12 on synthetic data
with known answer 2; re-ran on the sealed key. TRUE FLOOR: 7/12 (still >= 4,
spec guard satisfied). The 7/12 floor is exactly consistent with the ablation's
5/12 (5 all-3-char utterances where fixed-3 is correct, 7 with a non-3 word
where it provably fails). Lemma, key, and scorer now agree.

The defect is recorded in ~/AGENTS.md as a mandatory workaround.

## K_SEAL failure analysis

The mechanism is byte-identical to DEVANG5's (which scored 14/20 on
C-doubleprime), so the 14 -> 9 drop is entirely a family-draw effect, not a
mechanism change.

C-tripleprime was deliberately adversarial: the vocabulary includes an
intentional zora/zoraxu prefix-ambiguity stress (documented in genseal6.zag),
not present in C-doubleprime. This makes it a harder test by design.

Cross-family learner scores: DEVANG4 C-prime 12/20, DEVANG5 C-doubleprime
14/20, DEVANG6 C-tripleprime 9/20. The learner has NEVER beaten fixed-3 (C2)
on any C-family: 12v14, 14v14, 9v11. FINREG/POSSEG provides no advantage on
all-novel vocabulary; the base learner is at-or-below fixed-3 chunking there.

Classification: MECHANISM RESULT, not bar-miscalibration. The bar measures the
right quantity (fresh-vocabulary accuracy); the threshold (12/20) was frozen
before C-tripleprime existed; the test was adversarial by design; and the
consistent learner <= C2 pattern across three families indicates a genuine
capability gap (no robust generalization to novel vocabulary with ambiguity),
not a threshold error. The draw variance (12, 14, 9) is noted as a caveat:
single-draw C-family estimates are noisy, and a future wave should calibrate
K_SEAL across multiple draws rather than inheriting a threshold fit near a
single observation (DEVANG4 hit 12/20 exactly).

Per the task: the bar is NOT re-tuned. The kill stands.

## Verdict

BUILD-FAIL. Killing bar: K_SEAL (9/20 < 12/20).
The recalibrated K_ABL PASSES (gap 7 >= 4): the recalibration is validated as
a working bar (it discriminates; it passed here with real margin on a fresh
draw). The failure is in sealed generalization, not in the ablation logic.
