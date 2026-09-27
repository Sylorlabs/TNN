# SKEPTIC REPORT: wave-20260927-0521pdt

Role: skeptic, mandatory debate group. Evidence read in full:
FORK_RESULTS_0521.md, LANE_SURVEY_0521.md, INTERACTIVE_0521.md.
Independent verification performed with read-only git, shell, grep,
sha256sum. No Python anywhere. Zero em-dashes in this document.

## The skeptic's provenance probe

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer. The artifacts under judgment this wave are three worker
products plus standing items. Genuinely NEW this wave (freshly
executed or freshly read): the fork battery's 47 re-executions with
per-entry evidence and uniform greps; the rebuilt pure-Zag harness
whose sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
matches the frozen value and whose binary is byte-identical to prior
waves; the lane survey's fresh git scan of the 02:21 to 05:21 PDT
window (23 commits, verified independently); the interactive survey's
fresh pin verifications and the 463b115b6..ecbe9b5b7 entry-point scan
(1390 added files, zero keyword hits); the enumeration manifest
artifact (exists, uncommitted); the clean-merge verification of the
05:22 PDT run-start merge (empty combined diff, verified
independently). INHERITED (carried by citation, not re-executed): the
tnn_chat behavioral FIT battery, last actually run at
wave-20260925-1421pdt (evidence 9692f5d1d) and carried by citation
across 11 consecutive waves including this one; the pull-head
extraction FAIL cause attribution (sound, because the commits are
unchanged and git content-addressing makes same-commit means same-tree,
but not re-inspected); the prior wave's LOOP_STATE verdicts and the
prereg commit-order results the survey re-presents; DP-1's "ready"
status (from the 09-26 dossier, not freshly verified); the six
governance rulings and sealed-pair states (untouched, standing). The
verdict slate's [RE-CERT] labels do not all distinguish these two
classes, and that is the central weakness attacked below.

## Attack 1: the [RE-CERT] label on the stand-down is unearned language

Proposed verdict 2 reads "No-new-candidates stand-down: CONFIRM
[RE-CERT]." A stand-down is a negative finding from a fresh scan, not
the re-certification of a prior positive. The lane survey did fresh
work (23-commit window scan, 4 prereg filename hits all attributed to
closed prior-wave workstreams, 0 re-aimed preregs, 0 new design docs,
0 lane-directory touches, 37 untracked entries with 0 drafts), and I
verified the 23-commit count independently. The scan itself is sound.
But CONFIRM [RE-CERT] borrows the authority of positive verification
for an absence, and it lets the wave's verdict read as an endorsement
of productivity. This wave produced zero design or implementation
output toward any queued blocker: EXP1c still has zero material
anywhere in the repo, EXP2's grounding blocker is untouched, the
frozen enumeration manifest is still uncommitted (see Attack 4), B1's
P9 bar reformulation is still not found, COMP-2's P11
stemmer-contingency is still unresolved. The survey discloses every
one of these as NOT cleared, which is honest, but the slate's verdict
line does not carry them. A stand-down verdict that omits the open
blocker list can be misread as "all is well" when the accurate reading
is "no candidates, and no progress on the hard items either."

Recommendation: NARROW verdict 2. Relabel to STAND-DOWN on a fresh
scan (not CONFIRM [RE-CERT]), and require the verdict line to carry
the open blocker list explicitly. Discipline is not ducking, but the
verdict must not let the distinction blur.

## Attack 2: the tnn_chat FIT is 11 waves stale and still labeled [RE-CERT]

