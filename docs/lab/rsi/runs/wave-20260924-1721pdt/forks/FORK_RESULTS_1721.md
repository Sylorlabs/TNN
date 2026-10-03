# Fork Battery Results, wave-20260924-1721pdt

Run date: 2026-09-24 PDT. Runner: fork-battery subagent (Worker B).
Working copy ~/workspace/tnn-rsi, branch tnn-native-lab.

HEAD moved mid-wave: the task brief pinned 53616213e. A concurrent wave
worker committed on tnn-native-lab while the battery ran, moving HEAD to
5b625c0be09da2dcad7f3a62c4541cadd9ac55ef ("Worker D tnn_chat FIT
re-certification wave-20260924-1721pdt on HEAD 53616213e"). The local
tnn-native-lab battery entry tested the worktree znc file at run time;
the znc blob at 5b625c0be is byte-identical to the pinned sha, and the
diff 53616213e..5b625c0be touches only one tnnchat doc file, so the
local entry's result applies to both.

Pinned znc sha256:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Scratch: ~/workspace/tnn-forkbattery-1721pdt (NOT /tmp). Per-fork subdirs
each contain: znc (chmod +x copy), znc_probe.zag, fixture sources, built
binaries, RESULT.txt, full.log (shell battery), harness.log (pure-Zag
battery), znc.path. The shell driver lives at
~/workspace/tnn-forkbattery-1721pdt/driver.sh.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches expectation). Rebuilt with the pinned znc this wave; built
binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to last wave's built harness: harness build is
deterministic). The harness was run per fork with cwd = fork scratch dir
and ./znc.path naming the fork's own znc copy; harness returns 0 on
VERDICT=PASS, 1 otherwise.

## Enumeration vs the wave brief

Ran `git branch -a`, `git branch -r`, and `git worktree list` fresh; no
stale lists used.

Local branches found (all in the brief, plus one new archive since last
wave): tnn-native-lab, tnn-native-lab-wave-archive-20260923-2321pdt,
tnn-native-lab-wave-archive-20260924-0221pdt,
tnn-native-lab-wave-archive-20260924-0521pdt,
tnn-native-lab-wave-archive-20260924-1121pdt,
tnn-native-lab-wave-archive-20260924-1421pdt (new this wave),
wave-debate-session-1-backup. No brief-listed local branch was absent,
and no unlisted local branch was present.

