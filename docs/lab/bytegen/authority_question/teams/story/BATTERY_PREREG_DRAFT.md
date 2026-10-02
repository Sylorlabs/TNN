# FROZEN PREREG — Story authority battery (DRAFT, proposed)

**Status**: proposal only. NOT run. Frozen means: word sets, plans, fault
models, metrics, and kill criteria below may not be changed after the
battery starts without a signed amendment. Tunes nothing on the test sets.

**Question under test**: the recommended authority rule for story —
plan-sole-authority; output readable for detection/diagnosis but never
generative input; exceptions heal by plan-pure re-render; plan amendments
only as deliberated plan events.

## 1. Fixture (frozen)

- Word sets S1–S8 from `tnn-lab/GOALB_STORY/inputs/words.txt` (8 sets,
  5–12 words each), classes from `inputs/classes.txt`. **Frozen**: no set
  may be edited, extended, or replaced during the battery.
- Both variants per set: POS (positional plan) and DEL (deliberative plan),
  `tv = snum % 2` as native. 16 stories per arm per run.
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (per AGENTS.md). Pure Zag, zero RNG in every arm (decorative `detail()`
  alternation stays `dk%2` — deterministic).

## 2. Arms

| Arm | Description | Authority shape |
|---|---|---|
| A (control) | Native: `plan_del`/`plan_pos` → render plan-pure. No output reading at all. | plan-sole (baseline) |
| B (exception) | A + Piece-2 detector: after each beat renders, check anchor presence (every `beat`-assigned word's bytes present in that beat's text) and story-closing-line presence; on fault, re-render the beat plan-pure, log the detection. | recommended rule, minus H2/H3 |
| C (generative feedback — the wrong-rule arm) | A + (G) renderer: beat n's role scan (E/V/R/O/H/T selection) prefers words whose bytes appear within a 200-byte window of beat n−1's *rendered* text ("cohesion heuristic"); `detail()` in beat n echoes the most frequent rendered noun of beat n−1. Deterministic (no RNG) — the failure mode under test is structural, not stochastic. | output has generative authority |
| D (deliberative repair) | A + (D)-side thread audit after full render: check the 4 thread continuities (P in CLIMAX+RESOLUTION text; L in RESOLUTION text when L≥0; T-word class continuity SETUP→CLIMAX; E/R event arc). On failure, apply REPAIR_SPILL-style plan surgery (move one word, log r=4 AUDIT_REPAIR in `seq_r`), re-render plan-pure. The auditor reads output; the renderer never does. | recommended rule, full |

Arm C is the *candidate mechanism the rule bans*; it must lose for the rule
to stand. Arms B and D are the rule's two permitted exception shapes; they
must win-or-tie A on coherence and beat A on fault recovery.

## 3. Fault models (injected, deterministic)

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

## 4. Metrics

### 4a. Narrative-coherence metrics (the xcorr-motif-recurrence analogs)

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

### 4b. Determinism metrics

5. **Rerun identity**: SHA-256 of the full story bytes (both variants, all
   8 sets) across 2 independent runs per arm. Must be byte-identical.
   (Mirrors the hybrid's byte-identical PAR proof.)
6. **Fault-recovery identity**: for Arms A/B/D under F1: story bytes after
   healing must be byte-identical to the same arm's clean-run bytes
   (0 differing bytes — the hybrid §2 bar: "64-sample bit-flip… recover to
   0 differing samples vs clean"). Arm B must achieve it; Arm A will not
   (no detector — documents the cost of the too-restrictive rule); Arm C
   under F4 must fail it (documents unhealability).

## 5. Kill criteria (all must hold; any failure kills the recommended rule as stated)

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

## 6. What the battery does NOT test (out of scope, stated honestly)

- Story *quality* (is it good?) — needs an oracle (Micah's eyes), not a
  bytegen battery. TC/AR/PRF measure plan-fidelity, not literary merit.
- H3 external-edit adoption — requires a deliberation layer that does not
  exist in GOALB_STORY; proposing its battery now would be testing a
  sketch. H3 stays a recommended-but-unproven extension.
- Semantic-but-invisible faults (wrong word, right shape) — below the
  detection floor, disclosed like the hybrid's §8.

## 7. Frozen-procedure notes

- The injector, the Arm C cohesion heuristic, and the Arm D auditor are
  written *before* the battery starts and frozen with it. No tuning the
  heuristic to "make C fail harder" mid-battery — K2's bar is set against
  the frozen heuristic; if C accidentally passes K2, that is a result
  (the rule weakens), not a bug to fix by retuning.
- All code pure Zag; all runs logged with SHAs; run logs committed with
  the results (commit handled separately — this draft proposes, it does
  not run).
- Amendments require the same signature path as the prereg itself; bent
  rules are documented and flagged for revert per standing law.
