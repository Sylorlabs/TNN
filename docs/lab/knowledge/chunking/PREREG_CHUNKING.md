# PREREG_CHUNKING — Is chunking needed, and can TNN derive it itself?

Frozen: 2026-09-22 (pre-battery-generation). Battery generated only after this
document is committed.

## 1. Question

TNN operates on raw bytes (settled: no tokenizer, no units — verified from
`delib_si2.zag`, which lowercases the item to a raw byte string and runs
literal byte-substring predicates). Micah's question:

(a) Is CHUNKING needed at all — does some mechanism have to split the byte
    stream into pieces before verdicts are computed?
(b) If so, can TNN derive chunk boundaries itself from the byte stream's own
    structure, or must chunking be imposed from outside?

## 2. Mechanism under test (grounded, not invented)

Extracted verbatim from
`~/workspace/tnn-lab/coding/reflection/speed_intel/work_a1x/delib_si2.zag`
(`is_pos_word`, `is_neg_situation`, `matches_sarcasm`):

- POS markers (positive-expression substrings): `great`, `wonderful`,
  `fantastic`, `love`, `best`, `brilliant`, `perfect`, `awesome`
- NEG markers (negative-situation substrings): `flat tire`, `6 am`,
  `delayed`, `monday`, `broke`, `failed`, `terrible`, `awful`, `worst`
- Conjunction rule: `matches_sarcasm(w) = is_pos_word(w) AND is_neg_situation(w)`.

Trial verdict rule (frozen): item verdict = ENDORSE iff >=1 POS marker AND
>=1 NEG marker fire on the evaluated byte span; else WITHHOLD. (The
endorse/withhold polarity is a trial convention for the sarcasm-detection
task; the mechanism is the extracted one, unchanged.)

No trimming: the full 8+9 lists are used. No other predicates are evaluated.

## 3. Battery (generated AFTER this freeze)

Generator: `gen_battery.py`, deterministic, zero RNG.
sha256: `00dd81ebac1b229918b31b210bae095ba6e2a09c4840ecce09dbee4b9aa28cc5`

- All items lowercase plain-ASCII English prose; paragraphs separated by
  blank lines (`\n\n`).
- Filler sentences from a FIXED authored list of 48, cycled
  deterministically. The generator ASSERTS no filler sentence contains any
  marker substring (fails loudly), and re-validates every finished item:
  exactly the intended markers occur (count == 1 each), no others, and all
  offsets/distances in spec.
- Exact-length padding uses a neutral repeated token (`note ` trimmed to the
  byte); filler-asserted marker-free.
- `manifest.tsv`: ID, kind, byte_len, pos_marker, pos_byte_offset,
  neg_marker, neg_byte_offset (-1 if absent).
