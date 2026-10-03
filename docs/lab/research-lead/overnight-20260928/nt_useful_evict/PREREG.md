# PREREG: NT-USEFUL-EVICT -- a usefulness-aware eviction rule (D4) with a learner-available read/query signal

## 1. Question

NT-LOWVALUE-BOUNDARY (LIABILITY-CONFIRMED) showed D2's evict-youngest
is a liability for useful-but-infrequently-reinforced links.
NT-ORDER-MIRROR (MIRROR-CONFIRMED) showed installation recency, not
frequency, is D2's true determinant. NT-FREQ-EVICT (FIX-WITH-COST)
showed D3 (evict-least-frequently-reinforced) fixes K=2,3
(avail 4/4/3/0 vs D2's 4/2/1/0) but NOT K=6 (0/4), at the cost of one
phase-1 sleeper (u=3/4): the liability moves from "young" to
"infrequent" and is not eliminated. NTFQ's honest conclusion: "No
entry-local statistic (recency OR frequency) can protect a
useful-but-rarest link -- that needs a usefulness/relevance signal
the learner doesn't have." NTFQ's recommended (not preregistered)
follow-up: "a usefulness-aware rule with a learner-available
relevance signal (e.g. read/query frequency), which should pin 148
in both teach orders AND at K=6 -- a new lane, not an amendment."
This is that lane.

Questions:

(a) Does a usefulness-aware eviction rule (D4: evict the
    least-read entry, where "read" = the entry contributed an
    answer to a query) pin the RARE link (148,1)->152 when it is
    taught LAST (the NTLV liability case) and when it is taught
    FIRST (the NTOM mirror case)?
(b) Does it pin 148 at K=6 (taught once), the case D2 and D3 both
    fail, in either teach order?
(c) What are the tradeoffs vs D3 -- retention of uncontested
    phase-1 knowledge (u, phev), total eviction churn (nevict),
    final revision outcome (c/forget)?

Mechanism under test (derived from the frozen rules, not a new
hypothesis): the per-pass probe q(100) is a QUERY. After the
pass-3 revision (100->148), q(100) = 100 -> 148 -> 152 routes
through the RARE link, so 148 accumulates reads (R=1 after the
pass-3 probe, growing each pass). D4 evicts min-reads, so once 148
has been read it is protected: the churn is redirected onto the
never-read FREQ novels. Phase-1 sleepers were read during phase-1
probeA (R>=2), so unlike D3, D4 sacrifices no uncontested old
knowledge. Predicted signature: avail 4/4/3/0 last-order and
4/4/4/4 first-order; u=4/4 and phev=0 on all 8 arms; but last-order
K=6 is NOT fixed (avail 0): the taught-once RARE link is evicted on
pass 2 before any query can route through it (R=0), so no
entry-local usefulness statistic can distinguish it from the other
novels. The K=6 bar (K7) is therefore predicted to FAIL on the
last-order arm while PASSING on the first-order arm -- the exact
discrimination the follow-up hypothesis needs.

## 2. Subject (frozen)

The NT-LOWVALUE-BOUNDARY / NT-FREQ-EVICT subject verbatim
(continuing-learner skeleton, associative instance memory,
sequential lifetime phases, single main(), no resets, no task
labels), with D1 kept, D2/D3 REPLACED by D4. Slot fields (40
bytes): 0 subj, 4 rel, 8 obj, 12 dom, 16 valid, 20 sup, 24 ref,
28 ins, 32 reinf, 36 reads. Key = (subj, rel). rel = 1
throughout. `dom` = install-phase provenance, stamped on every
installation; entry metadata, never consulted by learner
decisions. Arena holds nentries, nevict, ins_seq, nslots.

- Evidence update (NT-frozen rule): on a teaching event for a
  PRESENT entry, taught obj matches stored obj -> sup++; taught obj
  differs -> ref++, and if ref > sup -> REVISE to (new obj, sup=1,
  ref=0), in place. Revision does NOT touch `ins`, `reinf`, or
  `reads`.
- reinf (kept from NTFQ): counts teaching events for the installed
  key. Fresh installation -> reinf=1. Teaching event for a present
  entry -> reinf++. D1-restore+update -> checkpointed reinf
  restored, then reinf++. Revision does not reset reinf. PRESERVED
  by D1 but NOT consulted by D4's comparator (documented dead
  weight kept for D1 continuity; the comparator uses reads+ins
  only).
