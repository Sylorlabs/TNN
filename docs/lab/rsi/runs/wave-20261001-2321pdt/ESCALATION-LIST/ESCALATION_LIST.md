# ESCALATION LIST: wave-20261001-2321pdt
Lane: ESCALATION-LIST (replacement worker). Date: 2026-10-02.
Sources (read only): LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md (5 wave escalations),
LANE-AUDIT/LANE_AUDIT_REPORT.md (142k files), WAVE_RECORD.md (queued next, escalation
mentions), RT-GOV/RT-GOV_REVIEW.md (5 verbatim decisions), GAP-DOC/GAP_DOCUMENTATION.md
(learner-authority gap), ARENA/PREREG_ARENA_INQUIRY.md and SEALED_EVAL.md (LLM baseline).
Zero em/en dashes verified with check_no_dash.sh before commit.

These are items requiring Micah's governance decision, or his awareness where noted.
This lane recommends only how to present each item. It makes no decision.

## Summary

| # | Item | Why it needs Micah | Kind |
|---|------|--------------------|------|
| 1 | TNN3-SUBSTRATE adoption (5 verbatim decisions) | Frozen-baseline change; soft irreversibility; amendment discipline touches his prereg red line | DECISION |
| 2 | EXECUTE placement ruling (amendments A-C) | Protected-core boundary change | DECISION (pending since 2026-09-30) |
| 3 | Three paused boundary-overreach repair threads | Corrections pending; scope must be re-established from his directive | DECISION |
| 4 | ~142k files outside the wave dir still deleted in HEAD | Restore-and-commit vs leave as working-tree recovery source | DECISION |
| 5 | H6R B4 substrate design gap (standing/retention) | Governance record for TNN-3; interacts with decision 1.3 | DESIGN INPUT |
| 6 | Learner-authority-over-integration gap (GAP-DOC) | Verified TNN-3 governance problem statement | DESIGN INPUT |
| 7 | LLM baseline still pending (no credential) | Blocks the standing TNN-vs-LLM arena mandate | DECISION |
| I1 | H5R2 claim boundary (no action required) | Honest bound, recorded | INFO |
| I2 | Staging races; H5R2-SKEPTIC2 git workflow flagged for review | Operational awareness | INFO |
| I3 | 15-vs-16 capability count discrepancy | Record hygiene | INFO |

## 1. TNN3-SUBSTRATE adoption: five verbatim governance decisions

The item: the 197-line zero-new-opcode TNN3-SUBSTRATE package (learner construction
service + contradiction trigger + learner-writable standing, PKG sha256
be4e5867ac305ba8ebe190922f7741f6a4c053729f99064354606c146affdff8) closes the three
gaps that stopped H2/H4/H6/H7, verified on the dev prototype (R0 46/46, V1/V2/V3 PASS,
frozen tnn2.zag untouched, hash a29972ca...). RT-GOV (commit 7a1ebe002) holds on all
three axes: ONE-SYSTEM RULE HOLDS, ISA RULING HOLDS (0 new opcodes, forbidden-class
audit of all 14 functions clean), GOVERNANCE HOLDS with one QUALIFY (Amendments 1-2
applied in place inside the prototype commit, never re-frozen alone; flagged for his
amendment-discipline decision). The lane RECOMMENDS but does not adopt. Adoption into
the TNN-2 cognition layer, and any protected-core change (none requested), are his
decisions.

Why it needs him: adopting changes the frozen baseline six lanes froze kill bars
against, which carries soft irreversibility (cheap to revert technically, expensive to
revert scientifically once re-attempts freeze bars against the adopted build; his
bar-change rule makes reversal invalidate those bars). Decisions 3 and 4 move
researcher constants into machinery (lbid composition default, +1/-1 polarities),
which touches his learner-authority stance. Decision 5 touches his prereg
amendment-discipline red line directly.

Evidence: TNN3-SUBSTRATE verdict (DESIGN-COMPLETE, commits be112b78f, a11dde4b9,
f77b7c7d5); RT-GOV_REVIEW.md full review and the five verbatim-ready decisions;
H2R/H7R BUILD-PASS and H6R BUILD-FAIL (gap, item 5) as the re-attempt pre/post evidence.

