# Chunking next-wall battery: red-team cause analysis (2026-09-26)

Red-team investigator report. Deliverable is CAUSES, not fixes — a fix crew follows.
Pure analysis; no production code was changed.

**Scope:** the 26-trap fresh battery (`docs/lab/mg_chunking_nextwall/battery2.zag`)
run through the frozen production intake (`docs/lab/mg_chunking_promote/intake.zag`,
assembled by `assemble.py` from `base.zag` + `hand_a/b/c1/c2/c3.zag` + the frozen
learned policy; promoted in commit `e74271015a7d`).

**Reproduction (done, not trusted blindly):**
- Built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  from the `mg_chunking_nextwall/` dir (`@import` resolves relative to CWD).
- Output **byte-identical** to `evidence/WALL1.out`
  (SHA-256 `3cc35d29032cf0e2b367db5006606b28efdd5b3937db7b56c09b16b415541fc2`):
  **14/26 correct, 0 panics** (post-fix intake).
- The 12 misses are qids **0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19**
  (W00–W08 except W09, plus W17, W18, W19).
- Parser decisions below were confirmed with a scratch probe (`probe.zag`,
  kept out of the repo) that calls `classify` / `parse_pos_n` / `parse_after` /
  `parse_wordref` directly on each trap question. Quoted values are observed,
  not inferred.
- W25 was verified against a reconstructed pre-fix intake (guard weakened to
  the committed pre-fix form `if (loc<0)`): deterministic
  `panic: slice index out of bounds` at qid 25, first 25 INTAKER lines
  byte-identical to the preserved `evidence/WALL0_PREFIX_PANIC.out`.

---

## Class 1 — Parser vocabulary: no sentence/line concepts (W00, W01, W02, W19)

**Reproduction.**
```
INTAKE qid=0 kind=KIND0 chunk=WORD why="question unclassified by the parser (kind 0); ..."
INTAKER ans="" exp="2" correct=0      # W00: how many sentences in "the cat sat. the dog ran."
INTAKER ans="" exp="the dog ran" correct=0   # W01: what is the 2nd sentence of ...
INTAKER ans="" exp="3" correct=0      # W02: how many lines in a\nb\nc (t has real newlines)
INTAKER ans="" exp="cat" correct=0    # W19: what is the 2nd word of the 1st sentence of ...
```

**Traced cause.** `classify()` (`intake.zag` lines 207–243) is a fixed
`has_sub` cascade over 17 kinds. There is no branch mentioning "sentence",
"sentences", "line", or "lines". All four questions fall through to
`return 0`. `tnn_intake` (line 2049) then calls `policy_winner(0,shape)`,
which falls through to `return 3`, routing to `cand_zoom` → `cand_zoom_19`
(line 1018). `cand_zoom_19` has arms for kinds 1–9 only; **no `kind==0` arm
exists**, so `ans` stays `abuf[0..0]` — the empty string — unconditionally
(ops=0, maxdepth=0, zooms=0 on all four lines). The KIND0 answer is not
"wrong addressing"; it is "no code path".

Note W19 specifically: the probe shows `parse_wordref` *did* parse the word
half (`wn=2`, inner=`"the 1st sentence of the cat sat. the dog ran."`), but
`classify`'s `" word of "` branch only yields kind 17 when `"contain "` is
also present — otherwise it falls through to 0. So even the word-level
subclause is unclassifiable.

**Mechanism named.** Fixed-vocabulary classifier with no sentence/line
branches; kind-0 fallthrough in `cand_zoom_19` answers empty by construction.

**Gap: (a) KNOWLEDGE.** The byte machinery can already express three of the
four answers: `scan_count(t,0,t.len,46)` counts periods (W00 → 2);
`scan_count` of byte 10 counts newlines (W02 → 3); W01/W19 need
split-on-delimiter + index, i.e. `enum_words` parameterized by a delimiter
instead of hardcoded space (line 132–147 splits on byte 32 only). What is
missing is an **instrument for TNN to place delimiter knowledge into the
classifier**: an extensible binding of (question-shape → primitive +
delimiter operand), e.g. "how many sentences" → count-byte('.'),
"how many lines" → count-byte('\n'), "Nth sentence" → split('.')+index.
TNN knows what a sentence/line is; there is nowhere to put that knowledge.

