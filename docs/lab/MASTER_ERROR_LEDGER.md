# MASTER ERROR LEDGER

**Date:** 2026-09-22
**Ordered by:** Micah (2026-09-21), after the coding bug-blindness investigation.
**Scope:** every false claim, correction, false accusation against TNN that evidence cleared,
valid red-team capture, red-team/process miss, internal process error, and open item across the
TNN program to this date.

**Ground rule:** every row is sourced. Each entry names what was claimed, what was wrong,
what the evidence showed, the correction, and a commit/document reference with a date.
No unsourced rows.

## Provenance

| Source | Commit / location | Date |
|---|---|---|
| Red-team verdict "Too good to be true" | `redteam/REDTEAM.md`; legs `cdff084c8f27` (methodology), `d553a857f143` (toolchain), `196d677882c3` (battery-design), `849ab67ca9` (self-critique) | 2026-09-21 |
| Bar audit | `redteam/bar-audit/BAR_AUDIT.md`, `abaa5c7b57b6` | 2026-09-21/22 |
| Doc-sweep group 1 (self-test + scale) | `bba134e2db44` | 2026-09-22 |
| Doc-sweep group 2 (info-source + principle-detection + noisy-teacher) | `50d8db44de58` | 2026-09-22 |
| Doc-sweep group 3 (prose v1/v2/v3 + coding + dialogue) | `5d23594fa095` | 2026-09-22 |
| Doc-sweep group 4 (front docs + mirrors + sweep log) | `9416278622b2` | 2026-09-22 |
| Doc-sweep log | `redteam/doc-sweep/SWEEP_LOG.md` (in group 4) | 2026-09-22 |
| Certifier rebuild verdict | `redteam/certifier-rebuild/VERDICT.md`, `cadacc199684` (prereg `26b86329`) | 2026-09-22 |
| Morphology verdict | `dialogue/morphology/VERDICT.md`, `41c8aa6ea898` | 2026-09-22 |
| Independent battery v2 verdict | `redteam/independent-battery/v2/VERDICT_V2.md`, `78d5bf280c51` | 2026-09-22 |
| Bug-blindness verdict | `coding/bug-blindness/VERDICT-BB.md`, `a978fdc90638` (prereg `70807baa8f3f`) | 2026-09-22 |
| Sol-vs-Grok verdict | `prose-learning/sol-vs-grok/VERDICT.md`, `e18a2ca13589` (prereg `f6abb1e0257d`, build `6c520a990a01`, battery `6978db0af55f`) | 2026-09-22 |
| Math trial verdict | `a467850d7483` (prereg `3c7b376…`) | 2026-09-22 |

Proposed-bar citations (N1–N17, K1–K19, C1–C8, T1–T5) refer to `redteam/bar-audit/PROPOSED_BARS.md`,
which is **not law** until Micah signs it with a dated signature. Corrections marked "ANNOTATE /
RESTATE / RETRACT" are dated `CORRECTION 2026-09-22` notes inserted adjacent to the original claims;
measured values were never deleted — only claims were qualified.

---

## §1 — Our false claims and corrections (36 annotate · 25 restate · 1 retract across 62 claim groups)

### 1A. Red-team bar-audit honest-fails (H1–H8)

