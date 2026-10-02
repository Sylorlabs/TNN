# TA-CORPUS v1 — Self-PAM text-approximate corpus

**Sealed:** 2026-09-28 (builder wave). **Status after seal: READ-ONLY to the builder.**

## Contents

| file | rows | description |
|---|---|---|
| `evidence.jsonl` | 200 | Atlas-7 stipulated evidence claims (Meridian Archipelago, invented domain) |
| `episodes.jsonl` | 64 | Derivation teaching episodes (P, Q, kind, warrant) for H-TA1 |
| `edges.jsonl` | 64 | Reference edges extracted from episodes (Python reference implementation) |
| `refused.log` | — | Edge candidates refused by the polarity constraint (0 refused) |
| `items.jsonl` | 950 | Scored main items (dual-labeled, adjudicated) |
| `stress.jsonl` | 450 | Stress sets: RECOMB 200 / TRANS-CHAIN 100 / LOW-OVERLAP 150 |
| `audit.jsonl` | 1454 | Per-item pass1/pass2/adjudication record |
| `adjudication_log.md` | — | Disagreement log + selection-to-quota record |
| `atlas7_fact_table.md` | — | Human-readable evidence table |
| `SHASUMS` | — | SHA-256 of every file + every item (seal manifest) |

## Class counts (main, 950)

IDENT 60 · PARA-LEGIT 200 · REL-SUBSET 90 · REL-ENTAIL 60 ·
CONFAB-GENUINE 200 · CONFAB-NEAR-MISS 120 · MEANING-SHIFT 120 · ADV-PARA 100

Stress (450, mechanism bars only, never feed shared kill bars):
RECOMB 200 · TRANS-CHAIN 100 · LOW-OVERLAP 150.

## Labels

- `expected`: ADMIT / WITHHOLD / PER-HYPOTHESIS (REL-ENTAIL only).
- `label_pass1`: generator recipe label. `label_pass2`: independent re-derivation
  (see `generators/audit_labels.py`). Audit agreement: 1454/1454.
- `evidence_ids`: cited Atlas-7 claims. `trap_notes`: adversarial intent
  (ADV-PARA, RECOMB, TRANS-CHAIN, LOW-OVERLAP).

## Regeneration (seal check)

```bash
cd generators
python3 gen_evidence.py && python3 gen_episodes.py && python3 gen_items.py \
  && python3 gen_stress.py && python3 audit_labels.py && python3 select_corpus.py
python3 make_manifest.py --check   # byte-compares against SHASUMS
```

Fixed seeds: evidence `20260928`, episodes `20260928`, items `20260929`,
stress `20260930`. Zero runtime RNG in the sealed artifacts beyond these seeds.
The seal check regenerates into a fresh directory and byte-diffs every file.

## Provenance

- Generators: `generators/` (committed with the build package, not the corpus).
- Style guide + 60-pair S1 substitution map + 191-token closed-class list:
  `generators/style_guide.md`, `generators/submap.py`, `generators/closed_class.txt`.
- Label rubric: `generators/label_rubric.md`.
- Derivation episodes built from evidence + style guide only, seed independent
  of sealed drafts (no-bridge rule, prereg §7).
- Prereg: `docs/lab/senses/pam-rebuild/selfpam/text_approx_2026-09-28/PREREG_TA.md`
  (committed b92e3937e4c21a8a1168c931a9ed737a4b143f58, BEFORE this seal).

## Rules after seal

1. The builder never scores the sealed corpus (tester crew does).
2. No tuning against sealed items. Constants freeze on the OPEN dev set (≤50).
3. Any change requires a prereg amendment committed BEFORE re-measurement.
