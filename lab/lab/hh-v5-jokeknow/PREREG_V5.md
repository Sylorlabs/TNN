# PREREG — Hell-Hole V5: joke-knowledge ceiling experiment (2026-09-24)

## Hypothesis (Micah's ruling under test)
The V4 joke classifier's "architecture ceiling" (~30% recall on the RT3e
natural blind set; 26 of 28 misses needing semantic comprehension) is
**knowledge, not architecture**: the shipped V4 architecture can deliberately
acquire and use dual-meaning/pun knowledge, idiom knowledge, world facts, and
phonetic knowledge at volume, via pure Zag mechanisms, with zero RNG and
byte-identical reruns.

## Starting state (frozen)
- Source: shipped V4 `g_intent6_v4fix4.zag`, commit
  `de01f387f825c7294cb880040ef99d7fafa45700` (tnn-native-lab).
- Reproduced baseline 2026-09-24: RT3e jokes 12/40 JOKING, deadpan 0/40 JOKING.
  - jokes SHA: `2f0f0d55fb6ab6aac635f018ec6842d670c0176f36475eb70aa38158a7fa716d`
  - deadpan SHA: `569adb5a3e1d99131edc2da6a8fce4b60bb45a0926cde4dc93b04b4f88d4126`
- Worktree: `~/workspace/hh-v5-jokeknow/base/` (immutable reference).

## What we build
1. **Knowledge stores** (`stores/*.tsv`, deliberately-managed memory):
   `pun.tsv` (~200 dual meanings), `idiom.tsv` (~200 idioms),
   `world.tsv` (~200 facts), `phon.tsv` (~150 sound-alikes).
   Authoring constraints: lowercase ASCII, no joke texts, sorted, deduped,
   cues evoke real senses/facts (not joke trigger wording), breadth beyond RT3e.
2. **Knowledge interpreters** (`rules/k_rules.zag`, pure Zag, zero RNG):
   general mechanisms, one per partition, each enforcing
   **shape + genuine incongruity turn**:
   - `K_PUN`: dual-meaning word + sense-A and sense-B cues in DIFFERENT
     discourse segments (boundary between them = the turn).
   - `K_QA_PUN`: riddle shape ("?" boundary) + answer reinterprets a
     dual-meaning word the question cued.
   - `K_IDIOM`: idiom + literal-play cue across a discourse boundary, or a
     substantive multi-word literal definition before the idiom.
   - `K_WORLD`: entity + violation cue (text contradicts/plays against fact).
   - `K_PHON`: written word + alt-meaning cues evoking the OTHER reading.
   Knowledge NEVER fires on shape alone. All rules appended with `contra==0`
   guards: nothing previously caught changes verdict.
3. **Volume tiers**: T0 (no knowledge) / T25 / T50 / T100 by deterministic
   interleave of the alphabetically sorted stores (no handpicking).
   Converter: `rules/tsv2zag.py` (validates + emits `k_tables.zag`).

## Experiment legs
- **L1 baseline fidelity**: T0 reproduces the RT3e baseline byte-identically.
- **L2 volume curve**: recall (total + by knowledge class) on RT3e jokes at
  T0/T25/T50/T100. Expect monotonic rise on the taught classes.
- **L3 partition ablation**: pun-only / idiom-only / world-only / phon-only /
  all. Each gain must vanish when its partition is removed.
- **L4 known-ceiling diagnostic**: RT3e rerun (diagnostic only, not headline).
  Expect recovery of the knowledge-ceiling misses (phonetic duality, novel
  dual meanings, idioms, world facts); pragmatic-inference misses
  (J05/J09/J21/J22/J25/J30) and hyperbole (J36) are expected to remain —
  they are the architectural-limit probe, not knowledge gaps.
- **L5 fresh blind red teams** (HEADLINE EVIDENCE): novel joke + sincere
  corpora, authored blind to the implementation, attacking each partition:
  sincere items containing learned words/facts but NO incongruity turn
  (must stay UNCERTAIN), novel jokes using the knowledge (recall measured),
  paraphrases, concepts absent from RT3e. Kill bar: **zero deadpan installs**.
- **L6 counterfactuals**: entry present + one sense only → withhold; both
  senses but no turn → withhold; genuine collision → install; remove
  partition/entry → gain disappears; irrelevant additions → no change.
- **L7 determinism**: ≥3 byte-identical runs per final leg; zero-RNG audit.
- **L8 regression**: all prior corpora (frozen30, neg sets, rt3* outputs)
  unchanged except additive knowledge catches; deadpan installs stay zero.

## Verdict rules (preregistered)
- **MICAH RIGHT**: deliberately acquired knowledge materially raises FRESH
  BLIND joke recall (L5) while deadpan installs remain zero (L5+L8).
- **MIXED**: only some classes rise, or a mechanism boundary remains visible
  (e.g. pragmatic inference / hyperbole stay flat while knowledge classes rise).
- **ARCHITECTURE LIMIT**: correct knowledge is installed and activated in
  text but the architecture cannot compose it into incongruity judgments
  (L6 counterfactuals fail: both senses present + turn present → no install).

## Commit
Full research (prereg, sources, corpora SHAs, run logs, ablations, red-team
reports, verdict) to tnn-native-lab. No binaries, no `.zagd`/cache files.
Provenance to the V4 shipped commit preserved.
