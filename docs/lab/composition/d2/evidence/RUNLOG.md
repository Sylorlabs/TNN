# D2 Run Log — 2026-09-27

## Teaching
- 5 sessions sent to learner (wb_dialogue_bin via chat mode):
  - S1: World physics (grid, energy, void, actions, OBS format).
  - S2: Sub-skill 1 FORAGE (motes, EAT, procedure).
  - S3: Sub-skill 2 WARD-BUILD (crystals, TAKE/COMBINE/DROP, procedure).
  - S4: Sub-skill 3 SHELTER (storms, zone, ward shelter, procedure).
  - S5: Retrieval question format (neutral examples only; RT1 certified
    no P2 order leakage after revision).
- Learner replies: "Noted." / "I don't know." (no action digits).

## P0 mastery gate (24 scenarios: F/W/T ×8, k=24..47)
- Driver: `drive_d2.py` via `d2 tui` channel.
- Early abort: episode terminated after 3 consecutive invalid replies
  (per §5: 3 invalid = episode FAIL; no need to burn remaining ticks).
- Results:
  - P0-F (S1 forage): 0/8. All FAIL (invalid replies, no EATs).
  - P0-W (S2 ward-build): 0/8. All FAIL (invalid replies, no ward).
  - P0-T (S3 shelter): 0/8. All FAIL (invalid replies).
  - **P0 total: 0/24.**

## P1 retrieval (24 items, one per P2 scenario)
- Question: "Which sub-skills, in which order, does this scenario require?"
- Canonical: FW→1,2,3,1; WF→2,3,1; FWF→1,2,3,1,3,1.
- Results: 0/24 correct. All replies "I don't know." (no digits).

## P2/P3
- NOT RUN. K2 gate triggered (see below). Running P2/P3 without mastery
  would be mastery theater; the outcome is determined by the (a) rule.

## Classification (per P2 episode, frozen §6 priority)
- All 24 P2 items require S1, S2, S3 (FW/WF/FWF all need forage+ward+shelter).
- P0-S1: 0/8 (<7/8). P0-S2: 0/8 (<7/8). P0-S3: 0/8 (<7/8).
- Therefore all 24 P2 items classify as **(a) unmastered parts**.
- P3 items: not run; would also be (a)-adjacent (no mastery), but P3 is
  (c-r) only per the taxonomy; moot under VOID.

## K-adjudication
- **K1 (composition)**: VOID (K2 operative). Raw P2 not measured; chance
  arms: NULL 0/24, SINGLE-RULE 0/24 (WRONG-ORDER 24/24, see build log).
- **K2 (mastery)**: **VOID — OPERATIVE VERDICT.** 24/24 P2 items classify
  (a) = 100% > 50% threshold. The learner never mastered the parts (0/24
  P0), so composition proper was never tested. This IS the finding.
- **K3 (retrieval)**: VOID (K2 operative). P1 0/24, but attribution moot.
- **K4 (reflex)**: VOID (K2 operative). P3 not run.
- **K5 (interference)**: VOID (K2 operative). P4 not run.
- **K6 (memorization)**: Construction PASS (N1–N3 80/80 novel); trace-replay
  N/A (no passed episodes to attack). The red team found no memorization
  surface exploited (there were no passes).

## Overall D2 envelope
**K2 VOID.** The D2 instrument is built, validated, and discriminating
(reference gate passes). The real learner (wb_dialogue_bin) does not
produce action digits in response to OBS lines; it replies "Noted." /
"I don't know." It mastered 0/24 P0 probes and 0/24 P1 items. Composition
cannot be tested until genuine part-mastery is demonstrated. This mirrors
the D1 outcome (K2 VOID, 0/600). The "REDO with actual learning" workstream
(learner repair) is the prerequisite for a non-VOID D2 run.