- reads (NEW, the usefulness signal): counts queries the entry
  contributed an answer to. Incremented in cl_predict when the
  entry is found AND sup > ref (the stored obj is returned).
  Learner-local: the learner observes its own query traffic; no
  oracle, no task identity, no correctness judgment (the learner
  cannot know whether an answer was "correct", only that the entry
  produced one). Fresh installation -> reads=0. D1-restore ->
  checkpointed reads restored.
- D1 (preserve-evidence, kept, extended by one field): on
  eviction, checkpoint (valid=1, obj, sup, ref, reinf, reads)
  keyed by subj. On insertion of an absent key with a valid
  checkpoint, install the checkpointed (obj, sup, ref, reinf,
  reads), stamp dom = current phase, then run the frozen update
  step with the taught obj. On insertion with no valid
  checkpoint, install fresh (taught obj, sup=1, ref=0, reinf=1,
  reads=0). Checkpoint entries are overwritten on each eviction
  (latest state wins) and never cleared on restore.
- D4 (evict-least-read; REPLACES D2/D3): arena holds `ins_seq`,
  zero-initialized. On EVERY installation (fresh and D1-restore
  alike): ins_seq++, slot.ins = ins_seq. Eviction victim =
  occupied slot with MINIMUM `reads`; tie-break = MAXIMUM `ins`
  (youngest among the least-read). `ins` unique per installation;
  no further tie-break needed. Revision in place touches neither
  `ins`, `reinf`, nor `reads`; eviction does not touch survivors.
- Rationale for the tie-break (frozen, load-bearing, disclosed):
  among entries with equal (zero) demonstrated usefulness, evict
  the most recently installed: older entries have survived prior
  eviction rounds (tenure as weak evidence). This is D2's
  comparator demoted to the tie-break, exactly as NTFQ demoted D2
  under D3 -- so the lineage D2 (recency primary) -> D3
  (frequency primary, recency tie-break) -> D4 (usefulness
  primary, recency tie-break) isolates the primary signal. The
  alternative tie-break (min ins / FIFO) is NOT tested here; it
  would evict the first-taught RARE link on pass 1 of the mirror
  (traced: avail 0/0/0/0 first-order) and is recorded as a
  boundary.
- Predict: entry present and sup > ref -> stored obj (and
  reads++); else -1 (no reads++).
- 2-hop query q(s): p1 = predict(s,1); if p1 < 0 -> -1;
  p2 = predict(p1,1); if p2 < 0 -> -1; else p2. The chaining
  procedure is fixed machinery; the KNOWLEDGE (links) is learned.
  No semantic labels anywhere; nodes/links are bare integers.
- Capacity CAP = 20 slots. The comparator is generic: per-entry
  read count plus installation order only; no task identity, no
  importance flags, no protection rules, no modes, no
  researcher-provided usefulness labels.

PROBE DISCLOSURE (load-bearing): the per-pass probe q(100) is
read-only with respect to learned KNOWLEDGE (no cl_learn, no
revision, no re-installation, no sup/ref/ins/reinf change). But
the reads counter IS incremented by queries -- observing query
traffic is precisely the signal under test, and the probe is a
query like any other. Counting it does not teach anything. This
is the D4 signal; without it D4 would have no reads at all.

The ONLY novelty vs NT-FREQ-EVICT is the eviction comparator (D4
for D3), the one extra slot/checkpoint field it needs, and the
read-counting in cl_predict. Workload inventory, oracles, and the
D1 machinery are verbatim; teach order is parameterized
(RARE-first vs RARE-last) per NT-ORDER-MIRROR.

## 3. Workload (frozen numeric inventory; opaque identifiers)

