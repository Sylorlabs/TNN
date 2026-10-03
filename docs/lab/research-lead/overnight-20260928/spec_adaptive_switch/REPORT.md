# SPEC-ADAPTIVE-SWITCH: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_adaptive_switch/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (9/9 frozen kill bars)**

## Summary

Implemented the executable adaptive policy switch recommended by
SPEC-LAZY-DEFAULT: the decision rule L > (W(k)-1)*C now runs at
runtime. 150 episodes (25 drift/query cells x 6 arms: fixed lazy, fixed
eager, adaptive at L = 0, 1, 3, 7 work units), one binary, pure Zag,
safebin-built, 3/3 byte-identical
(sha256 d41e9cdc9cb59551e50c47c60a0c02c383979d811e1f5038c2288d04712fcd58).

How it works: the adaptive arm serves a 16-tick warmup lazily and
observes Dw drifts and Qw queries. It then computes the measured
per-avoided-refusal price as the exact rational pnum/pden =
max(0, Dw-Qw)/Qw rebuilds -- this IS W(k)-1 from observed rates, no
floating point -- and selects eager iff L*pden > pnum*C, with C = 1
work unit = 1 rebuild. A separate calibration program measured the
wall-clock price of one rebuild at **~10.3 us** (min over 200
clock_gettime iterations), physically anchoring the work unit; the
switch itself runs on work units, keeping the experiment deterministic.

Answers to the task's three questions:

1. **Does the adaptive switch beat fixed lazy? Yes, at every L > 0**
   (total cost J = rb + rf*L over the 25 cells: 1801 < 2656 at L=1,
   2297 < 5312 at L=3, 2869 < 10624 at L=7). At L = 0 it ties fixed
   lazy exactly (1328 = 1328): the switch correctly never fires when a
   refused query costs nothing.
2. **Does it beat fixed eager? At L = 1 and L = 3, yes**
   (1801 < 2480; 2297 < 2480). **At L = 7, no** (2869 > 2480): when
   the deadline value is that high, eager is the right policy on 22/25
   cells and adaptive pays the warmup observation cost on all of them.
   The observation cost is the honest, measured price of not knowing k
   in advance.
3. **When does it switch? At k* = 1/(L/C + 1), strict >:**
   L=1 switches for k > 1/2, L=3 for k > 1/4, L=7 for k > 1/8.
   All 9 strict-boundary cells (L == price exactly) stay lazy,
   verifying the inequality is strict, and all 25 L=0 cells stay lazy.

## What was tested

