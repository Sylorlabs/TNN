# Combiner Architecture Salt Testing — TESTING.md

**Date:** 2026-09-28
**Tester:** TESTER-1 (combiner-architecture)
**Question:** Does each architecture learn the rule, or memorize the manifold?

## 1. Architectures under test

| ID | Name | Mechanism | Binary SHA-256 |
|----|------|-----------|----------------|
| H-A | operator-primitive induction + growth | Induces (position-op, byte-op) programs; grows new primitives | `abb948157a985cd480f870203af36f829820b3aa1e4e085846fd6374135201c9` |
| H-B | DELTA — affine position-program induction | Induces integer affine position maps; bytes ride along untouched | `d38ee13f86bbf7ab1a95742cfc1688ff51e09f5f8985052315a8208f9f87c199` |
| H-C | trace anti-unification | Anti-unifies execution traces into anchored role schemas | `5c1ab4843094ebca706fd136fc085e68a4534feb2cc04881fc410fb98ee889f1` |

All three SHAs reproduce the committed `BUILD.md` values byte-identically (verified 2026-09-28).

## 2. Battery

**Shape:** P0 48 probes (8/rule × 6 D1 rules) · P1 120 sequential compositions (30 ordered pairs × 4 lengths) · P3 8 probes (4 swap-first-last + 4 sort-descending).

**Salts (8 arms):**
| Arm | Salt | Provenance |
|-----|------|------------|
| A | Job-3 affine `(c+13k+9k²)%26` | Exact reimplementation of `docs/lab/composition/job3_affine/affine_test.zag` |
| C | Job-3 quadratic | Exact reimplementation |
| B | Job-3 cubic | Exact reimplementation |
| D26 | H-A piecewise-discontinuous quadratic (mod 26) | Frozen H-A §3 |
| D256 | Piecewise-discontinuous quadratic, canonical mod-256 | Tester-selected constants (see §7) |
| Esub | H-A frozen substitution strings | Frozen H-A §3 |
| Eaff | Phase-indexed affine byte permutation `(37b+11)%256` etc. | Tester extension of frozen H-B E (see §7) |
| Exor | XOR/ROTL8 keyed family | Tester-selected constants (see §7) |

**Teaching protocol (load-bearing — see §6):** Each architecture is tested under its hypothesis's preregistered teaching convention:
- **H-A:** salted teaching (train salt) — explicit in H-A HYPOTHESIS.md §3 ("Teach: indices 0–5, 700–705, train salt").
- **H-B:** CLEAN teaching, salted probes — explicit in H-B HYPOTHESIS.md §2.1 ("teaching examples are unsalted") and §3 ("salt applied to probe inputs; teaching clean").
- **H-C:** CLEAN teaching, salted probes — explicit in H-C HYPOTHESIS.md §5 ("teach on clean examples; probe on salted items").

**Composition adapter:** Two-pass, architecture-neutral. Pass 1: apply rule A to each P1 input. Pass 2: apply rule B to the *actually emitted* intermediate (not the oracle intermediate). Scores: link-A correctness, link-B correctness on the received intermediate, full-chain correctness. This preserves sequential Job-3 semantics and does not teach a composed rule.

**Determinism:** Every architecture output run twice byte-identically, plus a genuine allocator-perturbation spot check (`MALLOC_PERTURB_=165`). All pass.

## 3. Calibration — memorizers are dead on every arm

Job-3 affine memorizer (`aff26`), quadratic (`quad26`), cubic (`cubic26`), and free-delta (`freedelta`) run on every arm. P0 scores (hits/48):

| Arm | aff26 | quad26 | cubic26 | freedelta |
|-----|------:|-------:|--------:|----------:|
| A (salted teach) | 16 | 12 | 8 | 16 |
| C (salted teach) | 4 | 12 | 8 | 16 |
| B (salted teach) | 4 | 4 | 8 | 16 |
| D26 | 4 | 4 | 4 | 16 |
| D256 | 4 | 4 | 4 | 16 |
| Esub | 5 | 5 | 3 | 16 |
| Eaff | 5 | 5 | 5 | 17 |
| Exor | 5 | 4 | 3 | 14 |

