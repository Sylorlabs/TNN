# PREREG: Arena active-inquiry mechanism (ARENA-INQ, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any INQ implementation,
binary, dev world, or evaluation run. Any change to the design below
requires a dated amendment committed alone before the changed code runs.
Commit-order rule: this file's commit must strictly precede every
implementation commit in this lane.

## 1. Objective

Raise C8 (active inquiry) from 0.000 on the sealed 68-item arena battery
(seed 71503461337030) with zero score regressions on the other 15
capabilities, 3/3 byte-identical reruns, and full architecture accounting.
Target: 58/68 = 0.853 with C8 at 1.000.

Battery count note: the parent task says "15 capabilities" and "the other
14". The sealed records (REFREEZE_RECORD.md, wave-20261001-1721pdt) show 16
capabilities and 68 items. The count does not reproduce, so it is flagged
here rather than asserted. The frozen no-regression bar covers all 15
non-target capabilities (C1-C7, C9-C16).

## 2. Capability pick justification

INQUIRY (C8) is picked, per the recommended ranking, for three reasons.
First, it is the weakest verified metric family among the zeros: the other
zeros (C9 causal intervention choice, C12 cross-biome transfer, C15
autonomous goal completion) have no complete protocol loop in the sealed
battery, while C8's battery protocol already contains a full inquiry loop
(test -> observe_result -> re-ask on items 64..67). Second, the v6
contestant already answers "UNKNOWN" honestly on the first ask; the missing
piece is exactly the active half of inquiry (requesting the missing
information and integrating the result), which is a genuine, bounded
mechanism, not a benchmark patch. Third, the mechanism generalizes beyond
C8 by construction (section 3): it fires on any unknown fact query, so it
also covers the C7 unknowable items consistently without changing their
scores.

## 3. Mechanism spec (INQ)

The INQ loop has three generic parts. No part is gated on a capability
number.

3.1 Request. On a test turn whose q parses as `fact|E|A` or `fact2|E|A`,
if the general fact store lookup fails (unknown), the contestant replies
"UNKNOWN" (honest, never a guess) and appends exactly one inquiry field to
the reply JSON line:
`"observe":[{"e":"<E>","a":"<A>"}]`
where E and A are the entity and attribute parsed from the question, not
from any table. The request names precisely the missing information the
learner needs. A white-box trace line goes to stderr (deterministic).

3.2 Absorb. On an `observe_result` turn, the contestant parses vals[0]
(e, a, v) and stores it through the EXISTING learn_fact path (the same
lexicon/concept/rule/fact-store machinery the expo handler uses). The
observe_result reply JSON is unchanged. Absorption is into the general
fact store, usable by any later query, not into C8-specific state.

3.3 Answer. On any later test turn for the same fact query (the re-ask),
the general fact lookup succeeds and the contestant replies the value
exactly. No observe field is emitted when the fact is known.

Surgical implementation points (v6 base source
devint1_contestant_v6.zag, sha256
c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89):
(a) in the test handler, after the fact/fact2 lookup fails, set the
observe-emission flag and append the field before the reply object closes;
(b) in the observe_result handler, replace the tick-only body with
parse-vals plus learn_fact (tick is preserved inside learn_fact).
No other handler logic is touched.

Architecture constraints (frozen): 0 new modes, 0 bridges, 0 routers,
0 task-specific admission gates, 0 hardcoded semantic cases, 0 hardcoded
entities, attributes, values, or answers. The two insertion points are
event-type dispatch on existing turn kinds, parallel to existing handlers.
Learner-state structures created: absorbed facts in the general fact
store (visible in state_bytes growth and the stderr trace).

## 4. Why this scores on the sealed C8 items

The frozen scorer (arena.zag) scores C8 per item as: last test-turn reply
string exactly equals the key AND the FIRST test-turn reply for the item
contains `"observe":[`. The battery emits, per C8 item: test (first ask),
observe_result (oracle fact), test (re-ask). INQ emits the observe field
on the first ask (unknown), absorbs the oracle fact, and answers exactly
on the re-ask. Verified preconditions: the 4 C8 oracle facts have zero
expo hits in the sealed world (grep audit on the 1721pdt sealed
turns.jsonl), so the unknown path fires on all 4 first asks; the absorbed
facts are the last scored items in the battery (items 64..67, then done),
so absorption cannot perturb any other scored item.

Expected per-item flow: first ask reply "UNKNOWN" with observe field
(first_obs=1), re-ask reply exactly the value (streq=1), item score 1000.

## 5. Kill bars (frozen; never move after this commit)

