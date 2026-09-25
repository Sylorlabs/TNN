# RUNLOG — PAM GOV-LH CREW 6 (three HELD items: V4 two-tier, O2 live, F5 sweep)

## Inherited state (2026-09-24 ~15:35 PDT, resume after daemon restart)

- Predecessor wrote ONLY the prereg `~/workspace/pam_gov_lh/crew6_held/PREREG_CREW6_HELD.md`
  (16,267 bytes, drafted, FROZEN 2026-09-24). No build, no evidence, no verdict existed.
- This prereg was NOT yet committed: `docs/lab/pam/round4/gov_lh/` on branch
  `tnn-native-lab` had only m1, w12, w13, w20 — verified live via gh-api before
  any work.

## Drift check (crew prereg vs `~/workspace/tmp_commit/pam_r3/PREREG_V4_TWOTIER_DRAFT_HELD.md`)

Performed before committing. Verdict: NO unauthorized drift; differences are
documented scopings or faithful elaborations.

1. KB-V4-1: identical (RK-3 < 85% → KILL). ✓
2. KB-V4-2: draft scopes to "the frozen decoy or install streams". Crew prereg
   documents the format gap explicitly: the hardening battery's red-team
   streams are in rt4 sense-record format, which carries NO mrgF/agree/strong/progF —
   fields V4's rules require (R3 bar, MG6 floor, adjudicator). A faithful
   translation is impossible without inventing values. KB-V4-2 is therefore
   adjudicated on (i) RK-1/RK-2 over the 11,840-row sweep (1,109 wrong high-conf
   percepts = the frozen RK-2 battery) and (ii) the CC1 wrong-pair family
   (KB-V4-3), with an engineered decoy stream reported alongside as the
   adversarial probe. Scoping rationale recorded in the prereg §A.3(4) NOTE.
3. KB-V4-3: draft says "the CC1 wrong-pair trials"; crew prereg bars the 9
   scored CC1 cells and treats V9 as an unscored ceiling probe (reported, not
   kill-barred) per CC1 prereg §4 precedent — V9 did not exist when the HELD
   draft was written. Documented in the prereg.
4. KB-V4-4: identical (3 runs byte-identical or VOID). ✓
5. Added: KB-O2 (adjudicated on the same runs — testing V4's machinery IS the
   O2 test), the full frozen machinery spec (c3.zag base + R1/R3/R4 + MG6 + F5-exemplar
   veto), span derivation (W=2000, flagged as modeling choice with conjunct
   breakdown), 1x/10x/100x scales, adversarial boundary variants, honest limits.
   All elaborations; no contradictions with the draft.
6. Pre-registered expectation that KB-V4-1 will KILL (C3 RK-3' = 71.78%; vetoes
   cannot add installs — disposition CHALLENGER_PROV counts as install) — honest,
   documented, not drift.

## Prereg commit

- Committed ALONE: `docs/lab/pam/round4/gov_lh/held/PREREG_CREW6_HELD.md`,
  commit `8f4285f486f196daf01e4c435a61a9a0b857862e` on `tnn-native-lab`
  (parent 2e8a947c7fbc). Local SHA-256 of the prereg:
  `e4a424521a99b908772ca6f238ad945f8ca734768cc4ab50e1bdb77478892d23`.
- Local mirror: `~/workspace/tnn-lab/pam/round4/gov_lh/held/PREREG_CREW6_HELD.md`.

## Test legs (in flight)

- Leg A (V4/O2): build `src/v4.zag` from the prereg; batteries at 1x/10x/100x.
- Leg B (F5): build `src/f5_sweep.zag` + parameterized replay; 35-window sweep.

## Leg A build (2026-09-25 ~13:55 PDT, worker subagent)

- `src/v4.zag` (603 lines, written by predecessor) reviewed line-by-line against
  PREREG_CREW6_HELD.md A.2 and against frozen `c3.zag` (Crew 3, verdict PASS):
  adjudicator, scoring denominators, R1/R3/R4, disp codes 0..9, thr_of/tol_of
  all verbatim; V4-2 F5-exemplar veto BEFORE V4-3 MG6 (first-firing counted);
  MG6 conjuncts match `guard_main.zag`'s `mg_allow` gid==6 exactly
  (floor>=400, half-open span overlap `sa1<sb2 && sa2<sb1` with touching=disjoint,
  |dseq|>=20); veto -> disp 8 (CHALLENGER_PROV) with challenger slot RETAINED
  (no slot writes on the veto path); allow path byte-identical to c3's cmatch
  body (perm install, slot cleared, disp 9). F5 bank in source matches
  exemplars.tsv exactly: (718,2618) (704,2642) (713,2626) (701,2647)
  (710,2632) (713,2627). truth/correct parsed but never read by gate rules
  (field 12 structurally unparsed; `correct` used only in scoring).
