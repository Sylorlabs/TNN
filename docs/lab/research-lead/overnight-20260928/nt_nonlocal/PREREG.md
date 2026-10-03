# PREREG: NT-NONLOCAL -- a non-entry-local relevance signal for eviction (D5)

## 1. Question

NT-LOWVALUE-BOUNDARY (LIABILITY-CONFIRMED) showed D2's evict-youngest
is a liability for useful-but-infrequently-reinforced links.
NT-ORDER-MIRROR (MIRROR-CONFIRMED) showed installation recency, not
frequency, is D2's true determinant. NT-FREQ-EVICT (FIX-WITH-COST)
showed D3 (evict-least-frequently-reinforced) moves the liability to
"infrequent" without eliminating it. NT-USEFUL-EVICT (FAIL-PRESSURE)
showed D4 (evict-least-read) moves the liability to "never-yet-read"
and fails last-order K=6: link 148 is evicted on pass 2 before any
query routes through it (R=0), entry-locally identical to the other
novels (R=0, F=1). NTUE's honest conclusion, sharpening NTFQ's: "No
entry-local statistic (recency, frequency, or read-count) can protect
a useful-but-rarest link." NTUE's recommended (not preregistered)
follow-up #1: "Non-entry-local relevance signal lane (downstream
query dependence / query-intent pinning) targeting last-order K=6."
This is that lane.

Questions:

(a) Does a non-entry-local, forward-looking relevance signal --
    revision-target pinning (D5) -- pin the RARE link (148,1)->152
    when it is taught LAST (the NTLV liability case) and when it is
    taught FIRST (the NTOM mirror case), at K=1,2,3,6?
(b) In particular, does it fix last-order K=6 (avail 4/4), the case
    D2, D3, and D4 all fail?
(c) What is the cost -- retention of uncontested phase-1 knowledge
    (u, phev), total eviction churn (nevict), FREQ-novel probe
    coverage (bprobe), final revision outcome (c/forget)?

Mechanism under test: D5 = D4 (evict-least-read, max-ins tie-break)
PLUS revision-target pinning. An entry E is PINNED (excluded from the
eviction victim set) while E is the live target of another entry's
in-progress revision: some installed link L underwent a
contradicting teaching (ref++) with taught obj == E.subj, and L has
not since revised. The pin is:

- NON-ENTRY-LOCAL: E's protection is decided from L's state (L's
  contradiction) plus the teaching history, not from E's entry. At
  the last-order K=6 pass-2 decision, entry 148 is
  (sup=1,ref=0,F=1,R=0) -- indistinguishable from a fresh novel --
  but link 100 carries ref=2 toward taught obj 148. The signal lives
  in the (100,148) relationship.
- LEARNER-AVAILABLE: derived solely from the learner's own teaching
  observations (key, taught obj, agree vs contradict outcome) and its
  per-link sup/ref counters. No oracle, no task identity, no
  correctness judgments, no researcher-provided usefulness labels.
  The learner cannot know whether 148 is "useful"; it knows its own
  belief about link 100 is being revised toward 148.
- FORWARD-LOOKING (downstream query dependence): D2/D3/D4 are
  backward-looking (past recency, past reinforcement, past reads).
  D5's pin anticipates where the learner's knowledge is HEADING: once
  link 100's revision completes, queries q(100) will depend on
  link (148,1)->152. The dependence is known before any query
  succeeds through 148 -- exactly the "downstream query dependence"
  named in the follow-up, inferred from the learner's own learning
  dynamics rather than supplied.

