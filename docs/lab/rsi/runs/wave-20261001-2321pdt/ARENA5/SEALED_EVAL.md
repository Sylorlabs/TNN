# SEALED EVALUATION: ARENA5-DEFRECALL (wave-20261001-2321pdt, ARENA5 lane)

Independent sealed evaluation of the frozen DEFRECALL contestant
(sealed/bin/defrecall, sha256
3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7,
built with the pinned znc from the committed implementation source
defrecall_contestant.zag, commit 2320c3454; source verified
byte-identical to the commit before building; zero source changes
after the build) on the fresh sealed battery (seed 71503461337032,
selected per Amendment 1).

Scoring: per hidden item, thousandths via the frozen arena scorer;
cap 15 uses the order-insensitive set F1 sc = 2000*inter/(ne+nr).
Keys computed by the world generator, never by running the
contestant.

## Fresh battery (frozen per prereg + Amendment 1)

- Fresh seed: 71503461337032. Seed 71503461337031 was tried first
  and rejected: the world_gen variant aborted with exit 2 ("DSL
  EXHAUSTION FAILED"), a generator-validity failure, not an
  exposure outcome. Per Amendment 1 (committed alone as f3320caf8
  before any battery generation), candidates were tried in
  increasing order and the first valid seed was taken. Candidates
  tried: 2 (71503461337031 invalid, 71503461337032 valid). No other
  selection criterion was applied.
- world_gen fresh-seed variant source sha256
  d1deac919d462341821f0506737a6def5f97fad9c3a309fd2af3d12809fc168c;
  diff against the frozen world_gen.zag is exactly one line (the
  seed literal on line 265); the frozen source was never modified.
  Variant binary sha256
  f5d181da5c09006c80d62fa46b14aa125e546fe29dd55d8050aef7f450ae8936.
- arena.zag rebuilt from the committed frozen source: sha256
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
  matches the refreeze record.
- Pre-run hashes recorded BEFORE any contestant run:
  turns.jsonl
  cfe8f5a13e769586b6871e80d72e486058343329462210a5d747302bc5079b38;
  answer_key.json
  12acb1e5901629f1e34fae49b78f78011fb14cfc1565b11305521c09c3e90a68.
- Battery: 68 items; cap-15 probe is the bare prompt "listnames";
  the C15 key is the 10 fresh entity names in index order
  (Nurada,Nutazo,Perada,Numado,Rufise,Bekoka,Bevida,Beruka,Rurase,Momado).
- Exposure (structural, verified): 9 of the 10 entities appear in
  expo turn events (2-4 occurrences each); Momado (index 9) occurs
  0 times, as predicted from the frozen world_gen.zag (entity index
  9 appears only in the never-exposed C8 oracle facts, the C8 test
  questions, and the C15 key).

## v6 fresh baseline (K2 reference)

The v6 base contestant (devint1_contestant_v6.zag, built with the
pinned znc; binary sha256
5d2be6acf4d98ef2118e2e1f2e52d87d38a9f848cb83e04d8b252199ce966f15)
was run once on the fresh world before any DEFRECALL run:

| Cap | n | v6 fresh |
|-----|---|----------|
| 1 | 6 | 1.000 |
| 2 | 4 | 1.000 |
| 3 | 6 | 1.000 |
| 4 | 4 | 1.000 |
| 5 | 6 | 1.000 |
| 6 | 3 | 1.000 |
| 7 | 3 | 1.000 |
| 8 | 4 | 0.000 |
| 9 | 3 | 0.000 |
| 10 | 2 | 1.000 |
| 11 | 2 | 1.000 |
| 12 | 6 | 0.000 |
| 13 | 6 | 1.000 |
| 14 | 6 | 1.000 |
| 15 | 1 | 0.000 |
| 16 | 6 | 1.000 |
| TOTAL | 68 | 0.794 |

The pattern matches the original v6 refreeze exactly, confirming
the battery structure is seed-independent.

## Per-bar results

### K1 (C15 goal): PASS, 0.947 >= 0.900

All three sealed runs: C15 = 0.947 (single item; reply
"Nurada,Nutazo,Perada,Numado,Rufise,Bekoka,Bevida,Beruka,Rurase",
the 9 entities observed in the turn stream, enumerated from the
learner-state roster). White-box trace (roster_trace.txt,
byte-identical all runs):
  roster_add Nurada / Nutazo / Perada / Numado / Rufise / Bekoka /
    Bevida / Beruka / Rurase
  defrecall n=9
    reply=Nurada,Nutazo,Perada,Numado,Rufise,Bekoka,Bevida,Beruka,Rurase
The reply is the experience-built roster enumerated by the generic
default action. No sealed value is hardcoded anywhere in the
mechanism (K5 grep audit: zero hits for all 10 fresh entity names).
The 10th entity (Momado) is never observed in the turn stream (0
occurrences in exposure.jsonl); the kill bar 0.900 sits below the
honest 0.947 ceiling and does not demand it. Crucially, the trace
line is "defrecall", not "listnames": the goal was satisfied by the
generic default action, with zero mechanism branches keyed on the
goal string (K-C0A: zero "listnames" hits in the source).

### K2 (no regression): PASS

Per-capability scores, v6 fresh baseline vs DEFRECALL (all three
runs identical):

| Cap | n | v6 fresh | DEFRECALL |
|-----|---|----------|-----------|
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

Every non-target capability is byte-identical to the v6 fresh
baseline. Zero score regressions on all 15 non-target
capabilities. Total 54.947/68 = 0.808 on all three runs. Note in
particular that C11 (invent, 1.000) is preserved: the default
action fires only for bare prompts, so the parameterized invent
questions still reply UNKNOWN, which the frozen scorer rewards.

### K3 (determinism): PASS

3/3 full sealed runs produce byte-identical stripped reply streams
(sha256 7dbf163ed6523ad0f22b7d00a14033843022933908a8ed6d8395fb3dceeb49b9
all three; ms and rss_kb excluded, the v6 K6 exclusion class) and
byte-identical roster_trace.txt files (sha256
a8b9f675dac241db8636b9f89108bacf470b23b427a2258ccfba272e78f6267a
all three).

### K4 (pure Zag): PASS

Zero non-safebin executable invocations in this lane: bash sequenced
the pinned znc builds, the compiled binaries, git read/commit ops,
and file copies only. `which python3` prints nothing at lane start
(NAMECHECK.md Step 0) and lane end (exit 1, verified). No
PROCESS-FAIL event.

### K5 (sealed validity): PASS

- competitive_arena/ unmodified (git status clean on that tree;
  the frozen sources were read, never written).
- arena rebuilt from committed source: sha256
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
  matches the refreeze record.
- world_gen fresh-seed variant: 1-line diff verified (seed literal
  only); variant source sha256
  d1deac919d462341821f0506737a6def5f97fad9c3a309fd2af3d12809fc168c.
- Pre-run hashes recorded before any contestant run (see Fresh
  battery above).
- The contestant never opens key/idmap/proof/briefing files: the
  read_file call sites are /proc/self/status (rss), state.bin (own
  state), the turn file, and roster_trace.txt (own trace);
  worlddir is arg-presence-checked only.
- Grep audit of the mechanism source for all 10 fresh sealed
  entity-name strings returns zero hits. The roster is populated
  from the turn stream at runtime; no sealed entity, value, or
  answer string appears in the source.
- Disclosure: while verifying the turn protocol from the generated
  fresh world, the worker saw contestant-visible turn content
  (including the fresh entity names in exposure turns, which are
  the contestant's own experience). They are parsed at runtime,
  never hardcoded; the grep audit is the evidence.

### K6 (negative control, causal): PASS

Ablation DEFRECALL_ROSTER_OFF (the three roster_touch call sites
disabled, surgical 3-line source delta; binary sha256
ed707f19e5bb0955a2272d4d517c417b384a228112d8c08e21d9994813b45145):
the C15 item replies UNKNOWN, C15 = 0.000, total 54/68 = 0.794,
every capability byte-identical to the v6 fresh baseline. The
roster is necessary for the gain; the default action alone (with an
empty roster) hallucinates nothing.

### K7 (architecture): PASS

Diff of the v6 base source (devint1_contestant_v6.zag) against
defrecall_contestant.zag: 174 lines added, 0 lines removed, 0
lines changed. Additions: roster_touch / roster_has / roster_count
/ roster_emit (entity roster at W offset 14000, 12 x 16B, extracted
from ARENA4's committed implementation), trace1 (decision-log
appender), three roster_touch call sites in learn_fact/learn_rel,
expo-branch add tracing, the `known` dispatch-miss flag, and the
generic default action (bare-prompt knowledge report) at the
existing fallback position. The ARENA4 listnames handler block is
absent: replaced, not supplemented.
Keyword scan of all added lines for mode/bridge/router/gate: zero
hits. Zero new modes, zero bridges, zero routers, zero
task-specific admission gates, zero hardcoded semantic cases.
ZERO dedicated goal handlers: grep for "listnames" in the
mechanism source returns zero hits; no mechanism branch is keyed
on any goal or question string for enumeration; the default
action's trigger is structural (dispatch miss plus bare prompt),
documented in prereg section 3.2. Learner-state structures
created: one (entity roster, documented with offset and lifecycle
in the prereg and above). Capability-source delta: the goal answer
is computed from learner state (the experience-built roster) via
a general default action; source contributes only generic roster
maintenance and the structural default.

### K8 (no L3 claim): PASS (disclaimer recorded)

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

## Supplementary integrity check (not a kill bar)

Default action disabled with the roster enabled (surgical 1-line
delta forcing the default-action condition false): C15 = 0.000
(reply UNKNOWN), total 54/68 = 0.794. This proves the generic
default action is the goal-completion path: with the roster
populated but the default action off, the goal is not satisfied.
No hidden handler carries the goal.

## Dev generality demonstration (prereg 7.4, /tmp, never sealed)

Hand-crafted mini turn streams (fresh entities Aaa, Bbb, Ccc,
Ddd, never in any battery):
- Bare "listnames" -> "Aaa,Bbb,Ccc,Ddd" (roster enumerated)
- Novel bare prompts "recall", "who" -> "Aaa,Bbb,Ccc,Ddd"
  (the default is general, not goal-specific)
- Parameterized novel prompts "invent|notation", "foo|bar" ->
  "UNKNOWN" (honest abstention preserved)
- Bare prompt with empty roster -> "UNKNOWN" (no hallucination)
All passed before any sealed run.

## Verdict: BUILD-PASS

K1 PASS (0.947 >= 0.900), K2 PASS (54.947/68 = 0.808, zero
regressions), K3 PASS (3/3 byte-identical), K4 PASS (pure Zag),
K5 PASS (sealed validity on the fresh battery), K6 PASS (ablation
causal: C15 0.000, others unchanged), K7 PASS (174 added, 0 new
modes/bridges/routers/gates/semantic cases, zero dedicated goal
handlers), K8 PASS (L3 disclaimed).

Scope reminders (unchanged): DEFRECALL is a CANDIDATE only. No L3
claim, no TNN-2 substrate claim, no TNN-beats-LLM claim. The
canonical 0.573 is not moved by this result.

## Battery notes carried forward

- C15's honest experience-based ceiling is 0.947 on every seed:
  entity index 9 never appears in expo turn events (structural,
  verified from the frozen world_gen.zag). The kill bar (0.900)
  deliberately does not demand it.
- The frozen battery expresses the goal as a test-turn bare
  prompt; the original spec's tool protocol (goal turns with
  OBSERVE/EXPERIMENT tools, action-trace predicate) remains
  unimplemented by the battery. The autonomy demonstrated here is
  goal completion with no dedicated handler, via the generic
  default action. If multi-step tool use is the target, the
  battery needs the spec implemented.
- Counts used: 16 capabilities, 68 items, per the sealed records.

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing at
start and end; zero Python or other interpreter invocations; shell
only sequenced pinned znc, built binaries, git read/commit ops, and
file copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(byte scan via check_no_dash.sh before each commit).

## Lane infrastructure incidents (recorded honestly)

- The prereg-freeze commit (b63f80289) swept in two BATTERY-E4
  files that another worker had staged in the shared index. Fixed
  for all later commits by using `git commit -- <pathspec>`.
- The ARENA5 worktree directory vanished mid-lane (with the
  BATTERY-E4 directory); files were restored from the commit.
- A `pull --rebase` was started on the shared branch by another
  process (forbidden by the never-rebase rule); it stalled holding
  the index.lock. The lock was removed after verifying no active
  rebase remained, and the branch was confirmed intact.
- None of these affected the frozen prereg, the implementation
  source, the battery, or any measurement. All are local-only.
