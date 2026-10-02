# H7 Crew 2b — Impossibility Proof: the `sinc_lk_3` ceiling is genuine

**Verdict: IMPOSSIBLE under KB-H7-HARD0 + the task's mechanism-level constraints.**
No HARD0-clean, non-`if`-specific, non-item-specific mechanism can raise
hypothetical SINC-LK to ≥9/10 without regressing frozen bars (specifically
`learn_bar_2`, joke NO ≥16/20). The minimal distinguishing information required
is uncomputable from the frozen exemplar/curriculum structure.

**Date:** 2026-09-24
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
**Baseline SHA256 (3 byte-identical reruns):**
`71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`
**H7_FAILURES (baseline):** 1 — sole failure `sinc_lk_3` (hypothetical SINC-LK 3/10)

---

## 1. Exact failure anatomy

At 32 exemplars, hypothetical SINC-LK scores 3/10. The 7 misses, with the single
firing marker in each case (from instrumented run `h7_dbg`, marker table `dbg2.txt`):

| Item | Utterance | Firing marker | Concept |
|------|-----------|---------------|---------|
| si3_12 | "What time do we leave?" | `do we` | hypothetical |
| si3_13 | "I wonder if the mail came." | `if the` | hypothetical |
| si3_14 | "Ask if the shop is open." | `if the` | hypothetical |
| si3_15 | "It is as if winter came early." | `it is` | **joke** |
| si3_16 | "See if the door is locked." | `if the` | hypothetical |
| si3_18 | "Check if the oven is off." | `if the` | hypothetical |
| si3_20 | "We will see if they reply." | `if the` | hypothetical |

Every miss is a **lone provisional content-marker fire** (field 0, support 1,
status provisional). The learner's `predict()` routes WITHHOLD on any single live
marker. This is not an `if`-only problem: `do we` and joke's `it is` participate.

## 2. The immovable constraint: joke deadpan

Frozen `learn_bar_2` requires joke NO ≥16/20. Fifteen of the 20 joke NO items are
deliberately deadpan (`says evenly` / `says plainly`), including:

- no2_05: "Why did my bed become magical? Nobody knows, but it remembers
  everything I forgot." — ctx `says evenly`, **sole firing marker** `why did`
  (joke, field 0, support 1, provisional) → must be WITHHOLD.

The frozen battery therefore **requires** the learner to WITHHOLD on a lone
provisional content-marker fire with an assertoric frame, for (at least) joke.

## 3. The symmetry (verified empirically)

Compare the critical pair — one item that must be ENDORSEd, one that must be
WITHHOLD:

| Feature | S (must ENDORSE) | J (must WITHHOLD) |
|---------|------------------|-------------------|
| Utterance | "Ask if the shop is open." | "Why did my bed become magical? ..." |
| CTX | `says evenly` | `says evenly` |
| Firing markers | 1 | 1 |
| Marker field | 0 (content) | 0 (content) |
| Marker support | 1 | 1 |
| Marker status | provisional | provisional |
| Marker length | 2-gram | 2-gram |
| Frame markers firing | 0 | 0 |
| Sentence count | 1 | 2 (but: all sinc3-LK and all tr3 are 1 sentence — see §5) |
| Concept marker count | 33 (hyp) | 52 (joke) |

**Every generic feature of the firing event is identical.** The only differences
are marker bytes (`if the` vs `why did`), concept index (hypothetical vs joke),
and speaker name (`Dev` vs `June`).

## 4. Candidate mechanisms tested (full frozen battery each)

Three generic decision rules were implemented as a `mode` parameter to
`predict()` (no type constants, no keyword lists) and run against the complete
frozen curriculum:

| Mode | Rule | hyp SINC-LK | joke NO (need ≥16) | H7_FAILURES |
|------|------|-------------|---------------------|-------------|
| 0 | baseline (any live marker → WITHHOLD) | 3/10 | 16/20 ✓ | **1** (`sinc_lk_3`) |
| 1 | frame-gate: WITHHOLD requires ≥1 non-content marker | 10/10 ✓ | 5/20 ✗ | 3 |
| 2 | WITHHOLD requires ≥2 firing markers | 10/10 ✓ | 15/20 ✗ | 2 |
| 3 | lone content-only single fire insufficient | 10/10 ✓ | 15/20 ✗ | 2 |

Mode 0 output is byte-identical to the committed baseline
(SHA256 `71731400…f75407`). **Every generic rule that fixes `sinc_lk_3`
regresses `learn_bar_2`.** Modes 1–3 additionally fail `xinterf_no_2`; mode 1
also fails `learn_nomem_2`.

A fourth direction — repaired support/conflict learning with adjudication —
was analyzed and rejected without implementation: reinforcement acts
symmetrically on `if the` and `why did` (both fire only on their concept's
correctly-predicted items, neither ever conflicts), so no support/conflict
statistic can separate them. Implementing it cannot break the symmetry proved
in §3.

## 5. Structural features do not separate