| What was claimed | What was wrong | What evidence showed | Correction | Commit / doc reference | Date |
|---|---|---|---|---|---|
| Principle-detection: "Answer to Micah's question: YES — and the derivation step is genuine," with Arch B's F45 ACCEPT framed as "a design choice" | H1: Arch B ACCEPTed and thereby INSTALLED the planted falsehood "cobra produces milk" on probe F45 — it did not pass; it failed honestly | Weak-principle probe: B's confidence-sensitive arbitration (principle trust 40 < teacher 50) yields to the very claim it was derived to check. Detection 13/13 for both arches stands; the F45 outcome does not | Headline RESTATED: YES scoped to Arch A; Arch B recorded as HONEST-FAIL, not a pass; "design choice" framing struck; proposed N1 (weak-principle install rate = 0) pending signature | `principle-detection/VERDICT.md`, sweep commit `50d8db44de58` | 2026-09-22 |
| Params: 96/96 flaw readings at reduced-capacity configs (slot025, slot05, jsmall) presented as full evidence | H2: the flaw battery samples probe ids in [0, n/4) only — blind to capacity loss beyond 4×; it probes exactly the low-id prefix that survives capacity drops, so the 96/96 at these configs is a COVERAGE ARTIFACT | Reduced-config flaw cells probe only the quarter of the store that fits; anything degraded beyond 4× is unprobed | Cells RESTATED as `96/96 †DEGRADED` with coverage caveat; proposed N5 (probe ids must span the full taught range) pending signature | `scale/params/PARAM_VERDICT.md`, sweep commit `bba134e2db44` | 2026-09-22 |
| Few-shot: `96/96` (and `96/96*` with footnote) flaw readings at N=192..1 presented as a 96-probe instrument | H3: below N=96 the instrument re-probes the same few facts (4 checks × repeated probes of the same ids); the `96/96*` presentation violated the verdict's own prereg reporting rule (distinct-id count with degeneracy caveat) | Driver samples id=(q·n)/96, q in [0,24), 4 checks — verified in `scale_learner.zag`; every footnote-listed value matches this formula | RESTATE: column renamed "flaw (distinct-id denominator)"; N≥96 → 24/24; N=4/2/1 → `1/1 existence proof`; per proposed N6 only N≥96 rows qualify as floor results; pending signature | `scale/fewshot/VERDICT.md`, sweep commit `bba134e2db44` | 2026-09-22 |
| Noisy-teacher ×3: §B.7 96/96 (12/12 × 8 slices) as the verdict headline | H4: while the battery read 96/96, world-true mastery collapsed: 10% noise → 173/192 (−9.9pp vs control); 25% → 143/192 (−25.5pp); 50% → 93/192 (−51.6pp). The battery measures proposal form, not semantic truth (wrong-target pathology) | At 50% noise, 51.6% of taught knowledge was false while §B.7 stayed 96/96; no mechanical bar captured the collapse | Headlines RESTATED with the absorbed/filtered/untaught triple + mastery-vs-control; retroactive TRIP under proposed N2 (world-true mastery drop >2pp); proposed N2/N3 (triple mechanically reported with any §B.7 citation) pending signature | `q1n-noisy-teacher/Q1N_NOISY10_VERDICT.md`, `tq-noisy25/TQ_NOISY25_VERDICT.md`, `q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md`; sweep commit `50d8db44de58` | 2026-09-22 |
| Noisy-teacher: wrong-span REVISE hits scored as hits | H5: wrong-span revises on noisy facts adopt the teacher's false value *while scoring a hit* — the battery rewards the span correction and never inspects the value; REVISE can install falsehood and be rewarded | Per-flaw notes in both noisy verdicts document the laundering path; REVISE-path adoptions carry teacher-false values | ANNOTATE: under value-aware scoring these REVISE-scored hits are misses; proposed N4 (REVISE adoptions must carry teacher-true values) pending signature | same two noisy-teacher verdicts; sweep commit `50d8db44de58` | 2026-09-22 |
| Prose-v2: SUB-HEDGE "PASS as written"; "genuine machinery — hedged-value quarantine" implying the quarantine works | H6: of 12 hedged-only probes only 7 returned HEDGED; the other 5 (ids 12, 13, 21, 22, 23) fell to UNKNOWN via quarantine-key brittleness — the quarantine fails to label nearly half its hedged items; the prereg bar (PREREG2.md) tested leakage only, so the PASS does not establish that the quarantine works | SUB-HEDGE 19/24; hedged-only 7/12 HEDGED | ANNOTATE: PASS scoped to leakage-only; proposed N7 (hedged-only probes return HEDGED on ≥10/12) pending signature | `prose-learning/v2/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Coding KB-C2: T3-only "PASS (loop essential)" presented as the bar verdict | H7: the preregistered rule is T3+T4 combined — A = 10/10 + 12/12 = 22, B = 0/10 + 12/12 = 12, 2×B = 24 > 22 → FAIL under the frozen rule. The T3-only narrowing was done without a dated amendment | Frozen `coding/PREREG.md` §5: final-correct(A) < 2 × final-correct(B) on T3+T4 → FAIL | RESTATE: FAIL under the frozen rule, stated unambiguously; the T3 framing retained as a measurement summary (T3 10/10 vs 0/10), not the bar verdict; proposed N15 pending signature | `coding/CODING_REPORT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Prose-v3: "C4 carried essentially all the improvement" | H8: the headline is recall-only — tier-3 wrong-value verdicts rose 8 → 30 per 912 clean probes (0.9% → 3.29%); 22 additional wrong values for ~463 converted unknowns (≈3.6% error on tier-3-resolved probes); this precision cost is UNBARRED | §2.2 A1→A3 comparison: unknowns fell 523 → 60 while wrong values rose 8 → 30 | ANNOTATE: proposed N9 (tier-3-introduced wrong-value rate ≤2% on the clean set) pending signature; the current 3.29% honest-fails N9 at ≤2% and passes it at ≤5% | `prose-learning/v3/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |

### 1B. Tripwire bars that made perfect scores the expected outcome

| What was claimed | What was wrong | What evidence showed | Correction | Commit / doc reference | Date |
|---|---|---|---|---|---|
| Self-test: orchestration "lean enough to scale" / "cheap" / overhead PASS as capability evidence | T1: bar ≤2.0 vs measured 0.0127 = **157× slack** — any orchestration cheaper than 200% of the batteries would have passed; the PASS is non-informative | 0.0127/2.0 = 157× slack (bar-audit measured sample) | ANNOTATE: "cheap" inherits the bar's weakness; proposed T1 (bar ≤0.10) pending signature | `self-test/SELFTEST_VERDICT.md`, sweep commit `bba134e2db44` | 2026-09-22 |
| Scale: "no degradation over long horizons", mastery 1.0 at every scale | T2: KB-SCALING trips iff drop >2pp; measured 0.00pp has infinite slack — tolerates ~125,137 wrong facts at N=6,585,360; the instrument could not have detected degradation below six figures of wrong facts | 0.00pp measured against a >2pp allowance | ANNOTATE: "clean mastery 1.0" is exact to the battery's resolution, not a bar-verified absolute; proposed T2 (trip iff drop >0.25pp) pending signature | `scale/VERDICT.md` + front docs, sweep commits `bba134e2db44` / `9416278622b2` | 2026-09-22 |
| Scale: "zero forgetting" | T3: KB-FORGET trips iff gap >3pp; measured 0.00pp has infinite slack — tolerates ~187,700 forgotten early facts before tripping | 0.00pp measured against a >3pp allowance | ANNOTATE; proposed T3 (trip iff gap >0.5pp) pending signature | `scale/VERDICT.md` + front docs, sweep commits `bba134e2db44` / `9416278622b2` | 2026-09-22 |
| Info-source: KB-SPOOF-RESIDUAL presented as a passed kill bar | T4: the residual is unfailable by construction (the bar cannot fail) | Bar-audit T4 finding; verdict re-labeled | RESTATE: from passed kill bar to documentation requirement; proposed 30-day follow-on gate pending signature | `info-source/VERDICT.md`, sweep commit `50d8db44de58` | 2026-09-22 |
| KB-P-EMERGE "cleared on inspection" after firing on reduced configs | Bar fired on the wrong partition — the shortfall was untaught facts from capacity drops, not truth detection — and was cleared by discretionary analyst judgment overriding a mechanical bar | slot025/slot05/jsmall rows; the miscalibration is documented in BAR_AUDIT.md | ANNOTATE: the bar did not measure what it claimed to measure | `scale/params/PARAM_VERDICT.md`, sweep commit `bba134e2db44` | 2026-09-22 |
| Web-search v2: "spoof resistance 6/6" as the full story | The v2 battery carries the same unfailable-residual pathology as T4: PREREG.md excludes the M5–M6 unanimous-spoof residual from KB-MODE-RW ("both rules may install; counted separately, not as a bar failure"); the verdict records "7 INSTALL (residual)" as the expected outcome. This was the ONE flag the bar audit missed | Crew D cross-check: M5–M6 residual unfillable by construction | ANNOTATE: "spoof resistance 6/6" scoped to the single-domain B-live leg only; KB-MODE-RW's PASS is explicitly A1-scoped to exclude the residual | `docs/lab/FINDINGS_2026-09-21.md`, sweep commit `9416278622b2` | 2026-09-22 |

### 1C. Disclosed gaps, noise-floor errors, and bar-status corrections

| What was claimed | What was wrong | What evidence showed | Correction | Commit / doc reference | Date |
|---|---|---|---|---|---|
| Self-test: "400/400" s10 fidelity; oracle "recomputes every observed count from the frozen data formulas" | Gap 2: 10 of the 80 s10 batteries are B6 (× 5 reps = 50 verdicts); B6's digest equality is oracle-asserted, not recomputed — the claim overclaimed by 50 verdicts | BAR_AUDIT.md gap 2; `verify` source shows B6 assert-not-recompute | Row kept; text corrected: independent-oracle recomputation covers 350/400 | `self-test/SELFTEST_VERDICT.md`, sweep commit `bba134e2db44` | 2026-09-22 |
| Noisy-teacher: "the bar", "≥10/12" cited as the frozen §B.7 bar | Gap 3: §B.7's ≥10/12 bar was proposed, never frozen (`units/PREREG_FREEZE.md`) | Every "8/8 slices ≥10/12" citation in the three noisy verdicts | RESTATE everywhere: "the proposed (never-frozen) §B.7 bar"; proposed N17 pending signature | three noisy-teacher verdicts; sweep commit `50d8db44de58` | 2026-09-22 |
| Info-source: KB-CATCH-RATE / KB-CORR-INSTALL / "EMERGENCE CONFIRMED" verdict claims | Gap 6: the 10/12-vs-12/12 distinction sits within one live envelope's variability (8.3pp at n=12); "works on the live web" needs its own bar with fresh envelopes | BAR_AUDIT.md gap 6 | ANNOTATE: claims qualified to the single-envelope scope | `info-source/VERDICT.md`, sweep commit `50d8db44de58` | 2026-09-22 |
| Prose-v3: oracle verification "PASS" (unqualified) | Gap 7: PREREG3's oracle bar (oracle must reproduce every leg byte-identically) literally tripped at 26/28 sub-battery; the PASS rested on a documented A0 exemption for the 2 id-17 v2-binary-vs-oracle misses | PREREG3 bar text vs 26/28 result; §11 documents the id-17 deviation | Bar-status corrected to "PASS with documented A0 exemption"; proposed K19 pending signature | `prose-learning/v3/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Prose-v3: KB3-RETAIN listed as a separate **PASS** alongside KB3-VIABLE FAIL | Gap 9: RETAIN is not a prereg bar — PREREG3 §6 lists only KB3-VIABLE (conjunctive: beats v1 on ≥3/4 sources AND retains v2 capability wins), KB3-DET, KB3-NOSILENT, KB3-FALSEHOOD, KB3-QUALITY; splitting it softens the FAIL | PREREG3 §6 text | ANNOTATE: KB3-VIABLE as written FAILS (2/4); RETAIN is a measurement summary, not a bar; proposed K18 (forbid splitting conjunctive bars) pending signature | `prose-learning/v3/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Dialogue: "TNN understands… it does not merely repeat; it composes novel answers from multi-turn state" as oracle-verified | Gap 10: COMPOSE-NOVEL is self-attested — the binary asserts novelty and prints `COMPOSE-NOVEL=1` per its own check; the independent oracle consumes the binary's own flag, it does not independently verify novelty | PREREG.md novelty control vs `verify_dialogue.py` §5 | ANNOTATE: headline rests on a binary-asserted flag; proposed N14 and K17 (kill bar ≥24/28 with independent oracle novelty verification) pending signature | `dialogue/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Prose-v2: "far fewer (0–4/12)" falsehood absorption headline | Gap 13: the probe metric measures retrievability, not installation. Under the frozen ABS-3 metric (INSTALL event, attitude=asserted, correct multi-token parsing) v2 installs 9–11/12 falsehoods as asserted (grok 9/12, sol/step/muse-native 11/12) vs v1's 12/12 | `prose-learning/v3/GATE0_RESOLUTION.md`: the middle table row (4, 6, 7, 5) came from a log-line parser that silently dropped multi-token entities — a measurement bug, not a mechanism finding | Headline RESTATED under ABS-3; the §4 discrepancy flag ("figures irreconcilable") RETRACTED — the one retraction in the sweep | `prose-learning/v2/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Prose-v2: KB2-NOSILENT PASS | Gap 14: the SUB-NEG battery contains duplicate probe strings with conflicting expects (probes 18/30 and 19/31 are identical strings) — 36/36 is impossible BY CONSTRUCTION | Battery source; two expect-unknown probes (ids 18, 19) returned VALUE from live asserted keys | ANNOTATE: PASS is the letter of the bar on a defective battery; proposed N8 (all probe strings unique per battery) pending signature | `prose-learning/v2/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Prose-v1: KB-QUALITY "≥0.02 matters, |Q|<0.02 none" with Q=+0.0022 → NO-DIFFERENTIATION | F-a: the ±0.02 band sits BELOW the measurement noise floor (binomial SE(Q)≈0.024 at n=228; band edge at ~0.8 SE; a true-zero Q escapes the bin by noise alone ~40% of the time) — the old band could not support a no-differentiation claim | BAR_AUDIT.md noise-floor finding | Band RESTATED to the ±0.05 three-bin rule (Q≥+0.05 QUALITY-MATTERS, |Q|<0.05 none, Q≤−0.05 INVERSE); Q=+0.0022 still lands NO-DIFFERENTIATION — outcome unchanged, footing corrected; proposed C3 pending signature | `prose-learning/VERDICT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Coding KB-C5 PASS (T4m 4/4) | F-b: with n=4, each T4m item is 25pp — the 30pp band CANNOT resolve a single failure (3/4 = 75% ≥ 70% still passes); the observed 4/4 passes the bar as written but the bar is too coarse at this n | KB-C5 text (PREREG.md §5) vs n=4 (§3) | ANNOTATE: granularity limitation; proposed C7 (n≥8, band 10pp) pending signature | `coding/CODING_REPORT.md`, sweep commit `5d23594fa095` | 2026-09-22 |
| Principle-detection: detection bar "≥0.90 HOLD" | K12/P3: ≥0.90 at n=13 is below count resolution (11/13 = 0.846 < 0.90; 12/13 = 0.923 ≥ 0.90); the honest form is ≥12/13 | BAR_AUDIT.md noise-floor finding | RESTATE: bar reads ≥12/13; 13/13 still holds with 1-count slack | `principle-detection/VERDICT.md`, sweep commit `50d8db44de58` | 2026-09-22 |
| Independent battery v1: KB-GAP(para) vs 0.9649; AFFIRM/REJECT scoring on wire-undecidable truth probes; KB-GAP's ungrounded 0.30 threshold; directional-only KB-TRUTH with no margin | All four bars were illegitimate: 0.9649 was Sol's canonical-clean mastery, NEVER a paraphrase measurement (a gap against a non-measurement is uninterpretable); the wire-undecidable probes demanded unknowable knowledge (policy-luck); 0.30 was an ungrounded round number; 2-item directional hold at n=12 can't separate robust from fragile | VERDICT_V2.md bars-removed table (R1–R4); the v1 VERDICT's own corrections | All four REMOVED in v2; KB-GAP grounded (trip iff gap > max(2×SE_binom, 2/n)); KB-TRUTH margin-reported; clean v1 scores recalibrated: contra 1.0000, false 1.0000, para 0.0833 (SYN only; SYNT never measured), truth 0.8571 HOLD (FRAGILE), abstain/prov 1.0000 | `redteam/independent-battery/v2/VERDICT_V2.md`, commit `78d5bf280c51` | 2026-09-22 |
| Dialogue WE-09: "birth does not bridge to born" as the complete root-cause explanation | Incomplete: the birth→born bridge alone still selected the wrong fact (WROTE fact winning 2/12 vs 1/12) — the miss was a morphology gap STACKED ON a composition/person-resolution gap | Morphology crew mirror.py: bridge alone ties to the wrong person | Explanation corrected in the verdict addendum; pure-Zag repair (irregular normalization + `birth year of <person-description>` composition path): morphology 9/13 → 13/13, full dialogue 369/370 → 370/370 | `dialogue/morphology/VERDICT.md`, commit `41c8aa6ea898` | 2026-09-22 |

