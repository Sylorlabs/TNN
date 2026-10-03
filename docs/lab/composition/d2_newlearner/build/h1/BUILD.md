# H1 Practice-Trace Induction Learner — Build Notes

## What this is

A pure-Zag action-policy learner for the D2 composition battery, built from
frozen `PREREG_H.md` (H1 hypothesis). It learns OBS→action policies from
practice traces via:

1. **Relational abstraction** — each OBS is parsed by grammar into 11
   relational features (reachable mote direction/distance, on-cell content,
   storm bucket, zone, shelter, crystal count, ward presence, nearest untaken
   crystal direction, ward direction, energy bucket). No raw cell indices,
   tick numbers, or schedule constants appear in rules.
2. **Decision-list rules** — each rule is ≤4 feature tests → action, with
   firing count, mean predicted energy delta, and death count. Cap 256 rules.
3. **Seed hypotheses** — Sessions 2–4 procedures encoded as seed rules
   (hypotheses, not law: they start with n=1 and are revised by outcomes).
4. **Fixed-horizon outcome attribution** — each action's outcome is the energy
   delta 64 ticks later (plus storm-exposure penalty, minus death), attributed
   to the rules that proposed the action.
5. **Mismatch-driven splitting** — when |observed − predicted| > 10 (or
   unexpected death), split the rule on the most discriminative feature.
6. **Conflict resolution** — zero-death filter → max predicted mean → lowest
   action.

## Files

- `h1.zag` — the complete learner (single file, ~1200 lines, pure Zag).
- `h1bin` — compiled tester-handoff binary (NOT committed; rebuilt by testers).
- `proto/` — Python design prototype (not a deliverable; used for design
  iteration only).
- `scratch/` — determinism traces (not committed).

## Build

Toolchain (pinned):
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

```sh
cd ~/workspace/d2_new_learner/h1
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 h1.zag -o h1bin
```

Zero warnings. Binary SHA-256:
`4582975fa0c3b02accdb8ad7f1f6250716bf0c0e305657d7fd6185a73134c644`

## Protocol

Invoke as `<binary> chat`. The binary prints one startup banner line, then
reads stdin line-by-line. Every nonempty input line receives exactly one reply
beginning `A `:

- `OBS ...` → `A <digit>` (action 0–6).
- `CARD ...` → `A card noted`.
- `Which sub-skills ...` → `A 1,2,3,1` (etc., from card storm schedule).
- Anything else → `A noted`.

Debug output (rule dumps) goes to **stderr**, never stdout, so the protocol is
never broken. Invoke as `<binary> chat dumprules` to dump the rule table to
stderr at each episode end (tester audit path for P2 rule-firing inspection).

## Key design decisions

### Outcome: energy delta + storm-exposure penalty

The prereg says "mean energy delta". We compute outcome as:

    outcome = (E[t+64] − E[t]) − 10 × (storm-exposed ticks in (t, t+64])

The `−10` per exposed tick is a **deliberate augmentation**, openly declared
here. Rationale: EAT's +30 masks storm damage (−4/tick) in raw energy delta,
making unsheltered storm exposure statistically invisible (a rule "EAT during
ACTIVE storm" shows mean +25). Without the penalty, storm safety cannot emerge
from the statistics because the statistics don't see the risk. The penalty
makes exposure visible while keeping the outcome a function of the OBS trace
(no hardcoded storm-dodging policy — the learner still has to discover *which*
actions avoid exposure via rule statistics).

### Void inference and step veto

The prereg's "nearest reachable mote" feature requires a reachability notion.
We infer the per-episode void (adjacent zero-evidence cell pair, 20-tick
stability, self-refuting) and treat it as unreachable. The step veto (never
output LEFT/RIGHT into an inferred void cell) is **reachability machinery**,
not a policy head: it enforces the same reachability constraint the features
use. Without it, "reachable" in the features would be false advertising.

The void inference resets every episode (stale voids from previous scenarios
caused void-entry deaths in development).

### Seed rules

Sessions 2–4 procedures are hand-encoded as seed rules (16 seeds covering
forage, ward-build, and shelter). This is a **known gap** vs the prereg's
"parsed into seed hypotheses": we did not implement a controlled-vocabulary
parser. The seeds satisfy "not law" (n=1, revised by outcomes, splittable,
deletable), but a full implementation would parse the procedure text.

### Fixed horizon H=64

The outcome horizon (64 ticks) is an unpinned design choice. It covers a full
storm (30 ticks) plus settling time.

### Two passes

The prereg says "two passes over 24 practice scenarios" but the harness sends
each scenario once. We do one pass (what the harness gives us). Documented as
a material ambiguity.

### Death attribution

Narrow: only the proposers of the action taken on the death tick are blamed
(deaths++, outcome −200). Earlier pending triples are dropped uncompleted.
(Wide-window attribution smeared blame onto innocent rules and destroyed the
death filter.)

### Bounded memory

All tables are fixed-size `[]u8` arenas with explicit LE i32 accessors:
- 256 rules × 40B
- 8192-triple ring × 16B (overwrites oldest; no growth)
- 128 pending × 48B
- 512 exposed ticks × 4B
- 6 card lines × 512B
- 8192B line buffer

No `as []i32` casts (znc ZNC-2026-09-21-007). No unbounded growth. The 64KB
history panic class from D2 does not apply.

## Development validation (not the formal battery)

- Mock drive through real `d2bin`: P0 F/W/T 8/8/8 (development check only;
  testers run the formal battery).
- P1: FW→`1,2,3,1`, WF→`2,3,1`, FWF→`1,2,3,1,3,1` (all correct).
- Rule audit: 37 conditions sampled, all feature indices 0–10, zero raw
  cell/tick constants.
- Determinism: 3/3 byte-identical traces (see DETERMINISM.md).