- `items/item_S0_001.txt` etc. plus `items.txt` (single-line records
  `ID|LABEL|escaped-text`; `\`->`\\`, newline->`\n`).

Kinds (frozen counts, N=80):

| kind | n | paragraphs | construction | label |
|------|---|-----------|--------------|-------|
| S0 | 12 | 1 | ONLY a POS marker (6) or ONLY a NEG marker (6) | WITHHOLD |
| S1 | 24 | 1 | POS+NEG within 60 bytes, same subject (asserted <=60) | ENDORSE |
| S2 | 24 | 4-8, ~2-4KB | ironic review: POS in para 1, NEG later, SAME subject; POS-NEG byte separation D2: 8 items each in bands 300-700 / 700-1100 / 1100-1500 | ENDORSE |
| S3 | 16 | 4-8, ~2-6KB | POS about subject A early; NEG about UNRELATED subject B later; separation >=2000 bytes (asserted) | WITHHOLD |
| LONGEST | 4 | many, ~20-30KB | 2 S2-style, 2 S3-style | as styled |

S3 is the honest case where whole-item conjunction is WRONG: naive
whole-item AND over-fires on unrelated co-occurrence.

## 4. Arms (one Zag binary `chunk.zag`, mode via argv)

- WHOLE: conjunction over the entire item byte string. No chunking.
- FIXED-64 / FIXED-512: non-overlapping fixed byte windows (64 / 512; last
  window may be short). Per-chunk independent verdicts; item verdict = OR
  over chunks. Imposed-grid model of chunking.
- ADAPTIVE (structure-derived, the key arm). Frozen algorithm:
  - Scan bytes left to right. Structural boundary candidates = `\n\n`
    paragraph breaks, plus a hard cap of 4000 bytes per chunk (forced split
    at the byte, mid-paragraph if needed).
  - Per-current-chunk evidence: whether a POS fired (and its end byte),
    whether a NEG fired (and its end byte).
  - At each candidate boundary: if the current chunk has an UNRESOLVED
    marker (POS fired with no NEG yet in this chunk, or vice versa), look
    ahead up to W=1600 bytes for the conjunction partner (scan for any
    partner marker in [boundary, boundary+W)); if found, EXTEND the chunk
    through the partner occurrence's end byte (do not split at this
    boundary) and continue scanning from there; else SPLIT at the boundary.
    A resolved chunk (both fired, or neither) splits freely at candidates.
  - Per-chunk independent verdicts; item verdict = OR over chunks.
  - W=1600 declared here. Post-hoc sensitivity diagnostic at W in {800,
    3200} (diagnostic only, does not change the verdict).
- DIAGNOSTIC (no kill bar): FIXED-512-UNION — fixed 512 windows but evidence
  UNION across windows before applying the conjunction ONCE. Separates
  "boundary placement" from "verdict scope".

No short-circuit: every chunk is evaluated even after an ENDORSE (complete
cost accounting). All arms deterministic.

Cost metric: count every byte comparison inside `has_sub` (global counter,
reset per arm per item). Report total per arm and mean ratio vs WHOLE.
Boundary scanning in ADAPTIVE is not inside `has_sub` and is not counted
(documented lower bound).

## 5. Kill bars

- KB1 (key question): acc(ADAPTIVE) - acc(better of FIXED-64/FIXED-512)
  >= 20pp on LONG items (S2+S3 combined, n=40). Met -> self-derived
  boundaries beat imposed grids where it matters.
- KB2 (manipulation check): acc(WHOLE) - acc(FIXED-64) >= 20pp on S2
  (n=24). Met -> fixed windows CAN destroy long-range reference (battery
  valid).
- KB3 (no-collapse): acc(WHOLE) >= 90% on LONGEST items AND zero
  crashes/panics at any length.
  - KNOWN STRUCTURAL TENSION (declared pre-freeze, not hidden): LONGEST
    contains 2 S3-style items on which WHOLE's naive conjunction necessarily
    over-fires (ENDORSE vs WITHHOLD label), so the >=90% accuracy clause is
    structurally unachievable on this composition (ceiling 50%). The
    informative part of KB3 is the no-collapse substance: zero
    crashes/panics at 20-30KB and no scale-induced degradation on the
    S2-style half (expected 2/2). Reported honestly as such.
- KB4 (two-sided): acc(ADAPTIVE) >= acc(WHOLE) on S3 (n=16). Met ->
  adaptive fixes whole-item's over-merge failure.

Also reported: fraction of S2 items where FIXED-64/512 place POS and NEG in
different windows (from manifest offsets); per-kind accuracy tables for all
arms; W-sensitivity diagnostic (W in {800, 3200}); per-arm cost totals and
mean ratios vs WHOLE.

## 6. Determinism rule

Every official run twice; canonical logs must be byte-identical, else the
run is invalid. Zero RNG anywhere (generator, binary, analysis).

## 7. Allowed pre-freeze validation

Smoke-test `chunk.zag` on <=4 hand-made scratch items (NOT battery items).
Fix bugs. Commit this prereg batch FIRST (PREREG_CHUNKING.md,
gen_battery.py, vendored R33 native files), verify via gh-api, THEN
generate the battery.
