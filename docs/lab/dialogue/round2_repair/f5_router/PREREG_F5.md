# PREREG_F5 — F5-ROUTER: utterance-type dispatch (frozen 2026-09-23)

Family: F5-ROUTER. Parent: `dialogue/round2_repair/REPAIR_PREREG.md`
(kill bars 1–6 there apply; family specifics below). Written and committed
BEFORE any repair code. Held-out set frozen here; never used for tuning.

## Target failures (round-2 turns)

- Turn 14: "tell me a joke about darwin." → emitted a Darwin birth fact.
  No joke machinery and no decline machinery exist; the request was
  tokenized like a question and fell to step-5 Jaccard retrieval.
- Turn 15: "do you remember the first thing i asked you?" → emitted fact 0
  ("Herman Melville wrote the novel Moby Dick."). The hist/histb store is
  WRITE-ONLY: every user turn (kind=0) and response (kind=1) is recorded
  for novelty checks, but nothing ever reads it for recall.
- Turn 18: "forget everything i just told you." → emitted fact 0.
  No instruction/command recognition; `extract_assert`'s 7 declarative
  templates don't match, so it fell through to retrieval.

Shared root: a single retrieve-and-emit pipeline with no input-type dispatch.

## Repair design (general machinery, not three hacks)

Insert an **utterance-type dispatcher** as step 0 of `do_turn`, BEFORE
correction handling and BEFORE any retrieval. It classifies the input into
one of four types and handles the first three with dedicated response
strategies; type 0 falls through to the existing pipeline unchanged.

```
utter_type(input) -> 1 joke | 2 memory/history | 3 forget-instruction | 0 other
```

Detection (all on the lowercased input buffer; token-level, not substring,
so "joker"/"forgetful" can't false-fire):

- **JOKE (1):** input contains the token `joke` or `jokes`.
  Response: `I don't know any jokes.` — honest decline. The system has no
  joke machinery; it must SAY SO, never emit a fact.
- **MEMORY (2):** input contains token `remember` or `recall`, OR matches
  "what did I ask/say/tell" shape (tokens `did` + `i` + one of
  `ask asked say said tell told`).
  Response: READ the hist store — collect kind=0 rows excluding the current
  turn (always the last row, recorded by main before do_turn), select by
  ordinal (`first`->oldest, `last`/`previous`/`latest`->most recent,
  `second`..`thirtieth` via the number-word table, default->most recent),
  and quote it: `You asked: <turn text>`.
  If no prior user turn exists: `You haven't asked anything before this.`
- **FORGET (3):** input contains token `forget`, `forgot`, or `forgotten`.
  Response: `I can't forget.` — the true one, stated plainly: the system
  records user turns/assertions and has no erase mechanism, so the honest
  answer is that it cannot forget. NEVER a KB fact.
- **OTHER (0):** unchanged pipeline (correction/resume/compose/assert/retrieve).

Dispatch precedence: forget > joke > memory (nearly disjoint in practice;
documented for determinism).

Salience/state hygiene: the branch pushes gazetteer entities found in the
input (so "he" still binds after "tell me a joke about darwin."), sets
pv to a non-retrieval turn (no answer fid), and returns -1 like compose.
No probe-specific branches, no per-case constants, no tuning against probes.

## Exact frozen response strings

- `I don't know any jokes.`
- `You asked: ` + quoted prior user turn (lowercased, as stored)
- `You haven't asked anything before this.`
- `I can't forget.`

## Scaffold (GUIDE phase) — probes/scaffold_battery.txt

- F5S-R2: full R2-01 replay, real E-lines on 14/15/18, sentinels elsewhere.
- F5S-J: joke paraphrases ("tell me a joke about melville.",
  "can you tell me a joke?", "say a joke about the eiffel tower.").
- F5S-M: memory paraphrases ("what was the first thing i asked?",
  "do you remember what i just asked you?", "what was the second thing
  i asked?", "do you remember my last question?").
- F5S-F: forget paraphrases ("forget what i told you.",
  "please forget everything.", "i want you to forget all of this.").

## Held-out set (RELEASE phase) — FROZEN, probes/heldout_battery.txt

Never opened or tuned against during development. 7 probes:

| id | input (fresh context each block) | expected |
|----|----------------------------------|----------|
| H1 | tell me a joke about the eiffel tower. | `I don't know any jokes.` |
| H2 | tell me another joke. | `I don't know any jokes.` |
| H3 | do you remember the first thing i asked you? | `You asked: who wrote the martian?` |
| H4 | what did i just ask? | `You asked: do you remember the first thing i asked you?` |
| H5 | can you recall my second question? | `You asked: when was he born?` |
| H6 | please forget what i told you. | `I can't forget.` |
| H7 | forget it all. | `I can't forget.` |

Contexts: H1/H2 after "who wrote the martian?"; H3–H5 after
"who wrote the martian?"/"when was he born?"/"was he born before the
eiffel tower was built?"; H6/H7 after "who wrote the martian?".
(Context turns carry sentinel E-lines; their outputs are not scored.)

## Kill bars (family-specific)

1. **Acquisition:** turns 14/15/18 produce exactly the frozen strings above.
2. **Release:** held-out 7/7 PASS on the released build. Any per-case branch
   or constant that only fits scaffold phrasings = FAIL.
3. **No gaming:** the 5 good round-2 turns (1, 2, 5, 10, 12) keep their
   canonical outputs; router fires ONLY on joke/memory/forget inputs.
   Normal factual questions must still retrieve (guarded by the full
   round-1 battery and by context turns in the probe batteries).
4. **No regressions:** full round-1 battery (`dialogue/battery.txt`):
   every SECTION score identical to the canonical run
   (FOLLOWUP 45/45, CORRECTION 45/45, REFERENT 60/60, WEIRD 30/30,
   WEIRD_CLEAN 30/30, TOPIC 60/60, CONTRADICT 72/72, COMPOSE 28/28)
   and identical DIGEST
   (`35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`).
5. **Determinism:** two consecutive runs of every battery byte-identical
   (cmp clean); zero RNG (no random source exists in the code path).
6. **Cleanroom:** only `dialogue/round2_repair/f5_router/` touched;
   canonical `dialogue/` tree unmodified (verified by re-running the
   canonical binary — its outputs are unchanged).

## Non-goals / boundaries

- Turn 16 (provenance, "how do you know") belongs to F4-DEFEND; the router
  must NOT swallow it (it contains no joke/memory/forget token — verified
  by the F5S-R2 replay keeping its sentinel).
- Content-addressed recall ("my question about the martian") is out of
  scope; ordinal + recency recall is the built capability. Documented, not
  hidden.
- No new KB facts, no gazetteer changes, no retrieval-path changes.

## Deliverables

PREREG_F5.md (this file, frozen), repaired `dialogue.zag` fork + BUILD.md,
HELDOUT.md + run logs (scaffold vs released), VERDICT.md (plain language),
all committed under `dialogue/round2_repair/f5_router/`.
