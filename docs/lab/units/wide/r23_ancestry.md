# R23 ANCESTRY RECOVERY + LESSON MAPPING — WIDE EXPLORATION

**EXPLORATORY — NOT EVIDENCE.** Nothing in this document counts as program
evidence, changes any frozen bar/metric/kill criterion, or binds any build.
All claims are tagged **RECOVERED** (with file ID/path) or **INFERRED**
(clearly labeled). Amendment sections are **PROPOSAL** only — Micah's sign-off
required; nothing here alters the prereg.

**Date:** 2026-09-21 (worker session)
**Scope:** R23 Python-era teaching experiments → current teacher arms
(1=peer-handwired, 3=muse-live, 4=sym-hints, 5=sym-yesno-only).
**Standing constraints honored:** prereg frozen items untouched; ZERO randomness
in AI decision paths (this is a read-only archaeology task — no AI decision
paths were built or run); no binaries/`.zagd`/`.zag-cache` touched or committed;
Drive access stayed LIST + DOWNLOAD, read-only, nothing modified/moved/deleted.

## §0 — How to read the tags

- **RECOVERED** — verified from a file I actually read, with its ID/path cited.
  Quotes are verbatim from the source.
- **INFERRED** — my mapping/interpretation, labeled as such. Not evidence.
- **UNRECOVERED-VIA-THIS-PATH** — the material exists but this worker could not
  read it (reason stated). Not confabulated.

---

# PART 1 — RECOVERY (read-only)

## 1.1 What was recovered

### A. `r23_experiments.py` — the R23 teaching-experiment source — RECOVERED

- **Drive file IDs** (four byte-identical copies, 63,069 bytes each):
  `11DrsbgTGNtGDmIZ9_VR3Ja3uIUxZCGEE` (newest, 2026-09-18T05:18:05Z),
  `1noT9Oj2WAos0xVyFbkKFc972XwSVOpZa`, `110W-8PJwb2o3aWgSQpTQwJ_1SicIsNp3`,
  `1A5kddm2o2a4JjdsOmec0i3N3BFlZWixx` (2026-09-18T04:17:04Z → 04:55:49Z).
