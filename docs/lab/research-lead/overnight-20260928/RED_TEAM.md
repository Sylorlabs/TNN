# RED TEAM -- ATTACK ON THIS SESSION

Lane `ownership`. Adversarial review of every load-bearing claim made in
`FINAL_REPORT_ALL_PHASES.md`, plus mutation testing of the two
instruments the session produced.

The default posture here is **hostile**. A claim that survives this
document should be believed; a claim that does not should be
withdrawn or narrowed.

---

## PART 1 -- MECHANICAL VERIFICATION

### RT-A: reproducibility from committed source -- PASS

Deleted the binary, recompiled `b6.zag` from the committed source,
ran 3x:

```
7129e4bf89448642b396e7267ae062a48d6f95a9bd2800c2454130253c0aa93e  x3
report claims:
7129e4bf89448642b396e7267ae062a48d6f95a9bd2800c2454130253c0aa93e
```

**PASS.** The committed artifact reproduces its reported result. The
same check was run for `noisy`, `borrow`, `finder7`, `xform8`,
`selforg9`, `lifetime15` against their recorded shas: **all match.**

### RT-B: lint sweep -- one finding against my own code

Swept both lints across every `.zag` this session produced.
`tnn_loop_lint`: CLEAN. `tnn_bars_lint`: one violation, in an
*inherited* file (`spec_noisy_rates/nr_full.zag`, a verdict-named
counter assigned only a bare literal) and one note against my own
`xform8/f8.zag` for a hardcoded `BAR B11_named_modes=0`.

The inherited hit is a demonstration that the lint finds real
defects in code it did not write. **My own hardcoded bar is fixed.**

### RT-C: mutation test of the instruments -- TWO DEFECTS FOUND

The instruments are the session's only durable artifacts, so they
get attacked hardest. Three fixtures:

| fixture | expected | actual |
|---|---|---|
| `ok=1` bare literal | VIOLATE | **CLEAN -- false negative** |
| `ok=0` bare literal | VIOLATE | **CLEAN -- false negative** |
| missing loop increment | VIOLATE | VIOLATE (correct) |
| `ok` derived from `i>=0` | PASS | **VIOLATE -- false positive** |

**Defect 1 (false negative, FIXED).** The bars lint's identifier regex
required at least one character *before* the verdict word, so a
variable named exactly `ok`, `valid` or `pass` was invisible. The
single most obvious fake-bar spelling was the one spelling it could
not see. Regex widened; fixtures M1/M2 now correctly fire.

**Defect 2 (false positive, OPEN).** The lint is line-based, so a bar
derived from a comparison on an *earlier* line is flagged. `M4` is a
genuinely derived bar and it fails.

**Consequence for the governance claim:** `tnn_bars_lint.sh` is a
**prompt for human review, not a proof.** It detects two syntactic
shapes of hardcoded bar and nothing else. It cannot detect a bar that
is computed from a *wrong formula* -- which is the more dangerous
failure mode, and which actually occurred (the PHASE 8 sign
inversion). Neither lint is evidence of correctness.

---

## PART 2 -- ATTACKS ON THE CLAIMS

### A1. "COUNTING BEATS FIVE LEARNER MECHANISMS" -- STRONGEST ATTACK, PARTLY VALID

**The claim:** five independent mechanisms (contracts, generated
shapes, induced procedures, learned affinities, lifetime affinity)
all matched or lost to `argmax frequency`.

**The attack:** every one of those five tests ran in a substrate with
**at most five candidate structures** and a *flat candidate set*. With
n <= 5, `argmax frequency` is close to optimal: it is a lookup over a
handful of counts, and no amount of cleverness beats a lookup over a
handful of counts. The regularity may be a property of my substrate
size, not a law about learning.

Corroborating evidence for the attack: the *one* mechanism that beat
counting (query-scoped credit, C1681) also ran on 3 structures and 2
queries. If size were the whole story, that result should also have
failed. It did not. So size is not obviously the explanation -- but
neither is it excluded, and I never ran the decisive case.

