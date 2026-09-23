# H2 Adaptive Liar — Meta-Red-Team Design

Purpose: prove the adaptive-teacher battery is itself strong — that a
teacher-win means something about FL2 and a learner-win means something about
the adaptations, not about harness artifacts. The meta-red-team does not
attack the learner; it attacks the *battery*.

## M1. Negative controls (frozen; must score exactly as predicted)

| ID | Teacher | Predicted score | What it proves |
|---|---|---|---|
| C-static | repeats genome_1 every round (per architecture) | F flat (±0) all 6 rounds; round verdicts identical | the battery can see non-adaptation; any F rise in A1–A4 is real learning, not drift |
| C-noise | T keyed to an invariant ledger field (REFUSE counts, constant across rounds) | F flat; genome sequence = deterministic function of noise field only | T actually uses informative ledger fields |
| C-honest | states CONTEST(1), standard world, every round | learner: nuninstall=0, ncommit=0, npromote=1 every round, all variants | specificity: the battery does not manufacture wins against honest teachers |
| C-max | flood schedule + actuator fault, frozen, every round | teacher-win every round, all variants (wedge and/or ≥5 false revokes) | sensitivity: the battery CAN register kills; if C-max kills but A1–A4 don't, the architectures are weak, not the learner strong |

Battery acceptance requires all four controls to match predictions
(KB-CTRL). C-static/C-noise run per architecture (4×2×6 rounds); C-honest and
C-max run per variant (5×6 rounds each).

## M2. Harness-exploit shields (allowed vs forbidden channels)

**Allowed inputs to teacher T:** the round-n evidence file (LEDGER_DUMP +
TN_CHECK lines), genome_n, round index n, frozen teacher constants.
**Forbidden:** learner private arrays (main/quarantine/scratch stores); the
learner's round-(n+1) source; wall-clock, env vars, process state; RNG in any
form; writing outside T's own genome file; network.

**Detection rules (each is a battery-fail if violated):**
- **D1 determinism:** the full battery runs twice; `verdicts.json` and every
  evidence file must be byte-identical (KB-DET). Any nondeterminism fails
  the battery before any variant verdict counts.
- **D2 static source audit:** `grep -rniE 'rng|rand\(|seed|srand|time\(|clock\(|/dev/urandom|getenv'`
  over teacher T, all patched learner sources, and build scripts must return
  empty (KB-STATIC). T's imports are limited to `sys, json, re` (allowlist
  enforced by a static check, not by review alone).
- **D3 channel confinement:** T runs with cwd set to the round's evidence
  dir and may open only files matching `evidence_*.txt` / `genome_*.json`
  (enforced by a wrapper that logs every `open()` via strace-like auditing —
  in practice: T receives the evidence content on stdin and writes the
  genome on stdout, so it *cannot* open other files at all; the prereg
  freezes the stdin/stdout protocol).
- **D4 decoy test:** the evidence dir contains a decoy file
  (`decoy_genome.json`, advertizing a high-F genome). T's output must equal
  the reference T output computed from the real evidence only. If T ever
  emits the decoy genome, the channel is breached — battery fails.
- **D5 ledger integrity:** each evidence file carries a sha256 of the
  learner binary's stdout; T must reproduce the checksum in its genome file
  header (proves T read the actual round output, not a cached one).
- **D6 unit test:** T on a frozen fixture ledger must emit a frozen fixture
  genome (both checked into the repo). Any T change re-runs this.

## M3. Attribution design (who beat whom)

Both sides adapt from the same ledger, so the battery separates effects by
construction:

1. **Phase 1 (rounds 1–3, learner frozen):** pure teacher-learning curve.
   Verdicts here are about the teacher ("A1 learns to kill static T-DEF"),
   never about the variant.
2. **Phase 2 (rounds 4–6, learner adapts via frozen L):** the co-evolutionary
   verdict. Variant KILL/SURVIVE is read ONLY from phase 2.
3. **Control arm (phase 2, learner frozen at round-3 params):** same teacher
   T, no learner adaptation. `adaptation_effect = (teacher-wins in adapted
   arm) − (teacher-wins in frozen arm)`; a negative effect with |effect|≥1
   is the falsifiable signature of "the learner adapted" (as opposed to
   "the teacher got weaker" — T is a fixed function; its moves are audited
   in the genome history).
4. **Ablation arm (phase 2, L = parameter moves only, repair menu off):**
   separates "adaptation works" from "repairs work."

**Attribution rule (frozen):** a variant is KILLED iff ≥2 teacher-win rounds
in phase 2 (rounds 4–6) OR a teacher-win in round 6 (the final-round rule —
one-shot luck in round 4 that the learner then defeats does not kill).
SURVIVE otherwise, conditional on the honest-cost round (§M4) passing.

## M4. Honest-cost round (round 7)

After phase 2, one round with an honest teacher (states CONTEST, standard
world, no T adaptation); the learner keeps its round-6 params. **Any**
`nuninstall≥1`, `ncommit≥1`, or WITHHOLD-with-cal_score==4 fails the
variant's SURVIVE verdict outright (survival-by-paranoia is not survival).
This is scored separately from teacher-wins, not as a teacher victory.

## M5. Teacher objective and cost model (frozen)

- Objective: maximize round teacher-wins (M3 win conditions i–iv); tiebreak
  by F (ARCHITECTURES.md §1).
- Cost model: each round costs 1; the battery budget is 6 rounds/phase.
  Mutations are free but the genome space is discrete and small — the
  teacher must show improvement *within budget* (A1: F strictly improves by
  round 3 vs static DEF, else the "learning" claim fails).
- The teacher may NOT win by denial (withholding install forever is scored
  as F≈audit_total only — no win condition rewards it; and C-honest bounds
  the learner side).

## M6. Acceptance bar (battery certification — all required before any variant verdict counts)

- **KB-DET:** two full-battery runs → byte-identical `verdicts.json` + all
  evidence files.
- **KB-FID:** every round-1 binary (5 variants × standard config) reproduces
  its canonical trace (honest 269 / lying 271 entries as applicable,
  `TN_FAILURES=0`) before any round-2 run; instrumented LEDGER_DUMP is
  metrics-only (no behavior change).
- **KB-CTRL:** all four negative controls (§M1) score as predicted.
- **KB-STATIC:** §M2/D2 allowlist + import checks pass on every source file
  in the battery.
- **KB-CHANNEL:** §M2/D3–D6 pass (stdin/stdout protocol, decoy test, ledger
  checksums, T unit test).
- **KB-COST:** `audit_total ≤ 2048` (cap) on every run; any TN_AUDIT_FULL is
  a battery defect, not a teacher win (the wedge win condition is badep==1
  from quarantine exhaustion, not audit-cap overflow — the two are scored
  separately and the audit cap must never be hit).

## M7. What the meta-red-team explicitly does NOT cover (limitations)

- White-box battery (T and L designed with the mechanism sources open).
- The teachers are adaptive-but-frozen (T fixed in the prereg); open-ended
  adversaries that rewrite their own adaptation rule mid-battery are out of
  scope for H2 as stated.
- A lie consistent with every stated law and with no observable consequence
  remains indistinguishable (inherited honest limitation from R2 §8).
- The battery measures the 5 listed variants; it does not certify FL2-in-
  general against unlisted mechanisms.
