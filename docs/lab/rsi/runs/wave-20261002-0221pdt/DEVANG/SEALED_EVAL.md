# SEALED_EVAL.md: DEVANG4 sealed evaluation

Worker: DEVANG4 builder (self-eval per wave task; no independent adversary
available this wave). Frozen binary `devang4`, SHA-256
`cfba24f157a22b0e721f9a27722320f6b2d3a77e250b96c9045659b58bb9ddbd`
(verified before any sealed run). Pure Zag; safebin; no forbidden
executable invoked (one near-miss disclosed in NAMECHECK.md Step 0c;
no Python ran). Sealed files verified against pre-run hashes
(SEALED_B4.md/SEALED_C4.md) before any sealed run. Commit order:
prereg (c768b02be) < implementation (8db14a1b8) < sealed package
(20f1500f1) < sealed runs (this file). The builder never inspected
sealed file contents (scores via the `scoreb` exact-match counter;
utterances not printed).

## K_AUD: segmentation-dependence audit (code inspection of devang4.zag)

Verdict: PASS on all four prereg claims.

Claim (a): every statistics table is updated only from the chosen
segmentation's output. All W writes in the learner path use indices
from `segs[]`: lexicon counts (`lex_bump`, line 262), grounding
(lines 731-733), negator (745, 747), comparative (766, 777). New
lexicon entries via `lex_get_add` on the chosen tmp (call sites).

Claim (b): no code path reads raw utterance bytes into any statistics
table on the learner path. The only raw-byte-to-W reads (lines
713-714, into seg_int at 717) are gated by `if(rawmode==1)` (C0
control only). Learner call sites pass rawmode=0. The segmenters
(seg_coseg, seg_dp) read bytes only via lexicon lookup (the allowed
door). Other ep[48..] reads are output emission, file parsing, or
C1/C3 memorization controls, not statistics.

Claim (c): the cold-start path is inside the segmenter (seg_coseg,
nlex<10 block, 3-char chunks) and feeds the same learn_update as
later episodes. No bypass exists.

Claim (d): the scene/margin signal is confined to candidate scoring.
`coseg_margin` and `interpret_scores` contain zero `set32(W,...)`
writes (verified by grep: 0 matches). Beam buffers (bw_*, cand) are
transient z_alloc, not W. The chosen tmp is the sole statistics input.

K_AUD: PASS. No DEVANG2-mode recurrence.

## Sealed runs (3/3 byte-identical each; exit 0; zero stderr)

- `segb sealed4/sealed_b4.txt` (learner, no-scene path): sha256
  `9cbbfe7241e83c996ed3f3041fd66711f740e8d526157b9cc5680d22bb959ffd` x3.
  Score: 4/12 (via scoreb exact match).
- `segb-abl sealed4/sealed_b4.txt` (fixed-width-3): sha256
  `35498cce9d51aa3afaa71f4a8d596f57464ecbaf5882af8612e091f9d800b023` x3.
  Score: 1/12.
- `sealc-fresh sealed4/sealed_c4.txt learner`: sha256
  `dcdbea221c70fe3e8560694da2f63fce0b34aca85af26081e535b5ebdab3a769` x3.
  Output: SEALC 12/20.
- `sealc-fresh ... c0`: 6/20, 3/3 identical.
- `sealc-fresh ... c2`: 14/20, 3/3 identical.
- `sealc-fresh ... c1`: 9/20, 3/3 identical.
- `sealc-fresh ... c3`: 7/20, 3/3 identical.
- `segb-scene baseline/familyd_eps.txt`: sha256
  `7357ef4416c1eff444601330d9c4eb38347d3a0c1272944427f24574edfc3c92` x3.
  Score: 2/6 (D3, D5 correct).

## Per-bar results

