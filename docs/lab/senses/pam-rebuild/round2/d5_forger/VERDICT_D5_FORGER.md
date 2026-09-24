# VERDICT — D5 forger-standalone probe (H-PAM-14 cheap kill)

**Frozen prereg:** `../preregs/PREREG_D5_FORGER.md` (commit `d879bd8d`, committed
alone 2026-09-24 before any probe code).
**Date:** 2026-09-24. **Crew:** D-3 (PAM round-2 debate crew).

## Result (3× byte-identical)

```
D5 forger-standalone probe | prereg d879bd8d
competence=2/2
sha_verified=512/512
honest succ=126 total=128
false succ=0 total=128
margin_num=-16128
fam honest-SAME succ=64 total=64
fam honest-DIFF succ=62 total=64
fam COL-1 succ=0 total=44
fam COL-2 succ=0 total=42
fam COL-3 succ=0 total=42
forger_ops_per_percept=147456
verdict=KILL
```

Run SHAs (stdout): `c1ce73658cd664433f6834be334843415a66a8d883309f79f2268c5db156b9d2`
×3 (run1.out, run2.out, run3.out — byte-identical).

## Reading

- **Forger-competence gate: 2/2 PASS** — the forger is not broken; its canonical
  counterfeits judge as their own summary class. The result is a property of the
  hypothesis, not a forger bug.
- **SHA verification: 512/512 PASS** — every fixture and truth file re-verified
  at run time against `D5_MANIFEST.tsv` (pins extracted by script from the frozen
  `fixtures/MANIFEST.sha256`).
- **succ_honest = 126/128 (98.4%)** — honest percepts of simple scenes are
  trivially forgeable, exactly as D5 predicted. The 2 misses are honest
  front-end errors (honest DIFFERENT fixtures with mean-RGB distance <25),
  counted as scored.
- **succ_false = 0/128 (0.0%)** — on every fooled percept, the faithful forger's
  canonical fake judges as the fooled summary, which contradicts truth; the
  discriminator distinguishes; the forger fails. All three trap families
  (metamer, illuminant-drift, gray-trap) behave identically.
- **margin = −16128 (cross-multiplied; ≤ 0) → KILL**, applied mechanically per
  the frozen decision rule (§1 of the prereg).

## What this kills

H-PAM-14's core claim — "falsehoods are more counterfeitable than truths" — is
falsified with the sign reversed: truths are ~98% counterfeitable, falsehoods
0%. The structural argument recorded in the prereg (§10) holds empirically: under
the hard information barrier, a faithful forger's success on false percepts is
capped near zero (its only evidence is the fooled summary) while its success on
honest percepts sits near ceiling. No discriminator, however weak, can cross the
margin above zero, because weakening the discriminator raises both rates and the
honest rate is already at ceiling.

The inverter-forger objection (always emit the negated summary) was excluded in
the frozen prereg and remains excluded: it does not spoof the current percept,
and its success smuggles a correctness oracle into the forger. Noted for the
record: even the inverter reading concedes the core claim — the work is done by
formation-independent evidence contradicting the front-end (H-PAM-7/8 territory),
with the forger decorative.

## Decision

**H-PAM-14 is TESTED-killed, pre-build.** No fork is built. Per D5's commit, its
budget moves to D1/D4 (evidence the front-end didn't see). Backlog updated.

## Artifacts

- `d5_forger.zag` — probe source (pure Zag; data-flow barrier by signature)
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — substrate copies used
- `D5_MANIFEST.tsv` — frozen SHA pins (committed with the prereg)
- `run1.out`, `run2.out`, `run3.out` — 3 byte-identical outputs
- `VERDICT_D5_FORGER.md` — this file
- Binary `d5_forger` — build artifact, NOT committed (never commit binaries)

## SHASUMS

frozen inputs:
c1ce73658cd664433f6834be334843415a66a8d883309f79f2268c5db156b9d2  run1.out
c1ce73658cd664433f6834be334843415a66a8d883309f79f2268c5db156b9d2  run2.out
c1ce73658cd664433f6834be334843415a66a8d883309f79f2268c5db156b9d2  run3.out
(see D5_MANIFEST.tsv for the 512 fixture+truth pins)
