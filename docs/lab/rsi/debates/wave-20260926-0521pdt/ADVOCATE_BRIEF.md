# Advocate brief: wave-20260926-0521pdt

Debate group for the TNN RSI loop. The advocate argues FOR each adoption
on the coordinator's draft slate. Numbers are cited from the evidence
files read this session. No em-dashes are used in this file.

## Item 1. Fork battery 0521pdt: CONFIRM [RE-CERT]

The advocate's case rests on fresh enumeration, byte-level uniformity,
and honest failure classification.

Fresh enumeration this wave: `git branch -a` (15 local branches, one
remote-tracking ref), read-only `git ls-remote origin` (6 heads, 3 pull
heads), and `git worktree list` (10 detached worktrees). No stale lists.

Numbers: 35 named entries, 33 PASS, 2 FAIL. 27 unique commits, 2 unique
live commits (d0076134d and 6c3c7b69c), 3 live named entries, 32
fixtures. All duplicates named explicitly with SHAs in the results file:
origin-tnn-native-lab-rt duplicates rh-tnn-native-lab at
6c3c7b69ce81915c3fd73159102357e47dc31278; pull-3-head duplicates
rh-reorg-phase-0-1 and forktest-reorg_phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df; and three further duplicate
groups (wave-debate-session-1-backup, wg-freeze, bd30978748fa) each named.

Live entries are exactly the commits that moved since 0221pdt:
local-tnn-native-lab (aaabb0b89 to d0076134d), origin-tnn-native-lab-rt
and rh-tnn-native-lab (both to 6c3c7b69c). Both live commits were tested
directly at their own tips. Local HEAD d0076134d was static during the
run; closing read-only ls-remote returned 6c3c7b69c, identical to run
start. No untested origin tip exists for next-wave pickup.

Uniformity on 33/33 passing entries, grepped not sampled: extracted znc
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(byte-identical toolchain on every fork); probe source sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919;
B2 bin sha 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
matches the frozen 2321pdt value; NEG1/NEG2 discriminate as required on
all 33; harness rebuilt from extracted source sha f38d9154... with the
pinned znc, built binary a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to prior waves; harness VERDICT=PASS exit 0 on all 33.
Zero Python attested by the worker: shell, git read-only, sha256sum,
pinned znc, pure-Zag harness only. The driver was written directly as a
shell script and never edited after first use.

The 2 FAILs (pull/1/head 5802fec8, pull/2/head 4b76bb59f) are extraction
failures at the first step: the pinned znc path and probe path do not
exist in those trees, which hold non-TNN research documents and no src/
directory. This is a property of those forks' contents, identical to the
0221pdt wave, not a toolchain regression. They are honestly classified
and remain uncovered until their trees gain the pinned toolchain path.

Ancestry for the transit claims was verified this wave with
git merge-base --is-ancestor: 1c3f9571, aaabb0b89, 58dd10ae8, bf69a6f38,
and cc3b63d1a are all ancestors of the directly tested tips, so they
are transitively covered for current-tip purposes and not directly
tested at their own tips (P3 wording). Genuinely divergent entries (the
archive branches, remote heads, and the non-ancestor worktrees) were
tested directly at their own tips. Precedent P8 applies: the CONFIRM
survives named duplicates and a superseded tip when both are disclosed,
which they are.

The scope stamp is mandatory and travels: this battery certifies
toolchain and extraction stability only, not the contents of merged
commits.

## Item 2. FIT carry-over: CONFIRM [RE-CERT] without a fresh re-run

The advocate's case is cryptographic, and the qualification is disclosed,
not hidden.

Precondition (1): 10/10 chain inputs byte-exact to frozen shas on the
working tree at d0076134d, measured with sha256sum. Precondition (2):
the D1 hazard stays closed; docs/lab/rsi/fit_authority/ is a normal
tracked directory holding all four frozen sources byte-exact; the
README.md uncommitted modification is documentation only, not a chain
input.

Precondition (3): the worker enumerated all three merges in range
9526cdb5c..d0076134d (cc3b63d1a, aaabb0b89, d0076134d) and diffed all
six parent-to-merge pairs restricted to the chain paths. The result:
zero modifications, zero deletions, zero content changes to any frozen
chain input. Every delta is one of: additions of sha-verified
byte-exact frozen content (the b650ea46f and bf69a6f38 D1 freeze commits
surfacing through local parents, which the 1421pdt record itself
recommended as the D1 closure); a mode-only change on the pinned znc
(100644 to 100755 in the origin-parent diffs, blob sha identical in all
eight commits examined); and run-evidence scratch additions under
fitchat0521 with fixtures byte-exact to frozen shas. docs/lab/dialogue/
shows zero diff across the whole range. The debate group independently
re-verified the six diffs and the mode-only blob identity this session.

