# Fork battery addendum, wave-20260927-1721pdt

Post-battery repair of the local-tnn-native-lab FAIL.

Failure cause (identified): merge f55e8c27a kept
src/tools/toolchain/znc_linux_x86_64_abed8aa1 (pinned znc, byte-identical,
mode 100755) but dropped the other 12 files in src/tools/toolchain/ that
existed in its first parent 8929cdd93, including znc_probe.zag. The
frozen driver's probe-extraction step therefore failed at f55e8c27a with
verdict FAIL and cause "probe sha mismatch or extraction failure". This
was tree-content loss in the merge resolution, not a toolchain regression:
the pinned znc binary verified byte-identical (pin
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).

Repair (coordinator, local only, nothing pushed): restored the 12 dropped
files verbatim from the merge's first parent 8929cdd93
(git checkout 8929cdd93 -- the 12 paths); the znc binary was not touched
(pin still 498abcb5..., mode still 100755). Micah's deletion of the
toolchain dir stands in his own commits and in origin history; the local
branch keeps the loop's pinned toolchain per the merge's own stated
rationale (the fork battery extracts the pinned znc from the tree via
git show <commit>:src/tools/toolchain/...).

Re-test (same frozen procedure, repaired tree): pinned znc extracted,
pin verified; tree probe extracted from the repaired tree
(sha256 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
matching the frozen probe evidence); compiled with the fork's own znc,
exit 0 ("wrote native binary probe_bin (127 bytes main, 0 external
tools)", identical to frozen probe_build.log); run exit 0, stdout
R32_ZNC_PROBE_OK (sha256
acd4249a45aa79e2d7d5d4fe24106559466ebc8479362df2969232e6be348a01).
Verdict on the repaired tree: PASS on the tree-probe step.

Record honesty: the wave verdict table in FORK_RESULTS_1721.md stands as
committed (49 PASS, 1 FAIL, 4 UNTESTABLE over the pinned run-start HEAD
f55e8c27a); the FAIL there is correct for that commit. This addendum
records that the cause was identified and repaired, and the next wave's
battery tests the repaired tree. The commit-order self-check covers the
restoration commit with the other wave commits.

Evidence: this file, the restoration commit (files listed), and
~/workspace/fb1721-repair/ (scratch, ephemeral).
