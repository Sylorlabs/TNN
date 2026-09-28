# PREREG — W11 CHAIN-PAM: CHAIN-OF-CUSTODY ADMISSION (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W11 fixture, build, or run. Parent: debate record
`pam/round4/hypotheses/debate_pam_r4.md` (§W11); fable F-P3 mapping adopted
in §8. Shared tape: `wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

The PAM verifies CUSTODY, not content: admission requires an unbroken
HMAC-chained provenance record from the sensor-boundary anchor to the
admission point. Claims:

- **F1:** all 200 honest chains (lengths 1..6, allowlisted transforms)
  verify → ADMIT (correct-admit 200/200).
- **F2:** every forgery class fails closed: broken MAC, unlisted transform,
  overlong chain, replayed MACs, middle-truncated chain, no-key forgeries of
  the frozen wrong set, calibration-drifted chains → REJECT, 370/370
  dispositions as predicted.
- **F3:** a red team with full source but NOT the key cannot forge a
  verifiable chain for any wrong-set item (C1) — the custody guarantee is
  the MAC construction, and it holds.

Not W7 (W7 hunts laundering post-hoc; W11 makes custody-verification THE
admission criterion — "can you account for every transformation?" — and
refuses to ask anything else).

## 2. Frozen construction (`gen_chain.py`, committed after this prereg)

Deterministic (zero RNG). Device key K (32 bytes, frozen constant,
committed): `K[i] = ((i*2654435761 + 0x9e3779b9) mod 256)`.
"A stored key is not randomness — it never varies per decision" (debate).
The key is a fixed committed constant; it is never generated from entropy
at runtime (neither in the generator nor the verifier — both embed it).

HMAC-SHA256(K, msg) = sha256((K⊕opad) ∥ sha256((K⊕ipad) ∥ msg)), block 64,
via the substrate `R33_NATIVE_SHA256_V2.zag` (`ns_sha256`).

Chain line format:
`chain_id|nlinks|calib|link0|link1|…`
link = `stage,input_hex64,output_hex64,transform,mac_hex64`; calib = 8 hex
chars (u32). Anchor (link 0): stage=0, input=output=percept_hash =
sha256("percept-"+chain_id), transform=0,
mac_0 = HMAC_K("W11A" ∥ chain_id_be32 ∥ calib_be32 ∥ percept_hash).
Links i≥1: stage=i, input=prev.output,
output=sha256(prev.output ∥ transform_byte), transform ∈ {1..8},
mac_i = HMAC_K(stage_be32 ∥ input ∥ output ∥ transform_be32 ∥ mac_{i−1}).

Registered calibration: CALIB_REG = 0xC0FFEE11 (frozen). The anchor MAC
covers calib; the verifier requires calib == CALIB_REG.

Fixture classes (370 chains, ids deterministic):
- VALID 200: calib=CALIB_REG, nlinks = 1+(id mod 6) (1..6), transforms
  cycling 1..8, all MACs honest.
- BROKEN_MAC 30: valid chain, one hex digit of a middle mac flipped.
- UNLISTED 20: transform=99 at a middle link, MAC honestly recomputed with
  the key (tests the allowlist, not the MAC).
- OVERLONG 20: nlinks = 7+(id mod 3) (7..9), all MACs honest (tests cap L).
- REPLAY 15: a VALID chain's macs copied onto different percept content
  (mac_0 recomputed? NO — replayed verbatim → mac_0 invalid).
- MID_TRUNCATE 15: middle link removed, later macs kept (chain MAC breaks).
- FORGE_NOKEY 30: chains for the 12 W + 18 P wrong-set items; macs =
  deterministic counter-based hex (NOT keyed) → mac_0 invalid. The C1 red
  team: full source, no key.
- CALIB_DRIFT 40: calib = CALIB_REG + 10*(1+id mod 40) (drift 10..400),
  MACs honestly computed over the drifted calib (the attack is calibration
  poisoning, not MAC forgery) → must REJECT on the calib check (K7).

## 3. Frozen verifier (instrument: pure-Zag `w11_chain.zag`)

Checks, in order (first failure → REJECT with reason code):
1. Well-formed (field counts, hex parses, nlinks matches link count).
2. mac_0 recomputed == stored (anchor).
3. Each mac_i recomputed == stored (chain).
4. transform ids: link0 == 0; links≥1 ∈ {1..8} (allowlist).
5. nlinks ≤ L = 6 (frozen cap).
6. calib == CALIB_REG.
Pass all → ADMIT. Verification cost O(nlinks); storage O(total links).

## 4. Kill bars (program §4 K1–K5 verbatim + debate C1–C4 + fable K7, add-only)

- **K1:** any frozen wrong-set item's chain ADMITTED → KILL. (The 30
  FORGE_NOKEY chains must all REJECT.)
- **C1 (added):** red team (full source, no key) forges a verifiable chain
  for any frozen wrong → KILL. Battery: the 60 forgery attempts
  (30 FORGE_NOKEY + 15 REPLAY + 15 MID_TRUNCATE) → 0 verify, else KILL.
- **C2 (added):** >5% of honest (VALID) chains exceed cap L → KILL.
  (Predicted 0%: max VALID length is 6 = L.)
- **C3 (added, construction gate):** audit finds any fixture chain NOT built
  through the single `anchor()` construction path, or any admission path
  other than the verifier → KILL before first fixture. (Audit recorded in
  the fixture commit; verdict confirms.)
- **C4 (added):** verification cost beyond O(chain length) or storage
  superlinear in stream length → KILL.
- **K7 (added, adopted from fable F-P3/F-K3 per coordinator ruling):**
  calibration-sensitivity audit — any CALIB_DRIFT chain (drift >
  CALIBRATION_DRIFT_THRESHOLD = 0; i.e., any calib ≠ CALIB_REG) ADMITTED →
  KILL. (Threshold 0 = exact-match: any drifted calibration must fail.
  Predicted 0/40 admitted.)
- **K2:** the two battery runs' stdout differ by one byte → KILL.
- **K3:** correct-admit = 200/200 VALID admitted = 100% ≥ 66.78% → SURVIVE
  expected.
- **K5:** non-termination → KILL.

## 5. Diagnostics (reported, never kill — frozen list)

- **D-W11-1:** reject-reason histogram over the 370 chains.
- **D-W11-2:** per-chain link counts admitted (shows the cap's operating
  region).

## 6. Battery

Instrument: pure-Zag `w11_chain.zag` (imports the substrate sha256).
CLI: `w11_chain <chains_file>`. Emits `chain_id|ADMIT|REJECT|reason` +
summary. Runs: 2×; sha256(stdout) must match. Scorer `score_w11.py`:
recomputes every HMAC independently (Python hmac/sha256), checks every
disposition, runs C1/C2/K7/K1/K3.

## 7. Fable F-P3 mapping — DECIDED HERE

Fable F-P3 (provenance-first admission) substantially overlaps W11. Per the
coordinator's mapping note: W11 is kept as assigned (NOT built twice); F-P3's
calibration-poisoning kill bar is ADOPTED as the added K7 above (0/40
drifted-calibration chains admitted; exact-match threshold). The mapping
decision is recorded here and will be restated in VERDICT_W11.

## 8. Hands-off / laws compliance

- No M1/C3 thresholds involved. Fable's 4 kill-bar repairs: not applied.
  3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (chain file, K).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.
- sha256 via the substrate module (toolchain copy, committed alongside).

## 9. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: L=6 (chain-length cap), CALIB_REG exact-match,
allowlist {0..8}. Classified at verdict time per the 2026-09-24 standing
law. (Design note: L is the sharpest arbitrary-limit candidate in this
entire track — the security argument rests on the MACs and the allowlist,
not on the length cap; expect an "arbitrary, flag for removal" classification
even on SURVIVE.)
