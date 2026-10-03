# PREREG: GEN-CYCLES -- Trial Over Re-applicable Structure Sequences With Learned Halting

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

COMPOSE-CYCLES (verdict INFORMATIVE-FAIL (U), 2026-10-03) proved the frozen
U cannot compose cycles. The precise boundary: (a) no re-application of a
structure, (b) no termination vocabulary, (c) no state carry between trials.
Its PREREG Section 11 preregistered the general-principle direction (not
implemented there): generalize U's "ordered trial" from {singles, ordered
pairs, each applied once} to TRIAL OVER RE-APPLICABLE STRUCTURE SEQUENCES
WITH LEARNED HALTING.

This battery implements that direction, minimally, and tests it:
- Does the generalization solve the COMPOSE-CYCLES fixpoint workload?
- Does it reduce to U exactly at sequence length <= 2 (kill bar C3)?
- Do U's 5 pairs and GEN's diamond/fan-in/DAG/partial still work (no regression)?

## 2. The mechanism (frozen spec; the only new code is gc_uni.zag + drivers)

`gc_solve(A,B,c,s,kin,kout,exp,nm,seqmax,cap)`:

1. Call the frozen `uni_solve` (byte-identical `ref_uc_uni.zag`, main
   stripped) verbatim: singles, then ordered pairs (x!=y), then WIDEN=1
   on filter-rejected pairs. If found, return. U is a strict prefix of
   the trial order.
2. If not found and seqmax >= 3, sequence phases. For k = 3..seqmax, in
   increasing k, enumerate all nm^k sequences lexicographically
   (position 0 slowest; repetitions allowed), and for each:
   - Admit by the CHAIN KIND RULE: in{seq[0]} compatible with kin;
     out{seq[i]} INTERSECTS in{seq[i+1]} for every adjacent pair;
     out{seq[k-1]} compatible with kout. Empty kind-set = compatible
     (existing k_has/k_inter semantics). This rule subsumes U's
     admission: at k=1 it is uni_admit_single; at k=2 it is
     uni_admit_pair (verified by inspection in REPORT).
   - Execute stepwise from s with per-step halting, in the existing
     contract vocabulary:
       (a) miss (v < 0): trial fails;
       (b) output==input (v == step input): HALT (fixpoint signal; the
           STEP-at-fixpoint identity taught in the workload is what
           makes this signal available -- learned halting);
       (c) steps >= cap: HALT (step cap; totality bound);
       (d) sequence end: HALT (halt after one pass -- the pipeline case).
     Each step prints one INTER= line. One sequence trial = one TRIES
     increment (as U counts one try per pair).
   - End-to-end verification retained: halted value == exp. On success,
     record every step via observe (generalizes U's pair recording:
     observe(x,s,v1)+observe(y,v1,v2)), set found/ans, return.
