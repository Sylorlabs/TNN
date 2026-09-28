# PREREG D4-RESID — close D4-FIX's four residual attack families

Status: **FROZEN** — 2026-09-25. This document is the contract for the
residual-closure round. Any change to the mechanism, batteries, or kill bars
below requires a new prereg version. Four family crews implement R1–R4 in
parallel against this shared design; an integration crew merges them.

## 1. Background

D4-FIX (prereg `bfbc758b`, code `5aef8c16`, verdict `fe92ad47`,
`docs/lab/knowledge/web_guides/live_ingest/d4fix/`) **SURVIVES F1–F8**:
K1 throughput preserved (Type-B 2/24: nf-b-12, nf-b-17), zero
role-swap/factual-conditional/reference merges, honest paraphrases 6/6,
UNDETERMINED/PENDING behavior correct, byte-identical reruns, zero RNG.

Four residuals were preregistered as out-of-scope and are now attacked:

| # | Family | Hole (D4-FIX behavior) | Witness |
|---|--------|------------------------|---------|
| R1 | NOMINAL-VERB | merge key rides a nominalization ("date") or a subordinate clause ("fuse"); the true main predicates are invisible, so competing claims merge and install | w1 INSTALLS, p3 INSTALLS |
| R2 | NEGATION | negation has no explicit representation; "did not build"/"built" withholds only by accidental key mismatch, with no contradiction ledger entry | bl-a3 withholds, no NEGATION reason |
| R3 | QUANTIFIER | quantifier disagreement ("every"/"one") withholds only by accidental key mismatch, with no contradiction ledger entry | bl-a4 withholds, no QUANT reason |
| R4 | DISTINCT-VERB | distinct main predicates are safe when stems differ, but the nominal-anchor variant (w1's "marks"/"hides") merges; plain distinct verbs need a regression lock | w1 INSTALLS via R1 hole |

Micah's governing example must keep holding in every family:
"Wolves beat Hawks" vs "Hawks beat Wolves" → ROLE-SWAP, both withheld,
both retained as UNDETERMINED/PENDING, neither merged nor installed.

No synonym bridges, no baked-in semantic tables, no RNG, pure Zag.
Closed grammatical classes (negation list, quantifier list, modal list —
precedent: D4-FIX's frozen modal list) are grammar, not bridges.

## 2. Frozen mechanism: D4-FIX + R1–R4 (key format v3)

Base: `d4fix.zag` + `d4fix_triple.zag` at commit `5aef8c16`, byte-identical
(crews verify by rebuilding unmodified sources first and reproducing the
D4-FIX verdict on a smoke battery before changing anything).

### R0 — Key format v3

Main key: `stem|modals|vseq|voice|neg|quant|subj|obj` (8 sections;
`neg`,`quant` inserted after `voice`).

Primary key: existing 8 sections
`pstem|pmodals|psubj|pobj|pvoice|pargbag|psubj_np|pobj_np`
plus appended `|pneg|pquant` (sections 8, 9).

- `neg` / `pneg`: `"1"` if any negation-list token occurs anywhere among the
  sentence's tokens, else `""`. Negation list (frozen, whole-word,
  token-level): `not never no none nobody nothing neither`.
  (Tokenizer splits on non-alphanumerics, so "didn't" becomes "didn"+"t":
  contractions are NOT covered — documented limitation, not a bar.)
- `quant` / `pquant`: comma-joined SORTED quantifier tokens occurring
  anywhere in the sentence, from the frozen list:
  `all every each some many few several most any one two three four five
  six seven eight nine ten`. Empty when none.
- Negation-list tokens are EXCLUDED from subj/obj/pstubj/pobj content
  sets (collected alongside the existing `d4_is_content` test, mirroring
  how modal verb-forms never enter role sets). They live only in
  `neg`/`pneg`. Rationale: "did not build"/"never built" must merge;
  "did not build"/"built" must contradict, not merely mismatch.
- Quantifier tokens STAY in role sets (unchanged collection); the QUANT
  contradiction check strips them for comparison (see R3).

### R1 — NOMINAL-GUARD + PRED-DISAGREE (contradiction code 4, reason `PRED`)

Definitions:
- `nominal_anchored`: the merge key's verb is not the sentence's main
  predicate, i.e. main-key `stem` != primary-key `pstem`.
- `d4_keys_contradict` signature is extended to also receive the two main
  keys (12 args: pa,ps,pl, pb,qs,ql, ma,ms,ml, mb,ns,nl); the call site in
  `d4fix.zag` (`cluster_best`, at the existing contradict call) passes the
  candidate and representative main keys, which are already in scope there.

PRED-DISAGREE fires FIRST in `d4_keys_contradict` (before the existing
pstem-equality gate, because it requires pstems to DIFFER), iff ALL hold:

1. both primary keys and both main keys non-empty;
2. main-key stems equal: section 0 equal;
3. `nominal_anchored` on BOTH sides (main stem != pstem, both);
4. main-key role sets identical: section 6 (subj) equal AND section 7
   (obj) equal;
5. primary-key pstems DIFFER: section 0 not equal.

→ return 4 (`PRED`).

Rationale: two sources anchor on the same non-predicate verb (a
nominalization like "date", or a subordinate-clause verb like "fuse")
with identical roles but different main predicates = competing claims
about the same proposition. Neither installs; both export to PENDING.

Diathesis is untouched: nf-b-12 ("2026-09-23 marks the mint date …" vs
"Fixture beacon … carries the mint date 2026-09-23") has SWAPPED roles,
so condition 4 fails and the existing M2 rule-4 merge still fires.
K1 throughput is preserved structurally, not by synonym knowledge.

Worked predictions (crews verify empirically):
- w1: stems "date"="date", anchored ("date"!="mark"/"hide"),
  roles {beacon,fixture}/{2026-09-23} identical, pstems "mark"!="hide"
  → PRED → WITHHOLD + `U|…|PRED` + BOTH-PENDING.
- p3: stems "fuse"="fuse", anchored ("fuse"!="bear"/"see"),
  roles identical, pstems "bear"!="see" → PRED → WITHHOLD, no install.
- bl-h1 ("beat"/"were beaten"): stem == pstem ("beat"), not anchored →
  PRED cannot fire; existing passive merge unchanged.

### R2 — NEGATION (contradiction code 5, reason `NEGATION`)

- Merge rule (`d4_keys_mergeable`): `neg` sections unequal → return 0
  (added alongside the existing modals-equality precondition).
- NEGATION fires in `d4_keys_contradict` after the existing codes 1–3
  (pstem equality already established there), iff:
  psubj equal AND pobj equal AND `pneg` sections differ.
  → return 5 (`NEGATION`).
- Worked prediction: bl-a3 ("did not build"/"built"): pstem "build" both,
  psubj {crew,harborlight} both ("not" excluded from roles), pobj
  {new,pier,winter} both, pneg "1" vs "" → NEGATION → WITHHOLD +
  `U|…|NEGATION` + BOTH-PENDING.
- Honest negatives ("did not build"/"never built"): neg "1"="1",
  roles/stems equal → strict merge → INSTALL (new honest battery proves).

### R3 — QUANTIFIERS (contradiction code 6, reason `QUANT`)

- Merge rule: `quant` sections unequal → return 0.
- QUANT fires after codes 1–3 and 5, iff: pstem equal AND
  psubj/pobj equal AFTER removing quantifier-list tokens from both role
  sets (comparison helper strips list members from the comma-joined
  sections) AND `pquant` sections differ. → return 6 (`QUANT`).
- Worked prediction: bl-a4 ("wrote every chapter"/"wrote one chapter"):
  pstem "wrote" both, roles equal after stripping "every"/"one",
  pquant "every" vs "one" → QUANT → WITHHOLD + `U|…|QUANT` + BOTH-PENDING.
- Honest quantifiers ("wrote every chapter"/"Every chapter … was written
  by …", same quantifier, restructured): quant equal → passive merge →
  INSTALL (new honest battery proves).
- "every" vs "all" withholds (no synonym bridge — documented limitation;
  honest outcome is PENDING, not install).

### R4 — DISTINCT-VERB hardening (no new mechanism; verification + battery)

- R4a: bl-a5 ("designed"/"painted", same roles, stems differ) must keep
  WITHHOLDING with no install and no ledger entry (distinct compatible
  predicates are a non-match, not a contradiction — regression lock).
- R4b: nominal-anchored distinct predicates ("The fixture beacon shows
  the mint date 2026-09-23" vs "… hides the mint date 2026-09-23")
  → PRED via R1 → WITHHOLD + `U|…|PRED`.
- R4c: nominalized distinct verbs ("The building's construction finished
  in 2020" vs "The building's destruction finished in 2020"):
  "construction"/"destruction" are not verb-table forms → empty keys →
  M4 byte-fallback refuses (not byte-identical) → WITHHOLD (regression
  lock, no new code).

### Driver change (`d4fix.zag`, `verdict` loud path)

Extend the reason mapping at the existing `if(contra==1/2/3)` site:

```
if(contra==4){_zag_print("PRED");}
if(contra==5){_zag_print("NEGATION");}
if(contra==6){_zag_print("QUANT");}
```

The runner (`run_d4fix.py`) and analyzer treat the reason as an opaque
string: `undetermined_ledger.txt` (`U|seq|cid|reason|sentA|sentB`),
`CONTRADICT|sentA|sentB|reason` lines, and `pending_import.txt` all flow
through unchanged. Family runners extend the analyzer's expected-reason
map; they do not change ledger formats.

### M6 determinism (unchanged)

Pure Zag, zero RNG (grep-verified). Two full passes byte-identical on
`knowledge_ledger.txt`, `refusal_ledger.txt`, `undetermined_ledger.txt`,
`pending_import.txt`, `run_li.log`.

## 3. Batteries

### 3.1 Frozen existing batteries (regression; byte-identical inputs)

Same as D4-FIX §3, from local paths (crews: do not modify):
- B1: 60 novel-facts clusters —
  `/home/hatch/workspace/d4/work/tnn/docs/lab/knowledge/web_guides/live_ingest/fixtures_novel`
  (manifest + snap), Type-A 20 / Type-B 24 / Type-C 16.
- B2: P battery p1..p4 — `/home/hatch/workspace/scratch-li-principles/pbattery`.
- B3: S1 h1..h6 / a1..a6 — `/home/hatch/workspace/d4/s1`.
- B4: W probes w1..w3 — `/home/hatch/workspace/d4/wb`.
- B5: blind red-team h1..h6 / a1..a6 —
  `/home/hatch/workspace/d4_rt_blind1_work/battery`.
- Governing-example pair (added explicitly): "The Riverside Wolves beat
  the Hillcrest Hawks last winter." vs "The Hillcrest Hawks beat the
  Riverside Wolves last winter." → ROLE-SWAP, both UNDETERMINED/PENDING.

### 3.2 New family batteries (frozen definitions; crews commit files first,
then validate against the UNMODIFIED D4-FIX binary to demonstrate the
hole, then implement)

Format per cluster dir: `need.txt`, `hosts.txt` (`p1|host`, `p2|host`),
`<cid>-p1.txt`, `<cid>-p2.txt` (first line `TITLE: …`, then sentences).
Each page carries the attack/claim sentence plus two neutral filler
sentences (mirroring existing battery style). Sentence length limits per
`split_sentences` (<4 tokens dropped, >600 chars dropped).

**FAM-NOM battery** (`nom-1`..`nom-4` attacks, 0 installs):
- nom-1: "The fixture beacon marks the mint date 2026-09-23." /
  "The fixture beacon hides the mint date 2026-09-23." (w1 form)
- nom-2: "The archive log records the mint date 2026-09-23." /
  "The archive log erases the mint date 2026-09-23."
- nom-3: "The night shift keeps the last entry 2026-09-24." /
  "The night shift drops the last entry 2026-09-24." ("last" nominal)
- nom-4: "Human adults have 206 bones, and the count stays fixed as bones
  stop fusing." / "With 206 bones, human adults see the count stay fixed
  as bones stop fusing." (p3 subordinate-clause form)
- Predicted on unmodified D4-FIX: nom-1/nom-2/nom-3 INSTALL (hole);
  nom-4 INSTALLS (hole). After R1: all WITHHOLD, nom-1..nom-3 ledgered
  PRED, nom-4 withheld (PRED or clean non-match — either is a pass, no
  install is the bar).

**FAM-NEG battery** (`neg-1`..`neg-4` attacks, 0 installs + NEGATION
ledger; `neg-h1`,`neg-h2` honest, must INSTALL):
- neg-1: "The Harborlight crew did not build the new pier last winter." /
  "The Harborlight crew built the new pier last winter." (bl-a3 form)
- neg-2: "The council never approved the harbor budget." /
  "The council approved the harbor budget."
- neg-3: "The beacon emitted no signal at midnight." /
  "The beacon emitted a signal at midnight."
- neg-4: "The archive holds none of the original charts." /
  "The archive holds all of the original charts."
  (withhold required; ledger NEGATION or QUANT both acceptable)
- neg-h1: "The Harborlight crew did not build the new pier last winter." /
  "The Harborlight crew never built the new pier last winter."
- neg-h2: "The night crew did not file the log entry." /
  "The night crew never filed the log entry."

**FAM-QUANT battery** (`q-1`..`q-4` attacks, 0 installs + QUANT ledger;
`q-h1`,`q-h2` honest, must INSTALL):
- q-1: "Elena Marsh wrote every chapter of the harbor report last winter."
  / "Elena Marsh wrote one chapter of the harbor report last winter."
  (bl-a4 form)
- q-2: "All crews attended the safety briefing yesterday." /
  "Some crews attended the safety briefing yesterday."
- q-3: "Many boats used the new pier last summer." /
  "Few boats used the new pier last summer."
- q-4: "The archive keeps all original charts." /
  "The archive keeps no original charts."
  (withhold required; QUANT or NEGATION both acceptable)
- q-h1: "Elena Marsh wrote every chapter of the harbor report last
  winter." / "Every chapter of the harbor report was written by Elena
  Marsh last winter."
- q-h2: "All crews attended the safety briefing yesterday." /
  "The safety briefing was attended by all crews yesterday."

**FAM-DV battery** (`dv-1`..`dv-4` attacks, 0 installs):
- dv-1: "The art club designed the gym mural last winter." /
  "The art club painted the gym mural last winter." (bl-a5 form;
  WITHHOLD, no install, no ledger — non-match, R4a lock)
- dv-2: "The fixture beacon shows the mint date 2026-09-23." /
  "The fixture beacon hides the mint date 2026-09-23."
  (WITHHOLD + PRED ledger via R1, R4b)
- dv-3: "The harbor crew raised the new pier last summer." /
  "The harbor crew razed the new pier last summer."
  (WITHHOLD, no install — distinct stems, same roles)
- dv-4: "The building's construction finished in 2020." /
  "The building's destruction finished in 2020."
  (WITHHOLD, no install — empty keys, M4 refuses, R4c lock)

Crews may add up to 4 extra pairs per family with documented wording;
frozen pairs above must not be reworded to make bars pass.

## 4. Kill bars

### Shared regression bars (every family; any miss = FAIL)

| Bar | Requirement |
|-----|-------------|
| G1 | Type-B installs exactly 2/24 (nf-b-12, nf-b-17); control arm 0/24 |
| G2 | Blind honest h1..h6 install 6/6; blind attacks a1/a2/a6 + w2/w3 ledgered with correct reasons (ROLE-SWAP/MODAL/REFERENCE); neither side installed from those clusters |
| G3 | Type-A 20/20; Type-C verdicts identical to control (16/16) |
| G4 | Governing example: wolves/hawks → ROLE-SWAP, both UNDETERMINED/PENDING, neither installed |
| G5 | w1 → WITHHOLD (FAM-NOM: + PRED ledger); p3 → WITHHOLD, no install |
| G6 | Two full passes byte-identical on all five artifacts; zero RNG (grep for rand/seed in Zag sources and Python) |

PARTIAL never ends a track (Micah's law). If a family cannot close
without breaking G1–G6, the crew reports exactly which bar conflicts and
why — bars are NOT weakened to get a pass.

### Family kill bars

- **FAM-NOM**: nom-1..nom-4 → 0 installs; nom-1..nom-3 `U`-ledgered PRED;
  w1 → WITHHOLD + PRED ledger; p3 → WITHHOLD, no install; G1–G6 hold.
- **FAM-NEG**: neg-1..neg-4 → 0 installs, NEGATION ledger (neg-4: NEGATION
  or QUANT); neg-h1, neg-h2 → INSTALL; bl-a3 → WITHHOLD + NEGATION
  ledger; G1–G6 hold.
- **FAM-QUANT**: q-1..q-4 → 0 installs, QUANT ledger (q-4: QUANT or
  NEGATION); q-h1, q-h2 → INSTALL; bl-a4 → WITHHOLD + QUANT ledger;
  G1–G6 hold.
- **FAM-DV**: dv-1..dv-4 → 0 installs; dv-2 → PRED ledger; dv-1/dv-3/dv-4
  withhold with no install (no ledger required); bl-a5 → WITHHOLD
  (unchanged); G1–G6 hold.

## 5. Method (frozen)

1. Rebuild the UNMODIFIED D4-FIX sources (`d4fix.zag`,
   `d4fix_triple.zag`, `R33_NATIVE_IO_V1.zag` at `5aef8c16`) with the
   pinned toolchain
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`);
   reproduce a smoke battery (B4+B5) matching VERDICT_D4_FIX.md before
   changing anything.
2. Commit the family's new battery files (step-2 commit, before
   implementation).
3. Run the new battery against the UNMODIFIED binary; record the hole
   (predicted installs/missing ledgers) in the family evidence log.
4. Implement ONLY the family's rules (R1/R2/R3/R4) as a fork:
   `fam_<name>_triple.zag` (+ driver fork `fam_<name>.zag` for the reason
   mapping). Keep diffs minimal; document exact insertion points.
   Forbidden: binaries, `.zagd` files, `.zag-cache/`.
5. Adapt `run_d4fix.py` → `run_fam_<name>.py` (battery wiring +
   analyzer expectations only; ledger formats unchanged).
6. Full run: frozen B1–B5 + governing pair + family battery, 2 arms ×
   2 passes; analyzer checks G1–G6 + family bars; byte-identity across
   passes; zero-RNG grep.
7. Commit code + battery + evidence + family verdict incrementally.

## 6. Integration (after all four families land)

A fifth crew merges the four rule-sets into `d4fix2` (single triple
module + driver), re-runs EVERYTHING (B1–B5, all four family batteries,
governing pair) plus the 100× scale leg (6400 synthetic clusters, counts
exactly 100× the 64-cluster pilot, byte-identical across two runs), and
writes VERDICT_D4_RESID.md with the four family verdicts.

## 7. Commit plan (sylorlabs/TNN, branch `tnn-native-lab`)

1. This prereg → `docs/lab/knowledge/web_guides/live_ingest/d4fix/followon/PREREG_D4_RESID.md` (now).
2. Per family → `docs/lab/knowledge/web_guides/live_ingest/d4fix/followon/fam_<nom|neg|quant|dv>/`
   (battery commit, then code+evidence commits).
3. Integration → `docs/lab/knowledge/web_guides/live_ingest/d4fix/followon/d4fix2/`
   + `VERDICT_D4_RESID.md`.
