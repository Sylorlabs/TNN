# REPORT: L3-NIV2 Wave 4 (2S-CALR staged deepening)

Verdict: **BUILD-PASS**. All five frozen kill bars green. Staged
deepening works; CALR extends beyond depth 3.

Wave: 4 (replacement for completed wave-3 worker). Lane: commit
`e61c9c50c` on `lane-compinteg2-20261002`, dir
`docs/lab/research-lead/overnight-20260928/l3_novel_intermediate_v2/`.
Prereg frozen as `b956ffc15` (PREREG_WAVE4.md + NAMECHECK.md Step 0
only, before any wave-4 implementation). Implementation commit follows
this report.

## 1. What was built

2S-CALR (two-stage CALR), per PREREG_WAVE4.md sections 2-4:

- Stage 1: wave-3 CALR verbatim, plus Y1 yield rule. Phase C verifies
  prefixes in (potential_1 desc, score desc, id asc) bucket order and
  stops at first full acceptance (COMMIT) or when the next bucket's
  potential_1 drops below pmax_1 (YIELD to stage 2). Complete for
  depth-3 by theorem T1.
- Inter-stage: all 6400 depth-2 prefixes, Phase-A scores, and grown
  fhat carry into stage 2. No pruning, no quotas. Ordering only.
- Stage 2 (new file `impl/lm_cons4.zag`): Phase B2 computes
  potential_2 (max over 80x80 append pairs, local simulation, zero
  TESTs) for all 6400 prefixes. If pmax_2 < nk, principled early
  DEFER. Phase C2 verifies in (potential_2, score, id) order with
  nested complete descent: for each max_2 prefix, compute p1d0(c1)
  (max over 16 d=0 appends) for all 80 c1, then TEST P+c1+c2 for c1
  at max and d=0 c2 in the argmax (byte order). The d=0 restriction
  is the D2 provable prune (stage-1 completeness implies any depth-4
  solution's final instruction writes r0). Complete for depth-4 by
  theorem T2.
- Minimal edits: `fharv_on` added to `lm_cons.zag` (re-enable fhat
  without clearing, for stage-2 dynamic fhat); Y1 break and stage-2
  branch in `construct_calr` (`lm_cons3.zag`); `lm_cons4.zag` added
  to `battery.sh` build.

No new opcodes, no new semantic cases, no modes/bridges/handlers.
5-op ISA unchanged. No beam quotas.

## 2. Kill bar adjudication

### W4K1: T1 COMMITS on DEV-S2 via stage-2  -  GREEN

T1 (transfer=0) on DEV-S2 (y = x^2+x+1, depth-4 target):

- `CALR-HARVEST 2 6400 7668` (fhat covers 2 inputs, 7,668 TESTs;
  matches baseline exactly).
- `CALR-RANK 433 1677 1497 2 2` (P2 id 433, pot1-rank 1677,
  score-rank 1497, max1=2, nk=2; matches baseline exactly).
- Stage 1 yields after the max_1 level (211 verifications, 0 found).
- `CALR2-RANK 433 149 2 2 2` (P2 id 433, pot2-rank 149, pot2=2,
  max2=2, nk=2).
- `CALR2-FOUND 8459 465 9` (depth-4 program id 8459 accepted, via
  prefix id 465, at the 9th prefix expansion).
- `CALR2-DONE 1 1 13608` (accn=1, stage-2 found=1, 13,608 TESTs).
- `CAND 8459 465 1 4 000100040000020001040000`: bytes decode to
  [CPY r1,r0][INC r0][MUL r0,r1][INC r0] = (x+1)*x+1 = x^2+x+1.
  Valid depth-4 solution (distinct from the refprog, which is fine;
  the bar requires a committing depth-4 program).
- `SCORE 6 6 PASS` (6/6 on held-out x=6..11).
- `ARM-END T1 PASS`.

### W4K2: 3/3 byte-identical  -  GREEN

Three T1-on-DEV-S2 runs, sha256
`a72b50d1740623284340d7e16c68014c9fa9c2442d6599d52984b1eff946b724`
for all three. (Note: parallel battery.sh runs interfere via shared
FIFOs; the 3x were run sequentially.)

### W4K3: TEST budget  -  GREEN

13,608 total TESTs, well under B_CONSTRUCT = 50,000. The design-time
probe predicted 13,608 exactly.

### W4K4: DEV-S1 no-regression  -  GREEN

T1 on DEV-S1: log sha256
`5221c529905ee07d80e573ece060722fc743896b7385575d7e85e6577d1c1f02`,
byte-identical to the wave-3 canonical log. `CALR-FOUND 15257 433
229` (commit at verification #229 via stage-1 path, as wave-3). No
CALR2 lines (stage-1 found it, correctly did not trigger stage-2).
Stage-1 code path and order are unchanged on DEV-S1.

### W4K5: diagnosis  -  GREEN

P2 (bytes 00 01 00 02 00 00, id 433):

- Stage-1: `CALR-RANK 433 1677 1497 2 2`. Rank 1677 by
  (potential_1, score, id), max_1=2. P2's potential_1=1 (verified:
  with fhat={0->1,1->3}, the best 1-step append [INC r0] gives
  x^2+1, matching only x=0). So potential_1=1 < 2=max_1.
- Stage-2: `CALR2-RANK 433 149 2 2 2`. Rank 149 by (potential_2,
  score, id), pot2=2=max_2=nk. The pair ([ADD r0,r1],[INC r0])
  witnesses full agreement.

The 1-step potential is blind to P2's 2-step latent utility (rank
1677); the 2-step potential sees it (rank 149, at max). Diagnosis
confirmed, not falsified.