The literal empty-diff reading fails only because the recommended D1
freeze landed inside the carry-over range. Treating that as a failure
would punish the loop for doing exactly what the prior record required.
The rule's purpose is that no frozen chain input was modified or deleted
by intervening merges; that purpose is met and cryptographically shown.

Precondition (4): determinism cited explicitly in place of a re-run:
2/2 binary reproducibility (decline 20273a99..., baseline 1ada2fae...),
9/9 rerun pairs byte-identical (r1/r2, r2/r3, r1/r3 across KB1, KB2,
KB5), KB1 30/30 specific declines with 0 blanket refusals, KB2 17/17,
KB5 10/10, output hashes byte-identical to prior wave records. Same
inputs, same toolchain, deterministic build: a fresh re-run would
reproduce identical bytes and add nothing. The carry-over rule exists
precisely to avoid redundant re-runs when the cryptographic case holds.

The scope sentence travels verbatim: "This is not a candidate verdict
and it is not merge review of the merged-in work; it certifies the
38-fact closed-book probe chain only." Zero Python anywhere in the FIT
work.

## Item 3. Interactive TNN: CONFIRM, EXISTS for supervised red-team probe chats only

The finding is unchanged and honestly negative where it is negative.

No source-level chat/REPL/interactive-loop entry point exists in
src/zag/ or units/ on this tip: the only grep hit for
repl/interactive/chat was a "repl" substring false positive inside
"replication"/"replay" in a brief doc, and a follow-up grep for
entry-point signatures (fn main, stdin, readline, read_line,
interactive_loop, repl_loop) returned zero files. No merged upstream
work since the prior waves added an interactive entry point.

What EXISTS is all inherited and sha-verified: the frozen baseline
probe binary (1ada2fae..., ELF x86-64, runnable), the frozen
decline-gate binary (20273a99..., ELF x86-64, runnable), the CVP retest
binaries, the pinned znc (498abcb5...), and the frozen instrument
sources matching the authority manifest shas. No probe chat was run
this wave; availability only was verified (file plus sha256sum).

The known confabulation caveat travels: tnn_chat answers closed-book
from the 38-fact kb.txt and emits unflagged confabulations on out-of-KB
questions. FIT FOR SUPERVISED red-team probe chats only.

## Item 4. Backfill of wave-20260926-0221pdt: INCOMPLETE, breach recorded, superseded

The advocate supports the coordinator's proposed handling as the honest
one.

Facts: the 0221pdt wave ran the fork battery only (35 entries, 33 PASS,
same 2 extraction FAILs on pull/1 and pull/2). Its worker disclosed one
python3 heredoc used to patch the wave's driver text; no Python touched
the battery, harness, analysis, or verification steps. The wave had no
debate, no LOOP_STATE.md update, and its results file was left
untracked; this wave commits it.

The pure-Zag rule is absolute: no Python anywhere, including wave
artifacts. A python3 heredoc that patches the wave's driver text
touches a wave artifact, so the coordinator's classification as a
red-line breach disclosure against that wave's driver evidence is
correct. The remedy is proportionate and already executed: this wave's
fresh zero-Python battery re-ran everything and supersedes the 0221pdt
results, and no lineage claim travels from the superseded battery.

Reporting the wave's self-reported numbers with the breach attached
preserves the audit trail without granting evidentiary weight. The
alternative, pretending the wave never ran, would be worse: the merge
aaabb0b89 and the origin-tip move to 1c3f9571 happened, and the record
must show how they were handled. The backfill section is marked
INCOMPLETE because the wave is incomplete: fork battery only, no
debate, no state update.

## Item 5. Documentation: maintenance, not a verdict

The fit_authority README's stale residual note is fixed (the chain now
correctly states no residuals remain) and the AUTHORITY_MANIFEST.md
commit attribution is corrected to bf69a6f38 for the kb.txt/gaz.txt
addition. The shas were correct either way, so this is a
record-keeping nit. The four frozen chain inputs are untouched. The
advocate supports recording this as documentation maintenance, not a
verdict; no verdict tag applies.

Micah's six pending governance rulings and his sealed blind A/B
verdicts are his to make. This brief touches none of them.