Predicted signature: avail 4/4 on ALL eight arms (L3 improves 3->4,
L6 fixed 0->4 vs D4); evh(148)=0 everywhere (148 never evicted);
u=4/4 and phev=0 everywhere (no retention cost); churn redistributes
onto the FREQ novels (L-arm nevict 10/10/10/10 vs D4's 10/8/6/2 --
the pin does not reduce pressure, it redirects it); bprobe 2/3 on
all arms (143 ends absent; D4's L6 had 3/3 with 148 absent instead).
The headline prediction: K7 PASSES -- last-order K=6 fixed.

## 2. Subject (frozen)

The NT-USEFUL-EVICT subject verbatim (continuing-learner skeleton,
associative instance memory, sequential lifetime phases, single
main(), no resets, no task labels), with D1 kept, D4 kept as the
base comparator, and D5 = D4 + revision-target pinning. Slot fields
(40 bytes): 0 subj, 4 rel, 8 obj, 12 dom, 16 valid, 20 sup, 24 ref,
28 ins, 32 reinf, 36 reads. Key = (subj, rel). rel = 1 throughout.
`dom` = install-phase provenance, entry metadata, never consulted.

- Evidence update (NT-frozen rule): on a teaching event for a PRESENT
  entry, taught obj matches stored obj -> sup++; taught obj differs
  -> ref++, and if ref > sup -> REVISE to (new obj, sup=1, ref=0),
  in place. Revision does NOT touch `ins`, `reinf`, or `reads`.
- reinf: as in NTFQ/NTUE (counts teaching events; fresh -> 1;
  present teaching -> ++; D1-restore -> checkpointed, then ++).
  PRESERVED by D1 but NOT consulted by D5's comparator (documented
  dead weight, as in NTUE).
- reads: as in NTUE (counts queries the entry contributed an answer
  to; incremented in cl_predict on success with sup > ref; fresh ->
  0; D1-restore -> checkpointed).
- pendtgt (NEW, the pin state): per-slot i32, the taught obj of the
  link's most recent CONTRADICTING teaching (ref++ event), or 0 if
  none is pending. Learner-local record of its own contradiction
  dynamics. Lifecycle (all learner-observable):
  - set to the taught obj on every ref++ (overwrites any previous);
  - cleared to 0 when the link revises in place (the pending is
    resolved);
  - cleared to 0 on every fresh installation and every D1 restore
    (a newly installed entry is not mid-contradiction);
  - overwritten on slot reuse (eviction + reinstall starts clean).
  - NOT cleared when the target is evicted: a stale pendtgt pointing
    at an absent key protects nothing (the pin test only matches
    installed subjs) and reactivates correctly if the target is
    D1-restored while the contest is still live.
- D1 (preserve-evidence, kept, unchanged): on eviction, checkpoint
  (valid=1, obj, sup, ref, reinf, reads) keyed by subj; on insertion
  of an absent key with a valid checkpoint, install checkpointed
  values then run the frozen update step; else fresh. (pendtgt is
  NOT checkpointed: it is live contest state, not evidence.)
- D5 (evict-least-read + revision-target pinning; REPLACES D4 as the
  rule under test): victim = occupied slot with MINIMUM `reads`
  among NON-PINNED slots; tie-break = MAXIMUM `ins` (youngest
  among the least-read). A slot S is PINNED iff some occupied slot T
  has pendtgt[T] == S.subj. If every occupied slot is pinned (cannot
  occur in this workload; max 2 live pins), fall back to the D4 rule
  over all occupied slots so victim selection stays total.
- Rationale (frozen, disclosed): the pin is NOT a researcher
  importance flag. It fires uniformly for any link undergoing
  contradiction, toward any target: in this workload it protects
  148 (link 100's revision target) AND 130 (link 104's revision
  target) during passes 1-2. It encodes one general principle: do
  not evict the live target of the learner's own in-progress belief
  revision, because near-future queries routed through the revising
  link will depend on it. No modes, no task identity, no usefulness
  oracle.
- Predict: entry present and sup > ref -> stored obj (and reads++);
  else -1 (no reads++).
- 2-hop query q(s): p1 = predict(s,1); if p1 < 0 -> -1;
  p2 = predict(p1,1); if p2 < 0 -> -1; else p2. Fixed machinery;
  the KNOWLEDGE (links) is learned. No semantic labels; bare ints.
- Capacity CAP = 20. The comparator is generic: per-entry read
  count, installation order, and the learner's own pending-revision
  relation only.

PROBE DISCLOSURE (load-bearing, as in NTUE): the per-pass probe
q(100) is read-only w.r.t. learned KNOWLEDGE but DOES increment
reads (observing query traffic is the D4 signal). The D5 pin does
NOT use the probe schedule: pins are set exclusively by teaching
events (ref++), never by queries. The probe is what makes 148
useful; the pin is set by the contradiction dynamics, which are
learner-internal.

