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
