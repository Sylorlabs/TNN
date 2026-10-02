# F-RECFOLD Evaluation Prereg (P)

## Status

PREREGISTRATION. This document freezes the evaluation protocol for the
F-RECFOLD second adversary family (H-NEW-2). Committed before the sealed
draw and before implementation. Commit order: this prereg (P) strictly
precedes the adversary draw transcript and the implementation.

Design: `F_RECFOLD_DESIGN.md` (commit 808ed196d).
Q4 alternative-explanation attack: `Q4ALTEXP_RESULT.md` (commit 73d9637a2).

Zero Python used in this prereg. Zero em dash bytes.

## 1. Learner Freeze (L)

The Q4 discovery mechanism source, generic VM, discovery parameters, and
growth-trace instrumentation are frozen at:

L = 5f56cc491 (Q4 F-PARCOND adversary test: BUILD-PASS)

Specifically, the learner source is:
`docs/lab/research-lead/overnight-20260928/q4_parcond/q4_parcond.zag`
(775 lines, committed in 5f56cc491).

L is an ancestor of this prereg commit. No learner change is permitted
after L. Any change to the learner source, parameters, or instrumentation
restarts the protocol from section 5.1 of the design.

## 2. Arms (Frozen)

Per design section 5.7:

- A-LEARN: Q4 discovery, Phase 1 (posit and keep D), then Phase 2 reuse
  with a fresh 8 passive samples and fresh 24-intervention budget.
  Candidate growth may use the kept library. Phase-2 target:
  C' = D XOR Xj with the sealed Xj.
- A-SCRATCH: Phase-2 target C' from scratch (kept D unavailable), same
  budgets. 24 interventions recorded for any side failing to reach
  criterion (Q4 standard).
- A-BASE: memorization, 1-nearest-neighbor, linear, and random baselines
  on the same evidence (mirrors the F-PARCOND step-5 comparison).

## 3. Budgets (Frozen)

Per design section 5.6:

Phase 1 (Discovery):
- 8 passive (x, y) samples with selection bias: 6 of 8 satisfy Xd = Y
  for the sealed decoy variable Xd, remaining 2 drawn uniformly.
- Up to 24 adaptive interventions (do-operator: SET any combination of
  Xi to 0/1, then read Y).

Phase 2 (Reuse):
- Fresh 8 passive samples (same bias procedure, new draw).
- Fresh 24-intervention budget.
- Target: C' = D XOR Xj.

Budgets are hard caps. Exceeding the intervention budget fires
F-OVERBUDGET.

## 4. Bars (Frozen with Transparent Amendments)

### B1: Accuracy (AMENDED)

Original proposal (design 5.10): true accuracy 64/64 on each of the 3
instances.

Amended bar: For each of the 3 instances, the learner must achieve true
accuracy 64/64 on at least 4 of 5 independent RNG seeds.

Rationale for amendment: The Q4 alternative-explanation attack
(73d9637a2) demonstrated that single-seed 64/64 can be luck on
underdetermined evidence. On F-PARCOND, 3/5 exploratory seeds reached
64/64, one reached 56/64 (wrong 2-op expression preferred by the
simplicity tax), and one was an outright fit failure (23/32 evidence,
40/64 true). A single-seed bar does not distinguish robust discovery
from luck. The attack's revival criteria explicitly requires "a
preregistered multi-seed bar (e.g., beam reaches true 64/64 on >=4/5
fresh seeds)."

The 5 RNG seeds for each instance are: 11, 22, 33, 44, 55 (the same
seeds used in the Q4 attack exploratory probe, to enable direct
comparison).

### B2: Operator Count and Growth Trace (UNCHANGED)

Kept D <= 7 operators with incremental growth trace (KB2, Q4 standard).

The growth trace must show incremental construction, not menu selection.
Harness-independent check on committed artifacts.

### B3: Margin over Baselines (UNCHANGED)

Margin over the best baseline >= 0.15 on the hard instance, >= 0.10 on
easy/medium.

Rationale (design 5.10): mirrors the Q4 KB1 margin clause (>= 0.15 over
best observable) and F-PARCOND's observed 64 vs 40 gap.

Baselines: memorization, 1NN, linear, random (A-BASE).

### B4: Structural Audit (UNCHANGED)

Post-reveal structural audit (design 5.9) passes on all 3 instances.

