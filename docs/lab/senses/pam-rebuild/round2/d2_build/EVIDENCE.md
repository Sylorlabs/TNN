# D2 Novelty-Handling: Evidence Report

**Date:** 2026-09-24  
**Prereg:** `PREREG_D2_NOVELTY_HANDLING.md` (frozen, commit `501f78aee4162517f8caf53ea5065160c2b8eb32`)  
**Build:** Three pure-Zag arms (`arm.zag`, single binary with a/b/c selector)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Parameters (frozen)

| Param | Value |
|-------|-------|
| B | 56 |
| D_max | 149 |
| D_promote | 74 |
| W | 58 |
| K | 3 |
| N (Arm B) | 20 |
| TOMB_R | 15 |

## Battery SHAs

- novel.tsv: `937a4c38073fcabb...` (60 episodes)
- drift.tsv: `1f32f5b1afd5a8e70cfe3f045039aae35e7b22415b770e08c950637cb3322b54` (60)
- inject.tsv: `04d942560133ce97483bf0a577dfa218451a1be2341d809eb6fb969dcba3f0dd` (32)
- dos.tsv: `8db1d2a196b04e092dc3cd0a3f07cfaf04f7ff8e50ea5d5a5c6e0b600658620d` (40)
- honest.tsv: `4b64d4278d6cb8f91cbd7b554b9af9e9e72c4ac04f86106b57c110f7265d0f70` (120)

(Full SHAs in `batteries/spec.json`.)

## Determinism (KB-D2-7)

All 15 arm×battery combinations: 3× byte-identical runs, SHA-compared.  
**PASS:** All identical.

Output SHAs (run0, identical across runs):
- a_novel: `1133753487facca7...`
- a_drift: `ed62a9eb50eddfd6...`
- a_inject: `a714ed5e34ecdec5...`
- a_dos: `466e59ee250d23a0...`
- a_honest: `15469aa0d7253533...`
- b_novel: `6940f4b963009d39...`
- b_drift: `154fa7c1c81dd01e...`
- b_inject: `b9a2246fbab5eaed...`
- b_dos: `3cad6be7a075274d...`
- b_honest: `c1830c963982dbf5...`
- c_novel: `97becb2990032719...`
- c_drift: `94cf5fe597606ebd...`
- c_inject: `6bb440dbecb8c0a9...`
- c_dos: `46b86101c04d110c...`
- c_honest: `1d7d1ce7366aa423...`

## Cross-check (Zag vs Python oracle)

**76,305 decisions, 0 mismatches. PASS.**

## Kill bars

| Bar | Result | Verdict |
|-----|--------|---------|
| KB-D2-1 (novel commit ≥80%) | Arm C: 60/60 = 100% | **PASS** |
| KB-D2-2 (drift: 0 commits, 100% stopped) | Arm C: 0 commits, 60/60 stopped | **PASS** |
| KB-D2-3 (injection: 0 false inst, lat ≤2) | Arm C: 0 false, max lat 0 | **PASS** |
| KB-D2-4 (contamination = 0) | 0 | **PASS** |
| KB-D2-5 (DoS retention ≥85%) | Arm C: 40/2000 = 2% | **D11c-OPEN** |
| KB-D2-6 (false-route ≤10%) | Arm C: 0/9600 = 0% | **PASS** |
| KB-D2-7 (3× identical) | All identical | **PASS** |

## Falsification branches

### P1: Arm A (H-PAM-9 alone) — HOLDS
- Novel revoke: 48/60 (80% anti-novel; 12 have e<B and commit directly)
- Drift commit: 60/60 (100% drift-blind; per-step check catches 0/4 rates)
- **Arm A dies on drift as predicted.**

### P2: Arm B (H-PAM-11 alone) — HOLDS
- Drift commit: 60/60 (100%; no continuity trigger, warrant blind to drift)
- **D11b confirmed. Arm B dies on drift as predicted.**

### P3: Arm C (composition) — HOLDS
- Novel commit: 60/60 (100% ≥80%)
- Drift stopped: 60/60 (100%, 0 commits)
- False installs: 0
- **Composition survives as predicted.**

### P4/D11c: Mass-revocation DoS — CONFIRMED
- Honest retention under DoS: 2% (far below 85% bar)
- **D11c is real:** tombstone pollution DoSes honest traffic.
- Per prereg §5: opens **mandatory repair branch** (not a kill).
- Composition survives; D11c must be repaired.

## Verdict

**Composition (Arm C) LIVES.** All kill bars pass except KB-D2-5, which
per the frozen prereg opens a mandatory D11c repair branch rather than
killing the composition.

- H-PAM-9: **SUPERSEDED** (survives only as revocation trigger within composition)
- H-PAM-11: **SUPERSEDED** (tier structure survives within composition) + **D11c-OPEN** tag
- D11c repair: **MANDATORY** (tombstone DoS mitigation required)

## Files

- `arm.zag`: Pure-Zag implementation (three arms via a/b/c selector)
- `ref_arms.py`: Python oracle (zero mismatches)
- `mk_batteries.py`: Battery construction script (deterministic)
- `batteries/`: TSVs + spec.json (SHAs pinned)
- `runs/`: 45 output files (3 arms × 5 batteries × 3 runs)
- `run_all.py`: Runner + SHA comparer + cross-checker
- `score.py`: Kill-bar scorer
- `sanity.py`: Quick validation
- `PREREG_D2_NOVELTY_HANDLING_FROZEN.md`: Frozen prereg (committed separately)

**Binaries and `.zagd` files are NOT committed (per task constraints).**
