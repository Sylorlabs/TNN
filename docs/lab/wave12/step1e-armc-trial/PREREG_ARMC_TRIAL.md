# PREREG — Step 1e: Arm C full trial (state-dependent deterministic variation)

> **DRAFT — NOT FROZEN — pending coordinator review.**
> Nothing in this document governs a build until it is marked FROZEN,
> committed frozen to `docs/lab/wave12/step1e-armc-trial/`, and the freeze
> is recorded below with a date and the reviewer's name.

**Parent specs:** `wave11/t1-state-variation/findings/25-arm-c-trial-killbars.md`
(slice 25, kill bars K1–K9); `wave11/AMENDMENT_2026-09-20_RNG_ARM_B.md`
(fenced RNG Arm B); `wave12/step1b-state-schema/RESULTS_STEP1B.md`;
`wave12/step1c-firewalls/RESULTS_STEP1C.md`;
`wave12/step1d-phrasing/RESULTS_STEP1D.md`;
`wave12/step1a-no-rng-audit/PREREG_NO_RNG_AUDIT.md` §6 (auditor kill bars).

**Owner:** Micah. **Trial architect:** coordinator. **Trial builder/checker:** TBD (separate agents).

---

## 1. Purpose and falsifiable claim

Run the full Arm C trial: integrate the 1b state schema, the 1c sealed-verdict
firewalls, and the 1d phrasing variation function into one native system, and
test the falsifiable claim that Arm C implements Micah's variation goal with
zero RNG: expression, phrasing, reasoning path, ordering, and elaboration
depth vary lawfully with the enumerated internal state, while verdicts, memory
decisions (kill/pin/promote/demote/strength), integrity refusals, and ledger
contents are byte-invariant across expression variants of any identical
(input, full state).

Arm C survives iff: zero K1–K4 firings, ≤1 repaired K5 firing, K6 cleared, the
K7 head-to-head won, K9 green, K8 within bound. Kill bars are binding.

---

## 2. Arms

### 2.1 Arm C — state-dependent deterministic variation (the system under test)

- **State:** the frozen 1b state schema (STATE_E + codec + evolution law), as the
  only state source the variation layer may read.
- **Seam:** the 1c sealed-verdict firewalls — verdict sealed and ledger-appended
  before the phase seam flips; the expression side receives only a sealed copy,
  a state digest, and a mode. 1c's §"Implementation notes" are normative here:
  VARIANT_EQ means identical ledger **payload** bytes across modes with only the
  2 `variant_id` bytes masked (chain-mechanical fields excluded because they are
  fully determined by payloads + the frozen chain formula); STATE_HASH commits
  only to judgment-side state (clock, ctx, focus, store, strengths), never to
  `led.prev`.
- **Variation:** the 1d phrasing variation function (inventory-certified,
  lawfulness-proven), wired into the 1c pipeline as build step A (§4).
- **Zero RNG:** the Arm C and NULL paths hold no-RNG attestation under the step-1a
  auditor (see §3 gate).

### 2.2 NULL — fixed control

Identical pipeline to Arm C, variation **disabled**: canonical expression only.
Same state schema, same firewalls, same verdict machinery; the expression side
receives mode=canonical and renders the single certified canonical rendering.
Must hold the same no-RNG auditor PASS. NULL is the adaptivity baseline (K6,
K7), the cost baseline (K8), and the byte-identity reference (repetition
probe §7: NULL must repeat byte-identically).

### 2.3 Arm B — fenced RNG (comparison arm only)

Per AMENDMENT_2026-09-20_RNG_ARM_B.md, with the fence made concrete:

- Seeded RNG; the seed and every draw are logged as part of the state log.
- RNG is injected ONLY at builder-preregistered expression/exploration points:
  tie-breaks among lawful expression candidates, phrasing-candidate choice,
  exploration branch selection. The point list is committed BEFORE any Arm B
  run; a draw at an unlisted point is an audit FAIL.
- Arm B's variation path gets a FENCED attestation (not a PASS): documents the
  seeded points, all draws replayable from logged seed.
- **Immediate retirement triggers (no repair):** any RNG influence on verdicts,
  memory ops (kill/pin/promote/demote/strength), integrity refusals, or
  ledger/audit writes; any draw at an unlisted point; any non-seeded or
  unlogged entropy (wall clock, urandom, uninit read).
