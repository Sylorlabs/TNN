# PREREG_F3 — F3-ARITHMETIC guided-release repair (FROZEN 2026-09-23)

Family: F3-ARITHMETIC (round-2 repair program, see `../REPAIR_PREREG.md`).
Crew task: repair the round-2 turn-6 failure by guided release.
Status: FROZEN. Written before any implementation. Any change needs Micah's re-approval.

## 1. The failure (from `../ROOT_CAUSES.md`)

Round-2 turn 6: after "which is taller, the eiffel tower or the montparnasse tower?"
→ "the eiffel tower is taller.", the user asked "how much taller is it?" and TNN
emitted "The Eiffel Tower is in Paris." Correct answer: 120 (330−210).

Verified root causes (mechanistic):
1. **No arithmetic exists** anywhere in the 1917 lines — only `<`/`>` value
   comparisons inside `do_compose`. There is no subtraction, addition, or any
   numeric combination of two KB values.
2. **No cross-turn value passing**: the comparison in turn 5 computes 330 vs 210
   and discards both; turn 6 has no way to reach back.
3. **Morphology gap**: "taller" does not stem to "tall" (no "-er" rule; the
   morphology crew deliberately left comparative bridging out), so even the
   height facts score poorly on the question ("The Eiffel Tower is in Paris."
   2/4 beats "The Eiffel Tower is 330 meters tall." 2/5).

## 2. The capability being repaired (not a turn-6 hack)

**"Answer how-much-difference questions from KB values."**

A general difference engine, not a turn-6 branch:
- Detects difference questions by shape, not by exact phrasing:
  `how much taller/older …`, `how many years between …`, `what is the difference
  in height/years between …` (open list, same shapes, any entity pair).
- Resolves the entity pair two ways: **explicit** ("…the statue of liberty than
  big ben?") or **follow-up** ("how much taller is it?" — the pair is carried
  from the immediately preceding comparison turn, the same discourse job the
  existing pronoun binder does for "it").
- Looks up each entity's value for the asked dimension **live from the KB**
  (height via the "tall" marker, years via event markers: born/built/published/
  dedicated/opened/completed/won), subtracts, emits the number.