- BUILD FIX (faithful, no behavior change): the chunked input loop called
  `nio_read_exact(fd, ch, CHUNK)`, which is a WHOLE-FILE reader — it returns
  -7403 when total file size > max_bytes, so 10x (4.7MB) and 100x (47MB) failed
  with rc=1 while 1x worked. Added `z_read_fill` (raw read(2) fill loop with
  EINTR retry, same pattern the substrate uses internally) and replaced the
  call. Post-fix 1x output byte-identical to pre-fix (sha
  3f511a06b135c85dc317a69e25c5dd5089bef73d8210b96e6318438126526f5e);
  10x/100x now run. Compiler warnings only (A0101 off-by-one benign — guarded
  index; A0102 ignored nio_close). Binary: `src/v4_bin`
  (sha 62f4e4de86df3264a4b7a7b5bfecdab2ad663915e9f319859b292de650c2c418).
- Fixtures verified: c3_cases.txt sha
  ed1ad01fb65a37125b06163bd1243bd930435e655b7a446c5f16fa91333e3357,
  11,840 rows; exemplars.tsv sha
  13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e;
  gen/rk3_10x.txt and gen/rk3_100x.txt byte-compared as EXACT 10x/100x
  concatenations (byte-identical, kept as-is).

## Leg A RK-3 battery (2026-09-25 ~14:00 PDT)

- mode 1, 3 runs per scale, sha256-compared: 1x 3x identical
  (3f511a06...), 10x 3x identical (9df2f6fe...), 100x 3x identical
  (edf01e2c...). No VOID.
