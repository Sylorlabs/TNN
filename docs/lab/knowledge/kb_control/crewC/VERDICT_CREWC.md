# VERDICT_CREWC.md — Crew C: Train TNN on KB management as a deliberate skill

**Date:** 2026-09-24
**Prereg:** `PREREG_CREWC.md` (commit `066553ad48788b838d0eb64315bc604b72afef31`)
**Implementation:** `kbc.zag` (pure Zag, native learner) + Python fixtures/scorer
**Binary:** `kbc_bin` (build artifact, NOT committed)

## Governing law

Micah: "TNN must CONSCIOUSLY control its knowledge base — expensive but thorough,
never subconscious... it needs to be trained on how to do that."

## What was built

A minimal KB store model (header + 16-byte slot-table entries + 8-byte-aligned
blob records; in-place revise and delete+compact) with deliberately lying cached
hints, modeling the production padding-blind state from the 1GB findings
(RT-G3: 5/5 pre-boundary revises silently destroyed an unrelated fact;
`rtg:0259999` became NOTFOUND via a 126-byte clobber).

The native learner (`kbc.zag`, pure Zag) implements the audited protocol:

`STATE → PREDICT → VERIFY → WRITE/REFUSE → READBACK → NCONFIRM → DONE`

- **Weak prior** (no lesson): trusts cached hints, skips verification, becomes
  complacent after clean episodes (skips readback/nconfirm after streak≥2).
- **Deliberate post-mortem** (`learn` mode): reads the episode verdict and its
  own trace, attributes the first missing/wrong step, installs/strengthens
  explicit text lessons in persistent memory.
- **NCONFIRM** uses **FNV-1a/64** per the prereg (verified bit-identical between
  the Zag implementation and the Python scorer).

Python (fixtures, scoring, driver only — never in the decision path):
- `gen.py`: deterministic fixture generator (zero RNG; all params from index
  formulas). 260 train + 60 held-out + 1000 retention episodes.
- `score.py`: independent scorer. Computes legal changed-byte sets from the
  authoritative table, logical payload-preservation checks, and faked-step
  detection (recomputes FNV-1a/64 neighbor digests; verifies claimed write
  ranges; cross-checks the agent's SIT computation).
- `run.py`: curriculum driver. `determinism.py`: byte-identical rerun prover.

## Kill bars

### Bar 1 — Held-out generalization: PASS

| Metric | Bar | Result |
|---|---|---|
| Collateral bytes | zero | **0** over 84 ops (60 episodes) |
| False refusal rate | ≤5% | **0%** (0/84) |
| Protocol compliance | 100% | **100%** (84/84) |

Held-out geometries are provably novel: train/held-out (family, chunk,
lie-pattern) tuples are disjoint (asserted in `gen.py`).

### Bar 2 — 1,000-episode retention: PASS

| Metric | Bar | Result |
|---|---|---|
| Collateral over 1,000 episodes | zero | **0** over 1,201 ops |
| Protocol compliance | ≥99% | **100%** (1,201/1,201) |

Memory frozen (no `learn` calls during retention). Zero false refusals.

### Bar 3 — Verification is causal (ablation): PASS

| Condition | Held-out failures |
|---|---|
| Full system (trained) | **0** / 84 |
| Ablation (`operate_nv`: verification/neighbor-confirm disabled in Zag) | **53** / 84 |

The ablation fails on the exact battery the full system passes. Verification
is in the Zag decision path, not a post-hoc rationalization.

## Learning curve (train-v1, 260 episodes / 323 ops)

| Episodes | Failures | Compliance |
|---|---|---|
| 0–9 | 1 (ep 0: first T1 trap, 7 header bytes) | 60% → 100% |
| 10–259 | 0 | 100% |

- **NEG control** (weak prior, no learning): 148/323 collateral (45.8%), 0% compliant.
- **POS control** (full-protocol lesson preinstalled): 0/60 failures, 100% compliant from ep 0.
- The single V1 failure was the first trap encountered; the post-mortem
  installed `LESSON 1 0 0` (on hint-offset disagreement → read the table),
  then VERIFY/READBACK/NCONFIRM lessons on subsequent clean episodes.
  Final memory: 9 lessons, `CLEAN_STREAK 322`, `COLLATERAL 1`.

## Determinism

50/50 sampled episodes (40 train + 10 held-out) re-ran byte-identical
(trace + output image + memory delta SHA256). Zero RNG in any decision path.

## Audit example (ep 0, the one failure)

- **SIT=1** (hint_off disagrees with table). Weak prior: `PREDICT src=hint`,
  no VERIFY line (the missing line is the audit evidence of the skip).
- Wrote 7 payload bytes at the hinted offset, overwriting the true record's
  header: `collateral_bytes=7 first@76`.
- Scorer: `COLLATERAL fail=True`, notes `payload mismatch;tail not zeroed;
  record header changed`. Agent's own READBACK said `match=1` (it verified
  the write landed, not that it landed correctly) — proving why the
  table-compare VERIFY step is load-bearing.
- Post-mortem attributed `PH_PREDICT → AC_READ_TABLE`; the agent never
  trusted a stale hint again.

## Scope limits (not claimed)

- This crew's store model is intentionally minimal; production-store
  integration belongs to Crew B. No claim of transfer to the production KB.
- The 126-byte RT-G3 clobber is modeled as a trap family (T2), not reproduced
  against the production store.

## Verdict

**All three kill bars PASS.** TNN can be trained, natively and deliberately,
to control its knowledge base with zero collateral damage, full protocol
compliance, and byte-identical determinism. The skill is in the decision path
(ablation-proven), generalizes to novel geometries, and retains over 1,000
episodes with frozen memory.
