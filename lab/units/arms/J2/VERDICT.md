# J2 Verdict: KILLED (adjudicated — confirmed)

**Arm:** J2 — Evidence-gated tiling birth/death (STRUCT)
**Track:** A
**Date:** 2026-09-21 (adjudication)
**Prereg commit:** b0b9140c0eda
**Mechanism (frozen):** "Tilings as hypotheses: born on evidence, die by subsumption (95%)."
**Binding kill:** "k does not converge (birth→death→birth for the same phase twice on one corpus pass), OR converges to 1 on all corpora — tilings were never needed; J1 dies with it."

## Verdict

**KILLED — CONFIRMED on adjudication.**

## Fired criterion (verbatim)

"converges to 1 on all corpora — tilings were never needed; J1 dies with it."

## Adjudication history

The first KILLED verdict (2026-09-21, completion crew) rested on a selftest over a
640-byte SYNTHETIC corpus (k=1, no birth) plus an INFERENCE that real corpora have
weaker phase structure. The criterion says ALL corpora — a synthetic-only measurement
plus inference is not a measurement on all corpora. The verdict was placed under
adjudication and re-tested by direct measurement on the real corpora.

A second defect was found during adjudication (see "Rebirth-ban audit" below): the
as-built implementation made kill disjunct 1 (oscillation) unfireable by construction.
It was fixed, and both disjuncts were adjudicated on the fixed implementation too.

## Rebirth-ban audit (verified in source, not taken on word)

`cl/arm_minimal.zag`, `j2_birth_eval`, candidate eligibility (lines 208/213/218/223/228):

```zag
if(s.*.active[p]==0 && s.*.born[p]==0 && s.*.dead[p]==0){
```

All five candidate phases require never-born AND never-died. A phase that was ever
born or ever died can never be a birth candidate again — birth→death→birth for one
phase is impossible by construction. Additionally `nosc` (the oscillation counter)
has ZERO increment sites in the file (declared line 36, zeroed lines 86/93, never
touched). The as-built implementation therefore rigged survival on disjunct 1:
the kill criterion could never fire there regardless of evidence.

Per program law (an implementation that makes a kill criterion unfireable by
construction does not test the frozen criterion), the ban was removed in
`cl/birth_eval_fixed.zag`:
- Candidate eligibility is now dormant-only (`active[p]==0`); both the born-set and
  dead-set exclusions are removed (removing only the dead-set exclusion would not
  suffice — a reborn phase has `born[p]==1`).
- Rebirth (birth of a phase with `born[p]==1`) increments `nosc` and a per-phase
  rebirth counter `reb[p]`.
- The frozen death rule, absent entirely from the minimal build, was implemented:
  an active phase whose recall share of newline hits among active phases is <5%
  (50 permille) for two consecutive sweeps dies. (The "95% subsumption" clause is
  vacuous under exact-position evidence — hit sets are disjoint across phases —
  so recall-share is the operative rule.)
- The birth gate itself is UNCHANGED: best dormant of {0,16,32,48,24} must exceed
  best active by max(20 permille, 3·SE); one birth per sweep; K_max=5.

Disjunct 1 is now genuinely fireable — demonstrated on a synthetic oscillation
corpus (7 segments, A B B A B B A; A = newlines@phase24, B = newlines@phase0):

```
J2_BIRTH,phase=24,sw=0 | J2_DEATH,phase=24,sw=2 | J2_REBIRTH,phase=24,sw=3,nosc=1
J2_DEATH,phase=24,sw=5 | J2_REBIRTH,phase=24,sw=6,nosc=2
J2_RESULT_FIXED,osc_7seg,k_final=2,nbirth=3,ndeath=2,nosc=2,max_reb=2
```

birth→death→birth for phase 24, twice. The criterion is no longer rigged.

## Measured evidence (real corpora)

Corpora: `units/arms/harness/corpora/r1/prose.bin` (5,422,721 bytes,
sha256 a023115c…7fffb — matches MANIFEST) and `code.bin` (9,515,341 bytes,
sha256 b1dd5d74…1db28189 — matches MANIFEST).
Toolchain: `znc_linux_x86_64_abed8aa1` (frozen). All runs double-executed,
byte-identical stdout. Pure Zag, zero RNG.

### As-found implementation (`cl/birth_eval.zag`, whole corpus, 1 sweep)

| corpus | bytes | E0 (phase 0) | thresh | best dormant | E(best_d) | diff | born | k_final |
|---|---|---|---|---|---|---|---|---|
| prose.bin | 5,422,721 | 35 | 20 | 24 | 37 | +2 | none | 1 |
| code.bin | 9,515,341 | 28 | 20 | 16 | 28 | 0 | none | 1 |

