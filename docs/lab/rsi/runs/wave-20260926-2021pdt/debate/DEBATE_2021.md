# Debate transcript: wave-20260926-2021pdt

Debate group session for TNN RSI loop wave wave-20260926-2021pdt
(Sylorlabs/TNN, branch tnn-native-lab). Roles: ADVOCATE argues FOR
adoption, SKEPTIC argues AGAINST, JUDGE renders a reasoned ruling with
numbers cited. A verdict can be overturned only with cited evidence,
never rhetoric. Documentation rule observed throughout: no em-dashes
and no en-dashes anywhere.

Evidence under judgment, read in full before debate:
- forks/FORK_RESULTS_2021.md (fork battery)
- interactive/INTERACTIVE_2021.md (interactive-TNN survey)
- survey/LANE_SURVEY_2021.md (lane survey)
- the null prereg commit-order self-check record

## Procedural opening

JUDGE: This debate rules on four motions. M1: CONFIRM the fork battery,
proposed tag [RE-CERT]. M2: CONFIRM the interactive-TNN survey, proposed
tag [RE-CERT]. M3: CONFIRM the no-new-candidates stand-down, proposed tag
[RE-CERT]. M4: prereg commit-order self-check labeled VACUOUS per P17,
proposed tag [VACUOUS]. The SKEPTIC opens the proceedings with the
mandatory provenance probe.

SKEPTIC: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

JUDGE: Recorded. The slate-level answer, which each motion ruling below
will particularize: the artifacts under judgment are four wave artifacts
produced by this wave's workers against the task-pinned run-start HEAD
fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91. Nothing under judgment is a
loop-authored mechanism candidate. What is new this wave: the three
survey and battery executions themselves (new evidence gathered
2026-09-26 against the new HEAD), one newly enumerated local archive
branch (tnn-native-lab-wave-archive-wave-20260926-1721pdt at a4d4ff7cd),
and two newly untestable live remote tips (rh-tnn-native-lab-tip-start at
d9ddc556, rh-main at 27a4271f). What is inherited: the pinned znc
toolchain binary (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
byte-identical across waves), the frozen pure-Zag harness
fork_battery.zag (extracted sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
matching the expected value), the three frozen interactive pins, every
fixture entry with an unchanged SHA, and the stand-down posture itself.

---

## Motion M1: CONFIRM the fork battery for wave-20260926-2021pdt

ADVOCATE: The battery reports 40 named entries: 36 PASS, 4 extraction
FAIL. Of the FAILs, two are the expected ones, origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, whose trees lack the pinned
toolchain path, identical cause five waves running. The other two are
live remote tips rh-tnn-native-lab-tip-start at d9ddc556 and rh-main at
27a4271f, whose commit objects are absent from the local object store
because the origin tips moved after the executor's merge snapshot and no
fetch is performed by this worker under the frozen procedure. That is a
disclosed coverage gap, not a toolchain regression. On the tested
entries, the evidence is byte-uniform across all 38 tested runs (36
battery plus 2 spot): znc pin
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef at
38 of 38, probe source sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919 at
38 of 38, B2 bin sha
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2 at
38 of 38 (parsed with sed, never cut), NEG1 failing with E0002 at 38 of
38, NEG2 stdout differing from expected at char 1 at 38 of 38, and the
fork-tree probe printing R32_ZNC_PROBE_OK at 38 of 38. The SPOT_RE_RUN
confirmed all three 1721pdt verdicts (live local PASS, fixture worktree
PASS, pull/1 extraction FAIL) before anyone cited them. P19 delta
accounting is complete and named: entries 39 to 40 from the newly
enumerated archive branch, live 4 to 5 (plus the new archive branch,
plus the moved rh-main, minus arch-wave-20260926-1421pdt reclassified
fixture), FAILs 2 to 4 from the two absent-locally remote tips, unique
commits 31 to 33. Closing tip re-check: origin tips unchanged during the
run, local HEAD unchanged at
fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91, no fetch. The mid-run driver
bug was caught before any result was cited: every bogus evidence dir was
deleted, zero survive, the batch was rerun with correct name and ref
pairs, and all 43 surviving evidence dirs were verified against the
corrected run log. I move CONFIRM with the certified scope stamp:
toolchain and extraction stability only, on tested entries.