Assembly: `as_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + ld_spec (all reused
byte-unmodified, da_learn.zag explicitly untouched) + as_spec.zag
(adaptive policy layer) + as_main.zag (harness). Calibration binary
`as_calib_bin` = same reused set + as_calib.zag. Repro: `./as_build.sh`.

Sample lines (the switch moving with L on one cell, M=1 N=2,
observed Dw=16 Qw=8, measured price pnum/pden = 8/8 = 1 rebuild):

    CELL M=1 N=2 P=adapt L=0 ... sel=0 ... rebuilds=128 refusals=128
    CELL M=1 N=2 P=adapt L=1 ... sel=0 ... rebuilds=128 refusals=128
    CELL M=1 N=2 P=adapt L=3 ... sel=1 ... rebuilds=248 refusals=8
    CELL M=1 N=2 P=adapt L=7 ... sel=1 ... rebuilds=248 refusals=8

At L=1 the deadline (1) does not beat the measured price (1), so the
switch stays lazy; at L=3 it does, and the arm pays 248 rebuilds for
8 refusals instead of 128 rebuilds for 128 refusals. The price is
measured, not asserted: at M=1 N=16 the line carries pnum/pden = 15/1,
the exact W(k)-1 = 15 the parent lane measured.

Portfolio totals (J = rb + rf*L summed over the 25 cells; frozen values
matched exactly):

| L | adaptive | fixed lazy | fixed eager | adaptive beats |
|---|----------|------------|-------------|----------------|
| 0 | 1328     | 1328       | 2480        | ties lazy (never fires), beats eager |
| 1 | 1801     | 2656       | 2480        | both |
| 3 | 2297     | 5312       | 2480        | both |
| 7 | 2869     | 10624      | 2480        | lazy only |

Kill-bar adjudication: K1 prereg commit 8ce1ebf75 strictly precedes the
implementation commit (git log order on the lane dir). K2 safebin, no
python3/python, pinned znc sha256 verified in-script. K3 both binaries
build clean, exit 0, empty stderr, 3/3 byte-identical stdout, 150 CELL
lines. K4 fixed arms reproduce the parent's economics exactly on all 25
cells (lazy: rb=min(D,Q), rf=rb, kb=2Q; eager: rb=D, rf=0, kb=2Q). K5
all 100 adapt selections match the frozen table and equal the rule
recomputed from each line's own Dw/Qw/L. K5-boundary: all 9 equality
cells lazy. K6 every adapt line: answered=Q, kb=2Q; sel=0 lines
field-equal to their fixed-lazy twin; sel=1 lines satisfy
rb = min(Dw,Qw)+(D-Dw), rf = min(Dw,Qw). K7 portfolio totals match the
frozen table exactly. K8 `CALIB rebuild_ns_min=10346 iters=200`
(a second run measured 10285 ns; timing is nondeterministic and
excluded from K3). K9 ASCII-only, no world literals in new sources, one
fn main per binary, all reused sources `git diff --quiet` clean
including da_learn.zag. **9/9 PASS.**

## Tested findings

1. **The rule is now executable, not advisory.** The parent recorded a
   just token; this lane replaces the token with a measured comparison:
   the switch observes (Dw, Qw), forms the exact rational price
   max(0,Dw-Qw)/Qw, and compares against the caller-stated L in the
   same units. No human re-derives W(k) per cell.
2. **The warmup is honest lazy.** Every sel=0 adapt line is field-equal
   to its fixed-lazy twin (K6): observation costs nothing beyond what
   lazy would have paid anyway. The only cost of adaptivity is the
   warmup-phase refusals on cells where the switch then selects eager
   (e.g. 8 refusals on M=1 N=2 at L=3, vs 0 for fixed eager).
3. **Switch threshold is k* = 1/(L/C+1), strict.** Three L values put
   the boundary at three different grid points (1/2, 1/4, 1/8) and all
   three are hit exactly, including the strictness checks.
4. **C is physically anchored.** One rebuild costs ~10.3 us wall-clock
   (clock_gettime, min of 200). So "L = 3" means "one avoided refusal
   is worth ~31 us of rebuild work" -- the abstract units cash out.
5. **Adaptivity has a measured crossover vs fixed eager.** Adaptive
   wins while the eager tax saved on lazy-chosen cells exceeds the
   warmup observation cost on eager-chosen cells (L=1, 3 here); at L=7
   the tax is worth paying almost everywhere and fixed eager wins.
   This is the quantitative answer to "when is the switch worth it."

## Honest scope limits

- One drift type (unrelated, repeatable) and one query family (RET),
  inherited from the parent lane; the switch is per-family.
- Deterministic periodic schedules on the power-of-2 grid; W = 16 is
  the grid LCM, so observed rates are exact -- noisy real-world rate
  estimation (EWMA, confidence intervals) is not tested.
- L is a caller-stated policy input in work units, not itself
  measured; the lane makes the comparison executable, it does not
  verify the caller's valuation (same caveat the parent recorded for
  the just token).
- The calibration binary's timing is excluded from determinism bars by
  design; the work-unit anchor is approximate (~10.3 us, varies run to
  run), while the switch logic is exact.
- Refusals, not wall-clock latency, are the deadline currency in the
  experiment; wall-clock enters only through the C anchor.

## Recommendations

1. Future recovery proposals should state L in work units (rebuilds)
   and let the adaptive arm price them, instead of hand-arguing eager
   vs lazy per regime; the 16-tick warmup + exact-rational rule is the
   standing executable form of the parent's recommendation #3.
2. If rate estimation ever moves off the deterministic grid, the
   pnum/pden rational should gain a confidence term; the strict->
   comparison then becomes a margin test, which is a new lane, not a
   patch to this one.
3. The ~10 us rebuild anchor suggests the real cost of the eager tax
   at k=1/16 is ~150 us per useful answer at L just above 15; any
   future lane that changes what a rebuild does should re-run
   as_calib_bin and re-anchor C.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  znc_linux_x86_64_abed8aa1 (sha256-verified in as_build.sh); no Python
  invoked at any point.
- Git: `/usr/bin/git` directly; explicit pathspecs; commits local,
  never pushed.
- Commit order: 8ce1ebf75 (frozen prereg K1-K9 + NAMECHECK, alone) ->
  implementation + outputs + this report. Two tooling iterations,
  neither touching the frozen bars: (1) `expr` is not in the 36-tool
  safebin, so the K5 selection-table lookup uses bash substring
  `${S:idx:1}`; (2) the PREREG's hand-concatenated 25-char selection
  strings had transcription slips (24/23/24 chars) -- caught by the
  bar run itself, fixed by building the strings from 5-char row
  chunks with a runtime length guard; the frozen per-cell table and
  rule are unchanged.
- No amendments: the frozen bars adjudicated as written.
- Repro: `./as_build.sh` assembles both binaries, builds with the
  pinned znc, runs the experiment 3x (byte-identity + all kill bars)
  and records one wall-clock calibration run. All sources and logs
  are in this lane directory.
