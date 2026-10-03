# PROSE-LEARN2 — Architecture

Rich-comprehension TNN learner, frozen `PREREG2.md` mechanism. Pure Zag
(`src/prose_learn2.zag`), zero RNG anywhere; every decision is a deterministic
function of the input bytes and learner state. An independent Python oracle
(`src/oracle2.py`) re-implements the same mechanism; the synthetic self-test
log must be byte-identical between the two before any championship run.

## Pipeline

```
inputs/train_<src>.txt ─┐
inputs/test_<src>.txt  ─┼─► prose_learn2 <src> ─► stdout log (INSTALL/…/PROBE/SUMMARY/DIGEST/LEDGER/VERIFY/RESULT)
inputs/false_ids_<src>.txt ┘
```

Input text files are tab-separated, produced by `src/convert_inputs2.py` from
the JSON corpora (accepts `text` or `sentence`; test `expect` defaults to the
numeric `probe_value`):

- train lines: `<fact_id>\t<text>`
- test lines: `<probe_id>\t<probe_value>\t<probe_text>\t<expect>`
- false_ids lines: one integer id per line.

Stages per train item: split into sentences on `.`/`?`/`!` (trailing
unpunc­tuated tail kept), then per sentence: tokenize+classify →
value scan → entity tagging → relation tagging → attitude scan →
comes-after/before edge collection → install (asserted/quarantine/denial) →
save previous-sentence entity for coreference. After all train items:
fixed-point inference over comes-edges, then the probe loop, then the digest
and ledger verification.

## Frozen mechanism, stage by stage

### Tokenizer / word units / stemmer — v1 verbatim