**Fix direction.** Add a classifier extension table (shape → kind/primitive +
delimiter byte) writable from TNN-side knowledge, plus a
delimiter-parameterized splitter beside `enum_words`; keep the kind-0 arm
answering empty (honest) when no binding exists.

---

## Class 2 — Spelled ordinals unreadable (W07, W08)

**Reproduction.**
```
INTAKE qid=7 kind=POSITION chunk=CHAR ...   # "what is the second letter of strawberry"
INTAKER ans="s" exp="t" correct=0
INTAKE qid=8 kind=LENGTH_WORD chunk=WORD ...  # "how many letters in the third word of the quick brown fox"
INTAKER ans="?" exp="5" correct=0
```
Probe: W07 `posn=0 tw="strawberry"`; W08 `wn=0 inner="the quick brown fox"`.

**Traced cause.** Both ordinals go through `parse_digits` (lines 115–130),
which reads a run of ASCII digits starting exactly at the given offset and
returns 0 when the first byte is not a digit.
- W07: `parse_pos_n` (line 188) does `find_sub(q,"the ")` → the first
  `"the "` precedes "**second**", so `parse_digits("second letter…",0)` = 0.
  `idx = 0-1 = -1` → clamped to 0 → `t[0]` = `'s'`. The kind (POSITION) and
  the locate (`tw="strawberry"` == whole text) were both right; only the
  ordinal was misread.
- W08: `classify` correctly yields kind 11 (LENGTH_WORD). `parse_wordref`
  (line 274) extracts the token between the last `"the "` and `" word of "`:
  `"third"` → `parse_digits("third",0)` = 0 → `wn=0` → `wn_index(0,4)` = -1
  → the `k<0` arm answers `'?'`.

**Mechanism named.** Digit-only ordinal reader: `parse_digits` returns 0 for
any spelled ordinal, and both callers treat 0 as a real ordinal (clamp to
index 0 / word-index −1) instead of as "unparsed".

**Gap: (a) KNOWLEDGE.** This is the textbook case: TNN knows
"second" = 2nd and "third" = 3rd, and the downstream machinery (index the
Nth letter, measure the Nth word) works — the derivation battery proved it
on digit ordinals. The missing instrument is an **ordinal-knowledge hook in
the address parser**: a word→number table that `parse_pos_n` and
`parse_wordref` consult before/​instead-of the hardcoded digit-run reader.

**Fix direction.** Ordinal table consulted by both parse functions
(`"first"→1 … "twelfth"→12`, plus digit forms); treat still-unparsed as
abstain `'?'` rather than 0.

---

## Class 3 — Relative word addressing missing (W04, W05, W06)

**Reproduction.**
```
INTAKE qid=4 kind=LETTER_COUNT chunk=CHAR ...  # "how many e's in the word after the in the cheese wheel"
INTAKER ans="6" exp="3" correct=0
INTAKE qid=5 kind=POSITION chunk=WORD>CHAR ... # "what is the 1st letter of the word before fox in the quick brown fox"
INTAKER ans="?" exp="b" correct=0
INTAKE qid=6 kind=REVERSE chunk=CHAR ...       # "spell the word after quick backwards in the quick brown fox"
INTAKER ans="xof nworb kciuq eht" exp="nworb" correct=0
```
Probe: W04 `kind=1 has_of=0 tgt='e'`; W05 `kind=2 posn=1 tw="the word before fox in the quick brown fox"`;
W06 `kind=3 has_of=0`.

**Traced cause.** `parse_wordref` (line 274) only understands the literal
marker `" word of "` with a digit/`"last"` token. None of the three
questions contain `" word of "`, and there is no `"after"`/`"before"`
vocabulary anywhere in the parser.
- W04 → kind 1 (LETTER_COUNT). `cand_char`'s kind==1 arm (line 582)
  counts `parse_target_letter(q)`=`'e'` over the **whole text**:
  "the"(1) + "cheese"(3) + "wheel"(2) = 6. There is no "count within the
  word after X" path because X was never addressed.
