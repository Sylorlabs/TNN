# Phase-1 Scientific Record - Overnight Research Session 2026-09-28

**Authority:** Autonomous research lead, acting under Micah's overnight mandate.
**Method:** Five independent inspectors produced evidence reports
(`~/workspace/tnn-review/wave1/`); seven verifiers independently reproduced
every load-bearing claim from the repo record only
(`~/workspace/tnn-review/wave2-verify/`, CONSOLIDATED.md).
**Result:** 23 CONFIRMED / 1 REFUTED / 2 MIXED / 0 UNCLEAR (26 atomic claims).

This document is the canonical correction. Original verdict documents are NOT
rewritten; they are annotated with pointers here. Archival evidence is preserved.

**Markers used:** INVALID (verdict cannot stand), RETRACTED (claim withdrawn),
SUPERSEDED (replaced by a better classification), VOID (verdict-grade null -
measurements stand, judgment did not exist), DEFECTIVE (do not execute as is).

---

## 1. Combiner salt battery (57d055b) - governance INVALID

### 1a. H-C kill: INVALID

- At the H-C implementation commit (`a95e0d50c`, 2026-09-27 18:03:06 PDT), the
  only committed definition is `K-HC4 (learn the D1 six)` → verdict **PASS**
  (with documented deviations D1, D2). `BUILD.md:216`.
- The same document states the r7 swap-first-last withhold is "honest
  limitation, **not a bar**" (`BUILD.md:144-146`), and the chaining audit
  records r7 W5 withhold as **correct** behavior.
- The salt commit (`57d055b`, 2026-09-27 19:24:28 PDT) redefines K-HC4 as
  "minimum capability includes swap-first-last" (`TESTING.md:141`) - a phrase
  occurring nowhere else in the committed record - and kills H-C for the
  previously-accepted withhold.
- The referenced `hyp/hypo_c/HYPOTHESIS.md` was never committed; no other
  frozen definition exists to appeal to.
- **Correction:** the H-C kill is INVALID. H-C's status reverts to **SURVIVES**
  under its frozen bar (K-HC4 = "learn the D1 six"). The salt measurements for
  H-C (48/48 P0, 118/120 P1, 4/8 P3) are preserved as **exploratory data** -
  the salt battery had no frozen bars and cannot render verdicts.
- **Rule violated:** "Never retroactively alter a kill bar to save or kill an
  architecture." This instance altered a bar to kill.

### 1b. H-B "survives": VOID as a preregistered verdict

- K-HB-1 first appears in the results commit `57d055b` itself
  (`git log -S "K-HB-1"` returns exactly one commit). No prereg existed.
- The bar (118/120 P1; 47/48 P0) sits exactly one point below the observed
  scores (119/120; 48/48). The cited "HYPOTHESIS.md §2.1/§3" exists on no branch.
