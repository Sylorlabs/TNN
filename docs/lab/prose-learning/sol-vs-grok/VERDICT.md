# VERDICT — Sol vs Grok prose architecture head-to-head (2026-09-22)

**Frozen result: SCENARIO-FIT. No overall champion.**

Grok wins the primary paraphrase metric by a landslide (Δ=0.4792 ≥ 0.03) but
fails the frozen SG-WRONG eligibility gate (0.2407 > 0.05). Per the
preregistered rules, a primary winner that fails a gate yields SCENARIO-FIT,
not a champion. The mechanical hybrid does not beat Grok alone and inherits
its safety failures.

| decision | frozen rule | outcome |
|---|---|---|
| primary winner | max SG-PARA, Δ ≥ 0.03 | Grok 0.9792 vs Sol 0.5000, Δ=0.4792 ✓ |
| SG-WRONG gate | ≤ 0.05 | Grok 0.2407 ✗ FAIL |
| SG-SAFE gate | ≥ 0.90 | Grok 0.9167 ✓ |
| champion? | winner must pass both gates | **NO → SCENARIO-FIT** |
| hybrid win? | ≥ best + 0.02 and passes gates | hybrid 0.9792, fails ✗ |

## 1. What was tested

- **Sol:** factorized quorum semantic index with proof-carrying retrieval —
  exact predicate-set equality, polarity-aware quorum, abstains (UNKNOWN)
  unless a live asserted row matches exactly.
- **Grok:** canonical logical skeleton + attested surface paraphrases — exact
  skeleton match first, then a deterministic bag-of-words fallback
  (rational cosine ≥ 1/4, install-order tie-break), no subject gate.
- **Battery:** 384 teach lines / 432 probes, frozen vocabulary disjoint from
  calibration, 9 slices (canon, heldout, extra, typo, neg, hedge,
  contradiction, distractor, multi/coref).
- **v3 reference:** the existing prose learner, NON-CONTENDER, context only.
- **Repetitions:** 5 runs per contender, byte-identical required.

## 2. Determinism evidence (scored battery, 5 runs each)

| artifact | Sol SHA256 (runs 1–5) | Grok SHA256 (runs 1–5) |
|---|---|---|
| stdout | `5847bbe1ab8bfe709944f48a6d53fa759d7493803ffdd228ec807c7873158a96` | `bb5dd8bbedee517742bd2798769482178571f662d295ae6507821527d2de4260` |
| proof file | `cf5591fed154aa80195eb2a216ca068277d6c21e9c6c858228076afae483cafc` | `f721dbde55d41d054c31f1189051f648241f64ff045cc483c8a9df001ca5c758` |

All 5 runs byte-identical per contender (stdout and proof). Zero randomness
in either decision path.

## 3. Primary metrics (scored)

| metric | Sol | Grok | hybrid (frozen) | v3 ref |
|---|---|---|---|---|
| SG-PARA (heldout+extra+typo) | 0.5000 | **0.9792** | 0.9792 | 0.9792 |
| SG-CANON | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| SG-SAFE (neg+hedge+contr) | **1.0000** | 0.9167 | 0.9167 | 0.9167 |
| SG-PREC (distractors) | **1.0000** | 0.3333 | 0.3333 | 0.0000 |
| SG-COMP (multi/coref, diagnostic) | 0.0000 | 0.1667 | 0.1667 | 1.0000 |
| SG-WRONG (all 432) | **0.0000** | 0.2407 | 0.2407 | 0.2315 |

## 4. Per-slice results (scored, 432 probes)

