# SELF-PAM Battery — Sealed Corpora v1

**Authority:** frozen prereg `../PREREG.md` (commit `204b82831bbabd7dc2918f07d3a5ad75c9842e53`).
**Status:** SEALED. Corpora committed with SHA-256 manifests; generators
archived. No measurement has run against these corpora.

## Seal statement

- **Zero RNG.** All corpora are pure combinatorial constructions over fixed
  pools (no `random` module, no seeds). Regeneration is byte-identical
  (verified: 8/8 corpus files identical across two independent runs).
- **Manifests.** Every cell directory carries `MANIFEST.sha256`
  (`sha256sum -c` verifiable). Top-level `SHASUMS` pins every corpus file.
- **Generators archived** under `generators/` (world.py, gen_main.py,
  gen_cella.py, make_manifests.py, validate.py).

## Inventory

| Cell | Corpus | Count vs frozen minimum |
|---|---|---|
| CELL-A | `cell-a/` — pins the frozen 1,200 R2P pairs (sealed upstream manifest copied as `r2p_manifest.sha256`; not duplicated) | 1,200 pairs = minimum |
| CELL-C1 | `cell-c1/c1_drafts.jsonl` + `world/` store & gaps | 1,152 gap drafts (≥500), 576 held drafts (≥500) |
| CELL-C2 | `cell-c2/c2_tasks.jsonl` | 600 tasks (≥500), warranted+unwarranted drafts each |
| CELL-C3 | `cell-c3/c3_items.jsonl` | 600 items (≥500), 120/mode × 5 modes |
| CELL-W | `cell-w/w_claims.jsonl` | 360 true-but-ungrounded claims (≥300) |
| CELL-P | `cell-p/p_drafts.jsonl` + `WARRANT_VOCAB.md` | 600 drafts (≥500), 510 admissible / 90 defective |
| CELL-D | `cell-d/d_dialogues.jsonl` | 20 dialogues × 50 turns (≥20×50), 2 planted conflicts each |
| CELL-R-conf | `redteam/` (sibling red-team crew, blind) | 305 SCORED (≥300) |
| CELL-R-deny | `redteam/` (sibling red-team crew, blind) | 182 SCORED + 32 TENSION = 214 warranted-true attacked (≥200) |
| CELL-S | `cell-s/REUSE.md` — reuses C1/C2/C3/W/D corpora | no new corpus (per prereg) |

## Provenance notes

- `world/` (store.jsonl: 144 committed facts; gaps.jsonl: 144 KNOWN gaps
  with oracle-TRUE, store-unwarrantable claims) is the seeded memory store
  shared by CELL-C1/C2/W/P/D. Gap attributes (birthplaces, founding years,
  chroniclers, builders) are absent from the store by construction
  (machine-checked in `generators/validate.py`).
- `redteam/` was built blind by the sibling red-team crew from committed
  artifacts only (no shared state with this battery). Adopted unmodified;
  its seal (`MANIFEST.sha256`, 34/34 OK) was re-verified before this
  commit. See `redteam/README.md`, `redteam/DESIGN.md`, `redteam/RUNBOOK.md`.
- `cell-a/` pins the R2-3 crew's sealed fixture set; the pairs themselves
  live at `docs/lab/senses/pam-rebuild/round2/fixtures/r2p/`.

## Standing by

The integration build (`src/` + `build.py` + `verify.py`) has NOT landed on
branch `tnn-native-lab` as of this commit. Per the prereg sequencing rule,
**no cell has been executed**: no `report.txt`, no `ledger.txt`, no verdict.
Execution order when the build lands (§7): CELL-P first (cheapest), then
CELL-C1/C2 (+CELL-W, CELL-D alongside), then CELL-C3, then CELL-S;
CELL-A before any install-path claim is trusted. Kill at the cheapest
failing step. No cell counts as run until its evidence is committed under
`selfpam/evidence/<CELL>/`.

Pre-build blockers still open (§8): Micah's threshold sign-off, frozen
probe charter, FACT-type tolerance table, marked-emission format. The
corpus manifests (this commit) close §8 blocker #5.
