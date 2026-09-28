# PROTOCOL — Independent Red-Team Battery (battery-author side)

The learner harness must never read `expected.json` or the `## SEALED`
section at the end of this file. Everything above that section is safe for
the harness author: it describes process, not answers.

## Seed

`20260921`. Every random choice in `gen_indep.py` flows from
`random.Random(20260921)` — the teach-order shuffle and the provenance-id
sample. No other RNG is used. Determinism was verified by running the
generator twice and byte-diffing both outputs (`items.jsonl`,
`expected.json` identical).

## Domain

**The Virellian Exchange** — a fictional federation of canal-harbor cities,
invented for this battery. Nothing in it is drawn from prior program
vocabulary.

- Classes (single lowercase tokens): `broker`, `courier`, `pilot`, `weigher`.
- 12 named members, 3 per class: Maren, Tavin, Sarella (brokers); Borin,
  Kessa, Dralin (couriers); Ossian, Petra, Halvar (pilots); Ysolde, Corvin,
  Nessia (weighers).
- 6 further names (Zevran, Mirella, Osric, Fenwick, Liora, Tammas) appear
  only in abstain probes and never in the teach phase.
- Verbs: `insures`, `exports`, `ferries`, `carries`, `steers`, `weighs`,
  `calibrates`. Goods: copper bonds, sealed letters, river barges, grain
  sacks, salt, spice bundles, harbor skiffs, cedar planks, dried figs,
  lantern oil, brass scales, tide gauges, and the four forbidden goods named
  in the D4 principles.

## Generation steps

1. Fixed tables: 8 principles (4× D3 universal, 4× D4 exclusion, one per
   class×verb with no class×verb governed twice), 12 D2 memberships, 28 D1
   fact specifications each carrying a private truth flag (a sealed fraction
   are false; see SEALED).
2. Private ground-truth model: exactly one true object per (name, verb);
   a D3 fixes the object for every member of that class×verb; a D4 forbids
   one object for that class×verb. Corrupt teach items are recorded false
   per teach id. Smooth lies are backed by untaught true objects so
   the generator's verdicts are principled rather than hand-written.
3. Teach phase assembled (48 items), order shuffled with the seeded RNG,
   ids assigned 0–47.
4. Probes built per capability from fixed tables (ids 100–171), each one's
   expected verdict asserted against the ground-truth model before writing —
   no hand-written answer keys.
5. Outputs written: `items.jsonl` carries only `id`/`phase`/`text`;
   `expected.json` carries the sealed capability/verdict/detail key.

## Counts

- Teach (ids 0–47): 8 principles (4 D3, 4 D4) · 12 D2 memberships · 28 D1 facts.
- Probes (ids 100–171), 12 per capability:
  - `contra` — 12 × Q3: 4 principle-mediated conflicts (cross-name pairs
    whose clash is visible only through a taught D3 plus taught
    memberships) + 8 surface-identical conflicts (same name+verb, different
    objects).
  - `false` — 12 × Q1: 6 D3-violations + 6 D4-violations, each via a taught D2.
  - `para` — 12 (6 × Q1, 6 × Q2): genuine rewordings of true taught D1s —
    verb synonyms, adjective insertion, determiner changes, phrase
    reordering, passive alternation. The Name token is always present in Q1
    inners; every Q2 answer is the unique name matching (class, verb, object).
  - `truth` — 12 × Q1: one probe per corrupted D1 (expected REJECT) plus an
    equal number of true claims (expected AFFIRM). One of the AFFIRM probes
    is a novel composition: a claim entailed by chaining a taught D2 through
    a taught D3 that was never stated outright as a D1.
  - `abstain` — 12 (9 × Q1, 3 × Q2): 6 never-taught names, 3 novel verbs,
    3 class+verb pairs with no taught match and no governing principle.
  - `prov` — 12 × Q4: true taught D1s quoted in canonical form, answered
    with the teaching act's id (seeded sample of the true D1s).

## Ground-truth semantics (for the scorer)

- Each (name, verb) has exactly one true object; two claims sharing a
  name+verb with different objects cannot both be true.
- `Every <class> <verb> <words>.` ⇒ every member of the class verbs exactly
  those words. `No <class> <verb> <words>.` ⇒ no member verbs those words.
- Expected verdicts were derived from this model programmatically during
  generation; `expected.json` is its serialization, not a separate document.

## Validation performed by the generator

- Wire format on every line: ASCII only, no `"`, single spaces, ≤240 chars,
  strict shape regex per declared shape; ids unique; teach ids 0–47, probe
  ids 100–171; probe texts unique.
- Every Q4 cites an existing true-D1 teach id whose text matches the quoted
  clause exactly (minus the period).
- Every `false` probe's inner evaluates FALSE specifically via a taught
  principle plus a taught D2 membership.
- Every `contra` pair's conflict is derived from the ground-truth model, with
  the required reason recorded per pair (`surface` for 8, `d3-mediated` —
  and not `surface` — for 4).
- Every `para` probe's source is a true taught D1; every Q2 `para` answer is
  the unique matching name.
- Every `truth` probe's verdict matches ground truth; the REJECT set equals
  exactly the corrupted D1 set; the chaining probe's claim is entailed but
  absent from teach.
- Every `abstain` probe is unanswerable by construction (unknown name, novel
  verb, or class+verb with no taught match and no governing principle).

## SEALED — do not read before scoring

Corruption rate: **6 of the 28 D1 facts are FALSE (21.4%)**, within the
preregistered 20–35% band.

Kind breakdown (2 of each):
- (a) principle-violations: `Borin carries open coin.` (violates D4
  `No courier carries open coin.`), `Ossian steers harbor skiffs.`
  (violates D3 `Every pilot steers river barges.`).
- (b) inter-claim contradictions: `Maren exports dried figs.` (taught true:
  `Maren exports salt.`), `Petra ferries grain sacks.` (taught true:
  `Petra ferries sealed letters.`).
- (c) smooth lies (violate nothing, contradict nothing taught):
  `Kessa weighs iron weights.`, `Nessia exports cedar planks.`

Corrupt teach ids (post-shuffle): 2, 4, 6, 36, 39, 43.
