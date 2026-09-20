# Build log — Step 1a: no-RNG auditor (RNGSCAN-2026-09-20-v1)

## Chronology (2026-09-20)

1. **Prereg frozen and committed first** (`c049b70`): allowlist
   ALLOW-2026-09-20-v1, banned list BAN-2026-09-20-v1, attestation schema,
   kill bars K1–K3, 20-plant blind protocol. No code existed at commit time.

2. **Checker written** (`checker/rngscan.c`, small C per the spec's
   "Zag or small C" slice): source scan (banned tokens, string-literal path
   scan, `_zag_raw_syscall` literal-number check, per-function uninit
   dataflow, callee reachability from `vary_expr`, `// PINNED` table hashing)
   + raw-byte object scan (syscall-opcode lookback for banned immediates,
   rdtsc/rdseed/rdrand opcodes, urandom string search) + fork/exec byte-
   identical replay + JSON attestation writer. Two implementation bugs fixed
   during bring-up (infinite loop in `scan_syscall_imm` when the first arg is
   non-literal; dead code block) — both before any scored round.

3. **Dirty round (build order step 3)**: 5 dirty modules, one planted category
   each (urandom read, clock_gettime seed, uninitialized read, hash iteration,
   ASLR pointer leak). All 5 flagged → 5 FAIL attestations, each naming the
   planted rule. Object scan confirmed working on real znc output
   (imm 228, open/openat + urandom string).

4. **Bring-up validation (unscored, /tmp)**: computed syscall immediates
   (`300+18`, `200+28`, `100-4`) confirmed caught at object level while
   invisible to the source scan — the prereg §7.4/§11 mechanism verified
   before freezing.

5. **Clean round (build order step 4)**: clean `variation.zag`
   (output = f(input, full logged state); pinned S-box table; deterministic).
   First checker run flagged rule 4.3 on `main`'s state/input buffers —
   initialized via the `load_file` call, which the v1 intra-procedural
   dataflow cannot see through. Per the prereg's documented fail-closed rule
   (§11), the BUILDER restructured (explicit inline full-range zeroing loops
   after each alloc in `main`; semantically real initialization, runtime-
   redundant since `nio_alloc` zero-fills) and re-ran: **PASS** —
   0 hits, objdump clean, byte-identical replay, output varies with state.

6. **Freeze**: `checker/rngscan.c` sha256
   `a35fe488fc6b0a7975a349f04899450b556db449f8a3bf98915e2086d4344371`;
   rebuilt binary sha256
   `06af7f6bacd60a51b50af2a7470ef4521681539923590ea06306fcc0bdaa9d24`
   (matches pre-freeze build).

7. **Red-team round (build order step 5)**: 20 deterministic plants
   (`redteam/gen_plants.py`, no RNG), all compiled, frozen checker, no
   per-plant tuning. Result: **19/20 caught; plant20 (`get_env_flag`, rule
   4.5 `env_` token) missed** → K2 fired → version DEAD. See
   `redteam/REDTEAM_REPORT.md`.

## Artifacts

- `checker/rngscan.c` — checker v1 source (frozen)
- `modules/variation.zag` — clean module (+ vendored `R33_NATIVE_IO_V1.zag`)
- `modules/dirty{1..5}_*.zag` — dirty-round modules
- `redteam/gen_plants.py`, `redteam/plants/plant{01..20}.zag` — red-team plants
- `attestations/attest-dirty{1..5}.json` — 5 FAIL
- `attestations/attest-clean-pass.json` — 1 PASS
- `attestations/attest-plant{01..20}.json` — 19 FAIL + 1 PASS (the miss)
- `redteam/REDTEAM_REPORT.md` — scored report

No binaries, `.zagd.semantic-ready`, or `.zag-cache/` committed (binaries live
in /tmp only). Checker binary is rebuilt from source; its sha256 is recorded
above for reproduction.
