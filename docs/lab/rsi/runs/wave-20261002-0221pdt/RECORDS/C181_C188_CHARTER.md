# Retrospective charter for C181-C188

Lane: RECORDS, wave-20261002-0221pdt. Date: 2026-10-02.
Purpose: the wave-20261001-1721pdt zombie-lane investigation found the
seven commits were legitimate direct handoffs, but required a
retrospective charter for C181-C188 before any claim is adopted beyond
exploratory. This charter states, for each claim, what was claimed,
what evidence exists, what is missing, and the exact acceptance
condition for adoption.

No new experiments were run for this charter. All statements below are
grounded in the committed evidence (commit contents, REPORT files,
transcripts, NAMECHECK records) read from git.

## Standing context

All eight claims are ledgered as EXPLORATORY / BUILD-PASS (exploratory,
no frozen prereg) in the governance wave 2 ledger commit 293cf0672.
That status is the ceiling: none of C181-C188 may be cited as
SURVIVES, as establishing generality, or as an L3 result. None of the
eight asserts L3.

Adoption beyond exploratory for any of the eight requires the standard
11-step frontier promotion pipeline (per the 2026-09-29 strategic
reorientation): committed preregistration, implementation, sealed
evaluation, independent reproduction from committed source,
simple-baseline comparison, alternative-explanation attack, OOD test,
ablation, transfer/reuse test, independent red team, governance audit.
Only after all 11 may a mechanism become SURVIVES. Builders report
BUILD-PASS/BUILD-FAIL only.

The claim-specific acceptance conditions below add the concrete
evidence-completeness and sealed-evaluation requirements each claim
must meet inside that pipeline.

## C181. LEARNER-VERIFICATION (commit d52666a8b, 2026-10-01)

What was claimed: learner-owned prediction reliability replaces
researcher-provided `expected` for revision acceptance (Micah Priority
1). V4 revision acceptance PASS: the learner's adapted reliability
signal makes the same correct accept/reject decisions as
expected-based verification, using only learner-owned evidence.
Withholding (V1/V3a): honest withholding when no reliable predictor
exists, saving compute. Cross-subject candidate acceptance BLOCKED
(requires a generalization mechanism the base lacks). V2 INVALID
(design flaw); direct candidate rejection UNTESTED.

What evidence exists: REPORT.md (231 lines, verdict
LEARNER-VERIFICATION-COMPLETE, honest boundaries in sections 5 and 7);
NAMECHECK.md with Step 0 toolchain guard; full source set
(lv_base.zag, lv_cog.zag, lv_patch.zag, lv_patch_ctl.zag,
lv_driver.zag, lv_full_trt.zag, lv_full_ctl.zag); 6 run transcripts
(run_ctl_1/2/3.txt, run_trt_1/2/3.txt), 3/3 byte-identical per arm
(SHA-256 410f5b8a... treatment, 34c2d751... control). Pure Zag via
pinned znc.

What is missing: REPORT.md section 8 lists `lv_trt_bin`, `lv_ctl_bin`,
`compile_trt.log`, `compile_ctl.log` as artifacts, but the commit
contains no binaries and no compile logs (verified: zero bin/compile
files in d52666a8b). The core evidence (sources, driver, transcripts,
report) is complete; the artifact list overstates what is committed.

Acceptance condition for adoption: (1) commit the two binaries and
two compile logs, or amend REPORT.md section 8 to list only committed
artifacts; (2) fresh frozen prereg (commit-order rule: prereg commit
strictly before implementation) with a sealed battery that includes
at least one cross-subject acceptance family designed post-freeze
(the current BLOCKED limitation must be tested, not assumed away);
(3) independent reproduction 3/3 byte-identical from committed
source; (4) the remaining pipeline steps (baseline, attack, OOD,
ablation, transfer, red team, audit). The V2 design flaw must be
repaired or the direct-rejection claim dropped before adoption.

## C182. ADAPTIVE-THRESHOLD (commit b6135c531, 2026-10-01)

What was claimed: the evidence threshold is a learner-state value
written by experience (Micah Priority 8). One evidence node (tag 40,
subtype 3) holds V (run value), R (run length), E (error score, +3 on
mismatch, -1 on match, floor 0), T = 2 + E/3 clamped to [2,5].
Adapts to experienced noise: T=2 in stable, T=5 in noisy, T=3
(transient) in changing environments. 3/3 byte-identical per arm.

