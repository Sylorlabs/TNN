#!/usr/bin/env python3
"""Generate FROZEN v2 RT1b corpora (qty surface syntax corrected to the
engine's 3-field form qty(thing,mode,value); unit rides inside the value
token, e.g. qty(w,exactly,1min)). v1 (4-field qty items) is superseded and
retained as *_v1_superseded.tsv for audit."""
import datetime

TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

RT_A = [
    # --- novel attack: silent i32 truncation of quantity values (expect AFFIRM = hit) ---
    ("A-001", "qty(w,exactly,0)", "qty(w,exactly,4294967296)", "NEUTRAL"),      # 2^32 -> 0
    ("A-002", "qty(w,at_most,0)", "qty(w,exactly,2147483648)", "NEUTRAL"),      # 2^31 -> -2^31, subset-affirm
    ("A-003", "qty(w,exactly,2147483647)", "qty(w,exactly,6442450943)", "NEUTRAL"),  # 2^32+2^31-1 -> 2^31-1
    ("A-004", "qty(w,exactly,0sec)", "qty(w,exactly,4294967296sec)", "NEUTRAL"),    # with unit suffix
    ("A-005", "qty(w,exactly,60,sec)", "qty(w,exactly,4294967356sec)", "NEUTRAL"),  # 2^32+60 sec -> 60 sec; claim is 3-field? no: fixed below
    ("A-006", "qty(w,exactly,5)", "qty(w,exactly,4294967301)", "NEUTRAL"),      # 2^32+5 -> 5
    ("A-007", "qty(w,exactly,7)", "qty(w,exactly,4294967303)", "NEUTRAL"),      # 2^32+7 -> 7
    ("A-008", "qty(t,at_most,0sec)", "qty(t,exactly,8589934592sec)", "NEUTRAL"),    # 2^33 -> 0, subset-affirm
    ("A-009", "qty(w,exactly,1min)", "qty(w,exactly,4294967356sec)", "NEUTRAL"),    # 2^32+60 sec == 60 sec == 1 min
    # --- classic fallacies / fix-hold verifies (expect no AFFIRM) ---
    ("A-010", "p(x)", "if(p(x),q(x));q(x)", "NEUTRAL"),          # affirming the consequent
    ("A-011", "cause(r(x),q(x))", "r(x);q(x)", "NEUTRAL"),       # correlation -> causation
    ("A-012", "innocent(x)", "not(guilty(x))", "NEUTRAL"),       # scope-shifted negation
    ("A-013", "p(x)", "maybe(p(x))", "NEUTRAL"),                 # hedged evidence over-affirmed
    ("A-014", "q(x)", "if(p(x),q(x))", "NEUTRAL"),               # conditional consequent as fact
    ("A-015", "q(x)", "cause(not(r(x)),q(x))", "NEUTRAL"),       # vacuous (negated) reason
    ("A-016", "q(x)", "cause(maybe(r(x)),q(x))", "NEUTRAL"),     # vacuous (hedged) reason
    ("A-017", "q(x)", "cause(if(a(x),b(x)),q(x))", "NEUTRAL"),   # vacuous (conditional) reason
    ("A-018", "qty(w,exactly,5)", "qty(w,range,33_to_22)", "NEUTRAL"),  # inverted range -> lit()
    ("A-019", "p(x)", "p(x) brightly", "NEUTRAL"),               # trailing tokens -> lit()
    ("A-020", "maybe(p(x))", "maybe(p(x))", "NEUTRAL"),          # hedged identity
    ("A-021", "maybe(q(x))", "cause(r(x),q(x))", "NEUTRAL"),     # hedged claim via cause
    ("A-022", "maybe(q(x))", "if(p(x),q(x));p(x)", "NEUTRAL"),   # hedged claim via MP
    ("A-023", "not(p(x))", "q(x)", "NEUTRAL"),                  # deny from absence
    ("A-024", "qty(w,exactly,7)", "qty(w,range,5,6)", "DENY"),   # range mismatch -> deny
    ("A-025", "p(y)", "cause(r(x),p(x))", "NEUTRAL"),            # wrong subject
    ("A-026", "cause(r(x),q(x))", "cause(s(x),cause(r(x),q(x)))", "NEUTRAL"),  # causal claim not affirmable via cause
    ("A-027", "all(d,p(x))", "some(d,p(x))", "NEUTRAL"),         # quantifier over-affirm
    ("A-028", "q(x)", "cause(r(x),q(y))", "NEUTRAL"),            # consequent mismatch
    ("A-029", "not(q(x))", "if(p(x),q(x));not(p(x))", "NEUTRAL"),  # denying the antecedent
    ("A-030", "p(x)", "not(not(q(x)))", "NEUTRAL"),              # double-neg of other prop
    ("A-031", "qty(w,exactly,60)", "qty(w,exactly,1min)", "NEUTRAL"),  # unit hygiene: count vs sec
    ("A-032", "q(x)", "not(cause(r(x),not(q(x))))", "NEUTRAL"),  # negated causal wrapper
    ("A-033", "before(a,b)", "before(b,a)", "DENY"),            # temporal reversal -> deny
    ("A-034", "before(a,b)", "before(a,c)", "NEUTRAL"),          # unrelated temporal
    ("A-035", "qty(w,at_least,10)", "qty(w,at_most,5)", "DENY"),  # disjoint -> deny
    ("A-036", "q(x)", "cause(maybe(p(x)),maybe(q(x)))", "NEUTRAL"),
    ("A-037", "maybe(q(x))", "cause(r(x),maybe(q(x)))", "NEUTRAL"),
    ("A-038", "all(d,not(p(x)))", "none(d,p(x))", "NEUTRAL"),    # equivalent, not contradictory
    ("A-039", "none(d,not(p(x)))", "all(d,not(p(x)))", "DENY"),  # both-negated ALL/NONE -> deny
    ("A-040", "q(x)", "if(q(x),p(x));p(x)", "NEUTRAL"),          # consequent confusion
    ("A-041", "p(x)", "maybe(not(p(x)))", "NEUTRAL"),
    ("A-042", "q(x)", "if(p(x),q(x));maybe(p(x))", "NEUTRAL"),   # hedged antecedent evidence
    ("A-043", "q(x)", "if(p(x),q(x));r(x)", "NEUTRAL"),          # wrong antecedent evidence
    ("A-044", "not(q(x))", "cause(r(x),q(x))", "NEUTRAL"),
    ("A-045", "all(d,q(x))", "all(d,p(x))", "NEUTRAL"),          # no syllogism rule
]

