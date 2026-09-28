# D2 Instrument Spec — sim sub-skills composition battery

**Status:** SPEC ONLY. Written 2026-09-27 to satisfy the A7 build gate
(`AMENDMENT_2026-09-27_A7.md`, enacted 2026-09-27). This spec builds nothing,
runs nothing, enacts nothing. D2 construction may not begin until this spec
is reviewed; if the spec changes any frozen bar or design beyond what A1–A7
enact, §13 lists exactly what needs a further amendment.

**Frozen references.** `docs/lab/composition/PREREG.md` (frozen 2026-09-27,
commit `6ca9e042110ca`), §1 (operational definition), §2 (D2 paragraph), §3
(phases), §5 (novelty), §6 (taxonomy), §7 (kill bars). Enacted amendments
A1–A7 (2026-09-27) govern where they speak. TIDELOCK machinery: the real sim
is `docs/lab/invention/survival/src/world.zag` (Experiment 1); every
mechanism below cites the exact function/section it comes from. Nothing is
invented: the mechanics are TIDELOCK's; only the instrument (scenario
records, probe definitions, scoring criteria, reference arms) is new
writing, which is what A7 commissioned.

**Reading guide.** Micah reads these: the prose is plain English. The formal
definitions (generator formula, pass criteria, adjudication rules) are exact
because the build crew must implement them without inventing anything.

---

## 1. What D2 tests, in one paragraph