- 1x: RK-3 791/1102 = 71.78% (== C3's 71.78% exactly); rk1=0; rk2=0/1109;
  repaired=130; revised_installs=0 (C3: 92); challenger_provs=586 (C3: 194);
  vetoes: f5=0, floor=2, span=98, seqgap=0, allows=0.
- 10x: RK-3 6058/11020 = 54.97%; rk1=0; rk2=0/11090; revised_installs=0;
  vetoes f5=0, floor=20, span=818, seqgap=0, allows=0.
- 100x: RK-3 58708/110200 = 53.27%; rk1=0; rk2=0/110900; revised_installs=0;
  vetoes f5=0, floor=200, span=8018, seqgap=0, allows=0.
- Cross-check: rebuilt frozen c3.zag with the pinned toolchain, ran 1x/10x.
  C3 1x == V4 1x on every metric except revised_installs/challenger_provs/
  veto/d8/d9 (diff on file). C3 10x RK-3 = 6058/11020 == V4 10x EXACTLY.
  The 1x->10x install-rate drop (-16.81pp) is inherited C3 long-horizon state
  behavior under exact repetition (R4 negative-table accumulation: d4
  1588->33779; prov saturation: d0 flat at 1684), NOT a V4 regression.
  Prereg stability expectation (+/-0.5pp) falsified for both; not a bar.

## Leg A CC1 wrong-pair trials (2026-09-25 ~14:05 PDT)

- Transcribed the 10 CC1-family cells from gen_guard.py CELLS (single source
  of truth) to MODE-2 15-field streams with EXPLICIT fixture spans
  (`gen/transcribe_cc1_m2.py` -> `gen/cc1_cells/mode2/`). The predecessor's
  13-field mode-1 files were left untouched (not used for the bar).
- Ran all 10 cells 3x (metrics + trace), sha-compared, scored from trace
  (`gen/run_cc1.py` -> `evidence/cc1/`): all 9 scored cells 3x byte-identical,
  final_perm_j=3, false_installs=0, installs=4, revised_installs=0 —
  matches EXPECT_GUARD_CELL.tsv MG6 rows exactly. Veto attribution: F5 fired
  on 7 cells (challenger (718,2618) sits exactly on exemplar 1), MG6-floor on
  V4 (conf 850/840 off-exemplar, mrgF 382/358 < 400), V3 never reached a
  revision point (|dmeas|=121 > tol).
- V9 unscored ceiling probe: 3x identical, F5 veto fires, 0 REVISED_INSTALL,
  final perm 3.

## Leg A boundary variants + decoy (2026-09-25 ~14:10 PDT)

- 27 engineered cells (`gen/gen_boundary.py` -> `gen/boundary/`):
  mrgF {399,400,401} x |dseq| {19,20,21} x spans {overlap-by-1, touching,
  disjoint-by-1}, all wrong, conf 900/910, |dmeas|=50<=120, conf/meas far
  from all F5 exemplars (F5 never fires here — pure MG6 probe).
- All 27 ran 3x byte-identical (`gen/run_boundary.py` -> `evidence/boundary/`):
  0 deviations from the preregistered expectation. 8 ALLOW cells
  (400/401 x 20/21 x touching/disjoint) -> disp 9, rev=1, rk1=1 each (the
  wrong-pair residual class, as expected). 19 veto cells with the expected
  first-firing conjunct: floor x9 (mrgF=399), span x6 (overlap at 400/401),
  seqgap x4 (dseq=19 with disjoint spans).
- Decoy: verbatim CC1-V9 cell x100 (400 trials), 3x byte-identical:
  revised_installs=0, rk1=0, rk2=0/200, f5_vetoes=199, allows=0, d8=200, d9=0.
  PREREGISTERED EXPECTATION (REVISED_INSTALL) FALSIFIED: the F5-exemplar
  precondition vetoes the verbatim V9 (its challengers (718,2618)/(704,2642)
  sit exactly on exemplars 1/2). The 199 (not 100) vetoes demonstrate the
  retained-slot semantics: reps 2-100 pair BOTH trials against the retained
  challenger. The V9 perfect-storm residual that MG6 alone could not close is
  closed by the F5 precondition; the remaining residual class is the 8
  boundary ALLOW cells (wrong pairs off the exemplar cluster clearing MG6).

## Leg A verdict (2026-09-25 ~14:15 PDT)

- `VERDICT_V4_O2.md` written: KB-V4-1 KILL (71.78% < 85%), KB-V4-2 PASS
  (rk1=0, rk2=0/1109 at 1x/10x/100x), KB-V4-3 PASS (0/9 REVISED_INSTALL),
  KB-V4-4 PASS (all streams 3x byte-identical, no VOID), KB-O2 KILL on the
  liveness prong (71.78% < 85%; safety prongs pass). Adjudicated mechanically
  per prereg A.4. ADOPTION NOT resolved — needs Micah's word.

## Leg B — F5 window sweep (2026-09-25 ~13:55–14:00 PDT)

### Build
- `src/f5_sweep.zag` derived from `f5_tight.zag`; `src/f5_sweep_replay.zag`
  derived from `f5_tight_replay.zag`. ONLY change: rc/rm windows argv-parameterized
  (_zag_arg 3/4); predicate logic byte-identical otherwise. Buffer sizes raised
  (14MB block ledger / 12MB replay ledger, still < 2^25 znc ceiling) to carry the
  100x scale runs in the same binaries — capacity parameter, no predicate change.
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  both compiled clean, binaries local-only at `src/bin/` (NOT for commit).
- Fixture SHAs re-verified before the sweep: all three match prereg pins
  (0c5e2c0d…, 63ea591d…, 13f4ca47…).

### Anchor reproduction (byte-identical, before the sweep)
- (rc=9, rm=15) block output == frozen `f5_tightened/run1.out` == run2.out == run3.out
  (sha 170f53b3…); replay output == replay1/2/3.out (sha 1d6bee68…).
- (rc=150, rm=2000) replay: SUMMARY false_blocked=8/9 true_within=0/34 — reproduces
  the frozen backtest's 8/9 (VERDICT_F5.md §5 bar row).

### Sweep (35 windows, 1x)
- Driver: `gen/sweep_driver.py`. All 70 binary runs 3/3 byte-identical
  (digests in `evidence/sweep_digests.txt`).
- Table: `evidence/sweep_table.tsv`. Headline: (150,1000) → retention 8/9,
  over-block 66/300 (22.0%), far 0/60, true_blocked 0/34. The blocked-false set at
  (150,1000) is IDENTICAL to the frozen (150,2000) set (all via exemplar 10983);
  shrinking rm 2000→1000 removes 44 correct over-blocks, keeps all 8 caught falses.
- true_blocked = 0/34 at ALL 35 windows (no correct backtest candidate ever blocked).
- Pareto frontier (unique points): (0/9,0/300), (1/9,22/300), (3/9,44/300), (8/9,66/300)
  — representative windows (9,15), (150,245), (150,500), (150,1000).
  The frozen (150,2000) is Pareto-dominated by (150,1000).
- B.3 mechanical check → OVERTURN (only (150,1000) satisfies all three).

### Boundary percepts
- Driver: `gen/boundary_gen.py`. 8 CORRECT TMB percepts per frontier window from
  exemplar 10983 (conf 718, meas 2618) at |Δconf|=rc±1, |Δmeas|=rm±1, both sides
  of each boundary, both axes. Results in `evidence/boundary_percepts.tsv`:
  inside-boundary corrects are BLOCKED for every window with retention>0 (and the
  cluster geometry also blocks minus-side "outside" probes via neighboring
  exemplars) — the preregistered B.2 expectation confirmed: the boundary does not
  separate; falses and near-exemplar corrects share the neighborhood.

### Scale confirmation (10x / 100x)
- Driver: `gen/scale_confirm.py`. Exact-repetition fixtures
  (`gen/f5_block_10x.txt` 3,600 lines, `f5_block_100x.txt` 36,000,
  `f5_replay_10x.txt`, `f5_replay_100x.txt`; SHAs in `evidence/scale_digests.txt`).
- Frontier windows + both anchors, 10x and 100x, 3/3 byte-identical each.
  Rates EXACTLY stable: e.g. (150,1000) → 660/3000 and 6600/30000 (22.0%),
  80/90 and 800/900 retention. See `evidence/scale_confirm.tsv`.
