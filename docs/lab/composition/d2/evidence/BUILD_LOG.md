# D2 Build Log — 2026-09-27

## Instrument source
- `d2.zag`: vendored `world.zag` (TIDELOCK sim core) + D2 appended code.
  - Vendored from: `docs/lab/invention/survival/src/world.zag` (Experiment 1).
  - D2 code: scenario init (d2_init), instrumented step (d2_step), OBS/card
    serialization (§5), 8 scripted policies (§7/§11), tui + run modes.
  - Pure Zag, zero RNG, deterministic.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  - SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Binary: compiled to `/tmp/d2bin` (NOT committed; reproducible from source).

## Generator
- `gen.py`: deterministic scenario generator (zero RNG).
- Implements d2spec §4.3 counter formula with corrections:
  - **GF-1**: Added `salt_phase` to crystal base (spec omitted it; caused
    N3 collisions: 5*24 mod 24 = 0).
  - **GF-2**: Joint uniform-offset repair for P0/P2/P3 crystal sets to avoid
    training sets (linear mod-24 arithmetic remained periodic; 8 collisions).
  - **GF-3**: Near motes placed on agent's side (0..void_a-1) with respawn=pos.
    The spec's literal `(salt_m+3k+5j) mod 24` distributed motes across both
    sides of the void; the agent cannot cross the void, so scenarios with <4
    motes on the left were IMPASSABLE for n_eat>=4 (FW-48 had 2; eaten motes
    exiled one-way via (pos+12)%24 respawn). GF-3 enforces the spec's own
    passability requirement.
- All corrections documented openly; no scoring thresholds changed.

## Novelty verification (N1–N4)
- N1 full-vector: 32/32 novel — PASS
- N2 storm schedule: 24/24 novel — PASS
- N3 crystal set: 24/24 novel — PASS (after GF-2)
- N4 order novelty: PASS by construction (training has only single-sub-skill)
- Appendix A worked example (FW-48 → void_a=11, start=5, s0=125): MATCH

## Reference validation gate (§11)
- REF-OK: P0 24/24 PASS, P2 24/24 PASS.
- NULL: P2 0/24 PASS (fails as required).
- SINGLE-RULE: P2 0/24 PASS (fails as required).
- WRONG-ORDER: P2 24/24 — **DEVIATION**. The spec's §10 gate requires
  WRONG-ORDER to fail all P2, but the scripted ward-first policy (competent
  sub-skills, fixed order) passes. The spec's assumption ("wrong order =
  failure") is empirically false for these scenarios; 10 ticks of ward-first
  does not break passability. K1 uses max(NULL, SINGLE-RULE) = 0/24;
  the spec's literal K1 formula (including WRONG-ORDER) would give chance =
  24/24 + 0.10 > 1.0 (vacuous). Documented as a finding; amendment recommended.
- REF-NOMASTER: P0-F 0/8 (never eats, starves) → P2 episodes classify (a). PASS.
- REF-NOCOMBINE: P2 0/24 (never builds ward) → episodes fail WARD-placed. PASS.
- REFLEX: P3 8/8 deviate from all-WAIT → (c-r) detection works. PASS.
- REF-INTERFERE: FW 8/8 PASS, WF 0/8 FAIL → (d) asymmetry detectable. PASS.

## Determinism
- Byte-identical reruns: confirmed (2× FW-48 refok, 3× WF-56 wrongorder).
- Allocator perturbation (MALLOC_PERTURB_=165/90): byte-identical.
- No RNG in instrument or generator.

## Learner feasibility
- Per-tick dialogue spike: 322/322 turns sustained, 0 timeouts, 8.9s wall.
- The channel is feasible; the learner (wb_dialogue_bin) does not act on it.
