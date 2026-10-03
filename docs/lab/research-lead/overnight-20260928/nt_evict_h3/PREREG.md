# PREREG: NT-EVICT-H3 -- evidence-preserving revision under capacity pressure

## 1. Question and lineage

NT2 (NT-CAPACITY, FAIL) showed that under CAP=30 with eviction by lowest
NET (sup-ref), contradicted keys are evicted before revision completes:
contradiction depresses net to the insertion baseline, the tie-break
evicts the revising keys, and re-insertion as fresh (sup=1, ref=0) keeps
ref from ever exceeding sup. NT-EVICT-H1 (FAIL, per parent tasking: no
lane files found in workspace, see NAMECHECK Step 1) showed that evict-
by-lowest-TOTAL (sup+ref) fails differently: revision fires, but the
revision reset to (sup=1, ref=0) collapses total to the global minimum,
so the just-revised entry is immediately evicted -- a revolving door.

Parent diagnosis: "The breaking interaction is the evidence reset, not
the comparator." H3 tests exactly this: keep NT2's battery and NT2's
eviction rule frozen, and change ONLY the revision action so that a
revision PRESERVES accumulated evidence instead of resetting to
(sup=1, ref=0). If the reset is the breaking interaction, revision
should complete under pressure (c_vb=6/6, forget=0). If H3 fails, the
diagnosis is wrong and a deeper rethink is needed.

## 2. The H3 rule (frozen; variant (a))

When a contradiction makes ref > sup (revision trigger, unchanged), the
slot is revised as follows:

- value := new value (unchanged)
- sup := sup_old (PRESERVED; the reset to 1 is removed)
- ref := 0 (cleared; the refutations were evidence against the OLD
  value and do not transfer to the new one)

In `nt_learn`, NT2's revision line

    if(r>sk(L,s,2)){ sp(L,s,1,val); sp(L,s,2,1); sp(L,s,3,0); }

becomes

    if(r>sk(L,s,2)){ sp(L,s,1,val); sp(L,s,3,0); }

i.e. the `sp(L,s,2,1)` (sup reset) is deleted. One line. Nothing else in
the learner changes: the revision TRIGGER (ref > sup after increment),
the contradiction accumulation (ref++), the support accumulation
(sup++), the insertion rule (fresh slots are still (key,val,1,0)), the
eviction rule (lowest sup-ref, ties to lowest slot index), prediction
(sup > ref), capacity, addressing, and all protocol are NT2 verbatim.

### Why variant (a), and why not (b) or (c)

- (a) "keep the full (sup, ref) history", implemented as preserve-sup /
  clear-ref: the support count is entry-local standing that the reset
  destroys; the refutations are value-specific and correctly cleared.
  It has NO free parameters.
- (b) "transfer a fraction of the old evidence": rejected. Any fraction
  (1/2, 2/3, ...) is a researcher-chosen magic number with no
  principled derivation; governance forbids guessed constants. If (a)
  fails, (b) is not a fallback -- it would be a new hypothesis needing
  its own preregistration and parameter justification.
- (c) "mark recently-revised for eviction protection": rejected on
  governance grounds. NT2 PREREG Section 9 explicitly forbids protection
  ("Do NOT patch the tie-break or add protection"), and the eviction
  policy must remain generic with "no protection flags". (c) is a
  protection mechanism, not a generic rule.

## 3. Frozen machinery (NT2 verbatim except Section 2)

Learner state, CAP=30, slot layout (key,value,sup,ref), eviction by
globally lowest (sup-ref) with lowest-slot-index tie-break, ML1
associative dedicated addressing, ML0 overlapping map (NT1 verbatim),
`nt_learn` / `nt_predict` rules, oracle VA/VB, families SET_A/SET_B,
partitions C=100..105 / NC=106..111 / U=112..123, protocol
(CONTROL-A, CONTROL-B, SEQ with 6 fixed B passes, ABLATION on ML0),
measurement-only eviction histogram: all identical to NT2 PREREG
Sections 2-4. The `arm` harness selector is unchanged (0=ML1, 1=ML0).

## 4. Mechanism trace (grounds the directional prediction)

Hand-trace of the frozen H3 rules for ML1 SEQ (the trace that NT2's
measured histogram confirmed bin-for-bin; H3 changes nothing on this
path):

- Phase A: TTC=2; every A key ends (sup=2, ref=0).
- B pass 1: C keys contradicted once -> (sup=2, ref=1, net=1). Novel
  128..133 fill the 6 free slots (net=1). 134..139 each force an
  eviction; lowest net=1 ties broken by slot index evict slot 0 first:
  134 evicts 100, then 135..139 revolve through slot 0. nevict=6.
- B pass 2: 100 re-inserted fresh, evicts 139 from slot 0; 101..105
  found and contradicted -> (sup=2, ref=2, net=0). ref > sup is FALSE
  (2 > 2 false): NO revision fires. Novel phase: net=0 (slots 1..5) is
  the minimum; 134..138 evict 101..105; 139 evicts 100. nevict=13.