RT_B = [
    # --- novel attack: SOME/NONE both-negated quantifier gap (expect DENY, engine withholds) ---
    ("B-001", "none(d,not(p(x)))", "some(d,not(p(x)))", "DENY"),
    ("B-002", "some(d,not(p(x)))", "none(d,not(p(x)))", "DENY"),
    # --- valid denies (expect DENY) ---
    ("B-003", "p(x)", "not(p(x))", "DENY"),
    ("B-004", "not(p(x))", "p(x)", "DENY"),
    ("B-005", "q(x)", "cause(r(x),not(q(x)))", "DENY"),
    ("B-006", "cause(r(x),q(x))", "not(r(x))", "DENY"),
    ("B-007", "cause(r(x),q(x))", "cause(r(x),not(q(x)))", "DENY"),
    ("B-008", "all(d,p(x))", "some(d,not(p(x)))", "DENY"),
    ("B-009", "qty(w,at_most,5)", "qty(w,at_least,10)", "DENY"),
    ("B-010", "before(a,b)", "after(a,b)", "DENY"),
    ("B-011", "not(not(p(x)))", "not(p(x))", "DENY"),
    ("B-012", "all(d,not(p(x)))", "none(d,not(p(x)))", "DENY"),
    ("B-013", "qty(w,exactly,5)", "qty(w,exactly,6)", "DENY"),
    ("B-014", "qty(w,more_than,5)", "qty(w,exactly,5)", "DENY"),
    ("B-015", "cause(r(x),q(x))", "not(q(x))", "DENY"),
    ("B-016", "before(x,y)", "before(y,x)", "DENY"),
    ("B-017", "some(d,p(x))", "none(d,p(x))", "DENY"),
    ("B-018", "none(d,p(x))", "all(d,p(x))", "DENY"),
    ("B-019", "qty(w,at_least,5)", "qty(w,at_most,4)", "DENY"),
    ("B-020", "p(x,y)", "not(p(x,y))", "DENY"),
    # --- valid affirms (expect AFFIRM) ---
    ("B-021", "p(x)", "p(x)", "AFFIRM"),
    ("B-022", "Rains(Today)", "rains(today)", "AFFIRM"),
    ("B-023", "qty(w,exactly,five)", "qty(w,exactly,5)", "AFFIRM"),
    ("B-024", "qty(w,exactly,1min)", "qty(w,exactly,60sec)", "AFFIRM"),
    ("B-025", "p(x)", "not(not(p(x)))", "AFFIRM"),
    ("B-026", "q(x)", "cause(r(x),q(x))", "AFFIRM"),
    ("B-027", "q(x)", "cause(all(d,p(x)),q(x))", "AFFIRM"),
    ("B-028", "q(x)", "cause(before(a,b),q(x))", "AFFIRM"),
    ("B-029", "q(x)", "cause(qty(t,exactly,3),q(x))", "AFFIRM"),
    ("B-030", "q(x)", "if(p(x),q(x));p(x)", "AFFIRM"),
    ("B-031", "not(q(x))", "if(p(x),not(q(x)));p(x)", "AFFIRM"),
    ("B-032", "q(x)", "if(not(p(x)),q(x));not(p(x))", "AFFIRM"),
    ("B-033", "qty(w,at_least,4)", "qty(w,exactly,7)", "AFFIRM"),
    ("B-034", "qty(w,range,5,10)", "qty(w,exactly,7)", "AFFIRM"),
    ("B-035", "qty(w,at_least,1min)", "qty(w,exactly,90sec)", "AFFIRM"),
    ("B-036", "before(b,a)", "after(a,b)", "AFFIRM"),
    ("B-037", "all(d,p(x))", "all(d,p(x))", "AFFIRM"),
    ("B-038", "not(p(x))", "not(p(x))", "AFFIRM"),
    ("B-039", "cause(r(x),q(x))", "cause(r(x),q(x))", "AFFIRM"),
    ("B-040", "qty(w,range,22_to_33)", "qty(w,range,between_22_and_33)", "AFFIRM"),
    ("B-041", "p(x)", "not(not(not(not(p(x)))))", "AFFIRM"),
    ("B-042", "q(x)", "if(p(x),q(x));p(x);r(x)", "AFFIRM"),
    ("B-043", "qty(w,at_most,10)", "qty(w,less_than,10)", "AFFIRM"),
    ("B-044", "qty(w,more_than,4)", "qty(w,at_least,5)", "AFFIRM"),
    ("B-045", "q(x)", "cause(some(d,p(x)),q(x))", "AFFIRM"),
    ("B-046", "q(x)", ";".join([f"a{i}(x)" for i in range(1, 16)]) + ";q(x)", "AFFIRM"),  # 16 props
    ("B-047", "q(x)", "p(x);if(p(x),q(x))", "AFFIRM"),
    ("B-048", "qty(w,exactly,5)", "qty(w,range,5,5)", "AFFIRM"),
    ("B-049", "not(p(x))", "NOT(P(X))", "AFFIRM"),
]