- **SHA-256:** `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642`
  — **exactly matches** the hash quoted in the V91 exact-recovery note (item B)
  for "original R23 source" from `tnn-pre-v1-r27-general-learning.zip`
  (the user's ChatGPT Library artifact). Provenance chain: ChatGPT Library zip
  → 2026-09-17 V91 exact recovery → four Drive uploads 2026-09-18. One authentic
  source file, four uploads — not four versions.
- **Parents:** three copies sit in folders named `historical_source` (IDs
  `1dGQqtLS3iqTXrSdFpZRkrpDmrywFtrdV`, `1P-0ryuOgP6Or_0fWO20vNybLSBDQmhUx`,
  `1Pv97TyqSgwzHby4kvyTcJWWKEJyVYGRI`); one in `recovery_exact_20260917`
  (`1HESvuwW32p3z_1nYGAFccPpSxpzdfbSG`).
- **Internal structure (793 lines):** a research lineage (`import r22_experiments
  as R22`, `r21_experiments`, `r19_experiments`), checkpoint name
  `TNN_PRE_V1_R23_SEMANTIC_ENGLISH_V1`, and these teaching experiments:
  `strengthened_master_experiment` (L171), `sibling_language_community_experiment`
  (L476), `english_apprenticeship_inversion_experiment` (L504),
  `natural_human_word_transfer_experiment` (L639), `master_fade_experiment`
  (L670), `bounded_teenager_gate` (L684), `cooperative_play_experiment` (L442),
  `social_grounding_experiment` (L435).
- **Stochasticity note (RECOVERED from the code):** the experiments use
  `random.Random(seed)`, `np.random.default_rng(seed)`, and
  `torch.Generator().manual_seed(seed)` throughout. Any R23 numbers would be
  REFERENCE_ONLY at best under the no-randomness law. Design lessons transfer;
  parameters and verdicts do not.

### B. `RECOVERY_EXACT_R23_SOURCE_20260917.md` — the V91 recovery note — RECOVERED

- **Drive file ID:** `1sHyl1TFfFlcipQeQxTha83xSFGYS60U_`, text/markdown,
  3,984 bytes, parent `1s0UUqWtJc_Wpw7tPkKO2w4pIfK3aDJz9`
  (`recovery_exact_20260917` folder), uploaded 2026-09-18T22:21:13Z.
- Records the 2026-09-17 exact recovery of `src/r23_experiments.py` (hash match
  confirmed above), `lineage/r23-accepted-state.pkl`, and `lineage/r23_summary.json`
  from the ChatGPT Library zip. The latter two are **not on Drive** (searched —
  zero hits) and are not in the repo; the V91 note is about a different program
  (V91/R27), so its generator-semantics detail is out of scope here.

### C. Repo git history — R23-era teaching records — RECOVERED

Repo `sylorlabs/TNN`; Python was purged from the native-only checkout in
`9da6e30b` ("Remove historical Python from native-only checkout", 2026-08-29,
19,457 deletions). Searched the pre-purge tree (`28b3c07414f295ea667d236fd770be29ab307f30`)
via `gh-api`; **the R23 source was never in the repo** (only docs). GitHub
commit-message search for "R23" returned **0 results**. Recovered docs:

1. **`Research/tnn-pre-v1-r6-rsi-HARDCODED_ENGLISH_CONTROL.md`** (1,493 bytes) —
   the R6 **installed-dictionary control**: "explicit dictionary insertion for a
   novel label"; results `covered authored grammar exact 1.000 / outside authored
   grammar exact 0.000 / single-typo exact 0.125 / sensory grounding false /
   withdrawal without internal training exact 0.000 /
   co-trained raw-text substrate after withdrawal 0.9375`. Verbatim conclusion:
   *"A temporary scaffold may accelerate acquisition, but the scaffold itself
   does not solve grounding, transfer, pragmatics, natural speech, or
   open-domain English."* And: *"It cannot contribute to any TNN production gate."*
2. **`Research/R30_FINAL_REPORT.md`** §7 "Master teacher" — *"A diagnostic Master
   can materially improve hard performance when targeting learner failures.
   Over-fine targeting can fill finite episodic capacity with repeated hard cases
   and damage broad coverage. The correct direction is therefore a
   **capacity-aware diagnostic Master with explicit diversity protection**, not
   purely random teaching and not hard-example-only teaching."*
3. **`Research/R31_HANDOFF.md`** L123 — *"The Master can select experiences that
   expose confusions, contrasts, and information gaps, but **may not provide
   word/phoneme/chunk boundaries**. Capacity-aware teaching must preserve
   diversity and not flood episodic/chunk memory with repeated hard examples."*
4. **`Research/R31_HARDCODING_LEDGER.md`** — "Chunk boundaries: learned,
   TNN-recruited spans… boundary: **no VAD/word/phoneme boundaries supplied**";
   "Transformer/BPE/tokenizer/LLM: absent — prohibited from TNN cognition."
5. **`Research/TNN_R27_NATIVE_MASTER_RESULTS.md`** — adaptive (diagnostic) master
   vs random/diverse teaching dose curve: dose 8 → 68.57% vs 63.87%; 16 → 75.31%
   vs 69.25%; 32 → 82.06% vs 77.51%; 64 → 86.54% vs 82.85%; 128 → 87.92% vs
   88.34%; 256 → 89.94% vs 89.57%; 512 → 89.89% vs 90.93%. Verbatim: *"This
   supports strong diagnostic teaching early, then diversification/withdrawal
   rather than permanent Master control."* Sibling-teaching reference:
   passive description identification **96.45%**, with one discriminating
   question **98.08%** ("high but below 100%, and remains external reference
   evidence").
6. **`Research/TNN_MASTER_ARCHITECTURE_PLAN_R27_COMPLETION.md`** — verbatim:
   *"**Hardcoded Master is permitted as teacher, not learner.** Teacher knowledge
   cannot be counted as TNN competence and must be withdrawn before
   qualification."*; *"A novel spoken or byte-level name binds to an existing
   persistent entity/event/relation representation — **not to a separate
   dictionary slot**."*; *"The Master progressively withdraws. Final
   qualification contains no Master answers."*; teaching policy *"Can be promoted
   … if it improves learning after withdrawal. It never counts as runtime
   learner competence itself."*

### D. `ghost#1` — UNRECOVERED-VIA-THIS-PATH

- **Drive file ID:** `1sQxMCSozdUcRif-sht7e32z3e8wIWkKuA5RNdzsvWRA`,
  Google Doc named `ghost#1`, created 2026-05-17T00:30:08Z by Micah Cooley,
  lives in shared drive `0AD_unOoOKH-yUk9PVA`. It matched Drive `fullText
  contains 'vocabulary'`.
- **Why unreadable:** the Google Docs connector is `not_connected` (requires the
  user's tap on the connect link — not available to this worker), and the Drive
  skill explicitly forbids exporting Google-native files through Drive. Only
  metadata was read (read-only, permitted). No contents are claimed here.
- **What this means:** whatever R23-era vocabulary notes ghost#1 holds remain
  unrecovered by this worker. The recovery above stands on the code + repo docs.

### E. What was NOT recovered

- **No R23 run verdicts.** `r23_summary.json`, `r23-accepted-state.pkl`, and the
  `tnn-pre-v1-r27-general-learning.zip` are absent from Drive and absent from
  repo history. The code defines gates (e.g. `ENGLISH_APPRENTICESHIP_INVERSION:
  PASS_BOUNDED if tnn_taught.overall > master_taught.overall else PARTIAL`) but
  **no output values were recovered — I claim no R23 verdict numbers.**
- `GATE_FAILURES.md` (2026-08-23, native-gate release log) mentions
  `run_zag_apprenticeship.sh` and missing `results/zag-apprenticeship.json` /
  `results/english-zag-byte-training.json` — tangential (native-era gate
  scaffolding), not R23 teaching results. Listed for completeness.

### F. Provenance anomalies flagged (INFERRED — pattern observation, not accusation)

- The `r23_blake2b64_person_v1.zag` / `r23.pkl` / `extract_nested_r23.{argv,stdout,
  stderr,exit}` cluster and eleven `nested_r23` folders were uploaded in tight
  bursts (2026-09-18T22:21:04–15Z within seconds; folders created 2026-09-20
  19:25:20–29:14Z). A sampled `nested_r23` folder holds model weight tensors
  (`rnn.weight_ih_l0.f32le`, `interpreter.W.f32le`, `bpe.framed.bin`, …) — this
  is the **R23 identity-hashing line (arm-K territory), not teaching material**,
  and I drew no teaching lessons from it. The burst pattern is consistent with
  an automated archival/red-team run rather than the August Python era; treat
  anything in that cluster as lower-provenance unless independently verified.
- Drive-wide `fullText contains 'apprenticeship'` also matched August-era files
  (`GATE_FAILURES.md`, `final-summary.json`, `gate-status.json`, 2026-08-23) —
  those two JSONs downloaded as 0 bytes via `alt=media` (Drive returned no
  size/content); their contents are unverified, so nothing is claimed from them.

## 1.2 The recovered R23 teaching design (all RECOVERED from code, verbatim where quoted)

**The "no English dictionary" boundary.** `AnonymousGroundedLearner`'s docstring:
*"Mutable learner stores only parameters + replay. English strings/labels live
in the teacher/evaluator."* The learner holds generic byte-to-event weights;
the teacher/evaluator owns the curriculum and grounding.

**The inversion experiment.** `english_apprenticeship_inversion_experiment`
compares **master-taught** vs **TNN-taught** children: a strong master vs a
mature peer that *"varies surface from its own learned neighborhood."* Its
`boundary` string is the experiment's own verdict on what it tests: *"English-
specific teacher inversion on anonymous mutable learners; both teachers use
externally grounded consequences, **no English dictionary installed into
child**."* (L504–524). The gate: `PASS_BOUNDED` iff the TNN-taught child beats
the master-taught child — **the gate definition is recovered; the result is not.**

**The strengthened master.** `_teacher_train`'s `STRONG_DIAGNOSTIC_MASTER`
diagnoses low-margin or underexposed concepts, rotates paraphrase surfaces,
emphasizes contrast after confusion, and — critically — **every lesson pairs
language with an independent grounded consequence**
(`L.update(t, W.event((c,)), .75, 'MASTER')` immediately followed by
`L.update(t, W.event((c,)), 1.0, 'DIRECT_WORLD')`). It is compared against
`R22_STYLE_MASTER` (random curriculum), `MASS_MASTER` (overconcentrated
blocks), and `SYMBOLIC` (rejection-only). The symbolic gate:
`FAILED_TO_IMPROVE` if symbolic overall < .20; promotion of the diagnostic
master requires `symbolic_gap ≥ .40`.

**Evidence trust tiers.** `source_rel = {'DIRECT_WORLD': 1.0, 'MASTER': .75,
'SIBLING': .55}` — direct experience outranks teacher, teacher outranks peer.

**The fade experiment.** `master_fade_experiment` intervenes only on learner
error/low margin and reports `intervention_rate_by_quarter` — **teacher
withdrawal as a measured trajectory**, with the gate requiring the rate to
decay and `final_accuracy ≥ .90`. Boundary: *"teacher has English but mutable
learner does not."*

**Sibling teaching.** `sibling_language_community_experiment`: four independent
learners share sourced language evidence; the **receiver asks about its
lowest-margin probes**; sender shares surfaces **with provenance**; the
receiver keeps sibling evidence at weight **.45** *"until locally checked"* by
a direct consequence. Includes a **misinformation trap**: five repeated copies
from one origin vs one direct consequence — boundary: *"same-source repetition
is low authority relative to direct consequence."* Gate: `gain ≥ .10 AND
misinformation_recovery ≥ .90`.

**Cooperative play.** `cooperative_play_experiment`: NO_LANGUAGE vs SYMBOLIC
(yes/no rejection-only) vs MASTER_LANGUAGE vs SIBLING_LANGUAGE. Boundary:
*"language is useful because it reduces action cost, **symbolic rejection is a
negative control**."* Yes/no-only teaching was the experiment's **negative
control**.

---

# PART 2 — LESSON MAPPING (INFERRED unless marked RECOVERED)

Arms: **1** = peer-handwired · **3** = muse-live · **4** = sym-hints ·
**5** = sym-yesno-only. "Supports" means the R23-era record agrees with the
current design; "tension" means a genuine conflict or gap, written up as a
non-binding amendment PROPOSAL in §3. Nothing here softens a frozen bar.

## Arm 1 — peer-handwired: SUPPORTED (with one gap → PROPOSAL C)

- **INFERRED:** R23's sibling design is the direct ancestor of arm 1's "peer
  teacher" concept: peer evidence is real teaching **iff** it carries
  provenance, is held at reduced authority until locally verified, and loses to
  direct evidence on conflict (tiers 1.0 / .75 / .55, RECOVERED). The current
  arm-1 design — hand-wired fixture teacher, flaw manifest, §P iron rules,
  §C tripwire, disconnect test — is the stricter, deterministic-native version
  of the same idea. The 2026-09-21 amendment's rationale ("separates possession
  from learning") is exactly the R23 L2 boundary: the teacher may *possess*
  English; the learner must *learn* it.
- **INFERRED:** R23 adds a design the current prereg lacks on the learner side:
  the receiver **asks about its lowest-margin probes** (learner-initiated
  questioning). The current protocol is teacher-initiated (teacher proposes;
  learner adopts/revises/rejects/defers; appeal exists). A learner-side crew
  could consider an uncertainty-query channel — flagged here as an idea for the
  learner-machinery crew, not a teacher-arm change, and not a proposal against
  any frozen item.
- **Gap → PROPOSAL C:** the R23 misinformation trap (repeated same-origin
  false claims vs one direct consequence) has no counterpart in the current
  flaw-manifest taxonomy.

## Arm 3 — muse-live: SUPPORTED, but underspecified → PROPOSAL D

- **INFERRED:** `STRONG_DIAGNOSTIC_MASTER` is the ancestor specification of
  what "natural teaching" (T-7: "no flaw manifest (natural teaching only)")
  should actually do: **diagnose** low-margin/confused concepts; **rotate**
  paraphrase surfaces; **emphasize contrast after confusion**; **pair every
  lesson with an independent grounded consequence** (language update + direct
  world update, never language alone); **capacity-aware targeting with explicit
  diversity protection** (R30 §7, RECOVERED); **fade after foundations**
  (master_fade, RECOVERED). The current prereg leaves arm-3 behavior
  underspecified — R23 supplies the ancestor contract.
- **INFERRED:** R23 pairs language with grounded consequence on *every* lesson,
  which is the same requirement the current §L adopt rule (2) enforces on the
  learner side (corroboration by a source independent of the proposing
  teacher). Consistent, not contradictory.
- **INFERRED:** the R27 dose curve (adaptive master beats random/diverse early,
  then closes/reverses by dose 128–512; RECOVERED) predicts arm 3's claim is
  **acceleration, not ceiling** — which is precisely what the prereg measures
  (M2 episodes-to-criterion) and ends with (teacher withdrawal/disconnect).
  Supports the current framing.

## Arm 4 — sym-hints: no contradiction; R23-derived prior (INFERRED)

- R23 has no hints-only arm. The closest data point is the `SYMBOLIC`
  (rejection-only) policy, which lost badly (`FAILED_TO_IMPROVE` gate at < .20;
  promotion required `symbolic_gap ≥ .40`). Hints carry strictly more
  information than rejection-only, so R23 does **not** predict arm-4 failure —
  but its prior is that **rich diagnostic teaching > symbolic signals**.
- No-free-lunch demands arm 4 be tested anyway (RULE-2). The R23 prior becomes
  a checkable prediction: on mastery, arm 4 should sit between arm 5 and arm 3.
  If it beats arm 3, the diagnostic-master claim is falsified in this program —
  that is the point of testing.

## Arm 5 — sym-yesno-only: SUPPORTED as a test; predicted to lose (INFERRED)

- **RECOVERED:** R23 used yes/no-only teaching **explicitly as the negative
  control** (`cooperative_play_experiment` SYMBOLIC mode; *"symbolic rejection
  is a negative control"*). Including arm 5 is exactly the "test both"
  discipline (RULE-2): the honest control must run alongside the serious arms.
- **INFERRED prediction:** arm 5 loses on mastery but earns its place as the
  control — if arm 5 ever wins, the richer arms' mechanisms are suspect. No
  contradiction with any frozen item; the R23 record supports the current
  inclusion of arm 5 and sharpens what its loss would mean.

## What "no English dictionary installed into child" implies for installed-vs-learned

**RECOVERED chain, oldest to newest:**
1. R23 inversion boundary string (verbatim): *"no English dictionary installed
   into child"* — installation was the experiment's excluded condition, not a
   variable.
2. R6 prosthesis control: an installed dictionary scores **1.000 on covered
   grammar / 0.000 outside it / 0.000 on withdrawal without internal training**
   — the old program's empirical answer to "what does installed buy": **fake
   fluency, zero transfer**. It *"cannot contribute to any TNN production gate."*
3. R6's co-trained substrate after withdrawal: **0.9375** — the direct ancestor
   of the current law *"learned = persists after disconnect."*
4. R27 plan (verbatim): *"Hardcoded Master is permitted as teacher, not
   learner… must be withdrawn before qualification"*; *"binds to an existing
   persistent entity/event/relation representation — not to a separate
   dictionary slot"*; *"Final qualification contains no Master answers."*

**INFERRED implication:** the current installed-vs-learned ruling (default
learned; trainer force-install = visible, audited force-pin; learner can
reverse everything else; taught is a *route* to learned, never a quiet form of
installed) is the native-program restatement of the R23 boundary. The teacher
arms already comply: taught words arrive judgment-held at provisional
strength, §L gives adopt/revise/reject/defer, §C blocks tokenizer smuggling,
arm O's kill criterion (ii) is the disconnect test. **Nothing in the R23
record contradicts the ruling; all of it supports it.** The one gap is
instrumental — the fade trajectory (see PROPOSAL B).

---

# §3 — AMENDMENT PROPOSALS (non-binding; Micah's sign-off required)

None of these change, reinterpret, or soften any frozen bar, metric, or kill
criterion. Each touches only items that are still open (§0 T-3/T-5/T-7) or
adds an instrument.

## PROPOSAL A — Scope the R31 "no word boundaries from the Master" rule

**Genuine tension (RECOVERED texts):** `R31_HANDOFF.md` L123 says the Master
*"may not provide word/phoneme/chunk boundaries"* and the R31 hardcoding
ledger pins *"no VAD/word/phoneme boundaries supplied."* The current teacher
track's arm 1 (peer-handwired) is built around `WORD_SPAN` proposals — the
teacher literally proposes word spans. Letter vs spirit: the R31 rule's spirit
(no segmentation *authority* handed to the learner) is preserved by §P iron
rules 1–2 ("spans only, no commands"), §L (learner disposes), and the §C
tripwire — but the letter is in tension with WORD_SPAN proposals.
**Proposed resolution:** record explicitly that the R31 rule governs the
endogenous-chunking track's Master; in the teacher track, §P WORD_SPAN
proposals are *candidate spans* under "teacher proposes, TNN disposes," never
segmentation authority. Alternatively Micah may extend the prohibition to the
teacher track — his word either way. The two texts should not stay in silent
tension.

## PROPOSAL B — Teacher-dependence-decay instrument

**Gap (RECOVERED design, INFERRED gap):** R23's `master_fade_experiment`
measured the teacher's intervention rate *by quarter* (trajectory, not a
single event); the R27 plan required *"The Master progressively withdraws.
Final qualification contains no Master answers."* The current arm-O learned-
verdict is binary (kill criterion ii: post-scaffold M1 < 99.5% → "learned"
claim dead). A binary disconnect test can pass while the learner still depends
on the teacher for hard cases — partial dependence would be invisible.
**Proposed:** add a dependence-trajectory instrument to the teacher track —
e.g. teacher intervention / needed-appeal rate per curriculum quartile must
decay, and a taught word that survives only under sustained high intervention
is scored as not-learned. Additive instrument; no bar changed, none softened.

## PROPOSAL C — Misinformation-trap flaw item

**Gap (RECOVERED design):** the R23 sibling experiment's misinformation trap —
five repeated same-origin false claims vs one direct consequence, gate
`misinformation_recovery ≥ .90` — has no counterpart in the current flaw
manifest. The open T-3 taxonomy (4 wrong-span, 4 false-confidence,
2 missing-grounding, 2 plausible-false) tests false *words*, not false
*evidence with provenance*. **Proposed:** add one misinformation-trap item to
the sealed manifest (affects open items T-3/T-5 only): the teacher repeats a
false claim from a single origin across turns; the learner must weight
same-source repetition below independent evidence and REJECT/REVISE on the
record.

## PROPOSAL D — Arm-3 diagnostic-teacher bounds

**Underspecification (RECOVERED ancestor, INFERRED mapping):** §T-7 currently
bounds arm 3 as "obeys §P + §C; no flaw manifest (natural teaching only)."
R23's `STRONG_DIAGNOSTIC_MASTER` is the ancestor contract for what natural
teaching does: diagnose low-margin/confused concepts; rotate paraphrase
surfaces; emphasize contrast after confusion; pair every lesson with an
independent grounded consequence; capacity-aware targeting with explicit
diversity protection (R30 §7); fade after foundations. **Proposed:** extend
§T-7 with that specification (affects open item T-7 only). Without it, "muse-
live" is a vibes arm and the R23 lineage's main teaching lesson is unused.

---

# §4 — Caveats and qualifications

- **All R23 numbers are REFERENCE_ONLY at best** (seeded RNG, Python, a
  72-concept synthetic English world of `FOUNDATION` words — not open English).
  No R23 run verdicts were recovered; none are claimed.
- The inversion experiment compared *teacher policies* (master vs mature
  peer), not installed-vs-learned as a variable; the "no dictionary" condition
  was its design boundary, and the installed-vs-learned mapping above is
  INFERRED from that boundary plus the R6/R27 records — stated as such.
- The four Drive `r23_experiments.py` copies are byte-identical (SHA-256
  match with the V91 exact-recovery hash) — one source file, four uploads.
- `ghost#1` remains UNRECOVERED-VIA-THIS-PATH (Docs connector not connected;
  export via Drive forbidden). Its vocabulary contents could add, subtract, or
  reframe any lesson above — the mapping is conditional on what was actually
  read.
- The `nested_r23` / blake2b64 cluster is identity-line material (arm-K
  territory), uploaded in tight bursts 2026-09-18/20; it was listed, not used.
- R23's "English" was grounded in a synthetic 72-dim event world
  (`EnglishWorld`); the current program's corpora are Shakespeare prose and
  `sqlite3.c` code. Lessons about *teaching protocol* transfer; lessons about
  *English* do not.

**Files produced:** this document only —
`~/workspace/tnn-lab/units/wide/r23_ancestry.md`. Not committed (per task).
