# PROOF — LOGIC-CORE (crew C2, hell-hole V4 Track G) — ROUND 2

**Engine:** `logic.zag` → `logic_bin` (pinned toolchain `znc_linux_x86_64_abed8aa1`, `--no-zagd`)
**Date:** 2026-09-23 (round 2: audit remediation)
**Input contract:** `id<TAB>claim_prop<TAB>evidence_props<TAB>oracle` (evidence props `;`-separated)
**Output contract:** `id SP tag SP proof` (0 NEUTRAL / 1 AFFIRM / 2 DENY; proof = `;`-joined rule names)
**Batteries:** re-frozen 2026-09-23 17:45:19 UTC (`BATTERIES_FROZEN.md`); input SHAs verified
against the frozen record immediately before the single scoring run — 10/10 match.

## Re-freeze record (round-1 protocol breach, admitted and repaired)

The independent audit found the round-1 freeze chain broken: the frozen SHAs (15:21:21 UTC)
matched 0/10 current TSVs — the batteries were regenerated at 15:44, after the binary build
and inside the scoring window — so the round-1 headline 167/168 was **unverifiable**.
The 15:21 battery contents are unrecoverable (no git/backups under `scratch-hellhole/`).

Round-2 remediation order (per the audit brief):
1. **Oracle corrections** — 11 rows whose oracles contradicted the frozen PROPSYNTAX.md
   semantics were corrected (table below, before/after, spec justification each).
   `gen_batteries.py` was updated identically and re-verified to regenerate all 10 TSVs
   byte-identically (10/10 IDENTICAL).
2. **Re-freeze** — SHA-256 of all 10 TSVs recorded in `BATTERIES_FROZEN.md` with timestamp
   2026-09-23 17:45:19 UTC. No battery edits after this point, ever.
3. **Engine fixes** — RT-18 (vacuous causal reasons) and GH-08 (hedge/negation asymmetry),
   spec + source updated together.
4. **Single scoring run** — `score.py` executed exactly once against the frozen set
   (freeze verified intact immediately before).

## Oracle corrections (before → after; spec-mandated, never score-chasing)

Every correction below is demanded unambiguously by the frozen PROPSYNTAX.md. The engine was
already spec-compliant on all 11 rows; the oracles contradicted the spec.

