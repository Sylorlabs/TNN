# EXP_PREREG — H7 expanded sincere-hypotheticals experiment (exp2c)

**Status:** PREREGISTERED 2026-09-27. Frozen at commit; no 2c/expansion run
may precede the commit of this file. (Stage 0 is a reproduction of the
already-frozen, already-reported Crew 2 result — its expected values are
public in `utterance_types/crew2/docs/FINAL_REPORT.md` — and is re-run after
this commit as the official baseline.)
**Authorization:** Micah, 2026-09-27 — "test more" on the H7
sincere-hypotheticals broader fix. This is an EXPERIMENT, not a prereg
amendment: nothing here changes the frozen H7 prereg's bars, and no result
here enacts anything.
**What stays on hold:** the two-heads architecture split, the content-only
definition lock, and the unscored-question eval rule — none is built or
tested in this experiment. The learner MECHANISM is frozen: the only code
change is additive Phase-2c episode delivery in a copy of the learner
(`h7_exp2c.zag`); `h7_main.zag` is never edited.

## 1. Background and the question

Crew 2's frozen result: hypothetical SINC lookalikes 3/10 (bar ≥9/10);
every other §5c bar passes. Root cause: 2-gram markers (`if the`, `do we`,
`it is`) learned from hypothetical exemplars also occur in sincere
discourse, and the frozen endorse pool (20 facts + 20 calib) never shows
them in sincere use — the "missing bit" of the 2b impossibility proof.
The broader-fix corpus (48 FL2 episodes, `broaderfix/crew2/`) supplies the
missing bit as teaching data. Its own proposal is honestly pessimistic:
under the frozen bare-bigram representation the corpus is "bar-neutral at
best", and it gates family C on a scope-split demo that does not exist.

**This experiment asks, by running:**
1. Does the 48-item corpus move `sinc_lk_3` under the FROZEN mechanism,
   and at what price to the other bars? (Stage 1)
2. Does the gated/ungated distinction matter — run BOTH and report both.
   (Stage 1)
3. Does the delivery MODE matter — per-episode contradiction revocation
   only (design α) vs episode + endorse-pool append + calibrate (design β)?
   Does episode ORDER matter (E-then-W vs W-then-E)? (Stage 1)
4. Does the method generalize to NEW marker families derived from the
   learner's own marker set, and does more volume help or churn?
   (Stage 2)

## 2. Frozen references

- Frozen prereg: `docs/lab/epistemics/utterance_types/PREREG_H7_FROZEN.md`
- Baseline: `docs/lab/epistemics/utterance_types/crew2/docs/FINAL_REPORT.md`
  (SHA256 `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`,
  H7_FAILURES=1, `sinc_lk_3`=3/10)
- Learner: `utterance_types/crew2/learner/h7_main.zag` (frozen, never edited)
- Corpus: `utterance_types/broaderfix/crew2/calibration_corpus_items.txt`
  (cc01–cc48) + `CALIBRATION_CORPUS_PROPOSAL.md`

## 3. Runner: h7_exp2c.zag (additive only)

`h7_exp2c.zag` is a byte-copy of `h7_main.zag` plus:
- (a) `learn_sincere(...)`: the frozen FL2 sincere-episode rule. Learner
  predicts; teacher corrects toward ENDORSE. If predict=ENDORSE: correct,
  nothing installed (audit rc=0). If predict=WITHHOLD(type T):
  contradiction — revoke every live marker of T firing on the episode's
  fields (the exact loop from `learn_exemplar`'s wrong-type path; audit
  rc=1). No type-name strings, no keyword lists, no type constants in
  control flow — generic over the taught concept index.
- (b) Phase 2c block between the Phase-2b loop and Phase 3: reads the 2c
  item file for the selected mode, delivers one FL2 episode per item in
  file order (E→`learn_sincere`; W→`learn_exemplar(ti)` + `typed_write`
  into the typed session partition with the taught concept's name and said
  flag, exactly as 2b exemplars are written), then one `calibrate()`.
  Item format: `id|speaker|ctx|utterance|signal|ti` — `ti` is the taught
  concept INDEX (0=sarcasm,1=joke,2=hypothetical,3=quotation,4=roleplay;
  from `types.txt` order), an integer read from data, never a code
  constant. For E items `ti` is ignored.
