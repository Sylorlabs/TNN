# REPORT: NT-D2 -- D1 preserve-evidence + evict-youngest (LIFO) comparator

## Verdict

**PASS** per the frozen verdict mapping (PREREG Section 8). K1, K2,
K3, K4, K5 all hold. This is the preregistered directional prediction
(PASS), and -- unlike every predecessor lane -- EVERY frozen numeric
prediction matched exactly, including the full 7-bin eviction
histogram. First PASS in the NT series: the NT1 selective-retention
principle survives capacity pressure with D1's preserve-evidence and
D2's staleness-blind comparator combined.

## Frozen results (3/3 byte-identical)

- Run digest: `3c647247dd423ad58cb42a67f77145488a479df98edd06b8938be904213c621b`
- Binary digest: `a9e4e9a7d23e6092641e2aebe0b223acc6b35a78167a2aced9a3ee7d58e966c2`
- Source digest: `e7777572b5c7516b551d40c032153771e8e38c060b5388a8226cf770eac96e91`

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=18 nevict=41 nentries=30
NT2 ML1 RETEST c_vb=6 nc=6 u=12 forget=0
NT2 ML1 EVHIST 133=6 134=6 135=6 136=6 137=6 138=6 139=5
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=1 K3=1 K4=1 K5=1
NT2 VERDICT=PASS
```

Prediction vs actual: NO misses. nevict 41 = 41; c_vb 6/6; nc 6/6;
u 12/12; forget 0; accB 18/24; histogram bins 133=6, 134=6, 135=6,
136=6, 137=6, 138=6, 139=5 with all other keys (in particular all of
100..123) at 0; CONTROL arms, ABLATION arm, and every kill bar as
frozen. The prereg's hand-trace (Section 6) reproduced the binary
exactly, bin for bin.

## Kill-bar evaluation (forget regime stated explicitly)

- K1 (learning intact under capacity): PASS. TTC 2/2/2, accs 24/24.
  Capacity itself does not break learning; no VOID.
- K2 (eviction minimal, no churn, FORGET = 0 regime): PASS.
  nevict_seq = 41 = the frozen D2 minimum (36 pigeonhole lower bound
  under FORGET = 0, +5 traced revolving-door overhead among novel
  keys). All 41 victims are novel keys (128..139); zero A-keys
  evicted in any pass.
- K3 (uncontested retention survives): PASS. NC_OK = 6/6, U_OK =
  12/12. Untouched keys are never eviction candidates: staleness is
  protective under LIFO, never punished.
- K4 (revision survives pressure, FORGET = 0 regime): PASS. C_VB =
  6/6 (revision completes: ref accumulates across eviction boundaries
  via D1 restore, fires in pass 3) AND FORGET = 0.
- K5 (discriminative validity): PASS. ML0 shows the pure alias
  signature (u_abl = 0/12, nevict_abl = 0, nalias_abl = 12),
  distinct from ML1's eviction signature (nevict 41 vs 0).

## What this establishes

1. **The NT1 principle survives capacity pressure with both fixes.**
   D1 alone fixed revision but relocated forgetting to untouched keys
   (comparator punished staleness); D2's comparator fixes the
   relocation without touching D1's restore. Revision completes
   (6/6), nothing is forgotten that the table could keep (FORGET =
   0), and evictions are at the traced minimum (41 = 36 forced + 5
   forget-free door overhead). The breaking interaction chain
   NT2 -> H1 -> H3 -> D1 -> D2 is now closed: each failure's
   diagnosed cause was addressed by the next hypothesis, and the
   final combination passes.
2. **The necessity argument (PREREG 1.1) is empirically corroborated.**
   No pure-(sup,ref) comparator could satisfy the three requirements
   (untouched IDENTICAL to reinforced-novel; revised IDENTICAL to new
   after the reset); the temporal signal was required, and the
   battery confirms age aligns with the right victims with zero
   prediction misses. FIFO would be the anti-D2; LIFO is the unique
   temporal comparator meeting the brief.
3. **Protection without protection rules.** Contested keys are never
   evicted, yet the implementation contains no protection flag, no
   task identity, no "don't evict" logic of any kind -- only
   installation order. The comparator is as generic as the
   lowest-net rule it replaces. The revision reset is invisible to
   it (it does not touch `ins`), which is why H1's reset-moment
   failure mode cannot recur here.
4. **Five hypotheses, five clean signatures, one apparatus.**
   NT2: 41 evictions, c_vb=0/6, forget=6 (contradicted keys).
   H1: 40, c_vb=5/6, forget=1 (revolving door). H3: null
   (byte-identical to NT2). D1: 32, c_vb=6/6, forget=6 (untouched
   keys 112..117). D2: 41, c_vb=6/6, forget=0. D2 is the only PASS,
   and its signature (same count as NT2's 41, opposite outcome) shows
   the count was never the right measure -- the victim SET is.
5. **The revolving door is benign when the victims are right.** D2
   exhibits the same door H1 and D1 found (one slot per pass absorbs
   the churn), but confined to novel keys re-taught every pass, it
   costs only re-insertions, never forgetting. Churn != pathology;
   pathology = churning the entries current experience is about
   (NT2) or the entries nothing will ever re-teach (D1).

## Honest boundaries (from PREREG Section 10, unchanged)

- ML1/ML0 are minimal surrogates, not TNN's production substrate.
  This PASS characterizes the D1+D2 rule-set under pressure; it does
  not show TNN-as-built is robust.
- Families are memorized key-value mappings; no L2/L3 claim. The
  experiment measures retention/revision/eviction dynamics only.
- Single capacity point (CAP=30, 1.2x over capacity); single
  contradiction magnitude; pressure-ratio scaling and graded
  contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  and `ins` are learner state (own prior evidence / own installation
  order), containing no oracle/task information.
- LIFO was selected by the preregistered necessity argument, not by
  fitting the battery; the exact-match predictions are what the
  battery checked. Whether LIFO's "tenure = established claim"
  principle generalizes (e.g. novel keys NOT re-taught every pass)
  is preregistered follow-up, not established here.

## Recommended follow-up (preregistered, PREREG Section 9)

- Port D1+D2 to the shared continuing-learner substrate.
- Scale the pressure ratio (1.2x -> higher) with the same bars and
  the forget regime stated explicitly.
- Probe the "genuinely low-value" criterion's boundary: novel keys
  NOT re-taught every pass -- does LIFO still pick the right
  victims, or does tenure-protection become a liability?

## Provenance

- Prereg frozen alone: commit `6679be8f3` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT2/H1/H3/D1). Zero
  forbidden-executable invocations.
- Source: `nt_d2_full.zag`, transcribed from D1's `nt_d1_full.zag`
  with ONLY the PREREG Section 2.1 change sites (header/layout,
  sk/sp stride 16->20 + ck 652->772 + evhist 492->616, nt_evict_lowest
  -> nt_evict_youngest, nt_insert ins stamp, call site, K2 literal
  36->41). `diff` verified. One self-caught arena-layout bug fixed
  pre-build (ins_seq first placed at 1412, inside the checkpoint
  table's 776..1415 range; moved to 1416 before compiling -- the
  frozen binary was built only from the corrected source).
- Build: `znc nt_d2_full.zag -o nt_d2_bin` (exit 0; benign
  zagd-unavailable warning only); 3/3 runs byte-identical (cmp).
- Commits local only, explicit pathspecs, never pushed.
