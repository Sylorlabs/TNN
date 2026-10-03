# NT SYNTHESIS: Negative-Transfer Control under Capacity Pressure

**Status:** This document closes the NT chapter. It is analysis only; no code was produced.
**Date:** 2026-10-03
**Lane:** `docs/lab/research-lead/overnight-20260928/nt_synthesis/`
**Author:** NT-SYNTHESIS worker (analysis worker; all experiments below were run by prior workers)

## Identifier and ledger note (read first)

The NT-era claim numbers below (C404, C407, C412, C416, C427, C431, C437, C439, C445, C448) were claimed in watchdog commit messages during 2026-10-03 but were never written into `canonical_ledger/CLAIM_LEDGER.md`. The ledger file on this branch independently assigns C404 through C410 to different experiments (for example, C404 = MP-2 REGIME-CHANGE, C407 = COMPAUDIT-1; the file tops out at C410 and contains zero NT entries). To avoid identifier confusion, **experiment names are the primary identifiers**; the parenthetical NT-era numbers are disambiguated by name and do not refer to the current ledger entries. No NT claim below should be cited by bare number without its name.

## 0. What this series was about

Negative transfer under capacity pressure: when a learner must retain old knowledge, revise contradicted knowledge, and absorb novelty, all with a bounded memory, does the eviction rule destroy exactly what current experience needs most? The series ran on minimal surrogates (ML1: associative slot memory with entry-local (sup, ref) evidence revision; ML0: overlapping-address ablation), then on the shared continuing-learner substrate (`continuing_learner/contlearn2.zag` skeleton). Families are memorized key/value mappings throughout; this is retention/revision/eviction dynamics, not rule induction. No L2/L3 claim anywhere in the series.

All ten experiments were preregistered, frozen, pure Zag under safebin, pinned znc 2026.07.0-dev, 3/3 byte-identical runs.

## 1. The story: ten experiments, one breaking interaction, two fixes

### 1.1 NT1 (NEGATIVE-TRANSFER-1, NT-era C404): PASS

Without capacity pressure (36 keys, no eviction possible), selective retention EMERGES from the generic entry-local evidence rule with no protection mechanism: 6/6 contradicted keys revised to the B value (c_vb=6/6), 6/6 agreed keys kept, 12/12 untouched keys kept, FORGET=0, nevict=0. Negative transfer in the A→B direction is real but finite and overcome: prior A evidence costs exactly 2 extra passes of ref accumulation before ref > sup fires revision (D=2), then resolves by the same generic rule. The ML0 ablation (overlapping address map) shows the fragility source is ADDRESSING, not the update rule: ML0 revises contradicted keys normally but forgets all 12 aliased untouched keys (u=0/12, forget=12, nalias=12). The apparatus discriminates; the PASS is not vacuous. NT1's preregistered follow-up: test under capacity pressure.

### 1.2 NT2 (NT-CAPACITY, NT-era C407): FAIL

Capacity pressure (CAP=30, 36 active keys, 1.2x) with NT1's generic lowest-net (sup−ref) eviction kills the pattern. K1, K3, K5 hold; K2 and K4 fail. Eviction PREEMPTS revision: a contradicted C key accumulates ref, depressing net to the insertion baseline (sup=2, ref=1 → net=1, tied with just-inserted novel keys), and the frozen lowest-slot-index tie-break evicts it mid-revision; evicted C keys are re-inserted FRESH (sup=1, ref=0), so ref never exceeds sup. Revision can never complete: c_vb=0/6, forget=6, nevict=41 (vs the preregistered 6, itself shown later to be arithmetically impossible). The full 12-bin eviction histogram matched the hand-trace bin for bin (keys 100..105 evicted 5-6x each; novel 134..139 churned; agreed/untouched keys 0x). The evicted set is exactly the working set of ongoing learning: eviction cannibalizes the entries current experience is about. Complementary fragility: ML0 revises contested keys but destroys aliased uncontested keys; ML1 retains uncontested keys but cannot revise contested ones. The failure is diagnostic, not a defect: the two rules are locally consistent but dynamically pathological.

### 1.3 H1 (NT-EVICT-H1, NT-era C412): FAIL

