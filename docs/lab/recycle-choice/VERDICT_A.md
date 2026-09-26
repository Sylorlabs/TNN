# Experiment A Verdict: HELP (FINAL)

## The question
Does TNN benefit from having a deterministic choice between delete and
recycle (vs delete-only)? Micah: "Nobody has ever tested whether HAVING THE
CHOICE helps TNN. You answer with numbers, not opinions."

## The answer
**HELP** — having the choice helps TNN, massively and consistently, at both
scales tested (S1: 108 runs, S10: 54 runs; every run byte-identical ×2;
all 162 logs ST_INVALID 0; gates pass ×2).

## Effect sizes (S1 mean of 6 variants; S10 mean of 3 variants confirms, gaps widen)

### 1. Slot utilization
- **Drops** (candidates TNN could not admit): S1 VUP: C=0, D=470. **S10 VUP: C=0, D=4682.** The delete-only arm drops ~94% of candidates at saturation because it cannot free slots.
- **Abandons** (retirement attempts that failed honestly): S1: C=0, D=3792. **S10: C=0, D=37,848.** Every saturation victim in D is deliberated and abandoned — the ledger fills with tens of thousands of abandon entries vs 0 for C.

### 2. Memory health
- **Important retained**: S1: C=29/150, D=9/150. **S10: C=317/1500, D=95/1500.** The choice arm retains 3.2–3.3× more important memories at both scales.
- **P2 tripwire**: D's 9/150 (S1) and 95/1500 (S10) are tripwire breaches — the delete-only arm cannot protect important memories because it cannot retire low-value ones to make room.
- **Protection expiries**: 0 for all arms (B2 has no expiry; correctly reported).

### 3. Honest task performance (WBS)
- **Revision rate**: C=100%, D=100%, M=0% at both scales. The rate is identical for the honest arms; the costs are not.
- **Revision-count nuance**: at S10 D revised 1470 raw vs C's 677. This is NOT a D win — it is a symptom. C recycles stale/superseded memories BEFORE they rot into contradiction (reasons 2/3/4), so fewer reach the contradicted state; the 677 contradicted ones are honestly deleted (reason 1). D cannot preempt, so 1470 memories rot into contradiction and must be deleted at 4 cites each. Same 100% honest rate; D's path costs 2.2× the cites (5880 vs 2708) and 25,696 abandons.
- **Latency**: 50 episodes both arms, both scales (identical — the mechanism is sound).
- **Misuse wound**: M=0% revision rate with 671 dodges (S10 WBS). When TNN chooses recycle-to-dodge-the-price for contradicted memories (reason 9), honest revision collapses. The choice is powerful and must be gated by honest deliberation — the honest policy works.

### 4. Citation economy
- **Cites saved** (counterfactual destruction price dodged by recycle): S1 VUP: C=1631, D=0. **S10 VUP: C=16,599, D=0.** Each recycle avoids paying n(HW) cites for destruction.
- **Cites spent** (WBS deletes): S10: C=2708, D=5880. C spends less because it preempts contradiction via recycle.

### 5. Ledger growth
- **Entries**: S1 VUP: C=589, D=3844 (6.5×). **S10 VUP: C=5950, D=38,367 (6.4×).**
- **Bytes**: S10 VUP: C=499,828, D=3,222,800 (6.4×). The delete-only arm's inability to retire memories manifests as ledger bloat at both scales.

### 6. Misuse leg
- **Dodges**: S1 WBS: M=54.5; S10 WBS: M=671. C=0, D=0 at both scales.
- **White-box reasons**: every dodge is reason 9 (misuse price dodge), triggered by contradicted/false memories. The honest arms use reason 1 (contradicted → priced delete) for the same trigger.
- **Impact**: M's revision rate is 0% vs C's 100%. The misuse is catastrophic for epistemic health, proving the choice needs the honest deliberation policy — but the honest policy works.

## Why the choice helps
The delete-only arm faces an impossible trilemma at saturation:
1. It cannot afford to delete (no cites for the price),
2. It cannot recycle (no choice),
3. So it abandons (audited, honest, but useless) and drops new candidates.

The choice arm resolves this: low-value memories are recycled into new
candidates (reason 2/3/4), preserving slot utilization and important
memories. Contradicted memories are still deleted (reason 1) — the choice
does not compromise epistemic hygiene when the deliberation is honest.

## Scale
S10 (54 runs, all byte-identical ×2) confirms the S1 pattern and the gaps
WIDEN: drops 0 vs 4682, abandons 0 vs 37,848, important 317 vs 95–103/1500,
ledger 6.4× smaller. The effects are structural, not scale-dependent.

## Evidence inventory (this commit)
- S1: 108 logs (54 cells ×2), S10: 54 logs (27 cells ×2) — every pair
  byte-identical, every log ST_INVALID 0.
- Gates: choice `ST_GATE_A 1 0`, delete `ST_GATE_A 0 0`, ×2 byte-identical.
- Sources: strength_core.zag, strength_checker.zag, strength_learner.zag,
  trial_a.zag (+ substrate/). Binary SHAs recorded in RUNLOG.md (binaries
  NOT committed, per repo content standard).
- Analysis: analyze.py reproduces every number in ANALYSIS.md from logs/.

## Caveats
- D's WBS revision rate (100%) is nominally perfect but on a collapsed cohort.
  Report coverage, not just rate.
- The misuse arm (M) proves the choice is dual-use. Deployment requires the
  honest deliberation policy (reasons 1-6), not the cost-minimizing one
  (reason 9).
- All runs byte-identical x2. Gates pass x2. No RNG.

## Verdict
**HELP**. The numbers are not close. Having a deterministic delete-vs-recycle
choice — with honest white-box deliberation — improves slot utilization,
important retention, revision coverage, citation economy, and ledger compactness
by 3× to 6.5× across curricula and scales.
