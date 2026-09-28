# REDTEAM4 fresh mini-set — predictions (written BEFORE any run)

8 new items, authored 2026-09-27 by the red team, never seen by the implementation.
None of these queries were executed before this file was written.
Predictions derive from the Round-4 mechanism story (PREREG4 + v7 traces), not from runs.

## Item shapes and per-mode winner predictions

### r01 — V4-binding H2 (forget-hurt), new fact pair (eiffel tower / louvre)
Query: `forget the eiffel tower; really, the louvre is better?`
Story: forget(6)+challenge(2) fire; bid15 (forget, eiffel fact) vs bid19 (challenge, louvre fact).
V4 denies the forget-target fact (fewer dependent bids) → bid15 eliminated → 19.
- single → 15 | nov4nG → 15 | nov4 → 15 | nG → 19 | onebrain → 19 | ablate → 19 | min → 19
- human expected_bid: **15** (the forget directive is the operative act)

### r02 — V4-binding H1 (correction-hurt), new fact pair (tnn reproduce / tnn upscale)
Query: `no, i meant the tnn reproduce tale; really, the tnn upscale story is better?`
Story: mirrors q06–q08 INCLUDING the confound — correction(0)+challenge(2) fire;
bid16 (correction, reproduce fact, inter=1) vs bid19 (challenge, upscale fact, inter=2).
V4 denies the correction-target fact in onebrain; the REINT_RULE independently prefers
bid19's stronger fact (inter=2/qual=22 > inter=1/qual=11) in nov4.
- single → 16 | nov4nG → 16 | nov4 → 19 | nG → 19 | onebrain → 19 | ablate → 19 | min → 19
- human expected_bid: **16** (the correction is the operative act)

### r03 — reintegration-room, duel-kill (joke→memory), new facts (joke / tnn upscale)
Query: `tell a hilarious joke, then recall the tnn upscale story?`
Story: joke(4)+mem(5) fire; single argmax picks bid13 (joke, top score); branch duel kills
the thin joke reading; null/reint converge on bid14.
- single → 13 | nov4nG → 14 | nov4 → 14 | nG → 14 | onebrain → 14 | ablate → 14 | min → 14
- human expected_bid: **14** (the bare joke is a decoy; recall grounds the answer)

### r04 — reintegration-room, duel-kill (joke→resume), new facts (joke / tnn pig snout)
Query: `make me laugh, then continue the tnn pig snout saga?`
Story: joke(4)+resume(1) fire; duel kills joke; bid17 (resume) wins everywhere forked.
- single → 13 | nov4nG → 17 | nov4 → 17 | nG → 17 | onebrain → 17 | ablate → 17 | min → 17
- human expected_bid: **17**

### r05 — reintegration-room, one-bid reint-rule (resume→compose), new facts
Query: `resume the everest saga, but compare the louvre with the eiffel tower?`
Story: resume(1)+compose(8) fire; single argmax picks bid17 (resume, higher score);
REINT_RULE prefers bid18 (compose) on stronger fact overlap/quality; neutered null
(lowest-hid alive) keeps 17 in nG/nov4nG.
- single → 17 | nov4nG → 17 | nov4 → 18 | nG → 17 | onebrain → 18 | ablate → 18 | min → 18
- human expected_bid: **18** (the comparison is the deliverable; the saga is parked)

### r06 — reintegration-room, one-bid, duel-silent (joke→memory), new facts (joke / tnn sticker)
Query: `tell me a joke, then remember the tnn sticker tale?`
Story: mirrors q29 — joke(4)+mem(5) fire but the duel stays silent (as in q29's branches);
single and neutered modes stay on bid13; REINT_RULE prefers bid14's stronger fact.
- single → 13 | nov4nG → 13 | nov4 → 14 | nG → 13 | onebrain → 14 | ablate → 14 | min → 14
- human expected_bid: **14**

### r07 — support-quality (challenge+memory), new facts (joke / louvre)
Query: `prove the joke wrong, then recall the louvre tale?`
Story: challenge(2)+mem(5) fire; single picks bid13 by score; forked modes move to bid14
via duel or reint rule. ablate is low-confidence (q30 analog had ablate=13).
- single → 13 | nov4nG → 14 | nov4 → 14 | nG → 14 | onebrain → 14 | ablate → 13? | min → 14
- human expected_bid: **14**

### r08 — support-quality (joke+resume), new facts (everest / tnn reproduce)
Query: `tell a funny everest story, then resume the tnn reproduce saga?`
Story: mirrors q32 — joke(4)+resume(1); duel kills joke in forked modes; ablate=13 per q32 analog.
- single → 13 | nov4nG → 17 | nov4 → 17 | nG → 17 | onebrain → 17 | ablate → 13 | min → 17
- human expected_bid: **17**

## Aggregate story predictions (the kill test)
- V4-harm replicates on r01 (onebrain/nG → 19 vs nov4 → 15): the H2 mechanism.
- r02 replicates the q06–q08 confound (nov4 → 19 WITHOUT V4): the H1 mechanism story's weak point.
- Duel-driven flips (r03, r04, r08) and reint-rule flips (r05, r06) separate cleanly.
- Systematic misprediction (e.g., duels not firing where predicted, V4 binding a different fact) kills the corresponding mechanism claim.