NT2's preregistered first alternative: evict by lowest TOTAL evidence (sup+ref). The rationale was that contested keys carry high total evidence and should be protected during revision. It works during revision (passes 1-2: C keys accumulate ref to totals 3-4, never candidates) but fails AT the revision moment: the frozen revision reset collapses each revised key to (sup=1, ref=0), total=1, the global minimum, and the slot-index tie-break sacrifices it. nevict=40 (prereg predicted 60; the hand-trace missed the REVOLVING DOOR, see 1.4), c_vb=5/6, forget=1 (key 100). H1 fails less badly than NT2 (40 vs 41 evictions, one key forgotten vs six, 5/6 revisions completing vs zero) but the kill bars are not met. Lesson: the breaking interaction is the evidence RESET, not the comparator. But as H3 would show, "the reset" is not one thing.

### 1.4 The revolving door (found in H1, confirmed regime-independent in D1, D2)

Once an eviction+insert lands a low-net entry on the lowest slot index among global-minimum entries, the NEXT insert in the same pass evicts it again. Churn concentrates on one slot per pass instead of spreading (the prereg hand-traces of H1 and D1 both assumed one-for-one swaps and both missed it). Any future bar or mechanism must account for it. The door is benign when the victims are right (D2, FRESHCHURN) and pathological when they are wrong (NT2, D1).

### 1.5 H3 (NT-EVICT-H3, NT-era C416): FAIL (null)

H3 removed the revision reset (revision preserves accumulated evidence instead of resetting to sup=1). Output is BYTE-IDENTICAL to NT2's frozen output (cmp clean; identical run digest `3d33f833...`), because under lowest-net eviction no key ever reaches ref > sup: the revision rule is DEAD CODE. Deleting the reset changes no state transition. This falsifies the parent diagnosis ("the breaking interaction is the evidence reset, not the comparator") for the net-eviction regime: the reset that matters is the EVICTION-REINSERTION reset (fresh sup=1, ref=0 on re-insert), which H3 was barred from touching. H1 and NT2 fail at different interaction points: H1's total-eviction lets revision fire then punishes the reset entry; NT2's net-eviction never lets revision fire at all. No single revision-rule change fixes both. Two further findings: (a) the D1 recommendation, preserve evidence across eviction/re-insertion, the one reset H3 froze; (b) the K2 bar (nevict==6) is arithmetically impossible jointly with K3+K4: 36 keys vs 30 slots forces ≥36 evictions over 6 passes (U keys pin 12 slots under FORGET=0; each pass has ≥6 forced evictions). All future bars derive from this pigeonhole bound.

### 1.6 D1 (NT-D1, NT-era C427): FAIL informative

D1 implements H3's recommendation: a per-learner CHECKPOINT TABLE records (valid, value, sup, ref) on eviction; a re-inserted key RESTORES its prior evidence instead of starting fresh. Learner state only: the checkpoint records the learner's own prior evidence, no oracle/task information, and influences no decision except restoring the re-inserted key's own evidence. K1 and K5 hold; K2, K3, K4 fail (the predicted FAIL direction; the frozen numeric predictions missed the revolving-door concentration, corrected post-hoc bin-for-bin from the rules). The mechanism works: ref accumulates across eviction boundaries (2,2 → 3 > 2), revision fires in pass 3, c_vb 0/6 → 6/6, evictions 41 → 32 (below NT2's 41 and H1's 40; the frozen K2 literal of 36 assumed FORGET=0, D1 achieves FORGET=6, loosening the bound). But D1 RELOCATES forgetting rather than eliminating it: the frozen lowest-net comparator punishes staleness. Once every taught key's net grows past 2, the never-reinforced U keys (frozen net=2) become the global minimum, and 6 of them (112..117) are displaced in passes 4-5. Forgetting is conserved by capacity but moves from contradicted keys (NT2: 6 forgotten) to untouched keys (D1: 6 forgotten). Four hypotheses, four cleanly different signatures from one apparatus: NT2 (41, forget=6 C keys), H1 (40, forget=1 key 100), H3 (null, NT2-identical), D1 (32, forget=6 U keys). D1's preregistered next hypothesis: D2, a comparator that does not punish staleness/contradiction.