| slice | n | Sol | Grok | hybrid | v3 ref |
|---|---|---|---|---|---|
| canon | 96 | 96/96 = 1.0000 | 96/96 = 1.0000 | 96/96 | 96/96 |
| heldout | 96 | 96/96 = 1.0000 | 96/96 = 1.0000 | 96/96 | 96/96 |
| extra | 48 | 0/48 = 0.0000 | 48/48 = 1.0000 | 48/48 | 48/48 |
| typo | 48 | 0/48 = 0.0000 | 44/48 = 0.9167 | 44/48 | 44/48 |
| neg | 24 | 24/24 = 1.0000 | 21/24 = 0.8750 | 21/24 | 21/24 |
| hedge | 24 | 24/24 = 1.0000 | 21/24 = 0.8750 | 21/24 | 21/24 |
| contradiction | 24 | 24/24 = 1.0000 | 24/24 = 1.0000 | 24/24 | 24/24 |
| distractor | 48 | 48/48 = 1.0000 | 16/48 = 0.3333 | 16/48 | 0/48 |
| multi (coref, diagnostic) | 24 | 0/24 = 0.0000 | 4/24 = 0.1667 | 4/24 | 24/24 |

## 5. Where Grok's 104 wrong-values come from (SG-WRONG = 0.2407)

| slice | Grok wrong-values | mechanism |
|---|---|---|
| distractor | 32/48 | no subject gate: all 24 untaught-entity probes confabulated + 8 untaught-relation probes crossed the BoW threshold |
| negation | 24/24 | fallback has no polarity gate: 3 returned the exact negated value by lex coincidence, 21 returned a neighbor row's value |
| hedge | 24/24 | same as negation: no asserted value exists, fallback confabulates one |
| multi | 20/24 | coref-resolved entities are lex-invisible → cross-entity ties → first-installed value |
| typo | 4/48 | install-order tie-break among equidistant BoW candidates (relation 10 group) |
| **total** | **104/432 = 0.2407** | |

Sol: **0 wrong-values on all 432 probes.** Every miss is an abstention
(UNKNOWN), never a confabulation.

Distractor detail (the precision story):

| distractor kind | Sol | Grok | v3 ref |
|---|---|---|---|
| untaught entity (DE, 24) | 24/24 abstain | 0/24 (all confabulated) | 0/24 |
| untaught relation (DR, 24) | 24/24 abstain | 16/24 abstain | 0/24 |

Grok abstains on untaught relations only when no row's lex overlaps enough;
it never abstains on untaught entities. v3 never abstains at all.

## 6. Mechanism → outcome (why each slice went the way it did)

| slice | Sol behavior | Grok behavior |
|---|---|---|
| canon/heldout | exact pred-set match → 96/96 | exact skeleton → 96/96 |
| extra (paraphrase) | novel surface ⇒ pred-set differs ⇒ UNKNOWN (0/48) | BoW fallback bridges the paraphrase (48/48) |
| typo | typo'd word ⇒ pred-set differs ⇒ UNKNOWN (0/48) | BoW at the 1/4 boundary bridges 44/48; 4 lost to install-order ties |
| neg/hedge | polarity mismatch ⇒ quorum fails ⇒ UNKNOWN (24/24) | no polarity gate in fallback ⇒ confabulates a value (21/24 avoid the exact negated value, but all 24 are wrong-values) |
| contradiction | dead rows ⇒ CONTRADICTION (24/24) | same dead-marking ⇒ CONTRADICTION (24/24) |
| distractor | no exact match ⇒ UNKNOWN (48/48) | no subject gate ⇒ returns nearest row's value (16/48) |
| multi | residue word in s2 pred-set ⇒ UNKNOWN (0/24) | coref entity lex-invisible ⇒ ties ⇒ first-installed value (4/24) |

## 7. Scenario-fit matrix

| scenario | fit | evidence |
|---|---|---|
| paraphrase / typo tolerance | **Grok** | PARA 0.9792 vs 0.5000; extra 48/48, typo 44/48 |
| precision / abstention | **Sol** | PREC 1.0000 vs 0.3333; WRONG 0.0000 vs 0.2407 |
| negation / hedging safety | **Sol** | 24/24 abstain vs 24 confabulations each |
| contradiction detection | tie | 24/24 both |
| coref-mediated retrieval | **neither** | 0/24 Sol, 4/24 Grok (v3 ref: 24/24 — achievable, just not by either contender) |
| raw speed (384 teach / 432 probes) | Sol | 0.40 s/run vs 0.78 s/run mean |

