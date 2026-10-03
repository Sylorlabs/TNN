# PREREG — Principle Detection (Micah's question, 2026-09-21)

**Frozen:** 2026-09-21. No changes after this point without a dated amendment.

## Question

"If TNN knows the principles of the domain and gets told the lied fact, does it
figure it out using those principles?" This is NOT claim-vs-claim (done: 156/156
in new-mechanisms). This is **derivation**: the learner holds a general principle
(∀x∈C: P(x)=E), receives ONE specific fact about a member of C that violates it,
and must derive the conflict from the principle itself — with no second claim
present.

## Design

Pure Zag, zero RNG. Principles are taught first as (class, property, expected,
confidence). Class hierarchy is walked most-specific-first (universal
instantiation). Facts arrive one at a time; the learner derives the expected
value and compares.

Two architectures, head-to-head. Both SHARE the derivation step
(find_principle: walk class chain, instantiate ∀x∈C). They differ ONLY in the
decision procedure:

- **Arch A — derive-check (explicit inference):** derivation → direct verdict.
  Match → ACCEPT. Mismatch + known exemption → ACCEPT+REFINE (fact installed,
  refinement logged). Mismatch + no exemption → WITHHOLD (not installed).
  Confidence-blind.
- **Arch B — materialize + arbitrate:** derivation → materialize the implied
  claim (subject, property, expected; trust = principle confidence) → trust
  arbitration vs the taught claim (trust 50). Implied wins → WITHHOLD. Taught
  wins → ACCEPT. Exemption → taught wins + REFINE. Confidence-sensitive.

Honesty clause (preregistered): if B is just claim-vs-claim in disguise with no
genuine derivation doing work, the verdict must say so. Note both architectures
share the instantiation step — the experiment isolates the DECISION procedure,
not whether instantiation happens.

## Verdict codes

- `0` ACCEPT — consistent with principles, installed.
- `1` WITHHOLD — violates a principle, NOT installed.
- `2` ACCEPT+REFINE — true exception: installed AND refinement logged
  (principle scope exception recorded; principles are NOT rewritten in-run —
  refinement is logged only; deliberate principle revision is future work).
- `3` ACCEPT-NOSCOPE — no applicable principle; installed without check.

## Frozen battery

Classes (id: name, parent): 0 ROOT; 1 MAMMAL(0); 2 MONOTREME(1); 3 BIRD(0);
4 FISH(0); 5 REPTILE(0); 6 WATER(0); 7 ICE(0); 8 IRON(0); 9 WOOD(0);
10 MERCURY(0); 12 PLANET(0); 11 EARTH(12); 13 MARS(12); 14 VENUS(12);
15 MOON(0); 16 ICY_MOON(0).

Subjects (id: name, class): 100 dolphin(1); 101 platypus(2); 102 echidna(2);
103 bat(1); 104 blue_whale(1); 105 eagle(3); 106 ostrich(3); 107 penguin(3);
108 shark(4); 109 cobra(5); 110 water_sample(6); 111 ice_cube(7);
112 iron_nail(8); 113 oak_plank(9); 114 mercury_sample(10);
115 everest_water(6); 116 earth(11); 117 mars(13); 118 moon(15);
119 venus(14); 120 europa(16); 121 salmon(4).

Properties: 1 reproduction (1=LIVE_BIRTH, 2=EGGS); 2 milk (1/0);
3 breathes (1=AIR, 2=GILLS); 4 feathers (1/0); 5 boiling_point (°C int);
6 floats (1/0); 7 sinks (1/0); 8 human_walked (1/0); 9 orbits_sun (1/0);
10 orbits_earth (1/0); 11 rotation (1=PROGRADE, 2=RETROGRADE).

Principles (id: class, property, expected, confidence):
P1 (1,1,LIVE_BIRTH,100); P2 (3,1,EGGS,100); P3 (4,1,EGGS,100);
P4 (5,1,EGGS,100); P5 (1,2,YES,100); P6 (3,2,NO,100); P7 (1,3,AIR,100);
P8 (4,3,GILLS,100); P9 (3,4,YES,100); P10 (6,5,100,100);
P11 (7,6,YES,100); P12 (8,7,YES,100); P13 (9,7,NO,100);
P14 (12,11,PROGRADE,100); P15 (13,8,NO,100); P16 (11,9,YES,100);
P17 (15,10,YES,100); P18 (13,9,YES,100); P19 (5,2,NO,40) [weak, probes only].

Exemptions (principle, subject): (P1,101); (P1,102); (P10,115); (P14,119).

### Scored facts (43)

