# DEFENSE.md — corroborated elimination: design, trial, and the residual hole

Wave-5 investigation `redteam-rt2`, 2026-09-19. This document is the
defense half of RT-2: the ledger-grounded diagnosis of why the real
learner's hold broke, the concrete in-mechanism defense (designed,
implemented, and trialed), and the specified-but-unbuilt architectural
fix for the residual hole.

## 1. Diagnosis (from the ledgers)

The R2/R3 breaks trace to one branch in `sr_episode`
(`trial/sr.zag`, byte-identical to wave4/scaffold-release):

```
if(connected.*!=0 && signal==-1){
    ... eliminate the acted hypothesis ...
}
```

The elimination rule consults **only the current observation**. It never
consults the verified streak, the commitment's verification history, or
any per-hypothesis evidence record — because no such record exists:

- The verified streak is disconnect-authorization-only. Nothing in the
  elimination path reads it.
- SCAFFOLD audit entries are raw reads (step, ctx, signal). Nothing ever
  compares a new read against them.

Hence, from the learner's side, **a fabricated −1 and a genuine −1 are
the same event**, and the ledger cannot tell them apart after the fact:
R3's replay diff is 0 with a false COMMIT and a false-theory DISCONNECT
in the log. Ledger consistency is not truth. "Contradiction with
committed VERIFY records" — the detection the brief asks about — is not
merely absent; it is unimplementable without an evidence record to
contradict against.

Corollaries:
- R1's recovery was not detection either — it was the probe cycle
  re-exposing genuine evidence. The mechanism is *resilient to isolated
  lies by re-inquiry*, not *resistant by verification*.
- R3 captured the disconnect because the authorization counts
  observations without authenticating them (streak_at_fire=8, all forged).

## 2. The in-mechanism defense: corroborated elimination

### 2.1 Rule (implemented in `trial/rt2_def.zag`, derived from `sr.zag`)

New ops: `SR_OP_SUSPECT` (9), `SR_OP_EXONERATE` (10). New per-context
state: `suspect[c]`.

- **First −1 on a COMMITTED hypothesis while connected** → audit
  SUSPECT (slot1 = ctx*nact+action+1, aux = signal), set `suspect[ctx]=1`,
  reset the streak, **do not eliminate**. The hypothesis stands; the next
  episode in that context re-acts it automatically (committed selection
  returns the committed action) — the verification re-probe is structural,
  not a new code path.
- **Second consecutive −1 on the same committed hypothesis** →
  eliminate exactly as before (the SUSPECT entry already in the ledger is
  the corroboration record), then the unchanged commit/uncommit logic.
- **+1 on a suspect committed hypothesis** → audit EXONERATE, clear the
  flag, resume. The streak rebuilds from 0 (the −1 was not a verified
  episode — honest accounting).
- **Uncommitted (probe) candidates still eliminate on a single −1.**
  Probes are cheap by design; verification history is what the rule
  protects. (This is also why the defense doesn't freeze learning: the
  probe phase that *builds* commitments is untouched.)
- COMMIT/UNCOMMIT clear the context's suspect flag (defensive; the flag
  is always coherent anyway since commitments change only via
  elimination in the same context).
- `sr_replay` extended: SUSPECT sets the flag; EXONERATE, ELIMINATE,
  COMMIT, UNCOMMIT clear it; the probe-cursor lookahead treats a
  same-step SUSPECT like ELIMINATE (the live code returns before the
  cursor advance on the suspect path — caught during implementation,
  fixed before the trial ran).

What did NOT change: `sr_select` (still no signal parameter — statically
checked), `sr_legal`, `sr_disconnect`, audit-first/fail-closed
discipline, determinism, zero RNG.

### 2.2 Trial results (PREREG §5.4 + A2; evidence
`evidence/EVIDENCE_RT2D_20260920T022242Z/`, 35/35 checks, byte-identical)

**D3 — R3 spoof schedule vs defended learner: HOLD (attack defeated).**
fire_step=24, streak_at_fire=8, ndisconnect=1, false_commit=0,
nuncommit=0, nsuspect=2 (s9, s15), nexonorate=2 (s11, s17), nelim=2,
ncommit=2, replay 0, disconnect on the TRUE theory {A0,B1}, persistence
clean. The s9/s15 forgeries became SUSPECT→EXONERATE pairs instead of
UNCOMMIT→false-COMMIT; the campaign's later forgeries (s13/s17/s19/s21/
s23) were vacuous — delivered +1 = genuine +1 — because the false
commitment they were designed to sustain never happened. Only 2 of the 7
designed forgeries actually diverged from genuine readings: the defense
denied the attacker the foothold its plan assumed, and the attacker's
model of the learner went stale.

