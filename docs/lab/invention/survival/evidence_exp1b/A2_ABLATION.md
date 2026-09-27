# A2 Ablation (EXP1b)

## Method

Per PREREG_EXP1b.md: "deterministic replay with each novel-composition
step replaced by the best taught single-step alternative; measure the
survival drop (feeds K6)."

A1 found no agent-composed novel-composition steps, so the prereg's A2
as specified is vacuous. The implemented test went further: it replayed
each A1 variant's trace deterministically with every TAKE/COMBINE/DROP
primitive token replaced by the best taught single-step alternative,
and measured the survival drop.

## Correction (2026-09-27, independent red-team review, wave-20260927-0221pdt)

The first version of this file reported "zero steps replaced, drop 0"
with the ablated agent identical to I. That description was wrong on
two counts, found by the independent red-team reviewer's re-execution:

1. Steps WERE replaced. The implemented ablation replaced all T/C/D
   primitive tokens (not only "novel-composition steps", of which A1
   found none). Per the reviewer's independent run, replaced counts on
   the five A1 variants were 168, 97, 92, 45, and 167 (v1, v2, v4, v5,
   v7), with survival drops of 0, 0, 0, 489, and 0 ticks.

2. The v5 "drop 489" is a void-death artifact. The committed replay
   omitted I's void-safety reflex on the replayed L/R steps, so the
   replayed agent void-fell at tick 111. The reviewer's clean ablation
   (identical replacements, void-safety reflex preserved) gives a
   survival drop of exactly 0 ticks in ALL 12 variants, including v5.

Additionally, the reviewer's instrumented re-execution showed I builds
a LAMP (crystal+mote COMBINE) in 6/12 variants and DROPs/places it in
5/12 (v2, v5, v7, v8, v11). These builds are emergent accidents of the
fixed plan enumeration (a "C" token executing while two items happen to
be held), never selected or exploited: the clean ablation shows removing
all T/C/D behavior changes survival by 0 ticks everywhere, so the builds
are causally inert. They do not constitute agent-level composition, but
the evidence text's claim that I "never builds anything" was false and
is corrected here.

## Verdict

K6 FIRES. On the prereg's letter (A1 found no novel-composition steps;
removing them cannot reduce survival) and on the clean ablation (drop 0
in all 12 variants with the reflex preserved), the novelty was not doing
the work. The invention claim is killed.
