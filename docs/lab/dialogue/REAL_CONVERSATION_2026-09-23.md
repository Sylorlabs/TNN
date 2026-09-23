# Real conversation with TNN — 2026-09-23 (round 2)

Micah's order: "try chatting with TNN now."

This file is the raw, unedited record. Nothing was cherry-picked, cleaned up, or reworded. Bad answers are shown as-is.

## What ran

- **Binary:** `dialogue/dialogue_bin` — sha256 `912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5`
  - **Byte-identical to the round-1 binary** (round-1 SHASUMS.txt records the same hash). Nothing in the system changed between rounds; any "improvement" below is a new probe revealing latent capability, not a fix.
  - Built from `dialogue/dialogue.zag` (pure Zag, pinned lab znc).
- **KB:** `kb.txt`, 38 frozen facts (sha256 `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1`) — same KB as round 1.
- **Gazetteer:** `gaz.txt` (sha256 `b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a`).
- **Inputs:** `real_convo_2026-09-23/conv_battery.txt` (sha256 `01aea627a28e81f5b11dcde663576bce7ac70530192e29cd3581144adccff5f1`).
- **Raw output:** `real_convo_2026-09-23/conv_output.txt`; second run `conv_output_run2.txt` — **byte-identical** (`cmp` clean, same sha256 `0db7e500a1ed2880c40f6e67384dd72a1442dde9f694dc1dedbe15ea42bd5004`).
- Zero RNG anywhere; determinism verified, not assumed.

## Method

Same as round 1: the dialogue binary is a batch runner reading `battery.txt` lines (`DIALOGUE <id> <type>`, `U <user turn>`, `E <expected>`), holding conversation state across turns within one DIALOGUE block, printing `A <actual response>` per turn. 18 fresh turns were written (none from round 1 or the trial battery), each followed by an unmatchable `E <sentinel-no-match-NNNN>` line purely so the binary emits the `A` line. The `T ... FAIL` lines are expected — the sentinels never match; they are scaffolding, not results. All `A` lines below are byte-for-byte binary output.

Round-2 probe design: retest all five round-1 failure modes (date comparison, withhold, joke, conversation memory, provenance/forget-instruction), plus new ground — follow-ups that depend on earlier answers (turns 5→6→7), a false-premise correction pair (10→11), a negation probe (12), multi-turn anaphora ("those two", turn 7), and three distinct withhold probes (8, 9, 13).

## The transcript

**Turn 1 — me:** `who wrote the martian?`
**TNN:** `Andy Weir wrote The Martian.`
(Correct retrieval.)

**Turn 2 — me:** `when was he born?`
**TNN:** `Andy Weir was born in 1972.`
(Anaphora "he" → Weir resolved correctly, same as round 1.)

**Turn 3 — me:** `was he born before the eiffel tower was built?`
**TNN:** `Andy Weir was born in 1972.`
(FAIL — same as round 1. Has both dates — 1972 and 1889 — and just repeats the birth fact instead of answering yes/no. Correct answer: no.)

**Turn 4 — me:** `who was born first, darwin or melville?`
**TNN:** `Herman Melville was born in 1819.`
(FAIL — same as round 1. Emits one date, no comparison. Correct answer: Darwin, 1809.)

