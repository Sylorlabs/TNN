# NAMECHECK: NT-EVICT-H1 (evict by lowest total evidence)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

No external reference sources. `nt_h1_full.zag` is transcribed from
NT2's `nt2_full.zag` (../nt_capacity/nt2_full.zag, source digest
aac50efbd6eae5aeaeca83cb37001e290b8d0b4de49c8ab2b4c682a4fb72fdbb)
with exactly ONE functional change per PREREG Section 2: the eviction
comparator `sk(L,s,2)-sk(L,s,3)` becomes `sk(L,s,2)+sk(L,s,3)`, and the
function is renamed `nt_evict_lowest` -> `nt_evict_total` (call site
updated). All output labels, protocol, oracles, learner rules,
histogram, and kill-bar literals are carried over verbatim so the H1
output is directly comparable to NT2's line-for-line. The output-helper
block performs no science. A diff of the two sources must show only
the comparator/rename/comment lines.

## Step 2: Lane location and commit discipline

Lane directory:
`~/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/nt_evict_h1/`,
committed into the tnn-rsi-gpi3 repo (shared branch, same as NT2's lane).
Nothing is pushed to GitHub; commits stay local, explicit pathspecs only.
Prereg commit-order self-check: the first commit contains ONLY PREREG.md
and NAMECHECK.md (Steps 0-2) and must strictly precede the
implementation commit; verified via git log before the implementation
commit lands. Shared-workspace discipline per AGENTS.md: explicit
pathspecs on every commit; no `git reset`; on index.lock contention
retry with backoff, never remove the lock.

## Build record (completed 2026-10-03)

- [x] nt_h1_full.zag transcribed from ../nt_capacity/nt2_full.zag;
      diff-verified: ONLY the eviction comparator changed
      (`sk(L,s,2)-sk(L,s,3)` -> `sk(L,s,2)+sk(L,s,3)`), fn renamed
      nt_evict_lowest -> nt_evict_total, call site updated, comments
      updated. All learner rules, oracles, protocol, histogram,
      kill-bar literals, output labels verbatim.
- [x] audit grep for protect/freeze/don't-forget/task-label/importance
      logic: clean; eviction uses entry-local counters only
- [x] negated-conjunction while-check: clean; no `as *i32`+slice; no
      `_zag_print` for dynamic content; no `[]u8 as *u8`; if-nesting
      at most 3 deep (flag-let style in kill bars, transcribed)
- [x] pinned znc build: `znc nt_h1_full.zag -o h1_bin` (exit 0; one
      benign zagd-unavailable warning, foreground compilation)
- [x] 3/3 runs byte-identical (cmp); digests: runs
      `2337eb2a9d3614ea7ba58af12dd01be7709fcd0b76e5aa667915a5495ebf9a3e`,
      h1_bin
      `9ffc61c639299f66ad3b63c6de6162d7b0cd752065966f327cada1f24bd6cbf7`,
      nt_h1_full.zag
      `3886f6a127153a3d4c4121236f525af810b4da75cc5fcfbc44b1ec1c4247effd`
- [x] results vs frozen numeric predictions: CONTROL-A/B, ABLATION,
      nc, u matched; SEQ differed (nevict 40 vs 60, c_vb 5/6 vs 0/6,
      forget 1 vs 6, histogram differs) -- prereg trace missed the
      revolving-door effect; corrected mechanism derived from frozen
      rules matches binary bin-for-bin (see REPORT.md). Directional
      verdict FAIL unchanged; no amendment needed (bars/rules/mapping
      untouched).
- [x] K1-K5 evaluated against frozen bars: 1/0/1/0/1 (K4 fails on
      forget=1 despite c_vb=5 meeting the >=5/6 literal); REPORT.md
      with frozen verdict mapping: FAIL
