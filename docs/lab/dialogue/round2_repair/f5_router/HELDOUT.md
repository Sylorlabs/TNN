# HELDOUT.md — F5-ROUTER frozen held-out evaluation

Frozen: 2026-09-23, in PREREG_F5.md and `probes/heldout_battery.txt`,
before any repair code was written. First run: after the released build
passed all scaffold probes. Never used for tuning.

## The 7 probes

| id | context | input | expected |
|----|---------|-------|----------|
| H1 | who wrote the martian? | tell me a joke about the eiffel tower. | `I don't know any jokes.` |
| H2 | (same block) | tell me another joke. | `I don't know any jokes.` |
| H3 | martian / born / born-before-tower | do you remember the first thing i asked you? | `You asked: who wrote the martian?` |
| H4 | (same block) | what did i just ask? | `You asked: do you remember the first thing i asked you?` |
| H5 | (same block) | can you recall my second question? | `You asked: when was he born?` |
| H6 | who wrote the martian? | please forget what i told you. | `I can't forget.` |
| H7 | (same block) | forget it all. | `I can't forget.` |

New joke requests (H1/H2), new history phrasings incl. a no-`remember`
form and a `recall` form (H3–H5), new instruction phrasings (H6/H7).
Context turns carry sentinel E-lines (expected FAIL, not scored).

## Results

Run: `probes/run_heldout_1.log`, rerun: `probes/run_heldout_2.log`
(byte-identical, `cmp` clean).

**7/7 PASS.** Actual outputs matched the frozen expected strings
byte-for-byte:

- H1/H2 → `I don't know any jokes.`
- H3 → `You asked: who wrote the martian?`
- H4 → `You asked: do you remember the first thing i asked you?`
- H5 → `You asked: when was he born?`
- H6/H7 → `I can't forget.`

## Scaffold vs released

Scaffold (`probes/run_scaffold_2.log`): 13/13 target turns PASS
(R2 turns 14/15/18 + 10 paraphrases). The released build is the same
binary — no scaffold-only code was ever added, so there was nothing to
remove: the dispatcher is token-level general machinery (joke/memory/
forget token sets + ordinal selection over kind-0 hist rows), with no
per-case branches and no constants fitted to probe phrasings. One
scaffold-driven generalization happened during GUIDE: the memory
detector was widened from `did`+`i`+verb to self-referential past
speech (`i`/`my` + ask/asked/say/said/tell/told/question), because the
scaffold probe "what was the first thing i asked?" has no `did`.
This was a rule generalization, not a probe-specific patch, and the
held-out set was still unseen when it was made.
