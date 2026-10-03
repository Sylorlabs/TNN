# PREREG: NT-RESIDUAL -- the rare-but-useful link that is NOT a revision target

## 1. Question

NT-NONLOCAL (FIX-CLEAN) showed D5's revision-target pinning fixes
last-order K=6 (avail 0->4) via a non-entry-local,
learner-available, forward-looking signal: the learner knows its
belief about link 100 is heading toward 148, so near-future q(100)
queries will need 148's link -- known before any query succeeds
through 148. Its stated honest limitation: "It is NOT a usefulness
detector: a useful link that is never a contradiction target gets
no protection." Recommended follow-up #1: "The residual case:
rare-but-useful link that is NOT a revision target (D5 doesn't
cover it) -- signal must come from teaching/query stream, not the
stored graph (in-degree is 0 pre-revision)."

This lane runs that case:

(a) Does D5 protect a genuinely useful (queried every pass) link
    that is NEVER the target of a contradiction? Predicted: NO.
(b) In the same run, does D5 still protect the revision-target
    link 148 (the dissociation: D5 active and working, yet the
    residual link dies)? Predicted: YES (avail100=4, avail160=0).
(c) Is there any learner-available signal (no oracle, no task
    labels) in the teaching/query stream that could have predicted
    the residual link's future usefulness at the decision point --
    or is it fundamentally impossible in this workload? Predicted:
    IMPOSSIBLE (Section 5.4): at the pass-1 eviction decisions the
    residual entries are entry-locally identical to doomed FREQ
    novels (sup1,ref0,F1,R0), are never contradiction targets (no
    pin), have zero query history (the first probe comes after the
    eviction), and zero stored-graph in-degree. The only
    distinction is the FUTURE query schedule, which is oracle
    knowledge. The one operative query-stream signal (D4 reads)
    would protect the link only if it survived to its first read --
    which it does not.

## 2. Subject (frozen)

The NT-NONLOCAL subject verbatim (continuing-learner skeleton,
associative instance memory, sequential lifetime phases, single
main(), no resets, no task labels): D1 preserved, D4 base
comparator kept, D5 = D4 + revision-target pinning via per-slot
pendtgt (set on ref++, cleared on revision/install/restore;
pin-aware victim scan with D4 fallback). Slot fields, evidence
update, reinf/reads semantics, predict, 2-hop q(s), CAP=20 --
all NTNL Section 2 verbatim. The ONLY novelty vs NT-NONLOCAL is
the workload's two extra keys (160, 161) and one extra per-pass
probe (q(160) vs 162). The learner is byte-for-byte the D5
learner; the RULE under test is unchanged.

## 3. Workload (frozen numeric inventory; opaque identifiers)

NT-LOWVALUE-BOUNDARY Section 3 verbatim (Family A: 14 links, 8
chains, QS = {100,103,104,107,108,111,114,117}, ANSA =
{102,102,106,106,110,113,116,119}), PLUS two residual keys:

- RESIDUAL chain (the residual case): link (160,1)->161 and link
  (161,1)->162, taught on pass p iff (p-1) mod K == 0 (i.e. pass 1
  only at K=6), AGREE-ONLY, taught LAST in the pass order (just
  before the RARE 148 teaching). NEVER contradicted anywhere in
  the workload: no ref++ ever has taught obj 160 or 161, so no
  pendtgt ever points at them and D5's pin never fires for them.
  They are genuinely useful: the per-pass probe q(160) expects
  162 every pass (160->161->162), and the post-pass-6 retest
  includes resprobe = (q(160)==162).
- RARE (148,1)->152: as NTNL (taught LAST on K-passes).

Phase-2 teachings per pass, single arm order LAST (the NTLV
liability case), ascending subj with 160,161 inserted before
148:
- C (contradicted), every pass: (100,1)->148, (104,1)->130;
- NC (agreed), every pass: (101,1)->102, (105,1)->106;
- FREQ (frequent novel), every pass: (130,1)->131, (131,1)->132,
  (140,1)->141, (141,1)->142, (143,1)->144, (144,1)->145;
- RESIDUAL, on pass p iff (p-1) mod K == 0, agree-only, taught
  LAST: (160,1)->161, (161,1)->162;
