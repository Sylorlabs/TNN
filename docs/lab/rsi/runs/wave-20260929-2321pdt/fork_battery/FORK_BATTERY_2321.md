# FORK_BATTERY_2321.md

Wave: wave-20260929-2321pdt. Verdict: CONFIRM [NEW] as a process
confirmation (toolchain and extraction stability only).

Execution: full fresh run pinned to run-start commit
fed72668cb37cf6b75e82f0acae537e2529855b8, driver batch_2321.sh
(mechanical derivation of frozen batch_1721.sh; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen
instrument (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Scratch: ~/workspace/fb2321pdt/E/ (75 per-entry RESULT.txt files;
driver exit 0).

Counts: 75 named entries, 73 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (2): arch-wave-20260929-1721pdt at 7c11ac5af (newly
enumerated archive, pinned this wave), local-tnn-native-lab at
fed72668 (run-start tip).
FIXTURE: 73, including the renamed local-1721pdt-tip at 7c11ac5af (was
LIVE at 1721pdt; rename declared in ENUMERATION_MANIFEST_2321.md) and
the former LIVE entry arch-wave-20260929-1421pdt at 347260cee1 (moved
to fixture, name kept).

Uniform evidence on all 73 tested: znc pin 498abcb5 (0 pin divergence);
probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS; NEG1 E0002 hit 73/73;
NEG2 char-1 discrimination 73/73; probe_run_stdout R32_ZNC_PROBE_OK
73/73; harness_verdict_pass_count 1 on 73/73.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head
at 4b76bb59 (non-TNN research-doc trees, pinned toolchain path absent,
twenty-five waves running).

Per-entry results: branch name, commit SHA, and verdict are recorded in
each ~/workspace/fb2321pdt/E/<entry>/RESULT.txt file; the ref field pins
the exact commit tested. The full per-entry tally (73 PASS / 2
UNTESTABLE) was taken from those files; zero FAILs, so no "what broke"
entries to report.

Duplicate SHA groups: {arch-wave-20260929-1721pdt, local-1721pdt-tip}
at 7c11ac5af (new this wave); older groups carried forward unchanged
(see ENUMERATION_MANIFEST_2321.md).

Excluded: two stale RESULT.txt files from yesterday's
wave-20260928-2321pdt found in the scratch tree (arch-20260924-0521pdt,
arch-20260927-0521pdt); not part of this wave's enumeration, not
counted.

Remote: zero new refs (origin/tnn-native-lab bedf8b4a unchanged at run
start, read-only ls-remote).

Scope stamp: not evidence that the tip's contents are good; no
transitive claims about any branch's research quality. The battery
certifies that the pinned toolchain extracts and runs uniformly across
every enumerated fork.
