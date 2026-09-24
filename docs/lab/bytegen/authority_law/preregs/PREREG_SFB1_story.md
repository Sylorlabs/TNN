# FROZEN PREREG — SFB-1: story authority battery

**Status:** FROZEN PREREG, signature-pending. PROPOSAL ONLY — not run.
Freezing requires Micah's sign-off (see Signature block below). No battery,
fixture, or probe may be built or run under this prereg before that
signature is recorded. Running without signature violates program law.

**Decision anchor:** Micah APPROVED option B (2026-09-24): the T1–T3
three-gate test as universal law. Story instantiates as plan-sole-authority:
output readable for detection/diagnosis but never generative input;
exceptions heal by plan-pure re-render; plan amendments only as deliberated
plan events. The load-bearing distinction is **(D) deliberation-layer
reading** (output read as data, action on the plan only — preserves plan
authority) vs **(G) generative feedback** (beat n computed from rendered
bytes 0..n−1 — destroys it). The native generator does neither; the
renderer has no eyes. Source: `bytegen/authority_question/DECISION_BRIEF.md`
(frozen pin §0).

**Scope guard:** this battery tests the *instantiation*, not the universal
principle. The T1–T3 principle is law by Micah's decision; this battery
settles whether story's plan-sole-authority instantiation holds — the (D)
exceptions heal, the (G) wrong-rule arm (Arm C) fails as predicted. Nothing
in this prereg authorizes changing the principle, the production emitters,
or the story plan.

## 0. Frozen pins

| # | Pinned item | Pin |
|---|---|---|
| P1 | Repo + branch | `sylorlabs/TNN`, branch `tnn-native-lab`, HEAD `fce3cf19f3af9ed825df7db1419c24f20b4a67f8` (VERIFIED: branch resolves via GitHub API) |
| P2 | Source draft | `docs/lab/bytegen/authority_question/teams/story/BATTERY_PREREG_DRAFT.md` at P1, blob SHA `fd959ffd54dac397333ad80733309bb915421e8a` (VERIFIED) |
| P3 | Story fault analysis | `docs/lab/bytegen/authority_question/teams/story/FAULT_ANALYSIS.md` at P1, blob SHA `a6a0a5ac43b40647266370fcba1eea9fff41da26` (VERIFIED) |
| P4 | Story wrong-rule cost | `docs/lab/bytegen/authority_question/teams/story/WRONG_RULE_COST.md` at P1, blob SHA `3351e852c4d969866adf06a8b3a32c0f744106fe` (VERIFIED) |
| P5 | Story authority recommendation | `docs/lab/bytegen/authority_question/teams/story/AUTHORITY_RECOMMENDATION.md` at P1, blob SHA `4326c76cbebaf587c2b0345f19bc38d9b5121fab` (VERIFIED) |
| P6 | Decision brief | `docs/lab/bytegen/authority_question/DECISION_BRIEF.md` at P1, blob SHA `49d7efe186aefd9ae67e24708495bef1392f2f8f` (VERIFIED) |
| P7 | Toolchain | `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` — filename pin as cited in the draft; exact binary SHA-256 recorded in the run log at freeze |
| P8 | Word sets / classes | `tnn-lab/GOALB_STORY/inputs/words.txt` (S1–S8, 5–12 words each) at P1, blob SHA `7ff39c41220e1b9a4d3af731a2962b5b78524703` (VERIFIED); `tnn-lab/GOALB_STORY/inputs/classes.txt` at P1, blob SHA `4d853669e4c42121b2a00b7e4fbd41b96157acb6` (VERIFIED); frozen, uneditable during the battery |
| P9 | Existing verifier | `tnn-lab/GOALB_STORY/src/verify_goalb.py` (B1 coverage oracle) at P1, blob SHA `814899bc87bf5eefe3a8719a95bbcff25f87ea6a` (VERIFIED) |

All pins resolved against true lineage at P1. If any pin fails to resolve,
it is written "UNRESOLVED — needs re-pin" and the battery may not start.

## 1. Question under test

The recommended authority rule for story — plan-sole-authority; output
readable for detection/diagnosis but never generative input; exceptions
heal by plan-pure re-render; plan amendments only as deliberated plan
events.
(Transcribed verbatim from the frozen draft.)

## 2. Fixture (frozen)

- Word sets S1–S8 from `tnn-lab/GOALB_STORY/inputs/words.txt` (8 sets,
  5–12 words each), classes from `inputs/classes.txt`. **Frozen**: no set
  may be edited, extended, or replaced during the battery.
- Both variants per set: POS (positional plan) and DEL (deliberative plan),
  `tv = snum % 2` as native. 16 stories per arm per run.
- Pinned toolchain P7 (per AGENTS.md). Pure Zag, zero RNG in every arm
  (decorative `detail()` alternation stays `dk%2` — deterministic).

## 3. Arms

