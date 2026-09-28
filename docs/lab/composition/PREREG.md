# PREREG — Composition Battery (FROZEN 2026-09-27)

**Question:** Can TNN compose genuinely mastered parts into novel wholes —
produce correct behavior for combinations it has never seen, from parts it has
genuinely learned?

**Background (why this is the hunt):**
- R3 falsified the native-reasoner lead hypothesis.
- Invent-to-survive (commit `19f97c6cb`) KILLED the invention claim: removing
  "novel" steps cut survival only ~7%; the 220-vs-160 edge over recall-only came
  from avoiding harmful reflexive COMBINE plus safety logic — not from
  inventing strategies. Post-mortem: **combination failure (c)** with a side of
  **harmful reflexive application**.
- Task-1 comparison: "composition is the broken link" replicated under survival
  pressure. This battery isolates composition directly instead of inferring it
  from survival scores.

## 1. Operational definition (not vibes)

**Composition** holds for a part set P = {p1..pn} and a combination C iff ALL
of the following hold:

1. **Mastery:** each part pi scores ≥7/8 on HELD-OUT part probes (inputs never
   shown during teaching). Parts below bar are excluded from C-items and
   counted as failure mode (a) — never silently dropped.
2. **Novelty:** C is produced by the deterministic generator (§4), is absent
   from the training mass (verified by construction — training shows only
   single-part applications — plus text search of the committed training mass,
   mirroring the survival trial's kb-cleanliness check), and is not derivable
   from any single part (cuing audit, §5).
3. **Correctness:** TNN produces C's correct output, where "correct" is defined
   by the parts' semantics composed per C's structure — never by memorized
   C-instances (none exist).

## 2. Part inventories (frozen)

**D1 — text reasoning (primary):** string rewrite rules over lowercase tokens.
- P1 REVERSE: "abc" → "cba"
- P2 DUP-FIRST: "abc" → "aabc"
- P3 ROT-LEFT: "abc" → "bca"
- P4 DROP-LAST: "abc" → "ab"
- Full battery adds P5 (UPPER-FIRST: "abc"→"Abc") and P6 (SORT-CHARS:
  "cba"→"abc"), and 3-hop chains. Pilot uses P1–P4, 2-hop.

**D2 — sim sub-skills (secondary, reuses TIDELOCK machinery):**
- S1 forage: efficient mote eating (+30/mote, dormancy respected).
- S2 ward-build: crystal+crystal→WARD before a storm window.
- S3 storm-time: shelter during storm windows, forage outside them.
- Novel scenarios require novel SEQUENCES (e.g., forage-then-ward under a
  shifted storm schedule the agent never saw). Parts verified mastered in
  isolation first (same ≥7/8 gate on held-out scenarios).

## 3. Battery phases (per domain)

- **P0 — mastery gate:** 8 held-out probes per part. <7/8 → part excluded,
  items needing it classified (a).
- **P1 — retrieval:** for each combination C, "which parts, in which order,
  solve C?" Wrong/missing → (b). (Separates *finding* parts from *using* them.)
- **P2 — composition:** produce C's output. Exact-match scoring.
- **P3 — reflex probe (the survival post-mortem's mechanism):** distractor
  items where NO part applies (correct = identity / withhold). Any part
  application → reflexive-application count. This is failure mode (c-r):
  uncritical application — the harmful-COMBINE analog.
- **P4 — interference analysis:** per ordered-pair accuracy table. Systematic
  order asymmetry (pair (i,j) ≤0.25 while (j,i) ≥0.75, parts mastered in
  isolation) → (d).

## 4. Combination generator (deterministic, zero RNG)

Ordered pairs (i,j), i≠j, enumerated lexicographically; triples in the full
battery. Inputs are counter-derived tokens (`tok(i)`, length 2+i%4, bytes
(97+(7i+13k+k*k)%26)) — disjoint index ranges per phase (train 0–5, P0 6–13,
P2 14–61, P3 62–69). The quadratic term (k²) breaks accidental palindromes that
made the P3 reflex probe insensitive in the first pilot build. No RNG anywhere:
same binary, same bytes, every run. Byte-identical rerun required (run twice, diff).

## 5. Cuing / novelty audit (red-teamable)

- Training mass contains ONLY single-part applications; generator indices for
  P2/P3 never overlap training indices (disjoint by construction).
- Blind cuing audit: an auditor with the training mass + world description
  must not derive any C-solution without composing parts (same standard as the
  survival trial's §8).
- Trivial-recombination exclusion: a C solvable by a single part scores as a
  part probe, not a composition item (generator excludes i==j).

## 6. Failure-mode taxonomy (the discriminating core)

| Code | Name | Criterion |
|------|------|-----------|
| (a) | unmastered parts | either part <7/8 at test time |
| (b) | retrieval failure | parts pass, retrieval probe wrong |
| (c) | combination failure | parts pass, retrieval right, output wrong |
| (c-r) | reflexive application | part applied where none applies (P3) |
| (d) | interference | order-asymmetric pair failure, parts fine alone |

Classification is per-item, in that priority order; (d) is assigned at pair
level after P4. The battery REPORTS the distribution — it does not just
report a score.

## 7. Chance baselines and KILL BARS (frozen)

Baselines: NULL arm (identity output) and SINGLE-RULE arm (applies only the
first retrieved part). `chance` = max(NULL, SINGLE-RULE) accuracy.

- **K1 — chance kills composition:** combo accuracy ≤ chance + 0.10 →
  composition claim KILLED (clean negative; this is a finding, not a failure).
- **K2 — void:** >50% of P2 items classify (a) → battery VOID for composition
  (cannot test composition of unmastered parts); re-run after genuine mastery.
- **K3 — attribution:** (b) accounts for >50% of failures → finding is
  "retrieval failure, not combination failure" (different repair).
- **K4 — reflex defect:** P3 reflex rate > 0.20 → uncritical-application
  defect CONFIRMED (the survival post-mortem's mechanism, now isolated).
- **K5 — interference defect:** any pair meeting the P4 asymmetry criterion →
  interference defect CONFIRMED with the pair named.
- **K6 — memorization check:** red-team must fail to explain combo success via
  surface memorization (success holds on inputs sharing no bigram with any
  training input). If it explains it → battery VOID, generator fixed.

## 8. Pilot — instrument validation (this commit)

Seven scripted reference agents validate that the instrument DISCRIMINATES:
REF-OK (positive control), REF-NOMASTER→(a), REF-NORETRIEVE→(b),
REF-NOCOMBINE→(c), REF-INTERFERE→(d), REF-REFLEX→(c-r), NULL (chance).
Pilot kill bars: **PK1** REF-OK ≥0.90 combo accuracy · **PK2** NULL ≤0.10 ·
**PK3** ≥80% of each mode's failed items carry the intended class ·
**PK4** byte-identical reruns. The pilot validates the instrument; it makes
NO claim about TNN.

## 9. Full-battery execution (BLOCKED ON DISK at prereg time)

Home disk 99% (1.3G free) at 2026-09-27 01:10 PDT — full battery (real TNN
learner integration against `docs/lab/dialogue/deliberation/`, D1+D2,
independent red-team per §5/K6) is PREREGISTERED but NOT BUILT. Build order
when headroom exists: (1) verify disk, (2) D1 vs real learner, label-blind
with honest-broker scoring, (3) D2 sim scenarios, (4) cuing audit + red-team,
(5) verdict vs K1–K6. This prereg freezes the design; any amendment needs
Micah's re-approval.

## 10. Deliverables

- `PREREG.md` (this file, frozen)
- `pilot/pilot.zag` — pure-Zag instrument (post-red-team repairs landed)
- `pilot/PILOT_REPORT.md` — PK1–PK4 verdicts with run evidence
- `pilot/REDTEAM_REPORT.md` — independent red-team verdicts (pilot not voided;
  3 latent bugs repaired, 7 fixes proposed)
- `AMENDMENT_PROPOSAL.md` — PROPOSED (not enacted) bar/design changes for the
  full battery; requires Micah's re-approval
- Full battery: `battery/` (future, disk-gated)