### 1.7 D2 (NT-D2, NT-era C431): PASS (first PASS in the series)

D1's preserve-evidence PLUS an eviction comparator blind to staleness and blind to contradiction: EVICT-YOUNGEST (LIFO). Each slot carries an installation sequence number `ins`; the victim is the occupied slot with the greatest `ins` (most recently installed). K1, K2, K3, K4, K5 all hold: c_vb=6/6, FORGET=0, nevict=41 (= 36 pigeonhole minimum + 5 traced revolving-door overhead), all 41 victims novel keys (histogram 133..139), zero A-keys evicted in any pass. Every frozen numeric prediction matched exactly, including the full 7-bin histogram. The necessity argument (preregistered, corroborated): no pure-(sup,ref) comparator can satisfy the three requirements simultaneously, because "untouched" vs "reinforced-novel" (both (VA,2,0)) and "revised" vs "new" (both (VB,1,0) after the reset) are entry-locally IDENTICAL; the tie-break then decides and every tie-break kills something. Temporal metadata is required. FIFO is the anti-D2 (maximally punishes staleness); LIFO is the unique temporal comparator meeting the brief: age is protective (untouched entries are oldest, last evicted), contested entries are old (contradiction does not affect age), and the youngest entries are the least-established claims on their slots (re-insertion cost minimal in a continual-teaching regime). The D2 signature next to NT2's is the series' sharpest moral: the same count (41) with opposite victim sets. The count was never the measure; the victim set is.

### 1.8 NT-PORT (NT-era C437): PORT-PASS

D1+D2 ported to the shared continuing-learner substrate (`continuing_learner/contlearn2.zag` skeleton: associative instance memory, sequential lifetime phases, no resets, no task labels; schema discovery/verify/retire machinery not ported). Realistic continuing-learning sequence: early experience → world change with contradictions → novel experience → untouched old knowledge, 1.3x pressure (CAP=20, 26 subjects). K1-K5 all hold; every frozen numeric prediction matched exactly, including both eviction histograms. MAIN: revision 6/6, FORGET=0, nevict=20 (18 pigeonhole + 2 door), all victims novel subjects 123..129, zero phase-1 subjects evicted. ABL (D1+D2 removed, NT2 comparator): reproduces the NT2 failure signature on the same substrate (c_vb=0/6, forget=6, same count 20, opposite victim set). The NT2 failure mode is substrate-independent; the rules are doing the work, not the substrate or the workload. "Protection without protection rules": no phase-1 subject is ever evicted in MAIN, yet the implementation contains no protection flag, no task identity, no importance logic, only installation order (audit grep clean).

### 1.9 NT-PRESSURE (NT-era C439): PORT-PASS-ALL

D1+D2 at 2x/3x/5x pressure on the continuing-learner skeleton (CAP=20, N=24/44/84 novel subjects). K1-K5 hold at all three points; every frozen numeric prediction matched exactly, including all six eviction histograms. MAIN: FORGET=0, revision 6/6, nevict=62/122/242 (= 3N_n−10, the traced minimum), zero phase-1 subjects evicted across 426 MAIN evictions (phev=0). ABL reproduces the NT2 signature at each point (c_vb=0/6, forget=6, identical counts, opposite victim sets). The tenure structure is scale-invariant in novelty load: the only N_n-dependent quantities are the eviction count and histogram width; every bar-relevant quantity is invariant. The measured breaking point lies BEYOND the probed envelope. The D1+D2 rules do not break by 5x.

### 1.10 NT-LIFOBOUND (NT-era C445): INCONCLUSIVE (honest, preregistered)

