# Round-2 Dialogue Repair Program — Plain-Language Synthesis

2026-09-23. Branch `tnn-native-lab`. This document summarizes the whole
program: what was broken, what we did, what worked, and what the system
still cannot do.

## What was wrong

In the round-2 chat the system got 5 of 18 turns right. The 13 failures
looked different on the surface — wrong comparisons, confabulated facts,
no arithmetic, jokes answered with birth dates, "forget everything" answered
with a random fact — but the investigation found ONE underlying cause.

The program had exactly one way of answering: find the best-matching fact
in its knowledge base and print it word for word. Every input that needed
anything else — comparing two things, doing subtraction, saying "I don't
know", telling a joke request apart from a question, remembering what you
asked, following an instruction — got forced through that one path, and it
produced confident nonsense. The most dangerous version: "who wrote
hamlet?" was answered with "Andy Weir wrote The Martian." The system
matched the word "wrote", picked the shortest matching fact, and never
checked whether Hamlet had anything to do with it. There was no code
anywhere that could say "I don't know."

Full root-cause analysis: `dialogue/round2_repair/ROOT_CAUSES.md`
(commit `40f5ace1`).

## What we did

We ran a repair method we're calling **guided release** (Micah asked for a
better name than "scaffold-release"; this is the working term). The shape:

1. Write a frozen plan (prereg) BEFORE touching code — what will change,
   what must not change, and the kill bars that decide pass/fail.
2. Build the repair using temporary scaffold probes and hints.
3. Remove all scaffolding.
4. Prove the repair still works on frozen held-out test questions the
   repair never saw during development — this is what separates a real
   fix from memorizing the test.

Five independent crews each repaired one failure family in its own
cleanroom copy. The original program was never modified.

## What got fixed

| Family | Failures | Fix, in plain terms | Result |
|---|---|---|---|
| Comparison | turns 3, 4, 7 | A general comparison engine: finds the comparison word anywhere in the sentence, figures out the two things being compared (including "those two"), looks up their values, answers yes/no or names the winner | PASS |
| Withholding | turns 8, 9, 13, 17 | An "aboutness" gate before answering: if the question is about something the system doesn't know, or the matched fact doesn't actually concern the question, it says "I don't know." instead of inventing an answer | PASS |
| Arithmetic | turn 6 | A real subtraction engine ("how much taller is…" now computes the difference), plus teaching it that "taller" is the comparative of "tall" | PASS |
| Defense & honesty | turns 11, 16 | Fixed the word-filter (the word "a" was matching noise and derailing answers), taught it to hold its ground when challenged, and to answer provenance questions honestly ("I was taught that") instead of restating the fact | PASS |
| Input types | turns 14, 15, 18 | A dispatcher that runs before anything else: joke requests get an honest "I don't know any jokes", history questions actually read the conversation history, "forget…" gets "I can't forget" (true — it has no erase mechanism) | PASS |

Each family passed every kill bar: its assigned failures fixed, frozen
held-out questions passed (never seen during development), no regressions
on the 5 turns that were already good, no regressions on the full original
test battery, byte-identical reruns, zero randomness, no hard-coded
test answers.

## The integration story (told honestly)

Merging the five repairs into one program passed 18/18 round-2 turns and
36/36 held-out questions — but FAILED the strictest bar: 7 answers in the
original test battery changed. Two real interactions between the repairs:

- The "I don't know" gate was judging follow-up questions ("What about
  the Louvre?") against the wrong turn's words and declining questions it
  should have answered.
- A merge mistake dropped a guard condition on the follow-up handler, so
  it fired where it shouldn't.

A sixth crew fixed all 7 with three small, general edits (one was a merge
bug, not a design flaw) and re-verified everything. Final state:

| Check | Result |
|---|---|
| Round-2 conversation | **18/18 correct** |
| Held-out questions (all families + new interaction probes) | **44/44 pass** |
| Original full test battery | **370/370, byte-identical to before** |
| Determinism | every battery run twice, byte-identical, zero randomness |
| Original program | untouched (checksums verified) |

Commits: `40f5ace1` (root causes + program prereg), `1d826c7`/`390d17c`
(compare), `b1b6092`/`5e6a3db` (withhold), `7a028053`/`9659dcee`
(arithmetic), `b936d0f4`/`a13f6405` (defend), `269d209c`/`f529d8c6`
(router), `1cc0913c` (integration), `5dd76fd`/`cd4c3bf`/`843023f`
(interaction repair).

## What it still cannot do (honest limits)

- It can recall conversation history by position ("the first thing I
  asked") but not by content ("my question about the Martian").
- Arithmetic only covers height and years — the only paired numbers in
  its knowledge base. Answers come back as bare numbers ("120", not
  "120 meters").
- It still can't answer a genuinely new kind of question about something
  it knows ("population of Paris?") — that's outside this repair's scope.
- Mixed questions ("did X write Y before 1900?") get handled as one
  question type, not both.
- One piece of internal state goes stale after an "I don't know" — known,
  currently harmless, flagged for future work.

## Bottom line

The system went from 5/18 to 18/18 on the round-2 conversation, can now
say "I don't know" instead of confabulating (without becoming a machine
that declines everything — 25/25 answerable questions still answered), does
real subtraction, handles comparisons phrased any way, routes jokes /
history / instructions to honest responses, and defends true facts under
challenge. Every claim above is backed by frozen plans, held-out tests the
repairs never saw, and byte-identical reruns — all committed in
`dialogue/round2_repair/`.
