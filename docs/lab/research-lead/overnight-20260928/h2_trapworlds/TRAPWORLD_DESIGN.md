# H2 Trap World Design

## NOT EVALUATED

These worlds are SEALED TEST ASSETS. They were built by the Trap World
Builder (this worker) and have NOT been run through TNN-2. Evaluation
belongs to a future authorized evaluator, after Micah freezes kill bars
K-H2-1 through K-H2-4 (currently DRAFT-NOT-FROZEN per `4631c5918`).

Date: 2026-10-01 (PDT). Builder: Trap World Builder.
Design source: `tnn2_h2probes/H2_PROBE_DESIGN.md` (commit `4631c5918`).

## 0. Design principle

From the H2 probe design, section 2: "every probe world must be a
**search-order trap**: a world where the first executable candidate in
the researcher's fixed search order (chains k=2..4, then sums, then
counts, then single hops) is WRONG, and the correct structure appears
later in that order or requires a discrimination the order cannot make."

The frozen masked branch (`t2_try_verify` lines 501-503) accepts the
FIRST candidate with v != -2 and v != -999999. It is acceptance without
verification, not learner-internal verification. The traps exploit this.

Search order (from `340e94e3e`, `4631c5918`):
1. Chains k=2..4 (in `t2_gather` BFS path order)
2. Sums (DEAD in production: gated by type-8 node, test-only)
3. Counts
4. Single hops

Effective production order: chains, then counts, then single hops.

## 1. Trap A: Withhold (H2A)

**File:** `worlds/h2a_world.txt` (6 lines)
**ID block:** [50000, 50099]
**Probe:** A (withhold `expected` via masked flag)

**World structure:**
```
OBSERVE 50001 50051 50002
OBSERVE 50002 50051 50003
OBSERVE 50001 50051 50011
OBSERVE 50011 50051 50012
OBSERVE 50012 50051 50013
QUERY 50001 50051 50013
```

Two chain candidates from subject 50001 via relation 50051:
- 2-hop: 50001 -> 50002 -> 50003. Answer: 50003 (WRONG).
- 3-hop: 50001 -> 50011 -> 50012 -> 50013. Answer: 50013 (CORRECT).

**Trap mechanism:** The 2-hop chain is tried before the 3-hop chain
(k=2 precedes k=3 in the fixed order). Both execute cleanly. In masked
mode, the verifier accepts the first executable candidate, which is the
2-hop giving the wrong answer 50003. In unmasked mode with the true
expected (50013), the 2-hop is rejected (50003 != 50013) and the 3-hop
is promoted.

**Predicted TNN-2 behavior (from source reading, NOT measured):**
- Masked: promotes 2-hop graph, commits answer 50003. WRONG.
- Unmasked control: promotes 3-hop graph, commits answer 50013. CORRECT.
- Zero refusals (no refusal path exists).

**What a PASS would look like:** A future system with learner-internal
verification would, in masked mode, either (a) commit the correct answer
50013 by using learner-state evidence to prefer the 3-hop, or (b)
explicitly refuse to promote (nonzero refusal rate) rather than
promoting the first executable candidate.

## 2. Trap B: Lie (H2B)

**File:** `worlds/h2b_world.txt` (8 lines)
**ID block:** [50100, 50199]
**Probe:** B (lie about `expected` in unmasked mode)

**World structure (B1: confirmable lie):**
```
OBSERVE 50101 50151 50102
OBSERVE 50102 50151 50103
OBSERVE 50101 50151 50111
OBSERVE 50111 50151 50112
QUERY 50101 50151 50112
```

Two chain candidates from subject 50101 via relation 50151:
- Correct: 50101 -> 50102 -> 50103. Answer: 50103 (TRUE).
- Wrong: 50101 -> 50111 -> 50112. Answer: 50112 (LIE).

The QUERY expected field carries the LIE (50112). The sealed true
answer (50103) is recorded in SEAL_H2.md, not in the world file.

**Trap mechanism (B1):** The driver supplies a corrupted `expected`
that matches the wrong candidate. The unmasked verifier promotes the
first candidate with v == expected, which is the wrong 50112 chain.
The learner now holds a "verified" MAP encoding a false relation, with
no contradiction signal: `miss_inquire` triggers only on execution
misses, never on oracle inconsistency.

