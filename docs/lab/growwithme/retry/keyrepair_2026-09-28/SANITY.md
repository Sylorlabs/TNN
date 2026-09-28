# Sanity check — repaired battery rebuild + re-run (2026-09-28)

## What was done

The restored package (`docs/lab/growwithme/retry/` with the 79 repaired keys)
was rebuilt from source with the pinned toolchain and re-run fresh (D and N
arms), then scored against the RESTORED keys with the frozen 70%-overlap
scorer. This validates the repaired battery end-to-end: the package builds,
runs deterministically, and the restored keys score as the red team's
frozen-key rescore predicted.

## Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  SHA-256 verified `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Command (from package root): `znc_linux_x86_64_abed8aa1 runner.zag -o build/runner --no-zagd`
- Result: success, 0 errors. Binary SHA-256:
  `4b8d7f473d7b05c5505ed02989a35116c11c449b4956dfb2d3505b753a582cac`
  — **byte-identical to the red team's independently rebuilt binary**
  (REDTEAM.md §1). The restored keys do not enter the binary (the runner
  reads only the agent-visible `.q` questions), so bit-identity is expected
  and confirms the sources restored cleanly.

## Determinism

Fresh `runs/D_run1` and `runs/N_run1` are **byte-identical** (recursive
`diff -r`, zero differences) to the red team's original runs kept at
`~/workspace/growwithme_retry/runs/`. The repaired package reproduces the
original behavior exactly.

## Rescore against restored keys (frozen 70%-overlap scorer)

| Arm | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| D | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 13/18 .722 | 11/18 .611 |
| N | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 13/18 .722 | 11/18 .611 |

This **exactly reproduces the red team's frozen-key rescore** (REDTEAM.md §3:
"S5 13/18, S6 11/18, S1–S4 unchanged at 17/13/11/16"). C1 (D≥.95) and C2
(N≥.90) still fail every session — the M3 kill is unaffected by the repair,
as the red team predicted: the kill stands on S1–S4 alone, and S5/S6 remain
below the bars even with correct keys (genuine retrieval failures, not
scorer artifacts).

## Conclusion

The repaired battery is clean and staged: re-sealed questions, frozen keys,
frozen scorer, deterministic rebuild. M2 may now be evaluated against it.

## Miss characterization (from the independent rebuild crew's run)

27 misses per arm (of 108 immediate probes); miss lists identical between D
and N. Almost all misses are "Withheld" deliberation refusals; the only
genuine wrong answers are S1 F1-01-Q, S2 F2-02-Q, S3 F3-14-Q, S6 F6-14-Q
and F6-15-Q (one each). This is the M3 baseline M2 must beat: genuine
wrong answers on paraphrased demand-word probes, plus a large withhold
mass the prereg's kill criterion (b) pins as the floor.

## Rebuild ergonomics notes (for future rebuilders of this package)

1. The committed package tree contains no `build/` dir (git does not track
   empty dirs) — `znc runner.zag -o build/runner --no-zagd` fails with
   "failed to write executable" until `mkdir -p build/`.
2. `runner.zag`'s `mkpath` is a single non-recursive `mkdir("runs/D_run1")`
   that fails silently when `runs/` does not exist — first runs exit 0 but
   write nothing; `mkdir -p runs` first. Neither is a source defect.
