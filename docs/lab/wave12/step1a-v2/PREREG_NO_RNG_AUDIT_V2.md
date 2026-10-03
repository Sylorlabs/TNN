# PREREG — Step 1a v2: No-RNG auditor, native Zag rebuild (Track 1 gate)

Frozen: 2026-09-20. Owner: Micah. Auditor/builder: Muse (subagent, STEP 1a REBUILDER).
Parent: v1 prereg `~/workspace/tnn-lab/wave12/step1a-no-rng-audit/PREREG_NO_RNG_AUDIT.md`
(dead version RNGSCAN-2026-09-20-v1; K2 fired 19/20, plant20 `get_env_flag` missed —
a transcription gap: the frozen v1 rule 4.5 `env_` pattern was never implemented).
Amendment: `~/workspace/tnn-lab/wave12/step1a-no-rng-audit/AMENDMENT_2026-09-20_RNGSCAN_V2.md`.

**V2 rule deltas vs v1 — marked PENDING Micah's retroactive review** (build
proceeds under build-coordinator authority; nothing here is presented as approved):
- D1. BAN-2026-09-20-v2 = BAN v1 with rule 4.5 gaining the `env_` identifier-substring
  pattern (keeping the `lookup_table`/`pin_table` carve-outs). This is the exact gap
  that killed v1.
- D2. Transcription-gap closures of the same class: v1's frozen §4.1 banned `random`
  and frozen §4.5 banned `thread`, `spawn`, `go func`, `memcpy`, `eval`, and
  pointer-cast-to-int flows, and frozen §4.8 banned `eval`-like constructs — none of
  which the v1 implementation checked. The v2 implementation checks every frozen
  token (§4.7 mapping table). No frozen rule is added or removed; the implementation
  is brought up to the frozen list.
