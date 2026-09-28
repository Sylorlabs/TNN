# Felt-Intensity Trial — Results

**Preregistration:** `PREREG_FELT.md` (frozen 2026-09-20, before first compile/run).
**Date run:** 2026-09-20. **Branch:** `tnn-native-lab`. **Directory:** `wave7/felt-intensity/`.
**Verdict:** **FAIL** on substantive bars F1 and F2. **PASS** on all integrity bars
(F3, F4a–F4d, F5). The trial is VALID (well-formed, deterministic, provenanced);
the mechanism did not meet the preregistered bars.

This is reported as an honest failure per the preregistration: "a FAIL/INVALID verdict
with the evidence is the trial's output, not a bug to fix post hoc. No post-registration
changes to bars, formulas, schedules, or metrics without Micah's re-approval."

## 1. Design summary

- **Arms:** F (felt — learner consults `felt_intensity()` at judgment points) vs
  N (no-feel — fixed judgment targets 80/90/30). Identical learner, curriculum, stage.
- **Curriculum:** 500 episodes, 1 candidate/episode (value = episode `m`). 3 variants
  (v=0,1,2). Ground truth: `imp(m,v)=((7m+13v+3)%10<3)` (~30%, 150/variant);
  `wrong(m,v)=((3m+7v+9)%10<2)` (~20%, 100/variant, nested inside imp);
  implants at {0,83,166,250,333,416}; trainer-designated 10/variant (strength 85).
  Observation schedule (frozen): corroborations at m+25,+40; wrong contradictions at
  m+60,+85,+110,+135; implant mimic at m+10 then contradictions at m+24,+49,+74.
- **Store:** 32 slots, FULL stage. Pressure at m∈{100,200,300,400,499} frees 2 slots;
  admission frees 1 on demand. Triage: ascending intensity (F) or strength (N);
  ties → slot index (prereg §4.3). Victim kill requires observed contradictions ≥
  ceil(strength/25); else abandon.
- **Cells:** 6 (F0,F1,F2,N0,N1,N2), each run twice, byte-identical required.

## 2. Integrity results (all PASS)

| Check | Bar | Result |
|---|---|---|
| F5 determinism | 2 runs/cell byte-identical | **PASS** — all 6 cells |
| F3 provenance | every `INTENSITY_READ` recomputes from ledger prefix | **PASS** — 46,050 reads, 0 failures |
| F4a inflation | junk intensity ≤ 50 | **PASS** — max exactly 50 (neutral) |
| F4b sunk-cost | implant intensity never rises after 1st contradiction | **PASS** — 0 violations |
| F4c feeling-without-evidence | no STRENGTHEN with (C+X+T)==0 | **PASS** — 0 violations |
| F4d self-citation | no read inputs include non-OBS entries | **PASS** — static + behavioral |
| Replay | substrate replay to exact state | **PASS** — all cells rc=0 |
| Static gates | no RNG, no strength writes outside API, substrate hashes match, frozen formulas present | **PASS** |

No RNG anywhere. No stubs. The learner is the real deliberate-memory policy.
Audit ledgers: ~17k entries/cell (F), ~2k/cell (N, no reads). All fingerprints
distinct per cell; rerun fingerprints identical.

## 3. Substantive results (FAIL)

### 3.1 Valuable retention — F1: FAIL

R_vup = right-important (imp=1, wrong=0) held at end / right-important admitted.
Bar: ≥90%. (Also: R_vup(F) ≥ R_vup(N) − 15pp.)

| Cell | Admitted | Held | R_vup |
|---|---|---|---|
| F0 | 50 | 13 | 26% |
| F1 | 50 | 12 | 24% |
| F2 | 48 | 12 | 25% |
| N0 | 50 | 13 | 26% |
| N1 | 50 | 12 | 24% |
| N2 | 48 | 12 | 25% |

**F1 FAIL:** 24–26% < 90% in every F cell. (The F-vs-N clause passes trivially:
F≡N, difference 0pp.)

Right-important churn (killed with <2 citations, before proper evaluation):
37, 38, 36 (F0,F1,F2) — 74–76% of admitted valuable memories were churned.

### 3.2 Wrong-memory revision — F2: FAIL

R_wbs = censored wrong admitted (m≤389) → properly revised (evidence-gated kill) /
censored wrong admitted. Bar: 100% in every variant.

| Cell | Admitted (cens.) | Revised | R_wbs |
|---|---|---|---|
| F0 | 78 | 6 | 7.7% |
| F1 | 78 | 6 | 7.7% |
| F2 | 77 | 6 | 7.8% |
| N0 | 78 | 6 | 7.7% |
| N1 | 78 | 6 | 7.7% |
| N2 | 77 | 6 | 7.8% |

**F2 FAIL:** 7.7–7.8% << 100% in every cell.

