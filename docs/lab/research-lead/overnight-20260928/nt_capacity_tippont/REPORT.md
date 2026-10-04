# REPORT: NT-CAPACITY-TIPPOINT -- the exact opportunity-cost tipping point

## Verdict

**TIPPOINT-LOCATED-AT-20** per the frozen verdict mapping (PREREG
Section 8). Both arms hit their frozen exact predictions on the
first implementation run, 3/3 byte-identical:

- ARM21 (CAP=21): U1=1 U2=1 U3=1 U4=1 U5=1 -> TIP-CLEAN-AT-21
- ARM22 (CAP=22): R1=1 R2=1 R3=1 R4=1 R5=1 R6=1 R7=1 -> REPRODUCED

## Frozen results (3/3 byte-identical)

- Run digest: `b2810ba0d97886029990e9f51dc5688c76dd04000cc87f6b332b8da938ee245a`
- Binary digest: `87a2056e935504c9acfc01cd7ba49164e27947085d5161a5d3996d573dd0a4d6`
- Source digest: `38e204b677a09b425711045f1b01204cf22b18e0e342fdccdb2a143ad8ff530f`

```
NTSWEEP R6-CAP21 ttcA=2 probeA=8 nevict=28 phev=0
NTSWEEP R6-CAP21 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTSWEEP R6-CAP21 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTSWEEP R6-CAP21 RET c=2 nc=2 u=4 forget=0 bprobe=0 resprobe=1
NTSWEEP R6-CAP21 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTSWEEP R6-CAP21 EVHIST 131=5 140=6 141=6 143=6 144=5
NTSWEEP R6-CAP21 U1=1 U2=1 U3=1 U4=1 U5=1
NTSWEEP R6-CAP21 ARM-VERDICT=TIP-CLEAN-AT-21
NTSWEEP R6-CAP22 ttcA=2 probeA=8 nevict=22 phev=0
NTSWEEP R6-CAP22 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTSWEEP R6-CAP22 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTSWEEP R6-CAP22 RET c=2 nc=2 u=4 forget=0 bprobe=1 resprobe=1
NTSWEEP R6-CAP22 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTSWEEP R6-CAP22 EVHIST 140=5 141=6 143=6 144=5
NTSWEEP R6-CAP22 R1=1 R2=1 R3=1 R4=1 R5=1 R6=1 R7=1
NTSWEEP R6-CAP22 ARM-VERDICT=REPRODUCED
NTSWEEP VERDICT=TIPPOINT-LOCATED-AT-20
```

## The located tipping point

| CAP | pressure | rescue (avail160) | FP useless/apin | opportunity cost | nevict |
|-----|----------|-------------------|-----------------|------------------|--------|
| 20  | 1.25x    | 4 (YES)           | 2/4 (50%)       | YES: 118 displaced, u=3, forget=1, phev=1 | 30 |
| 21  | 1.19x    | 4 (YES)           | 2/4 (50%)       | none (u=4, forget=0, phev=0) | 28 |
| 22  | 1.14x    | 4 (YES)           | 2/4 (50%)       | none (u=4, forget=0, phev=0) | 22 |
| 24  | 1.04x    | 4 (YES)           | 2/4 (50%)       | none (u=4, forget=0, phev=0) | 10 |