The ONLY novelty vs NT-USEFUL-EVICT is the pin state (pendtgt),
its lifecycle hooks in cl_update/cl_insert, and the pin-aware
victim scan. Workload inventory, oracles, D1 machinery, teach
orders, and the D4 base comparator are verbatim.

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

Notation: R = reads, F = reinf, I = ins, P = pinned (some slot has
pendtgt == this subj). Phase 1 (all arms): A-links occupy slots
0..13, I 1..14, (sup=2, ref=0, F=2). Phase-1 probeA ran twice, so
R: 100:2, 101:4, 103:2, 104:2, 105:4, 107:2, 108:2, 109:2, 111:2,
112:2, 114:2, 115:2, 117:2, 118:2. pendtgt all 0. D5 victim = min
R among NON-PINNED, tie-break max I. Pins live only during passes
1-2: pendtgt[100]=148 and pendtgt[104]=130 are set by the pass-1
and pass-2 ref++ events and cleared when links 100/104 revise on
pass 3. Pinned installed entries during passes 1-2: {148, 130}.

### 5.1 Arm L1 (K=1; RARE every pass, taught LAST)

Pass 1: 100 -> ref=1 (F3), pt[100]=148; 101 -> sup=3; 104 ->
ref=1, pt[104]=130; 105 -> sup=3. Novels: 130(15),131(16),
140(17),141(18),143(19),144(20) fresh (R0,F1). 148 -> 21st key
-> evict: R=0 non-pinned {131,140,141,143,144} (130 pinned) ->
max I -> 144(20). Install 148 (I21,R0,F1). Probe MISS
(100->101->102; R100 2->3, R101 4->5). Absent: 144. nevict=1.

Pass 2: 100 -> ref=2, pt[100]=148; 104 -> ref=2, pt[104]=130;
101,105 -> sup=4. Novels 130,131,140,141,143 -> sup=2,F2. 144
absent -> restore (145,1,0,F1,R0) -> evict: R=0 non-pinned
{131,140,141,143} (130,148 pinned) -> 143(19). Install 144
(I22) -> sup=2,F2. 148 present -> sup=2,F2. Absent: 143.
nevict=1. Probe MISS (predict(100): sup2,ref2 -> -1).

Pass 3: 100 -> REVISE ->148 (sup1,ref0,F5), pt[100]=0; 104 ->
REVISE ->130 (F5), pt[104]=0. 101,105 -> sup=5. Novels
130,131,140,141 -> sup=3,F3. 143 absent -> restore -> evict:
R=0 {130(15),131(16),140(17),141(18),144(22),148(21)}, no pins
-> max I -> 144(22). Install 143 (I23) -> sup=3,F3. 144 absent
-> restore -> evict: R=0 {130,131,140,141,143(23),148(21)} ->
143(23). Install 144 (I24) -> sup=3,F3. 148 present -> sup=3,
F3. Absent: 143. nevict=2. Probe HIT: 100->148 (R100 3->4),
148->152 (R148 0->1).

Pass 4: 100,104,101,105 hits. 143 absent -> restore -> evict:
R=0 {130,131,140,141,144(24)} (148 R1) -> 144(24). Install 143
(I25). 144 absent -> restore -> evict -> 143(25). Install 144
(I26). 148 present -> sup=4,F4. Absent: 143. nevict=2. Probe
HIT (R148 1->2).

Pass 5: as pass 4 (2 evictions: 144,143). Probe HIT (R148 2->3).
Pass 6: as pass 4 (2 evictions). Probe HIT (R148 3->4).

Frozen L1: ttcA=2, probeA=8, nevict=10, phev=0. EVHIST: 144=5
(passes 1,3,4,5,6), 143=5 (passes 2,3,4,5,6). Sum=10.
Per-pass q(100)==152: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2
(q100=152 via 148 sup=5; q104=131); nc=2/2; u=4/4; forget=0.
bprobe=2/3 (q143: 143 absent -> -1). evh(148)=0, evh(118)=0.

### 5.2 Arm L2 (K=2; RARE on passes 1,3,5, taught LAST)

