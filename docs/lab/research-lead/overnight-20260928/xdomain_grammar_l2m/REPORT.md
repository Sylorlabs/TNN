# REPORT: Cross-Domain Grammar to Construction with L2 Adaptation and Learner-Created Intermediate (XDOMAIN-GRAMMAR-L2M)

Worker: Cross-Domain Grammar-Construction Worker, 2026-10-02.
Prereg: PREREG.md, frozen and committed BEFORE implementation
(commit e5b747176). No prereg changes since.

## Verdict

XDOMAIN-GRAMMAR-L2M-COMPLETE with L3 classification.

The learner created the generator intermediate M from generic
machinery and labeled experience: visible creation trace, white-box
learner state, persistence, reuse without rebuild, revision after a
regime change, and a clean origin audit. All 12 kill bars hold for
both H1 and H2, 3/3 byte-identical runs per binary.

## What was tested

Grammar to construction where Y, as taught, CANNOT construct: Y was
taught only as a memorized divisor to example-word lookup (16 to 17,
8 to 9), and the construction method for a NEW divisor did not exist
in any taught structure. The sealed goal Z (rule 3, divisor 24, need a
valid word) requires two things at once: (a) L2 relation rebinding of
the grammar extractor X from its training relation to the sealed
relation, and (b) a generator intermediate M that produces a valid
word from a divisor. The critical question was the origin of M:
learner-created (L3 evidence) or researcher-supplied (L2, not L3).

## Kill bar results

| Bar | H1 | H2 | Evidence |
|-----|----|----|----------|
| K1 H1-SOLVE | PASS | - | TREAT Z ARM-RESULT PASS; REBOUND a=5 param=73 rebound_of=0; m_created=1; M-PROG bytes (4,0,0) |
| K2 H2-SOLVE | - | PASS | VC-COMPOSE ok m1=1 m2=2 rel=73; m_created=1 |
| K3 L1-NECESSARY | PASS | PASS | L1-ONLY fails both (6 tries H1 / 9 tries H2, L1-FAIL) |
| K4 CAUSAL | PASS | PASS | ABL-X, ABL-Y, FRESH fail both with l2_on=1 |
| K5 M-NECESSARY | PASS | PASS | NO-M fails both: rebound succeeds (24 found) but Y lookup misses (24 to -1) |
| K6 M-CREATED | PASS | PASS | C-ROUND 1 gain=2 positive; score 2/2; grep audits 0/0/0 on glm_learner.zag; no SUPPLIED-INSTALL on TREAT |
| K7 REUSE | PASS | PASS | Z2 PASS both; build_count stays 1 (no rebuild) |
| K8 REVISE | PASS | PASS | adapt code 2 both; Mprev (4,0,0) sup=1; M (4,0,0,1,0,0); Z3 PASS both |
| K9 REBIND-DISCOVERED | PASS | PASS | 73/74 appear only in add_fact lines; scan/rebind/composer/constructor clean |
| K10 DETERMINISM | PASS | PASS | 3/3 byte-identical (sha256 below) |
| K11 NO-TEMPLATE | PASS | PASS | no GRAMMAR_TO_CONSTRUCTION, no CHAIN_COUNT, no signature literals in composer |
| K12 TOOLCHAIN | PASS | PASS | safebin, no python3/python, pure Zag |

## The critical test, in detail

Phase 1 (exact L1 reuse) fails for both mechanisms: H1 tries 2
singles and 4 pairs (X gives -1 on the sealed rule; D1 gives 9, whose
constructed word 10 is not the goal); H2 tries all 9 ordered mode
pairs. L1-FAIL is genuine, not a threshold artifact.

Phase 2 runs the L2 solver: the generic candidate scan finds the
sealed relations in first-seen order with the distractor relation
first (74 before 73), and the generic REBIND operator copies the
rebindable grammar MAP to each candidate. Before rebinding, the
intermediate gate runs the greedy constructor over the frozen generic
op basis {CPY,ADD,MUL,SET1,INC} against the driver-generated labeled
word-validity experience (labels only; the validity rule is never
called by the constructor). The creation trace is visible in the run
output:

