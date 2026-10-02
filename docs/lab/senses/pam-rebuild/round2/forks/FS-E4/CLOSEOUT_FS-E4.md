# CLOSEOUT_FS-E4 — "R2-15 Booster Pilot" (Debate E §7, §4 falsifier)

**Date:** 2026-09-24. **Status: INFEASIBLE — hypothesis UNTESTED (never ran).**

## What FS-E4 was

Debate E §7 specified FS-E4 as the cheap falsifier of §4's FOR claim:
*R2-15's concurrence mechanism scales to real batteries with the safe+live
profile intact.* Mechanism: R2-15's EXACT mechanism (naive RGB/zero-crossing
front-ends + install-on-agreement), no challenge machinery, on 3 R2A tasks
(colordisc, pitchdisc, motiondir — "the tasks with the best formation"),
2,000 adversarial + 1,000 controls per task. Joint kill bar: FI UCB ≤1% AND
recall ≥85% on the same battery; either fails → the booster-scaling
hypothesis DIES. Crew prediction recorded: fails on recall via
agreement-withhold.

## What was done

The FS-E4 crew did NOT commit a prereg and did NOT build the battery. It ran
a feasibility analysis first (correct call): wrapped raw R2FX F/G spans into
the payload formats of R2-15's frozen naive front-ends (`r2p_front.zag`) and
judged every fixture in `round2/forks/R2-7/fixtures_R2A/` (r2n/r2a/r2a2) with
a Python mirror of the naive judges (mirror validated 200/200 F-fooled and
200/200 G-clean on generator-verified R2P pitchdisc pairs).

Full analysis: `work/FEASIBILITY.md` (+ `work/FS-E4_spec_extracted.txt`,
`work/measure.py`, `work/measure_fast.py`, `work/measure_fast.log`).

## Finding: the specified battery cannot be assembled

R2-15's naive front-ends do not produce the required family shapes on R2A
fixtures. The debate's "tasks with the best formation" assumption does not
hold for the naive mechanism on these fixtures.

### Feasibility table (copied exactly from `work/FEASIBILITY.md`)

Format: n / F_ok% / G_ok% / both_ok (fj==gj==tc) / F_fooled with G_ok /
F_fooled with G_same_lie.

colordisc:
  r2n : n=1080 F_ok=33.3% G_ok=33.3% both=360  fooled: G_ok=0    G_samelie=720
  r2a : n=1150 F_ok=30.4% G_ok=30.4% both=350  fooled: G_ok=0    G_samelie=800
  r2a2: n=1180 F_ok=30.5% G_ok=30.5% both=360  fooled: G_ok=0    G_samelie=820
  -> both_ok ALL truth=SAME (r2n sub=0 normals; r2a/r2a2 COL-2 illuminant-drift).
     COL-1/COL-3 metamers fool the naive RGB judge on BOTH F and G (G is a
     re-render of metameric spectra; the naive judge cannot use the spectra).

shapetrans:
  r2n : n=1296 both=499  fooled: G_ok=265 G_samelie=106
  r2a : n=1150 both=411  fooled: G_ok=280 G_samelie=132
  r2a2: n=1195 both=397  fooled: G_ok=330 G_samelie=138

pitchdisc:
  r2n : n=720  both=295  fooled: G_ok=92  G_samelie=146
  r2a : n=1150 both=322  fooled: G_ok=239 G_samelie=241
  r2a2: n=1180 both=327  fooled: G_ok=248 G_samelie=255

Required vs available (per parent-brief family shapes):

E4-N (recall, fj==gj==tc): need 1000 + E4-WA 300 = 1300 per task.
  colordisc: 1070 available (all SAME-truth). SHORT by 230, and 100% SAME bias.
  shapetrans: 1307 available. OK (margin 7).
  pitchdisc: 944 available. SHORT by 356.

E4-U (F fooled L, G clean) 700 + E4-C (same + booster-F fooled) 650 = 1350 per task.
  colordisc: 0 available. FUNDAMENTAL BLOCKER (G never clean when F fooled).
  shapetrans: 610 available. SHORT by 740.
  pitchdisc: 487 available. SHORT by 863.

E4-W (F fooled L, second F fooled L): needs pairs; bounded above by F_fooled
  counts (colordisc 2340, shapetrans 1219+527, pitchdisc 1284+350) — feasible
  in count but the E4-U/E4-C blocker already kills the battery.

## The formation-transfer finding (why this is INFEASIBLE, not merely hard)

R2-15's mechanism is inseparable from its front-ends and its battery:

1. **colordisc is a fundamental blocker, not a count shortfall.** The R2A
   colordisc G-span is a re-render of metameric spectra; the naive RGB judge
   is fooled on G exactly when it is fooled on F (G_samelie = ALL fooled
   trials: 720/800/820). Zero E4-U/E4-C trials exist — no battery can be
   assembled around a concurrence witness that shares the blind spot.
2. **shapetrans/pitchdisc exist at <45% of the required E4-U+E4-C rate**
   (610/1350, 487/1350), and pitchdisc's E4-N controls are short (944 <
   1300). More fixtures cannot fix colordisc (structural), and generating
   2–3× more fixtures for the other two only to run a *pilot* is not the
   cheap falsifier the debate asked for.
3. **motiondir (the spec's third task) was never measured** — the naive
   front-end set has no motiondir judge; the feasibility covered only
   colordisc/shapetrans/pitchdisc.

Root cause (crew's words, kept): R2A G-spans are "clean" for R2-7's formation
front-ends (which use spectra/second-presentations), NOT for R2-15's naive
r2p judges. The concurrence mechanism cannot be lifted off its front-ends:
naive-judge concurrence on R2A fixtures is concurrence between two
identically-blinded judges.

## Verdict on FS-E4

- **INFEASIBLE as specified.** No prereg was committed (nothing feasible to
  preregister). No battery was built. The §4 FOR claim
  ("R2-15's concurrence mechanism scales to real batteries") was **NEVER
  TESTED** — it is untested, not falsified. Nothing about R2-15's 0%/100%
  R2P profile is overturned by this closeout.
- The crew's recorded prediction (fails on recall via agreement-withhold)
  remains a prediction, not a measurement.

## Handoff

The feasible redesign is **FS-E4b** ("Cross-Span Concurrence on R2A"): keep
the concurrence question, replace R2-15's naive front-ends with R2-7's
frozen formation front-ends (for which the R2A G-spans are clean witnesses),
base = R2-7 full mode, booster = + formation(G) agreement. Separate prereg
(`round2/preregs/PREREG_FS-E4b.md`), separate fork dir
(`round2/forks/FS-E4b/`). This closeout commits the FS-E4 feasibility record
so the redesign's premise is auditable.

## Provenance

- Debate: `round2/debates/DEBATE_E_safety_liveness.md` (committed 290f14de),
  §4 ruling + §7 FS-E4 spec.
- Spec extraction: `work/FS-E4_spec_extracted.txt` (from the debate §7
  section; the "colordisc, pitchdisc, motiondir / 2,000 adversarial + 1,000
  controls / joint kill bar" spec).
- Feasibility: `work/FEASIBILITY.md` (analysis only, 2026-09-24),
  `work/measure.py`, `work/measure_fast.py`, `work/measure_fast.log`
  (empty `work/measure_full.log` retained as evidence it never ran).
- Laws observed: zero RNG in any decision path (feasibility used
  deterministic fixture iteration); numbers above copied exactly from
  `work/FEASIBILITY.md`, not re-derived.