**What would settle it:** one world with 30+ structures where the
frequencies are deliberately diluted so that counting is *unable* to
rank, and a learned mechanism is not. PHASE 15 tried to build this at
5 structures and the world collapsed again.

**Verdict: NARROW.** The claim survives as "in five small worlds,
counting was not beaten." It does **not** survive as a general law.

### A2. "TYPES ARE INFORMATION-THEORETICALLY INSUFFICIENT" -- OVERSTATED

**The claim** (KILL-6): routing from types is information-
theoretically insufficient; routing from values is memorisation.

**The attack:** this was demonstrated on **two queries in one world**
that happened to share a signature. That shows those two instances
were indistinguishable *by that feature set*. It does not show that
no richer type-like abstraction exists. The phrase
"information-theoretically insufficient" claims more than n=2 can
support. Also untested: a **hybrid** -- type plus a small number of
facts-derived features. PHASE 9's affinity arm used such features and
lost, but it lost in a collapsed world, so it is not a clean test of
the hypothesis.

**Verdict: WITHDRAW the strong phrasing.** Correct statement:

> The derived signatures available in this substrate collide on the
> instances tested. A richer abstraction between type and value was
> not constructed, and nothing here shows it cannot exist.

The *structural* observation survives intact and is the valuable
part: with only types available, the researcher reaches for
value-specific rules, and that is what the bridges are.

### A3. "BR-4 SOLVED" -- TOO STRONG

**The claim:** retaining the aggregation in the MAP replaces the
count bridge (BASE 1/3, TREAT 3/3).

**Three attacks:**

1. `{COUNT, SUM, MAX}` is a **finite label vocabulary**. The audit
   itself flagged this as a near-miss to the menu pattern H16v3
   exists to kill. A general aggregation descriptor was never tested.
2. **One instance set.** BASE's single success was luck (COUNT on
   three facts). A different instance set gives BASE anywhere from
   0/3 to 3/3. The 1/3-vs-3/3 gap is not robustly measured.
3. The mechanism is a **lookup on a label**, which is precisely the
   "routing from VALUES" shape that A2 criticises. I applied a
   standard to KILL-6 that I did not apply to my own BR-4 treatment.

**Verdict: NARROW** to "the count-specific bridge is unnecessary for
three aggregations, given a MAP that records which one it learned."

### A4. THE DEEPEST ATTACK: NONE OF THIS MEASURED TNN

Every experiment in Phases 2-9 and 15 ran on a **declared minimal
reproduction** of an audited architectural shape. The canonical
learner was **never executed once**. It was read.

Consequences:

* The bridge *classifications* (BR-1..BR-4) rest on code reading.
  In particular "active on witnessed paths" means *I read the call
  site*, not that I traced an execution.
* Every capability number measures my reproductions.
* No claim in this session transfers to TNN's actual behaviour.

This was disclosed in every report, which is why the reports say
"L3 = 0" and "no architecture changed." But the final report's
section 7 ("method ownership progress") reads as a statement about
TNN. It is a statement about reproductions of TNN.

**Verdict: the disclosure is adequate but the framing in the summary
tables should be read as "in the reproduction," not "in TNN."**

### A5. PROCESS CLAIMS ARE SURVIVORSHIP-BIASED

**The claim:** "theory disagreed with measurement, and the
disagreement found a real bug -- every single time."

**The attack:** this counts only the cases where it *did*. I never
logged the cases where theory agreed and I found nothing by that
route, so no denominator exists. The phrasing is unfalsifiable as
stated and should not have been used.

Similarly "18 defects, all mine" has no independent audit. Some are
double-counted (the loop-increment defect appeared twice and is
counted twice, correctly, but it is one *kind*), and several are
trivial (a slice assigned to an i32, caught by the compiler).

**Verdict: NARROW.** The defensible claim is "theory-versus-
measurement caught every bug it was pointed at; the denominator is
unrecorded."

