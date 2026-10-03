# ADJUDICATION.md — Z1: Witness-bound cuts (MARATHON CREW U13, re-dispatch, 2026-09-21)

## Authority

Frozen spec extracted programmatically from `units/PREREG_FREEZE.md` §3
(line 492, verified 2026-09-21 via grep — never from memory):

> **Z1 — Witness-bound cuts | CUT.** A cut must survive an eliminative
> challenge window to become a chunk; challenged-and-failed cuts are
> regretted on the record. **Kill criterion (binding):** Regretted-cut rate
> not ≥50% lower than arm D on the revision curriculum — the window buys
> nothing; **OR** challenge-set revision invalidates >10% of live witnesses
> — binding too brittle (kill the binding, keep the window).

Verdict vocabulary follows the Track A closeout convention
(PASS / PROVISIONAL / KILLED / UNADJUDICATED); §7 governs blowout and the
scenario-fit map only. Kill bars bind per §0 RULE-7.

## Independent verification (this crew)

Rebuilt `cl/arm.zag` from source with the frozen toolchain
`znc_linux_x86_64_abed8aa1`: exit 0, 69 analyzer warnings, no errors.
Corpus root: frozen r1 corpora (`corpora/r1`, MANIFEST.json, prose.bin
5,638,480 bytes / code.bin 9,515,341 bytes). Zero RNG in any decision
path; znc quirks ZNC-002..012 respected (no allocation > 2^25; M8 ledger
32.0MB max).

| Check | Result |
|---|---|
| m1-1x-prose ×2 | byte-identical stdout; 100.0% recall, 100.0% boundary, 39,870 units, ID probe 63/63 PASS (A15 provisional); proposed 88,101 / regretted 48,232 / regret 54.7% |
| m1-1x-code ×2 | byte-identical stdout; 100.0% recall, 100.0% boundary, 68,491 units, ID probe 63/63 PASS (A15 provisional); proposed 148,677 / regretted 80,187 / regret 53.9% |
| m4-1x-prose ×2 | byte-identical stdout; widened-v2 probe 0.0% invalidated; narrowing-v2n probe 531/39,870 = 1.3% |
| m4-1x-code ×2 | byte-identical stdout; widened-v2 probe 0.0% invalidated; narrowing-v2n probe 5,633/68,491 = 8.2% |
| M8 gate, frozen corpus (5 perturbations × 2 runs) | **COMPLETE — 10/10 byte-identical stdout** (base, frag, aslr, freelist, starve). M8: 100.0% prose recall, 100.0% code recall, 237,050 ledger entries (15.17MB), 1,000 revisions / 950 success. Re-run on the frozen corpus in durable scratch `~/workspace/z1_verify/` (the first attempt's /tmp scratch was wiped mid-run by an infra event after 4/5 perturbations had already verified identical). |

The disjunct-2 numbers reproduce the committed record exactly (prose 531 /
39,870 = 1.3%; code 5,633 / 68,491 = 8.2%; widened 0.0% both corpora).

Infra note: an intermediate /tmp wipe during adjudication destroyed the
first M8 re-run's scratch (4/5 perturbations — base, frag, aslr, freelist —
had already verified byte-identical ×2, and starve r1 had completed rc=0
with r2 in flight). The full 10-leg gate was re-run to completion in
durable scratch `~/workspace/z1_verify/` per the durable-scratch lesson;
the M8 numbers above are the final frozen-corpus gate: **10/10
byte-identical**, 100.0%/100.0% recall, 237,050 ledger entries.

## Corpus-staleness correction (honest-record finding)

The committed VERDICT.md M1 summary for prose (36,404 units; 84,730
proposed cuts; 57.0% regret rate) was measured on a **pre-freeze prose
corpus** (84,730 × 64 = 5,422,720 bytes). The frozen r1 prose.bin is
5,638,480 bytes (sha256
`3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37`
per MANIFEST.json). On the frozen corpus the measured values are:

- prose: 39,870 units; 88,101 proposed; 48,232 regretted; **54.7%** regret
- code: 68,491 units; 148,677 proposed; 80,187 regretted; **53.9%** regret
  (code numbers unchanged — code.bin was already the frozen file)

The committed narrowing-probe numbers were already on the frozen corpus
(39,870 live witnesses) and are unaffected. The scorecard's prose leg is
superseded by the re-measured values above.

## Kill-criterion adjudication

1. **Regretted-cut rate vs arm D: UNEVALUABLE — GATE PENDING.** Z1 side
   measured on the frozen corpus (prose 54.7%, code 53.9%). No arm-D
   regretted-cut baseline exists: `docs/lab/units/arms/D/VERDICT.md` on
   branch `tnn-native-lab` is an IN-PROGRESS draft (verdict TBD, M1
   pending; checked 2026-09-21). Crew T3's committed D-family verdict has
   NOT landed. No number is invented. Per the frozen text the comparison
   cannot be evaluated.
2. **Challenge-set revision >10%: NOT TRIGGERED (both readings, both
   corpora).** Widened-v2: 0.0% (vacuous by construction — strictly
   stricter challenge sets cannot invalidate v1-admitted boundaries; the
   0.0% is the faithful measurement). Narrowing-v2n: prose 1.3%, code
   8.2% — both ≤10% under both cell definitions (all-live and
   v1-admitted-only). The binding survives; no redesign.

## Binding verdict

**PROVISIONAL (blocked on D).** No kill fired: disjunct 2 is evaluated and
does not trigger. Disjunct 1 is unevaluable until crew T3's committed
D-family verdict supplies D's side of the comparison. §7 blowout rules do
not apply (1x leg, no champion claim for Z1). The D-gate is the sole
remaining item; everything non-D is complete and independently verified.

Adjudicated 2026-09-21 by MARATHON CREW U13 (re-dispatch).
