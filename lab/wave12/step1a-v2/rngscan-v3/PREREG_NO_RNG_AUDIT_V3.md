# PREREG — Step 1a v3: No-RNG auditor, general static rebuild (parallel, NON-GATING)

Frozen: 2026-09-20. Owner: Micah. Builder: Muse (subagent, RNGSCAN-V3 BUILD LEAD).
Parent: v2 prereg `../PREREG_NO_RNG_AUDIT_V2.md`
(dead version RNGSCAN-2026-09-20-v2; K2 fired — 3 misses among 14 scored plants:
plant07 even-slots-only init, plant10 from-scratch `EntrySet`, plant11 mutable
`pin_table` riding the carve-out; plants 15–20 unscored).
Amendment: `../AMENDMENT_2026-09-20_RNGSCAN_V3.md` (DRAFT, commit `64cd373`).

**Standing:** v3 is a PARALLEL, NON-GATING line per Micah's 2026-09-20 decision.
It does not gate the Arm C trial. The Arm C gate is hardened replay + the thin
per-build certifier + the signed residual-risk statement. v1 and v2 stay DEAD
regardless of this version's outcome.

**V3 rule deltas vs v2** (all seven amendment fixes incorporated):
- D1. Rule 4.3 replaced by the STRICT CANONICAL INIT FORM (fail-closed, §7.3).
  INIT is granted only for the exact textual form
  `let I:i32=0;` immediately before `while(I<B.len){ B[I]=<expr>; I=I+1; }`
  with no conditionals, no non-counter index, no early exit, no self-read on
  the right-hand side. Anything else leaves the buffer UNINIT; any use while
  UNINIT is a 4.3 hit. This closes the plant07 class statically.
- D2. Rule 4.4 is STRUCTURAL, not token-based (§7.4): any struct/type — or any
  insert-family/iterate-family function pair sharing a name prefix — with both
  insertion and iteration is a 4.4 hit. The v2 identifier token list is retained
  as a first-pass tripwire only. This closes the plant10 class.
- D3. Carve-out NARROWED (§4.4): `lookup_table`/`pin_table` identifiers are
  exempt from the 4.4 token tripwire ONLY when the name is declared
  `const NAME:type=value; // PINNED` and the declaration is hashed into the
  attestation. A mutable map gets no carve-out regardless of its name. This
  closes the plant11 class.
- D4. Object scan: REGISTER-TAINT recovery per the amendment, implemented as
  EXTENDED IMMEDIATE RECOVERY (§7.5) — see the spike note below for why the
  letter of the amendment's pattern was superseded by observed znc lowering.
- D5. Rule 4.2 gains the explicit `_zag_clock_*` ban plus a ONE-TIME INTRINSIC
  SURFACE AUDIT: every `_zag_*` identifier on the variation path must be on
  the frozen allowlist (§4.2) or it is a 4.2 hit. ANY `_zag_raw_syscall(`
  occurrence in scanned module source is a 4.1/4.2 hit (prescriptive: modules
  must use the vendored natives for IO; raw syscalls do not audit).
- D6. Replay HARDENED (§7.6): N=8 byte-compared runs with documented argv/env
  layout variation, plus one alt-state run. Heap pre-dirtying as specified in
  the amendment was SPIKED and found INEFFECTIVE on znc's allocator (evidence
  §11); the zeroed-page uninit-hiding class is closed by D1 instead.
- D7. FRESH BLIND ROUND (§8): 20 plants — v2's unscored plants 15–20
  (reconstructed from the v2 red-team report) plus new plants covering the
  fixed gaps. Same K2 bar (miss rate 0 over 20), same blinding discipline
  (separate agent, frozen prereg + clean template only, never the
  implementation source).

**Spike evidence (capability spikes in /tmp, 2026-09-20, NOT committed):**
- S1 (heap reuse): `nio_alloc` returns zeroed pages UNCONDITIONALLY — tested at
  1 KiB and 1 MiB, with fill→free→realloc and with a live garbage buffer
  resident. Fresh mmap semantics in all cases. Consequence: heap pre-dirtying
  (allocate-and-fill garbage before the trial runs) cannot dirty pages the
  trial will allocate — the amendment's replay-hardening mechanism is
  ineffective as specified. The zeroed-page hiding class (v2 W2) is closed by
  D1's static canonical-init rule instead. This deviation from the amendment's
  letter is recorded here with evidence; the intent (defeat zeroed-page hiding
  of uninit reads) is satisfied.