Proposed verdict 3 reads "Interactive TNN: CONFIRM [RE-CERT]." What
was actually fresh this wave: binary and source pin verifications
(all MATCH), the 10-commit entry-point scan with zero keyword hits,
and my own independent spot check of the 6 new .zag files in range
(plan_r3.zag, deliberate_frozen_r4repair2.zag, R33_NATIVE_IO_V1.zag,
R33_NATIVE_SHA256_V2.zag, ehelp.zag, epistemic.zag): zero stdin reads
in all six, so the "no new interactive entry point" conclusion holds.
What was NOT fresh: the behavioral FIT battery itself (2/2 binary
reproducibility, 9/9 rerun pairs byte-identical, KB1 30/30, KB2 17/17,
KB5 10/10), last executed at wave-20260925-1421pdt and carried by
citation under P12/P16 across 11 consecutive waves including this one,
roughly 39 hours. The report discloses "determinism cited, not
re-run," which is honest, but the verdict label [RE-CERT] then
re-certifies a behavioral battery nobody ran. Pin integrity is not
behavioral integrity: pins prove the binaries and sources are the
same bits, not that the KB batteries still pass on today's tree. A
citation chain 11 waves long with no re-run cadence is inheritance,
not re-certification.

Recommendation: NARROW verdict 3. Split it: CONFIRM (fresh) on pins
and the entry-point scan; FIT behavioral battery CARRIED BY CITATION,
stale at 11 waves. Mandate a re-run cadence (for example every 8
waves) and fix the standing record defect the report itself carries:
docs/lab/rsi/fit_authority/SHA256SUMS still does not exist, pins still
live in README.md. A defect confessed for 11 waves without repair is
not a caveat, it is neglect.

## Attack 3: the interactive scan's methodology has a keyword blind spot

The entry-point scan is three keyword stems (chat, repl, interactive)
plus manual review of two close cases. I verified the two close cases
are genuinely batch harnesses with zero stdin reads, and my spot
check of all six new .zag files found no stdin reads. This wave is
clean. But the methodology would pass an interactive mechanism that
avoids those three stems: nothing in the standing procedure scans for
stdin reads, argv-driven REPL loops under other names, or socket
listeners as a backstop. The survey got the right answer this wave;
the procedure does not guarantee it gets the right answer every wave.

Recommendation: keep the verdict, but add a stdin-read backstop grep
over new .zag sources to the standing interactive procedure. Cheap,
and it closes the exact hole the current method leaves open.

## Attack 4: the frozen enumeration manifest is "done" and "NOT cleared" at the same time

The task premise for this debate says the frozen enumeration manifest
is done. FORK_RESULTS_0521.md says ENUMERATION_MANIFEST.md in the run
dir lists every named entry. I verified the file exists
(docs/lab/rsi/runs/wave-20260927-0521pdt/forks/ENUMERATION_MANIFEST.md).
But LANE_SURVEY_0521.md lists the manifest blocker as NOT cleared
because "no manifest committed in this window," and indeed the entire
wave dir is uncommitted (git status shows
?? docs/lab/rsi/runs/wave-20260927-0521pdt/). The fork worker treats
the artifact as done; the survey worker treats the queued item as
open; the debate premise treats it as done. Three different answers
to one yes-or-no question. If the queued item required a committed
frozen manifest, it is not cleared, and the premise is wrong. If the
run-dir artifact counts, the survey is wrong. The debate must pick one
and write it down.

Recommendation: carry the manifest item as OPEN until the manifest is
committed (commits stay local per the red lines; nothing here requires
a push). Do not let two workers silently disagree inside one wave's
verdict slate.

## Attack 5: the prereg commit-order check verifies timestamps, not run order, and this repo's timestamps are unreliable

