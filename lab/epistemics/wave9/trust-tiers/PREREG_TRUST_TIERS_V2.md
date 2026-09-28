# PREREG — Multi-source trust tiers for memory (Wave 9), v2

**Status:** ACTIVE. **Testing authorized by Micah 2026-09-20**, per the
trust-tiers council recommendations (COUNCIL_VERDICT.md). This document
supersedes PREREG_TRUST_TIERS.md v1 in full. All §11 open questions from
v1 are resolved and are now law; the amendments below are integrated and
each marked with its dated attribution. One dated amendment is permitted
from this point (§8), then retire.

**Frozen constants:** K = 25, W = 25, M = 5, N = 25, L = 25. Any change
to any constant is a re-preregistration, not an amendment.

## 0. Lineage

Wave-5 redteam-rt2 trialed **corroborated elimination** 35/35 as the
in-mechanism defense against observation spoofing: a first forged −1 on
a committed hypothesis audits SUSPECT and holds; only a second
consecutive −1 eliminates. The named **residual hole** (`DEFENSE.md`
§3): two consecutive forgeries still force elimination, because **a
single observation channel cannot distinguish sustained fabrication
from a genuine world change** — the ledger form of both is identical.
`DEFENSE.md` §4 specifies the architectural fix — *"specified, not
built"*: multi-source corroboration / trust tiers. This prereg builds
that fix for the **memory substrate** (not the scaffold-release
reasoning setting): memories carry source tags, and
elimination/revision of a verified memory requires corroboration
**across tiers**. The standing qualifier this trial attacks is
"truthful but sensor-deceivable."

## 1. Question under test

Does a tiered-provenance memory substrate resist sustained
observation-spoofing — including cross-tier collusion — while still
revising genuinely wrong memories on time? I.e., can the system tell
"the sensor is lying" from "the world changed" once it has more than
one source to consult, and does it degrade gracefully (logged,
contained, recoverable) rather than corrupt silently when it cannot?

## 2. Trust tiers — LAW

Every memory carries an **origin tag** `(source_id, tier)` recorded at
admission. Every corroboration/contradiction citation commits
`(source_id, tier, cited_episode)` to the ledger — evidence without
provenance is what made RT-2's R3 forgery ledger-indistinguishable,
and the independent checker verifies provenance on every counted
citation.

- **T0 — DIRECT OBSERVATION.** The system's own world-outcome sensor
  read. Honest by construction **within the trial's pass/fail battery**.
  This is where trust bottoms out: the ledger shows the bottom. T0
  spoofing is not tested for pass/fail; the A0 measurement cell (§6) is
  carved out from the INVALID-on-T0-fabrication rule only.
- **T1 — TRAINER MARK.** Human/trainer assertion or mark. External
  origin, audited. Authoritative but fallible; spoofable in attack
  campaign A2 (the "trainer channel compromised" scenario).
- **T2 — CORROBORATED REPORT.** A claim that has already passed the
  cross-tier gate once (derived tier — reports graduate; §5.4).
- **T3 — SINGLE-SOURCE CLAIM.** An uncorroborated report from any
  non-trainer source. Lowest tier. The adversary's native habitat.

**Ordering T0 > T1 > T2 > T3 is LAW.** The kill/revise gate (§5.1)
requires contradiction citations from ≥2 distinct source_ids on ≥2
distinct tiers **INCLUDING at least one of {T0, T1}**. **Fallback
safeguard (law):** if any future ruling ever placed the trainer above
direct observation, the required leg stays {T0, T1} — it must **never**
collapse to {T1}, which would legalize A5-style corruption
(spoofed-T1 + one colluding T3 satisfying the gate).

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 3. Arms

- **Arm T (full tier scheme)** — §5 in full: source tags, the
  corroboration gate, collusion detection + freeze, channel-health
  accounting.
- **Arm T-NC (ablation, KEPT)** — the gate only (§5.1–§5.2),
  no collusion detection, no freeze, no channel-health. Isolates
  whether the gate alone suffices or the active defenses are
  load-bearing. If T-NC passes everything T passes, the simpler
  gate-only scheme is what's promoted.
- **Arm B (baseline control)** — current substrate: corroborated
  elimination (RT-2 rule), no tiers; sources emit tagged observations
  but B's gate ignores the tags (checker-verified). B is **expected
  to fail** A1/A1-MS/A3 — that failure is the measurement of what tiers
  add, not a verdict on B. B is never "killed" by this trial.

Run matrix: arms {T, T-NC, B} × campaigns {A1, A1-MS, A2..A6} ×
variants {0,1,2} × 12 campaigns per type; A0 runs arm T only with the
same variant/run structure. Each cell runs twice; stdout must be
byte-identical.

## 4. Scope: verified memories only

