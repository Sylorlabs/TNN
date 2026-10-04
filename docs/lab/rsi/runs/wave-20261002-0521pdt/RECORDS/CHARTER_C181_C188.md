# Retrospective charter for C181-C188

Lane: RECORDS, wave-20261002-0521pdt. Date: 2026-10-02.
Required by: the wave-20261001-1721pdt zombie-lane investigation
(`docs/lab/rsi/runs/wave-20261001-1721pdt/GOV/ZOMBIE_INVESTIGATION.md`),
which found the seven commits were legitimate direct handoffs above
the 1421pdt coordinator (NOT a live zombie) and required this charter
before any claim is adopted beyond exploratory.

Method: no new experiments. Every statement below was verified against
the commit record with git (commit contents, REPORT files, transcripts,
NAMECHECK records, sha256 hashes). Commit ids are cited for every
claim. This charter supersedes the wave-20261002-0221pdt RECORDS
charter (`docs/lab/rsi/runs/wave-20261002-0221pdt/RECORDS/C181_C188_CHARTER.md`,
commit ac7f14ba6) on the three zombie-investigation gaps: the mli
run-2/run-3 transcripts and the C189 ledger entry have since entered
the record; the protect-how retry Step 0 has not and cannot.

## Standing ceiling

All eight are ledgered EXPLORATORY / BUILD-PASS (exploratory, no
frozen prereg) by governance wave 2 (293cf0672). That is the ceiling.
None may be cited as SURVIVES, as establishing generality, or as an
L3 result. None of the eight asserts L3. Promotion beyond exploratory
requires the 11-step frontier promotion pipeline (2026-09-29
strategic reorientation): committed preregistration, implementation,
sealed evaluation, independent reproduction from committed source,
simple-baseline comparison, alternative-explanation attack, OOD test,
ablation, transfer/reuse test, independent red team, governance
audit. Builders report BUILD-PASS/BUILD-FAIL only.

## C181. LEARNER-VERIFICATION (commit d52666a8b, 2026-10-01)

Claimed: learner-owned prediction reliability replaces
researcher-provided `expected` for revision acceptance (Micah Priority
1). V4 revision acceptance PASS; honest withholding when no reliable
predictor exists. Ledger also records: V2 INVALID (design flaw),
cross-subject candidate acceptance BLOCKED, direct candidate
rejection UNTESTED.

Evidence in the commit: REPORT.md (verdict
LEARNER-VERIFICATION-COMPLETE); NAMECHECK.md with Step 0; full source
set (lv_base.zag, lv_cog.zag, lv_driver.zag, lv_full_ctl.zag,
lv_full_trt.zag, lv_patch.zag, lv_patch_ctl.zag); 6 transcripts
(run_ctl_1/2/3.txt, run_trt_1/2/3.txt). 15 files total.

Missing: REPORT.md section 8 (lines 223-226) lists `lv_trt_bin`,
`lv_ctl_bin`, `compile_trt.log`, `compile_ctl.log` as artifacts, but
the commit contains zero binaries and zero compile logs (verified:
no bin/compile path in d52666a8b). The artifact list overstates what
is committed.

Status: BLOCKED for adoption beyond exploratory. The evidence package
is incomplete (binaries/logs absent), V2 is invalid, and cross-subject
acceptance is BLOCKED. Adoption requires the missing artifacts (or an
amended REPORT.md), a repaired V2 or a dropped direct-rejection
claim, and the full pipeline including a cross-subject acceptance
family.

## C182. ADAPTIVE-THRESHOLD (commit b6135c531, 2026-10-01)

Claimed: the evidence threshold is a learner-state value written by
experience, not researcher-fixed (Micah Priority 8). One evidence
node holds run value, run length, error score, and T = 2 + E/3
clamped to [2,5]. T=2 in stable, T=5 in noisy, T=3 (transient) in
changing environments. 3/3 byte-identical per arm.

