# Crew B — Preregistration: native Zag composition layer (frozen 2026-09-27)

Workbase: `~/workspace/wb2/crewB` (detached worktree of `origin/tnn-native-lab`
@ `6a0bec5e5`). Source: copy of Crew A's frozen `build/wb_dialogue.zag`
renamed `build/wb2_dialogue.zag`. Toolchain pinned:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
No commits by Crew B (parent handles branch surgery). No changes to
`~/workspace/workbuddy/` or Crew A's tree.

Frozen battery: `~/workspace/wb2/crewA/battery/` (24 probes, strict scorer
`score_battery.py`). Baseline: **2 PASS / 1 WEAK / 21 FAIL**.

## 1. HTD hypothesis debates

### T1 — comparison over session facts (bar: ≥7/9)

| # | Hypothesis | Debate | Verdict |
|---|---|---|---|
| H1 | Extend `do_compare`/`cmp_scan`: add more/most/fewer/fewest/less words | `do_compare` resolves entities only through the gazetteer (`ge`/`gnames`), which contains no session entities ("ana", "cara", "the north tank" are novel). Extending its word list cannot see taught facts. Also its two-entity slot design cannot do the 3-entity extremum (T1d). | KILLED |
| H2 | Register session entities into the gazetteer at teach time, reuse old compare | The gazetteer is a fixed install-time structure (32KB, entity-class metadata, `gord` ordering). Mutating it at runtime breaks the frozen-KB invariant and risks the S1 byte-identity gate. Session facts are not KB facts. | KILLED |
| H3 | New session-fact composition operator: for each candidate name in the question, find the newest live session quantity-fact with a matching subject, extract (value, verb, unit), order by direction word, render from the fact's own verb/unit | General: works for any taught subject/quantity, no entity lists. Falls through (returns 0) unless ≥2 names ground to quantity facts with compatible units — so KB-entity comparisons (S1) reach the old path untouched. Handles the 3-entity extremum (most/fewest) by construction. | CHOSEN |

Kill bar for H3: S1 turns `which is taller, the eiffel tower or the
montparnasse tower?` / `who was born first, darwin or melville?` must reach
the legacy path (proven by S1 byte-identity gate §5). No confident-wrong:
withhold unless fully grounded.

### T2 — anaphora over taught entities (bar: ≥3/4)

| # | Hypothesis | Debate | Verdict |
|---|---|---|---|
| H1 | Extend `sal`/gazetteer pronoun machinery to plurals | Same gazetteer blindness as T1-H1; plural "those two" has no slot anywhere in the existing machinery. | KILLED |
| H2a | Resolve he/she at teach time by rewriting stored text; resolve they/those-two/these-two/the-two at query time against a session subject stack | Teach-time rewrite makes the stored fact self-contained ("captain ray commands the ship."), so ALL existing machinery (retrieval, yes/no, bullets, state-choice) works with zero changes. Query-time plural resolution needs no stored rewrite because the question carries the anaphor. | CHOSEN |
| H2b | Resolve everything at query time, keep raw "he commands the ship." stored | Every consumer (retrieve, G6, state-choice, bullets) would need pronoun awareness; larger blast radius, more regression risk. | KILLED |

Kill bars for H2a: (a) "it" is NEVER teach-resolved — no noun-class
knowledge exists to bind it safely, and a wrong binding would be a new
confident-wrong; (b) he/she bind only to a most-recent subject that does
NOT start with an article (proper-name heuristic: "captain ray" binds,
"the pump" does not); (c) pure-pronoun subjects (they/it/we/you) are never
pushed on the stack.

### T3 — correction supersede (bar: 4/4)

| # | Hypothesis | Debate | Verdict |
|---|---|---|---|
| H1 | Tombstone/lifecycle flag on the 40-byte `fm` record | All 40 bytes are occupied (fid/key_off/key_len/val/text_off/text_len/ent_off/ent_n/unit_off/unit_len). Encoding lifecycle in fid or a side arena forces every scanner to change; high regression risk. | KILLED |
| H2 | In-place upsert keyed by (subject, verb) signature; correction-shaped turns strip the marker ("no,", "not that", "i meant") and upsert the remainder; plain re-teaching of the same slot also upserts | Observable semantics identical to tombstoning (old text unreachable, new text live, same fid/slot) with ZERO scanner changes — every reader sees only live facts. Uniform lifecycle: a session-fact slot is keyed, not appended. | CHOSEN |
| H3 | Correction handled only in the after-teaching position (§4b) | Task explicitly requires both turn positions (§1 after-question AND §4b after-teaching). | KILLED |

