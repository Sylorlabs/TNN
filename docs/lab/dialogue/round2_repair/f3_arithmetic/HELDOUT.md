# HELDOUT.md — frozen held-out probes for F3-ARITHMETIC

Frozen in `PREREG_F3.md` §5 **before** implementation (commit 7a02805328f8c51429a80cd8ad4dc459c4f6714d).
Written before any repair code existed; never used during development.
Battery file: `heldout/battery.txt`. Binary: `dialogue_bin`
(sha256 `4c6ee1ddb284c5aac355a807e0800d7d370dd199ba3fd40683d2f2ded5eb9df2`).

## Results (released fork, scaffold removed)

| id | probe | expected | actual | verdict |
|----|-------|----------|--------|---------|
| H1 | `which is taller, the eiffel tower or the montparnasse tower?` → `how much taller is it?` | `120` | `120` | PASS |
| H2 | `which is taller, big ben or the statue of liberty?` → `how much taller is it?` | `3` | `3` | PASS |
| H3 | `how much taller is the statue of liberty than big ben?` | `3` | `3` | PASS |
| H4 | `how many years between charles darwin and herman melville being born?` | `10` | `10` | PASS |
| H5 | `how many years between the louvre opening and the eiffel tower being built?` | `96` | `96` | PASS |
| H6 | `how much taller is mount everest than the eiffel tower?` | `8519` | `8519` | PASS |
| H7 | `what is the difference in height between the eiffel tower and the montparnasse tower?` | `120` | `120` | PASS |
| H8 | `how much older is herman melville than charles darwin?` | `10` | `10` | PASS |

**8/8 PASS.** Ground truth all from the frozen `kb.txt`:
330−210=120 (H1,H7); 96−93=3 (H2,H3); 1819−1809=10 (H4,H8);
1889−1793=96 (H5); 8849−330=8519 (H6).

## Why this is not memorization

- None of the answers (120, 3, 10, 96, 8519) appear as constants anywhere in
  the fork (verified by grep — the only numeric literals are ASCII codes,
  trigger-string lengths, pv slot offsets, and event indices).
- H2/H3/H6 use entity pairs that appear in **no** scaffold probe; the values
  are looked up from the KB at query time and subtracted.
- The only cross-turn state is entity ids (discourse referents, the same job
  the existing pronoun binder does) — never answers.

## Run logs

- `heldout/run1.log`, `heldout/run2.log` — two full runs, **byte-identical**
  (`cmp` clean), zero RNG. Digest `779b0d6da5fe46df25eefd1e9208c97ea34498e69b98fc642761a00612ba34b2`.
- `scaffold/run1.log` — scaffold-phase results (5/5 PASS during development;
  scaffold artifacts are dev logs only, never consulted by the binary).
- `baseline_battery.log` — frozen canonical binary on the round-1 battery
  (baseline sections: 45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72, 28/28).
- `new_battery_run1.log`, `new_battery_run2.log` — repaired binary on the
  round-1 battery: identical sections, byte-identical reruns, and the full
  output is identical to baseline except the DIGEST line.
- `round2conv/new_conv.log` — repaired binary on the full round-2
  conversation: all 18 A-lines identical to the frozen round-2 record
  **except turn 6**, which changed from `The Eiffel Tower is in Paris.` to
  `120` (the repair).