- S2 (znc syscall lowering): for `_zag_raw_syscall(<folded-const>,...)`, znc
  emits `48 C7 C0 imm32` (`mov rax,imm32`) FIRST, then ~100 bytes of argument
  shuffling (including a value-preserving canonicalization dance and a
  push-rax/pop-rax pair), then `0F 05`. Observed span: 108 bytes for the
  6-argument form. The amendment's hypothesized `mov reg,imm32` …
  `mov eax/rax,reg` pattern was NOT observed in znc output (60+ syscall sites
  examined). v3 therefore implements extended immediate recovery (160-byte
  backward window for the last `48 C7 C0 imm32` / `B8 imm32`, rejecting spans
  containing the `31 C0` / `29 C0` zeroing idioms) instead of the hypothesized
  register pattern. Native-call lowering keeps the number within ~48 bytes;
  the v2 16-byte window is retained as the direct path.

## 1. Purpose
Before any Track 1 Arm C (state-dependent deterministic variation) trial counts,
the variation path must PROVE it contains no RNG. The proof is a NATIVE ZAG
checker (RNGSCAN-2026-09-20-v3) that (a) scans the variation-path source +
transitive callees for banned constructs, (b) scans the linked binary's bytes
for banned syscalls/opcodes, (c) verifies the vendored trusted surface hashes,
(d) incorporates byte-identical replay evidence produced by the deterministic
shell runner, and (e) emits a versioned JSON attestation. PASS or FAIL
attestations are committed as evidence.

## 2. Frozen versions
- Allowlist: `ALLOW-2026-09-20-v1` (verbatim from v1/v2 prereg §3; reproduced
  in §3).
- Banned list: `BAN-2026-09-20-v3` (§4 below).
- Intrinsic allowlist: `INTRINSIC-ALLOW-2026-09-20-v3` (§4.2).
- Checker: `RNGSCAN-2026-09-20-v3` (native Zag program
  `rngscan-v3/checker/rngscan_v3.zag`).
- Runner: `RUNAUDIT-2026-09-20-v2` (`rngscan-v3/runner/run_audit.sh`;
  deterministic shell glue).
- Any change to §3–§6 requires a DATED amendment with Micah's re-approval.
  The checker binary is frozen before the red-team round (§8); any checker
  change after that point is a new version and all prior rounds must be re-run.

## 3. Allowlist (ALLOW-2026-09-20-v1) — permitted on the variation path (unchanged)
1. Pure arithmetic/logic on i32/i64/u8 words and booleans; deterministic integer ops only.
2. Slice/array read/write with bounds checks; struct field access (aliased locals per the large-struct rule).
3. Named constants; fixed lookup tables declared `const` in the module, marked
   `// PINNED`, content-pinned by sha256 in the attestation.
4. Control flow: if/else, for/while loops with deterministic bounds, match.
5. Calls into the read-only internal-state snapshot API (logged, replayable state words).
6. Deliberate deliberation primitives: gated choice where the gate's inputs are all state words and the gate is a pure function of its inputs.
7. Deterministic IO used ONLY to load the logged state and input and emit the output (file read/write via the vendored `R33_NATIVE_IO_V1` natives). IO on the variation path may not influence the computed output except through the logged input/state bytes.

## 4. Banned constructs (BAN-2026-09-20-v3) — each occurrence is a FAIL hit
Source-level (case-insensitive identifier/substring match, comments and string
literals EXCLUDED from identifier matching but string literals ARE scanned for
paths — see 4.6 and §7.3):
- 4.1 Entropy: `getrandom`, `urandom`, `random`, `rdseed`, `rdrand`,
  `_zag_raw_syscall` (ANY occurrence in scanned module source — prescriptive),
  `/dev/random`.