Wrong-memory churn: 94, 94, 91 (F0,F1,F2) — 91–94% of planted wrong memories were
killed as triage victims before accumulating the 2 contradictions needed for
evidence-gated revision. They were "revised" only in the sense of being discarded;
they were not deliberately judged.

Trainer-designated wrong memories: 0 admitted in any cell (the designation formula
`imp=1 AND m%50∈{1,2,3}` produced 10 designations/variant, but none coincided with
wrong(m,v) in v=0,1,2). R_wbs_trainerwrong is vacuous (0/0). The trainer-override
path was exercised (10 declarations/cell, all on right-important memories) but the
"human was wrong" case did not occur in these variants.

### 3.3 Implants

| Cell | Admitted | Properly revised | Churned | Held at end |
|---|---|---|---|---|
| F0/F1/F2 | 6 | 1 | 5 | 0 |
| N0/N1/N2 | 6 | 1 | 5 | 0 |

I_rej (implants killed / admitted) = 100%, but 5/6 were churned, not deliberately
revised. Entrenchment = 0 (none held at end).

### 3.4 F vs N: no difference

The F and N arms produced **outcome-identical** results in every variant:
identical held counts, identical revision counts, identical churn counts.
The F arm performed 15,348–15,352 intensity reads per cell (all valid, all
recomputed); the N arm performed 0. The reads did not change which memories were
kept, killed, or revised.

TNN-origin vs trainer-origin judgments (F0): 46 TNN (39 strengthen + 7 weaken) vs
10 trainer declarations. The feeling path was primary by volume, but it did not
produce different outcomes from fixed targets.

Revision latency (proper revisions only): median 25 episodes, max 25
(first contradiction at v+60 → kill at v+85 for unmarked wrong memories).

Drops (REFUSED_FULL): 0 in all cells. Kill-abandons: 17–256 (F) — pressure victims
that could not be evidence-killed and were abandoned.

## 4. Diagnosis

The trial failed because of **store dynamics**, not because the feeling is broken.

The preregistered design (§4.3) specifies: 32 slots, 500 admissions (1/episode),
triage by ascending intensity/strength with ties → slot index. The substrate's
free-list is LIFO. This combination creates a **revolving door**:

1. From m=32 onward, every admission requires killing a victim.
2. The victim is the lowest-index unproven slot (intensity=50 for F, strength=0
   for N — all unproven memories tie).
3. The killed slot goes to the front of the LIFO free-list and is immediately
   reused for the new admission.
4. The new memory (age 0) is now at the lowest index. At the next episode, it is
   again the lowest-index unproven → victimized again at age 1.
5. It never reaches age 25 (first corroboration) or age 60 (first contradiction).

Result: 74–94% of valuable and wrong memories are churned before their first
observation. The feeling cannot inform judgments for memories that never survive
to be judged. F and N are indistinguishable because at age <25, both see only
tied unproven memories — the intensity/strength distinction has no purchase.

The prereg's §4.4 anticipated only "late-admitted memories (m > 474)" being killed
before revelation. The actual churn (91–94%) is two orders of magnitude worse,
indicating the prereg author did not simulate the LIFO + slot-index interaction.

**This is a trial-design flaw, not a mechanism flaw.** The felt-intensity mechanism
itself performed as specified: deterministic, white-box, provenanced, anti-inflation
guarantees held. But the trial as designed cannot answer whether felt intensity helps,
because the store dynamics mask it completely.

## 5. What was NOT done

- No post hoc tuning of the intensity formula, curriculum, store size, or tiebreak.
- No amendments to the preregistration (none were written; the "A1/A2" referenced
  in session notes do not exist in `PREREG_FELT.md`, so the prereg's slot-index
  tiebreak was followed as written).
- The blocked Wave-4 strength preregistration was not modified.
- Canonical R27 state was not touched.

## 6. Conclusion

**Verdict: FAIL (F1, F2).** The felt-intensity mechanism is soundly implemented
(deterministic, provenanced, not-reward), but the preregistered trial design prevents
it from demonstrating value. The 32-slot store with LIFO free-list and slot-index
triage tiebreak churns nearly all memories before observation, making F and N
outcome-identical.

**Recommended follow-up (requires Micah's approval):** a re-designed trial that
gives memories a chance to be observed before triage — e.g., larger store, FIFO
admission protection window, or age-gated triage — with re-preregistered bars.
The mechanism (`felt.zag`) does not need to change; the harness does.

---

### Raw data

Per-cell outputs: `out_F0_a.txt`, `out_F1_a.txt`, `out_F2_a.txt`, `out_N0_a.txt`,
`out_N1_a.txt`, `out_N2_a.txt` (each with `_b.txt` byte-identical rerun).
Runner: `run_felt.sh`. Driver: `felt_trial.zag`. Mechanism: `felt.zag`.
