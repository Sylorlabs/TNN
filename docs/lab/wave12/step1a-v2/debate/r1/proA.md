# Round 1 Opening — DEBATER A (pro v3): Build RNGSCAN v3

## (1) Thesis

The no-RNG law is load-bearing for this entire program — every claim of deliberate, state-determined behavior rests on it, and a law enforced by vibes is not a law. Both RNGSCAN kills were the process working as designed: the blind red team found real gaps and K2 fired, honestly and publicly. The v3 amendment answers each known gap with concrete, localized fixes; the attack surface is finite (Zag surface + znc lowering + syscalls + intrinsics); and a passed auditor permanently de-risks every future trial. Build it.

## (2) Three strongest arguments

**1. The methodology is converging, not failing.** v1 died to RNG hidden from a C checker; v2 died to three specific, named misses — an even-slots-only init loop, a hand-rolled `EntrySet` table, a `pin_table` carve-out rider. Each death names a finite, patchable *class*, and the draft amendment patches all three: canonical init form with fail-closed, structural (not token-based) hash-iteration detection, carve-outs narrowed to const + `// PINNED` + attestation-hashed. A process that kills its own versions on honest misses is converging. Stopping after the second kill mistakes the *detector working* for the *detector failing*.

**2. The attack surface is bounded.** The hiding-spot space is concretely enumerable: the Zag language surface, znc's lowering, the syscall boundary, the intrinsic surface. v3 covers all four — register-taint on syscall numbers, an explicit `_zag_clock_*` ban plus a one-time intrinsic-surface audit, structural table detection at the language level. That's a checklist, not a research frontier. ~1280 lines of Zag, localized scope.

**3. Residual risk permanently poisons Arm C.** The state-variation trial asks one question: does identical input produce state-caused expression variation? Without a passing auditor, every variation claim is permanently attackable as "maybe hidden RNG" — exactly the confusion the experiment exists to eliminate. A passed v3 certifies the law for every trial downstream. The cost of *not* building it isn't delay, it's a permanent asterisk on the program's central result.

## (3) The strongest argument against, answered

**The concession:** the watch items. Several plants — computed syscall immediates, the runtime-built `/dev/urandom` path, the `_zag_clock_monotonic_ms` timer — were caught *only by replay divergence*, with both static scans missing the mechanisms entirely. And the v2 round stopped at 14/20 plants with 6 unscored, so the full miss count is unknown. If replay is doing the real catching, v3 may be polishing the wrong tool, and each version dying to a *new* trick is at least consistent with an inexhaustible space.

**The answer:** First, v3 incorporates the lesson — replay is hardened (N runs + heap pre-dirtying) as an explicit layer. Defense-in-depth is the design; the static scanner needn't be the only catcher, it needs to be the mechanical one that runs cheaply on every build. Second, "a new trick each time" is convergence behavior: the v2 misses are classes, not instances — canonical-init failure, structural table blindness, carve-out riding. Fixing a class kills its whole family of future tricks. Third, the 6 unscored plants are a measurement gap, and you don't close a measurement gap by deleting the instrument — you finish the red team properly under a v3 build.

## (4) What v3 unblocks, and what it costs

**Unblocks:** the Arm C gate (prereg 97882fc) — variation claims that can't be dismissed as hidden RNG — plus permanent mechanical enforcement of the no-RNG law, with kill bars K1/K2/K3 unchanged (the amendment doesn't move the goalposts).

**Cost:** ~1280 lines of pure Zag, localized scope, one more blind red-team round, and Arm C stays parked until a version passes. Science waits weeks either way — the question is whether it waits behind a certified gate or a permanent asterisk.