NT-LOWVALUE-BOUNDARY Section 3 verbatim. Family A: 14 links, 8
chains with shared substructure: 100->101, 101->102, 103->101,
104->105, 105->106, 107->105, 108->109, 109->110, 111->112,
112->113, 114->115, 115->116, 117->118, 118->119. Query starts QS
= {100,103,104,107,108,111,114,117}. ANSA =
{102,102,106,106,110,113,116,119}.

Phase-2 teachings per pass, two orders (order is the arm
parameter, a harness condition, not a cognitive mode):
- LAST (the NTLV liability case): ascending subj order --
  C (contradicted), every pass: (100,1)->148, (104,1)->130;
  NC (agreed), every pass: (101,1)->102, (105,1)->106;
  FREQ (frequent novel), every pass: (130,1)->131, (131,1)->132,
  (140,1)->141, (141,1)->142, (143,1)->144, (144,1)->145;
  RARE, on pass p iff (p-1) mod K == 0, taught LAST: (148,1)->152.
- FIRST (the NTOM mirror case): RARE taught FIRST on pass p iff
  (p-1) mod K == 0: (148,1)->152; then the rest ascending:
  100, 101, 104, 105, 130, 131, 140, 141, 143, 144.

ANSB: q(100) -> 152, q(104) -> 131, all others ANSA.

Retest partitions: C: starts 100, 104 (correct: ANSB). NC: starts
103, 107 (correct: ANSA). U: starts 108, 111, 114, 117 (correct:
ANSA). FORGET = C queries answering neither ANSA nor ANSB, plus
NC/U queries answering not-ANSA (absent link -> -1 counts as
forgotten).

Capacity accounting: 14 A links + 7 novel subjs
(130,131,140,141,143,144,148) = 21 distinct (subj,rel) keys >
CAP 20. Pressure ratio 21/20 = 1.05x. Exactly 1 key must be
absent at any time; any absence pattern beyond that, and WHICH
key is absent, is attributable to the rules.

Arms (each on a FRESH learner): L1 (K=1, LAST), L2 (K=2, LAST),
L3 (K=3, LAST), L6 (K=6, LAST), F1 (K=1, FIRST), F2 (K=2, FIRST),
F3 (K=3, FIRST), F6 (K=6, FIRST). M = 6 phase-2 passes, fixed,
all arms.

## 4. Protocol (frozen)

NT-LOWVALUE-BOUNDARY Section 4 verbatim, parameterized by order:
- `trainA`: repeat passes over the 14 A links (ascending subj);
  after each pass probe the 8 queries. Criterion = 8/8 correct
  for 2 consecutive passes. Max 50 passes (fail-safe; hitting it
  = arm FAIL). Returns passes used. Predicted: ttcA = 2,
  probeA = 8, all arms.
- Phase 2: 6 FIXED passes. Per pass, teachings in the arm's
  order (Section 3). After EACH pass, probe q(100) vs 152 (the
  RARE-usefulness probe; read-only w.r.t. knowledge per the
  Section 2 disclosure; it DOES increment reads). avail(K,order)
  = number of passes p in {3,4,5,6} with q(100) == 152.
- After pass 6: NTPP-style retest (c/nc/u/forget); bprobe =
  (q(130)==132) + (q(140)==142) + (q(143)==145), /3; record
  nevict, per-subj eviction histogram (bins 100..150), phev
  (evictions of subjs 100..119), evh(148), evh(118).

## 5. Frozen predictions (hand-derived by tracing the frozen rules)

Notation: R = reads, F = reinf, I = ins. A-links occupy slots
0..13, I 1..14, all (sup=2, ref=0, F=2) after phase 1. Phase-1
probeA ran twice (ttcA=2), so R: 100:2, 101:4, 103:2, 104:2,
105:4, 107:2, 108:2, 109:2, 111:2, 112:2, 114:2, 115:2, 117:2,
118:2. Novel slots 14..19. D4 victim = min R, tie-break max I.

### 5.1 Arm L1 (K=1; RARE every pass, taught LAST)

