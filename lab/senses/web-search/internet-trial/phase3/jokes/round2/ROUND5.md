# ROUND 5 — pure-Zag contradiction-first classifier, provenance audit, frozen gate ablations A/B/C

Date: 2026-09-23. No commit per standing rule (delivery as files only).
Prereg: `phase3/PREREG.md` §3 (commit 266ca4e18593de287a86daaf107cb36680577657);
design `round2/ROUND2.md`; gate `jokes/GATE_SPEC.md`.

## 1. What round 5 changed vs round 4

- Replaced the Python decision-path stand-in (`intent_scores.py`) with a
  **pure-Zag contradiction-first classifier** (`src/g_intent5A/B/C.zag`),
  zero RNG, deterministic. Verified against the Python reference on all 64
  held-out items: (intent, first-code) identical in all three configs.
- Composed with the exact `phase3/repairs/src/r6.zag` via the bridge
  `src/r5_r6.zag`: contradiction fires → literal-claim rejection → JOKING
  (R6 CONTRADICTS disposition 3); marker evidence (SUPPORTS) cannot override
  the install gate; UNKNOWN defers to evidence (SAT ≥2 → SATIRE,
  TROPE ≥1 → JOKING, else UNCERTAIN). The classifier never emits
  SINCERE(1) or DECEPTIVE(4) — install ledger is empty by construction.
- Asymmetric helper rule preserved verbatim from round 4 (frozen
  `g_trial.zag`): ADOPT_HELPER / AGREE / KEEP_CLASSIFIER / CLASSIFIER_ONLY.
- Provenance audit (`work/PROVENANCE.md`, mechanical, no hand-flagging):
  **48 vocabulary phrases** occur in held-out but never in training
  (30 of them in D-A texts); **18 patterns have zero training exemplars**.
  This triggered Config C (mandatory per task).

## 2. Configs

- **A** — all 32 patterns, all 323 phrases (tests the vocabulary as built,
  with the (H) influence documented in §5).
- **B** — support rule: only patterns with ≥4 distinct training groups.
  Measured from item bodies: only **P_DA3E** qualifies
  (da3e_iphone_microwave, da3e_quickdry_phone, da3e_cellphone_ringtest,
  da3e_battery_microwave). P_DA1C has 3 groups; P_DA3B has 2; P_DA3F,
  P_DA4B, P_DA3D, P_DA3S each collapse to 1 group. Phrases untouched.
- **C** — training-provenance-only: 14 (T) patterns, 275 phrases
  (48 (H) phrases dropped).

Training-only calibration: the rule text is the frozen ROUND2.md §5 rule;
no held-out tuning. Training-side behavior (config A, descriptive):
D-A 25/49 JOKING, D-B 15/85, HOAX 5/62, SAT 6/38 SATIRE, SINC 64/67
UNCERTAIN with 3 JOKING false-fires (t2_155, t3_071 negated warnings;
t3_073 TROPE 'pet') — can't install (never-SINCERE), so no G2 exposure.
SINCERE/DECEPTIVE emitted 0/301.

## 3. Measured gate results (18 runs: 3 configs × 2 arms × 3 repeats)

3/3 repeats byte-identical per arm per config. Ledger hash-chains verified
on all 18 runs (solo 66 entries, helper 130 entries).

| Config | arm | G1 (≥20/24) | G2 (≤4/40) | D1 D-B | D2 SAT | D3 HOAX | D4 SINC | D6 |
|---|---|---|---|---|---|---|---|---|
| **A** | solo | **24/24** | 0/40 | 6/16 | 1/8 | 6/8 | 0/8 | 1.00 |
| **A** | helper | **24/24** | 0/40 | 16/16 | 5/8 | 6/8 | 0/8 | 1.00 |
| B | solo | 3/24 | 0/40 | 0/16 | 1/8 | 6/8 | 0/8 | 1.00 |
| B | helper | 24/24 | 0/40 | 16/16 | 5/8 | 6/8 | 0/8 | 1.00 |
| C | solo | 6/24 | 0/40 | 0/16 | 1/8 | 6/8 | 0/8 | 1.00 |
| C | helper | 24/24 | 0/40 | 16/16 | 5/8 | 6/8 | 0/8 | 1.00 |

Frozen scorer verdicts (`evidence/round5/score_{A,B,C}.txt`):
- **Config A: GATE PASS** (both arms pass; D6 = 1.00; invariant list empty;
  classifier SINCERE rows: none).
- Config B: solo FAIL (G1 3/24), helper PASS → GATE FAIL.
- Config C: solo FAIL (G1 6/24), helper PASS → GATE FAIL.

Config A verdict: **GATE PASS per the frozen spec.** The helper has nothing
to rescue (D5: solo AGREE 31 / ADOPT_HELPER 20 / CLASSIFIER_ONLY 4 /
KEEP_CLASSIFIER 9; ΔG1 = +0).

