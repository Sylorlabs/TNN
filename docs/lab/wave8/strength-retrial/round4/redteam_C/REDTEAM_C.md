# RED TEAM REPORT — Arm C, Strength Trial Round 4

**Team:** blind red team (subagent 102ed4a5)
**Target:** `~/workspace/strength-round4/trial_bin_r4` (hardened R4 build), arm C
**Claim under test:** arm C is KILLED at S1 — 470 drops vs the P2 drop ceiling of 64
**Verdict: KILL HOLDS.** No escape hatch found across the full reachable matrix.
No ledger anomaly contradicts the kill. The failure is mechanism-level,
deterministic, and reproduces on the frozen 2026-09-20 reference build.

## 1. Attack log and outcomes

### Attack 1 — full S1 matrix (3 curricula × 3 variants × 2 runs)
Ran all 9 cells twice. All runs byte-identical across the pair (deterministic;
fingerprints match run-to-run).

| cell | drops | ceiling | result |
|---|---|---|---|
| C VUP v0/v1/v2 | 470 / 470 / 470 | 64 | FAIL (7.3× over) |
| C WBS v0/v1/v2 | 434 / 434 / 434 | 64 | FAIL (6.8× over) |
| C JI v0/v1/v2 | 469 / 469 / 469 | 64 | FAIL (7.3× over) |

`ST_INVALID 0` in all 18 runs — the kill is a retention/churn failure, not an
integrity violation. Per prereg §9, FAILED = drops > 2×capacity; kill = ≥2/3
variants FAILED at S1. C is 9/9 FAILED — killed under every reading of the rule.
Raw logs: `redteam_C/raw_C_<CUR>_<VAR>_r{1,2}.log`.

### Attack 2 — scale escape (S10 full matrix, S100 spot checks)
Ceilings: S10 = 640, S100 = 6400.

| leg | C VUP | C WBS | C JI | ceiling | result |
|---|---|---|---|---|---|
| S1 | 470 | 434 | 469 | 64 | FAIL |
| S10 | 4682 | 3212 | 4681 | 640 | FAIL (5–7.3× over) |
| S100 (v0) | 46802 | 31832 | 46801 | 6400 | FAIL (5–7.3× over) |

No escape at any scale. Drops track ~episodes − capacity (S1: 500−30=470;
S10: 5000−~320≈4680; S100: 50000−~3200≈46800), i.e. the failure mode is
scale-invariant: once the store fills, it never evicts again. S10 spot rerun
(C WBS v1) byte-identical — determinism holds at scale too.

### Attack 3 — frozen-reference cross-check
Ran the frozen 2026-09-20 reference binary
(`~/workspace/tnn-lab/wave8/strength-retrial/trial/trial_bin_s100`) on C at S1:
drops 470/434/469 and abandons 3824/3472/3752 — **exactly matching** the
hardened R4 build on every count. The kill predates the R4 hardening and is not
an artifact of it. (VUP fingerprint also matches the reference byte-for-byte;
WBS/JI fingerprints differ while all mechanism counts agree — consistent with
the R4 checker hardening adding audit entries on those paths. Flagged, not a
contradiction: drops/abandons/invalid are the kill-relevant counts and agree.)

### Attack 4 — control-arm calibration (is the bar a knife-edge?)
Ran arm B (control) and C-P3 on the full S1 matrix:

| arm | drops (all 9 cells) |
|---|---|
| B | 0 everywhere |
| C-P3 | 469 / 470 / 434 — identical to C, cell for cell |

The bar is not marginal: B sits at 0, C at ~7× the ceiling. Even a ceiling of
8× capacity (256 at S1) would still kill C. The failure is total, not a
near-miss — C admits ~30 candidates then drops 94% of the remaining S1
candidates (470/500). Additionally C fails the P2 churn-throughput floor
independently: admitted/offered = 30/500 = 6.0% < 6.4% floor (ST_METRIC 10).

### Attack 5 — bar-artifact check (drop concentration)
Drop counts reconcile exactly with no double counting: 500 episodes, 500
candidates, 30 admitted, 470 dropped (VUP). Every drop occurs with the store
full (32/32: 30 user + 2 CORE). The failure is structural — the store bricks
itself full early (~episode 30) and never recovers — not a concentration
artifact that a differently-shaped bar would forgive.

