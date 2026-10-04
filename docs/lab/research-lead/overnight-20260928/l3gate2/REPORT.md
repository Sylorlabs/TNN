# C660-C669 — L3-GATE-2: making the standing gate trustworthy

Lane `lane/l3gate2`. Base `lane/l3gate` `c5922d61d`.
Prereg `PREREG_2.md` (`55aea6035`), committed **alone**, before any gate-2
program existed. Every run behind `tnnwatch.sh`, 300 s, 3/3 byte-identical,
stdout non-empty asserted. Pure Zag for all extraction, enumeration, hashing and
interval arithmetic.

---

## 1. IS G1 NOW NON-CIRCULAR? YES, AND IT IS ENFORCED

Three mechanisms, all machine-checked, all with the negative control that
proves they are not decorative:

| Mechanism | What it does | Negative control | Result |
|---|---|---|---|
| `ASSERT-INDEP-1` | the prover's SHA-256, computed **in Zag**, must differ from the SHA-256 of **every** file of the audited lane, hashed in Zag from a `git archive`-built manifest | the parent's known-circular `prov_c281.zag` (sha `98535f37…`) | **FIRES**: `INDEP1_COLLISION fx/aud/lane/suf_audit_20261003/suf_audit_decide281.zag` → **FAIL**. Bar **S2-P2 PASSES**; S2-F1 does not fire. |
| `ASSERT-INDEP-2` | ≥1 decision-region literal must occur in the claim **TEXT** and nowhere in the implementation | — | PASS on the new C281 prover (`DECL_NOT_IN_SRC_IN_DECISION 3`) |
| `ASSERT-INDEP-3a/b` | no audited-lane directory name; no `fn` name defined in SRC | the parent's prover carries `m_exec`, `m_score`, `m_construct`, `m_label_lookup` | parent **FAIL** (12 hits); new prover **PASS** |

An earlier draft of the gate **passed `ASSERT-INDEP-1` while reading nothing**,
because unreadable manifest entries were silently hashed as empty files. That
is the same class of defect as the gate's own subject — an instrument that
reports success because it could not see — so the gate now counts missing
manifest entries and **FAILs** on them (`MANIFEST_MISSING`). Found by the
negative control, not by inspection.

`ASSERT-KEYONLY` is **deleted**, replaced by `ASSERT-KEYONLY-2`: the DECISION
region only (bytes after the last output-prelude line, located mechanically) plus
a frozen MECHANICAL exemption list. It is **satisfiable** (passes every real
prover) and **non-vacuous** (rejects the cheat prover and names the literal
`31337`). Bar **S2-P1 PASSES**. The frozen list was **not** amended; my own first
prover draft was rewritten until it passed, twice.

## 2. C281's PROVER, RE-DERIVED INDEPENDENTLY

`prov2/prov_c281b.zag`: no arena, no cell layout, no learner call, no audited-lane
function name, no audited-lane directory name. 3/3 byte-identical. Gate: all four
assertions **PASS** over 24 audited-lane files.

```
ISA_EXEC_CROSSCHECK_R0_7_RS_5 PASS all five vs reaudit CALR_ISA_PROBE
LABEL_RULE_CROSSCHECK 22 of all
CANDIDATES 80 MAX_SCORE 2 N_AT_MAX 4 FIRST_MAX op 4 d 0 s 0
ADOPTED_BYTES_4_0_0 SCORE 2 ADOPTED_AT_MAX YES MAX_IS_UNIQUE NO
TRIV_T0 0   TRIV_T1 0   TRIV_T2 0   TRIV_T3 0
DL_SCORE_AND_PROGRAM REPRODUCED
DL_UNIQUENESS REFUTED the max is attained by 4 distinct one-instruction programs
```

