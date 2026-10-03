# LOO_REPORT.md — Scale Epistemic Attempt 3, train LOO (2026-09-27)

Label-blind report. No scores computed. No labels consulted.

## Frozen inputs
- Prereg: `~/workspace/epi_a3/PREREG_ATTEMPT3.md`
  SHA-256: `497fe9f8436b0cc761898ad4cbba16926521b2426a5be12ec08859ef19e20c46`
  (verified unchanged before build and before LOO)
- Train: `~/workspace/epi_a3/blind/train_blind.tsv` (448 rows, T0001–T0448)
- Held-out: `~/workspace/epi_a3/blind/heldout_blind.tsv` (192 rows, H0001–H0192)
  — NOT run. Awaiting coordinator GO.

## Frozen build (parser/tables)
- Source: `build_parse.py`
  SHA-256: `b038d1fa1ab146a5e6643d52198425e8d8a4949e623bb5129cac947d85131cf7`
- Artifacts:
  - `frames.tsv`: `9a7f39345ed0bcda3c4297ce5b65fd7c31b5ba26ad537481f38e84e71d2b38f2`
  - `address.tsv`: `3a45b052dfa32c59198c6ba246d872f5743118cb5f1591529df6921f51f1a465`
  - `vocab.tsv`: `45fc45d17289a8fa0625e0c73213db3e06e5f3751b89fb874d87816f2e48a7d5`
  - `idmap.tsv`: `5537388caed1a7750cdc89f261d2599fa22fd943d10102365d773634d89b2c47`
  - `classmeta.tsv`: `8df5f142d1dc0ce2fc1375837201488f1304eebbc507d6bc1a0417bb808cdd88`
  - `antonym.tsv`: `dba639d78a52614171b8913577e074ca6785cf9259faf1c3e2719db8cdb4ba87`
  - `massaddr.tsv`: `9022e58657279183b4452e22867fba78d1b2b4f4576309fdd2acbd42235a6088`
- Full freeze record: `FREEZE.sha`
- Linguistic tables documented in `TABLES.md` (all labeled
  "general linguistic knowledge — no label exposure")
- Takeaways: `takeaways.md` is a byte-identical copy of `takeaways_a2.md`
  (SHA-256 `e4c919eee8d5a89e4fba76c2aa4e3ce573163aec4155eb570af2e4ebd02e59e8`;
  26 cited IDs all match `^[FOLS][0-9]+$`)

## Build statistics (label-blind)
- Items: 640 (448 train + 192 held-out index)
- Syntactic frame well-formedness: 640/640 = 1.0000 (bar: ≥0.90) ✓
- Premises: 684
- Addressing rows: 985 (train+heldout index; LOO uses train addressers only)
- Items with ≥1 non-self address: 214/640
- Item types: EVALUATIVE 171, FACTUAL 438, CAUSAL 25, DEONTIC 6
- Build is byte-deterministic across reruns (sha256 verified)

## Deliberation
- Source: `deliberate.zag`
  SHA-256: `9edf2448e05aa08048ad458edd621b924fcf60755451f029733d69ef4b8802df`
- Pure Zag, zero RNG. Implements prereg §4: comparison (SUPPORT/CONTRADICT/
  TOPICAL), premise status, uncontested-standing contradictor check,
  verdict ordering (opinion → lie → fact → contested → undetermined),
  causally bound NEED emission from UNADDRESSED premises.
- Standing level: **uncontested-standing** (initial). No escalation performed;
  escalation is the coordinator's mechanical decision per prereg §6.
- Train LOO excludes all self-originating train addresses; the LOO owner is
  excluded from the contradictor-standing mass.

## LOO outputs (train, 448 items)
- `loo_verdicts.tsv`:
  SHA-256: `30855a90a39604d434e641b3b8ed1007faed114caf9475d6200fbd5b4df63a2e`
- `loo_needs.tsv` (344 rows):
  SHA-256: `7c983fdbdb885f13f405159a389e54fc12d437244bfd1bcdb931a13c38502edb`

### Verdict distribution (label-blind)
| verdict | count |
|---|---|
| lie | 9 |
| opinion | 119 |
| undetermined | 320 |
| fact | 0 |

### Premise status counts (label-blind, from traces)
| status | premises |
|---|---|
| CONTRADICTED | 11 (9 p0 + 2 p1; all with ≥1 standing contradictor) |
| UNADDRESSED | 344 |
| SUPPORTED | 0 |
| CONTESTED | 0 |

Note: zero SUPPORTED is a corpus property, independently cross-checked in
Python: among train non-self addressing pairs, zero pairs satisfy the
prereg SUPPORT condition (same vkind + same vcode + same polarity). The
corpus contains no exact-duplicate claims. Consequently CONTESTED (which
requires a SUPPORT) is also zero, and the fact verdict (all-supported) is
unreachable on this corpus.

### NEED emission (label-blind)
- 344 NEED rows, one per UNADDRESSED premise (plus non-standing-contradicted
  premises) in undetermined verdicts.
- Format: `NEED: <ent0> | <ahead> <aclass> <adim>`, emitted from the same
  deliberation branch that produced the undetermined verdict (causal binding).

## Determinism
- Train LOO run twice; `loo_verdicts.tsv` and `loo_needs.tsv` byte-identical
  across both runs (sha256 verified).
- Deliberation binary removed after runs (not retained).

## Coordinator decision needed
- GO/NO-GO for held-out run.
- Standing escalation check (fact→lie false positives) is the coordinator's
  per prereg §6; the implementer has not seen labels and performed no
  escalation.
