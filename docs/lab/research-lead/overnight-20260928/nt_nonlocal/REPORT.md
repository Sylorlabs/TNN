# REPORT: NT-NONLOCAL -- revision-target pinning (D5), a non-entry-local relevance signal

## Verdict

**FIX-CLEAN** per the frozen verdict mapping (PREREG Section 8).
K1=1, K2=1, K3=1, K4=1, K5=1, K6=1, K7=1. Every frozen number --
all 8 arms' ttcA/probeA/nevict/phev, all 48 per-pass probe flags,
all avail, all c/nc/u/forget, all bprobe, all EVHIST bins,
evh(148), evh(118) -- matches the prereg exactly. No trace
arithmetic error this lane: the hand-derived Section 5 predictions
were byte-exact against the binary on the first run.

## Frozen results (3/3 byte-identical)

- Run digest: `36f36fec8c995f8ab78c3927a5bd0be6e3e65427d5e6e4eef25ab2c3617d4ada`
- Binary digest: `1d6a118a7dfb252dc55fc16fb921bcb23b3a1b0219f65c918f3580de42046170`
- Source digest: `3f11766d2c3eb664f56e675d96625b2061535102939deb8595808eeeeaae00dd`

```
NTNL L1 ttcA=2 probeA=8 nevict=10 phev=0
NTNL L1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL L1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL L1 EVHIST 143=5 144=5
NTNL L2 ttcA=2 probeA=8 nevict=10 phev=0
NTNL L2 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL L2 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL L2 EVHIST 143=5 144=5
NTNL L3 ttcA=2 probeA=8 nevict=10 phev=0
NTNL L3 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL L3 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL L3 EVHIST 143=5 144=5
NTNL L6 ttcA=2 probeA=8 nevict=10 phev=0
NTNL L6 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL L6 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL L6 EVHIST 143=5 144=5
NTNL F1 ttcA=2 probeA=8 nevict=11 phev=0
NTNL F1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL F1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL F1 EVHIST 143=6 144=5
NTNL F2 ttcA=2 probeA=8 nevict=11 phev=0
NTNL F2 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL F2 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL F2 EVHIST 143=6 144=5
NTNL F3 ttcA=2 probeA=8 nevict=11 phev=0
NTNL F3 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL F3 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL F3 EVHIST 143=6 144=5
NTNL F6 ttcA=2 probeA=8 nevict=11 phev=0
NTNL F6 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTNL F6 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTNL F6 EVHIST 143=6 144=5
NTNL K1=1 K2=1 K3=1 K4=1 K5=1 K6=1 K7=1
NTNL VERDICT=FIX-CLEAN
```

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8/8, all
  eight arms. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2 AND
  u = 4 on ALL eight arms. The pin protects only live revision
  targets; phase-1 sleepers are never victims (phev = 0,
  evh(118) = 0 everywhere). Zero D3-style sleeper cost, as in D4.
- K3 (the fix bar: availability): PASS. avail = 4 on ALL eight
  arms -- exactly as traced. L3 improves 3->4 and L6 0->4 vs D4;
  the per-pass series is 0,0,1,1,1,1 on every arm.
- K4 (final revision outcome): PASS. c = 2 AND forget = 0 on ALL
  eight arms, including L6 (D4: c=1, forget=1). Revision
  completes everywhere and the revised links answer.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS. nevict = 10,10,10,10 / 11,11,11,11 --
  exact. evh(148) = 0 on ALL eight arms (white-box: the RARE link
  is NEVER the D5 victim -- the pin holds through the pass-2
  decision on every last-order arm). EVHIST bins exact:
  L-arms 143=5/144=5, F-arms 143=6/144=5. evh(118) = 0 and
  phev = 0 on ALL arms.
- K6 (discriminative validity): PASS. avail(L1) = 4 AND
  nevict > 0 on all eight arms.
- K7 (the K=6 pin bar; the parent requirement): PASS.
  avail(L6) = 4 AND avail(F6) = 4. Last-order K=6 -- the case D2,
  D3, and D4 all fail -- is FIXED.

## What this establishes

