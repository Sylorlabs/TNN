# FORKBATTERY-RESULT.md

Run: fork-battery 2026-09-30, wave-20260930-0750pdt (parent task: Fork
Battery Wave Worker, with the new automated consistency gate).
Verdict: FORKBATTERY-80/82 PASS.

Execution: full fresh run pinned to run-start commit
3847065e2298a619096210db2d78d48f176d86c2, driver batch_0750pdt.sh
(mechanical derivation of batch_0732pdt.sh; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen
instrument (sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Scratch: ~/workspace/fb0930_0750pdt/E/ (82 per-entry RESULT.txt files).
BATCH-EXIT=0.

Counts: 82 named entries, 80 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (1), all PASS:
- local-tnn-native-lab at 3847065e2 (run-start tip)
FIXTURE: 81, including the renamed local-20260930-0750pdt-tip at
14a92a69d (was LIVE in the prior wave), arch-wave-20260930-0221pdt at
697d4f308 and arch-wave-20260929-1721pdt-tip2 at dff8c2005 (LIVE in the
wave before, rotated to fixture), and arch-wave-20260929-1721pdt at
7c11ac5af (old pin of the moved branch).

Uniform evidence on all 80 PASS: znc pin 498abcb5 (0 pin divergence);
probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS; b1_cmp PASS;
b2_bin_cmp PASS; harness_verdict_pass_count 1 on 80/80;
driver neg1_ok=PASS (E0002 hit, compile and check both fail) on 80/80;
driver neg2_ok=PASS (compiles, runs, stdout differs at char 1) on 80/80.
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
tnn-native-lab-wave-archive-* branch tips compared against their pins
in the prior wave's driver table. Result: 41/41 match, ZERO new
movement. Four driver arch entries have no local branch, all previously
documented states, none new: arch-wave-20260929-1721pdt-tip2 (branch
deleted; SHA lives on as the 1721pdt branch tip), arch-20260924-0821pdt
and arch-20260927-0821pdt (branches deleted; tested by pinned SHA),
arch-wave-20260929-1721pdt (driver holds the old fixture pin from the
known repointing; branch at dff8c2005, no further movement).

CONSISTENCY GATE (new this wave, run before the results commit):
consistency_gate.sh asserts (A1) driver run() count == manifest total,
(A2) every run() SHA resolves, (A3) every RESULT.txt ref matches its
driver SHA, (A4) the PASS/FAIL/UNTESTABLE tally sums to the manifest
total. This wave: A1 82==82, A2 82/82 resolve, A3 82/82 match,
A4 80+0+2=82==82. CONSISTENCY-GATE: ALL PASS. The gate was validated
pre-run against the prior wave's corrected data (pass) and its
pre-amend manifest (fails A1+A4 on the exact 80/81 slip it is built to
catch).

Per-entry results: branch name, commit SHA, and verdict are recorded in
each ~/workspace/fb0930_0750pdt/E/<entry>/RESULT.txt file; the ref field
pins the exact commit tested. The full per-entry tally (80 PASS / 2
UNTESTABLE) was taken from those files; zero FAILs, so no "what broke"
entries to report.

Scope stamp: not evidence that any tip's contents are good; no transitive
claims about any branch's research quality. The battery certifies that
the pinned toolchain extracts and runs uniformly across every enumerated
fork. Divergence detector, not capability evaluator.

Governance note: this wave ran clean on the shared branch. Explicit
pathspecs on every add/commit; git status checked before each commit;
no amend used; no other worker's files staged. The pre-existing
untracked scratch files from other lanes (ROUTER7_*, beam_g0/, beam_g2/)
were left untouched.

No em-dashes in this documentation.