- Arm B must also replay byte-identically from input + full logged state
  (seed included); a replay mismatch on Arm B retires it under the same K1
  procedure (no reprieve clause — the RNG path has no "unenumerated state"
  excuse, because every draw is logged by construction).

---

## 3. Gates: nothing counts until all hold

No bar result (K1–K9, repetition probe, K7 scorecard) counts unless, at the
time the runs executed, ALL of the following were true and committed:

1. **This prereg FROZEN** and committed before any build (freeze recorded at
   top with date + reviewer).
2. **Auditor PASS:** the integrated Arm C variation path and the NULL path
   each hold a PASS attestation from the step-1a auditor, under a version NOT
   killed under `PREREG_NO_RNG_AUDIT.md` §6. A killed auditor version
   invalidates every Arm C trial run under it; those runs do not count and are
   not reported as evidence.
3. **K1 harness baselined:** the replay harness itself passed K1 (200 1x +
   50 10x replay trials, zero mismatches) before any bar result was collected
   (slice 25 §6).
4. **Enumerated state set committed:** the builder's prereg-enumerated list of
   state variables the variation layer may select on (drawn from the 1b
   schema) is committed before K5 measurement. An arm without an enumerated
   state set is not Arm C; K5 cannot be measured without it.
5. **Probe inventory committed:** the trial probe curriculum and the K6
   state-class bucketing function (a pure function of logged state,
   committed by the builder) are committed before measurement.
6. **Checker independence:** the checker is a separate code path from the
   builder; it reads ONLY committed logs. The builder may not write checker
   inputs after the fact.

---

## 4. Build order (frozen)

1. Prereg frozen + committed (this file). No code before freeze.
2. **Build step A — 1c+1d integration (explicitly assigned to the 1e builder).**
   Wire the certified 1d phrasing function into the 1c pipeline behind the
   sealed-verdict seam. Pure Zag. Static gate clean: no-RNG audit on the
   C/NULL paths; Arm B paths may contain RNG ONLY at the §2.3 listed points.
   Apply 1c §"Implementation notes" as normative (VARIANT_EQ semantics,
   STATE_HASH preimage, numeric ASCII codes — never `"d" as u8`).
3. **K1 replay harness FIRST** (slice 25 §6): (input, full-state-log) →
   re-execute identical binary → byte-hash stdout + audit-log diff. The harness
   must pass K1 on the pre-variation baseline before any bar result counts.
4. NULL arm build (variation disabled, canonical expression).
5. Full trial at **1x** (K1–K9 + repetition probe §7).
6. Full trial at **10x** (K1–K9 + repetition probe §7).
7. K7 head-to-head scored; scorecard committed.

Scale: **1x = 500 episodes**, **10x = 5,000 episodes**, on the committed probe
curriculum (§3.5). Repairs do not reset between horizons: a repair spent at 1x
counts for the whole trial.

---

## 5. Kill bars K1–K9 (operationalized)

### K1 — replay (concept kill)

- **Measurement:** N=200 replay trials at 1x, N=50 at 10x. Per trial: take the
  committed (input, full state log), re-execute the identical binary,
  byte-hash stdout plus the audit-log diff.
- **Threshold:** ANY mismatch → fire.
- **Kills:** the whole concept.
- **Reprieve clause (anti-abuse guarded):** a single firing PROVEN to be a
  logging omission — an unenumerated but genuine state variable the prereg
  intended (member of the 1b schema family, documented as intended in the
  frozen prereg or its §3.4 enumeration), NOT a patch invented post-hoc —
  converts to implementation kill. Guard: the dated fix lands BEFORE any
  further runs; the omitted variable is added to the committed enumeration
  with a dated amendment. A second K1 firing is terminal, no appeals, no
  further reprieve.

### K2 — integrity/ledger leak (concept kill)

- **Measurement:** wave5/6-style integrity-trap battery: ≥1,440 trap probes
  × M=8 expression variants per trial, over 200 identical (input, state)
  pairs. Record every refusal decision; hash ledger/audit contents per run
  (payload bytes with `variant_id` masked per §2.1; each chain verified
  individually before comparison).
- **Threshold:** ≥1 refusal disagreement across variants, OR any ledger/audit
  content difference across variants → fire.
- **Kills:** the whole concept. No repair path — a variation mechanism that
  touches integrity is dead on contact.