### A6. RETRACTIONS ARE CHEAP, AND NOT ALL BARS COULD FAIL

**The claim:** the standing detector was applied to my own work and
retracted two results.

**The attack, and it has teeth:** the H16v4 positive control fired on
a **substrate bug** (`exec` step limit), not on the hypothesis under
test. And several prereg bars were structurally incapable of
falsifying their hypothesis:

* `B2_exhaustive_solves_all` -- a solvability check, not a claim.
* `B10_named_modes=0` -- hardcoded, therefore always true.
* `B7_misleading_worse_than_F` -- compared *proposals* between arms
  with different success rates, so it could not mean what it said.
  I recorded this as a bar-design defect but left the bar in place.

So "the preregistration did its job" is true for some bars and
false for others, and I did not distinguish them systematically.

**Verdict: PARTLY VALID.** The two retractions stand on their merits
(the fixed heuristics really do tie the learner). The *governance*
framing overstates how many bars were load-bearing.

### A7. THE LIFETIME LANE'S VERDICT IS WEAKER THAN REPORTED

PHASE 15 concluded "the lifetime programme is premature" on the
strength of `AFFINITY 1 of 2`. But one of the two held-out queries was
**unsolvable** (a structure learned as identity), and the training
pairs were degenerate. So the measurement was `1 of 2` on a world
where one query could not be posed.

The report says this. But the headline verdict -- that five
mechanisms have now failed -- rests partly on a lane that did not
produce a valid measurement. **A1 and the PHASE 15 result should be
counted as four mechanisms and one compromised lane, not five.**

---

## PART 3 -- WHAT SURVIVES

After all of the above, these stand:

| claim | status |
|---|---|
| Name-based bridge auditing is invalid here; all 4 bridges are implicit | **SURVIVES** -- read directly off the source |
| The bridges exist and 3 of 4 are in the canonical learner | **SURVIVES** (code-read, not executed) |
| Routing from types alone collides on the instances tested | **SURVIVES**, phrasing narrowed |
| With only types available, the researcher reaches for value-specific rules | **SURVIVES** -- the most useful structural claim |
| Learned contracts are necessary but NOT sufficient | **SURVIVES** -- the counterexample is concrete and shared across arms |
| A fixed heuristic matched or beat 4 learner mechanisms in small worlds | **SURVIVES**, scope narrowed from 5 to 4 |
| Additive support over chain elements is unsound (self-composition) | **SURVIVES** -- mechanism identified from source |
| Proposal learning is untestable in flat-gradient parity worlds | **SURVIVES** -- algebraic, not empirical |
| BR-4's count bridge is unnecessary given recorded provenance | **SURVIVES**, narrowed to 3 aggregations |
| L3 = 0, no architecture changed, 0 bridges deleted | **SURVIVES** -- directly verifiable |
| "theory found a bug every time" | **WITHDRAWN** -- no denominator |
| "types are information-theoretically insufficient" | **WITHDRAWN** -- n=2 |
| "five mechanisms lost to counting" | **NARROWED** to four, plus one compromised lane |

## PART 4 -- THE ATTACK I COULD NOT MOUNT

The most damaging objection to this entire session is one I have no
answer to:

> Every experiment was built by the same author who also wrote the
> preregistrations, chose the worlds, and scored the results. The
> defects were all caught by that same author. There is no
> independent check anywhere in this work.

I mitigated what I could -- fixed controls, closed forms, printed
learned objects, lint, mutation testing of the lints -- but every
mitigation is mine. The audit of `l3_rx` is *pending an independent
red team*, and that lane has been waiting for exactly this.

The concrete recommendation is therefore not another experiment. It
is:

> **Have someone else reproduce one number from this session from the
> committed source, without reading my reports.** I have verified
> mine are reproducible; I have not verified that they are
> reproducible by someone who does not already believe them.

`borrow/borrow6/b6.zag` is the best candidate: it is self-contained,
it builds in one command, its result is a single table, and its
negative conclusion is the one most worth attacking.