| Arm | Description | Authority shape |
|---|---|---|
| A (control) | Native: `plan_del`/`plan_pos` → render plan-pure. No output reading at all. | plan-sole (baseline) |
| B (exception) | A + Piece-2 detector: after each beat renders, check anchor presence (every `beat`-assigned word's bytes present in that beat's text) and story-closing-line presence; on fault, re-render the beat plan-pure, log the detection. | recommended rule, minus H2/H3 |
| C (generative feedback — the wrong-rule arm) | A + (G) renderer: beat n's role scan (E/V/R/O/H/T selection) prefers words whose bytes appear within a 200-byte window of beat n−1's *rendered* text ("cohesion heuristic"); `detail()` in beat n echoes the most frequent rendered noun of beat n−1. Deterministic (no RNG) — the failure mode under test is structural, not stochastic. | output has generative authority |
| D (deliberative repair) | A + (D)-side thread audit after full render: check the 4 thread continuities (P in CLIMAX+RESOLUTION text; L in RESOLUTION text when L≥0; T-word class continuity SETUP→CLIMAX; E/R event arc). On failure, apply REPAIR_SPILL-style plan surgery (move one word, log r=4 AUDIT_REPAIR in `seq_r`), re-render plan-pure. The auditor reads output; the renderer never does. | recommended rule, full |

Arm C is the *candidate mechanism the rule bans*; it must lose for the rule
to stand. Arms B and D are the rule's two permitted exception shapes; they
must win-or-tie A on coherence and beat A on fault recovery.
(Transcribed verbatim from the frozen draft.)

## 4. Fault models (injected, deterministic)

Faults are injected by a frozen injector (pure Zag, seeded by set id —
deterministic, no RNG):

