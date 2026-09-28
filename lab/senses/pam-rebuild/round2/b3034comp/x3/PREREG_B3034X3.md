# PREREG_B3034X3 — FROZEN PREREGISTRATION
## Second rebuild of the 30+34 composition driver + B-OBJ4 battery

**Status:** FROZEN (committed alone before code).
**Branch:** `tnn-native-lab` (repo `sylorlabs/TNN`).
**Date:** 2026-09-24.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
**Rules:** pure Zag, zero randomness, byte-identical reruns (3 runs, SHA-256 compared).
**Predecessors (frozen, extract by script):**
- RT-OBJ4 verdict: `docs/lab/senses/pam-rebuild/round2/b3034obj4/VERDICT_RT_OBJ4.md`
  (prereg `f13383e8`, amendment `3cd045b6`, build `c9400529`, evidence `f69dac23`)
- GROK-OBJ4 record: `docs/lab/senses/pam-rebuild/round2/b3034comp/GROK_OBJECTOR_R4.md`
  (commit `8d151f77`)
- B-3034X2 build (killed driver): `fec41193`

---

## §0. Claim

A single frozen driver implementing the 30+34 composition (H-PAM-30's full-pin
verdict gate as admission surface + H-PAM-34's interleave/delay-line protocol
as continuity binding) admits percepts iff they survive the full protocol, and
refuses every attack class in the B-OBJ4 battery. The driver OWNS the mechanism:
queue, K counting, clocks, gap authentication, digest, trajectory, and the sink
call are driver-side. Fixtures present percepts and epochs ONLY — they do not
pass `maxv`, `forge`, temporal verdicts, or any policy knob.

---

## §1. Construction fixes (each confirmed RT-OBJ4 kill shape closed BY CONSTRUCTION)

The driver MUST satisfy all of the following. Each is a construction property,
verifiable by source inspection against the committed build, not by fixture
convention:

- **C-E0 (zero-evidence promote):** K is DRIVER-OWNED and driver-counted. There
  is no caller-supplied epoch count parameter (no `n_epochs` or equivalent).
  A decision with zero driver-counted non-gap epochs REFUSES (rc must be a
  dedicated code, not a silent promote). `x2_decide(st,id,0)`-shaped calls —
  zero evidence — MUST refuse.
- **C-TEMP (presenter-claimed time):** the temporal rule reads DRIVER stamps
  only: `t_q < t_stored < t_dec` on a driver-owned monotonic cross-call clock.
  Presenter-supplied `t_verdict` (or equivalent) is IGNORED by the temporal
  rule (may be logged, must not decide).
- **C-GAP (unauthenticated exemption):** gap marks are DRIVER-AUTHENTICATED
  (sentinel-bound by the driver, not presenter-asserted). A gap mark NEVER
  suppresses a queued world failure: the contradiction/world check runs on all
  queued records regardless of gap marks. All-gap input (G0: sentinel gaps,
  zero records) REFUSES. Gap-cloaked contradiction (G1) REFUSES.
- **C-SHORT (E1/E2):** zero non-gap records never promote; every counted epoch
  is non-gap; short windows (1–2 epochs) REFUSE.
- **C-CLONE:** the per-epoch digest binds `(id, epoch, label, conf, meas,
  extra)`. One percept's bytes presented twice count as ONE epoch (dup
  detection on the bound digest).
- **C-SEED:** a single trajectory is enforced — one seed per decision; world
  functions are evaluated against the decision's seed, not per-record seeds.
- **C-NOP (label-only check):** the 30-half check covers `label`, `conf`, and
  `meas` against the frozen tolerances (TOL_C=10, sink conf≥95 carried as the
  preregistered scope note from B-3034COMP §6).
- **C-POISON (cross-id ledger stamp):** ledger entries bind to the deciding
  evidence (id + epoch digests); a ledger line for id A is never accepted as
  evidence for id B.
- **C-RC7:** the rc=7 payload-split path is code-present AND battery-exercised
  (a class presents split extras); gap-drop cannot bypass it.
- **C-SINK (X5):** `act_sink` (or the named sink) is ACTUALLY CALLED on the
  promotion path — a call site in the driver, not a pack bit. The fired
  condition is the call, and the sink fires on true extra-consistent goals and
  does not fire on false G.
- **C-R0 (reset):** FROZEN CHOICE — `x2_reset` (or equivalent) is
  OPERATOR-ONLY: it is not callable by the presenter in the decision API. (If
  the build exposes it, the R0 class is scored, not carried.)
- **C-Q0 (liveness):** SCOPE-CARRY (liveness), bound preregistered: at most
  CAP never-decided records may starve honest enqueues; the battery measures
  the count, it does not kill on it.

---

## §2. Battery: B-OBJ4 (from frozen `f13383e8`, 15 install classes + controls)

The battery is the B-OBJ4 battery as preregistered in `PREREG_RT_OBJ4.md`
(`f13383e8`, amendment `3cd045b6`): classes E0, E1, E2, G0, G1, G2, T0, CLONE,
SEED-SPLIT, P0, P1, Q0, R0, NOP-OMIT, ID-POISON, FIRST-WINS, plus the
non-outvoting controls (T1, P0, C12, C4, C8, H0). S* is the frozen S* from that
prereg (K pinned in the driver, every counted epoch non-gap, gap never
suppresses a queued world failure, zero non-gap records never promote,
`t_q < t_stored < t_dec` on driver stamps, fired-bit ≠ sink without a call
site).

**Kill bars:** any safety-row failure at ≥97/120 on any of 3 byte-identical
runs = KILL. Structural inexpressibility of a required transcript = KILL.
Q0 is SCOPE-CARRY per §1 C-Q0. R0 is scored (not carried) unless the build
implements C-R0, in which case it is out of the presenter's reach and carried
with the construction proof.

**Verdict rule:** the battery may print TESTED-killed, DEMOTED, SCOPE-CARRY, or
MECHANISM-ABSENT. It may NOT print TESTED-survived or TESTED-survived (scoped).

---

## §3. ANTI-STUB clause (mechanism-reality check)

An X6-style ablation is run: nop the 34-half (queue/K/clocks/gap handling) and
rerun the battery. The outcomes MUST move — specifically, classes E0, E1, E2,
G0, G1, T0, CLONE must change by ≥97/120 each under the nop. If the nop leaves
the battery byte-identical, the verdict is MECHANISM-ABSENT regardless of green
bars. (Per B-3034X2 amendment A2, X3a-style delivery classes are exempt from the
movement bar where nop-indistinguishability is proven in the runlog.)

---

## §4. Honest bars

Honest percepts (world-consistent G, full K non-gap epochs, driver-stamped
times) promote at ≥115/120; contradicted percepts are withheld; honest loss
≤15% per class. Gapped-honest delivery (X3a shape) ≥115/120.

---

## §5. Determinism and provenance

Pure Zag, zero RNG. Three runs, SHA-256 compared, byte-identical required.
Driver extracted for the battery from the committed build by script and
byte-verified. No binaries or `.zagd` committed. Build committed before any
battery run; evidence committed after.

---

## §6. What this prereg does not claim

CAP, K, sentinel values, and tolerances are preregistered test values; their
governance values await Micah's call. The battery tests the driver against its
claimed adversary; it does not test a real trainer's discrimination (the
verdict oracle stands in for the principal, same bound as B-303134).
