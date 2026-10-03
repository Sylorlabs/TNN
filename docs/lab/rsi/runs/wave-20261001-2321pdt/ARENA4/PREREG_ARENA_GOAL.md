# PREREG: Arena goal-by-roster mechanism (ARENA-ROSTER, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any ROSTER implementation,
binary, dev world, or evaluation run. Any change to the design below
requires a dated amendment committed alone before the changed code runs.
Commit-order rule: this file's commit must strictly precede every
implementation commit in this lane.

## 1. Objective

Raise C15 (goal) from 0.000 on the sealed 68-item arena battery
(seed 71503461337030) with zero score regressions on the other 15
capabilities, 3/3 byte-identical reruns, and full architecture
accounting. Target: 54.947/68 = 0.808 with C15 at 0.947.

Battery count note: the sealed records (REFREEZE_RECORD.md,
wave-20261001-1721pdt; ARENA2/ARENA3 per-capability tables) show 16
capabilities and 68 items. The count does not reproduce any "15
capabilities" phrasing, so it is flagged here rather than asserted.
The frozen no-regression bar covers all 15 non-target capabilities
(C1-C14, C16).

## 2. Capability pick justification

C15 (goal, n=1, "listnames") is picked. C8 (inquiry) is taken by the
sibling ARENA lane and is not duplicated here. C9 (causal) is taken by
the C9BAT lane on the corrected battery and is not attempted here.

The ARENA2 lane rejected C15 as "1 item, narrow enumeration,
ordering-fragile." This lane re-audited C15 from the frozen sources
(C15_AUDIT.md) and does not sustain that rejection:
- The frozen scorer (arena.zag, hash matches the refreeze record)
  scores cap 15 as an order-insensitive set F1 over comma-split
  names: sc = 2000*inter/(ne+nr). The "ordering-fragile" premise is
  refuted by the scorer source: order does not matter.
- 9 of the 10 entities are observable in exposure turns; an
  experience-based roster scores 2000*9/(10+9) = 947 = 0.947 in any
  order. The honest experience-based answer is 0.947, not 0.
- Unlike C9 (only gaming passes; the honest mechanism scores 0),
  C15 is passable by a general mechanism that maintains an entity
  roster in learner state from exposure experience and enumerates it
  to satisfy the stated goal. No sealed values, no briefing exploit,
  no format trick are needed.

C15 selected because: (a) genuinely zero in the v6 refreeze (0.000);
(b) genuinely passable without gaming, as shown above; (c) the
mechanism is learner-state roster maintenance plus goal enumeration,
the goal-family instance of "recall what the learner knows"; (d) it
builds on the v6 base, not on the TRX/INQ candidate line, because the
roster mechanism does not compose with transfer or inquiry machinery,
it is orthogonal to both, and the v6 base is the honest substrate.

## 3. Mechanism spec (ROSTER)

One learner-state structure plus one question-type handler in the
existing test-turn dispatch (the established v6 pattern, same as
fact/hop2/conflict/zem handlers).

3.1 Entity roster (new learner state). 12 slots x 16 bytes at W offset
14000 (inside the free region 13924..16384; templates end at 13924).
fn roster_touch(W, nm): nm is a null-terminated name buffer. Scan the
12 slots: if any occupied slot string-equals nm, return (dedupe). Else
copy nm (up to 15 chars plus NUL) into the first empty slot
(W[base]==0). If all 12 slots are occupied, return (roster full;
no eviction, deterministic).

3.2 Roster population (experience only). roster_touch is called:
- from learn_fact with the entity name buffer (covers f and k
  exposure events; both carry entity names),
- from learn_rel with both entity name buffers (covers r events).
No other call sites. The briefing file is never read; worlddir is
arg-presence-checked only, as in v6. The roster therefore contains
exactly the entities observed in the turn stream, in
first-appearance order, with zero researcher-supplied names.

3.3 listnames goal handler (test dispatch). If
streq(head,"listnames")==1: enumerate occupied roster slots in slot
order, comma-join into ans (no spaces, no trailing comma). If the
roster is empty, ans stays "UNKNOWN" (the v6 default). The handler
reads learner state only; it parses nothing from the question beyond
the head dispatch, which is the v6 wire-protocol pattern.

3.4 White-box trace. A trace file roster_trace.txt in the state dir
records "roster_add <name>" for each newly added name (expo turns)
and "listnames n=<k> reply=<...>" for the goal turn. The trace is a
decision record, not cognitive state.

3.5 Why this scores on the sealed C15 item. The sealed world exposes
9 entity names in its turn stream (verified in the audit). The roster
holds those 9 names; the handler emits them comma-joined; the frozen
set-F1 scorer computes 2000*9/(10+9) = 947. Expected C15 = 0.947 on
every regeneration, since the roster is derived from the turn stream
alone.

