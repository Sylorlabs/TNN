# Fork battery results, wave-20260928-0829pdt

Fork-battery lane. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start commit
9f38273560b7b20657dc27660f5c9d4a322dd9f8 ("wave-20260928-0821pdt:
INCOMPLETE record (second consecutive runtime failure, zero partial
commits, lock cleared)"). Run start 2026-09-28 08:32 PDT; batch close
2026-09-28 08:35 PDT. Read-only git throughout (rev-parse,
for-each-ref, ls-remote, show, worktree list, log, ls-tree; no
checkout, no pull, no push, no fetch, no reset). Pinned-commit
discipline: every entry extracted at its run-start-pinned SHA, never
at a live ref. Scratch: ~/workspace/fb0829 (fresh this wave). The
wave lock was not touched.

Honest-treatment note on carried evidence: the failed 0521pdt wave
committed fork-lane evidence ef418824b (56 PASS, 0 FAIL, 2
UNTESTABLE at pin f03aa6fc8) which the 0821pdt INCOMPLETE record
carried forward as evidence only, not a debated verdict. Precedent in
this loop is a full fresh re-run at each wave's run-start pin, so
this wave re-ran the full battery at the new pin 9f3827356. The
0521pdt carried evidence now agrees with a fresh execution and is
discharged as evidence only; it never became a debated verdict.

## Verdict

58 named battery entries. 56 PASS, 0 FAIL, 2 UNTESTABLE, 0 CONFIRM.
47 unique commits across the 58 named entries (recomputed from this
wave's own verdict table; standing hygiene rule). Live: 1
(local-tnn-native-lab at 9f3827356). Fixture: 57.

No new FAIL. The 1721pdt probe-loss FAIL stays closed: the
toolchain-dir repair (37d1d3cab) is an ancestor of the task-pinned
commit 9f38273560b7b20657dc27660f5c9d4a322dd9f8 (confirmed via
`git merge-base --is-ancestor` before the batch ran); znc_probe.zag
and the znc binary are present in the tree, the probe compiles and
runs with the pinned znc (R32_ZNC_PROBE_OK on all 56 tested
entries), and local-tnn-native-lab PASSES the full frozen battery
at the pinned commit.

The two UNTESTABLEs are the expected pull-head entries
rh-pull-1-head and rh-pull-2-head (identical cause seventeen waves
running: non-TNN research-doc trees, pinned toolchain path absent).
No result was faked. Scope stamp: this battery certifies toolchain
and extraction stability only, not the contents of the tested
commits.

UNTESTABLE caveat: the two UNTESTABLEs are content-dependent (their
trees lack the toolchain path), not toolchain regressions; the
counts above are never headlined without this caveat.

Duplicate named entries (11 beyond firsts, named honestly per the
standing hygiene rule): exp1 and wt-exp1 share
1010a63c3c1cc3f3724f6cf0ca55decc08207a2d; exp2 and wt-exp2 share
a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4; exp-sensory and
wt-exp-sensory share c368b8e1ffecec2f9061011f5d7c0e3e68675e0a;
wave-debate-session-1-backup and wt-forktest-debate-backup share
3947dca1a77c00818575dbc7476556c8278b8b7b; rh-pull-3-head,
rh-reorg-phase-0-1, and wt-forktest-reorg share
9914322267e1358e5542a23c72ec51d1a9ae43df; rh-wg-freeze and
wt-forktest-wg-freeze share f875b34179f570ba1ad555262cd401ddc4a52848;
wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
wt-wave3-trades share bd30978748fa83bbea6e423a7074cf32b7304291;
origin-tnn-native-lab-rt and origin-tnn-native-lab-live share
bedf8b4aab0110e3c115fb1bca3903551a32577e.

Per-entry verdicts live in evidence/<entry>/RESULT.txt (58 dirs).
Negative controls discriminate on every tested fork: neg1_ok PASS on
56/56, neg2_ok PASS on 56/56 (NEG1 fails compile and check with
E0002 on the fork's own znc stderr; NEG2 compiles, runs, and its
stdout differs from expected at char 1).

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
local branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the frozen value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc extracted read only from the task-pinned
commit 9f38273560b7b20657dc27660f5c9d4a322dd9f8
(src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use; build command: ./znc_build fork_battery.zag
--no-zagd --no-analyze --no-foreground-cache -o fork_battery). Built
binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to the frozen instrument; the harness build is
deterministic; lineage sha a2e6284c confirmed). The harness ran per
entry with cwd = entry scratch dir and ./znc.path naming that
entry's own extracted znc copy. Harness exit 0 with VERDICT=PASS on
56/56 tested battery entries, VERDICT=FAIL on 0.

The shell driver run_one.sh is the frozen 0521pdt driver byte
identical (diff exit 0): it extracts the znc and probe read only,
records their shas, verifies both against the pins, runs the
rebuilt harness, extracts the B2 bin sha by tokenizing the harness
output on whitespace first (no packed line is ever split on '='),
confirms NEG1 fails with E0002 reported by the fork's own znc
stderr, confirms NEG2 stdout differs from expected at char 1 (run
stdout "WRONG OUTPUT" vs expected "FORKBATTERY-OK 42"), compiles the
tree probe with the fork's own znc and runs it expecting
R32_ZNC_PROBE_OK, then deletes the per-entry znc copy.

## znc pin verification (this wave)

znc pin 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
uniform across all 56 tested entries (56/56 match; 0 pin divergence).
Probe pin 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
verified on every tested entry before harness use. B2 binary pin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
matched on 56/56. B1 run output pin
5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066
matched on 56/56.

Remote heads: ls-remote at run start and at batch close are
byte-identical (fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze,
tnn-native-lab, pull/1, pull/2, pull/3 heads all unchanged vs the
0521pdt pins). See lsremote_start.txt and lsremote_close.txt.
