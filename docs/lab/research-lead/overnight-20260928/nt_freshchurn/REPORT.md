# REPORT: NT-FRESHCHURN -- Churn without re-teaching: fresh novel subjects each pass

## Verdict

**FRESHCHURN-PASS** at P2 (2x), P3 (3x), and P5 (5x) per-pass pressure,
per the frozen verdict mapping (PREREG Section 7).
**OVERALL=FRESHCHURN-PASS-ALL.** This is the preregistered directional
prediction (the churn-dependence account), and every frozen numeric
prediction matched exactly, including all six eviction histograms bin
for bin, with two documented corrections (Amendments 1-2, both
pre-verdict, neither touching a kill bar).

The verdict answers the key question directly: **yes, fresh-novel-
per-pass restores the NT2 signature in ABL.** The ABL arm loses the
contradicted subjects (c_abl=0/6, forget_abl=6/6) under fresh churn,
reproducing NT-PRESSURE's NT2 failure signature without any
re-teaching, while MAIN keeps K1..K4 (revision 6/6, FORGET=0, churn at
the pigeonhole minimum 3N_n-4, zero phase-1 subjects evicted across
444 total MAIN evictions).

## Frozen results (3/3 byte-identical, post-fix runs)

- Run digest: `926f794cdde3d7807d6692d84d947e844c0558dbee715659d86262ebe6583085`
- Binary digest: `6cdf237fe5bed51934891c03b1d267f933e04960bb10226567688eacb1cd6016`
- Source digest: `b6de3f0ccef0cf7a9c1aed23288d8a719d4fc02f2f977b7ba2293f9a98d0fdee`

```
NTFRESH P2 MAIN ttc=2 probe1=16 nevict=68
NTFRESH P2 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTFRESH P2 MAIN EVHIST 123=1 ... 190=1 (68 bins, 123..190, each 1)
NTFRESH P2 ABL ttc=2 probe1=16 nevict=75
NTFRESH P2 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTFRESH P2 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 143=1 167=1 124..142=1 149..166=1 168..190=1
NTFRESH P2 K1=1 K2=1 K3=1 K4=1 K5=1
NTFRESH P2 VERDICT=FRESHCHURN-PASS
NTFRESH P3 MAIN ttc=2 probe1=16 nevict=128
NTFRESH P3 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTFRESH P3 MAIN EVHIST 123=1 ... 250=1 (128 bins, 123..250, each 1)
NTFRESH P3 ABL ttc=2 probe1=16 nevict=135
NTFRESH P3 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTFRESH P3 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 163=1 207=1 124..162=1 169..206=1 208..250=1
NTFRESH P3 K1=1 K2=1 K3=1 K4=1 K5=1
NTFRESH P3 VERDICT=FRESHCHURN-PASS
NTFRESH P5 MAIN ttc=2 probe1=16 nevict=248
NTFRESH P5 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTFRESH P5 MAIN EVHIST 123=1 ... 370=1 (248 bins, 123..370, each 1)
NTFRESH P5 ABL ttc=2 probe1=16 nevict=255
NTFRESH P5 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTFRESH P5 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 203=1 287=1 124..202=1 209..286=1 288..370=1
NTFRESH P5 K1=1 K2=1 K3=1 K4=1 K5=1
NTFRESH P5 VERDICT=FRESHCHURN-PASS
NTFRESH OVERALL=FRESHCHURN-PASS-ALL
```

(Full bin lists in `nt_freshchurn_run1.txt`; the ellipses above
compress contiguous =1 runs. Every bin verified against the PREREG
Section 4 trace.)

Prediction vs actual: the kill-bar numbers match at every point.
MAIN nevict 68/128/248 = 3N_n-4 exactly; c 6/6; k 4/4; u 6/6;
forget 0; phev 0; histogram bins exactly as traced (all victims N
subjects, contiguous 123..118+3N_n, each 1). ABL nevict 75/135/255
= 3N_n+3 exactly; c 0/6 (lost, not revised); forget 6/6; k 4/4;
u 6/6; histogram exactly as traced (100=3, 101..104=2, 105=2,
119+N_n=1, 119+2N_n=1, and the three pass-ranges at 1 each).
Histogram bin sums equal the nevict counters at all six arms
(68/75, 128/135, 248/255), confirming the histogram accounts for
every eviction.

