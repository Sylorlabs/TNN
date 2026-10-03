# REPORT: NT-PRESSURE -- D1+D2 pressure envelope to 5x

## Verdict

**PORT-PASS-ALL** per the frozen verdict mapping (PREREG Section 7).
K1..K5 hold at P2 (2x), P3 (3x), and P5 (5x). This is the preregistered
directional prediction, and -- like NT-D2 and NT-PORT before it --
EVERY frozen numeric prediction matched exactly, including all six
eviction histograms (3 MAIN, 3 ABL), bin for bin.

## Frozen results (3/3 byte-identical)

- Run digest: `32a86ab3c9d7abb83afcb19c734faeae93522046aef97da3eb1588f7749404fa`
- Binary digest: `d3ed9f614629f4be39088ff1c98608bd0c839d6384da77f5a3657aa47a53dfeb`
- Source digest: `f9282b55a4f8d6744bd4522fc6aed6552e8ecfa4a6723caf49eb615a2db2a8ec`

```
NTPRES P2 MAIN ttc=2 probe1=16 nevict=62
NTPRES P2 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTPRES P2 MAIN EVHIST 123=3 124=3 125=3 126=3 127=3 128=3 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=2
NTPRES P2 ABL ttc=2 probe1=16 nevict=62
NTPRES P2 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTPRES P2 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 124=1 125=1 126=1 127=1 128=1 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=2
NTPRES P2 K1=1 K2=1 K3=1 K4=1 K5=1
NTPRES P2 VERDICT=PORT-PASS
NTPRES P3 MAIN ttc=2 probe1=16 nevict=122
NTPRES P3 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTPRES P3 MAIN EVHIST 123=3 124=3 125=3 126=3 127=3 128=3 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=3 144=3 145=3 146=3 147=3 148=3 149=3 150=3 151=3 152=3 153=3 154=3 155=3 156=3 157=3 158=3 159=3 160=3 161=3 162=3 163=2
NTPRES P3 ABL ttc=2 probe1=16 nevict=122
NTPRES P3 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTPRES P3 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 124=1 125=1 126=1 127=1 128=1 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=3 144=3 145=3 146=3 147=3 148=3 149=3 150=3 151=3 152=3 153=3 154=3 155=3 156=3 157=3 158=3 159=3 160=3 161=3 162=3 163=2
NTPRES P3 K1=1 K2=1 K3=1 K4=1 K5=1
NTPRES P3 VERDICT=PORT-PASS
NTPRES P5 MAIN ttc=2 probe1=16 nevict=242
NTPRES P5 MAIN RET c=6 k=4 u=6 npres=4 forget=0 phev=0
NTPRES P5 MAIN EVHIST 123=3 124=3 125=3 126=3 127=3 128=3 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=3 144=3 145=3 146=3 147=3 148=3 149=3 150=3 151=3 152=3 153=3 154=3 155=3 156=3 157=3 158=3 159=3 160=3 161=3 162=3 163=3 164=3 165=3 166=3 167=3 168=3 169=3 170=3 171=3 172=3 173=3 174=3 175=3 176=3 177=3 178=3 179=3 180=3 181=3 182=3 183=3 184=3 185=3 186=3 187=3 188=3 189=3 190=3 191=3 192=3 193=3 194=3 195=3 196=3 197=3 198=3 199=3 200=3 201=3 202=3 203=2
NTPRES P5 ABL ttc=2 probe1=16 nevict=242
NTPRES P5 ABL RET c=0 k=4 u=6 npres=10 forget=6 phev=13
NTPRES P5 ABL EVHIST 100=3 101=2 102=2 103=2 104=2 105=2 124=1 125=1 126=1 127=1 128=1 129=3 130=3 131=3 132=3 133=3 134=3 135=3 136=3 137=3 138=3 139=3 140=3 141=3 142=3 143=3 144=3 145=3 146=3 147=3 148=3 149=3 150=3 151=3 152=3 153=3 154=3 155=3 156=3 157=3 158=3 159=3 160=3 161=3 162=3 163=3 164=3 165=3 166=3 167=3 168=3 169=3 170=3 171=3 172=3 173=3 174=3 175=3 176=3 177=3 178=3 179=3 180=3 181=3 182=3 183=3 184=3 185=3 186=3 187=3 188=3 189=3 190=3 191=3 192=3 193=3 194=3 195=3 196=3 197=3 198=3 199=3 200=3 201=3 202=3 203=2
NTPRES P5 K1=1 K2=1 K3=1 K4=1 K5=1
NTPRES P5 VERDICT=PORT-PASS
NTPRES OVERALL=PORT-PASS-ALL
```

