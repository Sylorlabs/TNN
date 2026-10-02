# NAMECHECK: Cross-Domain Grammar-Construction L2M Worker

## Step 0: Toolchain Guard (2026-10-02, mandatory)

Safebin activated at worker start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Guard check done.
No Python, no forbidden executables in PATH. Pure Zag for all research
computation. Shell only for: invoking znc, running binaries, git ops,
file moves/copies, checksums, diffs, builds, greps.

Toolchain idioms honored (AGENTS.md): u8-backed cells with
little-endian get32/put32 pack/unpack helpers; no `as *i32` plus slice
construction inside functions (z_alloc uses the proven `_zag_malloc`
plus `*u8` slice pattern); output via e1str/e1i64 cursor emits into one
preallocated buffer with a single `_zag_raw_syscall(1,1,ptr,len)`
write, never `_zag_print` for dynamic content; every binary's stdout
bytes verified before trust.

Pinned compiler for this repo:
$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1

## Worker identity

Cross-Domain Grammar-Construction Worker (subagent, 2026-10-02).
Mission: grammar to construction with L2 adaptation (REBIND of the
grammar extractor to a new sealed relation) where Y cannot construct
as taught, so a generator intermediate M is required; critical test is
whether the learner creates M (L3 evidence) or the researcher must
supply it (L2).

## Build record

(To be filled as the work proceeds: file digests, commit order,
binary sha256, run digests.)

- PREREG.md frozen: <commit pending>
- Scope: docs/lab/research-lead/overnight-20260928/xdomain_grammar_l2m/
- Files: PREREG.md, NAMECHECK.md, glm_learner.zag, gl2m_h1.zag,
  gl2m_h2.zag, h1_full.zag, h2_full.zag, build.sh, h1_bin, h2_bin,
  compile logs, run1/2/3 logs per binary, REPORT.md
