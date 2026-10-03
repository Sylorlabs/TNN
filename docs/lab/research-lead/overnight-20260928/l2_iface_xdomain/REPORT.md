# L2 INTERFACE-ADAPT Cross-Domain: REPORT

**Verdict: L2-IFACE-XDOMAIN-PASS (K1-K8 all PASS, no falsifier fires, F-COUNT silent).**

Date: 2026-10-02/03. Lane: `docs/lab/research-lead/overnight-20260928/l2_iface_xdomain/`.
Branch: `lane-l2iface-xdomain-20261002` (worktree `~/workspace/tnn-rsi-l2iface`).
Prereg: `968e3c3ab` (PREREG.md + NAMECHECK.md committed ALONE, strictly
before any implementation commit; PREREG.md unmodified).

## Summary

The L2 INTERFACE-ADAPT operation is implemented as a standalone pure-Zag
learner (`ia_learner.zag`, generic machinery only) + world side
(`ia_world.zag`) + experiment driver (`ia_driver.zag`), concatenated as
`ia_full.zag` and compiled with the pinned safebin znc (exit 0, no
errors; 22 analyzer warnings, all benign discarded-return-value notes).

A prior worker attempt in this worktree produced the full implementation
but reported BUILD-BLOCKED on two environment issues. Both were
diagnosed and resolved this session (see "Blocker diagnosis"): (1) the
git-write failure is the known safebin `git`-symlink EPERM bug; writes
succeed via `/usr/bin/git` directly. (2) the Zag binary-write block was
transient and is gone; the binary builds and runs. The prior worker's
two code fixes (saw_adapt fall-through guard; ABLATE kill moved before
QA) and its pre-verdict arithmetic amendment (FULL-Q2 484 -> 482) were
independently re-verified against the frozen design before being kept.

## Behavior (matches frozen PREREG.md section 4 exactly)

- ARM-FULL QA (100,64,7): S=24, E=1, term=64, val=7, via=0 (mX home domain).
- ARM-FULL Q2 (50,78,99): naive probe fails (entry 18 absent in B;
  IA-NAIVE-FAIL sm=0); adapt runs 4 trials over entry cands [9,17] from
  the learner's own fact scan: er=9 FAIL-WALK x2 (decoy drop), er=17
  pv=2 FAIL-VAL (decoy third arg bound as v), er=17 pv=255 ACCEPT;
  promotes zero-rel adapter mA id 1 with d=(17,0,1,255,2,2) and t17
  edge 1->0; Q2 S=482, E=1, term=78, val=50, via=1.
- Q2B/Q2C: S=134, E=1, via=1 (adapter reused, no re-adapt; a3=7 decoy
  ignored because pv=255 dropped). Q2D (t=73): S=84, E=1, via=-1 (the
  adapted interface genuinely walks entry 17 to terminal 78; saw_adapt
  guard prevents naive/adapt fall-through).
- ARM-ABLATE-X (mX killed before QA): QA and Q2 both S=3, E=0,
  ans -2/-2/-1; NM=1, NE=0, no mA, TRIAL_TOTAL=0.

## Kill bars

- K1 PASS: qa_via==0, qa_term==64, qa_val==7 (mX works in home domain).
- K2 PASS: naive_ok==0; verbatim `IA-NAIVE-FAIL sm=0` in run1.
- K3 PASS: trial_total==4, trial_fail_n==3, ad=(ps=0,pt=1,pv=255,er=17);
  verbatim `IA-CANDIDATES 9,17`, `IA-TRIAL ps=0 pt=1 pv=2 er=17 FAIL-VAL`,
  `IA-ACCEPT ps=0 pt=1 pv=255 er=17` in run1. Entry rels from the
  learner's fact scan; slots structural; choice by execution trial only.
- K4 PASS: q2_via==1, q2_term==78, q2_val==50.
- K5 PASS: snap_ok==1 (mX 32 record bytes identical teach->close),
  ma_rlen==0 (zero-rel adapter; core never duplicated), qa_via==0.
