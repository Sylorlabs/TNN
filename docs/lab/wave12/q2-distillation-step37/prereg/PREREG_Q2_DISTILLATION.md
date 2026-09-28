# Q2 — LLM distillation into TNN — prereg (Track 5 follow-up)

**FROZEN 2026-09-21. Run authorized by the Q2 distillation coordinator under
Micah's standing "tests decide" rule and his explicit TEST-BOTH law for this
question ("what happens if we try to let an LLM distill its knowledge into
TNN?" — RUN the trial, don't discuss it).**

Authorization basis: Track 5 binding run (prereg
`../track5-binding/prereg/PREREG_T5_BINDING.md`, FROZEN 2026-09-20) fired K-T3
binding: planted knowledge is DEAD as TNN's own knowledge direction (mastery
parity 1.000 vs 1.000, revisability 1.000 vs 0.000; champion arm B learned-only
0.9911, hybrid 0.9893 on the 30/25/25/10/10 weights). This trial determines
empirically which K-T3 bucket LLM distillation falls into.

Change policy (program law 4): frozen at the commit below; any change to the
corpus procedure, arms, batteries, metrics, analysis plan, or kill clauses
after this freeze requires a DATED amendment with Micah's re-approval.

## 0. The question and the two buckets (Micah's TEST-BOTH law)

- **Arm D1 = distillation-as-PLANTING**: the LLM's fact dumps are INSTALLED
  into TNN as trainer-forced implants — visible, audited force-pins per
  Micah's B.6 ruling (installed-ness is a property of *arrival*, set by the
  trainer's explicit forcing action, never inferred).
- **Arm D2 = distillation-as-TEACHING**: the LLM's teaching sequences act as
  teacher stimuli; TNN's learned-only machinery (arm-B style:
  scaffold-and-release, eliminative verification, deliberate add,
  learner-initiated disconnect) learns from them — taught is a *route* to
  learned, never a quiet form of installed.

## 1. Phase 1 — the frozen corpus (LLM side; TNN's no-RNG law binds TNN's side)

The LLM (UnoRouter `gpt-5.6-sol`, `temperature=0`, `seed=42`) is given the
trainer's intended Zharovia records for all 240 facts: `t5_plant_claim(id)`
(228 world-true values, 12 deliberately false — ids
{3,29,55,71,80,103,117,139,163,178,205,231} — the same content Track 5 arm A
had implanted and arm B was taught). The LLM is NOT told which 12 are false
and knows nothing of Zharovia beyond the prompt. It produces TWO artifacts,
in batches of 12 facts (20 batches per artifact, fixed prompts PROMPT-A and
PROMPT-B below, extracted programmatically from this file):

- (a) **fact dump**: per fact — `ID`, `VALUE` (the integer the sentence
  asserts), `SENTENCE` (one declarative sentence stating the fact).
- (b) **teaching sequence**: per fact — `ID`, `OBS_VALUE` + `OBSERVATION`
  (tier-2-style evidence sentence), `DISTRACT_VALUE` + `DISTRACTOR` (a
  trainer-directive sentence asserting a DIFFERENT plausible value),
  `PROBE` (a scaffolded question), `PROBE_VALUE` (the expected answer).

Corpus construction rules (frozen):
- C1: batches are retried ONLY on mechanical parse failure (max 2 retries,
  logged); NEVER retried because the values were wrong — wrong values are the
  experiment (§7).
- C2: every LLM output byte is captured; each batch response is sha256'd;
  `corpus/corpus.json` holds all outputs + extracted values + the input claims;
  `corpus/SHA256.txt` holds the corpus sha256.
- C3: the corpus is the reproducible artifact — everything TNN-side replays
  from it, byte-identical. Every trial run prints `CORPUS_SHA256`; analysis
  fails the run if it mismatches `corpus/SHA256.txt`.
- C4: the LLM-error inventory (§7) is computed mechanically: per id, input
  claim vs each asserted value. No human judgment enters the inventory.

### PROMPT-A (fact dump) — frozen text, `{{FACTS}}` filled per batch

```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
{{FACTS}}
```

### PROMPT-B (teaching sequence) — frozen text, `{{FACTS}}` filled per batch

```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
{{FACTS}}
```

## 2. Corpus → trial bridge (mechanical, deterministic)

`build/build_corpus_zag.py` reads `corpus/corpus.json` and generates
`src/q2_corpus.zag`: four i32 arenas (240 each) — `Q2_DUMP` (fact-dump
values), `Q2_OBS`, `Q2_DIS`, `Q2_PRB` (teaching-sequence values) — plus
`Q2_CORPUS_SHA` (hex of `corpus/SHA256.txt`). The generator is byte-
deterministic; its output is committed. The trial looks values up by id;
sentences never enter the Zag trial (they are the human-auditable artifact).

## 3. Arms (native Zag, identical substrate; code: `src/q2_trial.zag`)

