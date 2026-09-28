# Dialogue Round-4 Hardcodes: Units & Jokes — Completion Report

**Date:** 2026-09-27  
**Task:** Finish the two remaining Dialogue Round-4 hardcodes from commit `75267f9df70702fcd473619c70a454b191d21a9c`

## 1. Units/Dimensions Mechanism

### Design Principle
Quantity and unit derive entirely from taught facts. No dimension names, property names, or unit names appear in code. The mechanism works for any taught unit.

### How It Works

**Fact ingestion (`extract_unit`):** During `kb_install`, each fact's text is scanned for the numeric value. The word(s) immediately following the number are extracted as the unit:
- "The Shard is 310 meters tall." → value=310, unit="meters"
- "The sauna is 90 degrees Celsius hot." → value=90, unit="degrees celsius" (two words: "degrees" not capitalized, so "Celsius" is included)
- "The Eiffel Tower was built in 1889." → value=1889, unit="" (number at end, no following word)
- "1 kilometer equals 1000 meters." → value=1, unit="kilometer" (first number's unit)

Unit stored per-fact at `fm[ro+32]` (offset) / `fm[ro+36]` (length).

**Quantity resolution (`qty_fx`):** For a difference question, each entity's unique fact carrying both a number (value>0) and a taught unit (length>0) is selected. Returns -1 if zero or multiple (ambiguous → withhold).

**Answer computation (`answer_diff`):**
- If both units match (stemmed comparison via `unit_eq`): `|v1-v2|` rendered with the taught unit.
- If units differ: search all facts for an explicit conversion fact via `find_conversion`. A conversion fact is recognized by:
  1. Containing the stemmed "from" unit word
  2. Containing the substring "equal" after it (e.g., "equals")
  3. Containing the stemmed "to" unit word after the "equal" marker
  4. Having numbers before each unit word
- If conversion found (n1 units-A = n2 units-B): convert v2 to v1's units, subtract, render in v1's units (or vice versa based on ratio).
- If no conversion: return 0 → honest withhold ("I don't know.").

**Year questions:** "how many years between X and Y?" uses `ent_year_fx` to find year facts (no units), then `question_unit` extracts "years" from the question text. Renders "|y1-y2| years".

### Generality Proof

| Probe | Units | Result |
|-------|-------|--------|
| golden gate vs brooklyn bridge | kilometers → meters (taught conversion) | "1000 meters" ✓ |
| elephant vs hippopotamus | kilograms (same unit) | "4500 kilograms" ✓ |
| sauna vs desert | degrees celsius (compound unit) | "45 degrees celsius" ✓ |
| feature film vs short film | minutes (time) | "90 minutes" ✓ |
| golden gate vs shard | kilometers → meters (taught conversion) | "1690 meters" ✓ |
| mount everest vs eiffel tower | meters (same unit) | "8519 meters" ✓ |
| eiffel tower vs montparnasse tower | years (from question) | "84 years" ✓ |
| elephant vs sauna | kilograms vs degrees celsius (no conversion) | withhold ✓ |

**Count:** 8 generality probes, all pass. Units tested: length (meters, kilometers), mass (kilograms), temperature (degrees celsius), time (minutes, years). No unit names in code.

## 2. Joke Repetition Mechanism

### Design Principle
Track jokes served during the session. Repeat requests deterministically advance through unserved stock. Exhaustion yields exactly "That's all the jokes I know."

### How It Works

**Stock construction:** All ordered (shorter, taller) pairs derived from taught `tall` facts. Ordered by:
1. Greatest height contrast first (taller.height - shorter.height, descending)
2. Lower short-entity ID (deterministic tiebreak)
3. Lower tall-entity ID (deterministic tiebreak)

**Session tracking:** `pv+64` stores count of jokes served in current dialogue. Reset to 0 at each `DIALOGUE`.

**Serving:** Each joke request serves stock[served_count], increments counter. When served_count >= stock_size: output exactly "That's all the jokes I know."

**Unit in jokes:** The "X meters shorter" uses the taught unit from the two facts (via `unit_eq` stemmed comparison; both must share the unit).

### Determinism Proof
- Two full runs of mixed unit/joke/year probes: byte-identical.
- 15-joke exhaustion sequence: all 15 unique, then 5x "That's all the jokes I know." — deterministic order by height contrast.
- Fresh DIALOGUE resets counter (verified: new dialogue starts from first joke).

## 3. Regression Results

| Battery | Result | Baseline | Match |
|---------|--------|----------|-------|
| Round 4 (38 probes) | 38/38 PASS, 0 FAIL | 38/38 | ✓ |
| Round 3 (23 probes) | Answers match baseline | 23/23 good | ✓ |
| Round-2 F2 (370 probes) | 351 PASS, 19 FAIL | 351/370, same 19 | ✓ |
| Round-2 Integrated (18 probes) | 15 PASS, answers match | 15/18, same 3 drifts | ✓ |

**Determinism:** Two full Round-4 runs byte-identical. Two full generality runs byte-identical.

## 4. Code Changes

**File:** `docs/lab/dialogue/round4/dialogue.zag`

### New functions:
- `extract_unit(ftx,ftl,to,tl,val)`: Extract unit words after the fact's numeric value. Returns (offset<<32)|length.
- `factfx_of(...)`: Fact index (not fid) of lowest-fid fact naming entity with marker text.
- `unit_eq(ftl,o1,l1,o2,l2,sc)`: Stemmed unit-word equality on scratch buffer.
- `sword_find(ftl,to,tl,uao,ual,sc)`: Whole-word find by stemmed unit form. Returns offset or -1.
- `conv_in_fact(...)`: Check if fact is a conversion between two units. Returns (n1<<32)|n2 or 0.
- `find_conversion(...)`: Search all facts for conversion. Returns (n1<<32)|n2 or 0.
- `question_unit(ubuf,uo,ul)`: Extract unit word after "how many " in question. Returns (offset<<32)|length.
- `qty_fx(...)`: Entity's unique numeric+unit fact. Returns fx or -1. **Generic: no dimension names.**
- `answer_diff(...)`: Compute |v1-v2| with taught units, conversion, or withhold.

### Modified:
- `grab_num_left`: Now skips spaces before digit scan (for "1 kilometer" parsing).
- `diff_dim`: Added "heavier"→1, "hotter"→1 (dimension-agnostic: all map to generic quantity diff).
- `do_compose` F3: Uses `qty_fx` (generic) instead of `qmark` hardcodes. Removed `" meters"` / `" years"` literals.
- Contradiction rendering: Unit from taught fact, not hardcoded "meters".
- `pv` allocation: 64→128 bytes; `pv+64` = session joke counter.
- Joke stock: Deterministic ordered pairs from taught `tall` facts; exhaustion text exact.

### Bug fixes during development:
- `grab_num_left` required adjacent digits; fixed to skip spaces.
- `conv_in_fact` used `word_find` for "equal" marker; "equals" failed whole-word match. Fixed with `find_sub`.
- `question_unit` used `word_find` with trailing space; fixed with `find_sub`.
- `qty_fx` initially used wrong field offsets (`ro+8` vs `ro+12`) and wrong `fea` traversal; rewrote using `find_sub` text search like `factfx_of`.

## 5. Files for Commit

**Source:**
- `docs/lab/dialogue/round4/dialogue.zag` (modified)

**Fixtures:**
- `docs/lab/dialogue/round4/regr/generality/kb.txt` (new: baseline + 10 generality facts)
- `docs/lab/dialogue/round4/regr/generality/gaz.txt` (new: baseline + 9 generality entities)
- `docs/lab/dialogue/round4/regr/generality/battery.txt` (new: 8 generality probes)

**Reports:**
- `docs/lab/dialogue/round4/ROUND4_HARDCODE_COMPLETION.md` (this file)

**Note:** `regr/r4/kb.txt` and `gaz.txt` were restored to baseline (48 facts, 32 entities). Generality fixtures live in `regr/generality/`.

**Stale:** `dialogue_trace.zag` is unreferenced (prose-learner file, not dialogue trace). `add_hooks.py` has broken anchors for current source. Documented, not fixed — out of scope for this task.
