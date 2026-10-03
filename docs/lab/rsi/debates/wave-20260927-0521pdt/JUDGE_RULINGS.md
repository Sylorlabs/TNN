# JUDGE RULINGS: wave-20260927-0521pdt

Role: JUDGE, mandatory debate group. Evidence read in order:
FORK_RESULTS_0521.md, LANE_SURVEY_0521.md, INTERACTIVE_0521.md,
ADVOCATE_BRIEF.md, SKEPTIC_REPORT.md. Zero Python. Commit nothing.

The coordinator's motion list is ruled below, attack by attack, on
cited evidence only. Rulings rendered: UPHELD (verdict changes as
proposed), REJECTED (attack fails on cited evidence), MODIFIED
(partial; the exact final wording is stated).

## The skeptic's provenance probe

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer. The artifacts under judgment are the three worker products
(first-produced this wave under
docs/lab/rsi/runs/wave-20260927-0521pdt/) plus standing items. Genuinely
NEW this wave: the fork battery re-executions with uniform per-entry
evidence (47/47 znc pin matches, 47/47 B1/B2/B3, 47/47 negative
controls), the five-signal window scan of the 02:21 to 05:21 PDT
interval (23 commits classified), the pin plus entry-point checks on
the 463b115b6..ecbe9b5b7 merge range, the enumeration manifest
artifact (exists in the run dir, uncommitted), and the clean-merge
verification of the run-start merge. INHERITED: the FIT behavioral
battery by citation across 11 waves (last executed at
wave-20260925-1421pdt, evidence 9692f5d1d); the extraction-FAIL cause
attribution (sound by content addressing, same commits as eight waves
running, not re-inspected); the prior LOOP_STATE verdicts and the
prereg commit-order results the survey re-presents; DP-1 readiness by
citation (09-26 dossier); the six open governance rulings and the
sealed-pair states (untouched, standing). Verdict lines below label
each class explicitly.

## Attack 1: fork battery verdict line. Ruling: UPHELD

The battery is sound. The 49 to 48 delta is real new coverage
(arch-20260927-0221pdt at 463b115b6 postdates the 0221pdt run-start
HEAD), the rename arch-20260926-2321pdt to
arch-wave-20260926-2321pdt is count-neutral on the identical commit
004616f65, and the 2 extraction FAILs are the same commits with the
same cause eight waves running. The skeptic's labeling point stands:
49 named entries cover 39 unique commits, and the report's own text
says "experiment workers are implementing in them concurrently" while
also treating those entries as already merged. The battery certifies
run-start pinned commits, not branch tips. Final verdict line:

CONFIRM fork battery [RE-CERT]: 39 unique commits across 49 named
entries; 47 PASS, 2 extraction FAIL (expected, non-TNN research-doc
trees, unchanged cause eight waves running), 0 CONFIRM. Scope:
toolchain and extraction stability only on the tested pinned commits,
not the contents of the merged commits.

## Attack 2: stand-down label. Ruling: UPHELD

The survey's negative finding is fresh (23-commit window scan, 4
prereg filename hits all attributed to closed 0221pdt workstreams,
0 re-aimed preregs, 0 new design documents, 0 lane-directory touches,
37 untracked entries with 0 drafts). But CONFIRM [RE-CERT] borrows
certification authority for an absence, and the wave produced zero
design output toward any queued blocker. The label narrows to
STAND-DOWN on a fresh scan, and the verdict line carries the
untouched queued-blocker list explicitly. Final verdict line:

STAND-DOWN on fresh scan: no new mechanism this wave. 23 commits in
the 02:21 to 05:21 PDT window: 9 Micah-frontier (CLOSED) plus 14 loop,
of which 13 are the closed 0221pdt workstreams (EXP1b invention
claim DEAD, LIGHT-FIELD KILLED clean, EXP2 narrowed with wire-in off
the table) and 1 is the wave record with LOOP_STATE verdicts. 0 new
prereg drafts, 0 re-aimed preregs, 0 new design documents, 0
lane-directory touches, 37 untracked residue entries with no drafts.
Untouched queued blockers: EXP1c compositional-choice design, EXP2
grounding in real deliberation failures plus rescuer-lens K4
hardening, enumeration manifest committed, B1-class P9 bar
reformulation, COMP-2 ruling 6 plus P11 stemmer-contingency. Six lanes
hold prior standing; six governance rulings stay open.

