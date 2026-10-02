# SEALED EVALUATION: ARENA-ROSTER (wave-20261001-2321pdt, ARENA4 lane)

Independent sealed evaluation of the frozen ROSTER contestant
(sealed/bin/roster, sha256
abe647c7dfa369ccbde38b09f1acb65479b9b6ea04cbf1cd5d866253161c83d1,
built from the committed implementation source roster_contestant.zag
(commit 171c45101; source verified byte-identical to the commit before
building) with the pinned znc; zero source changes after the build)
on the regenerated sealed world (seed 71503461337030).

Scoring: per hidden item, thousandths via the frozen arena scorer;
cap 15 uses the order-insensitive set F1 sc = 2000*inter/(ne+nr).
Keys computed by the world generator, never by running the contestant.

## Per-bar results

### K1 (C15 goal): PASS, 0.947 >= 0.900

All three sealed runs: C15 = 0.947 (single item, item 63, reply
"Kavipe,Sehiru,Zovina,Datamo,Zovinu,Tetaru,Zosumo,Dagumo,Zofiru",
the 9 entities observed in the turn stream). White-box trace
(roster_trace.txt, byte-identical all runs):
  roster_add Kavipe / Sehiru / Zovina / Datamo / Zovinu / Tetaru /
    Zosumo / Dagumo / Zofiru
  listnames n=9 reply=Kavipe,Sehiru,Zovina,Datamo,Zovinu,Tetaru,Zosumo,Dagumo,Zofiru
The reply is the experience-built roster enumerated in
first-appearance order. No sealed value is hardcoded anywhere in the
mechanism (K5 grep audit). The 10th entity (Segunu) is never observed
in the turn stream (0 occurrences in exposure.jsonl, verified in the
audit); the kill bar 0.900 sits below the honest 0.947 ceiling and
does not demand it.

### K2 (no regression): PASS

Per-capability scores, v6 refreeze vs ROSTER (all three runs identical):

| Cap | n | v6 | ROSTER |
|-----|---|------|--------|
| 1 | 6 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 |
| 8 | 4 | 0.000 | 0.000 |
| 9 | 3 | 0.000 | 0.000 |
| 10 | 2 | 1.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 0.000 |
| 13 | 6 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.947 |
| 16 | 6 | 1.000 | 1.000 |
| TOTAL | 68 | 0.794 | 0.808 |

Every non-target capability is byte-identical to the v6 refreeze
record. Zero score regressions on all 15 non-target capabilities.
Total 54.947/68 = 0.808 on all three runs.

### K3 (determinism): PASS

3/3 full sealed runs produce byte-identical stripped reply streams
(sha256 5e1ff7223683c6f0e5998836e8aadfdc441cfc3476918963233f6e77e981efbd
all three; ms and rss_kb excluded, the v6 K6 exclusion class) and
byte-identical roster_trace.txt files (sha256
743113d0f340f03957ccd673269dcdc9b2fbe7b0d995c251635e81dd3e58a6bd
all three).

### K4 (pure Zag): PASS

Zero non-safebin executable invocations in this lane: bash sequenced
the pinned znc builds, the compiled binaries, git read/commit ops,
and file copies only. `which python3` prints nothing at lane start
(NAMECHECK.md Step 0) and lane end (exit 1, verified 2026-10-01).
No PROCESS-FAIL event.

### K5 (sealed validity): PASS

- competitive_arena/ unmodified (git status clean).
- world_gen rebuilt from committed source: sha256
  c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211,
  matches the refreeze record. arena rebuilt: sha256
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
  matches.
- Regenerated turns.jsonl sha256
  0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469,
  matches the sealed world.
- Pre-run answer_key.json sha256
  a05ef916122ea9643fa69e4a4973b94ea1c603da642d9bd07788f61b89a07a51,
  matches ARENA2's pre-run record; recorded before any contestant run.
- The contestant never opens key/idmap/proof/briefing files: the only
  read_file call sites are /proc/self/status (rss), state.bin (own
  state), the turn file, and roster_trace.txt (own trace); worlddir is
  only arg-presence-checked.
