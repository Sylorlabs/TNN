# Wave-8 Strength Re-Trial: Scale-Leg Results (S10, S100)

**Prereg:** `PREREG_STRENGTH_V2.md` §7 + §15 (advancement rule), §8–§9 (kill/promotion)
**Arm:** B only — uniform/machine type. C and C-P3 were KILLED at S1 and do not advance.
**Scale:** S10 (320 slots, 5,000 episodes, ledger cap 131,072), S100 (3,200 slots, 50,000 episodes, cap 1,048,576)
**Date:** 2026-09-20 | **Runs:** 18 cells × 2 (B × {VUP, WBS, JI} × {0,1,2} × {S10, S100}), zero RNG

## 1. Advancement-rule audit — why these legs ran

`TRIAL_RESULTS.md` (S1) states "**None advance to S10.**" That line misreads the prereg and is corrected here:

- Wave-4 `PREREG.md` §6, carried UNCHANGED per V2 §14: "**Arms killed at S1 do not run further legs.**" The rule bars *killed* arms; it does not bar survivors.
- V2 §15 run order: "finish driver → static checks → GATE cell → S1 cells (twice each) → **S10/S100 for survivors**."
- V2 §2: "**ARM B (uniform) — ADVANCES.** … B is both a candidate and the control."
- C and C-P3 were killed at S1 (P2 drop-ceiling tripwire, 3/3 variants) → they do not advance. B survived S1 → B **must** run S10/S100. "None promoted" (§9) is not "none advance": promotion and advancement are separate rules.

**Documentation defect (dated note):** V2 §7's body is damaged in the committed file — a literal `[truncated 11294 chars]` marker sits after "S100 (3200 slots, 5000". Scale-leg sizes used here are recovered from the preregistered constants in the trial code (`lr_slots`/`lr_episodes`/`lr_audit_cap`) and cross-checked against wave-4 §6 and the P3 K = 50/500/5000 horizon law: S10 = 320 slots / 5,000 episodes / cap 131,072; S100 = 3,200 slots / 50,000 episodes / cap 1,048,576.

## 2. Dated build note (2026-09-20) — chunked audit ledger

- The first S100 attempt panicked in 0.015s: `panic: slice index out of bounds`. Root cause is a **znc toolchain limitation**, not the trial: the runtime cannot index any single slice larger than 2^25 bytes (33,554,432 OK; 37,748,736 panics — even `a[0]` panics). S100's preregistered ledger cap (1,048,576 entries × 21 words × 4 B = 88 MB) exceeds it. (S10's 11 MB was fine.)
- Workaround: the audit ledger is physically 4 chunks (262,144 entries / 22 MB each) with **identical logical semantics** — same cap, same 21-word entry layout, same append-only behavior, same refusal at cap. Only `st_init` / `st_aw` / `st_audit_append` / `st_free` in `strength_core.zag` were touched; no mechanism, curriculum, metric, formula, or bar changed. Classified as a build-system detail per §15 (dated note, not an amendment).
- **Equivalence proof:** the chunked binary reproduces all 9 approved B S1 cells **byte-identically** against the committed S1 evidence logs, and GATE (B) re-passes on it. The chunking is behavior-preserving.

## 3. Run protocol

- Static checks re-run on the modified sources (same suite as `run_trial.sh`): no RNG tokens, no strength writes outside `strength_core.zag`, frozen formulas verbatim (`(7*m+13*v+3)%10<3`, `(m+3)%10<3`, implants `k<=5`, `m%50` designation), bare `@import`s, P3 opcodes present — all pass.
- §15 order followed: GATE (B) 2× → S10 cells 2× → S100 cells 2×. Every cell: exit 0, `ST_DONE`, `ST_INVALID 0`, independent checker 0 failures, byte-identical reruns.
- Timing: S10 ≈ 1 s/cell; S100 ≈ 13 s/cell. (One background runner was killed by a service restart mid-run; the 3 affected JI cells were re-run individually under the identical protocol — all pass.)

## 4. Results

### S10 (320 slots, 5,000 episodes)

| Curriculum | Variant results (v0 / v1 / v2) |
|---|---|
| VUP | retention 317/1500, 317/1500, 318/1500 (**21.1%**); drops **0** (ceiling 640); PTR 18/21, 19/21, 20/22; EC 0.21 → **UNEVALUATED** per P1 rule (same caveat as S1); ER 21.1%; CT 100% |
| WBS | R_wbs **100%** (577/577, 523/523, 477/477); median latency **25**; false revisions 0 |
| JI | I_rej **6/6 = 100%** all variants; junk held 1/3494 (**0.03%**), 1/3494, 0/3498 |

