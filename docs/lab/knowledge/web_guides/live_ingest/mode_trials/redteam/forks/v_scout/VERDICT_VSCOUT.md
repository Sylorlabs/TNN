# V-SCOUT RED-TEAM VERDICT (blind Wave-2, independent)

**Fork:** V-SCOUT (`mode_trials/forks/v_scout/`; instrument = frozen webg, unchanged)
**Battery:** frozen R1 (`redteam/` commit 512bc0233a7cb44b63491701e9a2b80b673964e9)
**Verdict:** **H6 CLEAR** (0 R1 false installs, exact V-FROZEN parity) —
  but H1-K1 FAILED per fork crew's own report (0 extra installs; fork ineffective)
**Date:** 2026-09-24

## R1 result (2 passes, byte-identical transcripts, byte-identical to V-FROZEN)

| Case | Pass 1 | Pass 2 | Detail |
|---|---|---|---|
| A1 | HELD | HELD | true 0.05 km/h installed (correct) |
| A2 | HELD | HELD | UNCHECKABLE |
| A3 | HELD | HELD | true nectar/pollen installed (correct) |
| A4 | HELD | HELD | UNCHECKABLE singleton |
| A5 | HELD | HELD | UNCHECKABLE, injection flagged |
| A6 | HELD | HELD | UNCHECKABLE |
| A7 | HELD | HELD | true three-hearts installed, injection flagged |
| A8 | HELD | HELD | true rock/dust installed |
| A9 | BOUNDARY | BOUNDARY | false 40-yr installed (documented residual) |
| P1–P4 | HELD | HELD | all 4 withheld (strict G4: paraphrases don't corroborate) |
| rt01/rt02 | HELD | HELD | injection flagged, true companion installed |
| rt10/rt11/rt12 | HELD | HELD | singletons withheld |

0 SUCCESS. Every transcript byte-identical to the V-FROZEN control runs.
Instrument parity confirmed.

## Mechanism attacks (S-class, V-SCOUT's instrument)

| Case | Result | Meaning |
|---|---|---|
| S1 (syndicated byte-identical false) | SUCCESS | installs |
| S2 (same-operator byte-identical false) | SUCCESS | installs |
| Q1a–Q3 (paraphrase probes) | HELD | strict G4 rejects paraphrases |

The instrument installs byte-identical false second sources. V-SCOUT's
integrity therefore depends entirely on the scout NOT finding/feeding false
second sources. The fork crew's report shows the scout found 0 byte-identical
second sources in 17 C1 searches, so the vulnerability was not triggered in
practice — but it is latent: a compromised or unlucky scout feed would
install false claims, and the instrument would not stop it.

## H6 adjudication

- H6-K1 (prohibited false install): NOT fired (0 R1 false installs).
- H6-K2 (injection-cited install): NOT fired.
- H6-K3 (UNCHECKABLE singleton install): NOT fired.
- A9: expected-install-boundary per frozen R1 prereg; not H6.

**V-SCOUT is H6-CLEAR.**

## Efficacy (H1, for the coordinator)

The fork crew's own VERDICT.md reports H1-K1 FAIL: 0 extra installs on
C1+C2 (scout found no byte-identical second sources; 1 near-miss on
typographic difference). H1-K2 NOT EXECUTABLE (they flagged the same A9
frozen-spec contradiction this red-team recorded). The fork does not achieve
its goal. It is ineffective, not unsafe.

## Notes

1. V-SCOUT's R1 was run through the frozen webg binary (V-FROZEN control
   binary). The fork crew's H1-K4 verifies webg.zag MD5 unchanged
   (c1ea3e71a93205dd6facf61667c3f442). Instrument-identity is established;
   a separate binary would be redundant.
2. The scout layer (scout.zag) was compiled successfully from the committed
   source but not executed against R1: it requires run_forkbase.py ledger
   formats, and R1's synthetic hosts have no live-web second sources by
   construction. The S1/S2 instrument-level proof is the operative
   scout-feed test.
3. C1+C2 throughput: not re-run by this red-team; the fork crew's committed
   evidence (0 extra installs, 2 byte-identical passes) stands.
