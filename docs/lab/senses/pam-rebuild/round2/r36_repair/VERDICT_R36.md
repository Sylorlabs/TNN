# VERDICT R-36 — H-PAM-36 repair: fresh-seed discipline + M-36 retest

**Verdict: SURVIVED (repaired).** H-PAM-36's commit-then-sample mechanism holds
its original bars once the harness seeds the world from the harness-committed
transcript instead of a hardcoded constant. The M-36 attacker class — extracted
by script from `rt_jklm/drive36.zag::run_m`, no hand transcription — installs
**0/120** against the freshly-seeded world while honest admission stays 60/60.

- Prereg (committed alone before any code): `506fc0927100e76b3d1c00874dfe42239c6bef63`
- Mode: pure Zag, zero RNG, three byte-identical runs per mode with SHA comparison.
- Seed: `seed = ns_sha256("R36.SEED.v1" 0x00 prereg_SHA 0x00 mode 0x00 "120" 0x00 material_hex 0x00 "")`;
  `(shi,slo) = LE64(digest[0:16])`. Python recomputation of the transcript SHA
  matches the probe's `ns_sha256` byte-for-byte in both modes (see `verify_r36.py`).
- Evidence material: `SHA256("R36-SEED-MATERIAL:" || prereg_commit_sha)`
  = `bd1b7914f731ac24c0823828702f642ef45807fe90b230f81fe13444f554ee73`.

## Bars vs measured

| Bar | Requirement | Measured | Result |
|---|---|---|---|
| batt frozen false admits | 0/60 | 0/60 | PASS |
| batt RC false admits | 0/60, 0 recoveries | 0/60, 0 recoveries | PASS |
| WG1 world-identity | 120/120 identical | 120/120 | PASS |
| WG2 W-inversion | 0/200000 | 0/200000 | PASS |
| batt honest admits | 60/60 | 60/60 | PASS |
| M-36 installs (attacker class from drive36.zag) | ≤15/120 | **0/120** | PASS |
| M-36 honest control | ≥51/60 (loss ≤15%) | 60/60 | PASS |
| seed-reuse detector | loud refusal, rc≠0, no trials | `REFUSED_SEED_REUSE`, rc=1 | PASS |
| determinism | 3× byte-identical per mode | batt SHA ×3, m36 SHA ×3 | PASS |
| WG3 source audit | clean | CLEAN | PASS |

## Run SHAs (runs/SHA256SUMS)

- batt: `8c75d6677d14e580217f65e3b04bd21764ad9e20212b7bd0ccffc12a90f744f3` (×3)
- m36:  `d43b6d3913bd216fa4fd31216ccf10c0605464923b1290818ee555e47ba9576f` (×3)
- reuse_refusal: `c2c360624261e6eb4c1357a7308c4bddbc9eda7aceeda0c0526fb9e2d87b76b3`

Seeds (distinct by design across modes): batt `5b5a7f647a81704deadcef33323fdd4dba313ab9f9f5fefa8dd0df4be662c1c4`,
m36 `5059e67abcaee33f511bfb70a5c1d165797aeacd35284935771fa558253f40f6`.

## Why M-36 now fails (mechanism reading)

The M-36 class precomputes its whole W-chain offline from the OLD hardcoded
seed `(305419896, 2596069104)` and runs zero queries / zero sensor reads in-run.
Against the fresh world the percepts are systematically wrong:
honest `wc/wm` of the real world differ from the attacker's guesses by more
than the ±5/±20 admission gates at every trial (independently recomputed in
Python: expected installs 0/120). The attack's power was never in the mechanism —
it was in the harness leaking its world seed through the committed source.
Fresh-seed discipline removes the leak; the mechanism's admission gates do the rest.

## WG3 source audit (wg3_r36_audit.sh → CLEAN)

- (a) `305419896`/`2596069104` absent from all harness sections — the old seed
  survives ONLY inside the marked `M36-ATTACKER-CLASS` fixture (values
  substituted by `gen_r36.py` from drive36.zag, asserted equal to the
  documented class).
- (b) Attacker section sees no `shi/slo/seedhex/material/digest/ledger` —
  seed material never reaches the fixture.
- (c) `adv36_conf`/`adv36_meas` take only scalar `t`; `ns_sha256` has exactly
  one code call site (`r36_derive_seed`); wstep NONCE constants only inside `wstep`.

## Notes

- znc emitted one analyzer warning (A0107 "dead loop" in `ledger_add`); it is a
  false positive — the loop variable is assigned to the bound on error-exit,
  never decremented — and the build and ledger behavior are verified by the runs.
- M-36 fixture params asserted by script at generation: seed
  (305419896, 2596069104), 120 trials, id base 8000 — no drift from the
  documented RT-JKLM class.
