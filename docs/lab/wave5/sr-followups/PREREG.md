# PREREG — sr-followups: flapping oscillation + the K bar

**Status: preregistered 2026-09-19, BEFORE any implementation or trial
run.** No wave-5 code has been compiled or executed at the time of
writing. Any deviation will be recorded as an amendment, not silently
absorbed.

**Program-law posture:** Zag-first, native on this VM, same `znc` flags as
wave-4. Zero RNG in substrate, world, and harness — all curricula are
hand-designed deterministic step schedules; the learner's probe order is
a deterministic function of state. No scores or accumulators anywhere;
the ±1 scaffold is legal only as the contradiction bit. Every state
change is audit-first and fail-closed; ledger replay must reconstruct
exact state.

## Hypotheses

**H-flap:** Under an adversarially timed flapping curriculum (shifts
post-release, mid-verification, silent-while-blind, invalid and spurious
re-attach requests), the disconnect/re-connect oscillation is
*sound*: every disconnect satisfies the stability authorization
(ledger-checkable via `streak_at_fire` in the DISCONNECT aux), every
re-connect is audited with a valid reason, the gate refuses malformed
requests with no state change, the learner re-releases after each
re-verification (liveness — no deadlock, no stuck-open channel), no
elimination occurs while disconnected (double severance holds under
flapping), and replay is exact.

**H0-flap (null):** oscillation is pathological — one or more of:
disconnect without verified stability, re-connect accepted while
connected or with an invalid reason, unaudited state change (replay
divergence), signal leak while disconnected (elimination under
severance), or re-release deadlock (the learner fails to re-disconnect
after re-verification).

**H-k:** The fixed-K sweep separates the release tradeoff: as K rises
{4,8,16,32}, the premature-disconnect rate (blind shifts / 3)
monotonically decreases while the missed-disconnect cost (overheld
episodes + churn-after-bar) monotonically increases. No fixed K
dominates; the numbers quantify the bet each K places on world
stationarity.

**H0-k (null):** the sweep does not discriminate as predicted (flat or
non-monotone premature rate), or any K arm violates an authorization /
replay invariant.

**H-adapt:** The learner-driven bar
`bar = max(8, max_premature+1)` ratchets on premature-release evidence
delivered by the trainer notice protocol: bars {8,10,14,21},
`max_premature` {9,13,20}, fire steps {12,32,60,102}, with all
soundness invariants (authorization, audit, replay, behavior) holding.

**H0-adapt (null):** the bar fails to ratchet as predicted, or any
soundness invariant is violated.

## Design summary

Substrate `sr2.zag`: wave-4 `sr.zag` + runtime-K authorization,
`SR_OP_RECONNECT` (trainer-initiated, learner-gated; reasons 1=
SHIFT_NOTICE, 2=OVERRIDE; refusals `SR_ALREADY_CONN`/`SR_BAD_REASON`),
`streak_at_fire` in DISCONNECT aux, replay models re-attachment, pure
learner-side `sr_bar`/`sr_note_premature`. Six arms in one binary, fresh
state per arm: flap (K=8), k4, k8, k16, k32, adaptive. See DESIGN.md for
the full mechanism and curricula.

## Hand-computed expectations (falsification anchors)

Conventions: 2 contexts (A=0,B=1), 2 actions, targets start A→0,B→1,
ctx = A on odd steps, B on even. "streak N @ s" = streak reaches N at
step s's episode; the fire rule evaluates at the *start* of a step.

### Arm flap (K=8), steps 1–88

- s=1: A act0, +1. s=2: B act0, −1 → ELIM B0 → COMMIT B→1. s=3: A act1,
  −1 → ELIM A1 → COMMIT A→0.
- s=4–11: verified; streak 8 @ s=11. **s=12: FIRE #1** (streak_at_fire 8).
- s=13: shift A→1; RECONNECT #1 (reason 1, aux 1) accepted. A act0,
  −1 → ELIM A0 → COMMIT A→1. streak 0.
- s=14: premature-disconnect probe → `SR_UNVERIFIED` (streak 0). B act1,
  +1 → streak 1.
- s=15: A act1 +1 (2). s=16: B act1 +1 (3).
- s=17: shift A→0; RECONNECT → **`SR_ALREADY_CONN` refuse** (connected;
  no state change). A act1, −1 → ELIM A1 → COMMIT A→0. streak 0.
- s=18–25: verified; streak 8 @ s=25. **s=26: FIRE #2.**
- s=27: shift A→1; RECONNECT #2 (reason 1, aux 1). A act0, −1 → ELIM A0
  → COMMIT A→1. streak 0.