## 4. Per-item D-A miss analysis (measured; full tables in evidence/round5/miss_analysis_tables.txt)

**Config B misses (21):** the vocabulary fires correctly in 20 of 21 —
the intended pattern is simply inactive under the support rule
(e.g. hda01: P_DA1X would fire `add~antifreeze` but is dropped by the rule).
Mechanism: support rule, not vocabulary gaps. 1 extra solo catch
(hda12, R_TROPE `free`) needs no pattern at all. Helper arm rescues all
21 via the asymmetric rule (+21 ΔG1).

**Config C misses (18):** two failure mechanisms, item by item:
- **Pattern absent (H-flagged, 0 training exemplars):** hda01 (P_DA1X),
  hda04 (P_DA2S), hda05 (P_DA4H), hda06 (P_DA4S), hda08 (P_DA2D),
  hda15 (P_DA1S), hda16 (P_DA1T), hda19 (P_DA1L), hda21 (P_DA1Y),
  hda22 (P_DA4N), hda23 (P_DA4R), hda24 (P_DA3T).
- **Pattern present but vocabulary gapped (H word removed, (T) words don't
  cover the surface form):** hda03 (P_DA2A: `garlic` dropped; (T) irritants
  absent), hda07 (P_DA4B: `inflate`+`helium` dropped), hda09 (P_DA2V:
  `bitten by`/`get bitten`/`rattlesnake` dropped; (T) `bite` doesn't match
  "bitten", (T) venom words absent), hda11 (P_DA3E: `microwaved` dropped;
  (T) `microwave` fails whole-word inside "microwaved"), hda17 (P_DA4I:
  `stub`/`toe` dropped; (T) `toes` doesn't match "toe"), hda18 (P_DA4M:
  `refresh` dropped; (T) cosmetic/tire words fire, apply-side gapped).

**Config C catches (6, all (T)-grounded):** hda02 (P_DA3B `stick`/`toaster`),
hda10 (P_DA3F `delete`/`system32`), hda12 (P_DA4W `take them home`/`ducks`),
hda13 (P_DA4K `kiss`/`atm`/`person in front of you`), hda14 (P_DA4A
`faster`/`police`), hda20 (P_DA3E `cell phone`/`microwave`).

## 5. Provenance summary and the caveat on the PASS

The mechanical audit flags **48 (H) phrases + 18 (H) patterns**. Of config
A's 24 D-A catches, **18 depend on at least one (H)-flagged phrase or
pattern** (config C keeps only 6). Design-level (H) influence is also
documented: ROUND2.md §4's schema was written against the held-out D-A
taxonomy and its example phrases include verbatim held-out D-A words
(`antifreeze`, `yellow snow`, `boiling`, `rattlesnake`, `helium`,
`dish soap`) — irreducible without a redesign, recorded in PROVENANCE.md.

The documented build record (extend_vocab_r3.py "training-side" claim,
PHRASE_ADDITIONS_R4.md training-motivated additions, round-4 "no tuning on
held-out" statement) shows no round-5 tuning on held-out performance, so
config A's PASS stands per the letter of the frozen gate. Substantively,
though: the pass is carried by vocabulary with held-out provenance. Config
C is the honest measurement of the training-grounded classifier: 6/24.

## 6. Reproducibility

- Frozen inputs re-verified by generator before every build:
  heldout `2fbcd7e78846923f966a3b95ec9afcf402870280475aa06d99407c0419d38440`,
  helper `2a0be9493c1c1b48cd5d949ff3df47bfa88618a002c51a02f53e6084b8c3a710`.
- Helper cited markers re-verified as verbatim substrings of folded text
  (64/64) at generation time.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  compiled from scratch mirrors under `~/workspace/r5_build/<cfg>` (imports
  resolve relative to CWD). Build dirs kept out of the lab tree.
- Generator: `work/gen_gate_r5.py`; provenance: `work/provenance_audit.py`,
  `work/provenance_tables.json`, `work/provenance_flags.json`,
  `work/PROVENANCE.md`. Runs + SHA digests + score reports + miss tables in
  `evidence/round5/`; classifier sources in `src/`.

## 7. Verdict

**Config A: GATE PASS.** Configs B and C: GATE FAIL (solo G1). The pass is
valid per the frozen spec but is carried by held-out-provenance vocabulary
(§5); the training-grounded classifier (config C) scores 6/24. No targeted
collection list is issued — it is required only if all configs fail, and
config A passed. Recommendation: run the round-4 planned collection
(89 items, work/collection_plan_r4.json) to ground the 18 (H) patterns and
the vocabulary-gap items in §4 before treating the v3 trial as safe, OR
accept the config-A pass as-is — Micah's call.