RT_D = [
    ("D-001", "q(x)", "cause(not(r(x)),not(q(x)))", "vacuous-reason DENY: deny-side twin of the affirm-side vacuous-reason fix; r_cau_deny has no reason-substance check"),
    ("D-002", "q(x)", "cause(maybe(r(x)),not(q(x)))", "hedged-reason DENY"),
    ("D-003", "not(maybe(p(x)))", "not(maybe(p(x)))", "nested-hedge identity: hedge inertness is top-level only; engine AFFIRMs"),
    ("D-004", "c(x)", "cause(a(x),b(x));cause(b(x),c(x))", "second cause prop directly affirms c(x) via R-CAU-AFFIRM (no transitivity needed)"),
    ("D-005", "c(x)", "if(a(x),b(x));if(b(x),c(x));a(x)", "no MP chaining"),
    ("D-006", "q(x)", "cause(r(x),not(q(x)));r(x)", "prevented cause: deny fires even with reason asserted"),
    ("D-007", "all(d,p(x))", "none(d,not(p(x)))", "quantifier equivalence has no affirm rule"),
    ("D-008", "some(d,p(x))", "all(d,p(x))", "all->some entailment has no rule"),
    ("D-009", "q(x)", ";".join([f"a{i}(x)" for i in range(1, 17)]) + ";q(x)", "17 evidence props -> loud capacity refusal (tag 3)"),
    ("D-010", "qty(w,exactly,5)", "qty(w,at_least,5)", "at_least does not pin exactly"),
    ("D-011", "qty(w,at_least,5)", "qty(w,exactly,5)", "exactly(5) affirms at_least(5)"),
    ("D-012", "all(d,p(x))", "all(d,not(not(p(x))))", "double-neg collapse inside quantifier body"),
    ("D-013", "qty(w,exactly,5)", "qty(w,at_least,five)", "word-number at_least vs exactly"),
    ("D-014", "before(a,a)", "before(a,a)", "degenerate self-before identity"),
    ("D-015", "p(x)", "", "empty evidence"),
    ("D-016", "p(x))", "p(x)", "unparseable claim -> lit() fallback"),
    ("D-017", "lit(x)", "lit(x)", "lit-named atoms are ordinary atoms"),
    ("D-018", "qty(w,exactly,3sec)", "qty(w,exactly,3 sec)", "space before unit breaks suffix: 3sec vs 3 count"),
]

