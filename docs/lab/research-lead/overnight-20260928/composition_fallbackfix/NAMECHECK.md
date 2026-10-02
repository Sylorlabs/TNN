# NAMECHECK: H-FALLBACKFIX-1 Composition Fallback Repair Worker

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
- PATH=/home/hatch/safebin (allowed tools only; python3/python do not resolve)
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: H-FALLBACKFIX-1 (RETRY-2 after daemon restarts). Verify the
  unified red-team kills (R7, R4b/R4c, R6a BOUND) transfer to the
  collapsed composition mechanism C234, then repair via (a) gating the
  plen fallback on extraction failure, (b) bounding branching,
  (c) type-15 dedup.
- Branch: tnn-native-lab (local only, nothing pushed).
- Prereg: PREREG.md committed ALONE strictly before any implementation
  file was written (commit-order self-check).
- Frozen inputs (read only, never modified):
  - composition_C/cc_base.zag (1677 lines)
  - composition_collapse/cl_patch.zag (382 lines; copied to
    ff_cl_patch_orig.zag in this directory as frozen reference)
  - composition_collapse/cl_driver.zag (C234 battery protocol)
  - composition_unified_redteam/rt_driver_main.zag (R7/R4b/R4c/R6a
    world constructions)

## Build Records

(to be filled after implementation; prereg committed first)

- Patch: composition_fallbackfix/ff_patch.zag (this worker)
- Driver: composition_fallbackfix/ff_driver.zag (this worker)
- Verify driver: composition_fallbackfix/ff_verify_driver.zag (unfixed build)
- Full: ff_full.zag = cat cc_base.zag ff_patch.zag ff_driver.zag
- Binary: ff_bin (pinned znc_linux_x86_64_abed8aa1)
- Runs: ff_run1.txt, ff_run2.txt, ff_run3.txt (3/3 byte-identical target)

## Constraints Observed

- Unfrozen only. Frozen source read only.
- Pure Zag for all research logic (Step 0 guard above).
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md (byte-verified
  before commit).
- Paper untouched.
- Nothing pushed to GitHub. Explicit pathspecs for all git operations.

## Orphan Recovery (2026-10-02, triage worker)

Step 0 note: this section was written by the watchdog triage worker
during orphan recovery. No code was compiled or run by the triage
worker. Assessment only: file mtimes, sha256 checksums, git history,
and file reads. No forbidden executables invoked.

Provenance: the directory was found untracked on branch tnn-native-lab
at HEAD 05d1b7a28. PREREG.md, PREREG_AMENDMENT1.md, and
PREREG_AMENDMENT2.md were already committed (frozen) before this
recovery:

- PREREG.md frozen ALONE: commit 9d1adc2f6, 2026-10-02 15:58:24 UTC.
  Byte-identical on disk.
- PREREG_AMENDMENT1.md: commit 03febc337, 16:10:03 UTC.
  Byte-identical on disk.
- PREREG_AMENDMENT2.md: commit 22439e89f, 16:21:05 UTC.
  Byte-identical on disk.

All three freeze commits are ancestors of the recovery base. Ordering:
prereg freeze 15:58:24 strictly precedes implementation (frozen
reference copy ff_cl_patch_orig.zag written 15:58:30; first builds
from 15:59). Commit-order self-check: prereg commits strictly precede
this implementation commit.

Evidence inventory (PARTIAL; no verdict is claimed or declared):

- K1 kill transfer V-R7: CONFIRMED. ff_vr7_run1.txt (unfixed build):
  Z ans=105 via segments [M,N], false LINK14 MAP_Z to M present,
  type-15 N to M present. Matches the frozen kill signature.
- K3 R7 repaired: PASS. ff_fast_run1.txt: Z ans=105 via segments
  [N,P]; LINK14 from MAP_Z only to N and P; type-15 co-use only
  P to N; zero false LINK14; zero duplicate type-15 triples.
- K7 R3: PASS (ans=306, ff_fast_run1.txt).
- K6 R6A-DEDUP: PASS (zero duplicate type-15 triples after Z
  composition; double cb_couse_link probe wrote one edge).
- K2 V-R4B/V-R4C 600s non-termination on unfixed build: NOT
  demonstrated. ff_probe_run1.txt is a training probe only;
  ff_probe_run2.txt is truncated (40 bytes). No 600s timeout
  evidence on disk.
- K4 R4B repaired terminates with ans=-2: NOT demonstrated.
  ff_r4_run1.txt ends at R4B-Z-START; the Z query never completed
  in the recorded output.
- K5 R4C repaired: no run on disk.
- K8 C234 battery regression (T1/T2A/T2B/T3/T4/T5/T4B): no runs on
  disk.
- K9 3/3 byte-identical runs: not demonstrated. K10 architecture
  audit: not documented. K11 toolchain guard: recorded in Step 0
  above (pure Zag, python3/python absent from safebin PATH).

STALE SOURCE WARNING: ff_patch.zag (mtime 16:27:11) postdates the last
run output (ff_r4_run1.txt, 16:21:24). The current ff_patch.zag file
has no direct run evidence. The R7/R3/R6A PASS runs correspond to the
patch as embedded in ff_fast_full.zag (built 16:12:50). A completion
run must rebuild and re-run everything against the final
ff_patch.zag; do not cite the existing PASS runs as validating the
current patch file.

Base note: the frozen composition_C/cc_base.zag (1677 lines, used
verbatim, never modified) itself contains the pc_patch.zag pilot at
line 1568. This is inherited from the frozen base, not added by this
worker; all full builds in this directory concatenate that base
unchanged.

Missing: REPORT.md; the Build Records section above was never filled
in by the original worker.

Non-duplication: no COMPOSITION-FALLBACKFIX verdict exists in history;
no other committed repair of the collapsed-mechanism C234
R7/R4b/R4c/R6a kills was found. The unified single-DFS commit
e97277957 replaced mechanisms A/B/C, a different line from the
collapsed C234 target of this repair.

Recommendation: complete the battery under the already-frozen prereg
(kill bars K1-K11 unchanged, amendments 1-2 in force): R4B/R4C
termination runs with the final ff_patch.zag, full C234 regression
battery, 3/3 determinism per binary, K10 audit, then REPORT.md. No
re-preregistration is needed because the prereg freeze is valid and
verifiable; only the missing evidence must be produced.
