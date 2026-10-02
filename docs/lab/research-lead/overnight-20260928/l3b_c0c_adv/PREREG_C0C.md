# PREREG L3B-C0C: independent adversary on the residual-growth C0-C claim

Frozen: 2026-09-30. This prereg is committed ALONE before any attack
family file, attack source, build, run, or result exists. Pure Zag. No
Python at any stage. The adversary reports L3B-C0C-BOUNDARY-EXPOSED or
L3B-C0C-OPEN-FORM only. No SURVIVES claim and no L3 claim is made here.

## 1. Objective

Attack the C0-C (open structural form) question for the L3B
residual-growth mechanism (L3B-GROWTH-PASS, prereg c5be6dfb5,
implementation 2fb110ce7): can the generic constructors compose a form
outside the fixed analyzer vocabulary, or is the fixed vocabulary the
boundary? Two sealed families, each requiring a form outside the
vocabulary {EQ, MUL(q), ADD(d), SUB(d)} of rel_of and outside what
build_expr can assemble.

Assume the open-form claim is false. The job is the break, not the
defense.

## 2. Step 0 name-check (standing rules)

Four standing rules govern this lane. (1) Pure Zag only: every lane
artifact (prereg, families, attack source, harness, byte checks,
analysis) is Zag or POSIX shell; no Python is authored or executed at
any step, and episode data are frozen literals in the Zag source, never
provisioned by another language. (2) Fork testing: wave-level
enumeration stays with the parent coordinator; this lane runs the
pinned znc on branch tnn-native-lab with 3/3 byte-identical reruns as
its per-task evidence. (3) Pure-Zag red line scope: fixture
provisioning counts as loop work, so all episode lists live as Zag
literals. (4) Shell-only byte checks: em/en dash screening uses only
worker_snippets/check_no_dash.sh, never python3. I honor all four: this
prereg is committed alone before any attack file exists, the attack
harness is pure Zag plus POSIX shell, and no Python check is used for
anything. The prohibited paper is never touched. Owned pathspec only.

## 3. Mechanism under attack (committed, unmodified)

Base language B: ops 1=CONST, 2=VAR, 3=ADD, 4=MUL, 5=SUB; binterp_eval
is the frozen interpreter (INTERP-BEGIN/END). Generic constructors:
CREATE, CONNECT, SPLIT, MERGE. Residual analyzer rel_of over the last
F=3 failures, fixed order: EQ (lj==l0 on all 3); else MUL(q) (lj==q*l0,
q in 1..8, constant on all 3); else ADD(d) (lj-l0==d, d in 0..8,
constant); else SUB(d) (l0-lj==d, d in 1..8, constant); else NONE.
build_expr assembles only VAR(F0), MUL(VAR,CONST(k)), ADD(VAR,CONST(k)),
SUB(VAR,CONST(k)). Growth fires iff BOTH runs yield non-NONE and both
symbol rules hold; otherwise NO-GROWTH. Revision: retire with
reason=contradiction, rebuild; SPLIT-reuse only from the immediately
retired growth. A grown program is one static (root1, root2) pair per
version; there is no conditional dispatch between versions and no
version archive.

Known sharp fact: binterp_eval CAN evaluate MUL(VAR,VAR) (op 4 with two
VAR children). build_expr CANNOT assemble it, and rel_of cannot detect
a quadratic residual. Execution substrate open; construction substrate
closed. Family A2 is built on exactly this gap.

## 4. Family A2 (QUAD): n-squared-class residual

Law: content a^n b^(n^2), head "ab" (97,98), spec '#'.

- LEARN-A2 (phase 0 LEARN, allow_create=1, is_learn=1): n in
  [2,3,5,7,4,6]; tl1=n, tl2=n^2 = [4,9,25,49,16,36].
- HIDDEN-A2 (phase 1 HIDDEN, allow_create=0): n in [1,4,8];
  tl1=n, tl2=n^2 = [1,16,64].

