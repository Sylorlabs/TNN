# PREREG F3b: interface-extension lane (length-program interface)

Wave: wave-20260930-1121pdt. Worker: F3B. Status: FROZEN. Committed alone
before any implementation.

## Background

F3a (procedure-invention v1, 'broadcast-last') scored 8/8 on hidden tests
but RT2 classified it bounded L2+: 1055 enumerated programs collapse to 85
distinct affine functions, the extractor fails on repeated characters, and
the H-REVISE revision test was KILLED by impossibility proof. The F3a
interface fixes output length equal to input length: out[k] = in[f(k,n)]
for k in 0..n-1. F3b extends the interface, not the semantics: the learner
discovers a second program g over the SAME fixed menu, and apply becomes
out[k] = in[f(k,n)] for k in 0..g(n)-1. No new semantic cases are added.
Micah explicitly forbade adding SUB, DIV, PARITY, 2-threshold COND, or any
additional researcher-authored semantic cases; this prereg freezes that
prohibition as a kill bar (K-F3B-3).

## Provenance header (per candidate)

INHERITED (from F3a, proc_learn.zag / unified_learn.zag lineage):
extract_seq extraction protocol, the 1055-program enumeration (terminals
K/N/C0/C1/C2, binary ops ADD/SUB, sizes 1/3/5), smallest-first search
order, eval_prog/eval_node machinery.
NEW (F3b): length-program discovery slot (second smallest-first search over
the same menu on (n -> L) pairs, evaluated at k=0), length-parameterized
apply, drop-last training family, 8 frozen hidden tests.

## Claim scope

No L3 claim is made. Best possible classification: bounded L2+ (menu
selection over a fixed finite family, now a product of two menus). C0-B
(open structural form) fails by construction: the solution family is
finite and researcher-enumerated. If any L3-adjacent claim arises it is
judged against Criterion 0 (C0-A through C0-D, conjunctive) and the
11-step pipeline; builders report BUILD-PASS/BUILD-FAIL only, never
SURVIVES.

## Frozen training family (drop-last)

T1: "abc" -> "ab" (n=3, L=2). T2: "xy" -> "x" (n=2, L=1).
T3: "defg" -> "def" (n=4, L=3).
Multiple lengths force the length program to be N-dependent (a constant
C2 would fit T1 alone but fails T2).

## Frozen hidden tests (8)

H1: "hello" (n=5) -> "hell". H2: "q" (n=1) -> "" (empty).
H3: "ptc" (n=3) -> "pt". H4: "eghjjupazbnf" (n=12) -> "eghjjupazbn".
H5: "ab" (n=2) -> "a". H6: "wxyz" (n=4) -> "wxy".
H7: "k" (n=1) -> "". H8: "0123456789" (n=10) -> "012345678".

## Frozen kill bars

K-F3B-1 (discovery): from T1..T3 only, the binary must discover f = K
(program index 0 in the frozen enumeration order) and g = SUB(N,C1)
(program index 38), print both programs node by node in the trace, and
report fails=0. Expected trace tokens: "f program index: 0", node list
"[K]", "g program index: 38", node list containing "N", "C1", "SUB".

K-F3B-2 (hidden generalization): all 8 hidden tests produce output (no
crash, no ERROR line) and 8/8 exact string matches against the frozen
expected outputs above.

K-F3B-3 (zero new semantic cases): the implementation defines no program
node type outside {0,1,2,3,4,5,6}; eval dispatch handles exactly types
0..6 with the same branch structure as F3a; grep for new type literals
or forbidden additions (t==7, DIV, PARITY, COND, new terminal) returns
zero matches. Recorded as a committed shell transcript.

K-F3B-4 (determinism): three consecutive runs of the frozen binary are
byte-identical (cmp clean). Zero randomness in decision paths.

K-F3B-5 (N-dependence of g): the trace shows g's node list containing N,
and a recorded probe applies g at n=7 yielding 6 (kills the
constant-program shortcut).

K-F3B-6 (anti-tuning): the eight expected-output literals ("hell",
"eghjjupazbn", "012345678", and the empty cases by construction) do not
appear as literals in the implementation source; discovery code path
references only T1..T3. Recorded grep transcript.

## Cost budget

Enumeration at most 2 x 1055 program constructions plus fits (same order
of work as F3a, doubled). Runtime at most 60 s per run on this host.
Implementation source at most 800 lines. Compile with the repo Linux znc
binary; compile failure voids the run.

## Fail definition

BUILD-FAIL overall if any K-F3B bar fails; the report names the failed
bar with verbatim evidence. BUILD-PASS requires all six bars.

## One-System Rule accounting (frozen fields to report)

Cognition source lines added, new hardcoded semantic cases (frozen
expectation: 0), new modes (0), new bridges (0), new task-specific
handlers (0), learner-state structures created (the discovered (f,g)
program-index pair persisted in memory).

## Commit order

This prereg is committed alone. Implementation and evidence commits
follow strictly after. Prereg-first self-check recorded in the results
doc via git log timestamps.
