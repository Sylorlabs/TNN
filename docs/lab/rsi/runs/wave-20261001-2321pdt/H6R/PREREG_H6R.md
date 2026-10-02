# PREREG H6R: learner-updatable standing, re-attempt on the prototype substrate

Lane: H6R, wave-20261001-2321pdt. Status: FROZEN with this commit.
Frozen: 2026-10-01. Documentation rule observed: no em-dashes in this document.

## 1. Lineage

- wave-20261001-2021pdt TNN3H6: SUBSTRATE-ABSENT. No learner-reachable path updated
  standing on UNCERT nodes; no CONFIRM/CONTRADICT events; no learner-maintained
  standing field for selectors. PREREG_H6.md, sections 2(b), 2(c), 3.
- wave-20261001-2321pdt TNN3-SUBSTRATE: package DESIGN-COMPLETE. Learner-writable
  standing (4C) verified: confirm/contradict events accumulate +1/-1 on per-node
  records, values persist unchanged across queries, lbid identical to bid where no
  record exists (V3). Prereg frozen alone (commit be112b78f); prototype built after
  (commit a11dde4b9); kill bars KB-H6R frozen in SUBSTRATE_PREREG.md section 8.
- This lane: the H6R re-attempt per protocol G1-G4 (re-verify package, sealed worlds
  post-freeze, deterministic byte-identical runs, L3 criteria govern authorship
  claims; builders report BUILD-PASS or BUILD-FAIL only).

## 2. Hypothesis (scoped re-attempt)

H6R: the prototype substrate's learner-writable standing unblocks the testable core
of H6: (a) standing trajectories discriminate a transient contradiction from a
systematic shift; (b) standing-guided selection beats raw-frequency selection on
worlds where frequency misleads; (c) high-standing nodes are preferentially
retained under memory pressure. The standing records are written ONLY by the frozen
generic event polarities (+1 on ev_observe confirm, -1 on ev_observe contradict);
no lane code writes standing directly. The full H6 architectural claim (deletion of
the fixed bid() formula, UNCERT merge) is NOT re-attempted here; it is carried
governance (section 10).

## 3. G1 substrate re-verification (completed 2026-10-01, BEFORE this freeze)

Against commit a11dde4b9
(docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/substrate_proto.zag),
by grep on 2026-10-01:

- `lbid(` appears at exactly four cognition-path selector sites: line 145
  (activate), line 259 (evict_node), lines 874 and 886 (ev_act, both candidate
  loops, marked SUBSTRATE-HOOK C3). These are KB-H6R B2's "three selectors"
  (activate, evict_node, ev_act). Remaining `lbid(` occurrences: the definition
  (line 1785) and the dev-check asserts (lines 1915, 1917).
- `bid(` remains at: the definition (line 237), the four test-battery sites
  (lines 956, 988, 1208, 1213, which unit-test the frozen formula), the lbid
  fallback (line 1788), and dev checks. No other production call site.
- `ls_bump(` appears only in ev_observe: line 842 (confirm branch, +1, marked
  SUBSTRATE-HOOK C1) and line 855 (contradiction branch, -1, marked
  SUBSTRATE-HOOK B C2), plus the definition (line 1772). There is NO event path
  that writes standing on guide nodes or UNCERT nodes. This verified package
  property forces the B3 scope note in section 5.
- alloc_node hands out increasing ids (scans from 2 upward), so the
  earliest-taught live node wins activate ties. Used by the section 4 analysis.

## 4. Frozen analysis: the H6R-B3-nil result (prediction, NOT a bar change)

Mechanism facts (all verified against the committed prototype in section 3):

- (F1) Standing changes only via ls_bump on the ev_observe-activated fact:
  +1 on confirm, -1 on contradict. A contradict also writes a type-3 self-edge,
  which permanently supersedes the node (is_superseded), excluding it from
  activate and ev_act candidacy.
- (F2) Raw-frequency self-edges accrue only to the activated fact: type-7 on
  confirm, type-6 on ev_query hit. No event writes type-1/type-2 self-edges or
  type-10 in-edges on facts.
- (F3) For a live (non-superseded) fact, contradicts = 0, so
  standing(n) = confirms(n), and bid(n) = confirms(n) + freq(n) with
  freq(n) >= 0. Hence lbid(n) <= bid(n), with equality iff the node never
  received query hits.