Pass 1: 100 -> ref=1 (F3); 101 -> sup=3; 104 -> ref=1; 105 ->
sup=3. Novel: 130(15),131(16),140(17),141(18),143(19),144(20)
fresh (R0,F1). 148 -> full -> evict min R (novels R0), max I ->
144(20). Install 148 (I21,R0,F1). Probe q(100): 100->101
(R100 2->3), 101->102 (R101 4->5). MISS. Absent: 144. nevict=1.

Pass 2: 100 -> ref=2; 104 -> ref=2; 101,105 -> sup=4 (F4).
130,131,140,141,143 present -> sup=2, F2. 144 absent -> restore
(145,1,0,F1,R0) -> sup=2,F2; evict min R=0 max I: {148(21),
130(15),131(16),140(17),141(18),143(19)} -> 148(21). Install
144 (I22). 148 absent -> restore (152,1,0,F1,R0) -> sup=2,F2;
evict: {144(22),130(15),...} -> 144(22). Install 148 (I23,R0).
Absent: 144. nevict=2. Probe: predict(100): sup2,ref2 -> -1.
MISS.

Pass 3: 100 -> REVISE ->148 (sup1,ref0,F5). 104 -> REVISE ->130
(F5). 101,105 -> sup=5. 130,131,140,141,143 -> sup=3,F3. 144
absent -> restore -> sup=3,F3; evict: {148(23,R0),130(15),...}
-> 148(23). Install 144 (I24). 148 absent -> restore -> sup=3,
F3,R0; evict: {144(24),...} -> 144(24). Install 148 (I25,R0).
Absent: 144. nevict=2. Probe: 100->148 (R100 3->4),
148->152 (sup3>0, R148 0->1). HIT.

Pass 4: 100,104,101,105 hits. 130,131,140,141,143 hits. 144
absent -> restore; evict min R=0 max I: 148 has R1 now, so
{143(19),141(18),140(17),131(16),130(15)} -> 143(19). Install
144 (I26). 143 absent -> restore; evict: {144(26),...} ->
144(26). Install 143 (I27). 148 present -> HIT (sup4). Absent:
144. nevict=2. Probe HIT (R148 1->2).

Pass 5: as pass 4 (2 evictions: 143,144). Probe HIT (R148 2->3).
Pass 6: as pass 4 (2 evictions). Probe HIT (R148 3->4).

Frozen L1: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST:
144=6 (pass 1 once + passes 2-6 once each), 148=2 (passes 2,3),
143=3 (passes 4,5,6). Sum=11. Per-pass q(100)==152:
0,0,1,1,1,1 -> avail=4. Retest: c=2/2 (q100=152 via present
148; q104=131); nc=2/2; u=4/4; forget=0. bprobe=2/3 (q130 OK,
q140 OK, q143: 144 absent -> -1). evh(148)=2, evh(118)=0.

### 5.2 Arm L2 (K=2; RARE on passes 1,3,5, taught LAST)

Pass 1: as L1. nevict=1. Absent: 144. Probe MISS.
Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2; 101,105 -> sup=4.
130,131,140,141,143 -> sup=2,F2. 144 absent -> restore; evict
min R=0 max I -> 148(21) (R0). Install 144 (I22). Absent: 148.
nevict=1. Probe: predict(100): sup2,ref2 -> -1. MISS.
Pass 3 (148): 100 -> REVISE ->148 (F5); 104 -> REVISE ->130.
101,105 -> sup=5. Novels 130..144 present -> hits (sup3,F3).
148 absent -> restore (152,1,0,F1,R0) -> sup=2,F2; evict:
{144(22),130(15),...} -> 144(22). Install 148 (I23,R0).
Absent: 144. nevict=1. Probe HIT (R148 0->1).
Pass 4 (no 148): 100,104 -> sup=2; 101,105 -> sup=6. Novels
hits. 144 absent -> restore; evict: 148 has R1, so
{143(19),...} -> 143(19). Install 144 (I24). 143 absent ->
restore; evict -> 144(24). Install 143 (I25). 148 present ->
HIT. Absent: 144. nevict=2. Probe HIT (R148 1->2).
Pass 5 (148): 148 present -> HIT (sup3). 144 absent -> restore;
evict -> 143(25). Install 144 (I26). 143 -> restore; evict ->
144(26). Install 143 (I27). Absent: 144. nevict=2. Probe HIT
(R148 2->3).
Pass 6 (no 148): 144 -> restore; evict -> 143(27). Install 144
(I28). 143 -> restore; evict -> 144(28). Install 143 (I29).
Absent: 144. nevict=2. Probe HIT (R148 3->4).

