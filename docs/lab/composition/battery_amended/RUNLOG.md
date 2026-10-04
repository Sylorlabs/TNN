# RUNLOG — Crew D, D1 under the amended composition prereg (A1–A7)

Date: 2026-09-27 (PDT). Operator: Crew D subagent. Law: brief
`~/workspace/comp_b4/crewD_brief_DRAFT.md`; frozen prereg commit
`6ca9e042110ca` (`docs/lab/composition/PREREG.md`); amendments A1–A7 from
`origin/tnn-native-lab` (observed at `2532d5e21` after fetch).

## Provenance (measured 2026-09-27)

- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Real learner binary (round-2 workbuddy, Crew B workdir, reused not copied):
  `~/workspace/comp_b4/battery/work/wb_dialogue_bin`,
  SHA-256 `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09`.
- Real learner provenance commit: `3cd24f11d119a17d14d9637e43ebdc8918b41e92`.
- `/tmp` was 100% full (512 MB tmpfs): all builds in `~/workspace/cd_build`.

## Steps

1. Read all 7 amendments, frozen prereg, Crew B runlog/interpretation/battery,
   Crew C redteam report + `rt_teach.py`.
2. Rebuilt the instrument as `battery_amended.zag`: 6 rules, salted phase
   generator `byte = 97 + (7i + C_phase*k + k^2) mod 26` with train=13, P0=17,
   P2=19, P3=23 (exact A2); 8 probes/rule; fixed pair/triple enumerators for
   six rules; neutral-index P1; direct-pair P2; interleaved reference-run
   P2/P3 schedule (one P3 per 75 P2, round-robin across combinations).
   Reference modes: null, singlerule, wrongord, refok, refnomaster,
   refnoretrieve, refnocombine, refinterfere, reflex, learner.
   Patched generator order mid-build: P1 interleaved pairs/triples in
   combination order; P2 round-robin across the 150 combinations; P3
   interspersed every 75 P2 items. Final `items.tsv`: 878 lines
   (72 TEACH / 48 P0 / 150 P1 / 600 P2 / 8 P3), all salt-formula verified.
3. A2 blocking gate (`shift_gate.py`, saved as `A2_GATE.txt`): 878/878 lines
   match salt formula; 0 cross-phase single-step shift pairs (all 6
   phase-pairs); 1080 two-step/prefix intermediates, 0 shift-equivalent to
   train tokens; shift-memorizer P0 [0,0,0,0,0,2] (no rule >= 7/8); chained
   memorizer P0 same, P2 16/600 — all 16 identity-fallback coincidences
   (input==expected), not shift-chain successes. GATE PASS.
   Two docstring typos noted: phase set should read {train,P0,P2,P3};
   rich training set is 72 examples (12 tokens x 6 rules), not 108.
4. Instrument re-validation: all 9 scripted modes x 3 runs (2 normal +
   MALLOC_PERTURB_=165) byte-identical. Discrimination confirmed:
   null 16/600 (2.67%), singlerule 38/600 (6.33%), wrongord 61/600 (10.17%)
   binding, refok 600/600, refnomaster 600x(a), refnoretrieve 600x(b),
   refnocombine 580x(c) + 16 soft-item ok, refinterfere 596 + 4x(d) on
   pair (0,1), reflex 6/8 on P3 (2 palindromic distractors insensitive).
   Two documented wrinkles (no bar broken): P3 tok 614/618 palindromes;
   P4 behavioral misfire on (0,5) for identity-output agents.
   Per I15 reading, the instrument's chance line = WRONG-ORDER = 61/600.
5. Fair-teaching driver `drive_amended.py` (Crew C rich protocol x 6 rules:
   definition + procedure + 12 worked examples on train-salt tok 0..5,
   700..705 with letter walkthroughs; probes tok 6..13; taught controls
   tok 0,1; P3 distractors interleaved at probe positions 2,5; 1 sample
   session with P1/P2 qualitative prompts). Smoke-tested, then 3 full runs:
   run1, run2, MALLOC_PERTURB_=165 run_pert — all completed; resp_p0.txt
   byte-identical across all three (SHA-256
   `658a7f308686be64016a3a5033827b8d91b763718c260530b0dfef14427497a8`).
6. Label-blind scoring (`score_blind.py`): transcripts copied into workdirs
   named by transcript-hash prefix; `learner` mode scored by the mechanical
   scorer; SCORES.md keyed by hash id only; mapping sealed in SEALED_MAP.txt.
   Scores byte-identical: mastery 0/6, retrieval 0/150, composition 0/600
   (600/600 class (a)), eligible 0/0, reflex 0/8, trueacc 0/600.
7. K1-K6 (`kbars_amended.py`): chance=0.1017 (binding: wrongord), K1 line
   0.2017. K1: 0.0000 -> composition claim KILLED. K2: (a)=600/600 -> battery
   VOID (operative verdict, reported with K1). K3: no. K4: 0/8 no defect.
   K5: no pair meets criterion. K6: vacuous (0 successes; covered set = 30/30
   pairs computed under salted generator).
8. Cuing/novelty audit (`audit_amended.py`, full output in INTERPRETATION):
   teaching mass 144 example lines all on train tokens; 0 byte-identical
   inputs across phases; 0 P2 expected-output leaks (len>=2); driver-vs-gen
   cross-check widened to all sections (72+48+150+600+8, 0 mismatches);
   P1 carries 0 semantic labels; A5: 22/600 soft items (19 at length 2);
   commutativity: (1,3),(3,1),(3,4),(4,3) commute — A5 expectation FALSIFIED
   for P5 vs P4 (upperfirst x droplast commute exactly); K6: 30/30 covered.

## Determinism

- Scripted modes: 3/3 byte-identical (incl. MALLOC_PERTURB_=165).
- Learner: 3/3 byte-identical transcripts; scores 3/3 identical.

## Deliverables (~/workspace/comp_b4/battery_amended/)

battery_amended.zag, items.tsv, drive_amended.py, shift_gate.py,
score_blind.py, kbars_amended.py, audit_amended.py, A2_GATE.txt,
run1/ run2/ run_pert/ (transcripts + teach_log), blind_scores/
(SCORES.md, SEALED_MAP.txt, learner.out), learner.out, null.out,
singlerule.out, wrongord.out, RUNLOG.md, INTERPRETATION.md, REPORT.md.
No binaries, no .zagd, no scratch copies.
