# PREREG — Step 1a: No-RNG auditor + versioned attestation (Track 1 gate)

Frozen: 2026-09-20. Owner: Micah. Auditor/builder: Muse (subagent).
Parent spec: `~/workspace/tnn-lab/wave11/t1-state-variation/findings/09-no-rng-audit.md`.

## 1. Purpose
Before any Track 1 Arm C (state-dependent deterministic variation) trial counts, the
variation path must PROVE it contains no RNG. The proof is a checker (v1) that
(a) scans the variation-path source + transitive callees for banned constructs,
(b) scans the linked object for banned syscalls/opcodes, (c) runs a byte-identical
replay, and (d) emits a versioned JSON attestation. PASS or FAIL attestations are
committed as evidence.

## 2. Frozen versions
- Allowlist: `ALLOW-2026-09-20-v1` (verbatim from spec §3; reproduced in §3 below).
- Banned list: `BAN-2026-09-20-v1` (§4 below).
- Checker: `RNGSCAN-2026-09-20-v1` (small C program; the spec's slice permits "Zag or small C").
- Any change to §3–§6 requires a DATED amendment, flagged for retroactive review by Micah.
  The checker binary is frozen before the red-team round (§8); any checker change
  after that point is a new version and all prior rounds must be re-run.

## 3. Allowlist (ALLOW-2026-09-20-v1) — permitted on the variation path
1. Pure arithmetic/logic on i32/i64/u8 words and booleans; deterministic integer ops only.
2. Slice/array read/write with bounds checks; struct field access (aliased locals per the large-struct rule).
3. Named constants; fixed lookup tables declared in the module, content-pinned by sha256 in the attestation (marked `// PINNED`).
4. Control flow: if/else, for/while loops with deterministic bounds, match.
5. Calls into the read-only internal-state snapshot API (logged, replayable state words).
6. Deliberate deliberation primitives: gated choice where the gate's inputs are all state words and the gate is a pure function of its inputs.
7. Deterministic IO used ONLY to load the logged state and input and emit the output (file read/write via the vendored `R33_NATIVE_IO_V1` natives). IO on the variation path may not influence the computed output except through the logged input/state bytes.

## 4. Banned constructs (BAN-2026-09-20-v1) — each occurrence is a FAIL hit
Source-level (case-insensitive identifier/substring match, comments and string
literals EXCLUDED from identifier matching but string literals ARE scanned for
paths — see 4.6):
- 4.1 Entropy: `getrandom`, `urandom`, `rdseed`, `rdrand`, `_zag_raw_syscall` with a
  banned number (see 4.5), `random`, `/dev/random`.
- 4.2 Wall-clock: `clock_gettime`, `gettimeofday`, `rdtsc`, `rdpmc`, `time(`,
  `Date.now`, `performance.now`, `nio_deadline`, `nio_metric`, `nio_guard`
  (the io-native timing helpers are impure-of-inputs even when used for deadlines).
- 4.3 Uninitialized memory: any read of a `nio_alloc`'d slice before a full-length
  initialization loop writes every element on every reachable path (v1 dataflow:
  per-function, per-variable; see §7.3). Reads from freed slices.
- 4.4 Hash-iteration order: maps/dicts banned outright on the variation path.
  Banned identifier substrings: `hashmap`, `hash_map`, `unordered`, `dict`,
  `bucket`, `slotmap`, `htable`, `treemap`, `map_iter`, `dict_iter`.
  (Explicit carve-out: the pinned-table identifiers `lookup_table`, `LOOKUP_TABLE`,
  `pin_table` are allowlisted and do not match 4.4.)
- 4.5 Impure-of-inputs ops: file/IO reads outside the state/input load path,
  environment reads (`getenv`, `environ`, `env_`), pointer-address arithmetic
  (`_zag_slice_ptr`, `_zag_cstr_ptr`, casts of pointers `as i64`/`as u64` where
  the value flows into output), thread ops (`thread`, `spawn`, `pthread`,
  `go func`), `memcpy` from unlogged state, inline assembly (`asm`, `__asm__`).
- 4.6 Syscall numbers (checked at the OBJECT level via objdump, catching computed
  immediates the source scan cannot see): `getrandom`=318, `clock_gettime`=228,
  `gettimeofday`=96 — flagged unconditionally. `openat`=257 / `open`=2 flagged
  only when the binary's rodata contains `/dev/urandom` (legitimate state-file
  opens use openat and are allowed per §3.7).