Frozen L2: ttcA=2, probeA=8, nevict=9, phev=0. EVHIST: 144=5,
148=1 (pass 2), 143=3. Sum=9. Per-pass: 0,0,1,1,1,1 -> avail=4.
Retest: c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3. evh(148)=1,
evh(118)=0.

### 5.3 Arm L3 (K=3; RARE on passes 1,4, taught LAST)

Pass 1: as L1. nevict=1. Absent: 144. MISS.
Pass 2 (no 148): 144 -> restore; evict -> 148(21). Install 144
(I22). Absent: 148. nevict=1. Probe: predict(100): sup2,ref2
-> -1. MISS.
Pass 3 (no 148): 100 -> REVISE ->148 (F5); 104 -> REVISE ->130.
Novels 130..144 present -> hits. No evictions. Probe:
predict(100)=148 (R100+1), predict(148): absent -> -1. MISS.
Pass 4 (148): novels hits. 148 absent -> restore; evict:
{144(22),130(15),...} -> 144(22). Install 148 (I23,R0).
Absent: 144. nevict=1. Probe HIT (R148 0->1).
Pass 5 (no 148): 144 -> restore; evict (148 R1): -> 143(19).
Install 144 (I24). 143 -> restore; evict -> 144(24). Install
143 (I25). Absent: 144. nevict=2. Probe HIT (R148 1->2).
Pass 6 (no 148): 144 -> restore; evict -> 143(25). Install 144
(I26). 143 -> restore; evict -> 144(26). Install 143 (I27).
Absent: 144. nevict=2. Probe HIT (R148 2->3).

Frozen L3: ttcA=2, probeA=8, nevict=7, phev=0. EVHIST: 144=4,
148=1, 143=2. Sum=7. Per-pass: 0,0,0,1,1,1 -> avail=3. Retest:
c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3. evh(148)=1,
evh(118)=0.

### 5.4 Arm L6 (K=6; RARE on pass 1 only, taught LAST)

Pass 1: as L1. nevict=1. Absent: 144. MISS.
Pass 2 (no 148): 144 -> restore; evict min R=0 max I ->
148(21) (R0, never read: the pass-1 probe routed 100->101).
Install 144 (I22). Absent: 148. nevict=1. Probe:
predict(100): sup2,ref2 -> -1. MISS.
Pass 3: 100 -> REVISE ->148 (F5); 104 -> REVISE ->130. Novels
130..144 present -> hits. No evictions. Probe:
predict(100)=148, predict(148): absent -> -1. MISS.
Passes 4-6: all hits, no evictions. Probes MISS (148 absent).

Frozen L6: ttcA=2, probeA=8, nevict=2, phev=0. EVHIST: 144=1,
148=1. Sum=2. Per-pass: 0,0,0,0,0,0 -> avail=0. Retest: c=1/2
(q100: 148 absent -> -1, neither 102 nor 152; q104=131);
nc=2/2; u=4/4; forget=1. bprobe=3/3 (all FREQ novels present).
evh(148)=1, evh(118)=0.

MECHANISM NOTE (5.4): at the pass-2 eviction, 148 is
entry-locally identical to the other novels (R=0, F=1): no
query has ever routed through it (the pass-1 probe went
100->101->102), so the read signal cannot distinguish it. Six
restores need six victims; a min-reads rule never sacrifices a
read (R>=2) sleeper for an unread novel, so 148 is necessarily
among the victims. No entry-local usefulness statistic fixes
this; only a non-entry-local signal (e.g. downstream query
dependence known before the query succeeds) could.

### 5.5 Arm F1 (K=1; RARE every pass, taught FIRST)