- D3. Checker reimplemented in native Zag (supersedes v1's "Zag or small C" slice).
  Pure Zag: checker, variation modules, harnesses. Python only for gh-api commit
  glue and log analysis (each use documented as an exception).
- D4. Object scan WITHOUT objdump (Zag cannot shell out): the checker parses the
  binary's bytes directly — scans for `0F 05` (syscall) with backward immediate
  recovery (`B8 imm32` / `48 C7 C0 imm32` within the 16 bytes before the opcode;
  znc is observed to move the immediate directly before `syscall`), flags immediates
  {318 getrandom, 228 clock_gettime, 96 gettimeofday} unconditionally and
  {257 openat, 2 open} only when the binary's bytes contain `/dev/urandom`;
  flags `0F 31` (rdtsc) and `0F C7` with ModRM /6 (rdrand) /7 (rdseed)
  unconditionally; raw byte-substring search for `/dev/urandom`, `/dev/random`,
  `getrandom`. Data-section false-positive risk is a known limitation, fail-closed
  (documented §11).
- D5. Replay WITHOUT fork/exec (Zag has no process spawn): the deterministic shell
  runner `runner/run_audit.sh` (build glue, same standing as phase-1 `run_*.sh`)
  runs the module binary twice with identical argv (state file, input file),
  byte-compares stdout, and runs a third time with a different state file that MUST
  differ (variation sanity). It writes the results to a replay-evidence file. The
  Zag checker performs the source scan + object scan, reads and validates the
  evidence file, and writes the attestation whose `replay` field carries the
  runner's evidence. The security property (run twice, compare bytes) needs no
  judgment and stays deterministic; this split is defined here so the attestation
  never implies the checker spawned processes.

## 1. Purpose
Before any Track 1 Arm C (state-dependent deterministic variation) trial counts, the
variation path must PROVE it contains no RNG. The proof is a NATIVE ZAG checker
(RNGSCAN-2026-09-20-v2) that (a) scans the variation-path source + transitive
callees for banned constructs, (b) scans the linked binary's bytes for banned
syscalls/opcodes, (c) incorporates byte-identical replay evidence produced by the
deterministic shell runner, and (d) emits a versioned JSON attestation. PASS or FAIL
attestations are committed as evidence.

## 2. Frozen versions
- Allowlist: `ALLOW-2026-09-20-v1` (verbatim from v1 prereg §3; reproduced in §3).
- Banned list: `BAN-2026-09-20-v2` (§4 below; = BAN v1 + `env_` in 4.5).
- Checker: `RNGSCAN-2026-09-20-v2` (native Zag program `checker/rngscan_v2.zag`).
- Runner: `RUNAUDIT-2026-09-20-v1` (`runner/run_audit.sh`; deterministic shell glue).
- Any change to §3–§6 requires a DATED amendment, flagged for retroactive review by Micah.
  The checker binary is frozen before the red-team round (§8); any checker change
  after that point is a new version and all prior rounds must be re-run.

## 3. Allowlist (ALLOW-2026-09-20-v1) — permitted on the variation path (unchanged)
1. Pure arithmetic/logic on i32/i64/u8 words and booleans; deterministic integer ops only.
2. Slice/array read/write with bounds checks; struct field access (aliased locals per the large-struct rule).
3. Named constants; fixed lookup tables declared in the module, content-pinned by sha256 in the attestation (marked `// PINNED`).
4. Control flow: if/else, for/while loops with deterministic bounds, match.
5. Calls into the read-only internal-state snapshot API (logged, replayable state words).
6. Deliberate deliberation primitives: gated choice where the gate's inputs are all state words and the gate is a pure function of its inputs.
7. Deterministic IO used ONLY to load the logged state and input and emit the output (file read/write via the vendored `R33_NATIVE_IO_V1` natives). IO on the variation path may not influence the computed output except through the logged input/state bytes.

## 4. Banned constructs (BAN-2026-09-20-v2) — each occurrence is a FAIL hit
Source-level (case-insensitive identifier/substring match, comments and string
literals EXCLUDED from identifier matching but string literals ARE scanned for
paths — see 4.6 and §7.3):
- 4.1 Entropy: `getrandom`, `urandom`, `random`, `rdseed`, `rdrand`,
  `_zag_raw_syscall` with a banned number (see 4.5), `/dev/random`.
- 4.2 Wall-clock: `clock_gettime`, `gettimeofday`, `rdtsc`, `rdpmc`, `time(`,
  `Date.now`, `performance.now`, `nio_deadline`, `nio_metric`, `nio_guard`
  (the io-native timing helpers are impure-of-inputs even when used for deadlines).
- 4.3 Uninitialized memory: any read of a `nio_alloc`'d slice before a full-length
  initialization loop writes every element on every reachable path (v2 dataflow:
  per-function, per-variable; see §7.3). Reads from freed slices.
- 4.4 Hash-iteration order: maps/dicts banned outright on the variation path.
  Banned identifier substrings: `hashmap`, `hash_map`, `unordered`, `dict`,
  `bucket`, `slotmap`, `htable`, `treemap`, `map_iter`, `dict_iter`.
  (Explicit carve-out: the pinned-table identifiers `lookup_table`, `LOOKUP_TABLE`,
  `pin_table` are allowlisted and do not match 4.4.)
- 4.5 Impure-of-inputs ops: file/IO reads outside the state/input load path,
  environment reads (`getenv`, `environ`, **`env_`** — v2 delta D1), pointer-address
  arithmetic (`_zag_slice_ptr`, `_zag_cstr_ptr`, casts of pointers `as i64`/`as u64`
  where the value flows into output), thread ops (`thread`, `spawn`, `pthread`,
  `go func`), `memcpy` from unlogged state, `eval`, inline assembly (`asm`, `__asm__`).
- 4.6 Syscall numbers (checked at the OBJECT level by direct byte scan, catching
  computed immediates the source scan cannot see): `getrandom`=318,
  `clock_gettime`=228, `gettimeofday`=96 — flagged unconditionally. `openat`=257 /
  `open`=2 flagged only when the binary's bytes contain `/dev/urandom` (legitimate
  state-file opens use openat and are allowed per §3.7).
- 4.7 Opcodes (object level): `rdtsc` (0F 31), `rdseed` (0F C7 /7), `rdrand`
  (0F C7 /6) — flagged unconditionally.
- 4.8 Dynamic dispatch: function pointers, `fn*` types, dynamic dispatch, and
  `eval`-like constructs are banned on the variation path outright — the
  transitive-callee boundary must be statically enumerable. Implemented tokens:
  `fn*`, `eval`.
- 4.9 `//`-commented `@import` directives are treated as absent (they are silently
  ignored by znc); only BARE `@import("path")` directives count for the
  transitive-source set.

