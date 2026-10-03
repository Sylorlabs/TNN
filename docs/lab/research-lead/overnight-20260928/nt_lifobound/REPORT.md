# REPORT: NT-LIFOBOUND -- The LIFO boundary: novel subjects NOT re-taught

## Verdict

**INCONCLUSIVE** at P2 (2x), P3 (3x), and P5 (5x), per the frozen
verdict mapping (PREREG Section 7). This is the preregistered
directional prediction, and -- like NT-PORT and NT-PRESSURE before
it -- EVERY frozen numeric prediction matched exactly, including all
six eviction histograms (3 MAIN, 3 ABL), bin for bin.

The verdict separates into the two preregistered dimensions:

- **Dimension A (the liability question): NO LIABILITY FOUND.**
  K1..K4 hold at all three points. Revision completes without any
  re-teaching (c_main=6/6), FORGET stays 0, eviction churn is at the
  pigeonhole minimum (nevict_main = N_n-4: 20/40/80) with the victim
  set confined to novel subjects, and zero phase-1 subjects are
  evicted in MAIN (phev_main=0) across 140 total MAIN evictions. The
  once-taught novel subjects do NOT become permanent residents that
  block revision: revision is in-place via the frozen evidence
  update (never needs a slot), and the surviving novel subjects
  remain eviction-eligible (youngest-first under D2). None of the
  INFORMATIVE-FAIL triggers fired. LIFO's tenure-protection is not a
  liability in the no-reteach regime.
- **Dimension B (discriminative validity): NOT ACHIEVED.**
  K5 fails at all three points: the ABL arm revises the contradicted
  subjects successfully (c_abl=6/6, forget_abl=0, nevict_abl=N_n-3:
  21/41/81) instead of reproducing the NT2 failure signature
  (c=0, forget=6). The NT2 signature is churn-dependent: in
  NT-PRESSURE the re-taught novel subjects' revolving door kept
  evicting ABL's contradicted subjects (net 0) before ref could
  exceed sup; without re-teach churn, even lowest-net eviction with
  no checkpoints completes revision. The no-reteach regime is too
  easy to discriminate fragility modes. That is an apparatus
  finding, not a D1+D2 finding.

## Frozen results (3/3 byte-identical)

- Run digest: `c983f0dd071f3c5f97e2bb34b35428fb124d1a7ed582aad52f8d8f5d2dba39d7`
- Binary digest: `6713b635b9cd0e6b5ce63f83496964f91642f8ac06aca687dd1e204c485a2766`
- Source digest: `eee16fe6c338ba0cbebda1cdb76c51ca4a242f4ec20704687f7a0beb52f1df0d`