With clean teaching (H-B/H-C protocol), memorizers score even lower on movement rules (aff26: r2 0/8; quad26: r2 0/8). **No fitting memorizer learns any family.** All fresh families are calibrated. (Per the task rule: had degree-2 survived on a family, that family would be marked uncalibrated and architectures not scored on it. It did not survive anywhere.)

Note on H-C §5.1: it predicts a *rule-aware* quadratic memorizer would reach 48/48 on the affine/quadratic arms. The Job-3 (rule-blind) memorizer used here does not. The arms remain diagnostic because the architectures beat the rule-blind baseline on movement rules where it scores 0–4/48.

## 4. Results

### H-A (salted teaching — its preregistered protocol)

| Arm | P0 /48 | P1 chain /120 (A/B) | P3 /8 |
|-----|-------:|--------------------:|------:|
| A | 48 | 120 (120/120) | 8 |
| C | 48 | 120 (120/120) | 8 |
| B | 48 | 120 (120/120) | 8 |
| D26 | 48 | 120 (120/120) | 8 |
| D256 | 48 | 120 (120/120) | 8 |
| Esub | 48 | 120 (120/120) | 8 |
| Eaff | 48 | **115** (118/117) | 8 |
| Exor | 48 | 120 (120/120) | 8 |

**The Eaff failures (5):** All are `upperfirst` (r4) emitting identity instead of uppercasing, on Eaff-salted bytes outside `a`–`z`:
- `r3+r4` on `p\xb7` → mid `p` → emitted `p`, expected `P`
- `r3+r4` on `g\xae\xf5\xda!` → mid `g\xae\xf5\xda` → emitted identity, expected `G...`
- `r4+r3` on `y\xc0\xa5\xec\xd1` → emitted identity, expected `Y...`
- `r4+r5` on `p\xb7\x9c\xe3` → emitted identity, expected `P...`
- `r5+r4` on mid `g\x82\xae\xf5` → emitted identity, expected `G...`

H-A's `UPPER1` is alphabet-gated: it does not fire when the first byte is outside `a`–`z`. The Eaff salt (byte permutation mod 256) routinely produces such bytes. These are **wrong emissions**, not withholds.

**Kill bars:**
- **K-HA-8 FIRES.** Tester-created injective salt (Eaff) causing wrong emissions kills. (5 wrong emissions documented above.)
- K-HA-1: no wrong emissions on the six preregistered arms (A/B/C/D26/D256/Esub) — holds there.
- K-HA-5: cross-arm score identity holds on preregistered arms (all 120/120); Eaff is not a preregistered arm.
- K-HA-6 (nondeterminism): does not fire — all runs byte-identical, perturbation spot-check passed.

**Verdict: H-A is KILLED by K-HA-8.** It is perfect on its preregistered battery (48/48, 120/120, 8/8 on all six frozen arms) but its `upperfirst` does not survive a byte-permutation salt — a genuine mechanism boundary (alphabet-dependent byte op), caught by its own kill bar.

### H-B / DELTA (clean teaching — its preregistered protocol)

| Arm | P0 /48 | P1 chain /120 (A/B) | P3 /8 |
|-----|-------:|--------------------:|------:|
| A | 48 | 119 (120/119) | 8 |
| C | 48 | 119 (120/119) | 8 |
| B | 48 | 119 (120/119) | 8 |
| D26 | 48 | 119 (120/119) | 8 |
| D256 | 48 | 119 (120/119) | 8 |
| Esub | 48 | 119 (120/119) | 8 |
| Eaff | 48 | 119 (120/119) | 8 |
| Exor | 48 | 119 (120/119) | 8 |

**The single P1 shortfall (all arms, same item):** pair `r3+r2` (droplast→rotleft) on a 2-byte input; droplast yields a length-1 intermediate; H-B **withholds** on rotleft of a length-1 token (no length-1 rotleft in training; its affine program has no length-1 clause). Honest withhold, not a wrong emission. Zero wrong emissions anywhere.

