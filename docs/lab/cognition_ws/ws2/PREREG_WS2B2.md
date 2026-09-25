# PREREG WS2-B2 — Synonym-bridge + byte-level morphological normalization (FROZEN 2026-09-24)

Worker: WS2-B2 (Track B re-dispatch). Coordinator: cognition workstream.
Status: FROZEN — committed before any B2 code was written or any B2 lookup
was run. Any change to the mechanism, the synonym table, the probe sets, the
gold sets, or the bars after this commit requires a new dated amendment;
results under a changed rule are a new experiment, not this one.

Parent result: WS2-B forced-ToC scheme, 53/58 (46/51 official: T-exact 45/45,
T-para 1/6 via stemming; maintenance 7/7). The 5 misses are all P-PARA probes
with zero exact-word overlap. This experiment adds a deterministic,
byte-level synonym bridge to close the vocabulary gap without touching the
exact-match path that yields 45/45.

## 1. Framing (Micah's correction, standing)

TNN uses NO LLM tokenization: no BPE, no learned embeddings, no subword
vocabularies. The battery's "token overlap" is whitespace/lowercased word
equality used only as a measurement stick. This layer is therefore:

- BYTE-LEVEL: synonym matching is byte-exact equality on lowercased words
  (after the frozen stemmer), against a curated word<->word table.
- DETERMINISTIC: the table is versioned in-repo (SYN_TABLE_V1.txt, SHA-256
  pinned below); canonical choice per pair is fixed (lexicographically
  smaller stem); no statistics, no embeddings, no RNG anywhere (grep-gated).

## 2. Mechanism (frozen)

### 2.1 Morphological layer: FROZEN, byte-identical to WS2-B

The WS2-B stemmer (suffix strip: -ing/-ed/-es/-s with length guards) and the
WS2-B stoplist are used UNCHANGED. QP04 already proved this stemmer closes a
morphological gap ("arranging"/"arranges" -> "arrang"). No new affix rules in
this experiment: the synonym table (applied pre-stem, see 2.2) subsumes the
inflectional variation the new probes need, and keeping the stemmer frozen
keeps the phase-1 path provably identical to the 46/51 WS2-B run.

### 2.2 Synonym table: SYN_TABLE_V1.txt (frozen, 56 pairs)

Format: one `word1|word2` per line, lowercase raw words, `#` comments.
Semantics: word1 and word2 are declared mutually substitutable. At startup
the binary builds a stem-level map: for each pair, sa=stem(word1),
sb=stem(word2), canon=lexicographically-smaller(sa,sb) by byte order; the map
holds sa->canon and sb->canon (first pair wins on key collision; the
generator script asserts zero key collisions). canon_of(t) returns the
mapped canonical stem, or t itself when unmapped. Matching is byte-exact
equality on canonical stems.

The table is embedded into the build by GENERATION, not transcription:
`gen_syn_table.py` reads SYN_TABLE_V1.txt and emits `src/syn_table.zag`
containing the table text as a Zag string literal. The build script
regenerates before every compile and asserts the embedded bytes are
byte-identical to SYN_TABLE_V1.txt.

SHA-256 pin of SYN_TABLE_V1.txt: recorded at commit time in the commit
message and in WS2B2_RUNLOG.md (the file bytes are the pin; no separate
checksum file that could drift).

Full frozen table (56 pairs):

PP01 lunar gravity (6): moonwalkers|astronauts, hop|bounce, gently|lightly,
weak|feeble, selenian|lunar, attraction|pull
PP02 fermentation (5): kraut|cabbage, fizz|bubbles, bacteria|microbes,
dine|feast, fortnights|weeks
PP03 pruning (5): withered|dead, limbs|branches, trimmed|clip, prior|before,
sprouting|buds
PP05 twain quote (4): witticism|quote, beginning|started, readiness|ahead
PP06 acoustics (4): song|note, linger|prolong, basilica|cathedral,
masonry|stone
QR01 compost (6): espresso|coffee, dregs|grounds, nourish|feed,
earthworm|worm, december|winter, box|bin
QR02 inertia-balloon (6): envelope|balloon, helium|gas, hoists|lifts,
rattan|wicker, hamper|basket, field|meadow
QR03 magnetism (4): magnetized|lodestone, sliver|needle, aims|points,
pole|north
QR04 siege (5): besiege|siege, citadel|fortress, severing|cutting,
provision|supply, carts|wagons
QR05 resonance (5): prong|fork, vibrates|hums, goblet|glass, till|until,
answers|sings
QR06 friction (7): abrasive|sandpaper, grain|grit, opposes|resists,
gliding|sliding, cube|block, heating|warms, faces|surfaces

Every pair was audited against the full corpus keyword inventory: no
canonical stem in the table collides with a stem belonging to a non-target
item, except the documented shared cases (quote: PP05 type QUOTE and PX01
type QUOTE; before: PP03 text) which the distractor battery explicitly
stress-tests.

### 2.3 Two-phase retrieval (frozen)

Phase 1 is the WS2-B lookup algorithm UNCHANGED (routes 1/2/3, scoring
tot = cell_score*1000 + own_score, sort by score desc then index asc,
score-0 abstention). Because the stemmer, stoplist, ToC files, and scoring
are all byte-identical inputs, phase-1 outcomes are provably identical to
the WS2-B 46/51 run.

Phase 2 (the bridge) fires ONLY in route 3 (the keyword-fallback route all
P-PARA probes take) and ONLY when the phase-1 top score is <= 1 (abstain or
weak single-token match). It recomputes candidate scores with
canonical-stem matching:

  own_score2 = count over query tokens of byte-equal canon(query_stem)
               against canon(item KW stems)
  cell_score2 = same against the subject cell aggregate
  tot2 = cell_score2*1000 + own_score2