## Attack 3: interactive TNN verdict. Ruling: UPHELD

Fresh this wave: pin verifications all MATCH and the 10-commit
entry-point scan (1390 added files, zero keyword hits; the two close
cases dismissed on stdin-read inspection). Stale this wave: the
behavioral FIT battery (KB1 30/30, KB2 17/17, KB5 10/10), last
executed at wave-20260925-1421pdt (evidence 9692f5d1d), carried by
citation across 11 consecutive waves. Pin integrity is not behavioral
integrity, and 11 waves with no re-run cadence is inheritance, not
re-certification. The verdict splits. Final verdict line:

CONFIRM interactive TNN pins and entry-point scan (fresh): no new
chat/REPL/interactive entry points in merge range
463b115b6..ecbe9b5b7; frozen pins all match. FIT behavioral battery
(KB1 30/30, KB2 17/17, KB5 10/10) CARRIED BY CITATION [RE-CERT by
citation]: last executed wave-20260925-1421pdt (evidence 9692f5d1d),
11 waves stale. Standing rule: re-run mandated at least every 8
waves. Record defect: docs/lab/rsi/fit_authority/SHA256SUMS does not
exist; pins live in fit_authority/README.md; repair is assigned.

## Attack 4: prereg commit-order self-check. Ruling: UPHELD

The label VACUOUS is correct for this wave: no loop candidate
commits, nothing to gate. The skeptic verified the survey's
re-presented orderings (7e0326d2c 09:34:19 before 938d188cb 09:49:21;
06e28f088 09:38:41 before 32eadf722 09:43:14; 4a937d994 09:41:06
before aa76f9b8d 09:45:21). But commit order is not run order: commit
d758a876c3 is dated 2026-09-27 07:50 PDT, about 5.5 hours in the
future relative to the 02:21 to 05:21 PDT window, so timestamps in
this repo are not trustworthy; and the LIGHT-FIELD amendment
c6b8190f3 sits one second before its implementation commit aa76f9b8d,
so the survey's "independently confirmed pre-run, no scores seen" is
asserted, not evidenced. Final verdict line:

VACUOUS prereg commit-order self-check: no loop candidate commits
this wave, nothing to gate. Standing caveat: the check evidences
commit order only, never run order; sub-minute margins on this
repo's clocks are weak evidence; "pre-run, no scores seen" must be
asserted, not reported as a finding.

## Attack 5: governance rulings and sealed pairs UNTOUCHED [VOID]. Ruling: REJECTED

The skeptic independently verified this item: no wave-worker commits
exist, the two in-window merges' resolutions touched only
.origin-wave.* files, no ruling-named files, and the survey names the
six rulings without relitigating them. Nothing in this wave warrants
a label change. Final verdict line stands unchanged:

UNTOUCHED [VOID]: the six governance rulings (S7 strike, MD-SSD-1,
S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) remain OPEN;
the sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13,
S14, whirlpool-planform) were not touched. This wave neither decided,
relitigated, nor re-presented any of them.

## Attack 6: DP-1 queue-HELD. Ruling: UPHELD

The queue-HELD posture is correct; moving the pair is a parent-agent
queue decision. But "ready" is inherited from the 09-26 dossier
(DP1_DOSSIER_1121.md, queue-HELD since the 1121pdt/1421pdt rulings),
not freshly verified this wave, so the citation travels with the
verdict instead of being re-asserted bare. Final verdict line:

Queue-HELD: DP-1 repaired sealed blind pair ready per the 09-26
dossier (DP1_DOSSIER_1121.md, queue-HELD since the 1121pdt/1421pdt
rulings), not freshly verified this wave. Presentation to his ears is
the parent agent's queue decision, not this wave's.

## Attack 7: enumeration manifest status. Ruling: UPHELD

