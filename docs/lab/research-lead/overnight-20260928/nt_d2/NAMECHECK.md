# NAMECHECK: NT-D2 -- evict-youngest (LIFO) comparator + D1 preserve-evidence

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as NT2/H1/H3/D1).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_d2_full.zag` (to be written after this prereg freeze) will be a
minimal derivative of D1's `nt_d1_full.zag` (source digest
`9064111ebbd86d3bc343ece45a22a5153663495db42051a1eb4c9c622972dfde` per D1
REPORT.md; read from the working tree at
`docs/lab/research-lead/overnight-20260928/nt_d1/nt_d1_full.zag`).
The ONLY semantic changes permitted by PREREG Section 2.1 are:

1. Slot layout: stride 16 -> 20 bytes (new fifth field `ins`,
   installation sequence number); arena offsets shifted accordingly
   (evhist 492 -> 612, checkpoint 652 -> 772); new `ins_seq` counter
   at arena offset 1412; `nt_new` allocation stays 2048 (1416 used).
2. `nt_evict_lowest` (globally lowest sup-ref, slot-index tie-break)
   REPLACED by `nt_evict_youngest` (occupied slot with maximum `ins`;
   `ins` unique per installation, no tie-break).
3. `nt_insert` stamps `slot.ins = ++ins_seq` on EVERY installation
   (fresh and D1-restore alike); revision in place does not touch `ins`.
4. Kill-bar literal K2: `ne1==36` -> `ne1==41` (PREREG Section 5
   derivation: 36 pigeonhole lower bound under FORGET = 0, +5 traced
   revolving-door overhead).
5. Header comment documents the D2 rule.

All helpers (z_alloc, get32, set32, o_app, o_i64, o_nl, o_flush),
learner fns (nt_find, nt_first_empty, nt_slotmap, nt_learn eviction
bookkeeping + D1 checkpoint/restore), oracle fns (va, vb, valof),
protocol fns (teach_pass, probe_acc, probe_c, probe_nc, probe_u,
forget_count, train_a, train_b, teach_b_fixed, nt_predict), the
revision rule (including the reset), and output formatting are
transcribed VERBATIM from D1 (modulo the mechanical offset/stride
renumbering in sk/sp/ck_get/ck_set/evhist accesses). Output lines keep
the `NT2` battery prefix so D2 output is directly comparable against
NT2/H1/H3/D1 frozen runs.

Diagnosis provenance (read 2026-10-03): NT2 REPORT
(`nt_capacity/REPORT.md`, C407 FAIL: eviction-preempts-revision,
nevict=41, c_vb=0/6, forget=6); H1 REPORT (`nt_evict_h1/REPORT.md`,
C412 FAIL: evict-by-total, reset collapses revised key, revolving
door, nevict=40, c_vb=5/6, forget=1); H3 REPORT
(`nt_evict_h3/REPORT.md`, C416 FAIL null: breaking reset is the
eviction-reinsertion reset); D1 REPORT (`nt_d1/REPORT.md`, C427 FAIL
informative: preserve-evidence fixes revision 0/6->6/6, nevict 41->32,
but forgetting relocates to 6 U keys via staleness-punishing
lowest-net comparator). D2 is D1's preregistered follow-up.

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_d2/` on the
current branch. Commits stay local, explicit pathspecs only, never
pushed. Prereg commit-order self-check: the first commit contains ONLY
PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `nt_d2_full.zag`, the binary, run outputs, and
REPORT.md come in later commits. The self-check (prereg commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_d2_full.zag written per PREREG Section 2.1; `diff` vs D1
      source confirms only the permitted change sites differ
      (header/layout comments, sk/sp stride 16->20 + ck 652->772 +
      evhist 492->616 renumbering, nt_evict_lowest ->
      nt_evict_youngest, nt_insert ins stamp, call site, K2 literal
      36->41). One self-caught arena bug fixed pre-build: ins_seq
      first placed at 1412 (inside the checkpoint table, 776..1415);
      moved to 1416 before compiling.
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts)
- [x] audit grep for protection/task-label/importance logic: clean
      (comparator uses only installation order; checkpoint holds only
      the learner's own prior evidence; no protection flags, no modes)
- [x] build: `znc nt_d2_full.zag -o nt_d2_bin` (exit 0; benign
      zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp); sha256 recorded in REPORT.md
- [x] REPORT.md written; verdict PASS per PREREG Section 8
      (K1=1,K2=1,K3=1,K4=1,K5=1); every frozen numeric prediction
      matched exactly, including the full 7-bin eviction histogram
- [x] commit-order self-check: prereg commit `6679be8f3` strictly
      precedes the implementation commit (verified via git log)
