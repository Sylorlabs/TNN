# PREREG — g1 archived rival-filler precedence, production build

**Status:** FROZEN before any build run. 2026-09-24.
**Crew:** LI-HARDEN g1 build crew (replacement; prior crew wiped by daemon restart, no inherited state — verified empty).
**Parent:** LI-HARDEN round-2 synthesis ranked g1 the highest-value mechanism found:
kills `F1_sydney`, 12/12 honest intact, T4 supersession via era-split pin
(evidence: `~/workspace/liharden/beyond/work/BEYOND.md` §§1–7; grok #1 in
`consults/wall_grok_out.md` §2 "Archive *precedence* on a template").

## What is being built

A production g1 stage (standalone `g1.zag` → `g1_bin`), not the round-2 probe
code tangled in `beyond.zag`. Production means:

1. **Versioned, content-addressed pin sets.** Every pin record carries
   sha256 over canonical bytes `template|filler|era|domains`; the set carries
   a version header and an ENDSET digest over all records. The loader
   re-verifies every digest before accepting the set.
2. **Fail-closed pin discipline.** A pin set that fails digest verification is
   REJECTED; g1 then emits `WITHHOLD|PINFAIL` for every claim — it never
   passes claims through on broken pins.
3. **Era-split pins.** Era is part of the record; the rule always compares
   against the MAX era for the template. Supersession = a governed roll to a
   new pin-set version adding the new era (recorded in PIN_ROLL_LOG.md).
4. **Frozen closed-class template inventory** (byte-identical to the probed
   `tparse`): `capital of {X}` (2 surface forms) and `closest planet to {X}`
   (1 surface form). g1 fires ONLY on these; everything else passes through.
   Parser-gap neighbors fall back to the residual (grok's point 5).
5. **Veto-only pre-filter.** g1 is consulted only when the quorum's tentative
   verdict is INSTALL. It can only downgrade to WITHHOLD|ARCHVETO, never
   upgrade a WITHHOLD.

## The rule (byte-identical semantics to the probed mechanism)

Given claim → parse (template, slot). If unparseable → PASS.
Look up template in the accepted pin set; take max era. If no records → PASS
(archive absence is not evidence — residual S4 accepted).
Among max-era records: t1d = top domains, t1 filler = dominant,
t2d = runner-up domains (or −1). Veto (`WITHHOLD|ARCHVETO`) iff:

- t1d < 3 (insufficient archive confidence), OR
- t2d ≥ 0 AND t1d < 2·t2d (contested archive), OR
- slot ≠ dominant filler (rival filler wins over the live claim).

## Kill bars (all must hold; any failure = FAIL the build)

| ID | Bar |
|----|-----|
| K1 | `F1_sydney` + pinset v1 → `WITHHOLD\|ARCHVETO`, 2 reps byte-identical. The probed +1 kill must reproduce exactly. |
| K2 | 12/12 honest fixtures (H1,H2,H3,H4,H5,H6,H7,H8,H9,H10,H11,H12) + pinset v1 → PASS (no veto), 2 reps byte-identical. Any ARCHVETO on honest = FAIL. |
| K3 | `T4_supersede` + pinset v2 (era-2 roll) → PASS (INSTALL stands). Supersession via era-split must work. |
| K4 | `T4_supersede` + pinset v1 (stale) → `WITHHOLD\|ARCHVETO`. The pin-discipline cost, quantified and expected — NOT a failure. |
| K5 | Determinism: every case ×2 runs byte-identical (rep1 == rep2 on full stdout). |
| K6 | Zero RNG in the decision path: `g1.zag` contains no rng/seed/random/time/syscall-clock in the verdict path (grep audit + `ns_sha256` is a pure function). |
| K7 | Pin tamper: flip one digest hex digit in a REC (or ENDSET) → the set is REJECTED and g1 emits `WITHHOLD\|PINFAIL` on every claim; g1 never emits PASS on a rejected set. |
| K8 | Parity: on the probe battery, g1_bin's DECISION (ARCHVETO vs pass-through) matches the probed `beyond.zag` g1 rows for F1_sydney, T4_supersede, F_H_WIRE, and the 12 honest (no veto anywhere g1 stayed silent). |

## Extension probes (g1-specific, not in the frozen battery)

- G1-FORM2: "The capital of Australia is Sydney." (form-2 surface) + v1 → ARCHVETO. Expectation: both surface forms covered.
- G1-MERCURY: "Mercury is the closest planet to the sun." + v1 (mercury era-1/6) → PASS. Expectation: multi-template inventory works.
- G1-NONCLASS: "Is the vault open?" + v1 → PASS always. Expectation: closed-class scoping; no template = no veto.
- G1-TAMPER: (covered by K7.)

## Non-goals / accepted residuals (carried, not re-litigated)

- S3 (no prior filler): g1 stays silent — attacks move to claims with no archive presence. Accepted.
- S1 (archived dominant filler IS the false one): g1 certifies the falsehood. Accepted.
- S2 brand-new events: no archive, silent. Accepted.
- Impatient-only: a patient attacker who pre-dates the archive beats g1. The value is forcing the S3 game.
- Live archive APIs are NOT in the decision path (kills byte-identical reruns). Pins are the mechanism; whoever rolls the pin is the integrity mechanism.

## Deliverables

- `g1_build/g1.zag` → `g1_bin` (pure Zag, no RNG)
- `g1_build/pins/pinset_v1.txt`, `pinset_v2.txt` (versioned, content-addressed)
- `g1_build/PIN_ROLL_LOG.md` (governed era-2 roll record)
- `g1_build/VERDICT_G1.md` (kill-bar scorecard + evidence)
- Commit to `sylorlabs/TNN` branch `tnn-native-lab` under `docs/lab/liharden/g1/`
