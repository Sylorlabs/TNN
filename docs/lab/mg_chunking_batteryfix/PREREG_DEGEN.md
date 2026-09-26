# PREREG_DEGEN — degenerate-input hardening sweep (2026-09-26)

Follow-up to the chunking battery fix (Micah order 2026-09-26 ~12:52 PDT):
"for panic continue it." Extend panic-hardening beyond W25.

## Item 1 — cand_span decision (preregistered)

`cand_span` (candidates 7/8, SPAN3/SPAN5) contains unguarded `t[0]` /
`t[t.len-1]` for kinds 8/9. Reachability proof (by exhaustive code reading):

1. Only callers of `cand_span`: `cand_answer`'s `c==7` / `c==8` branches.
2. Only caller of `cand_answer`: `tnn_intake`, with `c = policy_winner(kind, shape)`.
3. `policy_winner`'s return statements, exhaustively: {1, 2, 3, 6, 9, 10}.
   No branch returns 7 or 8.
4. Therefore `cand_span` is unreachable through every production path.

**Decision: REMOVE `cand_span` entirely** (function + both dispatch branches),
not harden. A hardened-but-dead function is still a maintenance trap; the
proof above is the record. `cand_name`'s "SPAN3"/"SPAN5" name strings stay
(harmless name table, no indexing).

Hazards found LIVE by the same reading (to harden, not remove):

- **H1** `cand_zoom` kind-7 arm reads `woffs[0]` with no `nw>0` check.
  Reachable: policy(7, shape=0)=3. Empty/whitespace text → uninitialized slot
  read → garbage slice → panic or garbage answer. **Harden: nw==0 → '?'.**
- **H2** `cand_word` kind-16 arm: `k=nw-1` → with nw=0, k=-1 →
  `r_u32le(woffs,-4)` negative read. Reachable: policy(16)=2.
  **Harden: nw==0 → '?'.**
- **H3** `cand_word` kind-7 arm: same unguarded `woffs[0]` pattern.
  Unreachable via policy (kind 7 never routes to candidate 2), but the
  identical hazard shape — **harden defensively** (nw==0 → '?'), zero
  behavior change on reachable paths.

## Item 2 — degenerate sweep (41 cases, battery3.zag)

Bar: every case answers or refuses cleanly — **no panics, ever**.
`correct=` is scored against `exp` below; the sweep passes 100% only with
zero panics AND all expected answers.

### A. Empty text × every kind (t="")

| id | question | kind | exp | rationale |
|---|---|---|---|---|
| D00 | "how many e's in " | 1 | "0" | scan_count over empty = 0 |
| D01 | "what is the 1st letter of " | 2 | "?" | W25 guard (ll==0) |
| D02 | "write  backwards" | 3 | "" | reverse of empty is empty |
| D03 | "how many words in " | 4 | "0" | enum_words = 0 |
| D04 | "how many letters in " | 5 | "0" | t.len = 0 |
| D05 | "does  contain z" | 6 | "no" | needle not found |
| D06 | "what is the first word of " | 7 | "?" | H1 hardened |
| D07 | "what is the first letter of " | 8 | "?" | cand_zoom ll==0 guard |
| D08 | "what is the last letter of " | 9 | "?" | cand_zoom ll==0 guard |
| D09 | "how many e's in the word after the in " | 10 | "?" | anchor not found |
| D10 | "how many letters in the word after the in " | 11 | "?" | anchor not found |
| D11 | "what is the 1st letter of the word after the in " | 12 | "?" | ws_locate fails |
| D12 | "write the word after quick backwards in " | 13 | "?" | target not found |
| D13 | "what is the first letter of the word after the in " | 14 | "?" | ws_locate fails |
| D14 | "what is the last letter of the word after the in " | 15 | "?" | ws_locate fails |
| D15 | "what is the last word of " | 16 | "?" | H2 hardened |
| D16 | "does the word after the contain z in " | 17 | "?" | k<0 |
| D17 | "how many sentences in " | 18 | "0" | gran_split = 0 |
| D18 | "what is the 1st sentence of " | 19 | "?" | si >= nseg |
| D19 | "what is the 2nd word of the 1st sentence of " | 20 | "?" | no granule |
| D20 | "what is the letter after the 2nd letter of fox in " | 21 | "?" | target not found |
| D21 | "what is the 1st letter of the 2nd word of the last word of " | 22 | "?" | nesting withhold |
| D22 | "ponder the void" | 0 | "" | unknown kind → empty answer (clean, deterministic) |

