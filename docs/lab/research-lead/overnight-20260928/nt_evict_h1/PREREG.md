# PREREG: NT-EVICT-H1 -- Evict by Lowest TOTAL Evidence (sup+ref)

## 1. Question

NT2 (NT-CAPACITY, FAIL per frozen bars, ledger C407) proved that under
capacity pressure the generic lowest-net (sup-ref) eviction rule
preempts revision: contradicted keys accumulate ref, depressing net to
1, tie with just-inserted novel keys, and are evicted mid-revision by
the slot-index tie-break (nevict=41 vs forced minimum 6; c_vb=0/6;
forget=6). NT2's Section 9 preregistered three separate hypotheses to
test whether ANY generic non-protective eviction policy preserves
revision under pressure; each requires its own prereg and kill bars.

This lane tests H1: evict by lowest TOTAL evidence (sup+ref) instead of
lowest NET (sup-ref).

H1 rationale (preregistered in NT2 Section 9): a key under active
revision has HIGH total evidence (it is being contested: sup and ref
both accumulate), so total-evidence eviction should protect it; a
just-inserted novel key has LOW total evidence (sup=1, ref=0), so it is
the right eviction candidate. If H1 works, the NT1 selective-retention
principle survives capacity pressure with the right eviction rule.

## 2. The H1 rule (precise specification; the ONLY change)

Eviction rule (replaces NT2 PREREG Section 2.1's rule verbatim): if the
table is full, evict the slot with globally lowest (sup + ref); ties
resolve to the lowest slot index.

The rule remains generic and domain-neutral: it operates only on
entry-local evidence counters (sup, ref); no task identity, no
importance flags, no protection, no modes, no researcher-supplied
"don't forget" logic. The tie-break is unchanged from NT2.

Minimal-change commitment: the implementation is NT2's `nt2_full.zag`
transcribed verbatim with exactly one functional change -- the eviction
comparator `sk(L,s,2)-sk(L,s,3)` becomes `sk(L,s,2)+sk(L,s,3)`
(function renamed `nt_evict_lowest` -> `nt_evict_total` for clarity;
call site updated). No other source line changes in meaning.

## 3. Frozen machinery (NT2 verbatim; see NT2 PREREG Sections 2-4)

- Learner state: slot table, 30 slots of (key, value, sup, ref).
- `nt_learn` update rule: NT1's rule verbatim, INCLUDING the revision
  reset: on contradiction ref++; if ref > sup, REVISE the slot to
  (key, new value, sup=1, ref=0). This reset is part of the frozen
  machinery for H1; only the eviction comparator changes.
- ML1 (treatment): associative dedicated addressing; ML0 (negative
  control): NT1's overlapping map verbatim; `arm` selector in harness.
- Families: keys 100..139, VA/VB oracles, SET_A/SET_B, C/NC/U
  partitions -- NT2 Section 3 verbatim. Opaque identifiers only.
- Protocol: CONTROL-A, CONTROL-B, SEQ (6 fixed B passes), ABLATION --
  NT2 Section 4 verbatim, including the frozen "correct eviction"
  definition (nevict == 6 forced minimum, revision completes,
  FORGET = 0).
- Build/run: single source `nt_h1_full.zag`, `znc nt_h1_full.zag -o
  h1_bin` under safebin-only PATH, 3 runs, byte-identical (cmp),
  sha256 recorded. Compiler-defect workarounds per AGENTS.md
  (mandatory, transcribed with the source).

## 4. Frozen predictions (hand-derived by tracing the frozen rules
under the H1 comparator; two independent traces)

- CONTROL-A: TTC_A_ctrl = 2, acc = 24/24, nevict = 0.
- CONTROL-B: TTC_B_ctrl = 2, pc = 1, acc = 24/24, nevict = 0.
- SEQ: TTC_A_seq = 2; phase-A probe 24/24; after 6 B passes,
  accB = 18/24 (C 0/6, NC 6/6, novel 12/12); nevict = 60, nentries = 30.
- SEQ retest: C_VB = 0/6, NC_OK = 6/6, U_OK = 12/12, FORGET = 6.
- SEQ eviction histogram (nonzero bins only): 100=4, 101=4, 102=4,
  103=4, 104=4, 105=4, 128=5, 129=5, 130=5, 131=5, 132=5, 133=5,
  134=1, 135=1, 136=1, 137=1, 138=1, 139=1; all other keys 0.