Evidence in the commit: REPORT.md (verdict
ADAPTIVE-THRESHOLD-COMPLETE); NAMECHECK.md with Step 0; sources
(at_core_adaptive.zag, at_core_fixed.zag, drivers, at_tests.zag);
6 transcripts (adaptive/fixed x run1/2/3); both binaries committed
(at_bin_adaptive, at_bin_fixed); at_build.sh. Complete transcript
set for the determinism claim.

Missing: nothing material for the exploratory claim. No frozen
prereg (exploratory by ledger status).

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation on
post-freeze adversary-designed noise schedules, a transfer test to a
new environment family, and the remaining pipeline steps.

## C183. PROVENANCE-LEARNING (commit 96fa237b1, 2026-10-01)

Claimed: source reliability learned from consequences, no hardcoded
OBSERVED-greater-than-INFERRED rank (Micah Priority 4). Treatment
switches source A to B from experience as B degrades; hardcoded
control stuck 0/4 in P5. Builds on C170 and 9e9a2e372. 3/3
deterministic per arm.

Evidence in the commit: REPORT.md (verdict
PROVENANCE-LEARNING-COMPLETE); NAMECHECK.md with Step 0; full
sources; 6 transcripts (pl_ctl/pl_trt x run1/2/3); both binaries
committed (pl_ctl_bin, pl_trt_bin); build.sh. Complete.

Missing: nothing material for the exploratory claim. No frozen
prereg. Risk noted for the pipeline: exactly two teachers and a
researcher-authored degradation schedule, so the switching result may
be schedule-shaped.

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation with a
post-freeze degradation/recovery schedule, more than two sources with
simultaneous degradation, and the remaining pipeline steps.

## C184. MINI-LIFETIME-INTEGRATION (commit 1963e994d, 2026-10-01)

Claimed: 3-arm persistent comparison (Micah Priority 9): A. frozen
TNN-2, B. reuse/rebinding, C. consequence plus provenance plus
structural protection integration. No resets. 3/3 byte-identical per
arm, with asserted SHA-256 prefixes (A 25749820f2c4a025, B
de6a9e18ed2d731d, C a0673125573b7da1).

Evidence in the commit: REPORT.md (verdict
MINI-LIFETIME-INTEGRATION-COMPLETE); NAMECHECK.md with Step 0;
sources (mli_full_A/B/C.zag, mli_driver.zag, mli_query.zag,
mli_protect_fns.zag, mli_rebind_fns.zag, mli_substrate_fns.zag);
binaries (mli_bin_A/B/C). The builder's own commit carried only
run-1 transcripts (mli_run_A1/B1/C1.txt). See Gap 1 below for the
run-2/run-3 disposition.

Missing (in the builder commit): runs 2 and 3 per arm. No frozen
prereg.

Status: exploratory BUILD-PASS stands (evidence gap closed, see Gap
1). BLOCKED for adoption beyond exploratory: this is the
continuing-learner integration claim, so adoption requires a fresh
frozen prereg with the event sequence and measurements fixed before
implementation, sealed evaluation on a post-freeze event stream with
unrelated interference and delayed-reuse probes, and the remaining
pipeline steps. No adoption on report-asserted hashes alone.

## C185. SUBSTRATE-EXPANSION (commit 02a338dbf, 2026-10-01)

Claimed: 5 behaviors from one consequence substrate with
per-behavior ablations (Micah Priority 5). The same tag-61 store
drives policy adaptation, withholding, abandonment, retention, and
search-order changes; ablations show the same consequence records
matter to multiple behaviors. All batteries PASS. 3/3 deterministic.

Evidence in the commit: DESIGN.md; REPORT.md (verdict
SUBSTRATE-EXPANSION-COMPLETE, per-battery results with ablation
arms); NAMECHECK.md with Step 0; sources (se_base.zag,
se_behaviors.zag, se_machinery.zag, se_driver.zag, se_full.zag);
binary se_bin; 3 transcripts (se_run1/2/3.txt). Honest boundary
disclosed in the report: the config bitmask is researcher-set per
battery, not learned; learner-owned arbitration between the five
reads is future work.