Pass 1: 148 fresh (I15,R0,F1). 100 -> ref=1; 104 -> ref=1;
101,105 -> sup=3. Novel: 130(16),131(17),140(18),141(19),
143(20) fresh. 144 -> full -> evict min R=0 max I -> 143(20)
(the max-ins tie-break spares the first-installed 148).
Install 144 (I21). Absent: 143. nevict=1. Probe MISS
(100->101->102).
Pass 2: 148 present -> HIT (sup2,F2). 100 -> ref=2; 104 ->
ref=2; 101,105 -> sup=4. 130,131,140,141,144 -> sup=2,F2. 143
absent -> restore -> sup=2,F2; evict: {144(21),148(15),...} ->
144(21). Install 143 (I22). 144 absent -> restore; evict:
{143(22),...} -> 143(22). Install 144 (I23). Absent: 143.
nevict=2. Probe: predict(100): sup2,ref2 -> -1. MISS.
Pass 3: 148 -> HIT (sup3). 100 -> REVISE ->148 (F5); 104 ->
REVISE ->130. 143 -> restore; evict -> 144(23). Install 143
(I24). 144 -> restore; evict -> 143(24). Install 144 (I25).
Absent: 143. nevict=2. Probe: 100->148 (R100 3->4), 148->152
(sup3>0, R148 0->1). HIT.
Pass 4: 148 -> HIT (sup4). 143 -> restore; evict (148 R1):
{144(25),...} -> 144(25). Install 143 (I26). 144 -> restore;
evict -> 143(26). Install 143 (I27). Absent: 143. nevict=2.
Probe HIT (R148 1->2).
Pass 5,6: as pass 4 (2 evictions each). Probes HIT (R148 2->3,
3->4).

Frozen F1: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6
(pass 1 once + passes 2-6 once each), 144=5 (passes 2-6 once
each). evh(148)=0: the RARE link is NEVER the D4 victim.
Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2;
nc=2/2; u=4/4; forget=0. bprobe=2/3 (q143: 143 absent -> -1).
evh(118)=0.

### 5.6 Arm F2 (K=2; RARE on passes 1,3,5, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2 (no 148): 100 -> ref=2; 104 -> ref=2. 148 untouched.
143 -> restore; evict -> 144(21). Install 143 (I22). 144 ->
restore; evict -> 143(22). Install 144 (I23). nevict=2. Probe:
predict(100): sup2,ref2 -> -1. MISS.
Pass 3 (148): 148 -> HIT (sup2). 100 -> REVISE ->148; 104 ->
REVISE ->130. 143 -> restore; evict -> 144(23). Install 143
(I24). 144 -> restore; evict -> 143(24). Install 144 (I25).
nevict=2. Probe HIT (R148 0->1).
Pass 4 (no 148): 148 untouched (sup2,R1). 143 -> restore;
evict (148 R1): -> 144(25). Install 143 (I26). 144 -> restore;
evict -> 143(26). Install 144 (I27). nevict=2. Probe:
100->148 (sup2), 148->152 (sup2, R148 1->2). HIT.
Pass 5 (148): 148 -> HIT (sup3). 143/144 revolve (2). Probe
HIT (R148 2->3).
Pass 6 (no 148): 143/144 revolve (2). Probe HIT (R148 3->4).

Frozen F2: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5, evh(148)=0. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4.
Retest: c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3.
evh(118)=0.

### 5.7 Arm F3 (K=3; RARE on passes 1,4, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2 (no 148): 143/144 revolve (2). nevict=2. Probe MISS.
Pass 3 (no 148): 100 -> REVISE ->148 (F5); 104 -> REVISE
->130. 143/144 revolve (2). nevict=2. Probe: 100->148 (sup1),
148->152 (sup1>0, R148 0->1). HIT.
Pass 4 (148): 148 -> HIT (sup2). 143/144 revolve (2). Probe
HIT (R148 1->2).
Pass 5 (no 148): revolve (2). Probe HIT (R148 2->3).
Pass 6 (no 148): revolve (2). Probe HIT (R148 3->4).

Frozen F3: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5, evh(148)=0. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4.
Retest: c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3.
evh(118)=0.

