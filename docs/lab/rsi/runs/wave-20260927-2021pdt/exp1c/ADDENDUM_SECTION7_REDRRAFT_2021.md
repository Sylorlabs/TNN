# ADDENDUM: Section 7 redraft for EXP1c wave-20260927-2021pdt (dated pre-implementation)

Date: 2026-09-27. Author: EXP1c implementation worker (wave-20260927-2021pdt).
Status: PRE-IMPLEMENTATION. This addendum is committed alone, before any
EXP1c implementation file for this wave exists. No runs, no scores, no
analysis preceded it. It redrafts one frozen section whose arithmetic is
defective; it changes no mechanism, bar, gate, horizon, or bonus number.

## 1. The frozen defect

Frozen PREREG_EXP1c_FROZEN.md section 7 (quoted verbatim for reference):

"399 sketches, at most one plan try per replan. Worst case, enumeration
completes within 399 replans. With mean plan length <= 3 ticks plus
replan overhead, enumeration provably completes before tick 600 of the
1200-tick horizon even in the adversarial case, leaving >= 600 ticks of
learned-credit choice. The implementing wave must reproduce this bound
check in the evidence; a shorter actual completion only helps."

The independent red team (wave-20260927-1721pdt, commit 51c1f1c1f,
finding F9) proved this bound unsatisfiable on the design's own terms:
the 399 sketches in length-ascending lex order (M1) are 7 of length 1,
49 of length 2, and 343 of length 3. Trying each sketch exactly once
costs 7x1 + 49x2 + 343x3 = 7 + 98 + 1029 = 1134 primitive-action ticks,
before any replan overhead. 1134 > 600 under one action per tick, so no
implementation of the frozen M1/M3 mechanism can complete enumeration
before tick 600. The "mean plan length <= 3" phrasing in the frozen text
does not repair this: the lex order is length-ascending, so the true
mean plan length is 1134/399 (about 2.84), and 399 replans x 3 ticks =
1197 > 600 even before overhead. The frozen "leaving >= 600 ticks of
learned-credit choice" is likewise impossible: even the minimum-cost
case (one full try per sketch, no re-tries, no preemption ticks) leaves
at most 1200 - 1134 = 66 ticks.

## 2. Redrafted section 7 (governs in place of the frozen text above)

Section 7 is redrafted as follows. The frozen text in section 1 above is
retained for reference; this redraft governs.

(a) Minimum enumeration cost. The 399 sketches (M1: 7x1 + 49x2 + 343x3
in length-ascending lex order) cost a minimum of 1134 primitive-action
ticks to try once each, given one primitive action per tick and replans
that consume no world tick. This minimum assumes every sketch is tried
exactly once in full: re-tried sketches (a tried sketch re-selected on
learned credit before enumeration completes) and M4 preemption ticks
can only add ticks, never remove them.

(b) Withdrawn claims. The frozen claims "enumeration provably completes
before tick 600 of the 1200-tick horizon even in the adversarial case"
and "leaving >= 600 ticks of learned-credit choice" are arithmetically
unsatisfiable and are withdrawn. They are not repaired by redefinition:
per the S10 rule the looser reading is never adopted post-run, so no
redefinition of "tick", "completes", or "enumeration" may be used to
recover the 600-tick figure.

(c) What the evidence measures. The design cannot guarantee a
post-enumeration phase within the 1200-tick horizon, so the choice
phase is measured, not proved. The bound mode runs all 24 I-arm runs
and reports per run: whether all 399 sketches were tried at least once
(enum_done), the tick of the 399th first-try (enum_tick), the number of
distinct sketches tried (n_distinct), and the number of replans. It
also reports the maximum enum_tick over runs that completed
enumeration, against the corrected 1134-tick minimum from (a). K7
continues to measure the choice phase from actual post-enumeration
plan selections, per the frozen K7 text: if no post-enumeration plans
are observed, K7 fails and the run is VOID as a test of H1/H2 under the
frozen verdict mapping (K7 takes precedence over any K1 firing).

(d) Unchanged. No mechanism (M1-M5), calibration gate (C1-C3), kill bar
(K1-K7), horizon (1200 ticks), variant count (12), arm count (5),
bonus schedule (B0 = 40 / 120), decay rule (B0/(1+n)), or determinism
requirement changes by this redraft. The prereg freeze commit still
strictly precedes every implementation commit of this wave.

## 3. Pre-implementation assertion

Pre-implementation, no scores seen. No EXP1c implementation source for
wave-20260927-2021pdt existed when this addendum was written. The world
template docs/lab/invention/survival/src/world.zag (blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a, verified by git hash-object
2026-09-27; note: the 1721pdt addendum cited path
lab/invention/survival/src/world.zag, which no longer exists at HEAD
after a later merge rename; this wave anchors on the blob, which is
byte-identical to the frozen bounce fix 938d188cb), the training mass
docs/lab/invention/survival/kb/kb_exp1c.txt and kb_p_exp1c.txt
(committed verbatim, unmodified in the working copy), and the pinned
toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified 2026-09-27) are inherited read-only.