Kill bars: T3c-critical stays PASS; T5b stays honest-withhold; S1 and the
batch battery byte-identical (upsert ≡ append when no signature clashes);
no new confident-wrong answers anywhere.

Subject split uses a CLOSED grammatical verb class (aux/copula +
common action verbs, §3), never content words.

### T4 — brief bullets (bar: 2/2)

| # | Hypothesis | Debate | Verdict |
|---|---|---|---|
| H1 | Multi-line response, one bullet per line | The runner only captures `A `-prefixed lines; bullets 2..n would be lost. | KILLED |
| H2 | Single-line composition: `- f1. - f2. - f3.` from verbatim live session-fact texts, topic-matched (shared stemmed content word), padded with most-recent facts to the requested count | Satisfies the scorer's bullet-marker regex; every bullet is a verbatim taught fact (no generation risk); falls through when there are no session facts. | CHOSEN |

Kill bar: s2 turn 16 (`draft three morning-brief bullets about disk space.`
with zero session facts) must still withhold exactly as today.

### T5 — work-order review (bar: 2/2, T5a a grounded full PASS)

| # | Hypothesis | Debate | Verdict |
|---|---|---|---|
| H1 | Template review that always finds a gap | Would invent gaps = confident-wrong; violates the preserved honest-withhold. | KILLED |
| H2 | Hole detector: extract (number, unit) pairs from the WO text and from relevant live session facts (relevance = ≥1 shared stemmed non-stopword); report a hole ONLY when a fact pair and a WO pair share the stemmed unit with different numbers; withhold when no relevant facts or no mismatch | Grounded: the judgment cites the taught fact verbatim. T5b (no relevant facts) keeps withholding. | CHOSEN |

Kill bar: no review may invent a gap; T5b answer stays `I don't know.`

### T6 — further composition (bar: ≥2/3)

| # | Hypothesis | Verdict |
|---|---|---|
| H-count | `how many facts/things did i teach you?` → count live session facts (fid ≥ 100000) | CHOSEN |
| H-yesno | `did X <verb> more/fewer/less <unit> than Y?` → resolve X,Y to session subjects, compare unit-matched quantities | CHOSEN |
| H-sum | `how many <unit> … in total?` → resolve `the two <noun>` via the subject stack, sum unit-matched quantities | CHOSEN |

Kill bar for all: return 0 (fall through to legacy machinery) unless every
binding step is grounded in live session facts.

## 2. Frozen kill bars (targets)

| Target | Bar | Baseline |
|---|---|---|
| T1 Compare | ≥7/9 | 0/9 |
| T2 Anaphora | ≥3/4 | 0/4 |
| T3 Supersede | 4/4 | 1/4 |
| T4 Bullets | 2/2 | 0/2 |
| T5 Review | 2/2, T5a a grounded full PASS (not a withhold) | 1 PASS + 1 WEAK |
| T6 Further | ≥2/3 | 0/3 |

Preserved: T3c-critical PASS · T5b honest-withhold PASS ·
zero new confident-wrong answers · frozen S1 answer stream byte-identical ·
round-1 reproduction sessions byte-identical (see §5 for the applicable set).

One bounded repair loop per target, max. A missed bar after one loop is
documented honestly, not patched around.

## 3. Design specification (frozen)

**Session subject stack** (`ssub` arena, 260B, allocated in main, passed
through `do_turn` → `do_compose`): entries are (fact-slot fx, subject-length
slen); subject text is a prefix of the fact's stored text, so no text
duplication. Most-recent-last, dedup by fx, cap 32, pure-pronoun subjects
never pushed.

**Subject split**: subject = text before the first token in the closed verb
class; verb = that token; if none, subject = whole text, verb = "". Verb
class (grammatical, not content): is are was were be been being has have
had do does did will would shall should can could may might must + common
action verbs need/needs destroy/destroys/destroyed sell/sells/sold
hold/holds filled fill change/changed launch/launched reach/reached
command/commands detect/detected paint/painted open/opened close/closed
break/broke fix/fixed find/found make/made take/took give/gave get/got
go/went come/came run/ran fly/flew drive/drove build/built write/wrote
eat/ate say/said tell/told ask/asked classify/classified expose/exposed
pass/passed route/routed.

**Signature**: (lowercased subject, verb). Upsert: strip correction marker →
if teach-shaped → extract signature → if a live session fact (fid≥100000)
has the same signature, rewrite its text/keys/value/entities/unit in place
(same fid/slot); else append via existing `session_teach`. Teach-time
pronoun rewrite: subject he/she → most recent stack subject without a
leading article; "it"/"they" never rewritten.

