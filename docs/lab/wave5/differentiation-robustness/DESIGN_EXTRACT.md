# Raw-conversation evidence extractor — design

Investigator: Wave-5, slug `differentiation-robustness`, part (b).
Date: 2026-09-19. Status: PROPOSED (preregistered in PREREG.md, untested
at time of writing).

This design attacks wave-4 differentiation boundary #1/#4: evidence
events were harness-supplied `(bit, value)` pairs, and the
evidence-extraction path was "unbuilt, large". This trial builds the
**smallest native extractor that can genuinely fail**: deterministic
dialogue-turn → evidence-event extraction with per-event reliability
tags, wired into the graded judgment from part (a), trialed end-to-end
on designed adversarial dialogues.

## 1. What the extractor is (and is not)

It is a fixed pattern table over dialogue turns, evaluated with
case-insensitive substring matching, zero RNG, zero learning. It is
honestly a **perception stub with stated failure modes** — the point of
the trial is not to solve extraction but to (a) prove the pipeline
dialogue → extraction → graded judgment → partition formation runs
natively end-to-end, and (b) show that extraction *errors* (hedged
claims, poisoned turns) degrade into abstention rather than
misattribution, because the graded layer absorbs them.

## 2. Pattern table (preregistered, fixed)

Checked per turn, in this order (denials before affirmations so a denial
suppresses its positive):

| # | needle (case-insensitive) | event (bit, value, kind) | bit meaning |
|---|---------------------------|--------------------------|-------------|
| 1 | "not alice"               | (0,0,k0)                 | name ALICE denied |
|   | "i am alice"              | (0,1,k0)                 | name ALICE claimed |
| 2 | "not bob"                 | (1,0,k0)                 | name BOB denied |
|   | "i am bob"                | (1,1,k0)                 | name BOB claimed |
| 3 | "not carol"               | (2,0,k0)                 | name CAROL denied |
|   | "i am carol"              | (2,1,k0)                 | name CAROL claimed |
| 4 | "secret is ember"         | (3,1,k1)                 | demonstrates secret S_A |
| 5 | "secret is quartz"        | (4,1,k1)                 | demonstrates secret S_B |
| 6 | "secret is harbor"        | (7,1,k1)                 | demonstrates secret S_C |
| 7 | "blue door"               | (6,1,k2)                 | recalls episode E1 |
| 8 | "kestrel is not"          | (5,0,k3)                 | fact K denied |
|   | "kestrel"                 | (5,1,k3)                 | fact K asserted |
| 9 | "--a"                     | (8,1,k2)                 | Alice's sign-off mark |
| 10| "look here"               | (9,1,k2)                 | Bob's catchphrase |
| 11| "hmm."                    | (10,1,k2)                | Carol's discourse mark |

Code words: S_A="ember", S_B="quartz", S_C="harbor". Fact K="kestrel".
Episode E1="blue door". Behavioral marks: "--a", "look here", "hmm.".

## 3. Reliability tagging (per-event)

Base reliability from kind (DESIGN_GRADED.md §3): k0→2, k1→3, k2→2, k3→1.
**Hedge downgrade**: if the turn contains any of "maybe", "i think",
"might", "probably", "not sure" (case-insensitive), reliability −1 to a
floor of 1. Rationale: hedged utterances are weaker evidence; the
downgrade is preregistered and mechanical, not interpretive. Reliability
is never upgraded.

Each emitted event is `(bit, value, kind, rel)` and is written to the
audit as an EXTRACT entry `(turn_idx, bit, OK, value, kind, rel)` before
the corresponding OBSERVE entry — extraction is white-box visible.

## 4. Pipeline

```
dialogue turns (string literals, designed)
  -> extract_turn per turn -> events (bit,val,kind,rel) + EXTRACT audit
  -> gdiff_observe per event (graded judgment, DOUBT/REFUTE audit)
  -> gdiff_commit (commit or HOLD->UNKNOWN)
  -> mem_add/mem_knows gated on committed != UNKNOWN (partition formation)
```

Replay: the pipeline driver re-runs extraction + judgment into a fresh
state and compares committed speaker, clock, all person fields
(incl. doubt/kmask/refuted), all slot fields, and entry count — a full
dialogue→state replay, since extraction is deterministic.

## 5. Adversarial dialogues (designed; predicted outcomes in PREREG.md)

- **D1 impostor**: "hello, i am alice" / "the secret is quartz" →
  ALICE doubt 3, BOB doubt 2, CAROL refuted → UNKNOWN, zero slots.
  (The hard-constraint trap, end-to-end from raw text.)
- **D2 confused speaker**: "i think i am alice" / "maybe the secret is
  ember" → hedged events (rel 1, rel 2): BOB/CAROL doubt 3 each, nobody
  refuted → UNKNOWN. Confusion abstains.
- **D3 evolving claims**: "i am bob" / "wait, no, i am alice" /
  "the secret is ember" → self-contradiction leaves ALICE doubt 2 →
  sticky doubt → UNKNOWN. (The extractor cannot represent the
  retraction; the doubt stands — honest limitation §6.)
- **D4 clean Alice**: "i am alice" / "the secret is ember" /
  "good to see the blue door again --a" → ALICE doubt 0, rivals refuted
  → COMMIT ALICE → slot owner=ALICE, partition reads correct.
- **D5 poisoned clean session**: D4's first two turns + injected
  "kestrel is not true" → ALICE doubt 1 → UNKNOWN (downgraded commit,
  never misattribution).
- **D6 denial-poison**: "i am not bob" / "kestrel is not true" → ALICE
  doubt 1, BOB doubt 3, nobody refuted → UNKNOWN. Under wave-4's
  mechanism the same extracted bit sequence commits CAROL — run as the
  comparative baseline.

## 6. Honest limitations (what the extractor does NOT do)

- **No retraction modeling.** "wait, no, i am alice" emits (0,1) but
  nothing cancels the earlier (1,1); D3's doubt is the price. A
  retraction operator is unbuilt.
- **No anaphora, coreference, or multi-turn state.** Each turn is
  extracted independently; "my secret" without the code word emits
  nothing; speaker-turn attribution within a turn is not modeled
  (single-speaker sessions only, as wave-4).
- **Fixed pattern table.** Paraphrases outside the table are invisible
  (audited as no-event turns). This is the stub's boundary, stated.
- **Prompt-injection resistance is NOT claimed.** A turn crafted to emit
  false events is exactly the poisoning threat (D5/D6); the defense
  trialed here is the graded layer's absorption, not extractor
  robustness. An adversarial extractor-red-team is future work.
- **Hedge list is fixed and English-specific.** Not a linguistic claim.
