# BAR-TEXT AUDIT: PREREG_H_EXP2_V2.md (wave-20261001-0221pdt)

Auditor: wave coordinator (inline). Date: 2026-10-01.
Prereg: docs/lab/rsi/runs/wave-20260930-1121pdt/exp2/PREREG_H_EXP2_V2.md
(frozen wave-20260930-1121pdt; 2021pdt debate M3 ruled it FROZEN with
audit precondition before implementation).

Method: each kill bar checked for (a) specificity (exact strings,
numbers, and comparison targets named), (b) machine-checkability
(the check can be done with grep/cmp/diff on committed trace files,
no human judgment), (c) non-vacuity (the bar can fail).

- K-X1: "the loop emits IDENTIFIED 2 3 within 6 executed probes; the
  emitted pair equals the sealed law file; no BUDGET-EXHAUSTED, no
  STALLED, no INCONSISTENT." Auditable: grep "IDENTIFIED 2 3" in the
  concatenated round log; count executed probes from history lines
  (must be <= 6); diff the pair against prereg/law_WA.txt ("LAW 2 3");
  grep-absence of the three failure markers. Specific, checkable,
  non-vacuous. PASS.
- K-X2: same structure for W-B ("IDENTIFIED 2 1", <= 10 probes,
  law_WB.txt "LAW 2 1"). PASS.
- K-X3: "IDENTIFIED occurs at round >= 3, and the per-round trace
  shows the surviving hypothesis count strictly decreasing in at
  least 2 distinct rounds." Auditable: parse "ROUND k" and
  "SURVIVORS s" lines; check round index and count strict decreases.
  PASS.
- K-X4: "two full loop runs per world are byte-identical (cmp on the
  concatenated round logs)." Auditable: cmp of the two logs. PASS.
- K-X5: "expseq.zag contains no reference to any law file name or
  path and never opens one; only expworld opens the law file.
  Verified by grep over both sources." Auditable: grep for law path
  strings in expseq.zag; grep _zag_read_file/_zag_arg call sites.
  PASS.
- K-X6: "every executed probe in both sealed runs has trace score
  >= 2 against the then-surviving hypothesis set." Auditable
  provided the per-round trace prints the executed probe's score
  next to the PROBE line (implementation contract recorded here).
  PASS.

Erratum (documentation only, not a bar change): the prereg's
"(1654 probes)" parenthetical is arithmetically wrong. Action
sequences of length 1..4 over 6 actions number
6 + 36 + 216 + 1296 = 1554. No kill bar references 1654; the rule
"length 1..4" is what the bars govern. The implementation enumerates
1554 probes per the rule.

No bar is vague, uncheckable, or tautological. No bar was altered.
AUDIT PRECONDITION SATISFIED. Implementation may proceed against
the frozen bars K-X1..K-X6.

No em-dashes in this documentation.
