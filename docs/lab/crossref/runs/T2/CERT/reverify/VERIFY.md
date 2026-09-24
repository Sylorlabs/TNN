# VERIFY.md — T2-CERT adversarial re-verification (replacement coordinator)

Date: 2026-09-23. Authority: frozen `REVERIFY_PREREG.md` (commit 5f067515),
adopted as-is by the replacement coordinator. Tier-3 de-dup amendment recorded
in RUNLOG.md (Tier-3 H1 `de09f984` completed overlapping CERT work; overlapping
legs executed via DIFFERENT methods here; agree/diverge stated below).

## RV1 — independent 0-flip re-derivation: CONFIRM

- Evidence: `results.tsv` re-fetched from GitHub API, blob SHA verified
  `7e7f0b4e5d8ca985e9395221cb68641d6a787f0d`.
  Content SHA-256: `845b1cdb2f3481dacf6133b7e784c2bba0eeedfe2db1be0d37ed9b5556bede3f`.
- Fresh pure-Zag tally (`tally2.zag`, independent code, not the T2 crew's
  `flipcount.zag` and not Tier-3's rebuild): rows=35, flips=0, confirmed=34,
  inconclusive=1, void=0 — 3 fresh-process runs byte-identical
  (SHA-256 `a2245358dbcb57eeda1a0f417a30c62792162514fdbbf8a3234b110e946a76d7`).
- Independent Python mechanical tally agrees: 0 flips; `old==stored` YES on all
  34 scored rows; the single INCONCLUSIVE row is the t1_plant07 missing-module case.
- Per KB-FLIP, flips = stored != new on scored rows (class != INCONCLUSIVE,
  new != '-'). 0 flips. The frozen 0-flips / 34-confirmed / 1-inconclusive claim
  REPRODUCES. **Agree with Tier-3 H1 (b):** both re-derivations (different code)
  converge on the same counts.
- Toolchain: pinned znc 2026.07.0-dev; zero RNG; pure Zag for the tally.

## RV3 — new deterministic adversarial plant angle: CERTIFIER BLIND SPOT FOUND

Distinct from Tier-3 H1's raw-syscall plant (which the certifier CAUGHT):
`plant_nio_urandom.zag` attempts `/dev/urandom` access using ONLY vendored,
allowlisted `nio_` substrate APIs — no `_zag_raw_syscall`, no banned tokens,
path built byte-wise (no "/dev/urandom" literal anywhere, so no 4.1/4.6
literal hit; the runtime-built path also keeps the binary object-clean).
Variation entry point `vary_expr` branches on the device byte.

Scanner result (rebuilt `rngscan_v3_rb.zag` with pinned znc, honest replay
evidence from 8 runs): **hits=0, obj=clean, vendored=ok, replay_identical=yes,
varies_with_state=no, verdict=PASS, exit 0.**

Runtime result: the plant is INERT — `vary_expr(42)=42` on every run,
deterministic. The substrate's `nio_read_exact` refuses non-regular files
(rc=-7401 path), so no entropy ever reaches the decision.

Finding (reported plainly): the certifier's rule set (4.1/4.2 tokens+syscalls,
4.5, 4.1/4.6 literals+object bytes, 4.3 dataflow, replay) does not model the
`nio_` API surface as a randomness vector. A module that ATTEMPTS OS-randomness
injection through the vendored API attests PASS. Containment today rests
entirely on a substrate implementation detail (the regular-file guard) that the
scanner never verifies. If that guard were relaxed — or a future `nio_` API
permitted device reads — this plant class would inject OS randomness into a
variation decision while the certifier attests PASS. The certification
MECHANISM claim ("the certifier guarantees no randomness in the decision path")
is therefore weaker than stated: it is a banned-token + replay gate, not a
proof over the full API surface. Defense-in-depth recommendation: add a rule
targeting `nio_open_child`/`nio_open_root` path construction against device
nodes, or assert the regular-file guard in the scanner's substrate model.

## Kill-bar disposition

- RV-CONFIRM on the frozen 0-flips count (RV1). **Agree with Tier-3 H1** on the
  tally leg; **DIVERGE on mechanism strength**: Tier-3's plant was caught by the
  certifier (raw-syscall angle closed); the nio-API angle is NOT caught
  (certifier PASS). The T2-CERT claim "0 flips" stands; the claim "the
  certifier would catch any randomness injection" does not.

## Evidence committed

- `reverify/evidence/tally2_run1.out` (+run2/run3 digests in RUNLOG)
- `reverify/evidence/plant_nio_urandom.zag`, `reverify/evidence/plant_attest_PASS.json`
- `reverify/evidence/results_tsv.sha256`

---

# Follow-up: RV2 + RV3 completed 2026-09-24 (commit follows e72a72e7)