- RARE, on pass p iff (p-1) mod K == 0, taught very last:
  (148,1)->152.

ANSB: q(100) -> 152, q(104) -> 131, all others ANSA; q(160) ->
162 (new). Retest partitions: C: starts 100, 104 (correct:
ANSB). NC: starts 103, 107 (correct: ANSA). U: starts 108, 111,
114, 117 (correct: ANSA). resprobe: q(160)==162. FORGET = C
queries answering neither ANSA nor ANSB, plus NC/U queries
answering not-ANSA.

Capacity accounting: 14 A links + 9 novel subjs
(130,131,140,141,143,144,148,160,161) = 23 distinct (subj,rel)
keys > CAP 20. Pressure ratio 23/20 = 1.15x. Exactly 3 keys must
be absent at any time; any absence pattern beyond that, and WHICH
keys are absent, is attributable to the rules.

Arms: ONE arm, R6 (K=6, LAST, RESIDUAL taught pass 1 only).
M = 6 phase-2 passes, fixed. (The dissociation -- D5 working on
148 while failing 160/161 -- is measured within this single
run; no second arm is needed to answer (a)-(c).)

## 4. Protocol (frozen)

NT-LOWVALUE-BOUNDARY Section 4 verbatim, with the additions:
- `trainA`: repeat passes over the 14 A links (ascending subj);
  after each pass probe the 8 queries. Criterion = 8/8 correct
  for 2 consecutive passes. Max 50 passes. Predicted: ttcA = 2,
  probeA = 8 (phase 1 is NTNL-verbatim; the residual keys are
  absent from phase 1).
- Phase 2: 6 FIXED passes. Per pass, teachings in LAST order
  (Section 3). After EACH pass, probe q(100) vs 152 (the
  D5-covered usefulness probe) AND q(160) vs 162 (the residual
  usefulness probe). Both probes are read-only w.r.t. knowledge
  but DO increment reads (the Section 2 disclosure). avail100 =
  passes p in {3,4,5,6} with q(100)==152; avail160 = passes p in
  {3,4,5,6} with q(160)==162.
- After pass 6: NTPP-style retest (c/nc/u/forget); bprobe =
  (q(130)==132) + (q(140)==142) + (q(143)==145), /3; resprobe =
  (q(160)==162), /1; record nevict, per-subj eviction histogram
  (bins 100..165), phev (evictions of subjs 100..119),
  evh(148), evh(118), evh(160), evh(161).

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Notation: R = reads, F = reinf, I = ins, P = pinned. Phase 1
(NTNL-verbatim): A-links occupy slots 0..13, I 1..14,
(sup=2,ref=0,F=2); R: 100:2, 101:4, 103:2, 104:2, 105:4, 107:2,
108:2, 109:2, 111:2, 112:2, 114:2, 115:2, 117:2, 118:2.
pendtgt all 0.

### 5.1 Arm R6 (K=6; RARE+RESIDUAL on pass 1 only, taught LAST)

Pass 1: 100 -> ref=1 (F3), pt[100]=148; 101 -> sup=3; 104 ->
ref=1, pt[104]=130; 105 -> sup=3. Novels fresh:
130(15,R0,F1,PINNED via pt[104]), 131(16), 140(17), 141(18),
143(19), 144(20). (160,1)->161: 21st key -> evict: R=0
non-pinned {131(16),140(17),141(18),143(19),144(20)} (130
pinned) -> max I -> 144(20). Install 160 (I21,R0,F1).
(161,1)->162: 21st key -> evict: R=0 non-pinned
{131(16),140(17),141(18),143(19),160(21)} -> max I -> 160(21).
Install 161 (I22,R0,F1). (148,1)->152: 21st key -> evict: R=0
non-pinned {131(16),140(17),141(18),143(19),161(22)} -> max I
-> 161(22). Install 148 (I23,R0,F1; PINNED via pt[100]).
Absent: 144,160,161. nevict=3. Probe q(100) MISS (100->101;
R100 2->3, R101 4->5). Probe q(160) MISS (160 absent). THE
RESIDUAL DECISION: at all three eviction points the residual
entries are (sup1,ref0,F1,R0) -- entry-locally identical to
the FREQ novels -- and no pin covers them; the max-ins
tie-break takes the youngest, i.e. the residual links
themselves. They die before the first q(160) probe.

