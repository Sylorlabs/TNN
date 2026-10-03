# NAMECHECK: NT-PRESSURE -- Scale the D1+D2 pressure ratio to 2x/3x/5x

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as
  NT-PORT/NT2/H1/H3/D1/D2).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: file staging, znc invocation,
  binary execution, hashing, cmp/diff for byte-identity checks, git
  operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_pressure_full.zag` (to be written after this prereg freeze) is the
NT-PORT source (`nt_port_full.zag`, C437 PORT-PASS) with ONLY the
PREREG Section 2/3 changes: parameterized N range per pressure point,
104-entry D1 checkpoint table indexed (subj-100), 104-bin eviction
histogram (subjects 100..203), 4096-byte arena, per-pressure-point
arms and kill bars. The D1/D2/ABL rules, evidence update, skeleton,
and protocol are NT-PORT's verbatim:

1. Slot layout: (subj, rel, obj, dom, valid, sup, ref, ins), 32 bytes;
   key = (subj, rel); arena holds nentries, nevict, ins_seq.
2. Evidence update (NT-frozen): hit+match -> sup++; hit+mismatch ->
   ref++, revise to (new obj, 1, 0) in place iff ref > sup; revision
   does not touch `ins`.
3. D1: eviction checkpoints (valid=1, obj, sup, ref) keyed by
   (subj, rel); re-insert with valid checkpoint restores then runs the
   update step; else fresh (taught obj, 1, 0).
4. D2: ins_seq++ and slot.ins stamp on every installation; eviction
   victim = max `ins`; no tie-break.
5. ABL arm: eviction victim = min (sup-ref), slot-index tie-break; no
   checkpoint table; every insertion fresh; `ins` not maintained.
6. Kill-bar literals per PREREG Section 6 (per pressure point p:
   K2: nevict_main == 3*N_n-10 AND phev_main == 0;
   K5: ABL exact NT2-signature numbers).

Diagnosis provenance (read 2026-10-03): NT-PORT PREREG.md + REPORT.md
(`nt_port/`, C437 PORT-PASS: D1 preserve-evidence + evict-youngest
LIFO on the continuing-learner substrate, CAP=20, 26 subjects, 1.3x
pressure; MAIN revision 6/6, FORGET=0, nevict=20, all victims novel
subjects 123..129, zero phase-1 subjects evicted; ABL c_vb=0/6,
forget=6, same count 20, opposite victim set; every frozen numeric
prediction matched exactly incl. both eviction histograms);
NT-PORT NAMECHECK.md (toolchain guard, minimal-change discipline).

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_pressure/` on the
current branch. Commits stay local, explicit pathspecs only, never
pushed. Prereg commit-order self-check: the first commit contains ONLY
PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `nt_pressure_full.zag`, the binary, run outputs,
and REPORT.md come in later commits. The self-check (prereg commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_pressure_full.zag written per PREREG Sections 2/3; audit grep
      for protection/task-label/importance logic: clean; zero "python"
      bytes in source
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts;
      _zag_print never used for dynamic content)
- [x] build: `znc nt_pressure_full.zag -o nt_pressure_bin` (exit 0;
      benign zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp), exit 0, zero stderr; sha256
      recorded in REPORT.md
- [x] REPORT.md written; verdict PORT-PASS-ALL per PREREG Section 7
      (K1=1,K2=1,K3=1,K4=1,K5=1 at P2/P3/P5); every frozen numeric
      prediction matched exactly, including all six eviction
      histograms
- [x] commit-order self-check: prereg commit `a27e484e4` strictly
      precedes the implementation commit (verified via git log)
