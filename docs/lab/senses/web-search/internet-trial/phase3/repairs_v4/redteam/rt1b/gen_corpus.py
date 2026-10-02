#!/usr/bin/env python3
"""Generate frozen RT1b attack corpora. Run once BEFORE any build/run."""
import datetime

TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Each item: (id, claim, evidence, oracle)
RT_A = [
    # --- novel attack: i32 truncation in quantity values (expect AFFIRM = hit) ---
    ("A-001", "qty(w,exactly,0,count)", "qty(w,exactly,4294967296,count)", "NEUTRAL"),   # 2^32 -> 0
    ("A-002", "qty(w,exactly,-2147483648,count)", "qty(w,exactly,2147483648,count)", "NEUTRAL"),  # 2^31 -> -2^31
    ("A-003", "qty(w,exactly,2147483647,count)", "qty(w,exactly,6442450943,count)", "NEUTRAL"),   # 2^32+2^31-1 -> 2^31-1
    ("A-004", "qty(w,exactly,0sec)", "qty(w,exactly,4294967296sec)", "NEUTRAL"),  # with unit suffix
    ("A-005", "qty(w,at_least,-2147483648,count)", "qty(w,exactly,2147483648,count)", "NEUTRAL"),  # subset affirm on wrapped value
    ("A-006", "qty(w,exactly,5,count)", "qty(w,exactly,4294967301,count)", "NEUTRAL"),  # 2^32+5 -> 5
    ("A-007", "qty(w,exactly,7,count)", "qty(w,exactly,4294967303,count)", "NEUTRAL"),  # 2^32+7 -> 7
    ("A-008", "qty(t,at_most,0sec)", "qty(t,exactly,8589934592sec)", "NEUTRAL"),  # 2^33 -> 0, subset affirm
    # --- classic fallacies / fix-hold verifies (expect no AFFIRM) ---
    ("A-009", "p(x)", "if(p(x),q(x));q(x)", "NEUTRAL"),          # affirming the consequent
    ("A-010", "cause(r(x),q(x))", "r(x);q(x)", "NEUTRAL"),       # correlation -> causation
    ("A-011", "innocent(x)", "not(guilty(x))", "NEUTRAL"),       # scope-shifted negation
    ("A-012", "p(x)", "maybe(p(x))", "NEUTRAL"),                 # hedged evidence over-affirmed
    ("A-013", "q(x)", "if(p(x),q(x))", "NEUTRAL"),               # conditional consequent as fact
    ("A-014", "q(x)", "cause(not(r(x)),q(x))", "NEUTRAL"),       # vacuous (negated) reason
    ("A-015", "q(x)", "cause(maybe(r(x)),q(x))", "NEUTRAL"),     # vacuous (hedged) reason
    ("A-016", "q(x)", "cause(if(a(x),b(x)),q(x))", "NEUTRAL"),   # vacuous (conditional) reason
    ("A-017", "qty(w,exactly,5,count)", "qty(w,range,33_to_22,count)", "NEUTRAL"),  # inverted range
    ("A-018", "p(x)", "p(x) brightly", "NEUTRAL"),               # trailing tokens
    ("A-019", "maybe(p(x))", "maybe(p(x))", "NEUTRAL"),          # hedged identity
    ("A-020", "maybe(q(x))", "cause(r(x),q(x))", "NEUTRAL"),     # hedged claim via cause
    ("A-021", "maybe(q(x))", "if(p(x),q(x));p(x)", "NEUTRAL"),   # hedged claim via MP
    ("A-022", "not(p(x))", "q(x)", "NEUTRAL"),                  # deny from absence
    ("A-023", "qty(w,exactly,7,count)", "qty(w,range,5,6,count)", "DENY"),  # range mismatch -> deny
    ("A-024", "p(y)", "cause(r(x),p(x))", "NEUTRAL"),            # wrong subject
    ("A-025", "cause(r(x),q(x))", "cause(s(x),cause(r(x),q(x)))", "NEUTRAL"),  # causal claim not affirmable via cause
    ("A-026", "all(d,p(x))", "some(d,p(x))", "NEUTRAL"),         # quantifier over-affirm
    ("A-027", "q(x)", "cause(r(x),q(y))", "NEUTRAL"),            # consequent mismatch
    ("A-028", "not(q(x))", "if(p(x),q(x));not(p(x))", "NEUTRAL"),  # denying the antecedent
    ("A-029", "p(x)", "not(not(q(x)))", "NEUTRAL"),              # double-neg of other prop
    ("A-030", "qty(w,exactly,60,count)", "qty(w,exactly,1,min)", "NEUTRAL"),  # unit hygiene
    ("A-031", "q(x)", "not(cause(r(x),not(q(x))))", "NEUTRAL"),  # negated causal wrapper
    ("A-032", "before(a,b)", "before(b,a)", "DENY"),            # temporal reversal -> deny
    ("A-033", "before(a,b)", "before(a,c)", "NEUTRAL"),          # unrelated temporal
    ("A-034", "qty(w,at_least,10,count)", "qty(w,at_most,5,count)", "DENY"),  # disjoint -> deny
    ("A-035", "q(x)", "cause(maybe(p(x)),maybe(q(x)))", "NEUTRAL"),
    ("A-036", "maybe(q(x))", "cause(r(x),maybe(q(x)))", "NEUTRAL"),
    ("A-037", "all(d,not(p(x)))", "none(d,p(x))", "NEUTRAL"),    # equivalent, not contradictory
    ("A-038", "none(d,not(p(x)))", "all(d,not(p(x)))", "DENY"),  # both-negated ALL/NONE -> deny
    ("A-039", "q(x)", "if(q(x),p(x));p(x)", "NEUTRAL"),          # consequent confusion
    ("A-040", "p(x)", "maybe(not(p(x)))", "NEUTRAL"),
    ("A-041", "q(x)", "if(p(x),q(x));maybe(p(x))", "NEUTRAL"),   # hedged antecedent evidence
    ("A-042", "q(x)", "if(p(x),q(x));r(x)", "NEUTRAL"),          # wrong antecedent evidence
    ("A-043", "not(q(x))", "cause(r(x),q(x))", "NEUTRAL"),
    ("A-044", "all(d,q(x))", "all(d,p(x))", "NEUTRAL"),          # no syllogism rule
    ("A-045", "q(x)", "cause(r(x),not(q(x)))", "NEUTRAL"),       # vacuous-reason deny twin (noted, not affirm-direction)
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
    ("B-009", "qty(w,at_most,5,count)", "qty(w,at_least,10,count)", "DENY"),
    ("B-010", "before(a,b)", "after(a,b)", "DENY"),
    ("B-011", "not(not(p(x)))", "not(p(x))", "DENY"),
    ("B-012", "all(d,not(p(x)))", "none(d,not(p(x)))", "DENY"),
    ("B-013", "qty(w,exactly,5,count)", "qty(w,exactly,6,count)", "DENY"),
    ("B-014", "qty(w,more_than,5,count)", "qty(w,exactly,5,count)", "DENY"),
    ("B-015", "cause(r(x),q(x))", "not(q(x))", "DENY"),
    ("B-016", "before(x,y)", "before(y,x)", "DENY"),
    ("B-017", "some(d,p(x))", "none(d,p(x))", "DENY"),
    ("B-018", "none(d,p(x))", "all(d,p(x))", "DENY"),
    ("B-019", "qty(w,at_least,5,count)", "qty(w,at_most,4,count)", "DENY"),
    ("B-020", "p(x,y)", "not(p(x,y))", "DENY"),
    # --- valid affirms (expect AFFIRM) ---
    ("B-021", "p(x)", "p(x)", "AFFIRM"),
    ("B-022", "Rains(Today)", "rains(today)", "AFFIRM"),
    ("B-023", "qty(w,exactly,five,count)", "qty(w,exactly,5,count)", "AFFIRM"),
    ("B-024", "qty(w,exactly,1,min)", "qty(w,exactly,60,sec)", "AFFIRM"),
    ("B-025", "p(x)", "not(not(p(x)))", "AFFIRM"),
    ("B-026", "q(x)", "cause(r(x),q(x))", "AFFIRM"),
    ("B-027", "q(x)", "cause(all(d,p(x)),q(x))", "AFFIRM"),
    ("B-028", "q(x)", "cause(before(a,b),q(x))", "AFFIRM"),
    ("B-029", "q(x)", "cause(qty(t,exactly,3,count),q(x))", "AFFIRM"),
    ("B-030", "q(x)", "if(p(x),q(x));p(x)", "AFFIRM"),
    ("B-031", "not(q(x))", "if(p(x),not(q(x)));p(x)", "AFFIRM"),
    ("B-032", "q(x)", "if(not(p(x)),q(x));not(p(x))", "AFFIRM"),
    ("B-033", "qty(w,at_least,4,count)", "qty(w,exactly,7,count)", "AFFIRM"),
    ("B-034", "qty(w,range,5,10,count)", "qty(w,exactly,7,count)", "AFFIRM"),
    ("B-035", "qty(w,at_least,1,min)", "qty(w,exactly,90,sec)", "AFFIRM"),
    ("B-036", "before(b,a)", "after(a,b)", "AFFIRM"),
    ("B-037", "all(d,p(x))", "all(d,p(x))", "AFFIRM"),
    ("B-038", "not(p(x))", "not(p(x))", "AFFIRM"),
    ("B-039", "cause(r(x),q(x))", "cause(r(x),q(x))", "AFFIRM"),
    ("B-040", "qty(w,range,22_to_33,count)", "qty(w,range,between_22_and_33,count)", "AFFIRM"),
    ("B-041", "p(x)", "not(not(not(not(p(x)))))", "AFFIRM"),
    ("B-042", "q(x)", "if(p(x),q(x));p(x);r(x)", "AFFIRM"),
    ("B-043", "qty(w,at_most,10,count)", "qty(w,less_than,10,count)", "AFFIRM"),
    ("B-044", "qty(w,more_than,4,count)", "qty(w,at_least,5,count)", "AFFIRM"),
    ("B-045", "q(x)", "cause(some(d,p(x)),q(x))", "AFFIRM"),
    ("B-046", "q(x)", ";".join([f"a{i}(x)" for i in range(1, 16)]) + ";q(x)", "AFFIRM"),  # 16 props, last affirms
    ("B-047", "q(x)", "p(x);if(p(x),q(x))", "AFFIRM"),
    ("B-048", "qty(w,exactly,5,count)", "qty(w,range,5,5,count)", "AFFIRM"),
    ("B-049", "not(p(x))", "NOT(P(X))", "AFFIRM"),
]