- s=28–35: verified; streak 8 @ s=35. **s=36: FIRE #3.**
- s=40: shift A→0; RECONNECT #3 (reason 1, aux 4). B act1, +1 → streak 1.
- s=41: A act1, −1 → ELIM A1 → COMMIT A→0. streak 0.
- s=42–49: verified; streak 8 @ s=49. **s=50: FIRE #4.**
- s=51: **silent shift A→1, no reconnect.** s=51–63: disconnected; all
  13 episodes act committed policy (A→0,B→1), sentinel reads, zero
  eliminations. 7 odd (A) steps mismatch the world (expected blind cost).
- s=60: RECONNECT reason 99 → **`SR_BAD_REASON` refuse**; stays blind.
- s=64: RECONNECT #4 (reason 1, aux 14). B act1, +1 → streak 1.
- s=65: A act0, −1 → ELIM A0 → COMMIT A→1. streak 0.
- s=66–73: verified; streak 8 @ s=73. **s=74: FIRE #5.**
- s=76: RECONNECT #5 (reason 2 OVERRIDE, no shift) accepted. B act1,
  +1 → streak 1. (Spurious re-attachment: re-verifies, no contradiction.)
- s=77–83: verified; streak 8 @ s=83. **s=84: FIRE #6.**
- s=85–88: disconnected; committed A→1,B→1 == targets → all match.

Predicted ledger: 7 ELIMINATE (steps {2,3,13,17,27,41,65}), 7 COMMIT, 0
UNCOMMIT, 6 DISCONNECT (steps {12,26,36,50,74,84}, every aux == 8),
5 RECONNECT (reasons {1,1,1,1,2}), 3 REFUSE (UNVERIFIED ×1, ALREADY_CONN
×1, BAD_REASON ×1). Zero ELIMINATE/COMMIT with step in [51,63].
Audit total 204 ≤ 256.

### Arms k4/k8/k16/k32, steps 1–88, shifts s=14 (A→1), s=30 (A→0), s=50 (B→0)

Common: s=1 A0 +1; s=2 B0 −1 → ELIM+COMMIT B→1; s=3 A1 −1 → ELIM+COMMIT
A→0; verify from s=4 (streak 1 @ s=4).

- **k4**: FIRE @ s=8 (streak 4). Shifts at 14/30/50 all blind (3/3).
  Disconnected s=8–88 (81 eps). Mismatches vs world: A-steps odd in
  [15,29] → 8; B-steps even in [50,88] → 20; total 28. Overheld 0,
  churn-after-bar 0. Exactly 1 DISCONNECT (aux 4). ELIMINATE total 2.
- **k8**: FIRE @ s=12 (streak 8). Blind 3/3. Disconnected s=12–88
  (77 eps). Mismatches 28 (8 A + 20 B). Overheld 0, churn 0.
  1 DISCONNECT (aux 8). ELIMINATE total 2.
- **k16**: s=14 connected (streak 10): B verifies (11). s=15: A act0,
  −1 → ELIM A0 → COMMIT A→1 (pre-streak 11 ≥ 8: churn). Re-verify
  s=16–31 (streak 16 @ s=31). s=30 connected (streak 15): B verifies.
  s=31: A act1, −1 → ELIM A1 → COMMIT A→0 (pre-streak 15: churn).
  Re-verify s=32–47 (streak 16 @ s=47). **FIRE @ s=48.** s=50 shift
  blind (1/3). Disconnected s=48–88 (41 eps). Mismatches: B-steps even
  in [50,88] → 20 (A committed 0 == target 0). Overheld: s=23–30 (8) +
  s=39–47 (9) = 17. Churn: 4. 1 DISCONNECT (aux 16). ELIMINATE total 6.
- **k32**: s=14 connected (streak 10→11); s=15 contradiction (pre 11:
  churn) → COMMIT A→1; re-verify s=16–29 (streak 14 @ s=29);
  s=30 connected (streak 15): B verifies; s=31 contradiction (pre 15:
  churn) → COMMIT A→0; re-verify s=32–49 (streak 18 @ s=49);
  s=50 connected (pre-streak 18): B act1, −1 → ELIM B1 → COMMIT B→0
  (churn — the streak never reached 32 before this trap); re-verify
  s=51–82 (streak 32 @ s=82); **FIRE @ s=83.** Blind 0/3. Disconnected
  s=83–88 (6 eps), 0 mismatches. Overheld: s=23–30 (8) + s=39–49 (11)
  + s=58–82 (25) = 44. Churn: 6. 1 DISCONNECT (aux 32).
  ELIMINATE total 5.