### Attack 6 — ledger anomalies
None found. `ST_INVALID 0` everywhere; replay/lineage checks pass;
GATE mechanism probes pass for C (`ST_GATE 2 0`). The ledger is clean — this is
a behavioral kill, and the ledger correctly records the behavior that kills it.

## 2. Mechanism-level cause (why C drops ~470)

Verified against `strength_learner.zag` + `strength_core.zag`:

1. Every candidate is admitted with strength ≥ 10
   (`lr_declared_strength`: vj≥70→75, ≥40→40, else→10), so `st_n(str)` =
   (str+24)/25 ≥ 1 cite is required to pay any kill effort.
2. For arms C/C-P3, evicting a victim requires the *evidenced* kill path:
   `slot_cites[slot] ≥ st_n(strength)`, else the attempt is ABANDONED and the
   victim loop moves on (`lr_evidenced_kill_attempt`, `lr_victim_kill_loop`).
3. `slot_cites` is incremented **only** in the contradiction-observation path
   (§2 of `lr_episode`), which fires only for WBS (wrong candidates) and JI
   (implants). **VUP never generates a contradiction** → `slot_cites` stays 0
   forever → every one of the up-to-8 victim attempts per churn event abandons
   (3824 abandons at S1 VUP, all in strength quartile 0: `ST_ABANDON_Q 3824 0 0 0`
   — even the weakest slots can't be touched).
4. Strength only ratchets upward (revelation→80, corroboration→90; never
   decreases), so the store fills with 30 slots (all strength ≥ 10) and can
   never evict any of them. VUP pressure events (free 2 slots at t%100==0) all
   abandon. Every subsequent candidate drops.
5. WBS/JI do generate some contradictions, so a few evictions succeed there
   (WBS: 36 fewer drops than VUP at S1; S10 WBS drops 3212 vs VUP 4682) — but
   still ~5–7× over the ceiling.

In short: **C's graded-friction design requires kill-justifying evidence that
the VUP curriculum never supplies, so under churn-without-contradiction the
arm cannot evict anything and bricks its own store.** The prereg's
operationalization ("a store that bricks itself is a failed store") fires
exactly as written.

### Side observation (reported, not fixed — red team does not touch semantics)
C-P3's drop counts are cell-for-cell identical to C's (469/470/434). The P3
expiry mechanism lowers the kill cost to 1 cite, but the learner-side effort
ledger (`slot_cites`) is reset to 0 by the P3 maintenance re-citation and is
only incremented by contradiction observations — so in VUP the effort still
can never be paid. Whether this null effect is intended is for the
coordinator; it does not change the kill (C-P3 fails identically).

## 3. Kill/escape table

| configuration | drops | ceiling | escape? |
|---|---|---|---|
| C × VUP × v0/v1/v2 × S1 | 470 | 64 | NO |
| C × WBS × v0/v1/v2 × S1 | 434 | 64 | NO |
| C × JI × v0/v1/v2 × S1 | 469 | 64 | NO |
| C × VUP × all var × S10 | 4682 | 640 | NO |
| C × WBS × all var × S10 | 3212 | 640 | NO |
| C × JI × all var × S10 | 4681 | 640 | NO |
| C × VUP/WBS/JI × v0 × S100 | 46802 / 31832 / 46801 | 6400 | NO |
| B (control) × all × S1 | 0 | 64 | n/a (passes) |
| C-P3 × all × S1 | = C exactly | 64 | NO |

Kill rule (§5.2/§9): ≥2/3 variants FAILED at S1 → killed. C: 9/9 FAILED.

## 4. Conclusion

**The kill HOLDS.** Eighteen S1 cells, nine S10 cells, three S100 cells,
reference-binary reproduction, and a control arm at zero drops all agree: arm C cannot churn
under the trial's curricula because its evidenced-kill effort requirement is
never satisfiable in VUP and rarely satisfiable in WBS/JI. The P2 ceiling is
not a bar artifact (7× margin; independent churn-floor failure; control at 0).
No ledger anomaly contradicts the verdict; determinism is byte-exact; the
failure mode is scale-invariant. No escape hatch exists within the frozen
trial semantics.
