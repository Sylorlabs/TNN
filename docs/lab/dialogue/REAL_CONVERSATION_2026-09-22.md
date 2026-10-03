# Real conversation with TNN — 2026-09-22

Micah's order: "have a back and forth conversation with TNN and show me real results nothing faked to make it look good."

This file is the raw, unedited record. Nothing was cherry-picked, cleaned up, or reworded. Bad answers are shown as-is.

## What ran

- **Binary:** `dialogue/real_convo_2026-09-22/dialogue_bin` (copied byte-identical from `dialogue/dialogue_bin`)
  - sha256: `912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5`
  - Built from `dialogue/dialogue.zag` (pure Zag, pinned lab znc); the dialogue trial's VERDICT.md (2026-09-22) records its trial digest `bc7e19f1c1368e47e04719b84dd89799b5874f691d85580b53e97fb1a1731439` and prereg commit `5d120faf`.
- **KB:** `kb.txt`, 38 frozen facts (sha256 `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1`)
- **Gazetteer:** `gaz.txt` (sha256 `b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a`)
- **Inputs:** `real_convo_2026-09-22/conv_battery.txt` (sha256 `1113170eaab1915b29440322d82a34d4b52351406b9363c61d32eac60f074a02`)
- **Raw output:** `real_convo_2026-09-22/conv_output.txt`; second run `conv_output_run2.txt` — **byte-identical** (`cmp` clean).
- Zero RNG anywhere; determinism verified, not assumed.

## Method

The dialogue binary is a batch runner: it reads `battery.txt` lines (`DIALOGUE <id> <type>`, `U <user turn>`, `E <expected>`), holds conversation state across turns within one DIALOGUE block, and prints `A <actual response>` per turn. To hold a genuine conversation, 14 fresh turns were written (none from the trial battery), each followed by an unmatchable `E <sentinel-no-match-NNNN>` line purely so the binary emits the `A` line. The `T ... FAIL` lines are expected — the sentinels never match; they are scaffolding, not results. All `A` lines below are byte-for-byte binary output.

## The transcript

**Turn 1 — me:** `who wrote moby dick?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`

**Turn 2 — me:** `when was he born?`
**TNN:** `Herman Melville was born in 1819.`
(Anaphora "he" → Melville resolved correctly.)

**Turn 3 — me:** `was he born before the eiffel tower was built?`
**TNN:** `Herman Melville was born in 1819.`
(It had both dates in the KB — 1819 and 1889 — and the trial's COMPOSE probes showed it *can* do this comparison. Here, phrased as a fresh yes/no question, it just repeated the birth fact instead of answering yes/no.)

**Turn 4 — me:** `how do you know that?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(No provenance, no "from my knowledge base" — just restated a fact.)

**Turn 5 — me:** `what is the capital of france?`
**TNN:** `Paris is the capital of France.`

**Turn 6 — me:** `do you remember the first thing i asked you?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(Emitted the *answer* to the first question rather than the question itself. It retrieved the right neighborhood but answered the wrong thing.)

**Turn 7 — me:** `tell me a joke about the eiffel tower.`
**TNN:** `The Eiffel Tower is in Paris.`
(No joke in the KB, so no joke — but also no honest "I don't know any jokes." It just emitted a related fact.)

**Turn 8 — me:** `who is the current president of the united states?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(Not in the KB. An honest gap would be a withhold. Instead: an unrelated fact. This is the no-withhold failure in its purest form.)

**Turn 9 — me:** `oh great another meeting that could have been an email. is the speaker happy about the meeting?`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(Sarcasm probe. Same fallback. No recognition of the utterance type at all.)

**Turn 10 — me:** `pin the fact that herman melville wrote moby dick.`
**TNN:** `NOTED.`
(It treated this as a memory operation and acknowledged it, rather than answering it as a question. Notably the only turn with this response shape.)

**Turn 11 — me:** `which is taller the eiffel tower or big ben?`
**TNN:** `the eiffel tower is taller.`
(Binary flagged `NOVEL=1` — this sentence appears nowhere in the KB or prior turns. Genuinely composed from 330m vs 96m, and correct.)

**Turn 12 — me:** `was darwin born before or after melville?`
**TNN:** `Herman Melville was born in 1819.`
(Darwin's 1809 was in the KB. It emitted Melville's date and stopped — no comparison, no answer to before/after.)

**Turn 13 — me:** `forget everything i just told you.`
**TNN:** `Herman Melville wrote the novel Moby Dick.`
(No refusal, no acknowledgment, no state change signal — just another fact. Whatever it does with instructions like this, it isn't deliberation.)

**Turn 14 — me:** `what did i ask you about paris?`
**TNN:** `The Louvre is in Paris.`
(On-topic retrieval — I had asked about the capital of France and the Eiffel Tower — but it answered with a Paris fact rather than describing what I asked.)

## Honest assessment

Talking to it feels like talking to a very fast, very confident librarian who only owns 38 index cards and has no way to say "I don't know." When the question lands on a card — turns 1, 2, 5 — it's crisp. When the question needs two cards combined — turns 11 — it can genuinely compose a novel correct sentence, and that is real. The anaphora in turn 2 is real too.

The failure mode is single and total: **it never withholds.** Every out-of-KB question — the presidency, the joke, the sarcasm, the yes/no comparison it fumbled, the "forget everything" instruction — gets answered with a nearest-ish fact or a full non sequitur, delivered with the same flat confidence as a true answer. There is no visible difference in the output between "I know this" and "I have no idea." For a system whose program is built on honest gaps and deliberate memory agency, that is the load-bearing gap: the judge exists in the trial harness (the E-line scoring), but the speaker has no "decline to answer" path.

The worst moment is turn 8. "Who is the current president of the United States?" → "Herman Melville wrote the novel Moby Dick." Not a hedge, not a guess, not a refusal — a confident, grammatical, entirely unrelated fact. If Micah's mother asked it that question, she would walk away believing the machine is broken. That is the turn to fix first: an honest gap must be speakable.