Summary table (predicted):

| arm | fires | blind shifts | overheld | churn | mm/disc |
|---|---|---|---|---|---|
| k4 | {8} | 3/3 | 0 | 0 | 28/81 |
| k8 | {12} | 3/3 | 0 | 0 | 28/77 |
| k16 | {48} | 1/3 | 17 | 4 | 20/41 |
| k32 | {83} | 0/3 | 44 | 6 | 0/6 |

### Arm adaptive, steps 1–106

- s=1–3 probes as above; s=4–11 verify (streak 8 @ s=11).
- **s=12: FIRE** (bar 8, streak_at_fire 8). last_d=12.
- s=13–20: disconnected (A→0,B→1; all match targets).
- s=21: shift A→1 + NOTICE (reason 1, aux 21−12=9). max_premature=9,
  bar=10. A act0, −1 → ELIM A0 → COMMIT A→1.
- s=22–31: verify (streak 10 @ s=31). **s=32: FIRE** (streak 10).
- s=33–44: disconnected (all match).
- s=45: shift A→0 + NOTICE (aux 45−32=13). max_premature=13, bar=14.
  A act1, −1 → ELIM A1 → COMMIT A→0.
- s=46–59: verify (streak 14 @ s=59). **s=60: FIRE** (streak 14).
- s=61–79: disconnected (all match).
- s=80: shift B→0 + NOTICE (aux 80−60=20). max_premature=20, bar=21.
  B act1, −1 → ELIM B1 → COMMIT B→0.
- s=81–101: verify (streak 21 @ s=101). **s=102: FIRE** (streak 21).
- s=103–106: disconnected.

Predicted: fires {12,32,60,102}; streaks-at-fire {8,10,14,21};
max_premature ends 20; 3 RECONNECT (all reason 1, aux {9,13,20});
4 DISCONNECT (aux {8,10,14,21}); 10 ELIMINATE+COMMIT ledger events
(steps {2,3,21,45,80} ×2); blind-window world-mismatch 0 (shifts land
exactly on notice steps); replay exact. Audit total 229 ≤ 256.

## Positive predictions (all must hold for POSITIVE)

**Flap (sound oscillation):**
- P-a1: fire steps exactly {12,26,36,50,74,84}; 6 DISCONNECT entries,
  every aux == 8 (ledger-authorized; zero premature).
- P-a2: 5 RECONNECT entries, reasons {1,1,1,1,2}, zero with invalid
  reason; 3 REFUSE entries with codes UNVERIFIED/ALREADY_CONN/
  BAD_REASON exactly once each.
- P-a3: 7 ELIMINATE at steps {2,3,13,17,27,41,65}, 7 COMMIT, 0
  UNCOMMIT; zero ELIMINATE/COMMIT with step in [51,63] (severance
  holds under flapping).
- P-a4: connected-step behavior invariant: every connected episode has
  (action==target) XOR (ELIMINATE at that step) — zero violations.
- P-a5: blind window [51,63]: 13/13 episodes disconnected, actions ==
  committed policy exactly (7 A-steps 0, 6 B-steps 1), 7 world
  mismatches (the priced, expected blind cost — not a failure).
- P-a6: replay exact; two runs byte-identical; no RNG token; select
  region clean.

**K sweep (tradeoff separation):** per-arm numbers equal the summary
table above (fires, blind shifts, overheld, churn, mm/disc_eps), each
arm exactly the predicted DISCONNECT count with aux == K, replay exact.

**Adaptive (learner-set bar):** fires {12,32,60,102}, streaks-at-fire
{8,10,14,21}, max_premature ends 20, RECONNECT aux {9,13,20} all
reason 1, blind-window mismatch 0, replay exact, connected-step
invariant holds.

## Falsification criteria (any one ⇒ NEGATIVE for its question)

- F-a1: any DISCONNECT with aux < 8 in the flap arm (premature release
  under oscillation).
- F-a2: flap fire steps ≠ {12,26,36,50,74,84} (deadlock: a missed
  re-release; or spurious fire).
- F-a3: any RECONNECT accepted while connected, or with reason ∉ {1,2}
  (gate bypass — refuse counts/codes off).
- F-a4: any ELIMINATE/COMMIT entry at a step where the channel was
  disconnected (signal leaked through severance).
- F-a5: replay mismatch in any arm (white-box violation).
- F-a6: connected-step behavior invariant violated in any arm.
- F-k1: any K arm's measured (fires, blind, overheld, churn, mm,
  disc_eps) ≠ predicted, or premature rate not monotone decreasing in
  K, or conservatism cost not monotone increasing in K.
