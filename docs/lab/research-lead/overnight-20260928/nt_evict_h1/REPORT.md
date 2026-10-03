# REPORT: NT-EVICT-H1 (evict by lowest total evidence)

## Verdict

**FAIL** per the frozen verdict mapping (PREREG Section 6). K1, K3, K5
hold; K2 and K4 fail. The directional prediction held (FAIL), but the
frozen NUMERIC predictions did not match: the prereg's hand-trace
missed the revolving-door effect described below. The mechanism section
derives the actual dynamics from the frozen rules and matches the
binary bin-for-bin.

## Frozen results (3/3 byte-identical)

- Run digest: `2337eb2a9d3614ea7ba58af12dd01be7709fcd0b76e5aa667915a5495ebf9a3e`
- Binary digest: `9ffc61c639299f66ad3b63c6de6162d7b0cd752065966f327cada1f24bd6cbf7`
- Source digest: `3886f6a127153a3d4c4121236f525af810b4da75cc5fcfbc44b1ec1c4247effd`

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=18 nevict=40 nentries=30
NT2 ML1 RETEST c_vb=5 nc=6 u=12 forget=1
NT2 ML1 EVHIST 100=4 128=6 134=6 135=6 136=6 137=6 138=5 139=1
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=0 K3=1 K4=0 K5=1
NT2 VERDICT=FAIL
```

Prediction vs actual: nevict 60 -> 40; c_vb 0/6 -> 5/6; forget 6 -> 1;
histogram differs (prereg predicted 100..105=4 each, 128..133=5 each,
134..139=1 each). CONTROL arms, ABLATION arm, nc, u, and the FAIL
verdict direction all matched. The miss is analyzed below; it does not
change the verdict.

## Kill-bar evaluation

- K1 (learning intact under capacity): PASS. TTC 2/2/2, accs 24/24.
- K2 (eviction minimal, no churn): FAIL. nevict_seq = 40, not 6.
- K3 (uncontested retention survives): PASS. NC_OK = 6/6, U_OK = 12/12.
- K4 (revision survives pressure): FAIL -- on a near miss. c_vb = 5/6
  meets the frozen >=5/6 literal, but FORGET = 1 (key 100), so the bar
  fails. Under the assigning worker's stricter 6/6 reading it fails
  outright.
- K5 (discriminative validity): PASS. ML0 shows the pure alias
  signature (u_abl = 0/12, nevict_abl = 0, nalias_abl = 12), distinct
  from ML1's eviction signature (nevict 40 vs 0).

## Actual mechanism (derived from the frozen rules; matches the binary
bin-for-bin)

The prereg trace treated each pass's evictions as one-for-one swaps and
thereby missed the REVOLVING DOOR: once an eviction+insert lands on the
lowest slot index among global-minimum-total entries, the new entry
itself has total=1 = the global minimum, so the NEXT insert in the same
pass evicts it again. Churn concentrates on one slot instead of
spreading. Traced per pass (S = slot):

1. Passes 1-2 (13 evictions): H1 works AS INTENDED. C keys accumulate
   ref (totals 3, then 4) and are never eviction candidates; novel keys
   churn through a revolving door at slot 24 (pass 1 evictions:
   128,134,135,136,137,138; pass 2: 139,128,134,135,136,137,138).
2. Pass 3 (6 evictions): C keys reach ref=3 > sup=2 and REVISE. The
   frozen reset collapses each to (sup=1, ref=0), total=1 -- the global
   minimum, tied with novel keys. Key 100 (slot 0, lowest index) is
   evicted for key 128; the revolving door moves to slot 0, and
   128..133 then 134..137 churn through it. Only ONE C key is lost;
   keys 101..105 survive revision at slots 1..5.
3. Passes 4-6 (7 evictions each): a stable cycle. Key 100 is re-inserted
   fresh each pass at slot 0 (total=1) and evicted again by key 128;
   keys 128 and 134..138 churn through slot 0; keys 101..105 accumulate
   sup safely and are never evicted again; keys 129..133 are NEVER
   evicted in any pass.
4. End state: nevict = 6+7+6+7+7+7 = 40. Key 100 never accumulates
   evidence (re-inserted fresh 4 times, evicted 4 times) and is absent
   at retest: c_vb=5/6, forget=1. accB=18/24 (100, 128, 134..137
   absent).

## What this establishes

1. **H1 does not rescue revision.** The total-evidence comparator
   protects keys DURING revision (passes 1-2, exactly as the rationale
   intended), but the revision reset destroys that protection AT the
   revision moment. The breaking interaction is the evidence RESET
   (sup=1, ref=0), not the comparator per se.
2. **The tie-break is load-bearing, not incidental.** The lowest-slot-
   index tie-break converts what could be diffuse churn into a
   revolving door on one slot, permanently sacrificing exactly the
   lowest-index contested key. A different tie-break would produce
   different dynamics -- but per the no-patch-treadmill rule the
   tie-break is part of the frozen generic rule and is NOT patched
   here; it is reported as a finding.
3. **H1 fails less badly than NT2's rule, but fails.** 40 evictions vs
   41, one key forgotten vs six, five of six revisions completing vs
   zero. The improvement is real but the kill bars are not met: churn
   persists (40 >> 6) and revision does not fully survive (forget=1).
4. **The result strongly motivates H3 (evidence-preserving revision).**
   Both NT2's and H1's pathologies route through the reset: under
   lowest-net it depresses the revising key to the global minimum
   (net=1); under lowest-total the reset collapses it to the global
   minimum (total=1). A revision rule that preserves accumulated
   evidence would keep the revised key ABOVE the minimum under H1's
   comparator -- the compound H1+H3 question is natural follow-up, out
   of scope for this lane.

## Prediction-miss accounting (honest)

The prereg predicted nevict=60, c_vb=0/6, forget=6 via a trace that
assumed one-for-one eviction swaps each pass. The actual binary gives
40/5/6->1. The error: the trace did not propagate the fact that a
freshly inserted entry (total=1) at the lowest tied slot index becomes
the next eviction victim, concentrating churn. The corrected trace
above reproduces all 8 nonzero histogram bins and every aggregate
exactly. The directional verdict (FAIL via K2+K4) is unchanged; no
prereg amendment is needed because the verdict mapping, kill bars, and
rules are untouched -- only the predicted numbers were wrong, and they
are reported as wrong here.

## Honest boundaries (from PREREG Section 7, unchanged)

- ML1/ML0 are minimal surrogates, not TNN's production substrate.
- Memorized key-value mappings; no L2/L3 claim.
- Single capacity point (CAP=30, 1.2x); single contradiction
  magnitude; scaling and graded contradiction out of scope.
- The eviction histogram is measurement-only instrumentation.
- H2 (recency-weighted) and H3 (evidence-preserving revision), and any
  H1+H3 compound, are separate hypotheses, not tested here.

## Provenance

- Prereg frozen alone: commit `5cbda988a` (PREREG.md + NAMECHECK.md
  only), strictly before implementation.
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev. Zero forbidden-executable invocations.
- Source: `nt_h1_full.zag`, transcribed from NT2's `nt2_full.zag`
  with the single functional change (eviction comparator sup-ref ->
  sup+ref; fn renamed `nt_evict_lowest` -> `nt_evict_total`). Diff
  against NT2 source verified: only header comment, fn
  comment/name, comparator, and call site differ.
- Build: `znc nt_h1_full.zag -o h1_bin` (exit 0; benign
  zagd-unavailable warning only); 3/3 runs byte-identical (cmp).
- Commits local only, explicit pathspecs, never pushed.
