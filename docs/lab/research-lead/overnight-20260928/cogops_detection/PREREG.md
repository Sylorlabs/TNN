# PREREG: COGOPS-DETECTION (learner-invented oscillation detection)

Date: 2026-10-03. Worker: COGOPS-DETECTION.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_detection/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

## 1. Research question

COGOPS-LEARNOSC (BUILD-PASS) showed the learner invents an
oscillation RESPONSE from its trajectory/outcome record, and
COGOPS-LEARNOSC2 (BUILD-PASS) showed the outcome record is
necessary for reuse. Both reports carry the same honest
boundary: the learner did NOT invent oscillation DETECTION.
The recurrence scan (`osc_review`: nearest-first whole-state
snapshot equality over lags) is generic machinery,
researcher-provided, same class as the quiescence check.

This worker asks: can the learner invent the recurrence-scan
itself, building detection from trajectory comparisons? The
detection procedure, not just the response, must be
learner-constructed from experience.

## 2. Design

### 2.1 What is generic machinery (researcher-provided, domain-blind)

- Per-pass trajectory recording (`traj_log`): mechanical
  recording, same class as the LSTATE dumps. Records, does
  not interpret.
- Pairwise whole-state snapshot equality (`traj_state_eq`):
  a generic comparison primitive. It compares two recorded
  snapshots and returns 0/1. It encodes no oscillation
  semantics, proposes nothing, scans nothing, and holds no
  lag concept. Same class as integer equality.
- Single-step plan execution (`exec_step_iter`, frozen),
  the outcome-record store (`outc_store`), the stored-phase
  comparator (`outc_phase_eq`), and the learner-owned spec
  versions. All frozen.
- The DET event ring (Section 2.4): an observation channel.
  It records what the learner did; it does not decide
  anything.

### 2.2 What is learner-created (from experience, in learner state)

- The lag prior: one word of durable learner state (DETC
  region). It starts at 0 (no prior). Every verified
  detection overwrites it with the verified lag. Its VALUE
  at any run is therefore determined by the learner's own
  verification history, not by the source.
- The proposal sequence: at each pass the learner proposes
  individual snapshot comparisons in an order its prior
  determines: the prior pair first (if the prior is set),
  then recency order. Which pairs get proposed, and whether
  the first proposal hits, is a consequence of the
  learner-state prior meeting the current trajectory.
- The hypothesis: when a proposed comparison returns equal,
  the learner forms a lag hypothesis, builds a checker from
  the recurring snapshots, and runs a confirm pass. The
  hypothesis (which lag, from which pair, on which goal)
  exists only in the learner's run-time activity.
- The constructed checker: the verified lag plus the phase
  records copied from the learner's own recurring
  snapshots, stored in the outcome record. Same stored form
  as LEARNOSC, but reached without any researcher scan.
- Retraction: if the confirm pass falsifies a hypothesis,
  the learner retracts it, records the retracted lag, and
  continues proposing. (Implemented; not exercised by this
  battery. See Section 2.5.)

### 2.3 The honest boundary (what this does NOT claim)

- The strategy space is researcher-provided: pairwise
  snapshot comparison over lags 1..3, the prior-then-recency
  proposal FORM, the hypothesis rule (equality implies a lag
  hypothesis), the confirm protocol, and the prior update
  rule (verified lag overwrites the prior). The learner
  does not invent comparison, does not invent the concept
  of lag, and does not choose among different detection
  strategies. A stronger claim (learner-chosen strategy
  among whole-state vs per-need vs alternation detectors)
  is explicit future work.
- The claim is L2 structural learning, not L3
  representational invention: the learner assembles a
  detection procedure INSTANCE (which pairs, which
  hypothesis, which checker, for which goal) from generic
  primitives, driven by its experience; the instance is
  stored in learner state, reused, and shown necessary by
  lesion. No new primitive, no new representational form,
  no new procedure class is invented. The checker's stored
  form (lag plus phases) is the same form LEARNOSC used.
  The 12-criterion L3 bar is not claimed.
