# GOVERNANCE AUDIT: DDES 11-step promotion pipeline (step 11)

Wave: wave-20261002-1121pdt. Lane: DDES. Queue item 5(b).
Auditor: the wave-20261002-1121pdt DDES lane worker (did not author the
repair; authored the step-10 red team and OOD probe in this wave).
Scope: the DDES lineage culminating in the t*=0 soundness repair R2
(ddesr2.zag). Every commit cited below was verified to exist via
git cat-file; every prereg/implementation ordering was verified via
git merge-base --is-ancestor (all ORDER-OK).

Prior assessment: b75886067 (2026-09-30, "DO NOT PROMOTE, 5 of 11
steps incomplete"). This audit supersedes it with the evidence that
has landed since.

Note on a similarly named artifact: 3420bff8e (ddesp2.zag, K-G1..K-G9
sealed evaluation, "ddes V2 steps 7-11 BUILD-PASS" per 947675258) is a
SEPARATE artifact from the t*=0 repair line audited here
(ddesr2.zag, K-R2.1..K-R2.6). Its steps 7-11 claim does not transfer
to the repair. This audit covers the repair line only.

Binding caveats (restated; they bind every citation): (1) "a menu of
size 2 reproduces the sealed phase-2 outputs"; (2) "World G is
signature-identical to F by prereg design"; (3) "the
derivation-to-record binding is enforced by offline reviewer checks
only".

## Step table

| # | Step | Status | Evidence (commits) |
|---|------|--------|-------------------|
| 1 | Committed preregistration | COMPLETE | d42294620 (builder prereg K-NX1..K-NX8, V-NX1..V-NX3, frozen before implementation; order-verified ancestor of 56db8d606). Repair preregs: 0f10fd0f2 (R1) and d31e901b0 (R2, K-R2.1..K-R2.6, committed alone; order-verified ancestor of b42b10db5). |
| 2 | Implementation | COMPLETE | 56db8d606 (BUILD-PASS 9/9; pure Zag; 3/3 byte-identical). Repair: 17c97a2cd (R1 REPAIR-PASS 11/11) and b42b10db5 (R2 re-implementation; 3/3 byte-identical 297d0b59; World F correct both configs; A-E byte-identical to DDES_RAW.txt). |
| 3 | Sealed evaluation | COMPLETE with noted bound | 56db8d606 carried DDES_RESULT.md (9/9 on frozen A/B plus sealed C/D/E; adversary added sealed World F, 11/11 on repaired binary). Deferred K-NX3 L>=8 sealed depth run: partially addressed since (step-7 O2 ran t*=12, 71aa55a87), but no dedicated L>=8 depth cell on the repair binary itself. Bound stated, not hidden. |
| 4 | Independent reproduction from committed source | COMPLETE | 838b8498a (wave-20261002-0221pdt; prereg 7dc99b131 frozen alone first, order-verified). A non-author party rebuilt from committed source and reproduced byte-identical outputs. |
| 5 | Simple-baseline comparison | COMPLETE | 838b8498a (BASELINE_COMPARISON.md; random/enumeration baselines incl. ddes_randbase.zag vs guided DDES on sealed worlds). |
| 6 | Alternative-explanation attack | COMPLETE (attack executed; verdicts narrow the claim) | Adversary K1 in e40bdfc9b (hidden-enumeration audit: ATTACK-FAILS; zero-enumeration claim stands). Second attack DDES-ALT: prereg d64688fa6 (alone, order-verified), implementation dd7cb640d, results 3914960cf: H1 ATTACK-SUCCEEDS (repair's decision substance is the clamp alone; FLAG unconsumed), H2 EVIDENCE-HOLDS (guidance_exclusive=2), H3 ATTACK-SUCCEEDS (RT2 loud failure is contract x clamp interaction, not boundary detection). The step was executed per prereg; its successes are BOUNDS on interpretation, recorded here, not hidden. |
| 7 | OOD test | COMPLETE | 71aa55a87 (SEALED_EVAL.md; prereg ac7cc6856 frozen alone, order-verified; 6 sealed OOD worlds O1-O6 incl. two-hop chains, t*=12, competing frontiers, fan-in, decoys, t*=0 negative control; 3/3 byte-identical f7a7ec52; BUILD-PASS). This wave adds 4 more OOD worlds (P1-P4, OOD_PROBE.md, 8/8 cells). The 09-30 "broader OOD suite" item (beyond 3-variable timing worlds) remains open as future work; the step as defined is complete. |
| 8 | Ablation | COMPLETE | 71aa55a87 (ABLATION.md; same frozen prereg; 5 controlled variants x 6 worlds; C1 clamp LOAD-BEARING, C2 t*-derived waits LOAD-BEARING, C3 earliest-frontier PARTIALLY-LOAD-BEARING; 4 kill bars HOLD; BUILD-PASS). |
| 9 | Transfer/reuse test | MISSING | No evidence found in the lane history: DDES guidance machinery has never been applied outside the 3-variable rule-delay domain (no new action vocabulary, rule format, or domain). The 09-30 assessment flagged this; nothing has landed since. This is the blocking step. |
| 10 | Independent red team | COMPLETE (this wave) | Prior: e40bdfc9b attacked the UNREPAIRED build (K2 ATTACK-SUCCEEDS, the t*=0 hole; stale for the repair per the 09-30 assessment). This wave: PREREG_DDES_RT10.md frozen alone at dd5d92f63, implementation ddes_rt.zag (mechanism diff-empty vs b42b10db5), REDTEAM_STEP10.md: 4 adversarial post-repair t*=0-adjacent worlds, 3/3 byte-identical a8b1ce04, all kill bars HOLD, verdict SURVIVES with the RT4 bound documented and queued. |
| 11 | Governance audit | COMPLETE (this document) | This audit: all 17 cited commits verified to exist; all 5 prereg/implementation orderings verified ORDER-OK; purity and determinism re-verified on this wave's artifacts (RT-K5/K6); disclosures carried below. |

## Purity, determinism, and disclosure ledger

- Pure Zag: this wave's artifacts (ddes_rt.zag, ddes_rt_bin, 3
  transcripts) built and ran under the safebin PATH with
  `which python3` resolving to nothing (Step 0 recorded in
  NAMECHECK.md before any work). Zero Python at any stage.
- Determinism: 3/3 byte-identical transcripts (sha256
  a8b1ce04009698b0f6c698937c6a502cc5f47ed6b16d814050430f451ce2a780),
  exit 0, zero stderr bytes every run.
- Dash scan: check_no_dash.sh clean on all committed lane files
  (run before each commit).
- Carried disclosure (from b75886067): the original builder
  disclosed a single Python use for an em-dash byte check, redone
  with shell tools; contained, not in artifacts. No new Python
  disclosures this wave.
- Commit hygiene: prereg dd5d92f63 committed alone; implementation
  and results committed after (ordering to be verified via
  merge-base before the verdict is reported; see REPORT.md).

## Verdict

10 of 11 pipeline steps are COMPLETE for the t*=0-repaired DDES
lineage. Step 9 (transfer/reuse) is MISSING and is the sole
blocker. Recommendation unchanged in substance from b75886067 but
narrowed: HOLD at BUILD-PASS plus REPAIR-PASS plus STEP-10
SURVIVES; DO NOT PROMOTE to SURVIVES until step 9 lands
(transfer probe of the guidance machinery to a new vocabulary,
rule format, or domain, preregistered and frozen before
implementation). DDES stays bounded L2 throughout; nothing in
this audit supports an L3 reading, and the DDES-ALT H1/H3 bounds
(the clamp does the work; no boundary reasoning) are part of the
audited record.