### B. Single-char text (t="x")

| id | question | exp | rationale |
|---|---|---|---|
| D23 | "what is the 1st letter of x" | "x" | |
| D24 | "what is the 5th letter of x" | "x" | pre-existing clamp-to-last (idx>=ll → ll-1); documented wart, not a panic |
| D25 | "what is the last letter of x" | "x" | |
| D26 | "how many e's in x" | "0" | |
| D27 | "write x backwards" | "x" | |

### C. All-whitespace text (t="   ")

| id | question | exp | rationale |
|---|---|---|---|
| D28 | "how many words in    " | "0" | no words |
| D29 | "what is the 1st letter of    " | " " | tw==t → whole-text span, idx 0 → space; clean |
| D30 | "what is the first word of    " | "?" | nw=0 (H1 shape=1 → cand_char arm is clean: t[0..0]="") |

Note D30: t="   " has spaces → shape=1 → policy(7,1)=1 → cand_char kind-7
arm (`ans=t[0..e]`, e=0 → ""). Hmm — that gives "" not "?".
Re-examine: cand_char kind-7: e=t.len=3; loop: t[0]==32 → e=0,stop=1;
ans=t[0..0]="". So D30 exp should be "" — clean. Preregister "".

### D. Position past end / zero / negative

| id | question (t="abc") | exp | rationale |
|---|---|---|---|
| D31 | "what is the 99th letter of abc" | "c" | clamp-to-last wart |
| D32 | "what is the 0th letter of abc" | "a" | idx<0 → 0 clamp wart |
| D33 | "what is the 1st letter of the last word of abc" | "a" | wn=-1 legitimate path |
| D34 | "what is the 2nd letter of the last word of " (t="") | "?" | empty |
| D40 | "what is the -1th letter of abc" | "a" | parse_digits stops at '-' → 0 → clamp wart |

### E. Empty question

| id | question | text | exp |
|---|---|---|---|
| D35 | "" | "abc" | "" | kind 0 → empty answer (clean) |

### F. More degenerate shapes

| id | question | text | exp | rationale |
|---|---|---|---|---|
| D36 | "how many lines in \n" | "\n" | "0" | gran_split drops empties |
| D37 | "how many sentences in a" | "a" | "1" | one segment |
| D38 | "what is the first word of  " | " " | "" | cand_char kind-7 → t[0..0] |
| D39 | "what is the 100th word of the 1st sentence of abc" | "abc" | "?" | wpos > nw2 |

## Item 3 — permanent battery

`battery3.zag` joins `battery1.zag` (57Q) and `battery2.zag` (26 traps) in
the deliverable; `build.sh` runs all three and requires: wall 26/26,
production 57/57, degenerate 41/41 clean, all byte-identical across two runs.

## Verification protocol

1. `cand_span` removal: `grep -c "cand_span" intake.zag` → 0; wall+production
   outputs byte-identical to pre-removal (dead code cannot change behavior).
2. H1/H2/H3: degenerate battery 41/41 with zero panics, two runs byte-identical.
3. Regression: wall 26/26 SHA `cd86da43…`, production 57/57 SHA `170bacd71…`
   (unchanged); telemetry audit 0 mismatches.
4. `build.sh` extended to run battery3; all three green from the deliverable.