Pass 2 (no RARE/RESIDUAL): 100 -> ref=2, pt[100]=148; 104 ->
ref=2, pt[104]=130; 101,105 -> sup=4. Novels 130,131,140,141,
143 -> sup=2,F=2. 144 absent -> D1-restore (F1->2, sup=2) ->
evict: R=0 non-pinned {131(16),140(17),141(18),143(19)}
(130,148 pinned) -> max I -> 143(19). Install 144 (I24).
Absent: 143,160,161. nevict=1. Probes: q(100) MISS
(sup2,ref2 -> -1); q(160) MISS (160 absent, never restored --
never re-taught).

Pass 3: 100 -> REVISE ->148 (sup1,ref0,F5), pt[100]=0; 104 ->
REVISE ->130 (F5), pt[104]=0. 101,105 -> sup=5. Novels
130,131,140,141 -> sup=3,F=3. 143 absent -> restore (F2->3,
sup=3) -> evict: R=0 {130(15),131(16),140(17),141(18),148(23),
144(24)}, no pins -> max I -> 144(24). Install 143 (I25).
144 absent -> restore (F2->3, sup=3) -> evict: R=0
{130,131,140,141,148,143(25)} -> 143(25). Install 144 (I26).
Absent: 143,160,161. nevict=2. Probe q(100) HIT: 100->148
(R100 3->4), 148->152 (R148 0->1). Probe q(160) MISS.

Pass 4: 100,104,101,105 hits. Novels 130,131,140,141 ->
sup=4,F=4. 143 absent -> restore (F3->4) -> evict: R=0
{130(15),131(16),140(17),141(18),148(23,R1),144(26)} -> max I
-> 144(26). Install 143 (I27). 144 absent -> restore (F3->4)
-> evict: R=0 {130,131,140,141,148,143(27)} -> 143(27).
Install 144 (I28). Absent: 143,160,161. nevict=2. Probes:
q(100) HIT (R148 1->2); q(160) MISS.

Pass 5: as pass 4 (2 evictions: 144,143). q(100) HIT (R148
2->3); q(160) MISS. Pass 6: as pass 4 (2 evictions: 144,143).
q(100) HIT (R148 3->4); q(160) MISS.

Frozen R6: ttcA=2, probeA=8, nevict=12, phev=0. EVHIST: 143=5
(passes 2,3,4,5,6), 144=5 (passes 1,3,4,5,6), 160=1 (pass 1),
161=1 (pass 1). Sum=12. Per-pass q(100)==152: 0,0,1,1,1,1 ->
avail100=4. Per-pass q(160)==162: 0,0,0,0,0,0 -> avail160=0.
Retest: c=2/2 (q100=152 via 148 sup=4; q104=131); nc=2/2;
u=4/4; forget=0. bprobe=2/3 (q143: 143 absent -> -1).
resprobe=0/1. evh(148)=0, evh(118)=0, evh(160)=1, evh(161)=1.

### 5.2 Predicted mechanism (directional: RESIDUAL-CONFIRMED)