The slate correctly marks this wave's check VACUOUS: no new preregs
were drafted this wave, nothing was adopted, so there is nothing for
the check to gate. I verified the survey's re-presented prior-wave
orderings against git directly: 7e0326d2c 09:34:19 precedes 938d188cb
09:49:21; 06e28f088 09:38:41 precedes 32eadf722 09:43:14; 4a937d994
09:41:06 precedes aa76f9b8d 09:45:21. The timestamps are as the survey
claims. But two facts gut the check's strength as a governance
instrument. First, commit d758a876c3 ("Native-deliberation epistemics
Phase 1") carries author and committer dates of 2026-09-27 07:50 PDT,
about five and a half hours in the future relative to the merge that
contains it (af657c8e5, 02:24 PDT). Timestamps in this repo are not
trustworthy; any close call decided on timestamp order is decided on
unreliable data. Second, the LIGHT-FIELD amendment c6b8190f3 sits at
09:45:20, exactly one second before the implementation commit
aa76f9b8d at 09:45:21. The survey claims it "independently confirmed"
the amendment is "pre-run" with "no scores seen." Commit order can be
confirmed; "no scores seen" cannot. A one-second margin on
untrustworthy clocks proves nothing about when the code actually ran.
The governance rule as tightened speaks of commit order, and on commit
order the three preregs PASS. The survey overclaims when it presents
"pre-run" as an evidenced finding rather than an asserted one.

Recommendation: keep VACUOUS for this wave, but attach the caveat to
the standing rule: the check evidences commit order only, never run
order, and margins under a minute on this repo's clocks should be
flagged as weak rather than reported as PASS without qualification.

## Attack 6: the 05:22 PDT run-start merge sat outside the survey window

Probed and largely cleared, but the process point stands. The lane
survey's window ends 05:21 PDT; the run-start merge ecbe9b5b7 is
stamped 05:22:13 PDT and was "not surveyed here." I verified
independently: the merge's combined diff is empty (no
conflict-resolution edits beyond either parent), and its 9 integrated
commits are exactly the 9 Micah-authored frontier commits the survey
characterized individually (b257c02cc through 7aad68fad, 02:27 to
03:54 PDT). Content risk: nil. But the stand-down verdict is stamped
on a wave whose own run-start HEAD includes a merge commit the lane
survey explicitly did not cover, and the next wave's survey inherits
the obligation by a one-minute seam. The loop got a clean merge this
time; the procedure does not require verifying that. A conflicted
merge landing at 05:22 would have entered the working HEAD
unsurveyed.

Recommendation: no verdict change needed on the facts (the merge is
verified clean), but the standing procedure should require the survey
window to cover the run-start merge, or require the fork battery's
scope stamp to include merge-resolution review when the run-start
merge is conflicted. Disclosed seams are better than lucky ones.

## Attack 7: the in-window 02:24 merge integrated 52 upstream commits the survey never characterizes

Commit af657c8e5 (02:24 PDT, in-window) merged origin/tnn-native-lab,
52 commits ahead. The survey characterizes the merge's conflict
resolutions (18 add/add conflicts in docs/lab/invention/survival/,
resolved keeping both sides as .origin-wave.* files; I verified the
combined diff shows only those files, no ruling-named files touched).
But the 52 upstream commits themselves (51 by micahcooley, 1 by Muse:
f7968ee15 "One-brain round 2: independent red-team report (Worker C)")
are not characterized anywhere in this wave's survey; the "23 commits
in the window" accounting (9 his, 14 loop) does not mention them.
They fall inside the prior wave's window (23:31 09-26 to 02:17 09-27,
plus the one future-dated outlier), so coverage depends on the 0221pdt
survey having characterized origin-side commits it had not yet merged.
The fork battery stamps all of it "CLOSED, not re-litigated." That
stamp is doing heavy lifting: 52 commits, including one loop-authored
commit, enter the working tree on the strength of a scope decision,
not a review.

Recommendation: no overturn on the facts (the 52 are his frontier
plus one prior-wave red-team report, all inside the prior window),
but the survey should explicitly account for merged upstream ranges
each wave: count, author split, and which wave's survey covered their
content. "CLOSED, not re-litigated" needs a cited prior review, not
just a stamp.

## Attacks probed and conceded (cleared on evidence)