**Quantity parse** (per fact text): first number token (digit or numword);
verb_q = word before it; unit = word after it; value = number. No number →
not a quantity fact.

**Operators** (each returns 1 = responded, 0 = fall through), called at the
top of `do_compose` in this order:
1. `wb2_bullets` — `draft <n> bullet(s)…`; topic after `about`; candidates
   = live session facts sharing a stemmed content word with the topic
   (oldest-first), padded with most-recent others to n; render single line
   `- f1. - f2. - f3.`
2. `wb2_review` — `review …: <WO text>`; relevant facts = shared stemmed
   non-stopword; hole = (number, unit) pair with same stemmed unit,
   different number; render
   `hole: the work order says <wo-num> <wo-unit>, but you taught me <fact>`
3. `wb2_count` — `how many facts/things did i teach you` → `<n> facts.`
4. `wb2_sum` — `how many <unit> … in total` → resolve `the two <noun>` via
   stack, sum unit-matched values → `<sum> <unit>.`
5. `wb2_didcmp` — `did X <v> more/fewer/less <unit> than Y?` → `yes.`/`no.`
6. `wb2_ana` — `those two|these two|the two [<noun>]` or leading `they` +
   compare intent → resolve two stack subjects → delegate to compare core
7. `wb2_cmp` — compare intent words
   (taller/tallest/shorter/shortest/more/most/fewer/fewest/less/least);
   names = segments after the intent word split on `,`/`or`, each matching
   a taught subject; ≥2 grounded quantity facts with compatible stemmed
   units → render: tall-type `<name> is taller.` / `<name> is shorter.`;
   more-type `<name> <verb> more <unit>.` / fewer / `the most` / `the fewest`
8. `wb2_state` — `was/is <subj> <A> or <B>?` → `<subj> was <matched>.`;
   `was/is <subj> <S>?` → `yes.`/`no.` from the newest live session fact
   with matching (subject, verb)

**§1 correction hook** (after-question position): inside the existing
`is_correction` block, first strip the marker; if the remainder is
teach-shaped and its signature matches a live session fact → upsert,
respond `Noted.`, teaching-style bookkeeping, return. Else → legacy re-ask
path unchanged.

**§4b** (after-teaching position): correction-shaped → strip + upsert;
otherwise → upsert (≡ append when no signature clash). Response stays
`Noted.`

**Response strings** (frozen): `Noted.` · `<name> is taller.` /
`<name> is shorter.` · `<name> <verb> more <unit>.` /
`<name> <verb> fewer <unit>.` / `<name> <verb> the most <unit>.` /
`<name> <verb> the fewest <unit>.` · `captain ray commands the ship.` ·
`yes.` / `no.` · `- f1. - f2. - f3.` ·
`hole: the work order says <n> <u>, but you taught me <fact>` ·
`I don't know.` · `<n> facts.` · `<sum> <unit>.`

## 4. Hold-out discipline

Held out of the dev loop (never run until the final frozen evaluation):
**T1e, T1f, T2b, T2d, T3c, T4b, T5b, T6c.** Dev set: the remaining probes.
Generalization probes (`gen/`) must use entities/quantities never seen
during development. One repair loop per target, then freeze.

## 5. Regression gates (all must pass)

1. S1 chat answer-stream SHA-256 =
   `3d60c4e33c0259b12fd7d27363aed6e8eca095a75bbc8a4daadcc2b6bbcf418f`
   (normal + allocator-perturbation runs).
2. `battery.txt` batch answer stream byte-identical to Crew A's frozen
   binary output.
3. `base_anaph.txt`, `val_teach.txt` byte-identical (no machinery touches
   those paths).
4. `base_correct.txt`, `val_shapes.txt`: INTENDED improvements (correction
   supersede now works; stale-fact serving fixed). Every diff vs the frozen
   binary is listed verbatim in RESULTS.md as an intended fix, not a
   regression.
5. New binary runs each battery session twice → byte-identical (determinism).

## 6. Implementation order (caller-safe: every callee defined before caller)

1. New block before `cmp_scan`: tokenizer, verb class, subject split,
   signature compare, ssub stack ops, correction strip, teach-time pronoun
   rewrite, `session_upsert`, quantity parse, the 8 operators.
2. `do_compose`: 8 operator calls at top.
3. `do_turn` §1: supersede branch; §4b: strip+upsert.
4. `do_turn`/`do_compose` signatures: append `ssub:[]u8`; update the two
   `main` call sites; allocate `ssub` in main.
5. Compile with pinned znc from `build/` (cwd = build dir: imports and
   `kb.txt`/`gaz.txt` resolve there).
