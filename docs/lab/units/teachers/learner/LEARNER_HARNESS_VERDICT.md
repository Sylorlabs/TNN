# W5 LEARNER+HARNESS VERDICT — B.4/B.5/B.6

**Worker:** W5 (Track B) | **Date:** 2026-09-21 | **Frozen §4 hash:** `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`
**Commit:** `4a6d898c1e6653ae6e4c6266a4aac8efc7b39d76` on `tnn-native-lab` (evidence: pcodec repair, test fix, verdict sheet, verify files, tape345.zag seed fix; harness files deliberately NOT committed — concurrent editor)

## VERDICT

| Bar | Result |
|---|---|
| **B.4 TST-1 tape / replay rule** | **FAIL (blocked)** — wire-format blocker FIXED, harness replay still broken |
| **B.5 Learner's rights (§L)** | **PARTIAL** — deliberation core verified, full integration blocked on harness |
| **B.6 Installed vs learned** | **NOT IMPLEMENTED** — no force-pin mechanism in learner yet |

This is an honest FAIL, not a bent PASS. The frozen rules were not amended.

## HEADLINE: pcodec repaired to frozen §B.3 (W7's blocker — FIXED)

W7 demonstrated the learner's `pcodec.zag` implemented a DRAFT §P layout, causing
`p_decode` on real arm-1 wires to return `rc=3` (P_V_BAD_TEACHER). Zero valid
learner sessions could exist.

**Repair (2026-09-21, W5):** Rewrote `pcodec.zag` wire codec to frozen §B.3:
- Was: kind u16@6, teacher_id u64@8, session_id u64@16, seq u64@24, 54-byte head.
- Now: teacher_id u32@6, session_id u64@10, seq u64@18, kind u8@26,
  span_start u64@27, span_end u64@35, aux_count u8@43,
  ground_count u8@44+ac*16, confidence u8@45+ac*16+gc*16, checksum u64.
- `p_wire_len` corrected to `54 + (aux+ground)*16`.

**Verification:**
- Learner suite re-verified: `test_driver` OK, `test_determinism` 5/5 byte-identical,
  `test_pins` PASS, `test_retract` PASS, `test_tripwire` 15/15 frozen B.8 cases.
- Real arm-1 wire (W7 `verify_flawscore/logs/wires_S0.bin`, 86 bytes):
  `p_decode` now returns **rc=0** (was rc=3). Fields: teacher=1, session=1001,
  seq=0, kind=1, span=36097..36100, ground_count=2.
- N=5 runs byte-identical; `MALLOC_PERTURB_` ∈ {0, 165, 17} all PASS.
- Evidence: `learner/verify/w5_pcodec_frozen.zag` (+ binary logs in verify/).

## HARNESS ZNC-007 + parse fixes (documented, not committed — concurrent editor)

The shared `harness/harness.zag` was repaired for ZNC-007 (19+ indexed narrow
typed arrays → `[]u8` arenas with LE accessors) and a pre-existing `rtape_parse`
off-by-4 (`blen = reclen - 14` → `reclen - 10`; bodies were truncated 4 bytes).

**Blockers found (not fixed — concurrent crew active, ownership unresolved):**
- `session_close` does NOT write the TAPE_FOOTER ("s_tape skipped (causes crash)").
  `rtape_parse` requires `footer_idx >= 0`, so ALL tapes fail validation (nev=-1).
  This is the root cause of 7 failing harness tests + the `pertA` panic
  (`t_footer_units` returns empty slice, test indexes it → out-of-bounds).
- A second worker is concurrently editing `harness.zag` (alast → `[]u8` arena)
  and writing `harness_new.zag` + `soa_p*.zag` probes. I stopped editing to avoid
  clobbering. The file was left in a building state with both our changes.

Harness test status (post my fixes, pre footer fix):
`PASS codec, det5` | `FAIL malformed, seq, tripwire, replay, defer, hint, oracle`
| `pertA` panics (slice index out of bounds).

## LEARNER SUITE (kept, re-verified after pcodec repair)

- `test_driver`: p1 rc=0 verdict=1, p2 verdict=3, tape len=570 — OK.
- `test_determinism`: 5/5 byte-identical — PASS.
- `test_pins`: pin add/reject/overlap/clear — PASS.
- `test_retract`: retract flows — PASS.
- `test_tripwire`: 15/15 frozen B.8 cases — PASS (repaired 2026-09-21; output
  count corrected 14/14 → 15/15).

## FIXTURES (kept, determinism fixed)

`fixtures345/tape345.zag`: zeroed the 32-byte tape chain seed (allocator memory
not guaranteed zeroed). All 7 tapes byte-identical after rebuild; `run_all.sh`
PASS. Baselines in prior W5 notes.

## KEPT vs REBUILT

| Component | Action | Why |
|---|---|---|
| Learner deliberation (`delib.zag`) | Kept (tripwire repaired) | Core logic sound; B.8 now frozen-exact |
| Learner `pcodec.zag` | **Rebuilt** (draft → frozen §B.3) | W7's blocker; zero sessions possible before |
| Harness typed arrays | **Rebuilt** (→ `[]u8` arenas) | ZNC-007 miscompile; reads were corrupt |
| Harness `rtape_parse` blen | **Rebuilt** (`-14` → `-10`) | Pre-existing 4-byte truncation |
| Fixture tape seed | **Rebuilt** (explicit zero) | Nondeterminism on allocator luck |
| Harness footer / full replay | Parked | Concurrent crew; structural workaround |

## PARKED FOR MICAH

1. **Harness TAPE_FOOTER**: the repair crew's `session_close` skips the footer
   ("causes crash"). Without it, no harness tape passes its own validation.
   Needs a proper fix or a prereg amendment — your call.
2. **Concurrent harness editor**: another worker is rewriting `harness.zag` /
   `harness_new.zag`. Ownership needs resolution before further edits or commit.
3. **Full B.5/B.6**: the learner's deliberation core is verified, but appeals
   (max 2, R6), DEFER (max 3), force-pin (B.6), and TST-1 replay need the
   harness repaired or a full isolated rebuild — priority call is yours.
4. **T-14 verdict weights** (30/25/25/10/10 PROPOSED): still awaiting sign-off.
5. **Isolated B.4 verifier** (`verify/w5_replay.zag`): sketched but incomplete —
   Zag has no mutable globals; needs a struct-based refactor. Parked.

## EVIDENCE

- `learner/verify/w5_pcodec_frozen.zag` — frozen-§P decode proof (rc=0 on real
  arm-1 wire; N=5 + perturbations).
- `learner/verify/w5_replay.zag` — incomplete B.4 mechanism sketch (parked).
- Learner test binaries/logs: `/tmp/w5_test_*` (rebuilt 2026-09-21).
- Harness diff (my ZNC-007 + blen fixes): `/tmp/w5_harness_mychanges.diff`
  (includes concurrent editor's alast changes; DO NOT commit as-is).

## COMMIT

No commit made. The pcodec repair (`learner/pcodec.zag`) and test fix
(`learner/tests/test_tripwire.zag`) are ready to commit. The harness was NOT
committed (concurrent editor). Awaiting coordinator direction on commit scope.
