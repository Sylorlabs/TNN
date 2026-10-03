# NAMECHECK: NT-EVICT-H3 -- evidence-preserving revision under capacity pressure

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as NT2).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt3_full.zag` is a minimal derivative of NT2's `nt2_full.zag`
(`../nt_capacity/nt2_full.zag`, digest
`aac50efbd6eae5aeaeca83cb37001e290b8d0b4de49c8b8ab2b4c682a4fb72fdbb`
per NT2 REPORT.md). The ONLY semantic change is the revision action in
`nt_learn` (PREREG Section 2). All helpers, oracle, protocol, output
formatting, and kill-bar evaluation are transcribed verbatim. Output
lines keep the `NT2` battery prefix so H3 output is directly
byte-comparable against NT2's frozen runs
(`3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`).

Note on H1 sources: the tasking referenced NT-EVICT-H1's PREREG.md and
REPORT.md (C412 FAIL), but no `nt_evict_h1` lane exists anywhere in the
workspace (searched `~/workspace/docs/lab/research-lead/overnight-20260928`,
`~/workspace/tnn-rsi/...`, and memory). This worker proceeds from the
parent tasking's summary of H1 (evict by lowest TOTAL sup+ref; revision
reset collapses total to minimum; revolving-door on lowest slot) plus
NT2's complete frozen spec, which is sufficient because H3 changes only
the revision action defined in NT2 PREREG Section 2. The gap is flagged
in REPORT.md for the parent to reconcile.

## Step 2: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/nt_evict_h3/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local, explicit pathspecs only. The prereg-alone-then-
implementation commit order is honored inside this repo: the first
commit contains ONLY PREREG.md and NAMECHECK.md (Steps 0-2).
`nt3_full.zag`, build outputs, binaries, run outputs, and REPORT.md come
in later commits. Prereg commit-order self-check (PREREG first commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt3_full.zag = nt2_full.zag with the single-line PREREG Section 2
      change (header comment updated; `diff` confirms only the header
      and the revision line differ; fresh-insertion line untouched)
- [x] audit grep for protect/freeze/don't-forget/task-label/importance
      logic: clean (no new logic added; one call DELETED)
- [x] negated-conjunction while-check: clean; no `as *i32`+slice; no
      `_zag_print` for dynamic content; no `[]u8 as *u8`; if-nesting
      at most 3 deep (unchanged from NT2)
- [x] pinned znc build: `znc nt3_full.zag -o nt3_bin` (exit 0; one benign
      zagd-unavailable warning, foreground compilation; same as NT2)
- [x] 3/3 runs byte-identical (cmp); digests: runs
      `3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`,
      nt3_bin
      `241a47faa363bcba680e35159fd46de3c1e837522b93cb672ddff8bdda4721dd`,
      nt3_full.zag
      `1b05435faa8ae91021aaa2081e14a54a0de707433a94a261f1c66454bc6ed6a5`
- [x] run output BYTE-IDENTICAL to NT2's frozen nt2_run1.txt (cmp clean);
      run digest equals NT2's frozen run digest -- the preregistered
      byte-identity prediction held exactly
- [x] every frozen numeric prediction matched (TTC 2/2/2, pc 1, accB 18,
      nevict 41, retest 0/6/12/6, full 12-bin evhist, ML0 2/24/0/12/24
      and retest 6/6/0/12)
- [x] K1-K5 evaluated against frozen bars: 1/0/1/0/1; REPORT.md with
      frozen verdict mapping: FAIL (preregistered directional prediction)
- [x] prereg commit-order self-check: `git log --oneline` shows
      0b8561c (PREREG.md + NAMECHECK.md only) strictly before this
      implementation commit
