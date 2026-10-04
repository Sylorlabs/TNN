# ADDENDUM EXP1c: implementing wave wave-20260927-1721pdt (dated pre-change)

Date: 2026-09-27. Author: EXP1c implementation worker (wave-20260927-1721pdt).
Status: PRE-RUN. This addendum is committed before any implementation file
for this wave exists. No runs, no scores, no analysis preceded it.

## 1. Prereg reuse

This implementing wave reuses the frozen prereg
docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md,
freeze commit 8b456736b (training-mass commit 5a043af3c, design draft
59b9df4b0). No number, bar, gate, or mechanism text changes. M1-M5, C1-C3,
K1-K7, item 7, and section 7 stand exactly as frozen.

## 2. M1 binding requirements (wave-20260927-1421pdt debate, quoted)

The 1421pdt attempt was ruled VOID as an uncertified attempt (M5 violated
5/5, item 7 violated, iteration 5 unauthorized). Its numbers (510, 91, 649,
649, 626) are planning data only, never findings. The binding redo
requirements for this wave:

(a) redo the retune from scratch under M5 with per-iteration commits of
variants and calibration medians before the next iteration;
(b) attempt the vel=0, lo<hi stationary-mote parameterization and at
least one boundary-trap family with the fixed P script before any
satisfiability claim about C1 is entertained; the worker-invented
|vel|-in-{1,2} constraint has no frozen standing and may not constrain
future search;
(c) fix the variants emitter's hardcoded "retune iteration 1" label
(each iteration's emitter labels itself with its own iteration number);
(d) mode_check must gate calibration (a CHECK_FAIL means no calibrate run
on those variants);
(e) clean certification end to end: pure Zag, shell only to invoke the
compiler, redirect stdout, and hash outputs (prereg item 7 verbatim:
medians computed inside Zag; sha256 hashes fine; never grep/sed/awk
evidence files);
(f) reproduce the section 7 enumeration bound check in certified evidence
(399 sketches complete before tick 600 of 1200; the implementing wave
reproduces this bound check in the evidence).

Degenerate-input standing rule (1421pdt debate): lo==hi drives the mote
guard loop into unspecified behavior; valid retunes use lo<hi; vel=0 with
lo<hi is the in-spec stationarity design. No frozen-template repair.

## 3. Path rename with blob identity

The frozen world-physics template moved by merge f55e8c27a from
docs/lab/invention/survival/src/world.zag to
lab/invention/survival/src/world.zag (rename only). Blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a at HEAD and in the working
copy, byte-identical to the bounce fix 938d188cb. Verified by
git rev-parse HEAD:lab/invention/survival/src/world.zag and git
hash-object before this addendum. The template is inherited read-only;
this wave does not modify it.

Training mass (read-only): lab/invention/survival/kb/kb_exp1c.txt and
kb_p_exp1c.txt, committed at mass 5a043af3c, verified present at HEAD.

Toolchain pin: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
mode 100755, verified before this addendum.

## 4. Pre-run assertion

Pre-run, no scores seen. No implementation source for this wave existed at
addendum time; the implementation is written from scratch after this
commit lands. Commit-order self-check: this addendum commit strictly
precedes every implementation commit of wave-20260927-1721pdt (to be
verified by the implementing worker at wave end).

## 5. Iteration plan (M5)

Each retune iteration commits, before the next iteration begins: its
variants source (self-labeled with its iteration number), its mode_check
result, its calibration medians (computed in Zag), and SHA-256 hashes of
the evidence stdout files. A retune discard reason must cite a frozen
criterion (C1, C2, or C3); "R median low" is not a frozen criterion.
Iteration 1: vel=0/lo<hi stationary-mote family (binding requirement b,
first half). Iteration 2 (if C1 unmet): boundary-trap family (binding
requirement b, second half). No satisfiability claim about C1 before both
families are attempted and committed.