## 5. Attestation schema (one JSON per audited build, committed)
```json
{
  "audit": "no-rng",
  "arm": "C",
  "allowlist_version": "ALLOW-2026-09-20-v1",
  "banned_version": "BAN-2026-09-20-v2",
  "checker_version": "RNGSCAN-2026-09-20-v2",
  "runner_version": "RUNAUDIT-2026-09-20-v1",
  "module_sha256": "<sha256 of variation.zag + transitive sources, concatenated in import order>",
  "lookup_table_sha256": ["<one per // PINNED table declaration>"],
  "variation_path_entry": "vary_expr",
  "callees": 14,
  "ops_checked": 2031,
  "banned_hits": 0,
  "banned_hit_detail": [],
  "object_byte_scan": "clean",
  "replay": {"runs": 2, "byte_identical": true, "varies_with_state": true, "state_words_logged": 4096},
  "verdict": "PASS"
}
```
- `verdict` is `PASS` iff `banned_hits == 0` AND `object_byte_scan == "clean"`
  AND `replay.byte_identical == true` AND the replay evidence file parsed cleanly.
  Otherwise `FAIL`. (`varies_with_state` is recorded, not verdict-gating: a
  constant-output function is deterministic; the flag exists so a silent
  constant is never mistaken for proven variation.)
- FAIL attestations are committed alongside PASS ones (a failed audit is evidence).
- `banned_hit_detail`: array of `{"rule": "4.1", "file": ..., "line": N, "text": "..."}`.

## 6. Kill bars (frozen; ANY firing kills audit version RNGSCAN-2026-09-20-v2)
- K1: An audit-PASS build produces non-byte-identical outputs from the same full
  logged state (replay disproves the claim). One occurrence kills the version.
- K2: Blind red-team (§8): checker misses a planted entropy source.
  Miss rate > 0 over 20 plants kills the version.
- K3: Any single banned-construct category (4.1–4.8) is found by post-hoc
  inspection on an audit-PASSING variation path. One find kills the version.
- A killed version invalidates all Arm C trials run under it; they do not count.
- v1 (RNGSCAN-2026-09-20-v1) stays DEAD. No trial ever ran under v1.

## 7. Checker v2 design (frozen)
7.1 Language: native Zag (`checker/rngscan_v2.zag`), compiled with the frozen znc
    toolchain. No RNG anywhere in the checker, modules, or harnesses. The checker
    is deterministic given its inputs. CLI:
    `rngscan_v2 <module.zag> <module-binary> <replay-evidence> <attestation.json>`
    Exit 0 on PASS, 1 on FAIL (attestation written either way), 2 on usage/IO error.
7.2 Vendored natives: `substrate/R33_NATIVE_SHA256_V2.zag` (sha256
    `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`) and
    `substrate/R33_NATIVE_IO_V1.zag` (sha256
    `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`) are audited
    ONCE at vendor time (hashes recorded here) and treated as trusted IO/crypto
    surface, NOT re-scanned as variation path. Module sources `@import` them by
    bare directive; the checker resolves imports relative to the module's directory
    and excludes any source whose path ends in either vendored filename from the
    scan set (they are still included in `module_sha256`).
