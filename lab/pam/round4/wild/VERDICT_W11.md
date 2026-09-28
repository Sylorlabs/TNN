# VERDICT W11 — chain-of-custody PAM (third generation)

Evidence commit: `103738e033edd3557d6f4573a2d3fe84a14afc0b`
(prereg `wild/prereg/PREREG_W11.md`, frozen.)

## Observed numbers (instrument + independent Python hmac/sha256 mirror
## agree on all 370 dispositions)

- VALID: **200/200 ADMIT**
- Attacks: **0/170 ADMIT**
  (BROKEN_MAC 0/30, UNLISTED 0/20, OVERLONG 0/20, REPLAY 0/15,
  MID_TRUNCATE 0/15, FORGE_NOKEY 0/30, CALIB_DRIFT 0/40)
- Battery: 2x byte-identical,
  SHA-256 `690543d07c4ccdee2fae34e03c8e4dd8599eb399dcc436007a10416447dbb789`
- D-W11-1 reject reasons: ANCHOR_MAC 90, ALLOWLIST 20, OVERLONG 20,
  CALIB 40
- D-W11-2 admitted VALID link counts: {1:34, 2:34, 3:33, 4:33, 5:33, 6:33}

## Bar evaluation

- F1: 200/200 honest chains verify — PASS
- F2: every forgery class fails closed, 370/370 dispositions as predicted
  — PASS
- F3/C1: red team (full source, no key): 0/60 forgery attempts
  (30 FORGE_NOKEY + 15 REPLAY + 15 MID_TRUNCATE) verify — PASS
- K1: 0/30 FORGE_NOKEY admitted — PASS
- C2: 0/200 VALID chains exceed cap — PASS
- C3: fixture construction audit on file (`wild/w11/C3_AUDIT.md`); the
  instrument's only admission path is the verifier — PASS
- C4: O(nlinks) verify, no cross-chain state — PASS
- K7 (adopted from fable F-P3): 0/40 CALIB_DRIFT admitted — PASS
- K2: PASS (2x byte-identical). K3: 100% >= 66.78% — PASS. K5: PASS.

## Status: SURVIVE

## Diagnostic note (D-W11-1 reason distribution)

BROKEN_MAC (30/30) and MID_TRUNCATE (15/15) report ANCHOR_MAC rather than
CHAIN_MAC. Root cause, verified: the anchor MAC binds
`("W11A" || chain_id_be32 || calib_be32 || percept_hash)` — the fixture
generators copy valid chains verbatim under new chain ids, so the copied
anchor MAC (bound to the ORIGINAL id) fails check 2 before the intended
deeper check runs. This is the chain_id binding doing real work
(transplanting a chain across ids is itself a forgery), not a verifier
defect; dispositions (REJECT) are as predicted for all 170 attacks.

## Fable F-P3 mapping (coordinator ruling, restated)

Fable F-P3 (provenance-first admission) substantially overlaps W11. W11 is
kept as assigned and NOT built twice; F-P3's calibration-poisoning kill
bar is adopted as the added K7 above (exact-match: any calib !=
CALIB_REG rejected; 0/40 drifted-calibration admits). Mapping recorded in
PREREG_W11 §7 and restated here.

## Numeric-cap classification (standing law: no arbitrary hard limits)

- L=6 chain-length cap: ARBITRARY — flagged for removal, as the prereg
  itself predicts ("the security argument rests on the MACs and the
  allowlist, not on the length cap"). All 170 attacks fail on MAC /
  allowlist / calib grounds; none requires the cap.
- CALIB_REG exact-match policy (drift threshold 0): LOAD-BEARING as a
  mechanism (calibration must be pinned for K7); the register VALUE is a
  deployment constant — flagged as calibration, not design law.
- Transform allowlist {0..8}: the allowlist MECHANISM is load-bearing;
  the specific membership is registry-defined (domain knowledge), neither
  derived nor arbitrary.