D1 tests composition of string-rewrite rules. D2 tests composition of
*behaviors over time*: three sub-skills learned in the TIDELOCK survival sim
— S1 forage (eat motes efficiently), S2 ward-build (crystal+crystal→WARD
before a storm), S3 storm-time (shelter during storm windows, forage outside
them). A D2 composition item is a *novel scenario* — a storm schedule and
resource layout the agent never saw — whose solution requires a *novel
sequence* of the sub-skills (e.g., forage-then-ward under a shifted storm
schedule). The agent acts tick by tick (one action per tick); scoring is per
episode against verifiable criteria derived from the sub-skills' semantics,
exactly as the frozen §1.3 requires ("correct is defined by the parts'
semantics composed per C's structure").

---

## 2. TIDELOCK mechanics this spec stands on

All from `docs/lab/invention/survival/src/world.zag` (Experiment 1 sim core)
and `docs/lab/invention/survival/PREREG.md` §3. If a mechanism below is not
in this table, it is not in the spec.

| # | Mechanism | Exact statement | Source |
|---|-----------|-----------------|--------|
| M1 | Grid & time | 1D line, 24 cells (0–23). Discrete ticks t=0..599. Fully observable state each tick. | PREREG §3; world.zag header |
| M2 | Agent energy | Start E=100, max 200. Basal cost 1/tick. Death at E≤0. | world.zag `world_init` (slot 2=100); `step` costs block |
| M3 | Void | Two adjacent cells (void_a, void_b); entering = death. | world.zag `step`, movement branch; slots 6,7 |
| M4 | Motes | 8 motes (6 near + 2 deep), fixed velocities, bounce at region ends. | world.zag mote drift block; slots 20+4k |
| M5 | EAT | On a mote's cell: +30 E per active mote; mote dormant 20 ticks, then respawns at its fixed cell. | world.zag `step`, `a==2` branch |
| M6 | Crystals | 4 at fixed cells. TAKE/DROP. Inventory cap 4. | PREREG §3; world.zag `a==3`/`a==4`, slots 60..67, 70..73 |
| M7 | Actions | One per tick: 0=LEFT 1=RIGHT 2=EAT 3=TAKE 4=DROP 5=COMBINE 6=WAIT. | world.zag header comment |
| M8 | COMBINE | Uses the two lowest-filled inventory slots, deterministic. | world.zag `lowest_two`, `a==5` branch |
| M9 | Recipe: WARD | crystal(0)+crystal(0) → WARD(3). Any other pair → no-op. | world.zag `recipe()` |
| M10 | DROP places WARD | DROP of a WARD puts it on the agent's cell as a placed item. | world.zag `a==4` branch (`placed_add`) |
| M11 | WARD shelter | On a WARD (or BEACON) cell: basal cost 0 AND storm-immune. | world.zag `sheltered()`; `step` costs block |
| M12 | Storms | 3 windows, 30 ticks each starting at s0,s1,s2. Storm zone cells 6..17. −4 E/tick in zone without shelter. Schedule/zone/damage are taught world physics; shelter *strategies* are not taught. | world.zag `storm_active()`; PREREG §3 |
| M13 | Variant files | 33 ints: void, start, 3 storm starts, 4 crystal cells, 8 motes × (pos, vel, respawn). No RNG. | world.zag `world_init`; `worlds/v00.txt` |
| M14 | Observation codes | Inventory codes: -1 empty, 0 crystal, 1 mote, 2 LAMP, 3 WARD, 4 SURGE, 5 PLANK, 6 BEACON. | world.zag slot-layout comment |
| M15 | Reference forage policy | Taught single-step heuristics exist as `r_policy`: storm→leave zone; on mote→EAT; low energy→approach mote; on crystal→TAKE; 2+ items→COMBINE; else WAIT. | world.zag `r_policy()` |

Deliberately NOT used: LAMP/BEACON/SURGE/PLANK recipes, void-crossing, the
I-arm deliberation machinery. D2 needs only M1–M15.

---

## 3. PARTS — S1, S2, S3 as D2 "parts"

Each part is defined by (i) what the agent must do, (ii) the scenario it is
probed on, (iii) the exact pass criteria. "Mastered" = ≥7/8 held-out probes
passed (frozen §2: "same ≥7/8 gate on held-out scenarios").

### S1 — forage: efficient mote eating (+30/mote, dormancy respected)

- **Definition.** Over a no-storm episode, the agent gains energy by moving to
  active motes and EATing on their cells (M5: +30/mote), never EATing where no
  active mote is (dormancy respected — an EAT on a dormant/empty cell wastes
  the tick), never entering void cells (M3), staying alive.
- **Probe scenario (template F).** 120 ticks. Storms at 900/930/960 (never
  active — M12 checks t in [s, s+30), T=600 max). Motes/crystals/void/start
  from the generator (§4). No ward needed or useful.
- **Pass criteria (all must hold):** alive at t=120; final E ≥ 100 (start);
  n_eat ≥ 4; wasted-EAT count = 0, where a wasted EAT = a tick with action 2
  (EAT) while no active mote shares the agent's cell and no SURGE is in
  inventory (M5/M14). Arithmetic check: every tick costs exactly 1 basal
  here (M2, no storm, no surge), so final E = 100 − 120 + 30×n_eat; n_eat=4
  gives exactly 100. Both criteria are stated for defense in depth.

### S2 — ward-build: crystal+crystal→WARD before a storm window

- **Definition.** The agent takes two crystals (M6), COMBINEs them (M8 — the
  two lowest-filled slots, so the agent must hold exactly the two crystals in
  the lowest slots or know the deterministic selection), gets a WARD (M9),
  and DROPs it onto a cell (M10) *before* the storm window starts, then
  shelters on it through the window (M11: basal 0, storm-immune).
- **Probe scenario (template W).** 90 ticks. Storms at 60/400/560 — only the
  [60,90) window matters. All 8 motes placed beyond the void (unreachable;
  nothing to forage). Two crystals within 2 cells of start, two further.
  Energy check: 100 − 60 basal = 40 at t=60; sheltered 60–90 costs 0 → 40 at
  t=90, alive. (No motes exist to extend this; the episode is short on
  purpose.)
- **Pass criteria (all must hold):** a WARD (type 3, M14) is placed on some
  cell before t=60; zero unmitigated storm ticks during [60,90), where an
  unmitigated storm tick = storm_active=1 AND in_zone(pos)=1 AND
  sheltered=0 (M11/M12); n_combine ≥ 1 (M8 — proves the ward was built, not
  found); alive at t=90.

### S3 — storm-time: shelter during storm windows, forage outside them

- **Definition.** Given a placed WARD (provisioned — see the coupling note
  below), the agent forages while no storm threatens and is sheltered
  (on the ward, M11) or out of the zone for every storm-active tick in the
  zone (M12). This is the "shelter during windows, forage outside" behavior
  from the frozen §2.
- **Probe scenario (template T).** 200 ticks. Canonical taught storm schedule
  150/350/550 (as in `worlds/v00.txt`), so only window [150,180) falls in the
  episode. A WARD is pre-placed on the agent's start cell (scenario extension
  §4). Motes available near start.
- **Pass criteria (all must hold):** zero unmitigated storm ticks during
  [150,180); n_eat ≥ 4 (proves foraging happened outside the window —
  energy check: 200 ticks, 30 sheltered at basal 0 → 170 basal; 100 − 170 +
  30×4 = 50 > 0, alive); alive at t=200.
- **Coupling note (documented limitation, not a bar change).** S3 depends on
  S2's product: sheltering needs a ward from somewhere. In isolation S3 is
  probed with the ward *provisioned*, so P0-S3 tests "shelter timing +
  forage timing given a ward," not ward acquisition. The composition items
  (§6) test the full chain where the agent must build the ward itself. This
  coupling is intrinsic to TIDELOCK (M11); the spec isolates by provisioning
  rather than by pretending the dependency away.