## 3. Predictions vs actual (PREREG_WAVE4.md section 3)

- P1 (P2's pot2 rank <= 200): actual 149. PASS.
- P2 (P2: pot1 < max1 AND pot2 == max2): actual pot1=1<2=max1,
  pot2=2=max2. PASS.
- P3 (stage-1: 211 max_1 verifications, <5,000 TESTs, 0 found):
  actual 211 verifications, 0 found (TESTs consistent with probe's
  2,748; total 13,608 matches probe exactly). PASS.
- P4 (stage-2: find within 12 expansions, total <20,000 TESTs):
  actual 9 expansions, 13,608 total. PASS (exact match to probe).

All four falsifiable predictions held, three of them exactly.

## 4. Why it works (mechanism summary)

The wave-2 failure (beam pruned crucial prefix at rank 326) and the
wave-4 baseline failure (1-step potential ranked P2 at 1677) share a
root cause: a fixed-horizon lookahead cannot see latent utility that
materializes k steps out. 2S-CALR addresses this by RAISING THE
HORIZON between stages, not by widening a beam. The inter-stage rule
is retention-by-default (all 6400 prefixes survive, ordered by
consequence-anchored potential) plus two provable prunes: Y1 (stage-1
completeness for depth-3) and d=0 (stage-1 completeness implies the
final instruction of any depth-4 solution writes r0). No score-based
pruning, no quotas. The CALR no-pruning principle is preserved.

## 5. Honest limitations

- 2S-CALR covers depth 4 only. Length 5-6 need a third stage
  (3-step potential); wave-5 work. The max_2 < nk early DEFER is
  honest about this boundary.
- The d=0 prune is complete only because stage-1 C1 is complete for
  depth-3; it does not generalize without the corresponding
  completeness argument.
- Stage-2 nested descent is TEST-hungry per prefix (~350 TESTs);
  if a future target's solution prefix ranks deep in potential_2
  order, the budget binds. fhat strengthening is the principled fix;
  deferred.
- T4 (transfer) still uses the wave-2 beam engine; T3 revise
  unchanged. KC0B adjudication stays with the K10 red team.
- Phase C1's dynamic argmax vs Y1's fixed yield level asymmetry is
  disclosed (PREREG_WAVE4.md section 9).

## 6. Artifacts

- `impl/lm_cons4.zag` (new): stage-2 implementation.
- `impl/lm_cons3.zag` (modified): Y1 yield + stage-2 branch.
- `impl/lm_cons.zag` (modified): `fharv_on` added.
- `impl/battery.sh` (modified): includes `lm_cons4.zag`.
- `impl/learner_bin` (rebuilt).
- Run logs: `impl/run_t1_devs2_w4{,b,c}.log` (3/3 identical),
  `impl/run_t1_devs1_w4.log` (byte-identical to wave-3).
- Baseline (wave-3 code on DEV-S2): `/tmp/baseline/` (not committed).

## 7. Verdict

**BUILD-PASS.** W4K1, W4K2, W4K3, W4K4, W4K5 all green. The staged
deepening design (2S-CALR) is validated: CALR extends beyond depth 3
via horizon-raising with provable inter-stage prunes, preserving the
no-pruning principle. The honest limitation is now depth 5-6 (third
stage), which is wave-5 work.
