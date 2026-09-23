# TNN Documentation Index

Master table of contents for the True Neural Network (TNN) research archive.

## Layout

- `program/` — charter, autonomy position, architecture, evaluation doctrine, living status map.
- `hypotheses/` — one falsifiable claim per file, with an evidence table linking experiments to results.
- `generations/` — R27 through R33, each with its own `INDEX.md`, handoff, reports, and per-experiment directories.
- `lab/` — the active native-lab waves. Headline results: `lab/wave6/doc-front/INTEGRITY_HEADLINE.md` (wave-5 integrity) and `lab/prose-learning/epistemic_wave/speechact_exp/SPEECH_ACT_HEADLINE.md` (speech-act learning: 7.1% to 50.0%).

## Conventions

### Status vocabulary (controlled)

Every research document carries a `status:` field using TNN's existing blunt vocabulary.
Do not sanitize failures; a negative result is a result.

- `CANONICAL` — the settled reference (e.g. R27 at step 60,423).
- `REFERENCE_ONLY` — produced by a shadow/substitute system, not the native target. Never promote.
- `NEGATIVE` — the experiment ran and the hypothesis failed. Keep and cite.
- `BLOCKED` — cannot proceed; the blocker must be named.
- `PROVISIONAL` — claimed but awaiting independent confirmation.
- `SUPERSEDED` — replaced by a later document; the pointer must name the replacement.
- `CONSUMED` — evidence admitted and closed; do not rerun.

### Document frontmatter

Every research doc starts with:

```yaml
---
id: R32-E45            # stable document id
title: "..."
generation: R32
status: NEGATIVE
hypotheses: [H-03, H-07]   # which hypothesis files this bears on
artifacts: artifacts/by-experiment/R32/E45/
updated: 2026-09-19
---
```

### Manifests

`data/manifest.json` and `artifacts/manifest.json` record every tracked file:

```json
{
  "path": "artifacts/by-experiment/R32/E45/seed-9714.joblib",
  "sha256": "...",
  "kind": "model-state | log | metrics | input | figure | source",
  "experiment": "R32/E45",
  "status": "NEGATIVE",
  "produced_by": "github-actions run 33944536498",
  "frozen": "2026-09-05",
  "original_path": "Research/R32_V16_...log"
}
```

`original_path` preserves the pre-reorganization location so old references stay resolvable.

### Filename rules

- Short canonical IDs: `E45/`, `seed-9714.joblib`, `handoff.md`.
- At most one status token in a filename (`REFERENCE_ONLY`, `NEGATIVE`); the rest belongs in frontmatter.
- Never commit: `*.openai-download-*`, `*.b64` (when a decoded original exists), transfer-staging contents.

### Directory indexes

Every meaningful directory has an `INDEX.md`: what lives here, its status, and where to start reading.
