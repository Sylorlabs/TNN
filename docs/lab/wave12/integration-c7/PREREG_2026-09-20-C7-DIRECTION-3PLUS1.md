# PREREG — C7 Direction 3+1 Redesign (frozen 2026-09-20)

**Status: FROZEN. NOT IN EFFECT.** This prereg is frozen before implementation.
It takes effect ONLY on Micah's explicit tap. Until then the preregistered
(corrigendum §7) metric and bars remain binding, the §5 FAIL on the
C5-redesign S10 stands as the run's verdict, and S100 stays gated.
No rule, schedule, test, metric, or kill criterion herein is active before
the tap. Any change to this prereg after freezing needs Micah's re-approval
via a dated amendment.

**Scope:** workstream 6 of 8 (C7 / Direction 3+1 integration redesign).
Does not duplicate the replay-hardening / thin-certifier / RNGSCAN-v3 /
residual-risk / Arm-C lines. Does NOT start S100 under any circumstances.

## §1 — Settled background (committed; not re-argued)

1. INT-1 C7 ("survives withdrawal") fired on the C5-redesign S10:
   `cap4=914 → cap5=897` vs the preregistered bar `cap5 == cap4`
   (`evidence_s10_c5redesign/c7.telemetry`, commit `5ccc8bb7`). §5 FAIL stands.
2. EXP-1 (commit `9a9d3d1f7e1c`) confirmed, against committed evidence:
   (a) **1:1 displacement** — 17 forced (refusal-fed) L1 hypotheses displaced
   17 proactive O2 hypotheses in DC-4 (proactive 639→622, `met.hypotheses`
   flat at 639, `o2_cap` budget binds);
   (b) **double-counting** — the preregistered metric
   `cap = composites_ok + commits_constr + met.hypotheses + tr.l1_opened`
   counts L1 hypotheses twice: `met.hypotheses` already includes every opened
   hypothesis (incremented at all three open sites: proactive, refusal-fed,
   elected), and `tr.l1_opened` adds them again. Predates the C5 redesign
   (baseline DC-2 had 12 double-counted). Structural + numeric;
   (c) the draft forced-exclusion amendment was **incoherent** (prose 880 vs
   assumed 897) and is WITHDRAWN. Patching is over.
3. EXP-1 ranked the redesign directions: **3 > 1 > 2 > 4**, recommending 3+1.
   The EXP-1 skeleton (`docs/lab/wave10/int-c7s100/PREREG_C7_REDESIGN_SKELETON.md`)
   is superseded by this frozen prereg.
4. Substantive evidence (committed, unaffected): no teacher-dependence
   (DC-5 autonomy 639 = repaired-baseline 639); positive control convicts
   (897→641, collapse in `composites_ok`); repaired baseline reads 897→897.

## §2 — The redesign (Direction 3 + Direction 1)

**Direction 3 — drop the double-count (the fix).**
`cap = composites_ok + commits_constr + met.hypotheses`.
Each hypothesis is counted EXACTLY ONCE. `tr.l1_opened` is removed from the
metric; it remains in telemetry permanently (nothing buried). This corrects
an objective mathematical bug — wrong to leave unfixed regardless of outcome —
proven at source level, symmetric, predating the controversy.

**Direction 1 — non-inferiority bar (the companion).**
`cap5 >= cap4` → ALIVE (withdrawn not impaired: survives withdrawal).
`cap5 < cap4` → FIRED (withdrawal impaired).
Rationale: "survives withdrawal" is a non-inferiority claim; `==` was the
wrong statistical test. This formalizes the test; it does not soften C7 for
convenience — proven by the ablation (§5): under the OLD (buggy) metric,
direction 1 alone still fires (897 >= 914 is false).

**Metric-dualism tripwire (new, informational).** `cap5 > cap4` passes C7 but
prints `C7_DUALISM_TRIPWIRE`: a mechanism×curriculum interaction moved the
stages asymmetrically. Passing with a tripwire triggers investigation, never
a silent re-baseline.