Pass 1: as L1. nevict=1. Absent: 144. MISS.
Pass 2 (no 148): 100 -> ref=2, pt[100]=148; 104 -> ref=2,
pt[104]=130. 144 absent -> restore -> evict: R=0 non-pinned
{131,140,141,143} -> 143(19). Install 144 (I22). Absent: 143.
nevict=1. Probe MISS.
Pass 3 (148): 100,104 revise (pins cleared). 143 absent ->
restore -> evict -> 144(22). Install 143 (I23). 144 absent ->
restore -> evict -> 143(23). Install 144 (I24). 148 present ->
sup=2,F2. Absent: 143. nevict=2. Probe HIT (R148 0->1).
Pass 4 (no 148): 143 absent -> restore -> evict -> 144(24).
Install 143 (I25). 144 absent -> restore -> evict -> 143(25).
Install 144 (I26). Absent: 143. nevict=2. Probe HIT (R148 1->2).
Pass 5 (148): 148 present -> sup=3,F3; revolve (2). Probe HIT
(R148 2->3). Pass 6 (no 148): revolve (2). Probe HIT (R148 3->4).

Frozen L2: ttcA=2, probeA=8, nevict=10, phev=0. EVHIST: 144=5,
143=5. Sum=10. Per-pass: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2;
nc=2/2; u=4/4; forget=0. bprobe=2/3. evh(148)=0, evh(118)=0.

### 5.3 Arm L3 (K=3; RARE on passes 1,4, taught LAST)

Pass 1: as L1. nevict=1. Absent: 144. MISS.
Pass 2 (no 148): 144 absent -> restore -> evict (148,130
pinned) -> 143(19). Install 144 (I22). Absent: 143. nevict=1.
Probe MISS.
Pass 3 (no 148): 100,104 revise (pins cleared). 143 absent ->
restore -> evict -> 144(22). Install 143 (I23). 144 absent ->
restore -> evict -> 143(23). Install 144 (I24). Absent: 143.
nevict=2. Probe HIT: 100->148 (sup1, R100+1), 148->152
(sup1, R148 0->1). (D4 missed here: 148 was absent.)
Pass 4 (148): 148 present -> sup=2,F2; revolve (2: 144,143).
Probe HIT (R148 1->2). Pass 5,6 (no 148): revolve (2 each).
Probes HIT (R148 2->3, 3->4).

Frozen L3: ttcA=2, probeA=8, nevict=10, phev=0. EVHIST: 144=5,
143=5. Sum=10. Per-pass: 0,0,1,1,1,1 -> avail=4 (D4: 3).
Retest: c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3.
evh(148)=0, evh(118)=0.

### 5.4 Arm L6 (K=6; RARE on pass 1 only, taught LAST) -- THE
### LIABILITY CASE