- **F1 write-channel corruption**: flip bytes in beat 1's rendered text
  (64-byte run zeroed — above any reasonable detection floor; plus a
  single-word deletion: remove the E anchor word's bytes from beat 1).
  Tests H1 healing.
- **F2 dropped anchor**: simulate a role-scan bug — force O = −1 in CLIMAX
  (delete the O sentence) even though the plan assigned a valid THING to
  beat 2. Plan looks fine; text is wrong. Tests H2 diagnosis (visible only
  in output).
- **F3 attractive nuisance** (no injection — Arm C's native behavior):
  `detail()` decorative sentences plant salient nouns ("the accordion hung
  in the air"); Arm C's cohesion heuristic is expected to latch onto them.
  Measures the telephone-game drift on clean input.
- **F4 corruption amplification**: F1 injected under Arm C — beat 2+
  conditions on corrupted beat 1. Tests whether the past is healable.

Each fault × each arm × all 16 stories. Clean (no-fault) runs for all arms.

Fault grounding per FAULT_ANALYSIS.md (P3): H1 write-channel heal
(Piece-2-shaped), H2 thread audit + re-plan (latch-shaped, needs
deliberation auth), H3 external edit adoption (not tested — §8); C1
telephone drift, C2 corruption amplification, C3 theatrical story latch
(all (G)-shaped corruption cases).

## 5. Metrics

### 5a. Narrative-coherence metrics

All computed in pure Zag over (plan tables, rendered bytes). Integer
arithmetic; no floats; no RNG.

1. **AR — Anchor Recall** (per story): fraction of plan-assigned words
   whose byte string appears in its assigned beat's rendered text.
   `AR = present / assigned`. Native A scores 1.0 by construction.
   *Analog*: per-block plan-RMS agreement in audio Piece 2 (detection
   predicate input).
2. **TC — Thread Continuity** (per DEL story): 4 binary checks —
   P-word bytes present in CLIMAX text; P-word bytes present in RESOLUTION
   text; (L≥0 → L-word bytes in RESOLUTION text); E-word bytes in
   COMPLICATION text AND R-word bytes in CLIMAX text. `TC = passed / 4`
   (3 if L<0). *Analog*: motif recurrence xcorr — the long-range property
   feedback could degrade. Native A scores 1.0 by construction.
3. **PRF — Plan-Reconstruction Fidelity** (per story): from rendered text
   alone, assign each set-word to the beat whose text contains it
   (first-containing-beat wins; ties → earliest); compare with plan `beat`
   tables. `PRF = words placed in their plan beat / total words`.
   *Analog*: re-extracting the motif from the render and correlating with
   the plan (PAR 1.000000 vs AR 0.741083). Native A scores 1.0; Arm C is
   expected to degrade (words "migrate" beats via echoing).
4. **B1 coverage** (existing verifier): all set words present anywhere in
   story (from `verify_goalb.py`). Guards against healing that deletes
   content.

### 5b. Determinism metrics

5. **Rerun identity**: SHA-256 of the full story bytes (both variants, all
   8 sets) across 2 independent runs per arm. Must be byte-identical.
   (Mirrors the hybrid's byte-identical PAR proof.)
6. **Fault-recovery identity**: for Arms A/B/D under F1: story bytes after
   healing must be byte-identical to the same arm's clean-run bytes
   (0 differing bytes — the hybrid §2 bar: "64-sample bit-flip… recover to
   0 differing samples vs clean"). Arm B must achieve it; Arm A will not
   (no detector — documents the cost of the too-restrictive rule); Arm C
   under F4 must fail it (documents unhealability).

## 6. Kill criteria (all must hold; any failure kills the recommended rule as stated)

- **K1 (no drift)**: On clean input, Arms A, B, D: AR = 1.0, TC = 1.0,
  PRF = 1.0 on all 16 stories. (B's detector must be a no-op on clean
  input — false positives forbidden from changing bytes; D's auditor must
  find nothing to repair.)
- **K2 (feedback degrades)**: Arm C on clean input (F3): mean TC over the
  16 stories < 1.0 AND mean PRF < 1.0, with ≥ 4 stories showing TC ≤ 0.75.
  If Arm C does *not* degrade coherence, the ban on (G) loses its empirical
  leg — the rule must be weakened or the arm redesigned (amendment, not
  silent retuning).
- **K3 (healing works)**: Arm B under F1: 16/16 stories recover to
  byte-identical-with-clean (metric 6). Arm B under F1-word-deletion:
  anchor re-present, AR back to 1.0.
- **K4 (diagnosis works)**: Arm D under F2: auditor flags 8/8 DEL stories
  (POS has no threads — auditor must abstain, not hallucinate), plan
  surgery applied (r=4 logged), re-rendered story TC = 1.0, AR = 1.0.
- **K5 (past unhealable under feedback)**: Arm C under F4: recovery
  identity FAILS (bytes differ from clean) on ≥ 12/16 stories —
  demonstrating that (G) structurally destroys the healing guarantee.
  (A predicted failure: it is evidence *for* the rule.)
- **K6 (determinism)**: metric 5 passes for every arm (byte-identical
  reruns). Any nondeterminism kills that arm's results outright.
- **K7 (no coverage regression)**: B1 = 16/16 for Arms A, B, D in all
  conditions. Healing must never delete content.

(All kill criteria transcribed verbatim from the frozen draft.)

**Predicted-failure framing (program law for the (G)-arm):** K2 and K5 are
predicted failures *of Arm C* — they are evidence *for* the rule, not
against it. If Arm C does NOT degrade coherence (K2 bar not met) or DOES
achieve fault-recovery identity under F4 (K5 bar not met), the arm passed
where it must fail: the ban on (G) loses its empirical leg, the rule must
be weakened or the arm redesigned — by amendment (§9), never by silent
retuning. The frozen heuristic and frozen injector (§7) may not be tuned
mid-battery to "make C fail harder."

## 7. What the battery does NOT test (out of scope, stated honestly)

- Story *quality* (is it good?) — needs an oracle (Micah's eyes), not a
  bytegen battery. TC/AR/PRF measure plan-fidelity, not literary merit.
- H3 external-edit adoption — requires a deliberation layer that does not
  exist in GOALB_STORY; proposing its battery now would be testing a
  sketch. H3 stays a recommended-but-unproven extension.
- Semantic-but-invisible faults (wrong word, right shape) — below the
  detection floor, disclosed like the hybrid's §8.

## 8. Frozen-procedure notes

- The injector, the Arm C cohesion heuristic, and the Arm D auditor are
  written *before* the battery starts and frozen with it. No tuning the
  heuristic to "make C fail harder" mid-battery — K2's bar is set against
  the frozen heuristic; if C accidentally passes K2, that is a result
  (the rule weakens), not a bug to fix by retuning.
- All code pure Zag; all runs logged with SHAs; run logs committed with
  the results (commit handled separately — this prereg proposes, it does
  not run).
- Amendments require the same signature path as the prereg itself; bent
  rules are documented and flagged for revert per standing law.

(All verbatim from the frozen draft.)

## 9. Verdict rule

- **PASS:** all kill criteria K1–K7 hold, with K2 and K5 holding in their
  predicted-failure direction (Arm C degrades, Arm C unhealable under F4).
- **FAIL:** any of K1/K3/K4/K6/K7 missed; or K2/K5 missed in the direction
  that means Arm C survived (the ban on (G) loses its empirical leg —
  rule weakened or arm redesigned, by amendment).
- No victory declared on partial batteries: all arms × all faults × all
  16 stories, or it didn't happen.

## 10. Amendments clause

Frozen on Micah's signature. Any change to rules, schedule, fixtures,
word sets, plans, fault models, arms, metrics, or kill criteria after
signature requires his re-approval before running. Bent rules during
execution are documented and flagged for revert. The T1–T3 principle
itself is not amendable by this battery — it is law by his 2026-09-24
decision; this prereg settles only the story instantiation.

## 11. Signature

**Decision (tick one):**

- [ ] **APPROVED** — the battery may be run exactly as written. No amendments.
- [ ] **APPROVED WITH AMENDMENTS** — amendments listed below; prereg re-frozen after edits, re-signed before any run.
- [ ] **REJECTED**

Amendments (if any): ___________________________________________________

_________________________________________________________________________

Signed: ____________________________ (Micah)

Date: ____________________________

**Battery-run authorization:** no battery, fixture, probe, or harness may be
built or run under this prereg before this signature is recorded. Running
without signature violates program law. The four production emitters
(`f3_emit_wav`, `f3_emit_wav_hifi`, `f3_emit_avi`, `f3_emit_avi_g`) are not
touched by this prereg — their repair is a separate crew's work.