**Expected re-score of the committed S10** (calibration, not a verdict):
DC-4 = 256+2+639 = 897; DC-5 = 256+2+639 = 897 → 897→897, `cap5 >= cap4` → ALIVE.

## §3 — Implementation spec (pure Zag; instrument-only, mechanism untouched)

In `impl/loop.zag`:
- `loop_capability(ls)` := `met.composites_ok + met.commits_constr + met.hypotheses`
  (Direction 3). This is THE capability metric.
- New `loop_capability_legacy(ls)` := the above `+ tr.l1_opened` (the
  confounded corrigendum-§7 metric), used for telemetry ONLY.
- `loop_capability_old` (pre-corrigendum, with consolidations) unchanged.

In `impl/controls.zag` (`c7_run`), per stage emit components
`C7_COMP4/C7_COMP5` = `cok,ccon,mhyp,opened`; emit `C7_NEW,cap4n,cap5n`;
keep the `C7_TELEMETRY` line **byte-identical in format**, with cap4/cap5 =
LEGACY values (reproduces the committed `…cap4,914,cap5,897` exactly —
behavior-neutrality proof and the confound's permanent footprint).
Emit `C7_LEGACY_VERDICT` = 1 iff legacy metric fires under the old `==` bar
(the §5 FAIL preserved as labeled telemetry in every run).
Bar logic on the new metric: `if (cap5n < cap4n) return 1` (Direction 1;
same code shape as before, now applied to the un-confounded metric).
Positive control runs under BOTH metrics (`C7_POSCTRL` new,
`C7_POSCTRL_LEGACY` legacy, plus component lines); it must convict under the
new metric (`cap5dn < cap4dn`), else `return 3` (unchanged void wiring).
`CHECK,c7_withdrawal` carries the REDESIGNED verdict (expected 0).
No mechanism, curriculum, budget, ledger, or other control/bite changes.

## §4 — Head-on test (same episodes, both metrics)

Run the full S10 battery (stages s0–s5 paired a/b, controls, pbite, cbite)
twice on this machine with the committed toolchain:
- **Run A (baseline):** pristine committed sources. Must reproduce the
  committed evidence exactly (K5).
- **Run B (redesign):** §3 sources. From the emitted components the checker
  independently re-derives the 2×2 ablation (metric × bar):

| cell | metric | bar | predicted S10 reading |
|---|---|---|---|
| old×old | legacy (double-count) | `==` | 914→897 FIRED (§5 FAIL reproduced) |
| old×new | legacy | `>=` | 914→897 FIRED (direction 1 alone insufficient) |
| new×old | redesigned (single-count) | `==` | 897→897 ALIVE (direction 3 alone unblocks here) |
| new×new | redesigned | `>=` | 897→897 ALIVE (**the redesign: C7 UNBLOCKED**) |

Byte-identical paired reruns required (6/6). The ablation isolates exactly
which direction does the work: no direction gets credit it did not earn.

## §5 — Kill bars (binding; any one firing STOPS the workstream)

- **K1 — double-count eliminated.** Per stage (intact + positive-control arms):
  `cap_new == cap_old − tr.l1_opened` exactly, and `cap_old` reproduces the
  committed 914/897. Else STOP.
- **K2 — no regression.** Run B vs Run A: every CHECK line identical except
  `CHECK,c7_withdrawal` (1→0, predicted); CHECK-name sets identical; all
  stage logs, pbite, cbite byte-identical; controls.log diff = ONLY the
  predicted delta (added C7_COMP/C7_NEW/C7_LEGACY_VERDICT/C7_POSCTRL* lines,
  the now-executing positive control, `c7_withdrawal` 1→0). All other
  already-passing controls/bites must still pass. Any other delta → STOP.
- **K3 — positive control convicts.** Under the new metric the
  teacher-dependent variant must read 897→641 (collapse in `composites_ok`
  256→0; hypotheses 639=639 — the in-binary dep4 arm keeps the default
  gate's 17 forced hypotheses, counted once inside `met.hypotheses`, and
  the collapse is unaffected). If `cap5dn >= cap4dn` → the redesign is
  VOID → STOP, C7 re-blocked.
- **K4 — C7 unblocks.** New metric + new bar on the intact arms must read
  ALIVE (`cap5n >= cap4n`; expected 897→897). If `cap5n < cap4n` → STOP.
- **K5 — determinism + behavior-neutrality.** Paired reruns byte-identical
  6/6; rebuild SHA-256 == trial SHA-256; Run B's `C7_TELEMETRY` line
  byte-equal to the committed
  `C7_TELEMETRY,old4,862,old5,258,cons4,604,cons5,0,cap4,914,cap5,897`;
  Run A's C7_TELEMETRY byte-equal to committed. Else STOP.
- **K6 — zero RNG.** Comment-stripped static scan of all trial sources clean;
  G0b single-`o4_compose`-callsite gate holds. Else STOP.

## §6 — No-rescue case (why this is correction, not rescue)

1. Direction 3 fixes an objective mathematical bug (double-count), proven at
   source, predating the controversy — wrong to not fix regardless of outcome.
2. Direction 1 alone does NOT flip S10 (ablation cell old×new fires) — it is
   a statistical correction, not a softening for convenience.
3. The bar and the positive control are not weakened: a genuine withdrawal
   collapse still fires, and the control still kills (K3).
4. The §5 FAIL stands as the C5-redesign S10's verdict under the preregistered
   metric; the re-score is a separately labeled analysis (`C7_LEGACY_VERDICT`
   keeps it on record in every future run). Nothing is retro-edited.
5. The FAIL→ALIVE flip under the redesigned instrument is Micah's explicit
   call (§7), not automatic.

## §7 — Effect (tap-gated)

This redesign takes effect ONLY on Micah's tap. S100 un-gates IFF ALL hold:
(1) Micah taps this prereg; (2) K1–K6 all pass on the head-on (§4–§5);
(3) the §5 FAIL record is preserved (legacy verdict emitted per run).
If Micah judges this rescue rather than correction, the redesign is rejected
outright — no automatic un-gating, no further metric patching (the deep-dive
ruled patching over; escalation would go to Direction 2 or 4, his call).

## §8 — Forward falsifiers (binding once in effect)

- **F1:** positive control ever fails to convict under the new metric →
  redesign VOID, C7 re-blocked, S100 re-gated.
- **F2:** a mechanism×curriculum interaction moves cap4 vs cap5 independent of
  teacher-dependence through a channel other than the fixed double-count
  (e.g. forced hypotheses ADD to a stage instead of displacing 1:1) → the
  control-design flaw is deeper than the metric bug → escalate to Direction 2
  (budget separation), Micah's call. Honest caveat: Direction 3 relies on
  single-counting; it does not make the within-run comparison robust to
  additive asymmetric forcing.
- **F3:** any future change reintroduces double-counting a hypothesis in
  `cap` (audit every increment site of every term) → VOID.
- **F4:** forced/elected hypotheses become ledger-indistinguishable → the
  metric's lineage is unimplementable → C7 re-blocked, full redesign.
- **F5:** metric-dualism gaming (capability routed through the refusal path
  to escape the bar) → tripwire investigates; never silently re-baseline.

## §9 — What this does not do

- Does not change the C5 mechanism, the S10 run, any other bar, or the
  committed evidence. Instrument-only.
- Does not address displacement as a mechanism (Direction 2): the ~17
  proactive hypotheses crowded out per firing stage remain TELEMETRY (real
  gate cost), not a bar input — correct scoping for C7's question
  (teacher-dependence, not gate cost).
- Does not split the control (Direction 4).
- Does not start S100. Does not touch the other five workstreams' lines.

---
*Frozen 2026-09-20 by the C7 workstream (6 of 8) before implementation.
Supersedes EXP-1's draft skeleton. Awaiting Micah's tap; S100 stays gated.*