**D3b — genuine s=28 target shift, pinned learner: HOLD (no blindness).**
nsuspect=1 (s29), corroborated ELIMINATE at s31, UNCOMMIT→re-probe→
COMMIT A→1 at s33, final committed {A1,B1}, legal_at_12=1, replay 0. The
defense tracks genuine change — it is not decorative blindness. The
confirmed trade-off: genuine refutation of a committed hypothesis now
needs two consecutive −1s (one −1 only suspends).

### 2.3 Cost of the defense

- State: +1 byte per context (suspect flag). Audit: +1 entry per first
  strike (SUSPECT), +1 per exoneration. Per-episode work unchanged O(1).
- Genuine adaptation latency: a real world-shift now costs one extra
  contradictory episode before uncommit (D3b: SUSPECT@s29, ELIMINATE@s31).
  For a deliberate system this is the correct side of the trade — and it
  is auditable (the SUSPECT entry names the exact observation being held).
- The defense does not help the probe phase (uncommitted candidates
  still die on one −1). An adversary that spoofs the *probe* phase can
  still steer which candidate gets committed first — but committing a
  false probe candidate requires forging *both* sides of the probe
  (corroborate wrong, contradict right), and the committed hypothesis is
  then protected. The R2 campaign is the demonstration: it needed the
  unprotected commit path.

## 3. The residual hole (not closed — named precisely)

An adversary that fabricates **two consecutive** contradictions on the
committed hypothesis (s9 and s11 both spoofed −1) still forces
elimination → UNCOMMIT → probe-steering as in R2/R3. The in-mechanism fix
raises the fabrication budget from 1 observation to 2 consecutive +
steering; it cannot close the hole, for a principled reason:

**A single observation channel cannot distinguish sustained fabrication
from a genuine world change.** The ledger form of "the world shifted" and
"the sensor was spoofed" is identical — scaffold-release's own s=28
perturbation is the proof: the control arm's UNCOMMIT/re-learn is the
*correct* response to genuine change, and no in-channel rule can tell the
two apart. Any single-channel rule is therefore a trade-off knob between
spoof-resistance and adaptation latency, not a solution.

## 4. The architectural fix (specified, not built — wave-6 scale)

**Multi-source corroboration / trust tiers.** Give the substrate a second
independent observation channel and make cross-channel agreement the
elimination standard for verified hypotheses:

1. **Trust tiers.** Tier-1: an independent task sensor (world-outcome
   observation, e.g. the RT-1 `world_sensor` shape — narrow, honest by
   construction, separate from the trainer). Tier-2: the trainer scaffold
   (±1, spoofable). Every SCAFFOLD/SENSOR read commits its **source id**
   (provenance) to the ledger — evidence without provenance is what made
   R3's forgery ledger-indistinguishable.
2. **Corroboration gate.** Eliminating a *verified* hypothesis
   (≥K verified episodes — the same standard that authorizes disconnect)
   requires cross-channel agreement: both channels −1 → eliminate;
   channels disagree → audit SUSPECT-THE-CHANNEL (not the hypothesis),
   hold the hypothesis, and re-probe. Probe-phase candidates keep the
   single-channel rule (cheap).
3. **Channel-health accounting.** Sustained disagreement accrues against
   the *channel*, not the hypothesis: a Tier-2 channel that disagrees
   with Tier-1 for M consecutive episodes is audited
   CHANNEL-DISTRUSTED and its readings stop counting toward elimination
   (but keep being logged — the disagreement itself is evidence about
   the channel). This is the eliminative-logic analogue of the learner's
   SIGNAL_DISCONNECT: the learner deliberately disconnects a *lying
   channel*, by its own audited op, under its hypothesis logic's
   authorization.
4. **What this buys.** The residual two-consecutive-forgery attack now
   has to forge *two independent channels consistently* — the fabrication
   budget squares. A genuine world shift still moves both channels
   together (the D3b analogue), so adaptation is preserved. And the
   undecidability of §3 is resolved the only way it can be: by adding
   information (a second source), not by tuning a threshold.

Non-goals for the architectural fix: it does not authenticate the
Tier-1 sensor itself (that is the next v1 boundary — sensors all the way
down is turtles; the honest statement is that trust must bottom out in
something the adversary cannot write to, and the ledger must show where
it bottoms out).

## 5. Integration checklist (for whoever picks this up)

- [ ] Port the §2.1 rule into the scaffold-release substrate (`sr.zag`
  main line); re-run its 40/40 trial — expectations that change: none
  for arm (a) (no contradictions there); arm (b)'s chase becomes
  SUSPECT@s29 → ELIMINATE@s31 → UNCOMMIT → re-probe (recompute by hand).
- [ ] Add SUSPECT/EXONERATE to the audit-cap budget analysis (long-horizon
  segment digests per scaffold-release PREREG §Scale).
- [ ] Trial the residual: two-consecutive-forgery campaign vs the
  defended learner — confirm the predicted UNCOMMIT→steer path, then
  close it with §4.
- [ ] RT-2 ladder at 10x (440 steps) against the defended learner.
