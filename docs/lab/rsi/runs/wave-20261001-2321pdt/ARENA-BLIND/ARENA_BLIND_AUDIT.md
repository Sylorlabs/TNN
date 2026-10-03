# ARENA-BLIND query-mechanism audit (wave-20261001-2321pdt, ARENA-BLIND lane)

Mandate: BATTERY-E3 E3-ORACLE-DEPENDENT (blind composition assembles
graphs correctly; CORRECT selections depended on the unmasked
verifier t2_try_verify: accept iff output equals the QUERY-carried
expected value). Every wave construction claim resting on unmasked
QUERY evidence must be re-examined blind. Target: the ARENA4 ROSTER
mechanism (C15 0.947, BUILD-PASS).

Audit method: PREREG_ARENA_BLIND.md (frozen alone, commit 0b95a6601),
criteria A1..A6. All evidence below was collected after the freeze,
from the recorded commits, read-only (git show for lane sources).

## A1. Sealed test-turn schema: PASS (no answer-carrying field)

The listnames test turn (sealed world, turns.jsonl line 118):
{"turn":117,"kind":"test","item":63,"cap":15,"q":"listnames"}

Across all 72 test turns in the sealed battery: 0 carry any
exp/answer/key/oracle/expected field (grep -c returned 0). The
complete top-level field set on test turns is exactly
{turn, kind, item, cap, q}. There is no unmasked-QUERY field to
mask; the turn protocol has no expected-answer slot at all.

## A2. Run-driver argv: PASS (contestant never receives keys)

run_sealed.sh (commit 171c45101) invokes the contestant per turn as:
  "$ROSTER" "$R/turn.json" "$R/state" "$W"
where turn.json is one line of turns.jsonl. The scorer runs
separately afterward:
  "$B/arena" score "$W" "$R/replies.jsonl" "$R"
The key file (answer_key.json) is an argument to the scorer only,
never to the contestant.

## A3. Turn-protocol contract: PASS (no answer field emittable)

world_gen.zag documents the turn protocol (in the frozen prompt
pack): "Turn protocol: each turn is one JSON object with a kind
field: brief, expo (an observation event), test (a question with
fields item, cap, q), observe_result (answers to your OBSERVE
requests), done." The test-turn emit code constructs exactly
{"turn":<n>,"kind":"test","item":<i>,"cap":<c>,"q":"<q>"}. The
generator cannot emit an expected-answer field on a test turn; the
field does not exist in the contract.

## A4. Contestant parse surface: PASS (handler reads learner state only)

From the frozen ROSTER source (git show 171c45101,
roster_contestant.zag, sha256
453855599c332c85eaaf896f9632888c5f23ca0a17b92415bfb24fdca4ecb3c2):
the test-turn branch (line 1173) parses item, cap, and q. item and
cap are echoed into the reply JSON envelope (lines 1269-1271) so the
scorer can map replies to items; they are not cognition inputs. q
is split into head/params for dispatch. The listnames handler
(lines 1259-1277) reads only the learner-state entity roster
(roster_count / roster_emit); it parses nothing from the question
beyond the head dispatch (the v6 wire-protocol pattern). No
expected value is read from the query because none is present.

## A5. Verifier scan: PASS (zero verifier-with-expected logic)

Grep over the frozen source for expected/expval/answer_key/
answerkey/try_verify/verif/correct/oracle semantics returns zero
semantic hits (one benign comment line about correction-event
fields old/new). There is no t2_try_verify analogue anywhere in
the arena path: no accept-iff-matches-expected logic, no candidate
set, no selection step. ROSTER generates exactly one candidate
(the roster enumeration), so the E3 failure mode (oracle selection
among multiple executable chains) has no structural analogue here.

## A6. observe_result turns: PASS (no oracle path)

The battery contains 4 observe_result turns answering OBSERVE
requests. The ROSTER contestant never emits an OBSERVE request
(zero OBSERVE request lines in any sealed reply stream; the source
matches are the kind string "observe_result" only). Its
observe_result branch (line 1163) is a no-op exposure: tick only,
no roster_touch, no learning of the carried values. The carried
vals are single fact triples (e.g. Segunu shape wide), not goal
answers, and the roster trace confirms Segunu was never added
(n=9). No oracle path exists through observe_result.

## Verdict: ORACLE-FREE

All six criteria PASS. The arena battery's query mechanism never
feeds the expected answer to the contestant: the turn protocol has
no expected-answer field (A1, A3), the driver never passes keys to
the contestant (A2), the frozen ROSTER source parses no expected
value and contains no verifier-with-expected logic (A4, A5), and
the observe_result channel is a no-op for this mechanism (A6).

Consequence per the frozen decision rule: the C15 claim never
rested on unmasked QUERY evidence. The masked re-test branch
(section 3/4 of the prereg) is not triggered; no new runs, no new
sealed battery. The E3 mandate is satisfied for ROSTER by this
audit: the mechanism is oracle-free by construction of the battery
protocol, not by masking a query that was never unmasked.

The ARENA4 BUILD-PASS stands as scored. This lane issues no repair
proposal (no-patch-treadmill rule); none is needed: there is no
oracle dependence to repair.

## Scope note

This audit covers the arena battery query mechanism (turns.jsonl
test turns) and the frozen ROSTER source at commit 171c45101. It
does not re-litigate the ARENA4 sealed evaluation itself, which
stands on its own 8 kill bars.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing at
lane start (NAMECHECK.md Step 0) and lane end (exit 1). Zero Python
or other interpreter invocations; shell only sequenced pinned znc
reference builds, git read ops, grep/sed/sha256sum, and file
writes. No PROCESS-FAIL event.