- **Correction:** H-B's measurements STAND (48/48 P0, 119/120 P1, 8/8 P3 -
  deterministic, byte-identical, committed raw scores), but the "SURVIVES"
  verdict is VOID: there was no frozen bar to survive. A principled bar must be
  frozen (justified from H-B's own design standards, NOT fit to 119/120) and
  the existing deterministic measurements judged against it.
- H-B's induction remains BOUNDED evidence for parameter-level structural
  generalization (discovers affine parameters, never the procedure; the 8 salts
  test one invariance property eight times; byte-op salt-riding untested).

### 1c. H-A kill: verdict STANDS, diagnosis RETRACTED

- The 5 wrong emissions on Eaff are real (committed raw rows).
- **RETRACTED:** TESTING.md's causal diagnosis. The Eaff teaching arm carried
  0/12 uppercasing signal - the salt maps all 12 r4 teaching first bytes outside
  a–z, so H-A **correctly** learned identity from signal-free teaching
  (`ha.zag` BYIDENT-first verification). This is an uncalibrated arm, not a
  proven mechanism boundary. (Refinement: TESTING.md's "outside a–z" failure
  description is contradicted by the raw bytes `0x79,0x70,0x70,0x67,0x67` -
  the failures are on in-alphabet bytes under salted teaching.)
- **Required:** a calibrated re-run (salt preserving the uppercasing signal in
  teaching) under a bar frozen BEFORE results.

### 1d. Mechanical enforcement (new standing rule)

Prereg-before-results held for memory control (prereg as direct parent commit)
but collapsed exactly where verdicts were most load-bearing. New rule: **no
verdict-grade claim may cite a kill bar whose first committed occurrence is not
strictly earlier than the results commit.** Verifiers must check this by
`git log -S` before any verdict is recorded.

---

## 2. H2 taught-physics world model (7979a55) - SUPERSEDED classification

The "learned world model" framing is SUPERSEDED by the L0–L3 classification:

- **What was taught (L1):** 13 integers extracted from frozen Session-1 text via
  hand-chosen anchor substrings. The prereg states verbatim: "H2's 'learning'
  is declarative-to-executable compilation plus online planning. It learns
  nothing from practice."
- **What was hand-coded (neither taught nor learned):** all M1–M15 dynamics in
  `model_step`; the 64-tick planner (8 candidates, hand-coded base policy and
  tie-break - BUILD.md's "9 candidates" is wrong, confirmed in `h2.zag`).
- **"0 mismatches over 32,912 ticks"** measures copy fidelity to the
  evaluator's own `d2bin`, not learned physics.
- **The central thesis (P2 composition 22–24/24) never ran.** No P2 evidence
  files exist.
- **Governance:** all 7 committed validation scripts are Python (violates the
  literal pure-Zag red line); `wp_compare.py` hard-codes dead workdir paths -
  the wrong-physics evidence is not reproducible from the repo.
- **Standing value:** L1 infrastructure (taught table causally drives a
  hand-coded planner - the wrong-physics traces do diverge 63–72%, so the
  planner genuinely reads the table). Usable as a planning substrate; NOT
  evidence that TNN learns world models.

## 3. Memory control (7abf194) - BOUNDED, with disclosures

Prereg discipline confirmed (prereg `066553ad4` is the direct parent commit).
The BOUNDED verdict stands with these mandatory disclosures:

- **What "learning" means here:** 9 text lessons (sitmask, phase → action) +
  strengths installed into persistent memory. The protocol, 6-bit situation
  vocabulary, failure→lesson attribution table, and strengthening schedule are
  authored. The run triggers installation; it does not discover the policy.
- **DISCLOSED:** `GEN:always_protocol` ("deliberate insight") never fired -
  trigger needs ≥3 diverse failures; actual was 1. No such lesson exists in
  final memory. The verdict's "deliberate" framing overclaims.
- **DISCLOSED:** the ablation is confounded - `operate_nv` forces TRUST_HINT
  AND skips verification (plus READBACK/NCONFIRM). It does not isolate
  verification. A clean single-factor ablation is still owed.
- **DISCLOSED:** `REUSE_TABLE` (prereg-specified 3×) is unimplemented.
- Held-out novelty is parameter-level (same 5 trap families, same generator).
  Retention is frozen-memory policy stability, not continual learning.
- **Standing value:** a real native persistent-lesson-memory mechanism with
  honest prereg and hard negative controls (NEG 148/323 collateral). Usable
  infrastructure for the continuing-learner program.

## 4. Text-approx prereg/seal/builder - DEFECTIVE, do not execute

- Commit ordering is formally clean (prereg < seal < builder).
- The corpus itself is good (credible labels, exact class counts, zero
  dev/sealed leakage, no sealed evaluation has run).
- **DEFECTIVE - do not execute as frozen:**
  1. `ta1_gate` is a universal-WITHHOLD stub; `ta3_gate` does not exist.
  2. `ta1_derive.zag` does not implement PREREG_TA.md §5 (byte-level vs
     token-level affix stripping; whole-episode negation refusal vs mid-span
     negation-multiset; case-folding where case-sensitive specified).
  3. H-TA3 has no admission rule - §6 lists only withhold triggers; building
     the gate requires inventing semantics the freeze forbids.
  4. KB-TA-1..4 thresholds are the builder crew's self-ratified "reconstructed
     bids," citing `HYPOTHESES_TA.md`, which was never committed (the
     "committed with the build package" claim sits in PREREG_TA.md:11-12 at the
     prereg commit itself).
  5. The prereg cites "the reference Python implementation in `generators/`" -
     the generators were never committed, so the seal's "fresh rebuild
     byte-identical (11/11)" is unreproducible, and a Python mirror is baked
     into the frozen spec (governance ruling 6 territory).
  6. H-TA2 (the inference-step hypothesis - the load-bearing question for
     replacing LLM systems) is deferred; the head-to-head as designed tests
     which withhold-gate is safer, not semantic inference.
- **Repair plan (not this night's primary):** amend the prereg openly -
  admission semantics for H-TA3, real threshold provenance, §5-conformant
  derive, committed generators or a struck rebuild claim - then re-freeze and
  build. The corpus is worth saving.

## 5. Large knowledge ingestion - L0 established, integration FAILED

- **Established:** 9,030,226 facts taught deterministically (merge SHA
  `af10db8b…`, teach ×2 byte-identical). Storage (blobs, sparse index, lessons,
  revise/delete) is solved infrastructure.
- **FAILED:** downstream audited QA 3/250 vs curated baseline 14/250
  (delta −11, `DRYRUN_REPORT.md:117/121/125/133`). Retrieval is keyword-count
  IR (Aho-Corasick over question words, max word overlap) - no synonyms, no
  paraphrase, no inference. This explains 3/250 exactly.
- **Bright spot preserved:** 3 probes genuinely correct where the baseline was
  wrong (K-078, K-092, K-160) - the only real knowledge-gain evidence.
- **Standing direction:** finishing Wikipedia ingestion before building semantic
  retrieval is backwards. The frozen 250-probe battery is the A/B floor for any
  retrieval prototype. (Phase-2 SEM-L3 is the first such prototype.)
- **Correction to Inspector E:** `teach/gate.zag` and `dryrun/` were not
  deleted by `13c557cd3`; they were dropped by a history rewrite. `gate.zag`
  (86,155 bytes) is recoverable from `454d48b40` via `refs/remotes/rh-main`.

## 6. L0–L3 classifications (standing)

| Result | Classification | Basis |
|---|---|---|
| 9M-fact ingestion | L0 (storage) | records supplied information; no invented structure |
| H2 world model | L1 (parameter learning) | 13 taught integers fill a hand-coded simulator |
| Memory control kbc | L1 (parameter learning) | 9 lessons installed under authored credit assignment |
| H-B combiner | L1+ (parameter induction) | discovers affine parameters via search; never the procedure |
| Text-approx (as designed) | L1 (would be) | taught derivation edges + gates |
| **SEM-L3 (Phase 2)** | **L3 target** | learner-invented concept nodes, not enumerated in source |

No L2 or L3 result exists anywhere in the current record. That is the night's
target.

---

**Committed:** (this commit) as the canonical Phase-1 correction. All prior
verdict documents remain in history, annotated by pointer to this record.
