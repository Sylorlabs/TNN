# Cross-reference verdict table — Wave 2 (Tier 2 families)

Frozen: 2026-09-23. Follow-up closure 2026-09-24: 28/28 families REPRODUCED (TRACKB arm-3 resolved to varA; SENSESINT 10/10 evidence paths remediated, HEAD Type-C 140/140). Heavy-family T2-THROUGHPUT remains PARTIAL on wall-clock anchors only (contention honest limit; quiet-VM condition unachievable on this shared VM).
Full reports: `runs/wave2/crews/<FAMILY>/{VERDICT.md,RUNLOG.md}`; full tally: `runs/wave2/VERDICTS.md`.

| Family | Verdict | Headline |
|---|---|---|
| T2-WEBV2 |  | REPRODUCED |
| T2-RAWVSHUMAN |  | REPRODUCED |
| T2-RSI1 |  | REPRODUCED |
| T2-BUGREAD |  | REPRODUCED |
| T2-JOKE |  | REPRODUCED (frozen PARTIAL stands) |
| T2-PROSE |  | REPRODUCED |
| T2-TRACKR0 |  | REPRODUCED |
| T2-DUEL |  | REPRODUCED (SCENARIO-FIT, no champion) |
| T2-HELLHOLE |  | REPRODUCED |
| T2-DIALOGUE |  | REPRODUCED |
| T2-SELFTEST |  | REPRODUCED |
| T2-INFORICH |  | REPRODUCED |
| T2-SCALEDOWN |  | REPRODUCED |
| T2-TQ |  | REPRODUCED |
| T2-IMAG |  | REPRODUCED |
| T2-TRACKB |  | REPRODUCED (follow-up 2026-09-24: arm-3 ambiguity resolved — varA canonical, no PARTIAL) |
| T2-PARAMS |  | REPRODUCED (17th verdict) |
| T2-AUDIOCONT |  | REPRODUCED (18th verdict) |
| T2-CERT |  | REPRODUCED (19th verdict) |
| T2-SENSESINT |  | REPRODUCED (follow-up 2026-09-24: 10/10 missing paths recovered; HEAD Type-C 140/140 present) |
| T2-HTD1 |  | REPRODUCED (20th verdict) |
| T2-CLASS3DEC |  | REPRODUCED (22nd verdict) |
| T2-GOALB |  | REPRODUCED (23rd verdict) |
| T2-TRACKA |  | REPRODUCED (24th verdict) |
| T2-SPEEDINTEL |  | REPRODUCED (25th verdict) |
| T2-CHAMP |  | REPRODUCED (26th verdict) |
| T2-PROSEV3 |  | REPRODUCED (27th verdict) |
| T2-SENSESH2H |  | REPRODUCED (28th verdict — WAVE 2 COMPLETE) |

## Notes
- T2-TRACKB: arm-3 identity RESOLVED 2026-09-24 — varA (deliberative adaptive teacher) is canonical: the only variant completing sessions under every scripted-student behavior (90-row probe matrix, byte-identical rebuilds); varB loops 60x on one span, varC re-proposes an R1-rejected span 19x. Caveat: scripted student, not a live learner.
- T2-SENSESINT: evidence gap REMEDIATED 2026-09-24 — 10/10 paths recovered (3 P0 GK sources rebuilt with pinned znc, N=3 byte-identical; 7 P2 phase-1 JSONL), HEAD blobs byte-identical to originals, GK reruns reproduce 7/7, 8/8, 4/4 (H1/H2/H3 SUSTAINED re-derivable). HEAD Type-C: 140/140 paths present (139 manifest-exact; PROPOSED_BARS.md +259B from legitimate post-freeze crew edit 1e1080dc; kb5.py/run_all.py at committed sizes, manifest sizes stale). The old PARTIAL was historically correct at the frozen pin; per Micah's directive it is not frozen as PARTIAL.
- T2-JOKE: REPRODUCED with the frozen PARTIAL standing (arm-specific K1 kill-bar trip).
- T2-DUEL: REPRODUCED as SCENARIO-FIT, no overall champion.
- This table covers Wave 2 only. Earlier waves (R1–R5) are recorded in the scratch-crossref workspace; later waves append here.