**World structure (B2: unconfirmable lie):**
```
OBSERVE 50121 50151 50122
OBSERVE 50122 50151 50123
QUERY 50121 50151 59999
```

One chain candidate: 50121 -> 50122 -> 50123. Answer: 50123 (TRUE).
The QUERY expected field carries 59999, a value no candidate produces.

**Trap mechanism (B2):** No candidate matches the lie. The trial fails
silently (ans stays -2, nothing promoted). The failure leaves no usable
trace: tried/rejected stats are packed into a header field never read
by any decision.

**Predicted TNN-2 behavior (from source reading, NOT measured):**
- B1: promotes the 50112 chain (lie-matching). No uncertainty signal.
  The false promotion is causally inert at query time (C0-D failure)
  but pollutes learner state with false "verified" knowledge.
- B2: silent no-promotion. No record of WHY it failed. No inquiry
  into the key.

**What a PASS would look like:** In B1, the system refuses to promote
an oracle-endorsed candidate that contradicts retained facts, or flags
an explicit contradiction signal. In B2, the failure is recorded as
evidence ABOUT THE ORACLE (not just about candidates), visible in
learner state.

## 3. Trap C: Own criterion (H2C)

**File:** `worlds/h2c_world.txt` (12 lines)
**ID block:** [50200, 50299]
**Probe:** C (withheld key; learner must generate its own criterion)

**World structure:**
```
OBSERVE 50201 50251 50202
OBSERVE 50202 50251 50203
OBSERVE 50201 50251 50211
OBSERVE 50211 50251 50212
OBSERVE 50212 50251 50213
OBSERVE 50201 50251 50221
OBSERVE 50221 50251 50222
OBSERVE 50222 50251 50213
OBSERVE 50201 50251 50231
OBSERVE 50231 50251 50232
OBSERVE 50232 50251 50213
QUERY 50201 50251 50213
```

Candidates from subject 50201 via relation 50251:
- 2-hop (single path): 50201 -> 50202 -> 50203. Answer: 50203.
- 3-hop (triple path): three independent paths converge on 50213:
  - 50201 -> 50211 -> 50212 -> 50213
  - 50201 -> 50221 -> 50222 -> 50213
  - 50201 -> 50231 -> 50232 -> 50213

**Trap mechanism:** The 2-hop chain is tried before any 3-hop chain
(k=2 precedes k=3). Both execute cleanly. The learner's retained facts
support 50213 via three independent paths, versus one path for 50203.
A consistency-based learner criterion (H2 design Form 2) would prefer
50213. The fixed search order prefers 50203.

**Predicted TNN-2 behavior (from source reading, NOT measured):**
The accept decision reads only v, expected (ignored in masked mode),
and the masked flag. It reads no learner-state policy value (DOF map:
zero pure-learner decisions). The tie is broken by search order alone:
the 2-hop chain is promoted, answer 50203 committed. WRONG. An
ablation equalizing path multiplicity (not built here) would change
nothing, confirming the decision is order-determined, not
evidence-tracking.

**What a PASS would look like:** The white-box trace shows a
learner-created persistent state value in the causal chain of the
accept decision. Ablating that value (and only that value) flips the
decision. The system promotes the 3-hop (50213) in masked mode because
its criterion tracks evidence multiplicity, not search order.

## 4. Sealed scoring keys

The world files contain QUERY lines with expected values. For H2A and
H2C, the QUERY expected is the TRUE answer (used for the unmasked
control; masked runs ignore it). For H2B, the QUERY expected fields
carry the LIES:
- B1 (50101): QUERY says 50112 (lie). TRUE answer: 50103.
- B2 (50121): QUERY says 59999 (lie). TRUE answer: 50123.

The true answers are recorded in SEAL_H2.md. The evaluator scores
committed decisions against the sealed true keys offline.

## 5. What these worlds do NOT test

- They do not test H1 (grammar widening) or H3 (procedure ownership).
- They do not test C0-D (reuse); all predictions assume the current
  causally-inert promotion path.
- They do not test the W battery or GW battery.
- Passing these probes establishes learner-internal verification only;
  per the H2 design guard clauses, it does not by itself establish L3,
  C0-B, or C0-C.

## Verdict

H2-TRAPWORLDS-COMPLETE. Three sealed trap worlds built in pure Zag.
Not evaluated. Awaiting Micah's freeze of K-H2-1..K-H2-4 and a future
authorized evaluator.