SKEPTIC: I oppose a clean CONFIRM, and I argue the coverage gap first.
Two of the five live entries, 40 percent of the live edge, are
untestable this wave. rh-main moved 0ab8ed6b to 27a4271f since 1721pdt,
and rh-tnn-native-lab-tip-start sits at d9ddc556, a distinct commit from
the remote-tracking 75267f9df that was actually tested. These are the two
freshest remote states in the repo, and neither was tested. The battery
cannot certify the current remote state, and the no-fetch frozen
procedure is the cause of the gap. Confirming the battery CONFIRM risks
entrenching a procedure that systematically misses remote movement while
wearing a passing headline. Second, the headline counts are padded by
duplication: 40 named entries but only 33 unique commits, 35 fixtures,
many testing identical SHAs (the 9914322267 commit tested four times,
the bd3097874 commit tested four times, per P8). The PASS count reads
larger than the tested diversity. Third, the mid-run driver bug: jobs
ran with empty refs, and git would have resolved extraction against the
working tree instead of the entry's commit. A bug that corrupts the
extraction ref strikes at the heart of the battery. The rerun is claimed
clean, but the same driver family produced the bug. Fourth, pull/1 and
pull/2 have failed extraction five waves running: a permanently
uncovered hole in two repos the battery claims to cover. I argue M1 is
not CONFIRMable as a whole; at best it is confirmable in part, and the
unconfirmed part must be named.

JUDGE: M1 is contested, so I rule with numbers and address each
objection in order.

On the coverage gap: the gap is real, disclosed, and quantified in the
report itself. Tested entries: 36 of 36 PASS, 100 percent. Tested runs:
38 of 38 byte-uniform on every check. Testable live entries: 3 of 3
PASS (local-tnn-native-lab at fe1b5e2c0, arch-20260926-1721pdt at
a4d4ff7cd, origin-tnn-native-lab-rt at 75267f9df). Untestable live
entries: 2 of 5, recorded as a coverage gap, not as failures and not as
a toolchain regression. Unique commits tested: 29 of 33. The report
stamps its own scope: this battery certifies toolchain and extraction
stability only, not the contents of the merged commits, and it
recommends that the next wave fetch before enumeration or that the
coordinator make the new tip commits available locally. I mint P20 for
this: when live remote tips are untestable under the no-fetch frozen
procedure, the battery may still be CONFIRMed only under an explicit
scope stamp limiting certification to the tested entries, with the
untested tips recorded as a coverage gap rather than as failures. The
skeptic's fear that CONFIRM launders the gap is answered by the stamp
itself: the ruling certifies toolchain and extraction stability on
tested entries, and nothing about the untested tips.

On duplication: every duplicate is disclosed with SHAs under P8, not
hidden. Fixture duplication is the point of a regression battery:
coverage of unchanged states across waves. The tested-diversity number
is stated openly (33 unique commits, 29 tested), so no one is misled by
the 40-entry headline.

On the driver bug: the incident is disclosed in the report. The bug was
caught before any result was cited, every bogus evidence dir was
deleted with zero surviving, the batch was rerun with correct name and
ref pairs, and all 43 evidence dirs were verified against the corrected
run log. I mint P21 for this: a mid-run driver bug that is caught before
any citation, with every bogus evidence dir deleted and the batch rerun
cleanly against the corrected run log, does not void the battery
verdict. The skeptic offered no evidence that the corrected rerun was
tainted; the verification count (43 dirs against the corrected run log)
is the evidence.

On pull/1 and pull/2: their trees hold non-TNN research documents, no
src/ directory, no toolchain path, and the probe path is likewise
absent. They are untestable by this battery until their trees gain the
pinned toolchain path. Identical cause five waves running makes this a
property of those forks' contents, not a toolchain regression and not a
hidden hole: it is an open, named, persistent extraction failure.

Ruling: M1 is CONFIRMED. Tag: [RE-CERT]. Scope stamp: toolchain and
extraction stability only, on the 36 tested entries and 38 tested runs.
The two untestable live remote tips (d9ddc556, 27a4271f) are carried
forward as an open coverage gap with the report's recommendation that
the next wave fetch before enumeration.

## Motion M2: CONFIRM the interactive-TNN survey

ADVOCATE: The survey scanned the merge range 45d449a56..fe1b5e2c0 (19
commits) and the tip tree, and found zero new chat/REPL entry points. The
evidence is layered: added-file name scan with word-boundary chat or
repl, zero matches; content scan of the range diff, whose only hits are
prior-wave survey prose inside LOOP_STATE.md and debate transcripts;
git diff stat on src and units, empty, so no file under src/ or units/
was touched at all; source-tree grep on the tip with false-positive
substrings (replay, replication, replace, replica, replicate) excluded,
zero matches. The one new file that could confuse, docs/lab/dialogue/
round4/dialogue.zag introduced in 75267f9df, was examined and excluded:
it is a batch prose-learning trial taking argv file paths, with no
stdin prompt, no read loop, and no interactive REPL path. All three
frozen pins PASS byte-identical: baseline probe
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
decline-gate probe
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
pinned znc
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
with the frozen source shas also matching the fit_authority README
record. The known record defect, that
docs/lab/rsi/fit_authority/SHA256SUMS does not exist, is carried as a
record caveat, not an evidence failure. I move CONFIRM with tag
[RE-CERT].

