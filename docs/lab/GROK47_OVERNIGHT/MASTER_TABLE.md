# GROK47_OVERNIGHT — Master Verdict Table

**Night:** 2026-09-21 → 2026-09-22 PDT · **Loop:** hypothesis → test → red-team → fix → repeat
**Engines:** grok-4.7 (hard down 23:30 PDT, 429 insufficient_credits) → gpt-5.6-sol (timed out 23:46 PDT) → fully native
**Workers:** 7 native sector workers, all complete · **Manifest:** 5,282 items, 4,042 resolved (76.5%)

---

## 1. HEADLINE: teacher showdown — UNRUN

| Leg | Prereg expectation | Outcome |
|---|---|---|
| A (numeric) | 4.7 cannot win; tie at 0.9952/digest `76e85c3e…772b5`, or expose a defect | **UNRUN** — no 4.7 corpus exists |
| B (faithfulness) | 4.7 wins only if E_dump < 7 with 12/12 falsehoods, E_obs=E_prb=0 | **UNRUN** |
| C (prose) | run prose v1 end-to-end if runnable | **UNRUN** |

Not a loss or a tie — an unrun comparison. grok-4.7 became unusable (429 insufficient_credits, $−0.02) before any valid corpus byte was captured; the earlier "truncations" were a `max_tokens:16` tooling artifact (voided). Frozen 4.6 baseline **re-verified natively, byte-identical** (digest `76e85c3e…772b5`; 4.6 corpus: E_dump=7, E_obs=0, E_prb=0, 12/12 falsehoods reproduced; a worker's hand-built truth-map "discrepancy" was its own error, resolved). Leg A build chain + Leg C pipeline validated and ready the moment a valid 4.7 corpus exists. Prereg deviation: gateway 400-rejects `seed` — dropped with log entry, no silent non-determinism. **Needs Micah:** credit top-up; rerun on recovery.

---

## 2. Sector verdicts

| Sector | Hypotheses tested | Verdict | Fix landed | Open question |
|---|---|---|---|---|
| **Teacher** | 19 (8 sol + 11 native-adjudicated) | 2 real bugs (t5_traps T8 `v`-unused — fix recommended; S37 tid-20 counter aliasing), 1 instrument inconsistency (first-vs-last decision), rest latent hardening; **none touch frozen showdown evidence** | none (frozen evidence untouched) | showdown rerun on credit recovery |
| **Memory** | R1–R7, all native byte-identical | R1: pin-kill confirmed; context gate refuted as stated; trust clamp ±256 exact; freeze-leak confirmed. R2: ctx=32 contributes zero; **ctx=31 hangs** (verified timeout). R3: killed-slot reuse leaves replacement recall-invisible. R4: churn replacement non-atomic. R5: equality promotes (vacuous-promotion open). R6: **P0's "fine" kill bar FAILED**; P2 corroborated-revive dominates. R7: **O3 revive dead-end CONFIRMED** (0,0,312) | probe-only: ctx-guard wrapper [0,30]; P2 corroborated-revive proposal; Q1a narrowed O3 refusal — frozen files untouched | R3 detach vs stale-handle? R4 atomicity? R5 vacuous promotion? R6 threshold scaling (own prereg)? R7 dead-end intended? |
| **Reasoning** | TT1 (15/15), RC2/RC3, sweep 35/35 | TT1 **PASSED** byte-identical; **H5b common-mode spoof = documented corruption boundary, no structural defense**. Sweep: self-test/principle-detection/q-partial/rsi all PASS, all kill bars hold | RC2/RC3 trial files + evidence (new) | RC2 ran overnight (was proposed-not-run): 8-failure run then passing — needs Micah's acknowledgment |
| **Language** | R1-* prereg battery (dialogue/code/prose) | Dialogue VERDICT.md **STALE** (birth-year fix never rebuilt; rebuild scores 370/370, new digest `35aaae8a…`); `coding/src/learner.zag` differs from frozen T3 binary (patch_brace fix); C-H1 pilot 12/12 | patch_brace fix verified; CODING_REPORT.md + prose-v2 VERDICT.md annotated (CORRECTION 2026-09-22) | dialogue re-freeze at 370/370 or amend; T3 pin-or-refreeze |
| **Representation** | B-T1 re-attack (H1/H2/H3 + red-team #1) | Binding B-T1 **FAIL stands** but **artifact-driven** (XOR-collision relocations, L=7 annihilator, empty-vocab zeroing) — not unit-driven; H3 refuted by own kill bar (_64 0.9961 top, raw_micro 0.7884 last). Scale: S2 flaw-coverage sustained + caught gap (`scale_learner.zag:954` probes [0,n/4) only; scale-up VERDICT lacks honest-fail annotation); S3b "decorative params" refuted | none (bars bind) | B-T1 probe amendment (strengthened case); 2nd 6.58M rep |
| **Senses** | info-source verdict HTRF (sol red-team → native adjudication) | Headline numbers spot-verified; attack #2 **SUSTAINED as headline-reframing**: R0→R2 confounds information with gating policy; GK2-8 proves the sense has zero truth discrimination | none | IS-R3 arm (R0 install + search; crew prereg before build) |
| **Imagination** | v2 verdict, sine-LUT mandate, blindness, audio staleness | **H1 NOT SUPPORTED, H0 survives** (verify_v2.py inoperable as shipped; reran own M1/M2: FAIL/FAIL/PASS). Sine-LUT attack **SUSTAINED**. Blindness failures **SUSTAINED** (M3f labels+key; Q4 footer key). Audio stale (B1/B2). H2-SUPPORTED already excluded; max H2-PARTIAL | 12 corrections filed in verdict sheet | packets re-render + re-blind before binding ratings; who authorized sine-LUT reinterpretation? (structural); exposure manipulation after H0? |

---

## 3. Fallback usage (logged in FALLBACK_LOG.md)

| Time | Event |
|---|---|
| 23:16–23:25 PDT | ~50–90-byte "truncations" → diagnosed as **tooling artifact** (stock `chat.py` `max_tokens:16`); all such outputs VOID; wrapper `~/workspace/grok47/senses/grokchat.py` issued |
| 23:30 PDT | grok-4.7 **hard down**: 429 insufficient_credits ($−0.02) → substantive generation to gpt-5.6-sol / native |
| 23:34 PDT | all 7 workers notified; hourly re-probe moved to coordinator cron |
| 23:46 PDT | gpt-5.6-sol **timing out** (parent-verified) → fully native mode; "do what you can when you can" |
| ongoing | `grok47-recovery-probe` cron checks both APIs hourly (one retry each); pages loudly on recovery |

Zero batches voided across all 7 workers (nothing technical rested on voided outputs; sol's one variant-confusion caught and re-adjudicated natively).

---

## 4. Manifest coverage

| Tier | Total | Resolved | In-progress | Pending |
|---|---|---|---|---|
| P0 | 2,894 | 2,202 (76.1%) | 1 | 691 |
| P1 | 2,221 | 1,768 (79.6%) | 0 | 453 |
| P2 | 129 | 54 (41.9%) | 39 | 36 |
| P3 | 38 | 18 (47.4%) | 0 | 20 |
| **Total** | **5,282** | **4,042 (76.5%)** | **40** | **1,200** |

All pending items are coordinator-mapped (new overnight files + review-only sibling-track docs). Per-sector ITEMS_DONE.tsv merged into MANIFEST_ITEMS.tsv with zero conflicts. No-RNG screen over 351 P0 `.zag` sources: 17 hits, all adjudicated clean. Few-shot N=1: byte-identical.

---

## 5. Needs Micah's word (external / governance / signature)

1. grok-4.7 credit top-up (then: showdown rerun).
2. B-T1 probe amendment (case strengthened tonight).
3. Frozen-prereg amendments: K17/K18/K19, N9/N14/N15, strength-trial rulings 3–5, integrity-doc sign-off, C3 (conditional inverse re-binning), RC2 overnight run acknowledgment.
4. Sine-LUT reinterpretation authorization (structural); Arm C stays parked (gate amendment unsigned).
5. IS-R3 arm prereg; sine-LUT phase-3 head-to-head; dialogue re-freeze; packets re-render/re-blind.

Full detail: `PENDING_FOR_MORNING.md` · Error ledger: `MASTER_ERROR_LEDGER.md` (120 rows, nothing never-corrected).
