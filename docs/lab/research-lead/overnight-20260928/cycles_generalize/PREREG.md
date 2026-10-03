# PREREG: CYCLES-GENERALIZE -- Is Sequences+Halting General?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

GEN-CYCLES (verdict PASS, 2026-10-03) proved that trial over re-applicable
structure sequences with learned halting solves the C403 fixpoint workload
(4-chain, single STEP MAP re-applied, seqmax=8 reduces byte-identically to U).
Its honest boundary: "One fixpoint family only; SEQMAX=8/CAP=8 are frozen
bounds, not learned; HALT-kind signal not implemented. Data-dependent halting
as the operative stop of a winning trial is not yet exercised."

This battery asks: is sequences+halting general, or just fitted to one
fixpoint family? Three tests:

- T1 (different fixpoint family): an alternating two-structure fixpoint
  chain (5 hops over two STEP MAPs on two relations; neither MAP alone
  suffices). If sequences+halting is general, the frozen mechanism solves
  it with no change.
- T2 (data-dependent halting): a workload where the winning trial MUST
  halt via output==input, provably not via end-of-pass. The winning
  sequence is longer than the hop count; the output==input halt fires at
  step i < k; without it the trial would continue into a provable miss.
- T3 (HALT-kind signal): implement the preregistered-but-missing third
  halting option of COMPOSE-CYCLES PREREG Section 11 ("output-kind
  includes a HALT signal"). The frozen core (gc_uni.zag) is NOT modified:
  the signal is implemented as a strictly additive extension
  (cg_base.zag: kind 3 + class 5; cg_uni.zag: one added HALT check),
  with a frozen-mechanism control (must FAIL: signal unrecognized) and a
  reduction test (extended executor byte-identical to frozen on all old
  workloads).

## 2. Frozen mechanism (untouched by T1/T2; extended only additively for T3)

`gc_solve` in gc_uni.zag (sha256
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6):
frozen uni_solve prefix (singles, ordered pairs x!=y, WIDEN=1), then for
k=3..seqmax lexicographic sequences with repetitions admitted by the chain
kind rule, executed stepwise with halting (a) miss v<0 -> fail,
(b) v==prev -> break (output==input), (c) i>=cap -> break, (d) end of pass;
success iff halted value == exp; every step recorded via observe; WIDEN=2
retries rejected sequences. Arena V history at 968. Base gc_base.zag
(sha256 0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125),
U region uni_nomain.zag (sha256
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3),
workload region cyc_nomain.zag (sha256
aa28dac4506bfa8dc2a7f821bbb15fff2bdf89dc157c16def1472d97965baea6).
All copied with sha256 verification; G8 audits they are unmodified.

Bounds: SEQMAX=8, CAP=8 for T1/T2/T3-signal (frozen values, not learned;
the claim under test is the halting vocabulary, not the bound values).
T3-control runs at seqmax=3 to keep the failure trace auditable.

## 3. T1: alternating two-structure fixpoint family (PROB=QG)

Setup setup_qg (all identifiers opaque integers):
- Chain: (3001,301,3002), (3002,302,3003), (3003,301,3004),
  (3004,302,3005), (3005,301,3006). 3006 has no 301/302 edge (fixpoint
  for both STEP MAPs). 3001..3005 are fact subjects; 3006 is not.
- Marker: (3101,305,3102). Distractor: (3201,306,3202), (3201,306,3203).
- MAPs: m0 = class 4 STEP on 301; m1 = class 4 STEP on 302;
  m2 = class 3 IDENT; m3 = class 1 COUNT on 306.
- Teaches: m0: (3001,3002),(3003,3004),(3005,3006),(3006,3006);
  m1: (3002,3003),(3004,3005),(3006,3006); m2: (3101,3101); m3: (3201,2).
- Learned masks: m0 in{1,2} out{1,2} (3006 not a subject);
  m1 in{1,2} out{1,2}; m2 in{1} out{1}; m3 in{1} out{2} (2 not a subject).
- Query: s=3001, kin=1, kout=1, exp=3006, nm=4, seqmax=8, cap=8.

Why this is a different family: the fixpoint is reached only by
ALTERNATING two structures ([0,1,0,1,0]); neither MAP alone can advance
more than one hop ([0,0,...] stalls at 3002, [1,...] stalls at 3001);
the chain is 5 hops (winner at k=5, deeper than the 4-chain); kind masks
are mixed {1,2} (vs C403's {1}/{2}).

Frozen predictions:
- U prefix: 3 admitted singles (m0: 3001->3002; m1: 3001->3001;
  m2: 3001->3001; m3 rejected, out{2}∌1), 8 admitted pairs
  ([0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[3,0],[3,1], all fail;
  [0,3],[1,3],[2,3],[3,2] rejected), WIDEN=1 retries the 4 rejected
  pairs (all fail: COUNT at 3001/3002 on 306 misses). TRIES=15, found=0.
- k=3: 39 admitted (b=0:12, b=1:12, b=2:9, b=3:6 by the chain rule;
  m3-containing fail via COUNT miss on 306; m2-containing fail via
  early output==input halt with cur<=3004; pure {0,1} fail:
  [0,1,0]->3004 end-of-pass, rest halt earlier). 39 tries, all fail.
- k=4: 139 admitted (b=0:44, b=1:44, b=2:33, b=3:18). All fail:
  pure {0,1} max out at [0,1,0,1]->3005 (end-of-pass, !=3006);
  m2/m3 sequences fail as at k=3. 139 tries.
- k=5: 495 admitted total. Lexicographic order: n=0..63 are [0,0,*,*,*]
  (39 admitted; all (b)-halt at step 2 with cur=3002); n=64,65,66 are
  [0,1,0,0,0..2] (admitted; (b)-halt at step 4 with cur=3004);
  n=67 [0,1,0,0,3] rejected (final out{3}∌1); n=68 [0,1,0,1,0]
  admitted: 3001->3002->3003->3004->3005->3006, end-of-pass halt,
  3006==exp: SUCCESS. 43 tries.
- Report: `ARM=GC PROB=QG ANS=3006 TRIES=236`
  (15 + 39 + 139 + 43). No WIDEN=2.
- Census: m0 n=7 inmask=3 outmask=3; m1 n=5 inmask=3 outmask=3;
  m2 n=1 inmask=1 outmask=1; m3 n=1 inmask=1 outmask=2.

## 4. T2: data-dependent halting as the operative stop (PROB=QH)

Setup setup_qh:
- Chain: (4001,401,4002). 4002 is never a fact subject (kind 2);
  stepf at 4002 returns 4002 (identity at fixpoint).
- (4101,402,9101); (1,409,2) [makes 1 a subject]; (4101,403,9101);
  (4201,404,9201),(4201,404,9202). 555 never a subject.
- MAPs: m0 = class 4 STEP on 401; m1 = class 1 COUNT on 402;
  m2 = class 1 COUNT on 403; m3 = class 1 COUNT on 404.
- Teaches: m0: (4001,4002),(4002,4002); m1: (4101,1),(555,-2)
  (count_rel(555,402)=0 -> -2; teach observes on v==exp, so the -2
  observation is legal and gives inmask∋2/outmask∋2);
  m2: (4101,1); m3: (4201,2).
- Learned masks: m0 in{1,2} out{2}; m1 in{1,2} out{1,2};
  m2 in{1} out{1}; m3 in{1} out{2}.
- Query: s=4001, kin=1, kout=1, exp=4002, nm=4, seqmax=8, cap=8.

Why the winner MUST halt via output==input: the chain rule REJECTS the
pure repetition [0,0,0] (final out{0}={2}∌kout=1) and the single [0], but
ADMITS [0,0,1] (out{0}∩in{1}={2}≠∅, final out{1}∋1). The winning trial
[0,0,1] (k=3, lexicographically first admitted: n=0 [0,0,0] rejected,
n=1 [0,0,1] admitted) executes: step1 4001->4002 (INTER=4002); step2
MAP 0 at 4002 -> 4002, v==prev -> (b)-halt with i=2 < k=3.
End-of-pass (i>=k) is never reached: only 2 INTER= lines are printed
for a k=3 trial. Strict necessity (code audit, preregistered): without
the (b) check the trial would continue to step 3 (MAP 1 = COUNT on 402
at 4002 -> -2 -> miss -> fail). So the (b)-halt is not just the firing
stop but necessary for this win.

Frozen predictions:
- U prefix: 2 admitted singles (m1: -2; m2: -2; m0/m3 rejected),
  4 admitted pairs ([0,1]: 4002 then -2; [1,2],[2,1],[3,1]: v1=-2),
  WIDEN=1 retries 8 rejected pairs (all -2). TRIES=14, found=0.
- k=3: [0,0,1] wins as above. 1 try.
- Report: `ARM=GC PROB=QH ANS=4002 TRIES=15`. No WIDEN=2.
- The winning trial prints exactly 2 INTER= lines (4002, 4002):
  the (b)-halt fired at i=2<k=3. This is the empirical proof that
  output==input was the operative stop.
- Census: m0 n=4 inmask=3 outmask=2; m1 n=2 inmask=3 outmask=3;
  m2 n=1 inmask=1 outmask=1; m3 n=1 inmask=1 outmask=2.

## 5. T3: HALT-kind contract signal

### 5.1 Design (additive extension; frozen core untouched)

COMPOSE-CYCLES PREREG Section 11 preregistered three halting options:
"output-kind includes a HALT signal, or output==input fixpoint, or a step
cap". GEN-CYCLES implemented the latter two. T3 implements the first:

- cg_base.zag = gc_base.zag PLUS exactly: (a) pkind returns 3 for the
  HALT sentinel v==-3; (b) new behavior class 5 STEP-HALT: one hop along
  rel, but emits -3 (HALT-kind signal) at fixpoint instead of identity;
  (c) exec_map dispatches cl==5. Classes 0-4 byte-identical semantics.
  G8 audits the diff is exactly this.
- cg_uni.zag = gc_uni.zag PLUS exactly one check in the stepwise loop,
  before the miss check: `if(v==-3){ break; } // HALT-kind signal:
  halt, cur keeps its pre-step value`. G8 audits the diff is exactly this.
- The HALT-kind is a LEARNED contract: teach/observe put bit
  (1<<(3-1))=4 into outmask when a MAP emits -3; k_has/k_inter carry it
  with no new admission dimension and no special-casing.

Semantics: a MAP emitting -3 says "stop; the answer is the current
value". This differs from output==input: the structure signals halt
WITHOUT producing the fixpoint identity.

### 5.2 Workload (PROB=QK0 control / QK signal)

Setup setup_qk:
- Chain: (5001,501,5002). 5002 never a fact subject.
- (5101,502,9101); (1,509,2); (5101,503,9101);
  (5201,504,9201),(5201,504,9202). 555 never a subject.
- MAPs: m0 = class 5 STEP-HALT on 501; m1 = class 1 COUNT on 502;
  m2 = class 1 COUNT on 503; m3 = class 1 COUNT on 504.
- Teaches: m0: (5001,5002),(5002,-3); m1: (5101,1),(555,-2);
  m2: (5101,1); m3: (5201,2).
- On the EXTENDED base: m0 in{1,2} out{2,4}(=6); m1 in{1,2} out{1,2};
  m2 in{1} out{1}; m3 in{1} out{2}.
- Query: s=5001, kin=1, kout=1, exp=5002, nm=4.

Control prediction (FROZEN gc_uni.zag + gc_base.zag, seqmax=3, PROB=QK0):
class 5 is unknown to the frozen base (degrades to class-2 logic), so
the -3 signal is never emitted and the workload is unsolvable: U prefix
14 tries (2 singles + 4 pairs + 8 WIDEN=1, all -2), k=3: 18 admitted
((a,0,1):2, (a,1,*):8, (a,2,*):6, (a,3,1):2; all fail: any trial reaching
5002 then steps into a miss), WIDEN=2 retries 46 rejected k=3 sequences
(all fail), found=0.
Report: `ARM=GC PROB=QK0 ANS=-2 TRIES=78` (14+18+46). WIDEN=2 fires.
This PROVES the HALT-kind signal is absent from the frozen mechanism:
the same workload bytes fail without it.

Signal prediction (EXTENDED cg_uni.zag + cg_base.zag, seqmax=8, PROB=QK):
U prefix 14 tries (same structure as control); k=3: n=0 [0,0,0]
rejected (final out{0}∌1); n=1 [0,0,1] admitted: step1 5001->5002
(INTER=5002); step2 MAP 0 at 5002 emits -3 (INTER=-3); HALT-kind break
with cur=5002==exp: SUCCESS. 1 try.
Report: `ARM=XH PROB=QK ANS=5002 TRIES=15`. No WIDEN=2.
The INTER=-3 line is the smoking gun: the HALT-kind signal fired.
Census: m0 n=3 inmask=3 outmask=6; m1 n=2 inmask=3 outmask=3;
m2 n=1 inmask=1 outmask=1; m3 n=1 inmask=1 outmask=2.

Reduction prediction (EXTENDED cg_uni.zag + FROZEN gc_base.zag on the
C403 QC workload, QG, QH): stdout byte-identical to the frozen binary's
output on the same three queries (the v==-3 check never fires: no class
emits -3 and -3 never appears as a value). This proves the extension is
strictly additive.

## 6. Build plan

1. Lane repo init (done). This PREREG.md + NAMECHECK.md commit alone.
2. Copy frozen sources with sha256 verification: gc_base.zag,
   uni_nomain.zag, gc_uni.zag, cyc_nomain.zag.
3. Write cg_setups.zag (setup_qg, setup_qh, setup_qk),
   cg_base.zag (gc_base + preregistered pkind/class-5),
   cg_uni.zag (gc_uni + preregistered HALT check; diff-audited),
   four mains: cg_main_frozen (QC,QG,QH), cg_main_frozk (QK0),
   cg_main_extred (QC,QG,QH on extended+frozen base),
   cg_main_extsig (QK on extended+extended base).
4. Assemble: cg_fbin (frozen), cg_fbin0 (frozen control),
   cg_xbin (extended+frozen base), cg_xsbin (extended+extended base).
   Compile with pinned safebin znc. Run each 3x, pairwise cmp.
5. build.sh encodes all audits fail-closed (set -e): sha256 of frozen
   copies, diffs of cg_uni/cg_base vs frozen showing exactly the
   preregistered additions, 3/3 cmp, report-line greps, reduction cmp,
   opacity grep.

## 7. Frozen kill bars

- G1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md + NAMECHECK.md
  Steps 0-2 ONLY) strictly precedes all implementation commits.
- G2 DETERMINISM: PASS iff 3/3 runs of each of the 4 binaries are
  pairwise byte-identical (cmp); digests recorded.
- G3 T1-PASS: PASS iff frozen binary reports
  `ARM=GC PROB=QG ANS=3006 TRIES=236`, no WIDEN=2 in the QG section.
- G4 T2-PASS: PASS iff frozen binary reports
  `ARM=GC PROB=QH ANS=4002 TRIES=15`, no WIDEN=2, AND the winning QH
  trial prints exactly 2 INTER= lines (the last two INTER= lines of the
  QH section are both 4002 with no third).
- G5 T3-CONTROL: PASS iff the frozen binary on the T3 workload reports
  `ARM=GC PROB=QK0 ANS=-2 TRIES=78` with WIDEN=2 fired (found=0).
- G6 T3-SIGNAL: PASS iff the extended binary reports
  `ARM=XH PROB=QK ANS=5002 TRIES=15`, no WIDEN=2, with an INTER=-3 line
  in the QK section.
- G7 REDUCTION: PASS iff the extended+frozen-base binary stdout is
  byte-identical (cmp, empty diff) to the frozen binary stdout on
  QC/QG/QH.
- G8 FROZEN-INTACT: PASS iff (a) sha256 of the lane's gc_uni.zag,
  gc_base.zag, uni_nomain.zag, cyc_nomain.zag match Section 2;
  (b) diff gc_uni.zag cg_uni.zag shows ONLY the preregistered HALT
  check (+ its comment); (c) diff gc_base.zag cg_base.zag shows ONLY
  the preregistered pkind kind-3, class-5 fn, and exec_map dispatch
  (+ comments).
- G9 OPACITY: PASS iff grep over all built sources for banned
  domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is a
  bare integer.

## 8. Verdict mapping

- G1/G8/G9 FAIL -> VOID.
- G2 FAIL -> UNDECIDED (name the decisive rerun).
- G3 FAIL -> INFORMATIVE-FAIL (family): sequences+halting does not
  cover the alternating two-structure family; REPORT characterizes the
  missed trial.
- G4 FAIL (with G3 PASS) -> INFORMATIVE-FAIL (halting): the winning
  trial did not halt data-dependently as preregistered; REPORT says
  which stop fired and why.
- G5 FAIL (frozen SOLVES the T3 workload) -> VOID the T3 control:
  the workload does not isolate the signal; REPORT investigates.
- G6 FAIL (with G5 PASS) -> FAIL (signal): the preregistered HALT-kind
  extension does not produce the predicted halt-and-verify.
- G7 FAIL -> FAIL (regression): the additive extension changed old
  behavior; REPORT names the moved section.
- All PASS -> PASS: sequences+halting generalizes to a second fixpoint
  family with no mechanism change; data-dependent halting is the
  operative (and necessary) stop of a winning trial; the HALT-kind
  contract signal is implemented as a strictly additive extension.

## 9. Honest boundaries (pre-declared)

- T1 is still a fixpoint family (alternating, not the 4-chain);
  oscillatory, convergent-signal, and multi-structure feedback cycles
  remain untested.
- exp is still supplied for end-to-end verification; the tests target
  the proposal space and the halting vocabulary.
- SEQMAX=8/CAP=8 remain frozen researcher bounds, not learned values.
- T3's extension is additive and separately reduction-tested; the
  frozen gc_uni.zag is byte-untouched. Whether HALT-kind belongs in the
  protected core is a governance question for Micah, not decided here.
- T2's strict-necessity claim is relative to the frozen trial order
  (increasing k, lexicographic); it shows the (b)-halt firing at i<k
  with the alternative continuation provably missing.