CAP=21 is CLEAN: no A-link displaced (phev=0, evh118=0),
uncontested retention intact (u=4), no forgetting event
(forget=0). The opportunity cost appears at CAP=20 and at no
higher tested capacity. The exact integer threshold where the
cost appears is **CAP=20**: cost iff CAP <= 20, clean iff
CAP >= 21, on the tested 20/21/22 slice. (CAP=23 untested;
the sweep's honest boundary on 23 stands.)

## Kill-bar evaluation

- ARM21: U1=1 (ttcA=2, probeA=8). U2=1 (rescue holds: avail160=4,
  resprobe=1, evh160=evh161=0). U3=1 (FP confirmed: dec=1,
  useless=2). U4=1 (clean tipping signature exact: phev=0,
  evh118=0, u=4, forget=0, nc=2, c=2). U5=1 (pressure exact:
  nevict=28, evh148=0, EVHIST 131=5,140=6,141=6,143=6,144=5,
  bprobe=0). -> TIP-CLEAN-AT-21.
- ARM22: R1-R7 all 1; every number matches the NT-CAPACITY-SWEEP
  ARM22 frozen run (ttcA=2, probeA=8, nevict=22, EVHIST
  140=5,141=6,143=6,144=5, u=4, forget=0, bprobe=1, apin=4,
  dec=1, useless=2). -> REPRODUCED (regression bar green;
  the CAP=21 reading is trustworthy).

## Mechanistic explanation of the threshold

The tipping point is decided in pass 1, before any assoc pin
matters, by a single-slot difference in eviction demand.

Pass-1 installs 11 novel keys (130,131,140,141,143,144,160,161,
170,171,148) into CAP-14 free slots, so pass-1 eviction demand
is 25 - CAP. The pass-1 victims, in max-ins order among the R=0
unpinned novels, are fixed: 144, 143, 141, 140, 131 (ins 20, 19,
18, 17, 16). Key 131 is the 5th victim. Therefore 131 survives
pass 1 iff 25 - CAP <= 4, i.e. CAP >= 21. At CAP=20 the five
evictions consume {144,143,141,140,131}; at CAP=21 only four
are needed ({144,143,141,140}) because 160 installs into the
21st free slot without an eviction, and 131 is spared.

The displacement itself happens at pass 2's first restore
(131@78). At that moment the six pins are all live: D5 pins
{130,148} (pending revision targets from the 100@73 and 104@74
contradictions) plus assoc pins {160,161,170,171}. If 131 was
evicted in pass 1 (CAP <= 20), every R=0 slot is pinned and all
14 A-links have R>=3 (100:4,101:7,105:6, the rest 3), so the D4
min-reads/max-ins scan falls through to the A-links and takes
the youngest R=3 one: 118 (ins 14). 118 is never restored
(teachB never teaches it), so retest q(117) misses: u=3,
forget=1, phev=1. If 131 survived pass 1 (CAP >= 21), the
restore finds 131 installed (an agree, no eviction), and every
later eviction finds at least one unpinned R=0 slot: 131
itself at pass-2 #5, then the rotating novel each pass, with
130 as a permanent R=0 unpinned backstop after pass-3 revision
clears the D5 pins (130 is never read, never evicted, and
loses every max-ins tie-break with ins 15). No A-link is ever
an eviction candidate: phev=0, u=4, forget=0.

In short: the step function is cost iff CAP <= 20, clean iff
CAP >= 21. The threshold is sharp because the 5th pass-1
victim in max-ins order is exactly 131, the key whose pass-2
restore is the displacement trigger. One more slot (20->21)
removes exactly that victim, and the whole downstream cascade
(118 displaced, u=3, forget=1) never fires.

## What this establishes

1. The exact integer tipping point is located: CAP=20 is the
   last capacity where the D6 assoc pin displaces an A-link;
   CAP=21 is already clean. The sweep's honest boundary
   ("CAP=21/23 untested -- the exact tipping point between 20
   and 22 is not located") is now closed for 21; CAP=23
   remains untested.
2. The mechanism is a one-slot pass-1 eviction-demand effect,
   not a gradual pressure gradient: 25-CAP >= 5 evictions in
   pass 1 consumes the 131 backstop, and the six pins then
   cover every R=0 slot at the critical pass-2 moment.
3. The rescue (avail160=4) and the FP cost (50%) are
   capacity-invariant across 20/21/22/24; only the retention
   cost is a step function, and its step is now exactly
   located between 20 and 21.

## What this does NOT establish (honest boundaries)

- The threshold is a 3-point slice (20/21/22), not a general
  capacity law. CAP=23 was not run; W=20, K=6, the exploratory
  gap (14 ticks), and contradiction magnitude are all fixed;
  the threshold's position may move with any of them.
- The 5th-victim account depends on the frozen install order
  and the max-ins tie-break; a different workload ordering
  could move which key is the marginal victim.
- No no-D6 control arms were run; the LINKS are memorized
  associations; no L2/L3 claim.

## Provenance

- Prereg frozen alone: commit
  `ae1ebeba5d0f8cc0c8fc1f03f36dcda8cecea4a5` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before
  implementation. Commit-order self-check: `git log` shows
  ae1ebeba5 strictly precedes the implementation commit below;
  no implementation file existed at prereg time.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev. `which python3` and `which
  python` return nothing under the worker PATH. Zero
  forbidden-executable invocations. The string "python" appears
  nowhere in the source.
- Source: `nttip_full.zag` = `ntsweep_full.zag` verbatim EXCEPT
  `main` runs two arms (R6-CAP21 with bars U1-U5, R6-CAP22 with
  bars R1-R7) instead of three; tag prefix NTSWEEP retained.
  ARM22 reproduces the sweep's ARM22 numbers exactly,
  confirming the re-spliced main changed nothing.
- Build: `znc nttip_full.zag -o nttip_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning + 4 benign A0102
  warnings on the intentionally result-discarding exploratory
  queries, same as NT-CAPACITY-SWEEP). 3/3 runs byte-identical
  (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5 pin
  and the D6 assoc rule under test; the K selector, exploratory
  episode, and probe schedule are harness conditions.
  Compiler-defect workarounds honored (single-buffer cursor
  output + one raw syscall; no `as *i32`+slice; no `!(A && B)`
  in while conditions; no `[]u8 as *u8` casts; `_zag_malloc as
  *u8` threaded through).
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
