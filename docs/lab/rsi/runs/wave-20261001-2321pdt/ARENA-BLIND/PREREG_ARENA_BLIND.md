# PREREG: Arena-blind re-examination of the ROSTER C15 claim (ARENA-BLIND, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any audit evidence
recording, masked driver, or evaluation run. Any change to the design
below requires a dated amendment committed alone before the changed
work runs. Commit-order rule: this file's commit must strictly precede
every audit-evidence and implementation commit in this lane.

## 1. Mandate

BATTERY-E3 returned E3-ORACLE-DEPENDENT: blind composition assembles
graphs correctly, but the trial's CORRECT selections depended on the
unmasked verifier (t2_try_verify: accept iff output equals the
QUERY-carried expected value). Mandate: every wave construction claim
resting on unmasked QUERY evidence must be re-examined blind. This
lane executes that mandate for the ARENA4 ROSTER mechanism
(C15 0.947, BUILD-PASS, commits 19d9edc87 / 171c45101 / f8d7b9b2e).

ROSTER is a construction claim: it builds an entity roster at runtime
from exposure events and enumerates it to answer a goal probe. The
question is whether the arena battery's query mechanism ever feeds
the expected answer to the contestant (unmasked QUERY), and if so,
whether the C15 score survives with the oracle withheld.

Disclosure: the worker inspected the arena battery sources
pre-freeze to design this audit method (which fields the turn
protocol carries, how the driver invokes the contestant, what the
frozen ROSTER source parses). The inspection shaped the method; the
audit verdicts below are computed and recorded only after this
freeze, from the recorded commits.

## 2. Query-mechanism audit method (frozen)

A1. Sealed test-turn schema. Read line 118 of the sealed
    turns.jsonl (turn 117, item 63, cap 15): list every top-level
    field. Any field carrying an expected answer, answer key, or
    answer hint is an unmasked QUERY.

A2. Run-driver argv. Read run_sealed.sh (commit 171c45101): record
    exactly what is passed to the contestant process per turn
    (turn.json, statedir, worlddir) and what the scorer receives
    separately (world dir, replies, keys). The scorer must be the
    sole key-holder.

A3. Turn-protocol contract. Read the turn-protocol statement and the
    test-turn emit code in the committed world_gen.zag (turn kind
    documentation; emit_item; the test-turn JSON construction):
    record the complete field set the generator can emit on a test
    turn.

A4. Contestant parse surface. From the frozen ROSTER source
    (git show 171c45101:...roster_contestant.zag): record every field
    the test-turn branch parses from the turn JSON and how each
    parsed value is used (cognition vs scorer-envelope echo).
    Record what the listnames handler reads: learner state only, or
    anything from the query.

A5. Verifier scan. Grep the frozen ROSTER source for
    expected/expval/answer_key/answerkey/try_verify/verif/"exp"/
    correct/want semantics. Any accept-iff-matches-expected logic
    (the t2_try_verify pattern) anywhere in the arena path is an
    unmasked-QUERY dependence.

A6. observe_result turns. The sealed battery contains 4
    observe_result turns ("answers to your OBSERVE requests" per the
    turn protocol). Record whether ROSTER ever emits OBSERVE
    requests and whether any observe_result turn carries a test-item
    expected answer. ROSTER emits none; the audit records this.

ORACLE-FREE requires all of: A1 shows no answer-carrying field on
the listnames test turn; A2 shows the contestant never receives the
key file or any scorer state; A3 shows the generator contract
emits no answer field on test turns; A4 shows the handler reads
learner state only (item/cap are envelope echoes, not cognition
inputs); A5 returns zero hits; A6 shows no oracle path through
observe_result. If any of A1..A6 finds an unmasked query or a
verifier-with-expected pattern, the lane proceeds to section 3
(masked re-test) instead of recording ORACLE-FREE.

## 3. Masked re-test spec (conditional; runs only if the audit finds an unmasked query)

3.1 Masked query construction. A masked driver wraps the sealed
    per-turn loop: on each test turn it parses the turn JSON, and
    (a) removes any expected-answer field before writing turn.json,
    (b) fails closed (nonzero exit, ERROR line) if a smuggled
    oracle field is detected that the driver cannot strip
    (the E3 blind-driver fail-closed technique: QUERY must carry
    exactly the protocol fields; anything extra is a parse error).
    The masked driver is transport-only: diff against run_sealed.sh
    must show no new semantic cases, no modes, no bridges, no
    handlers, no task identities.

3.2 Fresh sealed battery. New seed (not 71503461337030), regenerate
    the world with the hash-verified world_gen binary, record
    pre-run sha256 of turns.jsonl and answer_key.json, commit the
    manifest before any masked run. The masked battery must not be
    a trivial variant of the observed one.

3.3 Contestant. The frozen ROSTER binary (sealed/bin/roster,
    sha256 abe647c7dfa369ccbde38b09f1acb65479b9b6ea04cbf1cd5d866253161c83d1),
    unmodified. Zero source changes.

## 4. Kill bars for the masked branch (frozen; never move after this commit)

AB-1 (masked C15): masked C15 >= 0.900 on the fresh sealed battery,
    all 3 runs. Sustains the BUILD-PASS.

AB-2 (no regression): per-capability scores on the other 15
    capabilities byte-identical to the v6 refreeze record (caps 1-7,
    10, 11, 13, 14, 16 at 1.000; caps 8, 9, 12 at 0.000).

AB-3 (determinism): 3/3 masked runs produce byte-identical stripped
    reply streams and byte-identical roster_trace.txt files.

AB-4 (masked mechanism documented): the masked driver diff vs the
    unmasked driver committed; transport-only change verified
    (K1-identical style check: cognition region byte-identical,
    driver-section diff shows only field-stripping and fail-closed
    logic); zero new semantic cases; grep audit for smuggled oracle
    references PASS.

BUILD-PASS-SUSTAINED requires AB-1, AB-2, AB-3, AB-4 all PASS.
Any bar failing yields the corresponding collapse verdict below.

## 5. Decision rule (frozen)

ORACLE-FREE: the audit of section 2 shows the arena battery's query
mechanism never feeds the expected answer to the contestant and the
ROSTER source contains no verifier-with-expected logic. Then the
C15 claim never rested on unmasked QUERY evidence; no masked
re-test is run; the ARENA4 BUILD-PASS stands as scored.

BLIND-SUSTAINED: the audit found an unmasked query, the masked
re-test ran under section 3/4, and all AB bars PASS (masked C15 >=
0.900). The C15 claim survives blind.

BLIND-COLLAPSE: the audit found an unmasked query, the masked
re-test ran, and masked C15 drops below 0.900. Then the C15 claim
was oracle-assisted; the lane reports this honestly and the ARENA4
BUILD-PASS is revoked pending a non-oracle selection mechanism.

The verdict is reported whichever way it lands. This is a
verification, not a new build: no repair proposals, no
patch-treadmill, no new mechanisms are in scope for this lane.

## 6. Scope and toolchain

Read-only toward the ARENA4, ARENA2, ARENA3, and BATTERY-E3 lane
dirs: sources extracted via git show from the recorded commits.
Commits local only under
docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-BLIND/; never push;
never git reset --hard; never rebase. Pure Zag only: safebin PATH,
`which python3` prints nothing at lane start and lane end; any
forbidden-interpreter invocation is PROCESS-FAIL and voids the
verdict. No em-dashes in lane docs (check_no_dash.sh before each
commit).
