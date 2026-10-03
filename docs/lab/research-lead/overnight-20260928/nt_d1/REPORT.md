# REPORT: NT-D1 -- preserve evidence across eviction/re-insertion

## Verdict

**FAIL** per the frozen verdict mapping (PREREG Section 8). K1 and K5
hold; K2, K3, K4 fail. The directional prediction held (FAIL), but the
frozen NUMERIC predictions did not match: the prereg's hand-trace
missed the revolving-door concentration described below, predicting
nevict=36 with a spread histogram where the binary gives nevict=32
with a concentrated histogram. The mechanism section derives the
actual dynamics from the frozen rules and matches the binary
bin-for-bin (verified via a debug-instrumented build, discarded
after).

## Frozen results (3/3 byte-identical)

- Run digest: `0cf08d15c71f6e8614635bc62864f7515064ac29eac8693b9c4089d365424075`
- Binary digest: `a0c2f7006cd27c5b6ed20f58b0ef54ba11dcf7f55a73500c249c1e0a117d8fe9`
- Source digest: `9064111ebbd86d3bc343ece45a22a5153663495db42051a1eb4c9c622972dfde`

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=24 nevict=32 nentries=30
NT2 ML1 RETEST c_vb=6 nc=6 u=6 forget=6
NT2 ML1 EVHIST 100=4 101=3 102=3 103=3 104=3 105=3 112=1 113=1 114=1 115=1 116=1 117=1 134=2 135=1 136=1 137=1 138=1 139=1
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=0 K3=0 K4=0 K5=1
NT2 VERDICT=FAIL
```

Prediction vs actual: nevict 36 -> 32; c_vb 6/6 as predicted; u 6/12
as predicted; forget 6 as predicted; accB 24/24 as predicted;
histogram differs (prereg predicted 100..105=3 each, 134..139=2 each;
actual 100=4, 101..105=3 each, 134=2, 135..139=1 each). CONTROL arms,
ABLATION arm, nc, u, forget, accB, and the FAIL verdict direction all
matched. The miss is analyzed below; it does not change the verdict.

## Kill-bar evaluation

- K1 (learning intact under capacity): PASS. TTC 2/2/2, accs 24/24.
- K2 (eviction at pigeonhole minimum, no churn): FAIL. nevict_seq =
  32, not the frozen 36. (Discussion below: 36 was derived under the
  FORGET=0 regime; D1 achieves FORGET=6, which loosens the bound. The
  32 is nevertheless below NT2's 41 and H1's 40.)
- K3 (uncontested retention survives): FAIL. NC_OK = 6/6 but U_OK =
  6/12 (keys 112..117 absent at retest).
- K4 (revision survives pressure): FAIL -- on a split. C_VB = 6/6
  meets the revision literal (revision COMPLETES, the D1 goal), but
  FORGET = 6, so the bar fails.
- K5 (discriminative validity): PASS. ML0 shows the pure alias
  signature (u_abl = 0/12, nevict_abl = 0, nalias_abl = 12), distinct
  from ML1's eviction signature (nevict 32 vs 0).

## Actual mechanism (derived from the frozen rules; matches the binary bin-for-bin)

The prereg trace treated each pass's evictions as one-for-one swaps
and thereby missed the REVOLVING DOOR (the same effect H1's report
identified under total-evidence): once an eviction+insert lands a
low-net entry on the lowest slot index among global-minimum entries,
the NEXT insert in the same pass evicts it again. Churn concentrates
instead of spreading. Traced per pass (S = slot), verified against a
debug-instrumented build dumping the full slot table after each pass:

1. Pass 1 (6 evictions): novel keys 134..139 churn through slot 0.
   Key 134 evicts key 100 (checkpoint (VA,2,1)); then 135 evicts 134,
   136 evicts 135, ..., 139 evicts 138 -- each new entry has net=1 =
   the global minimum at the lowest tied slot. Only key 100 is
   permanently displaced; keys 101..105 are never evicted (they sit at
   slots 1..5 with net=1, never the unique minimum). End: slot 0 =
   139.
2. Pass 2 (7 evictions): key 100 re-inserts at slot 0 (restore
   (VA,2,1), contradiction -> ref=2, net=0), then keys 101..105 churn
   through slot 0 the same way (each restored, each reaching
   (VA,2,2), net=0, each immediately evicted by the next). Keys
   101..105 were PRESENT (never evicted in pass 1), so their pass-2
   teaching is a contradiction (ref=2), not a fresh insert. End:
   134..139 re-inserted at slots 0..5 (restore (VB,1,0), match ->
   sup=2); keys 100..105 absent, checkpointed (VA,2,2).
3. Pass 3 (7 evictions): keys 100..105 re-insert one by one through
   slot 0; EACH REVISES (restore (VA,2,2), contradiction -> ref=3 >
   sup=2 -> REVISE to (VB,1,0)) and is then immediately evicted by the
   next key in line. Revision COMPLETES (the D1 goal), but the revised
   entries (net=1) do not survive the pass. End: 134..139 at slots
   0..5 (sup=3); 100..105 absent, checkpointed (VB,1,0).
4. Pass 4 (6 evictions): keys 100..105 re-insert (restore (VB,1,0),
   match -> sup=2, net=2). Key 100 evicts U key 112 (slot 12, net=2,
   the new global minimum since all taught keys are now at net>=2);
   then 101 evicts 100, 102 evicts 101, ... -- revolving door on slot
   12. Only key 112 is permanently displaced from U. End: slot 12 =
   105 (VB,2,0); keys 100..104 absent, checkpointed (VB,2,0).
5. Pass 5 (6 evictions): keys 100..105 re-insert (restore (VB,2,0),
   match -> sup=3, net=3). They evict key 105 (slot 12, net=2) and U
   keys 113..117 (slots 13..17, net=2). NO revolving door: re-inserted
   net=3 exceeds the U net=2, so each insert sticks. End: slots
   12..17 = 100..105 (VB,3,0); keys 112..117 permanently absent.
6. Pass 6 (0 evictions): every taught key present; all hits. Stable.

End state: nevict = 6+7+7+6+6+0 = 32. Keys 100..105 all answer VB
(revision completed and retained); keys 112..117 are absent (never
taught in B, never return): c_vb=6/6, u=6/12, forget=6. accB=24/24
(all B keys resident).

## What this establishes

1. **D1 fixes the H3-diagnosed breaking interaction.** The
   eviction-reinsertion reset was the reason ref never exceeded sup in
   NT2's regime. With D1, ref accumulates across eviction boundaries
   (2,2 -> 3 > 2) and revision fires in pass 3. C_VB goes 0/6 -> 6/6.
   H3's "deeper rethink" direction is confirmed: preserving evidence
   across eviction is the change that matters, not the revision rule.
2. **But D1 relocates forgetting rather than eliminating it.** The
   frozen lowest-net comparator punishes staleness: U keys (net=2,
   never reinforced in B) become the global minimum once all taught
   keys' nets grow past 2, and 6 of them are displaced in passes 4-5.
   Forgetting is conserved by capacity (36 keys vs 30 slots) but moves
   from contradicted keys (NT2: 6 forgotten) to untouched keys (D1: 6
   forgotten). D1 does not touch the comparator; the comparator is the
   next breaking interaction.
3. **The pigeonhole bound needs its regime stated.** PREREG Section 5
   derived nevict >= 36 UNDER FORGET=0 (U keys pinned). D1 achieves
   FORGET=6, which loosens the bound: sacrificing 6 U keys leaves 30
   active keys in 30 slots, so evictions can stop after pass 5. The
   actual 32 < 36 is consistent -- it is the price of the 6 forgotten
   U keys, not churn. K2 as frozen (nevict==36) fails, but the failure
   is regime mismatch (forget=6), not excess churn: 32 is below NT2's
   41 and H1's 40, and passes 5-6 show zero churn once the resident
   set stabilizes.
4. **The revolving door is regime-independent.** H1 found it under
   total-evidence; D1 exhibits it under lowest-net with restored
   evidence. Whenever a re-inserted entry ties for the global minimum
   at the lowest slot index, the next insert re-evicts it. It
   concentrates the pass-1..4 churn onto one slot per pass instead of
   spreading it. Any future bar or mechanism must account for it; the
   prereg's spread-histogram prediction failed for exactly this
   reason.
5. **D1's signature is distinct.** NT2: c_vb=0/6, forget=6 (C keys),
   nevict=41. H1: c_vb=5/6, forget=1 (key 100), nevict=40. H3: null
   (identical to NT2). D1: c_vb=6/6, forget=6 (U keys 112..117),
   nevict=32. Four hypotheses, four cleanly different signatures from
   one apparatus.

## Prediction-miss accounting (honest)

The prereg predicted nevict=36 and histogram 100..105=3,
134..139=2 via a trace that assumed one-for-one eviction swaps each
pass. The actual binary gives 32 and 100=4, 101..105=3, 134=2,
135..139=1, 112..117=1. The error: the trace did not propagate the
revolving-door effect -- a re-inserted entry with net at the global
minimum at the lowest tied slot is immediately re-evicted by the next
insert, concentrating churn. (In pass 1, this meant only key 100 was
displaced while 134..138 churned through its slot; the trace had
assumed 100..105 all displaced.) The corrected trace above reproduces
all 18 nonzero histogram bins and every aggregate exactly. The
directional verdict (FAIL) is unchanged; K2's miss is regime mismatch
(Section 5 bound assumed FORGET=0), not a rule error. No prereg
amendment is needed: the verdict mapping, kill bars, and rules are
untouched -- only the predicted numbers were wrong, and they are
reported as wrong here.

## Recommended follow-up (preregistered, PREREG Section 9)

D1 failed as predicted in direction (K3/K4 fail) but the failure
splits instructively: revision completes (K4's C_VB literal met),
evictions drop below both predecessors, and the remaining failure is
purely the comparator punishing staleness (U keys at frozen net=2
become minimum). The preregistered next hypothesis is D2: an eviction
comparator that does not punish staleness/contradiction -- it must
distinguish "low evidence because new" from "low net because
contested" from "low net because untouched" -- with kill bars derived
from PREREG Section 5 (stating the forget regime). A D1+H1-total-
evidence compound is a two-change hypothesis needing its own prereg.
Do NOT patch D1's restore or add protection; the FAIL is diagnostic.

## Honest boundaries (from PREREG Section 10, unchanged)

- ML1/ML0 are minimal surrogates, not TNN's production substrate.
- Memorized key-value mappings; no L2/L3 claim.
- Single capacity point (CAP=30, 1.2x); single contradiction
  magnitude; scaling and graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table is
  learner state (own prior evidence only, no oracle/task info).
- The tie-break (lowest slot index) is frozen generic rule, not
  patched. H2 (recency-weighted) and D2 (staleness-blind comparator)
  are separate hypotheses.

## Provenance

- Prereg frozen alone: commit `2a162c01c` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  verified below (prereg commit strictly precedes this commit).
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev (same build as NT2/H1/H3). Zero
  forbidden-executable invocations.
- Source: `nt_d1_full.zag`, transcribed from NT2's `nt2_full.zag`
  with ONLY the four PREREG Section 2.1 change sites (header comment,
  arena + ck_get/ck_set + nt_new 2048, nt_insert helper + eviction
  checkpoint + insertion call, K2 literal 6->36). `diff` verified.
- Build: `znc nt_d1_full.zag -o nt_d1_bin` (exit 0; benign
  zagd-unavailable warning only); 3/3 runs byte-identical (cmp).
- Mechanism verification: a debug-instrumented COPY of the source
  (slot-table dump after each pass) was built and run to derive the
  per-pass trace above; the debug copy and binary were deleted and
  are NOT part of the frozen experiment.
- Commits local only, explicit pathspecs, never pushed.