Remote-tracking refs in this clone: only origin/tnn-native-lab (as last
wave). The brief-listed origin/fs-gr1, origin/main, origin/r2-7,
origin/reorg/phase-0-1, origin/wg-freeze are not remote-tracking refs
here; they were fetched read only into FETCH_HEAD one at a time (no
local ref created or updated, no merge, no reset, no push) and extracted
read only via `git show FETCH_HEAD:<path>`. Nothing was checked out and
nothing was written to any origin/* ref.

Worktrees: all 7 forktest/* detached worktrees are still registered with
unchanged SHAs: main 293602fb1, r2-7 a0e7f8ba2, reorg_phase-0-1
991432226, tnn-native-lab bd3097874, tnn-native-lab-remote cea8db22f,
wave-debate-session-1-backup 3947dca1a, wg-freeze f875b3417. They were
battery-tested read only (scratch copies of each worktree's own znc;
worktrees untouched).

The three previously untracked detached worktrees at
~/workspace/tnn-rsi-wave3/ (probe, senses, trades, all at bd3097874)
were enumerated and battery-tested this wave, read only. This wave every
enumerated fork was tested: 23/23.

## Method

1. `git fetch origin` (read only; local branches untouched) to observe
   the current origin/tnn-native-lab tip.
2. Per remote head: `git fetch origin refs/heads/<name>` into FETCH_HEAD
   only, then extracted the fork's znc and znc_probe.zag read only via
   `git show FETCH_HEAD:<path>`, copied into the per-fork scratch dir,
   chmod +x on the copy (git show extraction yields 644; the chmod +x
   workaround recurs and is required).
3. Ran the frozen shell battery per fork (B1, B2, B3, NEG1, NEG2, plus
   the fork-tree probe compile+run), using the frozen invocations:
   `znc <file> --no-zagd --no-analyze --no-foreground-cache -o <bin>`
   then run the produced binary directly (never parsing znc's stdout
   status line into program output), and
   `znc check <file> --strict --no-zagd` for strict checks (flag order
   per frozen spec).
4. Ran the rebuilt pure-Zag harness per fork (see harness section).

## znc mode normalization

The working-copy pinned znc had worktree mode 754 (owner rwx, group
rx, other r) versus 100755 recorded in the index; byte-identical to the
pinned sha. It was normalized to 755 at the start of this wave, before
any battery run. Bytes unchanged after normalization (sha still
498abcb5...). Normalization recorded here.

Mode on every fork, recorded:

| fork | source mode |
|---|---|
| local-tnn-native-lab (worktree file) | 755 (normalized this wave from 754) |
| local-archive-2321pdt | git tree 100755 |
| local-archive-0221pdt | git tree 100644 |
| local-archive-0521pdt | git tree 100644 |
| local-archive-1121pdt | git tree 100755 |
| local-archive-1421pdt | git tree 100755 |
| local-wave-debate-session-1-backup | git tree 100644 |
| origin-tnn-native-lab | git tree 100644 |
| origin-fs-gr1 | git tree 100644 |
| origin-main | git tree 100644 |
| origin-r2-7 | git tree 100644 |
| origin-reorg-phase-0-1 | git tree 100644 |
| origin-wg-freeze | git tree 100644 |
| forktest-main | file 660 |
| forktest-r2-7 | file 660 |
| forktest-reorg_phase-0-1 | file 660 |
| forktest-tnn-native-lab | file 660 |
| forktest-tnn-native-lab-remote | file 660 |
| forktest-wave-debate-session-1-backup | file 660 |
| forktest-wg-freeze | file 660 |
| wave3-probe | file 660 |
| wave3-senses | file 660 |
| wave3-trades | file 770 |

All worktree checkout copies are 660/770 (non-executable), so the
recorded chmod +x-on-extracted-copy workaround recurs on every file-mode
fork. All extracted znc copies sha256 to the pinned sha, so the mode
drift is metadata only, no byte drift anywhere.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 23 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | 53616213ef468386b068d8f8c271521cd2f22876 (moved mid-wave to 5b625c0be09da2dcad7f3a62c4541cadd9ac55ef; znc blob identical) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | local-archive-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 75532a04cf327fc3d9e9d059ff7bf27f1c9e9f99 | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | f2a0ecfdc2488162815c36478bc850dd18d3d532 | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |
| forktest/main worktree | forktest-main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | VERDICT=PASS |
| forktest/r2-7 worktree | forktest-r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | VERDICT=PASS |
| forktest/reorg_phase-0-1 worktree | forktest-reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| forktest/tnn-native-lab worktree | forktest-tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| forktest/tnn-native-lab-remote worktree | forktest-tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | PASS | VERDICT=PASS |
| forktest/wave-debate-session-1-backup worktree | forktest-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| forktest/wg-freeze worktree | forktest-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/probe worktree | wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/senses worktree | wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/trades worktree | wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |

Battery detail per fork (shell driver): B1 compile+run stdout
byte-identical to "FORKBATTERY-OK 42" PASS; B2 rerun identical and two
recompiles byte-identical (sha256 equal) PASS; B3
`znc check <file> --strict --no-zagd` exit 0 PASS; NEG1
unterminated-string compile exit 1 and check exit 1 (fails as required)
PASS; NEG2 wrong-output program compiled and ran fine with stdout
differing from expected (fails byte-compare as required) PASS;
fork-tree probe `znc_probe.zag` compiled, ran, stdout exactly
"R32_ZNC_PROBE_OK\n" PASS. The harness logs additionally show
b3_check_stdout=[znc: OK -- all capability claims proven] on every fork.

## Negative controls

NEG1 and NEG2 discriminated on all 23 forks: NEG1 compile and check
both exited 1; NEG2 compiled and passed check but its stdout differed
from the reference (fails byte-compare as required). No fork reported
CANNOT-CONFIRM. Per-fork RESULT.txt records B1=1 B2_rerun=1
B2_recompile_identical=1 B3=1 NEG1=1 NEG2=1 PROBE=1 and harness exit 0
with VERDICT=PASS everywhere.

No new negative control was added: no new branch type appeared this
wave. The three wave3 worktrees share sha bd3097874 with the already
covered forktest/tnn-native-lab worktree, so the frozen set covers them.

## origin/tnn-native-lab tip observed this wave

The remote tip moved since last wave. Pre-wave local remote-tracking ref
was ca2402b44b9a44e9baed7c9d115991bf6d1b9bbc (superseded; observed but
not tested this wave, since it is no longer the head of any ref). The
read-only `git fetch origin` brought 75532a04cf327fc3d9e9d059ff7bf27f1c9e9f99
("H5 SR-S9: release driver + eval script + analysis + VERDICT
(sufficiency KILLED)"). The battery tested 75532a04c read only (never
checked out, never written). Local tnn-native-lab is behind that tip;
the merge is the coordinator's call, not this runner's.

Remote head SHAs via FETCH_HEAD this wave: fs-gr1 23f6c0f901
(unchanged), main f2a0ecfdc24 (unchanged), r2-7 2d99d183f6
(unchanged), reorg/phase-0-1 9914322267 (unchanged), wg-freeze
f875b34179 (unchanged).

## Harness agreement

The rebuilt pure-Zag harness agrees with the shell driver on every fork:
23/23 VERDICT=PASS with harness exit 0, matching 23/23 shell OVERALL=PASS.
The rebuilt harness binary is byte-identical to last wave's build
(a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).

## Python contact

None. Every step used shell commands only: git, sha256sum, cmp, printf,
chmod, grep, wc, stat, the znc binaries themselves, and the compiled
pure-Zag harness binary. No Python interpreter was invoked at any point.
Scratch was under ~/workspace, never /tmp.

## Summary

23/23 forks PASS. Every enumerated branch and fork (working-copy
tnn-native-lab, the five wave archives, wave-debate-session-1-backup,
origin/tnn-native-lab at the current tip 75532a04c, the five other
remote heads fetched read only, all seven forktest/* worktrees, and the
three ~/workspace/tnn-rsi-wave3/ worktrees at bd3097874) carries a znc
binary byte-identical to the pinned 498abcb5 sha and passes the full
frozen battery on both the shell driver and the pure-Zag harness: B1,
B2, B3, both negative controls failing as required, and the fork-tree
probe compiling and printing R32_ZNC_PROBE_OK. Nothing broke anywhere.
One mode normalization (working-copy znc 754 to 755) was recorded; all
other mode drift is metadata only.
