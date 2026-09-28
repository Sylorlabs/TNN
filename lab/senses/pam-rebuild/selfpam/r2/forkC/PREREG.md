# FORK C — SELF-PAM AS CONSISTENCY ENFORCER (DUAL CANONICAL FINGERPRINTS)
## Frozen fork prereg — H6 revival round 2

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Program prereg:** `docs/lab/senses/pam-rebuild/selfpam/r2/PREREG.md`
committed as `b3db7b7a` (binding; content verified byte-identical locally).
**Design source:** `museA_forks.md` Fork 2 (Muse-A proponent).
**Role in round 2:** the NEGATIVE CONTROL. Expected to exhibit the
theater signature (pass M1–M3, fail M4/M5). Built as well as possible —
the value of a negative control is proportional to its quality — and
measured honestly. If it passes M4/M5 against prediction, the wall
verdict reopens for round 3.

**Status:** FROZEN on commit. Amendments require the coordinator and are
committed alone.

---

## 0. Honest claim (no corroboration claim is made)

Fork C is a **consistency enforcer**: a frozen normalization pipeline
maps every draft claim to two canonical fingerprints (surface and
meaning); a draft installs iff every meaning-atom hash-matches a
committed store entry or a deliberation conclusion — exact equality
only. It claims *identity with committed state*, never evidence about
the world. It cannot detect falsehood, only unlicensed speech.

## 1. Controlled claim language (frozen)

ASCII only. The tokenizer lowercases; all tables are lowercase.
A draft is one sentence matching one of:

- **F1** `<ent> is <adj>` → atom `(ent, HAS_PROPERTY, adj)`
- **F2** `<ent> is a|an <class>` → atom `(ent, IS_A, class)`
- **F3** `<ent> <prep> <ent2>`, prep ∈ PREPS → `(ent, LOCATED_<PREP>, ent2)`
- **F4** `<ent> <verb> <ent2>`, verb ∈ VERBS → `(ent, REL, ent2)`
- **F5** passive `<ent> was|were|is|are <pastpart> by <ent2>` →
  `(ent2, REL, ent)` (voice normalization; active/passive collide)
- Negation: `not`/`never` immediately before the predicate slot, or
  leading `no` as subject quantifier, wraps the atom in NEG (`~`).
- Quantifiers `all|some|many|few|no` before the subject entity fold
  into the subject token as `q:<q>|<ent>`.
- Numbers (NUMS table, incl. `50 percent` merge) in any entity slot
  canonicalize to `n:<canon>` (e.g. `n:1/2`).
- Pronouns (PRONOUNS) resolve per §3 step 5; unresolved → UNPARSED.
- Anything not matching F1–F5 → the atom is `UNPARSED` → WITHHOLD.
- Entities are single tokens `[a-z][a-z0-9-]*` (multi-word entities
  unsupported — documented limitation; the battery avoids them).

## 2. Frozen tables (verbatim; the build embeds exactly these)

- **STOP** (stripped after passive detection): the, a, an, this, that,
  these, those, is, are, was, were, be, been, being, do, does, did,
  and, or, but, of, to, for, with, as, at
  (NOT stripped: prepositions in PREPS, not/never/no, quantifiers,
  pronouns, `by` — `by` is consumed by passive detection first.)
- **CONTRACTIONS**: dont→do not, doesnt→does not, didnt→did not,
  cant→can not, wont→will not, isnt→is not, arent→are not,
  wasnt→was not, werent→were not, hasnt→has not, havent→have not,
  couldnt→could not, shouldnt→should not
- **PREPS** (surface→relation): on→LOCATED_ON, under→LOCATED_UNDER,
  above→LOCATED_ABOVE, below→LOCATED_BELOW, in→LOCATED_IN,
  near→LOCATED_NEAR, beside→LOCATED_BESIDE, behind→LOCATED_BEHIND
- **VERBS** (surface→relation): has→HAS, owns→OWNS, possesses→OWNS,
  built→BUILT, constructed→BUILT, wrote→WROTE, authored→WROTE,
  contains→CONTAINS, painted→PAINTED, depicted→PAINTED, leads→LEADS,
  visited→VISITED, made→MADE, created→MADE
- **PASTPART** (surface→base relation for passive): built→BUILT,
  written→WROTE, painted→PAINTED, owned→OWNS, possessed→OWNS,
  contained→CONTAINS, made→MADE, created→MADE, constructed→BUILT,
  authored→WROTE, depicted→PAINTED, visited→VISITED, led→LEADS
- **ANTONYMS** (negation cancellation, bidirectional): unhappy↔happy,
  dead↔alive, hot↔cold, big↔small, fast↔slow, true↔false, open↔closed,
  empty↔full, light↔dark, early↔late, clean↔dirty, rich↔poor
