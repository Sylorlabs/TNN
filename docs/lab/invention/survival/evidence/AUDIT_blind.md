# Blind Auditor Report — Experiment 1 (Invent-to-Survive)
**Auditor:** blind-auditor subagent · **Date:** 2026-09-26 PDT
**Frozen prereg:** `tnn-lab/docs/lab/invention/survival/PREREG.md` (§2, §8 read first, as required)

## Blinding declaration

- **Cuing audit (Audit 2)** was performed FIRST, using only: `kb/kb.txt`, prereg §3/§5, and the goal statement "Survive as long as possible". I did not open `runs/`, `evidence/A2_ablation.md`, `evidence/BAR_RESULTS.md`, `evidence/EVIDENCE.md`, or any agent source. The independently derived strategy (section 3 below) was written from the materials alone.
- **Novelty audit (Audit 1)** used only `evidence/A1_sketches.md` + `kb/kb.txt` (plus a programmatic text search of kb.txt).
- I did not read any results TSVs, ablations, or verdicts. I did see the A1 file's own summary of the outcome *within the sketches file itself* (it reports no coherent novel strategy was found) — that content is part of the assigned audit material, not a separate results file. No accidental exposure beyond the assigned files occurred.

---

## 1. Novelty audit (§8) — step table

**Finding: there are no strategy-sketch steps to audit.** The implementer's A1
extraction (§7 method: extract a sketch for each variant where I beats R by
≥60) reports that I-survive/I-invent execute **no coherent novel strategy**:

> "examination of the traces reveals that I does NOT execute a coherent novel
> survival strategy" — A1_sketches.md

I's behavior decomposes into three components, each of which I checked against
kb.txt:

| # | Observed behavior component (A1) | Composed step claimed? | kb.txt status | Evidence |
|---|---|---|---|---|
| 1 | Safety layer: flees storms, forages when E<40, avoids void | No — this is the taught baseline, not a novelty claim | **Present (taught, verbatim heuristics)** | kb: "If a storm starts within 20 ticks and you are in the storm zone, leave the zone." · "If E<40 and a mote is within 3 cells, move toward the nearest mote." · "Do not enter a void cell." |
| 2 | Systematic exploration: tries 1-step, then 2-step, then 3-step actions driven by novelty bonus (trace is "lexicographic enumeration… NOT a strategy") | No — explicitly characterized as exploration, not a composed plan | **N/A — no composition claimed; and nothing resembling it is in kb** | kb contains no enumeration/exploration procedure at all (grep for "strateg|plan|sketch" hits only the disclaimer lines) |
| 3 | Occasional LAMP built (v00, v04, v07, v10), kept in inventory or dropped without benefit; **no WARD built on any variant** | No — an unused byproduct, not a working strategy step | **N/A — and the item names do not exist in kb** | grep for `ward|lamp|surge|beacon|plank` in kb.txt: zero hits |

Because A1 claims **zero novel compositional steps**, K4's trigger condition
("novelty audit finds key strategy steps in the training mass") is vacuous:
there is no claimed novelty to falsify. The single candidate for "invention"
(the exploration loop, component 2) is:

- **Absent from kb.txt** (clean — see §2 below), but
- **Not a working strategy** by the prereg's own §2 definition: invention
  requires "composing discovered/known elements into a novel *working*
  strategy", and A1 reports I "explores without converging on one". Exploration
  is explicitly classified by §2 as *not* invention ("discovering what COMBINE
  pairs yield… is exploration").

**Novelty audit conclusion:** nothing to strike down, because nothing novel was
claimed. K4 cannot fire on an empty claim set — but equally, H1's positive
requirement (a novel *working* strategy) is not evidenced by A1.

---

## 2. kb.txt cleanliness verdict — CLEAN

Full read of the 40-line committed training mass + programmatic grep. Verdict:
**no recipe table, no multi-step plans, no strategy sketches, no item names.**

- Recipes: kb line 19 — "The recipe table is hidden; you must discover what
  combinations yield by trying." Line 2 header: "The recipe table is NOT
  included." No recipe appears anywhere (grep `recipe` hits only these
  disclaimer lines).
