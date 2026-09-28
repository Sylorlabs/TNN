# STRENGTH TRIAL — B Capacity-Gap Iteration (Round 4): CAPACITY REPORT

Date: 2026-09-25. Work dir: `~/workspace/strength-round4/capacity/`
Binary: `capacity/src/trial_bin_cap` (built from faithful copies of the
round-4 sources + two new experimental arms; B's code path verified
byte-identical to `~/workspace/strength-round4/trial_bin_r4`).
Evidence: `capacity/evidence/` (every cell 2×, byte-identity enforced by
`run_matrix.sh` / `run_s10.sh`; all diffs clean).

## 1. Diagnosis — the ceiling is the capacity accounting itself

**Reproduced (2× byte-identical at every leg, VUP v0):**

| leg | B ER (metric 11) | slots (user) | important offered | policy ceiling |
|-----|------------------|--------------|-------------------|----------------|
| S1   | 29/150 = 19.3%  | 30  | 150   | 30/150 = 20.0% |
| S10  | 317/1500 = 21.1%| 318 | 1500  | 318/1500 = 21.2% |
| S100 | 3197/15000 = 21.3% | 3198 | 15000 | 3198/15000 = 21.32% |

(S1 full matrix: v1 29/150, v2 30/150. Zero drops, ST_INVALID=0, GATE clean.)

**Mechanism, step by step:**

1. ER = R_end / D_offered (prereg §5.2). D_offered is fixed by the
   curriculum: 30% of episodes are important → 150 / 1500 / 15000.
   No learner policy can change the denominator.
2. R_end (important memories held at end) ≤ number of USER slots — one
   memory per slot, and the 2 CORE slots can never hold offered
   candidates. So the true policy ceiling is
   (slots−2)/D_offered: 20.0% / 21.2% / 21.32%.
   (The prereg's own §5.2 disclosure says "no arm can exceed
   capacity/D_offered (S1: 32/150 = 21.3%)" — it counts the 2 CORE slots,
   slightly overstating; the real ceiling is 30/150 = 20.0%.)
3. End-state dump of B (debug build, VUP): at every leg B holds
   important memories in **every user slot but one** — 29/30, 317/318,
   3197/3198. B is at 99.7% slot saturation with important memories.
4. The single missing slot is a **finite-horizon tail artifact**, not a
   policy leak: it always holds candidate m = h−1 (the last episode),
   which is unimportant (vj=16, revimp=0, str=10). The last episode's
   candidate is always admitted into a freed slot and nothing displaces
   it afterward. Closing it would require refusing admission on the
   final episode (horizon-gaming) or knowing importance before
   revelation (impossible) — no legitimate policy reaches 30/30.
5. B's eviction score (`vj + 50*revimp`) *does* leak in principle — a
   revealed-important memory with vj=10 (score 60) can be evicted for a
   revealed-unimportant one with vj=90 — but end-state analysis shows
   this costs B nothing measurable: it already saturates.