Three answers were in play: the fork worker treats the artifact as
done (ENUMERATION_MANIFEST.md exists in the run dir and lists every
named entry), the survey lists the blocker NOT cleared ("no manifest
committed in this window"), the debate premise treats it as done.
Only one written answer survives: the queued process item was a
committed frozen manifest, and the entire wave dir is uncommitted
(verified: git status shows ?? docs/lab/rsi/runs/wave-20260927-0521pdt/).
Final verdict line:

OPEN until committed: the enumeration manifest artifact exists in
docs/lab/rsi/runs/wave-20260927-0521pdt/forks/ENUMERATION_MANIFEST.md
but is uncommitted, so the queued process item is NOT cleared. It
will be committed with this wave's record. The fork worker's verdict
1 records the artifact's content; this item records the item's status.

## Final verdict slate (verbatim, for the LOOP_STATE update)

1. CONFIRM fork battery [RE-CERT]: 39 unique commits across 49 named
entries; 47 PASS, 2 extraction FAIL (expected, non-TNN research-doc
trees, unchanged cause eight waves running), 0 CONFIRM. Scope:
toolchain and extraction stability only on the tested pinned commits,
not the contents of the merged commits.
2. STAND-DOWN on fresh scan: no new mechanism this wave. 23 commits
in the 02:21 to 05:21 PDT window: 9 Micah-frontier (CLOSED) plus 14
loop, of which 13 are the closed 0221pdt workstreams (EXP1b invention
claim DEAD, LIGHT-FIELD KILLED clean, EXP2 narrowed with wire-in off
the table) and 1 is the wave record with LOOP_STATE verdicts. 0 new
prereg drafts, 0 re-aimed preregs, 0 new design documents, 0
lane-directory touches, 37 untracked residue entries with no drafts.
Untouched queued blockers: EXP1c compositional-choice design, EXP2
grounding in real deliberation failures plus rescuer-lens K4
hardening, enumeration manifest committed, B1-class P9 bar
reformulation, COMP-2 ruling 6 plus P11 stemmer-contingency. Six lanes
hold prior standing; six governance rulings stay open.
3. CONFIRM interactive TNN pins and entry-point scan (fresh): no new
chat/REPL/interactive entry points in merge range
463b115b6..ecbe9b5b7; frozen pins all match. FIT behavioral battery
(KB1 30/30, KB2 17/17, KB5 10/10) CARRIED BY CITATION [RE-CERT by
citation]: last executed wave-20260925-1421pdt (evidence 9692f5d1d),
11 waves stale. Standing rule: re-run mandated at least every 8
waves. Record defect: docs/lab/rsi/fit_authority/SHA256SUMS does not
exist; pins live in fit_authority/README.md; repair is assigned.
4. VACUOUS prereg commit-order self-check: no loop candidate commits
this wave, nothing to gate. Standing caveat: the check evidences
commit order only, never run order; sub-minute margins on this
repo's clocks are weak evidence; "pre-run, no scores seen" must be
asserted, not reported as a finding.
5. UNTOUCHED [VOID]: the six governance rulings (S7 strike, MD-SSD-1,
S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) remain OPEN;
the sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13,
S14, whirlpool-planform) were not touched. This wave neither decided,
relitigated, nor re-presented any of them.
6. Queue-HELD: DP-1 repaired sealed blind pair ready per the 09-26
dossier (DP1_DOSSIER_1121.md, queue-HELD since the 1121pdt/1421pdt
rulings), not freshly verified this wave. Presentation to his ears is
the parent agent's queue decision, not this wave's.
7. OPEN until committed: the enumeration manifest artifact exists in
docs/lab/rsi/runs/wave-20260927-0521pdt/forks/ENUMERATION_MANIFEST.md
but is uncommitted, so the queued process item is NOT cleared. It
will be committed with this wave's record. The fork worker's verdict
1 records the artifact's content; this item records the item's status.

## Standing process additions from this debate

- The interactive procedure gains a stdin-read backstop grep over new
.zag sources (skeptic attack 3; this wave's answer was verified clean).
- The lane survey window must cover the run-start merge, or the fork
battery's scope stamp must include merge-resolution review when the
run-start merge is conflicted (skeptic attack 6; this wave's 05:22 PDT
merge verified clean independently, empty combined diff).
- Surveys must explicitly account for merged upstream ranges each wave:
count, author split, and which wave's survey covered their content;
"CLOSED, not re-litigated" needs a cited prior review (skeptic attack
7; the 52 commits of af657c8e5 stand on the prior window's coverage).
- The tnn_chat FIT battery must be re-run at least every 8 waves, and
the fit_authority/SHA256SUMS record defect must be repaired.
