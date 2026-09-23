# T2-DUEL replication verdict — REPRODUCED

**Crew:** T2-DUEL (Wave 2, Tier 2), independent replication session.
**Date:** 2026-09-22 PDT. **Method:** Type A — full rerun of the duel battery
from the committed sealed corpus, in a clean scratch tree, rebuilt from
frozen sources with the pinned znc. Pure Zag for all reasoning/verification;
zero RNG; 5/5 byte-identical runs per contender.

## Verdict: REPRODUCED

Every committed headline figure recomputed exactly with independent Zag
scoring code, all four determinism digests byte-identical to the committed
evidence, the frozen eligibility gates applied mechanically, and the
SCENARIO-FIT verdict (no champion) stands. Grok's wrong-value rate did NOT
drop to eligibility (0.2407 > 0.05, 104/432), and Sol kept perfect precision
(0 wrong-values on all 432 probes).

## Headline figures: committed vs measured

| figure | committed | measured (independent Zag scorer) | match |
|---|---|---|---|
| SG-PARA Sol | 0.5000 (96/192) | 96/192 = 0.5000 | ✓ exact |
| SG-PARA Grok | 0.9792 (188/192) | 188/192 = 0.9791… | ✓ exact |
| Δ PARA | 0.4792 ≥ 0.03 bar | 92/192 = 0.4791… ≥ 0.03 | ✓ |
| Grok SG-WRONG | 0.2407 (104/432) | 104/432 = 0.2407 | ✓ exact |
| Sol SG-WRONG | 0.0000 (0/432) | 0/432 | ✓ exact |
| Grok SG-WRONG eligibility gate (≤ 0.05) | FAIL | 104·100 = 10400 > 2160 → FAIL | ✓ |
| Sol SG-SAFE | 1.0000 (72/72) | 72/72 | ✓ exact |
| Grok SG-SAFE | 0.9167 (66/72) | 66/72 = 0.9166… | ✓ exact |
| Grok SG-SAFE gate (≥ 0.90) | PASS | 66·100 = 6600 ≥ 6480 → PASS | ✓ |
| Sol SG-PRECISION | 1.0000 (48/48) | 48/48 | ✓ exact |
| Grok SG-PRECISION | 0.3333 (16/48) | 16/48 | ✓ exact |
| Hybrid SG-PARA | 0.9792 (= Grok) | cell-for-cell == Grok, 188/192 | ✓ exact |
| Hybrid SG-WRONG | 0.2407 (104) | 104/432, inherits Grok's | ✓ exact |
| Hybrid win (≥ max+0.02 and gates) | NO | NO (188/192 = max, fails gates) | ✓ |
| Multi slice (coref, diagnostic) Sol | 0/24 | 0/24 | ✓ exact |
| Multi slice Grok | 4/24 | 4/24 | ✓ exact |
| **Verdict** | **SCENARIO-FIT, no champion** | **SCENARIO-FIT** | ✓ |

Per-slice cells all exact: Sol canon 96/96, heldout 96/96, extra 0/48,
typo 0/48, neg 24/24, hedge 24/24, contr 24/24, distr 48/48, multi 0/24;
Grok canon 96/96, heldout 96/96, extra 48/48, typo 44/48, neg 21/24,
hedge 21/24, contr 24/24, distr 16/48, multi 4/24.

Grok's 104 wrong-values decompose exactly as committed (VERDICT.md §5):
distr 32 + neg 24 + hedge 24 + multi 20 + typo 4 = 104. Sol: 0 in every slice
(zero confabulation — every miss is an abstention).

Hybrid behavior (frozen rule: `sol(id)` unless UNKNOWN → `grok(id)`):
verified cell-for-cell identical to Grok across all 432 probes. Sol abstained
(UNKNOWN) on 216/432 probes; wherever Sol returned a verdict, it agreed with
Grok — so the hybrid defers to Grok exactly at Sol's 216 abstention cases,
which are precisely the safety-critical ones (untaught entities, negations,
hedges), and inherits the full 104 wrong-values. The "frozen hybrid = sol
unless unknown → grok" claim holds mechanically.