1. **A non-entry-local, learner-available signal DOES pin the
   useful-but-rarest link.** D5's revision-target pinning fixes
   last-order K=6 (avail 0->4) and improves last-order K=3
   (avail 3->4), with evh(148)=0 on all 8 arms. Mechanism
   (white-box, traced exactly): on pass 2 of every last-order
   arm, link 100 carries ref=2 toward taught obj 148, so 148 is
   pinned; the victim that D2/D3/D4 all select (148, the
   youngest unread novel) is replaced by 143. 148 survives to
   the pass-3 revision, the pass-3 probe reads it (R 0->1), and
   D4's read protection carries it from there. At the decision
   point 148's own entry is (sup1,ref0,F1,R0) -- entry-locally
   identical to the other novels -- so the protection comes
   entirely from the (100,148) relationship: link 100's live
   contradiction state plus the teaching history. That is the
   non-entry-local signal, and it is the earliest
   learner-available indicator of downstream query dependence:
   the learner knows its belief about 100 is heading toward 148,
   so near-future q(100) queries will need 148's link -- known
   before any query succeeds through 148.
2. **Forward-looking beats backward-looking for the
   never-yet-read case.** D2 (recency), D3 (frequency), D4
   (reads) are all backward-looking: they rank entries by past
   events. D5's pin is forward-looking: it protects where the
   learner's knowledge is heading (pending revision targets),
   not where it has been. The sharpening chain across the lanes
   is now: liability moves young (D2) -> infrequent (D3) ->
   never-yet-read (D4) -> ELIMINATED for revision targets (D5),
   with the honest residual that non-revision-target rare links
   remain unprotected (boundary below).
3. **The pin does not reduce pressure; it redirects it (cost).**
   L-arm nevict rises to 10/10/10/10 (D4: 10/8/6/2): keeping 148
   alive means the 143/144 revolve cascade runs on every arm
   instead of terminating early via 148's eviction. F-arms stay
   11. bprobe drops to 2/3 on ALL arms (D4's L6 kept 3/3 only
   because 148, not 143, was the absentee). The fix is paid in
   churn and FREQ-novel probe coverage, NOT in retention of
   uncontested knowledge (u=4/4, phev=0 everywhere) and NOT in
   revision outcome (c=2/2, forget=0 everywhere).