- (F4) Confirms, contradicts, and query hits always land on the current
  lbid-leader (the activated fact). A trailing node therefore never accumulates
  standing or frequency while trailing, and the earliest-taught live node is the
  perpetual leader until contradicted (ties break to the lowest id).

Theorem: on any event-interface-constructible workspace, among the live facts
matching a query (s, r), at most one (the earliest-taught live node) has nonzero
standing or frequency, and both the lbid-argmax (treatment) and the bid-argmax
(control) select it. Proof: by F4, only the leader ever receives standing or
frequency updates; by F1, a contradicted leader is superseded and leaves the
candidate set; the successor leader starts at (0,0) and the invariant is
restored. Both selectors therefore agree on every selection trial.

FROZEN PREDICTION: the sealed B3 margin (treatment accuracy minus control
accuracy) will be exactly 0 on every sealed world. The 15-point bar in section 6
stands UNCHANGED; the verdict follows the measured numbers, not this prediction.
If the sealed run contradicts the prediction, the data wins and this analysis is
reported as falsified. This prediction also resolves carried question (i)
empirically: the record-wins-else-bid default is what makes the selection effect
nil (a record-less high-frequency node keeps its full bid under lbid; a recorded
node's standing can never exceed its own raw bid).

## 5. B3 scope note (transparent; the bar is not moved)

KB-H6R B3 names guides ("high-frequency wrong guide vs low-frequency right
guide"). Section 3 verifies that the frozen package writes standing records ONLY
on ev_observe-activated fact nodes; no event path writes standing on guides or
UNCERT nodes. A guide-level B3 would require researcher-authored standing
updates, which this lane forbids. B3 therefore runs on fact candidates through
activate, which exercises the IDENTICAL lbid-vs-bid integration (line 145) that
guide selection uses (lines 874, 886). The 15-point margin, the ablation
requirement, and the determinism requirements are unchanged. The guide-level
reading of B3 is recorded as substrate-absent under the frozen package (exact
gap: ls_bump has no call site outside ev_observe's fact branches) and carried
for the governance record; it is not worked around.

## 6. Frozen kill bars

KB-H6R, quoted unweakened from SUBSTRATE_PREREG.md section 8:

- B1 substrate: ls_read trajectories discriminate a singleton contradiction
  (transient dip then recovery under confirms) from a systematic shift
  (monotonic decline); white-box asserted on scripted event sequences.
- B2 integration: grep of the adopted source shows lbid (not bid) at all three
  selector call sites (activate, evict_node, ev_act). (Verified on the
  prototype in section 3; the adoption decision itself is Micah's governance
  call and is not made here.)
- B3 sealed: on worlds where raw frequency misleads (high-frequency wrong guide
  vs low-frequency right guide), standing-guided selection beats the bid-only
  control by at least 15 percentage points on hidden trials. (Scope per
  section 5.)
- B4 retention: under memory pressure, high-standing nodes survive
  preferentially relative to the bid-only control.
- KILL: B1 trajectories do not discriminate, or B3 margin below 15 points.

Lane additions (frozen with this prereg; they strengthen, never weaken):

- P1 held-out probe: every B3 world carries a CONFIRM/CONTRADICT event stream
  followed by H = 20 held-out probe trials (ev_query on the world's slots).
  The probe's truth labels are stipulated by the world and never revealed
  through events. Margin = mean over worlds of (treatment accuracy minus
  control accuracy), where treatment is the prototype's own activate (lbid)
  and control is an argmax-bid scan over the identical candidate set computed
  before each probe query. Frozen bar: margin >= 15 percentage points.
- P2 ablation: after each B3 world's stream, tombstone all -44 standing records
  (harness kills the record nodes; no substrate change), re-run the 20 probes,
  and white-box assert lbid(n) == bid(n) for every probed candidate. The
  measured advantage must be mediated by the records: post-ablation the two
  arms must agree exactly.
- P3 determinism: the full experiment binary is run 3 times; all 3 stdout
  captures must be byte-identical (sha256 recorded). Any divergence voids the
  run.
- P4 K-C0A audit: zero new semantic cases in lane-added code. Procedure: grep
  the lane's added Zag for branch-on-content patterns plus a line-by-line
  review; the lane adds no functions that condition on domain, task, relation,
  or object values; world parameters are numeric test data, asserts compare
  measured standing/bid values to preregistered predictions. The substrate
  portion of the lane binary must be byte-identical to the committed
  prototype's substrate portion (mechanical rebuild verified by diff).

## 7. Sealed world family (structures frozen here; concrete numeric parameters chosen post-freeze at implementation)

B1 scripted worlds (exact white-box expectations frozen):

- B1-S (singleton contradiction, then recovery): teach (501,51,1); 4 confirms;
  1 contradict via observe (501,51,2); 3 confirms of (501,51,2). Frozen
  expectation: ls_read(n1) == 3 (dip of exactly 1 from the peak 4),
  ls_read(n2) == 3 (the successor fact recovers to the dipped value).
- B1-M (systematic shift): teach (502,52,1); 1 confirm; then alternating
  contradicts (502,52,2), (502,52,1), (502,52,2). Frozen expectation:
  ls_read(m1) == 0, ls_read(m2) == -1, ls_read(m3) == -1: monotonic
  non-increasing decline with no recovery (max post-onset standing 0, strictly
  below B1-S's recovery to 3). Discrimination: S shows dip-then-recovery,
  M shows monotonic decline.

B3 sealed worlds (each: event stream, then H = 20 held-out probes; truth labels
stipulated, never event-revealed):

- B3-W1 (frequency-loaded wrong leader): teach nW = (s,r,0); 10 ev_query hits
  on (s,r) (type-6 frequency on nW, no standing change); teach nR = (s,r,1).
  Truth stipulated: o = 1. Best fair attempt at "frequency misleads": the
  learner experiences no event that could endorse the trailer (any
  non-matching observe would supersede the leader; matching observes confirm
  it). Predicted: both arms select nW on all 20 probes; margin 0.
- B3-W2 (singleton contradiction then correction): as W1, then 1 contradict
  observe (s,r,1) (nW superseded, successor taught), then 4 confirms of
  (s,r,1). Truth: o = 1. Predicted: both arms select the corrected fact on
  all 20 probes; margin 0.
- B3-W3 (systematic shift then stabilize): teach (s,r,0); 6 query hits; then
  alternating contradicts ending with 3 confirms of the final object.
  Truth: the final object. Predicted: both arms track the corrected fact
  identically; margin 0.
- B3-W4 (two slots): slot A follows W1's structure, slot B follows W2's
  structure, 10 probes per slot. Predicted: margin 0.

B4 retention worlds (each: loading, then a pacemaker slot P keeps STAND_ROOT
pinned while target protection lapses, then one REAL evict_node call through
the retention mechanism; two further real evictions document the history-node
churn as an observation):

- Common structure: nH = teach (sH,rH,1) + nconfH confirms (standing nconfH,
  bid nconfH); nF = teach (sF,rF,2) + nconfF confirms; P = teach (pslot,90,7).
  Then nqF/2 rounds of [2 query hits on (sF,rF) + 1 confirm on (pslot,90,7)]:
  nF gains nqF type-6 frequency edges (standing nconfF, bid nconfF+nqF) while
  P's confirms re-pin STAND_ROOT (verified substrate property, section 12:
  the root's type-9 protection edge is removed after 12 standing-free events
  and ref_prot cannot restore a removed edge, so the pacemaker interleave is
  required). Then 2 rounds of [10 ev_acts (pure decay; no guides exist, node
  count asserted fixed) + 1 confirm on (pslot,90,7)]: nH and nF protection
  lapses (13+ decays since their last touch) while the root never sees 12
  decays without a standing touch. White-box asserts: is_prot(nH)==0,
  is_prot(nF)==0, is_prot(STAND_ROOT)==1; then v1 = evict_node() must equal
  nF (treatment evicts the high-frequency node first); the bid control
  provably reverses (bid(nH) == nconfH < nconfF+nqF == bid(nF), both static
  under eviction of other nodes).
- B4-R1: (701,71) nconfH=8; (702,72) nconfF=3, nqF=12; pslot 901.
  Expectation: v1 == nF; control premise 8 < 15.
- B4-R2: (703,73) nconfH=5; (704,74) nconfF=2, nqF=8; pslot 902.
  Expectation: v1 == nF; control premise 5 < 10.
- B4-R3: (705,75) nconfH=6; (706,76) nconfF=1, nqF=16; pslot 903.
  Expectation: v1 == nF; control premise 6 < 17.

Concrete (s, r) values above are illustrative of the frozen structures; the
implementation commits the final numeric parameters post-freeze under the
constraint that they are structurally distinct from the substrate lane's
dev-check values (dev checks used s in {101, 202, 301, 302, 9001} and
r in {11, 22, 31, 32, 90}; H6R uses the 5xx/6xx/7xx/9xx domains). The sealed
parameter file's sha256 is recorded before the evaluation run.

Ablation protocol (P2): per B3 world, after the stream, the harness sets
field36 = 0 on every -44 record under STAND_ROOT (tombstone; substrate
untouched), re-runs the 20 probes, and asserts exact agreement of the two arms
plus lbid == bid on all probed candidates white-box.

## 8. Implementation plan (no frozen-source modification)

1. Rebuild the substrate mechanically: copy the frozen tnn2.zag (hash
   re-verified: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd),
   apply the prereg's hook insertions with the substrate lane's exact sed
   commands, append the PKG block extracted mechanically (sed between PKG-BEGIN
   and PKG-END) from the FROZEN prereg at commit be112b78f.
2. Byte-compare the rebuilt substrate portion against commit a11dde4b9's
   substrate_proto.zag (modulo the dev-harness main line and the dev checks):
   must be identical, proving the rebuild reproduces the verified prototype.
3. Strip the dev checks; set main to h6r_main; append h6r_checks.zag (this
   lane's experiment code only: world drivers, probe, ablation, asserts;
   no ls_bump/ls_touch calls anywhere in lane code: standing arises only
   from the event stream through the frozen hooks).
4. Compile with the pinned znc; run; verify the 46/46 regression still passes
   as a guard.

## 9. Verdict rule

BUILD-PASS iff B1 exact trajectories hold AND B2 grep holds AND B3 margin >= 15
points AND B4 relative-order holds on all three worlds AND P2 ablation shows
exact post-ablation agreement AND P3 3/3 byte-identical AND P4 audit clean.
Otherwise BUILD-FAIL, naming the killing bar and quoting the measured numbers.
Per KB-H6R, B3 margin below 15 points kills regardless of the other bars.

## 10. Carried governance questions (recorded; NOT decided here)

(i) lbid's record-wins-else-bid default may need H6R override. This experiment
proceeds with the package AS FROZEN (researcher constants); section 4 predicts
the default makes the B3 selection effect nil, which the sealed run will confirm
or falsify. Designing an override is not this lane's job.
(ii) Whether the +1/-1 event polarities must become learner-owned before H6R
freezes. This experiment tests whether the standing MECHANISM unblocks H6's
hypothesis, not whether the constants are ideal; the polarities stay frozen
researcher constants.

If the sealed run shows the mechanism cannot express a frozen bar for reasons
beyond the section 4 prediction, the lane reports SUBSTRATE-INSUFFICIENT with
the exact gap instead of working around it with researcher-authored standing
updates.

## 11. Commit order

This prereg (+ NAMECHECK.md, process record only) is committed alone, before
any implementation. The implementation commit follows strictly after. The
commit-order self-check: this commit's timestamp precedes the implementation
commit's timestamp. Sealed world parameters are committed before the
evaluation run; the run log is committed after.

## 12. Amendments (transparent; kill bars in section 6 unchanged)

AMENDMENT 1, 2026-10-01 (after prereg freeze 784b329eb, before the sealed
evaluation; forced by a pilot run of the implementation, which failed
"B4 root unprotected"): B4 world construction corrected. Verified root cause:
STAND_ROOT's type-9 protection edge is removed by decay after 12 consecutive
standing-free events (the frozen B4-R1's 12 query hits), and ref_prot can only
refresh LIVE type-9 edges, so the frozen "13 filler confirms re-pin the root"
step was a no-op: the root stayed permanently unprotected and would have been
evicted before either target. The frozen bar (B4: preferential survival of
high-standing nodes) is unchanged. The corrected worlds keep the frozen nH/nF
confirm counts; R2/R3 query counts were adjusted from 9/20 to 8/16 (even, for
exact halving into interleave rounds; the bar-relevant control property
bid(nH) < bid(nF) is preserved: 5 < 10 and 6 < 17). A pacemaker slot P
(taught once, confirmed on a fixed interleave) whose confirms re-pin
STAND_ROOT without touching nH/nF standing: queries run as
[2 queries + 1 pacemaker confirm] rounds, and target protection is lapsed by
2 rounds of [10 ev_acts + 1 pacemaker confirm] (the root never sees 12 decays
without a standing touch, while the targets see 13+). The pacemaker is world
structure (a continuously confirming background slot), not a mechanism change;
its confirms go through the frozen ev_observe polarities like all other
events, so no researcher-authored standing update is involved. B1, B2, B3
are unaffected.