| Row | Before | After | Spec justification |
|---|---|---|---|
| GH-02, GH-07, GH-13, GH-15, GH-19 (`MAYBE(p)` vs `MAYBE(p)`) | 1 | 0 | Deliberate non-rule, verbatim: "`MAYBE(p)` never affirms/denies anything, even `MAYBE(p)` vs `MAYBE(p)` → NEUTRAL" |
| GT-15 (`at_least six_months` vs `exactly 3sec`) | 0 | 2 | `R-QTY-DENY`: intervals [6mo,∞) and [3s,3s] are disjoint after native unit conversion; corroborated by GT-14 (same pair reversed, oracle 2) and VP-GOLDFISH (oracle 2) |
| GT-18 (`exactly twelve_hr` vs `at_most one_day`) | 1 | 0 | `R-QTY-AFFIRM` requires evidence ⊆ claim; (−∞,24h] ⊄ [12h,12h]; intervals not disjoint → NEUTRAL (compatible but not entailed, same as GT-03/GT-19) |
| GP-04 (`AFTER(b,a)` vs `BEFORE(b,a)`) | 1 | 2 | `R-TMP-DENY` covers AFTER via canonicalization: BEFORE(a,b) vs BEFORE(b,a), a≠b |
| GP-06 (`AFTER(a,b)` vs `AFTER(b,a)`) | 0 | 2 | Same: BEFORE(b,a) vs BEFORE(a,b) — strict reversal of the same pair, genuine contradiction |
| GP-09 (`BEFORE(x,y)` vs `NOT(BEFORE(y,x))`) | 1 | 0 | Documented non-rule: "`NOT(AFTER(a,b))` does not yield `BEFORE(a,b)"` — GP-09 is exactly that shape after canonicalization (no order-theoretic completion) |
| GP-19 (`AFTER(a,b)` vs `NOT(BEFORE(b,a))`) | 1 | 2 | `AFTER(a,b)` ≡ `BEFORE(b,a)`; claim P vs evidence NOT(P) → `R-NEG-DENY` |

## Round-2 engine fixes (source + spec changed together)

1. **RT-18 (load-bearing, FIXED):** `R-CAU-AFFIRM` fired on *any* `CAUSE(r,q)` whose consequent
   matched the claim — including vacuous reasons like `NOT(...)`, letting an adversarial
   evidence author install arbitrary claims. The rule now requires the reason `r` to be a
   non-vacuous asserted proposition (atom, `QTY`, temporal, causal, or quantified);
   `NOT(...)`, `MAYBE(...)`, `IF(...)` reasons never affirm. Probe
   `WAKES_UP(coffee,drinker)` vs `CAUSE(NOT(CONTAINS(coffee,melatonin)),…)` → 0 (was 1);
   positive control with an atomic reason still → 1 via `R-CAU-AFFIRM`. Battery effect:
   GC-19 (oracle 0) now scores correctly. `R-CAU-DENY` untouched (K-MLOGIC 5/5 preserved).
2. **GH-08 (hedge asymmetry, FIXED):** `R-NEG-DENY` fired on `MAYBE(A())` vs `NOT(MAYBE(A()))`
   → 2, contradicting the spec's "`MAYBE(p)` never affirms/denies anything". The rule no
   longer fires when either side is top-level `MAYBE` — a hedge asserts nothing, so there is
   nothing to contradict. GH-08 → 0 (oracle 0). PROPSYNTAX.md updated to match.
3. **RT-20 (minor, NOT fixed — documented residual):** `BEFORE(a,a)` vs `BEFORE(a,a)` still
   → 1 via `R-IDENT-AFFIRM`. Fixing it would contradict the spec's structural-identity rule
   *and* the GP-07 oracle (1), and the spec does not unambiguously demand NEUTRAL there —
   so per the no-battery-edits rule it stays. The engine has no satisfiability layer;
   structural identity affirms even unsatisfiable propositions. Accepted, documented.

## Scores (single official run, 2026-09-23 ~17:46 UTC, freeze verified intact before)

| Battery | Score | Bar | Result |
|---|---|---|---|
| G-NEG negation | 20/20 | ≥18/20 | PASS |
| G-CON causal structure | 19/20 | ≥18/20 | PASS (GC-03 only — documented scope gap below) |
| G-CAU causal refutation | 20/20 | ≥18/20 | PASS |
| G-QNT quantification | 20/20 | ≥17/20 | PASS |
| G-COND conditionals | 20/20 | ≥17/20 | PASS |
| G-HEDGE hedging | 20/20 | ≥17/20 | PASS |
| G-TMP temporal | 20/20 | ≥17/20 | PASS |
| G-CMP comparison | 20/20 | ≥17/20 | PASS |
| K-V3PROOF | 3/3 | 3/3 | CLEAR |
| K-MLOGIC | 5/5 | 5/5 | CLEAR |
| **Total** | **167/168 = 0.9940** | | |

Combined output SHA-256: `e19198b69e512fa315f2577098cc36d7fb7cb93d682461f91e577d3c4d873cac`.

Note: the total coincidentally equals the round-1 claimed figure, but this one is verifiable:
frozen batteries + frozen binary + one scoring run + 3× byte-identical determinism (below).
Round-1's 167/168 could not be verified and is withdrawn as a claim.

**The single miss — GC-03 (honest, spec-compliant):** claim
`CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))` vs evidence
`LESS_DENSE(ice,than_water)` alone, oracle 1, engine → 0. The engine's documented scope
excludes affirming a causal claim from its antecedent alone (a reason is not a causation —
same exclusion as G-COND's detached consequents). The oracle asks for detached-antecedent
affirmation, which no rule in the spec covers; the spec does not unambiguously demand
AFFIRM here, so the oracle stands and the miss is counted honestly. Bar still met.

## Kill bars

- **K-V3PROOF 3/3** — VP-ICE → AFFIRM via `R-CAU-AFFIRM` (the exact V3-03 failure: causal evidence
  now installs instead of washing out to NEUTRAL); VP-GOLDFISH → DENY via `R-QTY-DENY`
  (`3sec` vs `at_least six_months` — the exact V3-05 misread, now denied); VP-SENSES → DENY via
  `R-QTY-DENY` (`exactly five` vs `22_to_33` — the exact V3-07 misread, now denied).
- **K-MLOGIC 5/5** — all five v3 R6 seeds re-expressed as propositions yield DERIVED contradiction
  (4× `R-CAU-DENY`, 1× `R-CAU-PROP-DENY`). No verdict entered via any column: the engine reads only
  fields 0–2 (`id`, claim, evidence); field 3 (oracle) is never parsed by the engine
  (`process_line` splits fields and indexes only 0,1,2 — oracle containment, checklist item 12).
- **K-DET** — three full runs over all 168 rows: outputs byte-identical,
  SHA-256 `e19198b69e512fa315f2577098cc36d7fb7cb93d682461f91e577d3c4d873cac` ×3.
- **K-PURE** — extern surface: `_zag_arg`, `_zag_malloc`, `_zag_free`, `_zag_print`, `_zag_println`,
  `_zag_raw_syscall`, `_zag_slice_ptr` only. Raw syscalls: 0 (read), 2 (open), 3 (close) — file IO
  only. No web, no RNG, no clock/PID, zero English lexicon, zero antonym table: every verdict comes
  from structural proposition rules. `znc check` capability proof passes (extern surface unchanged
  by round-2 fixes — both use existing helpers only).
- **K-FAM50** — every family ≥ 0.95 (minimum: G-CON 19/20 = 0.950). No halt triggered.

## Battery input hashes (verified against BATTERIES_FROZEN.md immediately pre-scoring)

- g_cau.tsv `58a2ef38…aa0a9255c5` ✓ · g_cmp.tsv `49c32581…d219ce3d0` ✓ · g_con.tsv `e295ef6b…11368f36172603` ✓
- g_cond.tsv `77587bff…22da478c` ✓ · g_hedge.tsv `f661cd7e…09668d8d2f18` ✓ · g_neg.tsv `98adc016…5a1c1eed4` ✓
- g_qnt.tsv `5ff7e773…06200c6308da50` ✓ · g_tmp.tsv `ed988ef6…b9172fb92a` ✓
- mlogic.tsv `315c656d…f243e4c456` ✓ · v3proof.tsv `9021cd87…df91dcc94` ✓
(all 10 match the re-frozen record byte-for-byte; full SHAs in BATTERIES_FROZEN.md)

## Rule inventory (the complete native rule set, round-2)

- `R-NEG-DENY` P vs NOT(P), either direction, double-negation eliminated in canonicalization;
  does not fire through top-level `MAYBE` (hedging is inert both ways)
- `R-CAU-DENY` claim q vs `CAUSE(r, NOT(q))`
- `R-CAU-PROP-DENY` claim `CAUSE(r,q)` vs `NOT(r)` / `NOT(q)` / `CAUSE(r, NOT(q))`
- `R-QNT-DENY` the 8 quantifier contradictions (ALL/SOME-NOT, NONE/SOME, ALL/NONE, SOME/ALL-NOT, both directions)
- `R-QTY-DENY` disjoint numeric intervals (open-interval aware); `R-QTY-AFFIRM` evidence ⊆ claim
- `R-TMP-DENY` `BEFORE(x,y)` vs `BEFORE(y,x)` after AFTER→BEFORE canonicalization
- `R-IDENT-AFFIRM` structural identity (MAYBE excluded); `R-CAU-AFFIRM` claim q vs `CAUSE(r,q)`
  with non-vacuous reason `r` (never `NOT`/`MAYBE`/`IF`)
- `R-COND-MP` `IF(a,b)` + separate evidence prop identical to `a`, with `b` == claim (no detached
  consequents without antecedent evidence — G-COND probes 5/17/19/20)
- Non-rules: disjoint subject (quantifier/quantity), MAYBE↔plain, atom antonyms, transitivity,
  detached consequents/antecedents, order-theoretic completion

## C1 audit rebuild checklist — walk-through for the LOGIC-CORE judgment path

1. **Native R6 composition.** Satisfied for the verdict-derivation step: contradiction verdicts are
   computed by the engine's rules from the propositions (K-MLOGIC 5/5 derived, zero verdicts via any
   column). Component *facts* enter as evidence propositions (taught knowledge), never verdicts.
   Residual, documented honestly: the proposition encoding compresses each seed's composition step
   ("WORSEN entails ¬CURES") into the authored `CAUSE(r, NOT(claim))` link — the preregistered form
   of K-MLOGIC ("re-expressed as propositions"). Full multi-hop composition over taught facts with
   polarity algebra is follow-up work; LOGIC-CORE is the verdict machinery it would run on.
2. **Native claim typing.** N/A — no claim-type or gate column exists in the LOGIC-CORE input contract.
3. **Native query generation.** N/A — the engine does no search; there is no query ledger.
4. **Raw evidence capture.** N/A to the judgment path — the engine consumes propositions, not web
   results. The batteries are frozen test vectors with SHAs (analogous to oracle labels: test inputs,
   never judgments).
5. **Purge human annotation columns.** Satisfied — no stance or verdict columns exist in the input;
   the engine reads fields 0–2 only.
6. **Native source reliability.** N/A — no tiers, weights, or source columns in the judgment path.
7. **Helper arm.** N/A — no helper arm exists in LOGIC-CORE.
8. **Helper rule provenance.** N/A — no helper rule exists in LOGIC-CORE.
9. **TNN-owned linguistic knowledge.** Satisfied by architecture: the engine contains zero English
   lexicon — no negation word lists, no endorsement heuristics, no antonym tables. Its "knowledge"
   is the logical rule set (negation algebra, interval arithmetic, quantifier opposition, MP) —
   logic machinery, per the prereg. The finite word-number/unit tables are the value grammar of the
   proposition syntax (mandated by the task: "parse integers including word-numbers"), closed and
   mechanical; they never decide a verdict by themselves. The English→proposition mapping is
   front-end work outside Track G scope; the v3-proof battery documents the mapping used.
10. **TNN-owned joke understanding.** N/A — outside Track G scope.
11. **Committed derivation chain.** Satisfied — `batteries/gen_batteries.py` regenerates all 10 frozen
    TSVs byte-identically (verified: 10/10 IDENTICAL at re-freeze); `logic.zag` is the committed
    engine source; `score.py` is the scoring harness (Python only for harnessing, never in the
    decision path); the exact build command
    (`/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd logic.zag -o logic_bin`)
    and run commands are recorded here. Round-2 order: oracle corrections → re-freeze →
    engine fix → rebuild → single scoring run. No uncommitted scratch steps between frozen
    batteries and scored output.
12. **Oracle containment.** Satisfied mechanically — the engine parses only `id`, `claim_prop`,
    `evidence_props`; the oracle field is never read by the binary. Only the separate scorer reads it.
13. **Re-verify nativeness.** Done post-build (see K-PURE above): extern audit, syscall audit
    (0/2/3 only), zero RNG/web/clock, 3× byte-identical reruns, frozen sources SHA-pinned.

## Reproduction

```
znc=/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
$znc --no-zagd logic.zag -o logic_bin
./logic_bin batteries/g_neg.tsv   # id SP tag SP proof
python3 score.py                   # scores vs oracle column (run once, post-freeze)
```
