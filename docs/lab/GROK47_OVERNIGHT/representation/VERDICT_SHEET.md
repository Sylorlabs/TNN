# VERDICT SHEET — Representation/Tokenization + Scaling (GROK47 overnight)
**Worker:** native Muse (sector: representation + scaling). **Engine:** grok-4.7 (hypothesis/attack) + gpt-5.6-sol (fallback substantive, per 23:25 fallback alert).
**Date:** 2026-09-21/22 overnight. **Report dir:** `docs/lab/GROK47_OVERNIGHT/representation/`
**Item tracker:** `ITEMS_DONE.tsv` (1229 owned items; coordinator merges).

## 1. Hypotheses (engine-proposed)

### B-T1 re-attack (grok-4.7, 3 hypotheses, kill bars preregistered BEFORE testing)
- **H1 ARTIFACT:** the perturbed probe leg (XOR every offset ≡0 mod 7, then exact byte-match re-location) is a length annihilator: every arm with unit length ≥8 scores exactly 0.0 and loses half its grounded score. *Kill:* any L≥8 arm with pert>0.01 on a controlled corpus kills H1; L∈{1,4} with pert≤0.5 weakens it.
- **H2 ARTIFACT:** the frozen empty-vocab rule zeroes 80% of fixed_window_64/prose (zero repeated 64-byte windows in Shakespeare) — a sparsity-vs-window-size cliff, not a quality signal. *Kill:* dropping empty-vocab zeroing still leaves raw_micro non-last.
- **H3 MECHANISM (REFUTED by its own kill bar):** on the clean delimiter-following leg, byte identity is a genuinely stable recurring unit (raw_micro mid-pack, not last); the preregistered dead-last bar is false as a property of the units under this probe. *Kill:* clean-only ranking with empty-vocab cells excluded placing raw_micro strictly last. → **FIRED: raw_micro 9/9 dead last (0.7884 vs next 0.8577). H3 WITHDRAWN.**

## 2. Prereg bars
- H1: synthetic periodic corpus (fixed 991-byte random block ×600; every window content phase-unique → units perfectly consistent by construction) scored with the **frozen** `bt1_score.py`. Predicted: clean≥0.9 all L; pert>0.5 for L∈{1,4}; pert==0.0 exactly for L∈{8,16,64}.
- Red-team settle tests: L=6/7 boundary pin; repetitive-corpus spurious-match test; counterfactual leaderboards (clean-only) from frozen `score_all.log`; exact cell reproduction (synthetic SEG + frozen scorer on hash-verified real corpora).

## 3. Results (native-verified)

| Test | Result |
|---|---|
| Synthetic periodic, L=1/4/8/16/64, frozen scorer | clean 0.9357/1.0/1.0/1.0/1.0; **pert 0.9337/0.9740/0.0000/0.0000/0.0000** — ALL prereg predictions hold |
| Boundary pin L=6 vs L=7 | L=6 pert=0.8789 (survives), L=7 pert=0.0000 (annihilated) — the 6-byte clean-run gap of stride-7 XOR confirmed exactly |
| Exact cell reproduction (real corpora, sha256-verified) | _8/code clean=0.9446 pert=**0.3276**; _8/prose 0.9419/0.0000; _16/prose 0.9807/0.0000; _16/code 0.9648/0.0000 — reproduce frozen `score_all.log` to 4 decimals |
| Dissection of _8/code perturbed relocations (40 vocab entries) | **genuine=0, spurious_XOR=20** — every counted occurrence is an XOR-collision, e.g. X=`"        "` (8 spaces) matched at clean offsets holding `"      z "` ('z'=0x7A=' '^0x5A) |
| Counterfactual: pert leg removed (grounded=clean) | _16 0.9778 > _8 0.9553 > surprise 0.9424 > _4 0.9272 > … > raw_micro 0.7884 (8/9) > _64 0.5973 — raw_micro STILL not dead last **with the frozen zeroing kept** |
| H2 settle: clean-only + empty-vocab EXCLUDED (not zeroed) | _64 0.9961 (code only) > _16 0.9778 > _8 0.9553 > surprise 0.9424 > _4 0.9272 > … > **raw_micro 0.7884 DEAD LAST (9/9)** — H3's own kill bar fires |
| Ranker audit | `bt1_rank.py:44` — `"vocab_probed_code": prose["vocab_probed"]` copy-paste bug: the code-vocab column displays the prose value (display-only; scores/ranks unaffected). Real _64/code vocab=256, displayed 0 |