Frozen walk-through. LEARN-A2: ep1 (n=2): bestL from empty training is
branch (1,1,1), c0=1 != 2, fail. ep2 (n=3): bestL=(2,2,4) (only branch
scoring on ep1, since n^2=4 <= 8 only for n=2), c0=2 != 3, fail. ep3
(n=5): c0=2 != 5, fail. consec=3: analyzer over eps 1-3. Run1:
(2,2),(3,3),(5,5) -> EQ. Run2: (2,4),(3,9),(5,25) -> MUL needs constant
q with 4=2q, 9=3q, 25=5q: q=2,3,5 not constant; ADD needs constant d
with 2,6,20: no; SUB negative: no -> NONE. Growth requires both runs
non-NONE: NO-GROWTH. consec reset. eps 4-6 (n=7,4,6): bestL=(2,2,4)
never fires (c0=2 not in {7,4,6}), 3 more fails; analyzer over eps 4-6:
run1 EQ; run2 (7,49),(4,16),(6,36): MUL q=7,4,6 not constant; ADD
42,12,30 not constant -> NONE -> NO-GROWTH.
HIDDEN-A2: bestL=(2,2,4) fires iff c0==n; n in {1,4,8}: never -> 0/3.

Frozen predictions A2:
- P-A2a: KX-A2 (max over the 512 canonical singles on E_m, m=1..12,
  with l1=m, l2=m^2) == 1. Justification: branch correct iff c0==m,
  c1==m, c2==m^2; m^2 <= 8 forces m in {1,2}; (1,1,1) hits m=1,
  (2,2,4) hits m=2; no branch covers two m.
- P-A2b: TRACE-CREATE count == 0 across family A2 (two NO-GROWTH
  events, one per 3-failure window).
- P-A2c: HIDDEN-A2 == 0/3.
- P-A2d: N2-INTERP == 25. Hand-build MUL(VAR(F0),VAR(F0)) with the
  generic constructors (CREATE VAR, CREATE MUL, two CONNECTs) and eval
  at f0=5. This is the crux exhibit: the interpreter evaluates n^2
  while growth cannot construct it.

A2 verdict rule: BOUNDARY-EXPOSED-A2 iff P-A2a, P-A2b, P-A2c, P-A2d all
hold. OPEN-FORM-A2 iff growth emits a TRACE-CREATE whose structure
scores HIDDEN-A2 >= 2/3 (growth composed the unforeseen form). Any
other outcome is reported verbatim as UNPREDICTED-A2 with the raw
numbers; it does not default to either label.

## 5. Family B2 (ALT): alternating law, revision churn

Laws: R1: content a^n b^(2n). R2: content a^n b^(n+4). Head "ab".

- LEARN-B2 (phase 0, allow_create=1, is_learn=1): n in [2,3,5,7,4,6],
  R1. Identical to the original inst1 LEARN-A: v1=(EQ,MUL(2)) created
  at ep3, eps 4-6 exact.
- HIDDEN-B2 (phase 1, allow_create=0): n in [1,4,8], R1 -> v1 3/3.
- SWITCH1 (phase 2 CONTRADICTION, allow_create=1): n in [3,6,5], R2.
  v1 predicts l2=2n: 6,12,10 vs 7,10,9: 3 fails. Analyzer over the 3:
  run1 (3,3),(6,6),(5,5) -> EQ; run2 (3,7),(6,10),(5,9) -> ADD(4)
  (7-3=4, 10-6=4, 9-5=4). Symbols bind. TRACE-RETIRE v1
  reason=contradiction superseded-by=2; TRACE-CREATE v2=(EQ,ADD(4))
  with run1 via SPLIT reuse.
- SWITCH2 (phase 2 CONTRADICTION, allow_create=1): n in [2,3,5], R1
  again. v2 predicts l2=n+4: 6,7,9 vs 4,6,10: 3 fails (n=4 excluded
  from the list because there v2 would be accidentally correct:
  4+4==2*4). Analyzer: run1 EQ; run2 (2,4),(3,6),(5,10) -> MUL(2).
  TRACE-RETIRE v2 superseded-by=3; TRACE-CREATE v3=(EQ,MUL(2)).
  v3's (rel,k) pair equals v1's, but the protocol SPLIT-reuses only
  from the immediately retired growth (v2), so v3 rebuilds run2 from
  scratch: v3 CALLS contain SPLIT (run1) and no MERGE (run2 via the
  MUL build path, not ADD/MERGE).
- FINAL-B2 (phase 3 FOLLOWUP, allow_create=0): n in [5,7], R2.
  v3 predicts 2n: 10,14 vs 9,11 -> 0/2.

Frozen predictions B2:
- P-B2a: TRACE-CREATE count == 3, TRACE-RETIRE count == 2.
- P-B2b: v1 rels == (EQ,MUL(2)), v2 rels == (EQ,ADD(4)),
  v3 rels == (EQ,MUL(2)); version counter == 3 at end.
