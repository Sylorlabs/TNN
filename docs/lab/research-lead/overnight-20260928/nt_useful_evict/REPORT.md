# REPORT: NT-USEFUL-EVICT -- usefulness-aware eviction (D4) with a learner-available read signal

## Verdict

**FAIL-PRESSURE** per the frozen verdict mapping (PREREG Section 8).
K1=1, K2=1, K3=1, K4=1, K5=0, K6=1, K7=0. The K5 failure is a
hand-trace arithmetic error in the preregistered nevict
predictions (overcounted 144 evictions by exactly 1 on L1, L2,
L3), NOT a mechanism or discipline violation: every white-box
mechanism-attribution check (evh(148) pattern 2/1/1/1 last-order
and 0/0/0/0 first-order, evh(118)=0, phev=0 on all 8 arms)
matches the trace exactly, and every substantive bar (K1-K4,
K6, and the headline K7) matches the frozen prediction exactly,
including the full per-pass probe series on all eight arms.
Corrected trace in Section "What broke" below; the binary is
authoritative and self-consistent.

## Frozen results (3/3 byte-identical)

- Run digest: `7cef01c53b6fe844fdf44f64407f532347e313063fb58a603939f3af9767be18`
- Binary digest: `0686f32bf71e2da2f454999984c6a95b8ec45bfca7eab2fa36d2c75355defcef`
- Source digest: `cb5d0f118e455cbdf5451afd2c829ee6974d2d376f6170f139ebc4e94dd56dde`

```
NTUE L1 ttcA=2 probeA=8 nevict=10 phev=0
NTUE L1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE L1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE L1 EVHIST 143=3 144=5 148=2
NTUE L2 ttcA=2 probeA=8 nevict=8 phev=0
NTUE L2 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE L2 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE L2 EVHIST 143=3 144=4 148=1
NTUE L3 ttcA=2 probeA=8 nevict=6 phev=0
NTUE L3 PPROBE p1=0 p2=0 p3=0 p4=1 p5=1 p6=1 avail=3
NTUE L3 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE L3 EVHIST 143=2 144=3 148=1
NTUE L6 ttcA=2 probeA=8 nevict=2 phev=0
NTUE L6 PPROBE p1=0 p2=0 p3=0 p4=0 p5=0 p6=0 avail=0
NTUE L6 RET c=1 nc=2 u=4 forget=1 bprobe=3
NTUE L6 EVHIST 144=1 148=1
NTUE F1 ttcA=2 probeA=8 nevict=11 phev=0
NTUE F1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE F1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE F1 EVHIST 143=6 144=5
NTUE F2 ttcA=2 probeA=8 nevict=11 phev=0
NTUE F2 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE F2 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE F2 EVHIST 143=6 144=5
NTUE F3 ttcA=2 probeA=8 nevict=11 phev=0
NTUE F3 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE F3 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE F3 EVHIST 143=6 144=5
NTUE F6 ttcA=2 probeA=8 nevict=11 phev=0
NTUE F6 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTUE F6 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTUE F6 EVHIST 143=6 144=5
NTUE K1=1 K2=1 K3=1 K4=1 K5=0 K6=1 K7=0
NTUE VERDICT=FAIL-PRESSURE
```

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8/8, all
  eight arms. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2 AND
  u = 4 on ALL eight arms. D4 pays no D3-style sleeper cost:
  the read signal protects phase-1 links (read during phase-1
  probeA, R>=2), so phev = 0 everywhere. This is D4's
  confirmed advantage over D3 (which sacrificed the 118
  sleeper, u=3/4).
- K3 (the fix bar: availability): PASS. avail = 4, 4, 3, 0 for
  L1, L2, L3, L6 and 4, 4, 4, 4 for F1, F2, F3, F6 -- exactly
  as traced, including the full per-pass probe series on all
  eight arms (every p1..p6 flag matches). D4 fixes K=2 and K=3
  last-order (2->4 and 1->3 vs the D2 baseline) and pins 148
  first-order at all K including K=6.
- K4 (final revision outcome): PASS. L1/L2/L3: c = 2,
  forget = 0; L6: c = 1, forget = 1 (the forget is the absent
  148, not a revision failure); F1/F2/F3/F6: c = 2,
  forget = 0. Revision completes on every arm.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): FAIL. nevict = 10, 8, 6, 2 (L1..L6) vs the
  traced 11, 9, 7, 2; F-arms match exactly (11, 11, 11, 11).
  evh(148) = 2, 1, 1, 1 (L) and 0, 0, 0, 0 (F) -- matches
  exactly. evh(118) = 0 and phev = 0 on all arms -- matches
  exactly. The failure is nevict only, on L1/L2/L3, off by
  exactly 1 each (fewer 144 evictions than hand-traced).
  Section "What broke" gives the corrected trace; the
  mechanism attribution is intact.
