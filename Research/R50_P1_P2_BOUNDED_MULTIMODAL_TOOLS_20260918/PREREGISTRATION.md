# R50 bounded P1/P2 language, tools, vision, hearing, and grounding — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EVALUATION**

R50 advances the longer-program P1/P2 tracks using synthetic, exact-verifier tasks. It deliberately does not relabel these as broad natural language, natural connected speech, or real-world vision.

## Frozen tracks

1. **Grounded compositional language**: learn arbitrary fresh word and relation tokens from grounded demonstrations, then execute unseen object-relation compositions and emit provenance-bearing explanations.
2. **Generic tool sequencing**: learn a hashed bag-of-words mapping from instructions to generic tool plans (`READ`, `SEARCH+READ`, `WRITE+TEST`, `CALCULATE`, `INSPECT+TEST`) using train templates; evaluate on held-out templates.
3. **Synthetic vision**: learn visual categories from raw 8×8 arrays across translation/noise, evaluate unseen placements and occlusion, and use uncertainty-triggered reinspection.
4. **Object persistence**: track a moving point through a hidden frame using observed velocity.
5. **Synthetic hearing**: learn acoustic motifs from raw waveforms across training speakers, evaluate held-out speaker/amplitude/phase/noise conditions, and recognize held-out motif compositions as phrases.
6. **Cross-modal grounding**: learn arbitrary visual↔audio concept correspondences only from co-occurrence, then retrieve on held-out examples.

## Gates

- grounded language novel-composition accuracy >= 0.90;
- tool-plan accuracy on held-out templates >= 0.85 and materially above update-disabled control;
- vision held-out accuracy >= 0.85, occluded accuracy >= 0.70, active reinspection improves or preserves accuracy while using fewer than all second views;
- object-persistence interpolation >= 0.95;
- acoustic motif accuracy >= 0.85 and phrase accuracy >= 0.80 on held-out speakers;
- cross-modal retrieval >= 0.90;
- all labels/tokens are randomized by the evaluator and the randomized literals are absent from source before execution.

`learn_authority=0`; canonical R27 remains unchanged.

