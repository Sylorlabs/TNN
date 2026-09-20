# Slice 09 — No-RNG audit procedure (the gate Arm C must pass before any trial counts)

## 1. Slice
Design the audit procedure that PROVES the Track 1 variation function contains no RNG: a source-code allowlist for the variation path, a checker that scans it for banned constructs, and the attestation format it emits. Arm C (deterministic state variation) trials are invalid unless this audit passes.

## 2. Falsifiable claim
A static checker scanning only the variation-path source and its transitive Zag callees will flag every entropy source — OS entropy reads, wall-clock reads, uninitialized memory, hash-map iteration order, any op whose output is not a pure function of its declared inputs — so that any build passing this audit is provably incapable of emitting RNG-influenced variation. The claim dies the day one of these happens: an audit-passing build varies across byte-identical replays, or a planted entropy source (in a blind red-team test) escapes the checker.

## 3. Design
The variation path is a named, prereg-enumerated call graph: the top-level `vary_expr(input, state)` function and its transitive callees, compiled from a dedicated Zag module (`variation.zag`) that may import only from the allowlist below. The audit has two halves: static scan + replay proof.

**Allowlist (permitted Zag ops on the variation path):**
- Pure arithmetic/logic on i32/i64/u8 words and booleans; deterministic integer ops only.
- Slice/array read/write with bounds checks; struct field access (aliased locals per the AGENTS.md large-struct rule).
- Named constants, fixed lookup tables (declared in the module, content-pinned by sha256 in the attestation).
- Control flow (if/else, for-loops with deterministic bounds, match).
- Calls into the read-only internal-state snapshot API (logged, replayable state words).
- Deliberate deliberation primitives (gated choice where the gate's inputs are all state words; the gate must be a pure function of its inputs).

**Banned constructs (checker flags each occurrence):**
- Entropy sources: any syscall/syscall-lowering reading `/dev/urandom`, `getrandom`, `rdseed`/`rdrand`, or Zag native stubs wrapping them. Explicitly: znc emitted no `getrandom`/`rdseed` in the linked variation object — check the object disassembly, not just the source.
- Wall-clock reads: `clock_gettime`, `gettimeofday`, rdtsc, `Date.now` equivalents — any time input is an entropy source, even if seeded into a deterministic PRNG, because the seed itself is state-external.
- Uninitialized memory: `nio_alloc` without full initialization before first read on every reachable path (dataflow check); reads from freed or out-of-slice regions.
- Hash-iteration order: any map/dict iteration on the variation path where the emitted output depends on visit order. Maps are banned outright on the variation path unless the checker proves full iteration before emission; default = ban.
- Impure-of-inputs ops: anything whose output is not a pure function of its declared inputs — file/IO reads, environment variable reads, pointer-address arithmetic (ASLR leaks), thread scheduling order, `memcpy` from unlogged state.

**The checker:** a native tool (Zag or small C, committed to the repo) that (a) parses `variation.zag` + transitive callees, (b) verifies every emitted op is in the allowlist, (c) scans the linked object for banned syscall numbers/imm values (defense in depth against stub smuggling), (d) emits the attestation below, and (e) runs the byte-identical replay check: full logged state + input → run twice, diff — must be identical.

**Attestation format** (one JSON file per audited build, committed with the trial results):
```json
{
  "audit": "no-rng",
  "arm": "C",
  "allowlist_version": "ALLOW-2026-09-20-v1",
  "checker_version": "RNGSCAN-2026-09-20-v1",
  "module_sha256": "<sha256 of variation.zag + transitive sources>",
  "lookup_table_sha256": ["<one per pinned table>"],
  "variation_path_entry": "vary_expr",
  "callees": 14,
  "ops_checked": 2031,
  "banned_hits": 0,
  "objdump_syscall_scan": "clean",
  "replay": {"runs": 2, "byte_identical": true, "state_words_logged": 4096},
  "verdict": "PASS"
}
```
`verdict: FAIL` entries are also committed (a failed audit is evidence, not something to hide).

## 4. Kill bar
This audit procedure is killed if ANY of the following fires:
- A build passing the audit produces non-byte-identical outputs from the same full logged state (replay disproves the "proven no-RNG" claim) — one occurrence kills the audit version.
- In the blind red-team test (a builder plants one entropy source per round, auditor does not know which), the checker misses a planted source — miss rate > 0 over 20 plants kills it.
- Any single banned construct category is found on an audited-passing variation path by post-hoc inspection — one find kills the audit version.
Arm C trials run under a killed audit version are declared invalid and do not count.

## 5. Honesty notes
- This audit proves *no entropy source on the variation path* — it does not prove the variation is *good* (expressive, adaptive, worth keeping). A build can pass with a constant-output variation function; quality is a separate trial question.
- The weak point is the transitive-callee boundary: the checker must know exactly which functions are on the variation path. If a builder can reach an un-audited function via a function pointer or dynamic dispatch, the audit is hollow. v1 handles this by banning function pointers and dynamic dispatch on the variation path outright; that is the rule I am least sure is complete.
- `objdump`-level syscall scanning only catches known banned syscalls — a novel entropy syscall introduced by a future kernel is a gap. The audit reviews syscall lists against the running kernel at each version bump.
- Not claiming: coverage of Arm B (the fenced RNG arm, which is *supposed* to contain seeded RNG — the checker must be run in per-arm mode and never gate Arm B on a no-RNG rule), nor of canonical production paths (covered by the standing no-RNG law, not this slice).

## 6. Next build step
Build the checker v1 against a deliberately dirty `variation.zag`: plant one of each banned category (urandom read, clock_gettime seed, uninitialized read, hash iteration, ASLR pointer leak), confirm all five are flagged and produce five FAIL attestations, then confirm a clean build passes with byte-identical replay. The blind red-team round (20 plants, auditor unaware) is the second step and the one that actually tests the claim.