- B passes 3..6: every C key is absent at pass start, inserted FRESH
  with the B value (sup=1, ref=0 -- an insertion, not a contradiction),
  revolves through slot 0 (6 evictions: each C key evicts the previous),
  then 139 evicts the last C key (1 eviction). 7 evictions per pass.
  No key ever holds ref > sup: the only contradictions in the whole
  battery are pass-1 (ref=1, sup=2) and pass-2 (ref=2, sup=2).

Therefore the H3 revision action is DEAD CODE in the ML1 arms: the
trigger condition (ref > sup) never occurs, so deleting the sup reset
cannot change any ML1 state transition. In the ML0 ABLATION arm,
revision DOES fire (no eviction; pass 3 gives ref=3 > sup=2), and H3
sets (new value, sup=2, ref=0) instead of (new value, sup=1, ref=0);
this changes no measured quantity (prediction tests only sup > ref;
ML0 never evicts; all counts and accuracies are sup-magnitude-
independent). The eviction histogram, nevict, TTCs, accuracies,
partitions, and FORGET are all unchanged.

CONSEQUENCE (frozen): H3's output must be BYTE-IDENTICAL to NT2's
frozen output. Any byte difference falsifies this trace (it would mean
revision fired somewhere unaccounted for, or the dynamics were
mis-traced) and is itself the finding.

## 5. Frozen predictions (directional: FAIL, identical numbers to NT2)

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=18 nevict=41 nentries=30
NT2 ML1 RETEST c_vb=0 nc=6 u=12 forget=6
NT2 ML1 EVHIST 100=6 101=5 102=5 103=5 104=5 105=5 134=1 135=1 136=1 137=1 138=1 139=5
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=0 K3=1 K4=0 K5=1
NT2 VERDICT=FAIL
```

Output lines keep the `NT2` battery prefix (this IS the NT2 battery,
run under H3) so the run output is directly cmp-comparable to NT2's
frozen runs. Predicted run sha256:
`3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`
(NT2's frozen run digest). Predicted verdict: FAIL with K1=1, K2=0,
K3=1, K4=0, K5=1 -- the revision does not complete (c_vb=0/6),
forget=6, nevict=41.

## 6. Frozen kill bars

Identical to NT2 (PREREG Section 7, as amended by A1), except K4 is
tightened to the tasking's literal bar:

- K1 (learning intact; else VOID): TTC_A_ctrl in 1..50 AND acc 24/24;
  TTC_B_ctrl in 1..50 AND acc 24/24; TTC_A_seq in 1..50 AND accA 24/24.
- K2 (eviction minimal, no churn): nevict_seq == 6.
- K3 (uncontested retention survives): NC_OK = 6/6 AND U_OK = 12/12.
- K4 (revision completes under pressure): c_vb == 6/6 AND forget == 0.
- K5 (discriminative validity): u_abl = 0/12 AND nevict_abl = 0 AND
  nalias_abl = 12 AND nevict_seq != nevict_abl. Else INCONCLUSIVE.

## 7. Verdict mapping (frozen)

- K1..K5 all hold: **PASS** -- evidence-preserving revision lets
  revision complete under capacity pressure; the NT1 principle survives.
- K1 fails: **VOID**.
- K1 holds, K5 fails: **INCONCLUSIVE**.
- K2 or K4 fail (K1, K3, K5 hold): **FAIL** -- H3 does not preserve
  revision under pressure. Report with the mechanism: if the output is
  byte-identical to NT2, the revision rule never fired and the parent
  "evidence reset" diagnosis is falsified for the net-eviction regime;
  the breaking interaction is eviction preempting revision (ref never
  exceeds sup because contradicted keys are removed mid-revision), not
  the revision reset.

## 8. Assembly, build, run (frozen)

- Single source file `nt3_full.zag`: `nt2_full.zag` transcribed with the
  single-line Section 2 change (header comment updated to name H3).
- Build: `znc nt3_full.zag -o nt3_bin` under safebin-only PATH.
- Run `nt3_bin` 3 times; outputs `nt3_run1.txt`, `nt3_run2.txt`,
  `nt3_run3.txt`. Require byte-identical (cmp) and record sha256; also
  cmp against NT2's frozen `nt2_run1.txt` (byte-identity prediction).
- Compiler-defect workarounds (mandatory, from AGENTS.md): unchanged
  from NT2 (get32/set32 only; single-buffer cursor output + one
  `_zag_raw_syscall`; no `!(A && B)` in while conditions; if-nesting at
  most 3 deep; no `[]u8 as *u8` casts). The one-line change introduces
  none of the flagged patterns (it DELETES a call).

## 9. Honest boundaries (inherited from NT2, unchanged)

- ML1/ML0 are minimal surrogates for the retention/revision/eviction
  principle, not TNN's production substrate. A result here
  characterizes the rule-set, not TNN-as-built.
- L1 memorization substrate; no L2/L3 claim. Families are memorized
  key-value mappings; the experiment measures retention/revision/
  eviction dynamics only.
- Single capacity point (CAP=30, 1.2x over capacity); single
  contradiction magnitude; eviction histogram is measurement-only.
- Opaque identifiers throughout: keys/values are bare integers; no
  semantic labels in code or output.

## 10. Amendment record

(none yet; any amendment will be committed alone before implementation,
per governance)
