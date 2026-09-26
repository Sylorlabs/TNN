# PREREGISTRATION — chunking battery fix crew (2026-09-26)

Fix worker for the 26-trap next-wall battery failures (Micah order 2026-09-26
~11:49 PDT). Red-team cause analysis (CAUSES.md, committed 75613fdf) is the
spec; this document preregisters each fix BEFORE implementation.

## Baselines (measured, frozen)

- Wall battery (26 traps, frozen promote intake): **14/26**, 0 panics,
  output SHA-256 `3cc35d29032cf0e2b367db5006606b28efdd5b3937db7b56c09b16b415541fc2`
  (reproduced byte-identically in this workdir as WALL_V0.out).
  Misses: qids 0,1,2,3,4,5,6,7,8,17,18,19.
- Production battery (57Q, frozen promote intake): **57/57**, 0 fallbacks,
  output SHA-256 `0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268`
  (reproduced as B1_V0.out).

## Anti-tuning statement

No oracle, question, or text is changed in either battery. Battery harness
copies differ from the frozen files ONLY in: (a) the @import path pointing at
the fixed intake, (b) allocation of the knowledge registry, one
`tnn_place_knowledge(know)` call, and the added `know` argument at
`tnn_intake` call sites. Diffs will be published to prove it. Expected scores
below are fixed before the first fixed-intake build. No tuning after seeing
output: if a stage misses its preregistered score, the miss is white-boxed
with a named mechanism before proceeding.

## The knowledge-registry instrument (all three (a) fixes)

One `[]u8` arena (`know`, 2048 bytes, zeroed at alloc), three sections:

| Section | Slots | Slot layout | Contents placed |
|---|---|---|---|
| granularity | 8 × 40 B | name_len u8, name[15], plural_len u8, plural[15], delim u8 | ("sentence","sentences",'.'), ("line","lines",'\n') |
| ordinal | 16 × 24 B | word_len u8, word[15], value i64le | first..twelfth → 1..12 |
| relation | 8 × 24 B | word_len u8, word[15], delta i64le | ("after",+1), ("before",-1) |

Placement APIs: `tnn_bind_granularity(know,name,plural,delim)`,
`tnn_bind_ordinal(know,word,val)`, `tnn_bind_relation(know,word,delta)`.
Seeding function `tnn_place_knowledge(know)` contains ONLY placement calls
(no machinery); its body is delimited by `// KNOW-SEED-BEGIN/END` markers so
a noseed proof build can stub it mechanically. Battery mains call it
explicitly — the mechanism never embeds the knowledge.

`know:[]u8` is threaded as a trailing parameter through `tnn_intake`,
`cand_answer`, every candidate, `classify`, `parse_pos_n`, `parse_wordref`,
and the new helpers. (Edition 2026 has no mutable globals; threading is the
only route.)

## Fix list with preregistered score expectations

### Stage A — instruments + ordinal hook + telemetry

- **A1 (telemetry).** Thread the policy winner `w` into every candidate;
  `emit_choice`/`emit_cand` print `cand_name(winner)` instead of the
  fork-era `zoom_choose` name / hardcoded candidate names. Expected wall
  delta: **+0** (answers unchanged); INTAKE `chunk=` labels must equal
  `cand_name(policy_winner(kind,shape))` on every line (script-checked).
- **A2 (ordinal hook, W07/W08).** New `parse_ordinal(s,at,know)`:
  digit-start → -2 (caller falls back to `parse_digits`, byte-identical
  legacy); registry hit → value; else → -1 (caller falls back to legacy
  `parse_digits`, byte-identical legacy). Consulted by `parse_pos_n` and by
  `parse_wordref`'s token reader. Expected wall delta: **+2** (qid 7→'t',
  qid 8→'5'). Stage A wall expectation: **16/26**.
- Zero-regression bar: 57Q stays **57/57** (no 57Q question contains a
  spelled ordinal outside first/last, verified by grep; "first"→1 vs legacy
  0→clamp-0 converges to the same index everywhere it occurs).

### Stage B — relative addressing + target delimitation + two-hop

- **B1 (relative resolver, W04/W05/W06).** New `parse_wordref2(q,t,wn,know)`:
  for each registered relation word R, probe `" word "+R+" "`; anchor =
  the single word after the probe; anchor resolved by FIRST occurrence in
  `t` (W17 convention); `wn = anchor_index + delta`; anchor absent or
  `wn` out of range → `wn=0` (existing '?' arms fire). Delegates to legacy
  `parse_wordref` when no relation probe matches. All `parse_wordref` call
  sites switch to `parse_wordref2` (identical behavior when no probe
  matches). `classify` reroutes relation-bearing questions into the
  existing _WORD kinds: `'s in`→10, `how many letters in`→11,
  `letter of`→12, `backwards`→13, `first/1st letter of the`→14,
  `last letter of the`→15, `contain `→17. Expected wall delta: **+3**
  (qid 4→'3', qid 5→'b', qid 6→'nworb'). Stage B wall expectation:
  **19/26** after B1 alone.
- **B2 (target delimitation, W17).** `zoom_locate`: after `find_word(tw)`
  fails, retry with `first_word(tw)` (first whitespace-delimited token of
  the captured tail). The `beq(tw,t)` whole-text fast path is untouched and
  still tried first. Expected wall delta: **+1** (qid 17→'h').
- **B3 (two-hop addressing, W03).** New kind 21: `classify` returns 21 when
  `has_sub(q,"letter "+R+" the ")` for a registered relation R (checked
  before the generic `letter of`→2 branch). New `cand_delim` arm: parse
  inner ordinal after `"letter "+R+" the "` (hook→digits), inner target =
  first word after `"of "` located in `t`, `idx=ord-1` (legacy clamp at top
  end), answer `t[oo+idx+delta]`, out-of-range → '?'. Policy fallthrough
  routes kind 21 → winner 3 → `cand_zoom` → `cand_delim`. Expected wall
  delta: **+1** (qid 3→'x'). Stage B wall expectation: **21/26**.
