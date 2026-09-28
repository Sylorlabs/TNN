# F2-WITHHOLD — frozen held-out report

The 7 held-out probes are frozen in the prereg (`PREREG_F2.md` §4), recorded
2026-09-23 before implementation. This is the first and only test of the
final repair on them. Each must emit exactly `I don't know.`

## Frozen set

| # | probe | result |
|---|-------|--------|
| H1 | what is the capital of spain? | I don't know. PASS |
| H2 | who wrote the odyssey? | I don't know. PASS |
| H3 | who painted the mona lisa? | I don't know. PASS |
| H4 | how tall is the colosseum? | I don't know. PASS |
| H5 | who discovered penicillin? | I don't know. PASS |
| H6 | which river is the longest? | I don't know. PASS |
| H7 | what is the capital of japan? | I don't know. PASS |

7/7 decline, all exact. Log: `run_heldout.log`.

## Release-bar evidence

- No held-out phrasing appears in the implementation: grepped the fork
  `dialogue.zag` for every held-out/scaffold probe keyword
  (hamlet, italy, dune, odyssey, spain, japan, penicillin, mona, lisa,
  longest, president, shakespeare) — zero hits.
- The decline mechanism is the general five-part aboutness gate, not a
  per-case branch. Each held-out is killed by a different path of the gate:
  H1/H2/H5/H7 by demand-focus (G3), H3 by orphan-aboutness (G4), H4 by
  relation-demand (G2), H6 by orphan-aboutness (G4).
- The held-out battery file `heldout_probes.txt` is byte-identical to the
  set written in the prereg.

B2 verdict: **PASS**.
