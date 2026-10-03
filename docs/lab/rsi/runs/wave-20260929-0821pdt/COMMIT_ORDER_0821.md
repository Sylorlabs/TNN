# Commit-order self-check: wave-20260929-0821pdt

Standing rule: a prereg is frozen only if the prereg file's first
commit strictly precedes the implementation files' first commits.
Timestamp gaps under batch commits do not count; content ordering
does. Candidates failing this check are UNVERIFIABLE ORDERING and
cannot be adopted.

Wave commit order (oldest first, from git log --reverse):

1. aed88c8f2 -- Prereg H-EXP FROZEN (K-E1..K-E5) plus the six frozen
   hypothesis fixture files. FIRST.
2. e2b6d5b04 -- H-EXP implementation (exp_learn.zag). After prereg.
3. 3ae98a9c9 -- Implementation build fix (i64s defined locally).
   After prereg.
4. c06a23cfb -- Transparent pre-execution prereg amendment (HYP name
   lines added to fixtures; pair semantics unchanged; no run had
   occurred). After implementation source, BEFORE any implementation
   execution. The amendment commit message states the pre-execution
   condition; the first successful execution artifacts are committed
   in (5).
5. 816fee7a7 -- H-EXP evidence (7 executions) and red-team report.
   After all of the above.
6. 7860c2694 -- Fork battery, FIT, debate positions, design lane,
   interactive survey. After all of the above.

Result: VALID. The prereg (aed88c8f2) strictly precedes every
implementation commit (e2b6d5b04, 3ae98a9c9). The amendment
(c06a23cfb) precedes all executions. No candidate is UNVERIFIABLE
ORDERING.

Permanent caveat: commit order evidences commit order only, never
run order and never content identity. The pre-execution status of
the amendment rests on the implementer's record (the failed parse
run that motivated it produced no committed artifacts), not on
commit metadata.

No em-dashes used in this document.