- Red-team note (pre-registered): the attack "det_propose
  is osc_review rewritten; the researcher still wrote the
  order" is answered four ways. (a) Structural: the
  additive section contains no lag-scan loop and no call
  to osc_review (K8); the only comparison the new code
  performs is single-pair traj_state_eq, driven by the
  learner-state prior. (b) Causal: lesioning the prior
  changes detection behavior (K6/K7); a fixed scan has no
  lesionable state. (c) Observable epistemics: every
  proposed comparison, including failures and skips, is
  printed (DET-CMP); the hypothesis/confirm cycle is
  printed (DET-HYP, OSC-CONFIRM); a scan would show none
  of this. (d) Transfer: the prior verified on goal 818
  measurably accelerates detection on goal 820 (1
  comparison vs 2), while a wrong prior costs more than
  no prior (3 vs 2). A scan learns nothing across goals.

### 2.4 Learner-state layout (additive, no frozen region moved)

L is 16384 bytes. c8 use ends at 15896 (OUTC entries).
New region DETC:
- 15900: lag prior (durable learner state; 0 = none).
- 15904: retracted lag (per-run; reset at detection start).
- 15908: event count ntev (per-run; reset at detection start).
- 15912 + tev*20: event ring, tev < 16, 5 words each:
  [kind, p, x, y, z].
  kind 0 = CMP (proposed comparison: p=pass, x=i, y=j,
  z=eq with -1 = prior pair inapplicable, skipped);
  kind 1 = HYP (p=pass, x=lag, y=q);
  kind 3 = PRIOR (x=prior at detection start);
  kind 4 = SET (x=prior after verification);
  kind 5 = APPLY (stored-checker application: p=pass,
  x=needs matched, y=needs total);
  kind 6 = RETRACT (x=retracted lag; not exercised here).
Worst case per run is S8: 14 events < 16. Ring top is
16232 < 16384.

### 2.5 The learner-owned driver (det_handle, additive)

New entry point in the additive section of c9_learn.zag.
Returns -1 / 0 / 1 / 2 with the same contract as
osc_handle. Procedure:

1. Plan setup: plan_find, else learn_bindings plus topo_g
   plus plan_new (same as osc_handle). On learn_bindings
   failure, return -1. Reset the per-run DET state
   (retracted lag, event ring); the prior persists.
2. Stored-checker application: look up the goal tag in the
   outcome record. If present, run up to 2 passes; after
   each pass compare every need's snapshot to the stored
   phase (outc_phase_eq) and log an APPLY event with the
   match count. On 2 consecutive full matches, emit the
   STORED checker and return 2. On any mismatch, reset the
   trajectory count and fall through to step 3.
3. Invention path: for passes 0..5, run all needs in plan
   order via osc_one_pass (learner-owned spec versions;
   SPECCHK flag as before), snapshot into TRAJ. From pass
   2 on, run the learner-owned proposal for this pass:
   - Log a PRIOR event once (the prior at detection start).
   - Slot 0: if the prior is set, propose (p, p-prior).
     If p-prior < 0 the pair is inapplicable: log a CMP
     skip event (eq=-1) and continue. This event is the
     observable cost of consulting a wrong prior.
   - Slots 1..3: (p,p-1), (p,p-2), (p,p-3), skipping the
     pair already proposed in slot 0 and any pair with
     b < 0 (silent; not a learner choice).
   - Any pair whose lag equals the retracted lag is
     skipped (a falsified hypothesis is not re-formed).
   - For each proposed pair, run traj_state_eq and log a
     CMP event with the result. On equality:
     * lag 1 means quiescence (a fixpoint, not an
       oscillation): stop, return 0, invent nothing.
     * lag 2..3: log a HYP event, run ONE confirm pass,
       check (p+1, q+1) via traj_state_eq. If it holds,
       store the outcome entry (src=0), overwrite the
       prior with the verified lag, log a SET event,
       and return 1. If it fails, log a RETRACT event,
       record the retracted lag, and continue detection
       at pass p+2 (the confirm pass already advanced
       the trajectory). The retract path is implemented
       but not exercised by this battery.
   - lag above 3: decline by construction (pairs only
     cover lags 1..3; honest boundary, same as LEARNOSC).
   If no hypothesis verifies by pass 5, return 0.

The emitted checker is verified by the learner's own
confirm pass, not by an oracle. For oscillatory goals
there is no oracle agreement bar (C6 established the
intended answer is ill-defined); correctness is internal:
the emitted phases are byte-exact copies of the
learner's observed recurring states and the confirm
pass verified the cycle predicts.

