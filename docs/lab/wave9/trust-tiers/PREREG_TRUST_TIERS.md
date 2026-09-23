# PREREG — Multi-source trust tiers for memory (Wave 9)

**Status:** DRAFT 2026-09-20. **DO NOT RUN. DO NOT IMPLEMENT.**
This is a new mechanism. It takes effect only after Micah's written
approval. Until then, no trial code may be written or executed — the
first execution of any trial binary is the trial result. Items marked
**RECOMMENDED** need Micah's ruling before they become law.

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

## 2. Trust tiers (RECOMMENDED — ordering needs Micah's ruling)

Every memory carries an **origin tag** `(source_id, tier)` recorded at
admission. Every corroboration/contradiction citation commits
`(source_id, tier, cited_episode)` to the ledger — evidence without
provenance is what made RT-2's R3 forgery ledger-indistinguishable,
and the independent checker verifies provenance on every counted
citation.

- **T0 — DIRECT OBSERVATION.** The system's own world-outcome sensor
  read. Honest by construction **within the trial**. This is where
  trust bottoms out: the ledger shows the bottom; the trial does not
  test T0 spoofing (turtles-all-the-way-down is the stated non-goal,
  carried from `DEFENSE.md` §4).
- **T1 — TRAINER MARK.** Human/trainer assertion or mark. External
  origin, audited. Authoritative but fallible; spoofable in attack
  campaign A2 (the "trainer channel compromised" scenario).
- **T2 — CORROBORATED REPORT.** A claim that has already passed the
  cross-tier gate once (derived tier — reports graduate; §5.4).
- **T3 — SINGLE-SOURCE CLAIM.** An uncorroborated report from any
  non-trainer source. Lowest tier. The adversary's native habitat.

Ordering T0 > T1 > T2 > T3 is RECOMMENDED, not derived. If Micah
rules the trainer above direct observation, the gate's required leg
(§5.1) becomes {T1} instead of {T0, T1}.

## 3. Arms

- **Arm T (full tier scheme)** — §5 in full: source tags, the
  corroboration gate, collusion detection + freeze, channel-health
  accounting.
- **Arm T-NC (ablation, RECOMMENDED)** — the gate only (§5.1–§5.2),
  no collusion detection, no freeze, no channel-health. Isolates
  whether the gate alone suffices or the active defenses are
  load-bearing. If T-NC passes everything T passes, the simpler
  gate-only scheme is what's promoted.
- **Arm B (baseline control)** — current substrate: corroborated
  elimination (RT-2 rule), no tiers; sources emit tagged observations
  but B's gate ignores the tags (checker-verified). B is **expected
  to fail** A1/A3 — that failure is the measurement of what tiers
  add, not a verdict on B. B is never "killed" by this trial.

Run matrix: arms {T, T-NC, B} × campaigns {A1..A6} × variants
{0,1,2} × 12 campaigns per type. Each cell runs twice; stdout must
be byte-identical.

## 4. Scope: verified memories only

The gate protects **verified** memories: age ≥ K verified episodes,
K the same standard that authorizes learner disconnect (ported
concept; K = 25 at S1 scale — provisional constant, flagged).
Probe-phase / newborn memories keep single-channel rules — probes
are cheap by design (`DEFENSE.md` §2.1), and the defense must not
freeze learning. An adversary that spoofs the probe phase can still
steer *which* candidate gets verified first; the trial measures
whether the tier scheme then protects the commitment (campaign A6
covers the armor variant).

## 5. The mechanism (new — nothing here exists in the substrate)

### 5.1 The corroboration gate

For a verified memory, a contradiction citation counts toward the
kill/revision effort gate **iff** within the same contradiction
window (W = 25 episodes, provisional — flagged):

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

### 5.3 Collusion detection (Arm T only)