**Sub-skill index mapping (fixed, used by P1 per A3's neutral-index rule):**
sub-skill 1 = forage (S1), sub-skill 2 = ward-build (S2), sub-skill 3 =
storm-time (S3). P1 items (§6) refer to "sub-skill 1/2/3" only — never the
names — exactly as A3 requires for D1 ("part 1, part 2, …", never REVERSE…).

---

## 4. SCENARIO GENERATOR — deterministic, zero-RNG, novelty-verifiable

### 4.1 Scenario record format

A D2 scenario is a text file: the 33-int TIDELOCK variant format (M13 —
identical layout to `worlds/v00.txt`: void, start, 3 storm starts, 4 crystal
cells, 8 motes × pos/vel/respawn), plus a D2 extension block (instrument
level — it configures the probe, it changes no mechanic):

```
# D2 scenario <template>-<k>. Deterministic. No RNG.
<void_a>              # int 0 (void_b = void_a+1)
<start>               # int 1
<s0>                  # int 2 } 30-tick storm windows [s, s+30)
<s1>                  # int 3 }
<s2>                  # int 4 }
<c0> <c1> <c2> <c3>   # ints 5-8: crystal cells
<m0pos> <m0vel> <m0resp>   # ints 9-11  } x8 motes
...                   # ints 12-32
EPISODE <ticks>       # probe length (90/120/200/320; 80 for P3)
PREWARD <cell|none>   # pre-placed WARD cell (template T only; else none)
```

All scenario files are committed with a SHA-256 manifest. Episodes run each
scenario twice; byte-identical action traces required (mirrors frozen §4's
"same binary, same bytes, every run").

### 4.2 Templates

The template fixes the storm regime and the probe's intent; the counter k
varies the layout. Storm regimes per template:

| Template | Used in | Storms (s0,s1,s2) | Episode | Intent |
|----------|---------|-------------------|---------|--------|
| F | train-S1, P0-S1 | 900, 930, 960 (never active) | 120 | forage only; no storms exist |
| W | train-S2, P0-S2 | 60, 400, 560 | 90 | one approaching storm; motes unreachable |
| T | train-S3, P0-S3 | 150, 350, 550 (taught schedule) | 200 | ward pre-placed at start; shelter+forage timing |
| N | P3 | 900, 930, 960 | 80 | no-op: storms never, motes+crystals beyond void |
| FW | P2, P4 | s0 = 90 + ((11k + salt) mod 40) → 90..129; s1 = s0+200; s2 = s0+400 | 200 | **forage-then-ward under a shifted storm schedule** (the frozen §2 example) |
| WF | P2, P4 | 30, 330, 560 | 200 | ward-first forced: storm at t=30, crystals adjacent |
| FWF | P2 | 60, 240, 540 | 320 | sandwich: two windows, forage→ward→shelter→forage→shelter→forage |

Template W and N place all 8 motes beyond the void (positions
void_b+1 .. 21); template N additionally places all 4 crystals beyond the
void (cells void_b+2 .. void_b+5). Templates FW/WF/FWF place 2 crystals near
start (cells start+1, start+2 — safe: start ≤ 5 per §4.3, void_a ≥ 8) and 2
via the layout formula.

### 4.3 Counter formula (zero RNG)

`gen(template, salt_phase, k)` → full scenario record, all closed-form
modular arithmetic:

- `void_a = 8 + ((5k + salt_phase) mod 8)` → 8..15 (v00 uses 10, M13).
- `start = (3k + salt_phase) mod 6` → 0..5, always left of the void.
- Storms: per template table above (FW's s0 uses k; max s2 = 529, window
  ends 559 ≤ 600 ✓).
- Far crystals (j=0..3 as needed): `base_j = (salt_c + 5k + 7j) mod 24`,
  then deterministic repair: take the smallest offset o ≥ 0 such that the
  four cells `(base_j + o) mod 24` are pairwise distinct and none equals
  void_a or void_a+1. Terminates: 22 free cells ≥ 4 needed.
- Near motes (j=0..5): `pos_j = (salt_m + 3k + 5j) mod 24`, repaired off
  void cells by +1 steps; `vel_j = ±(1 + ((k+j+salt_m) mod 2))` with sign
  from `(7k + j) mod 2`; `respawn_j = (pos_j + 12) mod 24`, repaired off
  void cells the same way.
- Deep motes (j=6,7, and all 8 in templates W/N): `pos = void_b + 2 +
  ((salt_m + k + j) mod (20 − void_b))`, vel ±1, respawn = pos.
- Fixed salts: `salt_c = 11`, `salt_m = 13`; per-phase salts —
  train = 101, P0 = 103, P2 = 107, P3 = 109 (distinct primes; phases are
  separated three ways: disjoint k-ranges below, distinct salts, and
  different templates — and novelty is *verified* by §4.5, not trusted to
  the salts; this is the A2 lesson applied to D2).

### 4.4 Disjoint counter ranges per phase (mirrors frozen §4)

| Phase | k range | Templates | Count |
|-------|---------|-----------|-------|
| train | 0–23 | F ×8, W ×8, T ×8 | 24 single-sub-skill scenarios |
| P0 | 24–47 | F ×8 (S1), W ×8 (S2), T ×8 (S3) | 24 probes, 8 per sub-skill |
| P2 | 48–71 | FW ×8, WF ×8, FWF ×8 | 24 composition episodes |
| P3 | 72–79 | N ×8 | 8 reflex probes |
| P4 | — | re-analysis of the 16 FW+WF items grouped by template (no new items; mirrors D1, where P4 re-analyzes P2 data per ordered pair) | — |
| P1 | — | one retrieval item per P2 scenario (24 items) | — |

Training shows ONLY single-sub-skill scenarios (frozen §5: "Training mass
contains ONLY single-part applications"). The 24 training scenarios are the
scenario side of the training mass; the transcript side (how episodes become
teaching material) is the teaching protocol's business, constrained to these
scenarios (see §12, open question 2).

### 4.5 Novelty verification (mirrors frozen §5 — verified, not asserted)

"What counts as novel": a P2/P3 scenario is a *novel sequence* iff (a) its
full parameter record appears in no training scenario, (b) its storm-schedule
triple (s0,s1,s2) appears in no training scenario, (c) its crystal-cell set
appears in no training scenario, and (d) its required sub-skill *order* was
never demonstrated in training (training shows only single-sub-skill
scenarios — no multi-sub-skill order exists anywhere in the training mass —
so (d) holds by construction).

Procedure (run by the build crew, output committed):
1. Commit every scenario record (train/P0/P2/P3) + SHA-256 manifest.
2. **N1 — full-vector check:** no P2/P3 record's 33-int vector equals any
   training record's vector (exact integer comparison).
3. **N2 — storm-schedule check:** no P2 scenario's (s0,s1,s2) triple occurs
   in any training scenario. (FW's shifted schedules 90..129 and WF's 30 and
   FWF's (60,240,540) are absent from training's {900s, (60,400,560),
   (150,350,550)} by construction; the check verifies it.)
4. **N3 — surface-similarity check (the K6 analog):** no P2 scenario shares
   its exact crystal-cell set with any training scenario.
5. The checker prints PASS/FAIL with counts per check; the result is
   committed with the battery. Any FAIL blocks the battery — the generator
   is fixed, not the check.

This is D1 §5's "verified by construction — training shows only single-part
applications — plus text search of the committed training mass," adapted:
the search is an exact comparison over scenario records instead of over
token strings.

### 4.6 Cuing audit (mirrors frozen §5's blind cuing audit)

An auditor holding the committed training mass + the TIDELOCK world
description must not be able to derive any P2 scenario's solution *action
sequence* without composing the sub-skills. Concretely the auditor checks:
(a) no training transcript demonstrates a multi-sub-skill sequence (they are
single-sub-skill by §4.4); (b) the recipe table and physics are taught, but
shelter *strategies* are not taught (M12 — same standard as Experiment 1);
(c) the P2 storm schedules/layouts are absent from training (N1–N3). If the
auditor can exhibit a training transcript that already solves a P2 scenario,
that scenario is discarded.

---

## 5. Learner channel — observation and action format

The learner (real TNN learner, as in D1's full battery) plays an episode
tick by tick. Each tick it receives one observation line; it replies with
one action digit. All fields derive from real sim state (M1–M15); the text
serialization is instrument, not mechanics.

```
OBS t=<tick> pos=<pos> E=<energy> inv=<c0,c1,c2,c3> storm_in=<n|ACTIVE|none>
    zone=<0|1> shelter=<0|1> motes=<pos:active|dormant(n),...> crystals=<cells> ward=<cell|none>
```

- `inv` codes per M14 (-1 empty, 0 crystal, 1 mote, 2 LAMP, 3 WARD, …).
- `storm_in` = ticks until the next window starts (from the taught schedule,
  M12), `ACTIVE` inside a window, `none` if no window remains in the episode.
- `motes` lists each mote's cell and state (active, or dormant with ticks
  remaining — M5); `ward` = cell of any placed WARD/BEACON, else none.
- The scenario card (given once, before tick 0) states: the storm schedule,
  the crystal/mote summary, start position/energy, episode length, and the
  taught physics reminder. It never states or hints the solution sequence
  (cuing audit §4.6).

The learner replies with a single digit 0–6 (M7). Anything else = the tick's
action is recorded as invalid (counts as a wasted tick; three invalid
replies in one episode = episode FAIL).

---

## 6. SCORING RULE — what counts as a correct novel sequence

D1 scores exact-match on output strings. Action sequences admit many optimal
paths (different routes to the same mote, different forage orders), so a
single reference action string cannot define correctness. D2 scores
**per-episode pass/fail against verifiable semantic criteria** — the direct
operationalization of frozen §1.3 ("correct is defined by the parts'
semantics composed per C's structure"). The one exception is P3, which keeps
literal exact-match (§7). The tension with frozen §3's "Exact-match scoring"
wording is flagged in §13.

### Pass criteria per template (all conditions must hold)

| Template | Episode PASS iff |
|----------|------------------|
| P0-F (S1) | alive at t=120 AND final E ≥ 100 AND n_eat ≥ 4 AND wasted-EAT count = 0 AND no void entry |
| P0-W (S2) | WARD placed before t=60 AND zero unmitigated storm ticks in [60,90) AND n_combine ≥ 1 AND alive at t=90 |
| P0-T (S3) | zero unmitigated storm ticks in [150,180) AND n_eat ≥ 4 AND alive at t=200 |
| P2-FW | zero unmitigated storm ticks AND WARD placed before s0 AND n_eat ≥ 4 AND final E ≥ 40 AND alive at t=200 |
| P2-WF | zero unmitigated storm ticks AND WARD placed before t=30 AND n_eat ≥ 4 AND final E ≥ 40 AND alive at t=200 |
| P2-FWF | zero unmitigated storm ticks across both windows AND WARD placed before t=60 AND n_eat ≥ 7 AND final E ≥ 30 AND alive at t=320 |
| P3-N | action trace is exactly 80 × WAIT (action 6) — literal exact-match |

Definitions: *unmitigated storm tick* = tick with storm_active=1 AND
in_zone(pos)=1 AND sheltered=0 (M11/M12 — leaving the zone also mitigates,
which is legitimate storm-time behavior); *wasted EAT* = action 2 with no
active mote on the agent's cell and no SURGE in inventory (M5/M14);
*n_eat, n_combine* = the sim's own counters (world.zag slots 122/124).
Final-energy thresholds are feasibility-checked arithmetically in §3/§4
(e.g., FW: 200 ticks − 30 sheltered at basal 0 = 170 basal; 100 − 170 +
30×4 = 50 ≥ 40 ✓); the reference-validation gate (§10) empirically confirms
every scenario is passable by the scripted composer.

### Partial credit

None at the episode level for kill-bar purposes: an episode is PASS or FAIL,
like D1's exact-match. The harness additionally records per-criterion
booleans and the violation counts (unmitigated storm ticks, wasted EATs,
n_eat, final E, cause of death) for diagnosis and for the classifier — but
K1–K6 adjudication uses only episode pass/fail plus the P0/P1 records. This
is stated so the build crew does not invent a partial-credit scheme later.

### Why "WARD placed" is a criterion (the trivial-recombination exclusion)

Frozen §5: "a C solvable by a single part scores as a part probe, not a
composition item." Every P2 template *requires* all three sub-skills; the
WARD-placed criterion is what makes S2 load-bearing (a forage-only agent
that merely dodges storms can never satisfy it). If calibration (§10) ever
shows a P2 scenario passable without a ward, the scenario is invalid — not
the criterion.

---

## 7. CHANCE ARMS — NULL, SINGLE-RULE, WRONG-ORDER for action sequences

Per A1, `chance` = max(NULL, SINGLE-RULE, WRONG-ORDER) episode-pass rate,
measured on the D2 instrument itself. All three are fixed scripted policies
(reference modes shipped with the battery, like D1's `wrongord`).

| Arm | D2 definition | Grounding |
|-----|---------------|-----------|
| **NULL-D2** | Action 6 (WAIT) every tick, all 80–320 ticks. Zero decisions. | The action-sequence analog of D1's identity output: applies no sub-skill. Fails P2 by construction (starves: 200 ticks × basal 1 > 100 start energy, M2). |
| **SINGLE-RULE-D2** | Forage-only policy: exactly `r_policy` (M15) with the TAKE-crystal and COMBINE branches removed — i.e., storm→leave zone; on mote→EAT; low energy→approach mote; else WAIT. Never TAKEs, never COMBINEs, never DROPs. | D1's "applies only the first retrieved part": the first sub-skill (S1 forage) alone. Fails every P2 scenario by construction via the WARD-placed criterion (§6). |
| **WRONG-ORDER-D2** | Correct sub-skills, wrong order: S2→S3→S1. At t=0 goes to crystals, TAKE×2, COMBINE, returns to start, DROPs the ward, then forages (nearest active mote), sheltering when the storm threatens. The transplanted template-W order applied to every P2 scenario. | A1's principle: "retrieves the correct parts and applies them in the wrong order — masters parts, retrieves correctly, composes backwards." Design intent: under FW's shifted schedule it burns the early foraging window on the ward run (the frozen §2 example is "ward-build before forage under a shifted schedule"). |

**Calibration requirement.** NULL and SINGLE-RULE fail P2 by construction
(above). WRONG-ORDER's failure is enforced by the reference-validation gate
(§10): every P2 scenario must be failed by all three arms and passed by the
scripted composer. If WRONG-ORDER passes a scenario, the build crew sharpens
that template's time pressure (storm-start range, crystal distance) as a
*documented calibration* — criteria and bars unchanged — until the gate
holds. If a template cannot be made to fail WRONG-ORDER, STOP and report; do
not soften the criteria to manufacture the failure.

---

## 8. P0–P4 PHASE ANALOGS

| Phase | D1 (frozen §3, as amended) | D2 analog (this spec) |
|-------|---------------------------|----------------------|
| **P0 mastery gate** | 8 held-out probes per part, ≥7/8 | 8 held-out scenarios per sub-skill (k=24–47, templates F/W/T), ≥7/8 per sub-skill per §3 criteria. <7/8 → sub-skill excluded; P2 items needing it classify (a). |
| **P1 retrieval** | "Which parts, in which order, solve C?" — neutral indices, semantic format-tolerant scoring (A3) | Per P2 scenario (24 items): "which sub-skills, in which order, does this scenario require?" Sub-skills referenced as sub-skill 1/2/3 only (§3 mapping). Scored semantically/format-tolerantly against the template's canonical order: FW → 1,2,3,1 (forage, ward, shelter, forage); WF → 2,3,1; FWF → 1,2,3,1,3,1. Wrong/missing → (b). P1 never names the solution and is never fed into P2 (A3's chaining resolution: P2 presents the scenario directly; the P1 record is used for (b)-vs-(c) attribution only). |
| **P2 composition** | Produce C's output; exact-match; scored independently of P1 (A3) | Play the episode (§5 channel); per-episode PASS/FAIL per §6 criteria, scored independently of the P1 answer (a correct episode always counts even if P1 was scored wrong — the red-team 3a fix). Report raw P2 pass rate AND *elig* pass rate (P2 restricted to P1-correct items), per A3. |
| **P3 reflex probe** | Distractors where NO part applies; correct = identity/withhold; any application → (c-r) | 8 no-op scenarios (template N, k=72–79): no storms in horizon, motes and crystals unreachable beyond the void. Correct = the all-WAIT action string (80 × action 6) — literal exact-match, the action-sequence analog of identity output. Any non-WAIT action (any TAKE/COMBINE/DROP/EAT, any movement) = reflexive application, counted per item → (c-r). Energy check: 80 × basal 1 = 80 ≤ 100 start, so all-WAIT survives (M2). |
| **P4 interference** | Per ordered-pair accuracy table; (i,j) ≤0.25 while (j,i) ≥0.75 with parts mastered → (d) | Per order-template accuracy table over the 16 FW+WF P2 items (elig set only — retrieval-correct items, per the red-team 3b fix: the D-gate requires the pair's own retrieval to be correct). If acc(FW) ≥ 0.75 while acc(WF) ≤ 0.25, or vice versa, with all required sub-skills mastered → interference **(d) CONFIRMED**, naming the asymmetric order (e.g., "forage-first works, ward-first fails"). Items in the failing template previously classified (c) are reclassified to (d) — only items actually classified (c), never (a)/(b) items (red-team 3b fix). The 0.25/0.75 numbers are unchanged from frozen §3; the unit moves from ordered part-pairs to order templates (§13 flags this). |

Interleaving (A3): P3 no-op scenarios are interleaved among P2 episodes,
never one block; episode order is interleaved across templates (no
template blocking), mirroring A3's item-interleaving requirement.

---

## 9. K1–K6 ADJUDICATION for D2

All bars keep their frozen meanings and numbers; only the measured quantity
changes from string exact-match to episode pass/fail.

- **K1 — chance kills composition:** P2 episode pass rate (raw; elig reported
  alongside per A3) ≤ chance + 0.10 → composition claim KILLED (clean
  negative). `chance` = max(NULL-D2, SINGLE-RULE-D2, WRONG-ORDER-D2) pass
  rate measured on the D2 instrument (§7), per A1. The +0.10 margin is
  unchanged.
- **K2 — void:** >50% of the 24 P2 episodes classify (a) → battery VOID for
  composition (cannot test composition of unmastered parts); re-run after
  genuine mastery. (a) = any required sub-skill <7/8 at P0; required sets:
  FW/WF/FWF all require {S1, S2, S3} (they differ in *order*, which is what
  P4 tests).
- **K3 — attribution:** (b) accounts for >50% of P2 failures → finding is
  "retrieval failure, not combination failure." Failures = P2 episodes with
  output FAIL; (b) = P1 record wrong/missing for that scenario (§8).
- **K4 — reflex defect:** P3 reflex rate > 0.20 → uncritical-application
  defect CONFIRMED. Reflex rate = fraction of the 8 P3 items whose trace
  deviates from all-WAIT (§8). (The survival post-mortem's harmful-COMBINE
  analog, now isolated: applying sub-skills where none applies.)
- **K5 — interference defect:** any order template meeting the §8 P4
  asymmetry criterion → interference defect CONFIRMED with the order named.
- **K6 — memorization check:** D1's bigram mechanism ("inputs sharing no
  bigram with any training input") has no action-sequence counterpart —
  action traces have no token bigrams, and the memorization surface for D2
  is the *scenario* (storm schedule + layout), not the trace. K6-D2 is
  adjudicated as: (i) the committed novelty verification N1–N3 (§4.5) must
  PASS — this is the construction argument, the analog of D1's "pair-level
  memorization is impossible by construction" (training shows only
  single-sub-skill scenarios; no P2 storm schedule or layout was ever shown);
  (ii) the independent red team must *fail* to explain any passed P2 episode
  via trace replay — exhibiting a training-episode trace that the passed
  trace replays (exact match up to time-shift), or via schedule memorization
  — mapping the P2 scenario to the nearest training scenario by storm
  schedule and replaying its trace (the D2 analog of the red team's
  shift-memorizer attack, REDTEAM_REPORT finding 1a). If the red team
  succeeds → battery VOID, generator fixed. The bigram notion is declared
  N/A with this justification; §13 flags the mechanism change.

---

## 10. Failure-mode taxonomy mapping — (a)/(b)/(c)/(c-r)/(d) for D2

Classification is per P2 episode (P3 items are (c-r) only; P4 reclassifies
at template level), in the frozen §6 priority order:

| Code | D2 meaning | Criterion |
|------|-----------|-----------|
| (a) unmastered parts | A required sub-skill never cleared the P0 gate | sub-skill <7/8 at test time; item needs it |
| (b) retrieval failure | Parts pass, but the agent misidentified the required sub-skills/order | P1 record wrong/missing for the scenario |
| (c) combination failure | Parts pass, retrieval right, episode failed | P0 ≥7/8, P1 correct, §6 criteria not met |
| (c-r) reflexive application | Sub-skill applied where none applies | P3 item: any non-WAIT action in a no-op scenario |
| (d) interference | Order-asymmetric failure, parts fine alone | §8 P4 criterion: template asymmetry ≥0.75/≤0.25 on the elig set; only (c) items in the failing template reclassified |

Scoring is always computed independently of classification (the red-team 3a
fix): an episode's PASS/FAIL is a fact about the trace; the class is the
attribution overlay. The battery REPORTS the distribution, not just a score
(frozen §6).

---

## 11. Reference-agent validation gate (instrument self-check)

Before the real learner touches D2, the instrument must prove it
discriminates — the D2 analog of the pilot's PK1–PK4 (frozen §8). The build
crew ships these scripted reference modes alongside the battery:

- **REF-OK-D2** (positive control): scripted composer — forage policy
  (nearest active mote, EAT on cell), crystal run + COMBINE + DROP when
  `storm_in` ≤ time needed, shelter at ward during windows, resume forage
  after. Must PASS every P0 probe and every P2 scenario. (Acceptance
  criterion, not a prescribed implementation — the policy above is the
  suggested baseline.)
- **REF-NOMASTER-D2** → its P2 episodes must classify (a) (sub-skill
  deliberately broken, e.g., never EATs).
- **REF-NORETRIEVE-D2** → (b) (P1 answers deliberately wrong; episodes may
  still pass — scoring independent of classification, §10).
- **REF-NOCOMBINE-D2** → (c) (correct P0/P1, episodes failed on purpose,
  e.g., never builds the ward).
- **REF-REFLEX-D2** → (c-r) (forages/builds during P3 no-op scenarios).
- **REF-INTERFERE-D2** → (d) (passes FW, fails WF by rigid forage-first
  ordering — exercises the P4 gate).
- **NULL-D2, SINGLE-RULE-D2, WRONG-ORDER-D2** (§7): pass rates measured;
  `chance` computed; all three must FAIL every P2 scenario (NULL and
  SINGLE-RULE by construction; WRONG-ORDER via calibration, §7).

Gate: REF-OK-D2 passes everything; each broken reference mode's failed items
carry the intended class (≥80%, mirroring pilot PK3); all three chance arms
fail all P2 scenarios; every scenario run twice byte-identical (mirroring
PK4). If any scenario cannot satisfy the gate, the scenario is discarded
(next k in range) — the criteria and bars are never softened to make the
gate pass.

---

## 12. OPEN QUESTIONS — PENDING, never invented

1. **Real-learner episode interface (PENDING).** The spec fixes the
   observation/action contract (§5), but whether the dialogue-based TNN
   learner can sustain 90–320 tick episodes (one observation → one action per
   tick, hundreds of turns) — context budget, latency, turn protocol — is
   undetermined. The build crew resolves this with the learner line; episode
   lengths are capped (320 max) partly to bound this. If per-tick dialogue
   proves infeasible, the channel changes — that change needs its own
   amendment, since the P1/P2 presentation protocol would differ.
2. **Teaching protocol (PENDING).** How single-sub-skill episodes become
   training mass (transcript format, how the learner studies them) is the
   build crew's design, constrained by this spec: ONLY the 24 training
   scenarios (§4.4) may appear, and the cuing audit (§4.6) must still pass.
   No mastery theater: P0 must be genuine (same standard as Crew D's brief).
3. **S3's standalone status (DOCUMENTED LIMITATION).** S3-in-isolation is
   probed with a provisioned ward (§3 coupling note). Whether "storm-time"
   is truly separable from "ward-build" as a learned sub-skill — or whether
   the pair is one skill — is an empirical question the battery will shed
   light on (P4's order asymmetry speaks to it). The spec does not resolve
   it.
4. **Pass-threshold sharpness (CALIBRATION, not PENDING).** The final-energy
   and n_eat numbers in §6 are arithmetically feasible and REF-OK-D2 must
   pass them (§11). If a whole template proves impassable, STOP and report —
   thresholds are spec'd, not tuned.
5. **K6-D2 red-team attacks (PENDING EXECUTION).** The trace-replay and
   schedule-memorization attacks (§9 K6) are defined; running them is the
   independent red team's job at battery time.
6. **Scenario-record extension serialization (PENDING).** §4.1 fixes the
   semantics (EPISODE length, PREWARD cell); the exact text serialization is
   the build crew's, as long as it round-trips byte-identically.

---

## 13. REQUIRES FURTHER AMENDMENT — explicit flags, nothing smuggled

The following points in this spec go beyond, or sit in tension with, frozen
text as amended by A1–A7. Each needs governance's word before D2 is built;
the spec takes no position on which way they should be resolved.

1. **P2 scoring is criterion-based, not literal exact-match.** Frozen §3
   (as amended by A3) says "P2 — composition: produce C's output.
   Exact-match scoring." For action sequences, literal exact-match against
   one reference trace is infeasible — many optimal paths exist (different
   routes, different forage orders) — so §6 defines per-episode pass/fail
   against semantic criteria (the frozen §1.3 definition of correctness).
   Only P3 keeps literal exact-match (the all-WAIT string). A7 mandated "the
   scoring rule (what counts as a correct novel sequence)" — this spec
   answers it — but if governance reads the frozen "exact-match" wording as
   binding on D2, a dated amendment must explicitly permit criterion-based
   episode scoring for D2.
2. **K6's mechanism changes from bigrams to scenario-novelty + trace-replay.**
   Frozen §7 K6: "success holds on inputs sharing no bigram with any
   training input." Action sequences have no token bigrams; §9 adjudicates
   K6-D2 via the committed N1–N3 novelty checks plus red-team trace-replay
   and schedule-memorization attacks. If governance reads the bigram
   mechanism as frozen for D2, this needs a dated amendment restating K6
   for action sequences.
3. **P4's unit moves from ordered part-pairs to order templates.** Frozen §3
   P4 is per ordered pair of parts with the 0.25/0.25… 0.25/0.75 asymmetry
   numbers; §8 applies the same numbers to FW-vs-WF order templates (with
   the elig-set and actual-C-only reclassification fixes from the red team).
   Flagged as an interpretation under A7's mandate ("phase analogs");
   if governance wants it as an amendment, it is written up as one.
4. **No other frozen bar, threshold, or taxonomy code is changed.** K1's
   +0.10 margin, K2's 50%, K3's 50%, K4's 0.20, P4's 0.25/0.75, the ≥7/8
   gate, the (a)→(b)→(c)→(c-r)→(d) priority order, and the chance=max-of-
   three-arms principle (A1) are all preserved exactly.

---

## Appendix A. Worked example — one FW scenario end to end

k=48 (first P2 counter), salt_phase(P2)=107: void_a = 8 + ((240+107) mod 8)
= 8 + (347 mod 8) = 8+3 = 11 → void (11,12); start = (144+107) mod 6 =
251 mod 6 = 5; s0 = 90 + ((528+107) mod 40) = 90 + (635 mod 40) = 90+35 =
125 → storms [125,155), [325,355), [525,555); crystals near: 6, 7; far via
formula+repair (off void 11,12); motes via formula; episode 200 ticks.
Training never saw storm triple (125,325,525) (N2), never saw this layout
(N1), never saw this crystal set (N3) — verified by the §4.5 checker, not by
this arithmetic. The learner must: forage (S1) ticks 0–~, take 2 crystals,
COMBINE, DROP the ward before t=125 (S2), shelter [125,155) (S3), resume
foraging to t=200 (S1) — passing all six §6 criteria. NULL-D2 starves at
t=100; SINGLE-RULE-D2 never builds the ward; WRONG-ORDER-D2 (ward-first)
must fail it per the §11 gate or the template's time pressure is sharpened.

## Appendix B. Source map (where every mechanism came from)

- Sim core: `docs/lab/invention/survival/src/world.zag` (M1–M15; recipe
  table, action codes, slot layout, `step`, `r_policy`, `world_init`).
- Variant format: `docs/lab/invention/survival/worlds/v00.txt` (33 ints).
- World requirements: `docs/lab/invention/survival/PREREG.md` §3
  ("TIDELOCK sketch"; storms taught as physics, shelter strategies not
  taught; ≥3 distinct strategies calibration).
- Battery design: `docs/lab/composition/PREREG.md` (frozen 2026-09-27,
  commit 6ca9e042110ca) §§1–7; pilot red-team findings
  `docs/lab/composition/pilot/REDTEAM_REPORT.md` (wrong-order K1 defeat,
  scoring/classification decoupling, P4 reclassification fixes, Caesar/salt
  lesson); enacted amendments A1–A7 (2026-09-27).
