# NAMECHECK: rebind_try scaling worker (replacement for H-FALLBACKFIX-1)

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02, first action of this session,
before any other work):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
which python3; echo "python3 rc=$?"
which python; echo "python rc=$?"
```

Result:
- `which python3` returned NOTHING (rc=1). `which python` returned
  NOTHING (rc=1).
- PATH=/home/hatch/safebin (allowed tools only; python3/python do not
  resolve).
- safebin/znc resolves to the system znc; all compiles use the pinned
  compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1 explicitly.
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files. File edits via
  file tools, never via interpreters.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: rebind_try scaling analysis, replacement for the completed
  H-FALLBACKFIX-1 worker. Characterize the allocation/eviction storm
  behind the R4B ~214.5s rebind_try CPU, then implement and measure
  three competing general alternatives: E1 trial-scoped bulk
  reclamation, E2 scratch-arena transactional trials, E3 bounded-scan
  (CLOCK-style) approximate eviction.
- Lane directory (new, own):
  docs/lab/research-lead/overnight-20260928/scaling_rebind/
  The scaling_fallbackfix lane is read-only and is never modified.
- Branch: current shared branch lane-hcontlife5-20261002 (the
  fallbackfix lane files were read from this working tree; the
  lane-tnn3-20261002-1421pdt branch does not track them).
- Prereg: PREREG.md in this directory, committed ALONE with this file
  strictly before any implementation file (commit-order self-check).
- Frozen inputs (read only, never modified):
  - scaling_fallbackfix/base_r4b_full.zag (2540 lines; cc_base +
    repaired ff_patch + ff_driver tests + timed driver, no main)
  - scaling_fallbackfix/base_c234_full.zag (C234 battery, own main)
  - scaling_fallbackfix/main_r4b.zag, main_corr.zag (mains)

## Build Records

(to be filled after the prereg commit; implementation follows)

- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1
- rb_base_full.zag: frozen input copy (cmp-verified)
- rb_char_full.zag: characterization build (counter hooks + phase emits)
- rb_e1_full.zag: E1 trial-scoped bulk reclamation
- rb_e2_full.zag: E2 scratch-arena transactional trials
- rb_e3_full.zag: E3 bounded-scan approximate eviction
- rb_c234_base_full.zag / rb_c234_e{1,2,3}_full.zag: C234 regression builds

## Constraints Observed

- Prereg committed alone before any implementation file exists.
- Pure Zag for all research logic (Step 0 guard above).
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md
  (byte-verified before commit).
- Local commits only with explicit pathspecs. Nothing pushed.
- Never git reset; never amend shared history.
- No new edge types, node tags, semantic cases, modes, bridges,
  handlers, or routers in any design (A0 audit at report time).
- No workload-specific constants or thresholds in any design.