- W05 → kind 2. `parse_pos_n` correctly yields 1, but `zoom_locate`
  (line 997) takes `parse_after(q,"of ")` = `"the word before fox in the
  quick brown fox"` as the target literal; `find_word` cannot match a
  multi-word literal → `loc=-1` → `'?'`.
- W06 → kind 3 (REVERSE): `classify` routes `"backwards"` without
  `" word of "` to kind 3, and `cand_zoom_19`'s kind==3 arm (line 1114)
  does `reverse_into(t,revbuf)` — whole-text reversal, the observed
  `"xof nworb kciuq eht"`. Notably, **word-scoped reversal machinery already
  exists** (`cand_zoom` kind==13 arm reverses the located word; candidate 5
  `cand_revword` too) — it is simply unreachable: nothing can address
  "the word after quick" to feed it.

**Mechanism named.** Address parser with a closed ordinal vocabulary
(`"the <digits>|last word of"`); no relative ("after"/"before") word
addressing; whole-text fallback (count) or whole-text operation (reverse)
when the relative clause is ignored.

**Gap: (a) KNOWLEDGE.** The downstream operations all exist and are proven:
locate word #N then count/index/reverse inside it (kinds 10–15). The only
missing link is mapping "the word after|before X" → `(index of X) ± 1`.
TNN knows what "after" means; the missing instrument is a
**relative-ordinal resolver** feeding the existing `wn` path — one
instrument fixes W04, W05, and (with routing to the existing kind-13 arm)
W06.

**Fix direction.** Teach the word addresser relative ordinals
(`after X` → successor, `before X` → predecessor, with occurrence
selection per the W17 convention below); route resolved relative refs into
the kind 10–15 machinery; never silently fall back to whole-text when a
relative clause was present but unparsed (answer `'?'`).

---

## Class 4 — Greedy target capture; two-hop relative letter addressing (W03, W17)

**Reproduction.**
```
INTAKE qid=3 kind=POSITION chunk=WORD>CHAR ... # "what is the letter after the 2nd letter of fox in the quick brown fox"
INTAKER ans="?" exp="x" correct=0
INTAKE qid=17 kind=POSITION chunk=WORD>CHAR ... # "what is the 2nd letter of the in the quick brown the fox"
INTAKER ans="?" exp="h" correct=0
```
Probe: W03 `tw="fox in the quick brown fox"`; W17 `tw="the in the quick brown the fox"`.

**Traced cause.** `zoom_locate` (line 997) computes its target with
`parse_after(q,"of ")` (line 192): `find_sub` for the **first** `"of "` and
returns **everything after it** to end-of-question. Any question carrying a
context clause after the target (`"...in the quick brown fox"`) produces a
multi-word pseudo-target. `find_word` (line 164) matches whole single words
only, so the lookup fails deterministically (`k<0` → `oo=0, ll=0`,
`return -1`) and both answer `'?'` via the `loc<0` arm.
- W17: PREREG specifies the oracle convention "repeated target word
  ('the' ×3); oracle = first occurrence" → exp `'h'`. Had the target been
  delimited to `"the"`, `find_word` returns the first match and the answer
  would be `'h'`. The failure is purely the undelimited capture, not
  occurrence ambiguity (all three occurrences agree on the answer here).
- W03: additionally needs **two-hop** addressing — resolve "2nd letter of
  fox" to a position, then step one letter forward ("the letter after").
  No routine composes two addressing operations; addressing is single-hop
  by construction (one `zoom_locate` + one index per question).

**Mechanism named.** `parse_after` is a marker→end-of-string cut with no
delimiter concept; the addressing layer is single-hop, so relative
letter-offsets over a resolved position cannot be composed.

**Gap: (b) MACHINERY.** No existing mechanism delimits the target word
(`parse_after` cannot express "the word right after 'of'"), and no
mechanism composes two addressing hops. These must be built, not taught.

**Fix direction.** Delimiter-aware target extraction (target = first word
after the marker, not the tail); first-occurrence convention for repeats
(per PREREG); a two-hop addressing composition for relative letter offsets.

