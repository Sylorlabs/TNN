# NAMECHECK: NT-LIFOBOUND -- The LIFO boundary: novel subjects NOT re-taught

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as
  NT-PRESSURE/NT-PORT/NT2/H1/H3/D1/D2).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
  (Note: the canonical `safebin_setup/setup_safebin.sh` script was absent
  at the documented path; the pre-provisioned `$HOME/safebin` was verified
  directly: 49 entries, python3/python do not resolve, znc resolves.)
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: file staging, znc invocation,
  binary execution, hashing, cmp/diff for byte-identity checks, git
  operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_lifobound_full.zag` (to be written after this prereg freeze) is the
NT-PRESSURE source (`nt_pressure_full.zag`, C439 PORT-PASS-ALL) with
ONLY the PREREG Section 2/3 changes: teach_p2 takes a pass index and
teaches N subjects only on pass 1 (passes 2-3: C+K only); per-point
kill-bar literals per PREREG Section 6 (K2: nevict_main == N_n-4;
K5 unchanged NT2-signature); output tag `NTLIFO`; liability-
prioritized verdict mapping per PREREG Section 7. The D1/D2/ABL
rules, evidence update, arena layout (4096 bytes; 104-entry D1
checkpoint table indexed (subj-100); 104-bin eviction histogram,
subjects 100..203), oracles O1/O2, phase-1 protocol, retention probe,
and FORGET definition are NT-PRESSURE's verbatim:

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
6. Kill-bar literals per PREREG Section 6 (per pressure point p,
   N_n = 24/44/84: K2: nevict_main == N_n-4 AND phev_main == 0;
   K5: c_abl==0 AND forget_abl==6 AND u_abl==6 AND
   nevict_abl == 3*N_n-10 -- deliberately unchanged from
   NT-PRESSURE; its predicted failure is the Dimension B finding).

Diagnosis provenance (read 2026-10-03): NT-PRESSURE PREREG.md +
REPORT.md (`nt_pressure/`, C439 PORT-PASS-ALL: D1+D2 survives to 5x
with re-taught novel subjects; MAIN revision 6/6, FORGET=0,
nevict=62/122/242=3N_n-10, zero phase-1 subjects evicted across 426
MAIN evictions; ABL reproduced the NT2 failure signature at each
point; every frozen numeric prediction matched exactly incl. all six
eviction histograms); NT-PRESSURE NAMECHECK.md (toolchain guard,
minimal-change discipline). The preregistered open boundary under
test: "Whether LIFO's tenure principle holds when novel subjects
are NOT re-taught every pass" (NT-PRESSURE PREREG Section 8 /
REPORT recommended follow-up).

Opaque identifiers: subjects are bare numeric ids 100..203; no
semantic labels appear in source, protocol, or output.

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_lifobound/` on the
current branch. Commits stay local, explicit pathspecs only, never
pushed. Prereg commit-order self-check: the first commit contains ONLY
PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `nt_lifobound_full.zag`, the binary, run outputs,
and REPORT.md come in later commits. The self-check (prereg commit
strictly precedes implementation commit) will be verified via git log
before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_lifobound_full.zag written per PREREG Sections 2/3/5; audit grep
      for protection/task-label/importance logic: clean (one inherited
      comment line stating their absence); zero "python" bytes in source
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts;
      _zag_print never used for dynamic content)
- [x] build: `znc nt_lifobound_full.zag -o nt_lifobound_bin` (exit 0;
      benign zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp), exit 0, zero stderr; sha256
      recorded in REPORT.md (run c983f0dd..., bin 6713b635...,
      source eee16fe6...)
- [x] REPORT.md written; verdict INCONCLUSIVE at P2/P3/P5 per PREREG
      Section 7 (K1=1,K2=1,K3=1,K4=1,K5=0 at every point); every frozen
      numeric prediction matched exactly, including all six eviction
      histograms bin-for-bin; Dimension A (no liability) and
      Dimension B (K5 discrimination not achieved; ABL signature
      churn-dependent) reported separately; no INFORMATIVE-FAIL
      triggers fired
- [x] commit-order self-check: prereg commit `8998c14a1` strictly
      precedes the implementation commit (verified via git log)
