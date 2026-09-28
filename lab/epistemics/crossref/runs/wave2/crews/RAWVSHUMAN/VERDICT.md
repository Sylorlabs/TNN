# VERDICT — T2-RAWVSHUMAN: raw-vs-human wave, binding KILL of the human-style line

**Crew:** T2-RAWVSHUMAN (replacement; predecessor killed by daemon restart)
**Date:** 2026-09-22/23 PDT
**Verdict: REPRODUCED**

## 1. Frozen claims checklist and decision rule (quoted verbatim from the prereg)

Source: `docs/lab/crossref/PREREG_TIER2.md` § T2-RAWVSHUMAN, frozen commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`. Extracted by this crew directly
from the frozen section (no summary relied upon):

> **Claims:** prereg `a87ddfd4`, diagnostics `8954577204f5`, forks `31c68a56fe7c` (2026-09-22): causal finding — 99.8% of B's color errors (99.2% pitch) happen when both stimuli fall inside one percept bin (bin destroys distinguishing information before any decision runs); 'training' was only threshold calibration over frozen bins, mathematically inert after T1; both rescues built and tested dead — vocabulary growth (splitting bins where errors happen) and fuzzy bin edges, both <1pp gains; killer finding — the only way percepts match raw precision is a vocabulary as fine as the raw space (thousands of handles) = quantized raw values wearing names, no longer 'human-style'. Binding recommendation: kill the human-style line as a precision competitor. Preserved: transducer stays in-repo as cheap coarse front-end (2.42× fewer ops, −27pp accuracy); redirect: KB4 memory integration (~50% adversarial false-install both approaches) is the binding constraint.
> **Method:** Type A rerun of the diagnostics (error-in-bin attribution) + Type C re-derivation of the two rescue forks' <1pp figures from committed evidence.
> **Rule:** REPRODUCED if the ≥99% in-bin attribution holds and both rescues stay <1pp; NOT REPRODUCED if any rescue crosses +1pp or the attribution drops below 95%.

## 2. Attribution vs measured (Type A rerun, independent Zag)

Committed claim → measured by `d1_verify` (3 byte-identical runs,
digest `c9e6733e82e4d86336e94aacf0187f97636c5611203675c1f0a2c624acfbb61f`):

| Modality | Committed | Re-derived (this crew) | ≥99% bar |
|---|---|---|---|
| colordisc | 505/506 = 99.8% | 505/506 = 99.80% | HOLDS (50500 ≥ 99×506 = 50094) |
| pitchdisc | 131/132 = 99.2% | 131/132 = 99.24% | HOLDS (13100 ≥ 99×132 = 13068) |

The re-derivation does not trust the precomputed flags: error is re-derived
from (judgment vs truth), same-handle/bin from (p1==p2), and sub_semitone from
rel_pitch via exact scaled-integer comparison against 2^(1/12)−1. All five
precomputed flag classes agree with the independent re-derivation on all 1200
rows (0 mismatches). Neither modality drops below 95% (no NOT-REPRODUCED
trigger). The withdrawn band-based color figure in `d1_results.json` (0.8794)
was not used, per the D1 report's correction note.

## 3. Rescue figures vs measured (Type C re-derivation, independent Zag)

Committed claim → measured by `rescue_verify` (3 byte-identical runs,
digest `b576517bc427051dc24b30ede36d7292a64781cb8517a42bc4f729ed8a0d002a`),
using EXACT fixture counts:

| Fork | Committed | Re-derived (exact) | <1pp bar |
|---|---|---|---|
| B2 vocabulary growth, T1 | +0.3pp | 1/360 = **+0.278pp** | HOLDS |
| B2 vocabulary growth, T2 | +0.0pp | **0** | HOLDS |
| B3 fuzzy bin edges, T1 | +0.85pp | 1/120 = **+0.833pp** | HOLDS |
| B3 fuzzy bin edges, T2 | +0.85pp | 1/120 = **+0.833pp** | HOLDS |

Kill-bar re-application (committed overall per-mille, A = 838):
B2-T1 563, B2-T2 562, B3-T1 563, B3-T2 565 — all < 600 and all fail the
(B−A ≥ +2pp) prong → **both forks DEAD at both budgets**, as committed.
No rescue crosses +1pp (no NOT-REPRODUCED trigger).

Grow-log rule check (committed logs): adopted cuts T1-color 4, T1-pitch 5,
T2-color 0, T2-pitch 2 — counts match the verdict table; every adopted cut's
gain ≥ 10‰ (the preregistered adoption threshold), so the ≥10‰ rule was applied
mechanically. Committed `b2/grown_T2.zag` sha256 recomputed as
`92c3c844b06d5156debf9ecdbb644120b8ec72747940db4c63877303a420e9c4`,
matching the committed determinism table (original + 2 reruns) exactly.

## 4. Supporting context figures (Type C re-derivation, independent Zag)

Measured by `context_verify` (3 byte-identical runs,
digest `a21c8bef208fe890679eacf234d33d271d79294b9e89061682222ea2b3cf0d85`),
from the rematch verdict at `1c01a1ad`:

| Claim | Re-derived | Result |
|---|---|---|
| Transducer: 2.42× fewer ops (413,890,710 / 171,235,328) | 2.4171 → **2.42** | HOLDS |
| Transducer: −27pp accuracy (B−A) | −272‰ → **−27pp** (−27.13 exact) | HOLDS |
| KB4: ~50% adversarial false-install, both approaches | A 55/114 = **48.2%**, B 72/132 = **54.5%** (bar ≤10%, both FAIL) | HOLDS |

## 5. Mechanical verdict

- ≥99% in-bin attribution: **holds** on both modalities (99.80% color, 99.24% pitch).
- Both rescues <1pp: **holds** (max exact gain 0.833pp; max committed 0.85pp).
- No NOT-REPRODUCED trigger fired (no rescue ≥ +1pp; no attribution < 95%).
- The binding recommendation (kill the human-style line as a precision
  competitor) follows mechanically: both rescues are DEAD under the wave
  prereg's kill bars, and the mechanism diagnostics show the bins — not the
  decision layer — destroy the information.

**T2-RAWVSHUMAN: REPRODUCED.** Every committed headline bar matches within the
preregistered tolerance; the exact-fraction re-derivations agree with the
committed 1-decimal figures (residuals ≤ 0.02pp, documented as rounding
provenance in RUNLOG.md, none verdict-relevant).

## 6. Pins frozen (all verified present before running)

- prereg `a87ddfd4c41f88710f5e573e9c0283d003360b6d` (2026-09-22)
- diagnostics `8954577204f5cd9ac772f071a213b3fb620a743c` (2026-09-22)
- forks `31c68a56fe7c012c543625465af6f1fd934e6212` (2026-09-22)
- clean checkout: `7b2100d09911c5c10252c5756c7def288e70bd1f`, tree clean

## 7. Caveats / open questions

- The original `d1.py` recomputed dE/truth from the frozen generator over
  external uncommitted fixture paths; this crew re-derived the attribution
  from the committed per-fixture rows instead (the committed evidence), with
  every precomputed flag independently re-derived from primitive fields.
  A from-generator rerun would require the rematch fixture corpus, which is a
  different family's committed evidence — out of scope for this Type A/C.
- The "killer finding" (thousands-of-handles = quantized raw values) is the
  wave's interpretive conclusion from the two dead rescues, not a separately
  gated number; the prereg's decision rule gates only on attribution + rescue
  gains, both verified.
- `m=0 byte-identical validation` for B3 is a committed process claim in the
  fork verdict; accepted from record (re-verifying needs the round-1 fixtures).
- One self-caught tooling bug is documented in RUNLOG.md (units error in a
  first-draft verifier, fixed and re-verified); no committed figure was
  affected.