- (c) Post-2c scoring: after 2c, re-score TR/PA/NO (20 each), SINC-DP,
  SINC-LK per type at final state and emit `2C_CURVE` lines plus `2C_`
  bar checks (`2c_learn_bar_N`, `2c_learn_nomem_N`, `2c_learn_nodis_N`,
  `2c_sinc_dp_N`, `2c_sinc_lk_N`) using the §5c thresholds. The frozen
  (viii) checks still run on the pre-2c curve array (they measure the
  frozen adjudication point); the `2C_` checks are the post-calibration
  adjudication the corpus proposal calls for. Phase 3 batteries
  (fact recall, NEST, FHYP, cross-type interference, leak audit +
  paraphrase, suppression, unfiltered-caller guards) run AFTER 2c, so
  they measure post-calibration state.
- (d) `MDUMP` block: emits every marker (concept idx+1, field, status,
  support, bytes) — read-only observability for Stage-2 derivation and
  mechanism analysis. The frozen `RULEDUMP` block is kept as-is.
- (e) `argv[2]` mode select (`""`/absent = `base`).

**Frozen-behavior proof:** `base` mode must reproduce the frozen run
byte-identically (SHA256 `71731400…5407`, H7_FAILURES=1). If it does not,
the build is rejected and no 2c cell runs.

**HARD0:** `h7_exp2c.zag` must pass the KB-H7-HARD0 static audit with no
new hits beyond the frozen file's adjudicated filename-prefix false
positives. The audit is committed as evidence.

**Capacities** (constants only, no logic change): endorse pool
`ient` 64→160 entries / `ipool` 32768→65536 bytes; 2c item list sized for
128 entries. Needed for the volume leg (88 endorse entries).

## 4. Stage 0 — baseline rerun

Frozen `h7_main.zag` + frozen curriculum, 3 reps, SHA256 per rep.
Expected: 3 byte-identical reps at SHA
`71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`,
H7_FAILURES=1, `sinc_lk_3` check 0/1 (3/10), all other checks pass
(TR/PA/NO 20/20 at 32 ex for all types, SINC-DP ≥9/10 all types,
SINC-LK 9–10/10 on types 1,2,4,5, phase-3 fact recall 20/20,
leak 0 + negctl live, supp 5/5, NEST/FHYP pass, learn bars 1–5 pass).
**Gate: any deviation → STOP, report, no further stages.**

## 5. Stage 1 — the 48-item corpus

### 5.1 Item files (exact corpus text + `ti` field)