- 4.7 Opcodes (object level): `rdtsc` (0F 31), `rdseed` (0F C7 /8), `rdrand`
  (0F C7 /6) — flagged unconditionally.
- 4.8 Dynamic dispatch: function pointers, `fn*` types, dynamic dispatch, and
  `eval`-like constructs are banned on the variation path outright — the
  transitive-callee boundary must be statically enumerable (spec §5 honesty note).
- 4.9 `//`-commented `@import` directives are treated as absent (they are silently
  ignored by znc); only BARE `@import("path")` directives count for the
  transitive-source set.

## 5. Attestation schema (one JSON per audited build, committed)
```json
{
  "audit": "no-rng",
  "arm": "C",
  "allowlist_version": "ALLOW-2026-09-20-v1",
  "banned_version": "BAN-2026-09-20-v1",
  "checker_version": "RNGSCAN-2026-09-20-v1",
  "module_sha256": "<sha256 of variation.zag + transitive sources, concatenated in import order>",
  "lookup_table_sha256": ["<one per // PINNED table declaration>"],
  "variation_path_entry": "vary_expr",
  "callees": 14,
  "ops_checked": 2031,
  "banned_hits": 0,
  "banned_hit_detail": [],
  "objdump_syscall_scan": "clean",
  "replay": {"runs": 2, "byte_identical": true, "state_words_logged": 4096},
  "verdict": "PASS"
}
```
- `verdict` is `PASS` iff `banned_hits == 0` AND `objdump_syscall_scan == "clean"`
  AND `replay.byte_identical == true`. Otherwise `FAIL`.
- FAIL attestations are committed alongside PASS ones (a failed audit is evidence).
- `banned_hit_detail`: array of `{"rule": "4.1", "file": ..., "line": N, "text": "..."}`.

## 6. Kill bars (frozen; ANY firing kills audit version RNGSCAN-2026-09-20-v1)
- K1: An audit-PASS build produces non-byte-identical outputs from the same full
  logged state (replay disproves the claim). One occurrence kills the version.
- K2: Blind red-team (§8): checker misses a planted entropy source.
  Miss rate > 0 over 20 plants kills the version.
- K3: Any single banned-construct category (4.1–4.8) is found by post-hoc
  inspection on an audit-PASSING variation path. One find kills the version.
- A killed version invalidates all Arm C trials run under it; they do not count.

## 7. Checker v1 design (frozen)
7.1 Language: C (allowed by spec slice: "Zag or small C"). No RNG anywhere in the
    checker or harnesses. The checker is deterministic given its inputs.
7.2 Inputs: path to `variation.zag`, path to compiled binary, state file, input file.
7.3 Source scan: line-based. Strips `//` comments (an unterminated `/*` block is a
    FAIL — v1 does not support block comments on the variation path). Bare
    `@import("...")` directives define the transitive source set (relative to the
    module dir; vendored natives `R33_NATIVE_SHA256_V2.zag` and
    `R33_NATIVE_IO_V1.zag` are audited ONCE at vendor time — their hashes are
    recorded — and then treated as trusted IO/crypto surface, NOT re-scanned as
    variation path; the variation path is `variation.zag` + its own helper files).
    Uninitialized-read dataflow (rule 4.3): per function, per `nio_alloc`'d
    variable: state UNINIT at alloc; a `while(i<NAME.len){ NAME[i]=...; i=i+1; }`
    full-range write loop marks INIT; any `NAME[` read while UNINIT is a hit;
    any read after `nio_free(NAME)` is a hit. Paths through early `return` inside
    the init loop before completion keep UNINIT.
