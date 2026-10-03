# RESULTS: CLAIM-VERIFY-1 implementation bars (wave-20260924-1121pdt)

Implementation verdict scope only: sealed scoring (CV-B1, CV-B6 seal-open) is
the coordinator's later step. Bars below are measured against the frozen
training fixtures (30 adversarial probes, 17 in-KB turns), the frozen KB, and
the frozen baseline.

## CV-B2 (no regression): PASS

- 17/17 in-KB turns byte-identical to the frozen baseline: cmp
  cand_kb2_r1.txt base_kb2_r1.txt clean; sha256
  e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264
  for both.
- 30/30 frozen adversarial training probes resolve as specific declines:
  30/30 lines match "tnn> [decline]", 30/30 contain quoted specific content
  words, 0 blanket refusals. Full per-probe table in runs/per_probe_kb1.md.
- Note (disclosed, not a bar failure): 9 of the 30 decline lines differ from
  the frozen baseline in the cited words or template, all still specific
  declines in the frozen "contains nothing about" template. Causes, all
  prereg-specified consequences of replacing word-literal match with
  coverage deliberation: (a) no stemming, so inflected forms such as
  "discover" and "win" are cited as uncovered where the baseline stemmer
  matched them; (b) uncovered words are computed relative to the
  maximum-overlap fact rather than the global unknown-word list; (c) one
  decline template instead of the baseline's D-B/D-C template mix.

## CV-B3 (determinism): PASS

- 3/3 full reruns byte-identical on both fixtures: transcripts identical
  (cmp clean across r1/r2/r3 for KB1 and KB2) and per-turn op-count streams
  identical (cmp clean across r1/r2/r3 .ops files).
- Zero RNG in any decision path: static grep over cv1.zag for
  rand/rdtsc/getentropy/urandom/systime/clock_gettime finds nothing outside
  comments; the candidate's only entropy-free inputs are the turn bytes and
  the frozen tables. deliberate_cv1 has exactly four return points (three
  decline paths, one single-fact selection); no data-dependent branching on
  anything but the input and the frozen KB.

## CV-B4 (cost): PASS, ratio 1.80x (bar: at most 10x)

- On the prereg's F6: no frozen op-counter artifact exists in the repo;
  archived evidence shows the cited 1.048x figure was wall-clock timing, not
  an op count. What was built instead (documented, comparable): a pure-Zag
  decision-op counter threaded through the frozen deliberate() and its
  helpers (gate_op.zag), verified to produce byte-identical stdout to the
  frozen baseline on both fixtures, so the instrument measures the same
  behavior it counts. Counting discipline, identical for both engines: one op
  per token/id comparison loop iteration; byte moves and output formatting
  not counted. Candidate counts its own deliberation (canonicalization,
  coverage scan over 38 facts, claim splitting, substring verification) under
  the same discipline.
- Same 30 training probes, per-turn mean ops: baseline 376.333 (sum 11290),
  candidate 677.4 (sum 20322). Ratio 677.4 / 376.333 = 1.80x. Within the
  prereg's expected 2x to 4x band and far under the 10x kill bar.
- Op streams are per-turn deterministic (3/3 identical), scale with input
  length, and cannot be gamed by turn index (the counter resets per turn).

## CV-B5 (specificity, anti-collapse): PASS

- 100 percent of declines name the specific uncovered content words in the
  frozen template: 30/30 training declines match
  "I do not know. My knowledge base contains nothing about "x", ...".
- 0 blanket refusals. No decline is emitted without at least one quoted
  content word (the empty-content-word input path is unreachable in the
  interactive protocol and returns the degenerate-input guard only then).

## Static checks

- No fact composition: the candidate gate (deliberate_cv1) either declines
  or selects exactly one KB fact id; do_turn emits it through the unchanged
  frozen emit_fact path. Paths 1-4 (correction, topic resume, composition,
  assertion/contradiction) are byte-untouched frozen code.
- No sealed references: grep over cv1.zag, cv1_section.zag, gate_op.zag,
  collapse_check.zag finds no mention of probes_sealed or sealed content.
- No Python: no .py file created or executed at any point in this task.

## Known conservative divergence (disclosed, travels with the implementation)

Because the prereg specifies exact F7 canonicalization with no stemming, the
candidate declines some answerable probes where the frozen baseline's stemmer
matches inflected forms. Observed existence case: "did marie curie discover
radium?" the frozen baseline answers "Marie Curie discovered radium." while
the candidate declines naming "discover". Fail-closed (a decline, never a
confabulation), prereg-faithful, but a paraphrase-recall miss the sealed key
may count against CV-B1. No divergence of this kind appears in the 17 frozen
in-KB turns (byte-identical) or the 30 training probes (30/30 specific
declines on both engines).