```
C-ROUND 1 base=0 win=4,0,0 gain=2 score=2
M-BUILT score=2
M-PROG n=1 gen=0 created=1 build_count=1 bytes=4,0,0,
```

The learner-created intermediate is the one-instruction program
[INC R0], i.e. w = D+1, which is the unique first-max greedy winner
on the G1 labels. It is stored in the dedicated learner-state slot
(created=1; the SUPPLIED arm instead sets created=0 with a supplied
marker). The rebound grammar MAP (param=73, rebound_of=X) composes
with Y, and Y now dispatches through M instead of the memorized
lookup: (X73, Y): 24 to 25, promoted with full provenance.

Causal decomposition of the two requirements, from the arms:
- NO-M (allow_build=0): rebinding succeeds (24 extracted) but the
  goal fails because Y's lookup has no entry for 24. L2 rebinding
  alone is insufficient; the intermediate is causally necessary.
- SUPPLIED (researcher installs M): passes. The task is solvable
  given M; the only question was origin, and on the TREAT path the
  learner creates it.

## Intermediate-origin analysis (L2 vs L3)

What is researcher-authored: the op basis, the greedy search
algorithm, the label tables, the world validity rules, the taught MAPs
and executors, the REBIND operator. This is generic machinery, in the
same footprint class as composition_l3 FORAGE (which set the
precedent for this bar).

What is learner-determined: the final program form [INC R0] was not
enumerated as a candidate by the researcher; it emerged as the
first-max greedy winner from labeled experience. The trace, the
white-box state, the persistence (Z2 solved via the persisted
composite with build_count unchanged at 1), the revision (G2 regime:
base score 0, extension round winner ADD R0,R0 gain 2, adapt code 2,
old M retired to Mprev with sup=1, Z3 solved 40 to 82), and the clean
origin audit (no fact-relation literals, no solution shapes, no
validity-rule shape in glm_learner.zag) all point the same way: the
intermediate is created by the learner, not supplied.

SUPPLIED-vs-TREAT discrimination: SUPPLIED passes and TREAT passes,
but TREAT's creation trace (C-ROUND gain>0, created=1, no
SUPPLIED-INSTALL line) proves the researcher installer was not
involved. Had TREAT failed while SUPPLIED passed, the preregistered
verdict would have been L2; that did not happen.

Caveats (all preregistered): the validity rules are
builder-designed, not adversary-designed; one L2 form (relation
rebinding) and one intermediate form (generator program) are tested;
this build targets the 12 frozen bars and does not claim the full
12-criterion L3 bar. The adversarial-generality direction stays open,
as with FORAGE before RELAY.

## H2 implementation note

One driver bug was caught and fixed before the determinism runs:
H2's training-relation binding took the last relation seen for the
training subject (72) instead of the first (71). The fix matches the
preregistered generic binding (first relation seen, as in H1's
bind_param). The experiment's verdict did not depend on it (L1 still
failed, the rebound still discovered the sealed relation), but the
fix was made for design fidelity; the fixed binary is the one whose
3/3 digests are recorded.

## Digests

- h1_bin: 6f076073eb1fdb2728b55c790369588310349e7423692bdaf72c8aba5e764eba
- h2_bin: af7870cd5332a97ab1f2df0ed61674dd77c5b2417ccacf20849533b6b04dc995
- H1 runs 1-3: abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426 (identical)
- H2 runs 1-3: ee0bf4ba9f8acc289d549c590b96c1ca41269b1939cd39dd8ab09e6f84b3a022 (identical)

## Files (all under xdomain_grammar_l2m/)

PREREG.md (frozen), NAMECHECK.md, REPORT.md, glm_learner.zag
(shared generic intermediate machinery), gl2m_h1.zag, gl2m_h2.zag,
h1_full.zag, h2_full.zag (built concatenations), build.sh,
h1_bin, h2_bin, h1_compile.log, h2_compile.log, run_h1_1..3.log,
run_h2_1..3.log.

Constraints honored: pure Zag; zero Python; safebin mandatory;
no em/en dashes in loop documentation; paper untouched; nothing
pushed (commits local on tnn-native-lab); 0 modes/bridges/handlers.
