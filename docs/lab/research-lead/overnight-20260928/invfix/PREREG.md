# INVARIANT-FIX PREREGISTRATION (C510-C5xx)

**Author:** invfix lane (isolated worktree `/Users/Shared/micah/Documents/TNN/.worktrees/invfix`)
**Role:** fix catastrophic CORRECTNESS defects as REPRESENTATION INVARIANTS.
**Date:** 2026-10-03
**Committed ALONE, before any implementation.**

## 0. INPUTS (frozen, copied into this lane, never edited in place)

| core | upstream path | sha256 first 12 |
|---|---|---|
| COGOPS base arena | `cogops_rescueaware/c15_base.zag` | `fc1f6e73c43a` |
| COGOPS learner | `cogops_learnosc2/c8_learn.zag` | `750cb01d086f` |
| TNN-2 frozen ref | `compression_exec/tnn2_frozen_ref.zag` (lines 1..917) | `a29972ca8183` |
| L3-SUF code-freeze | `l3_suf_intermediate/src/` (8 files) | see `CODEFREEZE.md` |

## 1. THESIS: ONE ROOT, NINE SYMPTOMS

Every confirmed defect (adversary C501-C509, property lane V1-V6) has the
same shape in the substrate:

> **A record is written on the basis of a PROJECTION of its own content, into
> a region whose size and occupancy are never recorded, and read back without
> re-validating that the record found is the record intended.**

Four consequences, each independently fatal:
- **P1 IDENTITY NOT CLOSED** -- the key is a coarser projection than the content
  (bare goal tag, bare need tag, relation alone, value magnitude).
- **P2 CAPACITY NOT RECORDED** -- strides, counts and cursors are literals.
- **P3 COUNT NOT THE STORED COUNT** -- a clamped store reports an unclamped count.
- **P4 NO CHECKED DECODER** -- dispatch is by magnitude on an untagged field, so
  two encodings share one representation and truncation is indistinguishable
  from completion.

**P1 is the deepest.** C501 (goal tag), C504/C508 (relation-only evidence),
C505 (node id vs frame slot), C509 (max-bid tie-break as "the" answer) are all
P1. C502/C503/C506/V3/V6 are P2+P3. V2 is P4.

## 2. THE MECHANISM I WILL INSTALL (general, not per-counterexample)

**M1 CLOSED-KEY CONTENT TABLES.** Supersede the fixed-stride BIND and PLAN
tables with self-describing, content-keyed record stores in which:
- the key IS the full canonical content of the item (cell-for-cell equality,
  never a hash, never a projection), so identity collision is impossible;
- records are variable length (a bump + free-list allocator) so there is no
  stride to overflow;
- each store header carries MAGIC / LIVE / USED / CAP.

**M2 EXPLICIT CAPACITY, CHECKED BEFORE WRITE.** Every bounded writer checks the
caller-visible capacity derived from the slice length or from the M1 header
BEFORE writing. On overflow it writes NOTHING, bumps a named counter, and
returns a distinct refusal code. No silent truncation anywhere.

**M3 CHECKED DECODER, FAIL LOUDLY.** Operand / record fields are TAGGED with
disjoint ranges (`OPND_NODE` vs `OPND_SLOT` over disjoint code bands). A value
outside every band decodes to `MALFORMED (-999998)`, which is counted in its
own counter and is NOT the same value as a guard rejection (`-999999`).

**M4 PROVENANCE CLOSURE.** Every fact node carries an explicit provenance code
in a reserved field. The exact-hit path serves only OBSERVED provenance.
Inference may never launder into the fact table. Every inference rule must be
invariant over its WHOLE evidence set, never a prefix of allocation order.

**M5 ANSWER-TYPE CLOSURE.** A set-valued question has a representation.
`ev_query_set` returns the sorted distinct object set; the scalar `ev_query`
REFUSES with `ANS_SET (-3)` when the object set does not have exactly one
member, instead of choosing one by `bid` tie-break.

**M6 VALIDATOR AS A RUNTIME GATE.** `iv_check` / `iv_scan` walk every table and
every record and return a violation code. `compose` and `ev_query` run the
validator on entry and exit; a violation is a loud decline, never an answer.

