# NAMECHECK: NT-FRESHCHURN -- Churn without re-teaching: fresh novel subjects each pass

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as
  NT-LIFOBOUND/NT-PRESSURE/NT-PORT/NT2).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
  (Note: the canonical `safebin_setup/setup_safebin.sh` script was absent
  at the documented path; the pre-provisioned `$HOME/safebin` was verified
  directly: python3/python do not resolve, znc resolves to the pinned build.)
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: file staging, znc invocation,
  binary execution, hashing, cmp/diff for byte-identity checks, git
  operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`nt_freshchurn_full.zag` (to be written after this prereg freeze) is the
NT-LIFOBOUND source (`nt_lifobound_full.zag`, C445 INCONCLUSIVE) with
ONLY the PREREG Section 2 changes: (a) teach_p2 takes a pass index and
teaches the fresh novel range N^(p) = 120+(p-1)*N_n..119+p*N_n on pass
p (each novel subject taught exactly once, ever); (b) apparatus: the
D1 checkpoint table and eviction histogram are 272-entry tables indexed
(subj-100) covering subjects 100..371, arena allocates 8192 bytes
(5596 used); per-point kill-bar literals per PREREG Section 6
(K2: nevict_main == 3*N_n-4; K5: c_abl==0 AND forget_abl==6 AND
u_abl==6 AND nevict_abl == 3*N_n+3); output tag `NTFRESH`;
liability-prioritized verdict mapping per PREREG Section 7. The
D1/D2/ABL rules, NT-frozen evidence update, slot layout
(subj,rel,obj,dom,valid,sup,ref,ins), CAP=20, oracles O1/O2, phase-1
protocol, retention probe, and FORGET definition are NT-LIFOBOUND's
verbatim:

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
   N_n = 24/44/84: K2: nevict_main == 3*N_n-4 AND phev_main == 0;
   K5: c_abl==0 AND forget_abl==6 AND u_abl==6 AND
   nevict_abl == 3*N_n+3, the fresh-regime traced value frozen in
   PREREG Section 4).

Diagnosis provenance (read 2026-10-03): NT-LIFOBOUND PREREG.md +
REPORT.md (`nt_lifobound/`, C445 INCONCLUSIVE: no LIFO liability at
2x/3x/5x; NT2 signature churn-dependent; no-reteach regime too easy;
every frozen numeric prediction matched exactly incl. all six eviction
histograms bin-for-bin); NT-LIFOBOUND NAMECHECK.md (toolchain guard,
minimal-change discipline, prereg-commit-order self-check). The probe
under test is NT-LIFOBOUND PREREG Section 8's preregistered follow-up:
"restore churn WITHOUT re-teaching by supplying FRESH novel subjects
each pass (each taught once)".

Opaque identifiers: subjects are bare numeric ids 100..371; no
semantic labels appear in source, protocol, or output.

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_freshchurn/` on the
current branch (`lane-gennm10-20261003`). Commits stay local, explicit
pathspecs only, never pushed. Prereg commit-order self-check: the first
commit contains ONLY PREREG.md and NAMECHECK.md (Steps 0-2), strictly
before any implementation file. `nt_freshchurn_full.zag`, the binary,
run outputs, and REPORT.md come in later commits. The self-check
(prereg commit strictly precedes implementation commit) will be
verified via git log before the implementation commit lands.

## Build record (completed 2026-10-03)

- [x] nt_freshchurn_full.zag written per PREREG Sections 2/3/5; audit grep
      for protection/task-label/importance logic: clean (one inherited
      comment line stating their absence); zero "python" bytes in source
      beyond the `// No Python.` header comment
- [x] compiler-defect workarounds honored (get32/set32 only; single
      output buffer + one _zag_raw_syscall; no `!(A && B)` in while
      conditions; if-nesting at most 3 deep; no `[]u8 as *u8` casts;
      _zag_print never used for dynamic content)
- [x] build: `znc nt_freshchurn_full.zag -o nt_freshchurn_bin` (exit 0;
      benign zagd-unavailable warning only)
- [x] 3/3 runs byte-identical (cmp), exit 0, zero stderr; sha256
      recorded in REPORT.md (run 926f794c..., bin 6cdf237f...,
      source b6de3f0c...)
- [x] REPORT.md written; verdict FRESHCHURN-PASS at P2/P3/P5 per PREREG
      Section 7 (K1=1,K2=1,K3=1,K4=1,K5=1 at every point;
      OVERALL=FRESHCHURN-PASS-ALL); every frozen numeric prediction
      matched exactly, including all six eviction histograms bin-for-bin;
      churn-dependence account CONFIRMED (K5 returns under fresh churn),
      re-teach-dependence alternative falsified; no INFORMATIVE-FAIL
      triggers fired
- [x] Amendment 1: post-freeze histogram offset bug (4508 -> 5008),
      caught pre-verdict, fixed, rebuilt, re-run; recorded in PREREG
      Section 9. Amendment 2: informational MAIN npres prediction typo
      (5 -> 4); recorded in PREREG Section 9. Neither touches a kill bar.
- [x] commit-order self-check: prereg commit `3f2232b9a` strictly
      precedes the implementation commit (verified via git log)
