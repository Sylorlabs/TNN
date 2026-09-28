# Arm-3 Variation B — "Phase-Scheduler Teacher" — committed proposal-policy spec

teacher_id = 3. Pure Zag (`teacher.zag`). Implements frozen PREREG §4 B.2.3:
a deterministic function `(spec, stimulus, history) → §P proposal sequence`.

## 1. What this teacher is

An **aggregate phase scheduler**. The (spec, stimulus, history) → proposal
mapping lives entirely in the teacher. Teaching proceeds in four phases —
INTRODUCE → CORROBORATE → RELATE → CONSOLIDATE — driven **only by aggregate
history signals** (adoption rate over the last 10 decided proposals,
consecutive-rejection count, appeals-used count). No single decision ever
drives a transition by itself. This is deliberately different from a
per-decision state machine: the teacher re-derives its phase from the whole
decision log on every invocation.

Negative declarations (auditor-verifiable, B.2.5):
- No learning machinery: per-invocation working state is fixed-size buffers
  declared below; the teacher is stateless across invocations — phase,
  cursor and counters are re-derived from the history argument every run.
  Nothing is written to spec or data files; output goes to stdout only.
- No RNG in any teacher path. No wallclock: all decisions are pure functions
  of (spec bytes, stimulus bytes, history bytes, argv).
- No flaw manifest (T-7): natural teaching only. Confidence is selective
  (120–220, never 255 — expressed uncertainty). Thesis holds: proposals
  carry byte spans only — no commands, no token ids, no string payloads.

## 2. CLI and inputs

```
teacher <dir> <stimulus_name> <history_name> <session_id>
```

- `<dir>`: directory holding the two files (opened with `nio_open_root`).
- `<stimulus_name>`, `<history_name>`: file names (`nio_name_valid`).
- `<session_id>`: decimal u64, stamped into every emitted proposal.

### 2.1 Stimulus
Raw bytes. `1 ≤ len ≤ 1048576`, else exit 5 / 6.

### 2.2 History (the session's decision log)
Binary. Layout (little-endian):

```
0..4   magic u32 = 1414744392 ("HIST")
4..6   version u16 = 1
6..10  count u32 (0 ≤ count ≤ 4096)
10..   count × 32-byte records:
         0..8   seq u64            (teacher's proposal seq; strictly increasing)
         8      kind u8            (1=WORD_SPAN 2=BOUNDARY 3=GROUP 4=SAME_AS 5=RETRACT)
         9      verdict u8         (0=ADOPT 1=REVISE 2=REJECT 3=DEFER)
         10     reason u8          (REJECT: 1=R1 2=R2 3=R3 4=R4 5=R5 6=R6; else 0)
         11     pad u8 (=0)
         12..20 span_start u64
         20..28 span_end u64
         28..32 reserved u32 (=0)
```

File size must equal exactly `10 + 32*count`. For kinds 1–4 the span is the
proposal's head span (`0 ≤ span_start < span_end ≤ stim_len`). For kind 5
(RETRACT) the span encodes the retraction target per the harness convention:
`span_start = target_seq`, `span_end = target_seq + 1`, with
`0 < target_seq < seq`.

The history is the student's decision record: one record per proposal of all
prior turns, in seq order, each carrying a terminal verdict (DEFER is allowed
as a provisional record). The teacher validates the ENTIRE history before
emitting anything.

### 2.3 Exit codes (§P iron rules: malformed input → exact exit, logged, zero proposals)

| code | meaning |
|------|---------|
| 0 | success (possibly an empty batch — still success) |
| 1 | usage: wrong/missing argv |
| 2 | cannot open `<dir>` |
| 3 | bad file name |
| 4 | cannot open/read stimulus |
| 5 | stimulus empty |
| 6 | stimulus too large |
| 10 | history bad magic |
| 11 | history bad version |
| 12 | history size ≠ 10 + 32*count (truncated/extended) |
| 13 | history bad kind/verdict/reason value |
| 14 | history seq not strictly increasing |
| 15 | history span invalid (bounds or RETRACT target rule) |
| 16 | history reserved/pad field nonzero |
| 17 | history too large (> 10 + 32*4096 bytes) |
| 20 | cannot open/read history file |
| 30 | stdout write failed |

All diagnostics go to **stderr**. On any nonzero exit, **stdout carries zero
bytes** (proposals are built fully in memory, then written once).

## 3. Spec constants

```
PHASE: 0=INTRODUCE 1=CORROBORATE 2=RELATE 3=CONSOLIDATE
K_WIN      = 10    (adoption/appeal window: last 10 decided teaching proposals)
K_ADV_IC   = 3     (base adoptions-in-window to leave INTRODUCE)
K_ADV_CR   = 5     (adopted units to leave CORROBORATE)
K_ADV_RC   = 2     (consecutive rejections to leave RELATE)
K_RESET    = 3     (consecutive rejections → INTRODUCE, fresh region)
MIN_WORD=3, MAX_WORD=32
INTRO_BATCH=8, CORR_BATCH=6, REL_BATCH=7, CONS_BATCH=4
MAX_UNITS=64, MAX_SPANS=512, MAX_OCC=8, REGION_SKIP=256
```

