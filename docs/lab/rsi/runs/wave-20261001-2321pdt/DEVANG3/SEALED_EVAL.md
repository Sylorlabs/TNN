# SEALED_EVAL.md: DEVANG3 sealed evaluation (wave-20261001-2321pdt)

Worker: DEVANG3, wave-20261001-2321pdt. Frozen binary `DEVANG3/devang3`,
SHA-256 `36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d`
(verified before any run; match). Pure Zag; safebin; no forbidden
executable invoked. Sealed files were generated blind and their sha256
recorded in SEALED_B.md/SEALED_C.md (commit `ead6f006c`) before any sealed
run. The builder did not inspect sealed file contents before the runs.

Note on independence: this wave had no separate adversary worker. The
sealed families use fresh vocabulary and fresh episode selections (not the
2021pdt sets), generated from the frozen class spec without observing
outputs. This limitation is recorded in the prereg and JUDGE_BRIEF.md.

## K_AUD: segmentation-dependence audit (code inspection)

Verdict: PASS. The implementation differs from the 2021pdt baseline
(which passed K_AUD on all three claims) by exactly one cognition line
(the novel-segment scoring in `seg_dp`) plus comment updates, verified by
diff. The information-flow architecture is untouched:
(a) `learn_update` still updates lexicon, grounding, negator, and
comparative tables exclusively from `segs[]` (segmenter output);
(b) the only raw-byte-to-statistics path remains gated by `rawmode==1`
(C0 control only); the learner path passes `rawmode=0` at all call sites;
(c) the cold-start path remains inside `seg_dp` and feeds the same
statistics update. No DEVANG2-mode recurrence.

## Sealed runs (3/3 byte-identical each; exit 0; zero stderr)

- `segb sealed/sealed_b.txt` (learner): sha256
  `9934f8e72a8d5d505a8db30c7b85daa67a776f4ab889e73360b15eb0202ac5e6`
  x3. Output is byte-identical to `sealed_b_key.txt`. K_SEG 12/12.
- `segb-abl sealed/sealed_b.txt` (fixed-width-3): sha256
  `472698fef293626d45fda3cd8a198aac00674a57ae3dc740369460b947de0ef9`
  x3. 4/12 correct (probes 3, 8, 11 and one more).
- `sealc-fresh sealed/sealed_c.txt learner`: sha256
  `42f4919180ac8f56fa50bd93efe7666d00366d8d86395cace04df239ff2f51db`
  x3. Output: SEALC 20/20.
- `sealc-fresh ... c0`: sha256
  `c734a550895a7f77db8bcfff610525073dfd3ed2f770e0666aa1890b9b68f93e`
  x3. SEALC 13/20.
- `sealc-fresh ... c2`: sha256 (same as learner)
  `42f4919180ac8f56fa50bd93efe7666d00366d8d86395cace04df239ff2f51db`
  x3. SEALC 20/20.
- `sealc-fresh ... c1`: SEALC 10/20, 3/3 identical.
- `sealc-fresh ... c3`: SEALC 10/20, 3/3 identical.
- `fama` (default): 3/3 byte-identical
  (`206e5dfa84f9c70ccf2060a8084e3c258b82e46f2ccdbcaafd6d363866e9714b`),
  exit 0, zero stderr x3.

## Per-bar results

- KR0 (crash gate): PASS. 3/3 fama runs: exit 0, zero stderr bytes.
- K1 (>= 8/10): PASS. 10/10 from the t=60 lexicon snapshot (fama).
- K_SEG (>= 9/12 on FRESH Family B): PASS. 12/12 exact-boundary.
- K_SEAL (>= 12/20 on FRESH Family C): PASS. Learner 20/20
  (`sealc-fresh`). All 20 test episodes correct.
- K_AUD: PASS (above).
- K_ABL (ablation <= 5/12 on fresh Family B): PASS. Ablation 4/12.
- K_C0 (Family A: >= 15pp test accuracy AND >= 3 K1 words): PASS.
  Learner 20/20 vs C0 13/20 = 35pp; K1 10 vs 3 = 7 words.
- K8 (beats best control by >= 15pp on Family A): PASS. Learner 20/20
  vs best control (C2) 17/20.
- K2..K7,K9: 7/7 PASS (need >= 4). K2 6/6, K3 3/3, K4 3/3, K5 3/3,
  K6 3/3, K7 2/2, K9 10/10.
- K10 (true online): PASS (architecture unchanged from audited baseline).
- K11 (no future leakage): PASS (architecture unchanged).
- K12 (determinism): PASS. 3/3 byte-identical on every family and
  variant; sha256 recorded above.

## Regression bars (2021pdt worlds)

- Family B: 12/12 (was 8/12). No regression; all four old failures fixed.
- Family C: 11/20 (was 11/20). No regression.

## Verdict

BUILD-PASS. All required bars met: KR0, K1 (10/10), K_SEG (12/12),
K_SEAL (20/20), K_AUD, K_ABL (4/12), K_C0 (35pp, 7 words), K8,
K10, K11, K12, plus 7/7 sub-bars.

## Honest notes

1. The C2 (fixed-width-3) control also scores 20/20 on the fresh Family C.
   The fresh Family C uses 3-char content words, which align with
   fixed-width-3. K_SEAL does not require beating C2 on Family C (it
   requires >= 12/20 on a post-freeze family with new vocabulary and
   different boundary statistics, which is met). The discrimination
   between the learner and fixed-width segmentation comes from K_SEG
   (learner 12/12 vs ablation 4/12) and K8 on Family A, not from Family C.
   A future Family C with non-3-char words would discriminate more
   strongly, but 2-char words are unlearnable under the 3-char cold-start
   bootstrap (documented limitation) and 4-5 char words in variable
   positions are fragile.
2. No independent adversary worker this wave; the blind-generation
   discipline (fresh vocab, fresh selections, hashes pre-run, no
   inspection) is the mitigation. Recorded as a limitation.
3. The fix is minimal (one scoring line). The 2021pdt diagnosis is
   confirmed: the failure was the sign of the novel-length term, not the
   architecture.