## 4. Red-team attacks (grok-4.7) + adjudication (native)

- **Attack 1:** "_8/code pert=0.3276 falsifies 'every ≥8-byte arm is exactly 0.0'; the cited zeros are cherry-picked." → **ADJUDICATED: attack premise confirmed, conclusion refuted.** The 0.3276 cell is 100% spurious XOR-collision relocations (genuine relocation is mathematically impossible for |X|≥7: every length-≥7 window spans an offset ≡0 mod 7). pg100 lacks the collision patterns; sqlite3.c has them (`"      z "`). The non-zero cell *confirms* the annihilator — the leg measures corpus accident, not unit quality. Full arm×corpus matrix dumped: the only non-zero among uniform-L≥7 arms is this spurious cell.
- **Attack 2:** "'driven by probe, not quality' is a false dichotomy; no counterfactual re-rank shown." → **ADJUDICATED: sustained — the counterfactuals are now computed.** (i) With pert removed but the frozen empty-vocab zeroing kept: _16 would WIN (0.9778), raw_micro 8/9 — still not last. (ii) H2's settle test (clean-only, empty-vocab EXCLUDED): _64 0.9961 > _16 0.9778 > _8 0.9553 > surprise 0.9424 > _4 0.9272 > … > **raw_micro 0.7884 dead last (9/9)** — the preregistered ordering **predictive_surprise > fixed_window_4 > raw_micro with raw_micro dead last HOLDS** under fair handling. Conclusion: the binding FAIL is driven by **two probe/operationalization artifacts** — the perturbed-leg exact-match annihilator (cost _8/_16/_64 their perturbed half) and the empty-vocab zeroing (kept _64 below raw_micro). NOT by raw_micro being genuinely competitive.
- **Attack 3:** "synthetic corpus doesn't identify the tournament; cliff reported at 8 only because the grid is {1,4,8,16,64}." → **ADJUDICATED: refuted by E1.** L=6 survives, L=7 annihilated — the mechanism predicts the boundary at exactly 7 and the data lands on it. Plus exact 4-decimal reproduction of four frozen cells on the real corpora with the frozen scorer.

