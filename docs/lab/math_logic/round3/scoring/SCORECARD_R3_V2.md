# MATH R3 SCORECARD v2 — native engines vs primary bars (post-repair rescore)

Repair+rescore crew report. No verdict beyond the prereg bars (round coordinator
writes the verdict after KB4 grading). Frozen prereg: PREREG_MATH_R3.md
(@01ffd095). 3 external runs/problem/engine, byte-identity asserted.

## What changed vs v1 (SCORECARD_R3.md) and why

Three mechanical integration defects found in v1 scoring were repaired with
parser/emission-only changes (no engine reasoning, license, search, referee,
or verdict logic touched; see engines/n{1,2,3}/BUILD_N{1,2,3}.md repair notes):
- **n2**: R3N files use multiline `STATEMENT:` blocks; n2 required statement
  content on the same line and exited 4 on all 24 R3N. The parser now consumes
  the multiline block (bare `STATEMENT:` header line, block lines to blank /
  next field / EOF, bullets kept verbatim, true file span, no copy).
- **n3**: twins/, b5x_nl/, b6x_nl/ use `PREMISES:`/`TARGET:`; n3 required a
  `STATEMENT:` line and exited 4 on all 100. It now presents
  premises-text + newline + TARGET: + target-text as the problem bytes (bullets
  verbatim; the 9-byte joiner is the only synthetic byte run; ledger spans stay
  file-grounded — the presentation is a contiguous substring of the file).
- **n1**: inference states recorded premise-relative hole offsets but the trace
  printer indexed tx absolutely, so traces cited wrong spans (16/24 R3N + all
  sampled twin traces). Hole provenance now stores tx-absolute spans; the hm
  table is read only by the trace emitter, so verdict logic is untouched.
n4 was not repaired; its v1 scores are carried forward verbatim (binary
SHA-256 re-verified unchanged). Controls unchanged. PB1/PB2/PB3 unchanged.

## 0. Build verification

- n1: rebuilt from committed sources, binary SHA-256 `d9a9a4cd57b0868c...` MATCHES crew-reported SHA.
- n2: rebuilt from committed sources, binary SHA-256 `9f82b3bc2c974476...` MATCHES crew-reported SHA.
- n3: rebuilt from committed sources, binary SHA-256 `519afe7c3dce9c97...` MATCHES crew-reported SHA.
- n4: rebuilt from committed sources, binary SHA-256 `002d3222a683d3d1...` MATCHES crew-reported SHA.
- NL knowledge store SHA-256 `910ea9da0989e113...` matches pinned store.
- Divergent reruns: NONE (all 3x runs byte-identical)

## 1. Primary bars

| engine | PB1 R3N (bar ≥12/24) | PB2 twins (bar ≥30/37) | PB3 B5X-NL (bar ≥45/60, <10 fd, <10 fw) | bars passed |
|---|---|---|---|---|
| n1 | 15/24 PASS | 3/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 1/3 |
| n2 | 8/24 FAIL | 1/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |
| n3 | 8/24 FAIL | 1/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |
| n4 | 8/24 FAIL | 1/37 FAIL | 24/60 correct, fd=0, fw=36, nv=0 FAIL | 0/3 |

Decision rule (frozen): R2 DUAL verdict STANDS unless a native wins ≥2/3 bars vs BOTH controls.
Controls (rebuilt, R2 numbers re-verified): DUAL-R1 formal B2R/B3R/B4R = 37/37; REF-FIRST = 34/37. DUAL/REF-FIRST did not attempt R3N in R3 (prereg: expected honest abstention).

## 2. Battery detail (correct / total)