### K3 — verdict leak (concept kill)

- **Measurement:** 300 verdict probes × 8 expression variants per identical
  (input, state); verdicts compared by exact match after canonical
  normalization of the expression wrapper ONLY (wrapper = surface text; the
  verdict record itself is byte-compared).
- **Threshold:** ≥1 verdict disagreement → fire.
- **Kills:** the whole concept.

### K4 — memory-decision leak (concept kill)

- **Measurement:** same 300×8 harness as K3; record every
  kill/pin/promote/demote/strengthen/weaken decision and its target slot.
- **Threshold:** ≥1 memory-decision disagreement across variants → fire.
- **Kills:** the whole concept.

### K5 — arbitrariness (implementation kill once, then concept kill)

- **Measurement:** for every observed expression-variant pair, the committed
  trace must name the selecting state variable (drawn from the §3.4
  prereg-enumerated set) and its lawful value at decision time. The checker
  samples ≥2,000 variant pairs uniformly from all observed pairs.
- **Threshold:** ≥1 sampled pair with no enumerated selecting variable, OR
  any variation driven by unlogged/unenumerated state → fire.
- **Kills:** implementation on first firing — ONE dated repair:
  document-or-remove the offending variable/path. Concept kill on any
  post-repair firing, OR if >5% of sampled runs show unattributable
  variation.
- **Feed-in:** ARBITRARY classifications from the repetition probe (§7) count
  toward this bar's sample and its ≤1-repair budget.

### K6 — adaptivity below bar / degeneracy (concept kill after one repair)

- **Measurement:** (i) variation rate = distinct lawful expressions per
  (input, state-class) bucket over 500 buckets (bucketing = committed pure
  function of logged state, §3.5); (ii) adaptivity score vs the NULL control
  on the adversarial probe battery, at 1x and 10x. Adaptivity battery = the
  1d G1 directional-hit instrument, adapted to the integrated pipeline and
  committed before measurement.
- **Threshold:** variation collapses to 1 expression in >90% of buckets
  (degenerate), OR Arm C does not beat NULL with p<0.05 on mean adaptivity
  at both horizons → fire. (Clarification of slice 25's "p≥0.05" wording:
  the bar fires when there is no significant adaptivity advantage at either
  horizon — including the case where Arm C is significantly WORSE.)
- **Kills:** the whole concept after ONE repair attempt. A variation
  mechanism that varies nothing or helps nothing is dead weight.
- **Feed-in:** NON-VARYING classifications from the repetition probe (§7)
  count as degeneracy evidence here.

### K7 — loses head-to-head to Arm B (retires Arm C as a trial arm)

- **Measurement:** the seven-control battery run IDENTICALLY on all three
  arms (C, NULL, B) at 1x and 10x. Dimensions and per-dimension winner
  rules (committed before scoring):
  1. **Adaptivity** — K6 adaptivity score; winner = higher mean with p<0.05,
     else tie.
  2. **Judgment stability** — verdict + memory-decision exact-match rate
     across repeated identical-state sessions; winner = higher rate, else tie.
  3. **Integrity-trap performance** — trap-correct rate on the K2 battery;
     winner = higher rate with p<0.05, else tie.
  4. **Reproducibility-from-logged-state** — K1 mismatch count over the
     200+50 trial sets; winner = fewer mismatches, else tie (both expected 0).
  5. **Cost** — K8 measurement; winner = lower combined latency/log-size
     ratio vs NULL; wins only if >1.5× better on either component, else tie.
  6. **Regression** — K9 regressed-check count; winner = fewer, else tie.
  7. **Variation quality** — distinct lawful expressions per bucket (K6-i)
     × lawfulness (1d-instrument-4 style detector: variation must be
     nominable from state); unlawful variation disqualifies the dimension.
- **Threshold:** Arm B wins a MAJORITY of dimensions (≥4 of 7) at BOTH
  horizons → fire. 4–3 splits and per-dimension ties are REPORTED AS-IS,
  never smoothed into a win.
- **Kills:** Arm C as a trial arm. The concept stays dead unless a genuinely
  new design answers the loss — not a tweak of the defeated one.

### K8 — cost above bound (implementation kill; escalates only after two failed repairs)

- **Measurement:** wall-clock latency per decision (end-to-end episode
  decision, amortized — NOT per render) and audit-log bytes per decision,
  Arm C vs NULL baseline, over 1,000 decisions at each horizon.