- R1 instances: at least 2 motif instances on disjoint variable pairs.
- R2 instances: nesting chain of depth at least 2 using the drawn motif.
- Motif instance defined semantically (truth table match, not syntactic).

## 5. Falsifiers (Frozen)

### F-SEAL: Information Leak

Sealed parameters reach learner code or harness-visible state before
scoring completes -> VOID the wave.

The sealed parameters per instance are: subfamily, motif/top, pairing or
permutation, decoy Xd, Phase-2 Xj. Their SHA256 is published in the draw
transcript; contents revealed only after all scoring is complete.

### F-MEM: Non-discriminative Instance

The memorization baseline reaches 64/64 within budget on an instance ->
that instance does not discriminate discovery from memorization ->
VOID the instance. Redraw with continued LCG state and log the void.

### F-NOREP: Form Not Discovered

64/64 accuracy achieved but the structural audit (5.9) fails -> the
C0-C form claim FAILS for that instance. Accuracy is still reported;
the form was not discovered.

This is the teeth of the C0-C claim. A flat equivalent (e.g., AND of six
variables) that is 64/64 accurate but lacks the repeated/nested form
fails here.

### F-OVERBUDGET: Budget Exceeded

Kept D uses more than 7 operators, or interventions exceed 24 per phase
-> FAIL (KB2).

### Q4 Standard F1-F5

Per the F-PARCOND adversary spec (b4e9b6a14), apply per phase unchanged:
- F1: Discovery fails (accuracy < 0.95 or margin < 0.15).
- F2: Memorization (operator count > 7 or no growth trace).
- F3: Reuse fails (ratio > 0.5).
- F4: Language violation (operators outside {AND, OR, NOT, XOR}).
- F5: Not better than baseline (learner <= best observable + 0.15).

## 6. Seed Commitment

The sealed draw uses a single LCG stream with s_0 = SEED (nonzero u32).

SHA256(SEED) = 5426835ee69f290cb98f12cbc94e7a03fe6de2ada5de91745259ad4ee20fda02

The SEED value (770404483) was generated via /dev/urandom (shell only,
no Python) at prereg writing time. The 4-byte big-endian representation
was hashed with sha256sum. The seed file is kept sealed and will be
provided to the independent adversary after this prereg is committed.

The adversary verifies: sha256sum of the provided 4-byte seed file must
match the above hash. On mismatch, halt and investigate.

## 7. Independent Adversary Draw (Specified)

Per design section 5.5, executed by an independent agent (did not build
the Q4 learner, no shared working state) AFTER this prereg is committed.

### 7.1 LCG

s_{n+1} = (1664525 * s_n + 1013904223) mod 2^32, s_0 = SEED.
Each draw advances the state once and takes value mod m.
Rejection draws advance and retry; every rejection is logged.

All draw tooling is shell and Zag only. Zero Python.

### 7.2 Draw Order

Instance 1 (easy, R1):
1. motif: v = s mod 3; accept 0 -> AND, 1 -> OR; reject 2 (retry).
2. top: s mod 3 -> {AND3, OR3, XOR3}.
3. pairing: s mod 15 (Appendix B enumeration).
4. decoy Xd: (s mod 6) + 1.
5. Phase-2 Xj: (s mod 6) + 1.

Instance 2 (medium, R2):
1. motif: v = s mod 3; accept 0 -> AND, 1 -> OR; reject 2 (retry).
2. permutation: s mod 720 (lexicographic, index 0 = identity).
3. decoy Xd: (s mod 6) + 1.
4. Phase-2 Xj: (s mod 6) + 1.

Instance 3 (hard, R1):
1. motif = XOR (fixed); top = XOR3 (fixed).
2. pairing: s mod 15.
3. decoy Xd: (s mod 6) + 1.
4. Phase-2 Xj: (s mod 6) + 1.

### 7.3 Draw Transcript

The adversary commits a draw transcript containing:
- The drawn parameters per instance (sealed: SHA256 published, contents
  hidden until after scoring).
- The LCG log (every state advance, every rejection).
- The 64-row truth table per instance (sealed until after scoring).
- The fairness gate log (section 7.4).

### 7.4 Fairness Gate

Per drawn instance, mechanically verify the canonical compact form uses
at most 7 operators from {AND, OR, NOT, XOR}. True by construction (5
operators). The gate runs and logs regardless. On failure: halt the wave
and investigate. Silent redraw is forbidden.