- Item names: zero hits for `ward|lamp|surge|beacon|plank`.
- Plans/sketches: section header line 28 — "Single-step heuristics
  (condition -> action ONLY; no multi-step plans)"; lines 38–40 ("NOT taught")
  explicitly disclaim "The COMBINE recipe table", "Any multi-step plan,
  strategy, or strategy sketch", "Any specific survival strategy". No
  first-then / step-1 / build-order language anywhere (grep: no hits).
- All five heuristics are genuine single-step condition→action rules.

**One yellow flag (cuing-adjacent, not a violation):** line 22 — "being in the
zone without shelter costs 4 E per tick." The word **"shelter"** presupposes a
shelter concept exists in the world. Combined with line 24 ("some built items
can be DROPPED onto a cell where they have effects") and the COMBINE heuristic
("if two items are in inventory and you are safe, you may try COMBINE"), this
orients a competent reasoner toward *seeking a storm-shelter item* rather than
only fleeing. It does not name any recipe, item, effect, build order, or
placement — so it is discovery scaffolding, not a strategy leak. Flagged for
the record, not a cleanliness failure.

---

## 3. Cuing audit (§8) — independently derived best strategy from materials alone

Derived from kb.txt + prereg §3/§5 (world rules as taught) + goal "Survive as
long as possible", with no knowledge of any agent's behavior and no sim access.
Presented in concrete action terms, as a competent reasoner would derive it:

**Threat accounting.** Basal drain is 1 E/tick (600 E over the run, affordable
from a 100-E start only with feeding). Motes give +30 E (near) / +40 E (deep).
Storms are the dominant threat: 3 windows × ~30 ticks at −4 E/tick = up to
~360 E of exposure if caught in the zone (cells 6..17) — far larger than any
other loss term, and the schedule is taught, so storms are plannable.

**Derived strategy:**

1. **Early game (before first storm minus 20 ticks):** Forage near-side motes
   (EAT on mote cells, +30 E); TAKE crystals when passing their cells
   (inventory cap 4; crystals are the only TAKE-able items and are inert, so
   their only taught purpose is as COMBINE inputs). Build an energy buffer
   toward the 200 cap.
2. **Discovery phase (only when safe — no storm within 20 ticks, E
   comfortable):** Systematically try COMBINE on pairs — crystal+crystal first
   (4 crystals available), then crystal+product for any product obtained
   (the kb says COMBINE "takes two inventory items and yields something";
   products land in inventory, so recombining them is the natural extension).
   This is directly cued: "if two items are in inventory and you are safe,
   you may try COMBINE" + "you must discover what combinations yield by
   trying."
3. **Placement testing:** DROP each product on a cell and observe — cued by
   "some built items can be DROPPED onto a cell where they have effects. An
   item in your inventory does nothing; it must be placed." The priority test
   target is storm protection, because the kb's storm rule names "shelter"
   as the condition that negates −4 E/tick.
4. **Storm response (the strategic fork):** (a) If a shelter item is
   discovered and its protection verified: ~20 ticks before each taught
   storm window, move to the item's cell and WAIT through the window, then
   resume foraging — a build → pre-position → wait composition. (b) If no
   shelter is found: fall back to the taught heuristic — leave the zone when
   a storm starts within 20 ticks.
5. **Void:** never enter; kb teaches "Do not enter a void cell" and entry is
   death. The +40 E deep motes are not worth an unquantified lethal risk
   (death ends the run; no taught safe-crossing mechanism exists). A
   competent reasoner tests void-crossing only if a placed item's observed
   effect plausibly enables it — otherwise avoids entirely.
6. **Ongoing:** keep E above a pre-storm buffer; use the taught E<40 → seek
   nearest mote rule; exploit the taught respawn mechanic ("dormant for 20
   ticks, then respawns at a fixed per-mote cell" + full observability) by
   returning to known respawn cells.

**Does this match the world's effective strategy?** The implementer's context
notes the world collapsed to a ward-based turtle (a placed shelter with no
basal cost and storm immunity, built from crystals). My derivation reaches the
**same compositional template** — COMBINE → place → pre-position before the
taught storm windows → WAIT out the storm — because the kb's "without shelter"
word plus the place/COMBINE mechanics point a competent reasoner at exactly
this shape.

**But the template is not the solution.** What the kb does NOT determine, and
what no competent reasoner could derive without experimenting in the world:

- That a shelter item exists at all (the kb only presupposes the *concept*);
- Which recipe produces it (crystal+crystal vs. anything else);
- Its exact effects (storm immunity AND zero basal cost — neither is stated);
- How many crystals to commit (scarcity tradeoff — the kb doesn't even state
  the scarcity requirement; "4 crystals" is given but not "you can't build
  everything");
- Where to place it and the pre-storm timing details.

The winning *instantiation* must be discovered by trial in the world; the kb
supplies only the discovery loop and the storm-priority orientation. Under the
prereg's own §2 taxonomy this is the intended exploration→composition path,
not experimenter cuing.

**Critical caveat on prereg §3:** The task permitted me to read §3, and §3 —
the *implementer's requirements*, not agent-facing material — contains a
verbatim answer key: "crystal+crystal→WARD (placed; shelter cell — no basal
cost, storm-immune)" plus named strategy sketches ("ward turtling",
"lamp-farming", "surge-gambling", "void-crossing for deep motes"). Had any
agent seen §3, cuing would be total. Per §5, the recipe table was explicitly
NOT taught and "never in the training mass", and the committed kb.txt I
verified contains no trace of §3's recipes or strategy names. **My K5 judgment
is therefore on the agent-facing materials only (kb + taught world physics +
goal).** If the coordinator intends §3 as in-scope "materials", K5 would fire
trivially — but that would be a category error, since §3 was never given to
the agents. I flag as an open check for the coordinator (outside my blinding
scope — I did not inspect agent source, runner prompts, or executor code):
verify no §3 content (recipe examples, strategy-sketch examples) leaked into
any agent-facing channel.

---

## 4. Kill-bar recommendations

### K4 — not novel → **NOT FIRED** (vacuously; with a substantive note)

- The novelty audit found **no key strategy steps in the training mass**
  because **no coherent novel strategy was claimed** — A1 reports I's behavior
  is exploration (systematic 1-/2-/3-step enumeration driven by the novelty
  bonus), not a composed working strategy, and no WARD was ever built.
- kb.txt is verified clean (no recipes, no plans, no item names).
- Substantive note for the record: K4 not firing here is not a vindication of
  H1. The §2 definition of genuine invention requires a *working* strategy;
  A1 explicitly concludes the deliberation machinery "does NOT produce genuine
  invention in this world." K4 tests whether claimed novelty is real; with an
  empty claim set it cannot fire — but H1's positive burden is likewise unmet
  by A1. (Whether K1/K6 fire is outside this audit's scope.)

### K5 — cuing → **NOT FIRED**

- The agent-facing materials (committed kb.txt + taught world physics + goal
  "Survive as long as possible") do **not** determine or strongly suggest the
  specific winning strategy. A competent reasoner derives a shelter-seeking
  *template* (explore COMBINE → place products → test for storm protection →
  pre-position and wait), but the recipe, item effects (storm immunity, zero
  basal cost), build order under scarcity, and placement are not derivable
  without world experimentation — which is the intended discovery loop, not
  cuing.
- The most cuing-adjacent element in the kb is the word "shelter" in the taught
  storm rule; it orients search toward shelter-seeking but hands over no
  solution. Not a K5 trigger.
- **Warning:** prereg §3 (implementer-facing) contains the explicit answer key
  (WARD recipe + effects + named "ward turtling" sketch). K5's validity rests
  on §3 never reaching the agents — the committed kb.txt confirms it didn't,
  but I recommend the coordinator independently verify no §3 content leaked via
  agent source, prompts, or executor code (channels I was blinded from).

---

## Files

- This report: `~/workspace/invent_survive_audit/AUDIT_REPORT.md` (workdir only; nothing written to the repo; nothing committed).
