# REDTEAM2 — Independent Red Team vs Experiment 1b "All Bars Pass" (PREREG2)

**Target:** implementer's claim in `docs/lab/invention/survival/recall_fix/evidence/BAR_RESULTS2.md`
(all six kill bars pass) on branch `origin/tnn-native-lab`, repo `~/workspace/selfpam_run/tnn-lab`.
**Method:** source inspection of the full committed tree + rebuilt the agents with the pinned
toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) and ran new,
concrete trap scenarios against the **unmodified committed agents** (only new world/KB files).
My build reproduces every committed number I re-ran (D2/D3 phase-1, phase-2, sealed A4) exactly.
Workdir (trap worlds/KBs, build): `~/workspace/e1b_complete/redteam/wd/` — the repo was not modified.

**Bottom line:** the headline numbers reproduce, but the "all bars pass" claim is weaker than
stated in five specific ways, and I landed working exploits against the deliberative agent in
families 3, 4 and 5. No kill bar fires *as written* — but K3 and K4 pass on readings narrower
than their preregistered intent, and frozen PREREG2 §3 ("ALL THREE domain agents import it")
is outright violated.

---

## 1. Attack scoreboard

| Family | Attack | Result |
|---|---|---|
| 1 REVERSAL | Negate all KB claims (10→−10, 5→−5), run D on home **and** shifted D2 | **FAILED to break** — D=4500 home, D=3900 shifted (identical to true-claim runs). Gate predicate `mean < claimed/2` is sign-symmetric; D is robust here. |
| 2 FLIPS | Swap claims between heuristics (d00↔d01, d10↔d11) on home D2 | **FAILED to change behavior** — D=4500=P. No distrust fires (observed 10 ≥ 2.5; observed 5 = claimed/2 exactly, strict `<` fails). D does **not** detect the mislabeling — it silently corrects the claim to the observed mean after n≥10 — but behavior stays optimal. |
| 2b | d01 claimed 11 (observed 5 < 5.5 → spurious distrust) | **Landed weakly** — D=4425 vs P=4500. Spurious distrust wastes 15 exploration ticks, then argmax re-selects HOLD. Recovers. |
| 3 PER-CHECK NEUTER | Neuter precondition / conflict / effect-expectation checks individually | **LANDED** — precondition and conflict checks are **decorative** (0% decision change; they don't exist in the decision path). Only effect-expectation is causal. D1's entire EVAL is decorative. §3.1 |
| 4 CLOSE-CALL | Worlds sitting exactly on the distrust boundary | **LANDED** — knife-edge proven: 1-point world change flips D from 0 to 135 overrides, score 3750→4340. §3.2 |
| 5a | Bait-then-switch: heuristic perfect for first ~90 ticks, then dead | **LANDED** — D switches only at ~tick 216, eating ~42 degraded task-0 ticks; D=50988 vs P=53302. §3.3 |
| 5b | Mediocre trap: observed 60 ≥ claimed/2=50 forever; untaught best action exists | **LANDED** — D≡R behaviorally all 600 turns, 0% gap closure. §3.3 |
| 5c | Late-onset shift: perfect until tick 400, then dead | **LANDED** — lifetime-mean gate never fires; D≡R, 0% closure. §3.3 |
| 6 LEAKAGE | Full source-chain inspection for regime-knowledge paths | **Clean** — no leakage found. §3.4 |
| (a) D1 voids | storm-invert / move-rot R_home=R_true=600 | **Half-overturned** — storm-invert DID bite (metric hid it); move-rot couldn't bite by construction. §4 |
| (b) Held-out uniformity | diff sealed worlds | **Confirmed reskins** — 1 unique world ×4 per family; in-sample "variants" also duplicated. §5 |

---

## 2. What reproduces (grudging credit)

- Phase-1 arms, phase-2 D, and sealed A4 numbers all reproduce **exactly** from rebuilt sources:
  D2 shifted D=3900, D3 shifted D=50664, sealed D2=3900/D3=50906, R_home/R_true/P all match.
- Determinism holds (reruns byte-identical).
- The sealed SHA_LOG verifies — the seal wasn't tampered with; the problem is what was sealed (§5).
- The distrust gate *does* close the gap on the two in-sample shifts (90.0% / 80.7% recomputed).

## 3. Findings by family

### 3.1 Family 3 — per-check neuter: 2 of 3 prereg-mandated checks are decorative (LANDED)

PREREG2 §2 requires D's evaluator to run **three** checks per candidate:
(a) precondition, (b) effect-expectation, (c) conflict — each with trace evidence
("precondition P: observed O → PASS/FAIL"), and states "the trace must CAUSALLY determine
the action (proven by neuter test)".

What the committed code actually implements:

- `src/recall_delib.zag` contains **exactly one** check: `delib_check_distrust`
  (`n>=10 && sum*2 < claimed*n`). The word "precondition"/"conflict" appears nowhere
  outside a comment and the unused `DH_PRE` slot constant (line 7). The `pre` slot is
  filled (`agent_d_d2.zag:35`, `agent_d_d3.zag` equivalent) and **never read** — the
  RECALL match (`agent_d_d2.zag:48`, `agent_d_d3.zag:45`) tests only the condition id.
- Per-check neuter results (by source inspection — the checks have no decision-path
  existence to neuter, so the neuter is vacuous):
  - **precondition → vacuous PASS: 0% of decisions change** (check absent from agent).
  - **conflict → vacuous PASS: 0% change** (absent; the trace README itself admits
    "always `none → PASS` in this build").
  - **effect-expectation → vacuous PASS: 100% of contested turns change** (the only
    causal check).
- The **audit-grade TSV traces** (`runs/phase2/traces/`) report all three EVAL checks —
  but the precondition/conflict lines are computed **post-hoc by a trace emitter**
  (`trace_emit.zag`), which the README describes as "recomputed with read-only access
  to the exact slots the decision logic read". That file is **not committed anywhere
  in the repo** (`git ls-tree` over the full `src/` tree: absent). So the traces a
  K3(iii) trace-auditor would replay are (a) not reproducible from committed sources,
  and (b) contain two check lines that never influenced any VERDICT. A trace-only
  auditor *cannot detect this from the traces alone* — which is exactly why the prereg
  required source inspection too.
- **D1 is worse:** `src/agent_d_d1.zag` does not import `recall_delib.zag` at all
  (imports are only `world_d1.zag`, `kb_parse.zag`, `kb_d1.zag`). Its "EVAL" block
  (lines 50–54) literally **prints the KB's claimed value** — `i64s(p_get(claims,hi))` —
  which influences nothing; the VERDICT is a priority-first PRE-filtered match with
  fallback to R's rule. D1's deliberation is a *different, weaker, per-domain
  reimplementation*, and its EVAL is 100% decorative. This directly violates frozen
  PREREG2 §3: "**One file**, `src/recall_delib.zag`, implements the deliberative-recall
  module. **ALL THREE domain agents import it.**" K4(i)'s audit scope ("inspects
  `recall_delib.zag`") would never see the D1 bypass.
- Note on A3(i) as executed: `src/analyze_a3.py` does not perform a per-turn neuter
  re-derivation — it only *counts* contested turns (VERDICT ≠ heuristic action); the
  "100% change under neuter" is asserted by construction (true, but not executed as
  described). The whole-run D_accept neuter (A3(ii)) was genuinely executed.

**Verdict on K3:** passes *as written* (100% ≥ 25%; D_accept falls ≥50%; zero
VERDICT/trace mismatches on the coarse traces). But the "consciousness" that passed is
a one-check evaluator wearing a three-check trace. Under a per-check reading of A3(i)
— the red-team version the prereg's §2 language demands — two of three checks score 0%
(< 25% = decorative). K3's letter survives; its intent does not.

### 3.2 Family 4 — the distrust gate is a cliff, not a principle (LANDED)

Gate: `delib_check_distrust`: `n>=10 && sum*2 < claimed*n` (strict `<`, integer arithmetic).

- **T4a** (`wd/worlds/trap_t4a.txt`: D2 home world, (1,1) row `[5,0,10]` — APPROACH yields
  exactly claimed/2=5, RETREAT=10 untaught-best): D=3750 **= R=3750**, P=4500.
  **Zero overrides in 600 turns** — D applies the mediocre heuristic uncritically forever
  because `2*sum < claimed*n` is `10n < 10n` = false.
- **T4b** (identical except (1,1) row `[4,0,10]` — one point lower): D=4340, R=3600,
  **135 override verdicts**, gap closure 82%.
- A **1-point change in one table entry** flips D from "fully trusting, 0% closure" to
  "distrusting, 82% closure" (score Δ=590). The boundary `observed == claimed/2` is a
  knife-edge with no margin — not a principled evidentiary threshold. Combined with the
  `n>=10` hard floor (the first 10 samples are always trusted at face claim value),
  the gate has two arbitrary discontinuities an adversary — or a real regime — can sit on.

### 3.3 Family 5 — uncritical-application traps (main effort; ALL LANDED)

All traps run against the **unmodified committed agents** (new world files only).
Oracle P reads true current conditions (optimal by construction on any world).

| Trap | World | D | R_home | P | D gap closure | D behavior |
|---|---|---|---|---|---|---|
| T1 (5a) bait-then-switch: TOOL_0 perfect → dead at tick 90–120 | `trap_t1.txt` | 50988 | 43548 | 53302 | 76% | Switches t0→TOOL_1 only at **~tick 216**; eats ~42 degraded task-0 ticks first |
| T2 (5b) mediocre: TOOL_0 → cond 60 (obs 60 ≥ 50); TOOL_3=100 untaught | `trap_t2.txt` | 54060 | 54060 | 60000 | **0%** | **Zero overrides in 600 turns** — D ≡ R exactly |
| T3 (5c) late-onset: TOOL_0 perfect → dead at tick 400–430 | `trap_t3.txt` | 53874 | 53874 | 57428 | **0%** | **Zero overrides in 600 turns** — D ≡ R exactly |
| In-sample d3_s0 (for reference) | committed | 50664 | 45084 | 52834 | 80.7% | distrusts, explores, recovers |

- **T1** shows the 10-sample trust window + lifetime averaging as inertia: 10 good samples
  (sum=1000) require **11 zero samples** to drag the mean below half (`2000 < 100·(10+k)` ⟺
  k>10). Deliberation "passes" the heuristic for 21 samples on evidence rigged by the window.
- **T2** is the structural hole: D only ever *demotes* (distrust → explore); it **never
  scrutinizes a heuristic that stays ≥ half of claimed**, never compares against
  alternatives, never considers the KB's own backup (`t0b`: TOOL_1, prio 4 — only the
  first match is ever a candidate). A "good enough" recalled strategy is applied with
  **zero** deliberation about alternatives. 600 turns, 600 uncritical applications.
