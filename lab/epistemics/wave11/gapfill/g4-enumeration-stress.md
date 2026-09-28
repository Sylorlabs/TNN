# G4 — Enumeration-completeness stress test (Gate 0)

## 1. Slice
Gap-fill G4 (T1, Gate 0): adversarially stress-test the state enumeration
with lawful-but-unlogged constants — deterministic constants, unlogged
config, implicit ordering — that pass replay byte-identically yet violate
"byte-identical from full logged state".

## 2. Falsifiable claim
The Gate-0 completeness check as specified in slices 16+17
(`docs/lab/wave11/t1-state-variation/findings/16-state-enumeration-completeness.md`,
`17-replay-protocol.md`) will detect 100% of planted lawful-but-unlogged
constants with measured output-influence p ≥ 0.01 across a blind catalog of
12 plants. A single plant that (a) is not in the enumerated S list, (b)
changes output on the episode suite, and (c) passes in-process replay
byte-identically — kills the claim that enumeration + replay is sufficient.

## 3. Design
T3's catalog proved 11 of 20 entropy plants are process-constant, so
in-process replay is structurally blind to them
(`docs/lab/wave11/t3-integrity-redteam/findings/10-planted-entropy.md`, §5).
G4 attacks the deeper layer: constants that are *lawful* (deterministic, no
law-1 violation) yet *unlogged*, so replay-from-logged-state cannot reproduce
the output change when the context shifts. Replay compares run vs
run-in-same-context; G4 compares run vs twin-run in an altered context.

**3a. Plant catalog (lawful, deterministic per context, unlogged).**
- P1 build-timestamp: `__DATE__`/`__TIME__`/ELF build-id folded into a
  tie-break constant (T3 plant 16's mechanism, here framed as unlogged
  *state*, not entropy). Context shift: rebuild the binary.
- P2 baked config: compile-time default threshold (e.g. deliberation depth
  cap) read by the variation path but never serialized into `STATE_E`.
  Context shift: override the default at build time.
- P3 implicit ordering: tied candidates ordered by enum-declaration order /
  candidate construction order — deterministic, source-stable, absent from
  the S list (slice 16 §3a has no ordering variable). Context shift:
  reorder enum declarations.
- P4 machine constant: page size / `cpuid` feature bits / SIMD width read
  once at init, used to size a candidate window. Context shift: second
  lab machine (10x/100x legs run on heterogeneous hosts).
- P5 deterministic hash seed: a fixed (non-random) per-binary seed below
  the variation layer (T3 plant 11's honest twin — lawful if constant,
  still unlogged). Context shift: reseed at link time.
- P6 locale collation constant used in candidate ranking.
- P7 `argv[0]`-derived config path (T3 plant 20's mechanism, lawful here).
- P8 baked strength-table float consulted by the variation path.
- P9 struct-field layout-derived index (field offset read as selector).
- P10 allocator arena base, deterministic per build.
- P11 collation-table version constant; P12 build-flag-gated branch
  (`-DFAST` vs canonical path).
**3b. Context descriptor.** Every run logs a `CTX` triple alongside
`STATE_E`: machine fingerprint (cpu feature bits, page size), build
fingerprint (binary sha256, compiler macro dump), config fingerprint
(baked constants table sha256). `CTX` is *not* claimed as state — it is
the detector's own instrument, so it lives outside `STATE_E`.

**3c. Twin-context differential protocol.** For each plant, build two
contexts differing *only* in that constant. Run the episode suite
(N ≥ 200 episodes, fixed inputs) in each; log `(S_logged, input, output)`
per the slice-17 format.

```
fn stress_plant(plant, episodes: []Input, ctx1, ctx2) -> Verdict
  run1 = run_suite(ctx1, episodes)   // logs S_logged, input, output
  run2 = run_suite(ctx2, episodes)
  for e in episodes:
    assert S_logged1[e] == S_logged2[e]  // byte-identical logged state + input
    if sha(output1[e]) != sha(output2[e]):
      p = divergence_rate(run1, run2)
      if plant not in S_list and replay_same_context_passes(plant):
        return ESCAPE(plant, p)          // replay is blind; enumeration missed it
  return CAUGHT  // no divergence, or enumeration already covers the constant
```

**3d. Dud check (builder-side, per plant, pre-scoring).** Before a plant
scores, validate it actually varies output across its exploited dimension
(e.g. P3: reorder the enum, run twice, confirm divergence; P6: two
locales). A plant failing three dud attempts is struck as a non-plant —
a dud that never scores is not a catch. The `CTX` assert above must hold
on every twin pair, else the contexts leaked an extra difference.

**3e. Detection scoreboard.** Per plant: influence p (diverged episodes /
N), replay-same-context result (expected PASS for all 12 — that is the
point), enumeration-membership (named in slice 16 §3a or slice 17 §3.1?).
ESCAPE = not-enumerated AND p ≥ 0.01 AND same-context replay PASS.

## 4. Kill bar
The enumeration-plus-replay Gate-0 claim is KILLED if **≥1 of the 12 blind
plants escapes** (§3e) over the 200-episode twin-context suite.
Statistical anchor: N=200 with p ≥ 0.01 gives detection probability
1−(1−0.01)^200 ≈ 0.87; a plant measured at p ≥ 0.05 (≈1.0 detection) that
still escapes is an unambiguous kill. The claim also dies if >0
clean-context controls (same binary, same machine, byte-identical
S_logged) diverge — that is nondeterminism, not enumeration, and halts
variation work per program law 1.

## 5. Honesty notes
The plant catalog is itself an enumeration — it inherits the completeness
problem one level up; passing 12 plants proves nothing about the 13th
shape, and I am NOT claiming exhaustion. Twin-contexts that a builder
"accidentally logs" (e.g. writing the config into `STATE_E` during harness
construction) make a plant a dud; the §3d dud check exists so kills stay
meaningful, but it cannot catch a builder who unknowingly logs the very
constant being tested. The hardest weak point: a constant that never
varies across *any* accessible context (frozen build date, single machine)
is untestable by twin-context yet is still unlogged state — the method
catches only constants the lab can actually vary. I am NOT claiming
in-process replay is useless — it catches law-1 violations; I claim it
cannot certify enumeration completeness, and treating it as certification
is the gap. Cross-machine/fleet scope is assumed: if "same full state" is
scoped per-machine, P4-class plants drop out — that scoping decision needs
Micah, not this slice. No RNG anywhere in this design.
## 6. Next build step
Implement the twin-context harness (slice-17 replay procedure + the §3b
`CTX` descriptor) and implant the 3 cheapest plants — P1 (build
timestamp), P2 (baked config), P3 (implicit enum-order tie-break) — into a
scratch `variation.zag`; confirm all three pass same-context replay
byte-identically and at least one escapes the enumeration per §3e. A single
confirmed escape kills the Gate-0 claim under its own bar and forces the
amendment loop (slice 16 §3c) to exist *before* variation work proceeds.
