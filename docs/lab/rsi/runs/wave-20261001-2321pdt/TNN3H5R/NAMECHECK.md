# NAMECHECK TNN3H5R2 (H5R re-prereg, trial-loop stale-provenance fix)

Lane: TNN3H5R. Wave: wave-20261001-2321pdt. Worker roles: coordinator
(prereg freeze), builder (substrate fix), evaluator (sealed run). This
is a FRESH prereg under VOID discipline: H5R was KILLED in
wave-20261001-2021pdt on KB-W2R (8/12; revert MAPs anchored DEP edges
to superseded facts, breaking the revision chain). Nothing from the
killed battery is salvaged.

## Step 0. Toolchain verification (Worker Toolchain Guard)

Ran at lane startup, before any other work:

```
$ cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
$ which python3
(no output; exit 1)
```

`which python3` printed nothing (exit 1). Safebin PATH active for all
subsequent commands. Pure Zag only: shell invokes znc, runs binaries,
does git ops, moves/copies files. Any forbidden-executable invocation
is automatic PROCESS-FAIL.

## Scope of this lane

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- Write and commit ONLY inside
  docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/. Never push.
- Never git reset --hard, never rebase.
- Documentation rule: no em-dashes anywhere (checked with
  docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before every commit).

## Step 1. Context read (before drafting the fresh prereg)

Read in full:
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/PREREG_H5R.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/IMPLEMENTATION_H5R.md
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/SEALED_EVAL_H5R.md
  (kill verdict: KB-W2R 8/12, stale-provenance root cause)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/SEALED_H5R.md
  (world design reference; keys/values/ranges NOT reused)

## Step 2. Fresh prereg plan (H5R2)

The killed finding: on revert probes, the frozen trial loop's
first-verifying-candidate ordering promotes the fresh MAP with DEP
provenance anchored to the superseded original fact instead of the live
reverted fact, because t2_trial accepts the first candidate whose
executed output matches the expected value regardless of whether its
licensing facts are still live. Fix: a provenance gate in t2_trial
(t2_prov_ok) requiring every licensing fact of an accepted candidate to
be live, tag-1, and non-superseded; candidates licensing through dead
facts are declined, so promotion always lands on the current
(post-revision) fact lineage. New KB-W3 family: two successive
revisions before a revert; the revert must land on the latest fact.

## Steps 3+. Recorded as they happen below.

- Step 3: fresh seeds generated pre-freeze from the strings
  "TNN3H5R2|wave-20261001-2321pdt|world1..4": s1=48984, s2=59920,
  s3=20822, s4=29675 (value offsets 5, 0, 4, 2). Driver template
  DRIVER_TMPL.zag written pre-freeze, SHA-256
  f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
  recorded in the frozen prereg.
- Step 4: prereg PREREG_H5R2.md committed ALONE at
  dc7df4aba1db84e71e3e0b61c84adbf77244e590 (2026-10-02 06:30:12 UTC).
  Coordinator rulings Q1-Q5 all CONFIRM, recorded in the prereg.
- Step 5: implementation. Base byte-copied from the H5R committed file
  at 830f95ab7, SHA-256
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384
  verified before edit. Applied prereg section 4 exactly: t2_prov_ok
  helper + gate at all four t2_trial promote sites. Built with the
  pinned znc, 3/3 byte-identical builds, binary frozen at
  19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287.
  Built-in battery 46/46 PASS. Unsealed smoke (keys 9xxx) PASS
  (revert and chained revert anchor DEP edges to live facts; zero
  tag-1 facts on the MAP key at every step), 3/3 byte-identical.
  Committed at 9db334bd4 (2026-10-02 06:31:39 UTC), strictly after the
  prereg freeze.
- Step 6: KB-S1 verified on the committed file before world assembly
  (t2_prov_ok x1 definition + x4 call sites; H5R hunks intact; zero
  shadow-fact teaching calls). Worlds assembled per the frozen rule
  from the committed substrate (blob SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a)
  plus the frozen template; pre-run world SHA-256s recorded in
  SEALED_H5R2.md. All four world binaries compiled clean, ran 3/3
  byte-identical (KB-D1 PASS).
- Step 7: evaluation. KB-W0 36/36, KB-W2R 12/12, KB-B2R 24/24,
  KB-W3 8/8, KB-B3 24/24, KB-G1R PASS (13 added cognition lines,
  budget <= 15), KB-D1 PASS, KB-P1 PASS. No negative control fired.
  Verdict: H5R2 ADVANCES (BUILD-PASS). JUDGE_BRIEF.md written.
- Zero forbidden-executable invocations in this lane. No push. No
  files written outside the lane directory and /tmp scratch.