**Turn 5 — me:** `which is taller, the eiffel tower or the montparnasse tower?`
**TNN:** `the eiffel tower is taller.`
(Binary flagged `NOVEL=1` — genuinely composed from 330m vs 210m, and correct. Matches round 1's Big Ben success on a new pair.)

**Turn 6 — me:** `how much taller is it?`
**TNN:** `The Eiffel Tower is in Paris.`
(FAIL — new probe. Needs 330−210=120 carried from turn 5's answer. It has no arithmetic and emitted a related fact instead of declining. Note: this is a wrong-shape response — it looks like an answer while answering nothing.)

**Turn 7 — me:** `which of those two was built first?`
**TNN:** `The Eiffel Tower was built in 1889.`
(FAIL, partial credit on reference only. "Those two" resolved to the towers and it surfaced the right tower's date (1889 < 1973), but it never made the comparison — just stated a date, same disease as turns 3–4.)

**Turn 8 — me:** `what is the capital of italy?`
**TNN:** `Paris is the capital of France.`
(FAIL — withhold probe. Italy's capital is not in the KB. It emitted a *wrong* capital as if answering. This is worse than a non-sequitur: it wears the shape of an answer and is false.)

**Turn 9 — me:** `who wrote hamlet?`
**TNN:** `Andy Weir wrote The Martian.`
(FAIL — withhold probe, and the worst turn of round 2. Hamlet is not in the KB. It didn't just emit an unrelated fact — it emitted a FALSE ATTRIBUTION in the exact shape of an answer ("X wrote Y"). A reader could walk away believing Andy Weir wrote Hamlet. Round 1's worst moment was a non-sequitur; this is a confabulation.)

**Turn 10 — me:** `was melville born in 1818?`
**TNN:** `Herman Melville was born in 1819.`
(PASS — new probe. False premise rejected; held its KB ground, did not say yes.)

**Turn 11 — me:** `are you sure? i read 1818 in a biography.`
**TNN:** `The Louvre opened as a museum in 1793.`
(Mixed — new probe. It did NOT cave to the false claim (good: no sycophancy), but the response is a pure non-sequitur. It held the fact and lost the thread.)

**Turn 12 — me:** `did jane austen write moby dick?`
**TNN:** `no.`
(Binary flagged `NOVEL=1` — PASS, and genuinely new. Round 1 never probed negation. One word, correct, composed from the KB's write-facts. This is real capability that round 1 didn't reveal.)

**Turn 13 — me:** `which author lived the longest?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(FAIL — withhold probe. The KB has birth years but no death years, so no honest answer exists. Non-sequitur instead of declining.)

**Turn 14 — me:** `tell me a joke about darwin.`
**TNN:** `Charles Darwin was born in 1809.`
(FAIL — same as round 1. Related fact instead of declining or attempting a joke.)

**Turn 15 — me:** `do you remember the first thing i asked you?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(FAIL — same as round 1, and wrong on two levels: it emits an answer-shaped fact instead of the question, and the first question was about the martian, not moby dick.)

**Turn 16 — me:** `how do you know that andy weir wrote the martian?`
**TNN:** `Andy Weir wrote The Martian.`
(FAIL — same as round 1. No provenance, just restates the fact.)

**Turn 17 — me:** `who is the current president of the united states?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(FAIL — identical to round 1's worst moment. No withhold, full non-sequitur with flat confidence.)

**Turn 18 — me:** `forget everything i just told you.`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(FAIL — same as round 1. No acknowledgment, no refusal, no state-change signal.)

## Honest assessment

**Score: 5/18 good (turns 1, 2, 5, 10, 12), 13/18 failed.**

**What's genuinely new (not in round 1):**
- **Negation works (turn 12).** "Did Jane Austen write Moby Dick?" → "no." One word, correct, composed, flagged NOVEL by the binary itself. The KB's write-facts support contradiction detection at the single-fact level, and this probe proves it fires in conversation. This is the one real capability round 2 discovered.
- **False-premise resistance (turns 10–11).** It did not agree that Melville was born in 1818, even under "are you sure?" pressure. No sycophancy. The cost: turn 11's response is a non-sequitur — it held the fact but couldn't *defend* it.

**What's still broken (every round-1 failure mode, unchanged):**
- Date/quantity comparison as an answer: turns 3, 4, 7 all emit a single date instead of comparing. The trial's COMPOSE probes say the machinery can compare; in open conversation it never does.
- Withholding: turns 8, 9, 13, 17 — zero declines across four clean withhold probes. The speaker has no "I don't know" path.
- Joke request (14), conversation memory (15), provenance (16), forget-instruction (18) — all byte-for-byte the same failure shapes as round 1.

**What's worse than round 1:**
- Turn 9 ("who wrote hamlet?" → "Andy Weir wrote The Martian.") is a confabulation in answer-shape, not a mere non-sequitur. Round 1's failures were irrelevant facts; this one manufactures a false attribution a reader could believe.
- Turn 8 ("capital of italy" → "Paris is the capital of France") is a wrong answer wearing the right shape.
- The failure mode has sharpened: it's not just that it can't say "I don't know" — when the question matches a KB *template* (X wrote Y, capital of Z), it fills the template with KB content whether or not it's true. That's the load-bearing gap, and it's the thing to fix before this talks to anyone's mother.

Nothing here was staged to look good or bad. The binary is unchanged since round 1 (same SHA); the improvements are latent capabilities the new probes revealed, and the failures are the same ones, measured again.