- ABLATION (ML0): identical to NT2 (eviction rule never fires for ML0):
  TTC_A_abl = 2; accB_abl = 24/24; nevict_abl = 0; nalias_abl = 12;
  nentries_abl = 24; retest C_VB = 6/6, NC_OK = 6/6, U_OK = 0/12,
  FORGET_abl = 12.

### Predicted mechanism (directional prediction: FAIL)

The H1 rationale is correct DURING revision but fails AT revision,
because of the frozen revision reset. Traced:

1. B passes 1-2: C keys accumulate ref (sup=2, ref=1 then ref=2; total
   3 then 4) and are never eviction candidates; novel keys (total=1)
   evict each other within each pass (6 evictions in pass 1, 12 in
   pass 2). H1 protects revising keys exactly as intended -- so far.
2. B pass 3: C keys reach ref=3 > sup=2 and REVISE. The frozen reset
   collapses the slot to (key, new value, sup=1, ref=0): total=1 --
   the global minimum, tied with the incoming novel keys.
3. The unchanged tie-break (lowest slot index) then evicts the
   JUST-REVISED C keys (slots 0..5) to make room for novel keys
   128..133. From pass 3 on, each pass evicts the C keys and the
   novel keys alternately (12 evictions/pass in passes 4-6; 6 in
   pass 3).
4. Net: nevict = 6+12+6+12+12+12 = 60 -- WORSE than NT2's 41. The
   churn is a stable cycle, not a transient; a stable all-24-B-keys
   assignment exists and is never found.

Predicted verdict: FAIL (K1, K3, K5 hold; K2, K4 fail). H1 does not
rescue revision; it relocates the pathology from "revision depresses
net evidence" (NT2) to "the revision reset collapses total evidence".
The interaction that breaks it is the evidence RESET, not the
comparator per se -- a strong pointer toward H3 (evidence-preserving
revision) and toward the compound H1+H3 question, neither of which is
tested in this lane.

## 5. Frozen kill bars (NT2 Section 7 verbatim; machinery frozen)

- K1 (learning intact under capacity; else VOID): TTC_A_ctrl in 1..50
  AND acc 24/24; TTC_B_ctrl in 1..50 AND acc 24/24; TTC_A_seq in 1..50
  AND accA 24/24. Else VOID.
- K2 (eviction minimal, no churn): nevict_seq == 6.
- K3 (uncontested retention survives): SEQ retest NC_OK = 6/6 AND
  U_OK = 12/12.
- K4 (revision survives pressure): SEQ retest C_VB >= 5/6 AND
  FORGET = 0 across all 24 A keys. (The assigning worker stated the
  bar as c_vb=6/6; the frozen NT2 literal is >=5/6. Both are evaluated
  and reported; the predicted 0/6 fails either.)
- K5 (discriminative validity): ML0 ABLATION shows the pure alias
  signature (U_OK_abl = 0/12 AND nevict_abl = 0 AND nalias_abl = 12)
  AND ML1's signature differs (nevict_seq != nevict_abl). Else
  INCONCLUSIVE, never PASS.

## 6. Verdict mapping (frozen; NT2 Section 8 verbatim)

- K1..K5 all hold: PASS -- the NT1 principle survives capacity
  pressure under the H1 eviction rule.
- K1 fails: VOID -- redesign.
- K1 holds, K5 fails: INCONCLUSIVE.
- K2 or K4 fail (K1, K3, K5 hold): FAIL -- H1 does not preserve
  revision under pressure; report failed bars with the mechanism.

## 7. Honest boundaries (NT2 Section 10 verbatim, unchanged)

- ML1/ML0 are minimal surrogates for the principle under test, not
  TNN's production memory substrate.
- Families are memorized key-value mappings; no L2/L3 claim.
- Single capacity point (CAP=30, 1.2x over capacity); single
  contradiction magnitude; pressure-ratio scaling and graded
  contradiction out of scope.
- The eviction histogram is measurement-only instrumentation.
- H2 (recency-weighted eviction) and H3 (evidence-preserving revision)
  are separate preregistered hypotheses, not implemented here. The
  predicted H1 failure mechanism explicitly motivates H3; no compound
  H1+H3 policy is tested in this lane.

## 8. Amendment record

(none at freeze)