Recommended framing: present the five decisions verbatim from RT-GOV_REVIEW.md section
"ESCALATION: exact governance decisions for Micah", in order, with the soft-irreversibility
note attached to decision 2 and the doc fix ("type-904 ticket nodes", not "904 ticket nodes"
in ADOPTION_RECOMMENDATION.md section 2) as a pre-adoption prerequisite. Bundle: decisions
1, 2, and 5 are yes/no on the package itself; 3 and 4 are parameter calls he can make now
or defer to H6R's own bars.

The five decisions verbatim:

1. Adoption: "Adopt the 197-line TNN3-SUBSTRATE package (PKG-BEGIN to PKG-END, sha256
be4e5867ac305ba8ebe190922f7741f6a4c053729f99064354606c146affdff8) into the TNN-2
lineage's cognition layer, with the specified adoption diff (lb_run at ev_observe's
three returns; ls_bump +1/-1 and lt_fire hooks; lbid at the four selector sites 145,
259, 872, 884), as the substrate for the H2R/H4R/H6R/H7R re-attempts? No protected-core
change is requested."
2. Baseline: "Accept that this changes the frozen baseline six lanes verified against
(frozen tnn2.zag a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd),
with the pre-package baseline preserved in git history for the sealed SUBSTRATE-ABSENT
findings? Note: once re-attempts freeze their kill bars against the adopted build,
reversing the adoption invalidates those bars."
3. Standing composition: "Accept lbid's record-wins-else-bid composition as the
substrate default, with H6R allowed to propose full replacement semantics under its
own bars, or direct a different composition rule now?"
4. Polarities: "Accept the +1/-1 confirm/contradict polarities as fixed machinery
(analogous to the existing ET_CFM/ET_CON self-edges), or require learner ownership of
polarity magnitudes before H6R freezes its bars?"
5. Amendment discipline: "Accept Amendments 1-2 as committed inside the prototype
commit (evidence is internally consistent; one-line deletion, bars unchanged), or
require future prereg amendments to re-freeze alone before implementation?"

## 2. EXECUTE placement ruling (amendments A-C): still pending

The item: his ruling on the EXECUTE placement recommendation (seventh protected-core
primitive EXECUTE(root, frame) over a 4-op ISA of MOVE, BRANCHEQ, INC, DEC; amendments
A-C), pending since 2026-09-30. The wave record notes H4R's closed loop still gates on
it (H4R's construction half is unblocked by the substrate package; the closed loop is
not). RT-GOV lists it as informational: the substrate package does not ask for it.

Why it needs him: it is a protected-core boundary change, which is his reserved
governance decision by the escalation boundary. Workers cannot discriminate it
experimentally; it is a design-commitment call.