- **ENTITY_SYN**: kitty→cat, puppy→dog, automobile→car, bike→bicycle,
  bunny→rabbit, sofa→couch, fridge→refrigerator, phone→telephone
- **NUMS**: one→1, two→2, three→3, four→4, five→5, six→6, seven→7,
  eight→8, nine→9, ten→10, eleven→11, twelve→12, half→1/2,
  quarter→1/4, dozen→12, 50%→1/2, 25%→1/4, 75%→3/4,
  "50 percent"→1/2, "25 percent"→1/4, "75 percent"→3/4
  (bare digit tokens pass through as their own canonical form)
- **PRONOUNS**: singular it, its, he, him, his, she, her;
  plural they, them, their
- **PLURALS**: frozen {cats, dogs, birds, rabbits, cars, boxes} plus
  heuristic: token ends in `s` → plural (documented heuristic;
  battery fixtures use unambiguous forms)
- **QUANTIFIERS**: all, some, many, few, no

## 3. Normalization pipeline (frozen order; deterministic; zero RNG)

1. Lowercase ASCII; tokenize on whitespace and `.,;:!?"()`; delete `'`.
2. Contraction expansion (CONTRACTIONS table).
3. Passive detection: `[ent] [was|were|is|are] [pastpart] by [ent]` →
   record swap, delete aux + `by`. (Runs before STOP-strip.)
4. STOP-strip.
5. Pronoun resolution: static ordered entity context = draft's own
   preceding entities, then the case's ENTCTX list in order. Singular
   pronoun → nearest preceding singular entity; plural → nearest
   preceding plural entity. None → UNPARSED.
6. `percent`-merge (`<num> percent` → one token), NUMS canonicalize,
   quantifier capture (`q:<q>|<ent>`), negation capture (`not`/`never`
   before predicate; leading `no` as quantifier).
7. ENTITY_SYN canonicalization.
8. Predicate canonicalization: PREPS / VERBS / is-patterns
   (F1 vs F2 by presence of a|an). Antonym-negation cancellation:
   NEG atom whose adj ∈ ANTONYMS → adj:=antonym, drop NEG.
9. Atom string `[~]<subj>|<REL>|<obj>`; sort atoms byte-wise; join
   with `\n`. This is the **meaning-canonical** form.
10. **Fingerprints** (frozen hash = SHA-256, vendored
    R33_NATIVE_SHA256_V2):
    - `meaning_fp` = sha256hex(meaning-canonical string)
    - `surface_fp` = sha256hex(sorted post-step-1 tokens joined
      with single spaces) — no stripping, no canonicalization.

## 4. Install rule (exact identity only)

- Atomize the draft (UNPARSED atom → WITHHOLD, cite the atom).
- License set = {sha256 of every atom of every committed store
  entry} ∪ {sha256 of every atom of every deliberation conclusion}.
  Store entries and conclusions are normalized with the same
  pipeline (§3); store entries resolve pronouns intra-entry.
- Per atom, first match wins, searched in store order then
  conclusion order. Attribution recorded per atom:
  `STORE:<id>`, `DELIB:<n>`, or `UNLICENSED`.
- INSTALL iff every atom is licensed. Otherwise WITHHOLD, naming
  the first UNLICENSED atom and the draft's meaning_fp.
- Provenance (`WORLD`|`GEN` on store entries) is READ and recorded
  in attribution but does NOT gate install — the design licenses
  "a committed memory entry"; discriminating provenance would be
  the write-once-partition follow-up, explicitly out of scope for
  this round (program prereg §0.2). The M5 measurement is exactly
  the cost of this design decision.

## 5. File formats (frozen)

- `store.txt`: lines `id|prov|text`, prov ∈ {WORLD, GEN}.
  GEN entries = harness-planted generator-authored entries from
  "earlier pinned episodes" (ids S900+).
- Case file: LF text with fields (order fixed):
  ```
  CASE: <id>
  BAR: m1|m2|m3|m4|m5|m6
  DRAFT: <sentence>            (m2/m3: A: and B: lines instead)
  ENTCTX: e1,e2,e3             (may be empty)
  DELIB: <c1> ;; <c2>          (may be empty; ;; separator)
  EXPECT: INSTALL|WITHHOLD     (m2/m3: SAME|DIVERGE)
  RULE: <paraphrase/attack rule exercised, or NOTE>
  ```
- `manifest.txt`: lines `<bar>/<file>` listing every case file, in
  fixed order; the battery runs the manifest top to bottom.
- Binary CLI: `forkc <store.txt> <case.txt>` → verdict lines on
  stdout (single-case probe API for the blind red team);
  `forkc_battery <store.txt> <manifest.txt>` → per-case lines +
  `SUMMARY` block with per-bar rates.