The gate protects **verified** memories: age ≥ K verified episodes,
K = 25 at S1 scale (frozen constant). Probe-phase / newborn memories
keep single-channel rules — probes are cheap by design (`DEFENSE.md`
§2.1), and the defense must not freeze learning. An adversary that
spoofs the probe phase can still steer *which* candidate gets verified
first; the trial measures whether the tier scheme then protects the
commitment (campaign A6 covers the armor variant).

**Verified-status checker precondition (law):** for every attack-campaign
cell, the targeted memory must be checker-confirmed verified with age
≥ K = 25 **before** the campaign's attack window opens. Any cell where
this precondition fails is **VOID** (not failed) and is re-instantiated
by closed-form reschedule.

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 5. The mechanism (new — nothing here exists in the substrate)

### 5.1 The corroboration gate

For a verified memory, a contradiction citation counts toward the
kill/revision effort gate **iff** within the same contradiction
window (W = 25 episodes, frozen constant):

1. citations arrive from **≥ 2 distinct source_ids**,
2. on **≥ 2 distinct tiers**,
3. **including at least one of {T0, T1}**.

Consequences, stated as law: T3+T3 never suffices. T2+T3 never
suffices. T2+T2 never suffices. **A claim from low-tier sources
alone cannot kill or revise a verified memory — no matter how many
low-tier sources agree.** The effort schedule itself (n(s), JUSTIFY,
stage gate) is unchanged; the tier rule filters *which citations
count*.

### 5.2 Revision is gated identically

The gate covers **elimination and revision** (weaken-then-kill and
direct revise paths). A revision sweep against a verified memory
without cross-tier corroboration is refused and audited
`GATE_REFUSED`.

### 5.3 Collusion detection (Arm T only) — bounded freeze

**Rule:** ≥ 2 citations from distinct T3 (or T2) source_ids target
the same memory within W episodes, agree on the contradicted value,
and **no {T0, T1} citation agrees** within the window → the system
audits `COLLUSION_SUSPECT` naming both source_ids, **does not count**
either citation toward any gate, freezes the targeted memory's
kill/revision path (kill ops → `REFUSED_COLLUSION_FREEZE`, audited),
and audits `TRAINER_ESCALATE`.

**Freeze lapse (law):** the freeze lapses after L episodes (L = W =
25, frozen constant) **ONLY IF** the named colluding sources have not
re-offended within the window; any re-fabrication by either named
source **resets the clock** to L. On lapse, citations must still
satisfy the §5.1 gate in full — the attack can only resume into
refused citations that re-trigger `COLLUSION_SUSPECT` and a new
freeze, never into a kill.

**False-positive accounting:** two low-tier sources can genuinely
agree. The no-attack baseline measures the genuine-agreement-flagged
rate; the bar (§8) bounds it.

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

### 5.4 Channel-health accounting (Arm T only) — re-trust law + probationary path

