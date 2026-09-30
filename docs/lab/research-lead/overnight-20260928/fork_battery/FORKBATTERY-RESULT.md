# FORKBATTERY-RESULT.md

Run: fork-battery 2026-09-30, wave-20260930-0805pdt (parent task: Fork
Battery Wave Worker, with the pre-run consistency gate).
Verdict: FORKBATTERY-81/83 PASS.

Execution: full fresh run pinned to run-start commit
593cc5906b9c5b2dca6a80a74140f1c2833883c1, driver batch_0805pdt.sh
(mechanical derivation of batch_0750pdt.sh; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen
instrument (sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Scratch: ~/workspace/fb0930_0805pdt/E/ (83 per-entry RESULT.txt files).
BATCH-EXIT=0.

Counts: 83 named entries, 81 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (1), all PASS:
- local-tnn-native-lab at 593cc5906 (run-start tip)
FIXTURE: 82, including the renamed local-20260930-0805pdt-tip at
3847065e2 (was LIVE in the prior wave), local-20260930-0750pdt-tip at
14a92a69d, arch-wave-20260930-0221pdt at 697d4f308 and
arch-wave-20260929-1721pdt-tip2 at dff8c2005.

Uniform evidence on all 81 PASS: znc pin 498abcb5 (0 pin divergence);
probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS; b1_cmp PASS;
b2_bin_cmp PASS; harness_verdict_pass_count 1 on 81/81;
driver neg1_ok=PASS (E0002 hit, compile and check both fail) on 81/81;
driver neg2_ok=PASS (compiles, runs, stdout differs at char 1) on 81/81.
Negative controls discriminate on every tested fork.

UNTESTABLEs (2, expected, unchanged): rh-pull-1-head at 5802fec8 and
rh-pull-2-head at 4b76bb59 (non-TNN research-doc trees, pinned toolchain
path absent; cause recorded in their RESULT.txt).

Harness provenance (S6): rebuilt this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag (sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738) with
the pinned znc (498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Rebuilt binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
BYTE-IDENTICAL to the frozen instrument ~/workspace/fb1421/fork_battery.

Remote: read-only git ls-remote this run shows zero new refs
(origin/tnn-native-lab bedf8b4aa unchanged; HEAD/main 27a4271f; fs-gr1,
r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at
their prior pins). Stale refs/remotes/rh-* carried as fixtures.

Archive-branch immutability check: all 41
tnn-native-lab-wave-archive-* branch tips checked against the prior
wave's driver SHA set. Result: 41/41 match, ZERO new movement. No new
archive branches. The four previously documented driver entries with no
live branch remain unchanged in status.

CONSISTENCY GATE (promoted to PRE-RUN this wave): the pre-run gate
(A1+A2) ran on the manifest and driver BEFORE the battery executed:
A1 83==83, A2 83/83 resolve. CONSISTENCY-GATE PRE-RUN: ALL PASS. The
full gate (A1-A4) ran before the results commit: A1 83==83, A2 83/83
resolve, A3 83/83 RESULT.txt refs match driver SHAs,
A4 81+0+2=83==83. CONSISTENCY-GATE: ALL PASS.

Per-entry results: branch name, commit SHA, and verdict are recorded in
each ~/workspace/fb0930_0805pdt/E/<entry>/RESULT.txt file; the ref field
pins the exact commit tested. The full per-entry tally (81 PASS / 2
UNTESTABLE) was taken from those files; zero FAILs, so no "what broke"
entries to report.

Scope stamp: not evidence that any tip's contents are good; no transitive
claims about any branch's research quality. The battery certifies that
the pinned toolchain extracts and runs uniformly across every enumerated
fork. Divergence detector, not capability evaluator.

Governance note: this wave ran clean on the shared branch. Explicit
pathspecs on every add/commit; git status checked before each commit;
no amend used; no other worker's files staged; no index.lock
encountered. The pre-run commit (enumeration manifest + gate promotion)
was committed strictly before the battery executed.

No em-dashes in this documentation.