## 3. SUPERSESSION (charter 51/158) -- declared BEFORE implementing

- **`bootstrap_miss` (tnn2:763) is SUPERSEDED and REMOVED from active
  architecture.** Subject-blind inversion ("all recent r-facts agree, therefore
  `s r v0`") is not knowledge: its evidence set excludes the queried subject
  (P1), it is a recency prefix (C508, P1), and it persists its output as a fact
  node (C504, laundering). The surviving general mechanism for a true miss is
  the Change-2 inquiry path `miss_inquire` -> UNCERTAINTY -> guide -> `ev_act`,
  which already refuses honestly and records the miss. Nothing is lost by
  removal; the rule has no licensed consumer.
- **The fixed-stride PLAN and BIND tables are SUPERSEDED** by M1.
- **Hard-coded strides 56 / 16 / 128 / 80 / 160 are SUPERSEDED** by M1/M2.

## 4. PER-DEFECT KILL BARS (frozen before implementation)

| id | invariant that must now hold | kill bar |
|---|---|---|
| C501 | plan identity = (goal_tag, FULL goal content); family memo = (need_tag, FULL need content) | B, C, D all answer 1 with `compose_rc=2` (fresh plan) or a recorded content-mismatch; no probe returns `{}` |
| C502 | variable-length plan record; explicit plan/bind capacity; capacity refusal is a distinct rc; decline zeroes `ans` | no phantom plan (`plan_find(L,0)=-1`); no 73-int garbage; arity 5..8 all answer or decline loudly; `plan_new` at capacity returns a refusal rc from `compose`, not 2 |
| C503 | reported count == stored count; overflow counted, not hidden | `ret_gen` reports 40 only if it stores 40, else reports 32 and sets OVERFLOW; the AW-03 COUNT is 1 or a loud refusal, never 2 |
| C504 | no fact node is created without evidence about the queried subject | `ev_query(999,10)` == -2 and fact-node count about 999 is 0, on the second query too |
| C505 | operand codes are tagged, disjoint; malformed decodes to -999998 and is counted separately | literal at node id 1013 reads 7777; E-large (996 padding) promotes the same graph as E-small and answers 3 |
| C506 | node capacity is an explicit record; admission is checked before write; refusal is loud; victim order is content-derived | at live<=1016 all 6 new facts retrievable; at full capacity `ev_teach` returns -1 and `cap_refusals` increments (never silent success) |
| C509 | set-valued answers have a representation | 4-object star returns -3 (refuse), identical under reversal; chain returns 3 |
| C508 | answers are order-invariant | dissenter-first == dissenter-last |
| V2 | a severed program cannot report success | post-severance `ev_query` refuses, MAP quarantined, ownership closure reported |
| V3 | log shortfall is itself recorded | 200 events -> `log_drops == 72`, stated in output |

## 5. DETERMINISM AND NON-REGRESSION BARS

- `zbuild --rep 3` on every reproducer: 3/3 byte-identical, rc=0, non-empty.
- **NON-REGRESSION.** Re-run the frozen COGOPS corpus worlds (`c8_world.zag`
  goals 808..821, world A/B/C/D/E) and the frozen TNN-2 self-test battery
  against the fixed engine. Byte-identity is required wherever the frozen
  engine was already correct: same answer ints, same stats cells, same version
  selection. Any behavioural delta must be at a site named in section 3 as
  SUPERSEDED, or at a site that was previously SILENTLY WRONG.
- **ADVERSARY RE-RUN.** Rebuild the adversary's own 9 worlds unchanged against
  the fixed engine and report which breaks are eliminated.
- **SUBSTRATE-WIDENESS.** Run the same 9 worlds against the L3-SUF code-freeze
  and report whether the defect class is TNN-2-specific or substrate-wide.

## 6. METHOD RULES

- Pure Zag for ALL computation (`. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`).
- `_zag_print`/`_zag_println` only; ASSERT non-empty output in every binary.
- The compiler is presumed SOUND; no memory-free oracle means no miscompile
  claim is admissible.
- No per-counterexample branch. If a fix cannot be expressed as a general
  mechanism plus a validator, it is not done.
- Explicit pathspecs. Never `git commit -a`.
- Claim IDs C510+.