- `cal_ab.txt`: cc01–cc32 (families A+B). W items: `ti=2` (hypothetical).
- `cal_c.txt`: cc33–cc48 (family C). W items: `ti=1` (joke).
- `cal_abc.txt`: cc01–cc48.
File order per family is E×8 then W×8 (the corpus file's order).

### 5.2 Designs

- **Design α (episode-only):** per-episode FL2 correction; the endorse
  pool is UNCHANGED (frozen 40); one `calibrate()` after the block.
- **Design β (episode + pool):** as α, plus every E item is appended to
  the endorse pool (lowered bytes, ev=0) as delivered, so the post-block
  `calibrate()` applies the frozen precision gate to the new sincere
  data. This is the "missing bit as data through the frozen FL2
  machinery": the bit is consumed by `calibrate`'s precision gate and by
  per-episode contradiction revocation. Both designs use only frozen
  machinery; β's pool append is `ilist_add`, the same call the frozen
  code uses to build the pool.

### 5.3 Legs (each: 3 reps, SHA256 per rep; divergence → cell INVALID)

| Leg | Mode | Items | Design | Order |
|---|---|---|---|---|
| L1 | `ab-a` | A+B (cc01–32) | α | E-then-W |
| L2 | `ab-b` | A+B (cc01–32) | β | E-then-W |
| L3 | `abc-a` | A+B+C (cc01–48) | α | E-then-W |
| L4 | `abc-b` | A+B+C (cc01–48) | β | E-then-W |
| L5 | `ab-a-rev` | A+B (cc01–32) | α | W-then-E (reverse per family) |

### 5.4 Mechanism analysis (preregistered; verified against the MDUMP)

Pre-2c, the hypothetical concept's live markers include the bare bigrams
`if the`, `do we`, `it is` (status 1 — the frozen RULEDUMP emits
nothing, so no marker ever reaches status 2; all learning is provisional)
plus governor markers (`suppose that`, `imagine if`, `what if`,
`let us say`, …) and longer n-grams. The 7 SINC misses fire on the bare
bigrams only.

- **L1 (ab-α, E-then-W):** E episodes revoke the firing hypothetical
  markers per item — `if the` (family A) and `do we` (family B) go to
  status 3. W episodes then `learn_exemplar(ti=2)`: with the bare bigrams
  dead, W items mostly miss and install fresh provisional markers
  (`say that`, `that if`, `assume if`, `where do`, `how do`, `what do`,
  …); `marker_add` does NOT resurrect status-3 entries, so `if the` /
  `do we` stay dead. Post-block `calibrate()` (frozen pool) commits
  support≥2 W markers. **Predicted:** `sinc_lk_3` → 9–10/10. Risks:
  (R1) a W-installed marker fires on a frozen SINC probe (checked
  post-hoc; predicted low — W-item neighborhoods were authored disjoint
  from probe neighborhoods); (R2) hypothetical TR/PA/NO items that
  depended SOLELY on `if the`/`do we` flip to ENDORSE (2C learn_bar_3
  dip); (R3) W-installed markers (`how do`, `where do`) fire on other
  types' probes (cross-type interference dip).
- **L2 (ab-β):** as L1, plus `calibrate()` revokes EVERY live marker
  matching any E item (not only ones that fired during episodes — e.g.
  markers of other types matching E-item bytes). Broader revocation
  surface. **Predicted:** `sinc_lk_3` → 9–10/10, at least as robust as
  L1; strictly more churn risk on non-hypothetical bars (R3 amplified).
- **L3 (abc-α):** + family C. E episodes revoke firing joke markers on
  `it is` items (`it is` → status 3 on joke AND hypothetical — si3_15 was
  withheld as hypothetical). W episodes install fresh joke markers.
  **Predicted:** `sinc_lk_3` → 10/10; joke bars at RISK — `2c_sinc_lk_2`
  and/or `2c_learn_bar_2` may dip (proposal §6: `it is` is load-bearing
  on joke items ex2_02/ex2_05/pa2_05). This leg prices the gated/ungated
  distinction.
- **L4 (abc-β):** as L3 with the broader β revocation. **Predicted:**
  `sinc_lk_3` → 10/10; joke regression risk highest here (mode-3
  tradeoff made visible: `sinc_lk_3` up, joke bars down).
- **L5 (ab-α, W-then-E):** W episodes run while `if the`/`do we` are
  still live → W items predict correctly via the bare bigrams → NO new
  markers installed; then E episodes revoke the bare bigrams. Net:
  `if the`/`do we` dead, zero marker churn. **Predicted:** `sinc_lk_3` →
  9–10/10 with the CLEANEST other-bar profile (no R1/R3 surface) —
  possibly the best leg. If L5 ≥ L1 on `sinc_lk_3` with fewer bar
  movements, order is load-bearing and the E-then-W file order is
  suboptimal.

**Honest projection for Stage 1:** the corpus proposal projects 9/10
(A+B) / 10/10 (+C or ruling); the 2b proof projects bar-neutral-at-best
under bare bigrams. This experiment's mechanism analysis predicts
**8–10/10 on L1/L2/L5 and 9–10/10 on L3/L4**, with the price (if any)
paid on joke bars (L3/L4) or hypothetical NO (L1/L2/L5, R2). A result of
≤5/10 on all of L1–L5 would CONFIRM the proof's pessimism (the missing
bit is not consumable through the frozen FL2 machinery at all).

### 5.5 Full bar set measured per leg

Per-type TR/PA/NO at final state (2C_CURVE), `2c_learn_bar_N`,
`2c_learn_nomem_N`, `2c_learn_nodis_N`, `2c_sinc_dp_N`, `2c_sinc_lk_N`
(N=1..5); Phase-1 fact recall 20/20 + fact predict 20/20;
KB-H7-LEAK1 substring audit (0 hits) + paraphrase audit (0 hits) +
negative control live; KB-H7-SUPP1 5/5; NEST verdict 20/20 + said-bytes
20/20; FHYP 20/20; cross-type interference ≥16/20 per type;
unfiltered-caller guards; HARD0 (once per source build, not per cell);
determinism 3/3 byte-identical + SHA256 per rep.

## 6. Stage 2 — expansion ("test more")

### 6.1 New marker families (D, E, [F])

