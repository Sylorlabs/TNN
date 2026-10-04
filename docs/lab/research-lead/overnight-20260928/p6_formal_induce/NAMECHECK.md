# P6 / NAMECHECK — static audit of the translation-unit separation

Verified by grep on 2026-10-03. Reproduce with the two commands in section 5.

## 1. Which files are on which side of the wall

| side | files |
|---|---|
| WORLD (holds the seed and derives the instance) | `p6_lang.zag` |
| CHECKER (true validity) | `p6_ckcore.zag` |
| world builder only | `p6_gencorpus.zag`, `p6_gcmain.zag`, `p6_io.zag` |
| **LEARNER side** (must be instance-free) | `p6_corpus.zag`, `p6_learner.zag`, `p6_induce.zag` |
| held-out verification driver | *not built* (see REPORT.md section 5) |

The binary that would generate artifacts is
`p6_corpus.zag + p6_learner.zag + p6_induce.zag + p6_train.zag`.
It contains **no** `lg_*` (instance derivation), **no** `ck_*` (true checker),
**no** `gc_*`/`gp_*`/`bd_*` (world generator), and **no** seed literal.

## 2. Audit results (all as required, all PASS)

| check | p6_corpus.zag | p6_learner.zag | p6_induce.zag |
|---|---|---|---|
| seed literals `1009 2027 3313 4091` | 0 | 0 | 0 |
| instance symbols `lg_ L_role L_val L_M L_C` | 0 | 0 | 0 |
| checker symbols `ck_ ck_check` | 0 | 0 | 0 |
| world-generator symbols `gp_ gc_ bd_` | 0 | 0 | 0 |
| role codes `rY rS rV rB rV2 rN rK` | 0 | 0 | 0 |
| type codes `tY tS tB` | 0 | 0 | 0 |
| keyword subroles `kPROC kLET kSEMI kTHEN kELSE kEND kIF kASG kLP kRP kCOM kCOL kTYN kTYS` | 0 | 0 | 0 |

This is guard **G1** of PREREG section 1.3 (as amended by AMENDMENT 2).

## 3. Guard G2 (held-out checker never in the generating binary)

Structural, not just textual: the true checker `p6_ckcore.zag` is a separate
file that is concatenated only into the world-builder translation unit. The
learner-side files do not reference it (section 2). The corpus files are
written to disk by the world builder and read back by the learner as opaque
bytes, so the learner's entire input is `(token sequence, one label bit)`.

## 4. Honest limitation (same posture as `.env/pure-zag.sh`)

This is enforcement by audit, not by sandbox. The corpus files sit on disk in
plain text and are human-readable; a determined adversary could read them. The
claim guarded here is narrower and is the one the prereg makes: **the learner
source contains no instance knowledge, and the generating binary contains no
ground-truth checker.**

## 5. Reproduce

```sh
cd docs/lab/research-lead/overnight-20260928/p6_formal_induce
grep -cE "1009|2027|3313|4091"                     p6_corpus.zag p6_learner.zag p6_induce.zag
grep -cE "lg_|L_role|L_val|L_M\(|L_C\(|ck_|kPROC|kLET|kSEMI|rY\(\)|rS\(\)|rB\(\)|rV\(\)|rV2\(\)|rN\(\)|rK\(\)|tY\(\)|tS\(\)|tB\(\)|bd_|gp_|gc_" \
                                                  p6_corpus.zag p6_learner.zag p6_induce.zag
```
Every count must be `0`.

## 6. What this audit does NOT cover

It cannot cover the learner, because the learner's induction body
(`p6_induce.zag`) is **incomplete and never executed**. PREREG criterion ZD-2
(removable-wiring census) requires reading every line of the learner's
generation path and classifying it; that classification was not performed and
no ZD verdict is claimed. See REPORT.md.
