# NAMECHECK: NT-CAPACITY (NT2 -- selective retention under capacity pressure)

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

No external reference sources: `nt2_full.zag` will be original code for
this lane, implementing the frozen learner rules of PREREG Section 2
verbatim (NT1's update rule; NT1's eviction rule; associative
dedicated addressing per PREREG Section 2.2; NT1's ML0 map). The
output-helper block (z_alloc, get32, set32, o_app, o_i64, o_nl,
o_flush) is transcribed from the NT1 template (`nt_full.zag`); it
performs no science. The oracle block (va, vb, valof) and protocol
helpers (teach_pass, probe_acc, probe_c, probe_nc, probe_u,
forget_count, train_a) are transcribed from NT1 verbatim; the families
are unchanged.

## Step 2: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/nt_capacity/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local, explicit pathspecs only. The prereg-alone-then-
implementation commit order is honored inside this repo: the first commit
contains ONLY PREREG.md and NAMECHECK.md (Steps 0-2). `nt2_full.zag`,
build outputs, binaries, run outputs, and REPORT.md come in later
commits. Prereg commit-order self-check (PREREG first commit strictly
precedes implementation commit) will be verified via git log before the
implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt2_full.zag written per PREREG Sections 2-5 (31 fns); audit grep for
      protect/freeze/don't-forget/task-label/importance logic: clean
- [x] negated-conjunction while-check: clean; no `as *i32`+slice; no
      `_zag_print` for dynamic content; no `[]u8 as *u8`; if-nesting
      at most 3 deep (flag-let style in kill bars)
- [x] pinned znc build: `znc nt2_full.zag -o nt2_bin` (exit 0; one benign
      zagd-unavailable warning, foreground compilation)
- [x] 3/3 runs byte-identical (cmp); digests: runs
      `3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`,
      nt2_bin
      `9f9aab1b053a35634b9bc7af65a4021e93b1d7b8e0064b7ee599ba8b1bc15a28`,
      nt2_full.zag
      `aac50efbd6eae5aeaeca83cb37001e290b8d0b4de49c8ab2b4c682a4fb72fdbb`
- [x] every frozen numeric prediction matched exactly (TTC 2/2/2, pc 1,
      accB 18/24, nevict 41, retest 0/6/12/6, full 12-bin evhist,
      ML0 2/24/0/12/24 and retest 6/6/0/12) -- except the K5 nalias
      literal, corrected by transparent amendment A1 (72->12; see
      PREREG Section 11 and REPORT.md). Pre-amendment output preserved
      at /tmp/nt2_run1_preamend.txt; post-amendment rebuild changed
      only the K5 bit and VERDICT line (diff-verified).
- [x] K1-K5 evaluated against frozen bars (as amended): 1/0/1/0/1;
      REPORT.md with frozen verdict mapping: FAIL (preregistered
      directional prediction)