- Tokens are maximal `[A-Za-z0-9]` runs (ASCII only; the Python oracle was
  fixed to match v1 exactly — Python's `str.isalnum` admits Unicode).
- Per-token interning of the lowercased raw form into the vocab on first
  sight (`v_intern`, first-seen order, never pre-interned — an earlier draft
  pre-interned the frozen phrase vocabulary and was corrected).
- Classification: digit (optional `st|nd|rd|th` suffix), number-word
  (cardinals + ordinals, v1 lexicon), stopword (v1 list), else content with
  the v1 stemmer applied and the stem interned.
- `LINK`: one vocab unit id appended per token in order (kept for
  v1-compatibility of the interning discipline).

### Value scan

Last digit-token value wins; else last number-word value; else the sentence
carries no value (EXTRACT-FAIL). The value *token bytes* travel with the
value into the role trace. Frozen reading: the recorded token is the one
that determined the value (last digit-token if any digits exist, else last
number-word) — not merely the last number-like token scanned ("There are 10
Ten Commandments" records `10`, value 10).

### Entity tagging (2a → 2d → coreference → EMPTY)

1. **2a**: tokens strictly inside the first `"…"` pair (byte offsets in the
   original sentence). Canonical = lowercased tokens joined with spaces.
2. **2b**: first single uppercase-letter token (`A`–`Z`, raw case).
3. **2c**: the authoritative example ("alphabet position of M" → M) beats the
   prose gloss: find the relation phrase, then the first `of` *after* the
   phrase end; the entity is the first ≤4 content tokens after that `of`.
   If no content token follows, the first word-token (stopwords allowed,
   digits never — a digit is the value, not the entity), so "The letter
   count of an is 2" → `an`. If any link is missing, 2c does not fire.
4. **2d**: first ≤4 content tokens before the first
   has/have/is/are/was/were. If none, falls through (does not return EMPTY
   early) so coreference can still fire — this is what lets "It has 4
   letters." resolve.
5. **Coreference** (train only): trigger = any token in
   {it, its, this, that, these, those} or an adjacent "the word"/"the
   letter" pair; resolves to the previous sentence's entity *within the
   item* (stem-unit ids and canonical bytes copied). Skipped when the
   previous entity is EMPTY. The previous-entity slot is reset at each
   train item boundary.
6. Otherwise EMPTY (`0xFFFFFFFF`).

Deterministic readings settled by test: 2c's of-follows-phrase order; 2d's
empty-lead fall-through; first-match wins everywhere (quotes, 2b scan,
phrase scan, `of`, verb).

### Relation tagging

Frozen phrases (stemmed forms): `alphabet position`, `letter count`,
`publish year`, `come after`, `come before`. Earliest start in the
content-token sequence; ties broken by phrase list order. Relation =
sorted stem-unit ids of the phrase tokens. Otherwise OPEN: sorted unique
content stem-unit ids with the entity's stem-unit ids removed. Empty/empty
Jaccard is defined as 0.

### Attitude

NEGATED (stemmed `not`/`never`/`no`, or a stemmed `t` token whose previous
raw token is `isn`/`don`/`can`/`won` — i.e. a split contraction) beats
HEDGE (13 frozen stems: think, believe, probably, maybe, perhap, might,
could, seem, allegedly, reportedly, possibly, likely, rumor). Content
tokens only. Else asserted.

### Stores

- **Asserted**: exact key `(entity, sha256(relation))` → value, status
  0=live/1=contradicted, first-seen fact id, ledger seq. New key → INSTALL.
  Same key+value → CORROBORATE (ledger only). Same key, different value →
  CONTRADICT (status flips to 1, ledger only). Already contradicted →
  silent no-op.
- **Quarantine** (hedged) and **denial** (negated): exact-key dedup on the
  row, but the ledger event is recorded on every sentence.
- Ledger event bytes (frozen wording, serialized exactly):
  `prev32 || seq<u64 || fact_id<u32 || kind<u8 || entity<u32 ||
  rel_hash32 || value<i64 || attitude<u8 || trace_len<u32 || trace`.
  Kinds: 1=INSTALL 2=CORROBORATE 3=CONTRADICT 4=QUARANTINE 5=DENIAL
  6=DERIVED. Chain hash = sha256 of the event; verified by full recompute.
- Role trace: `ent=<eid>|rel=<r1>,<r2>|val=<vtok>|att=<a>|coref=<0|1>`
  with `|rule=comes_after|comes_before|prem=<yeid>:<n>` appended for
  derived events (their `val` is the literal `derived`, `att=3`).

### Inference

comes-after/before edges are collected during training (asserted attitude
only): target = first ≤4 content tokens after the phrase. Fixed-point loop:
if the target entity has a live asserted alphabet-position value `n`, the
source gains `n±1` (DERIVED install, CORROBORATE, or CONTRADICT with
`sent=-1`, `attitude=derived`). Terminates: rows only go live→contradicted
and new rows are bounded.

### Probing

Exact asserted hit (live) → `VALUE:<v>`; contradicted → CONTRADICTION;
quarantine hit → HEDGED; denial hit → UNKNOWN; else fallback: entity-exact
candidates scored by Jaccard (no threshold — any entity-exact candidate
meets the 2.0 bar by construction, `2.0 + J`), EMPTY-entity candidates need
`2·inter ≥ union > 0`; argmax by cross-multiplication (no floats), ties →
lowest fact id (ties counted). None → UNKNOWN.

### Digest

v1 digest extended for the verdict stream (documented, deterministic):
per probe one verdict-code byte (0=VALUE, 1=CONTRADICTION, 2=HEDGED,
3=UNKNOWN) plus the `<i64` value for VALUE; then the ledger head;
sha256 twice; `dmatch` requires both equal. `RESULT PASS` =
chain-verified AND digest self-consistent. (PASS is an internal-integrity
bar, not probe accuracy — `ok`/`full`/`clean` report accuracy separately.)

## Memory layout (all []u8 arenas, explicit put/get — znc ZNC-2026-09-21-007)

- Vocab: `vbytes` (2 MiB) + `vent` (entry table); `linka` token→unit log.
- Per-sentence tables (≤256 tokens): offsets, lengths, stem offsets/lengths/
  unit ids, flags, i64 values, content positions; `sctx` 128 B context block.
- Asserted rows: 320 B (`eid@0`, `relhash@4`, `value@36`, `status@44`,
  `fid@48`, `seq@52`, `reln@56`, `relids@60`, ≤64 ids); cap 4096 rows.
- Quarantine/denial rows: 48 B; cap 1024 each.
- Ledger: parallel arrays (kind/fid/eid/relhash/value/attitude/trace-off/
  len, cap 8192) + 1 MiB trace arena + 32 B chain head.
- comes-edges: parallel arrays + 64 B canon slots, cap 512.
- No slice exceeds 2²⁵ bytes; every arena header is explicitly initialized
  (znc arena-init lesson).

## znc constraints honored

No `as []i32`/`as []u32`/`as []u16` indexed tables; no slice `==`; no
large/nested structs (flat arenas + integer handles throughout); no chained
`field.subfield` access; nesting flattened; `return;` with semicolon in
void fns; no `};`; `_zag_arg` never freed; `_zag_arg(n)` read unconditionally
(argc is 0 at runtime).

## Known limits / divergence risks

- ASCII-only tokenizer (spec); non-ASCII input bytes act as separators.
- Digit strings wider than i64 would wrap (not present in the corpora).
- `RESULT PASS` is internal integrity, not accuracy.
- Rule 2b takes the *first* single uppercase letter: "I do not think the
  alphabet position of Q is 17." tags entity `i`, not `q` (frozen reading,
  covered by the synthetic fixture).
- Build emits one analyzer warning (A0101 off-by-one on the 2a
  quote-span `b<=q2` check): false positive — `b` is a byte offset used
  only in a comparison, never as an array index; token access stays within
  `toff`/`tlen` bounds for `n<ntok`.
- Inference may emit repeated CORROBORATE ledger notes across fixed-point
  passes (same derived key re-corroborated); both implementations do this
  identically (0-diff), and it does not change probe verdicts.