The liability probe: novel subjects taught ONCE (no re-teaching), 2x/3x/5x. The fear was that once-taught novel subjects become permanent residents under LIFO, blocking revision of contradicted entries. Dimension A (liability): NO LIABILITY FOUND. K1-K4 hold at all three points: revision 6/6 without any re-teaching, FORGET=0, nevict=20/40/80 (= N_n−4, the pigeonhole minimum for this regime), phev=0 across 140 MAIN evictions. Mechanism: revision is in-place via the frozen evidence update and never requires a slot, so no resident can block it; surviving once-taught novel subjects remain eviction-eligible (youngest-first), not permanent. Dimension B (discriminative validity): NOT ACHIEVED. K5 fails at all points: the ABL arm revises 6/6 with FORGET=0 instead of reproducing the NT2 signature (c_abl=6, forget_abl=0, nevict=21/41/81=N_n−3). The NT2 signature is CHURN-dependent, not a pure function of the eviction rule: without re-teach churn, even lowest-net eviction with no checkpoints completes revision. The no-reteach regime is too easy to discriminate fragility modes. That is an APPARATUS finding, not a D1+D2 finding: it answers the liability question (no) but cannot discriminate fragility modes in this regime (K5). INCONCLUSIVE is the honest limit of this probe, and it is not presented as a PASS.

### 1.11 NT-FRESHCHURN (NT-era C448): FRESHCHURN-PASS-ALL

The preregistered resolution of LIFOBOUND's Dimension B: restore churn WITHOUT re-teaching by supplying FRESH novel subjects each pass (each taught once). At P2/P3/P5 per-pass pressure, K1-K5 all hold at every point; every frozen numeric prediction matched exactly, including all six eviction histograms. MAIN: revision 6/6, FORGET=0, nevict=68/128/248 (= 3N_n−4, the pigeonhole minimum), zero phase-1 subjects evicted across 444 MAIN evictions. ABL: c_abl=0/6, forget_abl=6/6, the NT2 signature RETURNS (nevict=75/135/255=3N_n+3, histogram piling repeated evictions onto contradicted subjects 100..105). Two conclusions: (1) the NT2 failure signature is churn-dependent, not re-teach-dependent (re-teaching was never load-bearing; churn was); (2) LIFO/D2 victim choice is correct under genuine pressure: the fresh novel subjects are genuinely low-value (taught once, never reinforced, never queried), and D2 sacrifices exactly them, youngest-first. The three-battery arc reads: NT-PRESSURE (re-teach churn; K5 returns), NT-LIFOBOUND (no churn; K5 lost; no liability), NT-FRESHCHURN (fresh churn; K5 returns; still no liability).

## 2. The final rule set

Two rules, each addressing one diagnosed breaking interaction. Nothing else changed; revision rule (including reset), update rule, and read rule are frozen throughout.