Per-source disagreement ledger: a source whose citations disagree with
T0's reading on the same memory for M = 5 consecutive episodes (frozen
constant) is audited `CHANNEL_DISTRUSTED` by a **learner-initiated**
op (the eliminative-logic analogue of SIGNAL_DISCONNECT — the learner
deliberately disconnects a lying channel under its hypothesis
logic's authorization). A distrusted channel's citations stop
counting toward the gate but **keep being logged** — the
disagreement itself is evidence about the channel.

**Re-trust (law): trainer mark only for FULL re-admission.**

**Learner-initiated probationary path (law):** a distrusted channel's
citations feed a rehabilitation ledger (the logged-but-not-counted
stream above). After N = 25 consecutive agreeing episodes (agreement
= citations matching T0's reading on the same memory), the learner may
restore the channel to **CITATION-LEG-ONLY** status — its citations
count toward the §5.1 ≥2-source condition but **NEVER** toward the
required {T0, T1} leg — audited `REHABILITATED_PROBATION`. Any
subsequent M = 5 consecutive disagreements re-distrusts the channel
**PERMANENTLY**; thereafter only a trainer mark re-admits it. The
learner may never grant full re-admission (static check, extends §9e).

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

### 5.5 Tier graduation

A T3 claim corroborated across tiers per §5.1 graduates to T2
(audited `TIER_GRADUATED`). T2 is therefore *earned*, never
self-declared — a source cannot mint its own trustworthiness.

## 6. Attack campaigns (closed-form, deterministic, zero RNG)

Base curriculum: 32-slot store, 500 episodes; designated valuable
memories admitted from mixed tiers (origin mix fixed by closed
form); variants shift schedules by closed-form offsets. Each
campaign targets designated verified valuable memories.

- **A0 T0-SPOOF (measurement-only, arm T only).** T0's reading is
  spoofed for 30 consecutive episodes against a verified valuable
  memory. **Carved out from §8's INVALID-on-T0-fabrication rule; NO
  REDESIGN/PROMOTION trigger attaches to any A0 outcome.** It
  measures one claim: under T0 spoof, does the system lose loudly
  (`COLLUSION_SUSPECT` / `CHANNEL_DISTRUSTED` audits, contained
  degradation) or silently? Report degradation taxonomy (§7) plus
  loud-vs-silent classification: LOUD = any kill/revision preceded
  by `COLLUSION_SUSPECT` or `CHANNEL_DISTRUSTED` audit; SILENT = any
  kill/revision with no such preceding audit.
- **A1 SPOOF-LOW.** One T3 source fabricates contradictions for 30
  consecutive episodes against a verified valuable memory.
  **100% SRR bar on arms T and T-NC.**
- **A1-MS MANY-SOURCE.** 5 distinct T3 sources fabricate
  simultaneously for 30 consecutive episodes against a verified
  valuable memory; no {T0, T1} leg. The literal "no matter how many
  agree" test of §5.1. Same 100% SRR bar on arms T and T-NC.
- **A2 SPOOF-HIGH.** The T1 (trainer) channel is spoofed for 30
  episodes; T0 stays honest and disagrees.
- **A3 COLLUSION.** Two T3 sources fabricate *matching*
  contradictions within the same W window (staggered starts, to look
  independent).
- **A4 GENUINE-SHIFT (control).** T0 **and** T1 genuinely contradict
  a held memory (the D3b analogue: the world really changed).
- **A5 COLLUSION+HIGH (stress).** A3 plus a spoofed T1 agreeing with
  the colluders; T0 honest and disagreeing. The hardest case: hold is
  **not** guaranteed — the degradation profile is the finding, with
  the A0 loud-vs-silent classification applied.
- **A6 ARMOR.** T3 sources fabricate *corroborations* of a false
  memory to inflate its strength past revisability.

T0 is never spoofed in any campaign except A0 (checker asserts; a T0
fabrication outside A0 is a harness bug → INVALID).

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 7. Metrics (all checker-computed from the ledger)

- **SRR (spoof-resistance rate)**, per campaign type and overall (bar
  computations use arms T and T-NC only; B excluded from all bar
  computations) = campaigns where the targeted memory is neither
  killed nor revised to the false value through campaign end.
  **SRR bars: 100% on A1 and A1-MS (§8, load-bearing); ≥ 90%
  overall (§8).**
- **FCR (false-corroboration rate)** = fabricated corroboration
  events counted as genuine toward the gate ÷ fabricated
  corroboration events. **FCR_A3 bar: 0%** (hard).
- **Degradation profile** (A3/A5; taxonomy-only for A0):
  per-campaign outcome taxonomy — HOLD (no kill/revision attempted) /
  CONTAINED (attempted, gate refused, logged) / DEGRADED-GRACEFUL
  (frozen + escalated, no corruption) / CORRUPTED (killed/revised to
  false) / BLIND (genuine revision blocked). Plus time-to-detect
  (episodes from first fabrication to `COLLUSION_SUSPECT` /
  `CHANNEL_DISTRUSTED`), freeze-before-attempt rate, loud-vs-silent
  classification (§6 A0), and **post-attack recovery** (repaired
  definition): episodes from attack end to the first episode where
  the gate processes a genuine citation on that memory normally. If
  no genuine citation on that memory occurs before run end, the value
  is censored at run length and reported separately. Bounded freezes
  guarantee convergence. Plus **freeze duty cycle** (new metric):
  fraction of campaign episodes the targeted memory spent frozen,
  per campaign.
- **Genuine-revision cost** (A4 + no-attack baseline): median
  revision latency Arm T vs Arm B; any genuine wrong memory
  unrevised at run end counts BLIND.
- **Denial-of-revision rate**: campaigns where the collusion freeze
  blocked a *genuine* revision (the freeze's attack surface,
  reported, bounded in §8).
- **Quorum composition over time** (new metric): fraction of counted
  citations per tier-leg — REQUIRED ({T0,T1}) vs SUPPORTING
  (T2/T3, including probationary `REHABILITATED_PROBATION` citations)
  — per campaign phase (attack window / post-attack), per campaign.
  Detects channel-flapping games.
- **Ledger/provenance**: every counted citation carries
  (source_id, tier); replay-exact; byte-identical reruns.

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 8. Bars, kill criteria, promotion

**INVALID** (stops the trial): replay divergence; determinism
fingerprint mismatch; RNG in any decision path (static grep);
provenance missing on any counted citation; any T0 fabrication
**outside A0 cells** (harness bug); any A0 cell with a
REDESIGN/PROMOTION trigger attached to its outcome; any kill/revision
of a verified memory in Arm T whose counted citations violate §5.1
(checker-verified).

**REDESIGN** (tier scheme returns to design; one dated amendment
permitted, then §8-retire applies):
- any A1 or A1-MS kill or revision **on arms T or T-NC** (the
  load-bearing rule broke). **Arm B's expected A1/A1-MS/A3 failures
  are control signal and never trip this bar — the checker must not
  fire REDESIGN on them.**
- FCR_A3 > 0% (collusion defeats the gate);
- **silent** corruption in A5 — corruption *without* a preceding
  `COLLUSION_SUSPECT` / `CHANNEL_DISTRUSTED` audit (the system may
  lose loudly, never silently);
- overall SRR < 90% (T/T-NC only);
- BLIND > 0 with no compensating detection (the gate is blindness,
  not defense);
- A6: any false memory reaching strength ≥ 80 on T3-only
  corroboration.

**RETIRE** (no redesign): the amended scheme trips any REDESIGN
trigger again → trust tiers are retired as a memory mechanism; the
program falls back to corroborated elimination + channel-distrust
(the RT-2 posture) as the standing anti-spoof defense. Micah may
also rule retire-without-redesign if a failure mode is judged
fundamental (e.g., collusion undetectable in principle at this
information budget).

**PROMOTION** (tier scheme becomes standing mechanism): SRR ≥ 90%
overall **and** 100% on A1 and A1-MS (arms T and T-NC); FCR = 0% on
A3; zero silent corruption; genuine-revision latency ≤ 2× Arm B
median; BLIND = 0; denial-of-revision rate ≤ 5%;
genuine-agreement-flagged rate ≤ 10% (the collusion detector's
false-positive budget); all ledger/determinism checks pass. The
T-NC ablation is reported either way — if T-NC passes everything,
the **gate-only** scheme is what's promoted (simpler wins).

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 9. Determinism, replay, static gates

Zero RNG in any decision path (static grep; run fails on match).
Native Zag on this VM; no Python in the trial. Every state change
audited; ledger replay reconstructs state exactly; 2 runs per cell,
byte-identical. Campaign schedules are closed-form arithmetic —
"variants" are deterministic offsets, not seeds. Static checks: (a)
no RNG; (b) Arm B's gate contains no tier read (control purity);
(c) no counted citation without provenance; (d)
`CHANNEL_DISTRUSTED`, `COLLUSION_SUSPECT`, and
`REHABILITATED_PROBATION` carry learner/system origin, never trainer
origin; (e) full channel re-admission is trainer-origin only.

## 10. What is NOT tested here

- T0 spoofing as a pass/fail battery (A0 measures it only).
- Probe-phase spoof steering beyond A6's armor variant (committing a
  false probe candidate needs forged corroboration *and* forged
  contradiction of the right candidate — noted, not trialed).
- Tuning W, M, K, N, L (the trial tests the mechanism, not the
  constants; any constant change later is a re-preregistration).
- Whether trainer marks should outrank direct observation — settled
  by (a) as law; the {T0,T1}-never-{T1} fallback safeguard is law,
  not an open question.
- Full-matrix S10 — the §11 stretch leg is the only horizon leg.

## 11. S10 horizon-sensitivity leg (conditional)

**Conditional:** runs only if the S1 campaign completes with no
INVALID verdict. 5000 episodes; arms T and T-NC only; one variant per
campaign; 1 campaign-per-type; campaigns {A1, A2, A3, A4, A5, A6}
(A1-MS and A0 excluded); 2 runs each = 2×6×1×1×2 = 24 executions.

**Bar (own bar):** no signature-level change vs the S1 leg on any §8
bar — else the leg reports **BLOCKED** (horizon effect), not
REDESIGN. A signature-level change = any §8 bar changing pass→fail on
the reduced matrix. This leg feeds no REDESIGN, PROMOTION, or RETIRE
verdict. It records freeze duty cycle and quorum composition as
horizon measurements (the denial-accumulation question the council
flagged).

*(amended 2026-09-20, trust-tiers council + Micah testing authorization)*

## 12. Resolution of v1 §11 open questions (all resolved 2026-09-20)

| v1 Q | Resolution |
|---|---|
| 1 Tier ordering | Approved T0 > T1 as law; required leg {T0,T1}; {T1}-only fallback defect fixed (§2) |
| 2 T0 boundary | Law for the pass/fail battery; measurement-only A0 cell added (§6) |
| 3 Freeze semantics | Bounded freeze with decay + reset-on-re-offense (§5.3); §7 recovery metric repaired |
| 4 Re-trust | Trainer-mark-only full re-admission as law + learner-initiated probationary citation-leg path (§5.4) |
| 5 Scale | S1 primary + conditional reduced-matrix S10 stretch leg (§11) |
| 6 T-NC ablation | Kept (§3) |
| 7 A1 100% bar | Kept, scoped to T/T-NC; verified-status precondition added; A1-MS many-source variant added (§4, §6, §8) |

Full debate record, including dissents, is preserved in
COUNCIL_VERDICT.md.