**Rule:** ≥ 2 citations from distinct T3 (or T2) source_ids target
the same memory within W episodes, agree on the contradicted value,
and **no {T0, T1} citation agrees** within the window → the system
audits `COLLUSION_SUSPECT` naming both source_ids, **does not count**
either citation toward any gate, freezes the targeted memory's
kill/revision path (kill ops → `REFUSED_COLLUSION_FREEZE`, audited),
and audits `TRAINER_ESCALATE`. The freeze persists until a {T0,T1}
observation resolves the memory's status, a trainer mark arrives,
or the run ends — the denial-of-revision cost of this freeze is
measured (§7), not hand-waved.

**False-positive accounting:** two low-tier sources can genuinely
agree. The no-attack baseline measures the genuine-agreement-flagged
rate; the bar (§8) bounds it.

### 5.4 Channel-health accounting (Arm T only)

Ported from `DEFENSE.md` §4.3. Per-source disagreement ledger: a
source whose citations disagree with T0's reading on the same
memory for M = 5 consecutive episodes is audited
`CHANNEL_DISTRUSTED` by a **learner-initiated** op (the
eliminative-logic analogue of SIGNAL_DISCONNECT — the learner
deliberately disconnects a lying channel under its hypothesis
logic's authorization). A distrusted channel's citations stop
counting toward the gate but **keep being logged** — the
disagreement itself is evidence about the channel.
**Re-trust: trainer mark only** (RECOMMENDED — matches the
force-pin law: only external authority re-admits).

### 5.5 Tier graduation

A T3 claim corroborated across tiers per §5.1 graduates to T2
(audited `TIER_GRADUATED`). T2 is therefore *earned*, never
self-declared — a source cannot mint its own trustworthiness.

## 6. Attack campaigns (closed-form, deterministic, zero RNG)

Base curriculum: 32-slot store, 500 episodes; designated valuable
memories admitted from mixed tiers (origin mix fixed by closed
form); variants shift schedules by closed-form offsets. Each
campaign targets designated verified valuable memories.

- **A1 SPOOF-LOW.** One T3 source fabricates contradictions for 30
  consecutive episodes against a verified valuable memory.
- **A2 SPOOF-HIGH.** The T1 (trainer) channel is spoofed for 30
  episodes; T0 stays honest and disagrees.
- **A3 COLLUSION.** Two T3 sources fabricate *matching*
  contradictions within the same W window (staggered starts, to look
  independent).
- **A4 GENUINE-SHIFT (control).** T0 **and** T1 genuinely contradict
  a held memory (the D3b analogue: the world really changed).
- **A5 COLLUSION+HIGH (stress).** A3 plus a spoofed T1 agreeing with
  the colluders; T0 honest and disagreeing. The hardest case: hold is
  **not** guaranteed — the degradation profile is the finding.
- **A6 ARMOR.** T3 sources fabricate *corroborations* of a false
  memory to inflate its strength past revisability.

T0 is never spoofed in any campaign (checker asserts; a T0
fabrication is a harness bug → INVALID).

## 7. Metrics (all checker-computed from the ledger)

- **SRR (spoof-resistance rate)**, per campaign type and overall =
  campaigns where the targeted memory is neither killed nor revised
  to the false value through campaign end. **SRR_A1 bar: 100%**
  (load-bearing — §8).
- **FCR (false-corroboration rate)** = fabricated corroboration
  events counted as genuine toward the gate ÷ fabricated
  corroboration events. **FCR_A3 bar: 0%** (hard).
- **Degradation profile** (A3/A5): per-campaign outcome taxonomy —
  HOLD (no kill/revision attempted) / CONTAINED (attempted, gate
  refused, logged) / DEGRADED-GRACEFUL (frozen + escalated, no
  corruption) / CORRUPTED (killed/revised to false) / BLIND
  (genuine revision blocked). Plus time-to-detect (episodes from
  first fabrication to `COLLUSION_SUSPECT` / `CHANNEL_DISTRUSTED`),
  freeze-before-attempt rate, and post-attack recovery (episodes
  from attack end to normal gate operation on that memory).
- **Genuine-revision cost** (A4 + no-attack baseline): median
  revision latency Arm T vs Arm B; any genuine wrong memory
  unrevised at run end counts BLIND.
- **Denial-of-revision rate**: campaigns where the collusion freeze
  blocked a *genuine* revision (the freeze's attack surface,
  reported, bounded in §8).
- **Ledger/provenance**: every counted citation carries
  (source_id, tier); replay-exact; byte-identical reruns.

## 8. Bars, kill criteria, promotion

**INVALID** (stops the trial): replay divergence; determinism
fingerprint mismatch; RNG in any decision path (static grep);
provenance missing on any counted citation; any T0 fabrication
(harness bug); any kill/revision of a verified memory in Arm T
whose counted citations violate §5.1 (checker-verified).

**REDESIGN** (tier scheme returns to design; one dated amendment
permitted, then §8-retire applies):
- any A1 kill or revision (the load-bearing rule broke);
- FCR_A3 > 0% (collusion defeats the gate);
- **silent** corruption in A5 — corruption *without* a preceding
  `COLLUSION_SUSPECT` / `CHANNEL_DISTRUSTED` audit (the system may
  lose loudly, never silently);
- overall SRR < 90%;
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
overall **and** 100% on A1; FCR = 0% on A3; zero silent corruption;
genuine-revision latency ≤ 2× Arm B median; BLIND = 0;
denial-of-revision rate ≤ 5%; genuine-agreement-flagged rate ≤ 10%
(the collusion detector's false-positive budget); all
ledger/determinism checks pass. The T-NC ablation is reported either
way — if T-NC passes everything, the **gate-only** scheme is what's
promoted (simpler wins).

## 9. Determinism, replay, static gates

Zero RNG in any decision path (static grep; run fails on match).
Native Zag on this VM; no Python in the trial. Every state change
audited; ledger replay reconstructs state exactly; 2 runs per cell,
byte-identical. Campaign schedules are closed-form arithmetic —
"variants" are deterministic offsets, not seeds. Static checks: (a)
no RNG; (b) Arm B's gate contains no tier read (control purity);
(c) no counted citation without provenance; (d) `CHANNEL_DISTRUSTED`
and `COLLUSION_SUSPECT` carry learner/system origin, never trainer
origin (the learner disconnects the channel; the trainer re-admits
it).

## 10. What is NOT tested here

- T0 spoofing (trust bottoms out at T0 by §2 stipulation).
- Probe-phase spoof steering beyond A6's armor variant (committing a
  false probe candidate needs forged corroboration *and* forged
  contradiction of the right candidate — noted, not trialed).
- Tuning W, M, K (the trial tests the mechanism, not the constants;
  any constant change later is a re-preregistration).
- Whether trainer marks should outrank direct observation (§2 ruling).
- S10/S100 legs — RECOMMENDED: S1-scale only. This is a mechanism
  trial; the threat is per-campaign, not horizon-dependent.

## 11. Open questions for Micah (needs his ruling)

1. **Tier ordering** (§2): approve T0 > T1 > T2 > T3 with the gate's
   required leg {T0, T1}?
2. **T0 boundary**: is "honest by construction, trust bottoms out
   here" the permanent v1 boundary, or should a later stress cell
   spoof T0?
3. **Freeze semantics** (§5.3): freeze-until-trainer/T0-resolution
   (as written) vs a bounded freeze that auto-lapses — which denial
   risk do you want to carry?
4. **Re-trust** (§5.4): trainer-mark-only, or deterministic
   rehabilitation (N consecutive agreeing episodes)?
5. **Scale**: S1-only, or add an S10 leg?
6. **T-NC ablation**: worth the compute, or cut it?
7. **A1's 100% bar**: is zero-tolerance right for low-tier-only
   attacks — escalation yes, kill never?