Two corrections vs the PREREG text (Amendments 1-2, both pre-verdict):
(1) the histogram base offset bug (4508 -> 5008), caught by an
impossible P5 MAIN histogram before any verdict was drawn, fixed,
rebuilt, re-run; (2) the MAIN npres informational prediction typo
(5 -> 4; the trace's victim list was always correct). Neither
touches a kill bar. See Provenance.

## Kill-bar evaluation (per point)

- K1 (learning intact under capacity): PASS at P2/P3/P5. TTC1 2/2/2,
  probe1 16/16 on both arms at every point. No VOID.
- K2 (eviction minimal, victims confined to N): PASS at P2/P3/P5.
  nevict_main = 68/128/248 = 3N_n-4 (the pigeonhole minimum for
  three passes of N_n fresh insertions into 4 free slots) at each
  point; phev_main = 0 at each point (not one phase-1 subject
  evicted across 444 total MAIN evictions).
- K3 (uncontested retention survives): PASS at P2/P3/P5. k = 4/4,
  u = 6/6 everywhere.
- K4 (revision survives under fresh churn): PASS at P2/P3/P5.
  c_main = 6/6 AND forget_main = 0 at every point. Revision
  completes in pass 3 under full revolving-door churn with zero
  novel-subject re-teaching.
- K5 (the NT2 signature RETURNS): PASS at P2/P3/P5. c_abl = 0 AND
  forget_abl = 6 (the contradicted subjects are lost, not revised)
  AND u_abl = 6 AND nevict_abl = 75/135/255 = 3N_n+3 at each point.
  The churn-dependence account is CONFIRMED; the re-teach-dependence
  alternative is falsified on this skeleton.

## What this establishes

1. **The NT2 failure signature is churn-dependent, not
   re-teach-dependent.** ABL (lowest-net, no checkpoints) loses the
   contradicted subjects whenever the per-pass revolving-door churn
   is reinstated, whether the novel subjects are re-taught
   (NT-PRESSURE) or fresh (here). Mechanism, confirmed by the trace:
   in pass 2 the fresh door evicts the net-0 contradicted subjects
   (101..105) then churns slot 0 through 100; in pass 3 the
   re-inserted contradicted subjects churn slot 0 and are evicted by
   the fresh door before ref can exceed sup. Re-teaching was never
   load-bearing; churn was.
2. **LIFO/D2 victim choice is correct under genuine pressure: the
   sharper "genuinely low-value" boundary holds.** The fresh novel
   subjects are genuinely low-value (taught once, never reinforced,
   never queried). D2 sacrifices exactly them (youngest-first):
   444 MAIN evictions across the three points touch zero phase-1
   subjects, churn sits exactly at the pigeonhole minimum, and
   revision completes in place. There is no dark side at 2x/3x/5x
   per-pass pressure: K1..K4 hold while the apparatus discriminates
   (K5), which the no-reteach regime could not do.
3. **NT-LIFOBOUND's Dimension B is resolved.** The no-reteach
   regime's K5 failure was an apparatus finding (too little churn),
   not a fact about D1+D2. Restore the churn another way and K5
   discrimination returns at all three points. The three-battery
   arc now reads: NT-PRESSURE (re-teach churn; K5 returns),
   NT-LIFOBOUND (no churn; K5 lost; no liability), NT-FRESHCHURN
   (fresh churn; K5 returns; still no liability).
4. **Victim-set moral, replicated a third time.** MAIN's 444
   evictions touch zero phase-1 subjects; ABL's 465 evictions reach
   into the contradicted set at every point (phev_abl=13: subject
   100 in pass 1, 100..105 in passes 2-3). Even the histogram shapes
   discriminate: MAIN's is a flat contiguous block of novel victims
   (each 1); ABL's piles repeated evictions onto the contradicted
   subjects (100=3, 101..105=2).

## Honest boundaries (from PREREG Section 8, unchanged)

- Same skeleton as NT-LIFOBOUND, not a redesign; contlearn2 schema
  machinery and H-CONTLIFE-1 hash-table memory remain unported.
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. Retention/revision/eviction dynamics only.
- The apparatus change (272-entry tables, 8192-byte arena,
  subjects 100..371) is documented in PREREG Section 2(b); it cannot
  affect victim choice (verified: D2 evicts max-ins, ABL evicts
  min-net, regardless of table size; the offset bugfix changed only
  where the histogram is stored).
- Three per-pass pressure points (2x/3x/5x); single contradiction
  magnitude; graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.
- What this does NOT show: whether D1+D2 survives churn where the
  novel subjects are not low-value (e.g. reinforced distractors),
  or churn an order of magnitude larger; the boundary probed here
  is specifically "genuinely low-value" novelty.

## Provenance

- Prereg frozen alone: commit `3f2232b9a` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Amendment 1 (PREREG Section 9): post-freeze implementation bugfix.
  The first build placed the eviction histogram at byte offset 4508,
  overlapping the D1 checkpoint table (which ends at 656+272*16 =
  5008). Caught before any verdict: P5 MAIN emitted an impossible
  histogram (bins like 102=220, an obj value written by ck_set into
  the histogram region; phev=918) while P2/P3 (max novel id below
  the overlap threshold) were clean. Fixed the histogram base to
  5008 (frozen layout; arena used 6096 of 8192 bytes), rebuilt,
  re-ran 3x. No rule, protocol, prediction, or kill-bar change; the
  frozen spec is unchanged. Only post-fix runs count.
- Amendment 2 (PREREG Section 9): corrected the informational MAIN
  npres prediction 5 -> 4 (the Section 4 trace always showed
  119+2N_n evicted in pass 3; the summary count was wrong). Not a
  kill bar; verdict unaffected.
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT-LIFOBOUND/NT-PRESSURE).
  Zero forbidden-executable invocations.
- Source: `nt_freshchurn_full.zag`, written to PREREG Sections 2/3/5
  (NT-LIFOBOUND source with only the frozen fresh-novel protocol
  change, 272-entry tables, kill-bar literals, verdict mapping).
- Build: `znc nt_freshchurn_full.zag -o nt_freshchurn_bin` (exit 0;
  benign zagd-unavailable warning only); 3/3 runs byte-identical
  (cmp), exit 0, zero stderr.
- Audit grep for protection/task-label/importance logic: clean (one
  inherited comment line stating their absence); zero "python" bytes
  in source beyond the `// No Python.` header comment; compiler-defect
  workarounds honored.
- Opaque identifiers: subjects are bare numeric ids 100..371; no
  semantic labels in source, protocol, or output.
- Commits local only, explicit pathspecs, never pushed.
