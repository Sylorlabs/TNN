# NAMECHECK: NT-PORT -- D1+D2 ported to the shared continuing-learner substrate

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as NT2/H1/H3/D1/D2).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_port_full.zag` (to be written after this prereg freeze) implements
the PREREG Section 2 port on the continuing-learner skeleton from
`docs/lab/research-lead/overnight-20260928/continuing_learner/contlearn2.zag`
(associative instance memory, sequential phases, single main(), no
resets, no task labels). The ONLY memory-management semantics are the
PREREG Section 2.1 rules:

1. Slot layout: (subj, rel, obj, dom, valid, sup, ref, ins), 32 bytes;
   key = (subj, rel); arena holds nentries, nevict, ins_seq, phase.
2. Evidence update (NT-frozen, ported): hit+match -> sup++; hit+mismatch
   -> ref++, revise to (new obj, 1, 0) in place iff ref > sup; revision
   does not touch `ins`.
3. D1: eviction checkpoints (valid=1, obj, sup, ref) keyed by
   (subj, rel); re-insert with valid checkpoint restores then runs the
   update step; else fresh (taught obj, 1, 0).
4. D2: ins_seq++ and slot.ins stamp on every installation (fresh and
   restore); eviction victim = max `ins`; no tie-break.
5. ABL arm: eviction victim = min (sup-ref), slot-index tie-break; no
   checkpoint table; every insertion fresh; `ins` not maintained.
6. Kill-bar literals per PREREG Section 6 (K2: nevict==20;
   K5: ABL exact NT2-signature numbers).

Diagnosis provenance (read 2026-10-03): NT-D2 PREREG.md + REPORT.md
(`nt_d2/`, C431 PASS: D1 preserve-evidence + evict-youngest LIFO,
nevict=41, c_vb=6/6, u=12/12, forget=0, full 7-bin histogram exact);
NT-D2 NAMECHECK.md (toolchain guard, minimal-change discipline).
Substrate provenance: `continuing_learner/contlearn2.zag` (one
continuing learner, 8 sequential domains, single main(), no resets, no
task labels) and its PREREG_CONTLEARN2.md / CL2_RESULT.md.

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_port/` on the
current branch. Commits stay local, explicit pathspecs only, never
pushed. Prereg commit-order self-check: the first commit contains ONLY
PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `nt_port_full.zag`, the binary, run outputs, and
REPORT.md come in later commits. The self-check (prereg commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_port_full.zag written per PREREG Section 2; audit grep for
      protection/task-label/importance logic: clean (one disclosure
      comment matched, no logic); zero "python" bytes in source
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts;
      _zag_print never used for dynamic content)
- [x] build: `znc nt_port_full.zag -o nt_port_bin` (exit 0; benign
      zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp), exit 0, zero stderr; sha256
      recorded in REPORT.md
- [x] REPORT.md written; verdict PORT-PASS per PREREG Section 7
      (K1=1,K2=1,K3=1,K4=1,K5=1); every frozen numeric prediction
      matched exactly, including both full eviction histograms
- [x] one self-caught display bug fixed pre-report (nevict emit
      field read ins_seq offset; kill bars always read the right
      offset; frozen binary built only from corrected source)
- [x] commit-order self-check: prereg commit `edd03b062` strictly
      precedes the implementation commit (verified via git log)
