# F1-COMPARE — family preregistration (frozen before implementation)

Date: 2026-09-23. Family: comparison-as-answer (round-2 turns 3, 4, 7).
Parent prereg: `dialogue/round2_repair/REPAIR_PREREG.md` (kill bars 1–6 apply).
Work dir: `dialogue/round2_repair/f1_compare/` (own fork of dialogue.zag + kb.txt + gaz.txt).
Canonical `dialogue/` tree is FROZEN — no edits.

## 1. What is broken (from ROOT_CAUSES.md)

Comparison machinery exists in `do_compose()` but is padlocked behind exact string
prefixes: `"was the author of…before…"` → yes/no, `"which is taller"` → "X is taller."
Turn 3 ("was he born before the eiffel tower was built?") misses the first prefix and
falls to Jaccard → emits one date. Turns 4 ("who was born first, darwin or melville?")
and 7 ("which of those two was built first?") match no template → Jaccard tie → lower
fid → one date, no comparison. "Those two" is never resolved (pronoun binder covers
only he/him/his/she/her/it/its/they/them; `pv` stores one entity).

## 2. Repair design (general, frozen here)

Replace the two frozen comparison branches in `do_compose()` with one general
comparison engine. The `did…write` → yes/no and `birth year` branches are NOT
comparisons and stay byte-identical in behavior.

**2a. Intent detection (no string prefixes).** A turn is a comparison iff it contains
at least one comparison word ANYWHERE in the turn (single words, grammatical class —
not multi-word phrasings):
`taller, shorter, tallest, shortest, before, after, earlier, later, first, last,
older, younger, oldest, youngest`.

**2b. Entity resolution (two entities).**
1. Run the existing `build_resolved()` (pronoun → name substitution via the salience
   stack) on the turn, then `gaz_scan()` the resolved text; dedupe; take the first two
   distinct entities in position order (e1, e2).
2. `"author of <work>"`: if the turn contains "author of", the subject slot (e1) is
   `author_of(work)` for the work named after "author of"; e2 is the first scanned
   entity that is neither that work nor the author. (This subsumes the old
   "was the author of" branch with identical yes/no outputs.)
3. Pair anaphora: if fewer than two entities resolve AND the turn contains one of
   `those two, these two, the two, either`, resolve to the last compared pair stored
   at `pv+32/pv+36` (new; `pv` currently uses 0..28, buffer is 64 bytes).