---

## Class 5 — Silent nesting collapse; should have abstained (W18)

**Reproduction.**
```
INTAKE qid=18 kind=FIRST_LETTER_WORD chunk=WORD>CHAR ...
INTAKER ans="w" exp="?" correct=0 ops=4 maxdepth=2 zooms=2
```
Q: "what is the 1st letter of the 2nd word of the last word of hello worldly words".
PREREG: "true two-level nesting; designed unanswerable ('?' = honest abstention)".
Oracle note: the last word "words" has no 2nd word.

**Traced cause.** `classify` yields kind 14 (FIRST_LETTER_WORD).
`parse_wordref` (line 274) finds the **first** `" word of "`, takes the token
after the last `"the "` before it (`"2nd"` → `wn=2`), and returns the rest —
`"the last word of hello worldly words"` — as `inner`. The kind-14 handler
in `cand_zoom` then indexes word #2 of the full text (`"worldly"`) and
returns its first letter `'w'`. The residual nesting in `inner` is
**discarded without inspection by every kind 10–17 handler** — none checks
whether `inner` still contains an unresolved `" word of "`. The question's
true structure (2nd word *of the last word*) is silently collapsed to one
level, producing a confident wrong answer on a trap whose correct behavior
is abstention.

**Mechanism named.** Single-level `"Nth word of"` resolution with the
unresolved tail returned-but-never-checked; no nesting-depth detection, no
abstention on residual structure.

**Gap: (c) GENUINELY UNANSWERABLE — the bug is answering instead of
abstaining.** The oracle's `'?'` is the designed-correct behavior (the last
word has no 2nd word). Nothing about the input is ambiguous to a human
either: the question is well-formed but unanswerable. The defect is that the
machinery cannot tell "resolved" from "silently dropped a level".

**Fix direction.** After `parse_wordref`, if the returned `inner` tail
still contains an addressing marker (`" word of "`, and by extension the
Class-4 delimiters), the question nested deeper than the machinery resolves
→ answer `'?'` (withhold), never a partial-level answer. The check is
cheap: the residual is already returned; it is just never read.

---

## Class 6 — Deterministic panic on empty-text position (W25) — FIXED, cause verified

**Reproduction (pre-fix).** Reconstructed pre-fix intake (guard weakened to
the committed pre-fix form, see below); binary exits rc=1 with
`panic: slice index out of bounds` at qid 25; the first 25 INTAKER lines are
byte-identical to the preserved `evidence/WALL0_PREFIX_PANIC.out`.

**Traced cause.** W25: q=`"what is the 1st letter of "`, t=`""`.
`tnn_intake` → kind 2 (POSITION), single shape → `cand_zoom_19` kind==2 arm.
`zoom_locate`: `tw = parse_after(q,"of ")` = `""`; the whole-text fast path
`if (beq(tw,t)==1)` compares empty-to-empty → true → returns
`(oo=0, ll=0, loc=0)`. Pre-fix, the arm checked only `if (loc<0)` — and
`loc==0`, so it fell into the else: `n=1, idx=0`; `idx>=ll` (0>=0) →
`idx = ll-1 = -1`; single shape → `c==1` → `abuf[0] = t[oo+idx]` = **`t[-1]`**
→ `panic: slice index out of bounds`. Deterministic: same input, same
negative index, every run. (The kind==8/9 arms had the identical shape:
`t[oo]` / `t[oo+ll-1]` on a zero-length span.)

**Fix-crew diagnosis: independently confirmed.** Commit `9147094613`
("Chunking: fix deterministic W25 panic") changed exactly 3 lines:
`if (loc<0)` → `if (loc<0 || ll==0)` at the kind 2/8/9 arms of
`cand_zoom_19` (lines 1058, 1080, 1098), answering `'?'` like a miss.
My pre/post comparison: qids 0–24 byte-identical, W25 now
`ans="?" exp="?" correct=1`, rc=0, reruns byte-identical
(`evidence/WALL1.out`/`WALL2.out` SHA
`3cc35d29032cf0e2b367db5006606b28efdd5b3937db7b56c09b16b415541fc2`).
The crew also added a degenerate regression battery
(`regress_degen.zag`, `build_regress.sh`, `evidence/DEGEN1/2.out`).
Cause attribution in their VERDICT addendum matches this analysis exactly.

