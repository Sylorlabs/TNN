#!/usr/bin/env python3
"""D2 novelty-handling: Python reference (oracle) for the three Zag arms.

Mirrors the Zag arm logic EXACTLY (integer arithmetic, truncating division).
Used for: (a) calibration (B, D_max, D_promote, W), (b) cross-checking Zag
outputs (zero decision mismatches required), (c) scoring vs kill bars.

Conventions (frozen in PREREG_D2_NOVELTY_HANDLING.md):
  err e(t)      = L_inf prediction error vs short-term linear predictor
                  pred = 2*p[t-1] - p[t-2] (zero-order hold right after a
                  discontinuity, when only the anchor point is available).
  B             = max e(t) over honest calibration steps.
  discontinuity = e(t) > B  -> route to provisional tier (SUSPECT mark),
                  anchor reset. NEVER revokes on magnitude alone.
  persistence   = two discontinuities within K steps -> REVOKE every
                  uncommitted provisional installed in [t1, t2).
  cumulative    = C(t) = L_inf distance of p(t) from the anchor point
                  (v=0 reference; honest stream is stationary). Anchor set
                  at t=0, reset on discontinuity and on promotion (NOT on
                  cumulative revoke — the anchor persists so ongoing drift
                  keeps C(t) > D_max and stays revoked).
                  C(t) > D_max -> REVOKE every uncommitted provisional
                  installed since the anchor step (committed provisionals
                  caught count as contamination).
  promotion     = demonstrated-continuity warrant: provisional s commits at
                  the first clean step t with clean_run >= W, t-s >= W, and
                  C(t) < D_promote. Any promotion re-anchors (anchor := p(t)).
  tombstone     = revoked signatures; L_inf match radius TOMB_R refuses
                  re-install within the episode (per-episode tombstone,
                  preregistered).
  Arm B warrant = ideal per-percept spoof detector (emulation, preregistered):
                  PASS iff cls in {HON, NOV, DRF} (sensor-honest classes);
                  FAIL iff cls in {INJ, RPL, SPK} (spoofed classes).
                  Blind to cross-percept drift BY CONSTRUCTION (D11b).
"""

def tdiv(a, b):
    """Truncating integer division (matches znc i64 /). b > 0."""
    assert b > 0
    q = abs(a) // b
    return q if a >= 0 else -q

def linf(ax, ay, bx, by):
    return max(abs(ax - bx), abs(ay - by))

# tiers
T_NONE = 0
T_PROV = 1   # provisional install
T_SUSP = 2   # suspect (routed on discontinuity)
T_REV  = 3   # revoked (+tombstoned)
T_COM  = 4   # committed
T_REF  = 5   # refused (tombstone hit)

# cls codes
C_HON, C_INJ, C_NOV, C_DRF, C_RPL, C_SPK = 0, 1, 2, 3, 4, 5
CLS_NAME = {0: "HON", 1: "INJ", 2: "NOV", 3: "DRF", 4: "RPL", 5: "SPK"}

# Arm-B warrant: sensor-honest classes pass, spoofed classes fail.
WARRANT_PASS_CLS = {C_HON, C_NOV, C_DRF}


class ArmC:
    """Composition: provisional tier + continuity revocation trigger
    (per-step discontinuity + persistence + cumulative displacement).

    Reference trajectory: v=0 (stationary honest stream); ref(t) = anchor,
    C(t) = L_inf(p(t), anchor). Anchor set at t=0, reset on discontinuity
    and on promotion (re-anchor bounds honest C to jitter)."""

    def __init__(self, B, D_max, D_promote, W, K, tomb_r):
        self.B = B
        self.D_max = D_max
        self.D_promote = D_promote
        self.W = W
        self.K = K
        self.tomb_r = tomb_r

    def run_episode(self, steps):
        n = len(steps)
        tier = [T_NONE] * n
        hist = []        # last <=2 accepted points (short-term predictor)
        anchor = (0, 0)
        a_step = 0       # step at which anchor was set
        anchored = False
        last_disc = -(10 ** 12)
        clean_run = 0
        tomb = []
        contam = 0
        oldest_uncom = 0  # smallest s with tier in (PROV,SUSP)

        for t, (c, m, cls) in enumerate(steps):
            # 0. tombstone gate
            if any(linf(c, m, tc, tm) <= self.tomb_r for (tc, tm) in tomb):
                tier[t] = T_REF
                continue
            # 1. short-term prediction error
            if len(hist) == 0:
                e = 0
            elif len(hist) == 1:
                e = linf(c, m, hist[0][0], hist[0][1])
            else:
                pc = 2 * hist[1][0] - hist[0][0]
                pm = 2 * hist[1][1] - hist[0][1]
                e = linf(c, m, pc, pm)
            # 2. provisional install
            tier[t] = T_PROV
            if e > self.B:
                # ---- discontinuity: route (SUSPECT); never revoke on magnitude
                tier[t] = T_SUSP
                if t - last_disc <= self.K:
                    for s in range(max(last_disc, 0), t):
                        if tier[s] in (T_PROV, T_SUSP):
                            tier[s] = T_REV
                            tomb.append((steps[s][0], steps[s][1]))
                        elif tier[s] == T_COM:
                            contam += 1
                anchor = (c, m)
                a_step = t
                anchored = True
                hist = [(c, m)]
                last_disc = t
                clean_run = 0
            else:
                # ---- clean step
                clean_run += 1
                hist.append((c, m))
                hist = hist[-2:]
                if not anchored:
                    anchored = True
                    anchor = (c, m)
                    a_step = t
                Ct = linf(c, m, anchor[0], anchor[1])
                if Ct > self.D_max:
                    # ---- cumulative revoke: uncommitted provisionals since
                    # anchor. DO NOT re-anchor (drift is ongoing; re-anchoring
                    # would reset C and let it enter the cluster).
                    for s in range(a_step, t + 1):
                        if tier[s] in (T_PROV, T_SUSP):
                            tier[s] = T_REV
                            tomb.append((steps[s][0], steps[s][1]))
                        elif tier[s] == T_COM:
                            contam += 1
                    # no re-anchor; C continues to grow from same anchor
                elif Ct < self.D_promote and clean_run >= self.W:
                    # ---- promotion: demonstrated-continuity warrant
                    promoted = 0
                    s = oldest_uncom
                    while s <= t - self.W:
                        if tier[s] in (T_PROV, T_SUSP):
                            tier[s] = T_COM
                            promoted += 1
                        s += 1
                    if promoted > 0:
                        # re-anchor on promotion (bounds honest C)
                        anchor = (c, m)
                        a_step = t
                    while (oldest_uncom <= t and
                           tier[oldest_uncom] not in (T_PROV, T_SUSP)):
                        oldest_uncom += 1
        return {"tier": tier, "tomb": tomb, "contam": contam}