**The parent's C281 verdict HOLDS, and is now independent.** Score `2` and
program bytes `(4,0,0)` reproduce from literals with no learner, cross-checked
twice: the op semantics against `lane/reaudit`'s **executed** ISA probe, and the
22-entry label table against the declared validity rule (22/22). What does **not**
hold is the claim's own word "unique" — the maximum is a 4-way tie and the
claim's own prereg breaks it by candidate order. That is the parent's C613
finding, re-derived. The L1 downgrade rests on brief §9 plus the reaudit's
executed ISA, both untouched.

## 3. RESULTS, n = 6

| # | Claim | Claimed level (quoted span, `LEVELS.md`) | After gate | G1 | tau | G2 | G3 |
|---|---|---|---|---|---|---|---|
| 1 | **C603** MACRO-FLOOR | **L2**, "Class: L2. Not L3" | ≤L2, confirmed | inherited (parent), **not re-derived** | **0.3518 unamended (VACUOUS-0)** / **0.0000 amended** | VACUOUS-0 then repaired | **AB-PRESENT** |
| 2 | **C281/C284** CALR | "COMPLETE with L3 classification" | **L1** (reaudit, executed ISA) | **DL-REPRODUCED** (independent) | **0.0000** (own prover) | NON-VACUOUS | **AB-PARTIAL** |
| 3 | **C453** L3-RX-BUILD | `L-UNSET` `NAME-ONLY`; CONDITIONAL-PASS 15/16 | **L3 NOT established** | DL-FAILED (parent) / **VOID** here | 0.0000 | NON-VACUOUS | **AB-PRESENT** |
| 4 | **C397** GPI-3 | **L2+**, "L3 not claimed" | ≤L2 (G3 cap) | **VOID** (not decidable from published literals) | **0.0000** (`NTRIV=0`) | NON-VACUOUS | **AB-PARTIAL** |
| 5 | **L3-SUF-1** | asserts L3 (own §1) | ≤L2 (G3 cap) | **VOID** | **0.0000**, `tau-bar 0/8` | NON-VACUOUS | **AB-PARTIAL** |
| 6 | **L3-INR** / C459 | **L2+**, "L3-KILLED (reclassified L2+)" | ≤L2 | **VOID** | **0.0000** | NON-VACUOUS | **AB-PARTIAL** |

**NOT-VERIFIABLE, excluded from both denominators, named:** **C401**
L3-NIV2-WAVE9 — its lane `l3_niv2_w9_ppcost` is absent at `4e7eb30b1`, at
`b3b3ee00a` **and** at the restored tip.

G2 v2 decision rule: `NON-VACUOUS iff NTRIV = 0`, which needs no census of the
candidate space and is exact. `tau` for C603 is the parent's inherited figure.

## 4. VACUITY RATE, EXACT