- P-B2c: HIDDEN-B2 == 3/3, SWITCH1+SWITCH2 correct == 0/6,
  FINAL-B2 == 0/2.
- P-B2d: v3's CALLS line contains SPLIT( and does not contain MERGE(.

B2 verdict rule: BOUNDARY-EXPOSED-B2 iff P-B2a through P-B2d all hold:
the mechanism oscillates v1(R1) -> v2(R2) -> v3(R1), ends wrong on
FINAL, keeps no version memory (v3 rebuilds v1's form from scratch),
and has no conditional form to represent "R1 on some episodes, R2 on
others". OPEN-FORM-B2 iff a single grown version scores both the R1
and R2 blocks correctly, or growth emits a conditional/versioned
structure. Any other outcome is reported verbatim as UNPREDICTED-B2.

## 6. Overall verdict

L3B-C0C-BOUNDARY-EXPOSED iff BOUNDARY-EXPOSED-A2 and
BOUNDARY-EXPOSED-B2. L3B-C0C-OPEN-FORM iff OPEN-FORM-A2 or
OPEN-FORM-B2. Otherwise the report carries the UNPREDICTED label with
full raw numbers and no verdict upgrade.

Interpretation note (frozen): BOUNDARY-EXPOSED means the fixed
analyzer vocabulary and the static single-program growth form are the
C0-C boundary. It does not impugn the C0-A result (semantics still
live in the pre-existing interpreter) and it does not claim the
mechanism is useless; it maps exactly where open-endedness stops.

## 7. Attack protocol (frozen)

- l3b_attack.zag is built AFTER this prereg commits: protocol lines
  (everything before `fn main()` in the committed l3b.zag at
  2fb110ce7) copied VERBATIM; only main() is replaced with the attack
  driver (KX-A2 check, family A2, family B2, N2-INTERP check, summary
  lines). Byte-identity of the protocol region is proven by shell
  diff/cmp and committed as DIFF_PROOF.txt. The committed mechanism is
  never modified.
- No randomness anywhere: all episode lists are frozen literals in
  this prereg. FAMILIES.md (verbatim family specs) is committed after
  the prereg with its sha256 recorded in the result doc.
- Build with the pinned in-repo znc
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1); binary in /tmp only,
  never staged. 3 runs, byte-compared (shell cmp).
- Shell harness run_adv.sh evaluates the frozen bars from program
  summary lines plus grep counts of TRACE-CREATE / TRACE-RETIRE /
  NO-GROWTH / CALLS lines. Exit 0 iff the reported verdict matches the
  frozen verdict rules.

## 8. Kill bars

- K1: this prereg committed alone before any attack family file,
  attack source, build, or run exists. Verified with
  `git merge-base --is-ancestor <prereg> <impl>`. Family spec sha256
  recorded after prereg, before implementation.
- K2: both sealed families executed 3/3 byte-identical, per-family
  verdicts (BOUNDARY-EXPOSED / OPEN-FORM / UNPREDICTED) against the
  frozen predictions P-A2a..d and P-B2a..d.
- K3: pure Zag, zero Python at every step; check_no_dash.sh clean on
  all lane files; protocol region of l3b_attack.zag byte-identical to
  committed l3b.zag (diff proof committed); u8-backed cells only,
  never `as *i32` slices in functions (toolchain lesson).

## 9. Pre-registered anti-objections

- "The families are designed to fail": they are designed to require a
  form outside the frozen vocabulary, which is exactly what C0-C
  demands (multiple unforeseen forms). The frozen predictions state
  what honest failure looks like (NO-GROWTH abstention; churn with
  declared signatures), and OPEN-FORM states what success would look
  like. A mechanism that is genuinely open should surprise the
  adversary on at least the N2-INTERP-adjacent construction.
- "n=4 excluded from SWITCH2 is cherry-picking": it is disclosed and
  justified (there v2 is accidentally correct, which would break the
  3-consecutive-failure trigger the churn demonstration needs). The
  exclusion is frozen here, before any run.
- "Family B2 reuses the builder's own R1/R2 laws": deliberate. The
  attack is on the FORM (static single program vs conditional), not on
  the relations. Reusing the builder's own relations removes the
  confound that the relations themselves were too hard.
