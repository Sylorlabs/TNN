# Round-3 TNN chat — verdict (2026-09-26)

Micah's order: "do another tnn chat round, see how it goes and show reasoning
traces of it too as you chat to it."

## What ran

- **Binary:** `dialogue_bin_trace` — the round-2 repaired dialogue system
  (f1 compare, f2 withhold, f3 arithmetic, f4 defend, f5 router) plus stderr
  reasoning-trace hooks (`dialogue_trace.zag`, generated from the integrated
  repair source by `add_hooks.py`, 13 anchored insertions). Traces go to fd 2
  via raw syscall; stdout answers are byte-identical to the no-trace control
  build (`cmp` clean). Pure Zag, zero RNG.
- **KB:** 43 facts (sha256
  `8ed85c236504cf65bd8ff4d08ec9972c81b6c6200524411b9176299f92da2986`)
  — the frozen 38 plus 5 newly taught facts from recent work: TNN upscaled
  the test image; TNN reproduced 359 audio clips; TNN learned the pig snout;
  TNN detected the sticker; the test image is 640 pixels wide.
- **Gazetteer:** 32 entities (sha256
  `8cd8f527ab3aeb9c52046ef6ac5dd6d4d624b89cbde34d3e49b2fd9493846379`).
- **Battery:** 23 fresh turns (sha256
  `8638ecc8b9537838b5e8f7ec809ab39d30a282b96557acace36b3fa16674b1c1`),
  none from round 2, each followed by an unmatchable `E sentinel` line.
- **Determinism:** two full runs byte-identical on stdout AND stderr.

## Scorecard: 20 good / 1 partial / 2 fail (23 turns)

Full per-turn record with traces: `~/workspace/your_files/tnn-round-3-chat/Round 3 TNN Chat.html`.

| # | Probe | Result |
|---|---|---|
| 1–2 | retrieval + anaphora (moby dick) | GOOD |
| 3 | who wrote hamlet? (template-filling retest) | GOOD — retrieved fid 15 ("Andy Weir wrote The Martian"), gate fired `withhold=1` |
| 4–5 | penicillin / capital of italy | GOOD — gate fired on fids 12, 33 (round 2's literal wrong answers) |
| 6–7 | big ben vs statue of liberty; how much taller | GOOD — compare 96 vs 93; f3 diff=3 |
| 8–10 | curie/austen; eiffel built before montparnasse; those two | GOOD — 1775<1867; yes; anaphora→330 vs 210 |
| 11 | what did TNN upscale? | **FAIL** — "TNN detected the sticker." (fid 41, withhold=0) |
| 12–13 | audio clips; pig snout | GOOD — new-domain retrieval |
| 14 | what did TNN paint? | **FAIL** — "TNN detected the sticker." (should withhold) |
| 15 | pride and prejudice | GOOD |
| 16 | no, i meant moby dick. | PARTIAL — correction fired, right entity, wrong fact ("published in 1851") |
| 17–18 | louvre paris/rome assertion pair | GOOD — NOTED then CONTRADICTION: turn 17 said paris |
| 19 | provenance | GOOD — "I was taught that…" |
| 20–22 | joke / first question / forget | GOOD — ut=1/2/3 routed |
| 23 | did TNN detect the sticker? | GOOD |

## The finding

The two fails are the same disease in the new TNN domain. The withhold gate
checks that the question's **entities** appear in the retrieved fact, but
never checks the **predicate**. Entity-known + predicate-unknown →
confabulation: "what did TNN upscale?" and "what did TNN paint?" both emitted
"TNN detected the sticker." (fid 41, withhold=0). Round 2's Hamlet fix holds
for entity-unknown questions, but the gate has a predicate-shaped hole.

Second, smaller gap (turn 16): the correction branch resolves the right
entity but does not carry the question shape ("who wrote") through the
correction, so it answered "published in 1851" to a "who wrote" intent.

## Recommended next repair

F2 gate, second half: after the entity-overlap check passes, require the
fact's predicate (wrote/born/published/in/built/tall/detected/upscaled/…)
to match the question's predicate; else withhold. Correction path: carry the
previous turn's question shape (or its resolved query) instead of the bare
entity.

## Files

- `dialogue_trace.zag` — traced source (diff vs integrated repair: 13 hook insertions only)
- `add_hooks.py` — hook insertion script
- `build_html.py` — artifact generator
- `kb_round3.txt`, `gaz_round3.txt`, `battery_round3.txt`
- `conv_output.txt` — stdout run 1 (answers + harness lines)
- `conv_trace.txt` — stderr run 1 (the reasoning traces)
- `SHASUMS.txt`
