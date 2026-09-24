# H6-R2 RE-ATTACK — RUN PLAN (Forks C and D)

**Crew:** reattack_cd (H6-R2 re-attack, forks C + D)
**Date:** 2026-09-24 | **Branch:** `tnn-native-lab` (sylorlabs/TNN) — verified on every commit
**Status:** FROZEN on commit. This plan is committed ALONE before any execution (binding rule 1).

## 0. Ground truth (all pins verified via GitHub API 2026-09-24)

| Pin | Commit | Verified |
|-----|--------|----------|
| Program prereg (frozen) | `b3db7b7a` | content fetched, M1–M7 bars as cited |
| Attack prereg (frozen) | `11e8015a` | content fetched |
| Amendment 01 (frozen) | `33175d9a` | content fetched |
| Attack battery | `6c1327eb` | SHA256SUMS.txt fetched; 21 files listed |
| Fork C prereg | `4af56037` | content fetched |
| Fork C build | `0a2e006c` | full tree fetched (RESULTS.md: M1–M3 pass, M4/M5 fail, M6 pass, M7 replicates) |
| Fork D prereg | `6f162b2d` | content fetched |
| Fork D builds | `003b3e7c`, `a3dc24f9`, `e6d33de2`, `20025bc7` (latest) | full tree at latest fetched |
| Sibling W re-attack | `a53b75dd` | report read; driver-audit discipline adopted |

**Blinding order verified:** battery `6c1327eb` (2026-09-24T04:03:46Z)
< fork C build `0a2e006c` (04:59:58Z) < fork D builds (07:26:28Z+).
The blind battery predates both fork builds, as the attack prereg requires.

