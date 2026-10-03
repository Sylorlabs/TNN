# PREREG_AMENDMENT1: L2-INVERT-VALUE (pre-verdict arithmetic correction)

Status: PRE-VERDICT, transparent. The frozen PREREG.md
(committed alone at ee8dca0ca) is not edited; this file
records the correction. No counting-rule change, no
learner-code change, no kill-bar semantic change: a pure
hand-derivation arithmetic fix, verified against the
implementation's actual output before any verdict.

## Correction

QV-AS (FULL-arm Q_INV): 1186 -> 1237.

Root cause: the PREREG.md section 5 derivation used the
PRE-amendment parent base 1142 for Q_INV ("Parent 1142 =
2+7+548+208+181+196"). The parent lane's frozen,
amended bar is QV-AS=1193 (PREREG_AMENDMENT1.md in
l2_metareuse_extend: "QV-AS 1142->1193: foldwalk (s1,s2)
discovery-order correction in QINV op-1 b=2"), and the
parent driver bars 1193. The correct delta derivation:

  new op-4 = Form B (44: reverse value lookup finds
  fact 27 = (127,2,60), t*=127 != mA end 43 ->
  MR-INVVAL-FAIL, no walk) + Form A (196, unchanged)
  = 240; parent op-4 = 196.
  QV-AS = 1193 - 196 + 240 = 1237.

The implementation's actual FULL-arm output is
QV-AS=1237 (ARM-FULL-END as=333/335/324/1237/1286/
1146/393), confirming the corrected derivation. The
trace shows the expected sequence on Q_INV:
MR-INVVAL-LOOKUP t*=127 srcend=43, MR-INVVAL-FAIL,
MR-INV-REV rels=6,5,6,5,6,5,18, MR-INV-OK.

## Mechanical driver fix

- driver.zag F-COUNT falsifier: `qv_as!=1193` (stale
  parent value carried into the first implementation)
  -> `qv_as!=1237`.
- driver.zag: removed a stale duplicate
  `F-ABLATET-T16` falsifier line (`at_t16!=6`, parent
  value) that survived alongside the correct
  `at_t16!=7` line.

## Informational-count corrections (not kill-barred;
recorded for transparency)

Two ablation-arm informational counts in PREREG.md
section 5 were derived from buggy parent bases; the
implementation's outputs are the correct values:

- ABLATE-TRUNC QTRUNC as: 585 -> 497. The PREREG.md
  derivation used the parent REPORT's 541 as base.
  That 541 itself contains two errors: the op-2
  hallucinated candidate (+44, the same (100,2,50)
  phantom corrected by the parent's QT-AS amendment;
  correct op-2 is 44 ticks, collection only, no
  candidates) and a phantom op-6 second candidate
  (+44; only fact 7 has sub==100, so op-6 is
  4+44+10=58, not 102). Corrected parent base:
  541-88=453. This lane's op-4 delta (+44: Form B 44
  + Form A 44 vs parent op-4 44) gives 453+44=497,
  matching the implementation (ARM-ABLATEV-END is
  not affected; ARM-ABLATET-END as=497).
- ABLATE-INV QINV as: 1132 -> 1183. The PREREG.md
  derivation used the pre-correction parent base and
  did not apply the +51 foldwalk (s1,s2)
  discovery-order correction (the same correction as
  the parent's QV-AS 1142->1193 amendment, which
  applies identically here since ops 1,2,3,5,6 run
  unchanged with op 4 skipped). 1132+51=1183,
  matching the implementation.

All other frozen bars, counts, and falsifiers stand as
in PREREG.md.