| Fid | Subject | Property | Value | Ground truth | Expected |
|---|---|---|---|---|---|
| F1 | dolphin | reproduction | LIVE_BIRTH | true | 0 |
| F2 | bat | reproduction | LIVE_BIRTH | true | 0 |
| F3 | blue_whale | reproduction | LIVE_BIRTH | true | 0 |
| F4 | eagle | reproduction | EGGS | true | 0 |
| F5 | ostrich | reproduction | EGGS | true | 0 |
| F6 | penguin | reproduction | EGGS | true | 0 |
| F7 | salmon | reproduction | EGGS | true | 0 |
| F8 | cobra | reproduction | EGGS | true | 0 |
| F9 | platypus | milk | YES | true | 0 |
| F10 | echidna | milk | YES | true | 0 |
| F11 | dolphin | breathes | AIR | true | 0 |
| F12 | shark | breathes | GILLS | true | 0 |
| F13 | eagle | feathers | YES | true | 0 |
| F14 | eagle | milk | NO | true | 0 |
| F15 | dolphin | reproduction | EGGS | FALSE | 1 |
| F16 | bat | reproduction | EGGS | FALSE | 1 |
| F17 | eagle | milk | YES | FALSE | 1 |
| F18 | shark | breathes | AIR | FALSE | 1 |
| F19 | penguin | feathers | NO | FALSE | 1 |
| F20 | platypus | reproduction | EGGS | TRUE exception | 2 |
| F21 | echidna | reproduction | EGGS | TRUE exception | 2 |
| F22 | water_sample | boiling_point | 100 | true | 0 |
| F23 | ice_cube | floats | YES | true | 0 |
| F24 | iron_nail | sinks | YES | true | 0 |
| F25 | oak_plank | sinks | NO | true | 0 |
| F26 | water_sample | boiling_point | 90 | FALSE | 1 |
| F27 | ice_cube | floats | NO | FALSE | 1 |
| F28 | iron_nail | sinks | NO | FALSE | 1 |
| F29 | oak_plank | sinks | YES | FALSE | 1 |
| F30 | everest_water | boiling_point | 71 | TRUE exception | 2 |
| F31 | mercury_sample | boiling_point | 357 | true, no principle | 3 |
| F32 | mars | human_walked | NO | true | 0 |
| F33 | earth | orbits_sun | YES | true | 0 |
| F34 | moon | orbits_earth | YES | true | 0 |
| F35 | mars | orbits_sun | YES | true | 0 |
| F36 | mars | human_walked | YES | FALSE | 1 |
| F37 | earth | orbits_sun | NO | FALSE | 1 |
| F38 | moon | orbits_earth | NO | FALSE | 1 |
| F39 | earth | rotation | PROGRADE | true | 0 |
| F40 | mars | rotation | PROGRADE | true | 0 |
| F41 | venus | rotation | RETROGRADE | TRUE exception | 2 |
| F42 | mars | rotation | RETROGRADE | FALSE | 1 |
| F43 | europa | orbits_earth | NO | true, no principle | 3 |

Violations (expected 1): 13 (F15–F19, F26–F29, F36–F38, F42).
Exceptions (expected 2): 4 (F20, F21, F30, F41).
Consistent (expected 0): 24. No-scope (expected 3): 2.

### Unscored probes (2, measured only — weak principle P19, conf 40)

- F44 cobra milk NO (true) — derivation fires on weak principle; both arches
  should ACCEPT (A by rule-match, B by match — no conflict either way).
- F45 cobra milk YES (FALSE) — A: WITHHOLD (confidence-blind rule).
  B: implied trust 40 < teacher 50 → taught wins → ACCEPT (detection miss).
  Preregistered as the architectural divergence probe.

## Kill bars

- **KB-PD-DET:** detection (correct WITHHOLD / 13 violations) < 90% → FAIL.
- **KB-PD-FA:** false alarms (consistent or no-scope items flagged or withheld,
  plus true exceptions blindly rejected) / 26 non-violation non-exception items
  > 5% (>1 item) → FAIL.
- **KB-PD-DET2:** any byte difference across 5 repetitions of either arch → FAIL.
- **KB-PD-HONEST:** if analysis shows no genuine derivation step (e.g., verdicts
  achievable by claim-vs-claim matching alone), the verdict must state it
  explicitly rather than claim a new capability.

## Metrics (reported, not kill)

- Refinement rate: correct ACCEPT+REFINE / 4 exceptions.
- A-vs-B decision agreement on scored items; divergence analysis on probes.
- Cost: ops per fact per arch.

## Notes

- Principles are stipulated installed background (simplified domain models);
  every battery truth value above is real-world true/false as of 2026.
- Refinement is logged, not applied: deliberate principle revision is future work.
- No randomness anywhere; reps must be byte-identical.
