# REPORT: GEN-POOLFLOOD -- Pool-Flood Battery at NM=11

Worker: gen-poolflood (replacement). Date: 2026-10-03.
Branch: lane-genpoolflood-20261003 (worktree ~/workspace/tnn-rsi-gpf).
Governs: PREREG.md (commit 8b65bed18, strictly before implementation).

## 1. Verdict

**PASS.** F1-F7 all PASS. The pool-flood signature is NM-independent:

- PF1 (nm=4): the section is byte-identical to the canonical
  GEN-REDIM S5 section modulo the PROB label (ANS=-2, TRIES=2734,
  3 INTER= lines, 2731 INTER2= lines, zero WIDEN=1 lines).
- PF2 (nm=11, 11 MAPs): the section is byte-identical to the
  canonical S5 section with exactly the 7 predicted R1 IDENT lines
  inserted and TRIES=2741 (ANS=-2, 10 INTER= lines, 2731 INTER2=
  lines, zero WIDEN=1 lines).

The 64-pool cap, the silent drop (overflow -> dropped value, no
line, no panic), and the deterministic decline behave identically
under the dynamic layout at nm=11. The only NM-dependent term is
the +7 first-round tries that the frozen trial-order rules mandate
for the 7 extra structures.

## 2. What was built

- pf_main.zag: setup_pf1 (byte-exact copy of the frozen setup_s5;
  verified by extraction + cmp in build.sh Step 1) + setup_pf2
  (S5 facts, S5's 4 MAPs m0..m3, plus 7 IDENT distractors m4..m10
  with teach(201,201) giving in{1}) + main (PF1 at nm=4, PF2 at
  nm=11, labels GEN/PF1/PF2, single o_flush). Driver only; no
  mechanism code.
- pf_full.zag: assembly (canonical ../gen_redim/rbase.zag +
  canonical ../gen_redim/rgen_nomain.zag + pf_main.zag); exactly
  one main (grep check).
- build.sh: the full fail-closed pipeline (canonical digests,
  setup_pf1 byte-exactness, F6 opacity with a genuine ERE audit,
  assembly, znc compile, 3x runs, section split, mechanical
  expected-file construction with pre-verification, cmp per
  battery, exact counts).
- Artifacts: pf_bin, pf_compile.txt, pf_bin_run{1,2,3}.txt/.err,
  pf_sec_PF1.txt, pf_sec_PF2.txt, exp_PF1.txt, exp_PF2.txt,
  setup_pf1_frozen_extract.txt, setup_pf1_mine.txt, this REPORT.md.

Binary sha256 (pinned safebin znc 2026.07.0-dev):
- pf_bin 3656d1b46cbc6d5d2f8940dfaf2396099f9f60e41f95d48d724327c6a4540507
Run-output sha256 (3/3 byte-identical, stderr empty):
- pf_bin bc57ab5d4149292bfbb12b57fb6bcb39caaa5917ebe1f5c3e30b886274f36e6b

## 3. Kill-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| F1 COMMIT-ORDER | PASS | 8b65bed18 (PREREG.md + NAMECHECK.md Steps 0-2 only) strictly precedes the implementation commit (see Sec 6). |
| F2 DETERMINISM | PASS | 3/3 runs pairwise byte-identical (cmp), stderr empty; digests above. |
| F3 PF1-BASELINE | PASS | Section byte-identical to the canonical S5 section modulo PROB label (cmp, empty diff); 3 INTER=, 2731 INTER2=, 0 WIDEN=1, ARM line exact. |
| F4 PF2-FLOOD | PASS | Section byte-identical to the Section 5 constructed expected (cmp, empty diff); 10 INTER=, 2731 INTER2=, 0 WIDEN=1, ARM=GEN PROB=PF2 ANS=-2 TRIES=2741 exact. |
| F5 NO-MODIFY | PASS | build.sh Step 1: all four canonical digests match; setup_pf1 byte-exact vs the frozen setup_s5 extract; lane held only the driver pre-assembly, driver + one assembly post-assembly. |
| F6 OPACITY | PASS | build.sh Step 2 (genuine ERE audit): no banned tokens in the driver or PREREG.md outside the definitional list; this REPORT.md verified separately with the same audit (clean); every exercised identifier is a bare integer. |
| F7 TOOLCHAIN | PASS | Safebin from the first command (`export PATH="$HOME/safebin"` prefixes every shell command, first command verified `which python3`/`which python` empty); zero forbidden-interpreter invocations; pure Zag. |