- Anything it cannot resolve (missing values, no pair, no comparison context)
  falls through to the existing pipeline — no new decline path is added here
  (withholding is F2's family).

## 3. Repair design (frozen)

### 3a. Subtraction + difference branch in `do_compose`

A new general branch placed after the "which is taller" branch:

- **Trigger** (raw lowercased input, substring tests): `how much taller`,
  `how much older`, `how many years between`, `difference in height`,
  `difference in years`, or (`how much` AND a comparative adjective
  in {taller, older, longer, bigger, smaller}).
- **Pair resolution**:
  - ≥2 distinct gazetteer entities in the question → first two (position order).
  - 1 explicit entity E + a stored comparison pair (A,B) from the immediately
    preceding turn + E ∈ {A,B} → (E, the other).
  - 0 explicit entities (e.g. pronoun "it") + a stored comparison pair from the
    immediately preceding turn → the stored pair.
  - Otherwise the branch returns 0 (falls through; not this family's problem).
- **Value lookup** (live KB computation, never memorized answers):
  - height: the existing `year_of(…, "tall", 4)` helper (substring "tall"
    matches "tall"/"taller", same technique the existing taller-branch uses).
  - years: per-entity event marker — the event word (`born/built/published/
    dedicated/opened/opening/completed/won`) nearest that entity's name in the
    question selects ` born `/` built `/…; if the question names no event, the
    priority order born → built → published → dedicated → opened → completed
    → won is used, first marker with a KB fact wins.
  - Missing value for either entity → branch returns 0 (fall through).
- **Output**: `|v1 − v2|` emitted as a bare decimal number (absolute
  difference; "how much taller" is symmetric). Turn 6 → `120`.

### 3b. Cross-turn comparison context (the "carried" part)

`do_compose`'s existing "which is taller" branch records the compared pair
into new `pv` slots (entity ids + dimension + turn number). Values are NOT
stored — they are re-looked-up from the KB at difference time, so the answer
is computed, not recalled. The follow-up path requires the pair to come from
the immediately preceding turn (a stale pair from five turns ago is not a
legitimate referent for "it").

### 3c. Morphology: the principled comparative fix

The stemmer core stays frozen. A general "-er" suffix strip is **rejected**:
it would mangle load-bearing proper nouns ("tower"→"tow", "water"→"wat",
"author"→"autho"). Instead, a **closed-class comparative-adjective list** is
added to the existing `irregular_norm` (the morphology crew's own
inflectional-normalization site, running inside `proc_token` so KB-install
and query paths stay symmetric by construction):

  taller→tall, older→old, longer→long, bigger→big, smaller→small,
  earlier→early, later→late

Principled basis (documenting the boundary the task asked for):
- Comparative inflection (-er) is **inflectional morphology** — a closed
  grammatical paradigm, like the -ed/-s/-ies strips the stemmer already
  performs. It is NOT the derivational class the morphology crew fenced off
  (tall/height, high/tall — different lexemes; penned/wrote — synonyms).
- The FIX.md safety rule ("a morphology bridge is only safe where the merged
  forms never distinguish expected answers") holds: no battery or conversation
  turn distinguishes tall from taller in its expected answer — the only
  "taller" turns are the prefix-gated compose templates, which operate on raw
  text before stemming. Verified by the full-battery regression bar below.
- The dialogue layer additionally detects comparatives by raw substring
  ("tall" matches "tall"/"taller"), consistent with the existing "which is
  taller" branch's own technique.

## 4. Guided release procedure

1. **Guide (scaffold):** develop against the scaffold probes (§6) — turn 6 plus
   paraphrases with hints about which strategy each needs.
2. **Release:** remove all scaffold-only artifacts. The design in §3 contains
   no per-case branches, no per-pair constants, no scaffold-phrasing tests;
   the scaffold battery files live in `scaffold/` as dev logs only and are
   never consulted by the binary.
3. **Verify it stands:** the repaired fork is tested on the frozen held-out
   set (§5) — new phrasings and new entity pairs, never seen during
   development. Byte-identical reruns, zero RNG.

## 5. Held-out probes (FROZEN — written before implementation)

Run as DIALOGUE blocks; state resets per block. E lines are exact-match.

| id | conversation | expected A |
|----|--------------|------------|
| H1 | `which is taller, the eiffel tower or the montparnasse tower?` → `how much taller is it?` | `120` |
| H2 | `which is taller, big ben or the statue of liberty?` → `how much taller is it?` | `3` |
| H3 | (standalone) `how much taller is the statue of liberty than big ben?` | `3` |
| H4 | (standalone) `how many years between charles darwin and herman melville being born?` | `10` |
| H5 | (standalone) `how many years between the louvre opening and the eiffel tower being built?` | `96` |
| H6 | (standalone) `how much taller is mount everest than the eiffel tower?` | `8519` |
| H7 | (standalone) `what is the difference in height between the eiffel tower and the montparnasse tower?` | `120` |
| H8 | (standalone) `how much older is herman melville than charles darwin?` | `10` |

Ground truth: 330−210=120 (H1,H7); 96−93=3 (H2,H3); 1819−1809=10 (H4,H8);
1889−1793=96 (H5); 8849−330=8519 (H6). All values from the frozen kb.txt;
all entity pairs differ from the scaffold pairs.

## 6. Scaffold probes (development only, NOT the release bar)

| id | probe | hint |
|----|-------|------|
| S1 | turns 5→6 verbatim (`which is taller…` → `how much taller is it?`) | follow-up pair + subtraction → `120` |
| S2 | `which is taller, the eiffel tower or the montparnasse tower?` → `by how much is it taller?` | generic `how much`+comparative trigger → `120` |
| S3 | (standalone) `how much taller is the montparnasse tower than the eiffel tower?` | explicit pair, reversed order → `120` |
| S4 | (standalone) `how many years between herman melville and charles darwin being born?` | event marker `born` → `10` |
| S5 | (standalone) `what is the difference in height between big ben and the statue of liberty?` | difference-in-height shape → `3` |

## 7. Kill bars

1. **Acquisition:** H1 (turn-6 verbatim) → `120`.
2. **Release (anti-hardcode):** H2–H8 all correct. A per-case branch that only
   fires on scaffold phrasings = FAIL. The binary may not contain any of the
   held-out answers as constants.
3. **No gaming:** values are looked up from the KB at query time; the only
   cross-turn state is entity ids (discourse referents), never answers.
   H2/H3/H6 use pairs never present in any scaffold probe.
4. **No regressions:** the 5 good round-2 turns (1, 2, 5, 10, 12) keep their
   exact responses; the full round-1 battery (`battery.txt`, all 8 sections)
   keeps its scores — **no section may drop** vs the frozen baseline binary.
5. **Determinism:** two full runs byte-identical (cmp clean), zero RNG.
6. **Cleanroom:** all work in `dialogue/round2_repair/f3_arithmetic/`; the
   canonical `dialogue/` tree untouched (verified by sha256 of
   `dialogue/dialogue.zag` before/after).

## 8. Deliverables

- This file (frozen, committed before implementation).
- Repaired `dialogue.zag` fork + build notes (pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- `HELDOUT.md` (the §5 probes) + run logs (scaffold vs released).
- `VERDICT.md`: PASS/FAIL per bar, plain language.
- All committed under `dialogue/round2_repair/f3_arithmetic/`.

## 9. What is explicitly out of scope

- The decline path ("I don't know") — F2's family.
- Utterance-type routing, challenge defense, history read-back — F4/F5.
- Generalizing comparisons beyond height/years (no KB data supports more).
- Changing the frozen stemmer core or the derivational boundary.
