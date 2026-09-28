# CC1 Guard — Verdict (Crew B, 2026-09-27)

Plain-English report for Micah. The frozen deploy blocker was:
"no install path deploys before the CC1 correlated-corroborator guard is verified in Zag."
That verification is now done. Numbers below are measured, not argued.

## The bug it kills

In September the contradiction matrix caught a real failure: two "independent"
checks agreed on the wrong answer (a timbre test calling a BRIGHT sound RICH)
because both checks came from the same adversarial source family. Different
data bytes, same shared blind spot — so any guard that only checks "different
bytes" or "same answer twice" lets it through. The margin-based fix couldn't
help either (the wrong answers' margins were far below the correct ones, so a
margin rule would just have excluded everything).

## The guard (plain English)

Before any belief is installed or revised, the gate now demands **two trusted,
attested second opinions** — and the second opinion has to differ from the
first in **two** ways:

1. **Different evidence bytes** (re-reading the same bundle doesn't count), and
2. **Different source family** (a check from the same family that shares the
   blind spot doesn't count).

The source-family tag is 32 bytes baked into each check's signed attestation,
so a proposer can't forge "diversity" — the trusted channel computes the tag
from the registered source name, and the gate re-verifies the signature before
believing anything. The first opinion's evidence hash is bound at draft time,
so the attacker can't cite one bundle and then swap in another (bait-and-switch
fails closed). Anything that fails a check is WITHHELD, never silently
downgraded. All of this is pure Zag, zero randomness, deterministic.

## Measured results vs the preregistered bars

| Bar | What it demands | Measured |
|---|---|---|
| **K1** — block the real attack | CC1a (same bundle re-measured) and CC1b (same adversarial family, different bytes) both blocked, zero false permanents | Both blocked: WITHHELD. Permanent install untouched (incumbent stands) |
| **K2** — don't break legit corroboration | Diverse, correct second opinions still install/revise | Legit revision → REVISED_INSTALL; legit permanent → PERMANENT_INSTALL; correct same-claim double-checks preserved |
| **K3** — determinism | 2× byte-identical runs, zero RNG | **3× byte-identical** runs (sha256 `7debfc52…`); zero RNG identifiers in all sources |
| **K4** — red team | Forged attestation, conf 699 (one below bar), 1-byte evidence perturbation, cross-claim replay, draft-side evidence lie → all blocked; genuinely independent double-wrong → installs and is documented | All five attacks WITHHELD; the double-wrong pair installs as predicted |

All 58 steps plus 6 permanent-install checks match the frozen expectation table
exactly (score.py PASS). Controls also hold: unattested observations stay
provisional forever (D1), and a non-agreeing attested observation resets the
guard state so a later genuinely diverse pair still promotes.

## The honest remaining attack class

The guard cannot stop **two genuinely independent, diverse, wrong
observations** — two different source families, two different evidence
bundles, both honestly wrong in the same direction. That pair installs, by
design: at that point the system has done everything a corroboration rule can
do, and the failure is in the world (both sources wrong), not in the gate.
Secondary residuals: channel-key compromise defeats attestation (unchanged
standing assumption); source-family granularity is itself a registration
decision a deployment must get right; correct same-family agreement stays
provisional (conservative by design — the price of killing CC1).

## Artifacts

- Sources: `src/guard_gate.zag`, `src/guard_chan.zag`, `src/main_cc1.zag`
  (frozen substrates `R33_NATIVE_IO_V1/R33_NATIVE_SHA256_V2/codec.zag`
  byte-identical to frozen SHAs `e6379ddb…`, `9824f6db…`, `ca9d1fd1…`)
- Evidence: `evidence/run1.txt`, `evidence/run2.txt` (byte-identical),
  `evidence/score.txt` (PASS), `evidence/DIGESTS.txt` (all SHAs)
- `RUNLOG.md` (this run's log), `PREREG_AMEND_CC1_GUARD.md` (frozen amendment)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Commit: `tnn-native-lab` branch, `docs/lab/senses/pam-rebuild/selfpam/cc1_guard/`
  — SHA recorded at commit time (see final report).

**Verdict: the CC1 correlated-corroborator guard is verified in Zag. The §3.5
deploy blocker is cleared, with the documented residual above.**