- Grep audit of the mechanism source for all 10 sealed entity-name
  strings returns zero hits. The roster is populated from the turn
  stream at runtime; no sealed entity, value, or answer string appears
  in the source.
- Disclosure: while verifying the turn protocol from the committed
  sealed world, the worker saw the sealed question strings
  (contestant-visible content). They are parsed at runtime, never
  hardcoded; the grep audit is the evidence.

### K6 (negative control, causal): PASS

Ablation ROSTER_OFF (the three roster_touch call sites disabled,
surgical source delta in roster_abla.zag; binary sha256
7ab7b0dc3cba7813f9945b3fc3c19b799148f0f638e84c8fac85ef014e7604e7):
the listnames item replies UNKNOWN (trace: "listnames n=0
reply=UNKNOWN"), C15 = 0.000, total 54/68 = 0.794, every other
capability byte-identical to the v6 refreeze. The roster is necessary
for the gain; no other machinery carries it.

### K7 (architecture): PASS

Diff of the v6 base source (devint1_contestant_v6.zag) against
roster_contestant.zag: 164 lines added, 0 lines removed, 0 lines
changed. Additions: trace1 (decision-log appender), roster_touch /
roster_has / roster_count / roster_emit (entity roster at W offset
14000, 12 x 16B, free region 13924..16384), three roster_touch call
sites in learn_fact/learn_rel, expo-branch add tracing, and the
listnames goal handler in the existing test-turn dispatch.
Keyword scan of all added lines for mode/bridge/router/gate: zero
hits. Zero new modes, zero bridges, zero routers, zero task-specific
admission gates, zero hardcoded semantic cases. The listnames handler
is a question-type handler in the existing dispatch, the established
v6 pattern. Learner-state structures created: one (entity roster,
documented with offset and lifecycle in the prereg and above).
Capability-source delta: the goal answer is computed from learner
state (the experience-built roster); source contributes only the
generic roster maintenance and enumeration operations.

### K8 (no L3 claim): PASS (disclaimer recorded)

This mechanism does not meet Criterion 0: the roster form (fixed
12x16 slot table) is researcher-authored, not incrementally
constructed from experience (fails C0-B); the enumeration semantics
is handler logic, not runtime-defined semantics (fails C0-A); no
unforeseen representational forms are produced (fails C0-C); no new
representation is invented, only an experience-derived roster
maintained and enumerated (fails C0-D). Plainly: ROSTER is L2 goal
infrastructure (persistent roster plus goal enumeration), not L3
representational invention. No L3 claim is made.

## Verdict: BUILD-PASS

K1 PASS (0.947 >= 0.900), K2 PASS (54.947/68 = 0.808, zero
regressions), K3 PASS (3/3 byte-identical), K4 PASS (pure Zag),
K5 PASS (sealed validity), K6 PASS (ablation causal: C15 0.000,
others unchanged), K7 PASS (164 added, 0 new
modes/bridges/routers/gates/semantic cases), K8 PASS (L3 disclaimed).

Scope reminders (unchanged): ROSTER is a CANDIDATE only. No L3 claim,
no TNN-2 substrate claim, no TNN-beats-LLM claim. The canonical 0.573
is not moved by this result.

## Battery notes carried forward

- C15's honest experience-based ceiling on this battery is 0.947:
  entity 10 (Segunu) is never observed in the turn stream. If C15 is
  meant to test autonomous goal pursuit, the prereg spec (goal turns
  with tools, action-trace predicate, all target entities
  discoverable) should be implemented; the current probe plus the
  set-F1 scorer can only test roster recall.
- Counts used: 16 capabilities, 68 items, per the sealed records.
  The "15 capabilities" phrasing in earlier parent task texts does
  not reproduce from the sealed records and is flagged, not asserted.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing at
start and end; zero Python or other interpreter invocations; shell
only sequenced pinned znc, built binaries, git read/commit ops, and
file copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(byte scan via check_no_dash.sh before each commit).