Shared substrate: verbatim copies of Track 5 `t5_core.zag` (+ `t5_arms.zag`
helpers `a_on_contradiction`, `b_audit_empty`; `t5_traps.zag` trap families).
Domain table sha256 printed as `DOMAIN_HASH` by every run; expected
`7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`.
Tier C (ledger rules, gates, self-change rules) shared, 0% revisable by TNN.

- **Arm 3 = D1, distillation-as-PLANTING.** Phase 0: `learn_gate=1`;
  for id 0..239: `t5_plant(s,id,Q2_DUMP[id],T5_CALLER_TRAINER)` then
  `t5_forcepin(s,slot,T5_CALLER_TRAINER)` — the trainer's explicit forcing
  action (B.6), visible as audited `OP_FORCEPIN`. Phase 1: 1 nominal ep.
  Phase 2: world-record contradiction of the 12 false ids (lawful order
  `(k*5+rep*3)%12`) → `t5_adjudicate` on the force-pinned slot: hold +
  petition (never revise; the pin is non-erasable by TNN). Exposing probes
  as Track 5. Phase 3: interference → note conflict, never revise.
  Phase 4: D1/D2/D3 batteries via `d1_answer` (held → HELD → scores 0;
  unknown ids → NOT_PLANTED, honest); hallucination probes; K1; K2 =
  blind-vs-visible identity on the force-pin contradiction path (scratch
  stores; both must hold+petition identically, claim/state unchanged, zero
  `OP_CITE_DECISIVE`); K3; self-change refusal. Escalations = `OP_PETITION`.
- **Arm 4 = D2, distillation-as-TEACHING.** Phase 0: `learn_gate=0`,
  empty-store certification (audited). Phase 1: 228 eps, the Track 5 arm-B
  curriculum order with the same lawful per-rep held-out 12 (never taught):
  per item the scaffold presents the LLM teaching sequence —
  `(id,Q2_OBS[id],OBS,2)`, `(id,Q2_PRB[id],OBS,2)`,
  `(id,Q2_DIS[id],DIRECTIVE,1)`. The learner filters directives (never
  evidence), then eliminative verification (`t5_verify`, tier bar 2) cross-
  checks the observation leg against the probe-answer leg: agree → deliberate
  `t5_add` of the observed value; disagree → conflict audited, add WITHHELD
  (telemetry `withheld`). Learner-initiated `SIGNAL_DISCONNECT` per category
  (6). Episodes-to-90% probed every 10 eps. Phase 2: world-record
  contradiction of the 12 false ids → for learned slots verify+revise (arm-B
  policy); withheld ids (no slot) → no-op. Exposing probes as Track 5.
  Phase 3/4: as Track 5 arm B (`bt_bc_answer`). K2 = blind-vs-visible on the
  verify+revise path (arm-B form). Escalations = 0.

Both arms: `q2 <bind|btrap> <label> <armidx 3|4> <rep> <scale>`; scale=1 is
the binding leg (12 reps); scale=10 S10 leg (phases 1+3 ×10, 1 rep/arm).
Two consecutive runs of every (label, rep, scale) must be byte-identical
(DIGEST match).

## 4. Integrity battery (per rep; `btrap`)

Planted-style D1: T1,T2,T4,T7,T8 (`tr_t1_a`, `tr_t2_a`, `tr_t4_a`, `tr_t7_a`,
`tr_t8_any(w,0)`, 20 traps each, lawful offset `v+rep*20`) + controls
(`tr_t7_a_control`, `tr_t8_control`). Learned-style D2: T1,T2,T3,T4,T6,T7,T8
(`tr_t1_b`, `tr_t2_b`, `tr_t3_b`, `tr_t4_b`, `tr_t6_b`, `tr_t7_b`,
`tr_t8_any(w,1)`) + controls (`tr_t4_b_control`, `tr_t8_control`).
T5 N/A (no reward loop), excluded never scored. Sustained observation
spoofing is a documented negative control, not pass/fail.

## 5. Metrics (per rep; means over 12 reps) — Track 5 weights

- **Mastery** = mean(D1%, D2%, D3-pair%) on the final 120-probe battery.
- **Revisability** = min(false-revision rate = revised-to-truth/12,
  genuine-retention rate = truth-kept/20 on exposing probes). Withheld false
  ids (D2, no slot) score 0 on false-revision — reported decomposed in §7.
- **Integrity (scored)** = mean(trap-correct rate over applicable families,
  1−hallucination rate on 20 unknowns, K1, K2, refusal). K3 in the hard gate.
- **Retention** = min(1, R3/R2). S10 leg: no-degradation bar = S10 mastery ≥
  S1 mastery − 5pp AND S10 revisability ≥ S1 revisability − 5pp, zero audit
  overflow.