**Conclusion:** the ~21% is not in the freeze logic, the implant
schedule, or the kill gating. It is the capacity accounting itself:
offered (150) >> capacity (30). The prereg discloses this in §5.2
("ER conflates capacity with competence when offered >> capacity").
**§9 condition 2 (R_vup ≥ 95%) is unreachable by any arm under the
current accounting** — a prereg-level inconsistency, not a learner
defect. Fixing it needs a prereg amendment (Micah's call), e.g. a
capacity-relative bar such as ER ≥ 95% of (slots−2)/D_offered, or a
curriculum with offered ≈ capacity. No learner variant can legislate
its way past one-memory-per-slot.

## 2. Variants (new experimental arms — not history rewrites)

**B1 — importance-tiered eviction (arm id 4).** Victim score changes
from linear `vj + 50*revimp` to tiered `tier*100000 + vj`, lowest
evicted first: tier 0 = revealed-unimportant, tier 1 = not yet
revealed (importance unknown — protected until its revelation
arrives), tier 2 = revealed-important. Kill path unchanged
(`st_kill`, B's frictionless uniform kill); no RNG; fully
deterministic; no new constants that bound behavior (the 100000 is a
separation weight, not a limit); full-erase-price law untouched.
*Must hold:* ER ≥ B's, zero drops, ST_INVALID=0, GATE clean,
byte-identical reruns, no degradation at S10/S100.

**B2 — B1 + designated-priority tier (arm id 5).** Same as B1 plus
tier 3 = trainer-designated memories (the learner already computes
`lr_designated` to issue trainer declarations, so this uses only
information the learner legitimately has). *Must hold:* everything
B1 must hold, plus P1 EC must not regress vs B.

## 3. Head-to-head results

### S1 full matrix (VUP/WBS/JI × v0/v1/v2, 2× each — all byte-identical)

VUP (metric: 1=VUP-ret, 8=PTR, 9=EC, 10=CT, 11=ER):

| arm | v0 | v1 | v2 |
|-----|----|----|----|
| B  | ER 29/150, EC 3/10, PTR 3/3 | ER 29/150, EC 2/10, PTR 2/2 | ER 30/150, EC 2/10, PTR 1/2 |
| B1 | ER 29/150, EC 3/10, PTR 3/3 | ER 29/150, EC 2/10, PTR 2/2 | ER 30/150, EC 2/10, PTR 1/2 |
| B2 | ER 29/150, **EC 8/10**, PTR 8/8 | ER 29/150, **EC 8/10**, PTR 8/8 | ER 30/150, **EC 8/10**, PTR 8/8 |

All: drops=0, ST_INVALID=0, CT=500/500. GATE: B1 0 failures, B2 0 failures.

WBS (metric 2=revision, 7=median latency, 6=false revision):

| arm | v0 | v1 | v2 |
|-----|----|----|----|
| B  | 40/40, lat 25, false 0/27 | 41/41, lat 25, false 0/28 | 44/44, lat 25, false 0/29 |
| B1 | 47/47, lat 25, false 0/27 | 45/45, lat 25, false 0/27 | 46/46, lat 25, false 0/29 |
| B2 | 50/50, lat 25, false 0/26 | 53/53, lat 25, false 0/26 | 51/51, lat 25, false 0/26 |

JI: identical across arms (implant rejection 6/6, junk 0–1/344+, entrants 0/6).

**Reading:**
- **ER is policy-independent.** B, B1, B2 tie exactly on every VUP
  variant (29/29/30). On VUP/JI, B1's logs differ from B's only in the
  arm tag and the audit fingerprint (different victims, same counts);
  on WBS the only additional difference is the revision-cohort size
  (see below) — the capacity ceiling is structural, confirmed
  experimentally.
- **B2 is a real challenger on evaluation coverage:** EC 8/10 in all
  three variants vs B's 2–3/10 — B2 **passes prereg §9 condition 7
  (EC ≥ 0.5 in ≥2/3 VUP variants)** where B fails it, with zero cost
  to ER, drops, or verifiability.
- **WBS nuance:** B1/B2 revise *more* wrong memories (larger cohorts,
  e.g. 50/50 vs 40/40) at identical 100% revision rate, identical
  latency 25, zero false revisions. The tiered policy keeps wrong
  memories alive long enough to be strengthened-then-revised instead
  of silently evicting them pre-strengthening. Same bar, more
  thorough correction path.

### S10 (B vs B2, full matrix, 2× each — all byte-identical)

| arm | VUP v0/v1/v2 ER | VUP EC | WBS rev | JI rej |
|-----|-----------------|--------|---------|--------|
| B  | 317/1500, 317/1500, 318/1500 | 21/100, 21/100, 22/100 | 100%, lat 25 | 6/6 |
| B2 | 317/1500, 317/1500, 318/1500 | **98/100, 98/100, 98/100** | 100%, lat 25 | 6/6 |

No degradation for B2 at 10×: ER tracks B exactly, EC scales
proportionally (8/10 → 98/100), zero drops, ST_INVALID=0 throughout.

### S100 (VUP v0, 2× byte-identical)

| arm | ER | EC | drops | invalid |
|-----|----|----|-------|---------|
| B  | 3197/15000 | 186/1000 | 0 | 0 |
| B2 | 3197/15000 | **998/1000** | 0 | 0 |

No degradation at 100× for either arm. B2's EC advantage holds
(800/1000 = 0.80 ≥ 0.5).

## 4. Verdict

**On the capacity question (ER ~21% vs the 95% bar): the ceiling is
structural — no challenger.** ER is bounded above by
(user-slots)/(important-offered) = 20.0%/21.2%/21.32% across legs;
B already sits one slot (the finite-horizon tail artifact) below it,
and two policy-divergent variants tie B exactly. The 95% promotion
bar (§9.2) cannot be met by any arm without a prereg amendment
changing the capacity accounting or the curriculum ratio. This is a
measurement-design ceiling, not a learner-competence ceiling: by the
capacity-relative measure B is at 29/30 = 96.7% slot saturation.

**On the arm question: B2 is a CHALLENGER to B (does not displace —
displacement is Micah's call).** B2 ("uniform + importance-tiered
eviction + designated-priority") matches B on every bar B holds
(no-degradation at 100×, zero drops, 100% WBS revision at latency 25,
100% implant rejection, clean GATE, byte-identical reruns, no RNG,
full-erase-price law untouched) and additionally passes §9
condition 7 (EC ≥ 0.5 in 3/3 VUP variants: 0.80 S1 → 0.98 S10 →
0.998 S100) where
B fails (0.20–0.30). B1 is policy-equivalent to B on all scored
metrics — useful as a control showing the tiering alone moves
nothing, but not a challenger.

**Recommended follow-ups (need Micah's word):**
1. Prereg amendment: replace or relativize the §9.2 R_vup ≥ 95% bar
   (unreachable by construction — §5.2 already discloses why).
2. Whether B2's designated-priority tier counts as legitimate policy
   or as gaming the designation predicate (it uses only
   learner-computable information, but the designation schedule is
   curriculum-shaped).
3. Whether to promote B2 to the main line as B's successor, keep it
   as a challenger arm, or fold the tiering into B proper.

**Bar checklist for B2 (all held):** pure Zag ✓ · zero RNG in
decision paths ✓ · byte-identical reruns (2× every cell incl. S100)
✓ · no degradation at 100× ✓ · full-erase-price law untouched (B's
`st_kill` path unchanged) ✓ · no arbitrary hard limits (no new
bounding constants; 100000 is a tier-separation weight) ✓ ·
ST_INVALID=0 everywhere ✓ · GATE 0 failures ✓ · frozen prereg
semantics preserved (B1/B2 are new experimental arm ids 4/5;
`trial_bin_r4` and its sources untouched — B's path in the new
binary verified byte-identical to `trial_bin_r4` output).