What evidence exists: REPORT.md (verdict ADAPTIVE-THRESHOLD-COMPLETE);
NAMECHECK.md with Step 0; full sources (at_core_adaptive.zag,
at_core_fixed.zag, drivers, at_tests.zag); 6 run transcripts
(at_run_adaptive_1/2/3.txt, at_run_fixed_1/2/3.txt); both binaries
committed (at_bin_adaptive, at_bin_fixed); at_build.sh. Complete
transcript set for the determinism claim.

What is missing: nothing material for the exploratory claim. No
frozen prereg (exploratory by ledger status).

Acceptance condition for adoption: (1) frozen prereg with the T-update
rule and the noise environments fixed before implementation; (2)
sealed evaluation on noise schedules designed post-freeze by an
independent party (the current environments were researcher-designed);
(3) a transfer test: the adapted T must carry usefully to a new
environment family, not just the three tested; (4) independent
reproduction and the remaining pipeline steps. The "threshold tuning
not a priority beyond this validation per Micah 2026-10-01" scope note
must be respected: adoption is of the mechanism, not of a tuning
program.

## C183. PROVENANCE-LEARNING (commit 96fa237b1, 2026-10-01)

What was claimed: source reliability learned from consequences, no
hardcoded OBSERVED-greater-than-INFERRED rank (Micah Priority 4). When
teacher B degrades, the learner demotes B from experience; when B
recovers and A degrades, the learner switches allegiance to B. A
hardcoded-rank control cannot switch and answers 4/4 probes wrong in
the final phase. Builds on C170 and 9e9a2e372. 3/3 deterministic per
arm.

What evidence exists: REPORT.md (verdict PROVENANCE-LEARNING-COMPLETE);
NAMECHECK.md with Step 0; full sources (pl_full_ctl.zag,
pl_full_trt.zag, pl_driver.zag, patches); 6 run transcripts
(pl_ctl_run1/2/3.txt, pl_trt_run1/2/3.txt); both binaries committed
(pl_ctl_bin, pl_trt_bin); build.sh. Complete transcript set.

What is missing: nothing material for the exploratory claim. No
frozen prereg.

Acceptance condition for adoption: (1) frozen prereg with the
source-degradation schedule fixed before implementation; (2) sealed
evaluation with a degradation/recovery schedule designed post-freeze
by an independent adversary (the current schedule was
researcher-authored, so the "switches allegiance" result may be
schedule-shaped); (3) a test with more than two sources and with
simultaneous degradation (the current design has exactly two
teachers); (4) independent reproduction and the remaining pipeline
steps.

## C184. MINI-LIFETIME-INTEGRATION (commit 1963e994d, 2026-10-01)

What was claimed: 3-arm persistent comparison (Micah Priority 9): A.
frozen TNN-2, B. reuse/rebinding, C. consequence plus provenance plus
structural protection integration. No resets. Tracks transfer,
persistent connections, examples-to-criterion, predictive accuracy,
memory growth, compute per event, structures retained, structures
reused, policy changes. Builds on C177 (mini-lifetime run, 4339119e9).
"3/3 byte-identical per arm" with asserted SHA-256 prefixes (A
25749820f2c4a025, B de6a9e18ed2d731d, C a0673125573b7da1).

What evidence exists: REPORT.md (verdict
MINI-LIFETIME-INTEGRATION-COMPLETE); NAMECHECK.md with Step 0; full
sources (mli_full_A/B/C.zag, driver, query, protection/rebind
functions); three binaries (mli_bin_A/B/C); run-1 transcripts per arm
(mli_run_A1/B1/C1.txt). This lane verified the committed run-1
transcripts hash to exactly the REPORT's asserted prefixes (A
25749820f2c4a025, B de6a9e18ed2d731d, C a0673125573b7da1), so run 1
is confirmed on disk.

What is missing: runs 2 and 3 per arm are NOT committed
(mli_run_A2/A3/B2/B3/C2/C3 absent; only A1/B1/C1 in the commit). The
"3/3 byte-identical per arm" claim therefore rests on report-asserted
hashes for runs 2-3, not on committed transcripts. This is the single
largest evidence gap across C181-C188.