# A-005 self-check: claim must be 3-field. qty(w,exactly,60,sec) is 4-field -> fix to qty(w,exactly,60sec).
RT_A = [("A-005", "qty(w,exactly,60sec)", "qty(w,exactly,4294967356sec)", "NEUTRAL") if i == "A-005" else i for i in RT_A]

def write(path, items, with_oracle):
    with open(path, "w") as f:
        f.write(f"# RT1b frozen corpus v2 {path.split('/')[-1]} frozen={TS}  (lines starting with # are skipped by the engine)\n")
        for it in items:
            f.write("\t".join(it[:4] if with_oracle else it[:3] + ("INFO",)) + "\n")

import os
d = "/home/hatch/workspace/scratch-hellhole/redteam/rt1b"
for n in ["rt1b_A.tsv", "rt1b_B.tsv", "rt1b_D.tsv"]:
    os.rename(f"{d}/{n}", f"{d}/{n.replace('.tsv', '_v1_superseded.tsv')}")
write(f"{d}/rt1b_A.tsv", RT_A, True)
write(f"{d}/rt1b_B.tsv", RT_B, True)
write(f"{d}/rt1b_D.tsv", RT_D, False)
print(f"frozen={TS} A={len(RT_A)} B={len(RT_B)} D={len(RT_D)}")
# sanity: no 4-field qty surface props
import re
bad = []
for n, items in [("A", RT_A), ("B", RT_B), ("D", RT_D)]:
    for it in items:
        for fld in it[1:3]:
            for prop in fld.split(";"):
                if prop.startswith("qty(") and prop.count(",") != 2:
                    bad.append((it[0], prop))
print("malformed qty props:", bad if bad else "NONE")