Missing: nothing material for the exploratory claim. No frozen
prereg.

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation on
post-freeze behavior batteries, replacement of the researcher-set
bitmask by learner-owned arbitration (or an explicitly bounded
existence-only claim: the substrate CAN drive five behaviors, not
that it DOES arbitrate), an all-reads-live interference test, and
the remaining pipeline steps.

## C186. PERSISTENT-CONNECTIONS (commit 105e9ee8b, 2026-10-01)

Claimed: persistent cross-domain A-B connections (Micah Priority
2). The learner creates a persistent relation recording that A
helped construct B; much later C exploits the learned A-B
relationship. No researcher-authored A-to-B mapping. 3/3
deterministic.

Evidence in the commit: REPORT.md (verdict
PERSISTENT-CONNECTIONS-COMPLETE; cognition delta pc_patch.zag on the
frozen TNN-2 base); NAMECHECK.md with Step 0; full sources; three
binaries (pc_ctrl_bin, pc_treat_bin, pc_abl_bin); complete
transcript sets (ctrl, treat, abl each run1/2/3); compile logs. The
most complete evidence package of the eight.

Missing: nothing material for the exploratory claim. No frozen
prereg.

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation with genuine
unrelated interference between B and C (not just a time gap), a
negative test (A-B connections must NOT form where A did not help
construct B), and the remaining pipeline steps.

## C187. UTILITY-INTEGRATION (commit ff0d91691, 2026-10-01)

Claimed: Test 6 redundancy plus predictive utility plus
wrong-but-frequent attack (Micah Priority 6). Test 6 falsifies
U-redundancy: U-order and bid-order for MAP eviction are opposite in
both U-arms, while the no-U control follows bid order. Utility tied
to learner-owned predictive success rather than fixed plus2/minus2
events.

Evidence in the commit: REPORT.md (verdict
UTILITY-INTEGRATION-COMPLETE, three experiments with result
tables); NAMECHECK.md with Step 0; full sources; complete
transcript sets (ctl, fixed, pred each run1/2/3). Complete.

Missing: nothing material for the exploratory claim. No frozen
prereg.

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation, and a
consequence test: utility must change a downstream decision under
memory pressure with a measurable capability difference, not only
eviction ordering (ordering alone is non-redundancy evidence, not
usefulness evidence), plus the remaining pipeline steps.

## C188. REBIND-HARDENING (commit 0509fd116, 2026-10-01)

Claimed: scale, deception, and adaptation hardening (Micah Priority
3). All 4 hardening worlds GRACEFUL, 3/3 byte-identical. Zero
crashes, zero hangs, zero false accepts on unmasked queries. Two
scale limitations documented (construction workspace limits,
wrong-plen scan cost).

Evidence in the commit: ADVERSARY.md serves as the report (titled
"Rebinding Hardening Report", verdict REBIND-HARDENING-COMPLETE,
per-world measurements H1S/H2/H3/H4 with honest limitation notes).
There is NO separate REPORT.md in this commit; the ADVERSARY.md
carries the verdict and measurements, which is sufficient for the
exploratory claim but is a naming inconsistency worth noting.
NAMECHECK.md with Step 0; sources (hard_base.zag, hard_driver.zag,
hard_full.zag, hard_patch.zag); build.sh; compile_err.txt;
3 transcripts (hard_run1/2/3.txt). The scale-100 fixture was
abandoned and documented as a test-harness limitation, not a
mechanism defect.

Missing: nothing material for the exploratory claim. No frozen
prereg.

Status: exploratory BUILD-PASS stands. BLOCKED for adoption beyond
exploratory pending a frozen prereg, sealed evaluation on
post-freeze adversary-designed hardening worlds, and re-testing the
scale limitation in a larger workspace (current evidence supports
"correct at 15-20 MAPs", not "scales"), plus the remaining pipeline
steps.

## The three zombie-investigation gaps: explicit disposition

### Gap 1. mli run-2/run-3 transcripts: LOCATED, VERIFIED, CLOSED

The builder commit 1963e994d carried only mli_run_A1/B1/C1.txt. All
nine transcripts (mli_run_A1/A2/A3, B1/B2/B3, C1/C2/C3.txt) are now
committed at HEAD and were verified this lane:

- Within each arm the three runs are byte-identical (sha256: A
  25749820f2c4a02553885e495fc2dcfc023255b9eea2164adc8596d54b988655,
  B de6a9e18ed2d731dc428d6b744ec5d1f76f2755a224acf21bed85b3925d795a8,
  C a0673125573b7da1999bdfb58d1ed26af61714a2a48288765fba71acf33a617b).
- These match the REPORT.md line 123 asserted prefixes exactly (A
  25749820f2c4a025, B de6a9e18ed2d731d, C a0673125573b7da1).

Provenance noise, stated plainly: runs 2-3 did NOT enter through the
builder's own commit. They were folded in by 249a1b85e (2026-10-01
21:58:53 UTC, "fold in uncommitted research files"), then deleted by
f461e812d and re-added by 9139a579c; the re-add is byte-identical to
the fold-in (verified: `git diff 249a1b85e 9139a579c` empty on these
paths). The 3/3 determinism claim is now backed by committed bytes,
not report assertion. The 0221pdt charter checklist item for C184 is
closed.

### Gap 2. protect-how retry Step 0: MISSING, UNRECOVERABLE, MARKED

The retry commit eb19a4f3c (2026-10-01 22:13:26 UTC) touches exactly
three paths: protect_how/REPORT.md, ph_ctl_run2.txt, ph_ctl_run3.txt.
It adds no NAMECHECK.md and records no Step 0 of its own. The Step 0
record present in protect_how/NAMECHECK.md at that commit is the
earlier (throttled) worker's, first committed via the fold-in
249a1b85e, not the retry worker's.

The retry worker's only toolchain evidence: REPORT.md line 13 ("Pure
Zag via pinned znc. Safebin active, zero forbidden executables") and
the commit message ("pure Zag; safebin"). A retroactive Step 0 cannot
be manufactured now; the moment it would have recorded is gone, and
inventing one would be a fabrication, not a record.

Mitigation, not closure: the 1721pdt fork battery FRESH PASSes the
seven-commit chain including eb19a4f3c (toolchain integrity at each
commit). This gap is a permanent governance blemish on C189
(PROTECT-HOW): its exploratory BUILD-PASS stands, but any promotion
path must re-run the retry under a recorded Step 0. This checklist
item stays OPEN with this note as its final disposition.

### Gap 3. C189 ledger append: DONE, CLOSED

Commit 245ecb5b9 (Fri Oct 2 05:00:30 UTC, "Governance: C189
protect-how appended") appended the C189 entry to
`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`.
The current ledger entry (lines 5353-5371) matches the appended
bytes exactly. C189 (PROTECT-HOW; commit eb19a4f3c, 2026-10-01) is
ledgered COMPLETE (exploratory, no frozen prereg): generative
structure protection by eviction order, 3/3 deterministic per arm,
BUILD-PASS (exploratory), with the honest boundary that the 3-tier
policy is researcher-authored (LEARNER-OWNED structural decisions:
0). The zombie investigation's "C189 never appended" finding is
superseded by this commit. The 0221pdt charter checklist item for
C189 is closed.

## Adoption verdicts, stated plainly

ADOPTABLE as exploratory BUILD-PASS records (evidence on disk;
citable at exploratory level, no promotion): C182, C183, C184
(evidence gap closed this charter), C185, C186, C187, C188, C189
(ledgered; Step 0 blemish noted in Gap 2).

BLOCKED from any promotion beyond exploratory (no frozen prereg on
any; the 11-step pipeline is mandatory): ALL of C181 through C189,
without exception. Specific additional blockers: C181 (incomplete
artifact package; V2 invalid; cross-subject BLOCKED), C184
(continuing-learner claim needs a fresh frozen prereg with sealed
evaluation), C185 (researcher-set bitmask or bounded existence-only
claim), C189 (unrecoverable retry Step 0; researcher-authored
3-tier policy).

No claim in this charter is adopted, promoted, or re-scored. This
charter closes the evidence-completeness portion of the
zombie-investigation follow-ups; the promotion pipeline remains the
only path forward.

Note: no em-dashes are used in this document.