### 5.8 Arm F6 (K=6; RARE on pass 1 only, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2: 143/144 revolve (2). nevict=2. Probe: predict(100):
sup2,ref2 -> -1. MISS.
Pass 3: 100 -> REVISE ->148; 104 -> REVISE ->130. 143/144
revolve (2). Probe: 100->148 (sup1), 148->152 (sup1>0,
R148 0->1). HIT.
Passes 4-6: 148 untouched (sup1, R grows 2,3,4; never
re-taught, never evicted: R>=1 excludes it from min-reads
victims, and it was never max-ins among R0). 143/144 revolve
(2 each). Probes HIT.

Frozen F6: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5, evh(148)=0. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4.
Retest: c=2/2 (q100=152 via 148 sup1; q104=131); nc=2/2;
u=4/4; forget=0. bprobe=2/3. evh(118)=0.

### 5.9 Predicted mechanism (directional: USEFUL-BUT-BOUNDED)

D4 evicts by demonstrated query-usefulness (reads). The RARE
link is read by the per-pass probe from pass 3 on (after
revision routes q(100) through it); once read (R>=1) it is
excluded from the min-reads victim set and the churn moves
entirely onto never-read FREQ novels. Phase-1 sleepers were
read during phase-1 probeA (R>=2), so unlike D3, D4 sacrifices
no uncontested old knowledge (u=4/4, phev=0 on all 8 arms).
Availability: 4/4/3/0 last-order, 4/4/4/4 first-order. The
first-order K=6 arm is FIXED (avail 4): the max-ins tie-break
spares the first-installed 148 on pass 1, the pass-3 probe
reads it, and reads protect it thereafter. The last-order K=6
arm is NOT fixed (avail 0): 148 is evicted on pass 2 before
any query routes through it (Section 5.4 mechanism note) --
no entry-local statistic (recency, teaching-frequency, OR
read-frequency) can protect a useful-but-rarest link that dies
before its first successful query. The usefulness signal moves
the liability from "young"/"infrequent" to "never-yet-read";
it does not eliminate it.

## 6. Assembly, build, run (frozen)

- Single source file `ntue_full.zag`: canonical helpers
  (z_alloc, get32, set32, o_app, o_i64, o_nl, o_flush; copied
  verbatim from the frozen ntfq template), learner fns (D1+D4
  per Section 2; cl_evict_leastread replaces
  cl_evict_leastfreq; slot field 9 = reads; checkpoint entry
  extended to 6 fields incl. reads; cl_predict increments reads
  on success), oracle fns (linka, ntha, nthq, bsub, bobj, ansa,
  ansb, isC, isNC verbatim), 2-hop query fn, teachA verbatim,
  teachB(K,pass,first) with the order parameter (RARE-first vs
  RARE-last per Section 3), per-pass probe, retest, phev, main
  running the 8 arms (L1/L2/L3/L6/F1/F2/F3/F6) sequentially. No
  other source.
- Build: `znc ntue_full.zag -o ntue_bin` under safebin-only
  PATH.
- Run `ntue_bin` 3 times; outputs `ntue_run1.txt`,
  `ntue_run2.txt`, `ntue_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Output lines (all numeric): per arm ttcA/probeA/nevict/phev,
  per-pass q(100)==152 flags p1..p6 and avail, retest partition
  scores (c/nc/u/forget), bprobe (/3), nonzero
  eviction-histogram bins, evh(148), evh(118), and K1..K7
  verdict bits plus a verdict line. Tag NTUE.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic
  output only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting at most 3 deep
  with hoisted call results; no `[]u8 as *u8` casts (thread
  `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8
  for ALL eight arms. Else VOID (families not learnable;
  redesign, do not reinterpret).
- K2 (retention of uncontested structure): nc = 2 AND u = 4 for
  ALL eight arms. Predicted: PASSES (the read signal protects
  phase-1 sleepers; D4 pays no D3-style sleeper cost).
- K3 (the fix bar: availability): avail = 4, 4, 3, 0 for
  L1, L2, L3, L6 and avail = 4, 4, 4, 4 for F1, F2, F3, F6
  (exact; Section 5). Discriminates fix vs no-fix per order.
