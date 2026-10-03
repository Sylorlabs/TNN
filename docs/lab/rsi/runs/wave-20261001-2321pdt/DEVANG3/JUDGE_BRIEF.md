# JUDGE_BRIEF.md: DEVANG3 (wave-20261001-2321pdt)

## Provenance

- RENDER_SHA: `11026f43b` (sealed evaluation commit; full chain below)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: DEVANG1 BUILD-FAIL (lexicon crash, root cause never
  isolated) -> DEVANG2 retry BUILD-FAIL (cold-start repair architecturally
  inert; bigram statistics were segmentation-independent by construction)
  -> DEVANG3 (2021pdt) BUILD-FAIL on segmenter quality (K_SEG 8/12,
  K_SEAL 11/20; K_AUD PASS confirmed mechanism result, not architectural
  recurrence) -> DEVANG3 (this wave) BUILD-PASS.
- NEW_KNOWLEDGE_CLAIM: Flipping the novel-segment length term from a bonus
  to a linear penalty fixes the merge pathology (K_SEG 8/12 to 12/12) and
  supports post-freeze generalization (K_SEAL 11/20 to 20/20) with a
  one-line change and no new mechanism.

## Commit chain (all local, branch tnn-native-lab, no pushes)

1. `5b7e55706`: prereg frozen ALONE (PREREG_DEVANG3.md, NAMECHECK.md).
2. `126ef2600`: implementation (one scoring line + comments; binary
   `36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d`).
3. `ead6f006c`: fresh sealed Family B/C package (generators, sealed files,
   keys, notes; sha256 recorded pre-run).
4. `11026f43b`: sealed evaluation (this brief's RENDER_SHA).

Commit order verified: prereg strictly precedes implementation, which
strictly precedes the sealed package, which strictly precedes the sealed
run. No implementation file predates the prereg freeze.

## Verdict: BUILD-PASS

| Bar | Threshold | Result |
|-----|-----------|--------|
| KR0 | 3/3 exit 0, zero stderr | PASS |
| K1 | >= 8/10 | 10/10 PASS |
| K_SEG (fresh B) | >= 9/12 | 12/12 PASS |
| K_SEAL (fresh C) | >= 12/20 | 20/20 PASS |
| K_AUD | code audit | PASS |
| K_ABL (fresh B) | <= 5/12 | 4/12 PASS |
| K_C0 (Family A) | >= 15pp and >= 3 words | 35pp, 7 words PASS |
| K8 | >= 15pp vs best control | PASS (20/20 vs 17/20) |
| K2..K7,K9 | >= 4 of 7 | 7/7 PASS |
| K10, K11 | code audit | PASS |
| K12 | 3/3 byte-identical | PASS |

Regression (2021pdt worlds): Family B 12/12 (was 8/12); Family C 11/20
(was 11/20). No regressions.

## What changed

One line in `seg_dp`: novel-segment score from `-50 + ilog(L+1)*5`
(length bonus) to `-50 - 1*L` (linear length penalty). The bonus rewarded
merging a novel word with an adjacent known word; the penalty restores the
character-level intuition that longer novel strings cost more. Cognition
lines added: 1 (cap was 120). No new tables, modes, bridges, handlers, or
semantic cases. The C0 control is untouched.

## Limitations (for the judge)

1. No independent adversary worker this wave. Mitigation: fresh vocabulary
   and fresh episode selections, blind generation (hashes committed before
   the sealed run, no inspection between generation and run).
2. The fresh Family C uses 3-char content words, so the fixed-width-3
   control also scores 20/20 there. Discrimination comes from K_SEG
   (12/12 vs 4/12) and K8, not from Family C. Documented 2-char words as
   a cold-start limitation; 4-5 char words in variable positions are
   fragile under this segmenter.
3. This is developmental L2 evidence (lexicon discovery under a
   researcher-designed interpretation skeleton), not L3 or a generality
   claim.

## Evidence paths

- Prereg: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/PREREG_DEVANG3.md`
- Implementation: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/devang3.zag`
- Sealed package: `docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/sealed/`
- Sealed notes: `SEALED_B.md`, `SEALED_C.md` (pre-run sha256)
- Results: `SEALED_EVAL.md`, `IMPLEMENTATION.md`, `BUILD-LOG.md`
