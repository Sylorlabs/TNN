# MATH R3 SCORECARD — native engines vs primary bars

Scoring crew report. No verdict beyond the prereg bars (round coordinator
writes the verdict after KB4 grading). Frozen prereg: PREREG_MATH_R3.md
(@01ffd095). 3 external runs/problem/engine, byte-identity asserted.

## 0. Build verification

- n1: rebuilt from committed sources, binary SHA-256 `a4b0a33ed4d2fd98...` MATCHES crew-reported SHA.
- n2: rebuilt from committed sources, binary SHA-256 `97ef61681baf750b...` MATCHES crew-reported SHA.
- n3: rebuilt from committed sources, binary SHA-256 `c02f37eaba8bcc1e...` MATCHES crew-reported SHA.
- n4: rebuilt from committed sources, binary SHA-256 `002d3222a683d3d1...` MATCHES crew-reported SHA.
- NL knowledge store SHA-256 `910ea9da0989e113...` matches pinned store.
- Divergent reruns: NONE (all 3x runs byte-identical)

## 1. Primary bars

| engine | PB1 R3N (bar ≥12/24) | PB2 twins (bar ≥30/37) | PB3 B5X-NL (bar ≥45/60, <10 fd, <10 fw) | bars passed |
|---|---|---|---|---|
| n1 | 7/24 FAIL | 3/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |
| n2 | 0/24 FAIL | 1/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |
| n3 | 8/24 FAIL | 0/37 FAIL | 0/60 correct, fd=0, fw=0, nv=60 FAIL | 0/3 |
| n4 | 8/24 FAIL | 1/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |

Decision rule (frozen): R2 DUAL verdict STANDS unless a native wins ≥2/3 bars vs BOTH controls.
Controls (rebuilt, R2 numbers re-verified): DUAL-R1 formal B2R/B3R/B4R = 37/37; REF-FIRST = 34/37. DUAL/REF-FIRST did not attempt R3N in R3 (prereg: expected honest abstention).

## 2. Battery detail (correct / total)

| engine | R3N | twins | B5X-NL | B6X-NL (verdict, derivations) | B1N |
|---|---|---|---|---|---|
| n1 | 15/24 | 3/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/None; B6X_NL_DAG: DERIVED/None; B6X_NL_LINEAR: WITHHELD/None | 6/22 |
| n2 | 0/24 | 1/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/0; B6X_NL_DAG: WITHHELD/0; B6X_NL_LINEAR: WITHHELD/0 | 9/22 |
| n3 | 8/24 | 0/37 | 0/60 | B6X_NL_CONTRADICTION: NO_VERDICT/None; B6X_NL_DAG: NO_VERDICT/None; B6X_NL_LINEAR: NO_VERDICT/None | 10/22 |
| n4 | 8/24 | 1/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/None; B6X_NL_DAG: WITHHELD/None; B6X_NL_LINEAR: WITHHELD/None | 9/22 |

B6X sealed step counts: LINEAR 104, DAG 104, CONTRADICTION 103 (no sealed verdict key).

## 3. Anti-bridge audit

### 3a. Trace inspection (honesty: every step cites byte-spans of input/store text or prior steps)

- **n1** R3N traces: 8/24 honest.
  - cross-battery sample: 0/12 honest.
  - R3N/R3N_01 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - R3N/R3N_02 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes ' p be a prime number that di' absent from premise S18 text (span [66,94) does not cite the premise)"]
  - R3N/R3N_03 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - R3N/R3N_04 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'ov' absent from premise S7 text (span [70,72) does not cite the premise)", "S29 hole span bytes 'that p + 2 is also' absent from premise S24 text (span [126,144) does not cite the premise)"]
  - R3N/R3N_07 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' A' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - R3N/R3N_08 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes '80' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_11 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' l' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes ' O' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_12 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'gl' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes 'th' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_13 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'al' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes ' w' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_15 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' t' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes ' T' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_16 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes ' E' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_17 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' y' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes ' Y' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_19 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes 'he' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_21 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'Th' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes 'rn' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - R3N/R3N_22 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - R3N/R3N_24 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'Ev' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - twins/T2_01 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes 'e ' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - twins/T2_02 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - twins/T2_03 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - twins/T2_04 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'he' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - twins/T2_05 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' t' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - twins/T2_06 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'le' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes 'no' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - twins/T2_07 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes ' l' absent from premise S7 text (span [70,72) does not cite the premise)", "S28 hole span bytes 'ht' absent from premise S22 text (span [117,119) does not cite the premise)"]
  - twins/T2_08 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - twins/T2_09 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'll' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - twins/T2_10 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)"]
  - twins/T2_11 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S27 hole span bytes 'le' absent from premise S7 text (span [70,72) does not cite the premise)"]
  - twins/T2_12 findings: ["S26 hole span bytes 'ID: ' absent from premise S12 text (span [0,4) does not cite the premise)", "S28 hole span bytes 'no' absent from premise S22 text (span [117,119) does not cite the premise)", "S29 hole span bytes ' is not red, the' absent from premise S25 text (span [113,129) does not cite the premise)"]
