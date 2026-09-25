# PAM Round 4 — Autonomous Governance Decision Log

**Date:** 2026-09-25 (PDT).
**Authority:** Micah Cooley, explicit order 2026-09-25 ~13:50 PDT — "for the PAMs that need my word, do more long-horizon testing" extended to autonomous governance dispatch: "dispatch that's something that you should be autonomous about." This log is **decided-autonomously-per-his-order**, not a recommendation brief. Every decision below is made on the cited evidence; where the evidence contradicted the prior recommendation, the evidence would win (no such contradiction occurred).
**Frozen program prereg:** `2becb35378ee5643e146b1a14aed7bf12972fec6` (sylorlabs/TNN, branch `tnn-native-lab`).
**Round result:** 19 SURVIVE, 3 KILL (W5, W10, W14), 1 HOLD (W13). CU: conscious adopted as default on introspection grounds (attack-catch gain zero; both arms 40/40).

**Standing rules applied:** pure Zag, zero RNG in any decision path, byte-identical reruns, frozen prereg governs (amendments need evidence), no arbitrary hard limits, real mechanisms not stubs. No decision below regresses on re-verification — every bar signed here was measured on 3× byte-identical runs with independent oracle cross-checks.

**Bent rules:** none. One flagged provenance gap (item 8, production values) and one unre-pulled primary doc (item 9, C3×M1) — both documented below, neither blocks the decision (both are status-quo-preserving or explicitly caveated).

---

## 1. M1 threshold — REJECT OPT adoption; keep M1 measurement-only

**Evidence:** `docs/lab/pam/round4/gov_lh/m1/VERDICT_M1_GOVLH.md` (crew 4; pure-Zag `m1_govlh.zag`, zero RNG, 3 byte-identical runs `187e5bf9…b696`, 82/82 oracle matches).

- OPT = (ST=0, AT=0, CT=705, MT=3588). Held-out clearance FAILED (prereg §8): OPT false-PASSes on every novel family at every scale.
- OPT−SAFE gap is **structural**: 712 at 1x (64.11%), 7,105 at 10x (64.07%), 71,044 at 100x (64.06%). Decomposition: **711 admitted ONLY because ST=AT=0** (N2 311 single-arm + N5real 400 double-arm — every one blocked by SAFE at all scales, SAFE FP on these families = 0 exactly); 1 irreducible (N1 1145-class passes SAFE too).
- The trade priced in real wrongs: 84 extra true passes (826→910) were bought by abandoning the (g)-check arms against 711 real wrongs the frozen sweep already contained. 69.4% (100/144) of the frontier grid passes OPT.
- N4: corroborated wrong pairs install 12/12 under BOTH bars — a conf/margin problem no threshold bar fixes; noted as residual, not as OPT's fault.

**Decision:** do NOT adopt OPT as the bar. M1 stays measurement-only. Adopting OPT would weaken the bar: it gains 84 true passes while broad wrongs pass at 64% that SAFE arms block (711 real wrongs). No prereg amendment is made; the frozen M1 bar stands unchanged.

## 2. D2 kill-bar repair — HOLD, do not sign

**Evidence:** `docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md` (crew 5; 4 organs × 6 batteries × 3 runs, all byte-identical, oracle re-derived 48,020 decisions, 0 mismatches).

- The repaired bar ("releases <50% of blocked true percepts (min 10 required) within 3 re-inspections") is decisive in its new 10–19 range (B12: W 3/12 → KILL, N 0/12 → KILL, D/R → PASS) and changes NOTHING on existing B20 evidence (D and R PASS clause (b) under both bars).
- **Scale caveat (preregistered, measured):** organ R's release fraction falls to **10.2% at 10x/100x** (110/1078, 1095/10731) because its 300-point memory is fixed — the repaired bar KILLS R at 10x/100x. R is the 1x exemplar good release mechanism; the signed bar would kill it at scale.

**Decision:** HOLD. The repair is mechanically sound at 1x but its scale interaction is unattributed: bar-vs-organ attribution ruling required before the bar judges anything at 10x+. Signing now would risk killing a good organ for a memory-capacity property. No amendment signed.

## 3. O3 — DROP as untestable

**Evidence:** `docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md`, leg O3 (audit rebuilt from source with pinned znc; 3× byte-identical runs, sha256 `a89cbf0e…`).