SKEPTIC: I press four points. First, tnn_chat exists: the survey itself
verifies two frozen built binaries. Claiming "no interactive TNN
exists" while holding two runnable chat artifacts is an overclaim unless
the boundary is exact. Second, the record defect matters: the pins live
in fit_authority/README.md because the expected SHA256SUMS file does not
exist. A stale or edited README would pass the pins against itself; the
survey has no independent anchor. Third, the grep strategy is
spelling-bound: word-boundary chat or repl misses an entry point called
console, shell, prompt, or tty. Absence of a spelling is not absence of
a capability. Fourth, the range is only 19 commits deep. Anything
interactive predating 45d449a56 is outside the scan, so the tip-level
claim rests on the grep, which I have already attacked.

JUDGE: The boundary is exact and it is stated in the evidence. Per the
fit_authority README Scope section, quoted in the survey: "These
instruments certify the 38-fact closed-book probe chain only. No runnable
interactive TNN exists on this branch beyond these frozen probe
instruments." tnn_chat is supervised red-team probe-chat material only,
and the brief states explicitly that it must not be presented as an
interactive TNN available for adoption. The survey does not deny the
binaries exist; it classifies them, and the classification is sourced to
the fit authority record. On the record defect: the pins verified are
the frozen built-binary shas, and the survey cross-checked the frozen
source shas against the same README record; the defect is carried as a
caveat, not hidden, and the three binary comparisons are
byte-identical computations, not self-referential claims. On
spelling-bound greps: the survey did not rely on one grep. It combined
the added-file name scan, the range-diff content scan, the src and units
diff stat (empty: no file under src/ or units/ touched in the entire
range), and the tip source-tree grep with false-positive exclusion. No
concrete missed candidate was offered; the skeptic's hypothetical
spellings are not evidence. On range depth: the range is the delta since
the last wave by design; prior waves covered prior ranges, and the tip
tree itself was grepped. Provenance: the three pins are inherited, the
survey execution and its 19-commit scan are new. Ruling: M2 is
CONFIRMED. Tag: [RE-CERT].

## Motion M3: CONFIRM the no-new-candidates stand-down

ADVOCATE: Five signals over 17:21 to 20:21 PDT are all clean. Zero new
prereg drafts: exactly one commit touched docs/lab/rsi in the window,
ba0487c2384bcf0b9b7ab930633b5336947d2145, the prior 1721pdt wave
evidence batch, with zero prereg or design filename hits. Zero design
ideas: the markdown added in the window is all prior-wave process
evidence (advocate brief, skeptic report, judge rulings, fork results,
interactive survey, lane survey). Zero re-aimed preregs: per-file scan
of every prereg under docs/lab/rsi/runs with git log over the window
returned zero modifications, and no prereg filename was modified
anywhere in the repo; no D-VID re-aim exists. Zero loop-authored
mechanism commits: the merge range 45d449a56..fe1b5e2c0 holds 19
commits, 16 authored by micahcooley (his frontier work, CLOSED) and 3
authored by tnn-rsi-loop (the merge itself, the prior wave evidence
batch, the prior wave LOOP_STATE verdicts). Thirty-seven untracked
entries were each classified: old binary, frame, and bin residue from
older waves; his-frontier fixture material under docs/lab/senses/
rebuild; an empty err.txt; the untouched .wave_lock. Zero drafts, zero
preregs, zero design notes. All six lanes keep their prior standing
(G1 stood down, D-VID-1 stood down, CV-P barred pending his governance
ruling 6, COMP-2 with ruling 6 open and P11 unresolved, B1-class with P9
not found, ST-1 dead on pristine evidence). His six governance rulings
remain open and untouched. I move CONFIRM with tag [RE-CERT].

SKEPTIC: Absence evidence is only as good as the scans, so I probe the
scans. First, the 37 untracked entries are classified by name and
location; a draft could hide among binary residue or fixture material,
and the survey's classification is asserted, not shown content by
content. Second, the loop-authored merge fe1b5e2c0 is itself a loop
commit, and the fork battery treats merged upstream contents as CLOSED,
content not reviewed, toolchain stability only. If unreviewed content
rode in inside the merge, the stand-down's claim of zero new mechanism
rests partly on a scope stamp, not on review. Third, the window's
prereg|design filename hits include his own frontier prereg
(docs/lab/dialogue/trace-trial/trial/PREREG.md) and eight deleted
preregs from his de-synth cleanup. The survey calls them CLOSED because
they are owner-authored, but the loop's standing mandate is to hunt his
frontier; calling his newest prereg CLOSED without engagement looks
like standing down where the action is. Is the stand-down honest, or is
it the loop looking away?

