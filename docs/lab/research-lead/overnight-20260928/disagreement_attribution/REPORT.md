# DISAGREEMENT-ATTRIBUTION: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/disagreement_attribution/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (12/12 kill bars)**

## Summary

Addresses INTEGRATION-COMBINED gap F4 ("Trigger-B can't attribute binding-caused vs coverage-caused disagreement") with a learner-owned disagreement-attribution probe (`attr_probe` in da_learn.zag) evaluated on purpose-built collision worlds. The probe attributes each learner/oracle disagreement to BINDING (wrong plan family selected) vs COVERAGE (stale/wrong learned spec) using per-need evidence tests that run before the healing path, and emits machine-checkable ATTR lines with evidence flags. It scores **16/16** correct attributions with evsig=16 (every correct attribution carries the expected evidence signature), while a null probe that always guesses BIND scores **8/16** with evsig=0, satisfying the discrimination bars. All binaries are pure Zag, safebin-built, and 3/3 byte-identical.

## Design (frozen in PREREG.md, commit f26d4fe46)

- **Collision worlds:** 16 trials, fresh learner+spec per trial. Kinds: 0 (t0-3, BIND, RET-bound tag reused on COUNT-shaped need); 1 (t4-7, BIND, COUNT-bound tag reused on RET-shaped need); 2 (t8-10, COV-RET, drift A->A2 permutation); 3 (t11-13, COV-VFY, drift A->A2); 4 (t14-15, COV-CNT, drift A->A3 deletion world). CLEAN stage (q0-3) agrees first-try; probe never fires.
- **Probe:** On learner!=oracle with spec versions in use (vbuf 2/3/5), before `note_answer_disagree` (healing untouched). Per spec-using plan step: E_bind = fresh `try_family` trials vs executing fam F plus read-only `bind_fam` vs F (bindbad if tf[F]==0 or live!=F); E_cov = learned spec vs generic re-run on identical inputs (refusal or divergence = coverage-bad). Attribution: BIND if any bindbad (precedence), else COV if any coverage-bad, else IND. Emits `ATTR trial=<t> cause=BIND|COV|IND evb=<0/1> evc=<0/1> nspec=<k>`; telemetry S931=cause, S934=evb, S935=evc, S933=first cause, S936=latch, S930=trial id; ATTR-MISMATCH if cause flips across retries.
- **Null control:** `attr_probe_null` (pmod=1) always emits BIND with evb=0, evc=0, null=1.

## Kill bar adjudication

| Bar | Frozen requirement | Result |
|-----|-------------------|--------|
| K1 | Prereg commit strictly precedes implementation | PASS. Prereg (PREREG.md + NAMECHECK.md) committed alone as f26d4fe46; implementation committed after (see below). |
| K2 | Toolchain guard (safebin, no python) | PASS. PATH=/home/hatch/safebin; which python3/python empty; znc 2026.07.0-dev; pinned compiler used. |
| K3 | Both binaries build, one main each, exit 0, empty stderr | PASS. da_bin and da_nullbin build clean (warnings only); all 6 runs exit 0; all .err files empty. |
| K4 | Exactly 32 ATTR lines, 0 ATTR-MISMATCH, trial>=0 | PASS. 32 ATTR, 0 ATTR-MISMATCH, all trial=0..15. |
| K5 | Real probe SCORE-ATTR correct >=15/16 | PASS. **16/16**, expected 16. |
| K6 | Null probe correct <=9/16, evsig=0 | PASS. **8/16**, evsig=0 (guesses BIND, right only on the 8 BIND trials). |
| K7 | Clean: 4 agree=1, 0 ATTR/RETRY after STAGE CLEAN | PASS. 4 agree=1, 0 ATTR, 0 RETRY. |
| K8 | Bounded: 68 Q, agree=1 count 28, agree=0 count 40, 32 RETRY, exit 0 | PASS. Exactly as specified. |
| K9 | 0 HOOK lines | PASS. |
| K10 | 3/3 byte-identical per binary | PASS. sha256 unique=1 across 3 runs for each binary; build script cmp-verifies. |
| K11 | Zero em/en-dash bytes; zero world literals in da_learn/da_main additions; byte-copies cmp-identical | PASS. No dash bytes; da_main clean; da_learn additions clean (only inherited compose line 1017 has z_alloc(640), identical to cb_learn.zag); da_base.zag and da_module.zag cmp-identical to cb_*. |
| K12 | evsig=16 with (evb=1,evc=0) on BIND, (evb=0,evc=1) on COV | PASS. All 8 BIND trials show evb=1/evc=0; all 8 COV trials show evb=0/evc=1. |