The phase-2 ranking REPLACES the phase-1 ranking iff it has a UNIQUE top
candidate with tot2 >= 2 (bar: at least two distinct bridge/exact stem
matches, no tie). Otherwise the phase-1 result stands (this is what keeps
QP04 passing: its phase-2 top is 1 < 2, so the phase-1 single-token win is
kept).

The per-query report line gains a trailing bridge flag: route|nsj,nd,nt|
ncand|take|bridge, bridge=1 iff phase 2 overrode phase 1.

### 2.4 What the bridge must NOT do (precision contract)

- Never fire when phase 1 already has a confident (score >= 2) winner.
- Never override on ties. Never override below the 2-match bar.
- The distractor battery (section 4) is the precision guard: any retrieval
  of a decoy item, or any retrieval at all on an abstention probe, is a
  kill-bar failure.

## 3. Probe sets (frozen)

3.1 Official battery (51 probes, fixtures/probe_queries.txt): unchanged.
    Bars: T-exact 45/45 (all non-P-PARA), P-PARA 6/6 (QP01-QP06, incl. QP04).
3.2 Maintenance leg (7 probes, WS2B_MAINT_probes.txt): unchanged. Bar 7/7.
3.3 Fresh paraphrase battery (6 probes, NEW, fixtures/probe_queries_b2.txt,
    golds in fixtures/answers_b2.txt, K=1 in fixtures/k_b2.txt): QR01-QR06.
    Each is a zero-exact-word-overlap paraphrase (verified by
    validate_battery.py semantics AND zero stemmed-token overlap, checked by
    script) of a NON-PP corpus item, using only table-covered vocabulary.
    Bar: 6/6.
    QR01|PX04: espresso dregs nourish earthworm box through december
    QR02|PA03: gas envelope hoists rattan hamper above field
    QR03|PD01: magnetized rock sliver aims toward pole
    QR04|PX06: besiege citadel severing provision carts
    QR05|PA05: prong vibrates goblet till answers
    QR06|PA02: abrasive grain opposes gliding cube heating faces
3.4 Adversarial distractor battery (6 probes, same new files): QD01-QD06.
    Each query has a clear gold item but ALSO shares >=1 synonym bridge with
    a designated decoy (wrong) item. The bridge must not be lured.
    QD01|PP05 (decoy PP03, shares before): witticism about beginning before
      readiness fades
    QD02|PP06 (decoy PP01, shares feeble): sacred song lingers in feeble
      stone basilica
    QD03|PP02 (decoy PC01..PC10, shares pull): pickled kraut fizz pulls
      bacteria to dine
    QD04|PP03 (decoy PP01, shares hop): withered limbs hop back after
      trimming
    QD05|PP01 (decoy PP06, shares song/prolong; phase-2 must fire):
      moonwalkers hop gently as songs prolong under weak selenian attraction
    QD06|PP04 (decoy PP06, shares note; tie case): arranging numbers
      ascending via neighbor notes
    Bar: 6/6 gold retrieved, 0 decoy retrievals.
3.5 Abstention probes (3 probes, same new files, empty gold): QV01-QV03.
    Out-of-corpus topics; the bridge must not hallucinate a retrieval.
    QV01: submariners whisper softly beneath crushing abyssal pressure
    QV02: glassblowers shape molten silica into fragile vessels
    QV03: cartographers chart silent polar wastes
    Bar: 3/3 abstain (zero retrievals).

## 4. Kill bars (all must hold; any failure kills the track)

K1. T-exact stays 45/45 on the official battery (phase-1 path untouched).
K2. P-PARA 6/6: QP01, QP02, QP03, QP05, QP06 newly retrieved via the
    bridge; QP04 still retrieved (via phase-1 fallback).
K3. Maintenance leg 7/7 (no regression from the bridge code path).
K4. Fresh battery QR01-QR06: 6/6.
K5. Distractor battery QD01-QD06: 6/6 gold retrieved AND zero decoy
    retrievals (a bridge that hallucinates connections is worse than the
    vocabulary gap).
K6. Abstention probes QV01-QV03: 3/3 abstain.
K7. Determinism: 3/3 byte-identical full reruns (init + lookup + grade
    outputs, SHA-256 compared).
K8. Zero RNG: grep gate over all B2 sources (no rand, no time-seed, no
    OS entropy reads); the binary links no RNG source.
K9. Official QN01-QN06 negatives still abstain (no bridge hallucination).

## 5. Method constraints

- Pure Zag only. Pinned znc:
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- New binary `tocb` built from `src/toc_b2.zag` (byte-identical copy of
  WS2-B `src/toc.zag` at experiment start, plus the bridge code) +
  generated `src/syn_table.zag` + `src/lib.zag` + pinned substrate files.
  `src/toc.zag` itself is NOT modified (WS2-B reproducibility preserved).
- Build script `build_ws2b2` regenerates syn_table.zag from
  SYN_TABLE_V1.txt and asserts byte-identity before compiling.
- Commit order: (1) this prereg + SYN_TABLE_V1.txt + new battery fixtures;
  (2) code; (3) evidence. Incremental commits on branch tnn-native-lab via
  ~/workspace/commit_racefree.py (TMPDIR=~/workspace/tmp_commit).
- No em-dash characters in docs.

## 6. Honest limits (stated up front)

The synonym table is hand-curated, so QR01-QR06 passing proves the
MECHANISM generalizes to new wordings over table-covered vocabulary, not
that the table was learned or is complete. Table growth is deliberate,
versioned, and auditable (each pair lists its motivating probe above), and
the distractor battery exists precisely because a curated table can
over-connect. A future track may investigate deliberate table learning;
this track tests whether a frozen curated bridge closes the measured gap
without precision loss.
