# RT3 Joke-Classifier Fix Report (v4fix)

## Fidelity gate (prerequisite)
- Attacked source SHA-256: `71a33af3be2029b23b343a25d98a7697ab7fd1d236b647f5833ebe6473cf4098`
  (matches RT3's recorded attacked source).
- Byte-identical rebuild `rt3_bat_repro` from pristine source with pinned
  `znc_linux_x86_64_abed8aa1`: run output SHA
  `438599877c1af6e685d9fb060217bf4a656766d92cee517bed64bb9601126b19`
  = RT3's committed `run1.txt`. Frozen 30 rows 30/30 exact (intent+codes+markers).
- Attack reproduction: **70/75 hits**, item-by-item code-identical to RT3's hit
  list (A 14/15, B 15/15, C 15/15, D 12/15, E 14/15). No phantoms, no misses
  beyond RT3's list. Gate PASSED before any repair.

## Root causes repaired (pure Zag, zero RNG)
1. **Deadpan installs (A/B families, 29): single-word trope triggers.**
   Any one of `free/ram/upgrade/ama/findings/joke/pet/downloaded/traveler`
   forced JOKING on sincere text. Fix: `R_TROPE` now requires a two-clause
   punchline shape (`; ? ! .+text , which , who`); as a *secondary* tag it may
   also corroborate an already-established joke when a purpose infinitive is
   present (`contra!=0 && j_purpose_to`), which restores frozen J05's
   `P_DA3F+R_TROPE` without resurrecting A05-style attacks.
2. **Contradiction rules fired on bare word co-occurrence (D family, 12).**
   Rules 1–35 now require `j_justify` (deadpan-benefit/completion signal):
   two-clause shape, `if/when` conditional setup, purpose infinitive
   (`to <non-determiner>`), `for/to+article+comparative` benefit claim
   ("for a brighter morning"), or casual quantity ("a splash of").
3. **P_DA5D (moon/cheese) fired on non-constitutive co-occurrence (A09).**
   Replaced with `j_da5d_shape`: sky word within 24 chars *before*
   "made of/from"|"composed of" AND food stem within 52 chars *after*.
4. **R_IRONY fired on sincere cessation advice (A06/A07).**
   Now vetoed by `j_cessation` (quit/stopped/stop/gave up/never) and `j_you`
   (second-person audience address).
5. **R_PUN1 fired on single-clause dual-word texts (A15/B11).**
   Now requires two-clause punchline shape.
6. **R_PUN2 fired when the pivot was mid-sentence (D15).**
   Now requires `j_pun2_pivot`: "make/made up everything/anything" at a
   clause end (`. ; ? !` or end-of-text).
7. **R_SATIRE fired on hostile news text (B15).** Vetoed by `j_insult`
   (idiot/moron/stupid/dumb/ugly/loser).
8. **Dead stemmer branch (RT3 §7).** The dropped-e check
   (`smoke→smoking`, `shove→shoving`) was nested inside the full-stem-match
   branch, unreachable when the stem's final `e` was absent. Moved outside so
   it also runs on prefix matches. (Also fixes real understemming, e.g. A07
   "drinking" now stems.)
9. **Iron false positive (A08).** `n_A_IRON` suppressed on the collocation
   "iron deficiency"/"iron-deficiency" (sincere health context).
10. **Missed joke shapes (C/E families, 29): new structural rules 40–51.**
    - N_QA (40): riddle opener (`why did/do/does`, `what do you call/did/is/are`,
      `how many`) + `?` + non-empty answer.
    - N_DENY (41): "not a joke" / "not joking".
    - N_BAR (42): walked-into-a-bar opener + two-part body.
    - N_NEG (43): negation joke — negation marker(s) + two-part body +
      reframe/pivot (`just/but/instead/now/or/too bad/enjoy/always/might/
      still/yet/however`), or single clause with but-negation contrast
      reversal ("but you did not like it").
    - N_WHISPER (45): conspiratorial speech verb (whispered/muttered/hissed)
      + quoted speech + two-part body.
    - N_PUN_GROW (47) / N_PUN_OVER (48) / N_PUN_JUMP (49) / N_PUN_LINE (50) /
      N_PUN_OUT (51): pun = figurative idiom + literal-context word priming
      the literal meaning ("grew on me"+growable, "getting over it"+fear+
      traversable, "jump(ing) to conclusions"+jumping-context,
      "fine line between"+math-domain, "come out"+celestial+dental).
      Both halves are semantic classes, not row-specific strings.
    - Two candidate detectors were built and then REMOVED: N_TRY
      ("tried to"+two-clause) false-positived on sincere "I tried to fix the
      sink. It is still leaking."; N_PROVERB never fired on anything.
      Neither was load-bearing (C04 is caught by N_WHISPER).

## Results
- **RT3 attacks: 0/75 hits** (was 70/75). Per family: A 0/15, B 0/15, C 0/15,
  D 0/15, E 0/15.
- **Frozen battery: 30/30 byte-identical** to committed `v4_run1.txt`
  (intent, codes, and markers all exact; zero deadpan installs).
- **Held-out (fresh, oracle-labeled BEFORE running, 15J/15N): 28/30.**
  All 15 non-jokes correct, including adversarial sincere probes
  (sincere negation, whisper, tried-to, used-to/now, fear+getting-over-it,
  jumping-to-conclusions, fine-line, grew-on-me). Misses: H13 ("embrace
  change" — `change` not in the pre-existing F_ABSTRACT inventory; lexical
  gap, left untouched) and H15 (novel "killing me / stop carrying the team"
  pun with no covering detector; documented limitation).
- **Determinism: 3× runs byte-identical**, SHA-256
  `792cb82135404535a4d4541f2a058ff2d74f6b1fb614eb9f809de63566d6ae14`.

## Artifacts (in `rt3fix/`, not committed)
- `g_intent6_v4fix.zag` — repaired classifier source, SHA-256
  `833d8e127d5edb12ec115b58e0d015fe58cead3791b204c9c34803e251ec6b09`
  (1453 lines; generated by `patch_v4fix.py` from pristine
  `g_intent6_v4.zag` + `v4fix_helpers.zag`, both kept for audit).
- `rt3_bat_fix.zag` / `rt3_bat_fix` — battery driver + pinned-znc binary.
- `run_fix_{1,2,3}.txt` — three byte-identical runs.
- `heldout.tsv` — 30 oracle-labeled held-out items (labels frozen pre-run).
- `rt3_heldout.zag` / `rt3_heldout`, `run_heldout.txt` — held-out run.
- `run_repro.txt` — fidelity reproduction run (matches RT3's SHA).

## znc constraints honored
No indexed `as []i32/u32/u16`; no slice `==`; `_zag_arg` never argc-gated
(driver takes no args); no slice >2^25; else-nesting ≤4 (helpers are flat
early-return chains); no struct >8 fields (none added); `return;` in void
fns; no new raw syscalls. Only new warnings: none (build shows the
pre-existing L0012 harness string-leak note, also present in the repro build).

## Verdict
All reproduced RT3 attacks are now classified correctly (75/75), the frozen
30-item battery is byte-identical (30/30, zero deadpan installs), fresh
held-out scores 28/30 with the two misses analyzed as pre-existing lexical
gap + uncovered novel pun (no new false-positive class introduced), and
three runs are byte-identical. **FIX COMPLETE — ready for re-attack.**