## Sample evidence

- t0 (BIND): `ATTR trial=0 cause=BIND evb=1 evc=0 nspec=1` (x2, attempts 1-2)
- t8 (COV): `ATTR trial=8 cause=COV evb=0 evc=1 nspec=1` (x2)
- t14 (COV-CNT): `ATTR trial=14 cause=COV evb=0 evc=1 nspec=1` (x2)
- null t0/t8: `ATTR trial=0 cause=BIND evb=0 evc=0 nspec=0 null=1` (always BIND, no evidence)

## Deviations and amendments (all pre-execution, kill bars unchanged)

1. **ans_eq fix (deviation):** Reconstructing do_query from cb_main exposed a latent out-of-bounds bug in the carried ans_eq (it walked the flat answer buffer as fixed-size records, misreading object ids as record lengths). Replaced with flat element-wise comparison. Documented in da_main.zag header and PREREG Amendment A1.
2. **Amendment A1 (pre-execution, transparent):** t9 obj 625->622 (no (602,*,625) fact existed, so no disagreement could fire); t14/t15 redesigned after analysis of cnt_spec (see finding 3). Kill bars unchanged.

## Findings

1. **The probe attributes correctly on all 16 collisions.** Binding trials (stale tag->family) yield evb=1/evc=0; coverage trials (drifted world, correct family) yield evb=0/evc=1. Cause is stable across retries (0 ATTR-MISMATCH), and the healing path still converges within 3 attempts (32 RETRY, bounded).
2. **Null control discriminates.** Always-guess-BIND scores 8/16 (chance on this balanced battery) with evsig=0, vs 16/16 with evsig=16 for the real probe. The evidence flags, not the label, carry the discrimination.
3. **cnt_spec and ret_spec are relation-blind at bucketed slots** (they verify the queried subject/object but not the relation id). On drifted worlds the stale buckets count wrong-relation facts. This made kind-4 design subtle: the deletion drift A3 was chosen so the spec and generic genuinely diverge (t14: spec counts surviving (611,603,*) facts at stale slots, returns 2 vs generic 0; t15: stale 603-buckets see only deleted-relation facts, returns 0 vs generic 2). vfy_spec correctly checks all three fields and needed no such care. This fragility is worth a follow-up but is outside this lane's scope.
4. **Trigger B remains blunt on BIND trials** (documented F6 note): it invalidates coverage contracts even when the probe shows the binding was the culprit. The probe gives the learner the information to be selective; the current trigger does not use it.

## Process notes

- Pure Zag throughout; safebin mandatory; no Python invoked (toolchain guard recorded in NAMECHECK.md Step 0 and enforced by da_build.sh).
- A near-miss occurred during debugging: a `python3 -c` one-liner was drafted for output analysis but the worker self-disclosed and aborted before execution (no output produced, no scientific wave affected). The analysis was redone with grep/awk. Recorded here for transparency; the battery results are unaffected (all numbers come from the safebin-built binaries).
- Repro: `da_build.sh` assembles da_full.zag / da_full_null.zag from the da_*.zag sources, builds with the pinned znc, runs each binary 3x, and checks byte-identity. All sources and logs are in this lane directory.

## Verdict

**BUILD-PASS (12/12 kill bars).** The learner-owned attribution probe distinguishes binding-caused from coverage-caused disagreement on purpose-built collision worlds, with evidence signatures that a null guesser cannot fake. INTEGRATION-COMBINED gap F4 is addressed by this follow-up.
