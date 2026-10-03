# NAMECHECK: NT-D1 -- preserve evidence across eviction/re-insertion

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as NT2/H3).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_d1_full.zag` (to be written after this prereg freeze) will be a
minimal derivative of NT2's `nt2_full.zag` (source digest
`aac50efbd6eae5aeaeca83cb37001e290b8d0b4de49c8ab2b4c682a4fb72fdbb` per NT2
REPORT.md; read from the `tnn-native-lab` branch at
`docs/lab/research-lead/overnight-20260928/nt_capacity/nt2_full.zag`).
The ONLY semantic changes permitted by PREREG Section 2.1 are:

1. Learner arena grows to hold the 40-entry checkpoint table
   (`nt_new` allocation bump; layout documented in source header).
2. `nt_learn` eviction branch: checkpoint (value, sup, ref) of the
   victim key before the slot is overwritten.
3. `nt_learn` insertion: restore a valid checkpoint then run the
   frozen update step; else fresh (key, value, 1, 0) as before.
4. Kill-bar literal K2: `ne1==6` -> `ne1==36` (PREREG Section 5
   derivation); output label for the K2 line unchanged.

All helpers (z_alloc, get32, set32, o_app, o_i64, o_nl, o_flush),
learner fns (nt_find, nt_first_empty, nt_evict_lowest, nt_slotmap),
oracle fns (va, vb, valof), protocol fns (teach_pass, probe_acc,
probe_c, probe_nc, probe_u, forget_count, train_a, train_b,
teach_b_fixed, nt_predict), the eviction comparator, the revision
rule, and output formatting are transcribed VERBATIM from NT2.
Output lines keep the `NT2` battery prefix so D1 output is directly
comparable against NT2/H1/H3 frozen runs.

Diagnosis provenance (read 2026-10-03 from the `tnn-native-lab`
branch): NT2 REPORT (`nt_capacity/REPORT.md`, C407 FAIL:
eviction-preempts-revision, nevict=41, c_vb=0/6, forget=6); H1 REPORT
(`nt_evict_h1/REPORT.md`, C412 FAIL: evict-by-total, revolving door,
nevict=40, c_vb=5/6, forget=1); H3 REPORT (`nt_evict_h3/REPORT.md`,
C416 FAIL null result: revision rule dead code under lowest-net,
output byte-identical to NT2, breaking interaction is the
eviction-reinsertion reset, K2's nevict==6 arithmetically impossible,
minimum 36 evictions derived). D1 is H3's recommended follow-up (D1).

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_d1/` on the
current branch. Commits stay local, explicit pathspecs only, never
pushed. Prereg commit-order self-check: the first commit contains ONLY
PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `nt_d1_full.zag`, the binary, run outputs, and
REPORT.md come in later commits. The self-check (prereg commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_d1_full.zag written per PREREG Section 2.1; `diff` vs NT2
      source confirms only the four permitted change sites differ
      (header, arena+ck_get/ck_set+nt_new 2048, nt_insert helper +
      eviction checkpoint + insertion call, K2 literal 6->36)
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts)
- [x] audit grep for protection/task-label/importance logic: clean
      (no new decision logic; checkpoint table holds only the
      learner's own prior evidence)
- [x] build: `znc nt_d1_full.zag -o nt_d1_bin` (exit 0; benign
      zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp); sha256 recorded in REPORT.md
- [x] REPORT.md written; verdict FAIL per PREREG Section 8
      (K1=1,K2=0,K3=0,K4=0,K5=1); prediction miss honestly accounted
- [x] commit-order self-check: prereg commit `2a162c01c` strictly
      precedes the implementation commit (verified via git log)
