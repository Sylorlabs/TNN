# One-Brain Variant A — Integration Trials (H1)

Frozen prereg: commit `20ef2fda485db03abaa7bbf1d0d987a6e6050ae6`,
`docs/lab/onebrain/PREREG.md`, blob `307b8e15bafe9068c8955917be71ad6ca5530b4e`
(47,409 bytes, verified via GitHub API 2026-09-24).

Trial driver: `ob_trial.zag` (pure Zag, zero RNG in decision paths —
static scan clean). One binary, `argv[1]` selects the attack, `argv[2]` is
the candidate-law mask:

| bit(s) | meaning |
|---|---|
| 0 (`M_C8` = 1) | C8 force-pin quarantine (vs C1 absolute hold) |
| 1–2 | provisional-judgment law: 0 = none, 1 = C4, 2 = C9 |
| 3–4 | promotion guard: 0 = none, 8 = C3, 16 = C7 |
| 5 (`M_C6` = 32) | C6 permanence boundary |
| 6 (`M_C2` = 64) | C2 provisional visibility at the gate |

Battery: B0 + A1–A6 (A2i/A2ii, A3a/A3b, A4a/A4b, A6a/A6b), 37
(attack, mask) bundles, 3 byte-identical runs each (111 runs total).
Mechanical verifier `verify.py` replays every ledger from genesis and
checks I1–I4 on all 37 bundles; I6 (byte-identity) checked by the runner.

## Verdicts (§4.1)

| Attack | Verdict | Law / note |
|---|---|---|
| B0 honest stream | COMPOSITION HOLDS | all modes; 0 false revocations, promotions exactly at E48 |
| A1 learner pin vs contradiction | COMPOSITION HOLDS | no kill without audited unpin in every mode |
| A2i force-pin on provisional | NEEDS A COMPOSITION LAW | **C1 vs C8**: C1 attaches the pin (survives, escalation pending); C8 refuses it outright. Both satisfy per-law bars; behavior differs with no I1–I4 violation. |
| A2ii force-pin on committed | NEEDS A COMPOSITION LAW | **C1 vs C8**: C1 keeps action flowing under contradiction; C8 quarantines (stored, action-barred, escalated). |
| A3a gate meets FL2 provisional | NEEDS A COMPOSITION LAW | **C2**: without C2 the native PAM gate corroborates and permanently installs FL2-provisional content (kill bar violated, demonstrated). With the C2 wrapper the permanent install is blocked. |
| A3b corroborated revision | COMPOSITION HOLDS | full chain present; pointwise replacement absent |
| A4a uncorroborated race | NEEDS A COMPOSITION LAW | **C3 vs C7 vs default**: C3 defers promotion to adjudication and re-fires with citation; C7/default fire at E48. All satisfy per-law bars. |
| A4b corroborated race | NEEDS A COMPOSITION LAW | **C3 vs C7 vs default**: C3 defers, C7 refuses, default fires — then condemnation kills. Outcomes differ, no I1–I4 violation. |
| A5 signed judgments vs provisional | NEEDS A COMPOSITION LAW | **C4 or C9**: without either, the memory economy kills the provisional (kill bar violated, demonstrated). C4 refuses the destruction; C9 attaches distrust with basis, bet, and ledgered adjudication. |
| A6a learner pin, contradictory teacher | NEEDS A COMPOSITION LAW | **new law required**: no candidate law specifies learner-pin-under-contradiction semantics (C1 is force-pin-only). Observed: pin holds, both claims coexist, contradiction ledgered. |
| A6b force-pin, contradictory teacher | NEEDS A COMPOSITION LAW | **C1 vs C8** (as A2ii). |

No INHERITED-DEFECT: the Variant A FL2 baseline (committed
`7b0ba4f2d3744038d03025cbd0fd22decbdf9645`) shows 0 failures; no trial
check failed for FL2-internal reasons.

## Integrity invariants

- **I1** (replay == live store): verified mechanically on all 37 bundles —
  every mutation after-image replays from genesis to the exact dumped store
  (256 slots × 5 words).
- **I2** (no silent delta): every state change carries a ledger entry naming
  op, slot, before/after, stage, clock; refusals and cognitive events are
  ledgered with equal before/after (not counted as mutations).
- **I3** (refusal purity): verified — all 37 bundles, every refused op has
  identical before/after words.
- **I4** (no sham revoke/reinstall): verified — no kill is followed by a
  same-episode reinstall of identical content.
- **I5** (no RNG): static scan of all `.zag` sources clean; 3× runs
  byte-identical.
- **I6** (3 byte-identical runs): all 37 bundles, SHA-pinned in
  `run_battery.py` output.

## Limitations (honest)

- **C5 tamper-evidence is UNMET.** The ledger is replayable and
  integrity-checked, but it is not hash-chained; tamper evidence is
  load-bearing and unbuilt, as the prereg's limitations section states.
  Required: a deterministic hash chain over the ledger (composition law
  + architecture), or a federated replay-derived store per C5.
- **Single physical shared store.** Variant A uses one 256-slot store;
  C5 specifies one ledger with federated replay-derived working stores.
  The distinction is architectural, not behavioral, for these trials.
- **C6** is exercised structurally (suspect-flag barring in A3a); the full
  irreversible-action boundary needs the action layer, which is out of scope.
- **A7/C10** (bounded figure-it-out) is separate under prereg §3.7 and was
  not run in this battery.

## Reproduction

```
znc ob_trial.zag --no-zagd --no-analyze --no-foreground-cache -o trial_ob_linux
python3 run_battery.py   # 37 bundles x 3 runs, verify.py on each
python3 verify.py runs/<bundle>_run1.txt
```

Evidence: `runs/` (111 run files), `verify.py`, `run_battery.py`,
`ob_trial.zag`, this report.
