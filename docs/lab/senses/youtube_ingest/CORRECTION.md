# CORRECTION — code/src/sense.zag threshold (2026-09-22)

Commit b6e1c31d shipped `code/src/sense.zag` with the UNfitted motion
rule (`mag2 >= 9`, i.e. STILL iff |disp| < 3px), but the KB4-video
readiness numbers in READINESS.md were produced with the rematch-T4
fitted rule (`mag2 >= 1`, STILL iff mag < 1). The fitted binary that ran
the trial is no longer on disk; the committed source did not reproduce
the recorded runs.

Fix: `code/src/sense.zag` now carries the fitted rule (the single-line
diff vs the previous commit is the threshold plus a comment — verified
by diff). Rebuilt with the pinned znc toolchain; the binary is
byte-identical (sha256 1f208c2362000564179fed80a669b1c063ce4a97cb57299b4987f901e1a16385)
to the independently built and behaviorally probed `yt_sense/sense_t1`
used by the YT-INGEST-1 pipeline (see validation/BUILD_EVIDENCE.md).

The readiness verdict (GATED) is unchanged — it was computed with the
fitted rule, which is what the source now matches. Lesson: never commit
a sense source without rebuilding and byte-comparing against the binary
that produced the recorded results.
