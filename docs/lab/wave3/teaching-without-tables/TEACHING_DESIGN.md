# TEACHING_DESIGN.md — Teaching without tables

Agent (Wave-3, teaching-without-tables), 2026-09-19.
Status: design, pre-trial. Preregistered in `PREREG.md` before any run.

## 0. The question

How does a teacher convey knowledge to a TNN learner **without the learner
becoming a lookup table of teacher answers**? What makes taught knowledge
*the learner's own* rather than a copy?

## 1. Candidate mechanism: propose → verify → commit/refuse

The teacher never writes into the learner. The teacher **proposes** — a
trace, a hypothesis, a memory candidate, a belief. The learner then runs a
**verification** against its own evidence channel (its own recorded
observations, its own probes — never the teacher's word), and either:

- **COMMITS** — as a deliberate, audited memory op carrying the learner's
  *own provenance* (`SELF_VERIFIED`, in the R27 Trace vocabulary), with the
  teacher recorded only as attribution (`taught_by`), never as authority; or
- **REFUSES** — with an explicit reason (`CONTRADICTED` by own evidence,
  `INSUFFICIENT_EVIDENCE`), the refusal itself audited (MEMORY_OPS.md: a
  refusal is an event worth auditing).

After teaching, the teacher is **withdrawn** (H-09): the learner's subsequent
decisions are made from committed slots only. **Teacher dependence** is then
*measured*, not asserted:

```
dependence = (# post-withdrawal correct answers whose provenance chain
              bottoms out at a teacher assertion with NO intervening
              learner verification op)
           / (# post-withdrawal correct answers)
```

measured by walking the audit ledger's provenance fields. This is the direct
answer to `MutableStudent.teacher_dependence` (STATE_SCHEMA.md open question
#4 — unexamined until now): dependence is a *structural property of the
provenance ledger*, computable white-box.

## 2. Why this is not a table (the anti-table argument)

The banned shape (DO_NOT_REPEAT.md §8.2): teacher hands over (key → answer)
pairs and the learner stores them verbatim — decision becomes reflexive
lookup of teacher content. The proposed mechanism differs in three
structural ways:

1. **Commit is gated by the learner's own evidence.** Nothing enters memory
   on teacher authority. The commit op is impossible without ≥K agreeing own
   observations and zero contradicting ones. The gate is in the op
   implementation (like REFUSED_CORE in MEMORY_OPS.md), not in policy.
2. **What is stored is the verification, not the assertion.** The committed
   record carries: the belief, the agreeing/contradicting own-observation
   counts, the learner's verification op id, and `taught_by` attribution.
   Replaying the ledger reconstructs *why* the learner believes it.
3. **The learner can and does refuse.** Refusal is a first-class outcome
   with reasons. A copy cannot refuse.

Counts of own observations are *recorded evidence*, not accumulated scores:
there is no accumulator, no argmax, no confidence threshold anywhere in the
decision path. Abstention post-withdrawal is structural (no committed slot
→ no answer), not a probability bucket (cf. H-05).

## 3. The honest limit (built into the design)

Verification is only as good as the learner's own evidence. If the learner's
own observations are wrong, the learner will **verify a falsehood and commit
it — with its own provenance**. The mechanism's guarantee is "no copying,"
not "no error." Taught knowledge becomes the learner's own *including the
failure mode*: errors are the learner's errors, traceable to its own
evidence, not the teacher's. The trial deliberately includes this trap
(PREREG.md §4) because a mechanism that cannot show its failure mode is a
facade.

## 4. The smallest native trial (what this wave runs)

Beliefs as the unit (a memory candidate in the MEMORY_OPS.md frame):
- World: 16 items with fixed ground truth (designed, not random).
- Learner's own channel: 24 own observations (2 per item for items 0–11),
  with designed noise on items 5 (both wrong) and 9 (split).
- Teacher: proposes claims on items 0–11 — adversarially, *all claims are
  "TRUE"*, so 6 are true and 6 are false.
- Two arms, identical curriculum:
  - **VERIFY** (the mechanism): commit iff ≥2 own obs agree AND 0 contradict;
    else refuse with reason.
  - **COPY** (negative control — the banned shape, explicitly labeled, run
    only to validate that the dependence metric discriminates; it is not a
    candidate mechanism).
- Teacher withdrawal; then query all 16 items; measure dependence per arm.

Expected: VERIFY commits 6 (5 correct + the item-5 verification failure),
refuses 6 (5 contradicted falsehoods + 1 under-evidenced truth), dependence
0. COPY commits all 12 teacher-only, dependence 1.0.

## 5. Scale dimension (Micah's program law, 2026-09-19)

The ban was on scaling *toy mechanisms* (N×N score tables), never on scale.
This mechanism's scale argument:

- **Per-proposal cost:** O(K) evidence checks, K = own-observation count per
  item (bounded by the learner's own probing budget, not by domain size).
- **Per-commit cost:** O(1) audited op + O(1) slot.
- **State:** O(committed items) with provenance — never O(domain). A table
  must cover the domain; verification covers only what is taught.
- **Dependence measurement:** O(slots) provenance walk.
- **Ledger replay invariant** (MA1's "conscious" definition): O(ledger
  entries), unchanged in kind at 100x.

10x/100x items, longer horizons, larger memory: the mechanism's structure is
unchanged; only the audit grows linearly. The trial at 16 items is small on
purpose — it tests the *mechanism*, like MA1's 8 slots — and the prereg
names the next scale test explicitly (PREREG.md §7).

## 6. Determinism (Micah's program law, 2026-09-19)

**No RNG anywhere in the system's decision paths.** The verify gate is a
pure deterministic function of (proposal, recorded own evidence). The
world is a designed fixed table (adversarial by design, §4) — no seeded RNG
even in the harness; test adversity is an explicitly designed curriculum.
The trial runs twice and must be byte-identical. The verdict distinguishes
"the system is deterministic" (same output, run to run) from "the test was
adversarial" (the designed false-claim and noise traps).