- K6 PASS: 3/3 runs byte-identical, sha256
  `f3ba73db757dd62decd30c6190a941f147b0cd5fad5dcba02e118b8fb15d2d14`.
- K7 PASS: all 8 frozen grep patterns return 0 hits on ia_learner.zag
  (`50,17,74`; `74,15,75`; `99`; `78,50`; `_MODE`; `bridge` -i;
  `python` -i; `as *i32`).
- K8 PASS: ABLATE-X Q2 ans -2/via -1, NM==1, NE==0, QA ans -2.

Falsifiers: 0 (in-Zag FALSIFIERS 0; F-COUNT checked on all 7 query S/E
values against the amended frozen values; F-EDGE-NEW: t17-count==1 FULL,
0 ABL).

## PREREG_AMENDMENT1.md (pre-verdict, arithmetic only, prereg-permitted)

FULL-Q2 frozen S 484 -> 482. Independently re-derived this session: the
prereg's T4 "77 + VALs 18+19 = 114" double-counted the entry scan
(13=scan1(50,17)); correct is 13 (entry) + 62 (foldwalk:
scan_nv(74)=14, scan_nv(75)=15, scan1(76,15)=16, scan1(77,16)=17) + 37
(addends: scan_val(75,2)=18, scan_val(77,2)=19) = 112. T3 (13+62+20=95)
was already correct. No algorithm, tick-model, or other frozen value
changes. No bar narrowed.

## Blocker diagnosis (prior BUILD-BLOCKED report, resolved)

1. `.git` writes "Operation not permitted": NOT a sandbox block. This is
   the documented safebin `git`-symlink bug (AGENTS.md, 2026-10-03):
   `$HOME/safebin/git -> /usr/bin/git` fails EPERM on object/index
   writes while `/usr/bin/git` directly works. Verified this session:
   `hash-object -w` and `update-index` via `/usr/bin/git` succeed.
   The prior worker ran with safebin first on PATH and never retried
   the resolved path. Workaround applied for all commits below.
2. Zag binary writes blocked ("znc -o produces 0-byte files"): transient;
   not reproducible this session. Fresh `znc ia_full.zag -o ia_bin`
   succeeded (exit 0, 116921 bytes on disk, 110165 main) and the binary
   runs correctly. The stale pre-fix binary in the tree was rebuilt.

Both issues were environment/toolchain, not design; no prereg change was
needed to unblock.

## Residual footprint (frozen non-claims, unchanged)

- One world family (arithmetic ADD x plan-cost aggregation);
  builder-designed, not adversary-designed; no generality claim beyond
  the two arms.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types beyond disclosed t17,
  0 new opcodes, 0 new semantic cases. Pure Zag; safebin toolchain;
  `which python3` / `which python` return nothing; zero forbidden
  executables.
- Pinned-znc-safe: no `as *i32` slice construction, no `!(A && B)` while
  conditions, no `_zag_print` for dynamic content (single preallocated
  buffer + one raw-syscall flush loop), `_zag_malloc as *u8` threading
  only, if-nesting <= 3. Every binary's stdout bytes verified.
- No em/en dashes in loop documentation. Nothing pushed; commits local
  with explicit pathspecs. Unfrozen only; frozen TNN core untouched.

## Files

- `ia_learner.zag` (generic learner; K7-clean), `ia_world.zag` (world
  facts + mX teaching), `ia_driver.zag` (two arms, in-Zag bars),
  `ia_full.zag` (concatenation; verified byte-identical to the three),
  `ia_bin` (pinned-znc build, exit 0), `ia_compile.txt` (build log),
  `ia_run1/2/3.txt` (3/3 byte-identical runs), `PREREG.md` (frozen,
  committed alone at 968e3c3ab), `PREREG_AMENDMENT1.md` (pre-verdict
  arithmetic fix), `NAMECHECK.md` (toolchain guard + steps), `REPORT.md`
  (this file).

## Open future work (not claimed)

Sealed-adversary generality of interface-adapt; composition with the
SUBSTITUTE/EXTEND/TRUNCATE/SPECIALIZE operators toward one general
composition operation.
