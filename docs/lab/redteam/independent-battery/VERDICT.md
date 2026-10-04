# INDEPENDENT BATTERY — VERDICT (red-team attacks #2 and #4)

Frozen prereg: `PREREG.md` (commit `d7657741`, 2026-09-22).
Protocol: process-separated, disjoint vocabulary, no kind labels, hidden corruption,
novel compositions, truth/provenance/abstention scoring.

## Battery (stranger-authored)

- Domain: the Virellian Exchange (canal-harbor federation). Classes broker/courier/pilot/weigher,
  12 member names, 7 verbs, invented goods. Zero overlap with prior lab vocabulary.
- 48 teach (28 D1, 12 D2, 4 D3, 4 D4) + 72 probes (12 per capability), 120 wire items.
- Corruption (sealed until scoring): 6/28 D1 = 21.4% — 2 principle-violations,
  2 inter-claim contradictions, 2 smooth lies (ids 2, 4, 6, 36, 39, 43 post-shuffle).
- Generator: `gen_indep.py`, seed `20260921`, byte-identical on rerun.
- Learner: `indep.zag` (pure Zag), frozen before the battery existed; debugged only
  against the author's own synthetic sample, never against this battery.

## Scores

| cap | n | correct | independent | coupled (old headline) | gap |
|---|---|---|---|---|---|
| contra | 12 | 12 | **1.0000** | 1.0000 (156/156) | +0.0000 |
| false | 12 | 12 | **1.0000** | 1.0000 (13/13) | +0.0000 |
| para | 12 | 1 | **0.0833** | 0.9649 (Sol prose-v1) | **+0.8816** |
| truth | 12 | 8 | **0.6667** | n/a (no prior instrument) | n/a |
| abstain | 12 | 12 | **1.0000** | n/a | n/a |
| prov | 12 | 12 | **1.0000** | n/a | n/a |

- Mirror baseline (truth): 0.5000. Learner 0.6667 > mirror → "truthful" qualifier survives.
- Parse coverage: 72/72 probes parsed, 0 unparseable, 0 silent skips.
- Determinism: 5/5 runs byte-identical (`cf958e2036fd7cd5040c9ee15e7f0c1f`).
- Source audit: `indep.zag` contains no reference to `expected.json`
  (single "expected" hit is a comment asserting NO expected answers);
  binary contains no such string; only file opened is `items.jsonl`.

## Kill bars (applied mechanically)

- **KB-GAP(contra): HOLD.** The 156/156 contradiction headline survives a stranger's battery,
  including 4 principle-mediated conflicts. Attack #2 fails here: contradiction
  detection is a real capability, not a generator artifact.
- **KB-GAP(false): HOLD.** 13/13 principle-derived falsehood detection reproduces at 12/12
  with zero false alarms. Real.
- **KB-GAP(para): TRIPPED.** Gap 0.8816 > 0.30 → the old "0.9649 paraphrase" headline is
  reclassified **GENERATOR-COUPLED** and revised to **0.0833** on the independent battery.
- **KB-TRUTH: HOLD.** 0.6667 > mirror 0.5000. First "does it believe true things?" instrument:
  the learner is truthful-but-mirroring (see misses), not a parrot and not a liar.
- **KB-DET: HOLD.**

## What the misses say (mechanism-level)

**Paraphrase (1/12).** 10 misses are single-sided synonym swaps (ships/exports,
guides/steers, hauls/ferries, measures/weighs, tunes/calibrates, conveys/carries):
the synonym never appears in teach, so no wire information supports the mapping —
prose-v1's bag-of-words mechanism cannot know them. The 1 hit was passive-voice-only
(syntactic), which BoW survives. Correction to the frozen table: the coupled 0.9649
was Sol's *clean mastery* (220/228 canonically-worded facts), never a paraphrase
measurement — the independent battery is the program's first real paraphrase-robustness
instrument, and this is its first reading. One further miss (Q2 "which broker ships
dried figs?"): two names match the *taught* claims because a corrupt D1 ("Maren
exports dried figs", id 36) duplicates Sarella's true claim; the learner abstained on
non-uniqueness — reasonable under corruption, scored a miss per frozen rules.

**Truth (8/12).** Two misses are smooth lies the learner affirmed ("Kessa weighs iron
weights", "Nessia exports cedar planks", corrupt ids 43/6): pure mirroring, exactly what
the instrument was built to detect — with no independent evidence, taught lies are
believed. One miss is a genuine capability gap: "Sarella insures copper bonds" is
entailed by chaining D2 ("Sarella is a broker") through D3 ("Every broker insures
copper bonds") but never taught as a D1 — the champion instantiates principles only
to *reject*, never to *entail*. One miss is a generator-severity note: "Maren exports
salt" (true, id 27) was REJECTED because the taught inter-claim contradiction
("Maren exports dried figs", corrupt id 36) fired the learner's conflict detector;
the expected AFFIRM requires knowing which of the two taught claims is the planted
lie — unknowable from the wire. Scored a miss per frozen rules; flagged, not excused.

## Bottom line for Micah

- Contradiction 1.0000 and principle-falsehood 1.0000 are **real** — they survived a
  hostile stranger's battery with new words, new tricks, and hidden lies.
- Paraphrase 0.9649 was **never measured before**; first real reading is 0.0833 on
  synonym swaps. Syntactic paraphrase works; synonym knowledge is the missing organ.
- The program now has a truth instrument: 0.6667 vs a 0.5000 mirror baseline.
  The learner believes taught smooth lies (mirroring) and cannot yet entail through
  principles — both are now quantified, not suspected.

## Reproduction

- Binary sha256 of the scored build is in `SHA256SUMS` (binary itself not committed,
  per lab convention; rebuild: pinned znc `abed8aa1` on `indep.zag` + the two
  `R33_*` substrate files in this directory).
- `SCORES.md` is the scorer's machine output; this file is the human verdict.
- `runs/run1..5.log` are the five byte-identical scored runs.