**D1, preserve-evidence (fixes the eviction-reinsertion reset):** each learner holds a checkpoint table over its key space. On eviction, before the slot is overwritten, write (valid=1, value, sup, ref). On insertion of an absent key, if the checkpoint is valid, install the checkpointed (value, sup, ref) and then process the taught value through the frozen update step; otherwise install fresh (sup=1, ref=0) exactly as before. Checkpoint entries are overwritten on each eviction (latest state wins) and never cleared on restore. The table is learner state (the learner's own prior evidence only; no oracle or task information) and never influences any decision except restoring a re-inserted key's own evidence. Effect: ref accumulates across eviction boundaries, so revision completes in pass 3 instead of being preempted forever. Cost: one checkpointed entry per key slot of the key space, plus one valid bit per entry.

**D2, evict-youngest LIFO (fixes the staleness-punishing comparator):** each slot carries an installation sequence number `ins` stamped from a learner-local `ins_seq` counter at install time. The eviction victim is the occupied slot with the greatest `ins` (most recently installed). Staleness is protective (untouched entries are oldest, hence last evicted); contradiction is invisible to the comparator (a contested entry's age predates the contradiction; the revision reset does not touch age); the youngest entries are the least-established claims on their slots, with minimal re-insertion cost in a continual-teaching regime. The comparator is as generic as the lowest-net rule it replaced: entry-local metadata only, no task identity, no importance flags, no protection rules, no modes. FIFO is its rejected mirror image (maximally punishes staleness).

Both rules are domain-neutral. The series used opaque integer identifiers throughout (keys 100..139 / subjects 100..371; values likewise); no semantic labels, no task tags, no researcher-supplied importance enter the machinery. Whether D1's checkpoint/restore and D2's age comparator behave identically under adversarial identifier permutation was not directly tested (that is the standing domain-blindness gate, not part of this series).

## 3. Validated envelope

| Dimension | Points probed | Result |
|---|---|---|
| Pressure ratio | 1.2x (surrogate, 36 keys / 30 slots), 1.3x (port, 26 subjects / 20 slots), 2x/3x/5x (pressure) | FORGET=0 and revision 6/6 at every point; eviction at the traced pigeonhole minimum each time. Breaking point lies beyond 5x. |
| Churn regime | re-teach churn (PRESSURE), zero churn (LIFOBOUND), fresh-per-pass churn (FRESHCHURN) | MAIN K1-K4 hold in all three; no LIFO liability in any; NT2 signature in ABL requires churn (re-teach or fresh) |
| Substrate | minimal surrogate ML1 → continuing-learner skeleton associative instance memory | Full D1+D2 behavior transfers; NT2 failure signature reproduces substrate-independently in every ABL arm |
| Contradiction | single magnitude (one alternative value per contradicted key) | Untested: graded/partial contradiction |
| Novelty value under churn | re-taught every pass (PRESSURE); taught once, fresh each pass (FRESHCHURN); taught once, retained (LIFOBOUND) | D2 picks the right victims in all three. Untested: reinforced distractors (novel subjects that ARE reinforced but should still lose) |
| Continual lifetime | sequential phases, no resets, no task labels (port/probe skeletons) | Transfers. Untested: interaction with contlearn2 schema discovery/verify/retire; H-CONTLIFE-1 hash-table memory not ported |

Cross-cutting invariants observed at every probed point: learning intact under capacity (K1/TTC never degrades), uncontested retention survives (K3), eviction count alone never discriminates (MAIN and ABL evict the same number; the victim set discriminates), churn is not pathology (churning the wrong entries is), and every frozen numeric prediction of the PASS/PORT-PASS lanes matched exactly, including full eviction histograms bin for bin.

## 4. Verdict ledger (NT series)

| Experiment | Ledger (NT-era) | Verdict | Signature (nevict, c_vb, forget) |
|---|---|---|---|
| NT1 | C404 | PASS | 0, 6/6, 0 (no pressure) |
| NT2 | C407 | FAIL | 41, 0/6, 6 (contradicted keys) |
| H1 | C412 | FAIL | 40, 5/6, 1 (key 100) |
| H3 | C416 | FAIL (null) | 41, 0/6, 6; byte-identical to NT2 |
| D1 | C427 | FAIL informative | 32, 6/6, 6 (untouched keys 112..117) |
| D2 | C431 | PASS | 41, 6/6, 0; all victims novel |
| NT-PORT | C437 | PORT-PASS | 20, 6/6, 0 (1.3x, continuing-learner skeleton) |
| NT-PRESSURE | C439 | PORT-PASS-ALL | 62/122/242, 6/6, 0 at 2x/3x/5x |
| NT-LIFOBOUND | C445 | INCONCLUSIVE | 20/40/80, 6/6, 0; K5 apparatus limit |
| NT-FRESHCHURN | C448 | FRESHCHURN-PASS-ALL | 68/128/248, 6/6, 0 at P2/P3/P5 |

Ten experiments, five FAILs (three mechanism-rejecting, one null, one informative), one INCONCLUSIVE, four PASS-family verdicts. The series followed the frozen rule: each failure's diagnosed cause was addressed by the next hypothesis, and the final combination passes on the production-shaped substrate.

## 5. What is NOT yet proven (honest boundaries)

1. **Beyond 5x.** The breaking point was never found; it was only bounded (beyond 5x pressure). The envelope's far edge is unmeasured.
2. **Graded contradiction.** Every experiment used one full contradiction magnitude per contradicted key. Partial/mixed evidence regimes are untested.
3. **Reinforced distractors.** The "genuinely low-value" boundary was probed for taught-once novelty, but not for novel subjects that ARE reinforced (distractor learning) yet should still lose to older knowledge. This is the sharpest untested form of the D2 liability question: tenure-protection could become a liability if a young entry is genuinely high-value or an old entry genuinely low-value. LIFOBOUND closed the taught-once liability; the reinforced-distractor liability remains open.
4. **Schema interaction.** The port covers the continuing learner's associative instance memory only. contlearn2's schema discovery/verify/retire machinery was not ported; whether D1+D2 interact well with schema formation is untested. H-CONTLIFE-1's hash-table memory was not ported (it would require inventing evidence machinery, a redesign, not a port).
5. **Scale beyond the tested points.** Validated at 36 keys (surrogate) and up to 100 subjects (5x). No claim is made about far larger stores; the series' scaling claim is only that the tenure mechanism is N_n-invariant across the probed range.
6. **Surrogate caveat.** NT1 through D2 ran on minimal surrogates measuring retention/revision/eviction dynamics of memorized mappings; no L2/L3 claim. The port to the continuing-learner skeleton narrows but does not close this gap.
7. **Identifier-blindness of D1/D2.** The series used opaque identifiers, but a dedicated domain-blindness test of the D1+D2 rule set (adversarial relabeling, Micah's 2026-10-03 standard) was not run.
8. **The ledger numbering.** The NT-era numbers were never committed to the canonical ledger and collide with later claims; this document's citations should be read with the Section 0 note.

## 6. Assessment: is negative-transfer control solved for this substrate class?

**Within the validated envelope, yes.** For the substrate class tested (associative instance memory with entry-local (sup, ref) evidence revision, capacity pressure via slot eviction, sequential lifetime phases, single-magnitude contradictions, the three churn regimes), the D1+D2 rule set closes the breaking interaction chain: NT2's eviction-preempts-revision is fixed by D1's evidence-preserving re-insertion; D1's staleness-punishing relocation is fixed by D2's youngest-first comparator; the combination transfers to the continuing-learner skeleton, holds from 1.2x to 5x pressure, holds under re-teach, fresh, and zero churn, and reproduces the NT2 failure signature in ablation arms as the discriminating control at every step. The rule set does this with zero protection machinery: no task identity, no importance flags, no freeze flags, no modes. That is the sense in which negative-transfer control is solved here: the learner retains what is uncontested, revises what is contradicted, and sacrifices only the least-established claims on its slots, with eviction churn confined to re-teachable novelty.

**What "solved" does not mean.** It does not mean all negative transfer: NT1 itself quantified the A→B interference (D=2 extra passes) as real and only overcome, not eliminated, and the series never claimed to eliminate interference during learning, only to control its retention/revision consequences under pressure. It does not mean all memory substrates: schema-forming and hash-table memories are unported. It does not mean all contradiction or novelty regimes: graded contradiction and reinforced distractors are untested. The chapter closes with a solved core and a bounded, named frontier.

## 7. Recommended next work (for whoever reopens this chapter)

1. Reinforced-distractor regime: novel subjects that are reinforced (real distractors) under fresh churn; does LIFO still pick the right victims, or does tenure-protection become a liability? (The sharpest open question, preregistered across D2, PORT, PRESSURE, FRESHCHURN.)
2. Push past 5x toward the actual breaking point of D1+D2.
3. Graded/partial contradiction magnitudes.
4. Interaction with contlearn2 schema discovery/retire on the full continuing-learner substrate.
5. Domain-blindness battery for the D1+D2 rule set (adversarial identifier relabeling).
6. Reconcile the NT-era ledger numbers with the canonical ledger (Section 0).

## 8. Provenance of this document

- Analysis only; no code was written, compiled, or run for this synthesis. No toolchain beyond file reading and git archaeology.
- Every experiment summary above is sourced from the frozen REPORT.md files in their lanes: `negative_transfer/`, `nt_capacity/`, `nt_evict_h1/`, `nt_evict_h3/` (retrieved from git history, commits 64aa3bccd, d1d55de31, 77cc20b59, bc018d84d), and `nt_d1/`, `nt_d2/`, `nt_port/`, `nt_pressure/`, `nt_lifobound/`, `nt_freshchurn/` (current worktree, this branch). Numbers, digests, and verdicts are copied verbatim from those reports.
- Ledger-number claims (NT-era C404-C448) are sourced from watchdog commit messages in git history; the collision with the current ledger's C404-C410 is verified against the current `canonical_ledger/CLAIM_LEDGER.md` and reported in Section 0.
- No em/en dash bytes (per the loop documentation style rule).
- This document lives in the new lane directory `docs/lab/research-lead/overnight-20260928/nt_synthesis/` on branch `lane-gennm10-20261003`. Committed locally with an explicit pathspec; never pushed.
