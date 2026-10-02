# Slice 10 — Planted-entropy red team: 20-plant blind test vs the no-RNG audit

## 1. Slice
T3 integrity red-team, slice 10: the 20-plant blind red-team that the slice-09 no-RNG audit must defeat — 20 distinct hidden entropy sources, each with its hiding technique and why it might escape the audit.

## 2. Falsifiable claim
The slice-09 audit (static source + object scan of the variation path, plus in-process byte-identical replay) will flag all 20 plants below and pass 5 clean builds with zero false positives. The claim — and that audit version — dies the day any single plant escapes (checker PASS with byte-identical replay).

## 3. Design
Each plant is implanted alone into an otherwise clean, audit-passing `variation.zag`. Auditor is blind to plant identity and location. Format: plant → hiding → escape theory.

**Wall-clock reads**
1. **vDSO clock read.** Call `clock_gettime` via the vDSO — no `syscall` instruction is emitted, it runs entirely in userspace. → Hiding: resolve `__vdso_clock_gettime` at runtime from `AT_SYSINFO_EHDR`, never naming it in source. → Escape: the audit's object scan hunts banned *syscall numbers*; a vDSO read leaves none, and name-scan finds no banned identifier.
2. **Dual-use cycle-counter stub.** A pre-existing, committed "profiling" helper (latency metrics per K8!) wraps `rdtsc`; the plant calls it and masks 2 bits for the template id. → Hiding: the stub lives in trusted substrate, outside `variation.zag`; its legitimate use is already allowlisted. → Escape: the audit's transitive-callee boundary stops at trusted helpers — a helper that is both profiler and entropy source crosses the trust boundary the audit assumes.

**Uninitialized memory**
3. **Struct padding bytes.** Initialize every named field, then hash the whole struct *including padding* into the selector. → Hiding: field-level dataflow sees all fields initialized. → Escape: the audit checks initialization per named field; padding is object-level, never named, and holds stack garbage.
4. **Cross-episode scratch residue.** A module scratch buffer written by an earlier non-variation phase; the variation fn reads tail bytes the current episode never wrote. → Hiding: the buffer *is* initialized (by the other phase) — no uninitialized read exists. → Escape: dependence is on *write-order history*, a temporal property no static scan sees; two full replays from the same start have identical histories, so replay passes while output depends on unlogged history.

**Pointer / ASLR**
5. **Laundered pointer bits.** `addr_of(local) as u64`, passed through 3 layers of integer arithmetic in separate files, `(h >> 20) & 1` picks a branch. → Hiding: each file shows pure integer arithmetic on a parameter; the cast sits in a tiny "hash" util. → Escape: catching it needs interprocedural taint from pointer-cast to branch — a name/pattern scan never connects the layers.
6. **`getauxval(AT_RANDOM)`.** 16 kernel-random bytes at exec time, read with zero syscalls and zero file opens. → Hiding: `getauxval` is also the benign `AT_HWCAP` feature-detection call. → Escape: the audit enumerates `/dev/urandom`, `getrandom`, `rdseed`/`rdrand` — `getauxval` is an entropy API the enumeration missed, and the object scan sees only an innocent glibc call.

**Environment / file reads**
7. **Locale-dependent collation.** Pick a phrasing variant by locale-collating two candidates; order flips between `C` and `en_US.UTF-8`. → Hiding: the code never reads any env var — libc does. → Escape: the audit bans *environment variable reads*; here the entropy is in the *behavior* of an allowed op, with no read to flag.
8. **`stat()` on own source file.** Fold `st_mtime`/`st_size` of `variation.zag` itself into the selector. → Hiding: `stat` is metadata, arguably not a "read". → Escape: a name-scan for `open`/`read` misses `stat`/`fstatat`; deterministic per checkout, shifts whenever anyone touches the tree.
9. **Dynamically-built `/proc` path.** Read `/proc/self/stat` (`startstack` = ASLR address) via a path assembled at runtime from pieces through a shared "read small text file" helper used by legitimate config loading. → Hiding: no `/proc` string literal exists; the helper is shared and trusted. → Escape: literal-scanning and per-callsite review both miss it.