## 4. Kill bars (frozen; never move after this commit)

K1 (C15 goal): C15 >= 0.900 on the sealed 68-item battery, all 3
runs. Expected 0.947. The bar is set below the honest
experience-based ceiling so it does not demand the briefing-provided
10th name (Segunu is never observed in the turn stream; the audit
records this as a battery limitation, not a mechanism defect).

K2 (no regression): per-capability scores on C1-C14 and C16
byte-identical to the v6 refreeze record (caps 1-7,10,11,13,14,16 at
1.000; caps 8,9,12 at 0.000); total 54.947/68 = 0.808. Zero score
regressions on all 15 non-target capabilities.

K3 (determinism): 3/3 full sealed runs produce byte-identical
stripped reply streams (ms and rss_kb excluded, the v6 K6 exclusion
class) and byte-identical roster_trace.txt files.

K4 (pure Zag): zero non-safebin executable invocations in this lane;
`which python3` prints nothing at lane start and lane end. Any
forbidden invocation is PROCESS-FAIL and voids the verdict.

K5 (sealed validity): world_gen and arena rebuilt from committed
sources with hashes matching the refreeze record (world_gen
c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211;
arena 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076);
regenerated turns.jsonl hash matches the sealed world
(0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469);
pre-run hashes of turns.jsonl and the key file recorded before the
contestant runs; the contestant never opens key/idmap/proof/briefing
files (worlddir arg-presence-checked only); grep audit of the
mechanism source for the sealed entity-name strings returns zero
hits. Disclosure: while verifying the turn protocol from the
committed sealed world, the worker saw the sealed question strings
(contestant-visible content); the mechanism hardcodes none of them,
and the grep audit is the evidence.

K6 (negative control, causal): ablation ROSTER_OFF (roster_touch
call sites disabled, surgical source delta): the listnames item
replies UNKNOWN, C15 = 0.000, all other capabilities unchanged. The
roster is necessary for the gain; no other machinery carries it.

K7 (architecture): delta accounting recorded (source lines
added/changed; 0 new modes, 0 bridges, 0 routers, 0 task-specific
admission gates, 0 hardcoded semantic cases); keyword scan of added
lines for mode/bridge/router/gate finds only benign hits; learner
state adds one structure (entity roster, documented above with its
offset and lifecycle).

K8 (no L3 claim): explicit disclaimer in the evaluation report. This
mechanism does not meet Criterion 0: the roster form (fixed 12x16
slot table) is researcher-authored, not incrementally constructed
from experience (fails C0-B); the enumeration semantics is handler
logic, not runtime-defined semantics (fails C0-A); no unforeseen
representational forms are produced (fails C0-C); no new
representation is invented, only an experience-derived roster
maintained and enumerated (fails C0-D). Plainly: ROSTER is L2 goal
infrastructure (persistent roster plus goal enumeration), not L3
representational invention. No L3 claim is made.

BUILD-PASS requires K1, K2, K3, and K4 all PASS. K5 through K8 must
also PASS for the verdict to stand; any bar failing yields BUILD-FAIL
with the killing evidence named. Kill bars never move after freezing;
a broken prereg is amended transparently and re-frozen, never salvaged.

## 5. Evaluation protocol (frozen)

5.1 Rebuild world_gen and arena from committed competitive_arena
sources with the pinned znc; verify hashes against the refreeze
record; abort on mismatch.
5.2 Regenerate the world (deterministic seed inside world_gen.zag);
verify turns.jsonl sha256 equals
0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469.
5.3 Record pre-run sha256 of turns.jsonl and answer_key.json. Build
the ROSTER contestant from the committed implementation source;
record its sha256.
5.4 Dev smoke test (in /tmp, never sealed): hand-crafted mini turn
streams exercising roster add (f event), dedupe (repeated entity),
rel entities added, listnames with 2 names (exact reply string),
listnames with empty roster (UNKNOWN). Must pass before the sealed run.
5.5 Sealed run: fresh state dir, per-turn invocation
`roster <turn.json> <statedir> <worlddir>`, replies appended, over all
turns; score with the rebuilt arena binary. Repeat twice more (3/3)
for K3.
5.6 Ablation K6: surgical source delta (roster_touch call sites
disabled), rebuilt, one sealed run on the same world.
5.7 Audits: grep for the 10 sealed entity-name strings in mechanism
source (K5); keyword scan for mode/bridge/router/gate in added lines
(K7); byte scan for em-dash in lane docs.

## 6. Scope reminders (frozen)

ROSTER is a CANDIDATE only. No L3 claim, no TNN-2 substrate claim, no
TNN-beats-LLM claim. The canonical 0.573 is not moved by this result.
C9 remains the C9BAT lane's on the corrected battery; C8 remains the
ARENA lane's. This lane touches neither.
