# Grow-with-me Phase 2 — VOID REPORT

**Date:** 2026-09-27 (evening PDT)
**Frozen prereg:** commit `6e15c93144` (unchanged, still binding)
**Verdict:** **VOID** per prereg §5 (validity gates C1/C2 unmet after complete good-faith debugging)
**Hypotheses H1–H7:** UNTESTED (not killed — "VOID the run, not a kill")

---

## Plain-English summary

We built the learning-companion trial exactly as the frozen prereg specified: three
versions of the agent (deliberative, naive hoarder, ablation) taught 120 facts over
six sessions, then tested on 151 sealed questions. Before the real test, the prereg
requires a calibration check: each agent must immediately recall what it was JUST
taught, at 95%+ (deliberative) or 90%+ (naive) per session. If the agent can't
remember what it learned five minutes ago, nothing measured later means anything.

**The agents failed calibration.** The deliberative agent scored 78–100% per session
(needed 95%+ every session); the naive agent scored 78–100% (needed 90%+). We then
fixed every bug we could find — nine genuine defects, including a broken keyword
registry, a wrong session-consolidation rule that was merging PENDING items, and a
mis-ordered probe — re-ran everything from clean builds, and **the scores did not
move at all.** The failures are not bugs; they are a capability ceiling in the
retrieval machinery.

**Per the frozen prereg, the run is VOID.** No hypothesis verdicts (H1–H7) are
claimed. The hypotheses are untested, not disproven.

---

## Calibration results (final, post-fix, frozen keys)

| Session | Deliberative (bar ≥0.95) | Naive (bar ≥0.90) |
|---|---|---|
| S1 | 0.889 (16/18) ✗ | 0.889 (16/18) ✗ |
| S2 | 0.889 (16/18) ✗ | 0.889 (16/18) ✗ |
| S3 | 0.889 (16/18) ✗ | 0.889 (16/18) ✗ |
| S4 | 1.000 (18/18) ✓ | 1.000 (18/18) ✓ |
| S5 | 0.944 (17/18) ✗ | 0.944 (17/18) ✓ |
| S6 | 0.778 (14/18) ✗ | 0.778 (14/18) ✗ |

**C1: FAIL. C2: FAIL. → VOID per prereg §5.**

Determinism: PASS (all arms byte-identical across reruns).
Information barrier: PASS (verified, with negative control).
Store sizes: D=10 records, N=108, A=108 (D ≤ 0.5×N satisfied structurally).

---

## Root cause (white-box, verified)

Every miss is a **taught near-neighbor outranking the key's fact** in keyword-overlap
retrieval. Two patterns:

1. **Vocabulary mismatch.** Teaching says "void fn"; a probe asks about a "void
   function". The retriever does not know "fn" and "function" are the same concept,
   so it returns an unrelated fact that happens to share more keywords.
2. **Similar-fact confusion.** The probe asks for a precise definition; the
   retriever returns a related general fact that shares more keywords (e.g. general
   strength-tier visibility instead of the full tier definitions; a general
   audit-ledger description instead of "append-only").

Critically: the D and N arms produce **identical miss sets**, and scores were
**identical before and after five behavior-changing bug fixes**. The full scoring
path (tokenizer, merge-join, allocators, keyword offsets) was independently audited
and is correct and deterministic. Intake is complete (108 facts, 6 corrections
applied, 6 PENDING held, 6 falsehoods flagged, 3 contradiction entries). This is a
retrieval-ranking ceiling, not a defect.

Fixing it requires synonym handling or a better ranking algorithm — i.e. exactly
the capability engineering the prereg's anti-tuning rule forbids once probes are
known. The implementers have seen the probes; any such improvement is tainted.
Hence VOID, honestly.

---

## Bugs fixed during good-faith debugging (9)

All genuine defects; no capability changes; diff attested bug-fix-only in BUILD.md §3.

1. CS registry slot layout: `cs_add` wrote kw_off/kw_n to slots 16/20; `reg_kw`
   reads 20/24. Contradiction entries were unreadable. Fixed.
2. Forward reference (`answer_question` → later `trace_emit`): reordered.
   Programmatic audit: 132 functions, 0 violations.
3. Six `\u2014` literals rendered as "u2014" → ASCII `--`.
4. Snapshot schema: added `ver=1`; fixed S7 session label.
5. **Session consolidation tested `tagk==0||tagk==4` (4=PENDING) instead of
   `tagk==0||tagk==2` (2=DEPB)** — the D arm was consolidating PENDING items.
   Fixed; D store 16→10 records. (A G4-relevant defect, caught before scoring.)
6. Arm selection factored into `arm_from_arg()` in the agent core.
7. `dependency_pre_S4.q` was administered after S4; moved to pre-S4 per prereg §4.3.
8. Barrier verifier was overbroad; repaired with negative control → BARRIER OK.
9. Round-4 provenance header corrected: per-mechanism honest table
   (adapted / analogous / not present) replacing the blanket "reused" claim.

---

## Observation (not a verdict)

The D arm consolidated 108 taught facts to **10 records** vs the naive arm's 108,
with **identical recall** (identical miss sets on every session). The retrieval
weakness is constant across arms, so the D-vs-N comparison is structurally fair —
this is the H2 signal, and it is strong. **But per the frozen prereg the run is
VOID, so no H2 verdict is claimed.** This observation is reported for Micah's
consideration of a prereg amendment, not as a result.

---

## What would unblock a re-run (needs Micah — prereg amendments)

1. **Retrieval repair as a separate work item.** Build a better retriever
   (synonym handling, discriminative ranking) WITHOUT probe access — fresh crew,
   probes re-sealed — then re-run the frozen trial.
2. **Or amend C1/C2.** If Micah judges the current bars too strict for the
   implementation's stage, the bars can be lowered by signed amendment.
3. **Or amend §5 gating.** Carve out comparative hypotheses (H2's D-vs-N) from the
   absolute calibration gates, on the argument that constant retrieval weakness
   preserves comparative validity.

None of these are enacted. The prereg stands as frozen.

---

## Evidence committed

- `BUILD.md` — full build/fix record, bug ledger, no-capability attestation
- `MANIFEST_SHA256.txt` — 356 files, `sha256sum -c` clean
- `runs/fixed/{D,N,A}_run{1,2}/` — canonical post-fix outputs (incl. voided S7 battery)
- `out/` — pre-fix baseline (build crew)
- `src/` — companion.zag, runner.zag, tools
- `VOID_REPORT.md` — this file
- `RUNLOG_PHASE2.md` — coordinator run log (in workdir)

Binary: `7a3ea375…` (toolchain `498abcb5…` verified). Caches and debug drivers removed.
