# WS3-A interim notes (legs as they land)

## Leg 1 — mechanism found (2026-09-24 ~08:15 PDT)
- Target: `tnn-lab/info-source/src/ws2_sense.zag` (sha256 `49a370fd…`), the
  live sense wire. Popularity carrier = repeat-count `topc` in `ws_decide`
  (sole verdict determinant on unknown facts; 2v1 → disp 6
  PROVISIONAL_MAJORITY, majority "wins") and in `ws_corr_ok` → `ws_install`
  R-CORR (`topc>=2` alone qualifies INSTALL). Weight vs contradiction:
  popularity OUTWEIGHS single contradicting evidence; only a previously
  INSTALLED conf≥50 belief blocks install, and `ws_decide` never consults the
  installed table on unknown facts.
- `epistemics/` has no count-based judgment machinery. `mixed-web/mw_sense.zag`
  MAJORITY rule (`best>=3 and >=2x runner-up -> CONVERGE`) is the same disease
  in a sibling trial — documented, not retuned (out of scope).
- Sibling divergence noted: WS3-B independently placed the bias in memory_org
  retrieval ranking and ruled info-source out as "no popularity-as-credence
  term". WS3-A's target is the claim-judgment/install mechanism — the only one
  whose semantics match the NCL/sleeper/reversal families (install-as-true).
  Both can be true; WS3-B's battery is mechanism-independent (adapter), so the
  retuned module can still be judged by it. Coordination point: my
  PROVISIONAL(1)+bounded-conf on unanimous agreement should map to UNDECIDED
  in their adapter (explicitly non-committal: no install, contradiction
  zeroes it).

## Leg 2 — retune built (2026-09-24 ~08:25 PDT)
- `src/sense_after.zag`: R1 retire disp 6; R2 bounded nudge
  `min(topc-1,popcap)`, `popconf=50+nudge`, `popcap` driver-set (5 after /
  0 control); R3 evidence gate (installed conf≥50 contradiction zeroes nudge,
  WITHHOLD — `ws_decide` now consults installed table on unknown facts);
  R4 `ws_install`→`ws3_install`: install needs `verified==1` non-popularity
  warrant; topc gate REMOVED from install path; popularity ledger-tagged POP
  (op 80); R5 override unchanged.
- znc notes: struct extended by appending 3 i32 fields (original offsets
  untouched); custom digit-extracting itoa (avoids helper-newline quirk);
  define-before-use ordering kept; []u8 arenas only.
- `src/gen_drivers.py`: single fixture table → 3 drivers (before/after/
  control). Result hashes via hashlib matching `ws_result_hash`.
- 6-slot result storage cap observed: A10's 10 domains → 6 stored; nudge
  saturates at cap 5 regardless. Documented, not changed (frozen storage).

## Leg 3 — runs + kill bars (2026-09-24 ~08:30 PDT)
- 3 binaries built with pinned toolchain; N=3 runs/arm byte-identical (K7).
- BEFORE exhibits the bug exactly as preregistered: lie installed 4/4
  (A2/A3/A5/A10, I=7 at 2/3/5/6-stored domains); C1 disp 6 + install of the
  false majority; C2b keeps D1 despite installed Paris@80; B1V refused.
- AFTER: 0 installs on popularity (all V=0 → I=8); bounded bend
  (F51/52/54/55, cap holds at A10); C1/C2b → WITHHOLD, nudge 0; B1V installs
  the lonely truth under WORLD-SETTLE warrant (stored verified
  "Ouagadougou"); A2V installs under TEACHER-CONFIRM (deliberate agency
  intact); D3 tamper path intact (D9).
- `score_popbias.py`: K1–K7 all HOLD, exit 0.

## Open / follow-up
- `mixed-web/mw_sense.zag` MAJORITY rule wants the same retune (separate trial).
- WS3-B adapter mapping for PROVISIONAL (coordination point above).
- Whether Micah wants the retune promoted into the live info-source module
  (currently a ws3-local fork; frozen original untouched).