Acceptance condition for adoption: (1) commit the missing
mli_run_A2/A3/B2/B3/C2/C3 transcripts if they exist; if they do not
exist, the determinism claim MUST be downgraded in the record to
"run 1 on disk; runs 2-3 asserted in the report only" before any
further citation; (2) because this is the continuing-learner
integration claim (the standing "one persistent learner" question),
adoption requires a fresh frozen prereg with the event sequence,
interference families, and measurement definitions fixed before
implementation; (3) sealed evaluation on an event stream designed
post-freeze, including unrelated interference and delayed-reuse
probes; (4) independent reproduction and the remaining pipeline
steps. No adoption on report-asserted hashes alone.

## C185. SUBSTRATE-EXPANSION (commit 02a338dbf, 2026-10-01)

What was claimed: 5 behaviors from one consequence substrate with
per-behavior ablations (Micah Priority 5). Extends C174 and
fa8405a90. The same tag-61 store drives policy adaptation,
withholding, abandonment, retention, and search-order changes;
ablations show the same consequence records matter to multiple
behaviors. All batteries PASS. 3/3 deterministic byte-identical runs
(SHA-256 8945d3d64b3b0be805f146dce9a67c02a4dc8adacf3603d3dca9377e8e52b4a2).

What evidence exists: DESIGN.md; REPORT.md (verdict
SUBSTRATE-EXPANSION-COMPLETE, per-battery results B1-B5 with
ablation arms, honest boundary: "The config bitmask is
researcher-set per battery, not learned. Learner-owned arbitration
between the five reads is future work."); NAMECHECK.md with Step 0;
sources (se_base.zag, se_behaviors.zag, se_machinery.zag,
se_driver.zag, se_full.zag); binary se_bin; 3 run transcripts
(se_run1/2/3.txt, byte-identical).

What is missing: nothing material for the exploratory claim. No
frozen prereg. The researcher-set config bitmask is disclosed, not
hidden.

Acceptance condition for adoption: (1) frozen prereg; (2) sealed
evaluation on behavior batteries designed post-freeze; (3) the
researcher-set bitmask must be replaced by learner-owned arbitration
before any adoption claim about substrate arbitration, OR the adopted
claim must be explicitly bounded to "one substrate CAN drive five
behaviors" (existence), not "the substrate DOES arbitrate between
them" (agency); (4) an interference test: the five reads must not
destructively interact when all are live simultaneously (the current
batteries gate reads per battery); (5) independent reproduction and
the remaining pipeline steps.

## C186. PERSISTENT-CONNECTIONS (commit 105e9ee8b, 2026-10-01)

What was claimed: persistent cross-domain A-B connections (Micah
Priority 2). Addresses the spontaneous-lifetime finding (82dd6c00d)
that XEDGES a-b equals 0: prior rebinding was functional reuse, not
structural. The learner creates a persistent relation recording that
A helped construct B; much later C exploits the learned A-B
relationship. Tests faster later retrieval, better transfer, reusable
higher-level structure, ablation loss when the connection is removed.
No researcher-authored A-to-B mapping. 3/3 deterministic.

What evidence exists: REPORT.md (verdict
PERSISTENT-CONNECTIONS-COMPLETE; cognition delta pc_patch.zag on the
frozen TNN-2 base, base SHA-256 verified byte-identical to frozen;
control arm uses the vanilla rebind patch verbatim); NAMECHECK.md
with Step 0; full sources; three binaries (pc_ctrl_bin,
pc_treat_bin, pc_abl_bin); complete transcript sets (ctrl, treat,
abl each run1/2/3); compile logs. The most complete evidence package
of the eight.

What is missing: nothing material for the exploratory claim. No
frozen prereg.

Acceptance condition for adoption: (1) frozen prereg; (2) sealed
evaluation in which the "much later" reuse is tested after genuine
unrelated interference learning (distractor structures acquired
between B and C), not just a time gap; (3) a negative test: A-B
connections must NOT form for pairs where A did not help construct B
(false-connection rate); (4) independent reproduction and the
remaining pipeline steps.

## C187. UTILITY-INTEGRATION (commit ff0d91691, 2026-10-01)

What was claimed: Test 6 redundancy plus predictive utility plus
wrong-but-frequent attack (Micah Priority 6). Completes c912b9b19
(utility WORKS 5/6) by running the missing Test 6 control build.
Connects utility to learner-owned predictive success rather than
fixed plus2/minus2 events. Test 6 falsifies U-redundancy: U-order and
bid-order for MAP eviction are opposite in both U-arms (fixed and
predictive), while the no-U control follows bid order. Explicitly
attacks the wrong-but-frequently-used case: structures that predict
well, reduce search, enable later structures, and survive reuse
become more valuable than frequently-used-but-wrong structures.

What evidence exists: REPORT.md (verdict UTILITY-INTEGRATION-COMPLETE,
three experiments with result tables, 3/3 byte-identical per arm);
NAMECHECK.md with Step 0; full sources (ui_core_ctl.zag,
ui_core_pred.zag, ui_pred.zag, ui_util.zag, test drivers); complete
transcript sets (ctl, fixed, pred each run1/2/3). Complete.

What is missing: nothing material for the exploratory claim. No
frozen prereg.

Acceptance condition for adoption: (1) frozen prereg; (2) sealed
evaluation; (3) a consequence test: utility must be shown to change a
downstream decision (e.g., which structure gets built or kept under
memory pressure with a measurable capability difference), not only
eviction ordering, before adoption as "utility"; ordering alone is
evidence of non-redundancy, not of usefulness; (4) independent
reproduction and the remaining pipeline steps.

## C188. REBIND-HARDENING (commit 0509fd116, 2026-10-01)

What was claimed: scale, deception, and adaptation hardening (Micah
Priority 3). All 4 hardening worlds GRACEFUL, 3/3 byte-identical.
Zero crashes, zero hangs, zero false accepts on unmasked queries. Two
scale limitations documented (construction workspace limits,
wrong-plen scan cost). Extends db263d74c (REBIND-ADV-COMPLETE, 7
worlds GRACEFUL). Measures experienced-vs-fresh cost under 15 and 20
prior MAPs, deceptive MAPs, partial applicability, branched
topologies, negative transfer, and misleading structurally similar
MAPs.

What evidence exists: ADVERSARY.md (serves as the report: titled
"Rebinding Hardening Report", verdict REBIND-HARDENING-COMPLETE,
per-world measurements H1S/H2/H3/H4 with honest limitation notes);
NAMECHECK.md with Step 0; sources (hard_base.zag, hard_driver.zag,
hard_full.zag, hard_patch.zag); build.sh; compile_err.txt; 3 run
transcripts (hard_run1/2/3.txt). There is no separate REPORT.md; the
ADVERSARY.md carries the verdict and measurements, which is
sufficient for the exploratory claim.

What is missing: nothing material for the exploratory claim. No
frozen prereg. The scale-100 fixture was abandoned (documented as a
test-harness limitation, not a mechanism defect).

Acceptance condition for adoption: (1) frozen prereg; (2) sealed
evaluation on hardening worlds designed post-freeze by an independent
adversary; (3) the scale limitation must be re-tested in a larger
workspace before any scaling claim is adopted (the current evidence
supports "correct at 15-20 MAPs", not "scales"); (4) independent
reproduction and the remaining pipeline steps.

## Cross-cutting open items (adjacent to C181-C188, from the zombie investigation)

1. The protect-how retry commit (eb19a4f3c) adds no new NAMECHECK.md
   and records no Step 0 of its own; it inherits the protect-how
   lane record first committed in the fold-in 249a1b85e. The retry
   worker's own Step 0 record is still missing.
2. Ledger C189 was never appended: the governance report anticipated
   "Will be C189 when committed" for the protect-how retry, but
   eb19a4f3c does not touch the ledger. Either append C189 or record
   why it stays unledgered.

## Adoption checklist (all eight)

- [ ] C181: binaries/compile logs committed or REPORT.md section 8 amended
- [ ] C184: runs 2-3 transcripts committed, or determinism claim downgraded
- [ ] Each adopted claim: fresh frozen prereg (commit-order rule), sealed
      evaluation on post-freeze (adversary-designed where noted) worlds,
      independent 3/3 byte-identical reproduction, simple-baseline
      comparison, alternative-explanation attack, OOD test, ablation,
      transfer/reuse test, independent red team, governance audit
- [ ] No L3 or generality language attached to any of the eight until the
      L3 bar (Criterion 0 A-D plus the 12 criteria) is independently met
- [ ] C189 ledger disposition recorded; protect-how retry Step 0 recorded