7.4 Object scan: `objdump -d` the binary; for each `syscall` instruction, recover
    the immediate moved into rax/eax in the preceding 12 instructions; flag 4.6
    numbers. Flag `rdtsc`/`rdseed`/`rdrand` mnemonics anywhere. Scan raw binary
    bytes for the substrings `/dev/urandom`, `/dev/random`, `getrandom`.
7.5 Replay: run the binary twice with identical argv (state file, input file);
    capture stdout bytes; PASS requires byte equality. A third run with a
    DIFFERENT state file must produce different output (variation sanity: the
    audit does not bless constant-output functions silently — recorded in the
    report, not the attestation).
7.6 Callee enumeration: collect `fn NAME(` definitions in the module + helper
    files; reachability from `vary_expr` via textual call sites `NAME(`;
    `callees` = reachable count excluding `vary_expr`. `ops_checked` = non-blank,
    non-comment source lines across the transitive variation-path set.
7.7 `module_sha256`: `sha256sum` over the transitive sources concatenated in
    import order. `lookup_table_sha256`: sha256 of each `// PINNED` const-table
    declaration's text.

## 8. Blind red-team protocol (20 plants)
8.1 After the checker binary is built and frozen (sha256 recorded), a plant list
    of 20 entropy-source plants is generated — covering all five banned
    categories (4.1 entropy, 4.2 clock, 4.3 uninit, 4.4 hash-iteration, 4.5 ASLR/
    impure) with varied disguises, including at least: a computed syscall
    immediate (`200+28` instead of literal `228`), a runtime-built `/dev/urandom`
    path, a partial-init loop, an early-return-before-init-complete path, and a
    renamed map (`slotmap`/`BUCKETS`). No RNG is used in plant selection (standing
    law); plants are a fixed ordered list.
8.2 Blinding control: the checker is a FIXED artifact — no per-plant tuning,
    no source edits between plants. If any checker change is required, that is a
    new checker version and §8 restarts from plant 1.
8.3 Each plant: checker runs → expect verdict FAIL. A plant the checker does not
    flag (verdict PASS) is a MISS. Miss rate = misses / 20. Bar: miss rate must
    be 0 (K2).
8.4 Honesty note: builder and auditor are the same agent in this round; the
    blinding is structural (fixed checker, fixed plant list, no per-plant edits),
    not interpersonal. A future round with a separate red-team agent is
    recommended and recorded as follow-up.

## 9. Build order (frozen)
1. Prereg frozen and committed (this file) BEFORE any checker/module code.
2. Build checker v1; compile; record its sha256.
3. Dirty round: 5 dirty `variation.zag` modules (one planted category each:
   urandom read, clock_gettime seed, uninitialized read, hash iteration,
   ASLR pointer leak) → expect 5 FAIL attestations, each naming the planted rule.
4. Clean round: clean module → compile → byte-identical replay → PASS attestation.
5. Red-team round (§8) → report.
6. Commit: prereg + checker source + modules + all attestations + red-team report.

## 10. Standing laws carried in
Pure-Zag-or-small-C only. No RNG in build, checker, or harnesses. No binaries,
`.zagd.semantic-ready`, or `.zag-cache/` committed. Dated amendments only —
never silently bend a rule. Arm B (fenced RNG) is explicitly OUT of scope for
this gate.

## 11. Known v1 limitations (not hidden)
- The 4.3 dataflow check is intra-procedural and pattern-shaped; exotic init
  idioms may false-positive (fail-closed: builder restructures, audit re-runs).
- The 4.4 map ban is identifier-based; a from-scratch open-addressed table with
  innocent names would evade the identifier scan BUT its iteration order is still
  deterministic given inputs (pure function of inputs) — the residual risk is
  iteration order depending on insertion history not present in declared inputs,
  which the state-snapshot API requirement (§3.5) is meant to close. Flagged as
  the weakest rule; K3 covers post-hoc finds.
- objdump syscall-number recovery looks back 12 instructions; znc's lowering is
  observed to move the immediate directly before `syscall` (verified on the
  dirty builds in the build log).
- Novel future entropy syscalls are out of scope for v1 (reviewed at each version bump).
