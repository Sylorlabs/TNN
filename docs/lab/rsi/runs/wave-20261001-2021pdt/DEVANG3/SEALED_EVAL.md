# SEALED_EVAL.md: DEVANG3 sealed evaluation (adversary)

Worker: DEVANG3-ADVERSARY, wave-20261001-2021pdt. Frozen binary
`DEVANG3/devang3`, SHA-256
`7006ce4d23bdacf5f0c8fed1362e92451822b14ee3204ed23cb35027434e354e`
(verified before any run; match). Pure Zag; safebin; no forbidden
executable invoked. The builder's dev files were never opened. Sealed
files were written and their sha256 recorded in SEALED_B.md/SEALED_C.md
before any sealed run.

## K_AUD: segmentation-dependence audit (code inspection of devang3.zag)

Verdict: PASS on all three prereg claims. Relevant code quoted.

Claim (a): every statistics table is updated only from segmenter output.
All W writes in the learner path derive from `segs[]` (lexicon indices
produced from the segmenter's tmp), never from raw bytes:

- Lexicon counts: `lex_bump` does
  `set32(W,2720+li*24+20, get32(W,2720+li*24+20)+1)` (line 256), with
  `li` from `segs[]`.
- Grounding (W 4256..6304): lines 557-559,
  `set32(W,4256+(li*8+tc)*4,...+1)` etc., per `li=get32(segs,i*4)`.
- Negator stats (W 6304..6816): lines 571,573, per adjacent pair
  `(mi,xi)` from `segs[]`.
- Comparative stats (W 6816..7328): lines 592,603, per adjacent pair
  from `segs[]`.
- The bigram table seg_int (W 0..2704) is written only at line 543,
  inside the `if(rawmode==1)` branch.

Claim (b): no code path reads raw utterance bytes into any statistics
table on the learner path.

- The only raw-byte-to-W read is lines 539-540
  (`let ba:i32=(ep[48+k] as i32)-97;`), gated by `if(rawmode==1)`.
- Learner call sites all pass rawmode=0: `mode_segb` line 950
  (`learn_update(W,segs,nseg,ep,48,ulen,0)`), fama learner line 1258,
  `sealc_train_one` line 1047 (`let rm:i32=0; if(variant==1){ rm=1; }`),
  ablation line 1391. The rawmode=1 call sites are the C0 control only
  (lines 1047 with variant==1, 1477).
- `seg_dp_raw` (the only reader of seg_int) is called only for
  variant==1 / C0 (lines 1037, 1098, 1469, 1487); the learner segmenter
  is always `seg_dp` (lines 943, 1038, 1241, 1300).
- Other `ep[48..]` reads are not statistics: line 1014 is
  `sealc_parse_ep` file ingestion into the episode buffer; lines
  1028, 1066, 1082 are C1/C3 control memorization/matching.
- `lex_get_add(W,ep,48+off,len)` reads segment bytes at the
  segmenter's declared (off,len); that is segmenter output, the one
  allowed door for bytes.

Claim (c): the cold-start path is inside the segmenter and feeds the
same statistics update.

- Cold start is lines 357-370, inside `fn seg_dp` (defined line 356),
  triggered by `if(get32(W,2704)<10)` (nlex<10), emitting 3-char chunks.
- Every caller runs the segmenter then the same update: `mode_segb`
  lines 943/950, fama lines 1241/1258, `sealc_train_one` lines
  1038/1047. No bypass exists.

K_AUD: PASS. No DEVANG2-mode recurrence in the learner path.

## Sealed runs (3/3 byte-identical each; exit 0; zero stderr)

- `segb sealed/sealed_b.txt` (learner): sha256
  `9aa2a94650083ebea8fd9dc4efd91e7ef46ffe8f8d7b7f4216e3f87a635f83bf`
  x3.
- `segb-abl sealed/sealed_b.txt` (fixed-width-3): sha256
  `f655b4b30c3677d5dd66a50a713012d7405a73b62b6e44be5e3c73f14ed6c3bf`
  x3.
- `sealc-fresh sealed/sealed_c.txt learner`: sha256
  `1e2c3ec99962e8a438bf9ef541a595f543b74d39f87cf48f72d6135a94690a6e`
  x3. Output: SEALC 11/20.
- `sealc-fresh ... c0`: SEALC 11/20, 3/3 identical.
- `sealc-fresh ... c2`: SEALC 7/20, 3/3 identical.
- `sealc-fresh ... c1`: SEALC 10/20, 3/3 identical.
- `sealc-fresh ... c3`: SEALC 10/20, 3/3 identical.
- `fama` (default): 3/3 byte-identical, exit 0, zero stderr x3.

## Per-bar results

- KR0 (crash gate): PASS. 3/3 fama runs: exit 0, zero stderr bytes.
- K1 (>= 8/10): PASS. 10/10 from the t=60 lexicon snapshot (fama).
- K_SEG (>= 9/12 exact-boundary on sealed Family B): FAIL. Learner
  8/12. Failures (learner output vs key):
  - probe 6 `blumalagrn`: got `3` ([blu][malagrn]), key `3,7`.
  - probe 8 `grnsalabal`: got `7` ([grnsala][bal]), key `3,7`.
  - probe 9 `takbigerkala`: got `3,6` ([tak][big][erkala]), key `3,8`.
  - probe 12 `nottemagrn`: got `3` ([not][temagrn]), key `3,7`.
  Analysis: probes 6, 8, 12 merge a novel word with an adjacent known
  word, consistent with the known word's lexicon score being too low
  to beat the merge (e.g. "grn" occurs only in phase 2, so its
  frequency score loses to the -50 merge penalty arithmetic). Probe 9
  resolves the big/biger prefix ambiguity toward "big", i.e. the
  frozen lexicon scores s(big) > s(biger). These are genuine
  segmentation errors on valid ambiguity probes, not key errors.
- K_SEAL (>= 12/20 on sealed Family C): FAIL. Learner 11/20
  (sealc-fresh). Per-test: correct on tests 1,4,5,8,9,10,11,13,16,
  17,19; wrong on 2,3,6,7,12,14,15,18,20. The learner is correct on
  all 10 tgt=0 episodes but only 1 of 10 with tgt=1 or 2, indicating
  the new-vocabulary grounding/segmentation does not support the
  novel combinations (including the 4 "zokanatemo" raw-byte-trap
  episodes, of which 2 were missed).
- K_AUD: PASS (above).
- K_ABL: task reading (ablation < 9/12 on sealed Family B): PASS.
  Ablation scores 3/12 (correct only on probes 4, 7, 10, the three
  all-multiples-of-3 utterances). Prereg Family-B leg (<= 5/12):
  PASS. Note: the prereg's Family-A leg (ablation K1 < 8/10) is not
  met (ablation K1 = 8/10 from fama); the builder reported this
  deviation in IMPLEMENTATION.md. Per the task's operationalization
  the binding K_ABL test is the sealed Family B leg, which passes.
- K_C0: prereg reading (Family A test accuracy margin >= 15pp AND K1
  margin >= 3): PASS. Learner 20/20 vs C0 13/20 = 35pp; K1 10 vs 3
  = 7 words (fama output confirms `K_C0 control-trails: 1
  (dAcc_pp=35 dK1=7)`). Task reading (raw-byte control trails by
  >= 15pp on the sealed families): FAIL. On sealed Family C,
  C0 = 11/20 vs learner = 11/20, margin 0pp. The raw-byte control
  matches the learner exactly on the sealed adversarial family.

## Verdict

BUILD-FAIL. Killing bar: K_SEG (8/12 < 9/12). K_SEAL also fails
(11/20 < 12/20), and K_C0 fails on the sealed-family reading (0pp
margin; C0 ties the learner at 11/20).

Per prereg section 9, this is a mechanism result, not an
architectural-recurrence result: K_AUD, the prereg K_C0, and the
K_ABL Family-B leg all pass, so the segmentation-dependence design
requirement holds; the segmenter quality is insufficient on the
sealed ambiguity cases (K_SEG) and on the post-freeze adversarial
family (K_SEAL), and the win over the raw-byte architecture does not
replicate on sealed Family C (K_C0 sealed reading).

## Determinism evidence

Every sealed command was run 3/3 with byte-identical stdout (sha256
recorded above), exit code 0, zero stderr bytes. K12-style
determinism holds for all families and variants run here.

## Notes for the coordinator

1. Commit order: this worker does not commit (per task). Sealed
   sha256 values were recorded in SEALED_B.md/SEALED_C.md before any
   sealed run. The coordinator must verify the committed sealed files
   match these hashes; the sealed-evaluation run necessarily preceded
   the commit in this wave's worker flow, and the prereg section
   5.5 commit-order check should be applied to those hashes.
2. Prereg vs task reading discrepancies are documented above for
   K_ABL (Family-A leg) and K_C0 (sealed vs Family A). The verdict
   follows the task's verdict rule; the prereg-letter numbers are
   reported alongside.
3. No em dashes were used in any adversary-written file.