**Kill bars:**
- K-HB-1 ("below 47/48 P0 or 118/120 composition kills"): measured 48/48 and 119/120 — **does not fire** (119 > 118).
- K-HB-2 (dupfirst/droplast both orders match oracle): holds — 120/120 link-A, and the only shortfall is a withhold.
- K-HB-5 (swapfl/sortdesc): 8/8 P3 on all arms — holds.
- K-HB-6 (nondeterminism): does not fire.

**Verdict: H-B SURVIVES.** 48/48 P0 on all 8 salts, 119/120 composition (one honest withhold on a degenerate length-1 intermediate), 8/8 P3. The salt-riding mechanism (§2.1) is confirmed: identical scores across all 8 salt families, memorizers dead on the same items.

**H-B implementation notes (findings, not kills):**
1. H-B's driver expects rule IDs `R1`–`R6`, `SWAP`, `SORTD` (not `r0`–`r7`); an adapter translates.
2. H-B's induction is **order-sensitive**: it requires teaching examples contiguous per rule (rule-major). Token-major (interleaved) teaching yields `NO_LENGTH_RULE` withholds on everything. Its own committed fixtures are rule-major. This is a robustness gap worth a follow-up, but the preregistered battery uses the format its implementation expects.

### H-C (clean teaching — its preregistered protocol)

| Arm | P0 /48 | P1 chain /120 (A/B) | P3 /8 |
|-----|-------:|--------------------:|------:|
| A | 48 | 118 (120/118) | 4 |
| C | 48 | 118 (120/118) | 4 |
| B | 48 | 118 (120/118) | 4 |
| D26 | 48 | 118 (120/118) | 4 |
| D256 | 48 | 118 (120/118) | 4 |
| Esub | 48 | 118 (120/118) | 4 |
| Eaff | 48 | 118 (120/118) | 4 |
| Exor | 48 | 119 (120/119) | 4 |

**P1 shortfalls (2 per arm):** both are honest `upperfirst` (r4) **withholds** on composition intermediates:
- `r1+r4` (dupfirst→upperfirst): intermediate `hhbxvv` (doubled first byte) → withhold.
- `r3+r4` (droplast→upperfirst): intermediate `g` (length-1) → withhold.
Zero wrong emissions.

**P3 4/8:** the 4 swap-first-last probes withhold (W5); the 4 sort-descending probes are correct. This is the **known frozen-spec conflict**: the committed H-C withholds W5 on swap-first-last, contradicting K-HC4's "minimum capability includes swap-first-last."

**Kill bars:**
- **K-HC4 FIRES.** Minimum capability includes swap-first-last; H-C withholds it (0/8 on swapfl probes, W5). This is a frozen-spec contradiction documented in the hypothesis itself — the architecture as committed does not meet its own K-HC4.
- K-HC5 ("sequential chaining must be 100% on learnable links"): 118/120 with 2 honest withholds — the links withheld on are degenerate (length-1, doubled-byte); no wrong emissions. Counted as a miss against the 100% bar but not a wrong-emission kill.
- K-HC6 ("clean-trained score cannot drop on any salt family"): P0 48/48 on all 8 arms — **does not fire**.
- K-HC7 (nondeterminism): does not fire.

**Verdict: H-C is KILLED by K-HC4** (its own minimum-capability bar, on the swap-first-last probes it withholds). It otherwise confirms its salt-invariance mechanism: 48/48 P0 on all 8 families with clean teaching, zero wrong emissions anywhere, memorizers dead on the same items.