Full candidate tables in `evidence/birth_eval_ORIG_{prose,code}_1sweep.txt`.
Per-phase newline rates sit at 27–37 permille with ≤2 permille differences —
two orders of magnitude below the 20 permille birth threshold. No tiling born.

### Fixed (unrigged) implementation (`cl/birth_eval_fixed.zag`)

| corpus | sweeps | k_final | nbirth | ndeath | nosc | max_reb |
|---|---|---|---|---|---|---|
| prose.bin | 1 | 1 | 0 | 0 | 0 | 0 |
| prose.bin | 4 | 1 | 0 | 0 | 0 | 0 |
| code.bin | 1 | 1 | 0 | 0 | 0 | 0 |
| code.bin | 4 | 1 | 0 | 0 | 0 | 0 |

No birth in any sweep of either corpus (best dormant never exceeds best active by
more than 2 permille vs the 20 permille bar). With nothing born, nothing dies,
nothing is reborn: `nosc=0` on both corpora.

### Gate reachability (mechanism not broken)

Synthetic corpus, newlines every 32 bytes aligned to dormant candidate phase 24
(`evidence/birth_eval_ORIG_synth32_p24.txt`, `evidence/birth_eval_FIXED_synth32_p24.txt`):

```
J2_BIRTH_EVAL,synth32_p24,k=1,E0=0,thresh=20,best_d=24
J2_BIRTH,phase=24
J2_RESULT,born=24,k_final=2,nbirth=1
```

The birth gate fires when the evidence genuinely favors a dormant phase
(E=1000 vs E0=0, diff 1000 > 20). The "never needed" verdict is about the real
corpora, not a broken gate. (The original selftest aligned newlines to phase 0 —
the already-active phase — guaranteeing a tie; that test could not have shown a
birth under any threshold.)

## Adjudication of the two disjuncts (fixed implementation, real corpora)

- **Disjunct 1** — "k does not converge (birth→death→birth for the same phase
  twice on one corpus pass)": `nosc=0`, `ndeath=0`, `nbirth=0` on both real
  corpora (1 and 4 sweeps). **Does not fire.** The mechanism is now capable of
  exhibiting oscillation (proven on the osc corpus), and the real corpora do not
  produce it.
- **Disjunct 2** — "converges to 1 on all corpora — tilings were never needed":
  `k_final=1` on prose.bin and code.bin, both implementations, all sweep counts.
  No tiling is ever born. **FIRES.**

## Verdict

**J2 is KILLED.** Disjunct 2 fires on measured evidence from the real corpora:
k converges to 1 everywhere; tilings were never needed. The 95%-subsumption death
rule is moot — nothing is ever born to die. The original death certificate stands;
its synthetic-only evidence defect is cured by the measurements above (see the
adjudication addendum in DEATH_CERTIFICATE.md).

**J1 dies with it** (per the binding criterion).

## M1–M9 1x row

| M | Status |
|---|--------|
| M1 | NOT RUN |
| M2 | NOT RUN |
| M3 | NOT RUN |
| M4 | NOT RUN |
| M5 | NOT RUN |
| M6 | NOT RUN |
| M7 | NOT RUN |
| M8 | NOT RUN |
| M9 | NOT RUN |

**Reason:** The kill criterion fired on the tiling mechanism itself; the full
2070-line `cl/arm.zag` never compiled under znc (struct limits, ZNC-2026-09-21-004).
The adjudication ran the frozen birth/death mechanism directly against the real
corpora instead. The battery is moot for a killed arm.

## 10x status

NOT RUN (arm killed at the mechanism level).

## Sources committed

- `cl/arm_minimal.zag` — as-found minimal implementation (unchanged)
- `cl/birth_eval.zag` — adjudication measurement driver (as-found birth logic + file input)
- `cl/birth_eval_fixed.zag` — fixed driver (rebirth allowed, nosc counted, death implemented)
- `evidence/` — 9 raw run logs (byte-identical double runs)
- `DEATH_CERTIFICATE.md` — stands, with adjudication addendum

## Notes

1. The rebirth ban was a completion-crew design choice, not part of the frozen
   mechanism ("Tilings as hypotheses: born on evidence, die by subsumption (95%)"
   says nothing about banning rebirth — and disjunct 1 presupposes rebirth is
   possible). Removing it restores the frozen mechanism; it does not change it.
2. The fixed implementation reproduces the as-found results exactly on the real
   corpora (k=1, no birth), so the fix changes nothing about the disjunct-2
   outcome — it only un-rigs disjunct 1.
3. Collision backup at `~/workspace/j2_collision_backup/arm.zag` (md5
   ae9c161b610e027eacfa65afc7118c73) was left untouched; it never compiled and
   is not evidence.