- 49 vs 48 named entries: the +1 is real new coverage, not
reclassification. arch-20260927-0221pdt tips 463b115b6, the 0221pdt
wave record, which postdates the 0221pdt battery's run-start HEAD and
was therefore never battery-tested before. The renamed branch
arch-wave-20260926-2321pdt tips the identical commit 004616f65
(verified), so the rename is count-neutral with continuous coverage.
No hidden coverage loss.
- rh-tnn-native-lab-live-tip superseded pinning: the ref pins
b257c02cc (Micah's own 02:27 PDT chunker commit, verified) while the
live origin tip is 7aad68fad; the live value is covered by the
origin-tnn-native-lab-rt entry and closing ls-remote showed no tip
movement during the run. The "live-tip" name is now misleading, but
the no-coverage-gap claim is verified. Hygiene note only: rename or
annotate the ref.
- The two extraction FAILs: same commits as eight waves running, so
git content-addressing makes the "unchanged cause" attribution sound
without re-inspection. The FAIL evidence dirs hold RESULT.txt and
extract.err with the exact fatal messages. Conceded as genuinely
expected, not a fresh gap.
- 49 evidence dirs present (count verified), 0 znc.bin files in the
evidence tree (verified), 47/47 uniform evidence claims are at least
structurally plausible with per-entry files present.
- Headline inflation: 49 named entries cover 39 unique commits; the
P19 accounting discloses the duplicates explicitly. The verdict line
should carry the unique-commit count, but the disclosure is present.
- "Experiment workers implementing concurrently" vs "already merged":
both true at once is possible (merged tips, workers adding new
commits in checked-out worktrees; the + prefix in branch output
confirms worktree checkouts). But the battery certifies run-start
pins, not branch tips. The verdict language should say pinned
commits, not branches.
- Governance rulings and sealed pairs untouched: VERIFIED. No
wave-worker commits exist; the two in-window merges' resolutions
touched only .origin-wave.* files; no ruling-named files. The
survey names the rulings without relitigating them. UNTOUCHED stands.
- DP-1 queue-HELD: the "ready" status is inherited from the 09-26
dossier (DP1_DOSSIER_1121.md, queue-HELD since the 1121pdt/1421pdt
rulings), not freshly verified this wave. Keep queue-HELD, but the
readiness citation should travel with the verdict rather than being
re-asserted bare.
- The V-D directional rule from his REDTEAM_R3: correctly marked
CLOSED as his frontier existence proof. Standing caution only: the
loop must not adopt it without his ruling; no evidence of violation.
- Zero-Python attestations: the fork and interactive workers'
attestations are consistent with their described toolchains (shell,
git, sha256sum, grep, pinned znc, pure-Zag harness). No counter
evidence found.

## Verdict recommendations

1. Fork battery CONFIRM [RE-CERT]: KEEP, with the verdict line
amended to carry the unique-commit count (39 unique commits across
49 named entries; 47 PASS, 2 expected extraction FAILs) and the
toolchain-stability-only scope. Probed clean on the coverage delta.
2. No-new-candidates stand-down: NARROW. Relabel STAND-DOWN on a
fresh scan; drop CONFIRM [RE-CERT]; carry the open blocker list
(EXP1c design, EXP2 grounding, manifest commit, B1 P9, COMP-2 P11)
in the verdict line.
3. Interactive TNN: NARROW. Split the verdict: fresh CONFIRM on pins
and the entry-point scan; FIT behavioral battery CARRIED BY CITATION
at 11 waves stale. Mandate a re-run cadence and repair the
fit_authority/SHA256SUMS record defect.
4. Prereg commit-order self-check VACUOUS: KEEP the label for this
wave; attach the standing caveat that the check evidences commit
order only, never run order, and sub-minute margins on this repo's
clocks are weak evidence.
5. Governance rulings and sealed pairs UNTOUCHED [VOID]: KEEP.
Verified on evidence.
6. DP-1 queue-HELD: KEEP, with the readiness citation (09-26
dossier) attached instead of re-asserted bare.
7. New open item for the slate: resolve the enumeration manifest
contradiction (done as artifact vs NOT cleared as uncommitted) with
a single written answer; carry it open until committed.

The loop's evidence discipline this wave is high and most of its
claims survived independent re-checks. The failures are in labeling
honesty ([RE-CERT] on inherited or negative findings), stale
carry-overs with no re-run cadence, and a commit-order check that
cannot prove what its writeups claim it proves.
