# LI-D4 run log — 2026-09-24

Coordinator: Track A subagent (D4 triple/predicate-level corroboration).

## Pins (observed, SHA-256)

- Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- IO `R33_NATIVE_IO_V1.zag`: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- BF1 source (== `src/control.zag`): `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
- `src/d4.zag`: `6c542e185b0f03fd6c39846395113f526d3e927921faf2be1ecb33da349dbb28`
- `src/d4_triple.zag`: `65563fd06559f4313469ed560e5580175026c521f2b096345348af149a181340`

## Prereg timeline

1. `eb65f76cdde58f5461f547cef10c41b596b577bc` — freeze (PREREG + gen_s1.py +
   sealed S1), before any D4 build or result run.
2. `4f963cb46b69e32916655860ec2b84dcce947ee7` — Amendment 1 (modal mapping,
   lost:lose/showing:show corrections, W1–W3 scope).
3. `9e62d27cd20938d99cdcf1a4e4926e42637cbef9` — Amendment 2 (pre-run audit:
   W1/W3 expectations corrected, W3 re-authored beat/will-beat, noun–verb
   shadowing documented). No verdict data seen before this commit.

## Implementation audit (pre-run)

- Verb table: 532/532 forms match prereg A.1 exactly (Amendment 1 modal
  mapping applied); stems identical; no duplicates.
- Glue: 99 words, all within prereg A.2; the 18 excluded words are the
  deliberate kept negations/quantifiers.
- Diff d4.zag vs control.zag: only `@import("d4_triple.zag")` + the
  `cluster_best` fork (triple keys, `d4_keys_mergeable`, winner returns
  first candidate sentence). All other code byte-identical to BF1.
- Calibration fidelity on frozen 28 pairs: 2/24 Type-B (nf-b-12, nf-b-17),
  1/4 P (P3) — exactly the prototype's prediction.

## Main runs (`run_d4.py`, 79 clusters × 2 arms × 2 passes)

- Batteries: frozen 60 (manifest order) + P4 + S1 (12) + W3.
- Teach: G1–G6 installed, G7 rejected, validated per pass.
- control: 24 install / 55 withhold, both passes byte-identical.
- d4: 26 install / 53 withhold, both passes byte-identical.
- K4 determinism: PASS (all three artifacts identical within arm).

## Analysis (`analyze_d4.py`)

- K1 PASS: d4 2/24 Type-B (nf-b-12, nf-b-17); control 0/24.
- K2 FAIL: d4 installs p3 (parabones). Predicted.
- K3 FAIL: d4 Type-A 17/20 (withholds nf-a-13, nf-a-19, nf-a-20);
  Type-C agree 15/16 (diverge nf-c-12); A9-C3 d4 3/4 vs control 4/4.
  Root cause: exact-duplicate sentences whose verbs are outside the frozen
  table fail closed ("") — verified in the design prototype too.
  NOT predicted by the prereg (calibration covered only the 28 B+P pairs).
- S1: honest 0/6 both arms; attacks 0/6 both.
- W: w1/w2/w3 all control WITHHOLD / d4 INSTALL, matching Amendment 2.
- M4 separation: 8.3% − 25.0% = −16.7pp.

## Verdict

**D4 KILLED** on K2 (predicted) and K3 (unpredicted regression).
See `VERDICT_D4.md`.

## Scale leg (K5) — appended on completion

(leg1x: 32/64 install; leg100x_a/b: two full 6400-cluster runs)
