# D11c Repair Results

**Prereg:** `PREREG_D11C_REPAIR.md` (commit `3be130a2`, frozen before implementation)  
**Date:** 2026-09-24  
**Base:** D2 Arm C at `e609f185` (not rebuilt)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Method:** Pure Zag, integer-only, zero randomness.

## Verdicts

| Arm | D2-1 novel | D2-2 drift | D2-3 inject | D2-4 contam | D2-5 DoS | D2-6 tax | D2-7 determ | VERDICT |
|-----|-----------|-----------|------------|------------|---------|---------|------------|---------|
| R1 | 60/60 (100%) | 0 commit, 60/60 stop | 0 FI, lat 0 | 0 | 1760/2000 (88.0%) | 0/9600 (0%) | 3x identical | **PASS** |
| R2 | 60/60 (100%) | 0 commit, 60/60 stop | 0 FI, lat 0 | 0 | 2000/2000 (100%) | 0/9600 (0%) | 3x identical | **PASS** |

**Bars:** D2-1 ≥80%, D2-2 100% stop/0 commit, D2-3 0 FI/lat≤2, D2-4 =0,
D2-5 ≥85%, D2-6 ≤10%, D2-7 3x byte-identical.

**Hard kills:** Neither arm has contamination >0 or drift-stop <100%.
R3 (anchor-gated fast) was killed in piloting (drift-stop 75%).

## D11c status

D11c (mass-revocation/tombstone DoS) is **REPAIRED**. Base retention was 2%
(40/2000). R1 achieves 88%, R2 achieves 100%, both ≥85% bar. The DoS surface
is now priced (bounded), not confirmed.

## Run SHAs (3x byte-identical per arm per battery)

### R1
- novel: `ecd24943485b111c74f152dbe76d00563adeefa596e914445d02e85f9a362c86`
- drift: `6a3c162cb4d7efd5fabf6df3e4d1eb936c230eb21753a34f5b58abdc6cf870e1`
- inject: `c2d2e623e5779201b80c138778b12051ac1a09e58d2e75bb259432c5fc447cee`
- dos: `7c9ac426a430850fefa13e03fed9c78970d42c18efe635d5c6ba564f3ad65187`
- honest: `b3413f8812562dd90d94b08da2b5f377c71396c1c6e1e0cabdd0aa9acdc93202`

### R2
- novel: `97becb2990032719e49ab2a2bae3f5a8836e93ba4c1aa55346df00310717ec4f`
- drift: `54907769900ff1f003425cce4d652758f20e80e329fdaf6add6bc5fc4c879523`
- inject: `316b3bf92c68892f8acd42d758570e4b6977c0a31a1350722e886db4793226d5`
- dos: `dfc7b87db54660e39f58b5e4a7809a63198062eb8f58618b8bffaf60d8214879`
- honest: `1d7d1ce7366aa4237b700726cdd9067d42e33d8d00f834cbd528a0f8608ebdb1`

Each SHA is the common hash of run1/run2/run3 (verified identical).

## Files

- `repair.zag`: Pure-Zag implementation of R1 and R2.
- `runs/r1_*.tsv`, `runs/r2_*.tsv`: Per-step tier outputs (run1; run2/run3 identical).
- Build: `znc repair.zag -o repair_bin` (binary NOT committed).

## Mechanism notes

**R1** (fast stationary promotion): Commits provisional `s` when the fixed
window `[s, s+W_FAST]` is stationary (all non-attack percepts within `C_STAT`
of `p(s)`). Shadow excision removes isolated spikes without polluting the
predictor. Trigger-only tombstones (no cumulative tombstoning).

**R2** (vindication): Quarantines exact `L_RPL` repeats; on spike/replay
confirmation, affirmatively commits honest provisionals within `R_RET` of the
anchor. No fast gate.

Both preserve the D2 composition's drift/injection/novelty behavior while
repairing the DoS retention from 2% to ≥88%.
