# VERDICT.md — F5-ROUTER (plain language)

Date: 2026-09-23. The problem: the dialogue system had one response
strategy — find the best-matching fact and say it. So a joke request got
a birth fact, "do you remember what I asked?" got an unrelated fact, and
"forget everything" got an unrelated fact. The fix: sort the input by
type FIRST, then decide how to respond.

## What was built

A dispatcher that runs before anything else and asks: is this a joke
request, a question about our conversation history, or a "forget"
instruction? Each type gets its own honest response:

- Joke request → "I don't know any jokes." (It has no joke machinery,
  so it says so instead of reciting a fact.)
- History question → it actually reads its conversation log (which was
  being recorded but never read) and quotes your earlier question back.
- "Forget…" → "I can't forget." (It records what you say and has no way
  to erase, so the honest answer is that it can't — stated plainly.)
- Anything else → the old pipeline, untouched.

## Verdict per kill bar

1. **Acquisition — PASS.** Round-2 turns 14, 15, 18 now produce exactly:
   `I don't know any jokes.` / `You asked: who wrote the martian?` /
   `I can't forget.`
2. **Release (anti-hardcode) — PASS.** 7/7 frozen held-out probes pass —
   new joke requests, new history phrasings ("what did i just ask?",
   "can you recall my second question?"), new instruction phrasings.
   The held-out set was never seen during development.
3. **No gaming — PASS.** The dispatcher only fires on joke/history/forget
   inputs. The 5 good round-2 turns (1, 2, 5, 10, 12) produce byte-identical
   output to before. Edge probes confirm no over-firing: "the joker
   smiled", "forgetful people lose keys", "what did darwin write?",
   "tell me about the eiffel tower" all take the normal path.
4. **No regressions — PASS.** Full round-1 battery: all 8 section scores
   identical (45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72, 28/28)
   and the output digest identical
   (`35aaae8a…34474b`) — the repaired binary's full output is
   byte-identical to the canonical binary's.
5. **Determinism — PASS.** Every battery run twice, `cmp` clean every
   time. No randomness exists anywhere in the code.
6. **Cleanroom — PASS.** Only `dialogue/round2_repair/f5_router/` was
   touched; the canonical `dialogue/` tree is unmodified.

## What worked

Token-level type detection turned out to be enough — no substring
false-fires ("joker" and "forgetful" don't trigger). Reading the
history store was straightforward once the read path was built; the
data was always there. Ordinal selection (first/second/last) fell out
of the existing number-word table.

## What didn't / limits

- The first memory-detector draft only recognized "did I ask…" phrasing
  and missed "what was the first thing i asked?" (no "did"). The scaffold
  caught it; the rule was generalized to self-referential past speech.
- Content-addressed recall ("my question about the martian") is NOT
  built — recall is by ordinal/recency only. Documented boundary, not a
  hidden gap.
- Turn 16 ("how do you know…?", provenance) is F4's territory; the
  dispatcher deliberately leaves it alone.

## Overall: PASS (6/6 bars)

Commits: prereg freeze `269d209c49dc99bb23e2fb97cc008586b728441d`;
implementation + results (this commit) — see final report.