7.3 Source scan (variation path = module + its own helper files, in import order):
    - Line-based. `//` comments stripped (string-literal-aware); an unterminated
      `/*` block opener is a FAIL hit (block comments unsupported on the variation
      path). Each line is split into code part and string literals: identifier
      rules (§4.7 mapping) run on the code part with literal contents blanked;
      the extracted literals are scanned for `/dev/urandom`, `/dev/random`,
      `getrandom` (rule 4.1/4.6).
    - `_zag_raw_syscall(<num>,...)` with a literal first argument equal to 318/228/96
      is a hit (4.1/4.2). Computed immediates are invisible here and are caught at
      the object level (§7.4) — verified on the dirty round (cf. v1 bring-up).
    - Uninitialized-read dataflow (rule 4.3), per function, per `nio_alloc`'d
      variable: state UNINIT at the `let NAME ... = nio_alloc(` line; a
      `while(...NAME.len...)` loop whose body writes `NAME[` and contains no
      `return` marks INIT once the scan passes the loop's end; `nio_free(NAME)`
      marks FREED; any `NAME[` occurrence that is not a write (`]` not followed
      by `=`) while state != INIT is a 4.3 hit (reported once per variable per
      function). Path-insensitive: a free or return on any textual path keeps the
      conservative state — KNOWN PRECISION LIMITATION, fail-closed (builder
      restructures, audit re-runs; carried over from v1 §11 / amendment D2 note).
    - Callee enumeration: `fn NAME(` definitions collected; reachability from
      `vary_expr` via textual `NAME(` call sites; `callees` = reachable count
      excluding `vary_expr`; missing `vary_expr` is a FAIL hit. `ops_checked` =
      non-blank, non-comment source lines across the variation-path set.
    - `module_sha256`: sha256 over the transitive sources concatenated in import
      order. `lookup_table_sha256`: for each raw-text line containing `PINNED`,
      sha256 of the enclosing `fn` body text (re-read from the raw file, since
      PINNED markers are comments).
    - The 4.5 pointer-cast check: a code line containing `as i64`/`as u64` together
      with `ptr`/`cstr` is a 4.5 hit (approximation of "pointer value flows into
      output"; fail-closed, documented).
7.4 Object scan (direct byte parse of the module binary; no objdump, no shell-out):
    - Raw byte-substring search for `/dev/urandom`, `/dev/random`, `getrandom` —
      any occurrence is a 4.1/4.6 hit.
    - For each `0F 05` (syscall) byte pair, recover the immediate moved into
      eax/rax by scanning the 16 bytes before the opcode for the LAST `B8 imm32`
      or `48 C7 C0 imm32` pattern fully inside the window. Flag immediates
      318/228/96 unconditionally; flag 257/2 only when the binary's bytes contain
      `/dev/urandom`. KNOWN LIMITATION: `0F 05` bytes occurring in data sections
      can false-positive — fail-closed (documented, §11).
    - `0F 31` (rdtsc) and `0F C7` with ModRM mod=3, reg=6 (rdrand) / reg=7 (rdseed)
      flagged unconditionally (rule 4.7).
    - `object_byte_scan` is `"clean"` iff no object-level hit fired.
7.5 Replay (split honestly between runner and checker):
    - `runner/run_audit.sh <checker-bin> <module.zag> <module-bin> <state> <input>
      <alt-state> <evidence> <attestation>`: runs the module binary twice with
      identical argv (state, input), captures stdout bytes, requires byte equality
      (`byte_identical`); runs a third time with `<alt-state>` and records whether
      output differs (`varies_with_state`); records `state_words_logged` =
      filesize(state)/8; writes the evidence file (deterministic key=value lines).
      A module-binary nonzero exit or a `timeout` trip fails the evidence
      (checker treats malformed/missing evidence as FAIL).
    - The Zag checker reads the evidence file, validates its shape, embeds its
      fields in the attestation's `replay` object, and gates the verdict on
      `byte_identical == true`. The checker never spawns processes.
7.6 §4.7 frozen-token → implementation mapping (the anti-transcription-gap table;
    every frozen token has a row; case-insensitive):
    4.1: getrandom→ident, urandom→ident, random→ident, rdseed→ident, rdrand→ident,
      /dev/random→ident+literal, _zag_raw_syscall literal 318→syscall-arg check,
      318/257/2→object scan.
    4.2: clock_gettime→ident, gettimeofday→ident, rdtsc→ident, rdpmc→ident,
      time(→ident, Date.now→ident, performance.now→ident, nio_deadline→ident,
      nio_metric→ident, nio_guard→ident, literal 228/96→syscall-arg check,
      228/96→object scan.
    4.3: uninit dataflow (§7.3); freed-slice reads.
    4.4: hashmap, hash_map, unordered, dict, bucket, slotmap, htable, treemap,
      map_iter, dict_iter→ident (carve-out: lines containing lookup_table/pin_table
      skip 4.4).
    4.5: _zag_slice_ptr→ident, _zag_cstr_ptr→ident, getenv→ident, environ→ident,
      env_→ident (v2 D1), pthread→ident, thread→ident, spawn→ident, go func→ident,
      memcpy→ident, eval→ident, __asm__→ident, asm(→ident, as-i64/u64-on-ptr→cast
      check, openat/open+urandom→object scan.
    4.6: 318/228/96 unconditional + 257/2-with-urandom→object scan; /dev/urandom,
      /dev/random, getrandom→raw byte search.
    4.7: 0F 31, 0F C7 /6, /7→object scan.
    4.8: fn*→ident, eval→ident.
    4.9: only bare @import("...") joins the transitive set.

## 8. Blind red-team protocol (20 plants)
8.1 After the checker binary is built and frozen (sha256 recorded), a plant list of
    20 entropy-source plants is generated by a SEPARATE red-team agent (per the v1
    report's recommendation) — covering all five banned categories (4.1 entropy,
    4.2 clock, 4.3 uninit, 4.4 hash-iteration, 4.5 ASLR/impure) with varied
    disguises, including at least: a computed syscall immediate, a runtime-built
    `/dev/urandom` path, a partial-init loop, an early-return-before-init-complete
    path, a renamed map, and an `env_`-family token (the v1 killer, must be caught
    by v2). No RNG in plant selection (standing law); plants are a fixed ordered
    list. The rebuilder does NOT write red-team plants.
8.2 Blinding control: the checker is a FIXED artifact — no per-plant tuning, no
    source edits between plants. Any checker change is a new checker version and
    §8 restarts from plant 1.
8.3 Each plant: compile with the frozen toolchain, run the frozen checker
    (source scan + object scan + replay evidence via the runner) → expect FAIL.
    A plant the checker does not flag (verdict PASS) is a MISS. Miss rate =
    misses / 20. Bar: miss rate must be 0 (K2).
8.4 Honesty note: builder and red-team are separate agents in this round; the
    rebuilder receives the 20 plants blind and runs the FROZEN checker over them
    unmodified.

## 9. Build order (frozen)
1. Capability spike in /tmp ONLY (ELF byte-scan, sha256 native, file IO) — done
   2026-09-20 before this prereg.
2. This prereg written, frozen, committed BEFORE any checker code exists.
3. Build the Zag checker; compile; record sha256 of source and binary.
4. Dirty round: 5 dirty Zag variation modules (one planted category each: urandom
   read, clock_gettime seed, uninitialized read, hash iteration, ASLR pointer
   leak) → expect 5 FAIL attestations, each naming the planted rule.
5. Clean round: clean `variation.zag` (output = f(input, full logged state);
   pinned table; deterministic) → PASS attestation + byte-identical replay +
   different-state-differs sanity.
6. Freeze the checker (record sha256; no source edits after — any edit = new
   version, restart at step 4).
7. Blind red-team round (§8) → scored report.
8. Commit everything: prereg, checker source, substrate, runner, modules, all
   attestations, red-team scoring report → `docs/lab/wave12/step1a-v2/`.

## 10. Standing laws carried in
Pure Zag for checker, modules, harnesses — zero exceptions. No RNG in build,
checker, or harnesses. No binaries, `.zagd.semantic-ready`, or `.zag-cache/`
committed. Byte-identical reruns; deterministic given inputs. Dated amendments
only — never silently bend a rule. Arm B (fenced RNG) is explicitly OUT of scope
for this gate. The v1 audit version stays DEAD; no trial ever ran under v1.

## 11. Known v2 limitations (not hidden)
- The 4.3 dataflow check is intra-procedural and pattern-shaped; exotic init idioms
  (cross-function init, init via helper call) false-positive — fail-closed:
  builder restructures, audit re-runs. Path-insensitivity (free/return on any
  textual path keeps the conservative state) is the same documented limitation.
- The 4.4 map ban is identifier-based; a from-scratch open-addressed table with
  innocent names would evade the identifier scan BUT its iteration order is still
  deterministic given inputs — the residual risk is iteration order depending on
  insertion history not present in declared inputs, which the state-snapshot API
  requirement (§3.5) is meant to close. K3 covers post-hoc finds.
- Object-scan backward recovery looks back 16 bytes; znc's lowering is observed
  to move the immediate directly before `syscall`. Data-section `0F 05` bytes can
  false-positive — fail-closed.
- The replay property is established by the shell runner, not the Zag checker;
  the checker validates and embeds the evidence. The split is defined in §7.5 so
  no attestation implies otherwise.
- Novel future entropy syscalls are out of scope for v2 (reviewed at each version
  bump).
- The 4.5 pointer-cast check (`as i64`/`as u64` on ptr/cstr lines) is an
  approximation; a cast laundered through an integer variable with an innocent
  name would evade the identifier form but the value still originates from a
  banned `_zag_slice_ptr`/`_zag_cstr_ptr` token, which is caught.

## 12. Retroactive-review items for Micah
- R1 (D1): rule 4.5 `env_` identifier-substring addition (the v1 killer fix).
- R2 (D2): transcription-gap closures — `random`, `thread`, `spawn`, `go func`,
  `memcpy`, `eval`, `fn*`, pointer-cast check now implemented per the already-frozen
  v1 list; no frozen rule added/removed.
- R3 (D3–D5): checker in native Zag; object scan by direct byte parse (no objdump);
  replay split between shell runner (evidence) and Zag checker (scan+attest).
