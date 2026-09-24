# RUNLOG — hell-hole V5 joke-knowledge experiment (2026-09-24)

## Baseline (reproduced)
- V4 shipped source rebuilt with pinned znc; RT3e rerun byte-identical:
  jokes 12/40 JOKING, deadpan 0/40 JOKING.
- Worktree: `base/` (immutable), `corpora/rt3e_*.tsv`, `runs/base_*`.

## Knowledge design
- `KNOWLEDGE_SPEC.md`: 4 partitions (pun/idiom/world/phon), shape+turn discipline.
- `rules/k_rules.zag`: general interpreters (K_PUN, K_QA_PUN, K_IDIOM, K_WORLD, K_PHON).
  - k_pun_turn: dual-meaning word + sense cues in different segments, STRICT pivot (contrast/;/ ?/! — not bare sentence break).
  - k_idiom_turn: idiom + literal-play cue across boundary, or substantive multi-word literal definition.
  - k_world_turn: entity + violation cue.
  - k_phon_turn: written word + ≥2 DISTINCT alt-meaning cues.
  - Matching: stem-aware single words (k_stem_pos), ordered-words multi-word (gaps allowed, 80ch span).
- `rules/tsv2zag.py`: validates + emits tables; deterministic interleave tiers.
- `rules/build_v5k.py`, `rules/build_tier.py`: assemble + compile + 2x determinism.

## Mechanism refinements (from counterfactuals)
- C04 ("seafood diet" FP) → K_PHON now needs ≥2 distinct alt cues.
- C11 ("bank... lost interest" FP) → K_PUN uses strict pivot (no bare ". ").
- All 12 counterfactuals now correct; RT3e holds 32/40, deadpan 0/40.

## Dev-set results (RT3e diagnostic, small hand tables)
- 12 → 32/40 jokes (+20), deadpan 0/40.
- Recovered: J03,J04,J32,J35 (phon); J06,J28,J29,J33 (pun); J15,J18,J34,J39 (idiom); J12,J17,J19,J23,J24,J26,J27,J31 (world).
- Still missed: J05,J09,J21,J22,J25,J30 (pragmatic inference), J36 (hyperbole), J37 (pragmatic). Expected: not knowledge gaps.

## Stores (complete 2026-09-24)
- pun.tsv: 234 entries (two halves merged). idiom.tsv: 201. world.tsv: 207. phon.tsv: 150.
- Total 792 entries. All validate (tsv2zag.py).
- Authoring gaps fixed: idiom literal-play cues (were idiom's own words for 3 ceiling items), world violation cues (kitkat/siri/true crime), pun collocates (interest/problems/uplift/working on/break needed "lost interest", "banker", "sad", "elevator", "construction").

## T100 results (RT3e diagnostic)
- Jokes: 32/40 (baseline 12 + 20 knowledge). Deadpan: 0/40 (SHA byte-identical to baseline: `569adb5a...`).
- Newly caught: J03,J04,J32,J35 (phon); J06,J28,J29,J33 (pun); J15,J18,J34,J39 (idiom); J12,J17,J19,J23,J24,J26,J27,J31 (world).
- Missed: J05,J09,J21,J22,J25,J30,J37 (pragmatic inference), J36 (hyperbole). Expected.

## Volume curve (RT3e jokes / deadpan)
- T0: 12/40, 0 deadpan. T25: 18/40, 0. T50: 25/40, 0. T100: 32/40, 0.
- Monotonic rise; deadpan holds at zero throughout.

## Ablations (RT3e jokes; each = baseline 12 + partition items)
- abl_pun: 16 (+J06,J28,J29,J33). abl_idiom: 16 (+J15,J18,J34,J39).
- abl_world: 20 (+J12,J17,J19,J23,J24,J26,J27,J31). abl_phon: 16 (+J03,J04,J32,J35).
- Each gain vanishes when its partition is removed. Clean.

## Determinism
- T100: 3x byte-identical on jokes (`5fe21fc1...`) and deadpan (`569adb5a...`, = baseline SHA).

## Blind red teams (dispatched 2026-09-24)
- Team A: 60 novel jokes (~15/partition) → corpora/rt5_jokes.tsv.
- Team B: 60 sincere traps (T1..T5) → corpora/rt5_sincere.tsv.
- Both blind to implementation; kill bar = zero sincere installs.

## TODO
1. Run blind corpora on T100 (headline evidence).
2. Expanded counterfactual battery on T100.
3. Regression on prior corpora (frozen30, neg sets).
4. Verdict + commit to tnn-native-lab.