K1 (C8 inquiry): C8 = 4/4 = 1.000 on the sealed 68-item battery.
K2 (no regression): per-capability scores on C1-C7 and C9-C16
byte-identical to the v6 refreeze record; total 58/68. Zero score
regressions on all 15 non-target capabilities.
K3 (determinism): 3/3 full sealed runs produce byte-identical stripped
reply streams (ms and rss_kb excluded, the v6 K6 exclusion class) and
byte-identical stderr traces.
K4 (pure Zag): zero non-safebin executable invocations in this lane;
`which python3` prints nothing at lane start and lane end. Any forbidden
invocation is PROCESS-FAIL and voids the verdict.
K5 (sealed validity): world_gen and arena rebuilt from committed sources
with hashes matching the refreeze record (world_gen
c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211,
arena 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076);
regenerated turns.jsonl hash matches the sealed world
(0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469);
pre-run hashes of turns.jsonl and the key file recorded before the
contestant runs; the contestant never opens key/idmap/proof files
(worlddir arg-presence-checked only); grep audit of the mechanism source
for the 4 C8 oracle values and the 4 C8 entity/attr names returns zero
hits. Disclosure: while verifying the turn protocol from the committed
1721pdt sealed world, the worker incidentally saw the observe_result
values; they are never used by the mechanism (the request content is
parsed from the question, the answers come from the turn stream), and
the grep audit is the evidence.
K6 (negative controls, both halves causal):
K6a ablation INQ_ASK_OFF (observe emission disabled, one-line source
delta): C8 = 0/4 on the sealed battery.
K6b ablation INQ_ABSORB_OFF (learn_fact on observe_result disabled,
one-line source delta): C8 = 0/4 on the sealed battery.
K7 (honesty preserved): on the 3 C7 unknowable items, the reply field is
exactly "UNKNOWN" in all sealed runs (an observe request is a request,
never an answer; no hallucination).
K8 (architecture): delta accounting recorded (source lines added/changed;
0 new modes, 0 bridges, 0 routers, 0 task-specific handlers, 0 hardcoded
semantic cases); learner-state structures created (absorbed facts in the
general fact store, verified live in the stderr trace and state_bytes).
K9 (no L3 claim): explicit disclaimer in the evaluation report. This
mechanism does not meet Criterion 0: the "request the named missing fact"
semantics is researcher-authored handler logic (fails C0-A
runtime-defined semantics); the inquiry form is fixed, not incrementally
constructed from experience (fails C0-B); no unforeseen representational
forms are produced (fails C0-C); absorbed facts are reused for answering
but no new representation is invented (fails C0-D). Plainly: INQ is
L1/L2 fact-acquisition infrastructure (a better ask-observe-answer loop),
not L3 representational invention. No L3 claim is made.

BUILD-PASS requires K1, K2, K3, and K4 all PASS. K5 through K9 must also
PASS for the verdict to stand; any bar failing yields BUILD-FAIL with the
killing evidence named. Kill bars never move after freezing; a broken
prereg is amended transparently and re-frozen, never salvaged.

## 6. Evaluation protocol (frozen)

6.1 Rebuild world_gen and arena from committed competitive_arena sources
with the pinned znc; verify hashes against the refreeze record; abort on
mismatch.
6.2 Regenerate the world (deterministic seed inside world_gen.zag);
verify turns.jsonl sha256 equals
0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469.
6.3 Record pre-run sha256 of turns.jsonl and the key file. Build the INQ
contestant from the committed implementation source; record its sha256.
6.4 Dev smoke test (in /tmp, never sealed): hand-crafted mini turn
streams exercising request-on-unknown, absorb-on-observe_result,
answer-on-reask, and no-request-on-known. Must pass before the sealed run.
6.5 Sealed run: fresh state dir, per-turn invocation
`inq <turn.json> <statedir> <worlddir>`, replies appended, over all 131
turns; score with the rebuilt arena binary. Repeat twice more (3/3) for K3.
6.6 Ablations K6a/K6b: one-line source deltas, rebuilt, one sealed run
each on the same world, C8 scored.
6.7 Audits: grep for C8 oracle strings in mechanism source (K5); grep of
C7 reply fields for exact "UNKNOWN" (K7); keyword scan for
mode/bridge/router/handler/gate in added lines (K8); byte scan for
em-dash in lane docs.

## 7. Scope reminders (frozen)

INQ is a CANDIDATE mechanism only. No L3 claim (K9), no TNN-2 substrate
claim, no TNN-beats-LLM claim. The canonical 0.573 is not moved by this
result (only a clean refreeze reproducing composition without
contamination can move it). The LLM baseline comparison remains pending
credentials and is out of scope for this lane.

FROZEN 2026-10-01 PDT. Lane: wave-20261001-2321pdt/ARENA.
