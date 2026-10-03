# FORK_BATTERY_0221.md

Wave: wave-20260930-0221pdt. Verdict: CONFIRM [NEW] as a process
confirmation (toolchain and extraction stability only).

Execution: full fresh run pinned to run-start commit
1f681e87b6a64fc65e4c01ead66b6db919c365b8, driver batch_0221.sh
(mechanical derivation of frozen batch_2321.sh; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen
instrument (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Scratch: ~/workspace/fb0930_0221pdt/E/ (77 per-entry RESULT.txt files).

Counts: 77 named entries, 75 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (2): arch-wave-20260929-2321pdt at a4314633 (newly
enumerated archive, pinned this wave), local-tnn-native-lab at
1f681e87b (run-start tip).
FIXTURE: 75, including the renamed local-20260929-2321pdt-tip at
fed72668 (was LIVE at 2321pdt; full-date rename declared in
ENUMERATION_MANIFEST_0221.md because local-2321pdt-tip was already
taken) and the former LIVE entry arch-wave-20260929-1721pdt at
7c11ac5af (moved to fixture, name kept).

Uniform evidence on all 75 tested: znc pin 498abcb5 (0 pin
divergence); probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS;
NEG1 E0002 hit 75/75; NEG2 char-1 discrimination 75/75;
harness_verdict_pass_count 1 on 75/75.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and
rh-pull-2-head at 4b76bb59 (non-TNN research-doc trees, pinned
toolchain path absent; verdict=UNTESTABLE in their RESULT.txt).

Per-entry results: branch name, commit SHA, and verdict are recorded
in each ~/workspace/fb0930_0221pdt/E/<entry>/RESULT.txt file; the ref
field pins the exact commit tested. The full per-entry tally (75 PASS
/ 2 UNTESTABLE) was taken from those files; zero FAILs, so no "what
broke" entries to report.

Duplicate SHA groups: {arch-wave-20260929-1721pdt, local-1721pdt-tip}
at 7c11ac5af (carried); {arch-wave-20260927-0221pdt, local-0221pdt-tip}
(carried per 1421pdt manifest).

Remote: zero new refs (origin/tnn-native-lab bedf8b4a unchanged at run
start, read-only ls-remote).

Scope stamp: not evidence that the tip's contents are good; no
transitive claims about any branch's research quality. The battery
certifies that the pinned toolchain extracts and runs uniformly
across every enumerated fork.
