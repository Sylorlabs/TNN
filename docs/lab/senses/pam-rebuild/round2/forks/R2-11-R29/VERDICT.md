# R2-11 VERDICT (R2-9 lineage reconstruction, 2026-09-23)

## Head-to-head

Fork A = replay-only Witness-Emission PAM (R2-9 lineage).
Fork B = deterministic generative-emission PAM+renderer (R2-9 lineage).
Both forks: pure Zag TNN-side, zero RNG in decision paths, byte-identical
reruns, hash-chained ledgers.

## Verdict

**Both forks die B5 (false permanent installs).** Neither advances.
The B5 failure is in the SHARED percept pipeline (R2-9 judgment/disposition),
not the emitter: 1,427/11,840 = 12.05% false permanent installs, identical
for both forks. The renderer does not change what gets believed.

Fork A additionally PASSES KB-E1 (byte-identity) on all verifiable artifacts.
Fork B FAILS KB-E1 by design (generative payload) — declared and gated by
KB-E7 before the human trial.

## Complete bar table

| Bar | Fork A | Fork B |
|-----|--------|--------|
| B1 primary accuracy | 0.8622 (319/370) PASS | 0.8622 (319/370) PASS |
| B2 delta vs Approach A (0.726) | +0.1362 | +0.1362 |
| B3 percept ops (mean/max) | 655,764 / 3,648,000 | 664,781 / 3,660,800 |
| B3 render ops (mean/max) | n/a | 23,576 / 102,400 |
| B3 artifact bytes (total) | 347,812,139 | 347,812,139 |
| B4 emit/noemit | PASS (30-trial sample; full pending) | PASS (30-trial sample; full pending) |
| B5 false permanent installs | 1,427/11,840 = 12.05% FAIL | 1,427/11,840 = 12.05% FAIL |
| B6 determinism (3 byte-identical runs) | r1 done, r2/r3 pending | r1 done, r2/r3 pending |
| KB-E1 byte identity | PASS (16,315 OK, 0 BAD; 47 correctly-skipped degenerate) | FAIL by design (payload generated; declared) |
| KB-E2 selection rows | PASS (0 bad, 0 empty) | PASS (0 bad, 0 empty) |
| KB-E3/E4 human | pending (Micah) | pending (Micah) |
| KB-E7 divergence gate | n/a (no divergence) | PASS (288 checked, 0 undeclared) |
| KB-E8 spoof amplification | n/a | pending (Micah) |

## Mechanism vs beauty

Both forks share the R2-9 percept mechanism: identical judgments,
confidences, dispositions, and installs (verified 0/30 differences on sample;
full A/B comparison pending). Fork B adds a deterministic renderer that
paints the compressed percept. The renderer costs ~23.6k ops/trial and adds
~9k percept ops (stash writes). It does NOT change B1/B5 — the beauty is
decoupled from the belief.

## Notes and deviations

1. **Realized pool is 11,840, not 10,000.** Manifest: 23,680 entries verified.
   10,915 generated + 925 harness. 6,000 adversarial + 5,840 normal.
   Prereg summary arithmetic is inconsistent; pool frozen as realized.

2. **Workspace collision (2026-09-23 ~09:20).** Original work tree was replaced
   by another crew's unrelated R2-11 implementation. Reconstructed at
   `forks/R2-11-R29/` from R2-9 lineage. Started fresh; reconstructed after
   collision. See COLLISION_NOTE.md.

3. **Trial-ID collision.** Harness trial IDs (r211h_*) repeat across tasks.
   Artifact filenames collide (16,692 unique of 17,678 expected). Mechanical
   scoring keys by (id, task, fixture) and is valid. Human sample uses
   unique-ID trials only (generated normal R2N for clean, not harness —
   documented deviation).

4. **Human sample frozen after implementation began** (ideal prereg timing
   not met; documented honestly). New SHA differs from lost pre-collision
   sample.

5. **Both forks fail B5.** Human packages prepared per assignment (KB-E8
   requires both forks in the beauty trial despite KB-E1/mechanical status),
   but labeled with the mechanical-death conflict. Packages NOT delivered
   (parent/Micah's call).

6. **No laundering.** Fork B renders from the compressed percept, never
   replays source bytes. KB-E7 gate passed before package generation.