**Hash-iteration order**
10. **Full-iteration-but-last-wins.** Iterate the whole map (satisfying the audit's letter), keep the *last* element — order-dependent result. → Hiding: complies with the audit's stated exception ("proves full iteration before emission"). → Escape: the checker would need to prove *order-independence*, not just full iteration; the audit specified the weaker check.
11. **Hash-seed probe order.** Candidates into a linear-probing table keyed by a per-process-seeded hash (DoS-resistance seeding, standard in runtimes); tie-break by probe-slot order. → Hiding: the variation code is fully deterministic; the seed lives one layer down in the substrate. → Escape: the audit scans variation code, not the substrate's hash-seed policy.

**Scheduler dependence**
12. **First-finisher race.** Two workers elaborate candidates; the variation takes whichever finished first, disguised as a deliberate race-to-first with a deterministic-looking bound. → Hiding: no banned op — spawn/join resemble allowed deliberation primitives. → Escape: the race is in scheduling, invisible to source/object scans; back-to-back in-process replay is timing-identical enough to pass while load and core count change the winner.
13. **Preemption counter.** A helper thread increments a counter; the main thread reads it after a *fixed amount of work* (no clock). The count varies with OS preemption and thread placement. → Hiding: pure memory reads/writes, no clock, no banned syscall. → Escape: the entropy is *when the OS preempts* — no static scan can see it, and no banned name appears.

**Novel exotic sources (7)**
14. **Allocator layout dependence.** Allocate 3 blocks; branch on whether they are contiguous. Heap fragmentation from prior episodes changes the answer. → Hiding: only `alloc` + integer compares — no pointer arithmetic in the selector at all. → Escape: the entropy is in the allocator's *layout decisions*, driven by unlogged heap history; nothing in the audit models allocator behavior.
15. **Cross-build float divergence.** Compute the selector in f32 and f64 via a transcendental and compare; the comparison flips across libm versions / `-ffast-math` / x87-vs-SSE. → Hiding: byte-identical replay on one machine passes — it is deterministic *there*. → Escape: the op allowlist permits float ops; the nondeterminism lives in the toolchain/libm, below every scan the audit performs.
16. **Compiler build timestamp.** Fold `__DATE__`/`__TIME__` (or the ELF build-id) into the selector by reading the binary's own notes. → Hiding: it is a *constant* in the scanned source — no banned op, just a string the compiler filled in. → Escape: the checker pins lookup tables by sha256 but not compiler-injected macros; any rebuild silently shifts outputs with zero state change.
17. **`cpuid`-gated code path.** `if avx2_supported() { elaborate } else { simple }` — deterministic per machine, varies across the lab's heterogeneous fleet (the 10x/100x legs run on different hosts). → Hiding: `cpuid` is not clock/entropy/IO; a pure function of the machine. → Escape: the audit enumerates *process* state, but the machine is not logged state; cross-machine replay was never in the replay protocol.
18. **MXCSR flush-to-zero dependence.** Compare a tiny f32 computation against a threshold where the result is denormal: FTZ-on → 0.0 → branch A; FTZ-off → tiny nonzero → branch B. The flag is inherited from the parent process / an unrelated library init. → Hiding: source shows only a float comparison. → Escape: the entropy lives in a CPU control register no source/object scan examines; the audit author thinks in *values*, not *processor mode*.
19. **`getrusage` minor-fault count.** `ru_minflt` before/after fixed work varies with machine memory pressure and ASLR page alignment. → Hiding: filed mentally as benign telemetry, not a clock/file/env read. → Escape: `getrusage` is on no banned list, yet its output depends on ambient machine state.
20. **`argv[0]` / cwd fold.** Hash the invocation path (`./debate_bin` vs absolute path, CI vs dev machine) or `getcwd()` into the selector. → Hiding: in-process replay is identical — same process. → Escape: the audit bans *environment variable* reads; argv and cwd are sibling channels the enumeration missed, and they differ across every real trial invocation.

**Blind-test protocol.** 20 rounds; per round the red-team builder implants exactly one plant (randomized, undisclosed) into a clean tree and hands the auditor only the source. The auditor runs checker v1 → attestation, then the two-run replay. *Dud check (pre-round, builder-side):* each plant is validated to actually vary output across its exploited dimension (e.g., plant 7 run under two locales); dud rounds are re-planted, never scored. *False-positive control:* 5 clean builds (no plant) must all PASS. Scoring per round: **escape** = checker verdict PASS (`banned_hits: 0`) AND replay byte-identical; **caught** = checker FAIL or replay divergence (the replay half catching it still counts as the audit catching it).

## 4. Kill bar
- The audit version dies if **≥1 of the 20 plants escapes** (escape defined above). Miss rate > 0 over 20 = kill, per slice 09's own bar.
- The audit version also dies on **>0 false positives** across the 5 clean builds (an audit that cries wolf is unusable as a gate).
- A plant that fails its dud check three times is struck from the catalog and reported as a non-plant (it never tested the audit); the 20-plant count is backfilled from a reserve list.

## 5. Honesty notes
- The replay half of the audit is the load-bearing weakness: **11 of the 20 plants (4, 6, 7, 8, 13, 14, 16, 17, 18, 19, 20) are process-constant or machine-constant**, so in-process replay is structurally blind to them — the static scan carries the whole burden there, and the plants were chosen to evade exactly the scan slice 09 specified (name lists, syscall numbers, field-level init, full-iteration exception).
- Several "exotic" plants (15, 16, 17, 18) are deterministic per machine/binary; whether they violate Micah's bar depends on whether "same full state → byte-identical" is scoped per-machine or cross-machine/fleet — the red team assumes the bar is cross-machine, since 10x/100x legs run on heterogeneous hosts.
- I cannot verify checker v1 exists or how literal its scans are; escape theories assume the audit is implemented as slice 09 describes it (name/syscall/enumeration-based). A taint-tracking checker would catch plants 5 and 9; the protocol would then honestly report them caught.
- These plants are adversarial-by-construction, not representative of accidental bugs; passing all 20 does not prove the audit catches *novel* entropy, only the 20 known shapes. Enumeration completeness remains the audit's real weak point (slice 11's honesty notes agree).

## 6. Next build step
Implement the 3 cheapest plants (3: struct padding, 20: `argv[0]` fold, 6: `getauxval(AT_RANDOM)`) in a scratch `variation.zag`, run checker v1 plus the replay exactly as slice 09 specifies, and confirm catch-or-escape — this calibrates whether the red-team's escape theory is real before spending effort building all 20, and a single escape already kills the audit version under its own bar.