- **n2** R3N traces: 0/0 honest.
  - cross-battery sample: 12/12 honest.
- **n3** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.
- **n4** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.

### 3b. Paraphrase perturbation (6 variants — verdict must match the engine's base-item verdict)

- **n1**: 3/6 match. AUD_P1(base R3N_04 WITHHELD→DERIVED); AUD_P2(base R3N_05 DERIVED→WITHHELD); AUD_P3(base R3N_07 WITHHELD→DERIVED); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)
- **n2**: 6/6 match. AUD_P1(base R3N_04 NO_VERDICT→NO_VERDICT); AUD_P2(base R3N_05 NO_VERDICT→NO_VERDICT); AUD_P3(base R3N_07 NO_VERDICT→NO_VERDICT); AUD_P4(base R3N_24 NO_VERDICT→NO_VERDICT); AUD_P5(base R3N_17 NO_VERDICT→NO_VERDICT); AUD_P6(base R3N_11 NO_VERDICT→NO_VERDICT)
- **n3**: 6/6 match. AUD_P1(base R3N_04 WITHHELD→WITHHELD); AUD_P2(base R3N_05 WITHHELD→WITHHELD); AUD_P3(base R3N_07 WITHHELD→WITHHELD); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)
- **n4**: 6/6 match. AUD_P1(base R3N_04 WITHHELD→WITHHELD); AUD_P2(base R3N_05 WITHHELD→WITHHELD); AUD_P3(base R3N_07 WITHHELD→WITHHELD); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)

### 3c. Nonce-word variants (6 variants — verdict must match the engine's base-item verdict)

- **n1**: 4/6 match. AUD_N1(base R3N_02 WITHHELD→DERIVED); AUD_N2(base R3N_08 WITHHELD→DERIVED); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)
- **n2**: 6/6 match. AUD_N1(base R3N_02 NO_VERDICT→NO_VERDICT); AUD_N2(base R3N_08 NO_VERDICT→NO_VERDICT); AUD_N3(base R3N_19 NO_VERDICT→NO_VERDICT); AUD_N4(base R3N_15 NO_VERDICT→NO_VERDICT); AUD_N5(base R3N_02 NO_VERDICT→NO_VERDICT); AUD_N6(base R3N_24 NO_VERDICT→NO_VERDICT)
- **n3**: 6/6 match. AUD_N1(base R3N_02 WITHHELD→WITHHELD); AUD_N2(base R3N_08 WITHHELD→WITHHELD); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)
- **n4**: 6/6 match. AUD_N1(base R3N_02 WITHHELD→WITHHELD); AUD_N2(base R3N_08 WITHHELD→WITHHELD); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)

## 4. Findings

(mechanical observations from scoring; interpretation belongs to the verdict stage)

- **n2**: 24 NO_VERDICT (engine exit!=0 or no parseable verdict): r3n: 24
- **n3**: 100 NO_VERDICT (engine exit!=0 or no parseable verdict): b5x_nl: 60; b6x_nl: 3; twins: 37
- **n1 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n2 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n3 B5X-NL**: 0 correct_withheld, 0 false_withheld, 0 correct_derived, 0 false_derived, 60 no_verdict
- **n4 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n1 trace honesty**: R3N 8/24 honest; cross-battery sample 0/12 honest
- **n2 trace honesty**: R3N 0/0 honest; cross-battery sample 12/12 honest
- **n3 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n4 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n1 anti-bridge**: paraphrase 3/6 match, nonce 4/6 match
- **n2 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **n3 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **n4 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **static no-RNG backstop**: PASS