## 5. Fixes landed
- **None to frozen evidence** (closeout/repair dirs untouched — no-reinterpretation rule). Two fix candidates filed for coordinator/Micah: (a) `bt1_rank.py:44` vocab_probed_code display bug (trivial, display-only); (b) B-T1 probe amendment proposal (NOT enacted — needs Micah's dated signature): replace exact-match relocation with a length-fair relocation (Hamming-tolerant or anchor-based), smooth the empty-vocab rule, recalibrate the dead-last clause for the byte-stream substrate. Grounded-repair already landed by crew3 (commit `53d5612c5ed0`), verified intact.

## 6. Final verdicts (both voices labeled)

- **[native] B-T1 binding verdict: FAIL stands** (bars bind; raw_micro 7/10, not dead last). The re-attack explains WHY with two separable probe/operationalization artifacts: (1) **perturbed-leg annihilator (dominant):** exact-match relocation cannot genuinely relocate any unit ≥7 bytes — measured pert=0.0 for _8/_16/_64 on both corpora except one spurious cell; synthetic boundary pin at exactly L=7; dissection shows 100% of _8/code's 0.3276 relocations are XOR-collisions; (2) **empty-vocab zeroing:** the frozen rule cliffs _64/prose to 0.1984, keeping _64 below raw_micro. The H2 settle counterfactual (clean-only, empty-vocab excluded) produces **_64 0.9961 > _16 0.9778 > _8 0.9553 > surprise 0.9424 > _4 0.9272 > … > raw_micro 0.7884 DEAD LAST (9/9)** — the preregistered ordering **predictive_surprise > fixed_window_4 > raw_micro, raw_micro dead last, HOLDS** under fair handling. The FAIL is artifact-driven, not unit-driven.
- **[grok-4.7] H1 SUSTAINED, H2 SUSTAINED, H3 REFUTED** — H3's own preregistered kill bar (clean-only + empty-vocab excluded → raw_micro strictly last) fired: 9/9 dead last. The "bytes are genuinely competitive units" mechanism claim is withdrawn; byte identity is a *stable* unit (clean 0.85–0.90) but strictly the worst of the nine under fair scoring.
- **[native] Section champions (frozen §7 recording, unchanged):** B-T1 tournament champion **predictive_surprise** (0.9190); compression champion predictive_surprise; retrieval champion predictive_surprise; grounded-consistency champion fixed_window_64 (qualifier: _64's win rides the clean leg — 0.9958 on code — since its prose cell is empty-vocab and its perturbed leg is artifact-zeroed; see §4).
- **[native] Adaptive MDL:** repaired (heap-overflow fix), 0.8319 mean, rank 7/11, binding verdict FAIL — verified against `repair_2026-09-21/REPAIR.md`; no re-test needed (byte-identical non-grounded goldens).

## 7. Fallback log
- 2026-09-21 ~23:25 PDT: coordinator FALLBACK ALERT (truncation). **My instance:** my wrapper (explicit max_tokens) returned COMPLETE responses at 23:16 (hypotheses) and 23:23 (red-team, ~2.5KB) — never used stock chat.py. No truncation observed; no conclusions drawn from truncated outputs.
- 2026-09-21 ~23:34 PDT: coordinator CORRECTION + ESCALATION. **CORRECTION confirmed:** the ~50–90-byte truncations were stock `experientiallabs/bin/chat.py` hardcoding `"max_tokens": 16` (line 26) — a tooling artifact, not model degradation. All outputs in this sheet were captured via the working wrapper (or sol) and are **NOT voided**; no recaptures needed. **ESCALATION:** grok-4.7 HARD DOWN — gateway HTTP 429 insufficient_credits, org balance $-0.02 (re-probed 23:30 PDT). Unusable even for short outputs until Micah tops up credit. Substantive generation → gpt-5.6-sol via UnoRouter; I am EXEMPT from hourly grok re-probing (coordinator cron handles it). Fallback instances this sheet: grok→sol red-team routing (1 batch, scale verdicts) — logged above; the hypotheses + B-T1 red-team batches were grok-4.7 via working wrapper pre-down, valid.

## 7b. Native cross-checks (this session)

## 8. Scale verdicts — red-team (gpt-5.6-sol, per fallback routing) + adjudication (native)

**Attack S1 (circularity):** "mastery 1.0 may just be exact-address store write/read; perfect from N=1 to 6.58M with no variance is the warning sign." → **[native] PARTIALLY SUSTAINED as scope-clarification, refuted as refutation.** The frozen prereg's question (`scale/PREREG.md:3`) is explicitly "no degradation over long horizons" — a retention/cost/determinism question, not a generalization question. Mastery = fraction of taught facts recalled == truth, and the verdict reports FULL-probe counts at top scale (6,256,828/6,256,828 — not a sample). Generalization is other workstreams' preregistered job (prose paraphrase 48/48, dialogue 370/370, Sol-vs-Grok duel). The verdict never claims generalization. Review-note only.
**Attack S2 (flaw coverage):** "96/6.58M = 0.0015% coverage, probes in [0,n/4) — structurally blind to high-ID corruption; doc-sweep already flagged tripwire slack." → **[native] SUSTAINED — and it caught a gap the doc-sweep missed.** Verified in `scale/driver/scale_learner.zag:954`: `id=(q*n)/96`, q∈[0,24) → ids ∈ [0,n/4). The params verdict carries the H2 honest-fail annotation for this; the **scale-up VERDICT.md does NOT** (3 CORRECTION notes, none on flaw id-coverage — grep verified). **FAIL-open fix candidate for coordinator:** annotate scale-up VERDICT.md flaw column ("96/96 at every scale") with the [0,n/4) coverage caveat. The mastery column is unaffected (full-probe).
**Attack S3a (single rep at top scale):** "N≥999,984 has reps=1 — byte-identical reruns unestablished at the largest sizes." → **[native] SUSTAINED as residual risk.** Table confirms reps=1 at the top two scales. KB-DETERMINISM "NOT TRIPPED" at 6.58M rests on one run. Mitigating: identical code path, 3–5/5 byte-identical at 240→240K, single-threaded deterministic Zag (no allocator/threading nondeterminism surface). Residual risk stands; recommend a second 6.58M rep when capacity allows (cheap relative to the first — no new code).
**Attack S3b (decorative parameters):** "16/19 identical digests = parameters don't participate." → **[native] REFUTED.** Parameters demonstrably execute: verify-depth ×4 → ops/fact 4.0→7.0; redundancy ×4 → 10.0; audit ×4 → B/fact 202→639. They change cost, not learned state — digest-identity means the extra verification/redundancy found nothing to alter (a weak integrity signal, honestly reported). "Parameter-insensitive above the capacity floor" stands at digest level; the absorption-bar miscalibration is already documented in-verdict.

## 9. Open questions
- B-T1 probe amendment (length-fair relocation + empty-vocab smoothing + dead-last recalibration): needs Micah's dated signature; NOT enacted. **New supporting evidence this session:** the clean-only + empty-vocab-excluded counterfactual satisfies both binding bars (surprise 0.9424 > _4 0.9272 > raw_micro 0.7884 dead last, 9/9) — the FAIL is artifact-driven, strengthening the amendment case. The fair *perturbed* leg still doesn't exist (needs the length-fair relocation design).
- Whether the counterfactuals should trigger a B-T1 re-vote or stand as diagnostic only — coordinator call.
- Scale-up VERDICT.md flaw-coverage annotation ([0,n/4) ids): FAIL-open fix candidate for coordinator.
- Second 6.58M determinism rep: recommended when capacity allows.
- Knowledge-unit bridges (representation↔prose↔memory): unbuilt; testable once Track A closes.
- `bt1_rank.py:44` vocab_probed_code display bug: FAIL-open fix candidate (display-only).

## 10. Knowledge-unit audit (repo-evidenced, cross-workstream)

**Question:** is there a single settled universal "unit of knowledge" for TNN? **Answer: NO — five workstream-local units, no universal unit.** Each is evidenced below with its frozen definition and status.

| Workstream | Unit (frozen definition) | Source | Status |
|---|---|---|---|
| Representation (53 arms + R0) | **Chunk = a byte span with a stable ID** that memory points back to, retrieves, and reuses (Micah's thesis; no fixed tokenizer) | `units/PREREG_FREEZE.md:14-17` | Thesis under test; B-T1 champion predictive_surprise segments. Adaptive MDL repaired 0.8319 (rank 7/11). No blowout winner yet (Track A still running) |
| Prose learning | **LINK = one ID over a non-contiguous span set** (ordered set of fixed spans); WORD UNITS: each distinct token form → u32 id | `prose-learning/PREREG.md:36-42` | v1 pinned path; v3 repair FAILED KB3-VIABLE (2/4) — unit definition not the failure point |
| Coding | **Authored fact tables** (curriculum.json; bug-knowledge gaps found: learner never taught bug principles — 11/11 installed items were correct-code patterns) | `coding/curriculum/curriculum.json`, bug-blindness verdict | Curriculum/integration gap, not a unit-definition verdict |
| Memory (MA1–MA4) | **Slot** = `{live, value, pinned, region, tier, step_added}` — deliberate ops (kill/pin/promote) act on slots | `wave2/memoryagency/MEMORY_OPS.md` | MA1 58/58; MA4 signed values 18/18. Slot is the settled memory unit |
| Imagination | **Scene element** (≤32 per scene, byte arena; machine vs human mode) | `imagination/VERDICT.md:6` | 36/36 scene QA both modes; native emitter delivered |
| Scale-up / few-shot | **Fact** = `(id, value)` with `id = c*M + i` (24 categories); 6.58M facts at 92 B/fact | `scale/corpus/FACTSPEC.md` | Facts are the scale workstream's unit; 1.0 mastery 1→6.58M |

**Cross-unit tensions (honest):**
1. Representation chunks are *byte spans* (contiguous); prose LINKs are *non-contiguous span sets*. A prose LINK is not directly a representation chunk — the composition layer between them is unbuilt.
2. Memory slots hold *values* (i32 judgments), not chunks — how a chunk becomes a slotted memory (the install path) is the web-search-sense-era open problem, not a settled bridge.
3. Scale facts are integer `(id,value)` pairs — the coarsest unit; the scale results (1.0 mastery, linear cost) say nothing about chunk-quality.
4. The B-T1 finding sharpens the representation question: under the frozen probe, *byte identity* (raw_micro) is already a highly stable unit (clean 0.85–0.90). The bar for "cognitive chunking beats bytes" is therefore higher than the R31 calibration assumed.

**Audit verdict [native]:** no universal unit; five local units, each settled inside its workstream, with unbuilt bridges between representation↔prose↔memory. This is a CORRECT state to report (not a failure): the arm battery's job is to name the representation champion; the composition work is downstream. **Not** recommending a forced unification — that would be goalpost-moving. Open: whether the eventual champion chunk can serve as the prose LINK's span primitive (testable once Track A closes).

## 11. Item sweep status

Tracked in `ITEMS_DONE.tsv` (1229 owned items: 436 P0 / 703 P1 / 76 P2 / 14 P3). Final status this session: **P0 436/436 done, P1 703/703 done, P3 14/14 inventoried, P2 37/76 sampled (49%, 0 failures)** — 1,190/1,229 resolved; 39 P2 remain in-progress for the next shift (mandate prescribes sampling; 49% with zero failures exceeds it). Deep HTRF threads: B-T1 re-attack (units/r0 P0 evidence), knowledge-unit audit (cross-workstream P0 docs), scale verdicts (scale/ P0), no-RNG source screen (351 P0 .zag — 17 token hits, all clean), few-shot N=1 native re-verification (byte-identical). Coordinator merges the TSV.

### 11a. Track A arm status board (46 VERDICT.md headline-reviewed 2026-09-22; §7 champion naming pending battery closeout)

| Status | Arms |
|---|---|
| PASS | A, B-16, C-P, C-W, D-T, K2, L1, L2, N, P, U, W, X, Y4, Y6, Z1, Z2, Z7, Z8 (+ partials) |
| KILLED | E, F-B, G2, H2, I1, I2, J2, K1, M, O, T, Y1, Z5, Q |
| PROVISIONAL/BLOCKED/DRAFT | D (DRAFT), D-R (PROVISIONAL), F-S (PROVISIONAL), K3 (PROVISIONAL), R (BLOCKED) |
| NO VERDICT yet | B-8, G1, M2, Y2, Z3, Z4, briefs, harness |

**[native] recording:** no arm self-declares a §7 champion (F-S's "champion" mention is a forward reference to the pending §7 evaluation). The R0 B-T1 champions (predictive_surprise tournament champion; see §6) remain the only recorded tokenizer-replacement champions. Battery-level §7 naming is the coordinator's closeout job.

- **Few-shot N=1 native re-verification (2026-09-22 ~06:35 PDT):** built `scale/fewshot/driver/fewshot_learner.zag` with pinned znc (build warnings only, 11 analyzer notes), ran `eval 1 1 1 1 r ~/workspace/scale/corpus/texts` twice. Results: clean_mastery 1/1 both runs; flaw battery 96/96; ops 5/fact (small-N overhead vs 4.0 at scale); digest fnv1a=44bd2ed473ccfcb2 both runs; logs **byte-identical** minus the SCALE_RECALL_TIMING line (md5 9ddf1c830ee5e090ffd33aaaffea81f3). One-shot learning + determinism at N=1 independently confirmed natively.
- **B-T1 cell reproduction (this session):** synthetic SEG + frozen `bt1_score.py` on sha256-verified corpora reproduces _8/code clean=0.9446 pert=0.3276, _8/prose 0.9419/0.0000, _16/prose 0.9807/0.0000, _16/code 0.9648/0.0000 — all to 4 decimals vs frozen `score_all.log`.
- **No-RNG source screen (this session):** 351 P0 .zag sources scanned; 17 RNG-token hits, all adjudicated clean (comments, frozen-seed deterministic test controls, "seed vocabulary"/"chain seed" terms of art). Zero live RNG in AI decision paths.