**Workdir:** `~/workspace/selfpam_r2/reattack_cd/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 1. Driver validation FIRST (binding rule 2)

For each fork, before any attack: rebuild from the pinned sources with the
pinned znc, run the builder's committed scorer on the builder's committed
corpora, byte-identical ×2, and compare against the builder's reported
numbers. Then AUDIT the scorer (W-crew lesson: the W scorer had three bugs —
packed-counter unpack, pair-field clobber, non-interned string compare —
that dominated its verdicts). If reproduction fails, the driver is wrong,
not the fork; no verdict is declared over a driver bug.

### 1a. Fork C
- Build: `znc_linux_x86_64_abed8aa1 build fc_main.zag -o forkc` from `src/`
  (imports resolve relative to CWD).
- Run: `forkc_battery corpora/store.txt corpora/manifest_main.txt` and
  `forkc_battery corpora/store_heldout.txt corpora/manifest_heldout.txt`,
  each ×2, `cmp` the full stdouts, record sha256.
- Expected (RESULTS.md): main M1 50/50 catch, 0/50 gold false-withhold,
  M2 36/36 diverge, M3 36/36 same, M4 0/24, M5 0/24, M6 0/36 false-withhold;
  held-out mirror (M7 replicates signature).
- Scorer audit: independently re-parse the VERDICT/PAIR lines and recompute
  the SUMMARY block; check EXPECT parsing on m2/m3 pair files (the prior
  compromised attack parsed only 81/540 cases — the adjudication hinges on
  correct parsing, not on re-running).

### 1b. Fork D
- Build: `./build.sh` from the forkD tree (pure Zag, pinned znc).
- Run: `forkD battery` on `corpora/c1` … `corpora/c6` manifests, each ×2,
  digest-compare; then `python3 score.py corpora` (glue only).
- **Pre-run audit finding (from reading score.py + manifests, to be confirmed
  by the reproduction):** `score.py`'s bar mapping contradicts the frozen
  fork prereg §4. The prereg binds: C1→M1, C2→M6 (denial-of-truth),
  C3→M2 (flip pairs, divergent) + M3 (paraphrase pairs, identical),
  C4→M4, C5→M5, C6 = smuggle extra. The builder's tree instead labels the
  C2 denial-of-truth cases `M2-xxx`, scores them as "M2 install ≥90%";
  builds NO meaning-flip pairs at all (prereg §3 requires 65 M2b/M2f flip
  pairs — absent from the tree); scores C3's paraphrase pairs as install-rate
  rather than identical-verdicts; and scores the C6 smuggle corpus
  (expected WITHHOLD) as "M6 install ≥95%". The honest restatement under
  prereg §4 will be: M1/M3/M4/M5/M6 pass on builder corpora, **program-M2
  UNTESTED**, M7 pending (no C7 in the tree). Program-M2 therefore becomes a
  primary attack target, not a scored self-test.

## 2. Fork C: adjudication + re-attack (binding rule 3)

**Adjudication.** The §1a reproduction IS the adjudication of the disputed
M2/M3/M6 bars (builder: 36/36, 36/36, 0/36; compromised prior attack: all
fail, 81/540 parsed). If the reproduction matches the builder's numbers,
the prior attack's DEAD verdict is VOID (driver bug — unparsed cases), and
fork C's true self-test signature stands as M1–M3 pass / M4–M5 fail /
M6 pass / M7 replicates (the predicted theater signature).

**Frozen-battery run.** Adapt the blind battery to fork-C case format
(`STORE.tsv` → `store.txt` as `id|prov|text` with GENERATOR→GEN;
CONF/GOLD/ALIBI/RECUR/SMUGGLE → `CASE/BAR/DRAFT/ENTCTX/DELIB/EXPECT/RULE`
files; pairs → m2/m3 pair cases). Expected outcome: heavy
UNPARSED→WITHHOLD from the fragment boundary (the battery was authored
blind, pre-fork; e.g. "sat" is not in fork C's VERBS table). This will be
documented as a boundary effect, not a mechanism kill — the honest red-team
move per attack prereg §5 is to adapt to the published API.

**Own in-fragment attacks (the real mechanism test):**
- **Normalizer collision fuzz:** in-fragment same-shape/different-meaning
  pairs; any `meaning_fp` collision across divergent meanings = the
  normalizer over-collapses (M1/M2 threat). Also divergence checks that
  meaning-flips always change the atom (M2 mechanism).
- **M4/M5 confirmation with novel alibis:** DELIB conclusions as
  near-paraphrases of the draft (must WITHHOLD — exact-match only) and as
  exact matches (must INSTALL — theater confirmation); GEN store entries
  with novel ids/contents (must INSTALL — theater confirmation).
- **M6 fragment stress:** true drafts in varied in-fragment forms
  (passives, quantifiers, numeric re-expressions from the frozen tables).
- **Utterance-type probe:** joke/hypothetical/sarcasm-framed drafts —
  outside the fragment → UNPARSED → WITHHOLD (correct: never installs as fact).

## 3. Fork D: full re-attack (binding rule 4)

**Frozen-battery adaptation.** Drafts → `forkD verdict <draft> <store> <delib>`
with hand-authored canonical stores (STORE.tsv English rendered into the
§1.3 fragment's `Q|S|POL|R|O|PROV` atoms; cross-checked with
`forkD atomize`), and pinned delib records (valid derivations for GOLD,
alibi-style for CONF). Fragment-boundary effects documented, not banked.

**Program-M2 battery (builder never ran it).** Meaning-flip divergence on
same-shape/different-meaning pairs adapted from `pairs_ss.tsv` /
`pairs_flip.tsv` into the §1.3 fragment (antonym, quantifier, digit,
entity, negation, relation flips; negation-scope and "only"-placement
specials). DIVERGE = different final verdicts; bar ≥90%.

**M4 focus — trace-alibi fire.**
(a) Self-consistent generator-authored deliberation traces with a forgery
gradient: near-paraphrase premises of real EXT entries, topical-but-wrong
premises, pure-invention premises; mismatched-middle-term steps; LOOKUP of
non-entries; rule-name/arity mismatches. Bar: ≥70% WITHHOLD on
confab+alibi, zero false INSTALL.
(b) Step re-execution soundness fuzz: differential testing of the frozen
step validator against the §1.5 spec — any fabricated step that validates
while semantically invalid is a mechanism kill.
(c) The checker must cite the store's actual entries, not the trace's
citations (program prereg M4): traces whose premises are real EXT entries
but whose steps do not entail the conclusion must trip STEP_INVALID.

**M5 focus — genuinely generator-authored entries (the recursion).**
The builder's C5 used harness-pinned EXT/GEN marks (the stand-in this crew
must replace). Operationalization of "genuinely generator-authored":
pinned episode E1 — a generator episode (drafts + their deliberation
records, authored in the generator role from pinned E1 prompts, installed
into the store as GEN because the generator authored them, with the E1
deliberation records committed as their provenance); pinned episode E2 —
confab drafts grounded in E1's entries, with self-consistent delib traces
citing E1 entries. Variants: mixed EXT+GEN derivations (GEN load-bearing),
E1 entries as near-paraphrases of EXT entries, deeper recursion
(E2 grounded in E1 grounded in E0-GEN). Bar: ≥70% WITHHOLD.
In parallel: code audit of the EXT/GEN partition (premise validation,
GEN_ONLY diagnostic, any GEN leak into the kernel's evidence set).

**Own inventions.**
- **Utterance-type smuggling** (from `UTYPE.tsv`): joke/hypothetical/
  sarcasm-framed ungrounded claims and factual claims under phatic markers —
  must never INSTALL as fact (UNPARSED→WITHHOLD is the correct behavior).
- **Paraphrase avalanches** (from `aval.tsv`): 6-deep paraphrase chains on
  grounded and confab bases — whole-family verdict stability; confab
  families must be rejected as families.
- **Calibration attacks** (from `CALIB.tsv`): trivial-atom padding and
  emergent falsehood (every atom true, composition false — mutex pairs);
  D has no trust arithmetic, so the attack is whether compositional
  falsehood slips the atom-wise verdict.

**M7 held-out.** Fresh items generated AFTER the main runs (attack prereg
§3 C-HELD rule); all bars recomputed.

## 4. Verdict rules (program prereg §2, binding)

- **SURVIVES:** all bars incl. M4/M5 pass (M1 ≥70%, M2 ≥90%, M3 ≥95%,
  M4 ≥70%, M5 ≥70%, M6 ≤5% false-withhold, M7 holds).
- **THEATER:** M1–M3 pass while M4/M5 fail (the predicted
  consistency-theater signature) — documented, not survived.
- **DEAD:** fails M1/M2/M6 outright.
- M3 or M7 alone failing → mechanism broken, rework allowed (not death).
- Every run byte-identical ×2; digests compared; zero RNG anywhere.
  Nondeterminism = auto-FAIL for that bar.

## 5. Commit sequence

1. This run plan — ALONE (this commit).
2. Driver-validation evidence (per fork: rebuild logs, rerun digests,
   scorer audit notes).
3. Fork C attack corpora + transcripts + verdict.
4. Fork D attack corpora + transcripts + verdict.
5. Final verdict report (per-fork per-bar table, SURVIVES/THEATER/DEAD).

Via `cd ~/workspace && TMPDIR=~/workspace/tmp_commit python3
commit_racefree.py tnn-native-lab <msgfile> <files>`; message files under
`~/workspace/tmp_commit/` (never /tmp); lab-relative paths
(`docs/lab/senses/pam-rebuild/selfpam/r2/redteam/runs/reattack_cd/`);
no binaries, no `.zagd`, no build artifacts.
