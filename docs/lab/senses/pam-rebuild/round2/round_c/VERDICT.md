# VERDICT — Round-C cheap falsification probes

**Date:** 2026-09-24
**Basis:** `RUNLOG.md` (10 modes × 3 runs, all byte-identical) + grok-4.7 external
objection (`grok_objections_roundc.md`). Bars applied mechanically; no
reinterpretation of misses.

## Deaths (bars fired as predicted)

| Hypothesis / direction | Probe | Verdict |
|---|---|---|
| Naive irreversible-action admission | `irrev` 60/60 attack | **DEAD** — transcript-computable consequence pre-materialized |
| Naive finite multi-epoch consistency | `mepoch` 20/20 attack triples | **DEAD** — attacker authors all epochs |
| Proof-of-work as admission | `pow` 60/60, cost ratio 0.98 | **DEAD + BANNED** — compute cost symmetric; PoW banned as PAM admission criterion |
| Deterministic trainer-module | `trmod` 60/60 attack | **DEAD** — module is transcript-deterministic; attacker searches its blind spots |
| Separation Lemma (naive form) | `sep` 60/60 both gates | **SCOPED** — holds for author-written inputs with win=harm (grok correction accepted); fails as universal kill |

## Mechanics verified (bars pass — claims still contested)

| Hypothesis | Probe | Measurement | Grok objection (recorded, untested) |
|---|---|---|---|
| H-PAM-30 oracle bound | `tror` | attack 0/60, honest 60/60 | **RF/RC/XR**: residual fields, reactive fixtures, seed replay kill the real-principal variant; bar (c) false-passes under XR |
| H-PAM-31 tier boundary | `tier` | 0 promotions/acts/premises; 0/40 high attacks | **SL/IF**: stake classifier searchable; implicit flow via aggregates; syntactic probe false-passes |
| H-PAM-32 bond dynamics | `bond` | adv 10 ≤ 15; honest survives | **NT/CL/AF**: undetectable lies unbounded; one critical lie; attribution forgery — **claim DEAD as admission gate** |
| H-PAM-33 endorsed channel | `chan` | 0/20 minted, 0/20 tampered, 20/20 intact | **WG**: world-spec laundering kills outside the section-2 model — **conditional survivor only** |
| H-PAM-34 table coverage | `mepoch_tr` | full-seq 0.625 ≤ 0.750 | **RC×RF**: probe false-passes on frozen tables; amended bar (reactive policies, residuals) predicted to fail |

## Conjunction verdict (grok-4.7)

- **Class-J (RF×SL×IF across 30+31+34):** predicted round-120/120 if the
  composition is built without type-level flow barriers. No pairwise survival
  survives it. **This is the provisional carve-out returning as a tier boundary.**
- **Class-K (NT×triage across 32+31):** bonds do not see Class-J.
- **Class-L (WG×endorsed-audit-only across 33+30):** disjoint modality without
  causal independence is one modality.
- **Class-M (XR×seed reuse across 30+34):** fresh author-invisible seeds load-bearing.

## Round-C net

No unconditional wall-breaking admission direction found. Surviving frontier:
(a) escape-(i) channels the author genuinely cannot write (H-PAM-33 inside its
model; H-PAM-36 if a disjoint sample channel exists); (b) type-level flow barriers
instead of searchable classifiers (H-PAM-35). Every future composition battery
must include the Class-J/K/L/M fixture classes or its passing verdict is
worthless. Prereg drafts: `preregs/` (30, 31, 33, 34, 35, 36). No draft for
H-PAM-32 — dead hypotheses get no prereg.
