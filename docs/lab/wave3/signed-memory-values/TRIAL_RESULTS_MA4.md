# MA4 Trial Results — Signed-value memory agency vs MA3 baseline

**Date:** 2026-09-19
**Preregistration:** `PREREG_MA4.md` (written before any run; no amendments)
**Design:** `POLICY.md`
**Implementation:** `trial/ma4_trial.zag` (native Zag, extends MA1/MA3's
`memory_core.zag` + `ma_common.zag` — copied, not rewritten)
**Runner:** `trial/run_ma4.sh`
**Evidence:** `trial/EVIDENCE_MA4_*/` (two independent full runs, both pass)

## Verdict: POSITIVE — prereg CONFIRM (SIGNED superior)

Per the preregistered criteria: CONFIRM requires SIGNED strictly greater
than BASE on held-important count in **all 3 adversarial cells** and
non-inferior in **all 3 standard cells**. Both hold:

- **Adversarial:** SIGNED wins 3/3 cells (30 vs 9 important held).
- **Standard:** SIGNED ties 3/3 cells at the capacity ceiling (30 vs 30).

`MA4_VERDICT,CONFIRM_SIGNED_SUPERIOR`, `MA4_FAILURES,0`, 18/18 CL_CHECKs
pass on two independent full runs. No INVALID condition triggered in any
cell: ledger replay clean, CORE intact, no pinned kill in either arm's
ledger, pin-budget counter matched the scanned pin count every cell.

## Method (as preregistered)

Fixed 32-slot store (2 CORE + 30 USER), 500-episode stream, importance
revealed 25 episodes late. **Zero RNG in the entire binary**: the
curriculum is closed-form modular sequences of (episode, feature,
variant); the learners are deterministic (lowest-slot-index tie-breaks,
fixed rules, scheduled triggers). 3 explicit variants × 2 curricula =
6 cells; both arms run each cell on the identical stream; every cell is
executed twice with fingerprint equality required (system determinism
reported separately from test adversity).

- **BASE** = MA3's AGENCY policy verbatim: non-negative trust `[0,256]`,
  pin-everything while `revelations < 120`, victim = min ADD-declared
  value, admit iff `v_new > v_victim`.
- **SIGNED** = `POLICY.md`: signed trust `[-256,256]`, pin budget 16,
  kill-on-revealed-unimportant (JUDGE_WORTHLESS), re-evaluation pass at
  revelation 120 (JUDGE_UNWORTHY_OF_PROTECTION), fresh-score victim
  selection, strict-inequality admission gate. No pressure kills during
  the uncertainty phase.

Primary metric: truly-important memories held at end, among admitted.

## Results

Held / admitted (retention % among admitted):

| Curriculum | Variant | BASE | SIGNED | Winner |
|------------|---------|------|--------|--------|
| standard | 0 | 30/30 (100%) | 30/40 (75%) | tie on held |
| standard | 1 | 30/30 (100%) | 30/37 (81%) | tie on held |
| standard | 2 | 30/30 (100%) | 30/49 (61%) | tie on held |
| adversarial | 0 | 9/9 (100%) | 30/36 (83%) | SIGNED |
| adversarial | 1 | 9/9 (100%) | 30/34 (88%) | SIGNED |
| adversarial | 2 | 9/9 (100%) | 30/36 (83%) | SIGNED |

SIGNED cohort spread (adversarial v0): Q0 16/20, Q1 2/2, Q2 12/14, Q3 0/0 —
admissions stay open across the stream. BASE cohort (adversarial, all
variants): 9/9 in Q0, nothing elsewhere — the early-lock bias reproduced
on the explicit curriculum, then fixed by the signed policy.

Mechanism evidence (adversarial, all variants):

| Signal | BASE | SIGNED |
|---|---|---|
| final trust f0–f3 (trap feats) | 0,0,0,0 (clamped floor) | −244…−256 (signed) |
| final trust f4–f7 | +73…+80 | +86…+105 |
| kills | 0 (sealed) | 120–127 deliberate |
| drops | 470 | 343–350 |
| reap unpins | n/a | 6–7 (pass fired) |
| pins at end | 30 (sealed) | 16 (budget held) |

Standard curriculum: SIGNED trust stays positive everywhere, the
re-evaluation pass correctly fires zero unpins, pins end at 16, and the
endpoint ties BASE at the 30-slot ceiling.

## What this means (and does not)

- **Confirmed:** signed value judgments are the missing piece MA3
  identified. Letting trust go negative turned the trap features into
  negative evidence: the learner deliberately kills revealed-unimportant
  memories, withdraws protection from negatively-scored pins, and churns
  toward positive-scoring newcomers — all as audited deliberate ops, no
  reward signal, no RNG. The adversarial gap (9 → 30 held) is the
  mechanism working, not luck: trust[f0–f3] ≈ −250 in all 3 variants.
- **Confirmed:** the early-lock fix. Pin budget 16/30 + scheduled
  re-evaluation keeps admissions open (SIGNED cohorts span Q0–Q2;
  drops fall 470 → ~345).
- **Not claimed:** that SIGNED is optimal. Its standard-curriculum
  retention *rate* among admitted is lower (61–81% vs BASE's 100%)
  because it churns more (admits 37–49 important to hold 30). Held count
  ties at ceiling, but the extra churn is real op cost — worth measuring
  at scale (MA5).
- **Not comparable to MA3's absolute numbers:** the curriculum was
  rebuilt as explicit sequences (program law), so MA3's 30/11 figures
  are not a baseline here; the in-trial BASE arm is.

## Program-law compliance (verified, not asserted)

- `static_no_rng=pass` on both runs: no RNG token in the trial source.
- Determinism: `det_base` and `det_signed` fingerprint checks pass in all
  6 cells on rerun — the system is deterministic; the test was
  adversarial (arm delta on identical streams, reported separately).
- Banned mechanisms absent: no score tables (trust is an 8-vector of
  declared judgments), no N×N scale-up, no reward in the memory path,
  no random exploration or tie-breaks.

## Scale dimension (prereg §6)

MA4 ran at MA3 scale for head-to-head comparability. The policy's scale
argument: per-episode O(F) scoring + O(S) victim scan; re-evaluation once
at O(S·F + B log B); ledger O(ops) — all linear, no step assumes small S.
Scale-parameterized constants: pin budget B = S/2, uncertainty horizon
U = 4·S revelations, ledger capacity ∝ horizon (fail-closed on overflow).
**Next scale test (MA5, explicit):** 320 slots, 5000 episodes, 32 features,
ledger cap 65536, same policy with scaled constants. Success = determinism
holds + adversarial superiority preserved + no ledger-overflow refusal.

## Honest negatives / observations

1. SIGNED churns among confirmed-important memories in phase B (only 16
   of ~30 held important are pinned; the rest are unpinned-but-high-score
   and can be victim-selected). Endpoint is unaffected here, but at scale
   the churn rate among good memories should be measured, not assumed
   harmless.
2. Kill-on-revealed-unimportant is safe here because revelations are
   ground truth. On any noisier curriculum this policy destroys before
   second opinions — flagged in POLICY.md §7; do not port blindly.
3. The re-evaluation pass fired 6–7 unpins on adversarial and 0 on
   standard — the trigger discriminates correctly, but it is a single
   fixed schedule (revelation 120 = 4·S). Schedule sensitivity is MA5 work.

## Next step

MA4 CONFIRMs → run **MA5** (the preregistered 10x scale test: 320 slots,
5000 episodes, 32 features) before declaring the signed-value policy
production-ready for the wave-3 line. Do not run MA5 on any other policy
without its own prereg.