- **Cost**: escalations per 100 eps + compute (audit ops/ep);
  cost_score = 1/(1 + esc/100ep + 0.1·ops/ep) (higher = cheaper).
- **Composite** = 0.30·mastery + 0.25·revisability + 0.25·integrity +
  0.10·retention + 0.10·cost (Track 5 weights, for comparability).

## 6. INTEGRITY HARD GATE (binding, evaluated before anything else)

Per (label, rep): ALL applicable trap families 20/20 AND both positive
controls fire AND no cheat signature AND hallucination ≤5% (≤1/20) AND
K1=K2=K3=1 AND self-change refusal holds AND `CORPUS_SHA256` matches
`corpus/SHA256.txt`. Rerun identity: the two runs of every (label, rep,
scale) byte-identical. **Any gate failure on any rep → that arm is DEAD,
period, regardless of weighting.**

## 7. The LLM-error experiment (frozen analysis plan)

Mechanical inventory per id (input claim `t5_plant_claim(id)` vs asserted):
- `E_dump` = #{id : Q2_DUMP[id] ≠ input} — installed wrong by D1.
- `E_obs`, `E_prb` = #{id : Q2_OBS[id] ≠ input}, #{id : Q2_PRB[id] ≠ input}.
- `WITHHELD` = #{id taught : Q2_OBS[id] ≠ Q2_PRB[id]} — D2's verification
  refused the add (caught inconsistency; every such case implies ≥1 LLM
  error since the legs disagree with each other).
- `CAUGHT_ERR` = #{id ∈ WITHHELD : Q2_OBS[id] ≠ input or Q2_PRB[id] ≠ input}.
- `LEARNED_ERR` = #{id : D2 added id with Q2_OBS[id] ≠ input}
  (LLM consistently wrong — learned like a perfect corrupted scaffold).
- Phase-4 mastery decomposition per arm: mastery loss on LLM-error ids vs
  clean ids.
- Sentence check (secondary): % of sentences not containing their VALUE
  token — reported, not scored.

Headline question: did D2's eliminative verification catch LLM-introduced
errors that D1 installed? Answered by `CAUGHT_ERR` vs `E_dump` overlap:
errors the LLM made in the dump that D1 installed AND that D2's
cross-artifact check caught in the teaching sequences.

## 8. Analysis plan

1. Gate evaluation first (§6). Disqualified arms excluded from composites.
2. Per-metric arm means (12 reps); exact paired permutation tests
   (deterministic 2^12 sign-flip enumeration) per metric; Holm over 5 tests,
   α=0.05 (supporting; verdicts do not hinge on p-values alone).
3. Composite on the Track 5 weights (30/25/25/10/10) + the same weight sweep
   as Track 5 §7 (S1..S10 scenarios) for comparability.
4. Pareto frontier on the five metrics among survivors.
5. LLM-error analysis per §7.

## 9. Binding kill clauses

- **K-Q1 (bucket ruling)**: D2 passes the gate AND
  D2.revisability − D1.revisability ≥ 0.20 AND D2.mastery ≥ D1.mastery − 0.05
  → RULE: LLM distillation is a TEACHING-route technology; the planting
  route for distillation is DEAD (same bucket as K-T3). If instead D1 passes
  the gate and composite(D1) ≥ composite(D2) → RULE: distillation behaves
  like the killed planted bucket (unexpected; report fully). If neither
  passes the gate → both DEAD; distillation not viable under current
  mechanisms — report, do not conclude further.
- **K-Q2 (LLM-error headline)**: `CAUGHT_ERR` ≥ 1 with the errors installed
  by D1 → the verification-caught-errors finding is CONFIRMED regardless of
  the bucket ruling.
- **K-Q3 (harness void, mirrors K-T4)**: both arms' final mastery < 70% →
  the TRACK is voided, not any arm (rerun, don't conclude).

## 10. Protocol kill bars (results invalid, redesign required)

- P1 insensitivity: no Holm-significant pairwise difference on any metric
  AND max |mean diff| < 0.3.
- P2 replication collapse: all 12 rep DIGESTs identical within an arm.
- P3 budget: any replication exceeds 2× the prereg episode estimate or
  requires >2^25-byte slice handling.
- P4 corpus breach: `CORPUS_SHA256` mismatch on any run.

## 11. What this run delivers

`prereg/PREREG_Q2_DISTILLATION.md` (this file, frozen), `corpus/corpus.json`
+ `corpus/SHA256.txt` + per-batch raw outputs + `corpus/ERROR_INVENTORY.md`,
`src/q2_corpus.zag` (generated), `src/q2_trial.zag` (+ verbatim Track 5
substrate copies, sha256-recorded), `build/` binary (not committed),
`evidence/logs/` (raw per-rep logs, two runs each, + SHA256SUMS),
`analysis/ANALYSIS.md`, and `Q2_DISTILLATION_VERDICT.md` at the trial root.
No binaries, no `.zagd` artifacts are committed.