**Gap: robustness bug (fixed).** No classification needed — closed.

---

## Cause table (for the fix crew)

| Failure | Mechanism (precise) | Gap | Missing instrument / fix direction |
|---|---|---|---|
| W00, W01, W02, W19 | `classify` (207–243) has no sentence/line branches → kind 0; `cand_zoom_19` has no kind-0 arm → answers `""` unconditionally | (a) KNOWLEDGE | Extensible classifier binding: (question-shape → primitive + delimiter byte); delimiter-parameterized splitter beside `enum_words` |
| W07, W08 | `parse_digits` (115) reads digit runs only: "second"→0→clamp→`'s'`; "third"→`wn=0`→`wn_index`=-1→`'?'` | (a) KNOWLEDGE | Ordinal-knowledge hook: word→number table consulted by `parse_pos_n`/`parse_wordref` |
| W04, W05 | `parse_wordref` (274) accepts only `"the <digits>\|last word of"`; no after/before vocabulary → whole-text count (6≠3) / failed locate (`'?'`) | (a) KNOWLEDGE | Relative-ordinal resolver: "word after\|before X" → `(index of X)±1` into the existing `wn` path (kinds 10–15) |
| W06 | `classify`→kind 3 on "backwards" w/o `" word of "`; kind-3 arm (1114) reverses whole text; existing word-scoped reverse (kind 13) unreachable | (a) KNOWLEDGE | Same relative-addressing instrument as W04/W05 + routing to the kind-13 arm |
| W03, W17 | `parse_after(q,"of ")` (192) takes first-`"of "`→end as an undelimited literal (`"fox in the quick brown fox"`); `find_word` can't match multi-word → `'?'` | (b) MACHINERY | Delimiter-aware target extraction (first word after marker); first-occurrence convention for repeats |
| W03 (2nd aspect) | No two-hop addressing: "letter after <resolved position>" can't be composed; addressing is single-hop by construction | (b) MACHINERY | Addressing composition (resolve inner, then offset) |
| W18 | `parse_wordref` resolves one `"Nth word of"` level; residual tail (`"the last word of …"`) discarded unchecked → answered `'w'` on a designed-unanswerable trap | (c) ABSTAIN | Check residual `inner` for unresolved markers → withhold `'?'` |
| W25 | Pre-fix kind 2/8/9 arms: `zoom_locate`'s `beq("","")` fast path → `(loc=0,ll=0)`; `idx`→`-1`; `t[-1]` panic | fixed (`9147094613`) | Independently verified; no further action |

## Secondary finding (telemetry, not a miss)

The `INTAKE` choice lines print chunk names from the hardcoded fork-era
`zoom_choose` (line 955) while `tnn_intake` (line 2049) actually routes via
the learned `policy_winner` (line 1775). E.g. W07's line reads
`kind=POSITION chunk=CHAR why="derived WORD>CHAR (class POSITION/single)…"` —
the `why` text and the `chunk` label contradict each other, and the executed
candidate was `cand_zoom` (policy winner 3), not `cand_char`. Any fix-crew
debugging that trusts the `chunk=` label will misread which machinery ran.
Recommend emitting `cand_name(policy_winner(kind,shape))`.

## Notes for the fix crew

- The learned policy itself (`policy_winner`) is untouched by all 12 misses:
  every miss traces to the hand-authored parser/addressing the derivation
  never exercised (classifier vocabulary, ordinal reader, target capture,
  nesting) — consistent with the wall VERDICT's conclusion.
- `parse_pos_n` reads the ordinal after the **first** `"the "` (W03 showed
  `posn=0` because the first `"the "` precedes "letter", not "2nd") — a
  second latent misread in the same function, worth fixing alongside the
  ordinal table.
- `parse_target_letter` (line 184) indexes `q[p-1]` with no absent-marker
  check — same latent shape as the W25 panic, on the question side.