Pass 1: as L1. nevict=1 (144). Absent: 144. MISS.
Pass 2 (no 148): 100 -> ref=2, pt[100]=148; 104 -> ref=2,
pt[104]=130. 144 absent -> restore -> evict: R=0 non-pinned
{131(16),140(17),141(18),143(19)} (130,148 PINNED) ->
143(19). Install 144 (I22). Absent: 143. nevict=1. Probe MISS.
MECHANISM NOTE: this is the exact decision point where D2, D3,
and D4 all evict 148. Entry-locally 148 is (sup1,ref0,F1,R0),
identical to the other novels; D5 spares it ONLY via the
non-entry-local pin (link 100's live contradiction toward 148).
Pass 3: 100 -> REVISE ->148 (sup1,ref0,F5), pt[100]=0; 104 ->
REVISE ->130, pt[104]=0. Novels 130,131,140,141,144 -> hits
(sup3,F3). 143 absent -> restore -> evict: R=0
{130,131,140,141,144(22),148(21)}, no pins -> 144(22). Install
143 (I23). 144 absent -> restore -> evict -> 143(23). Install
144 (I24). Absent: 143. nevict=2. Probe HIT: 100->148 (sup1),
148->152 (sup1, R148 0->1). (D4: MISS -- 148 absent.)
Pass 4: revolve (2: 144,143). Probe HIT (R148 1->2).
Pass 5: revolve (2). Probe HIT (R148 2->3).
Pass 6: revolve (2). Probe HIT (R148 3->4).

Frozen L6: ttcA=2, probeA=8, nevict=10, phev=0. EVHIST: 144=5,
143=5. Sum=10. Per-pass: 0,0,1,1,1,1 -> avail=4 (D4: 0 --
FIXED). Retest: c=2/2 (q100=152 via 148 sup1; q104=131);
nc=2/2; u=4/4; forget=0. bprobe=2/3 (D4: 3/3 -- the pin keeps
148 present, so the churn lands on 143 instead). evh(148)=0
(D4: 1), evh(118)=0.

### 5.5 Arm F1 (K=1; RARE every pass, taught FIRST)

Pass 1: 148 fresh FIRST (I15,R0,F1). 100 -> ref=1, pt[100]=148;
104 -> ref=1, pt[104]=130. Novels 130(16),131(17),140(18),
141(19),143(20) fresh. 144 -> 21st key -> evict: R=0 non-pinned
{131,140,141,143} (148,130 pinned) -> 143(20). Install 144
(I21). Absent: 143. nevict=1. Probe MISS (100->101->102).
Pass 2: 148 present -> sup=2,F2. 100 -> ref=2, pt[100]=148;
104 -> ref=2, pt[104]=130. 143 absent -> restore -> evict:
R=0 non-pinned {131,140,141,144} -> 144(21). Install 143 (I22)
-> sup=2,F2. 144 absent -> restore -> evict -> 143(22).
Install 144 (I23). Absent: 143. nevict=2. Probe MISS.
Pass 3: 148 -> sup=3,F3. 100,104 revise (pins cleared). 143
absent -> restore -> evict -> 144(23). Install 143 (I24). 144
absent -> restore -> evict -> 143(24). Install 144 (I25).
Absent: 143. nevict=2. Probe HIT (R148 0->1).
Pass 4: revolve (2: 144,143). Probe HIT (R148 1->2).
Pass 5,6: revolve (2 each). Probes HIT (R148 2->3, 3->4).

Frozen F1: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6
(passes 1-6), 144=5 (passes 2-6). Sum=11. Per-pass: 0,0,1,1,1,1
-> avail=4. Retest: c=2/2; nc=2/2; u=4/4; forget=0. bprobe=2/3.
evh(148)=0, evh(118)=0.

### 5.6 Arm F2 (K=2; RARE on passes 1,3,5, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2 (no 148): 100 -> ref=2, pt[100]=148; 104 -> ref=2,
pt[104]=130. 148 untouched (sup1,F1,R0, pinned). 143 absent ->
restore -> evict -> 144(21). Install 143 (I22). 144 absent ->
restore -> evict -> 143(22). Install 144 (I23). Absent: 143.
nevict=2. Probe MISS.
Pass 3 (148): 148 -> sup=2,F2. 100,104 revise (pins cleared).
Revolve (2: 144,143). Probe HIT (R148 0->1).
Pass 4 (no 148): 148 untouched (sup1,R1). Revolve (2). Probe
HIT (R148 1->2).
Pass 5 (148): 148 -> sup=3,F3. Revolve (2). Probe HIT (R148
2->3). Pass 6 (no 148): revolve (2). Probe HIT (R148 3->4).

Frozen F2: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2;
nc=2/2; u=4/4; forget=0. bprobe=2/3. evh(148)=0, evh(118)=0.

### 5.7 Arm F3 (K=3; RARE on passes 1,4, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2 (no 148): revolve (2: 144,143). nevict=2. Probe MISS.
Pass 3 (no 148): 100 -> REVISE ->148 (F5); 104 -> REVISE ->130
(pins cleared). Revolve (2). Probe HIT (R148 0->1).
Pass 4 (148): 148 -> sup=2,F2. Revolve (2). Probe HIT (R148
1->2). Pass 5,6 (no 148): revolve (2 each). Probes HIT.

Frozen F3: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2;
nc=2/2; u=4/4; forget=0. bprobe=2/3. evh(148)=0, evh(118)=0.

### 5.8 Arm F6 (K=6; RARE on pass 1 only, taught FIRST)

Pass 1: as F1. nevict=1. Absent: 143. MISS.
Pass 2: 100 -> ref=2, pt[100]=148; 104 -> ref=2, pt[104]=130.
148 untouched (pinned). Revolve (2: 144,143). nevict=2. Probe
MISS.
Pass 3: 100,104 revise (pins cleared). Revolve (2). Probe HIT
(R148 0->1).
Passes 4-6: revolve (2 each). Probes HIT (R148 1->2, 2->3, 3->4).

Frozen F6: ttcA=2, probeA=8, nevict=11, phev=0. EVHIST: 143=6,
144=5. Sum=11. Per-pass: 0,0,1,1,1,1 -> avail=4. Retest: c=2/2
(q100=152 via 148 sup1; q104=131); nc=2/2; u=4/4; forget=0.
bprobe=2/3. evh(148)=0, evh(118)=0.

### 5.9 Predicted mechanism (directional: NON-LOCAL-FIX)

D5 layers revision-target pinning on D4's evict-least-read. The
pin is set by the learner's own contradiction dynamics (ref++
events), so during passes 1-2 -- the never-yet-read window where
no entry-local signal can distinguish the RARE link -- the
revision targets {148, 130} are excluded from the victim set.
The pass-2 eviction that kills 148 under D2/D3/D4 instead takes
143; 148 survives to the pass-3 revision, is read by the pass-3
probe (R 0->1), and D4's read protection carries it from there.
Result: avail 4/4 on ALL eight arms (L3 3->4, L6 0->4 vs D4),
evh(148)=0 everywhere, u=4/4 and phev=0 everywhere. The pin does
NOT reduce eviction pressure: it redirects it. L-arm churn rises
to 10/10/10/10 (D4: 10/8/6/2) because the 143/144 revolve cascade
now runs on every arm; bprobe drops to 2/3 on all arms (143 ends
absent; D4's L6 kept 3/3 only because 148 was the absentee).
Cost summary: the fix is paid in churn and in FREQ-novel probe
coverage, not in retention of uncontested knowledge.

## 6. Assembly, build, run (frozen)

- Single source file `ntnl_full.zag`: canonical helpers
  (z_alloc, get32, set32, o_app, o_i64, o_nl, o_flush; copied
  verbatim from the frozen ntue template), learner fns (D1+D4
  base per NTUE Section 2 verbatim; NEW: per-slot pendtgt array,
  set on ref++ in cl_update, cleared on in-place revision and on
  every installation; cl_evict_d5 = min-reads/max-ins scan over
  non-pinned slots with D4 fallback if all pinned), oracle fns
  (linka, ntha, nthq, bsub, bobj, ansa, ansb, isC, isNC verbatim),
  2-hop query fn, teachA verbatim, teachB(K,pass,first) with the
  order parameter, per-pass probe, retest, phev, main running the
  8 arms (L1/L2/L3/L6/F1/F2/F3/F6) sequentially. No other source.
- Build: `znc ntnl_full.zag -o ntnl_bin` under safebin-only
  PATH.
- Run `ntnl_bin` 3 times; outputs `ntnl_run1.txt`,
  `ntnl_run2.txt`, `ntnl_run3.txt`. Require byte-identical
  (cmp) and record sha256.
- Output lines (all numeric): per arm ttcA/probeA/nevict/phev,
  per-pass q(100)==152 flags p1..p6 and avail, retest partition
  scores (c/nc/u/forget), bprobe (/3), nonzero
  eviction-histogram bins, evh(148), evh(118), and K1..K7
  verdict bits plus a verdict line. Tag NTNL.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic
  output only via the single-buffer cursor helpers + one
  `_zag_raw_syscall` write (never `_zag_print`); no `!(A && B)`
  in while conditions (De Morgan); if-nesting mirrors the frozen
  NTUE template shapes; no `[]u8 as *u8` casts (thread
  `_zag_malloc as *u8`).

## 7. Frozen kill bars

- K1 (learnability; else VOID): ttcA in 1..50 AND probeA = 8
  for ALL eight arms. Else VOID (families not learnable;
  redesign, do not reinterpret).
- K2 (retention of uncontested structure): nc = 2 AND u = 4 for
  ALL eight arms. Predicted: PASSES (the pin protects only
  revision targets; phase-1 sleepers are never victims).
- K3 (the fix bar: availability): avail = 4 for ALL eight arms
  (exact; Section 5). Predicted: PASSES -- L3 improves 3->4 and
  L6 0->4 vs D4.
- K4 (final revision outcome): c = 2 AND forget = 0 for ALL
  eight arms (exact; Section 5). Predicted: PASSES -- L6
  improves from D4's c=1/forget=1.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): nevict = 10, 10, 10, 10 for L1, L2, L3, L6 and
  nevict = 11, 11, 11, 11 for F1, F2, F3, F6 (exact);
  evh(148) = 0 on ALL eight arms (white-box: the pin means the
  RARE link is NEVER the D5 victim); evh(118) = 0 and phev = 0
  on ALL arms (white-box: no phase-1 link is ever the victim).
- K6 (discriminative validity): avail(L1) = 4 (the probe
  passes when the link is present; not a broken probe) AND
  nevict > 0 for ALL eight arms (pressure actually
  exercised). If K6 fails the apparatus cannot discriminate
  -> INCONCLUSIVE at the lane level.
- K7 (the K=6 pin bar; the parent requirement): avail(L6)
  = 4 AND avail(F6) = 4 (the case D2, D3, and D4 all fail, in
  both teach orders). Predicted: PASSES.

## 8. Verdict mapping (frozen)

Checked in order; first match wins:

- K1 = 0 -> VOID.
- K6 = 0 -> INCONCLUSIVE (apparatus cannot discriminate).
- K4 = 0 -> INFORMATIVE-FAIL (revision/final-outcome off-trace;
  mechanism deeper than the fix).
- K5 = 0 -> FAIL-PRESSURE (eviction discipline violated: counts
  or white-box histograms off-trace).
- K3 = 0 -> NO-FIX (the pinning rule does not achieve the traced
  availability curve; REPORT characterizes the actual curve).
- K7 = 0 -> SIGNAL-INSUFFICIENT: the non-entry-local signal does
  not pin the taught-once last-order link; the useful-but-rarest
  problem survives even forward-looking learner-available signals
  of this form. REPORT characterizes what did happen.
- K2 = 0 -> FIX-WITH-COST: D5 pins 148 at K=6 but sacrifices
  un-reinforced phase-1 knowledge to do it (unexpected; REPORT
  explains).
- else -> FIX-CLEAN: D5 pins 148 in both orders at all K
  including last-order K=6 via a learner-available non-entry-local
  signal, with zero retention cost (unexpected only in the sense
  that no entry-local rule achieved it; REPORT explains the cost
  in churn and bprobe).

Predicted verdict: FIX-CLEAN (K1-K7 all 1).

## 9. Honest boundaries (frozen)

- The LINKS are memorized associations; what is rule-STRUCTURED
  is the family. No rule induction tested; no L2/L3 claim.
  Retention/revision/eviction dynamics over structured knowledge
  only.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed.
- The pin is learner-available but NOT a usefulness detector: it
  fires for ANY live revision target (here 148 and 130 alike),
  with no judgment about which target matters. A useful link that
  is never the target of a contradiction gets NO protection from
  D5 -- the signal covers "where my beliefs are heading," not
  "what will matter." A workload whose rare-but-useful link is not
  a revision target would still fail; that is a stated coverage
  limit, not a defect to patch inside this lane.
- Stale-pin boundary: a pin persists until the contesting link
  revises. If contradiction stopped forever (revision never
  completes), the pin would leak capacity. Not exercised here
  (revision always completes on pass 3); a decay would be a new
  lane, not an amendment.
- The D5 pin is a protection mechanism, which NTUE's subject
  description listed among things the comparator does not have.
  This lane's explicit hypothesis is that a LEARNER-STATE-DRIVEN
  pin (not a researcher importance flag) is the missing piece; the
  pin condition uses only the learner's own contradiction state,
  applies uniformly, and carries no task identity. The REPORT must
  judge whether that distinction held.
- reinf is preserved by D1 but not consulted by D5's comparator
  (documented dead weight, as in NTUE).
- Port covers the associative instance memory only (NT-PORT
  boundary stands).
- New rule = new lane: D1/D2/D3/D4 and their lanes are untouched
  by this work. Baselines from the frozen NTLV/NTOM/NTFQ/NTUE
  REPORTs: D2 avail 4/2/1/0 last-order; D3 avail 4/4/3/0, u 3/4;
  D4 avail 4/4/3/0 last-order and 4/4/4/4 first-order, u 4/4,
  evh(148) 2/1/1/1 last-order.