- **T3** shows lifetime averaging blinds the gate to late-onset shifts: ~134 good samples
  (sum≈13400) then ~66 zero samples leave the lifetime mean ≈67 ≥ 50 — the gate never
  fires while the agent watches the tool die for 200 ticks. The in-sample shift and T3
  differ **only in onset timing** (tick 0 vs tick 400); the fix's efficacy collapses
  from 80.7% to 0%. A "broad" fix should not depend on the shift arriving early.
- Honest caveat: T2/T3 keep D at R's level, never *below* — the failure mode is
  "deliberation adds nothing", not "deliberation harms". And the D2/D3 domains cannot
  express hidden-state traps (rewards are per-(signal,action)); a same-observed-effect /
  different-cause trap (5b purist) isn't constructible here — T2 is the closest runnable
  instantiation (degraded capability, plausible observed effect, better untaught alternative).

### 3.4 Family 6 — regime-knowledge leakage (CLEAN)

- `agent_d_d2.zag` / `agent_d_d3.zag` use `_zag_arg` only for: (1) world path, (4) KB path,
  (2)/(3) output labels. Variant name/number never enters a decision.
- `parse_ints` (common.zag) skips `#`→newline; `kb_parse.zag` skips `#` lines — the world
  headers ("SHIFTED…", "ROTATION shift") and KB comments describing the shifts are never
  parsed. No `shift`/`regime`/`invert`/`degrad` keywords in any decision-path source
  outside comments.
