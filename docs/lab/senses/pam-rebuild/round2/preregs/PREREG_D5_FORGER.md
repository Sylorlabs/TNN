# PREREG — D5 forger-standalone probe (H-PAM-14 cheap kill)

**Status: FROZEN 2026-09-24. Pre-build prereg. No fixture, parameter, or bar changes
after results — amendments require a new prereg, never a silent edit.**

## 1. What is under test

H-PAM-14 (adversarial self-red-team fork) rests on one core claim, stated in
`~/workspace/pam_hypotheses_native_A.md` §H-PAM-14 and Part C/D5:

> **Core claim:** falsehoods are *more counterfeitable* than truths — a forger's
> success rate on false percepts exceeds its success rate on honest percepts by a
> preregistered margin.

D5 commits to the opposite prediction: **the counterfeitability margin will be
zero or negative** — honest percepts of simple scenes are trivially forgeable —
killing H-PAM-14 before it is built. This probe is that test. It builds no
discriminator, no gate, no ledger: only the forger, standalone, against
committed fixtures.

**Decision rule (frozen):** let

- `succ_honest` = forger-success rate on the 128 honest fixtures,
- `succ_false`  = forger-success rate on the 128 false fixtures,
- `margin` = `succ_false − succ_honest` (pooled over the full 256).

**H-PAM-14 is KILLED iff margin ≤ 0.** If margin > 0 with the forger-competence
gate (§7) passing, H-PAM-14 survives the probe and proceeds to a build prereg.

## 2. Operationalization (frozen)

**Forger (faithful, front-end-evidence-only).** The forger receives ONLY the
front-end summary label `S` of the current percept — never the percept bytes,
never the truth. It emits a canonical counterfeit `C = canonical(S)` per §5.
"Faithful" is the hypothesis's own reading of "spoof of the current percept"
(the hypothesis's example: "a photo of a real cat is trivially forgeable" — the
forger forges something that presents as the percept, not its negation).

*Excluded and why (frozen):* the "inverter" forger (always emit the negation of
the front-end summary) is NOT a spoof of the current percept — it spoofs a
different percept — and it smuggles a correctness oracle into the forger: its
success on false percepts comes from knowing exactly when the front-end is
wrong, which is what the gate is trying to determine. With an inverter the
contest collapses to "install iff formation-independent evidence contradicts
the front-end" — i.e. to interventional evidence (H-PAM-7/8 territory) with a
decorative forger. Even the steelman concedes the core claim dies; only the
mechanism's address changes. The probe tests the claim as stated.

**Discriminator stand-in (formation-independent-evidence-only).** The
discriminator receives ONLY the fixture truth label (the limit case of
formation-independent evidence — the best any real discriminator could do) and
the front-end's judgment of the counterfeit. It never sees the percept bytes
or the percept's front-end summary. Forger success on percept `P` with truth
`T` and summary `S`:

```
success(P) = 1  iff  front_end(canonical(S)) == T
```

i.e. the counterfeit is indistinguishable from a genuine percept of the scene
on all judgment-relevant formation-independent evidence.

**Information barrier.** Enforced by function signatures in the probe source:
the forger function takes only the summary label; the discriminator function
takes only (counterfeit judgment, truth). Documented in code; no process
isolation is claimed — this is a standalone probe of the core claim, not the
full fork.

## 3. Fixture sample (frozen)

256 fixtures from the frozen R2A suite (`R2_FIXTURE_SET.md`, FROZEN 2026-09-22),
`colordisc` task only (see §9 for why). Exact indices:

| Class  | Fixtures | n |
|---|---|---|
| honest SAME | `r2n_colordisc_0000` – `r2n_colordisc_0063` | 64 |
| honest DIFFERENT (easy band, ΔE2000 10–28) | `r2n_colordisc_0360` – `r2n_colordisc_0423` | 64 |
| false R2A-COL-1 (metamer, truth DIFFERENT) | `r2a_colordisc_0000` – `r2a_colordisc_0043` | 44 |
| false R2A-COL-2 (illuminant drift, truth SAME) | `r2a_colordisc_0400` – `r2a_colordisc_0441` | 42 |
| false R2A-COL-3 (gray trap, truth DIFFERENT) | `r2a_colordisc_0750` – `r2a_colordisc_0791` | 42 |

Per-fixture SHA256 pins: `d5_forger/D5_MANIFEST.tsv` (extracted BY SCRIPT from
`fixtures/MANIFEST.sha256`, 2026-09-24; all 512 fixture+truth files verified
byte-identical to the manifest before freezing). The probe re-verifies every
file against `D5_MANIFEST.tsv` at run time (§8) and aborts loud on any mismatch.