- K6 (discriminative validity): PASS. avail(L1) = 4 and
  nevict > 0 on all eight arms.
- K7 (the K=6 pin bar; the follow-up hypothesis): FAIL as
  PREDICTED. avail(L6) = 0 (traced 0), avail(F6) = 4 (traced
  4). The usefulness rule pins the taught-once RARE link in
  first-order but not in last-order -- the exact
  discrimination the follow-up hypothesis needed, and the
  predicted USEFUL-BUT-BOUNDED outcome, preempted in the
  verdict ordering only by the K5 trace error.

## What this establishes

1. **The usefulness-aware rule DOES pin the RARE link via a
   learner-available signal, with zero retention cost.**
   Availability: 4/4/3/0 last-order (vs D2's 4/2/1/0 and D3's
   4/4/3/0) and 4/4/4/4 first-order (vs D2's 4/4/4/4).
   Mechanism (white-box): the per-pass probe q(100) routes
   through 148 from pass 3 on (after revision); 148
   accumulates reads (R>=1) and is then excluded from the
   min-reads victim set, so the churn moves onto never-read
   FREQ novels. Phase-1 sleepers (R>=2 from phase-1 probeA)
   are never victims: u=4/4, phev=0 on all 8 arms, evh(118)=0.
   D4 achieves D3's availability WITHOUT D3's sleeper
   sacrifice -- the read signal dominates teaching-frequency
   as a protection criterion for old knowledge.
2. **First-order K=6 is FIXED (avail 4); last-order K=6 is
   NOT (avail 0).** In first-order, the max-ins tie-break
   spares the first-installed 148 on pass 1, the pass-3 probe
   reads it (R 0->1), and reads protect it thereafter
   (evh(148)=0 on all F-arms). In last-order K=6, 148 is
   evicted on pass 2 before any query routes through it
   (R=0; the pass-1 probe went 100->101->102): at the decision
   point it is entry-locally identical to the other novels
   (R=0, F=1), six restores need six victims, and a min-reads
   rule never sacrifices a read (R>=2) sleeper for an unread
   novel -- so 148 is necessarily among the victims. This
   confirms and sharpens NTFQ's honest conclusion: not even
   read/query frequency -- the most natural learner-available
   relevance signal -- escapes the useful-but-rarest problem.
   The liability moves from "young"/"infrequent" to
   "never-yet-read"; it is not eliminated.
3. **The tie-break is load-bearing (finding, not a free
   parameter).** The frozen max-ins tie-break (D2's comparator
   demoted, as in NTFQ) is what spares first-order 148 on pass
   1. The min-ins (FIFO) alternative is traced (not run) to
   give avail 0/0/0/0 first-order: the first-installed RARE
   link would be the first victim on pass 1, before any read.
   For an LFU rule, the tie-break -- not just the primary
   signal -- determines order-dependence. Recorded as a
   boundary in PREREG Section 9.
4. **D4 vs D3 comparison (last-order):**

   | arm | D3 avail | D4 avail | D3 u | D4 u | D3 phev | D4 phev | D3 nevict | D4 nevict |
   |-----|----------|----------|------|------|---------|---------|-----------|-----------|
   | P1  | 4        | 4        | 3    | 4    | 1       | 0       | 5         | 10        |
   | P2  | 4        | 4        | 3    | 4    | 1       | 0       | 3         | 8         |
   | P3  | 3        | 3        | 3    | 4    | 1       | 0       | 3         | 6         |
   | P6  | 0        | 0        | 4    | 4    | 0       | 0       | 2         | 2         |

   D4 matches D3's availability at every K, retains all
   phase-1 knowledge D3 sacrificed, but churns roughly 2x
   (the read signal protects sleepers, so evictions stay
   confined to the novel set and the restore cascade runs
   longer). Tradeoff within the fix: retention vs churn.
5. **D1's evidence preservation is intact throughout.** Every
   evicted entry's checkpoint (obj, sup, ref, reinf, reads)
   survives; nothing is "forgotten" in the D1 sense. As in
   NTLV/NTFQ, the failure is about PRESENCE (availability when
   queried), not evidence loss.

## What broke / what needed to change

The K5 failure is a hand-trace arithmetic error in PREREG
Section 5, not a mechanism defect. The prereg traced 2
evictions on every pass from pass 2 on for L1/L2/L3; the
binary shows the actual pattern has a phase shift: on passes
where the absent novel at pass start is 144 (not 143), only
ONE eviction occurs (143), because 143 was already taught
(as a hit) before 144's restore in the ascending teach order
and is not re-taught. Corrected per-pass eviction counts:

- L1: 1,2,2,1,2,2 (nevict=10; 144=5,148=2,143=3). The prereg
  said 1,2,2,2,2,2 (nevict=11, 144=6): pass 4 has 1 eviction,
  not 2.
- L2: 1,1,1,1,2,2 (nevict=8; 144=4,148=1,143=3). The prereg
  said 1,1,1,2,2,2 (nevict=9): pass 4 has 1 eviction, not 2.
- L3: 1,1,0,1,1,2 (nevict=6; 144=3,148=1,143=2). The prereg
  said 1,1,0,1,2,2 (nevict=7): pass 5 has 1 eviction, not 2.
- L6 and all F-arms: traced exactly (nevict 2 and 11;
  EVHIST exact).

Every other frozen number -- all 48 per-pass probe flags,
all avail, all c/nc/u/forget, all bprobe, evh(148),
evh(118), phev, ttcA, probeA -- matches the prereg exactly.
The D4 mechanism (min-reads victim, max-ins tie-break,
read-protection of 148 and of phase-1 sleepers) is confirmed
by the white-box histograms; only the churn-count arithmetic
was off by one on three arms. Nothing in D1/D2/D3 or their
lanes was touched: this is a new lane with its own source.

## Honest boundaries (from PREREG Section 9, unchanged)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed.
- The read signal is learner-local query-observation preserved
  by D1; no usefulness oracle, no researcher-provided labels,
  no task identity enters the comparator. The per-pass probe
  is a query like any other (PREREG Section 2 disclosure).
- The max-ins tie-break is frozen (D2's comparator demoted, as
  in NTFQ); the min-ins alternative is traced-not-run
  (avail 0/0/0/0 first-order) and recorded as a boundary.
- reinf is preserved by D1 but not consulted by D4's
  comparator (documented dead weight).
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
- New rule = new lane: D1/D2/D3 and their lanes are untouched.
  D2/D3 baselines from the frozen NTLV/NTOM/NTFQ REPORTs.

## Recommended follow-up (not preregistered; for the parent)

- The remaining honest alternative is a NON-entry-local
  relevance signal: downstream query dependence (which queries
  NEED this link, known before the query succeeds), or a
  pinning/protection mechanism driven by query intent rather
  than past reads. D4 shows past-usefulness is insufficient
  for the never-yet-read case; the next lane should test
  whether a forward-looking signal pins last-order K=6.
- The tie-break finding (Section "What this establishes",
  point 3) deserves its own lane: for LFU-family rules, the
  tie-break determines order-dependence. A principled
  tie-break theory (tenure vs recency vs frequency-secondary)
  would generalize beyond this workload.
- The D4-vs-D3 retention/churn tradeoff (point 4) suggests a
  hybrid worth testing: usefulness-primary with a
  churn-bounded victim policy -- but the K=6 result shows no
  entry-local comparator escapes the useful-but-rarest
  problem, so hybrids should be evaluated on retention/churn,
  not on K=6.

## Provenance

- Prereg frozen alone: commit `598a22f89` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before
  implementation. Commit-order self-check: `git log` shows
  598a22f89 strictly precedes the implementation commit below;
  no implementation file existed at prereg time. Committed via
  git plumbing (read-tree/add/write-tree/commit-tree/
  update-ref with old-value check) to `tnn-native-lab`
  because the shared working tree is on a side branch with
  other workers' staged changes; explicit pathspecs only.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE/NT-PORT-PRESSURE/NT-LOWVALUE-
  BOUNDARY/NT-ORDER-MIRROR/NT-FREQ-EVICT). `which python3` and
  `which python` return nothing under the worker PATH. Zero
  forbidden-executable invocations.
- Source: `ntue_full.zag`, written to PREREG Sections 2-4
  (learner: D1 kept, D4 = evict-least-read replaces D3;
  oracles/protocol/harness from ntfq_full.zag; teachB
  parameterized by order; 8 arms; K1-K7 bars per PREREG
  Sections 7-8).
- Build: `znc ntue_full.zag -o ntue_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning only, as in
  NTFQ); 3/3 runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner (the arm/order/K
  selector is a harness condition); "python" appears only in
  header comments ("Pure Zag. No Python.") and NAMECHECK;
  compiler-defect workarounds honored (single-buffer cursor
  output + one raw syscall; no `as *i32`+slice; no `!(A && B)`
  in while conditions; if-nesting as in the frozen NTFQ
  template; no `[]u8 as *u8` casts; `_zag_malloc as *u8`
  threaded through).
- The K5 verdict (FAIL-PRESSURE) is reported per the frozen
  mapping; the REPORT documents it as a trace arithmetic
  error with the corrected trace, not a mechanism failure.
- Commits local only, explicit pathspecs, never pushed.