- The effect model (`delib_update`) is fed only by `d2_step`/`d3_step` returns — the run's
  own observations. The R_true regime-correct KBs go only to the R_true arm by the runner
  scripts, per the arm definitions. **No leakage path found.**

### 3.5 Families 1 & 2 — failed attacks (robustness confirmed)

- **Reversal:** with all claims negated, D=4500 on home and D=3900 on shifted D2 —
  **identical** to true-claim runs. The predicate `mean < claimed/2` is sign-consistent
  (with claimed=−10 it distrusts only when observed < −5), so D behaves sensibly under
  sign-flipped KB content. Genuine robustness, worth keeping.
- **Flip:** swapped claims produce no distrust and no behavior change (D=4500=P).
  D does not *detect* the mislabeling — after n≥10 its score silently becomes the
  observed mean; the trace never represents "KB claim was wrong" as a first-class fact —
  but with these worlds it doesn't need to.

## 4. Anomaly (a) — D1's void shifts: half-overturned

Committed claim: storm-invert/move-rot show R_home=R_true=600 — "shift misses R's realized
policy" (H0), counted as neutral.

- **storm-invert: NOT a void — the metric hid real harm.** The generator
  (`gen_d1_worlds.py`, `in_zone=True`) deliberately starts R *inside* the storm zone so
  h2 (flee) fires. R's traces prove it fired: on `d1_a0`, R moves LEFT at exactly
  ticks 100–101 (20 ticks before storm 1 at t=120) and again at 340–343 (before storm 2)
  — 16–27 flee moves per run — then pays `storm_out=10`/tick outside the zone.
  Final energy: **r_home E = 100/187/73 vs r_true E = 196/196/198** on a0/a1/a2
  (r_true's KB replaces FLEE with WAIT). The shift intersected the realized policy and
  extracted a large, deterministic energy cost. R_home=R_true=600 only because the D1
  score is **ticks survived, capped at 600**, in a world retuned (C3) to be survivable.
  A1's "it avoids the storm zone entirely (so storm-invert never triggers)" is factually
  false. In energy terms the shift is valid *and* the harm is application-not-content
  (R_true's WAIT fixes it) — which would have **strengthened** H1/H3 to 3/3 domains.
- **move-rot: genuine design failure, worse than a void.** On all `d1_b*` variants R's
  stats are *identical* to R_true down to the integer (take=5, eat=131, comb=355,
  **move=0**, E=196). R's realized policy contains **zero moves** — it is a pure
  sitter (E never drops below 40, so h1/A_MOVE_TO_MOTE never triggers). A per-move cost
  of 6 applied to zero moves is zero: the shift **cannot bite in principle**, not merely
  "in this run". The generator docstring even anticipated "sitting and eating drifted
  motes is correct" — the shift was aimed at an imagined forager, not the realized
  sitter. Counting this as "neutral" puts a non-informative domain leg under K1.
- **K1 verdict:** still passes as written (2/3 with D1 neutral). But the taxonomy entry
  H0 is half-wrong, and the drawn lesson ("harm requires the shift to intersect the
  realized policy") misses the metric-saturation half: storm-invert *did* intersect,
  and the tick metric buried it.

## 5. Anomaly (b) — held-out uniformity: confirmed reskins

- `diff` on numeric content (comments excluded): **d2_hs0..hs3 are pairwise identical;
  d3_hs0..hs3 are pairwise identical.** The four files differ only in the header comment
  (`d2_hs0` vs `d2_hs1`…).
- The duplication is in the generator itself (`gen_sealed.py` loops `for i in range(4)`
  emitting the same table/breaks under four names). The "sealed family of 4 variants"
  is **1 unique shift per domain**, not 4. (Also: its docstring says "TOOL_1 degrades";
  the code and A4 correctly use TOOL_2.)
- The in-sample "variants" are equally duplicated **by design** (`gen_d2_worlds.py`:
  "Fixed balanced pattern (same for all variants…)"): all 6 D2 home worlds identical,
  all 6 shifted identical; all 4+4 D3 worlds identical. Totals: **D2 = 2 unique worlds
  out of 12 claimed; D3 = 2 out of 8; sealed = 1 out of 4 per family.**
- Consequence: every "median over variants" in A1/A4 is a median over identical copies
  (determinism makes the uniformity trivial), and K4(ii)'s "100%/95.8% of in-sample"
  generalization claim rests on **one held-out world per family** — which, for D2,
  differs from the in-sample shift in exactly **one table row** (s=0: HOLD-best instead
  of APPROACH-best; the s=3 row is byte-identical to the in-sample inversion).
- The seal itself is intact (SHA_LOG verifies) — this is a design-inflation issue, not
  tampering. **K4 verdict:** passes as written (closures reproduce: 90.0%, 77.3%), but
  the "held-out *family*" framing overstates the generalization evidence by ~4×.

## 6. Additional integrity notes

- **D3 "silent degradation" is not silent.** `d3_obs` (world_d3.zag) exposes
  `F_WEARx_OK` bits (wear bit clears at cond ≤ 50), and the home KB itself carries
  `F_WEARx_OK` preconditions (`kb/home_d3.txt`). A1's "it is silent — no observable
  fact indicates the loss" and EVIDENCE2's "the environment never announces it" are
  **false of the committed code** — the shift announces itself from tick ~150; R and D
  simply never consult PRE (neither matches on it). A precondition-checking reflexive
  agent would have handled D3 with no deliberation at all.
- K5 passes trivially (D≡R on home: 600/4500/60000 all 1.00×) — but note D1's D is a
  *different algorithm* from D2/D3's D, so "the fix" whose home-parity is being certified
  is not one thing.
- K6 passes as written; in energy terms D1's storm-invert shift is valid (>10% difference)
  and supports the H3 framing (application, not content).

## 7. Kill-bar verdicts (explicit)

| Bar | As-written verdict | Red-team qualification |
|---|---|---|
| K1 harm <2/3 domains | **PASS** (2/3) — no fire | Evidence is *stronger* than claimed: storm-invert harmed R in energy terms (metric hid it). Move-rot was non-informative by construction. |
| K2 closure <50% | **PASS** (90.0%, 80.7% reproduce) — no fire | T2/T3: same shift *type* with different timing/depth → **0% closure**, D≡R. H2's "broad" is overstated; recommend a follow-up bar, not a retroactive fire. |
| K3 decorative consciousness | **PASS** (100%; falls 90/80.7%; 0 mismatches) — no fire | Passes on a narrowed reading. Per-check: 2 of 3 prereg §2 checks decorative (0%); D1's EVAL fully decorative; audit-grade traces contain emitter-computed lines from an **uncommitted** file. The §2 evaluator spec was silently narrowed. |
| K4 hardcodes / held-out | **PASS** (no hardcodes in module; 100%/95.8% reproduce) — no fire | **Closest to a fire.** Frozen §3 ("ALL THREE domain agents import it") is violated by `agent_d_d1.zag`, which reimplements deliberation per-domain — the K4(i) audit scope (module only) cannot see it. Held-out "family" = 1 unique world; D2 held-out differs from in-sample in one row. |
| K5 home regression | **PASS** (all 1.00×) — no fire | Trivial; and "the fix" is two different algorithms across domains. |
| K6 content vs application | **PASS** (gaps >>10%) — no fire | In energy terms D1 also supports H3; implementer's D1 "void" classification was a metric artifact. |

**No kill bar fires as frozen.** But I would not sign "all bars pass" without amendments:
1. PREREG2 §3 is violated (D1 agent bypasses the shared module) — needs an amendment or a
   rebuilt D1 agent; the K4(i) audit must be rescoped to all three agents.
2. The §2 three-check evaluator was implemented as a one-check gate — the A3/K3 claim
   should be restated to the implemented evaluator, or the missing checks implemented.
3. `trace_emit.zag` (generator of the audit-grade TSV traces) must be committed, or the
   TSVs withdrawn as audit evidence — currently they are unreproducible from the repo
  and contain non-causal lines presented as deliberation.
4. Variant counts should be reported as unique worlds (D2: 2+1, D3: 2+1), and the A4
   generalization claim restated as n=1 held-out shift per family.
5. T2/T3/T4a are concrete, runnable counterexamples to "broad fix" generality and should
   enter the evidence record as open failure modes (0% closure regimes for the current gate).

## 8. Reproduction kit (all in `~/workspace/e1b_complete/redteam/wd/`)

- `src/` — copied committed sources + rebuilt binaries (`agent_d_d2/d3`, `agent_r_d2/d3`,
  `agent_p_d2/d3`; built with the pinned znc; byte-reproduces all committed scores).
- `worlds/trap_t1.txt` … `trap_t4b.txt`, `worlds/sealed/` — trap + sealed worlds.
- `kb/kb_rev_d2.txt`, `kb/kb_flip_d2.txt`, `kb/kb_flip2_d2.txt` — reversal/flip KBs.
- Trap result table (§3.3) is produced by e.g.:
  `./src/agent_d_d3 worlds/trap_t3.txt trap_t3 0 kb/home_d3.txt | grep RESULT`
- Anomaly (a): phase-1 D1 stats + traces in
  `/tmp/e1b_rt_runs/docs/lab/invention/survival/recall_fix/runs/phase1/results.txt`
  (extracted from the committed `runs/phase1/results.txt` archive); flee ticks verified
  at t=100–101 and t=340–343 on `d1_a0`.
- Anomaly (b): `diff <(grep -v '^#' …)` over `worlds/*.txt` and `worlds/sealed/*.txt`
  from the committed tree; generator sources `src/gen_d2_worlds.py`, `src/gen_sealed.py`.

**What I could not execute:** nothing material — the toolchain worked and disk sufficed
(lean workdir, ~1 MB). A same-effect/different-cause trap in the strict 5b sense is not
expressible in the D2/D3 domains (rewards are per-(signal,action) with no hidden state);
T2 is the closest runnable instantiation. The per-check neuter for precondition/conflict
is vacuous by source inspection (the checks have no decision-path existence) — no
stronger execution exists.