- 4.2 Wall-clock and intrinsics: `clock_gettime`, `gettimeofday`, `rdtsc`,
  `rdpmc`, `time(`, `Date.now`, `performance.now`, `nio_deadline`, `nio_metric`,
  `nio_guard`, **`_zag_clock_`** (any identifier containing this substring),
  and any `_zag_<name>` identifier NOT on INTRINSIC-ALLOW-2026-09-20-v3
  (one-time surface audit; the allowlist is frozen below).
- 4.3 Uninitialized memory: any USE of a `nio_alloc`'d slice (or its aliases,
  §7.3) while not INIT under the strict canonical init form (§7.3), and any
  use after `nio_free`. Reads from freed slices.
- 4.4 Hash-iteration order: STRUCTURAL (§7.4) — any struct/type with
  insert-family + iterate-family functions (type-associated or
  prefix-associated) is a hit. Token tripwire (identifier substrings):
  `hashmap`, `hash_map`, `unordered`, `dict`, `bucket`, `slotmap`, `htable`,
  `treemap`, `map_iter`, `dict_iter`. NARROWED carve-out: the tripwire is
  skipped for a line ONLY if the line contains an identifier declared
  `const NAME:type=value; // PINNED` (const declaration with the PINNED
  marker, hashed into the attestation per §5). A mutable map named
  `lookup_table`/`pin_table`/anything else gets NO carve-out.
- 4.5 Impure-of-inputs ops: file/IO reads outside the state/input load path,
  environment reads (`getenv`, `environ`, `env_`), pointer-address arithmetic
  (`_zag_slice_ptr`, `_zag_cstr_ptr`, casts of pointers `as i64`/`as u64`
  where the value flows into output), thread ops (`thread`, `spawn`,
  `pthread`, `go func`), `memcpy` from unlogged state, `eval`, inline
  assembly (`asm`, `__asm__`).
- 4.6 Syscall numbers (OBJECT level, §7.5): `getrandom`=318,
  `clock_gettime`=228, `gettimeofday`=96 — flagged unconditionally.
  `openat`=257 / `open`=2 flagged only when the binary's bytes contain
  `/dev/urandom` (legitimate state-file opens use openat and are allowed
  per §3.7).
- 4.7 Opcodes (object level): `rdtsc` (0F 31), `rdseed` (0F C7 /7), `rdrand`
  (0F C7 /6) — flagged unconditionally.
- 4.8 Dynamic dispatch: function pointers, `fn*` types, dynamic dispatch, and
  `eval`-like constructs are banned on the variation path outright — the
  transitive-callee boundary must be statically enumerable. Implemented
  tokens: `fn*`, `eval` (whole-word).
- 4.9 `//`-commented `@import` directives are treated as absent (they are
  silently ignored by znc); only BARE `@import("path")` directives count for
  the transitive-source set.

**INTRINSIC-ALLOW-2026-09-20-v3** (frozen; every other `_zag_*` on the
variation path is a 4.2 hit):
`_zag_arg`, `_zag_print`, `_zag_println`, `_zag_strcmp`, `_zag_i64_to_str`,
`_zag_malloc`, `_zag_free`.
Special-cased (not on the allowlist, handled by their own rules):
`_zag_raw_syscall` → 4.1/4.2 hit on ANY occurrence;
`_zag_slice_ptr`, `_zag_cstr_ptr` → 4.5 hit (checked before the allowlist);
any identifier containing `_zag_clock_` → 4.2 hit (checked before the
allowlist).

## 5. Attestation schema (one JSON per audited build, committed)
```json
{
  "audit": "no-rng",
  "arm": "C",
  "allowlist_version": "ALLOW-2026-09-20-v1",
  "banned_version": "BAN-2026-09-20-v3",
  "intrinsic_allowlist_version": "INTRINSIC-ALLOW-2026-09-20-v3",
  "checker_version": "RNGSCAN-2026-09-20-v3",
  "runner_version": "RUNAUDIT-2026-09-20-v2",
  "module_sha256": "<sha256 of variation.zag + transitive sources, concatenated in import order>",
  "vendored_sha256": {
    "R33_NATIVE_SHA256_V2.zag": "9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf",
    "R33_NATIVE_IO_V1.zag": "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8"
  },
  "vendored_ok": true,
  "lookup_table_sha256": ["<one per const // PINNED table declaration>"],
  "variation_path_entry": "vary_expr",
  "callees": 14,
  "ops_checked": 2031,
  "banned_hits": 0,
  "banned_hit_detail": [],
  "object_byte_scan": "clean",
  "replay": {"runs": 8, "byte_identical": true, "varies_with_state": true,
             "state_words_logged": 4096, "layout_variants": 4},
  "verdict": "PASS"
}
```
- `verdict` is `PASS` iff `banned_hits == 0` AND `vendored_ok == true` AND
  `object_byte_scan == "clean"` AND `replay.byte_identical == true` AND
  `replay.runs == 8` AND the replay evidence file parsed cleanly. Otherwise
  `FAIL`. (`varies_with_state` is recorded, not verdict-gating.)
