# PREREG: Autonomous goal completion by generic default recall (ARENA5-DEFRECALL, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any DEFRECALL
implementation, binary, dev world, or evaluation run. Any change to
the design below requires a dated amendment committed alone before
the changed code runs. Commit-order rule: this file's commit must
strictly precede every implementation commit in this lane.

## 1. Objective and the gap being closed

The ARENA4 lane's C15 audit (flag #2) records that the implemented
C15 (ROSTER, BUILD-PASS, 0.947) is a single probe satisfied by a
listnames question handler added to the test-turn dispatch, while
the prereg spec described AUTONOMOUS GOAL COMPLETION WITH TOOLS.
This lane closes that gap, subject to the load-bearing design
constraint: the goal must be satisfied WITHOUT a dedicated
goal-completion handler. The learner must enumerate its persistent
entity roster to satisfy the goal through the EXISTING generic
action machinery (the same machinery that answers other questions).
If a dedicated handler proves unavoidable, the verdict is
HANDLER-DEPENDENT (an honest negative), not BUILD-PASS.

Target: C15 >= 0.900 on a fresh 68-item sealed battery, zero score
regressions on the other 15 capabilities, 3/3 byte-identical reruns,
full architecture accounting, zero dedicated goal handlers.

Battery count note: the sealed records (REFREEZE_RECORD.md,
wave-20261001-1721pdt; ARENA2/ARENA3 per-capability tables; the
battery.json format) show 16 capabilities and 68 items. The frozen
no-regression bar covers all 15 non-target capabilities (C1-C14,
C16).

## 2. Autonomous goal spec (frozen)

2.1 Goal as stated to the learner. On the sealed battery,
capability 15 is posed as a test turn
{"kind":"test","item":<i>,"cap":15,"q":"listnames"}: a bare prompt
(no "|" parameters) asking the learner to list the entity names it
knows. (On the original battery this was item 63; the index may
differ on the fresh seed. The goal string is the battery's C15
probe.)

2.2 Tools and actions available. The frozen battery provides no
multi-step tool protocol for the contestant: the original spec's
OBSERVE and EXPERIMENT tools exist only in the LLM prompt pack, not
in the per-turn contestant harness (run_sealed.sh feeds turns
sequentially; the contestant replies once per turn). This divergence
is stated honestly, as ARENA4 stated it. The actions available are
the existing generic test-turn actions: parse the turn, consult
persistent learner state (facts, relations, conflicts, templates,
and the experience-built entity roster), compose a reply string,
emit the reply JSON. The autonomy tested here is that the goal is
completed with no dedicated goal handler, via the generic default
action defined below.

2.3 What counts as autonomous completion. The learner produces a
reply that enumerates its persistent entity roster, scoring >=
0.900 under the frozen order-insensitive set-F1 scorer, with NO
mechanism branch keyed on the goal string "listnames" (or on any
other goal or question string for this purpose). The enumeration is
produced by the generic default action, which fires for ANY bare
prompt with no specific handler, and whose generality is
demonstrated on novel dev prompts never present in any battery
(see the evaluation protocol).

## 3. Mechanism spec (DEFRECALL)

Built on the v6 base
(docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/devint1_contestant_v6.zag).
The roster is orthogonal to TRX/INQ; the roster implementation is
extracted from ARENA4's recorded commits (171c45101), not rebuilt
from working files.

3.1 Entity roster (learner state, from ARENA4, unchanged logic). 12
slots x 16 bytes at W offset 14000 (free region 13924..16384; zem
templates end at 13924). Functions roster_touch, roster_has,
roster_count, roster_emit, extracted verbatim from the committed
ARENA4 implementation. Population: roster_touch called from
learn_fact with the entity name buffer (covers f and k exposure
events) and from learn_rel with both endpoint name buffers (covers
r events). Experience only. No briefing reads. No
researcher-supplied names. The roster holds exactly the entities
observed in the turn stream, in first-appearance order.

3.2 Generic default action (the goal-completion path; NOT a
dedicated handler). In the test-turn dispatch, at the existing
fallback position (where v6 carries only a no-op comment):
- Compute `known`: 1 if the question head matches any existing
  specific handler (fact, fact2, hop2, conflict, zemprod, zemclass),
  else 0. This mirrors the existing dispatch; it encodes no new
  question semantics.
- If known==0 AND the question is a bare prompt (p1, p2, p3 all
  empty, i.e. the question string contains no "|" parameters) AND
  the roster is non-empty: enumerate the roster into the reply
  (comma-joined via roster_emit). This is the bare-prompt knowledge
  report: with no applicable specific procedure and no parameters
  to interpret, the learner volunteers its persistent knowledge
  state.
- Otherwise the v6 behavior is preserved exactly (reply stays
  UNKNOWN). In particular, parameterized questions with no handler
  (invent|notation, discrim|..., remap_prod|..., remap_class|...)
  keep replying UNKNOWN, which preserves the frozen scorers that
  reward honest abstention (cap 11 scores 1.000 iff the reply is
  exactly UNKNOWN; cap 7 iff the reply contains UNKNOWN).
