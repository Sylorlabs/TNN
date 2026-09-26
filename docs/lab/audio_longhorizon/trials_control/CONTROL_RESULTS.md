# CONTROL_RESULTS — Phase B2b §2b (real references)

## Headline (r1; r3 byte-identical, 2/2 complete runs — see rerun identity)

**Determinism status 2026-09-26:** r1≡r3 proven byte-identical (160/160).
r2 died at 159/160 (VM reboot) and does not count as a completed rerun.
r4 (third complete run) in progress; the 3× requirement is PENDING.

| Axis     | Hits / 40 | Hit rate | Bar (≥70%) | RC0 p (wired>severed) | RC1 deranged |
|----------|-----------|----------|------------|----------------------|--------------|
| Pitch    | 28/40     | 70.0%    | PASS       | p=1.9e-12 PASS       | 0.0% PASS    |
| Envelope | 39/40     | 97.5%    | PASS       | p=6.1e-10 PASS       | 0.0% PASS    |
| Prosody  | 29/40     | 72.5%    | **VOID**   | (pending)            | 27.5% **VOID** |

**Prosody scorer VOID**: RC1 deranged hit rate 27.5% (11/40) exceeds the 25% bar.
Per prereg, this voids the SCORER (not the trial). The 72.5% hit rate cannot be
certified as valid evidence. The ±25% CV hit criterion is insufficiently
discriminating for the prosody40 CV range (0.094–0.487); deranged pairs fall
within tolerance by chance.

§2b verdict: Pitch and envelope PASS with valid scorers. Prosody cannot be
claimed (scorer void). The "each ≥70%" bar is NOT fully met.

**Sanity-floor caveat (ANOM-011):** the prereg's ≥95% scorer-agreement floor
to independent manifest labels cannot be established — the sealed corpus
manifest carries no independent pitch/envelope/prosody labels, and the only
independent F0 tracks (31 PTDB lowf0 clips) are unusable as validators.
Per the prereg's own rule this voids the §2b battery; the hit rates above
stand as measured quantities with this caveat.

Hit criteria (frozen scorer_ctrl.py, SHA 7a4c232a1b96aa1a9a2b52a5b843c35a3c604c7c3f246ea2898ab8421e726224):
- pitch: |f0_ren − f0_ref| / f0_ref ≤ 5%
- env: scorer 3-class == ref 3-class
- prosody: |cv_ren − cv_ref| / cv_ref ≤ 25% (robust CV)

Pitch misses (12, 0-based within the 40-target axis): indices
0,1,4,5,6,9,16,27,30,33,35,37 (corrected scorer; the earlier draft listed
36,38 — those came from the defective pre-correction scorer).
Env miss (1): index 23.
Prosody misses (11, scorer VOID — reported for the record):
3,4,7,8,12,16,27,30,31,32,35.

RC1: frozen derangements (pitch shift-20, env shift-1, pros shift-20) yield 0%
hits — scorer valid (≤25% bar).

## Per-target tables

Full per-target table (r1, corrected scorer): `evidence/control_tables_r1.json`
— per target: ref file, ref vs render F0/env/robust-CV, hit. Headline counts
verified from the same data: pitch 28/40, env 39/40, pros 29/40 (void).

## Drift vs H1

Prereg §2b STABLE rule: hit rate at later checkpoints ≥ H1 − 0.05 per axis,
where H1 = this phase's 40-target real set (depths 1–40 pitch, 41–80 env,
81–120 prosody). This phase ran one continuous 160-target session (no H10/
H100 checkpoint); the only later-checkpoint control data are the paired
pitch repeats at depths 141–160 (same refs as depths 1–20):

| Set (pitch) | Hits | Rate |
|-------------|------|------|
| Early (1–20) | 13/20 | 0.65 |
| Deep (141–160) | 15/20 | 0.75 |
| Drift | | +10.0 pp |

**No DRIFT-FAIL** (bar is drop >5pp). Envelope and prosody have no repeat
targets in this phase's design → no later checkpoint; drift untestable for
those axes. Prosody additionally scorer-void. Verified 2026-09-26 with the
corrected scorer (score_axis lo=1,hi=21 vs lo=141,hi=161 on r1).