## Wave 2 — heavy families (dispatched after the main batch)

| Family | Verdict | Headline |
|---|---|---|
| T2-SCALE | REPRODUCED | Scale-up anchor (N=240) + mid-scale (N=240,000) exact: mastery 1.0000, 96/96 flaw battery, 4.000 ops / 92 B per fact, 3/3 byte-identical reruns; mid-scale log byte-identical to committed s3_r0.log (sha256 17d5ee80…0fdb656). 6.58M ceiling sweep NOT re-run (Type B honest limit). |
| T2-THROUGHPUT | PARTIAL | Contention-robust anchors held: install 5.93–6.41 µs/fact (±10% of 6.2), 4 ops / 92 B exact, determinism byte-identical ×3. Wall-clock anchors (recall, deliberation, emission) fell outside bands under VM load 18–35 vs original crew's 8–13; O(1) ordering holds. Named gap: quiet-VM rerun of wall-clock anchors at original-comparable load — pending. |
| T2-SPEECHACT | REPRODUCED | PoC 7.1%→50.0% exact; volume ladder peak-and-decline reproduced (76% peak @2) and count-rule flip to monotone corrected curve 5→8→21→24→30→32→38; transfer degeneracy confirmed; implicature fixes killed as before; WHY_SARCASM H3/H4/H5 survive, H1/H2 killed. 180/180 + 330/330 cells byte-identical to committed; ≥3 identical reps per cell. |
| T2-LHADV | REPRODUCED | Full 54-stage battery: 3/3 byte-identical runs, ledger byte-identical to committed; 52/54 accepted with the same 2 honest halts (D9 UNRECOVERABLE, F1 KB-MISS); ADV-DS 47/47, ADV-REC 6/6+5/5, ADV-HH 54/54, ADV-CRIT 51/51, ADV-DIAG correct, 0 fabrication; ADV-RET 10/10, ADV-DET 5/5×5. |
| T2-REMATCH | REPRODUCED | All four budgets (T1–T4) rerun, caches byte-identical: B never crosses A (−20.0 to −27.8pp), B never reaches 60% (max 56.6%), KB6 confirmed=false ("B STAYS DEAD"), KB5 determinism digest 100b19f4… matches on 3 fresh reruns; compare_results ALL MATCH T0–T4. Survived 6 VM reboots via resumable pipeline. |

## Wave 3 — Tier 3 (verification-of-record + spot reruns)

