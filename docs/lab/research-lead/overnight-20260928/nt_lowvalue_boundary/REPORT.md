# REPORT: NT-LOWVALUE-BOUNDARY -- the "genuinely low-value" boundary: D2 evicts useful-but-infrequently-reinforced links

## Verdict

**LIABILITY-CONFIRMED** per the frozen verdict mapping (PREREG
Section 8). K1, K2, K3, K4, K5, K6 all hold. This is the preregistered
directional prediction (liability hypothesis), and -- like NT1, NT-D2,
NT-PORT, NT-PRESSURE, and NT-PORT-PRESSURE before it -- EVERY frozen
numeric prediction matched exactly, including the full per-pass probe
series on all four arms and all four eviction histograms.

## Frozen results (3/3 byte-identical)

- Run digest: `d02dcf32d609fdc31ac7f6299c0b746a0e03c581e08d1aa274d367036ab57932`
- Binary digest: `aaff5aa0a8e65084eee7c813117993c6880dc826eefc7f78cf472e0c752f6525`
- Source digest: `8ddb1790b53262b22e24ad942aa14148e627b0c5896a9b45da391e720436af56`

```
NTLV P1 ttcA=2 probeA=8 nevict=11 phev=0
NTLV P1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTLV P1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTLV P1 EVHIST 144=6 148=5
NTLV P2 ttcA=2 probeA=8 nevict=6 phev=0
NTLV P2 PPROBE p1=0 p2=0 p3=1 p4=0 p5=1 p6=0 avail=2
NTLV P2 RET c=1 nc=2 u=4 forget=1 bprobe=3
NTLV P2 EVHIST 144=3 148=3
NTLV P3 ttcA=2 probeA=8 nevict=4 phev=0
NTLV P3 PPROBE p1=0 p2=0 p3=0 p4=1 p5=0 p6=0 avail=1
NTLV P3 RET c=1 nc=2 u=4 forget=1 bprobe=3
NTLV P3 EVHIST 144=1 148=1
NTLV P6 ttcA=2 probeA=8 nevict=2 phev=0
NTLV P6 PPROBE p1=0 p2=0 p3=0 p4=0 p5=0 p6=0 avail=0
NTLV P6 RET c=1 nc=2 u=4 forget=1 bprobe=3
NTLV P6 EVHIST 144=1 148=1
NTLV K1=1 K2=1 K3=1 K4=1 K5=1 K6=1
NTLV VERDICT=LIABILITY-CONFIRMED
```

Prediction vs actual: NO misses. avail 4/2/1/0; nevict 11/6/4/2;
EVHIST bins exactly as hand-traced (P1: 144=6, 148=5; P2: 144=3,
148=3; P3: 144=2, 148=2; P6: 144=1, 148=1); final c 2/1/1/1 with
forget 0/1/1/1; nc = 2 and u = 4 on all arms; bprobe 2/3/3/3;
phev = 0 on all arms. The prereg hand-traces (Sections 5.1-5.4)
reproduced the binary exactly on all four arms.

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8/8, all four
  arms. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2/2, u = 4/4,
  all four arms. The infrequent-reinforcement regime does not disturb
  agreed/shared/untouched chains.
- K3 (the boundary bar: availability tradeoff): PASS. avail =
  4, 2, 1, 0 for K = 1, 2, 3, 6, exactly as traced.
- K4 (final revision outcome): PASS. P1: c = 2/2, forget = 0; P2/P3/
  P6: c = 1/2, forget = 1. Revision itself always completes
  (100 -> 148 revises in place on pass 3 in every arm); what is lost
  is the RARE second link, so q(100) answers -1.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS. nevict = 11/6/4/2 exactly; phev = 0 on all
  arms (zero phase-1-link subjs evicted); evh(148) > 0 on all arms
  (5/3/2/1: white-box confirmation that D2 evicted the RARE link
  itself, on every non-teach pass).
- K6 (discriminative validity): PASS. avail(P1) = 4 (the probe
  passes whenever the link is present; not a broken probe) and
  nevict > 0 on all arms.

## What this establishes

1. **D2's evict-youngest IS a liability for genuinely-useful-but-
   infrequently-reinforced links under capacity pressure.** The RARE
   link (148,1)->152 is required by the scored revised query q(100),
   yet D2 evicts it on every pass it is not re-taught. Mechanism
   (white-box, from the histogram): the RARE link is taught last in
   ascending order, so each D1-restore re-installs it YOUNG (fresh
   max ins); the FREQ background churn then evicts the youngest
   entry first, which is the just-restored RARE link. Tenure
   protection never engages because re-installation keeps resetting
   its age: the churn trap.