Evidence: recorded pending in WAVE_RECORD.md and in the LOOPSTATE draft ("H4R's closed
loop remains gated on his pending EXECUTE placement ruling"); RT-GOV_REVIEW.md
informational note confirms the substrate package does not depend on it.

Recommended framing: one line in the decision queue: rule on EXECUTE placement
(amendments A-C) so H4R's B4 can be attempted, or defer explicitly with a statement of
what happens to H4R in the meantime. Pair with item 1: if he adopts the substrate
package, the EXECUTE ruling is the only remaining gate on the full H2R/H4R/H6R/H7R
re-attempt set.

## 3. Three paused boundary-overreach repair threads: no repair branch, scope to re-establish

The item: three boundary-overreach repair threads opened and paused 2026-10-01 19:14 UTC
on his directive messages. A repair-branch check this wave found no repair branch in the
working copy, and the threads left no recoverable state in the repo. The corrections are
still pending.

Why it needs him: the threads were paused on his directive messages, so only he can
re-establish scope: resume the repair, re-task it, or cancel it. Workers have no standing
instruction to restart them.

Evidence: WAVE_RECORD.md line 5 ("no repair branch exists in the working copy for the
three boundary-overreach repair threads paused 2026-10-01 19:14 UTC. The threads left no
recoverable state in the repo. Recorded as an escalation item for Micah (corrections
still pending, scope to be re-established)"); LOOPSTATE draft escalation item 2;
QUAL-SUMMARY repair-branches qualification.

Recommended framing: ask him whether to re-open the repair work as a fresh repair lane
(with scope from his original directive), or drop it. Note explicitly that there is
nothing to resume from (no branch, no state), so the choice is restart-fresh vs cancel,
not resume.

## 4. ~142k files outside the wave dir: restore and commit, or leave?

The item: commit f461e812d (H5R2-SKEPTIC2 implementation) deleted 147,296 files
repo-wide. The LANE-AUDIT lane restored and committed all 4,833 under this wave's dir
(34 per-lane restore commits, 4,831 byte-identical to the pre-incident parent, 2
legitimately superseded; all 43 preregs intact in HEAD; full SHA-256 manifest in
RESTORED_MANIFEST.tsv). The remaining ~142,000 deleted files elsewhere in the repo
(docs/lab/*, src/, units/, etc.) exist on disk as untracked files but are NOT in HEAD.
Restoring them was outside the audit lane's tasking.

Why it needs him: this is repo stewardship with a large blast radius: committing
~142k restored files is a heavyweight, irreversible-in-practice history event; leaving
them means the working tree (untracked) is the only recovery source and any fresh
checkout loses them. The trade is his to call.

Evidence: LANE-AUDIT/LANE_AUDIT_REPORT.md, final section ("Out of scope observation for
the parent"); the audit method (hash-verified byte-identical on-disk copies) generalizes
to the remaining files.

Recommended framing: give him the two options with costs: (a) a follow-up restore lane
using the same byte-verify method, committed per subtree, which makes HEAD whole again;
(b) leave the working tree as the recovery source, with the risk stated (fresh checkouts
lose the files; uncommitted state is fragile). Ask which, plus whether to snapshot the
untracked files to a bundle first as insurance regardless of his choice.

## 5. H6R B4 substrate design gap: standing records cannot express preferential retention

The item: H6R (substrate re-attempt, standing/accumulation) BUILD-FAIL. The gap is
crisp and recorded for the governance record: standing values live on kind-904 record
nodes that are never protection-pinned (no ref_prot call in ls_touch; only facts and
roots are pinned) and carry lbid 0 (value in field 24, invisible to the lbid selector;
only in-edge is the type-10 root link, which bid does not count). The adopted
evict_node selects argmin lbid over unprotected live nodes, so it always evicts standing
records before any fact node (sealed evidence: B4-W1 first real eviction = node 6,
nH's standing record, not nF). Evicting a record destroys that node's standing, so no
world can express "high-standing nodes survive preferentially". The package unblocks
accumulation and integration but cannot beat the no-standing baseline on probe
prediction. This is a crisp substrate design gap for the governance record
(TNN3-SUBSTRATE adoption pending).

Why it needs him: it is a design gap, not a decision, but it interacts directly with
decision 1.3 (lbid's record-wins-else-bid default) and with whether the substrate
package, as designed, is the right basis for TNN-3's standing/retention semantics. He
should see the gap before ruling on adoption.

Evidence: H6R verdict in WAVE_RECORD.md (B4 SUBSTRATE-INSUFFICIENT with the exact gap);
H6R lane commits (prereg 784b329eb, implementation+sealed eval a0283287b); kill bars
KB-H6R not weakened.

Recommended framing: present as a pre-adoption caveat attached to item 1, not a blocker
to be decided now: if he adopts, H6R's re-attempt must be designed against this known
gap (protection-pinning of records and/or lbid-selector visibility), and the adoption
should name whether that redesign is part of the package or a follow-up under H6R's
own bars.

## 6. Learner-authority-over-integration gap (GAP-DOC): TNN-3 governance problem statement

The item: GAP-DOC/GAP_DOCUMENTATION.md is the verified problem statement for TNN-3
governance on learner-owned integration. Measurement: the learner records facts,
reifies uncertainty, and selects guides, but cannot initiate the one construction act
that integrates new experience; human hand-holding is maximal on the integration path
(the 6/6 to 0/6 drop when the event-triggered machinery is removed is the measurement
of the hand-holding share). Any TNN-3 design claiming learner-owned integration must
address three absent properties: initiation-from-state, control-from-state,
trigger-from-state. The acceptance run that would close the gap: event-triggered
machinery disabled, the learner still integrates, with white-box evidence of the
learner-created structure that initiated construction (bar CO-1).

Why it needs him: it is a standing architecture-commitment question (initiation
semantics, control plane, protected-core boundary for TNN-3), not an experimentally
discriminable choice within the current system. Any change to the protected-core
boundary or to initiation semantics is a TNN-3 governance decision.

Evidence: GAP-DOC/GAP_DOCUMENTATION.md sections 4 and 5 (explicitly: "This document
proposes no patch, handler, mode, bridge, or opcode. Any change to the protected-core
boundary or to initiation semantics is a TNN-3 governance decision.").

Recommended framing: present as the companion design input to item 5: together they
define what TNN-3's substrate must provide (retention semantics + initiation
semantics). Ask whether he wants these two problem statements frozen as acceptance
criteria for TNN-3 design proposals, so future lanes build against them.

## 7. LLM baseline: still pending (no credential)

The item: the arena's TNN-vs-LLM baseline comparison remains pending. ARENA's
PREREG_ARENA_INQUIRY.md and SEALED_EVAL.md both record: "The LLM baseline comparison
remains pending credentials and is out of scope for this lane." An llm_prompt_pack.txt
is sealed in the ARENA lane's sealed world files, so the instrument is ready; the
credential is not. His standing TNN-vs-LLM arena mandate requires a capable
non-crippled baseline, 15 measured capabilities, honest resource charging, and
capability curves rather than a superiority declaration; without the baseline, the
arena candidates (INQ 0.853, REMAP/TRX C12 transfers, ROSTER 0.947, DEFRECALL) cannot
be placed against a serious LLM.

Why it needs him: obtaining the credential (or approving the service/account to use)
is his call; lanes cannot spend money, open accounts, or contact outside services.

Evidence: ARENA/PREREG_ARENA_INQUIRY.md lines 176-177; ARENA/SEALED_EVAL.md lines
135-136; sealed ARENA/sealed/world/llm_prompt_pack.txt exists.

Recommended framing: ask for the credential/approved path, or an explicit ruling that
the arena proceeds without an LLM baseline for now (and what standing baseline, if any,
takes its place, e.g. the simple-baseline suite used for H5R2). Note the cost: every
arena wave that lands without it accrues comparison debt.

---

## Informational items (no decision required)

I1. H5R2 claim boundary (honest, no action required): the t2_prov_ok provenance gate
beats recency, no-gate, and chance at every chain level, but its necessity is still
unproven against the stronger skeptic NEWEST-LIVE-ON-KEY (SKEPTIC-SURVIVES 8/8 vs 8/8).
The two-live-facts-on-one-key family (H5R2-SKEPTIC3, already queued) is the named next
discriminator. Recorded so the H5R2 claim is not overclaimed.

I2. Staging races (operational, for his awareness): the skeleton commit c5ea959d4 swept
composition_compare/ staged by another worker; fc2f910e5 swept six F1-BUFFER files;
f461e812d swept thousands of unrelated staged deletions and deleted BATTERY-E4's
PREREG_E4.md + NAMECHECK.md (restored byte-identical before any implementation commit,
E4-K1 holds; that commit is also the source of item 4); BATTERY-E4's restored prereg
files were then swept into ARENA5's prereg commit b63f80289. Affected workers adopted
explicit-path staging; history left as-is per the no-rewrite rule. The H5R2-SKEPTIC2
worker's git workflow is flagged for review. No data was lost.

I3. 15-vs-16 capability count discrepancy (record hygiene): sealed records govern 16
capabilities / 68 items, but several lane reports say 15. ARENA4 flagged it ("sealed
records govern: 16 capabilities, 68 items"). Not a decision; the record should be
stated consistently in future lanes.