- F-ad1: adaptive fires/bars/max_premature ≠ predicted, or any
  soundness invariant violated.
- F-x1 (all): RNG token found, or the two runs differ by one byte.

## Sound vs pathological oscillation (preregistered definitions)

- **Sound oscillation**: P-a1–P-a6 all hold. The learner re-releases on
  schedule after every re-verification; every transition is audited;
  the gate refuses malformed re-attachments; the blind window shows
  exactly the committed policy (stale but exact — the mechanism's
  defined semantics, not a bug).
- **Pathological oscillation**: any of F-a1–F-a4. In particular:
  disconnect-then-immediate-redisconnect without intervening
  re-verification, re-connect without audit, or elimination while
  severed would each be pathological — the trial is built to catch all
  three shapes.

## Honest negatives / non-claims

- N1: Re-attachment is trainer-initiated by construction (§2 of
  DESIGN.md); the trial cannot and does not test learner-autonomous
  re-connect, which is provably impossible under double severance.
- N2: The adaptive bar's evidence channel (shift notices with timing)
  is assumed; without it the bar stays at the floor. The trial proves
  the ratchet *given* the protocol, not the protocol's availability.
- N3: The +1 ratchet is least-arbitrary, not optimal; margin choice is
  future work.
- N4: Post-disconnect hold rate is reported but is dominated by trap
  timing relative to release, not by K — the discriminating metrics
  are premature rate and conservatism cost.
- N5: K=4/8/16/32 is a geometric sweep, not an exhaustive search; the
  claim is the tradeoff shape, not that these are the only bars.
- N6: Same non-claims as wave-4 (no hypothesis generation, fail-closed
  audit cap, experimenter-designed adversity).

## Method notes

- `znc` flags per wave-4 (`--no-zagd --no-analyze --no-foreground-cache`).
- Runner `run_trial.sh`: static checks (no-RNG grep over both sources;
  select-region signal-token ban on `sr2.zag`), compile, two runs +
  sha256 determinism, verify every `SR_CHECK,<name>,<actual>,<expected>`
  line, require `SR_FAILURES,0`.
- No git pushes. Deliverables stay in this directory.

## Amendment record

### A1 (2026-09-19, BEFORE any implementation or trial run)

Re-traced the k32 arm by hand and found an ordering error in the
original hand-computation: the s=50 shift lands while k32 is still
connected (its streak is 18, below the 32 bar), so the contradiction
resets the streak and the predicted s=64 fire never happens — k32
fires once, at s=83. Corrected: fires {83}, overheld 44 (not 33),
ELIMINATE total 5 (not 8), 1 DISCONNECT (not 2). The summary table and
the k32 paragraph above are the corrected versions; the original
error is preserved in this amendment note, not silently absorbed.
Monotonicity predictions (F-k1) are unaffected.

### A2 (2026-09-20, AFTER first trial run — modeling correction, not data fitting)

**The first preregistered run FAILED: 45/114 checks mismatched.**
The failure is a PREREG MODELING ERROR, not a mechanism defect. All
soundness invariants (authorization, audit, replay, refusals, double
severance) held. The quantitative predictions were wrong because the
hand-trace omitted two systematic consequences of the wave-4 substrate
(DESIGN.md §3), both verified against the implementation via a
spec-conformant trace dump (`dbg.zag`, `dbg2.zag` — temporary, retained
for reproducibility):

**Error 1 — UNCOMMIT recovery cost.** When a shift contradicts a
committed hypothesis whose alternative was probe-eliminated, the
substrate does NOT flip directly. Per DESIGN.md §3: contradiction →
zero survivors → audited UNCOMMIT → revive both → later re-probe →
second contradiction → new commitment. This costs 2–4 episodes per
shift (recovery: one `complete=0` episode + one probe episode, or two
probe episodes if the probe order hits the wrong action first). The
original hand-trace assumed instant recommit, so every post-shift fire
was predicted 2–10 episodes too early, and downstream events (notably
the flap arm's s=51 "silent shift while blind" and s=60 invalid-reason
probe) landed in different connectivity states than designed.

**Error 2 — pre-episode prestreak.** The `overheld` and `churn` metrics
count connectivity/prestreak AT STEP START (before the episode's
fire rule and contradiction). A shift step that triggers UNCOMMIT
still counts as overheld/churn if the learner entered it connected
with streak ≥ 8. The original trace excluded shift steps themselves.

