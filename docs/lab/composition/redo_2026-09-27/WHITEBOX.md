# WHITE-BOX: why the round-2 workbuddy learner cannot synthesize strings

**Date:** 2026-09-27. **Target:** `wb2_dialogue.zag` (SHA-256
`0bec5459b2959ec056c6c8771de7de009d7fd9406d7029d98fa97faa1a9d531b`),
the round-2 workbuddy binary source (binary SHA `7636a577…`), i.e. the
"real learner" of the D1 composition battery.
**Method:** exhaustive static audit of every response-writing code path,
plus intake-path inspection. No behavior changed.

## 1. The output channel is a verbatim-span concatenation machine

Every byte that ever reaches the response buffer arrives through exactly
two primitives:

- `rput(resp, s, so, sl)` — copies the contiguous span `s[so..so+sl]`
  **verbatim** into the response (95 call sites, all audited);
- one direct-write site (`do_turn`, line ~5794): a memmove-style right
  shift that prepends the literal bytes `Y e s . space` — all other bytes
  keep their order (verbatim prefix insertion, not a transform).

The source operand `s` at all 95 `rput(resp,…)` sites is one of:

| Operand | Sites | What it is |
|---|---|---|
| `ftx` / `ftl` | 12 | **stored fact text** — whole fact rows (`fact_text_into`, `emit_fact`) or contiguous sub-spans, always copied in source order |
| `gnames` | 13 | **stored entity names** from the gazetteer, verbatim |
| `ubuf` | 6 | **the user's own utterance** — contiguous spans echoed back verbatim (e.g. `? Because it's <user words>`) |
| `nbuf` / `nb` | 8 | **decimal digits of a computed integer** (`i64str`: counts, sums, year differences) — the ONLY computation-to-text operator, digits only |
| string literals | ~50 | hardcoded English fragments (`"I don't know."`, `" is taller."`, …) |
| `qbuf`,`histb`,`pre`,`nm`,… | 6 | other verbatim buffers (prior query text, history bytes, names) |

**There is no code path that**
(a) writes a source's bytes in a non-source order,
(b) writes a byte computed from a source byte by a letter mapping
    (upper/lower/replace — `i64str`'s digit extraction is the sole
    byte-deriving operator and emits `0`–`9` only),
(c) indexes into a stored string at a character position to extract a part
    (all span selections are whole-span or contiguous-verbatim copies).

Consequence: the set of strings the learner can ever emit is the
concatenation-closure of {taught fact texts, taught entity names, user
utterance spans, decimal integers, literals}. A novel string such as the
reverse of a held-out token (`qeum` → `mueq`) is **not in that closure** —
no operator exists that could produce it. This is why every string-rule
probe withholds: the machinery has no string-synthesis operator at all,
not a weak one.

## 2. The intake stores strings as opaque spans

Taught facts are stored as atomic text rows (`fm` rows: fid, key offsets,
`text_off`/`text_len`, …). The text is an **opaque byte span**: retrieval
matches on key metadata (subject/verb/complement signatures) and returns
whole rows. No answer-path code addresses a character *inside* a stored
span — matching uses whole-span/keyword comparisons (`find_sub`,
`word_find`, `beq2`), and every write copies the span verbatim (§1).
So even though intake *receives* `the letters of qeum are q e u m`,
nothing can reach into that span and pull out its 3rd letter: the
representation has no character-level addressing on the answer path.

## 3. Independent second mechanism: intake case-folding destroys P5's signal

`main`'s chat loop lowercases every input byte into `ubuf`
(`ubuf[k5]=to_low(line[k5])`). The P5 teaching line
`the upperfirst of abc is Abc.` therefore arrives at all machinery as
`the upperfirst of abc is abc.` — the uppercase distinction the rule
teaches is **erased before any learning machinery sees it**. Even a
learner with a perfect synthesis operator, learning only from `ubuf`,
would induce the identity map for P5. P5 is unlearnable through this
intake by construction — a separate causal block from §1.

(The amended battery's scorer compounds this: `norm_last_word`
lowercases the response before a case-sensitive `bufeq` against the
uppercase expected value, so P5 could never score even if answered
correctly — an instrument defect repaired in the redo scorer.)

## 4. Why no teaching protocol can fix this (Crew C, confirmed here)

The failure is not in teaching *content* (12/12 taught recall proves
receipt and storage) but in answer *machinery*: the operators the output
channel lacks (character addressing, byte permutation, case mapping)
cannot be installed through the intake, because intake only appends
opaque spans to the stores the existing operators read. This is an
architectural envelope fact: **retrieval-echo is all the channel can do.**

## 5. What a repair must supply (causal, not cosmetic)

To gain genuine string-synthesis capacity the learner needs, natively in
the substrate:

1. **Character-level addressing** of strings (treat a taught/uttered
   string as an indexable sequence, not an opaque span);
2. **A construction operator** that writes bytes in a computed order
   (the missing output-side primitive);
3. **A learning path** from teaching to transformation — example-driven
   program induction over a general string-program family (not six
   hardcoded rules);
4. **Case-preserving capture** for the string domain (repair of §3),
   independent of the legacy case-folded KB channel.

The repair (`srule_engine.zag`, `wb3_stringrule.zag`) implements exactly
these four, with the legacy `do_turn` left byte-for-byte untouched. The
intervention test: if string-rule probes flip from 0/8 to 8/8 while the
24/24 workbuddy battery still passes and reruns stay byte-identical, the
missing operator was the causal block.
