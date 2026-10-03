# AMENDMENT 1 to PREREG_DDES_FOLLOWUP_V2.md: K-G1 repair

Status: RE-FROZEN this wave (wave-20261001-1121pdt), before any
implementation commit and before any sealed evaluation run. The frozen
prereg is docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/
PREREG_DDES_FOLLOWUP_V2.md (first committed 20261001-0821pdt in commit
dc6b0cfd2). Kill bars K-G2 through K-G9 are unchanged. Only K-G1 is
repaired, as authorized by the prereg's own amendment clause ("Any
amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results").

## The defect

K-G1 as frozen requires "the pinned znc compiles ddesp2.zag with exit
0, zero stderr bytes, and produces an executable", with "any stderr
byte" as the kill. This bar is unsatisfiable for every possible
implementation under the pinned toolchain: the pinned znc
unconditionally prints the line

  znc: warning: zagd unavailable; foreground compilation continues
  without background planning

to stderr on every compilation. This is documented loop knowledge
(docs/lab/research-lead/overnight-20260928/MEM6_RESULT.md: "znc prints
'warning: zagd unavailable...' on every build. Compilation succeeds;
the binary is native and deterministic"), and the identical warning is
present in the R2 REPAIR-PASS wave's own build evidence
(docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/build.err). The R2 prereg
carried no compile-stderr bar at all; the V2 prereg's K-G1 introduced
one that no implementation could pass. Killing a working mechanism on
this bar would be a false negative against the loop's own documented
toolchain facts.

## Amended K-G1 (re-frozen)

- K-G1 (compiles under the pinned znc): the pinned znc compiles
  ddesp2.zag with exit 0 and produces an executable. stderr must
  contain no bytes other than the pinned toolchain's unconditional
  zagd-availability warning (the single documented warning line above;
  byte-identical to the warning in the R2 REPAIR-PASS build evidence).
  Kill: nonzero exit, no executable, any compile error, or any stderr
  byte beyond that documented warning line.

## Transparency record

- Discovered from toolchain behavior during the first compile attempt,
  before any evaluation run; no experiment result was seen, so no bar
  is altered after results.
- The implementation file ddesp2.zag is written but uncommitted; this
  amendment is committed first, then the implementation, so the
  amended prereg strictly predates the implementation in the commit
  record and the commit-order self-check holds.
- This is a repair of a defective bar (unsatisfiable under the pinned
  toolchain for any implementation), not a weakening to force a pass:
  any genuine compile error or unexpected stderr byte still kills.