Prediction vs actual: NO misses at any pressure point. MAIN nevict
62/122/242 = 3*N_n-10 exactly; c 6/6; k 4/4; u 6/6; forget 0;
phev 0 (zero phase-1 subjects evicted at any pressure); histogram
bins exactly as traced (all victims N subjects: 123..142=3/143=2 at
P2; 123..162=3/163=2 at P3; 123..202=3/203=2 at P5). ABL nevict
62/122/242 = same count as MAIN, opposite victim set; c 0/6;
forget 6; u 6/6; npres 10/10; histogram exactly as traced
(100=3, 101..105=2, 124..128=1, last-N=2, 129..rest=3).

## Kill-bar evaluation (forget regime stated explicitly, per point)

- K1 (learning intact under capacity): PASS at P2/P3/P5. TTC1 2/2/2,
  probe1 16/16 on both arms at every point. No VOID.
- K2 (eviction minimal, no churn, victims confined to N): PASS at
  P2/P3/P5. nevict_main = 62/122/242 = the frozen port minimum
  (3*N_n-10) at each point; phev_main = 0 at each point (not one
  phase-1 subject evicted across 426 total MAIN evictions).
- K3 (uncontested retention survives): PASS at P2/P3/P5. K_OK = 4/4,
  U_OK = 6/6 everywhere.
- K4 (revision survives pressure): PASS at P2/P3/P5. C_VB = 6/6 AND
  FORGET = 0 at every point. Revision completes in pass 3 at 5x
  exactly as at 1.3x.
- K5 (discriminative validity): PASS at P2/P3/P5. The ABL arm
  reproduces the NT2 failure signature at each point (c_vb_abl = 0/6,
  forget_abl = 6, u_abl = 6/6, nevict_abl = 62/122/242), sharply
  distinct from MAIN's signature (same counts, opposite victim
  sets). The apparatus discriminates at every probed pressure.

## What this establishes

1. **D1+D2 does not break by 5x.** The key questions are answered:
   FORGET stays 0 at 2x/3x/5x; revision stays 6/6 at 2x/3x/5x;
   eviction stays at the traced minimum with the victim set confined
   to re-taught novel subjects. The measured breaking point lies
   beyond the probed envelope.
2. **The tenure structure is scale-invariant in novelty load.** The
   mechanism that protected D1+D2 at 1.3x (C/K/U older than every N
   subject by construction; D1 restore invisible to the D2
   comparator; churn concentrated on re-taught N subjects) does not
   degrade as N grows from 10 to 84 subjects. The only
   N_n-dependent quantities are the eviction count (3*N_n-10, at the
   pigeonhole lower bound + 2 traced overhead) and the histogram
   width; every bar-relevant quantity is invariant.
3. **The victim-set moral replicates at scale.** MAIN and ABL evict
   62/122/242 times respectively at P2/P3/P5 -- identical counts
   within each point, opposite victim sets across arms. At 5x, ABL's
   242 evictions include all six contradicted subjects (phev_abl =
   13: 100x3 + 101..105x2); MAIN's 242 evictions touch zero phase-1
   subjects. The count was never the measure; the victim set is --
   at 5x as at 1.3x.
4. **Protection without protection rules, at 5x.** No phase-1 subject
   is evicted in MAIN at any pressure point, yet the implementation
   contains no protection flag, no task identity, no importance
   logic -- only installation order (audit grep clean).

## Honest boundaries (from PREREG Section 8, unchanged)

- Same skeleton as NT-PORT, not a redesign; contlearn2 schema
  machinery and H-CONTLIFE-1 hash-table memory remain unported.
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. Retention/revision/eviction dynamics only.
- Three capacity points (2x/3x/5x); single contradiction magnitude;
  graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.
- Whether LIFO's tenure principle holds when novel subjects are NOT
  re-taught every pass remains the preregistered open boundary, NOT
  tested here.

## Recommended follow-up (preregistered, PREREG Section 8/NT-PORT)

- Probe the "genuinely low-value" boundary: novel subjects NOT
  re-taught every pass -- does LIFO still pick the right victims, or
  does tenure-protection become a liability? (preregistered open
  boundary; the natural next lane)
- Push beyond 5x toward the actual breaking point, or probe the
  interaction with schema discovery/retire on the contlearn2
  substrate.

## Provenance

- Prereg frozen alone: commit `a27e484e4` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT-PORT/NT2/H1/H3/D1/D2).
  Zero forbidden-executable invocations.
- Source: `nt_pressure_full.zag`, written to PREREG Sections 2/3
  (NT-PORT source with only the frozen scaled-inventory changes).
- Build: `znc nt_pressure_full.zag -o nt_pressure_bin` (exit 0;
  benign zagd-unavailable warning only); 3/3 runs byte-identical
  (cmp), exit 0, zero stderr.
- Audit grep for protection/task-label/importance logic: clean; zero
  "python" bytes; compiler-defect workarounds honored.
- Commits local only, explicit pathspecs, never pushed.