### 2.6 Worlds and goals

c9_world.zag is cmp-identical to c8_world.zag. No new
worlds, relations, or goals: the detection claim must
hold on the exact worlds LEARNOSC used (D, E, C; goals
818, 820, 821, 816). All literals live in the world
file; the additive learn section carries zero world,
goal, or relation literals (K8).

### 2.7 Battery stages (c9_main.zag)

S1A, S1B, S2, S4, S7: identical calls to LEARNOSC
(byte-identical EP/SPEC/LSTATE lines expected).
- S3 OSC-D0 (goal 818, world D): det_handle. Prior=0.
  Predicted: DET-PRIOR prior=0; 2 CMP (fail, hit);
  DET-HYP lag=2; confirm ok; DET-PRIOR set=2; Q how=1
  passes=4; OSC-CYCLE (LEARNOSC's exact phases);
  OSC-CONFIRM ok=1; SPECCHK spec=1; OSC-STATE src=0.
- S5 OSC-E0 (goal 820, world E): det_handle. Prior=2
  (verified in S3). Predicted: 1 CMP (the prior pair
  hits at once); DET-HYP lag=2; Q how=1 passes=4;
  OSC-CYCLE phases 771/772; prior stays 2. The 1-vs-2
  CMP count against S3 is the transfer evidence: the
  learner's past detection experience accelerates the
  new detection.
- S6 OSC-E1 (goal 821, world E): det_handle. Prior=2.
  Predicted: 5 CMP (2 fails at p=2, 2 fails + 1 hit at
  p=3); DET-HYP lag=3 p=3 q=0; confirm ok; DET-PRIOR
  set=3; Q how=1 passes=5; OSC-CYCLE lag=3 phases
  781/782/783. The checker STRUCTURE differs (lag 3):
  built per trajectory, not a filled template.
- S8 CONV-816 (goal 816, world C): det_handle. Prior=3.
  Predicted: 13 CMP (12 fails + 1 prior skip), no HYP;
  return 0; fallback compose_iter; Q how=0 passes=9;
  AGREE id=S8 a=1 (byte-exact C6 control behavior:
  no false positive, no regression).
- S9 REUSE-818 (goal 818, world D again): setup_worldD,
  re-specialize (no new episodes), det_handle. Predicted:
  stored-checker application: 2 DET-APPLY match=3/3;
  Q how=2 passes=2; OSC-CYCLE byte-identical to S3's;
  OSC-REUSE match=2; SPECCHK spec=1; OSC-STATE src=0.
- S10 DET-PRIOR-LESION: setup_worldE, re-specialize ret
  (13,20) and vfy (21,22) with no new episodes, tombstone
  goal 820's outcome entry (tag to -1; the ring eviction
  then places the re-invented entry at e=0, overwriting
  818's entry; documented, deterministic), zero the
  prior, det_handle on goal 820. Predicted: DET-PRIOR
  prior=0; 2 CMP (fail, hit: full recency order, no
  prior); DET-HYP lag=2; Q how=1 passes=4; re-invented
  OSC-CYCLE byte-identical to S5's; OSC-STATE src=0;
  DET-PRIOR set=2. More comparisons than S5's 1: the
  prior causally drives detection efficiency.
- S11 DET-PRIOR-CORRUPT: tombstone goal 820's entry
  again, set the prior to 3 (wrong), det_handle on goal
  820 (world E still set up; no re-specialize needed).
  Predicted: DET-PRIOR prior=3; 3 CMP (prior skip,
  fail, hit); DET-HYP lag=2; Q how=1 passes=4;
  OSC-CYCLE byte-identical to S5's; DET-PRIOR set=2.
  A wrong prior costs strictly more than no prior
  (3 > 2 > 1): the prior is genuinely consulted, not
  merely stored.
- SUMMARY-DET.

Output vocabulary (new lines; all dynamic content
through the single preallocated buffer, one flush):
- `DET-PRIOR prior=<k>` (prior at detection start)
- `DET-CMP p=<p> a=<i> b=<j> eq=<e>` (each proposed
  comparison; e=-1 means the prior pair was
  inapplicable at this pass)
- `DET-HYP goal=<gt> lag=<k> p=<p> q=<q>`
- `DET-PRIOR set=<k>` (prior overwritten after
  verification)
- `DET-APPLY goal=<gt> pass=<p> match=<m>/<nn>`
  (stored checker applied on the reuse path)
- `DET-RETRACT goal=<gt> lag=<k>` (implemented; no
  battery stage triggers it)
Q / OSC-CYCLE / OSC-CONFIRM / OSC-REUSE / OSC-STATE /
SPECCHK / AGREE / EP / SPEC / LSTATE / STAGE lines as in
LEARNOSC; SUMMARY-DET carries agree, plans_built,
plans_loaded, trials, declines, and the final prior.

## 3. Kill bars (frozen)

- K1 (detection by construction, S3): the exact S3 block
  of Section 7: `Q id=S3 goal=818 how=1 passes=4`,
  `DET-PRIOR prior=0`, exactly 2 DET-CMP lines
  (`p=2 a=2 b=1 eq=0` then `p=2 a=2 b=0 eq=1`),
  `DET-HYP goal=818 lag=2 p=2 q=0`,
  `DET-PRIOR set=2`, LEARNOSC's exact OSC-CYCLE line,
  `OSC-CONFIRM goal=818 ok=1`, `SPECCHK goal=818 spec=1`,
  `OSC-STATE goal=818 lag=2 nph=2 src=0`.
- K2 (prior accelerates transfer, S5): the exact S5
  block: `DET-PRIOR prior=2`, exactly 1 DET-CMP line
  (`p=2 a=2 b=0 eq=1`), `DET-HYP goal=820 lag=2 p=2 q=0`,
  `Q id=S5 goal=820 how=1 passes=4`, the exact
  OSC-CYCLE line with phases 771/772, confirm ok=1,
  spec=1, `OSC-STATE goal=820 lag=2 nph=2 src=0`.
- K3 (period-3 structure built, S6): the exact S6 block:
  `DET-PRIOR prior=2`, exactly 5 DET-CMP lines (2 fails
  at p=2, 2 fails + 1 hit at p=3),
  `DET-HYP goal=821 lag=3 p=3 q=0`,
  `DET-PRIOR set=3`, `Q id=S6 goal=821 how=1 passes=5`,
  the exact lag-3 OSC-CYCLE line (phases 781/782/783),
  confirm ok=1, spec=1, `OSC-STATE goal=821 lag=3
  nph=3 src=0`.
- K4 (no false positive, S8): the exact S8 block:
  `DET-PRIOR prior=3`, exactly 13 DET-CMP lines (12
  eq=0 plus the `p=2 a=2 b=-1 eq=-1` skip), no DET-HYP
  anywhere in S8, `Q id=S8 goal=816 how=0 passes=9`,
  `AGREE id=S8 a=1`.
- K5 (checker application, S9): `Q id=S9 goal=818 how=2
  passes=2`, 2 `DET-APPLY goal=818 pass=<p> match=3/3`
  lines, the OSC-CYCLE line byte-identical to S3's,
  `OSC-REUSE goal=818 match=2`, `SPECCHK goal=818
  spec=1`, `OSC-STATE goal=818 lag=2 nph=2 src=0`.
- K6 (prior lesion, S10): `DET-PRIOR prior=0`, exactly
  2 DET-CMP lines (vs 1 in S5),
  `DET-HYP goal=820 lag=2 p=2 q=0`,
  `Q id=S10 goal=820 how=1 passes=4`, the OSC-CYCLE
  line byte-identical to S5's, `OSC-STATE goal=820
  lag=2 nph=2 src=0`, `DET-PRIOR set=2`.
- K7 (prior corrupt, S11): `DET-PRIOR prior=3`, exactly
  3 DET-CMP lines (skip, fail, hit),
  `DET-HYP goal=820 lag=2 p=2 q=0`,
  `Q id=S11 goal=820 how=1 passes=4`, the OSC-CYCLE
  line byte-identical to S5's, `DET-PRIOR set=2`.
- K8 (structural non-use of the provided primitive):
  c9_base.zag cmp-identical to c8_base.zag; the first
  <len(c8_learn.zag)> bytes of c9_learn.zag cmp-identical
  to c8_learn.zag (purely additive; no frozen function
  modified); grep for `osc_review` finds zero call
  sites in the additive section of c9_learn.zag and in
  c9_main.zag (the primitive is present in the binary
  via the frozen prefix but no execution path in this
  battery reaches it); word-boundary grep for every
  world/goal/relation identifier empty in the additive
  section (comments included: no literals anywhere).
- K9: 3/3 byte-identical stdout across runs, stderr empty.
- K10: safebin active for every command,
  PATH=$HOME/safebin, `which python3` / `which python`
  empty, all computation pure Zag, pinned znc only, no
  `while.*!(` negated-conjunction pattern in new Zag.
- K11: zero em/en dash bytes in all lane docs.

Verdict rule: BUILD-PASS requires K1..K11 all PASS. Any
deviation is reported with the observed bytes; a miss on
K1..K7 is INFORMATIVE-FAIL (mechanism), on K8..K11 is
PROCESS-FAIL.

A note on what INFORMATIVE-FAIL would mean here: if the
CMP counts do not order S5(1) < S10(2) < S11(3), or the
detection trace is observationally identical to a fixed
scan with no lesionable learner state, the honest
verdict is that learner-executed detection collapses to
the provided strategy space and the invention remains in
the response, not the detection. That negative result is
valuable: it would show the next step needs a richer
strategy space (learner-chosen among genuinely
different detectors), not a finer proposal order.

## 4. Implementation plan (post-freeze)

- c9_base.zag: byte copy of c8_base.zag (cmp-verified).
- c9_world.zag: byte copy of c8_world.zag (cmp-verified).
- c9_learn.zag: byte copy of c8_learn.zag plus one
  additive section (DETC helpers: det_ev, det_try,
  det_propose_pass, det_handle; lesion helper
  outc_tombstone lives in main). No frozen function
  modified. New code scanned for the `while.*!(`
  pattern; if-nesting kept at 3 or fewer with hoisted
  flags per the znc defect notes.
- c9_main.zag: new driver per Section 2.7 (harness; may
  reference pattern/goal ids like c7_main.zag did);
  do_losc calls det_handle and dumps the DET event ring.
- c9_build.sh: assemble (base+world+learn+main),
  compile with the pinned znc
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
  run 3x, cmp, sha256.
- Any post-freeze correction follows the transparent
  pre-implementation erratum convention (no silent
  edits); errata after execution are reported, not
  amended into the prereg.

## 5. Governance notes

- Pure Zag. safebin mandatory from the first command.
- Opaque identifiers throughout; zero world literals in
  the additive learn section (K8).
- Commits local, never pushed, explicit pathspecs only,
  on the current branch; no other lane touched.
- This prereg is adopted as frozen without modification.
- Non-ledger task: claim minting paused; no ledger
  entries are made for this work.

## 6. What success would establish (and not)

Would establish: the learner can assemble an oscillation
detection procedure from a generic comparison primitive
(L2 structural learning): detection by learner-proposed
comparisons (K1), an experience-shaped prior that
measurably accelerates transfer (K2) and is causally
necessary for that acceleration (K6/K7), per-trajectory
checker structures (K3), no false positives on
convergence (K4), and stored-checker application on
re-presentation (K5). The detection instance (which
pairs, which hypothesis, which checker, for which goal)
is built from the learner's trajectory experience; the
researcher-provided scan is provably unused (K8).

Would not establish: learner-invented detection
STRATEGY (the pairwise-comparison strategy space stays
researcher-provided); L3 representational invention;
lag above 3; divergent trajectories; scaling; behavior
under a different cap.

## 7. Frozen exact predictions

Every stdout line the battery prints, in order. EP
counts and LSTATE/SPEC lines are hand-traced from the
world definitions and the specialize provenance (the
S10 re-specialize lines follow the union rule observed
in LEARNOSC S9); Q/DET/OSC lines from the pass-by-pass
traces in the worker's design notes.

```
STAGE S1A RET-LEARN
EP ep=0 ret n=1
EP ep=1 ret n=1
EP ep=2 ret n=1
EP ep=3 ret n=1
SPEC-RET rev=1 nrel=2 ep0=0 ep1=3 nfacts=56
LSTATE-RET nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
STAGE S1B VFY-LEARN
EP ep=4 vfy v=1
EP ep=5 vfy v=1
EP ep=6 vfy v=1
EP ep=7 vfy v=0
SPEC-VFY rev=1 nrel=3 ep0=4 ep1=7 nfacts=56
LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
STAGE S2 OSC-LEARN-D
EP ep=8 ret n=1
EP ep=9 ret n=1
EP ep=10 ret n=1
EP ep=11 ret n=1
SPEC-RET rev=2 nrel=3 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3 prov=0,8,11,61 rev=2
EP ep=12 vfy v=1
SPEC-VFY rev=2 nrel=4 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=4 ids=601,602,603,608 cnts=16,16,16,2 prov=1,12,12,61 rev=2
STAGE S3 OSC-D0
Q id=S3 goal=818 how=1 passes=4
DET-PRIOR prior=0
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=818 lag=2 p=2 q=0
DET-PRIOR set=2
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-CONFIRM goal=818 ok=1
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
STAGE S4 OSC-LEARN-E
EP ep=13 ret n=1
EP ep=14 ret n=1
EP ep=15 ret n=1
EP ep=16 ret n=1
EP ep=17 ret n=1
EP ep=18 ret n=1
EP ep=19 ret n=1
EP ep=20 ret n=1
SPEC-RET rev=3 nrel=5 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=5 ids=601,602,606,613,615 cnts=16,16,0,3,4 prov=0,13,20,68 rev=3
EP ep=21 vfy v=1
EP ep=22 vfy v=1
SPEC-VFY rev=3 nrel=6 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=6 ids=601,602,603,608,614,616 cnts=16,16,16,0,2,3 prov=1,21,22,68 rev=3
STAGE S5 OSC-E0
Q id=S5 goal=820 how=1 passes=4
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=820 lag=2 p=2 q=0
DET-PRIOR set=2
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0
STAGE S6 OSC-E1
Q id=S6 goal=821 how=1 passes=5
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=0 eq=1
DET-HYP goal=821 lag=3 p=3 q=0
DET-PRIOR set=3
OSC-CYCLE goal=821 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=821 ok=1
SPECCHK goal=821 spec=1
OSC-STATE goal=821 lag=3 nph=3 src=0
STAGE S7 CYCLE-LEARN-C
EP ep=23 ret n=1
EP ep=24 ret n=1
EP ep=25 ret n=1
SPEC-RET rev=4 nrel=6 ep0=23 ep1=25 nfacts=72
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,0,0,8 prov=0,23,25,72 rev=4
EP ep=26 vfy v=1
SPEC-VFY rev=4 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=4
STAGE S8 CONV-816
Q id=S8 goal=816 how=0 passes=9
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=-1 eq=-1
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=4 a=4 b=1 eq=0
DET-CMP p=4 a=4 b=3 eq=0
DET-CMP p=4 a=4 b=2 eq=0
DET-CMP p=5 a=5 b=2 eq=0
DET-CMP p=5 a=5 b=4 eq=0
DET-CMP p=5 a=5 b=3 eq=0
AGREE id=S8 a=1
STAGE S9 REUSE-818
SPEC-RET rev=5 nrel=6 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,3,0,0,0 prov=0,8,11,61 rev=5
SPEC-VFY rev=5 nrel=7 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,2,0,0,0 prov=1,12,12,61 rev=5
Q id=S9 goal=818 how=2 passes=2
DET-APPLY goal=818 pass=0 match=3/3
DET-APPLY goal=818 pass=1 match=3/3
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-REUSE goal=818 match=2
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
STAGE S10 DET-PRIOR-LESION
SPEC-RET rev=6 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=6
SPEC-VFY rev=6 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=6
Q id=S10 goal=820 how=1 passes=4
DET-PRIOR prior=0
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=820 lag=2 p=2 q=0
DET-PRIOR set=2
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0
STAGE S11 DET-PRIOR-CORRUPT
Q id=S11 goal=820 how=1 passes=4
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=-1 eq=-1
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=820 lag=2 p=2 q=0
DET-PRIOR set=2
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0
SUMMARY-DET agree=1 plans_built=4 plans_loaded=4 trials=6 declines=0 prior=2
```
