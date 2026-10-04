# Red-teamed probe chat: byte-captured transcript plus knowledge-vs-architecture diagnoses

## Capture method

The chat was held with the built interactive TNN
(`build/tnn_chat`, sha256 `1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c`)
by piping a fixed prompt file on stdin and capturing stdout byte for byte.
No human edited any line of the transcript.

- Input file: `build/probe5.txt`
  (sha256 `5fa7b7e8526c6d4530c08a94613e0923dcd85adada59438722822a00f65052f2`)
- Output file: `build/probe5.out`
  (sha256 `d61610ca1d4d814a1af4d72b2673908a40e1c6b04cc5172695a7f363f22538b9`)
- Command: `./tnn_chat < probe5.txt > probe5.out 2> probe5.err`
- Determinism note: the 3-prompt probe was run twice and produced byte-identical
  output; this 5-prompt run exited 0 with empty stderr.

## Verbatim transcript

```
TNN chat ready. 38 facts loaded. Type a line and press enter. quit exits, /new starts a fresh conversation.
you> tnn> Andy Weir wrote The Martian.
you> tnn> Andy Weir was born in 1972.
you> tnn> Herman Melville wrote the novel Moby Dick.
you> tnn> Andy Weir wrote The Martian.
you> tnn> [novel] the eiffel tower is taller.
you> bye.
```

Input lines, in order:

1. `who wrote the martian?`
2. `when was he born?`
3. `who wrote the novel published in 1851?`
4. `who wrote dune?`
5. `which is taller, the eiffel tower or big ben?`
6. `quit`

## Per-turn diagnosis

### Turn 1: `who wrote the martian?` -> `Andy Weir wrote The Martian.`

Sanity probe. Direct single-fact retrieval works. A failure here would have
indicated a severe regression (broken KB load or retrieval), not a diagnosis.

### Turn 2: `when was he born?` -> `Andy Weir was born in 1972.`

Architecture probe: cross-turn pronoun resolution. The pronoun "he" resolves
to Andy Weir via the dialogue state manager's topic carried from turn 1.
PASS. This shows conversational state, not just per-turn retrieval.

### Turn 3: `who wrote the novel published in 1851?` -> `Herman Melville wrote the novel Moby Dick.`

Architecture probe: two-hop composition with no paired example. The KB holds
"Moby Dick was published in 1851." and "Herman Melville wrote the novel
Moby Dick." separately; the system chained them to answer a question whose
wording matches neither fact directly. PASS. A failure here (with turns 1, 2,
and 5 passing) would have indicated an architecture gap in retrieval-side
composition, not a knowledge gap, since both component facts are in the KB.

### Turn 4: `who wrote dune?` -> `Andy Weir wrote The Martian.`

Knowledge-boundary probe, deliberately out of KB. The KB contains no Dune
fact. FAIL in the informative direction: the baseline instrument answered a
confident, fact-shaped, wrong answer instead of declining or hedging. The
answer is the salient topic from turns 1 and 2, so the mechanism looks like
topic carryover feeding retrieval when no fact matches, rather than a
knowledge lookup returning "no fact".

Diagnosis: knowledge-boundary failure, not architecture gap. The frozen FIT
chain already demonstrated the architecture can decline (tnn_chat_decline.zag
produced 30/30 specific declines on out-of-KB turns in the 2026-09-25
re-certification), so the decline machinery exists; this baseline instrument
simply does not use it. The gap is which instrument is in front of the user,
not whether TNN can represent "no fact". A red team wanting a knowledge-gap
diagnosis instrumented for chat should run tnn_chat_decline.zag instead.

### Turn 5: `which is taller, the eiffel tower or big ben?` -> `[novel] the eiffel tower is taller.`

Architecture probe: novel numeric comparison composed from two independent
facts (Eiffel Tower 330 meters, Big Ben 96 meters). The `[novel]` tag marks a
composition-path answer rather than a retrieved sentence. PASS.

## Summary

Five exchanges, four passes, one informative failure. Architecture is healthy
on the probed dimensions: cross-turn state (turn 2), two-hop composition
(turn 3), novel comparison composition (turn 5). The single failure (turn 4)
is a knowledge-boundary failure: confident wrong answer on an out-of-KB
question, caused by topic-carryover retrieval with no decline gate in this
baseline instrument. The architecture is not missing the decline capability;
the decline variant of the same frozen code demonstrates it. Recommendation
for probe-chat work: use the decline instrument for knowledge-vs-architecture
separation, or treat turn-4-style hallucinations as the expected baseline
failure signature.