- K4 (final revision outcome): L1/L2/L3: c = 2 AND forget = 0;
  L6: c = 1 AND forget = 1; F1/F2/F3/F6: c = 2 AND forget = 0.
  Revision itself completes on every arm.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 11, 9, 7, 2 for L1, L2, L3, L6 and
  nevict = 11, 11, 11, 11 for F1, F2, F3, F6 (exact);
  evh(148) = 2, 1, 1, 1 for L1..L6 and 0, 0, 0, 0 for F1..F6
  (white-box: the RARE link is evicted early in last-order,
  never in first-order); evh(118) = 0 and phev = 0 on ALL
  arms (white-box: no phase-1 link is ever the D4 victim).
- K6 (discriminative validity): avail(L1) = 4 (the probe
  passes when the link is present; not a broken probe) AND
  nevict > 0 for ALL eight arms (pressure actually
  exercised). If K6 fails the apparatus cannot discriminate
  -> INCONCLUSIVE at the lane level.
- K7 (the K=6 pin bar; the follow-up hypothesis): avail(L6)
  = 4 AND avail(F6) = 4 (the case D2 and D3 both fail, in
  both teach orders). Predicted: FAILS (L6 traced 0, F6
  traced 4; Section 5.4 mechanism note).

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace;
  mechanism deeper than the fix).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated: counts
  or white-box histograms off-trace).
- K3 = 0 -> NO-FIX (the usefulness rule does not achieve the
  traced availability curve; REPORT characterizes the actual
  curve).
- K7 = 0 -> USEFUL-BUT-BOUNDED: D4 pins the RARE link via the
  learner-available read signal in both teach orders at
  K=1,2,3 and in first-order at K=6, with zero retention cost
  (u=4/4, phev=0 everywhere), but cannot pin a taught-once
  last-order link that is evicted before its first successful
  query. The usefulness signal moves the liability from
  "young"/"infrequent" to "never-yet-read"; it does not
  eliminate it. This sharpens NTFQ's conclusion: not even
  read/query frequency -- the most natural learner-available
  relevance signal -- escapes the useful-but-rarest problem.
- K2 = 0 -> FIX-WITH-COST: D4 improves RARE-link availability
  but sacrifices un-reinforced phase-1 knowledge to do it
  (unexpected; REPORT explains).
- else -> FIX-CLEAN: D4 pins 148 in both orders at all K
  including last-order K=6 with zero retention cost
  (unexpected; REPORT explains).

Predicted verdict: USEFUL-BUT-BOUNDED (K7=0 on the L6 arm;
K1-K6 predicted 1).

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
  Retention/revision/eviction dynamics over structured knowledge
  only.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed, so the per-pass probe series (not the
  aggregate curve) is what separates usefulness from phase.
- The read signal is learner-local query-observation preserved
  by D1; no usefulness oracle, no researcher-provided labels, no
  task identity enters the comparator. The per-pass probe is a
  query like any other (Section 2 disclosure).
- The max-ins tie-break is frozen as the minimal departure from
  D2/D3 (D2's comparator demoted to tie-break, as in NTFQ); the
  experiment isolates the usefulness primary signal. The
  tie-break is load-bearing: the min-ins (FIFO) alternative is
  traced (not run) to give avail 0/0/0/0 first-order, because
  the first-installed RARE link would be the first victim on
  pass 1 before any read. The tie-break choice, not just the
  primary signal, determines order-dependence -- recorded as a
  finding, not a free parameter.
- reinf is preserved by D1 but not consulted by D4's comparator
  (documented in Section 2); D4's comparator uses reads+ins
  only.
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
- New rule = new lane: D1/D2/D3 and their lanes are untouched by
  this work. The D2 baseline (avail 4/2/1/0 last-order,
  4/4/4/4 first-order) and D3 numbers (avail 4/4/3/0
  last-order, u 3/4) are taken from the frozen NT-LOWVALUE-
  BOUNDARY, NT-ORDER-MIRROR, and NT-FREQ-EVICT REPORTs.