**Derivation rule (frozen before Stage-2 runs):** from the Stage-0 MDUMP
(base mode — frozen mechanism, proven byte-identical), take live
hypothetical markers (status 1; field 0 = utterance) excluding the three
known families (`if the`, `if we`/`do we`, `it is` and their 3-gram
extensions). A marker founds a new family iff it occurs in NATURAL
sincere sentences absent from the frozen endorse pool AND a genuine
hypothetical use of the same bigram exists. Each family: 8 ENDORSE + 8
WITHHOLD items, same anti-confound rules as the corpus (below). Target
2–3 families; if fewer than 2 markers qualify, report that as a finding
("no further sincere-colliding markers in the learned set") and run the
volume leg only.

**Anti-confound verification (deterministic script, committed):**
- zero shared ≥16-byte substrings between any new item and any of: all
  frozen utterances (exemplars, probes, calib, facts, supp, nest, fhyp,
  paraphrases), all 48 corpus items, all other new items;
- every item contains its family's target bigram under the learner's
  tokenizer (lowercased `[a-z0-9]+` runs);
- speakers rotated through the six frozen names on both polarities;
- ctx from the sincere pool (`says evenly`/`says plainly`) on both
  polarities; no type labels;
- no new item within 16 bytes of any of the 7 miss utterances.

Legs: L8 `de-a` (new families, design α), L9 `de-b` (design β).
**Predicted:** neutral on frozen bars (anti-confound rules prevent
probe collisions by construction); the value is methodological — does
the 2c delivery fix FRESH marker collisions the same way? Each new
family's E items must flip from WITHHOLD→ENDORSE post-2c (measured as
an 8/8 diagnostic, not a frozen bar).

### 6.2 Volume leg

48 NEW items: 8+8 per family on the ORIGINAL three families A/B/C
(same anti-confound rules; disjoint from cc01–cc48 by the 16-byte rule),
delivered as one 96-item block (corpus 48 + 48 new). Legs: L6 `vol-a`
(design α), L7 `vol-b` (design β).
**Predicted:** `sinc_lk_3` no better than L1–L4 (ceiling effect);
churn risk rises with volume (more W-installed markers → more R1/R3
surface; β pool grows to 88 entries → broader revocation). Tests "does
more data help or churn" — expected answer: churn-neutral to
churn-negative, i.e. 8+8 is already at/over the effective dose.

### 6.3 Predictions lock

After the Stage-0 MDUMP analysis and before ANY 2c run, the concrete
new-family items + a `PREDICTIONS_LOCKED.md` (per-probe firing analysis:
which live markers fire on which probes pre-2c, and the resulting
per-leg per-bar point predictions) are committed. The conditional
predictions in §5.4/§6 become unconditional there.

## 7. Stop / invalid rules

- Stage-0 gate fails → STOP, report, no 2c runs.
- Any leg with non-identical rep SHAs → cell INVALID (not failed);
  investigate, do not score.
- HARD0 new hit in `h7_exp2c.zag` → build rejected, no runs.
- Anti-confound script failure on new items → items rejected, re-author.

## 8. Evidence and commit

All evidence under `docs/lab/epistemics/utterance_types/exp2c/` on
branch `tnn-native-lab`:
`EXP_PREREG.md` (this file), `PREDICTIONS_LOCKED.md`,
`items/cal_ab.txt`, `items/cal_c.txt`, `items/cal_abc.txt`,
`items/cal_vol_new.txt` (48 volume items), `items/cal_de_new.txt` (new
families), `items/verify_anticonfound.py` (+ its report),
`src/h7_exp2c.zag`, `src/hard0_scan.txt`,
`cells/<leg>/rep{1,2,3}.txt` + `cells/<leg>/sha256.txt`,
`bartable.md` (full bar × leg table), `REPORT.md`.
No binaries, no `.zagd`, no `.zag-cache`. After push, verify by walking
the tree non-recursively (never trust `?recursive=1` listings).

## 9. Verdict questions the report must answer

1. Did `sinc_lk_3` move, per leg? Numbers, not vibes.
2. What traded against what (full bar table per leg)?
3. Is the broader fix REAL — i.e. does the missing bit get consumed
   through the frozen FL2 machinery, and in which delivery design?
4. Verdict on the 6–9/10 projection: confirmed / refuted / refined.
5. What surprised the preregistered predictions?
6. Recommendation: is there a delivery configuration worth keeping as a
   (still-experimental) teaching-data option, and what remains on hold.

---
Preregistered 2026-09-27 by the exp2c experiment crew. Enacts nothing.