```
NTLIFO P2 MAIN ttc=2 probe1=16 nevict=20
NTLIFO P2 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTLIFO P2 MAIN EVHIST 123=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1
NTLIFO P2 ABL ttc=2 probe1=16 nevict=21
NTLIFO P2 ABL RET c=6 k=4 u=6 npres=4 forget=0 phev=1
NTLIFO P2 ABL EVHIST 100=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1 143=1
NTLIFO P2 K1=1 K2=1 K3=1 K4=1 K5=0
NTLIFO P2 VERDICT=INCONCLUSIVE
NTLIFO P3 MAIN ttc=2 probe1=16 nevict=40
NTLIFO P3 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTLIFO P3 MAIN EVHIST 123=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1 143=1 144=1 145=1 146=1 147=1 148=1 149=1 150=1 151=1 152=1 153=1 154=1 155=1 156=1 157=1 158=1 159=1 160=1 161=1 162=1
NTLIFO P3 ABL ttc=2 probe1=16 nevict=41
NTLIFO P3 ABL RET c=6 k=4 u=6 npres=4 forget=0 phev=1
NTLIFO P3 ABL EVHIST 100=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1 143=1 144=1 145=1 146=1 147=1 148=1 149=1 150=1 151=1 152=1 153=1 154=1 155=1 156=1 157=1 158=1 159=1 160=1 161=1 162=1 163=1
NTLIFO P3 K1=1 K2=1 K3=1 K4=1 K5=0
NTLIFO P3 VERDICT=INCONCLUSIVE
NTLIFO P5 MAIN ttc=2 probe1=16 nevict=80
NTLIFO P5 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTLIFO P5 MAIN EVHIST 123=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1 143=1 144=1 145=1 146=1 147=1 148=1 149=1 150=1 151=1 152=1 153=1 154=1 155=1 156=1 157=1 158=1 159=1 160=1 161=1 162=1 163=1 164=1 165=1 166=1 167=1 168=1 169=1 170=1 171=1 172=1 173=1 174=1 175=1 176=1 177=1 178=1 179=1 180=1 181=1 182=1 183=1 184=1 185=1 186=1 187=1 188=1 189=1 190=1 191=1 192=1 193=1 194=1 195=1 196=1 197=1 198=1 199=1 200=1 201=1 202=1
NTLIFO P5 ABL ttc=2 probe1=16 nevict=81
NTLIFO P5 ABL RET c=6 k=4 u=6 npres=4 forget=0 phev=1
NTLIFO P5 ABL EVHIST 100=1 124=1 125=1 126=1 127=1 128=1 129=1 130=1 131=1 132=1 133=1 134=1 135=1 136=1 137=1 138=1 139=1 140=1 141=1 142=1 143=1 144=1 145=1 146=1 147=1 148=1 149=1 150=1 151=1 152=1 153=1 154=1 155=1 156=1 157=1 158=1 159=1 160=1 161=1 162=1 163=1 164=1 165=1 166=1 167=1 168=1 169=1 170=1 171=1 172=1 173=1 174=1 175=1 176=1 177=1 178=1 179=1 180=1 181=1 182=1 183=1 184=1 185=1 186=1 187=1 188=1 189=1 190=1 191=1 192=1 193=1 194=1 195=1 196=1 197=1 198=1 199=1 200=1 201=1 202=1 203=1
NTLIFO P5 K1=1 K2=1 K3=1 K4=1 K5=0
NTLIFO P5 VERDICT=INCONCLUSIVE
NTLIFO OVERALL=INCONCLUSIVE
```

Prediction vs actual: NO misses at any pressure point. MAIN nevict
20/40/80 = N_n-4 exactly; c 6/6; k 4/4; u 6/6; forget 0; phev 0;
histogram bins exactly as traced (all victims N subjects,
123..142/162/202 = 1 each). ABL nevict 21/41/81 = N_n-3 exactly;
c 6/6 (revised, not lost); forget 0; phev 1 (subject 100 evicted in
pass 1); histogram exactly as traced (100=1, 124..143/163/203=1).

## Kill-bar evaluation (per point)

- K1 (learning intact under capacity): PASS at P2/P3/P5. TTC1 2/2/2,
  probe1 16/16 on both arms at every point. No VOID.
- K2 (eviction minimal, no churn, victims confined to N): PASS at
  P2/P3/P5. nevict_main = 20/40/80 = N_n-4 (the pigeonhole minimum
  for the no-reteach regime) at each point; phev_main = 0 at each
  point (not one phase-1 subject evicted across 140 total MAIN
  evictions).
- K3 (uncontested retention survives): PASS at P2/P3/P5. k = 4/4,
  u = 6/6 everywhere.
- K4 (revision survives without re-teaching): PASS at P2/P3/P5.
  c_main = 6/6 AND forget_main = 0 at every point. Revision
  completes in pass 3 with zero novel-subject re-teaching.
- K5 (discriminative validity): FAIL at P2/P3/P5, as predicted. The
  ABL arm does not reproduce the NT2 failure signature: c_abl = 6
  (not 0), forget_abl = 0 (not 6), nevict_abl = N_n-3 (not
  3N_n-10). Per the frozen mapping this yields INCONCLUSIVE, never
  PASS, at each point.