JUDGE: Each point is answered by standing rules and cited counts. First,
the 37 untracked entries: the survey lists their classification entry
class by entry class (older-wave residue dirs, his-frontier fixture
material, the lock file, the empty err.txt) and reports zero entries
resembling a draft, prereg, or design note. The skeptic offered no
candidate entry; a bare possibility is not evidence. Second, the merge:
the merge range's loop-authored commits are the merge itself, the prior
wave evidence batch, and the prior wave LOOP_STATE verdicts, all
process, all disclosed. The merged upstream contents are CLOSED by the
battery's scope stamp (toolchain stability only), and the stand-down
motion judges loop-authored mechanism candidates, of which there are
zero. The merged content is his frontier work, which the loop never
claims and never re-certifies; that is the standing rule, not evasion.
Third, his frontier prereg and the deleted preregs: owner-authored work
is CLOSED by standing rule, and the alignment synthesis is explicit that
the loop stands down where he has already won. The trace-trial PREREG is
his experiment, and the eight deletions are his de-synth cleanup in
4f782c40d. The stand-down is a re-certification of a standing posture
over this window's five signals, all clean, not a judgment on his
research. Provenance: the stand-down posture is inherited; the five
clean signals this window are new. Ruling: M3 is CONFIRMED. Tag:
[RE-CERT].

## Motion M4: prereg commit-order self-check labeled VACUOUS per P17

ADVOCATE: The self-check is vacuous this wave. The merge range
45d449a56..fe1b5e2c0 contains 16 owner commits (CLOSED) and 3 loop
process commits (the merge, the evidence batch, the LOOP_STATE
verdicts). Zero loop candidate commits exist, so there is no prereg and
implementation pair whose commit order could be checked. Per standing
precedent P17, the check is labeled VACUOUS and recorded as null, not
a pass. I move acceptance of the vacuous label.

SKEPTIC: A vacuous label is convenient. If the loop ever wanted to dodge
the commit-order rule, declaring vacuous would be the way. I want
proof, not assertion, that no candidate commits exist. The loop did
author the merge fe1b5e2c0; could a mechanism have ridden in inside the
merge and escaped the candidate definition?

JUDGE: The proof is the cited commit inventory, corroborated by two
independent workers. The lane survey inventories the 19-commit range:
16 micahcooley commits, 3 tnn-rsi-loop process commits. The fork
battery independently records the same run-start HEAD and the same
merge parentage (a4d4ff7cd pre-merge state, 75267f9df merged upstream
tip). The loop-authored commits are the merge, the evidence batch, and
the LOOP_STATE verdicts: process artifacts, none a mechanism candidate.
The merged upstream contents are his frontier work, CLOSED, not loop
candidates. With no prereg/impl pair in existence, there is no ordering
to check, and P17 applies exactly: labeled vacuous, recorded as null,
not a pass. The skeptic's evasion scenario is answered by the
inventory: nothing to order, nothing dodged. Ruling: the VACUOUS label
is CONFIRMED per P17. Tag: [VACUOUS] as proposed. Note on taxonomy: the
[NEW]/[RE-CERT]/[STACK]/[VOID] tags apply to artifacts under judgment;
M4 judges no artifact, so the P17 vacuous label is the complete ruling.

---

## Precedents minted this session

- P20: When live remote tips are untestable under the no-fetch frozen procedure, the battery may still be CONFIRMed only under an explicit scope stamp limiting certification to the tested entries, with the untested tips recorded as a coverage gap rather than as failures.
- P21: A mid-run driver bug that is caught before any citation, with every bogus evidence dir deleted and the batch rerun cleanly against the corrected run log, does not void the battery verdict.

## Final rulings

| Motion | Ruling | Tag |
|---|---|---|
| M1 fork battery | CONFIRM | [RE-CERT], scope stamp: toolchain and extraction stability only, on tested entries; coverage gap carried for rh-tnn-native-lab-tip-start (d9ddc556) and rh-main (27a4271f) |
| M2 interactive-TNN survey | CONFIRM | [RE-CERT] |
| M3 no-new-candidates stand-down | CONFIRM | [RE-CERT] |
| M4 prereg commit-order self-check | VACUOUS label confirmed per P17 | [VACUOUS] |

Provenance summary for the record: no motion adopts or certifies a new
loop-authored mechanism candidate this wave. Everything confirmed is
inherited and re-certified ([RE-CERT]) or a null process record
([VACUOUS]). The two untestable live remote tips are the single open
coverage item, carried with a next-wave fetch recommendation. No debate
narrowed any red line. Nothing is committed by this transcript; the
coordinator commits.
