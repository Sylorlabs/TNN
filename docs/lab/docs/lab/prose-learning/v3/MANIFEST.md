# MANIFEST — prose-learning v3 package

Packaged 2026-09-22 from `~/workspace/tnn-lab/prose-learning/v3/`.
v2 remains frozen; v3 is a deliberate pure-Zag repair attempt. Verdict: KB3-VIABLE **FAILS (2/4)** —
v1 stays the pinned prose path.

## Contents

| Path | What |
|---|---|
| `PREREG3.md` | Frozen preregistration (normative §§1–7; §8 non-normative hypotheses, added 2026-09-22) |
| `GATE0_RESOLUTION.md` | Gate 0: falsehood-metric dispute resolution (ABS-3 frozen metric) |
| `VERDICT.md` | Final verdict: KB3-VIABLE FAILS 2/4; C4 carried recovery; §11 documents the trigger-expansion prereg deviation |
| `build_inputs3.py` | Dense-input + NEG-rebuild generator (26 checksums verified pre-scoring) |
| `run_legs.sh` | Ablation run harness (A0–A3, 5 champ reps + 5 sub-battery reps, byte-identical gate) |
| `score_legs.py` | External scorer (original-fact mapping; semantic KB3-NOSILENT checks) |
| `src/prose_learn3.zag` | Pure-Zag learner: m0 = v2-compatible, m1 = coref-order repair, m2 = + KEYSOFT tier-3 |
| `src/oracle3.py` | Independent Python oracle (byte-identical on 16/16 championship, 26/28 sub-battery) |
| `src/PROOF.md` | Implementation proof (with 2026-09-22 gate-(a) correction) |
| `src/build.sh`, `src/R33_NATIVE_*.zag` | Build script + pinned substrate deps |
| `inputs3/` | Dense championship inputs (3 phrasings/fact) + rebuilt sub-batteries |
| `inputs3_v2single/` | Single-exposure inputs for A0 (symlinked false_ids) |
| `runs/A0/` … `runs/A3/` | All scored logs, 5 reps each (championship 4×5, sub-batteries 7×5 per leg) |
| `proof/`, `proof_dense/` | Gate (a)/(b) proof inputs and logs |
| `checksums.sha256` | SHA-256 of every packaged file (302 files) |

Excluded per workspace law: compiled `prose_learn3` binary, `.zagd` files, `__pycache__`,
run scratch dirs (symlinks).

## Reproduction

```sh
cd src && ./build.sh   # needs ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd .. && ./run_legs.sh A3 && python3 score_legs.py A3
```

## Key results (VERDICT.md)

| Leg | Grok | Sol | Step | Muse-native |
|---|---|---|---|---|
| A3 clean mastery | .8026 | .8947 | .9123 | .9956 |
| v1 reference | .8289 | .9649 | .8947 | .8772 |

A3 beats v1 on step and muse-native only (2/4). C4 KEYSOFT carried the recovery
(+0.30–0.56/source); dense phrasing +0.00–0.06 (zero on grok); coref order fixed
CORE 11/24→22/24 with no championship movement. KB3-NOSILENT passes all legs;
KB3-BYTEID passes (5/5 everywhere).