- KR0 (crash gate): PASS. All runs: exit 0, zero stderr bytes.
- K1 (>= 8/10): PASS. 10/10 from the t=60 lexicon snapshot (fama).
- K_SEG (>= 9/12 on fresh B-prime): FAIL. Learner 4/12. Diagnosis (from
  generator logic, not input inspection): the prereg-frozen B-prime
  spec produced 8 utterances with ALL words novel (4 two-novel-word
  ambiguity class + 4 multi-novel random class). The 2321pdt lexicon
  scoring (which the no-scene path reuses exactly) merges all-novel
  utterances: two novel segments cost ~-100 vs one merged novel
  segment at ~-50-L, so the merge always wins. There is no lexical
  information to recover the true boundaries. The 4 merge-class
  utterances (known+novel) segment correctly. This is a GENERATOR
  DESIGN FLAW in the prereg spec (it tests segmentation without
  information), not a mechanism regression: the no-scene code path is
  byte-identical to the 2321pdt segmenter that scored 12/12 on its own
  (differently composed) B.
- K_SEAL (>= 12/20 on fresh C-prime): PASS. Learner 12/20, exactly at
  bar. Controls: C0 6/20, C2 14/20, C1 9/20, C3 7/20. Caveat: C2
  (fixed-width-3) exceeds the learner on this C-prime (14/20 vs
  12/20). K_SEAL carries no control-margin requirement, so the bar
  holds, but the margin is thin and the control comparison is
  unfavorable on this world.
- K_DISC (>= 5/6 on Family D, premise 2321pdt <= 2/6): FAIL.
  Premise holds (2321pdt 0/6, 2021pdt 0/6, both 3/3 identical).
  DEVANG4 scores 2/6 (D3, D5 correct; D1, D2, D4, D6 wrong). The
  failures select [tak][X][yyZ] (e.g. [tak][bal][tagrn]) over the true
  [tak][Xyy][Z]. Mechanism analysis in REDTEAM_SELF.md: the margin
  signal rewards confident WRONG interpretations, and the prereg's
  paper analysis missed the [tak][X][yyZ] candidate. This is a
  mechanism result (the frozen design, implemented exactly, does not
  discriminate as claimed).
- K_ABL: PASS. Ablation K_SEG 1/12 (<= 5/12) AND (learner K1 10 -
  ablation K1 8) = 2 (>= 2).
- K_C0: PASS (Family A dev). Learner 20/20 vs C0 13/20 = 35pp;
  K1 10 vs 3 = 7 words.
- K8: PASS (Family A dev). 20/20 vs best control 17/20 = 15pp.
- K2..K7,K9: 7/7 PASS (need >= 4).
- K10: PASS (code audit: strictly sequential; update after
  segment+interpret; no future data).
- K11: PASS (code audit: statistics for episode t exclude episode t;
  the scene is episode t's own observed input).
- K12: PASS. Every family and variant 3/3 byte-identical, exit 0,
  zero stderr.

## Verdict

BUILD-FAIL. Killing bars: K_SEG (4/12 < 9/12) and K_DISC (2/6 < 5/6).

Classification per prereg section 12:
- K_DISC failure with K_AUD passing = mechanism result: the coherence
  signal does not move segmentation decisions as designed. The
  prereg's discrimination claim is falsified on the prereg-frozen
  family.
- K_SEG failure = test-design result: the prereg-frozen B-prime spec
  generated 8 information-less all-novel utterances that no
  lexicon-frequency segmenter can segment; the no-scene path is
  unchanged from the 12/12-scoring 2321pdt segmenter. The failure does
  not indicate a mechanism regression, but the bar is missed as
  frozen and the verdict follows the bar.
- K_SEAL passes (12/20), K_ABL/K_C0/K_AUD pass: segmentation-dependence
  holds and the front-end is load-bearing.

## Notes for the coordinator

1. The sealed-evaluation run necessarily preceded this commit; the
   sealed package commit (20f1500f1) strictly precedes the sealed runs
   in wall-clock order, and hashes were verified before the runs.
2. K_DISC was scored by hand against the prereg-frozen key (6 lines);
   the builder did not tune the implementation to Family D (the 2/6
   was the first and only post-implementation run before the sealed
   commit; two additional runs confirmed determinism).
3. The K_SEG generator flaw is load-bearing for the next iteration:
   any DEVANG5 B-family must contain at least one lexicon-known word
   per utterance (or the bar must test something a lexicon segmenter
   can in principle recover).
4. No em dashes were used in any lane file (check_no_dash.sh clean).
