# POSITION 3 — Structural change, not a patched race (trust-tiers redesign council debater)

**2026-09-20. Position paper; nothing implemented.**

## 1. Diagnosis

A5's mechanism proof (§1.1): a spoofed T1 *satisfies* the required {T0,T1} leg by law, so
the kill path (≤4 eps) is definitionally faster than every detection path (≥5).
**Change what revision requires so the race can't be won by spoofing.**

## 2. The structural change: disagreement veto + two-phase commit

**(a) Disagreement veto (law).** The {T0,T1} leg is satisfied only if both legs are
present-or-silent **and agree**. If T0 and T1 both cite the same memory in window W and
*disagree*, no revision/elimination proceeds — audited `TIER_CONTEST`, trainer-escalated,
memory frozen under §5.3 semantics. A T1-only leg (T0 silent) may proceed only via (b).

**(b) Propose→confirm for single-leg revisions (law).** A {T1}-only revision does not
execute. Phase 1 audits `REVISION_PROPOSED` and freezes the memory; phase 2 confirms after
D = W episodes only if no veto fired, T0 stayed silent-or-agreeing, no `COLLUSION_SUSPECT`
fired, and all counted leg sources are channel-clean; confirmation is learner-initiated,
audited `REVISION_CONFIRMED`. Native-Zag: per-slot ledger propose-state with a countdown;
static checks extended to it.

**Why it beats the race:** in A5 the spoofed-T1 + colluding-T3 combo either hits (a) —
honest T0 disagrees — or stalls in (b) for D = 25 eps, far beyond the M = 5 detection window.
The kill path becomes the slowest path *by construction*.

## 3. Predicted effects per campaign and §8 bar

- **A1/A1-MS/A3/A6:** unchanged. 100% / FCR 0% ✓
- **A2:** HOLD via veto (honest T0 disagrees with spoofed T1). ✓
- **A4:** agreement already met, no two-phase; GENUINE_REVISED at ≈ B's 3.0; ≤6.0 ✓, BLIND 0 ✓
- **A5:** veto freeze or phase-2 stall; distrust (needs M = 5) arrives before confirmation
  (needs D = 25 + clean channel-health). Zero silent corruption ✓, SRR ≥90% ✓
- **Genuine T1-only shift:** two-phase, latency ≤ ~29 eps — the honest cost. Denial ≤5% ✓
  ((b) stalls, never denies).
- **Sensor-blind memories:** no mechanism revision without trainer — §4(i); §5.2 stands.

## 4. Required amendment texts (the one permitted dated amendment)

**(i) BLIND-bar scoping** (A.2): *"§8 bullet 5 (BLIND > 0) applies only to memories observable by at least one of {T0,T1}.
Memories where both are structurally silent are exempt; their defense is logged
`TRAINER_ESCALATE`."*

**(ii) False-positive budget** (A.7): *"The ≤10% budget covers spontaneous flags on
{T0,T1}-observable memories only. Flags on probes designed to be indistinguishable from
collusion are reported separately."*

**(iii) Freeze-lapse fix** (A.3): *"Reset-on-re-offense means re-**fabrication** — a citation
disagreeing with the frozen memory — not any citation activity by a named source."*

**(iv) Chronological audit fields:** absolute episode numbers on
propose/confirm/distrust/kill audits (A.5).

## 5. Red-team answer

*"Structural requirements just give the attacker a new checklist; sensor-blind cases still
can't be defended."* — Two parts:

- **Checklist:** the new checklist *costs the attacker T0 agreement*. Before: "spoof T1 + one
  T3". Now: "forge T1 AND neutralize T0's disagreement" (T0 is the honest floor, §2/A0).
  That moves the threat from channel-spoofing to sensor-compromise —
  out of pass/fail scope. A checklist the attacker cannot complete is a defense.
- **Sensor-blind:** no trusted channel can observe the memory, so *no mechanism can revise
  it* — any scheme claiming otherwise smuggles trust somewhere. The honest outcome is
  `TRAINER_ESCALATE` + frozen memory + human override: humans as backup/override, applied
  where autonomy has no evidence.

## 6. Verdict recommendation

**Redesign with this structural change as the one permitted dated amendment.** Strictly
stronger — more attack surface closed, never softer — every §8 bar satisfiable.
If the amended scheme trips REDESIGN again on A5, RETIRE: the failure is then fundamental.
**Do not attempt:** shortening M, faster distrust, or a {T1}-only fallback.