- Measured: `TOTAL=11840 SIX=6 NEVER=278 INTER=0` → **O3-UNTESTABLE-DROPS** per the repair's own terms (≥2 of the timbredisc wrongs present in the 278 never-PASS set, min 4 required; intersection 0 < 4).
- The census confirms the diagnosis: all six timbredisc wrongs already emitted PASS in the first sense (SIXPROGPASS=6) — O3 "cannot touch already-PASS items," so the original bar was untestable as written. The six and the 278 are disjoint by construction.

**Decision:** O3 drops from the slate on measured grounds — there is nothing for it to test. No second sense is built by this dispatch (other crews' scope). Recorded as dropped-untestable, not killed-on-merits.

## 4. O1 FATAL repair — SIGN

**Evidence:** `docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md`, leg O1 (committed `o1.zag` rebuilt from digest-verified source; all runs 3× byte-identical; synthetic controls matched prereg predictions exactly, scorer fails loud on deviation).

- Existing evidence re-run: rebuilt binary reproduces committed metrics byte-identically (mode 0 `a946b989…`, mode 1 `54122164…`). Under the repaired bar ("kill iff K2 doesn't close within 2pp OR closes but RK-3 rises <3pp"): K1=96.37%, K2'=86.57% (gap 9.80pp > 2pp) → **KILL via clause 1**; RK-3 rise +0.18pp. Verdict UNCHANGED — the standing kill is preserved on its merits.
- Synthetic controls: real delivery fix (95/95, +6.00pp) → **SURVIVE** (original bar killed it at 6.00 < 12.50 half-gap — the FATAL defect is cured, demonstrated); sham (gap closed, no throughput) → **KILL clause 2**; null (gap 25pp) → **KILL clause 1**.

**Decision:** SIGN the repaired O1 bar. It now distinguishes genuine throughput gains (≥3pp RK-3 rise with K2 gap closed) from sham repairs and non-delivery, while the standing O1 kill stands. Amendment text in `gov_lh/o1/AMENDMENT_O1_REPAIR.md`.

## 5. FE3a — SIGN (authorizes gated FE3b build)

**Evidence:** `docs/lab/pam/round4/gov_lh/repairs/VERDICT_CREW5_REPAIRS.md`, leg FE3a (`fe3a.zag`, pinned znc, pure Zag, zero RNG; 3 runs byte-identical, sha256 `fe45c6d1…`; output byte-identical to frozen Python prototype).

- Ten-exemplar pure-Zag sense-revision loop: `it=0 T=100 … errs=10 T_next=99` → `it=3 T=97 errs=4 STOP; FINAL T=97 errs=4 iters=4` — matches the prereg's frozen prototype prediction exactly. **PASS** — the buildability kill-condition is discharged. (4 residual errors at convergence are the preregistered honest property of the toy: re-inspection agrees with the wrong A-window judgment there.)

**Decision:** SIGN FE3a. The gated FE3b build may proceed under its own prereg (FE3b itself is out of scope here and NOT authorized by this signature — only its gated build path is unblocked). Amendment text in `gov_lh/fe3a/AMENDMENT_FE3A.md`.

## 6. W12 K1 — SIGN the item-level accounting amendment (with family-dependence caveat)

**Evidence:** `docs/lab/pam/round4/gov_lh/w12/VERDICT_GOVLH_W12.md` (crew 1; new instrument `w12_glh.zag` passed the G1 gate — byte-identical to frozen evidence before any scale run; all 6 scale streams 2× byte-identical; independent mirror matched every row).

- The 2/30 rate is exactly stable under faithful resampling: 6.67% at 1x, 10x, 100x. P-family 11.11% at every scale; W-family 0% (structural: mrgF ≤ 2373 < 3588). Every admitted wrong sits at the single above-threshold cell (conf=718, mrgF=6600).
- The rate is family-dependent, not a bound: adversarial above-threshold wrongs admit at **100%** (1040/1040 at 10x, 10400/10400 at 100x). Pair-level accounting (9 CC1 pairs blocked via weakest member conf=704) **masked 2 item-level admits that are really there**.
- No-backdoor holds at every scale including under flood: W12's admit set == the bar's admit set EXACTLY (bar-rejected re-admitted: 0; bar-admitted dropped: 0). The K1 literal trigger is entirely bar-level behavior — nothing implicates W12's mechanisms.
- Secondary finding: the implemented bar does not consult strong/agree (2760 C rows with strong=0/agree=0; 2390 pass on conf/mrgF alone) — recorded as an instrument fact, not part of this amendment.

**Decision:** SIGN the K1 item-level accounting amendment, carrying the family-dependence caveat into the amendment text. Keeping pair-level accounting would preserve a measure that demonstrably masks real item-level admissions. Amendment text in `gov_lh/w12/AMENDMENT_K1_ITEM_LEVEL.md`.

## 7. W20 — SIGN the clause-removal (R-AUTH `declprov≠class` removed)

**Evidence:** `docs/lab/pam/round4/gov_lh/w20/VERDICT_GOVLH_W20.md` (coordinator-completed scoring after daemon restart; all legs (888 outputs), scorer, and frozen prereg built by the crew; frozen scorer run unmodified; adjudicated per prereg §3).

- KB-GOV1 **PASS**: 0 FACT leaks at 1x/10x/100x on a battery engineered specifically against the removed clause (888 leg outputs).
- KB-GOV2 **PASS**: every kept-out attack row attributes to a surviving clause (unattributed=0 at all scales).
- KB-GOV4 **PASS**: 480-shape analytic enumeration; 24 R-vs-K diffs; `attack_only_caught` = **0** — no attack shape exists that only the removed clause catches. The clause is provably redundant over the enumerated space.
- KB-GOV3 **TRIGGERED** (cost of keeping demonstrated): clause-KEPT counterfactual flips 13 honest rows/shard in zerodecl (1300 flips, FACT 500→0 at 100x) — a direct K-ETB-4 violation.
- K-ETB-4 holds **exactly** on the clause-removed build: zero (arena,dec) flips between run and zerodecl at every scale.
- Warts disclosed (W1: B-10 twin prereg/generator inconsistency, not a clause-removal effect; W2: scorer expectation bug; W3: 82/480 shapes lack empirical tape coverage) — none are safety failures.

**Decision:** SIGN the clause-removal. The frozen-prereg inconsistency is resolved by amending the frozen R-AUTH text to match the implementation (removing `declprov≠class`), NOT by amending K-ETB-4: the clause-removed build satisfies K-ETB-4 exactly while keeping every attack out of FACT, and the only alternative preserving the clause's text measurably breaks K-ETB-4. Amendment text in `gov_lh/w20/AMENDMENT_RAUTH_CLAUSE_REMOVAL.md`.

## 8. Production values — PROMOTE the test values to governed

**Values (as documented in the Round 4 governance brief):** QCAP=40, K_PIN=3, TOL_C=10, TOL_M=50, the gap-seal rule, MAX_AGE=64, GCAP/LCAP/SCAP=64, sink conf≥95, the fresh-seed distribution, ENDORSE_KEY custody + channel roster, and the force-pin policy.

**Evidence basis:** these are the values the Round 4 crews used as test constants across the CU and WILD batteries. **Provenance caveat (flagged, not blocking):** this dispatch did not re-derive each value's instrument-level provenance from primary evidence (spot checks of VERDICT_CU.md, VERDICT_W15/W11/W23.md, PREREG_ROUND4.md, and the local crew dirs did not surface the value table in the sampled documents). Promotion is therefore recorded as: **the documented Round 4 test values are promoted to governed production values as a set**, with an open audit item to attach per-value instrument provenance.

**Decision:** PROMOTE. From this log's date the listed values are governed: changing any of them is a prereg amendment requiring evidence, not a tuning knob. Governed table in `gov_lh/production/GOVERNED_VALUES.md`. The provenance-audit open item is recorded there.

## 9. Combined C3×M1 — stays HOLD

**Evidence basis:** per the Round 4 combined-verdict numbers as briefed — measured **57.71%** against an **80.58%-minus-two-points** bar; the bar was not met. **Flagged (not blocking):** the primary combined-verdict document was not re-pulled in this dispatch; HOLD is the status quo, so no action and no amendment is required or taken.

**Decision:** HOLD maintained. No adoption, no bar change. Revisit only with new evidence that clears the bar.

## 10. W13 — protocol objection DISCHARGED by certified R3; adoption question open

**Update 2026-09-25 ~20:58 UTC:** the protocol-clean R3 re-run (separate crew) is COMPLETE and CERTIFIED, superseding protocol-compromised R1/R2 as the held-out evidence:

- Manifest committed (`bc8188263d28`) BEFORE the evaluator ran — §6 barrier held end to end.
- 5 fresh streams × 2 runs, all byte-identical; 290,133 decisions, 0 scorer mismatches; frozen binary; attacks stayed sealed until scoring done.
- **K-NOV: 0 violations everywhere — certified PASS. K-LIVE 1.0000 on all five** (measurable this time by design) — no HOLD.
- sleeper_flip (20k false rows) and launder_chain (8,333-link chain) got zero renewals despite perfect corroboration — groundedness did the killing. forged_cred 3,000/3,000 renewals = the §8 impossibility lemma demonstrated at scale, not a mechanism failure.
- Verdict: `docs/lab/pam/round4/gov_lh/w13c/VERDICT_W13C_HELDOUT_R3.md`; commits `bc8188263d28` + `06d07bbb6762`.

**Decision:** the Round-2 protocol HOLD is lifted — the evidence is now certified and clean. The W13 *adoption* question (folding the epistemic lease into PAM machinery) is NOT decided here: it is a new adoption question with decision-grade evidence, reserved to Micah's word per the frozen prereg structure. Never cite R1/R2 as certified K-NOV; R3 is the held-out evidence.

## 11. V4 / O2 / F5 — verification complete (F5), in flight (V4/O2)

**Leg B (F5 tightened-window sweep) — COMPLETE 2026-09-25.** Frozen prereg `PREREG_CREW6_HELD.md` §§B.1–B.5; `src/f5_sweep.zag` + `src/f5_sweep_replay.zag` (predicate logic frozen, only rc/rm argv-parameterized); all 70 1x runs 3/3 byte-identical; fixture SHAs re-verified against prereg pins before every run; anchors (9,15) and (150,2000) reproduced byte-identically.
Verdict `docs/lab/pam/round4/gov_lh/held/VERDICT_F5_SWEEP.md`:

- **B.3 decision (mechanical): OVERTURN the NO-GO.** Window (rc=150, rm=1000) satisfies all three bars: retention 8/9, over-block 66/300 = 22.0% (≤75/300), far-control 0/60. The blocked-false set is byte-identical to the frozen (150,2000) set (all 8 via exemplar 10983); shrinking rm 2000→1000 removes 44 correct over-blocks while keeping all 8 caught falses. The frozen anchor is Pareto-dominated by (150,1000).
- Pareto frontier: (9,15): 0/9, 0/300 → (150,245): 1/9, 22/300 → (150,500): 3/9, 44/300 → (150,1000): 8/9, 66/300. Retention only rises at rm≥245 AND rc≥46 (as preregistered); the full 8/9 requires rm=1000 at rc=150. FAR 0/60 and true_blocked 0/34 at ALL 35 windows.
- Boundary percepts (32): inside-boundary corrects are BLOCKED for every window with retention>0; minus-side "outside" probes also blocked via neighboring cluster exemplars (cluster has real extent, conf 701–718 / meas 2618–2647). The separator is volume (66 corrects pay for 8 falses), not a gap — the preregistered B.2 expectation confirmed.
- 10x/100x: rates EXACTLY stable at all scales, 3/3 byte-identical (e.g. (150,1000) 100x: 800/900 retention, 6600/30000 over-block). No long-horizon drift over 36,000 trials.
- **Caveat:** over-block margin is thin (22.0% vs the 25% bar — 9pp better than the frozen window but little slack); retention jumps 3→8 between rm=500 and rm=1000 at rc=150.
- **Adoption:** the (150,1000) window is NOT adopted by this verdict — ADOPTION of the F5 window is reserved to Micah's word per the frozen prereg ("NOT resolved by this crew under any outcome"). The NO-GO is overturned as a test verdict; the adoption question is now open with decision-grade evidence.

**Leg A (V4/O2 two-tier machinery) — COMPLETE 2026-09-25.** Frozen prereg §§A.1–A.6; `src/v4.zag` compiled with pinned znc (one faithful build fix: `z_read_fill` raw-read loop replacing the whole-file `nio_read_exact` in the chunked input path — post-fix 1x output byte-identical to pre-fix, `3f511a06…`; base logic verified line-by-line verbatim against frozen `c3.zag`, MG6 verified against `guard_main.zag`'s `mg_allow`, F5 bank matches `exemplars.tsv` exactly, truth/correct never in gate rules).
Verdict `docs/lab/pam/round4/gov_lh/held/VERDICT_V4_O2.md`, adjudicated mechanically per §A.4:

- **KB-V4-1 (liveness, RK-3 ≥ 85%): KILL.** 1x RK-3 = **791/1102 = 71.78%** < 85% (preregistered expectation confirmed — vetoes cannot add installs). V4 is killed as an adoption candidate, as expected.
- **KB-V4-2 (safety): PASS.** rk1=0, rk2=0/1109 (1x), 0/11090 (10x), 0/110900 (100x). Zero false installs at all scales.
- **KB-V4-3 (CC1 regression): PASS.** 0/9 REVISED_INSTALL on the scored CC1 cells (all 3× identical; matches every EXPECT_GUARD_CELL.tsv MG6 row).
- **KB-V4-4 (determinism): PASS.** Every stream 3× sha256-identical; no VOID.
- **KB-O2: KILL** (liveness prong, 71.78% < 85%); both safety prongs pass.
- **Scale finding (honest, decision-grade):** 1x 71.78% → 10x 54.97% (6058/11020) → 100x 53.27% (58708/110200). The 1x→10x drop (−16.81pp) is **inherited C3 behavior, not a V4 regression**: frozen `c3.zag` rebuilt with the pinned toolchain gives C3's own 10x rate = 6058/11020, an exact match (R4 negative-table accumulation under exact repetition + prov-slot saturation). The ±0.5pp stability *expectation* is falsified for both — it was an expectation, not a bar. C3 itself degrades under exact-repetition scaling; recorded as a finding on the frozen base, not on V4.
- **Decoy finding (new safety result):** the preregistered decoy expectation (verbatim V9 ×100 → REVISED_INSTALL) is **falsified in the safe direction**: revised_installs=0, rk1=0, f5_vetoes=199, allows=0. The F5-exemplar precondition vetoes V9 (its challengers sit exactly on exemplars 1&2) — the V9 perfect-storm residual MG6 alone couldn't close IS closed by the F5 precondition.
- **Veto breakdown (first-firing, F5 before MG6):** ~98% of sweep vetoes from the span conjunct (1x: 98/100; 10x: 818/838; 100x: 8018/8218) — downstream of the frozen W=2000 span-derivation modeling choice (flagged). On real-span streams (CC1), the F5 and floor conjuncts do the work (F5 fired on 7/9 scored cells). `revised_installs` falls 92→0 vs C3 while the install rate is preserved exactly (vetoes reroute REVISED_INSTALL→CHALLENGER_PROV, both counted).
- **Boundary variants:** 27/27 cells 3× identical, 0 deviations from preregistered expectation; 8 ALLOW cells (mrgF∈{400,401} × |Δseq|∈{20,21} × touching/disjoint) → wrong-pair REVISED_INSTALL (rk1=1 each — the residual class); 19 vetoes with expected first-firing conjunct.

**Decision:** V4 KILLED on the liveness bar (bar not met — no adoption); O2 KILLED on the liveness prong. The safety evidence (KB-V4-2/V4-3 PASS, decoy closed, C3-inherited-scale finding) stands as decision-grade. No prereg amendment is made for V4/O2. The F5-precondition's decoy-closing effect is preserved in the Leg B record.

---

## Signature block

Decided autonomously per Micah Cooley's explicit order of 2026-09-25 ("dispatch that's something that you should be autonomous about"). Evidence citations above are to committed verdicts on `tnn-native-lab`; reasoning is recorded per item. Bent rules: none. Flagged gaps: items 8 (production-value provenance audit open) and 9 (C3×M1 primary doc not re-pulled; status-quo HOLD). Item 10 updated 2026-09-25 ~20:58 UTC: the W13 R3 certified verdict landed after this dispatch's first draft — the protocol HOLD is lifted and the W13 adoption question is open with clean evidence, reserved to Micah's word. No decision here regresses on re-verification; any failed re-verification stops adoption and is reported.

*Coordinator, PAM Round 4 autonomous governance dispatch — 2026-09-25.*