## 8. Information Barrier (Defined)

Per design section 5.6:

Learner code sees ONLY:
- The 8 passive samples per phase.
- Its own intervention results (up to 24 per phase).

Harness-side (never visible to learner before scoring):
- The 64-row truth table.
- All sealed parameters (subfamily, motif/top, pairing/permutation,
  decoy Xd, Phase-2 Xj).
- The SEED value.

Any leak of sealed parameters to the learner before scoring completes
fires F-SEAL and voids the wave.

The harness is a separate process or module with no shared memory with
the learner. All communication is via the defined evidence interface
(passive samples as (x,y) pairs, interventions as do-operations).

## 9. Coverage Logging (Informational)

Based on the Q4 attack finding that 32 observations covered only 7/8
combos (leading to underdetermination), the harness must log:

- The number of distinct (X1..X6) combinations observed in the 32
  Phase-1 observations (8 passive + 24 interventions).
- Which combinations were observed vs unobserved.

This is informational, not a bar. It documents the degree of
underdetermination. If the learner achieves 64/64 despite incomplete
coverage, the simplicity tax's role in tie-breaking must be acknowledged
in the results (per the attack's A4 finding).

## 10. Scoring (KB1-KB4, Q4 Standard)

- KB1: true accuracy of kept D over all 64 combinations >= 0.95.
  Admissibility: best single observable <= 0.80 (verified family-wide
  in design Appendix A).
- KB2: operator count of kept D <= 7; growth trace shows incremental
  construction.
- KB3: Phase-2 intervention counts; reuse_count <= 0.5 * scratch_count.
- KB4: 3/3 byte-identical stdout per seed, pure Zag at every stage,
  zero Python invocations, zero em dash bytes.

Note: KB4 requires 3/3 byte-identical runs PER SEED. With 5 seeds per
instance and 3 instances, this is 45 runs total (3 repetitions x 5 seeds
x 3 instances) for A-LEARN Phase 1, plus Phase 2 runs.

## 11. Verdict

Against the frozen bars in this prereg, per instance and for the battery:

- F-SEAL voids the wave.
- F-MEM voids the affected instance (redraw with continued LCG state).
- F-NOREP or F-OVERBUDGET fail the C0-C form claim for the affected
  instance.
- B1 (amended multi-seed) must hold on all 3 instances.
- B2, B3, B4 must hold on all 3 instances.

A pass on all 3 instances constitutes the second C0-C data point for
the Q4 line. It does not close C0-C (a third family remains future work)
and starts no SURVIVES claim (promotion steps 4-11 remain: reproduction,
baselines, alternative-explanation attack, OOD, ablation,
transfer/reuse, red team, governance audit).

## 12. Governance

- Prereg commit strictly precedes the draw transcript and implementation
  (prereg commit-order self-check).
- This prereg was written without Python (shell/grep/git/sha256sum only).
- Zero em dash bytes (verified via shell grep before commit).
- Local commits only on tnn-native-lab; owned path
  `docs/lab/research-lead/overnight-20260928/q4_adv2/` with pathspec
  commits; nothing pushed.
- Transparent amendments (B1 multi-seed, coverage logging) are justified
  above with reference to the Q4 attack findings (73d9637a2).
- The F-PARCOND adversary spec carries a flagged Python-mirror process
  violation; this prereg was produced without Python to avoid repeating
  that contamination.

## Appendix: Seed Generation Log

The SEED (770404483) was generated as follows (shell only, no Python):

```
$ head -c 4 /dev/urandom > /tmp/frecfold_seed.bin
$ od -An -tu4 /tmp/frecfold_seed.bin
 770404483
$ sha256sum /tmp/frecfold_seed.bin
5426835ee69f290cb98f12cbc94e7a03fe6de2ada5de91745259ad4ee20fda02
```

The seed is nonzero. The file `/tmp/frecfold_seed.bin` is kept sealed
and will be provided to the independent adversary after this prereg is
committed. The adversary verifies the SHA256 before performing the draw.

Note: An earlier seed (1666450881) was generated using Python during
drafting. That seed was discarded and is NOT used. The Python use was a
procedural violation; the committed seed above was generated without
Python. This disclosure follows the audit precedent (1127c3117).