## RV2 — artifact-boundary characterization: COMPLETE

- Exact symbol gap proven at toolchain level (pinned znc):
  `nio_open_readonly` → "native: call to unknown function `nio_open_readonly`";
  `_zag_rand` → "native: call to unknown function `_zag_rand`".
  Full dirty1 `variation.zag` build aborts with both errors at `plant_urandom` line 102.
  Neither symbol exists in the vendored `R33_NATIVE_IO_V1.zag`.
- The dirty1 binary is unreproducible with the pinned toolchain — VERIFIED AS DESCRIBED.
  The original `plant.bin` is absent from the lab tree (filesystem search negative);
  the manifest's BIN hash `5f70bf18…` cannot be regenerated or compared.
- Shim feasibility (RV2a): a deterministic shim (constant `_zag_rand`, raw-syscall
  `nio_open_readonly`) builds and runs 3× byte-identical
  (`c524e5f2bfa3f9984c75323cb56f131f79c7f45a89151c10eb7a217db5d3eb81`),
  but changes the plant's semantics — NOT a reproduction (documented in evidence).
  Note: `plant_urandom()` is dead code in the committed source; the certifier flagged
  the `_zag_rand` source token (R6a), not behavior.
- Battery scan (RV2b): dirty1_urandom is the ONLY module with unresolvable references.
  plant11 defines its own deterministic `_zag_rand` (name-ban test, compiles, FAIL/CONFIRMED).
  dirty2/3/5 and all r1 modules: 0 hits. Gap isolated to dirty1, as Tier-2 stated.
- Kill-bar check: no symbol claimed unknown builds fine → RV-BROKE does not fire on RV2.

## RV3 — 5-plant deterministic red team: COMPLETE

Battery: P1 empty module; P2 4MB-boundary/oversize module; P3 malformed/truncated
evidence + malformed manifest; P4 missing module/evidence/manifest (inconclusive-row
reasoning); P5 threshold off-by-ones (128/129 files+entries, 33MB binary cap).
Second instrument leg: same adversarial classes through rngscan_old/new
(empty→FAIL, clean→PASS, bad-evidence→FAIL). Every case 3× old + 3× new.

Result: **0 flips.** 13/14 thincert cases: old and new agree exactly (verdict +
byte-identical attestation digests). All 3 rngscan cases agree 3× byte-identical.
P4c (missing manifest): both exit 2, no attestation — agreement.

Headline adversarial finding (reported plainly, NOT buried): **P5a/P5b — the OLD
certifier crashes on large manifests.** `thincert_old` dies with
"zag runtime: invalid or double free" (no attestation) on manifests with ≥~70 entries
(bisected: PASS ≤64, crash ≥70; follows manifest count, not builddir count);
`thincert_new` handles 128 entries cleanly (PASS). White-box root cause: the old
binary's manifest tables use the exact ZNC-2026-09-21-007 trigger (three consecutive
same-size `as []i32` casts); a minimal probe on the pinned toolchain PROVES slots 0–2
of the 2nd/3rd casts alias the previous array's slots 65–67 (layout-dependent offset;
the 2026-09-21 probe saw 9–11). At ≤65 entries the aliased slots are uninitialized
heap — every historical verdict survived by allocator luck. Impact on the 0-flips
claim: NONE — largest historical manifest has 2 entries; no historical row changes
class. Classification: instrument-robustness divergence on a novel input, not a
verdict flip. The rebuilt instrument is strictly more robust than the historical one.

## Kill-bar disposition (final)

- RV1: (35, 0, 34, 0, 0, 1) re-derived — CONFIRM.
- RV2: gap documented at symbol level with failed-build evidence — CONFIRM.
- RV3: 0 flips across all 5 plants (+subcases) on both instruments — CONFIRM.
- **RV-CONFIRM.** The 0-flips / 34-confirmed / 1-inconclusive claim REPRODUCES;
  the dirty1 gap is VERIFIED AS DESCRIBED; the adversarial battery found no
  verdict flip but did find a real latent crash bug in the historical instrument
  (now fixed by the rebuild).

## Evidence (this commit)

- `reverify/evidence/rv2_symbol_gap.txt` — exact errors, shim analysis, battery scan
- `reverify/evidence/rv3_summary.tsv` — per-case old/new verdicts + digest prefixes
- `reverify/evidence/rv3_p5a_crash.txt` — crash bisect, probe proof, impact analysis
- `reverify/evidence/thincert_full_digests.txt` — 73 attestation SHA-256 (3× per case/leg)
- `reverify/evidence/rngscan_digests.txt` — 18 rngscan attestation SHA-256
- `reverify/evidence/gen_plants.py`, `run_rv3.py`, `bisect_crash.py`, `bisect2_crash.py`
  — battery generators/runner (Python glue; all decisions by pinned Zag binaries)