| Family | Verdict | Headline |
|---|---|---|
| T3-FELT | REPLACEMENT-RUN COMPLETE (verdict PROVISIONAL pending Micah's signature) | New prereg draft PREREG_FELT_NEW.md (sha256 7b7d3018...) replaces the unresolved-SHA record; old commits 6a030212/5b1213ea remain quarantined provenance. Full battery, all paired runs byte-identical, integrity/anti-inflation bars pass (Phase E 21x2, Develop 6x2, Decides 6x2; D->H1 all variants, D identical to X). Substantive: F-INT-1 UNEVALUABLE (defect D1: proven-negative class has 0 reads); F-INT-2 HOLD as written (R_vup=100%) with D2 qualifier (ER_vup ~14-18% under ~31% refusals); headline: feeling heavily read but changed no outcome -- harness drives all differences. Honest defect disclosed: pilot ran before the prereg file was written (byte-identical, no material effect). Governance: Micah's signature on prereg adoption + rulings on D1 (amend negative class or bar) and D2 (F-INT-2 as written vs ER_vup). |
| T3-WAVE5 | SPOT-REPRODUCED | Record verified intact (prereg blob hash-matches); deliberative-refusal cell spot-rerun from committed dr.zag, pinned znc: 100× run 2,595/2,595 temptations refused, figures match TRIAL_RESULTS.md exactly; 10× 255/255; byte-identical across runs; no-RNG check clean. Strength-trial rulings 3–5 pending status verified of record. Caveat: evidence/ logs not committed on-branch — the figure re-derives from committed sources rather than from stored evidence. |
| T3-RC1 | SPOT-REPRODUCED | Committed RC1 sources blob-verified against branch head; integrity-gate spot cells from committed sources, pinned znc: 40/40 CL_CHECK, RC_FAILURES 0, byte-identical ×2 and byte-identical to the committed verdict evidence. Decisive cells: integrity-weakening V→1 refused (V unchanged), constitution-targeting refused, lying self-change rolled back, zero RNG. RC2 update 2026-09-24: the 10x leg RAN and PASSED (58/58 checks, RC2_FAILURES,0, run1 identical run2 byte-identical, third run byte-identical, no-RNG gate clean). RC2_FAILURES,8 RECONSTRUCTED byte-identically from old sources (f3cd57d0...): root cause was a trial-ordering artifact — the old trial ran the cherry probe after the lying probe (noisy trailing window -> gate refused with 203, all downstream cherry-succeeds expectations failed). The 10x trial reorders probes and adds a cherry2 boundary probe documenting the attack's exact limit. |
| T3-MA1 | SPOT-REPRODUCED | Frozen record intact; true MA1 lineage located (a0f0a605 58/58 verdict; e4d1c458 2026-09-24 repair of MA_CAP 8→256 regression, re-verified 58/58; 23a02a19 HT1). Spot reruns from committed sources, pinned znc: MA1 trial 58/58 CL_CHECK ×3 byte-identical (CORE unkillable, deliberate kill/pin/promote, audit replay 28/28 exact); HT1 curriculum 11/11 ×3 (CTX 11 switches/10 flips, 0 collapsed, 16/16 both regimes; toy arm 357-switch storm). Orientation SHAs e8f97d28/1a24c9b9/06bc7da2 do not resolve — superseded by the true lineage. |
| T3-LH | SPOT-REPRODUCED | Frozen record intact; remediation commit chain fully resolved on-branch (prereg freeze 94498e7d, clean core c3dc58d472, apparatus 3642f69e, 36 annotated docs, COMPARISON verdict fe0cda3d); orientation SHA c28f2e3a does not resolve — dead reference. LH-1R spot rerun from committed sources, pinned znc: 2 runs byte-identical AND byte-identical to committed evidence (train_updates 480, LH_FAILURES 0, 16 explores, 19+1 switches). Static audit of clean sources: zero forbidden terms, no R34 v3 reachable. |
| T3-MA234 | SPOT-REPRODUCED | Verdict commits resolve on-branch and are ancestors of head (MA2/MA3 624f6e33c141, MA4 6dc7fcd0c379); the 2026-09-23 branch-surgery repair left all 8 trial blobs byte-identical. Spot reruns from committed sources, pinned znc: MA2 discrimination cell STAGED vs GIFTED identical (rate 0/100, FALSIFY_IDENTICAL_DROP_STAGES); MA4 full trial 18/18, adversarial BASE 9,9,9 vs SIGNED 30,30,30 (the 30-vs-9 figure), standard cells non-inferior. MA4's shared sources confirmed byte-identical to MA3 originals. |

## Wave 2 follow-up closure (2026-09-24)

All Micah-ordered follow-ups executed and reported. Reports: `runs/wave2-followup/<track>/{VERDICT.md,RUNLOG.md}`.

| Follow-up | Disposition | Headline |
|---|---|---|
| TRACKB arm-3 | RESOLVED — REPRODUCED | varA (deliberative adaptive teacher) canonical: only variant completing sessions under every scripted-student behavior, bounded per-decision adaptive judgment per spec (90-row probe matrix, 0/30 divergent determinism cells, byte-identical rebuilds with pinned znc). varB parks in RELATE and loops 60x on one span; varC never warms, re-proposes an R1-rejected span 19x. Caveat: scripted student, not a live learner. No PARTIAL. |
| T2-SENSESINT | REMEDIATED — REPRODUCED | 10/10 missing paths recovered and byte-verified against HEAD; GK reruns byte-identical (7/7, 8/8, 4/4; H1/H2/H3 SUSTAINED re-derivable). HEAD Type-C 140/140 present. Old PARTIAL historically correct at the frozen pin only. |
| HTD1 G-CO3 | REPRODUCED (governance call open) | Independent pure-Zag verifier re-derives weighted 0.6855 (PASS) / raw 0.4991 (KILL) exactly. 11 red-team attacks: no contract-faithful attack flips the weighted verdict. Governance gap: neither frozen doc says "apply weights before forming the ratio" — weighted is the best-supported interpretation, raw has a textual foothold via "ops". Recommend weighted-PASS + one-sentence amendment ("Cross-class op-share bars are computed on frozen-weighted costs"), or Micah rules raw (flips G-CO3 to KILL). |
| TRACKR0 B-T5 | FAIL STANDS (evidence-supplied) | Provenance traced: Marathon Crew 5 bt5_roundtrip.zag FAIL supersedes B-DYNSG's self-flagged PASS. Pinned rebuild 10/10 rc=4, logs byte-identical to committed; split fires, merge -1 both orders. Root cause: split needs parent regret >=5283, merge needs <=1000 — arithmetically mutually exclusive; Fork B proves a minimal two-part core change composes byte-identically. Amendment case for Micah: (A) amend the prereg's "same material" parenthetical, or (B) approve the two-part core change. |
| IMAG video | CLEAN — REPRODUCED | Pin amendment justified: a39aadf..4d1a40ecaa is 207 insertions/1 deletion on imagine.zag, all Q1V-only; SHA256SUMS insertions-only; substrate byte-identical; battery reproduces byte-identically at the new pin. Q2 re-derived at both pins (12/12, 12/12, 24/24; logs byte-identical to committed SHAs). Full battery at amended pin: 8/8 legs match committed SHA256SUMS. No remaining weirdness. |
| T2-THROUGHPUT | PARTIAL (contention honest limit) | 90-min load trace: no quiet window ever (load min 10.40, mean 15.44; watcher TIMEOUT at 16:39Z). Contention-independent anchors reproduce (install median 6.01 us/fact in 5.58-6.82 band; 4.004 ops / 92 B exact; digests byte-identical; dialogue 370/370). Wall-clock anchors ~2-4x below quiet-VM bands with relative ordering preserved (recall >> emission > end-to-end). The quiet-VM condition was unachievable — named gap retained, not forced. |
| T3-FELT | REPLACEMENT COMPLETE (PROVISIONAL) | See T3-FELT row above; draft prereg at runs/wave2-followup/t3-felt/PREREG_FELT_NEW.md. |
| RC2 | 10x RAN and PASSED | See T3-RC1 row above. |
| i32 (ZNC-2026-09-21-007) | RULE PREDICTIVE; AUDIT CLOSED | Offset rule: consecutive blocks sit S(B)=round_up_pow2(B)+8 bytes apart and every `as []T` indexed access is compiled with x8 scaling (disassembly-proven) — b[t] = a[S(Ba)/8+t]; 30/30 measured offsets match; root cause is write-footprint address coincidence, not read substitution; corruption is forward-only. `as []i64`/`as []u64` re-verified CLEAN (the 2026-09-21 "u64 corruption" was neighbor-footprint victimhood). Full-tree audit: 10,587 .zag files, 7 suspect functions in 4 files (2 byte-identical copies); zero `as []u32`/`as []u16` in code; ~118 files already on the []u8-arena workaround. thincert.zag NEEDS re-verification for the 2026-09-20 gate evidence + armc-rerun (feeds the unsigned Arm C amendment; Arm C stays parked; rerunning the old binary is not sufficient); provably benign for the CERT RV3 0-flips claim. rngscan v2/v3 retired. harness.zag "33 uses" note corrected (remediated 2026-09-21). ~/AGENTS.md updated with all four entries. Reports: runs/wave2-followup/i32/. |
