# Fork Battery Results, wave-20260924-2321pdt

Run date: 2026-09-24 PDT. Runner: fork-battery subagent (Worker 1).
Working copy ~/workspace/tnn-rsi, branch tnn-native-lab, HEAD ead33399e
at run start (unchanged during this worker's run; no concurrent commits
observed by this worker).

Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified before use. Working-copy file mode 755 (no normalization
needed this wave).

Scratch: ~/workspace/tnn-forkbattery-2321pdt (NOT /tmp). Per-fork subdirs
each contain: znc (chmod +x copy), znc_probe.zag, fixture sources, built
binaries, RESULT.txt, full.log (shell battery), harness.log (pure-Zag
battery), znc.path. The shell driver lives at
~/workspace/tnn-forkbattery-2321pdt/driver.sh (adapted from the 1721pdt
driver: new scratch path, new archive branch, plus an explicit
origin-tnn-native-lab run-start tip entry).

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

Ran `git branch -a` and `git worktree list` fresh; no stale lists used.

Local branches found: tnn-native-lab,
tnn-native-lab-wave-archive-20260923-2321pdt,
tnn-native-lab-wave-archive-20260924-0221pdt,
tnn-native-lab-wave-archive-20260924-0521pdt,
tnn-native-lab-wave-archive-20260924-1121pdt,
tnn-native-lab-wave-archive-20260924-1421pdt,
tnn-native-lab-wave-archive-wave-20260924-1721pdt (new this wave),
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

The three detached worktrees at ~/workspace/tnn-rsi-wave3/ (probe,
senses, trades, all at bd3097874) were enumerated and battery-tested
this wave, read only. This wave every enumerated fork was tested: 25/25.

## Method

1. `git fetch origin` (read only; local branches untouched) to observe
   the current origin/tnn-native-lab tip. The tip moved before the
   battery ran: run-start tip 14c8838558a29a558a041789189cf05287d98e8a
   (merged at ead33399e) was superseded by
   787212443060fe454a8a6a686a90c15994e82d59 ("NCAL v3b JOB2 results:
   K-A/K-B battery, bars, T1/T2/T3, runlog, verdict"). Both tips were
   battery-tested read only (never checked out, never merged).
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

## origin head SHAs via FETCH_HEAD this wave

fs-gr1 23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged since last
wave); main 6e621178038f5e0dd61dafa7c70df1e9eca9eb3e (MOVED since last
wave's f2a0ecfdc24); r2-7 2d99d183f693145c53213639990a3474ff786b69
(unchanged); reorg/phase-0-1 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged); wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848
(unchanged). All five passed the battery at their current tips.

## znc mode record

Working-copy pinned znc: file mode 755. All git-extracted copies came
out 644 and were chmod +x in scratch. Fork worktree copies: 660/770
(non-executable), so the recorded chmod +x-on-extracted-copy workaround
recurs on every file-mode fork. Git tree modes observed: 100755 on the
1721pdt archive and 1421pdt archive; 100644 elsewhere. Mode drift is
metadata only: every extracted znc copy sha256 matches the pinned sha.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 25 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | ead33399e277ddf53c2b6a6f95cd2af31b7c7731 (unchanged this worker's run) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | local-archive-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | local-archive-wave-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab (current tip) | origin-tnn-native-lab | 787212443060fe454a8a6a686a90c15994e82d59 | PASS | VERDICT=PASS |
| origin run-start tip (superseded) | origin-tnn-native-lab-runstart-tip | 14c8838558a29a558a041789189cf05287d98e8a | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD, moved) | origin-main | 6e621178038f5e0dd61dafa7c70df1e9eca9eb3e | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |
| forktest/main worktree | forktest-main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | VERDICT=PASS |
| forktest/r2-7 worktree | forktest-r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | VERDICT=PASS |
| forktest/reorg_phase-0-1 worktree | forktest-reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| forktest/tnn-native-lab worktree | forktest-tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| forktest/tnn-native-lab-remote worktree | forktest-tnn-native-lab-remote | cea8db22f53ed1294aff5324bbba143bd6d1df845e | PASS | VERDICT=PASS |
| forktest/wave-debate-session-1-backup worktree | forktest-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| forktest/wg-freeze worktree | forktest-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/probe worktree | wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/senses worktree | wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| ~/workspace/tnn-rsi-wave3/trades worktree | wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |

Note: the full sha for forktest/tnn-native-lab-remote is as recorded in
RESULT.txt (cea8db22f53ed1294aff5324bbba143bd6d1df845e); the worktree
list showed the short form cea8db22f.

Battery detail per fork (shell driver): B1 compile+run stdout
byte-identical to "FORKBATTERY-OK 42" PASS; B2 rerun identical and two
recompiles byte-identical (sha256 equal) PASS; B3
`znc check <file> --strict --no-zagd` exit 0 PASS; NEG1
unterminated-string compile exit 1 and check exit 1 (fails as required)
PASS; NEG2 wrong-output program compiled and ran fine with stdout
differing from expected (fails byte-compare as required) PASS;
fork-tree probe `znc_probe.zag` compiled, ran, stdout exactly
"R32_ZNC_PROBE_OK\n" PASS. The harness logs additionally show
b3_check_stdout reporting all capability claims proven on every fork.

## Negative controls

NEG1 and NEG2 discriminated on all 25 forks: NEG1 compile and check
both exited 1; NEG2 compiled and passed check but its stdout differed
from the reference (fails byte-compare as required). No fork reported
CANNOT-CONFIRM. Per-fork RESULT.txt records B1=1 B2_rerun=1
B2_recompile_identical=1 B3=1 NEG1=1 NEG2=1 PROBE=1 and harness exit 0
with VERDICT=PASS everywhere.

## Harness agreement

The rebuilt pure-Zag harness agrees with the shell driver on every fork:
25/25 VERDICT=PASS with harness exit 0, matching 25/25 shell OVERALL=PASS.
The rebuilt harness binary is byte-identical to last wave's build
(a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).

## Python contact

None. Every step used shell commands only: git, sha256sum, cmp, printf,
chmod, grep, wc, stat, the znc binaries themselves, and the compiled
pure-Zag harness binary. No Python interpreter was invoked at any point.
Scratch was under ~/workspace, never /tmp.

## Summary

25/25 forks PASS. Every enumerated branch and fork carries a znc binary
byte-identical to the pinned 498abcb5 sha and passes the full frozen
battery on both the shell driver and the pure-Zag harness: B1, B2, B3,
both negative controls failing as required, and the fork-tree probe
compiling and printing R32_ZNC_PROBE_OK. Nothing broke anywhere.
Incidents: origin/tnn-native-lab moved mid-wave (14c883855 to
787212443); both tips were tested read only and both pass. origin/main
moved since last wave (f2a0ecfdc24 to 6e621178); current tip passes.
New archive branch tnn-native-lab-wave-archive-wave-20260924-1721pdt
passes. No absent forks vs the brief; all mode drift is metadata only.

[RE-CERT] Fork battery