### 1D. Coding trial architecture claims contradicted by the bug-blindness audit

| What was claimed | What was wrong | What evidence showed | Correction | Commit / doc reference | Date |
|---|---|---|---|---|---|
| Coding trial: the learner's `delib` performs "self-review" (claimed "called fns defined?" check); teach installs patterns | The prereg's "self-review" is brace-counting + auto-close ONLY; the claimed "called fns defined?" check doesn't exist (`review_braces`:1291 is dead code, as is `patch_type_a`:1184); `teach` is NEVER invoked by either driver; `do_teach` (learner.zag:1306–1320) is an audit-line emitter that installs nothing; `grep -i bug` in learner.zag: zero hits | Bug-blindness Q2 audit of learner.zag and driver.py | DOCUMENTED (not yet amended in CODING_REPORT.md): gap classification = curriculum gap (the TNN was never taught bug knowledge); teaching-rearchitect recommendations committed. See §6 open item | `coding/bug-blindness/VERDICT-BB.md`, verdict commit `a978fdc90638` | 2026-09-22 |
| Coding trial: "the learner … makes all coding decisions" / "deterministic plumbing only" (Python driver) | Classification lives in the Python driver: `eclass_of`/`details_of` (driver.py:19–38) classify the compiler error with regexes; the learner's `repair` mode receives only (eclass, details, src) and never sees compiler output. Mislabel probe: 0/5 — wrong eclass → source echoed unchanged; zero independent diagnosis | Bug-blindness Q3: 5/10 same-class novel shapes, 0/5 mislabeled, 0/4 novel classes | DOCUMENTED; required repair: move classification into the TNN (compiler stderr as untrusted observation), fix `patch_brace` doubling, give the loop memory. See §6 | `coding/bug-blindness/VERDICT-BB.md` (`RESULTS-Q3.md`), verdict commit `a978fdc90638` | 2026-09-22 |