- The action references no question string and no goal string. Its
  trigger is structural (dispatch miss plus bare prompt).

3.3 Rationale (frozen). A bare prompt with no applicable specific
procedure is maximally ambiguous; the general default is to
volunteer the knowledge state. A parameterized question makes a
specific demand; with no applicable procedure the honest default is
abstention (UNKNOWN). This is a general structural rule, not a
goal-specific branch: it is blind to which goal it satisfies.

3.4 What this is NOT. There is no branch keyed on "listnames" or on
any other goal or question string. The string "listnames" appears
nowhere in the mechanism source (verified by grep in K5 and the
K-C0A audit). The goal is satisfied as a consequence of the general
default, demonstrated on novel dev prompts.

3.5 Trace. The default action appends one line
"defrecall n=<k> reply=<...>" to the state-dir trace file
(decision record, not cognitive state). Roster population appends
"roster_add <name>" (as in ARENA4). Empty-roster default firings
leave the reply UNKNOWN and write no trace line.

3.6 Why this scores on the C15 probe. The world exposes 9 entity
names in its turn stream on any seed (structural; see K1). The
roster holds those 9 names. The C15 probe is a bare prompt with no
specific handler, so the default action enumerates the roster,
comma-joined. The frozen set-F1 scorer computes
2000*9/(10+9) = 947. Expected C15 = 0.947 on every regeneration,
since the roster is derived from the turn stream alone.

## 4. Kill bars (frozen; never move after this commit)

K1 (C15 goal): C15 >= 0.900 on the fresh 68-item battery, all 3
runs. Expected 0.947. Structural basis (frozen here): on any seed,
exactly 9 of the 10 world-gen entity names appear in expo turn
events. Entity index 9 occurs only in the never-exposed C8 oracle
facts, the C8 test questions, and the C15 key. Verified from the
frozen world_gen.zag: f events cover entity indices 0-5 (C1) and
6-8 (C5 wrong facts); k events cover 6-8 (corrections); r events
cover 0-7 (the hardcoded rel array); x events cover 2,3,4
(hardcoded c6ent). Union: indices 0-8, nine entities, on every
seed. The bar sits below the honest 0.947 ceiling and does not
demand the unobservable 10th name.

K2 (no regression): per-capability scores on C1-C14 and C16
byte-identical to the v6 baseline run on the SAME fresh battery.
The baseline is the v6 base contestant
(devint1_contestant_v6.zag), built with the pinned znc from the
committed v6 source, run once on the fresh world before any
DEFRECALL run. Zero score regressions on all 15 non-target
capabilities.

K3 (determinism): 3/3 full fresh-battery runs produce byte-identical
stripped reply streams (ms and rss_kb excluded, the v6 K6 exclusion
class) and byte-identical defrecall trace files.

K4 (pure Zag): zero non-safebin executable invocations in this lane;
`which python3` prints nothing at lane start (NAMECHECK.md Step 0)
and lane end. Any forbidden invocation is PROCESS-FAIL and voids
the verdict.

K5 (sealed validity; adapted for the fresh battery, frozen here):
- competitive_arena/ is unmodified (git status clean on that tree).
- arena.zag is rebuilt from the committed frozen source with the
  pinned znc; its sha256 must equal the refreeze record
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076;
  abort on mismatch.
- world_gen fresh-seed variant: copied from the committed frozen
  world_gen.zag with ONLY the seed literal on line 265 changed from
  71503461337030 to 71503461337031; the diff between the variant
  and the frozen source is exactly that one line (verified and
  recorded); the variant's sha256 is recorded; the frozen source is
  never modified.
- Fresh turns.jsonl sha256 and fresh answer_key.json sha256 are
  recorded BEFORE any contestant run.
- The contestant never opens key/idmap/proof/briefing files
  (worlddir is arg-presence-checked only; read_file call sites are
  audited).
- Grep audit: zero hits for the fresh world's 10 entity-name
  strings in the mechanism source.
- Disclosure: while verifying the turn protocol from the generated
  fresh world, the worker sees contestant-visible turn content; no
  sealed answer string is hardcoded; the grep audit is the evidence.

K6 (negative control, causal): ablation DEFRECALL_ROSTER_OFF (the
roster_touch call sites disabled, surgical source delta): on the
fresh battery, the C15 item replies UNKNOWN, C15 = 0.000, all other
capabilities unchanged versus the v6 fresh baseline. The roster is
necessary for the gain; the default action alone (with an empty
roster) hallucinates nothing.

K7 (architecture): diff of the v6 base source against
defrecall_contestant.zag, with lines added, changed, and removed
recorded; 0 new modes, 0 bridges, 0 routers, 0 task-specific
admission gates, 0 hardcoded semantic cases; ZERO dedicated goal
handlers (no mechanism branch keyed on any goal or question string
for enumeration; verified by grep for "listnames" returning zero
hits in the mechanism source and by the structural-trigger
documentation in section 3.2); keyword scan of added lines for
mode/bridge/router/gate finds only benign hits; learner state adds
one structure (entity roster, W offset 14000, documented in section
3.1).

