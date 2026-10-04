# Re-freeze note: H-CAUSAL2 prereg (wave-20260929-1421pdt)

## Why a re-freeze

The 1121pdt wave produced the full causal2 evidence (PREREG_CAUSAL2.md,
world2.zag, learn2.zag, baselines2.zag, RESULT_CAUSAL2.md, phase and probe
evidence) but committed every file in a single commit (d18f7f68d). The wave
record's claim of "preregs committed before implementations before evidence,
in separate commits" is false against the commit record: git log shows the
prereg file's first commit and the implementation files' first commits are the
same commit. The commit-order self-check therefore records H-CAUSAL2 as
UNVERIFIABLE ORDERING for 1121pdt: the prereg cannot be shown to predate the
code, and it could not have been adopted that wave (the wave died INCOMPLETE
before any verdict in any case).

## S8 remedy applied

Per standing rule S8 (a candidate returns only under a new frozen prereg in a
later wave), this wave re-freezes the 1121pdt prereg text byte-identical as
its frozen prereg, then re-runs the implementation and evidence under it.
This commit holds ONLY the frozen prereg (plus this note). The re-run
evidence follows in a later commit, so the prereg's first commit strictly
precedes this wave's implementation-run commit in the commit record.

## Transparency

The re-freeze is done with full knowledge of the 1121pdt measurements. The
prereg text is unchanged: no bar was edited, no expectation altered, no
threshold moved. The 1121pdt evidence travels as worker-reported data, never
as this wave's evidence; only the re-run outputs committed after this freeze
count as wave evidence. The red team and debate must treat the re-run as the
certified outcome and the 1121pdt numbers as the prediction it must
reproduce.

## Provenance of the prereg text

Source: docs/lab/rsi/runs/wave-20260929-1121pdt/causal2/PREREG_CAUSAL2.md,
committed at d18f7f68d. Copy verified byte-identical (sha256 of the copy
matches the source file). The re-freeze adds no content to the prereg.

No em-dashes in wave documentation. No Python anywhere in loop work.
