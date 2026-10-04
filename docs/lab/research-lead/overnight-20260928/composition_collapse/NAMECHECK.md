# NAMECHECK: H-COLLAPSE-1 Composition Collapse Worker

## Step 0: Toolchain Guard

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
- PATH=/home/hatch/safebin (36 allowed tools; python3/python do not resolve)
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: H-COLLAPSE-1 (P0). Delete the unified mechanism's whole-MAP
  composition path into fragment DFS; route ALL composition through the
  shared type-15 fragment store plus fragment DFS.
- Branch: tnn-native-lab (local only, nothing pushed).
- Prereg: PREREG.md committed ALONE as dada745c8, strictly before any
  implementation file was written (commit-order self-check).
- Context inputs read (frozen, never modified): composition_unified/
  (prereg 06ea103bd, results 83f8853b2, ledger C224), frag_storage/
  (prereg b5b8fe190, results 7087302a8, ledger C227).

## Build Records

- Base: composition_C/cc_base.zag (1677 lines, frozen, read only)
- Patch: composition_collapse/cl_patch.zag (382 lines, this worker)
- Driver: composition_collapse/cl_driver.zag (this worker; 6 unified
  battery tests verbatim protocol plus T4B)
- Build: cat cc_base.zag cl_patch.zag cl_driver.zag > cl_full.zag
  (2379 lines)
- Binary: cl_bin (pinned znc_linux_x86_64_abed8aa1), 301632 bytes
- Compile log: cl_compile.txt (exit 0; benign A0102 warnings only, same
  class as the unified build)
- Runs: cl_run1.txt, cl_run2.txt, cl_run3.txt
- SHA-256: 4c898771fdaafe79a7bd0c0daa3faf247cbbde742fe7102a945e0e94e0b4ad5a
  (all three runs byte-identical)
- Determinism: 3/3 byte-identical (cmp clean across run1/run2/run3)

## Line Count Audit (kill bar K8)

- Unified un_patch.zag: 420
- Collapse cl_patch.zag: 382
- Delta: 38 fewer lines (9% reduction). STRICTLY FEWER: PASS.

## Bridge Audit (kill bar K10)

- `fn compose_try`: exactly 1 definition (cl_patch.zag), exactly 1 call
  site (ev_query, line 349).
- COMPOSE_MODE: 0 occurrences. `_mode` identifiers: 0.
- Whole-MAP DFS remnants: none (no cc_relseq, cc_satisfy, un_dfs,
  un_candidates, un_satisfy, cx_contract anywhere in the patch).
- Candidate enumeration consults ONLY type-15 edges with aux != 0
  (FRAG marks); B's co-use type-15 edges (aux == 0) are excluded there
  and matched only in cb_has_couse. Verified by grep over cl_patch.zag.
- Modes / bridges / handlers / new semantic cases: 0.
- Task-specific relation numbers in cl_patch.zag: none (only generic
  tags 101/102/20 and edge types 1/12/14/15, same as the unified patch).

## Co-use / Fragment Discrimination Probe (supplementary, /tmp)

Probe driver (base + cl_patch + probe main, separate build, not part of
the frozen battery): T1-style train, one X->Y episode, then Z query.
- pre Z: couse (aux==0) = 1, frag (aux!=0) = 0
- COMP-SEGS n=3 (13 26 39), z=107
- post Z: couse = 3 (episode 1 + 2 written by the 3-segment composition
  success), frag = 5 (auto-marked (m,0,L) marks)
Proves: B's history accumulates from composition successes in the
collapsed build, and FRAG marks vs co-use edges are correctly
discriminated by aux.

## T4B Fragment Consumption Evidence (kill bar K7)

- T4B-X ans=15 mx=45; T4B-Y ans=23 my=58; seeds written at edges 46-48.
- T4 world with seeded marks (mx,0,3),(mx,1,3),(my,0,2):
  COMP-SEGS n=2 (45 58), T4B-ANS=106, T4B-RESULT=PASS.
- The unseeded T4 run FAILS (ans=-2), so the seeded sub-fragment marks
  are the causal difference: the collapsed mechanism genuinely consumes
  sub-fragment marks, not a renamed whole-MAP path.

## Constraints Observed

- Unfrozen only. Frozen source read only (cc_base.zag used as assembly
  base, never modified; composition_unified and frag_storage read only).
- Pure Zag for all research logic (Step 0 guard above).
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md (byte-verified
  before commit).
- Paper untouched.
- Nothing pushed to GitHub.
- Explicit pathspecs for all git add/commit operations.