3. If still not found and kind_filter_on()==1: WIDEN=2 -- log "WIDEN=2",
   retry filter-rejected sequences once each (the sequence-phase analog
   of U's WIDEN=1; triggered solely by exhaustive admitted failure).

Frozen bounds: SEQMAX = 8, CAP = 8 (driver passes 8, 8). The workload's
own safety cap is 8; the fixpoint is 4 applications away.

Generality constraints (frozen):
- No cycle-specific handler: the executor is uniform over all sequences.
  The fixpoint halt (b) is checked after every step of every sequence
  trial; it is not conditioned on repetition, on MAP identity, or on
  any shape predicate. An IDENT MAP (class 3, always returns its input)
  triggers it on any sequence -- the rule is general.
- No new behavior classes, no new opcodes, no new admission dimensions.
  The HALT-kind signal of PREREG Sec 11's option list is NOT implemented
  (it would need a third kind; the "or" options output==input and step
  cap suffice and stay inside the existing vocabulary).
- Arena scratch: V history at 968 (9 x 4 bytes: V[0]=start, V[i]=value
  after step i), zeroed by world_new. U's 936/940/944 keep their
  semantics. No other layout change.

## 3. Reduction to U (frozen; kill bar C3 rests on this)

Claim: gc_solve with seqmax <= 2 is EXACTLY uni_solve.

Proof sketch (mechanical, audited in REPORT): the sequence phases are
guarded by `if(seqmax>=3)`. With seqmax=2 the guard is false, so
gc_solve executes `c=uni_solve(...); if(found) return c; return c` --
the identical code path, identical arena state, identical output as
calling uni_solve directly. No sequence code runs; no extra output is
printed; TRIES/ANS are U's. Hence byte-identical outputs on every world.

The reduction is therefore structural, not empirical: C3 checks the
empirical consequence (byte-identical stdout) on all 6 worlds (5 pairs
+ fixpoint workload).

## 4. Workload (frozen; reused byte-identical from COMPOSE-CYCLES)

The fixpoint-iteration workload of COMPOSE-CYCLES PREREG Section 5,
unchanged: setup_cyc (chain 1001..1005 on rel 201; measure rel 202 with
non-monotonic counts 2,1,3,1,2; subject-marker rel 203; distractor rel
204), MAPs 0..3 (class 4 STEP on 201; class 1 COUNT on 202; class 3
IDENT; class 1 COUNT on 204), teach calls as frozen there. Query:
s=1001, kin=1, kout=1, exp=1005, nm=4. All identifiers opaque integers.

Base: gc_base.zag = byte-copy of cyc_base.zag (sha256 verified in
NAMECHECK Step 1). U region: uni_nomain.zag = ref_uc_uni.zag minus main
(sed '/^fn main/,$d', region-verified). New: gc_uni.zag (Section 2),
cyc_nomain.zag = cyc_new.zag minus main (setup_cyc only, region-verified),
gc_main.zag (driver: fixpoint query at seqmax=8, then U's 5 pairs at
seqmax=8), gc_redmain.zag (driver: fixpoint query at seqmax=2 then U's
5 pairs at seqmax=2, UNI labels -- the reduction check).

## 5. Frozen predictions

### 5.1 Fixpoint workload at seqmax=8 (gc_solve)

- U prefix: 14 tries, WIDEN=1, found=0 (exactly the frozen C3 run).
- k=3: 16 admitted sequences (m1 in {0,1,2,3}, m2 in {0,2}, m3 in
  {0,2} by the chain rule: all in-masks are {1}; non-final positions
  need out INTERSECTS {1}, i.e. MAP 0/2; final needs out{1}, i.e.
  MAP 0/2). All 16 fail: [0,0,0]->1004; [0,0,2]->1003 (fixpoint halt
  at step 3); [0,2,*]->1002 (fixpoint halt at step 2); [1,*,*]->2
  (fixpoint halt at step 2); [2,*,*]->1001 (fixpoint halt at step 1);
  [3,*,*] miss at step 1. 16 tries, 26 INTER= lines.
- k=4: [0,0,0,0] (lexicographically first) admitted; stepwise
  1001->1002->1003->1004->1005; no mid-sequence fixpoint; end-of-pass
  halt; 1005==exp: SUCCESS. observe fires 4x on MAP 0.
- Predicted report: `ARM=GC PROB=QC ANS=1005 TRIES=31`.
  TRIES = 14 (U) + 16 (k=3) + 1 ([0,0,0,0]).
- Census: MAP 0 n=9 (5 teach + 4 success-recorded), inmask=1 outmask=1;
  others unchanged (m1: 1/2 n=5; m2: 1/1 n=1; m3: 1/2 n=1).
- WIDEN=2 never fires (found at k=4).

### 5.2 U's 5 pairs at seqmax=8

U solves all 5 in its prefix (found=1 before any sequence phase), so
the sequence phases never run. Predicted: the 5-pair section is
byte-identical to canonical u_run1.txt up to the ARM= label (GC vs UNI).

### 5.3 Reduction at seqmax=2

Predicted: reduction binary stdout is byte-identical to
cyc_run1.txt concatenated with u_run1.txt (C3).

### 5.4 GEN regression (frozen GEN, unmodified)

- Diamond battery (d6_base + d6_gen[1..239] + d6_gen[240..270] main):
  stdout byte-identical to gsf_diamond_run1.txt (sha256 962ca4f0...).
- Generality battery (d6_base + d6_gen[1..239] + gg_new.zag):
  stdout byte-identical to gg_run1.txt (sha256 4b81226d...).
  (Fresh arenas per query; the GEN-STATEFIX tried-state reset is
  immaterial there, so canonical d6_gen.zag is the right reference.)

## 6. Build plan (implementation follows this prereg commit)

1. Copy frozen sources into the lane with sha256 verification:
   gc_base.zag (<= cyc_base.zag), ref copies for audit.
2. Write gc_uni.zag (Section 2 spec; nothing else).
3. Write gc_main.zag, gc_redmain.zag, cyc_nomain.zag (sed-stripped).
4. Assemble gc_full.zag = gc_base + uni_nomain + gc_uni + cyc_nomain +
   gc_main; gc_redfull.zag = same but gc_redmain. Region cmp audits.
5. Compile with pinned safebin znc; run gc_bin 3x (pairwise cmp);
   run gc_redbin 1x (deterministic by C2; still run 3x, cmp).
6. GEN regression assemblies from sha256-verified copies; run 3x each;
   cmp against recorded outputs.
7. build.sh encodes all audits fail-closed (set -e).

## 7. Frozen kill bars

- C1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md + NAMECHECK.md
  Steps 0-2 ONLY) strictly precedes all implementation commits.