### S100 (3,200 slots, 50,000 episodes)

| Curriculum | Variant results (v0 / v1 / v2) |
|---|---|
| VUP | retention 3197/15000, 3197/15000, 3198/15000 (**21.3%**); drops **0** (ceiling 6,400); PTR 186/213, 189/213, 188/214; EC 0.213 → **UNEVALUATED**; ER 21.3%; CT 100% |
| WBS | R_wbs **100%** (5917/5917, 5353/5353, 4797/4797); median latency **25**; false revisions 0 |
| JI | I_rej **6/6 = 100%** all variants; junk held 1/34994 (**0.003%**), 1/34994, 0/34998 |

### Cross-leg stability — arm B

| Leg | VUP retention | WBS revision | WBS latency | JI implant rej. | JI junk | Drops |
|---|---|---|---|---|---|---|
| S1 | 29/150 = 19.3% | 100% (40/40) | 25 | 100% | 0.3% | 0 |
| S10 | 317/1500 = 21.1% | 100% | 25 | 100% | 0.03% | 0 |
| S100 | 3197/15000 = 21.3% | 100% | 25 | 100% | 0.003% | 0 |

B sits **at the capacity ceiling** at every leg (S100: 3,197/15,000 vs ceiling 3,200/15,000 = 21.33%) — its retention is capacity-bound, not competence-bound. It keeps essentially every important memory it has room for.

### Integrity / determinism (both legs)

- All 18 cells × 2 runs: byte-identical stdout, `ST_INVALID 0`, independent checker 0 failures (replay-exact, refusal hygiene, strength lineage, kill-effort, no bad kills).
- GATE (B): pass on the chunked binary (2× deterministic).
- Ledger: `audit_n` ≈ 10.5K (S10) / 103–112K (S100) vs caps 131,072 / 1,048,576 — **no ledger-overflow refusal**.
- Linear-scaling check (wave-4 §6): per-episode cost S100 ≈ 0.3 ms/ep vs S1 ≈ 0.2 ms/ep — far inside the 12× bound.

## 5. Verdict

- **B SURVIVES at S10 and S100.** No degradation on any primary across 100× scale: retention stable at the capacity ceiling (~21%), revision 100% with constant latency 25, implant rejection 100%, junk ≈ 0%, zero drops — no freeze signature (as expected for the uniform arm).
- B's thesis (prereg §10 — "uniform erasability costs nothing") holds at long horizon within the tested envelope.
- **Standing:** B remains the control/baseline per §8–§9 ("B remains the valid *control* regardless of the verdict"). B is not promoted — promotion condition 2 (R_vup ≥ 95%) is designed for graded configs and B's capacity-bound ~21% does not meet it; the scale legs do not change B's S1 standing.
- **No-free-lunch comparative verdict** (prereg §9): with C/C-P3 killed at S1, B is the only surviving config. No champion is named beyond survival; the S1 verdict (graded judge-type freezes under churn; uniform machine-type does not) now holds at 100×.

## 6. Honest limits

1. **P1 EC < 0.5 at all legs** (0.2–0.3): B's pressure-tested retention remains UNEVALUATED — the same caveat as S1. B was never meaningfully evaluated under the P1 lens.
2. **B ran alone.** No competitor survived S1, so the scale legs test B's long-horizon behavior, not a comparison.
3. **The §7 truncation defect** in `PREREG_STRENGTH_V2.md` should be repaired by dated note (sizes recovered from code constants in §1 above).
4. **The nested-N stress cell** (§13, C/C-P3 at S1) remains deferred and is unaffected by these legs.

## Evidence

- Cell logs: `evidence/cell_B_<VUP|WBS|JI>_<0|1|2>_<S10|S100>_r<1|2>.log` (36 files)
- `evidence/runner_scale.log`, `evidence/VERDICT.txt` (now `S1_COMPLETE` + `SCALE_COMPLETE`)
- Equivalence proof: chunked binary vs committed S1 evidence — 9/9 B cells byte-identical (workspace only)
- Modified source: `trial/strength_core.zag` (chunked audit; workspace only — trial sources were not part of the S1 commit convention)
- Runner: `run_scale_legs.sh` (workspace only)