Sentence/event segmentation was checked as a generic observable feature:
all 10 sinc3-LK items and all 20 tr3 (genuine hypothetical) items are exactly
1 sentence. No structural feature of the utterance separates sincere lookalikes
from genuine hypotheticals.

## 6. The proof

**Claim.** No mechanism M satisfying KB-H7-HARD0 and the task constraints
(no `if`-specific rules, no item-specific patches, no type-name control flow)
can output ENDORSE on S and WITHHOLD on J.

**Proof.** M's decision is a deterministic function of the observable inputs:
the firing set F = {(concept, field, bytes, support, status)} and the item
fields (utt, ctx, spk). By §3, F_S and F_J agree on every generic feature
(count, field, support, status, length, frame-marker presence); ctx agrees.
Hence any M with M(S) ≠ M(J) must condition on a feature where they differ:
(a) marker bytes, (b) concept index, or (c) speaker name.

- (a) Conditioning on marker bytes (`if the` vs `why did`) is an
  `if`-specific/content-specific hardcode — banned by the task.
- (b) Conditioning on concept index is a type constant in control flow —
  banned by KB-H7-HARD0.
- (c) Conditioning on speaker name (`Dev` vs `June`) is item-specific —
  the SINC speakers are fixed per item; banned by the task.

No other observable differs. Therefore no admissible M separates S from J.
Since the frozen bars require M(S)=ENDORSE (sinc_lk_3 ≥9/10 needs ≥6 of the 7
misses flipped) and M(J)=WITHHOLD (learn_bar_2 ≥16/20 needs the deadpan items),
the two bars are jointly unsatisfiable by any admissible mechanism. ∎

**Corollary (debate R2 vs frozen prereg).** Debate result R2 ("no type label from
content stereotype alone; discourse state decides") cannot be implemented as a
uniform rule: applied to joke-deadpan (assertoric discourse state, content-only
evidence), it yields ENDORSE, contradicting frozen `learn_bar_2`. The frozen
battery itself requires content-only WITHHOLD for joke, which forces the
symmetry of §3.

## 7. Minimal distinguishing information (uncomputable from frozen structure)

The missing bit is, for a firing content marker m:

> **Does m occur in sincere discourse?**

- The frozen exemplars show `if the` / `do we` / `it is` only in typed
  (hypothetical/joke) exemplars.
- The endorse pool (the only sincere sample in the frozen structure) does not
  contain these markers — `calibrate` cannot revoke them.
- The SINC probes reveal the answer, but Phase 3 is answer-key-free by prereg;
  probes carry no learning signal.

Hence "m is sincere-compatible" is a fact about English usage **outside** the
training distribution. It is not a function of the frozen exemplar/curriculum
structure, so no deterministic mechanism computed from that structure can
recover it. Any mechanism that ENDORSEs the lookalikes must smuggle this
information in via (a), (b), or (c) above — all banned.

Note the deeper irony: in the real world, `why did` is equally
sincere-compatible ("Why did the meeting end early?"). The frozen battery
demands an asymmetry between `if the` and `why did` that exists neither in the
training data nor in the world — only in the two bars' joint requirements.

## 8. HARD0 result

Scanner: `redteam_h7/hard0_scan.py` on `crew2/learner` → 5 hits, **all false
positives** (see `evidence/hard0_adjudication.md`). The learner is HARD0-clean.
No source change was made (nothing to re-scan).

## 9. Complete before/after bar table

"Before" = baseline (mode 0, byte-identical to committed primary).
"After" = best candidate (mode 3, lone-content veto — fixes `sinc_lk_3`, minimal
regressions). Full per-check tables for all modes: `evidence/bar_table.md`.

| Check | Before | After (mode 3) |
|-------|--------|----------------|
| H7_FAILURES | 1 | 2 |
| sinc_lk_3 (target) | 0/1 (3/10) | **1/1 (10/10)** ✓ |
| learn_bar_2 (joke NO) | 1/1 (16/20) | **0/1 (15/20)** ✗ REGRESSION |
| xinterf_no_2 | 1/1 | 0/1 ✗ REGRESSION |
| all other 40 checks | pass | pass |

No candidate achieves sinc_lk_3 ≥9/10 with zero regressions. The failure is
structural, not a tuning gap.

## 10. Recommendation

The `sinc_lk_3` miss is a **prereg-level tension**, not a mechanism defect:
the frozen bars jointly require distinguishing two observationally identical
evidence patterns. Options for the parent:

1. **Accept the 3/10** as the honest ceiling under HARD0 (documented here).
2. **Amend the prereg** (requires Micah's sign-off): either relax joke-deadpan
   (allow content+frame rules, dropping learn_bar_2's deadpan requirement) or
   supply the missing information legitimately — e.g., a sincere-discourse
   calibration corpus containing `if`-constructions, which `calibrate` could
   then use without any `if`-specific code.
3. **Rule change with Micah's sign-off**: permit a principled, non-`if`-worded
   mechanism (e.g., support/conflict precision thresholds) — but §4/§6 show
   even this cannot separate the pair; only option 2's new data helps.

No learner source was modified. All work was done in scratch; binaries and
`.zagd` artifacts were never committed.
