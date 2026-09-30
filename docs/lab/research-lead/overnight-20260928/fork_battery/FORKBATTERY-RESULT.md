# FORKBATTERY-RESULT.md

Run: fork-battery 2026-09-30 (parent task: Fork Battery Worker).
Verdict: FORKBATTERY-78/80 PASS.

Execution: full fresh run pinned to run-start commit
955106ae5fb7b8e62a9ed6273c3048a5a2f8f156, driver batch_fbt.sh
(mechanical derivation of frozen batch_0221.sh; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen
instrument (sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978).
Scratch: ~/workspace/fb0930_forkbatt/E/ (80 per-entry RESULT.txt files).
BATCH-EXIT=0.

Counts: 80 named entries, 78 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (3), all PASS:
- arch-wave-20260930-0221pdt at 697d4f308 (newly enumerated archive)
- arch-wave-20260929-1721pdt-tip2 at dff8c2005 (moved archive branch tip;
  branch moved forward since 0221pdt, descendant of the enumerated pin)
- local-tnn-native-lab at 955106ae5 (run-start tip)
FIXTURE: 77, including the renamed local-20260930-0221pdt-tip at 1f681e87b
(was LIVE at 0221pdt) and arch-wave-20260929-1721pdt at 7c11ac5af (old pin
of the moved branch).

Uniform evidence on all 78 PASS: znc pin 498abcb5 (0 pin divergence);
probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS;
harness_verdict_pass_count 1 on 78/78;
driver neg1_ok=PASS (E0002 hit, compile and check both fail) on 78/78;
driver neg2_ok=PASS (compiles, runs, stdout differs at char 1) on 78/78.
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
their 0221pdt pins). Stale refs/remotes/rh-* carried as fixtures.

Per-entry results: branch name, commit SHA, and verdict are recorded in
each ~/workspace/fb0930_forkbatt/E/<entry>/RESULT.txt file; the ref field
pins the exact commit tested. The full per-entry tally (78 PASS / 2
UNTESTABLE) was taken from those files; zero FAILs, so no "what broke"
entries to report.

Scope stamp: not evidence that any tip's contents are good; no transitive
claims about any branch's research quality. The battery certifies that
the pinned toolchain extracts and runs uniformly across every enumerated
fork. Divergence detector, not capability evaluator.

Finding for the loop: archive branch tnn-native-lab-wave-archive-20260929-1721pdt
was repointed (reflog "branch: Created from HEAD") from its enumerated pin
7c11ac5af to dff8c2005, a descendant carrying additional wave-1721pdt record
commits. Benign, but archive branches are supposed to be immutable; the
loop should re-create rather than move archive branch pointers.

No em-dashes in this documentation.
