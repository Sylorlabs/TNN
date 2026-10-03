# Advocate brief: wave-20260926-0821pdt

Debate group for the TNN RSI loop. The advocate argues FOR each item on
the coordinator's draft slate. Numbers are cited from the evidence
files read this session (FORK_RESULTS_0821.md, FIT_0821.md,
INTERACTIVE_0821.md). No em-dashes are used in this file. Zero Python
was used by this debate group; all verification was read-only git,
sha256sum, grep, and shell coreutils.

## Item 1. Fork battery 0821pdt: CONFIRM [RE-CERT]

The advocate's case rests on fresh enumeration, byte-level uniformity,
honest failure classification, and disclosed incident handling.

Fresh enumeration this wave: `git branch -a` at run start (16 local
branches, one remote-tracking ref origin/tnn-native-lab), read-only
`git ls-remote origin` (6 refs/heads plus 3 refs/pull/*/head refs), and
`git worktree list` (10 detached worktrees). No stale lists carried
forward.

Numbers: 36 named entries, 34 PASS, 2 FAIL. 27 unique commits, 1 unique
live commit (4328a8350d987a65c4e86e4973dbe45c9d5f6cd5), 2 live named
entries, 34 fixtures. All duplicates named explicitly with SHAs in the
results file, six duplicate groups: local-tnn-native-lab duplicates
arch-wave-0926-0521 at 4328a8350d; origin-tnn-native-lab-rt duplicates
rh-tnn-native-lab at 6c3c7b69ce81915c3fd73159102357e47dc31278;
rh-pull-3-head duplicates rh-reorg-phase-0-1 and wt-forktest-reorg at
9914322267e1358e5542a23c72ec51d1a9ae43df; wave-debate-session-1-backup
duplicates wt-forktest-debate-backup at 3947dca1a77c00818575dbc7476556c8278b8b7b;
rh-wg-freeze duplicates wt-forktest-wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848; wt-forktest-tnn-native-lab,
wt-wave3-probe, wt-wave3-senses, and wt-wave3-trades each test
bd30978748fa83bbea6e423a7074cf32b7304291.

Live entries are exactly what moved or appeared since 0521pdt:
local-tnn-native-lab (d0076134d to 4328a8350d) and the new archive
branch tnn-native-lab-wave-archive-wave-20260926-0521pdt (newly
enumerated this wave, at 4328a8350d). Both test the same single live
commit at its own tip, and the results file says so. Local HEAD
4328a8350d was static during the run. Closing read-only ls-remote of
origin tnn-native-lab returned 6c3c7b69c, identical to run start. No
untested origin tip exists for next-wave pickup.

Uniformity on 34/34 passing entries, grepped not sampled: extracted znc
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(byte-identical toolchain on every fork); probe source sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919;
B1 compile exit 0, run exit 0, stdout byte-identical to FORKBATTERY-OK
42; B2 rerun stdout identical, recompile byte-identical, bin sha
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
matches the frozen value; B3 `znc check --strict --no-zagd` exit 0;
NEG1 fails as required (compile exit 1, check exit 1, E0002
unterminated string literal); NEG2 fails as required (stdout differs at
char 1, line 1); PROBE compiles with the fork's own znc exit 0. The
pure-Zag harness was extracted read-only from the 2321pdt archive
(source sha f38d9154..., matching expected) and rebuilt with the pinned
znc to binary a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to prior waves; harness VERDICT=PASS exit 0 on 34/34.

The 2 FAILs (pull/1/head 5802fec8, pull/2/head 4b76bb59f) are
extraction failures at the first step: the pinned znc path and the
probe path do not exist in those trees, which hold non-TNN research
documents and no src/ directory. The debate group independently
verified this with read-only git ls-tree this session: the toolchain
path is absent in both commits, and pull/1/head's tree root holds
research docs (R33_FINAL_CLOSEOUT.json, README.md, .github, .gitignore,
LICENSE). Same cause as 0521pdt, not a toolchain regression. They are
honestly classified and remain uncovered until their trees gain the
pinned toolchain path.

The two incidents were disclosed by the worker and handled correctly.
The /tmp 100% incident: the two affected entries (wt-wave3-trades,
wt-wave3-senses) were not judged on compromised artifacts. After /tmp
was freed, both were re-run from scratch via read-only git show and
both completed cleanly with full PASS and matched pin/probe shas. The
final 34 verdicts rest on intact post-rerun artifacts. The accidental
python3 -c "print('skip')": it ran after the results file was written,
printed one word to stdout, and touched no wave data, files, analysis,
or tooling. Under P13 and the COMP-2 distinction it is a disclosed
contact, not a breach: it read and wrote no file and contacted no
wave artifact. The battery itself was pure shell, git, sha256sum, the
pinned znc, and the pure-Zag harness.

The scope stamp is mandatory and travels: this battery certifies
toolchain and extraction stability only, not the contents of merged
commits.

## Item 2. tnn_chat FIT: CONFIRM [RE-CERT] on 4328a8350 without a fresh re-run (per P12)

The advocate's case is cryptographic, and this wave's range is cleaner
than the one P12 was written for.

Precondition (1): 10/10 chain inputs byte-exact to frozen shas on the
working tree at HEAD 4328a8350d, measured with sha256sum
(tnn_chat.zag c0776ad6, tnn_chat_decline.zag a87011fe, kb.txt 3ef27296,
gaz.txt b75fd113, the two R33 sources, pinned znc 498abcb5, three probe
fixtures). All PASS.

Precondition (2): the D1 durable authority path holds.
docs/lab/rsi/fit_authority/ is a normal tracked directory holding all
six entries; git status clean on all chain paths. The README.md
working-tree modification noted by the 0521pdt record was committed in
8564128c4.

Precondition (3): the carry-over range d0076134d..4328a8350 contains
exactly two commits. The debate group independently re-verified the
chain-path diffs this session with read-only git diff: 8564128c4
touches exactly two files, both documentation only
(AUTHORITY_MANIFEST.md one-line attribution correction, README.md
residual closure; sha rows untouched); 4328a8350 shows zero diff on
any chain path. Zero modifications, zero deletions, zero content
changes to any frozen chain input. No mode-only changes in this range.
This satisfies P12 without needing the 0521pdt qualification at all: no
freeze landed in range, no metadata-only znc change, nothing but
doc-only fixes and an empty diff.

Precondition (4): determinism cited explicitly in place of a re-run,
per P12: 2/2 binary reproducibility (decline rebuild byte-identical to
frozen 20273a99..., baseline to frozen 1ada2fae...), 9/9 rerun pairs
byte-identical (r1/r2, r2/r3, r1/r3 for each of KB1, KB2, KB5), KB1
30/30 specific declines with 0 blanket refusals, KB2 17/17 answered
with 0 declines and byte-identical baseline parity, KB5 10/10 answered
with 0 declines and byte-identical baseline parity, output hashes
byte-identical to prior wave records, all 15 runs exit 0 with empty
stderr. Same inputs (byte-exact, verified), same pinned toolchain,
recorded deterministic history: a fresh re-run would reproduce
identical bytes and add no information. The carry-over rule exists
precisely to avoid redundant re-runs when the cryptographic case
holds.

The literal-scope sentences travel verbatim: not a candidate verdict,
not merge review; certifies the 38-fact closed-book probe chain only.
Zero Python anywhere in the FIT work (no python3 invocation of any
kind, attested in the evidence file).

## Item 3. Interactive TNN: CONFIRM [RE-CERT], EXISTS for supervised red-team probe chats only

The finding is unchanged and honestly negative where it is negative.

No source-level chat/REPL/interactive-loop entry point exists in
src/zag/ or units/ on this tip: grep for repl/interactive/chat
returned exactly one file, a verified false positive (the substring
"repl" inside "replication"/"replay" in a brief doc); a follow-up grep
for entry-point signatures (fn main, stdin, readline, read_line,
interactive_loop, repl_loop) returned zero files; the d0076134d..HEAD
delta adds no new chat/repl-named file in src/ or units/. No merged
upstream work since the 0521pdt wave added an interactive entry point.

What EXISTS is all inherited and sha-verified: the frozen baseline
probe binary (1ada2fae..., ELF 64-bit LSB x86-64, runnable), the frozen
decline-gate probe binary (20273a99..., ELF 64-bit LSB x86-64,
runnable), the CVP retest binaries, the pinned znc (498abcb5...), and
the frozen instrument sources matching the authority manifest shas. No
probe chat was run this wave; availability only was verified by file
plus sha256sum, and the verdict says exactly that.

The known confabulation caveat travels: tnn_chat answers closed-book
from the 38-fact kb.txt and emits unflagged confabulations on out-of-KB
questions. FIT FOR SUPERVISED red-team probe chats only (knowledge vs
architecture diagnosis). Not a general assistant, not a candidate for
adoption.

## Item 4. No new candidates this wave: CONFIRM the coordinator's stand-down

The advocate's case: standing down is the disciplined move, not an
empty wave, and the gates are named.

Every candidate lane is stood down or gated for a stated reason: G1
sunshafts pending a genuinely new design idea; D-VID-1 pending a
re-aimed prereg with a different mechanism; CV-P and COMP-2 adoption
barred pending Micah's governance ruling 6; B1-class re-freezes require
the P9 bar reformulation; ST-1 DEAD on pristine evidence. The lane
survey found no new prereg drafts or design ideas. With no preregs this
wave, the prereg commit-order self-check is vacuous: no UNVERIFIABLE
ORDERING.

The six governance rulings are Micah's to make. Advancing any adoption
while CV-P and COMP-2 are doubly gated pending his ruling 6, and while
the Python-mirror question is an open red-line decision, would gamble
with his explicit boundaries. The loop's coverage duties (fork battery,
FIT, interactive availability) ran in full this wave: 36 entries
tested, 10/10 chain inputs verified, binary availability confirmed. A
wave that re-certifies the infrastructure and declines to invent
candidates to fill a quota is the loop behaving as designed.

Micah's six pending governance rulings and his sealed blind A/B
verdicts are his to make. This brief touches none of them.