2. **The tradeoff is quantified: availability ~= 1/K.** Over the
   scored window (passes 3-6), q(100) answers correctly on 4/4, 2/4,
   1/4, 0/4 passes for K = 1, 2, 3, 6. The link is lost ~1 pass after
   each re-teach. There is no safe infrequent regime at this
   pressure and teach order: even K=2 halves availability, and K=6
   (taught once) never recovers after pass 2.
3. **The failure is D2's usefulness-blindness, not capacity alone.**
   Pigeonhole forces exactly 1 of 21 keys absent; a usefulness-aware
   policy could pin 148 (needed for a scored query) and sacrifice a
   FREQ link instead. D2 cannot: its victim choice is pure
   installation recency. Note the perverse detail: at K=6 the FREQ
   chains score a perfect bprobe = 3/3 (no churn once the RARE link
   stops being re-taught) while the genuinely useful RARE link is
   gone. Less reinforcement of the useful link IMPROVES the
   background scores.
4. **D1's evidence preservation is intact throughout.** The RARE
   link's checkpoint (obj, sup, ref) survives every eviction; on
   re-teach passes it is restored with accumulated evidence and
   answers correctly immediately. The liability is purely about
   PRESENCE (availability when queried), not about evidence loss.
   Nothing is ever "forgotten" in the D1 sense; it is simply absent
   when needed.

## What broke / what needed to change

Nothing in the rule set broke: the D1+D2 port required NO changes.
One build note: the first draft of the kill-bar section nested ifs
8-12 deep; per the AGENTS.md third-compiler-defect workaround these
were refactored into per-arm helper fns (max 3-deep) before
building. The frozen binary was built only from the corrected
source. No prediction was touched.

## Honest boundaries (from PREREG Section 9, unchanged)

- The RARE link is taught LAST in ascending order; its youth at
  re-teach is load-bearing for the churn-trap mechanism. A
  first-taught RARE link would tenure-protect instead (old ins is
  never the D2 victim). That is a separate experiment, not this one.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed, so the availability curve conflates period
  with final-pass phase alignment by construction (the per-pass
  probe series is what separates frequency from phase).
- The liability named is D2's usefulness-blindness manifesting as a
  churn trap, not a claim that any policy retains everything
  (21 keys, 20 slots).
- Port covers the associative instance memory only (NT-PORT
  boundary stands: contlearn2 schema machinery and H-CONTLIFE-1
  hash-table memory remain unported).

## Recommended follow-up (not preregistered; for the parent)

- Order-dependence experiment (preregistered as a note in Section 9):
  teach the RARE link FIRST among novel links; prediction from the
  frozen rules is tenure-protection (avail = 4/4 for all K) -- the
  mirror image that would confirm installation recency, not
  reinforcement frequency, is the true determinant under D2.
- Frequency-aware or usefulness-aware comparator: the honest
  alternative-policy comparison this lane cannot run (would need a
  new rule, i.e., a new prereg).
- Interaction with the nt_lifobound INCONCLUSIVE result: that lane
  (key-value workload, once-taught novels) could not discriminate;
  this lane shows the structured-family + usefulness-probe design
  does.

## Provenance

- Prereg frozen alone: commit `2a372baf1` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  `git log` shows 2a372baf1 strictly precedes the implementation
  commit below; no implementation file existed at prereg time.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE/NT-PORT-PRESSURE). `which python3`
  and `which python` return nothing under the worker PATH. Zero
  forbidden-executable invocations.
- Source: `ntlv_full.zag`, written to PREREG Sections 2-4 (learner
  fns verbatim from the nt_port_pressure template; novel oracles,
  teachB(K,pass), per-pass probe, 4-arm harness, K1-K6 bars per
  PREREG Sections 3/4/7).
- Build: `znc ntlv_full.zag -o ntlv_bin` under safebin-only PATH
  (exit 0; benign zagd-unavailable warning only, as in NTPP); 3/3
  runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode logic in
  the learner (the arm/period selector is a harness condition);
  "python" appears only in header comments ("Pure Zag. No Python.")
  and NAMECHECK; compiler-defect workarounds honored (single-buffer
  cursor output + one raw syscall; no `as *i32`+slice; no
  `!(A && B)` in while conditions; if-nesting at most 3 deep).
- Commits local only, explicit pathspecs, never pushed.