## What this establishes

1. **LIFO's tenure-protection is not a liability when novel subjects
   are not re-taught.** The liability hypothesis -- once-taught
   novel subjects become permanent residents that block revision of
   contradicted entries -- is falsified on this skeleton at
   2x/3x/5x. Mechanism, confirmed by the trace: revision is in-place
   via the frozen evidence update and never requires a slot, so no
   resident can block it; the surviving once-taught novel subjects
   (120,121,122,119+N_n) are eviction-eligible (youngest-first under
   D2), not permanent. Tenure protects the phase-1 subjects (the
   reinforced, high-value entries) while the genuinely low-value
   once-taught novel subjects absorb 100% of the (minimal) churn.
2. **The NT2 failure signature is churn-dependent, not a pure
   function of the eviction rule.** ABL (lowest-net, no checkpoints)
   loses contradicted subjects only when the churn of re-taught
   novel subjects keeps evicting them (net 0) before ref exceeds
   sup. Remove the churn and ABL revises 6/6 with FORGET=0. This
   reframes NT-PRESSURE's K5: the discrimination there measured
   churn-fragility, and the no-reteach regime is below the churn
   threshold at which the two rules diverge.
3. **The no-reteach regime is strictly easier than the re-teach
   regime for both arms.** MAIN churn drops from 3N_n-10 to N_n-4;
   ABL churn drops from 3N_n-10 to N_n-3 and its retention failure
   disappears. Any future probe that wants K5 discrimination without
   re-teaching must restore churn another way (see below).
4. **Victim-set moral, replicated.** MAIN's 140 evictions touch zero
   phase-1 subjects; ABL's 143 evictions include subject 100
   (phev_abl=1 at every point). Even where ABL revises successfully,
   its victim set still reaches into the contradicted set while
   MAIN's never does.

## Honest boundaries (from PREREG Section 8, unchanged)

- Same skeleton as NT-PRESSURE, not a redesign; contlearn2 schema
  machinery and H-CONTLIFE-1 hash-table memory remain unported.
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. Retention/revision/eviction dynamics only.
- The INCONCLUSIVE verdict is the honest limit of this probe: it
  answers the liability question (no) but cannot discriminate
  fragility modes in this regime (K5). It is not a PASS and is not
  presented as one.
- Three capacity points (2x/3x/5x); single contradiction magnitude;
  graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.

## Recommended follow-up (preregistered, PREREG Section 8)

- Restore churn WITHOUT re-teaching: supply FRESH novel subjects
  each pass (each taught once). This keeps "taught once" while
  reinstating the revolving-door pressure that produced ABL's NT2
  signature; if the churn-dependence account is correct, K5
  discrimination should return while MAIN keeps K1..K4. That probe
  would test LIFO victim-choice under genuine pressure -- the
  sharper form of the "genuinely low-value" boundary.

## Provenance

- Prereg frozen alone: commit `8998c14a1` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT-PRESSURE/NT-PORT/NT2).
  Zero forbidden-executable invocations.
- Source: `nt_lifobound_full.zag`, written to PREREG Sections 2/3/5
  (NT-PRESSURE source with only the frozen no-reteach protocol
  change, kill-bar literals, and verdict mapping).
- Build: `znc nt_lifobound_full.zag -o nt_lifobound_bin` (exit 0;
  benign zagd-unavailable warning only); 3/3 runs byte-identical
  (cmp), exit 0, zero stderr.
- Audit grep for protection/task-label/importance logic: clean (one
  inherited comment line stating their absence); zero "python" bytes
  in source; compiler-defect workarounds honored.
- Opaque identifiers: subjects are bare numeric ids 100..203; no
  semantic labels in source, protocol, or output.
- Commits local only, explicit pathspecs, never pushed.