RT_D = [
    # (id, claim, evidence, note) - informational probes, no kill bar
    ("D-001", "q(x)", "cause(not(r(x)),not(q(x)))", "vacuous-reason DENY: deny-side twin of the RT1-A1 affirm fix; engine has no reason-substance check in r_cau_deny"),
    ("D-002", "q(x)", "cause(maybe(r(x)),not(q(x)))", "hedged-reason DENY"),
    ("D-003", "not(maybe(p(x)))", "not(maybe(p(x)))", "nested-hedge identity: hedge inertness is top-level only; engine AFFIRMs"),
    ("D-004", "c(x)", "cause(a(x),b(x));cause(b(x),c(x))", "no causal transitivity rule"),
    ("D-005", "c(x)", "if(a(x),b(x));if(b(x),c(x));a(x)", "no MP chaining"),
    ("D-006", "q(x)", "cause(r(x),not(q(x)));r(x)", "prevented cause: deny fires even with reason asserted"),
    ("D-007", "all(d,p(x))", "none(d,not(p(x)))", "quantifier equivalence has no affirm rule"),
    ("D-008", "some(d,p(x))", "all(d,p(x))", "all->some entailment has no rule"),
    ("D-009", "q(x)", ";".join([f"a{i}(x)" for i in range(1, 17)]) + ";q(x)", "17 evidence props -> loud capacity refusal (tag 3)"),
    ("D-010", "qty(w,exactly,5,count)", "qty(w,at_least,5,count)", "at_least does not pin exactly"),
    ("D-011", "qty(w,at_least,5,count)", "qty(w,exactly,5,count)", "exactly(5) affirms at_least(5)"),
    ("D-012", "all(d,p(x))", "all(d,not(not(p(x))))", "double-neg collapse inside quantifier body"),
    ("D-013", "qty(w,exactly,5,count)", "qty(w,at_least,five,count)", "word-number at_least vs exactly"),
    ("D-014", "before(a,a)", "before(a,a)", "degenerate self-before identity"),
    ("D-015", "p(x)", "", "empty evidence"),
    ("D-016", "p(x))", "p(x)", "unparseable claim -> lit() fallback"),
    ("D-017", "lit(x)", "lit(x)", "lit-named atoms are ordinary atoms"),
    ("D-018", "qty(w,exactly,3,sec)", "qty(w,exactly,3sec)", "digit+suffix spacing canonicalization"),
]

def write(path, items, with_oracle):
    with open(path, "w") as f:
        f.write(f"# RT1b frozen corpus {path.split('/')[-1]} frozen={TS}  (lines starting with # are skipped by the engine)\n")
        for it in items:
            if with_oracle:
                f.write("\t".join(it[:4]) + "\n")
            else:
                f.write("\t".join(it[:3]) + "\t" + "INFO" + "\n")

write("/home/hatch/workspace/scratch-hellhole/redteam/rt1b/rt1b_A.tsv", RT_A, True)
write("/home/hatch/workspace/scratch-hellhole/redteam/rt1b/rt1b_B.tsv", RT_B, True)
write("/home/hatch/workspace/scratch-hellhole/redteam/rt1b/rt1b_D.tsv", RT_D, False)
print(f"frozen={TS} A={len(RT_A)} B={len(RT_B)} D={len(RT_D)}")
