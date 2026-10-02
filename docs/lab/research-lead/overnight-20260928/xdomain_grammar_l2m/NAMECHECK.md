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

- PREREG.md frozen: commit e5b747176 (strictly before implementation)
- Scope: docs/lab/research-lead/overnight-20260928/xdomain_grammar_l2m/
- Pinned compiler: ~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
- Binaries: h1_bin sha256 6f076073eb1fdb2728b55c790369588310349e7423692bdaf72c8aba5e764eba
            h2_bin sha256 af7870cd5332a97ab1f2df0ed61674dd77c5b2417ccacf20849533b6b04dc995
- H1 runs 1-3: abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426 (identical)
- H2 runs 1-3: ee0bf4ba9f8acc289d549c590b96c1ca41269b1939cd39dd8ab09e6f84b3a022 (identical)
- Implementation: glm_learner.zag, gl2m_h1.zag, gl2m_h2.zag, h1_full.zag, h2_full.zag, build.sh
- One driver fix before determinism runs: H2 teach_all first-seen binding (was last-seen, rel=72)
- Verdict: XDOMAIN-GRAMMAR-L2M-COMPLETE, L3 classification
- Files: PREREG.md, NAMECHECK.md, REPORT.md, glm_learner.zag, gl2m_h1.zag,
  gl2m_h2.zag, h1_full.zag, h2_full.zag, build.sh, h1_bin, h2_bin,
  h1_compile.log, h2_compile.log, run_h1_1..3.log, run_h2_1..3.log
