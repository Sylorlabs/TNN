# RESULTS F3b: length-program interface

Wave: wave-20260930-1121pdt. Worker: F3B.
Prereg: PREREG_F3B.md, committed alone at 2a298f310 (strictly before any
implementation commit; verified by git log below).
Implementation: f3b_len.zag (417 lines, pure Zag, zero Python, zero
randomness), compiled with the repo Linux znc binary.

## Provenance header

INHERITED (F3a proc_learn.zag lineage): extract_seq, the 1055-program
enumeration (terminals K/N/C0/C1/C2, ops ADD/SUB), smallest-first search,
eval_prog/eval_node.
NEW (F3b): length-program discovery slot (second smallest-first search
over the same menu on (n->L) pairs evaluated at k=0),
length-parameterized apply (out[k]=in[f(k,n)] for k in 0..g(n)-1),
drop-last training family, 8 frozen hidden tests.

## Numbers vs frozen bars

K-F3B-1 (discovery): PASS. Trace (run1.txt, byte-identical x3) shows
"f program index: 0 [K]" and "g program index: 38 [N C1 SUB]" from
T1..T3 only, fails=0, BUILD-PASS.

K-F3B-2 (hidden generalization): PASS. 8/8 exact matches, no crash, no
ERROR line. H1 hello->hell, H2 q->(empty), H3 ptc->pt,
H4 eghjjupazbnf->eghjjupazbn, H5 ab->a, H6 wxyz->wxy, H7 k->(empty),
H8 0123456789->012345678. Expected outputs rule-derived (input minus
last char), never literals.

K-F3B-3 (zero new semantic cases): PASS. eval_node byte-identical to F3a
(diff clean, audit_k3.txt); zero matches for t==7/DIV/PARITY/COND; node
types remain exactly {0,1,2,3,4,5,6}.

K-F3B-4 (determinism): PASS. run1/run2/run3 byte-identical (cmp clean,
502 bytes each).

K-F3B-5 (N-dependence of g): PASS. Trace shows g = [N C1 SUB] (contains
N); g-probe n=7 -> 6 recorded. Constant shortcut killed by design (C2
fits T1 alone but fails T2).

K-F3B-6 (anti-tuning): PASS. Expected-output literals absent (audit_k6.txt);
discovery references only T1..T3.

Cost budget: PASS. Enumeration 2 x 1055 constructions; runtime 0.007 s
per run (budget 60 s); source 417 lines (budget 800).

## Verdict

BUILD-PASS on all six frozen bars. Classification: bounded L2+ (finite
menu selection over a product of two researcher-enumerated families). No
L3 claim made; C0-B fails by construction. Not submitted as SURVIVES.

## One-System Rule accounting

Cognition source lines added: 417 (one new file, no edits to existing
cognition code). New hardcoded semantic cases: 0. New modes: 0. New
bridges: 0. New task-specific handlers: 0. Learner-state structures
created: one persisted (f_idx=0, g_idx=38) program-index pair.

## Commit-order self-check

2a298f310 (prereg, alone) strictly precedes the implementation commit;
evidence mtimes postdate the implementation commit. git log --format
'%h %ad %s' confirms ordering.

## Toolchain guard (per 2026-09-30 governance ruling)

`which python3` returns /usr/bin/python3 (system binary, present in PATH,
not removed: removing a system interpreter is destructive and out of
scope). It was never invoked: all research computation is pure Zag
(f3b_len.zag compiled by the repo znc binary); shell used only for
orchestration (compile, run, git, grep/diff/cmp audits). Zero Python in
any decision path, harness, or analysis.

## Limitations (honest)

The length program is still menu selection, not invention: g comes from
the same 1055-program family, so the pair (f,g) collapses into the same
85-function affine closure RT2 documented. The interface now expresses
length-changing procedures F3a could not (drop-last is inexpressible
under fixed equal-length apply), but the extractor still fails on
repeated characters (RT2-C unaddressed) and revision after counterexample
remains KILLED by the impossibility proof. Cost of the extension: one
more search over the same menu, zero new semantics, which is the point.
