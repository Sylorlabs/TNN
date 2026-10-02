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

- Step 3: fresh seeds generated and driver template written; hashes
  recorded in the frozen prereg.