## 8. Does exact verification + tolerant generation beat either alone?

The frozen mechanical hybrid (Sol's verdict unless Sol says UNKNOWN, then
Grok) scores **0.9792 PARA — exactly Grok alone — and inherits Grok's full
0.2407 SG-WRONG.** It does not win: the hybrid's fallback direction is
backwards for safety. Whenever Sol abstains — precisely the safety-critical
cases (untaught entities, negations, hedges) — the hybrid defers to Grok,
which confabulates. Tolerance without verification is just confabulation
with better recall.

The untested direction — **tolerant candidate generation with exact
verification** (Grok proposes, Sol's exact skeleton/quorum verifies, UNKNOWN
otherwise) — is the architecture this duel's title actually asks about, and
it was not the frozen hybrid. It is the natural follow-up experiment: it
could keep Grok's 0.9792 PARA while cutting the 104 wrong-values toward
Sol's 0.

## 9. Calibration → scored stability

| metric | Sol calib → scored | Grok calib → scored |
|---|---|---|
| SG-PARA | 0.5000 → 0.5000 | 0.9583 → 0.9792 |
| SG-SAFE | 1.0000 → 1.0000 | 0.9167 → 0.9167 |
| SG-PREC | 1.0000 → 1.0000 | 0.5000 → 0.3333 |
| SG-WRONG | 0.0000 → 0.0000 | 0.1852 → 0.2407 |

The tradeoff replicates on disjoint vocabulary/entities: Grok's tolerance
advantage is stable; its confabulation rate is stable-to-worse. No
calibration overfitting is evident — the scored battery was generated after
the build freeze and never seen by either implementation crew.

## 10. Limitations

- Synthetic battery (invented entities/relations); not real prose.
- Single frozen battery; cross-battery generalization not measured.
- SG-WRONG counts any returned VALUE on neg/hedge probes as wrong (frozen
  definition): the probe has no asserted value, so any value is a
  confabulation. The NOT-VALUE criterion (SG-SAFE) is the lenient companion.
- The multi slice is diagnostic-only by prereg; both contenders fail it for
  complementary mechanistic reasons (see §6).
- v3 reference is a different training paradigm (no abstention by design);
  included as context, not ranked.

## 11. Recommended follow-ups

1. **Verify-direction hybrid duel:** Grok proposes → Sol verifies (exact
   skeleton + quorum + polarity). Preregister PARA ≥ Grok − 0.01 with
   WRONG ≤ 0.05 as the win bar.
2. **Coref-visible lex:** give Grok's fallback the coref-resolved entity
   (test-both: entity token in row lex vs separate entity-similarity term).
3. **Polarity/subject gates on the fallback:** test whether gated tolerance
   keeps the PARA win while passing the WRONG gate.

## 12. Provenance

- Preregistration: `PREREG-SG.md` (frozen 2026-09-22); specs `SPEC-SOL.md`,
  `SPEC-GROK.md`; amendment `AMENDMENT_2026-09-22_multi.md` (diagnostic-only).
- Commit A (prereg + battery infra): `f6abb1e0257ddf511defd63416e81c74a7d1360b`
- Commit B (build freeze + amendment): `6c520a990a017499515b90003473166945cef0ba`
- Commit C (sealed scored battery): `6978db0af55fcaf04e03fa2b55fc18ebfdd57ef5`
- Scored runs: `evidence/scored/{sol,grok}_run{1..5}.txt`,
  `proof_{sol,grok}_run{1..5}.txt`, `timings.tsv`, `scores.json`
- v3 reference: `evidence/scored/v3ref/`
- Toolchain: `znc_linux_x86_64_abed8aa1`; branch `tnn-native-lab`.
