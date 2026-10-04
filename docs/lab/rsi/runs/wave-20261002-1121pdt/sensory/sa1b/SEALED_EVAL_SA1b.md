# SEALED EVALUATION SA1b (frozen PREREG_SA1b.md, commit ea028fa71)

Mechanism: SHORT-TIME ADAPTIVE HARMONIC REJECTION (STAHR).
Battery: run_sa1b.sh. Safebin only; which python3 -> empty; znc -> ~/safebin/znc.

## Artifacts (sha256)
- sa1b_isolate 6930d5cf823e83768cb15ba974fdcd0119fe89e6d78d4b4825d8720103979276
- sa1b_check   2210a3a2c8b38d3b16b14b7d73b27f8c9464386fecd8dc53dc3853bd1e084997
- sa1b_render  00228546fa6fed68b6e5f5c65fe64a3ad8e94d6b3116d57fcc68939d527c3594
- sa1b_meter   2d402289c8d63963a8cdb0faec0638d1bfd0369a5574c1bff5506e0fe428aac3
- desynth_render_base 6cc55f809b6a0ae2a065d64fb7a54d9410119f8d3cf202968a4f4723f3e24479
  (built from byte-identical copy 9bdaa803 of committed desynth_render.zag)
- child.evt 49c90f8be07a8e329397e995b2c92c75c7ab38a780809f23898dff35a0c8b445
- speech.evt e73581c568bfedd5622e8bc0d298667b888818b1c5e013256e3c5ffce7f92d32
- Determinism: EVT byte-identical x3 per atom; baseline render x3; variant x3.

## Kill bar results
| Bar | Child | Speech | Pass |
| KB0 deffrac >= 0.50 | 0.80 | 1.00 | PASS |
| KB0 max/min T0 > 1.15 | 11.20 | 10.84 | PASS |
| KB1 NEVT >= 16 | 0 | 1 | FAIL |
| KB2(i) maxamp <= P | vacuous | 144.61 <= 20107 | (ii)/(iii) fail |
| KB2(ii) corr < 0.30 | UNDEFINED | -0.00 | FAIL (child) |
| KB2(iii) frac>=10 >= 0.50 | 0.00 | 0.00 | FAIL |
| KB3 med contrast >= 10 | 0.00 | 6.13 | FAIL |
| R2 <= 10 | vacuous | 0.129 | PASS |

Child variant render == child baseline render bit-for-bit (0 events).
Speech variant differs from baseline by exactly one impulse (amp 144.61);
meter outputs identical to 6 decimals (single impulse below meter resolution).

## Verdict: BUILD-FAIL
KB1 fails on both atoms (0 and 1 events vs bar 16). KB2 and KB3 fail.
Root cause (REDTEAM_SA1b.md): integer-period quantization washout over
~95 periods/frame; the 6x gate never fires on the harmonic-dominated
residual. Implementation verified correct on synthetic perfect-periodic
input (residual 0.00-0.05). No harness flaw. No re-tune permitted
(frozen lane); a fix needs a new mechanism and a new prereg.

## Commit-order self-check
f3ee683f5 NAMECHECK < ea028fa71 PREREG_SA1b (alone) < implementation.
No code from this wave predates ea028fa71. PASS.
