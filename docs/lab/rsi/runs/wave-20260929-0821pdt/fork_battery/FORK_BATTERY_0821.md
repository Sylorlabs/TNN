# FORK_BATTERY_0821.md

Wave: wave-20260929-0821pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only). Judge: JUDGE_0821.md (M2).

Execution: full fresh run pinned to run-start commit
d24eda8bdc34dee54aace6451b193754e96784ab, driver batch_0821.sh (faithful frozen
driver; pure shell, git, sha256sum; zero Python), run_one.sh byte-identical to the
frozen run_one.sh (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978
on both copies), harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not rebuilt from
source this wave). Scratch: ~/workspace/fb0821pdt/E/ (67 per-entry RESULT.txt files; driver exit 0).

Counts: 67 named entries, 65 PASS, 0 FAIL, 2 UNTESTABLE. 54 unique commits
recomputed from this wave's own table per the standing hygiene rule.
LIVE entries (2): arch-wave-20260929-0521pdt at 2e9326e6 (newly enumerated archive),
local-tnn-native-lab at d24eda8b (run-start tip). FIXTURE: 65, including the
renamed local-0521pdt-tip at d2fdf1225 (was LIVE at 0521pdt; rename declared in
ENUMERATION_MANIFEST_0821.md) and the former LIVE entry arch-wave-20260929-0221pdt
at d2fdf1225 (moved to fixture, name kept).
Duplicate groups (10): bd309787 (wt-forktest-tnn-native-lab, wt-wave3-probe,
wt-wave3-senses, wt-wave3-trades); 99143222 (rh-reorg-phase-0-1, wt-forktest-reorg,
rh-pull-3-head); f875b341 (rh-wg-freeze, wt-forktest-wg-freeze); d2fdf122
(arch-wave-20260929-0221pdt, local-0521pdt-tip); c368b8e1 (exp-sensory,
wt-exp-sensory); bedf8b4a (origin-tnn-native-lab-rt, origin-tnn-native-lab-live);
a2a36e65 (exp2, wt-exp2); a014dc1d (arch-wave-20260928-2321pdt, local-0221pdt-tip);
3947dca1 (wave-debate-session-1-backup, wt-forktest-debate-backup); 1010a63c
(exp1, wt-exp1); 2e9326e6 is unique (new archive); d24eda8b is unique (run-start tip).

Uniform evidence on all 65 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06 (0 divergence); b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit
65/65 (neg1_ok PASS, driver compile exit 1, check exit 1); NEG2 char-1
discrimination 65/65 (neg2_differs_at_char1 PASS); probe_run_stdout R32_ZNC_PROBE_OK
65/65; harness_verdict_pass_count 1 on 65/65.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at 4b76bb59
(non-TNN research-doc trees, pinned toolchain path absent, git show exit 128,
twenty-two waves running).

Recorded gaps: batch_0821.log carries only the batch-exit trailer (driver
execution trace is the 67 per-entry RESULT.txt files; verdicts rest on those,
verified by the tally above).

Setup anomaly 2 (caught by the coordinator's enumeration check, repaired
before any verdict): the mechanical sed deriving batch_0821.sh from
batch_0521.sh renamed two fixture entry NAMES (arch-wave-20260925-0521pdt
and arch-wave-20260926-0521pdt) to arch-wave-20260925-0821pdt and
arch-wave-20260926-0821pdt, colliding with the genuine 0821pdt entries of
those dates. The first background run therefore tested 65 unique names
(the second run of each collided name overwrote the first's E dir). The
names were restored, and the two missing entries
(arch-wave-20260925-0521pdt at 0ee06268, arch-wave-20260926-0521pdt at
4328a835) were run individually with the identical frozen driver; both
PASS. Final: 67 unique named entries, 67 RESULT.txt files, each recording
its correct ref SHA. No verdict was rendered on the incomplete 65-entry
tally.

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start and close (read-only
ls-remote plus the run-start check); HEAD ref -> 27a4271f unchanged. Local HEAD
static at the pin during the run for the battery's purposes (pinned-commit
discipline: mid-battery lane commits inert; the battery certifies the run-start
tip directly).

The 1721pdt probe-loss FAIL stays closed (repair 37d1d3cab is an ancestor of the pin;
toolchain files intact).

Scope stamp: certifies toolchain and extraction stability only, not the contents of
the tested commits. No future wave may cite this run as evidence that the tip's
contents are good. No transitive claim about the overnight SEM-L3 session's sims or
verdicts rides this verdict.

No em-dashes used in this document.
