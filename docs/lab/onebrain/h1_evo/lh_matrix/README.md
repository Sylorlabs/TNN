# LH matrix — integrator long-horizon evidence

Two deterministic mixed propose/commit/revoke/promote streams, each run on
all four variants (V0 control, V1 H-organ, V2 H-sep, V3 full compose) at
multiple horizons, 3× byte-identical reruns per cell.

## Stream A — R1-sensitive (V1 crew's `lh_stream.zag`)

12-episode cycle: propose/revoke/drifted-commit/novel-commit/
corroborated-recommit/propose/promote/commit/revoke/novel-commits.
Horizons: 300 eps (10x), 3000 eps (100x).

For V0/V2 a matrix-only compat shim `pam_has_contradiction()->0` was
appended to the *matrix copies* of `ob_pam.zag` (V0/V2 predate the R1
contradiction register; the shim is informational-tally-only and is NOT
part of any variant).

Evidence: `ev/A_<variant>_<horizon>_<run>.txt`
(`A_v0_300_1.txt` … `A_v3_3000_3.txt`), plus `A_<v>_<h>_dec.txt`
per-episode decision deltas derived for the divergence analysis.

## Stream B — R3-sensitive (V2 crew's `h3_lh.zag`)

4-episode blocks: PROPOSE{11,(41k)%129} / COMMIT{1,30+(k%5)} /
REVOKE{11} / PROMOTE{11}; claim stride 41 forces commit-ring collisions at
blocks 7,14,21 (mod 129). Horizons: 300 (1x), 3000 (10x), 30000 (100x).

Evidence: `ev/B_<variant>_<horizon>_<run>.txt`.

## Results

See `../v3_full/COMPARISON_MATRIX.md` §3 for the full table. Headline:
- Stream A: V1 SHAs reproduce the crew's recorded values exactly; V2 ≡ V0;
  V3 shows exactly the 7 preregistered R1 withholds at both horizons
  (no widening at 100x); V3-vs-V0 divergence fully classified
  (7 withholds + L4 56-row capacity effect).
- Stream B: (see COMPARISON_MATRIX.md §3).
- Bars on every cell: no panic; 3× byte-identical; prefix-consistent
  across horizons; no new failure mode at 100x.