- FAIL attestations are committed alongside PASS ones.
- `banned_hit_detail`: array of `{"rule": "4.1", "file": ..., "line": N,
  "text": "..."}`. Rule codes: `4.1`…`4.9`, `ENTRY`, `SRC`, `OBJ`, `REPLAY`,
  `VENDOR`.
- `lookup_table_sha256`: for each `const NAME…// PINNED` declaration, sha256
  of the enclosing `fn` body text (or the declaration line if top-level).
  A `// PINNED` marker on a NON-const declaration grants nothing: no
  carve-out, no attestation entry.

## 6. Kill bars (frozen; ANY firing kills audit version RNGSCAN-2026-09-20-v3)
- K1: An audit-PASS build produces non-byte-identical outputs from the same
  full logged state (replay disproves the claim). One occurrence kills the
  version.
- K2: Blind red-team (§8): checker misses a planted entropy source.
  Miss rate > 0 over 20 plants kills the version.
- K3: Any single banned-construct category (4.1–4.9) is found by post-hoc
  inspection on an audit-PASSING variation path. One find kills the version.
- A killed version invalidates all Arm C trials run under it; they do not
  count. v3 does not gate Arm C either way (parallel line).
- v1 (RNGSCAN-2026-09-20-v1) and v2 (RNGSCAN-2026-09-20-v2) stay DEAD.

## 7. Checker v3 design (frozen)
7.1 Language: native Zag (`rngscan-v3/checker/rngscan_v3.zag`), compiled with
    the frozen znc toolchain. No RNG anywhere in the checker, modules, or
    harnesses. The checker is deterministic given its inputs. CLI:
    `rngscan_v3 <module.zag> <module-binary> <replay-evidence> <attestation.json>`
    Exit 0 on PASS, 1 on FAIL (attestation written either way), 2 on
    usage/IO error.
7.2 Vendored natives: `rngscan-v3/substrate/R33_NATIVE_SHA256_V2.zag` and
    `rngscan-v3/substrate/R33_NATIVE_IO_V1.zag` are audited ONCE at vendor
    time AND hash-verified at every audit run against the §5 constants
    (mismatch → `VENDOR` FAIL hit). They are trusted IO/crypto surface, NOT
    re-scanned as variation path. Module sources `@import` them by bare
    directive; the checker resolves imports relative to the module's
    directory and excludes any source whose path ends in either vendored
    filename from the scan set (they are still included in
    `module_sha256`).