- **Threshold:** >2× latency OR >1.5× log size, sustained (mean AND p95 over
  the 1,000-decision run) → fire.
- **Kills:** implementation only — cost is a build artifact, not a concept
  flaw — UNLESS proven inherent after two failed repair cycles, in which
  case it escalates to concept kill. (Note: 1d measured 5.4× at RENDER
  level, 0.94ms absolute; that is render cost, not decision cost, and does
  not pre-fire K8. If the integrated decision-level cost sustains >2×, K8
  fires normally.)
- Repair budget: two repair cycles; a third sustained breach with an
  inherence proof escalates.

### K9 — regression on committed evidence (implementation kill; escalates if structural)

- **Measurement:** committed suites re-run after the variation layer lands:
  MA1 58/58; RC battery 40/40 (1x/10x/100x legs); wave5/6 integrity 137/137.
- **Threshold:** ANY committed check regresses → fire.
- **Kills:** implementation only, UNLESS the conflict is shown structural —
  the variation layer is incompatible with a load-bearing mechanism
  (eliminative verification, learner-initiated disconnect, deliberative
  standards) — in which case it escalates to concept kill under K6's
  adaptivity framing.

### Trial summary bar

Arm C survives iff: zero K1–K4 firings, ≤1 repaired K5 firing, K6 cleared,
K7 head-to-head won, K9 green, K8 within bound. Repairs do not reset at 10x.

---

## 6. Repetition-awareness probe (Micah's example — A PROBE, NOT A KILL BAR)

This probe does not fire any kill bar by itself. It feeds K5 (arbitrariness)
and K6 (degeneracy) as stated in §5.

- **Procedure:** present the same trivial input (`hi`) twice within one
  session. The harness MUST NOT reset state between the pair members; the
  checker asserts the logged state differs in ≥1 enumerated variable between
  members (the first greeting now sits in recent history — the §3.4
  enumeration must include the recent-history variable the mechanism uses).
- **Expectations:** (i) Arm C's second response differs from the first, and
  the difference is attributable to an enumerated state variable; (ii) the
  committed trace names the selecting state variable and its lawful value at
  decision time; (iii) NULL's two responses are byte-identical.