## 4. Why this establishes NM-independence of the silent-drop signature

The 2731 INTER2= lines are a deterministic function of the pool's
add/dup/drop sequence: every sum printed is a sum of two pool
values, and the pool contents at each step are fixed by which adds
were accepted (n<64) and which were silently dropped. At nm=11 the
pool regions moved (VPOOL 1024->1408, KPOOL 1280->1664, PROV
1536->1920, nv counter 3588->5764). Byte-identity of all 2731 lines
across that move means the 64-cap and the silent drop behaved
identically: any misaddressing, cap change, or non-silent drop at
nm=11 would have diverged the sums somewhere in those 2731 lines.

No panic occurred at nm=11 with 11 live MAPs and a flooded pool;
all three runs are byte-identical. The 7 distractors were tried
exactly once each (R1, on the kind-1 seed) and never again -- the
trace shows exactly 7 extra `INTER=201` lines after line 3 and
nothing else differs from nm=4. This isolates the NM effect to the
trial count, exactly as the frozen rules predict. The pool bound is
therefore NM-independent: same cap, same silent drop, same
deterministic decline at nm=4 and nm=11.

## 5. Observations (not kill bars)

O1. Hardcoded provenance -1 slots in gen_solve. The canonical
rgen.zag writes `set32(A,1540,-1); set32(A,1544,-1)` -- literals,
not r_pv(A)+4/+8. At nm=4 these are prov[0].i1/i2 (correct); at
nm=11 they land on VPOOL slots 33/34 instead. Provably benign for
these batteries: (a) gen_record never runs (exp=999999 is never
produced), so prov[0].i1/i2 are never read; (b) VPOOL slots 33/34
are overwritten through the r_vp(A) accessor path before nv can
reach 34, and no read path (gV, gen_addval dup scan) touches an
index >= nv. GEN-REDIM's PREREG Section 3 listed "+4/+8 for the -1
slots" among the intended substitutions and C10 passed, so the
minimal-diff audit did not catch the remaining literals. Flagged
for a future hardening lane; NOT changed here (F5 NO-MODIFY).

O2. Prior opacity audits were vacuous as coded. GEN-NM10's (and
GEN-REDIM's) build.sh opacity greps use BRE alternation
(`grep -in "a|b|..."`), in which `|` is literal, so the pattern can
never match anything -- verified directly (BRE exit 1 vs ERE match
on the same input). This lane's F6 audit uses `grep -Ein` and is
genuine: it caught two real substring hits during prereg drafting
(one ordinary English word embedding a banned token, and the
workspace operating manual's filename embedding another), both
reworded before the prereg commit. A re-run of the genuine
audit over the prior lanes' sources was not in this battery's
scope; their N6/C11 conclusions should be re-checked with the ERE
form before being relied on.

## 6. Commit record

- 8b65bed18 GEN-POOLFLOOD prereg (frozen): NAMECHECK.md (Steps 0-2)
  + PREREG.md only.
- (this commit) implementation: pf_main.zag, build.sh,
  setup_pf1_frozen_extract.txt, setup_pf1_mine.txt, pf_full.zag,
  pf_bin, pf_compile.txt, pf_bin_run{1,2,3}.txt/.err,
  pf_sec_PF1.txt, pf_sec_PF2.txt, exp_PF1.txt, exp_PF2.txt, this
  REPORT.md.

## 7. Boundaries and follow-ups

- The pre-declared boundaries (PREREG.md Section 9) stand:
  installed MAPs, expected-answer verification, one ADD2 class,
  behavioral (not nv-printing) verification of the silent drop,
  NM>11 not exercised, tried2 cap not stressed, WIDEN unchanged.
- The pool bound is now empirically NM-independent at nm=11 (this
  battery, F4) in addition to nm<=4 (GEN-REDIM S5, C9).
- Suggested follow-ups: (a) harden the gen_solve prov -1 slots to
  r_pv(A)+4/+8 under a fresh prereg (canonical-source change, needs
  governance); (b) re-run the genuine ERE opacity audit over the
  GEN-REDIM/GEN-NM10 lanes per O2.