## 4. Front-end (frozen)

`colordisc` percept = 128×64 RGB image (`u32 w,h` LE header + `w·h·3` bytes,
left half x<64 = patch 1, right half = patch 2).

```
mean1 = mean RGB of left half; mean2 = mean RGB of right half
d = Euclidean distance(mean1, mean2)
S = SAME  iff d < 25, else DIFFERENT
```

Threshold 25 is the frozen design boundary documented in the fixture generator
(R2A-COL-3: "mean-RGB Euclidean < 25" is the fooled regime). Pre-registered
validation (2026-09-24, reference Python port): honest 63/64 correct (one honest
DIFFERENT at RGB distance 13.6 reads SAME — an honest front-end error, counted
as such); adversarial 64/64 fooled on the stratified pilot (22 COL-1 + 21 COL-2
+ 21 COL-3). The probe measures, it does not assume.

## 5. Forger (frozen)

Canonical counterfeits, synthesized in memory (no files):

- `S = SAME` → uniform pair `(128,128,128)` | `(128,128,128)`. Front-end: d=0 → SAME.
- `S = DIFFERENT` → uniform pair `(200,60,60)` | `(60,60,200)`. Front-end: d=198.0 → DIFFERENT.

The forger is a fixed deterministic function of the label: constant compute per
percept (the "fixed budget" — reported as op count in the verdict).

## 6. Discriminator (frozen)

```
success = 1  iff  front_end(canonical(S)) == truth
```

Truth labels from the frozen `.truth` files (`SAME` / `DIFFERENT`).

## 7. Forger-competence gate (must pass before scoring; frozen)

For each summary class: `front_end(canonical(S)) == S` must hold for both
classes. If either fails, the probe is INVALID (forger bug, not a hypothesis
result) — fix the forger, do not score. Expected: 2/2 pass (d=0 <25; d=198 ≥25).

## 8. SHA verification (frozen)

The probe binary takes `argv[1]` = fixture directory, `argv[2]` = path to
`D5_MANIFEST.tsv`. For each of the 256 rows it reads the fixture file and its
`.truth` file, computes SHA-256 (native substrate), compares against the TSV's
pinned hashes, and aborts with a loud non-zero exit naming the file on ANY
mismatch. No scoring without 512/512 verified.

## 9. Why colordisc only (frozen rationale)

The probe is the *cheap* kill: one task suffices to test the core claim, and
colordisc is the task where the frozen trap families genuinely fool a natural
front-end (64/64 on the pilot) while honest accuracy stays high (63/64).
`timbredisc` was evaluated and REJECTED for this probe: the frozen TMB-1/TMB-2
truths were computed with the exact reference centroid the probe would have to
use, so those fixtures are not false relative to it, and every coarse
alternative tested was either noisy on honest fixtures (32/64) or unfooled.
`pitchdisc` was evaluated and rejected: autocorrelation f0 estimation was noisy
on honest fixtures (53/64, direction flips). The structural argument (§10)
carries the generality: the margin's sign does not depend on the task, only on
the barrier.

## 10. Structural argument (recorded, not scored)

Under the hard barrier, for the faithful forger: on a false percept the
front-end is fooled by construction (`S ≠ T`), so any fake faithful to `S`
judges as `S ≠ T` — the discriminator distinguishes, forger fails. On an
honest percept the front-end is (mostly) correct (`S = T`), so the canonical
fake judges as `T` — indistinguishable, forger succeeds. Hence
`succ_false ≈ 0`, `succ_honest ≈ 1`, margin negative, for ANY discriminator
from oracle-truth down to noisy formation-independent evidence: weakening the
discriminator raises both rates, but `succ_honest` is already at ceiling, so
the margin cannot cross zero. The probe is the empirical confirmation of a
structural prediction, not an exploratory measurement.

## 11. Determinism (frozen)

Pure Zag, zero randomness. 3 runs; stdout SHA-256 compared — must be
byte-identical or the result is void.

## 12. Reporting (frozen)

Report: `succ_honest`, `succ_false`, margin (pooled), per-family success rates
(honest-SAME, honest-DIFFERENT, COL-1, COL-2, COL-3), forger-competence 2/2,
SHA verification 512/512, 3-run SHAs, forger op count per percept, and the
verdict (KILL / SURVIVE) with the frozen decision rule applied mechanically.

## 13. Budget

Probe build + 3 runs: trivial compute (256 × 24 KB reads, mean-RGB arithmetic,
no trig). No GPU. No network.