D5 is active in this run and works exactly as in NTNL on the
revision-target link: the pass-1/2 pins on 148 and 130 hold,
evh(148)=0, avail100=4 (D4's L6 gave avail100=0). The residual
links 160/161 are evicted on pass 1 before the first q(160)
probe reads them, and are never re-taught (K=6, pass-1-only),
so they never return: avail160=0, resprobe=0. The dissociation
is the finding: the pin protects "where my beliefs are
heading" and nothing else; a useful link that is never a
contradiction target gets zero D5 protection, as the NTNL
honest limitation stated.

### 5.3 Why no learner-available signal could have predicted it
### (frozen interpretive prediction for the REPORT)

At the three pass-1 eviction decision points, the learner's
entire information about 160/161 is: taught once, agreed,
(sup1,ref0,F1,R0), installed youngest. The FREQ novels
131/140/141/143 are (sup1,ref0,F1,R0), installed older. No
contradiction has ever targeted 160 or 161 (no pin possible --
pins are set only by ref++). The query stream has not touched
them (first probe comes after the pass-1 teachings). The stored
graph has in-degree 0 for both (nothing installed points at
them; 160's role as a future query start is harness knowledge,
not learner state). The ONLY distinguishing fact -- "q(160)
will be probed every future pass" -- is oracle knowledge. The
one learner-available query-stream signal that protects
useful-but-rare links, D4's read count, requires surviving to
the first read; the residual link does not. Hence: in this
workload the residual case is fundamentally unpredicted by any
learner-available signal, and the REPORT will record that as
the finding rather than propose a patch. (A follow-up lane
could test whether a teaching-stream association signal --
e.g. protecting keys taught adjacent to a query start -- works,
but that requires a world where the teaching stream carries the
dependence; this workload deliberately does not provide it.)

## 6. Assembly, build, run (frozen)

- Single source file `ntres_full.zag`: the NTNL learner
  verbatim (D1 + D4 base + D5 pin via pendtgt; canonical
  helpers copied from the frozen ntnl template), oracles
  extended only by the RESIDUAL teachings in teachB (K-pass,
  LAST, agree-only, (160,1)->161 and (161,1)->162 inserted
  before the RARE 148 teaching) and the q(160) probe; retest
  extended by resprobe; EVHIST extended to bins 100..165;
  output adds per-pass q160 flags r1..r6, avail160, resprobe,
  evh(160), evh(161), and the K1..K7 bits plus verdict line.
  Tag NTRES. Single arm R6.
- Build: `znc ntres_full.zag -o ntres_bin` under safebin-only
  PATH.
- Run `ntres_bin` 3 times; outputs `ntres_run1.txt`,
  `ntres_run2.txt`, `ntres_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic
  output only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the
  frozen NTNL template shapes; no `[]u8 as *u8` casts (thread
  `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8.
  Else VOID.
- K2 (retention of uncontested structure): nc = 2 AND u = 4.
- K3 (the residual bar): avail160 = 0 (exact; Section 5.1).
- K4 (final revision outcome): c = 2 AND forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 12 (exact); evh(148) = 0 AND
  evh(118) = 0 (the D5 pin still holds on the revision target);
  evh(160) = 1 AND evh(161) = 1 (white-box: the residual links
  ARE the pass-1 victims); phev = 0.
- K6 (discriminative validity): avail100 = 4 (the D5-covered
  probe passes when its link is present; not a broken probe)
  AND nevict > 0 (pressure actually exercised).
- K7 (the dissociation bar; the lane's headline): avail100
  = 4 AND avail160 = 0 in the same run (D5 active and working
  on the revision target while providing zero protection to
  the residual link).

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated).
- K3 = 0 -> NO-RESIDUAL: the residual link survived (avail160
  > 0); the honest limitation does not reproduce in this
  workload. REPORT characterizes the actual curve.
- K7 = 0 -> DISSOCIATION-BROKEN: either D5 failed the
  revision-target link too, or it covered the residual link;
  the dissociation did not hold. REPORT characterizes.
- K2 = 0 -> FIX-WITH-COST: unexpected retention cost.
- else -> RESIDUAL-CONFIRMED: D5 provides zero protection to
  the rare-but-useful non-revision-target link (avail160=0,
  evh(160)=evh(161)=1) while fixing the revision-target link
  in the same run (avail100=4, evh(148)=0); and no
  learner-available signal in this workload could have
  predicted the residual link's usefulness (Section 5.3).

Predicted verdict: RESIDUAL-CONFIRMED (K1-K7 all 1).

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
- Single capacity point (CAP=20, 1.15x); single contradiction
  magnitude; M=6 fixed; single arm (K=6, LAST).
- The residual teachings are agree-only and pass-1-only by
  construction; the lane tests D5's coverage limit, not a new
  protection rule. No new eviction rule is proposed or tested
  here.
- The Section 5.3 impossibility claim is workload-relative: it
  says no learner-available signal in THIS workload predicts
  the residual link, not that no signal could exist in any
  workload. A teaching stream that carries the dependence (or
  a query stream the link survives to meet) would change the
  analysis; that is a new lane, not an amendment.
- D1 checkpoints for 160/161 exist (evidence preserved) but are
  never consulted (never re-taught): the failure mode is
  PRESENCE, not evidence loss, as in NTLV/NTFQ/NTUE/NTNL.
- New rule = new lane: D1/D2/D3/D4/D5 and their lanes are
  untouched by this work.