"Decided teaching proposal" = history record with kind ∈ {1,2,3,4} and
verdict ∈ {0=ADOPT, 1=REVISE, 2=REJECT}. RETRACT records (kind 5) and DEFER
records never enter the window and never touch `consec_rej`.

## 4. Aggregate computation (single ordered pass over history)

State (all fixed-size; re-derived every invocation):

- `consec_rej`: +1 on REJECT, =0 on ADOPT/REVISE, unchanged on DEFER/RETRACT-record.
- window: ring of the last ≤10 decided teaching proposals → `adopt10`
  (#ADOPT), `appeals10` (#proposals whose span had been proposed before
  **and** whose last verdict was REJECT — a re-proposal of an adopted or
  revised span is corroboration, not an appeal; DEFER leaves the last
  verdict untouched).
- `adopted[]`: chronological list of ADOPTed (kind 1–4) spans, ≤64.
  (REVISE counts as non-adopt for the window but still resets `consec_rej`.)
- per-span stats (keyed by head span, ≤512 distinct spans): `nprop`
  (#proposals), `nrej` (#REJECTs), `cfin` (consecutive session-final rejects),
  `lreason` (last reject reason), `lverdict` (last verdict), `lseq` (latest
  proposal seq), `dead` flag.
- `maxseq`, `cursor` (= max head `span_end` over kinds 1–4, else 0).
- `retracted[]`: targets of kind-5 records in history.

Per record, in seq order:

- kind 5: record target in `retracted[]`; signals untouched.
- verdict ADOPT: `consec_rej`=0; span `nprop`+1, `lverdict`=ADOPT; window push
  (adopt=1, appeal=`nprop_before ≥ 1` and `lverdict_before` was REJECT);
  append to `adopted[]`; `cfin`=0.
- verdict REVISE: `consec_rej`=0; span `nprop`+1, `lverdict`=REVISE; window
  push (adopt=0, appeal=`nprop_before ≥ 1` and `lverdict_before` was REJECT);
  `cfin`=0.
- verdict REJECT: `consec_rej`+1; span `nprop`+1, `nrej`+1, `lverdict`=REJECT;
  window push (adopt=0, appeal=`nprop_before ≥ 1` and `lverdict_before` was
  REJECT); `lreason`=reason, `lseq`=seq.
  Session-final ⟺ reason ∈ {R3,R4,R6} or `nprop` ≥ 3 (appeal budget
  exhausted → R6 by construction). If session-final: `cfin`+1 else `cfin`=0.
  If reason ∈ {R3,R4} → `dead`=1. If `cfin` ≥ 2 → `dead`=1
  (two consecutive session-final rejections of the normalized span).
- verdict DEFER: span `nprop`+1, `lverdict`=DEFER; signals untouched.

After each record, phase transitions in priority order:

```
R1. consec_rej ≥ K_RESET(3)            → phase = INTRODUCE   (fresh region)
R2. phase = INTRODUCE, adopt10 ≥ T     → phase = CORROBORATE,  T = K_ADV_IC + (appeals10 ≥ 4 ? 2 : 0)
R3. phase = CORROBORATE, adopted ≥ K_ADV_CR(5) → phase = RELATE
R4. phase = RELATE, (cursor ≥ stim_len or consec_rej ≥ K_ADV_RC(2)) → phase = CONSOLIDATE
```

R1 has top priority (it also fires from CONSOLIDATE). Phases never move
backwards except via R1. `fresh` = (consec_rej ≥ 3) ? 1 : 0.
`eff_cursor` = min(stim_len, cursor + (fresh ? REGION_SKIP : 0)).

The appeals-used aggregate drives the policy in three places: the R2
threshold modulation above, INTRODUCE batch composition (§5.1, appeals before
fresh words), and the appeal/dead rules (§4.1).

### 4.1 Appeals and dead spans

A span is **appealable** ⟺ not dead, `nrej` ≥ 1, `lreason` ∈ {R1,R2,R5},
`nprop` ≤ 2 (this re-proposal is appeal #1 or #2 — max 2 appeals per span per
session; a third is auto-refused R6 by construction), and the word occurs
`m ≥ nprop + 2` times in the stimulus (so the appeal carries genuinely NEW
evidence — occurrence #`nprop`+1, 0-based).

A span is **dead** ⟺ R3/R4 ever, or appeals exhausted with a final REJECT,
or `cfin` ≥ 2. Dead spans are never proposed again.

## 5. Proposal policies per phase

Words: maximal `[A-Za-z0-9_]` runs with `3 ≤ len ≤ 32`. Word-boundary
occurrences: byte matches with non-word (or edge) bytes on both sides.
The **blocked list** = every history head span (kinds 1–4) plus every dead
span; fresh-word scans skip tokens overlapping it. `next_seq` = maxseq+1,
then +1 per proposal (monotonic, continuing the session).

### 5.1 INTRODUCE — fresh teaching
Batch: up to 2 appeal proposals (appealable spans, spanstat index order),
then fresh words scanned from `eff_cursor` (cursor order, non-overlapping
by construction of the scan), filling the batch to `INTRO_BATCH`=8.
- kind=WORD_SPAN, `aux_count`=0, `ground_count`=1.
- grounding[0] = occurrence #g of the word, g = 1 if m>1 else 0
  (a second usage; the word's own span when it is a hapax).
- Appeal re-proposal of a span with `nprop`=p uses occurrence #p+1
  (new evidence by §4.1) and confidence = base + 10·p.
- confidence = min(180, 120 + 4·len + (m ≥ 2 ? 20 : 0)) — moderate,
  expressed uncertainty.

### 5.2 CORROBORATE — strengthen adopted units
Candidates: adopted units, newest first, whose bytes occur m ≥ 3 times
(≥2 *other* occurrences). Up to `CORR_BATCH`=6.
- kind=WORD_SPAN re-proposal of the adopted span (deliberate re-proposal;
  the student may judge R5 redundant — its right).
- `ground_count` = min(3, m−1) other occurrence spans, earliest first.
- confidence = min(220, 180 + 10·ground_count) (180–220: higher, still
  selective, never 255).

### 5.3 RELATE — link units
Up to `REL_BATCH`=7, in this order:
- GROUP (kind 3): pairs (adopted[0],adopted[1]), (adopted[2],adopted[3]),
  (adopted[4],adopted[5]) — up to 3. Head span = first unit, `aux_count`=1
  (second unit's span), `ground_count`=1 (head span), confidence 150.
- SAME_AS (kind 4): up to 3 fresh words scanned from `eff_cursor` (blocked
  check applies); the i-th fresh word pairs with adopted[i].
  Head span = fresh word, `aux_count`=1 (adopted unit's span),
  `ground_count`=1 (head span), confidence = min(170, 140 + 2·len).
- BOUNDARY (kind 2): one region-edge marker. be = min(cursor, stim_len);
  span = [max(0,be−16), be], skipped if shorter than 4 bytes.
  `aux_count`=0, `ground_count` = (be < stim_len) ? 1 : 0 with grounding
  [be, min(be+16, stim_len)] (the fresh side of the edge), confidence 145.

### 5.4 CONSOLIDATE — retract and summarize (low rate)
Up to `CONS_BATCH`=4 per turn, retracts first:
- RETRACT (kind 5): every span with `nrej` ≥ 2, not dead, whose latest
  proposal seq has no kind-5 record in history yet. Encoded per harness
  convention: `span_start` = target seq (= the span's latest proposal seq),
  `span_end` = target+1, `aux_count`=0, `ground_count`=0, confidence 128.
- BOUNDARY summaries: fill remaining slots (up to 4 total) with BOUNDARY
  proposals over the largest covered blocks (head spans of the most recent
  ≤256 kind 1–4 records, sorted by start, merged; largest blocks first):
  span = [b0, min(b0+64, b1)], `aux_count`=0, `ground_count`=0,
  confidence 140.

## 6. §P emission (frozen §B.3, byte-exact)

```
0..4   magic u32 = 1414550096   4..6  version u16 = 1
6..10  teacher_id u32 = 3       10..18 session_id u64
18..26 seq u64 (monotonic, continues maxseq+1)
26     kind u8 (1..5)
27..35 span_start u64           35..43 span_end u64 (span_start < span_end;
                                   RETRACT: target_seq / target_seq+1)
43     aux_count u8             44..  aux_count × 16B (u64 start, u64 end)
..     ground_count u8          ..    ground_count × 16B
..     confidence u8 (120–220 teaching; 128 retract; never 255, never 0)
..     checksum u64 = FNV-1a-64 over all preceding bytes
```

Proposals are built fully in memory, then written with one `nio_write_all`
to stdout. Iron rules preserved: spans only (no token ids / text), no
commands (no ADOPT kind; confidence is a weight), monotonic seq, checksum.

## 7. Diagnostics (stderr, deterministic)

```
V3TRACE phase=<0..3> name=<PHASE> adopt10=<n> consec_rej=<n> appeals10=<n> T=<n> adopted=<n> cursor=<n> fresh=<0/1> batch=<n>
V3PROP seq=<s> kind=<k> ss=<a> se=<b> naux=<n> ng=<n> conf=<c>
```

These make the phase computation auditable from the outside.

## 8. §C tripwire posture

The teacher keeps the conservative cumulative §C monitor evaluable and
never trips it by construction: confidence is never 255 (secondary
vocabulary-dump rule cannot fire; `maxconf_rate` = 0 so the main rule
cannot fire), and per-turn batch caps keep coverage far below 0.95 on any
realistic stimulus. Verification (§C battery) checks: synthetic smuggle and
vocab-dump tapes DO fire the monitor; this teacher's clean streams do not.

## 9. Fixed-size working state (B.2.5 declaration)

Stimulus ≤1048576 B; history ≤ 10+32·4096 B; adopted ≤64 spans;
spanstats ≤512 spans; blocked ≤ 4096+512 spans; occurrences ≤8/word;
batch ≤8 proposals (≤4096 B out). No heap growth across invocations —
every run re-derives everything from its arguments.