K8 (no L3 claim): explicit disclaimer in the evaluation report.
DEFRECALL does not meet Criterion 0: the roster form (fixed 12x16
slot table) is researcher-authored, not incrementally constructed
from experience (fails C0-B); the default-action semantics is
researcher-written dispatch logic, not runtime-defined semantics
(fails C0-A); no unforeseen representational forms are produced
(fails C0-C); no new representation is invented, only an
experience-derived roster maintained and reported by a general
default (fails C0-D). Plainly: DEFRECALL is L2 goal infrastructure
(persistent roster plus a general default recall action), not L3
representational invention. No L3 claim is made.

BUILD-PASS requires K1, K2, K3, and K4 all PASS. K5 through K8 must
also PASS for the verdict to stand. If the evidence shows that a
dedicated goal handler is unavoidable (i.e. the goal cannot be met
through the generic default without breaking other capabilities),
the verdict is HANDLER-DEPENDENT with the killing evidence named,
not BUILD-PASS. Any other bar failing yields BUILD-FAIL with the
killing evidence named. Kill bars never move after freezing; a
broken prereg is amended transparently and re-frozen, never
salvaged.

## 5. Frozen sealed battery spec (fresh seed, 68 items)

- Fresh seed: 71503461337031 (the sealed seed 71503461337030 plus
  one). Declared here and frozen. No reselection for any reason.
- world_gen fresh-seed variant as specified in K5, built with the
  pinned znc from the lane-local variant source.
- 68 items; the battery structure (capability/item layout, C15
  bare-prompt probe, 10-name key in index order) is
  seed-independent, verified from the frozen world_gen.zag.
- The battery is generated ONCE. Pre-run hashes of turns.jsonl and
  answer_key.json are recorded before any contestant run. The
  contestant runs never read the key.

## 6. K-C0A audit (zero new semantic cases; frozen)

- The mechanism introduces zero branches that match on question or
  goal meaning. The `known` flag mirrors the six existing v6
  handler heads (fact, fact2, hop2, conflict, zemprod, zemclass);
  it encodes no new semantics.
- The default action's trigger (dispatch miss plus bare prompt) is
  structural. It parses no goal string and references none.
- The roster operations (touch, has, count, emit) are generic state
  operations over experience-observed names.
- Verification (frozen): grep for "listnames" in
  defrecall_contestant.zag returns zero hits; grep for the fresh
  world's entity-name strings returns zero hits; keyword scan of
  added lines for mode/bridge/router/gate is clean. The audit is
  re-run on the final committed source before the verdict.

## 7. Evaluation protocol (frozen)

7.1 Build arena.zag from the committed frozen source with the pinned
znc; verify its sha256 against the refreeze record; abort on
mismatch. Build the world_gen fresh-seed variant; verify the diff
against the frozen source is exactly the seed literal line; record
the variant hash.
7.2 Generate the fresh battery once into the lane sealed/world
directory. Record pre-run sha256 of turns.jsonl and
answer_key.json. Verify 68 items and the presence of the cap-15
bare-prompt probe.
7.3 Build the v6 baseline contestant from the committed v6 source
with the pinned znc; record its sha256. Run it once on the fresh
world (fresh state dir); record per-capability baseline scores.
This is the K2 reference.
7.4 Dev smoke test (in /tmp, never sealed): hand-crafted mini turn
streams exercising roster add (f event), dedupe (repeated entity),
bare "listnames" (exact reply string), novel bare prompts
("recall", "who") also enumerating the roster (generality),
parameterized novel prompts ("invent|notation", "foo|bar")
replying UNKNOWN (abstention), and a bare prompt with an empty
roster replying UNKNOWN. Must pass before any sealed run.
7.5 Build DEFRECALL from the committed implementation source with
the pinned znc; record its sha256; verify the source is
byte-identical to the committed file before building.
7.6 Sealed runs: fresh state dir per run; per-turn invocation
`defrecall <turn.json> <statedir> <worlddir>` over all turns;
score with the rebuilt arena. Repeat twice more (3/3) for K3.
7.7 Ablation K6: roster_touch call sites disabled (surgical source
delta), rebuilt, one sealed run on the same fresh world.
7.8 Supplementary integrity check (not a kill bar): default action
disabled with the roster enabled, rebuilt, one sealed run;
expected C15 = 0.000, proving the default action is the
goal-completion path and no hidden handler carries the goal.
7.9 Audits: grep audits (K5 entity names; K-C0A "listnames" and
semantic cases); keyword scan for mode/bridge/router/gate in added
lines (K7); byte scan for em-dash in lane docs before each commit.

## 8. Scope reminders (frozen)

DEFRECALL is a CANDIDATE only. No L3 claim, no TNN-2 substrate
claim, no TNN-beats-LLM claim. The canonical 0.573 is not moved by
this result. C9 remains the C9BAT lane's on the corrected battery;
C8 remains the ARENA lane's. This lane touches neither. The
original spec's tool protocol (goal turns with tools, action-trace
predicate, all target entities discoverable through interaction)
remains unimplemented by the frozen battery and is not implemented
here; that is a battery limitation, recorded honestly, not a
mechanism defect.