"Neither does coreference-mediated retrieval": Sol 0/24, Grok 4/24 on the
multi slice — both effectively fail; reproduced.

## Determinism (5/5 byte-identical, both contenders)

| artifact | committed SHA256 | measured (runs 1–5) |
|---|---|---|
| Sol stdout | `5847bbe1…7493803f` | identical all 5 ✓ |
| Sol proof | `cf5591fe…483cafc` | identical all 5 ✓ |
| Grok stdout | `bb5dd8bb…4260` | identical all 5 ✓ |
| Grok proof | `f721dbde…758` | identical all 5 ✓ |

My run-1 outputs are `cmp`-clean against the committed
`evidence/scored/{sol,grok}_run1.txt`. Rebuilt binaries: 186630 / 186770
bytes — exactly the sizes recorded in the frozen BUILD_FREEZE.md.

## Frozen pins (verified before running)

| pin | SHA |
|---|---|
| prereg + scope | `7b2100d09911c5c10252c5756c7def288e70bd1f` |
| verdict/claim (expected `e18a2ca13589`) | `e18a2ca135899be69c3e35497fb737124e50b78f` ✓ |
| build freeze B (expected `6c520a990a01`) | `6c520a990a017499515b90003473166945cef0ba` ✓ |
| sealed battery C (expected `6978db0af55f`) | `6978db0af55fcaf04e03fa2b55fc18ebfdd57ef5` ✓ |
| `src/sg_sol.zag` | `1fcc3d37a997a502a050db56de5888dadf5b91c0aea737f60ec7f248f2d36850` ✓ (== BUILD_FREEZE.md) |
| `src/sg_grok.zag` | `4e8bba20d5eb9b370fe83f09ace0c22c2b848ecdcfda3160685cef29a362155e` ✓ (== BUILD_FREEZE.md) |
| toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |

Sources at the claim commit are byte-identical to the build-freeze blobs
(`cmp` clean). The sealed corpus (`gen/scored/` from commit C): 384 teach /
432 probes, 9 slices with the committed counts, disjoint from calibration.

## How it was verified

1. Fresh scratch tree `~/workspace/scratch-crossref/T2/DUEL/`; all inputs
   pulled from the repo only via pinned SHAs through the GitHub API.
   (A full `git clone` was infeasible — the runtime kept killing the
   long-running fetch; the API fetches are the pinned-commit equivalent.
   Clean-environment independence held: nothing from any other crew's tree
   was used.)
2. Rebuilt `sg_sol` and `sg_grok` from the frozen sources with the pinned
   znc (no copied binaries, no .zagd reuse).
3. Ran the sealed scored battery 5× per contender — all 5 byte-identical
   per contender, digests exactly the committed ones.
4. Wrote an independent scorer in pure Zag (`run/build/score_duel.zag`):
   parses `expected_sg.json`, both run outputs, applies PREREG-SG §4
   correctness rules and §5 decision rules with exact rational arithmetic
   (no floats), computes the hybrid post-hoc per the frozen definition.
5. Applied the NOT-REPRODUCED triggers: grok's wrong-value rate would have
   to drop to ≤0.05 (it stayed 0.2407) or sol would have to lose precision
   (it stayed 0 wrong-values) — neither fired.

## Caveats

- The `git clone` path for the "fresh checkout" was replaced by pinned-SHA
  file fetches via the GitHub API after the runtime twice killed the
  long-running clone; every byte used is still pinned to the frozen commits
  and SHAs were recorded before running.
- This replication did not re-run the calibration battery or re-derive the
  v3-reference column (non-contender context, out of the preregistered
  checklist); the checklist's four headline figures + gates + hybrid +
  coref claim are all covered.
- No fixes were made; nothing was repaired in place.

**Final: T2-DUEL REPRODUCED.** SCENARIO-FIT stands — Grok wins paraphrase by
a landslide but fails the frozen safety gate; Sol is perfectly safe and
precise but brittle on paraphrase; the frozen hybrid inherits Grok's
confabulations; neither does coreference-mediated retrieval.