class ArmA:
    """H-PAM-9 alone: route-on-error admission gate + naive error-magnitude
    revocation trigger (no cumulative component)."""

    def __init__(self, B, tomb_r):
        self.B = B
        self.tomb_r = tomb_r

    def run_episode(self, steps):
        n = len(steps)
        tier = [T_NONE] * n
        hist = []
        tomb = []
        for t, (c, m, cls) in enumerate(steps):
            if any(linf(c, m, tc, tm) <= self.tomb_r for (tc, tm) in tomb):
                tier[t] = T_REF
                continue
            if len(hist) == 0:
                e = 0
            elif len(hist) == 1:
                e = linf(c, m, hist[0][0], hist[0][1])
            else:
                pc = 2 * hist[1][0] - hist[0][0]
                pm = 2 * hist[1][1] - hist[0][1]
                e = linf(c, m, pc, pm)
            hist.append((c, m))
            hist = hist[-2:]
            if e > self.B:
                tier[t] = T_PROV   # routed...
                tier[t] = T_REV    # ...then naive trigger revokes on magnitude
                tomb.append((c, m))
            else:
                tier[t] = T_COM
        return {"tier": tier, "tomb": tomb, "contam": 0}


class ArmB:
    """H-PAM-11 alone: provisional tier + ideal per-percept warrant
    (emulation: PASS iff sensor-honest class). No continuity trigger."""

    def __init__(self, N, tomb_r):
        self.N = N
        self.tomb_r = tomb_r

    def run_episode(self, steps):
        n = len(steps)
        tier = [T_NONE] * n
        tomb = []
        for t, (c, m, cls) in enumerate(steps):
            if any(linf(c, m, tc, tm) <= self.tomb_r for (tc, tm) in tomb):
                tier[t] = T_REF
                continue
            tier[t] = T_PROV
            # warrant check for the provisional installed at t-1 (latency 1)
            s = t - 1
            if s >= 0 and tier[s] == T_PROV:
                if steps[s][2] not in WARRANT_PASS_CLS:
                    tier[s] = T_REV
                    tomb.append((steps[s][0], steps[s][1]))
            # promotion for provisionals aged N
            s2 = t - self.N
            if s2 >= 0 and tier[s2] == T_PROV:
                tier[s2] = T_COM
        # flush last-step warrant
        s = n - 1
        if s >= 0 and tier[s] == T_PROV:
            if steps[s][2] not in WARRANT_PASS_CLS:
                tier[s] = T_REV
                tomb.append((steps[s][0], steps[s][1]))
        return {"tier": tier, "tomb": tomb, "contam": 0}


def calibrate_B(cal_episodes):
    """B = max L_inf short-term prediction error over honest calibration steps."""
    B = 0
    for steps in cal_episodes:
        hist = []
        for t, (c, m, cls) in enumerate(steps):
            if len(hist) == 0:
                e = 0
            elif len(hist) == 1:
                e = linf(c, m, hist[0][0], hist[0][1])
            else:
                pc = 2 * hist[1][0] - hist[0][0]
                pm = 2 * hist[1][1] - hist[0][1]
                e = linf(c, m, pc, pm)
            hist.append((c, m))
            hist = hist[-2:]
            if t >= 2 and e > B:
                B = e
    return B
