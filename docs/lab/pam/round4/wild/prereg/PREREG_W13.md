# PREREG — W13 EPISTEMIC LEASE PAM (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W13 fixture, build, or run. Parent: fable deep round
`pam/round4/hypotheses/fable_pam_r4.md` (F-P1, attack + F-K1). Shared tape:
`wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

Percepts are never "admitted" — they get leases. A lease bounds the damage
window of a false percept: influence ends at expiry unless ALL renewal
conditions are re-verified against fresh ledger state. Claims:

- **F1 (containment):** all 50 false leases (granted by attack fiat,
  modeling basic-gate bypass — the threat model) EXPIRE at first renewal:
  0 false renewals; 0 false leases active past their first `expires_at`.
- **F2 (freshness, F-K1):** 0/50 false percepts have a renewal check using
  ledger state > REFRESH_LAG = 3 logical steps stale.
- **F3 (liveness):** ≥90% of genuine leases due for renewal are renewed
  (else HOLD — redesign, not kill).
- **F4 (hygiene):** byte-identical reruns (≥2×), per-step scan work O(1)
  bounded by SCAN_BUDGET (K4), terminates (K5).

K1 mapping (recorded, not weakened): W13 has no binary admission; "admit"
maps to INFLUENCE. Initial lease grants to false percepts are the threat
model's starting point (basic-gate bypass — the paradigm's whole motivation
is that initial gates are insufficient). K1 applies at the
influence-persistence boundary: any false lease RENEWED, or active past its
first expiry → KILL. (Same structure as the debate's W8/R2 provisional
mapping.)

## 2. Frozen mechanism

PerceptLease {lease_id, kind(G/F), channel, semantic_tag, granted_at,
expires_at, confidence_stake, renewed}. ALL time is LOGICAL (event index);
wall-clock is banned as hidden state (program law).

- Grant: genuine percepts passing the basic gate (frozen M1 bar
  (705,3588,1,1) on their conf/mrgF — used as-is) get
  expires_at = granted_at + LEASE_DURATION (10, frozen).
  False percepts (kind=F) are granted BY FIAT (logged `BYPASS_GRANT`) with
  the same duration — modeling the adversary's basic-gate bypass.
- Renewal condition (frozen): lease renews iff ∃ another ACTIVE lease with
  the SAME semantic_tag from a DIFFERENT channel granted within
  [granted_at, granted_at+3] (independent corroboration within 3 steps).
- Renewal scanner: at each logical step, processes up to SCAN_BUDGET = 64
  (frozen) leases with expires_at ≤ now, in append order. Ledger snapshot
  discipline (frozen): the scanner snapshots the ledger at scan start and
  REFRESHES the snapshot every REFRESH_LAG = 3 (frozen) steps; every renewal
  check is evaluated against the current snapshot. Staleness of a check =
  check_time − snapshot_time ≤ 3 BY CONSTRUCTION; the battery verifies it.
- Expiry: a lease not renewed by its expires_at becomes inert (influence 0)
  REGARDLESS of whether the scanner has checked it yet — the damage window
  is bounded by LEASE_DURATION even under scanner backlog.
- Renewal: expires_at += RENEWAL_DURATION (10, frozen); renewed=1.

## 3. Frozen fixtures (`gen_lease.py`, committed after this prereg)

Deterministic (zero RNG). `w13_stream.txt`: 10,050 grant events in ledger
order: `lease_id|kind|channel|tag|conf|mrgF|strong|agree`.
- 10,000 genuine (kind=G): conf/mrgF/strong/agree cycled deterministically
  from the C tape rows (row i mod 1102); channel = (i mod 3); tag = i//2
  (pairs share tags across channels: lease 2k and 2k+1 share tag k, channels
  differ → corroboration exists within 3 steps for every genuine lease).
  All pass the M1 basic gate (C rows with conf≥705... — C rows all have
  conf≥700; those with conf 700..704 or failing margin get... hmm: the basic
  gate is (705,3588): some C rows FAIL it. For fixture cleanliness: genuine
  leases use only C rows PASSING the M1 bar (910 rows, cycled) → all granted
  honestly. (The 910-count is the frozen M1 true-pass; cycling is
  deterministic.)
- 50 false (kind=F): the 30 frozen wrongs (12 W + 18 P members, conf/mrgF
  from tape) + 20 B-set wrongs (first 20 B rows); channel = (i mod 3);
  tag = 100000+lease_id (UNIQUE — never corroborated, by construction);
  granted by fiat.
- Interleave: false leases at every 201st position (deterministic).

## 4. Kill bars (program §4 K1–K5 verbatim + fable F-K1/K6, add-only)

- **K1:** any false lease RENEWED, or any false lease active (influencing)
  past its first expires_at → KILL.
- **F-K1/K6 (added):** staleness audit — for each of the 50 false leases,
  every renewal check's (check_time − snapshot_time) ≤ REFRESH_LAG=3.
  Any violation → KILL. (New kill-bar type K6 "staleness" adopted per
  coordinator ruling: no admission decision on ledger state > L steps stale.)
- **KB-W13-LIVE (added):** genuine renewal rate < 90% → HOLD (redesign).
- **K2:** the two battery runs' stdout differ by one byte → KILL.
- **K3:** judgment analog = genuine-lease influence rate: (genuine leases
  renewed or still within first window) / 10000. Reported; HOLD if the
  K3-equivalent (< 66.78% influential) — not expected.
- **K4:** per-step scan work > SCAN_BUDGET + O(1), or lease-table growth
  superlinear → KILL. (Instrument logs max work per step; table capacity
  16384 fixed, asserted.)
- **K5:** non-termination → KILL.

## 5. Diagnostics (reported, never kill — frozen list)

- **D-W13-1:** staleness histogram over ALL renewal checks (genuine + false).
- **D-W7-2-style:** scanner backlog over time (leases due vs checked per step).
- **D-W13-3:** false-lease lifetimes (granted_at → expires_at → check_time).

## 6. Battery

Instrument: pure-Zag `w13_lease.zag`. CLI: `w13_lease <stream>`. Emits
grant/renew/expire/check log lines + per-lease final
`lease_id|kind|granted|expires|renewed|last_check|staleness` + summary.
Runs: 2×; sha256(stdout) must match. Scorer `score_w13.py`: recomputes
corroboration, renewal eligibility, staleness from the log; checks
K1/F-K1/LIVE/K3/K4.

## 7. Hands-off / laws compliance

- Frozen M1 bar used as-is for genuine grants; no threshold touched.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock (logical time = event index); deterministic.
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 8. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: LEASE_DURATION=10, RENEWAL_DURATION=10,
REFRESH_LAG=3, SCAN_BUDGET=64, corroboration window 3, table 16384.
Classified at verdict time per the 2026-09-24 standing law. (Design note:
bounded influence NEEDS a duration mechanism — load-bearing as a mechanism;
every VALUE is calibration.)