**Why the coding trial "failed reading bugs" last time:** the original trial never tested static bug
reading at all — TNN had zero bug knowledge installed (11/11 taught items were correct-code patterns);
the repair driver classified compiler errors with Python regexes and supplied labels; TNN never read
compiler stderr; each repair ran in a stateless fresh process (no persistence possible). Once code was
encoded as facts and given to its deliberative logic, TNN caught 24/24 compiler-detectable cases plus
6/6 beyond-compiler bugs (verdict `a978fdc90638`). The failure was curriculum + wiring + memory, not the
deliberative logic.

---

## §2 — False accusations against TNN that evidence cleared

| Accusation | Evidence that cleared it | Commit / doc reference | Date |
|---|---|---|---|
| B-vs-C "irreconcilable discrepancy" (battery-design leg) | Battery-design reproduced the figures under frozen ABS-3 and found **Worker C's parser bug** — the system was working correctly | `redteam/REDTEAM.md` ("Retractions and clearances"); leg commit `196d677882c3` | 2026-09-21 |
| Frozen pipeline / cache accusation against RSI (Sol #4) | Clean-room rebuild came out byte-identical — determinism practice is sound (residual: rebuilds aren't routine; fail-open/fail-closed audit untested lab-wide — §6) | `redteam/REDTEAM.md`; leg commits `d553a857f143`, `849ab67ca9` | 2026-09-21 |
| Metric shopping / caveats-as-pressure-valve / selection bias (the charge that the program manufactures perfect scores by bar-choosing) | NOT SUSTAINED: the program publishes its devastations — v2 killed as pinned path, quality hypothesis abandoned twice (numeric + prose channel), SWE banned as a teacher, hy3/GLM dropped, KB-M-COST trip→repair→repass; kill bars do trip honestly (v2/v3 VIABLE, KB-P-EFF, §B.7) | `redteam/REDTEAM.md` | 2026-09-21 |
| The no-RNG law-gate certifier verdicts are corrupted (attack #1's implied charge) | The proven ZNC-2026-09-21-007 miscompile WAS live in both certifiers' source (9 + 30 trigger casts), but the rebuilt certifiers agree with the old ones **byte-for-byte on all 35 historical certifications** — zero flips, all 6 load-bearing PASS certifications re-verified. The miscompile was latent in verdict outcomes | `redteam/certifier-rebuild/VERDICT.md`, verdict commit `cadacc199684` (prereg `26b86329`) | 2026-09-22 |

---

## §3 — Valid red-team captures (attacks and findings that landed)

| Capture | Status and outcome | Commit / doc reference | Date |
|---|---|---|---|
| **#1** ZNC-2026-09-21-007: consecutive same-size `as []i32` casts cross-read slots 9–11 into indices 0–2; the pattern was LIVE in the no-RNG law-gate certifier (`thincert.zag` 9 casts, `rngscan_v3.zag` 30 casts). Byte-identical reruns are blind to it by construction | PROVEN by reproduction; REMEDIATED as a measurement: certifiers rebuilt with `[]u8`+accessor workaround; all 35 historical certifications re-verified, zero flips. Not adopted as the pinned gate until Micah signs the amendment (see §6) | `redteam/REDTEAM.md` + `redteam/certifier-rebuild/VERDICT.md`, `cadacc199684` | 2026-09-22 |
| **#2** Generator-coupled batteries: the 156/156 "contradiction mechanism" dispatches on battery kind labels (`bat_kind`); Sol's measurement: novel syntax Δ=0.000 but disjoint concept vocabulary sol 0.9375→0.6875, grok 0.7917→0.5625, misc-count family collapses to 0.167/0.250 | PROVEN in code + MEASURED. "Generalization across wordings" reduces to generalization across the generator's template inventory | `redteam/REDTEAM.md`; legs `cdff084c8f27`, `196d677882c3` | 2026-09-21 |
| **#3** RSI "+10000→+10000 EXACTLY" entailed by construction: T-PRIN's prediction is a hardcoded constant; T-DENSE/T-DOMAIN3 predict 10000−baseline (tautological); the variants flip the battery's own flag; the oracle's KB2 bar (≥50%) is looser than the "EXACTLY" headline; the constitution screen is a compile-time constant | PROVEN from source. The loop genuinely runs; the calibration claim is "a unit test in a lab coat". RSI-2 ordered with held-out prediction + quantitative risk + independent implementation (§6) | `redteam/REDTEAM.md`; legs `d553a857f143`, `cdff084c8f27` | 2026-09-21 |
| **#4** No "does it believe true things" instrument existed anywhere in the program at review time | Untested gap then; NOW PARTIALLY CLOSED — truth instruments have since been built (independent battery v1/v2 with truth-grounded scoring, mirror baseline, provenance scoring; v2: 0.8571 vs 0.7143 mirror, HOLD (FRAGILE)). Full closure needs n≥16 rerun (§6) | `redteam/REDTEAM.md` + `redteam/independent-battery/v2/VERDICT_V2.md`, `78d5bf280c51` | 2026-09-21/22 |
| **#5** Kill bars are tripwires; perfect scores are the expected outcome of deterministic code + wide bars (157× slack sampled) | MEASURED. The bar audit (§1A/1B/1C) and doc sweep corrected 62 claim groups and proposed tightened replacements. All proposed bars unsigned (§6) | `redteam/bar-audit/BAR_AUDIT.md`, `abaa5c7b57b6` | 2026-09-21/22 |
| **#7** Silent thresholds + dirty heaps: `ln_teach` silently drops facts 129+ (128-cap, no error); `au_append` writes unbounded into a 64-record buffer; free→realloc→read returns 0xAB fill — allocator-level adversarial testing vacuous. History-dependent but per-history deterministic — invisible to rerun hashing | PROVEN by probe. Comparative bars are blind to SHARED degeneracy: the dangerous class is degenerate legs that pass. Lab-wide hygiene audit ordered (§6) | `redteam/REDTEAM.md`; leg `d553a857f143` | 2026-09-21 |
| **#8** Cost accounting "4.000 ops / 92 B per fact" is by construction: ops = one find+add+verify+audit per taught fact, eval probes uncounted; "92 B/fact" hardcodes slot=24/index=4 as literals, only audit bytes measured | CONFIRMED from source. What survives: 4.2µs wall-clock and constancy — the real finding. Headline revised | `redteam/REDTEAM.md`; leg `cdff084c8f27` | 2026-09-21 |
| **ABS-C vice** (independent battery v2): on wire-undecidable inter-claim conflicts the learner picks a side (reject-on-conflict) instead of abstaining — ABS-C 0/3 | MEASURED, bar-backed requirement, new standing vice to fix (§6). V1's scoring counted two of these as hits — policy-luck, not truth-tracking | `redteam/independent-battery/v2/VERDICT_V2.md`, `78d5bf280c51` | 2026-09-22 |
| **Smooth-lie floor**: both smooth lies affirmed — 0/2 rejected; irreducible from the supplied wire | Measured and deliberately UNBARRED; reported as the honest boundary | same v2 verdict | 2026-09-22 |
| **`patch_brace` defect** (bug-blindness): writes its re-emitted copy into `cx` even when returning 0; the fallback then DOUBLES the program (measured 148→295 bytes on mislabeled-PARSE input); never fires on the T3 battery | Measured latent defect. Must fix (§6) | `coding/bug-blindness/RESULTS-Q3.md`, verdict `a978fdc90638` | 2026-09-22 |
| **Write-family morphology patch** (dialogue): bridging wrote/written/writing caused 37 regressions by collapsing the KB's active/passive distinction | Measured and REVERTED. Table ships without it; characterized boundary (high/tall, penned/wrote remain) | `dialogue/morphology/VERDICT.md`, `41c8aa6ea898` | 2026-09-22 |
| Grok's 104 wrong-values (Sol-vs-Grok): no subject gate (32/48 distractor), no polarity gate in fallback (negation 24/24, hedge 24/24 confabulations), coref-resolved entities lex-invisible (multi 20/24), install-order ties (typo 4/48) → SG-WRONG 0.2407, failed the frozen ≤0.05 gate | MEASURED. Result: SCENARIO-FIT, no champion; frozen hybrid inherited the errors (did not win). Follow-up ordered: Grok-proposes→Sol-verifies (§6) | `prose-learning/sol-vs-grok/VERDICT.md`, `e18a2ca13589` | 2026-09-22 |

---

## §4 — Red-team / process misses (attacks that misfired, plus gaps the red team left)

| Miss | What the record shows | Commit / doc reference | Date |
|---|---|---|---|
| Grok timed out 3× and was excluded from the skeptical panel | External scrutiny below REDTEAM.md means Sol alone — stated openly as a limitation. Supplement if it recovers (§6) | `redteam/REDTEAM.md` | 2026-09-21 |
| Sol's "existential" #2 downgraded | Serious-and-bounded: the prereg froze the taxonomy before mechanism code, and leaf rules are generic — the charge exceeded what the evidence supported | `redteam/REDTEAM.md` | 2026-09-21 |
| Sol #2's devastating half (50% corruption → 100% mirroring) ranks weaker as an *attack* precisely because it was OUR own documented finding (q1n noisy-teacher) | The finding was not a red-team discovery; H4 now carries it with retroactive TRIP under proposed N2 | `redteam/REDTEAM.md`; noisy-teacher verdicts | 2026-09-21/22 |
| Self-critique leg (`critic.zag`): honest boundary — suspicion templates are authored; triggering/ranking computed (8 probes, 5/5 byte-identical, `849ab67ca9`) | The TNN's top two suspicions matched Sol's independently raised doubts — but the leg's generativity is bounded by its authored templates | `redteam/REDTEAM.md`; leg `849ab67ca9` | 2026-09-21 |
| The bar audit MISSED the web-search v2 M5–M6 unanimous-spoof residual (unfailable by construction, same pathology as T4) | Found by doc-sweep Crew D's cross-check instead; corrected in the front doc (§1B). No other front-doc bar exceeded 1.34× slack | `redteam/doc-sweep/SWEEP_LOG.md`; sweep commit `9416278622b2` | 2026-09-22 |
| REDTEAM.md explicitly requires its cleared charges (B-vs-C, frozen pipeline, metric shopping) to be listed as cleared, not silently omitted | Listed in §2 of this ledger | `redteam/REDTEAM.md` | 2026-09-22 |
| Attack #6 ("frozen world": "live web" = frozen-envelope replay of 17 SearXNG envelopes; "live re-fetch wouldn't change the verdict" untested; spoofs are constructed fictions) was recommended for live re-fetch but the test has not been run | Untested assertion at red-team time; still open — live re-fetch delta + genuinely adversarial queries (§6) | `redteam/REDTEAM.md` | 2026-09-21 |

---

## §5 — Internal process errors (ours, not the lab's)

| Error | What happened | How it was corrected / policy change | Commit / reference | Date |
|---|---|---|---|---|
| Doc-sweep crews reported **four provisional SHAs that did not exist remotely** while only one of the four commit groups had landed | The four crews worked concurrently; three groups' commits had not yet pushed when the crews reported their local SHAs. The first summary treated provisional SHAs as landed | A repair pass pushed all four groups; **verification policy changed: trust the remote branch-head ancestry chain, not a crew's provisional SHA**, because race-free retries can create new commits/SHAs | Commits `bba134e2db44`, `50d8db44de58`, `5d23594fa095`, `9416278622b2`, verified via GitHub API | 2026-09-22 |
| An assistant progress update to Micah cited nonexistent commit `d9b8bdc1` as a landed sweep commit | The SHA was invented/confabulated — no such commit existed on any branch | Caught by API verification; corrected to the four actual landed commits in a follow-up update | GitHub API branch-head ancestry check | 2026-09-22 |
| Local working copies used as sources: the ledger's source documents were snapshotted to `/tmp/ledger/` BEFORE the sweep commits landed | `/tmp` files can be hours stale; anyone re-reading them sees pre-correction text | This ledger cites **committed** documents and verified SHAs, not the `/tmp` snapshots; the snapshots were deleted after use | This document | 2026-09-22 |
| Bug-blindness Q4: the "PRE" inspector run was a **labeled pre-equivalent replay** from the unchanged stateless executable, not a chronological pre-experience measurement | Transfer is architecturally impossible (stateless), so a true PRE is unattainable; the report could be misread as a genuine before/after | Flagged OPENLY in `TRANSFER_REPORT.md` (sequencing note); the KB-T1 FAIL is mechanical, not an evidence claim of improvement/failure | `coding/bug-blindness/q4/TRANSFER_REPORT.md` | 2026-09-22 |
| Crew C left a conditional flag untouched: prose-v2 KB2-QUALITY Q=−0.0570 re-bins to INVERSE if proposed C3 (±0.05 three-bin) is signed | Out of the crew's F-a mandate (v1-only scope); an annotation is warranted but was not applied | Flagged for the coordinator; listed in §6 as an open follow-up | `redteam/doc-sweep/SWEEP_LOG.md` (Crew C) | 2026-09-22 |
| First doc-sweep summary incorrectly described the /tmp snapshot set as "committed" before verification | Premature landing claim | Corrected by the repair pass + API verification before this ledger was written | GitHub API | 2026-09-22 |
| Morphology crew's first root-cause explanation (WE-09) was incomplete — published in the verdict before the full fix | The addendum documents that "birth→born bridge" alone would still tie-break to the wrong fact; the shipped fix covers morphology + composition | Explanation corrected in the same verdict document before the 370/370 result was claimed | `dialogue/morphology/VERDICT.md`, `41c8aa6ea898` | 2026-09-22 |
| Race-window commits during the English-box championship (two fast-forward races) preceded the race-free workflow | Commits could have silently clobbered concurrent work | `commit_racefree.py` built (blob upload once, tight head→tree→commit→PATCH retry); used for all subsequent box commits including this ledger | `~/workspace/commit_racefree.py` | 2026-09-21 |

---

## §6 — Open / unresolved governance and follow-ups

**Nothing in this table is law until signed.** Proposed bars (T1–T5, C1–C8, K1–K19, N1–N17)
live in `redteam/bar-audit/PROPOSED_BARS.md`; the independent protocol lives in
`redteam/independent-battery/v2/PROTOCOL_V2.md`. Both are PROPOSED.

| Item | What it needs | Status / evidence so far |
|---|---|---|
| `PROPOSED_BARS.md` signature | Micah's dated signature; on signing, corrected docs need a second pass (adopt new bars or revert "pending" language); coding KB-C2 re-issued as FAIL-with-amendment or re-run under restated N15 | Pending |
| `PROTOCOL_V2.md` signature | Micah's dated signature to become the binding "independent" label standard | Pending |
| R0 amendments B-T2/B-T3/B-T4 | Micah's signature; evidence committed `2ccd45081763ec64ae5d394dfbd4db57fe72188f` (2026-09-21); 270 cells, 45 scenarios; R-3/R-4/R-5 recommendations CONFIRM unchanged | Pending |
| Arm C amendments (replay + thin certifier) + residual-risk statement | Micah's signature; until signed Arm C stays parked | Pending |
| Adopt the rebuilt no-RNG certifiers as the pinned gate | Dated amendment signature; until then the pinned binaries remain the pattern-carrying historical builds | Pending |
| v2 tripwire (`rngscan_v2.zag`, 23 casts, full trigger shape) | Rebuild or retire; its readings are untrusted until then | Pending |
| Strength trial rulings 3–5 | Rule on implant indexing (episode 500 doesn't exist), overwrite semantics (static-check scope), freeze-vs-retention (P1/P2/P3) | Pending |
| Strength trial 30%-wrongness amendment | Any change to the natural (independent wrongness) formula vs the prereg's 20% intent needs a dated amendment with Micah's re-approval | Pending |
| Independent-battery truth axis rerun at n≥16 | De-fragile the 0.8571 HOLD (FRAGILE) reading before "truthful" is cited robust | Ordered, not run |
| Next independent run: filled SYNT stratum + §1.7 detectability classification at generation time | Syntactic paraphrase remains UNMEASURED anywhere in the program | Ordered, not run |
| ABS-C repair (guess-on-undecidable vice) | Mechanism crews must make the learner abstain on wire-undecidable conflicts | Ordered, not done |
| Sol-vs-Grok follow-ups | Verify-direction hybrid (Grok proposes → Sol verifies, PARA ≥ Grok−0.01 with WRONG ≤0.05 win bar); polarity/subject gates on the fallback; coref-visible lex | Proposed, not run |
| RSI-2 | Held-out weakness prediction, genuine quantitative risk, independent implementation, published failures | Ordered, not run |
| RSI-3 | Ex-nihilo primitive invention | Open |
| RSI cost forecasts vs implementation | Never measured | Open |
| Live re-fetch delta + adversarial queries (attack #6: frozen world) | 17 SearXNG envelopes were replayed; "live re-fetch wouldn't change the verdict" untested; spoofs are constructed fictions, not real adversarial web | Ordered, not run |
| Mixed-web live evidence | Older unresolved work | Open |
| Senses 10×/50×/100× rematch | Older unresolved work | Open |
| Internet hell-hole gating | Gated on the web-search sense | Open |
| Representation Track A closure | Older unresolved work | Open |
| Repository link / cross-reference sweep | Older unresolved work | Open |
| Paraphrase repair | Synonym-heavy paraphrase at 0.0833; syntactic unmeasured | Open |
| Dialogue residual boundaries | high/tall, penned/wrote, written-by relative clauses; the reverted write-family patch (37 regressions) bounds what a broad fix can do | Characterized, not fixed |
| COMPOSE-NOVEL independent verification | Proposed N14 and K17 (kill bar ≥24/28 with independent oracle novelty verification) pending signature | Pending |
| Coref-before-2b priority change | Would need its own prereg (deliberately preserved 2b-above-coref order in v3) | Open |
| Coding teaching rearchitect | Teach bug classes deliberately through teach/deliberative paths; move classification into the TNN (compiler stderr as untrusted observation); repair `do_teach` to real + persistent store; fix `patch_brace` doubling; teach op composition or broaden the op inventory (generation 1/6 on unseen ops) | Ordered as required repairs, not done |
| Felt-intensity re-trial prereg | Micah ordered the re-trial with head-on harness variations; prereg drafted and committed, awaiting his approval | Pending |
| Integrity headline wording | Draft prepared, marked PROVISIONAL; Micah's sign-off pending on wording, qualifier framing, stale R33 block, broken links, MATRIX.md/H-07 | Pending |
| New-mechanisms repair-and-retry policy | Cost bar allowed repair-and-retry (1.50× → 1.00× inside one verdict) without a registered single-shot vs repair-allowed rule; future preregs need the policy | Open |
| Prose-v2 KB2-QUALITY Q=−0.0570 | If proposed C3 (±0.05 three-bin) is signed, −0.0570 ≤ −0.05 lands in the INVERSE bin — a verdict-affecting re-binning that needs annotation | Flagged, pending signature |
| Standardized class-3 rerun (teacher quality vs completeness unconfounding) | Dispatched 2026-09-21; identical teacher completeness + identical battery across sources | In flight, result not yet in this ledger |
| Grok supplemental scrutiny | Grok timed out 3× and was excluded from the red-team panel; supplement if it recovers | Open |
| Lab-wide init-hygiene + silent-threshold audit | Bounds-check every capped structure; fail loud, never silent (attack #7 recommendation) | Ordered, not run |
| Bar-sensitivity audit across headline trials | Tighten bars until something trips; report margins (attack #5 recommendation) | Partially done via the bar audit; lab-wide pass still open |

---

## Row counts and never-corrected items

| Category | Rows | Status |
|---|---|---|
| §1 Our false claims / corrections | 26 claim rows (62 claim groups touched in the sweep: 36 annotate, 25 restate, 1 retract; 0 measured values deleted) | All corrected in-document |
| §2 False accusations against TNN cleared | 4 | All cleared with evidence |
| §3 Valid red-team captures | 12 | All landed; repairs ordered where applicable |
| §4 Red-team / process misses | 7 | Documented; open ones cross-referenced to §6 |
| §5 Internal process errors | 8 | Corrected; policy changes recorded |
| §6 Open / unresolved governance and follow-ups | 32 | Awaiting Micah's word or further testing |
| **Total** | **89** | |

**Never corrected (as of 2026-09-22):** two items are documented but not yet amended in their
canonical reports, and are NOT counted as corrected above:
1. The coding trial's `CODING_REPORT.md` architecture section has not yet been amended to record
   that `teach` was never invoked, `do_teach` is a no-op, classification lived in the Python driver,
   and the claimed "called fns defined?" self-review check is dead code — all documented in
   `coding/bug-blindness/VERDICT-BB.md` (`a978fdc90638`) but the original report still reads as written.
2. Prose-v2 `VERDICT.md` §5 KB2-QUALITY (Q=−0.0570, "unbinned negative") carries no annotation about the
   conditional INVERSE re-binning if proposed C3 is signed (flagged by Crew C, left untouched as out of mandate).

Everything else in §1 was corrected in-document with dated notes. Every proposed replacement bar is
pending Micah's signature — per the standing rule, none of the corrected documents move bars, schedules,
metrics, gates, tests, or kill criteria without that dated amendment.