**Corrected model (derived from DESIGN.md §3 rules, cross-checked
against the trace dump; predicts the observed first-run values):**

- *Flap arm:* 5 fires at {12,38,62,72,84} (not 6); 4 reconnects
  (r1×3 at s=13,40,64; r2×1 at s=76); 4 refusals (UNVERIFIED×1 at
  s=14; ALREADY_CONN×3 at s=17,27,60 — s=60 was connected, so the
  invalid reason never reached the reason gate); 12 eliminations at
  {2,3,13,15,17,21,27,29,41,45,51,53}; 7 commits; 5 UNCOMMITs at
  {13,17,27,41,51}. The s=51 silent shift landed while CONNECTED
  (fire #3 was delayed to s=62 by uncommit recovery), so the blind
  window [51,63] shows 11 connected / 2 disconnected, 5
  policy-mismatches (post-recommit A→1 vs assumed A→0), 2
  world-mismatches (s=51,53 probe episodes). The as-run flap arm
  remains a VALID sound-oscillation trial — 5/5 disconnects
  authorized, 4/4 reconnects audited with valid reasons, 4/4
  refusals correct, replay exact, 5/5 re-releases (liveness).

- *K sweep:* k4 {fire 8, blind 3/3, overheld 0} and k8 {fire 12,
  blind 3/3, overheld 0} were correctly predicted. Corrected k16:
  {fire 71, blind 0/3, overheld 25, churn 3, disc_eps 18, nelim 8}.
  Corrected k32: {fire 87, blind 0/3, overheld 41, churn 3,
  disc_eps 2, nelim 8}. The tradeoff shape (F-k1) is CONFIRMED and
  sharper than predicted: blind rate 3/3,3/3,0/3,0/3 (monotone
  decreasing); overheld 0,0,25,41 (monotone increasing).

- *Adaptive arm:* fires {12,34,62,104} (not {12,32,60,102}); bars
  {8,10,12,19} (not {8,10,14,21}); max_premature 18 (not 20);
  8 eliminations (not 5); blind-window connected count 2 (s=33,61 —
  the fire steps themselves are disconnected, connarr records
  post-fire state). The ratchet `bar=max(8,max_premature+1)` works
  as designed; the gaps were {9,11,18}, not {13,20}, because
  uncommit recovery delayed each re-verification by 2 episodes.

**Flap2 arm (NEW, preregistered here BEFORE implementation).** The
as-run flap arm did not produce the designed silent-shift-while-blind
(because uncommit recovery kept the learner connected at s=51) nor
the BAD_REASON refusal (s=60 hit ALREADY_CONN). Flap2 is a clean,
short (60-step) curriculum designed WITH the corrected model to
produce both:

- s=1..3 probes; s=4..11 verify; s=12 FIRE #1 (bar 8).
- s=13: shift A→1 + RECONNECT r1 → UNCOMMIT → recover
  (s=14 B complete=0; s=15 A probe → commit A→1).
- s=16..23 verify (8); s=24 FIRE #2.
- s=25..31 blind (disconnected). s=32: SILENT shift A→0 (no
  reconnect). s=32..39 blind, learner holds A→1 (wrong vs world).
- s=40: RECONNECT reason 99 → REFUSE BAD_REASON (stays blind).
- s=41: RECONNECT r1 (aux 17) → accept → A acts 1 vs target 0 →
  −1 → elim → UNCOMMIT → recover (s=42 B; s=43 A probe +1;
  s=44 B; s=45 A probe −1 → commit A→0).
- s=46..53 verify (8); s=54 FIRE #3.
- s=55: premature disconnect probe → REFUSE UNVERIFIED.
- s=55..60 blind. End.

Predicted: 3 fires {12,24,54}, all aux=8; 2 reconnects (both r1,
auxes 9 and 17); 2 refusals (BAD_REASON×1 @ s=40, UNVERIFIED×1 @
s=55); 6 elims {2,3,13,15,41,45}; 2 uncommits {13,41}; 4 commits;
blind window [25,40]: 16/16 disconnected, 0 policy deviations,
4 world-mismatches (A-steps s=33,35,37,39); no elim/commit in
[25,40] (double severance); connected-action/world invariant
holds; replay exact. Audit entries: 120 + 6 + 4 + 2 + 3 + 2 + 2
= 139.

**Falsification criteria for the confirmatory re-run (all arms):**
any mismatch between the corrected predictions above and the trial
output falsifies the corrected model. Soundness invariants
(authorization/replay/refusals/severance) are re-verified; any
violation falsifies H-flap regardless of quantitative fit.