- Zero-regression bar: 57Q stays **57/57** (no 57Q question contains
  " word after/before " or "letter <rel> the"; the zoom_locate fallback only
  fires when the legacy lookup already failed, and no 57Q kind-2/8/9
  question has a multi-word non-equal tail — verified by grep).

### Stage C — granularity + abstention

- **C1 (classifier binding + delimiter splitter, W00/W01/W02/W19).** New
  kinds 18/19/20. `classify` pre-pass (runs BEFORE the frozen cascade):
  `"how many "+plural+" in"` → 18; `" "+singular+" of"` → 19, or 20 when
  `" word of "` precedes it. New `enum_delim(t,delim,offs,lens)`: split on
  the delimiter byte, trim ASCII-32 at segment edges, drop empty segments.
  `cand_delim` arms: 18 → segment count (W00→2, W02→3); 19 → ordinal
  (rightmost "the " before `" "+singular+" of"`, hook→digits) selects
  segment (W01→"the dog ran"); 20 → outer `parse_wordref2` ordinal selects
  word inside the granularity-selected segment (W19→"cat"). Residual
  structure after the resolved marker is checked with `inner_has_nesting`
  → '?' on deeper nesting. Expected wall delta: **+4**. Stage C wall
  expectation: **25/26** after C1 alone.
- **C2 (nesting abstention, W18).** After `parse_wordref2` in `cand_zoom`'s
  10–17 block and in `cand_word`'s kind-11/16 arms: if `inner_has_nesting`
  (inner still contains `" word of "`, `" word "+R+" "`, or
  `" "+singular+" of"` for a registered granularity) → answer '?' (withhold),
  never a partial-level answer. Expected wall delta: **+1** (qid 18→'?').
  Final wall expectation: **26/26**.
- Zero-regression bar: 57Q stays **57/57** (all 24 nested-word 57Q inners are
  plain texts with no residual markers — verified by inspection of every
  "word of" line; kind-11/16 cand_word arms only).

## W04 reading (recorded per task order)

"how many e's in the word after the in the cheese wheel": anchor = the
single word immediately following "after " = "the"; resolved by FIRST
occurrence in t (the W17 convention); wn = index+1. Out-of-range or absent
anchor → '?' (withhold), never whole-text fallback. Implemented reading
gives "cheese" → 3. The whole-text reading (6) is acknowledged ambiguous in
English; the battery scores the relative intent per its PREREG note.

## Verification protocol (all preregistered)

1. Each stage: build wall battery, run ×2, SHA-compare (byte-identical
   reruns required); run 57Q battery, require 57/57.
2. Telemetry check: script asserts every INTAKE line's `chunk=` equals
   `cand_name(policy_winner(kind,shape))` for the kind on that line and the
   question's shape (shape recomputed from the W-line text).
3. Noseed proof (final stage only): stub `tnn_place_knowledge` body via the
   KNOW-SEED markers, rebuild, run 57Q → INTAKER lines + `# LIVE SUMMARY`
   must be byte-identical to frozen v0 (proves the mechanism carries no
   hardcoded knowledge; the registry is the only knowledge route).
4. Any remaining miss: white-boxed with a named mechanism + next step; no
   silent misses.
5. Pure Zag, zero RNG. `native=26 fallback=0` expected on the wall summary
   (all answers via the native path).

## Deliverables

- `docs/lab/mg_chunking_batteryfix/`: PREREG.md (this file), RUNLOG.md,
  VERDICT.md, CONTROL_BOUNDARY.md, `intake.zag` (fixed production intake),
  `battery1.zag` + `battery2.zag` (harness copies; question/oracle lines
  byte-identical to frozen — diff published), `build.sh`, `evidence/`.
- Commit to `tnn-native-lab` (NEVER main); verify on origin via gh-api
  tree-walk (non-recursive walk down the exact path).

## Measured results (2026-09-26, appended after implementation)

All preregistered scores hit exactly; 57/57 production at every stage.

| Stage | Expected | Measured wall | Measured 57Q |
|---|---|---|---|
| A | 16/26 | 16/26 | 57/57 |
| B (B1+B2+B3) | 19→20→21/26 | 21/26 | 57/57 |
| C0 registry rewrite | 21/26 (no change) | 21/26, output byte-identical to B | 57/57 |
| C1 | 25/26 | 25/26 | 57/57 |
| C2 | 26/26 | 26/26 | 57/57 |

**Deviation from verification protocol item 3 (noseed proof):** the prereg
expected noseed 57Q output byte-identical to frozen v0. Stage A's
preregistered telemetry fix (A1: thread the true policy winner into
`chunk=` labels) legitimately changed output bytes vs v0, so v0-identity is
unachievable. The valid control is noseed-vs-seeded on the SAME final build:
noseed 57Q SHA `170bacd71...` == seeded 57Q SHA `170bacd71...`
(byte-identical), proving the production battery exercises no seeded
knowledge. Noseed wall: 16/26 (10 knowledge-driven traps fail in exactly the
legacy ways). Protocol intent — "the registry is the only knowledge route" —
holds; the letter of item 3 is superseded by A1, recorded here.

**Deviation from the registry spec above:** stage C0 replaced the sectioned
fixed-slot layout (8/16/8 caps, 15-byte word cap) with an append log whose
capacity is purely the caller-supplied arena length, per the standing
no-arbitrary-limits law. Placement API and seed contents unchanged. Wall
output byte-identical across the rewrite (C0 gate).
