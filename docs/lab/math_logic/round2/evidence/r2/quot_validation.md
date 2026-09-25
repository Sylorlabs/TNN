# QUOT engine validation (repair verification, 2026-09-25)

Engine (d) from the MATH R2 ideas round. Sources: `math_logic/round2/engines/quot/`
(14 files; `quot.zag` entry). Repair commit on tnn-native-lab:
`6574167232e22790af999a67f3b8cf78a4511526` ("Math R2 engine (d) QUOT: build
(repaired, on lab branch)").

## Source integrity

All 14 local files byte-match the repair commit's git blob SHAs
(verified via gh-api commit object vs local `git hash-object`):

| file | blob SHA |
|---|---|
| R33_NATIVE_IO_V1.zag | a6b440d256437de5e34faa77a0d73079e2755375 |
| cx_claim.zag | 1233ce542dadf15ccacd1a74c55eb019e654c6a0 |
| cx_io.zag | 7306ece44674cd4dce03110aac0c0ad2ddcbb2c7 |
| cx_match.zag | 93f5f0ac8047e53e4b19a3e122810dd5beeecc1d |
| cx_schemas.zag | 2cb5e950c8723cf6985f7d8d6e7fd68a06d48b16 |
| cx_store.zag | 3f1360f0ce990631ca8d5472192ac1c7f1c758d3 |
| cx_str.zag | 1e1fdf9908680779ca6ecd322113d597ef6bce98 |
| dlb_util.zag | 1675e82159f82ed0a3818ae3a7425fa08f815623 |
| q_bit.zag | 714aea847852f8a5a722587e8369a5a77ff9e074 |
| q_main.zag | 95302f5f7d8555ae19e719355a3bb6f2b259e9d4 |
| q_pool.zag | 48b9cf658b1621439147d435f77adce0301cd12e |
| q_rules.zag | 791baddd2940fb18c30f9240ddd1baa94bd532c1 |
| q_wl.zag | eb26173b1d28593531bc61fdfd6101b8ffb8d339 |
| quot.zag | fa6d9c01f630c0c592dfa1bc8291bf220c8b3d4d |

## Build

- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  `build quot.zag`, cwd = engines/quot (imports are bare filenames, resolve
  relative to cwd). Build clean (one benign zagd warning).
- Binary SHA-256 recorded in `results_formal_quot.json` (`binary_sha256`).

## Repair-crew validation reproduced

- Penguin specificity trace (premises need the `forall(x,...)` wrapper per
  store convention — bare `imp(...)` premises are not universal rules):
  - `penguin(tweety)` -> DERIVED (reason: committed)
  - `not(flies(tweety))` -> DERIVED (reason: committed)
  - `flies(tweety)` -> WITHHOLD (reason: absent)
  Matches the repair crew's expected trace exactly.
- B2 smoke: B2_01 -> DERIVED, rc=0.
- Sealed guard: binary exits 3 (via raw exit syscall) when the problem file
  path, the store file path, or the output path contains "sealed"
  (verified all three vectors).
- Zero-RNG grep over all 14 sources: no RNG/clock/urandom references
  (only comment-text false positives like "Herbrand universe (8 fields)").

## Battery protocol (same as the round-2 eval)

- Runner: `runners/run_quot.py` (replicates `run_battery.py`: 3 reruns per
  problem, byte-identical SHA check across r0/r1/r2, per-problem timeout
  600s, cwd `math_logic/` for STORE: resolution, sealed-solution scoring
  with the F-SEAL-01 B2_07 correction). Deviations from the eval runner,
  both hygienic and result-neutral:
  1. `verdict:`/`committed:` parsed lowercase (QUOT's output format).
  2. Process-group kill (`start_new_session` + `killpg` on timeout) so a
     timed-out engine leaves no orphaned processes to distort later wall
     times. Recorded outcome (TIMEOUT) is identical to the eval's.
- KB2 runner: `runners/run_kb2_quot.py`. QUOT emits no numeric CONFIDENCE;
  per SPEC_QUOT §4 ("confidence is non-zero iff DERIVED"), conf=1 iff
  verdict DERIVED else 0, and the same DUAL-bar (>=18/20) is applied.
- B1N / B7F: QUOT has no NL formalizer; on raw NL input it exits 4
  ("bad .form"). Recorded honestly as abstain (0/22 B1N; no B7F produced
  forms — the checker has nothing to score).

## B4X timeout note

On B4X (KB_B4X store with transitive `before/3` rules), QUOT exceeded the
600s per-run protocol timeout on every problem attempted in the first run
(B4X_01..B4X_05 recorded TIMEOUT; B4X_06 was in-flight when the run was
restarted for runner hygiene — see below). The engine is deterministic and
the store is shared, so all 15 problems were run through the same protocol
in the final run. TIMEOUT per problem — not solved, not incorrect.
This is a genuine engine property: the repair crew validated only the
penguin trace + B2 smoke; B4X-scale stores were never exercised.

Runner hygiene note: the first run used the eval's exact `subprocess.run`
timeout pattern, which kills only the shell wrapper and left orphaned
quot_bin processes. The run was restarted with a process-group-kill runner
(result-neutral: same 600s timeout, same TIMEOUT records). The B2R/B3R/B4R
tallies from the first run (12/12, 9/10, 15/15) were reproduced byte-identically
in the final run.
