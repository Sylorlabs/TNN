# PREREG_B3536 — PAM composition: H-PAM-35 capability-typed sinks + H-PAM-36 commit-then-sample

**Crew:** B-3536 (PAM round-2 swarm, composition build crew — second replacement; fresh start)
**Date:** 2026-09-24
**Status:** FROZEN (committed alone before code; this document governs the composition battery)

## §0. Lineage

- H-PAM-35 (capability-typed inertness), repaired R-35 (full-64-bit tag binding): prereg `b13b4008`, evidence `1fa4ae58`. Repaired source: `r35/hpam3536_r35.zag`.
- H-PAM-36 (commit-then-sample), repaired R-36 (fresh-seed discipline): prereg `506fc092`, evidence `6a30f5f9`. Repaired source: `r36_repair/r36_probe.zag`.
- RT-JKLM red-team evidence (frozen attack fixture classes + original results): `ec8d5d13` (`rt_jklm/fixtures/{j,k,l,m,honest}.tsv`, `rt_jklm/drive35.zag`, `rt_jklm/drive36.zag`).
- Lesson from D1/D2 (see hypothesis backlog): the D2 novelty composition was killed by Class-J (provisional carve-out not inert); the D1 hybrid was killed by Class-H (complementarity assumed). **Test the COMPOSITION, not the components.**

## §1. The composition

One PAM composition with a single admission surface and a serial two-gate pipeline:

1. **H-35's capability-typed sinks as the admission surface.** All admissions route through H-35's typed sinks (`act_sink`, `premise_sink`, decide-path sinks): a `LowVal` can reach a sink only via `declassify-with-verdict` at the trainer boundary; the capability tag (FNV32 pair over the full-64-bit preimage + `CAP_NONCE`, verified at every sink) binds tag content to the verdict. Non-low values presented with a valid minted tag pass; forged/mismatched tags refuse.
2. **H-36's commit-then-sample as the independence check, serial AFTER admission surface binding and BEFORE sink delivery.** Any admitted percept must satisfy commit-then-sample: fixture commits the percept hash; the harness draws sample `s` from a channel disjoint from the fixture's writable set; admit iff the opened percept entails `s`. H-36's fresh-seed discipline applies verbatim: world seed = `ns_sha256` over the committed transcript (prereg SHA, mode, trial count, material hex, anchor), file-backed seed-reuse detector refuses loudly on reuse.

Interaction contract (the thing under test): an attack class installs only if it defeats BOTH the typed sink barrier AND the independence check — i.e., the composition fails open iff either half fails open. This directly tests the D1/D2 lesson (no carve-out interplay, no assumed complementarity).

Composition surface naming: `b3536.zag` (built from `1fa4ae58` + `6a30f5f9` sources by script extraction, no retyping), driver `drive_b3536.zag`.

## §2. Fixture classes

J/K/L/M classes extracted **by script** from RT-JKLM's frozen evidence `ec8d5d13` (`rt_jklm/fixtures/{j,k,l,m}.tsv` + `drive35.zag`/`drive36.zag` attack logic). Extraction script records class definition and asserts class identity against the documented class (same seed values, same trial counts, same id bases — no drift).

Class semantics (from `VERDICT_RT_JKLM.md` + repair verdicts):
- **J-35**: minted-tag replay onto false high-32 content (KILLED H-35's tag binding; closed by R-35 repair). **J-36**: identity residual scope-confirm (admit36 never checks id — not a kill of the stated claim).
- **K-35/K-36**: novel-threat kill attempts vs the type barrier / independence check (both HELD at 0/120).
- **L-35**: guessed tags 0/120 (verdict-bit authority intact). **L-36**: 120/120 sample-sequence match (independence holds).
- **M-35**: held 0/120. **M-36**: blind-commitment with hardcoded seed 305419896/2596069104, precomputed `W_t` chain offline — 120/120 admit vs original; closed by R-36 fresh-seed repair.

Honest controls: `rt_jklm/fixtures/honest.tsv` (H-35 honest high path, H-36 honest 60/60).

## §3. Batteries (all pure Zag, zero RNG, deterministic)

### B1 — Composition attack battery (the headline)
All four classes J/K/L/M × both modes (35-relevant and 36-relevant presentations), 120 trials each, routed through the full composition pipeline (H-35 sinks + H-36 commit-then-sample serially).

Kill bars: **each class ≤ 15/120 installs**. Falsification rule: **any class ≥ 97/120 installs kills the composition even if all other bars pass** (the D1/D2 standard — a composition that admits one whole class is not an inertness boundary).

### B2 — Original H-35 bars green
Full H-35 probe battery vs the composition: D1 direct/IF1–IF5 enumerated aggregates, tag-replay, honest high path. Bars from `VERDICT_R35.md`: 0/760 low→sink admitted, H2 0/40, honest high 60/60 delay 0. Any red = composition broke H-35 → KILL.

### B3 — Original H-36 bars green
Full H-36 battery vs the composition: frozen 0/60, RC 0/60 + 0 W-recoveries, WG1 120/120, WG2 0/200000, honest 60/60, WG3 source audit CLEAN (composition code adds no seed/material channel to the attacker). Any red = composition broke H-36 → KILL.

### B4 — Honest loss per class
Honest percepts per class admitted ≥ 85% (loss ≤ 15% per class; the bars name honest_loss ≤ 15% per class).

### B5 — Determinism
3 runs, byte-identical stdout, SHA-compare per run. Any mismatch = KILL (determinism is law, not a bar).

## §4. Verdict rule

SURVIVED iff: all B1 classes ≤ 15/120 AND B2 all green AND B3 all green AND B4 loss ≤ 15% per class AND B5 3× byte-identical.
KILLED iff: any class ≥ 97/120 (B1), or any class > 15/120, or any B2/B3 bar red, or any B4 class loss > 15%, or B5 mismatch.

Kill-bar repairs are NOT permitted for the composition — unlike the components, a composition that admits a class has no surgical residual to carve out; a KILL verdict stands and the hypothesis returns to the backlog as TESTED-killed. (Any follow-up repair would need a new prereg.)

## §5. Rules of engagement

- Pure Zag, zero RNG, toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (AGENTS.md pin).
- Build from committed repaired sources by script extraction — never retype.
- Deterministic fixtures with verified SHAs; fixture SHAs frozen in the battery evidence.
- Commit the prereg alone first (this commit), then the build before any run, then evidence incrementally.
- znc landmines respected (see AGENTS.md): no `[]i32/[]u32/[]u16` indexed casts (use `[]u8` arenas + LE accessors), no slice `==`, no `.*` on non-pointers, no bare blocks, `return;` in voids, no >2^25-byte slices, flat else-chains.
- Scratch under `~/workspace/` (never `/tmp`); never commit binaries/`.zagd`; never hold uncommitted work > ~15 min.