- C2 DETERMINISM: PASS iff 3/3 runs of gc_bin are pairwise byte-identical
  (cmp); digests recorded. (Reduction + GEN batteries also 3x cmp.)
- C3 REDUCTION: PASS iff gc_redbin stdout is byte-identical
  (cmp, empty diff) to cyc_run1.txt ++ u_run1.txt. This is the
  reduction-to-U kill bar: seqmax=2 must BE U.
- C4 CYCLE-PASS: PASS iff the GC/QC report line shows ANS=1005
  (found=1), TRIES=31, no WIDEN=2.
- C5 U-REGRESSION: PASS iff the seqmax=8 5-pair section, with ARM=GC
  relabeled to ARM=UNI, is byte-identical to u_run1.txt (ANS
  65,2,2,2,3). The generalization must not disturb U's pairs.
- C6 GEN-REGRESSION: PASS iff the diamond battery stdout is
  byte-identical to gsf_diamond_run1.txt AND the generality battery
  stdout is byte-identical to gg_run1.txt. Pipelines and DAGs stay in
  the envelope.
- C7 OPACITY: PASS iff grep over all built sources (gc_base.zag,
  gc_uni.zag, cyc_nomain.zag, gc_main.zag, gc_redmain.zag,
  uni_nomain.zag) for banned domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is
  a bare integer.
- C8 NO-CYCLE-HANDLER: PASS iff (a) grep for `fixpoint|Fixpoint|FIXPOINT`
  in gc_uni.zag finds only the output==input halt inside the uniform
  stepwise executor and its header comment (no branch on repetition,
  MAP identity, or shape); (b) the halting checks apply to every
  sequence trial identically (audit by reading gc_try_seq).

## 8. Verdict mapping (frozen)

- C1 FAIL -> VOID. Commit order broken; re-freeze.
- C2 FAIL -> UNDECIDED. Name the decisive rerun.
- C3 FAIL -> VOID. The reduction is broken: the implementation is not
  a strict generalization of U. Do not salvage; re-freeze.
- C4 FAIL (with C1,C2,C3 PASS) -> INFORMATIVE-FAIL (mechanism): the
  Section 11 shape does not compose the fixpoint workload. REPORT
  characterizes which trial the enumeration missed and why.
- C4 PASS but C5 FAIL -> FAIL (regression): the generalization disturbs
  U's pipeline pairs. REPORT names the disturbed pair and cause.
- C4 PASS but C6 FAIL -> FAIL (envelope): REPORT names the GEN battery
  that moved and investigates (expected: no movement; GEN untouched).
- C7/C8 FAIL -> VOID. Implementation deviated from prereg.
- C1-C8 all PASS -> PASS: cycles join pipelines and DAGs in the
  general composition envelope via sequences with learned halting.
  (Scope: one fixpoint family, per Section 9.)

## 9. Honest boundaries (pre-declared)

- One cycle family (fixpoint iteration on a 4-chain, M1-M5 from
  COMPOSE-CYCLES). Oscillatory, convergent-signal, and multi-structure
  feedback cycles are NOT tested.
- The oracle answer exp is supplied for end-to-end verification (as in
  the P6/U batteries); the test targets the PROPOSAL space.
- SEQMAX=8 and CAP=8 are frozen researcher bounds, not learned. The
  halting SIGNALS (output==input via the taught STEP identity; the cap
  as totality) are in contract vocabulary; the bound values are not
  claimed as learned.
- The HALT-kind signal (PREREG Sec 11 option) is not implemented.
- GEN is tested unmodified as a regression battery only; this lane
  makes no GEN claim.
- Behavior classes 0-4 and the -2 sentinel keep their canonical
  semantics; kind labels 1/2 keep theirs.