- Verdict line:
  `VERDICT <case> <INSTALL|WITHHOLD> mfp=<64hex> sfp=<64hex>
  atoms=<n> lic=<STORE:id|DELIB:n|UNLICENSED,...>`
- Pair line (m2/m3):
  `PAIR <case> <SAME|DIVERGE> va=<INSTALL|WITHHOLD>
  vb=<INSTALL|WITHHOLD>`

## 6. Corpora (harness-pinned; frozen at build commit)

All sentences authored by the fork-C harness (the builder acting as
harness; drafts are pinned in fixture files, never generator-authored
at run time). Sizes:

| Bar | Corpus | n | Expectation |
|-----|--------|---|-------------|
| M1 | m1/catch: confab drafts (contradict or ungrounded vs store) | 50 | WITHHOLD ≥70% |
| M1 | m1/gold: grounded drafts licensed by WORLD store entries | 50 | INSTALL (false-withhold ≤8%) |
| M2 | m2: same-shape/different-meaning pairs (one-slot edits: antonym, quantifier swap, digit perturb, entity swap, negation insert; token overlap ≥90%) | 36 | DIVERGE ≥90% |
| M3 | m3: same-meaning/different-shape pairs (synonym table, active↔passive, clause reorder, antonym-negation, numeric re-expression) | 36 | SAME ≥95% |
| M4 | m4: confab draft + self-consistent alibi trace (DELIB conclusions atom-match the draft; trace cites store ids whose actual entries do not license) | 24 | WITHHOLD ≥70% |
| M5 | m5: confab drafts licensed by GEN-provenance store entries (S900+, planted "earlier episodes"); DELIB empty | 24 | WITHHOLD ≥70% |
| M6 | m6: true drafts licensed by WORLD entries, incl. 12 true-but-surprising | 36 | INSTALL (false-withhold ≤5%) |
| M7 | held-out mirror: 24 catch + 24 gold + 12 m2 + 12 m3 + 12 m4 + 12 m5 + 16 m6, fresh sentences never seen in tuning | 112 | all bars hold |

- Store: ~70 WORLD entries covering all gold/m6 atoms + entries
  the M4 traces falsely cite + 24 GEN entries (S900–S923).
- M2 pair construction: start from a grounded base sentence, apply
  exactly one meaning-flip edit; B's EXPECT is DIVERGE of verdicts.
- M3 pair construction: apply paraphrase rules from the frozen
  tables only; each pair records its RULE.

## 7. Kill bars (from the program prereg, operationalized)

- **M1** ≥70% withhold on m1/catch AND ≤8% false-withhold on m1/gold.
- **M2** ≥90% DIVERGE on m2 pairs.
- **M3** ≥95% SAME on m3 pairs.
- **M4** ≥70% WITHHOLD on m4 alibi cases.
- **M5** ≥70% WITHHOLD on m5 recursion cases.
- **M6** ≤5% false withhold on m6 true drafts.
- **M7** all of the above recomputed on the held-out manifest;
  bars hold.
- Kill rule (program prereg §2): fail M1/M2/M6 → fork dead
  outright. M1–M3 pass + M4/M5 fail = the predicted theater
  signature — documented, not survived.

## 8. Theater-signature prediction (falsifiable)

Fork C is expected to PASS M1 (unlicensed confabs have no hash
match), PASS M2 (flips change atoms → different hashes), PASS M3
(paraphrases collapse to identical atoms), and FAIL M4 (the alibi
trace's conclusions hash-match the draft's atoms via the DELIB
license path → INSTALL) and FAIL M5 (GEN entries hash-match →
INSTALL; no provenance gate by design §4). The per-atom license
attribution will localize each failure to STORE:GEN or DELIB.
**If C passes M4/M5 against this prediction, the wall verdict
reopens for round 3 — reported loudly.**

## 9. Determinism plan

- Zero RNG in all decision paths: no RNG builtins; static source
  scan for `random|rand(|rng|time(|clock(` committed with evidence.
- Fixed iteration orders (manifest order, table order, store order).
- Full battery run twice; sha256 of the complete stdout compared —
  must be byte-identical; any nondeterminism = auto-FAIL.
- znc pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 10. Build discipline

- Fork prereg (this file) committed ALONE before any mechanism
  code is written.
- Pure Zag for mechanism + battery; Python only for glue/analysis.
- Commit via race-free script, lab-relative paths, no binaries,
  no `.zagd`, TMPDIR under `~/workspace/tmp_commit`.
- Layout: `docs/lab/senses/pam-rebuild/selfpam/r2/forkC/`
  (`PREREG.md`, `src/*.zag`, `corpora/...`, `evidence/...`).
