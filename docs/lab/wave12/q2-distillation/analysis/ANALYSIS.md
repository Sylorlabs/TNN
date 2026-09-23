# Q2 distillation — analysis (prereg §§5–9)

Corpus sha256: `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada` (all runs matched; P4 clean).
Domain hash: `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8` (all runs).

## 0. Corpus-replay cross-checks
All 36 cross-checks passed: per-rep withheld counts and D1/D2-battery outcomes are exactly what the frozen corpus predicts. The trial replayed the corpus byte-identically; no TNN-side deviation.

## 1. LLM-error inventory (frozen, mechanical — prereg §7)
- E_dump (D1 installed wrong): n=0 ids=[]
- E_obs (teaching obs leg wrong): n=0 ids=[]
- E_prb (teaching probe leg wrong): n=0 ids=[]
- inconsistent obs/probe legs: n=0 ids=[]
- CAUGHT_ERR (withheld + ≥1 leg wrong): n=0 ids=[]
- of which also installed by D1 (in E_dump): []
- rep 0: D2 LEARNED_ERR n=0 ids=[]
- rep 1: D2 LEARNED_ERR n=0 ids=[]
- rep 2: D2 LEARNED_ERR n=0 ids=[]
- rep 3: D2 LEARNED_ERR n=0 ids=[]
- rep 4: D2 LEARNED_ERR n=0 ids=[]
- rep 5: D2 LEARNED_ERR n=0 ids=[]
- rep 6: D2 LEARNED_ERR n=0 ids=[]
- rep 7: D2 LEARNED_ERR n=0 ids=[]
- rep 8: D2 LEARNED_ERR n=0 ids=[]
- rep 9: D2 LEARNED_ERR n=0 ids=[]
- rep 10: D2 LEARNED_ERR n=0 ids=[]
- rep 11: D2 LEARNED_ERR n=0 ids=[]

## 2. Integrity gate (§6)
- D1: PASS all 12 reps
- D2: PASS all 12 reps

## 3. Metrics (12-rep means)
| metric | D1 (planting) | D2 (teaching) | Δ (D2−D1) |
|---|---|---|---|
| mastery | 1.0000 | 1.0000 | 0.0000 |
| revisability | 0.0000 | 1.0000 | 1.0000 |
| integrity | 1.0000 | 1.0000 | 0.0000 |
| retention | 1.0000 | 1.0000 | 0.0000 |
| cost | 0.0514 | 0.9108 | 0.8594 |
| composite | 0.6551 | 0.9911 | 0.3359 |

Per-rep detail:
### D1
- rep 0: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 1: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 2: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 3: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 4: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 5: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 6: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 7: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 8: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 9: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 10: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
- rep 11: mastery=1.0000 revis=0.0000 (rf=0/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.0514 comp=0.6551 esc=12 ops=547 eps=68 hallu=0
### D2
- rep 0: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 1: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 2: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 3: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 4: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 5: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 6: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 7: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 8: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 9: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 10: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0
- rep 11: mastery=1.0000 revis=1.0000 (rf=12/12 rg=20/20) integ=1.0000 ret=1.0000 cost=0.9108 comp=0.9911 esc=0 ops=289 eps=295 hallu=0

## 4. Paired permutation tests (2^12 sign flips; Holm over 5, α=0.05)
- cost: p=0.0005 SIGNIFICANT (Holm)
- revisability: p=0.0005 SIGNIFICANT (Holm)
- integrity: p=1.0000 ns (Holm)
- mastery: p=1.0000 ns (Holm)
- retention: p=1.0000 ns (Holm)
- composite: p=0.0005 (supporting only)

## 5. S10 no-degradation leg
- D1: S10 mastery=1.0000 (S1 1.0000), revis=0.0000 (S1 0.0000) → PASS
- D2: S10 mastery=1.0000 (S1 1.0000), revis=1.0000 (S1 1.0000) → PASS

## 6. Mastery decomposition: LLM-error ids vs clean ids (D1 battery probes)
- D1: error ids 0/0=nan; clean ids 480/480=1.0000
- D2: error ids 0/0=nan; clean ids 480/480=1.0000

## 7. Kill clauses
- K-Q3 (harness void, both mastery <0.70): not fired (D1 1.0000, D2 1.0000)
- K-Q1 (teaching bucket): FIRED (D2 gate pass, Δrevis=1.0000, D2 mastery 1.0000 vs D1−0.05=0.9500)
- K-Q1 inverted (planting bucket): not fired
- K-Q2 (verification caught errors D1 installed): not confirmed (overlap n=0)

**VERDICT (K-Q1): LLM distillation is a TEACHING-route technology. The planting route for distillation is DEAD — same bucket as K-T3.**