If still fewer than two entities, the engine declines (returns 0 → falls through to
retrieval; F1 adds no decline path — that is F2's family).

**2c. Value extraction (data-driven, entity-type-agnostic).**
- Dimension TALL if the turn contains `taller/shorter/tallest/shortest`; else TIME.
- TALL: value = `year_of(eid, "tall")` (existing helper reused for heights).
- TIME: value = first hit of the ordered marker list
  `" born ", " built ", " published ", " completed ", " dedicated ", " opened "`
  via the existing `year_of()` — the marker order is fixed and KB-shape-driven, not
  phrasing-driven, so it works for any entity (persons → born; towers → built;
  colosseum → completed; statue of liberty → dedicated; louvre → opened).
- If either value is missing (<0), the engine declines (returns 0).

**2d. Answer.**
- Shape: yes/no iff the turn begins with an auxiliary verb
  (`was/is/are/were/did/do/does/has/have/can/could/would/will`); otherwise name the winner.
- Direction: min-wins for `before/earlier/first/older/oldest/shorter/shortest`;
  max-wins for `after/later/last/younger/youngest/taller/tallest`.
  Yes/no: "yes." iff (v1<v2 for min-words) or (v1>v2 for max-words).
- Winner response: `[the ]<name> <verb> <dir>.` where `<verb>` comes from the marker
  that yielded the winner's value (`born→was born, built→was built,
  published→was published, completed→was completed, dedicated→was dedicated,
  opened→was opened, tall→is`) and `<dir>` is `first` (min, TIME), `last` (max, TIME),
  or the echoed `taller/shorter` (TALL). The existing "the "-prefix name list
  (eiffel tower, montparnasse tower, statue of liberty, louvre, colosseum) is reused
  unchanged, so round-1 taller outputs stay byte-identical.
- Ties: yes/no → "no." for min-words ("before" is strict); winner → first entity
  (deterministic). Documented, not probed.

**2e. Pair memory.** After every successful comparison, store (e1, e2) at pv+32/36.
Non-comparison turns never touch these slots, so "those two" survives intervening
turns (turn 7's pair comes from turn 5's comparison even with turn 6 between).
`pv` slots are initialized to −1 at each DIALOGUE reset.

## 3. Scaffold set (development guidance — NOT the release test)

Round-2 turns 3/4/7 verbatim, plus dev paraphrases:
- S1 `was the author of the martian born before the eiffel tower was built?` → `no.`
  (old-template coverage: weir 1972 vs eiffel 1889)
- S2 `which is shorter, the eiffel tower or the montparnasse tower?`
  → `the montparnasse tower is shorter.`
- S3 `was andy weir born after the eiffel tower was built?` → `yes.` (1972 > 1889)
- S4 `who was born first, charles darwin or jane austen?`
  → `jane austen was born first.` (1775 < 1809)
- S5 two-turn: `which is taller, the statue of liberty or big ben?`
  → `big ben is taller.` then `which of those two is shorter?`
  → `the statue of liberty is shorter.` (anaphora + pair persistence)

## 4. Held-out set (FROZEN — never used in development, release test only)

Each is its own DIALOGUE block (fresh state) unless noted. Entities/markers are all
in the frozen KB; none of these phrasings appear in §3 or in the round-1/round-2
batteries.

- H1 `was jane austen born before herman melville?` → `yes.` (1775 < 1819)
- H2 `who was born earlier, marie curie or andy weir?`
  → `marie curie was born first.` (1867 < 1972)
- H3 `which was built later, the eiffel tower or the montparnasse tower?`
  → `the montparnasse tower was built last.` (1973 > 1889)
- H4 `was the statue of liberty dedicated before the eiffel tower was built?`
  → `yes.` (1886 < 1889; tests the `dedicated` marker + mixed markers)
- H5 `who is older, jane austen or charles darwin?`
  → `jane austen was born first.` (1775 < 1809)
- H6 two-turn anaphora: `which is taller, the statue of liberty or big ben?`
  → `big ben is taller.` then `which of these two was built first?`
  → `the statue of liberty was built first.`
  (dedicated 1886 < big ben: big ben has NO built/dedicated year — only "is 96 meters
  tall" and "is a landmark in London". TIME value for big ben: born→−1, built→−1,
  published→−1, completed→−1, dedicated→−1, opened→−1 → missing → engine declines →
  falls to retrieval. EXPECTED: engine declines; the turn is scored as decline-correct
  only if no comparison is emitted. See note §6.)
- H7 `was the colosseum completed before the louvre opened?`
  → `yes.` (80 < 1793; tests `completed`/`opened` markers)

**Release bar: ≥6/7 held-out probes correct** (H6 counts as correct iff the engine
declines the comparison, i.e. emits no comparison-shaped answer — the honest
behavior when a value is missing).

## 5. Kill bars (family-specific)

1. **Acquisition:** turns 3, 4, 7 produce exactly:
   - T3 `was he born before the eiffel tower was built?` → `no.`
   - T4 `who was born first, darwin or melville?` → `charles darwin was born first.`
   - T7 `which of those two was built first?` → `the eiffel tower was built first.`
2. **Release:** held-out §4 ≥6/7 with the scaffold gone. A branch keyed on any
   multi-word literal from §3/§4 = FAIL by definition.
3. **No regressions:** the 5 good round-2 turns (1, 2, 5, 10, 12) still produce their
   recorded-good outputs; full round-1 battery (`dialogue/battery.txt`) — no section
   may drop below baseline (baseline, pinned toolchain, unmodified source:
   FOLLOWUP 45/45, CORRECTION 45/45, REFERENT 60/60, WEIRD 30/30, WEIRD_CLEAN 30/30,
   TOPIC 60/60, CONTRADICT 72/72, COMPOSE 28/28; 370/370 total, 0 FAIL).
4. **Determinism:** two full runs byte-identical (sha256 of outputs equal); zero RNG
   (program contains no RNG machinery — verified by inspection).
5. **No gaming:** no per-phrasing branches, no per-entity special cases, no
   probe-tuned constants. Allowed: the single-word comparison-word list (§2a, a
   grammatical class), the fixed marker list (§2c, KB-shape-driven), the aux-verb
   shape test (§2d).

## 6. Known edge documented in advance

H6 turn 2 is deliberately unanswerable as a TIME comparison (Big Ben has no year
fact). The specified behavior is engine-decline → retrieval fallback (whatever it
emits, it must not be a comparison-shaped answer). This is not F2's decline path —
it is the comparison engine refusing to compare without two values.

## 7. Deliverables

- This file (frozen).
- Repaired `dialogue.zag` fork + build notes (pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- `HELDOUT.md` + run logs (scaffold vs released results).
- `VERDICT.md`: PASS/FAIL per bar, plain language.
- All committed under `dialogue/round2_repair/f1_compare/`.
