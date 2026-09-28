# Job-3 verdict: the affine-memorizer adversarial test

Date: 2026-09-27. Prereg: `PREREG_JOB3.md` (frozen 2026-09-27, commit
`3a8ec2dac09de638cd5ea53385ff437efaa7adc3`). Red team ran BEFORE this
verdict (`redteam/REDTEAM_REPORT.md`). Pure Zag, zero RNG, byte-identical
reruns throughout.

## The question

Micah asked: is there a salt/transformation family under which genuine
combiners pass while Crew E's affine memorizer provably cannot?

## The answer

**Yes — the cubic non-affine salt.** Salt each token's letters with a
cubic polynomial in the position (`C1·k + C2·k² + C3·k³`, with the
higher-order coefficients changing per phase). The genuine combiner never
sees the salt and stays perfect; the affine memorizer can no longer find a
single straight-line map that connects a probe to its training examples,
because the cross-phase difference is curved, not straight. Every
length-3-or-longer probe fails the memorizer's own consistency check, so it
withholds — exactly as it should when it has no valid map.

## What was measured

Three salt families, fresh items, both agents, all in one deterministic
binary:

| Arm | Salt | Genuine combiner | Affine memorizer |
|---|---|---|---|
| A (affine baseline) | `C1·k + k²` (enacted A2) | 48/48, 120/120, 8/8 | 16/48, 5/120, 0/8 — reproduces Crew E's signature exactly (P0 [0,0,0,8,8,0]; chains (3,4) 3/4) |
| C (quadratic) | `C1·k + C2·k²` | 48/48, 120/120, 8/8 | 4/48, 2/120, 6/8 — zero non-vacuous exploitation |
| **B (cubic)** | `C1·k + C2·k² + C3·k³` | **48/48, 120/120, 8/8** | **4/48, 2/120, 6/8 — zero non-vacuous exploitation** |

The memorizer's arm-B/C hits are exactly the preregistered unavoidable
floor: length-2 probes (two points always admit a straight-line fit) on
droplast/upperfirst, two sorted-train data accidents at indices 312/316,
and P3 withholds on every length≥3 probe (6/8). Gates: G1=0 (no memorized
probe), G2′=0 on arms B/C (zero non-vacuous cross-phase affine systems),
G3=1 (constants correct) — all as preregistered.

## The proof mechanism (plain English)

The memorizer's whole trick is finding one straight-line map
(offset + slope × position) that turns a training token into the probe.
Under the old affine salt, the salt's own curve cancelled out across
phases, leaving a straight line — so the trick worked. Under the cubic
salt, the phase-dependent `k²` and `k³` coefficients leave a genuinely
curved remainder that no straight line can match on 3+ positions. The
memorizer's fitter solves the line from the first two letters and checks
the third — the check fails, always, on arms B/C (G2′=0). The genuine
combiner is unaffected because it never fits anything: it just applies the
rules it was shown, letter by letter, and the salt rides along untouched.

## The degree ladder (red-team confirmation)

A 3-parameter (quadratic-fit) memorizer recovers the **full Crew-E
signature on the quadratic arm C** (P0 [0,0,0,8,8,0], (3,4) 3/4) but
**cannot beat the cubic arm B** (8/48, 4/120, nothing at length≥4, no
other rule). Salt of degree d requires a memorizer of degree ≥ d. The
cubic salt therefore separates the *fixed* 2-parameter affine class —
"provably cannot" is scoped to Crew E's two-parameter class, exactly as
preregistered.

## The boundary, stated honestly

Two limits are permanent and no salt removes them:

1. **The degrees-of-freedom floor.** Two parameters always match two
   points. The red team built the strongest 2-parameter survivor
   (interpolation without the consistency check) and proved by exhaustive
   search over every position pair, probe, and train token that its arm-B
   hits are exactly this floor: correct only where the output has ≤2
   positions (droplast 4/8, upperfirst 2/8, (3,4) 1/4 on length-3), plus
   one sortedness data accident of the preregistered family. Every one of
   these hits also scores on the affine arm — the floor is salt-invariant
   and information-theoretic. The variant pays with total reflexivity
   (P3 0/8 — it can never withhold). This is why K-J3-4(a) fired **by
   letter** (a 2-parameter variant scored (3,4) 1/4 beyond the §7
   accidents) while its **intent** — recovering the exploitation
   signature on arm B — provably failed.
2. **Identity-position rules.** A per-position-delta copier scores
   droplast/upperfirst 8/8 on every arm (red-team confirmed) —
   behaviorally identical to the genuine combiner there. Salt alone
   cannot separate "applies the rule" from "copies the deltas" when the
   rule doesn't move letters; the separation lives in the rules that do
   (reverse/rotleft/dupfirst: copier 0/8, combiner 8/8).

## Bar disposition

| Bar | Result |
|---|---|
| K-J3-1 (non-affine salt kills affine exploitation) | **PASS** — G2′=0, memB/memC match §7 exactly |
| K-J3-2 (affine baseline reproduces Crew E) | **PASS** — memA [0,0,0,8,8,0], (3,4) 3/4, 0/8 P3 |
| K-J3-3 (genuine combiner salt-invariant) | **PASS** — 48/48, 120/120, 8/8 on all three arms |
| K-J3-4(a) (no within-class extension beats arm B) | **TRIGGERED BY LETTER** — 2-param interpolation variant scores (3,4) 1/4, (3,5) 1/4 on arm B; mechanism proven to be the characterized floor, not salt exploitation (exhaustive pair scan; salt-invariant; P3 0/8) |
| K-J3-4(b) (free-delta identity-σ limit) | **PASS** — σ=id clone 8/8 droplast/upperfirst on all arms |
| K-J3-4(c) (combiner white-box clean) | **PASS** — no generator references in probe path |

## Final verdict

**YES — the cubic non-affine salt family separates genuine rule
composition from the fixed affine memorizer.** The memorizer provably
cannot exploit it: every length≥3 cross-phase affine system is
inconsistent (G2′=0), and the red team proved exhaustively that no
2-parameter trick recovers anything beyond the salt-independent
degrees-of-freedom floor. The genuine combiner passes all arms at
48/48, 120/120, 8/8. The refined boundary: "provably cannot" = "cannot
extract any structure from the salt" — the residual is the characterized,
unremovable floor (correct iff #output positions ≤ #fitted positions,
plus data accidents of the known sortedness family), identical on every
salt and exposed by the P3 reflex check.

## Evidence index

- `PREREG_JOB3.md` — frozen prereg (this file's parent commit)
- `affine_test.zag` — the instrument (pure Zag)
- `runs/run1/`, `runs/run2/` — byte-identical run pairs (12 outputs)
- `score_job3.py`, `scored/SCORES_JOB3.md` — 45/45 bar checks
- `redteam/rt_attacks.py`, `redteam/rt_output.txt`,
  `redteam/REDTEAM_REPORT.md` — independent red team, pre-verdict
- `BUILD_LOG.md`, `SHA_MANIFEST.txt` — build/run provenance
