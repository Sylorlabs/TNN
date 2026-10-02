# NAMECHECK: Substrate Consolidation (decline gate over shared substrate)

## Step 0: Toolchain guard (mandatory)

Executed at session start, 2026-10-01:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
`guard-check-done`). PATH is `$HOME/safebin` only, containing the 36
allowed tools. Pinned compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

Any forbidden executable invocation = PROCESS-FAIL for this wave.
None occurred.

## Step 1: Scope

- UNFROZEN variant only. Frozen TNN-2 source is READ-ONLY in this task.
- `sc_base.zag` is a verbatim copy of the decline-gate pilot's frozen
  base (`dg_base.zag`), SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified before and after copy. It is treated as read-only reference;
  the variant is assembled as `sc_full.zag`, never by editing the base.
- Pure Zag for all research computation (substrate machinery, variant,
  driver, census). Shell used only for: invoking znc, running binaries,
  git operations, moving/copying files, assembling text (sed/head/tail).
- No sealed worlds opened or inspected. No new sealed assets created.
- Research paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Commits stay local on `tnn-native-lab`.

## Step 2: What this wave tests

Whether the decline gate (pilot `f3e6985d4`: tally live UNCERTAINTY
nodes keyed (s,r), WITHHOLD after 3) can be reimplemented as a consumer
of the shared consequence substrate (`550fa268b`): generic PURSUIT
records keyed (s,r) with a generic write path (`sub_note`) and a generic
read path (`sub_consec`), with the decline decision becoming one
substrate read in `ev_query`. Verdict target: EMERGES or SEPARATE.

## Step 3: Deliverables

In `docs/lab/research-lead/overnight-20260928/substrate_consolidation/`:
- `NAMECHECK.md` (this file)
- `CONSOLIDATION.md` (analysis, mapping, results, verdict)
- `sc_base.zag` (verbatim frozen base copy, hash-verified)
- `sc_substrate.zag` (substrate machinery + replacement ev_query)
- `sc_driver.zag` (DYN-1 driver + decline counters + substrate census)
- `sc_full.zag` (assembled unfrozen variant)
- `sc_bin` (compiled binary)
- `sc_run1.txt`, `sc_run2.txt`, `sc_run3.txt` (3/3 byte-identical)

## Step 4: Constraints honored

- Unfrozen variant only; frozen source untouched.
- Pure Zag via pinned znc; safebin; `which python3 python` empty.
- Zero em dashes in this file and all wave documentation (byte-verified
  before commit).
- Paper untouched. No sealed worlds. Nothing pushed.
- Commit with EXPLICIT pathspecs on both `git add` and `git commit`.
