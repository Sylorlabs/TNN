# NAMECHECK: Unified Composition Red Team

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup (2026-10-02):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result:
- `which python3 python` returned NOTHING (empty output before "guard-check-done")
- PATH=/home/hatch/safebin
- znc: /home/hatch/safebin/znc (2026.07.0-dev)
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files, grepping sources.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: Independent adversarial attack on the UNIFIED composition
  mechanism (builder prereg 06ea103bd, results 83f8853b2), before the
  canonical-adoption recommendation is accepted.
- Posture: genuine adversary. The recommendation must survive; any
  verified kill is reported as a kill.
- Branch: tnn-native-lab (local only, nothing pushed).
- Target under test: composition_unified/un_patch.zag as COMMITTED
  (copied verbatim to rt_patch.zag in this directory, never modified;
  sha256 recorded below). Frozen base: composition_C/cc_base.zag,
  read only.

## Attack Battery (as executed; R4 split, R5/R6 redesigned after probes)

- R1 REUSE-C: C's original Z-prime reuse (composed MAP reused as a
  single segment on a fresh subject). The unified battery dropped all
  reuse tests; this checks for regression.
- R2 REUSE-B: B's original W reuse via ev_cq chained episodes.
- R3 NECESSITY-A: A's original Suite A (plen contract carries the load).
- R4a SEG-DEPTH: 6/7/8-segment chains (1-link segments); 9-segment
  decline run separately (timed).
- R4b DECLINE-BLOWUP: 3-wide depth-8 layered graph, unreachable goal.
  Worst-case decline cost; timed vs C-original control.
- R4c SUCCESS-BLOWUP: same + reachable goal, correct-path MAPs trained
  last. Worst-case success cost.
- R5 CEILING: trial's max learnable chain is 4 links (probed L=1..6).
  R5a: 4-link + 1-link compose. R5b: 5-link unlearnable, must decline.
- R6a POISON-QUALITY: equal-plen candidates, one false type-15 edge;
  does history steer selection?
- R6b POISON-COST: 5 decoy MAPs with dead-end facts + poison edges;
  search-cost inflation.
- R6c WRITE-ONLY: type-15 edges never decay, no deletion path, no dedup
  (static + dump-verified).
- R7 CONFLICT: M[1,1] vs N[7,7] vs P[8,8]; Z needs r7,r7+r8,r8.
  C says NO to M, A says YES. Unified vs C-original control.
- R8 BRIDGE-AUDIT: static. 0 modes/bridges/handlers; single
  compose_try def/call; no task-specific relation numbers;
  no COMPOSE_MODE; predicate interface purity.

## Build Records

- Base: ../composition_C/cc_base.zag (frozen, read only)
- Target: rt_patch.zag = verbatim copy of
  ../composition_unified/un_patch.zag (sha256 below)
- Driver: rt_driver.zag (this worker; adversarial battery above)
- Instrumented target: rt_patch_instr.zag = rt_patch.zag + emit
  probes ONLY (fallback-fire counter, DFS node counter); used only
  for R6b/R7 measurement, never for verdicts.
- Build: cat cc_base.zag rt_patch.zag rt_driver.zag > rt_full.zag
- Binary: rt_bin (pinned znc_linux_x86_64_abed8aa1)
- Runs: rt_run1/2/3.txt (byte-identical, sha256 recorded in REPORT.md)

## Constraints Observed

- Unfrozen only. Frozen source read only.
- Pure Zag for all research logic.
- Zero em/en dashes in NAMECHECK.md, REPORT.md (byte-verified before
  commit).
- Paper untouched.
- Nothing pushed to GitHub.
- Explicit pathspecs for all git add/commit operations.
- 0 modes/bridges/handlers added by this worker.