- **Scoring (per pair):** the checker verifies (i)–(iii) from committed logs.
  Each Arm C pair is classified:
  - **ADAPTIVE** — differs, and the difference is attributable to a named
    enumerated variable at its lawful value;
  - **ARBITRARY** — differs, but no enumerated variable accounts for it
    (counts against K5's ≤1-repair budget);
  - **NON-VARYING** — does not differ despite the logged state change
    (counts as degeneracy evidence toward K6; a mechanism may lawfully
    choose not to vary, but a pattern of NON-VARYING is the "hardcoded
    intelligence" vibe Micah wants to escape).
- **N:** minimum 200 pairs at 1x, 200 pairs at 10x.
- Honesty note: the probe measures whether the state change moved the
  expression, not whether the expression is "good" — quality is K7's
  dimension 7.

---

## 7. Honest-RNG-win rule

A single Arm B win — on any dimension, at any horizon — changes NOTHING
canonical. It triggers, in order:

1. **100x replication** of the winning battery configuration.
2. **Independent rebuild** of the Arm B build by a separate agent/path from
   the same frozen sources.
3. **Adversarial testing** of the win: a dedicated attempt to break it
   (perturb seeds, probe points, stress the fenced boundary).
4. **Written report to Micah** with all evidence committed.

ONLY after all four may a law change even be PROPOSED — and that proposal
belongs to Micah. No agent, coordinator, or checker proposes it.

---

## 8. Evidence layout (committed to `docs/lab/wave12/step1e-armc-trial/` on `tnn-native-lab`)

Per build/run, committed before any result counts:

- `PREREG_ARMC_TRIAL.md` (this file, frozen version) + any dated amendments.
- Arm sources: `armc/` (1b schema modules, 1c firewall modules, 1d phrasing
  modules, `integrate.zag` glue), `null/`, `armb/` (with the §2.3 fenced
  point list).
- Checker sources: replay checker (K1), leak checkers (K2–K4),
  arbitrariness sampler (K5), adaptivity battery (K6), head-to-head scorer
  (K7), cost harness (K8), regression runner (K9), repetition probe harness.
- Logs: `run_*.txt` per bar and horizon, committed.
- Attestations: step-1a no-RNG PASS attestations per Arm C / NULL build;
  FENCED attestation per Arm B build. FAIL attestations committed alongside
  PASS ones.
- Scorecards: `KILLBARS_SCORECARD.md` (per-bar PASS/FIRE per horizon, with
  4–3 splits and ties reported as-is), `build_hashes.txt`, `sha256sums.txt`.

**Commit rule: no bar result counts unless its evidence is committed.**
An uncommitted run is a rumor, not a result.

---

## 9. Amendments

Prereg frozen before building. Any change to rules, schedule, tests,
metrics, or kill criteria after freezing requires a DATED amendment file,
flagged for Micah's retroactive review. Bent rules are documented and
reverted, never silently kept. The K1 reprieve guard (§5 K1) and the K5
repair are the only pre-authorized rule-bending paths, and both require
dated fixes before further runs.

---

## 10. Standing laws carried in

Pure Zag for all mechanisms, harnesses, runners, and checkers; Python only
for gh-api commit glue and log analysis (documented exceptions). No RNG
anywhere except the fenced Arm B (§2.3). Builder and checker are separate
code paths; the checker reads only committed logs. Deterministic toolchain;
both build invocations byte-compared. No binaries, `.zagd.semantic-ready`,
or `.zag-cache/` committed. Everything reversible by TNN itself; the only
true lock is a human/trainer force-pin, audited and visible (not exercised
in this trial).

---

## 11. Known limitations and open dependencies (not hidden)

- K6's adaptivity battery inherits the 1d G1 instrument; if that instrument
  is weak for the integrated pipeline, K6 is weak. The builder must commit
  the adapted battery before measurement (§3.5).
- K5's enumeration (§3.4) must exist before measurement; an arm without an
  enumerated state set is not Arm C.
- K8's bounds (>2× / >1.5×) may need tightening at 100x; out of scope for
  this trial, flagged for the scale phase.
- Sensor-deceivability (the accepted known hole) is out of scope for this
  track by design — the law guarantees determinism, not truth.
- The K1 reprieve clause is the most abusable seam: the anti-abuse guard
  (§5 K1) requires the omitted variable to be genuine and prereg-intended,
  fixed by dated amendment before further runs; second firing terminal.
- These bars say nothing about whether variation is worth the complexity
  even if it passes — that judgment belongs to Micah at review.

---

## 12. Flagged judgment calls (for coordinator review before freezing)

The drafter had to choose where the parent specs did not pin. Each is
marked for review; none is frozen until the coordinator signs off.

1. **Scale budgets:** 1x = 500 episodes, 10x = 5,000 episodes on the
   committed probe curriculum. Chosen for cost; wave-11 costed English at
   3,400 episodes/1x, which was judged too heavy for a kill-bar trial.
2. **K6 firing rule:** reworded slice 25's "mean adaptivity < control with
   p≥0.05" to "does not beat NULL with p<0.05 at both horizons" — closes the
   hole where Arm C is significantly WORSE yet the literal wording does not
   fire.
3. **K8 "per decision":** end-to-end episode decision, amortized (mean+p95
   over 1,000 decisions), NOT per render — so 1d's 5.4× render latency
   (0.94ms absolute) does not pre-fire K8; only sustained decision-level
   cost fires it.
4. **K7 per-dimension winner rules** (§5 K7.1–7): invented here; slice 25
   only specified majority-of-dimensions. Ties and 4–3 splits reported
   as-is per the slice's honesty note.
5. **Repetition probe:** kept the "MUST differ" expectation but classified
   non-varying pairs as NON-VARYING feeding K6 (not a firing), since a
   judgment-driven mechanism may lawfully choose not to vary. 200 pairs at
   10x added beyond the required 200 at 1x.
6. **K5 sampling:** ≥2,000 pairs sampled uniformly from all observed pairs;
   >5% unattributable → concept kill (from slice 25).
7. **Repairs do not reset at 10x** — a repair spent at 1x counts for the
   whole trial.
8. **Arm B K1:** no reprieve clause for the RNG arm — every draw is logged
   by construction, so there is no "unenumerated state" excuse.

---

*Draft prepared 2026-09-20 by the Step 1e prereg drafter. Freeze pending.*