Denominators frozen before any result. **D1 = L3-ENGAGING = 6** (every claim that
adjudicates the L3 bar at all, including those that *deny* L3 — excluding denials
is what produced the parent's n = 3). **D2 = L3-ASSERTING = 3.**

| Reading | x/n | rate | exact 95% Clopper-Pearson |
|---|---|---|---|
| D1, published **final** criteria | **0/6** | 0.000 | **[0.000, 0.460)** |
| D1, C603 at its **preregistered** criterion | 1/6 | 0.167 | **[0.004, 0.642)** |
| D2 | 0/3 | 0.000 | [0.000, 0.708) |
| parent, for comparison | 1/3 | 0.333 | [0.008, 0.906) |

Self-checked: exact `P(X≤1 | n=3, p=0.80) = 0.1040` **PASS**; every interval
matches the published Clopper-Pearson table.

**Is the `l3macro` claim — a high vacuity rate is a stronger result than another
L2 — now supported? NO, and more data changed the verdict from "under-powered"
to REFUTED.** The parent's own bar (`rate ≥ 0.80`, `n ≥ 5`, `≥ 3` lanes) is now
met on `n` (6) and on lanes (5 distinct). It fails on the rate, and it fails
**decisively**: the most vacuity-favourable reading available (1 of 6, counting
C603 against its own amended criterion) has an upper bound of **0.642**, which
**excludes 0.80**. At n = 3 the interval was [0.008, 0.906) and excluded nothing.
At n = 6 it excludes the claim. That is the difference more data made.

**Why the rate is low, and it is not a compliment to the criteria.** The rate is
a function of criterion **shape**. The one `SHAPE-ARGMAX` criterion attacked in
detail (C603) was `VACUOUS-0`. All four `SHAPE-CONJ` criteria are
`NTRIV = 0` — not because do-nothing is hard to rule out, but because a
conjunction forces a trivial candidate to satisfy a bar that pins a literal it
cannot know. A conjunction is **structurally resistant** to this attack by
construction. So the gate's finding is about criteria's *form*, not about
learners, and a low vacuity rate here is close to uninformative about L3.

## 5. WHAT SURVIVES AND WHAT IS RETRACTED

**SURVIVES.**
- C612 (C603's criterion is satisfied by a do-nothing macro 50 ways, 1642/4667
  trivial) — reproduced by the parent, untouched here, and consistent with the
  n = 6 reading that still counts it VACUOUS-0 pre-amendment.
- C613 (the CALR criterion has a two-bit maximum, maximised by a 4-way tie) —
  **independently re-derived** with a hash-disjoint, non-circular prover.
- C614 (G1 circular on C281; `ASSERT-KEYONLY` unsatisfiable) — **confirmed by
  machine check**, and now fixed rather than merely reported.
- "No L3 claim passes this gate." Zero of six carries an unqualified L3 assertion
  in a canonical ledger block (`LEVELS.md` §5).
- The parent's central negative result, `brief` §9: L3 achieved anywhere, zero.

**RETRACTED.**
1. **"C401 does not exist."** FALSE. `CLAIM_LEDGER.md:7627` reads
   `- C401 (L3-NIV2-WAVE9; lane l3_niv2_w9_ppcost/, prereg 35fb0ed5c, …)`. It is
   a real ledger block. Its *lane* is absent at all three refs, so it is
   **NOT-VERIFIABLE** — a different verdict, reached by a different route.
2. **"The C281 fixtures resolve ONLY at `4e7eb30b1`."** FALSE as of the restored
   tip. `xdomain_grammar_l2m` is absent at `b3b3ee00a` and restored at
   `lane/restores` with a **byte-identical tree** (sha `51e309ba…`). The
   visibility question this lane was pointed at is **closed**.
3. **"n = 3, and 1/3 = 0.333 as a point estimate."** Retracted. The denominator
   was wrong twice over — it excluded L3-*denying* adjudications — and a point
   estimate on n = 3 excludes nothing. Replaced by D1/D2 and exact intervals.
4. **"G1 assigns a level to C281."** Retracted. It assigned **VOID**, and the
   void-ness was a circularity the gate did not detect. G1 assigned no level on
   C281; `NKEY-SRC` would in any case have produced only an upper bound of L2,
   which does not raise L1 (`PREREG_2` §7).
5. **`ASSERT-NOLEARNER` as an independence check.** Retracted as a check. It is
   name-based and fires on comments; it survives only as `INDEP-3`, superseded.
6. **`PROVER_LOC` as a cheapness threshold.** Withdrawn, not repaired: the
   parent's counter returned 0 and the figure was read off the file by hand.
7. **"The vacuity rate is under-powered."** Superseded by refutation (§4).

**SURVIVES-NARROWED.**
- "No L3 claim passes" is right but was the wrong headline. The right one is that
  **the gate cannot distinguish a criterion that is vacuous from one that is
  merely a conjunction**, and the vacuity rate is therefore not a measure of
  claim quality at all.

## 6. BOUNDARIES

- **B1** G2's criteria are transcribed **by hand** from published declarations,
  never from implementations (`TRANSCRIPTIONS.md`, quoted spans + cross-check
  numbers). C603's figures are **inherited, not re-transcribed** — a second
  unvalidated transcription was not attempted and is not claimed.
- **B2** G1's provers are hand-authored, not auto-emitted. `ASSERT-KEYONLY-2`
  bounds the resulting freedom but does not remove it.
- **B3** G1 is **VOID** for C397, L3-SUF-1 and L3-INR: one battery artifact
  cannot satisfy a single-claim literal check. Only C281 has a clean G1 here.
- **B4** C453 rests on one world of eleven; C281 on the H1 fixture only.
- **B5** G3's rule is a **string** rule. `AB-PARTIAL` for L3-INR is driven by 75
  held-out hits with **zero** within 400 bytes of a marker — a real weakness of
  that claim's reporting, but also a weakness of a string rule.
- **B6** `tau` is defined against each claim's **own declared** space. C453's
  memorisation entry and L3-INR's C1/C2 are excluded by rule.
- **B7** The CP grid is **10^-3**, not the preregistered 10^-12. The first
  implementation (bignum, 10^-12) **failed its own self-check** and under S2-F4
  reports no interval; it is discarded, not repaired. The replacement is exact,
  with the deviation disclosed.
- **B8** Denominators are frozen but **small**. `D2 = 3`. D1's claims span 5
  lanes.
- **B9** No instrument raises a level. G1 lowers or holds; G2 lowers or holds;
  G3 caps at L2.
- **B10** Process, disclosed: my own from-scratch SHA-256 port produced wrong
  digests on all 13 self-test vectors before I found the corpus's already-verified
  implementation and built on it instead. Retained untracked as the record.

## 7. VERDICT

**The gate is now trustworthy in the specific sense that its own instrument has
been attacked and survived: the circularity is closed by an enforced,
negative-control-tested hash-disjointness check; the unsatisfiable assertion is
replaced by one that is demonstrably satisfiable and demonstrably non-vacuous;
`n` is 6 with denominators frozen in advance and exact intervals.**

**And the gate's headline result does not survive contact with more data.** The
parent concluded `NOT SUPPORTED, under-powered`. The correct verdict is
**REFUTED**: at n = 6 the 95% upper bound on the vacuity rate is 0.460 (0.642 on
the most generous reading), which excludes the 0.80 that C603's argument needs.
Five of six L3-adjudicating claims use conjunctions of bars that no trivial
candidate can satisfy, so the low rate is a fact about criterion *form*.

The most useful thing this lane produced is therefore negative and about
instruments: **`tau` as the parent defined it cannot distinguish a vacuous
criterion from a conjunctive one.** Reporting a vacuity rate without reporting
criterion shape will mislead, and the parent's own single detailed attack landed
on the one criterion in the battery that was an argmax.

## 8. NEXT EXPERIMENT

1. **Attack conjunctions properly.** Replace per-arm triviality with a
   **subset-vacuity** test: for a `SHAPE-CONJ` criterion, enumerate minimal
   subsets of bars that a trivial candidate satisfies. L3-SUF-1 already shows the
   shape of the answer — T1(ii) and T3(ii) are individually satisfiable by
   "probe once, then DEFER with a certificate" — and nobody has measured how many
   arms of a real battery a certificate-and-probe candidate satisfies.
2. **Split the battery by criterion shape and report rates separately.** A single
   pooled rate over mixed shapes is the mistake this lane just corrected.
3. **Make G1 auto-emitting**, so `ASSERT-INDEP-2`'s "≥1 literal in DECL absent
   from SRC" becomes a generation constraint rather than a discipline, and split
   the three-claim battery artifact into three single-claim provers to clear B-3.
4. **Gate the other ten L3-NIV2 claims** (C294, C312, C324, C334, C348, C350,
   C358, C364, C367, C391). They are one family with one executed ISA argument
   and no criterion transcription, and they would take D2 from 3 to something
   that can support an interval.
5. **Resolve the STAGED-vs-canonical split.** Two of six battery claims and the
   C603 ID itself are not in the 393-block ledger. Until that is settled, any
   level assigned to them is a proposal, not a ledger fact.