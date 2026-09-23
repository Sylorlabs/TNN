# RNGSCAN v3 — Build Log

Date: 2026-09-20. Branch: `tnn-native-lab`. Dir: `docs/lab/wave12/step1a-v2/rngscan-v3/`.

## Frozen source/binary hashes (no-edit rule in effect from here)

| artifact | sha256 |
|---|---|
| `checker/rngscan_v3.zag` (source) | `8e9d20721674ce5779e49f305f49f4a1bb3b76dac1167b4d10f897c65aa87c6a` |
| `checker/rngscan_v3` (binary, znc `abed8aa1`) | `af0ebba954280b3af50aa79b9bc51b1c7331ecadc9369a3ba81e22776f08e055` |
| `modules/harness.zag` | `2adccaf4c8146f285be31071e11c9a4ccdf18d68d0b588e1cdbb7e5e71a01b3e` |
| `modules/clean2_pinned.zag` | `fa067893f1642f3ab676464f3e49b59c6b329ca50f22339f463ce5c4ba882082` |
| `runner/run_audit.sh` | `4da9878ccba0732d91afffa02d0d2684640982fd88dce4771b39a3970a64fc49` |
| `substrate/R33_NATIVE_IO_V1.zag` | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` (matches prereg §1) |
| `substrate/R33_NATIVE_SHA256_V2.zag` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` (matches prereg §1) |

**No-edit rule:** the checker source and binary above are frozen. Any further
change to either requires a new checker version, new hashes, and a dated
amendment; the blind round (below) runs against exactly these bytes.

Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Build warnings: A0101 (off-by-one, benign — fdepth sized 20001, nfl ≤ 20000),
A0102 (ignored return values, style). No errors.

## Implementation clarifications (prereg §7 refinements, no §3–§6 change)

- **C1 — PINNED marker on raw line.** Pass 0 and the attestation-hash pass
  detect the `PINNED` marker on the raw (comment-preserving) line while
  parsing `const NAME` from the code-only line, because the marker lives in
  a `//` comment. (Initial build checked the comment-stripped line and could
  never observe the marker; fixed before any round.)
- **C2 — family-token boundaries.** Prereg §7.4: `_` and `$` are BOUNDARY
  characters for 4.4 family tokens (so `entryset_insert` contains `insert`).
  Implemented via a dedicated `is_fambound` (alphanumeric-only) helper used
  by `contains_famtok` / `prefix_before_fam` for the insert/iter families and
  the 4.4 tripwire carve-out name match. (Initial build reused the
  identifier-char class where `_` is an identifier char, which let
  `entryset_insert`/`entryset_iterate` evade structural 4.4 — the exact v2
  plant10 miss. Fixed before any round; dirty5 now fails as required.)
  Within the family's evident intent the token sets were widened to
  insert{,ion}, put, add, push, emplace and
  iter{,ate,ator}, enumerate, foreach, emit, dump.
- **C3 — canonical-init body framing.** The body accumulator stripped the
  loop's closing `}` before the exact `B[I]=<e>;I=I+1;` match; without this
  the canonical form never recognized and clean modules false-failed.
- **C4 — vendored check.** Requires every vendored file *in the module's
  transitive import graph* to hash-match (`vfound>=1 && vmatch==vfound`),
  rather than requiring both substrate files regardless of use.
- **C5 — §4.8 import-graph allowlist enforced.** Transitive bare-`@import`
  targets must be a pinned substrate file, `harness.zag`, or the module
  itself; anything else is a 4.8 hit. (Was specified but unimplemented in the
  first build.)

## Dirty round (2026-09-20) — all 8 FAIL in the expected family

| fixture | verdict | hits | rule family | object scan |
|---|---|---|---|---|
| dirty1_urandom | FAIL | 4 | 4.1/4.6 (`/dev/urandom` literal; open/openat imm 2/257) | BANNED-FOUND |
| dirty2_clock | FAIL | 2 | 4.1/4.2 raw syscall + 4.6/4.2 (imm 228 recovered) | BANNED-FOUND |
| dirty3_uninit | FAIL | 1 | 4.3 (read-before-write) | clean |
| dirty4_eveninit | FAIL | 1 | 4.3 (conditional even-slot init, plant07 shape) | clean |
| dirty5_entryset | FAIL | 2 | 4.4 structural T1+T2 (plant10 shape) | clean |
| dirty6_mutablepin | FAIL | 5 | 4.4 tripwire `bucket` + structural T2 (plant11 shape) | clean |
| dirty7_clockintrinsic | FAIL | 4 | 4.2 `_zag_clock_*` token+intrinsic + 4.6/4.2 (imm 228 via 160B window) + REPLAY non-identical | BANNED-FOUND |
| dirty8_alias | FAIL | 1 | 4.3 (alias exfiltration) | clean |

dirty7 additionally confirms the §7.2 extended 160-byte recovery window:
the real `_zag_clock_monotonic_ms` intrinsic lowers to folded code and the
object scan still recovers syscall 228.

## Clean round (2026-09-20) — PASS

Module `clean2_pinned.zag` (pinned consts `SBOX_POLY`, `MIX_ROUNDS`,
strict canonical init everywhere, no banned constructs):
`hits=0 obj=clean vendored=ok replay_identical=yes varies_with_state=yes verdict=PASS`.
Evidence: `runs=8 exit_ok=1 layouts=4 byte_identical=1 varies_with_state=1
state_words=131072`. Eight outputs byte-identical across L0/L1/L2/L3;
alternate-state output differs. K1 clear (no replay divergence).

## Next: blind round

A separate red-team agent receives ONLY the frozen prereg
(`PREREG_NO_RNG_AUDIT_V3.md`) and the clean template
(`modules/clean2_pinned.zag` + `modules/harness.zag`) — never the checker
source. It authors/runs 20 fixed-order plants (§8, incl. reconstructed v2
plants 15–20). K2: any blind miss kills v3 with no partial credit.