4. **The pin is not a researcher importance flag (honesty
   check).** It fires uniformly for any live revision target:
   during passes 1-2 it protects 148 (link 100's target) AND 130
   (link 104's target) alike, with no judgment about which
   matters. No usefulness oracle, no task identity, no probe
   schedule enters the pin: pins are set exclusively by teaching
   events (ref++), never by queries. The per-pass probe is what
   makes 148 useful; the pin is set by the contradiction
   dynamics, which are learner-internal. The distinction held:
   130 was pinned on every arm and the mechanism trace confirms
   both pins behaved identically.
5. **D1's evidence preservation is intact throughout.** Every
   evicted entry's checkpoint survives; the failure mode under
   test was always PRESENCE (availability when queried), not
   evidence loss -- as in NTLV/NTFQ/NTUE.

## D4 vs D5 comparison (last-order then first-order)

| arm | D4 avail | D5 avail | D4 nevict | D5 nevict | D4 evh148 | D5 evh148 | D4 bprobe | D5 bprobe |
|-----|----------|----------|-----------|-----------|-----------|-----------|-----------|-----------|
| L1  | 4        | 4        | 10        | 10        | 2         | 0         | 2         | 2         |
| L2  | 4        | 4        | 8         | 10        | 1         | 0         | 2         | 2         |
| L3  | 3        | 4        | 6         | 10        | 1         | 0         | 2         | 2         |
| L6  | 0        | 4        | 2         | 10        | 1         | 0         | 3         | 2         |
| F1  | 4        | 4        | 11        | 11        | 0         | 0         | 2         | 2         |
| F2  | 4        | 4        | 11        | 11        | 0         | 0         | 2         | 2         |
| F3  | 4        | 4        | 11        | 11        | 0         | 0         | 2         | 2         |
| F6  | 4        | 4        | 11        | 11        | 0         | 0         | 2         | 2         |

u=4/4, phev=0, evh(118)=0 on all arms under both rules (not
tabulated). D5's gains (L3/L6 availability, zero 148 evictions)
are paid in L-arm churn and one bprobe point on L6.

## What broke / what needed to change

Nothing. The frozen predictions matched the binary exactly on
all 8 arms on the first build -- including the exact nevict
counts (10/10/10/10, 11/11/11/11), the exact EVHIST bins, all 48
per-pass probe flags, and the white-box evh(148)=0. No K5-style
trace correction was needed.

## Honest boundaries (from PREREG Section 9, unchanged)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed.
- The pin is not a usefulness detector: it fires for ANY live
  revision target (148 and 130 alike) with no judgment about
  which matters. A useful link that is never the target of a
  contradiction gets NO D5 protection -- the signal covers
  "where my beliefs are heading," not "what will matter." A
  workload whose rare-but-useful link is not a revision target
  would still fail. Stated coverage limit, not a patch target
  for this lane.
- Stale-pin boundary: a pin persists until the contesting link
  revises. If contradiction stopped forever, the pin would leak
  capacity. Not exercised here (revision completes on pass 3);
  a decay would be a new lane.
- The D5 pin IS a protection mechanism -- the thing NTUE's
  subject description said the comparator lacks. This lane's
  hypothesis was that a learner-state-driven pin (not a
  researcher importance flag) is the missing piece; the REPORT
  judges the distinction held (point 4 above).
- reinf preserved by D1 but not consulted by the comparator
  (documented dead weight).
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
- New rule = new lane: D1/D2/D3/D4 and their lanes are untouched.

## Recommended follow-up (not preregistered; for the parent)

- The residual honest case: a rare-but-useful link that is NOT a
  revision target (no contradiction ever points at it). D5 does
  not cover it. Candidate non-entry-local signals for that case:
  query-dependence inferred from the query procedure's own
  routing structure (which keys does the 2-hop machinery need
  for the queries the learner actually issues?), or
  structural-dependence (in-degree) once revision completes --
  but NTUE Section 5.4's mechanism note already shows in-degree
  from stored objs is 0 for 148 pre-revision, so the signal must
  come from the teaching stream or the query stream, not the
  stored graph.
- The stale-pin boundary (pin persists if revision never
  completes) deserves its own lane: principled pin lifecycle /
  decay, evaluated on retention/churn, not on K=6.
- The D5-vs-D4 churn tradeoff (L6: nevict 2->10, bprobe 3->2)
  suggests measuring the pin's cost curve across capacity
  points (1.05x is a single point): at higher pressure the
  redirect may cost more than the fix is worth.
- The tie-break finding from NTUE (max-ins vs min-ins
  determining order-dependence) still stands and still deserves
  its own lane.

## Provenance

- Prereg frozen alone: commit `b6ff8416039d8a5614c4ed2ee319dbb1c28147c2`
  on `tnn-native-lab` (PREREG.md + NAMECHECK.md only), strictly
  before implementation. Commit-order self-check: `git log` shows
  b6ff84160 strictly precedes the implementation commit below;
  no implementation file existed at prereg time (lane dir
  contained only PREREG.md + NAMECHECK.md). Committed via git
  plumbing (separate index file: read-tree / add / write-tree /
  commit-tree / update-ref with old-value check) to
  `tnn-native-lab` because the shared working tree is on a side
  branch with other workers' staged changes; explicit pathspecs
  only; the shared index untouched.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE/NT-PORT-PRESSURE/NT-LOWVALUE-
  BOUNDARY/NT-ORDER-MIRROR/NT-FREQ-EVICT/NT-USEFUL-EVICT).
  `which python3` and `which python` return nothing under the
  worker PATH. Zero forbidden-executable invocations.
- Source: `ntnl_full.zag`, written to PREREG Sections 2-4
  (learner: D1 kept, D4 base comparator kept, D5 =
  revision-target pinning via per-slot pendtgt set on ref++,
  cleared on revision/install; pin-aware victim scan with D4
  fallback; oracles/protocol/harness from ntnl template =
  ntue verbatim; teachB parameterized by order; 8 arms;
  K1-K7 bars per PREREG Sections 7-8).
- Build: `znc ntnl_full.zag -o ntnl_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning only, as in
  NTUE); 3/3 runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5
  pin (the arm/order/K selector is a harness condition); the
  pin condition uses only learner contradiction state. The
  string "python" appears nowhere in the source (header comment
  reads "Pure Zag. No Python."); compiler-defect workarounds
  honored (single-buffer cursor output + one raw syscall; no
  `as *i32`+slice; no `!(A && B)` in while conditions;
  if-nesting mirrors the frozen NTUE template shapes; no
  `[]u8 as *u8` casts; `_zag_malloc as *u8` threaded through).
- The K7 verdict (FIX-CLEAN) is reported per the frozen mapping;
  the REPORT documents the cost (churn, bprobe) honestly rather
  than as a defect.
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