**Critical protocol note:** With *salted* teaching (not H-C's preregistered protocol), H-C scored 32/48 on D256 and 0/48 on Eaff/Exor. With its preregistered *clean* teaching, it scores 48/48 on all 8. The hypothesis's protocol specification was load-bearing and correct.

## 5. Measured vs preregistered predictions

| Arch | Predicted | Measured | Kill bars fired |
|------|-----------|----------|-----------------|
| H-A | 48/48, 120/120, 8/8 every arm | 48/48, 120/120, 8/8 on 6 frozen arms; 115/120 P1 on tester Eaff (5 wrong) | **K-HA-8** |
| H-B | 48/48, 120/120, 8/8 every arm | 48/48, 119/120, 8/8 every arm (1 honest withhold) | none (K-HB-1 threshold 118 not breached) |
| H-C | 48/48, 120/120, 8/8 every arm | 48/48, 118/120, 4/8 every arm (2 honest withholds; W5 on swapfl) | **K-HC4** |

## 6. Methodological findings

1. **Teaching protocol is load-bearing and hypothesis-specific.** H-B and H-C both preregister clean teaching; testing them with salted teaching (the Job-3 convention) produces total failure (H-B: 0/48 withholds) or degraded scores (H-C: 0/48 on Eaff/Exor). Each architecture was tested under its own preregistered protocol — the only honest comparison to its predictions.
2. **H-B salt formulas in its hypothesis (mod 256) differ from the mandated Job-3 salts (mod 26).** Arms A/B/C use the exact Job-3 reimplementation per the task constraint; H-B's §3 salt table describes mod-256 variants. H-B's mechanism is salt-agnostic (§2.1: "for every per-byte salt function S"), and the measured 48/48 on the Job-3 salts confirms the generality claim.
3. **H-B is order-sensitive** (rule-major teaching required) and needs its own rule-ID vocabulary (`R1`–`R6`/`SWAP`/`SORTD`). Both are accommodated by adapters; both are documented robustness gaps.
4. **No architecture misled.** Every shortfall is an honest withhold except H-A's five upperfirst wrong emissions on Eaff (which its own K-HA-8 kills it for) and H-C's W5 swapfl withholds (which its own K-HC4 kills it for).

## 7. Tester-created constants (not frozen)

- **D256** piecewise-quadratic tuples `(A1,B1,A2,B2)`: train `(3,3,11,233)`, P0 `(5,3,7,233)`, composition `(7,3,3,237)`, final `(11,3,3,237)` — deterministically searched for zero TSV hazards, zero byte-sorted P0 tokens, distinct half-equations, phase variation.
- **Eaff** phase key bases `(37,11)`, `(13,7)`, `(53,29)`, `(91,3)` — the frozen H-B E (`S(b)=(37b+11)%256` fixed) collides 40 G1 pairs; phase-indexing was required for calibration. Labeled tester extension.
- **Exor** phase key bases `58, 29, 45, 161` — selected for zero TSV hazards and nonzero keys.

## 8. Reproducibility

- Instrument: `test/saltlab/saltlab.zag` (pure Zag, zero RNG). Binary `saltlab_bin` NOT committed.
- Fixtures: `test/fixtures/<arm>/{teach,p0,p1,p2}.tsv` (salted teaching) and `test/fixtures_clean/<arm>/` (clean teaching).
- Raw outputs: `test/raw/<arch>_<arm>/` (both runs + perturbation).
- Scores: `test/raw/<arch>_<arm>/SCORES.json`.
- All architecture outputs: twice byte-identical + `MALLOC_PERTURB_` spot check.
- Memorizer outputs: `test/calibration/`.

## 9. Bottom line

A dead hypothesis is a successful test. Two of three architectures are killed by their own kill bars:
- **H-A killed by K-HA-8:** `upperfirst` is alphabet-gated; a byte-permutation salt exposes 5 wrong emissions.
- **H-C killed by K-HC4:** withholds swap-first-last (W5), failing its own minimum-capability bar.
- **H-B survives:** the affine position-program mechanism rides every salt untouched (48/48 P0 × 8 arms), with one honest withhold on a degenerate length-1 composition intermediate.

All three beat every fitting memorizer on every arm. The memorizer ladder is dead; the remaining separations are mechanism boundaries, and the kill bars caught them by name.