7.3 Source scan (variation path = module + its own helper files, in import
    order):
    - Line-based. `//` comments stripped (string-literal-aware); an
      unterminated `/*` block opener is a FAIL hit (block comments
      unsupported on the variation path). Each line is split into code part
      and string literals: identifier rules run on the code part with literal
      contents blanked; the extracted literals are scanned for
      `/dev/urandom`, `/dev/random`, `getrandom` (rule 4.1/4.6).
    - ANY `_zag_raw_syscall(` occurrence in scanned source is a 4.1/4.2 hit
      ("raw syscall on variation path — use the vendored natives").
    - Intrinsic audit: every `_zag_` identifier in the code part is checked
      against INTRINSIC-ALLOW-2026-09-20-v3 after the banned-identifier
      rules (`_zag_clock_*`, `_zag_slice_ptr`, `_zag_cstr_ptr`,
      `_zag_raw_syscall`) have fired; any other `_zag_*` is a 4.2 hit
      ("unlisted intrinsic").
    - Uninitialized-use dataflow (rule 4.3), per function, per `nio_alloc`'d
      variable, with SIMPLE ALIAS tracking:
      * State starts UNINIT at the `let NAME … = nio_alloc(` line.
      * `let ALIAS[:type] = NAME…` (right-hand side begins with NAME
        followed by a non-identifier char) makes ALIAS share NAME's state
        slot (same memory; reads through either name are tracked together).
      * INIT is granted ONLY by the STRICT CANONICAL INIT FORM, verified
        textually per variable:
        1. the first non-blank code line before the loop is
           `let I:i32=0;` or `I=0;` (I = counter identifier);
        2. the loop condition, whitespace removed, is exactly `I<B.len`;
        3. the loop body, whitespace removed, is exactly two statements:
           `B[I]=<expr>;` then `I=I+1;`, where statement 1 begins with
           `B[I]=` (exact identifiers B, I), `<expr>` does not contain
           `B[`, and the body contains no identifier-boundary token from
           {`if`,`for`,`while`,`break`,`continue`,`return`,`match`}.
        * Any buffer with no canonical init loop stays UNINIT.
      * `nio_free(NAME)` marks the slot FREED.
      * A USE of a tracked name while its slot is not INIT is a 4.3 hit
        (reported once per variable per function). A USE is any
        identifier-boundary occurrence of the name except: the alloc line,
        `NAME.len`, `nio_free(NAME)`, and lines inside NAME's own canonical
        init loop. (This covers both `NAME[` element reads and passing the
        buffer as a function argument.)
      * Path-insensitive and intra-procedural: conservative state is kept
        across all textual paths (documented limitation, fail-closed).
      * Blessed pattern for kernel-filled buffers: `nio_alloc` → canonical
        zeroing loop → kernel fill → reads permitted (the v1/v2 clean-round
        precedent, now required to be canonical).
    - Callee enumeration: `fn NAME(` definitions collected; reachability
      from `vary_expr` via textual `NAME(` call sites; `callees` = reachable
      count excluding `vary_expr`; missing `vary_expr` is a FAIL hit.
      `ops_checked` = non-blank, non-comment source lines across the
      variation-path set.
    - `module_sha256`: sha256 over the transitive sources concatenated in
      import order.
    - The 4.5 pointer-cast check: a code line containing `as i64`/`as u64`
      together with `ptr`/`cstr` is a 4.5 hit (approximation; fail-closed,
      documented).
    - Pinned tables: pass 0 collects identifiers declared
      `const NAME:type=value;` on a line containing `PINNED` (case-sensitive
      marker); these names are hashed into `lookup_table_sha256` and are the
      ONLY names that activate the 4.4 carve-out.
7.4 Rule 4.4 structural check (variation path):
    - T1 (type-associated): for each `struct T {` declaration (T lowercased,
      len ≥ 2): if some `fn` name contains T as a substring AND a
      boundary-aware insert-family token, AND some (possibly different) `fn`
      name contains T AND a boundary-aware iter-family token → 4.4 hit
      naming the type.
    - T2 (prefix-associated): for each `fn` name with a boundary-aware
      insert-family token, take the prefix before the token; for each `fn`
      name with a boundary-aware iter-family token, take the prefix before
      the token; if the two prefixes are equal, non-empty, and ≥ 2 chars →
      4.4 hit naming the prefix.
    - Insert-family tokens: `insert`, `put`, `add`, `push`, `emplace`.
      Iter-family tokens: `iter`, `enumerate`, `foreach`. Boundary-aware =
      the char before/after the token is not `[a-z0-9]` (`_` and string
      edges allowed).
    - The v2 identifier token list (§4, 4.4) is retained as a first-pass
      tripwire; the narrowed carve-out (§4.4) applies to the tripwire only.
    - KNOWN RESIDUAL: insert/iterate functions that share neither a
      declared struct name nor a name prefix evade T1/T2 (covered by the
      tripwire, replay, and K3).
7.5 Object scan (direct byte parse of the module binary; no objdump):
    - Raw byte-substring search for `/dev/urandom`, `/dev/random`,
      `getrandom` — any occurrence is a 4.1/4.6 hit.
    - For each `0F 05` (syscall): DIRECT recovery (v2) — the last `B8
...[truncated 5455 chars]