| engine | R3N | twins | B5X-NL | B6X-NL (verdict, derivations) | B1N |
|---|---|---|---|---|---|
| n1 | 15/24 | 3/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/None; B6X_NL_DAG: DERIVED/None; B6X_NL_LINEAR: WITHHELD/None | 6/22 |
| n2 | 8/24 | 1/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/0; B6X_NL_DAG: WITHHELD/0; B6X_NL_LINEAR: WITHHELD/0 | 9/22 |
| n3 | 8/24 | 1/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/8; B6X_NL_DAG: WITHHELD/8; B6X_NL_LINEAR: WITHHELD/8 | 10/22 |
| n4 | 8/24 | 1/37 | 24/60 | B6X_NL_CONTRADICTION: WITHHELD/None; B6X_NL_DAG: WITHHELD/None; B6X_NL_LINEAR: WITHHELD/None | 9/22 |

B6X sealed step counts: LINEAR 104, DAG 104, CONTRADICTION 103 (no sealed verdict key).

## 3. Anti-bridge audit

### 3a. Trace inspection (honesty: every step cites byte-spans of input/store text or prior steps)

- **n1** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.
- **n2** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.
- **n3** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.
- **n4** R3N traces: 24/24 honest.
  - cross-battery sample: 12/12 honest.

### 3b. Paraphrase perturbation (6 variants — verdict must match the engine's base-item verdict)

- **n1**: 3/6 match. AUD_P1(base R3N_04 WITHHELD→DERIVED); AUD_P2(base R3N_05 DERIVED→WITHHELD); AUD_P3(base R3N_07 WITHHELD→DERIVED); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)
- **n2**: 6/6 match. AUD_P1(base R3N_04 WITHHELD→WITHHELD); AUD_P2(base R3N_05 WITHHELD→WITHHELD); AUD_P3(base R3N_07 WITHHELD→WITHHELD); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)
- **n3**: 6/6 match. AUD_P1(base R3N_04 WITHHELD→WITHHELD); AUD_P2(base R3N_05 WITHHELD→WITHHELD); AUD_P3(base R3N_07 WITHHELD→WITHHELD); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)
- **n4**: 6/6 match. AUD_P1(base R3N_04 WITHHELD→WITHHELD); AUD_P2(base R3N_05 WITHHELD→WITHHELD); AUD_P3(base R3N_07 WITHHELD→WITHHELD); AUD_P4(base R3N_24 WITHHELD→WITHHELD); AUD_P5(base R3N_17 WITHHELD→WITHHELD); AUD_P6(base R3N_11 WITHHELD→WITHHELD)

### 3c. Nonce-word variants (6 variants — verdict must match the engine's base-item verdict)

- **n1**: 4/6 match. AUD_N1(base R3N_02 WITHHELD→DERIVED); AUD_N2(base R3N_08 WITHHELD→DERIVED); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)
- **n2**: 6/6 match. AUD_N1(base R3N_02 WITHHELD→WITHHELD); AUD_N2(base R3N_08 WITHHELD→WITHHELD); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)
- **n3**: 6/6 match. AUD_N1(base R3N_02 WITHHELD→WITHHELD); AUD_N2(base R3N_08 WITHHELD→WITHHELD); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)
- **n4**: 6/6 match. AUD_N1(base R3N_02 WITHHELD→WITHHELD); AUD_N2(base R3N_08 WITHHELD→WITHHELD); AUD_N3(base R3N_19 WITHHELD→WITHHELD); AUD_N4(base R3N_15 WITHHELD→WITHHELD); AUD_N5(base R3N_02 WITHHELD→WITHHELD); AUD_N6(base R3N_24 WITHHELD→WITHHELD)

## 4. Findings

(mechanical observations from scoring; interpretation belongs to the verdict stage)

- **n1 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n2 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n3 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n4 B5X-NL**: 24 correct_withheld, 36 false_withheld, 0 correct_derived, 0 false_derived, 0 no_verdict
- **n1 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n2 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n3 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n4 trace honesty**: R3N 24/24 honest; cross-battery sample 12/12 honest
- **n1 anti-bridge**: paraphrase 3/6 match, nonce 4/6 match
- **n2 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **n3 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **n4 anti-bridge**: paraphrase 6/6 match, nonce 6/6 match
- **static no-RNG backstop**: PASS

