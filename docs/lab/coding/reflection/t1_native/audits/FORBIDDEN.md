# IV-P0 FORBIDDEN VOCABULARY — frozen 2026-09-22

Static audit of the deliberation ENGINE source (`t1n_delib.zag`), run BEFORE
the first deliberation. Any hit voids the trial. The audit greps the engine
source for each pattern below (case-sensitive unless noted). Runtime INPUTS
(entries.txt, records.txt) are taught knowledge and are NOT audited — only
the crew-authored engine source is.

## A. Original crew-authored emitter names (Task 1's invention, must not recur)

em_f_rec | em_f_popcount | em_f_tri | em_f_sentinel | em_f_filter |
em_f_multiacc | em_f_fizzbuzz | em_f_rle

## B. Solution keywords as code identifiers or string literals

fizzbuzz | popcount | fact_r — as identifiers, string literals, or comments
in the engine source. (The engine is generic; it has no reason to name
these. It reads them from taught records at runtime.)

## C. Hardcoded trigger lists

Any string literal containing a comma-separated keyword list bound to a
mechanism/family/schema id, e.g. `"lcm,multiple"`, `"count"`,
`"palindrome,forwards,backwards,racecar"`, or any `if(sid==N){return "...";}`
/ `if(fid==N)` table mapping ids to keyword strings or code shapes.

## D. Complete solution programs

Any string literal (or concatenated literal sequence) that, alone, is a
complete compilable Zag program solving a probe task (P1–P6) or a T4x item.
Rationale: the engine must never contain a full solution; solutions are
assembled at deliberation time from taught inputs.

## E. Schema-name-indexed tables

Any table/array/map keyed by construct names (recursion, bit-walk,
nested-loop, sentinel-scan, char-filter, multi-accumulator,
modular-dispatch, run-group, or equivalents) mapping to code, triggers,
or emitter ids. The engine's indexing is by TAUGHT ENTRY ID (L-*, A-*,
E-*, I-*, S-*, G-*, C-ARCH-*) only.

## F. T4x/probe task text

No T4x item spec text, no probe goal text, and no expected-output literal
(`55`, `3628800`, `3a2b`, …) tied to a task may appear in the engine
source. (Expected outputs live in the driver's frozen probe/battery
files, which the engine never reads before freeze — §7.1.)

## Audit procedure (frozen)

`sweep_forbidden.py <engine-source>` greps sections A–F, prints every hit
with line number, exits nonzero on any hit. The driver runs it after
building the engine and BEFORE the first `propose`; the output is
committed as `audits/ivp0_result.txt`. Manual review of the full engine
source by the coordinator follows the grep (grep is necessary, not
sufficient).
