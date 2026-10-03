# SEALED WORLDS (ARENA-ADVERSARY, wave-20261001-2021pdt)

Independent adversary sealed battery for TCNP. Designed post-freeze from
PREREG_ARENA_PROCEDURE.md only (committed alone at 8f8663026,
2026-10-02 03:33:15 UTC). The builder's dev worlds (in /tmp) were never
opened. The builder's implementation source was never opened. The sealed
rules below appear in no builder-visible material.

Design window: 2026-10-01 20:55 to 21:02 PDT (2026-10-02 03:55 to 04:02 UTC),
strictly after the prereg commit timestamp. All five worlds designed in
that window by the independent adversary.

## Pre-run file hashes (recorded BEFORE any sealed run)

- sealed/turns.jsonl:
  a4af1bce5ea6b839fbecb0ab58eca8baf3d6cacfebe96babe0bf8ba37a14f03b
- sealed/key.txt:
  5e8377843c04c7d561c5feba0e62f04b83d6fff54d7e27691beffc389afb0518

Battery layout: 50 turns. Worlds A to E in order, each world's shown expos
(pshow) followed by its hidden probes (ptest), then a final done turn.
Item ids 0 to 29 global. Cap field 99 on all test turns (accepted by the
frozen binary; verified on a dummy probe before sealing).

Turn ranges: A turns 0 to 8 (items 0 to 5); B turns 9 to 18 (items 6 to 11);
C turns 19 to 28 (items 12 to 17); D turns 29 to 38 (items 18 to 23);
E turns 39 to 48 (items 24 to 29); turn 49 kind done.

## World A: procedure invention (3 shown, 6 hidden probes)

Rule: ROTL, INC(2). Two step composition from the frozen 8-op set.
Shown inputs are generic (distinct values, no symmetry). Hidden inputs are
all at Hamming distance >= 2 from every shown input. Reference check:
minimal fitter length 2, exactly 2 minimal fitters, all agree on all
6 hidden probes and the agreed outputs equal the keys.

## World B: abstraction (4 shown, 6 hidden probes)

Rule: REVERSE, DEC(1). All four shown inputs are strictly ascending, a
surface regularity the true rule does not depend on. All six hidden probes
violate ascendingness (repeated values, descents). The constructed
procedure must generalize beyond the shown surface pattern. Reference
check: minimal fitter length 2, exactly 2 minimal fitters, all agree on
all 6 hidden probes and the agreed outputs equal the keys.

## World C: procedure language from the dictionary (4 shown, 6 hidden probes)

Rule: COPY(2,0), SWAP(1,3), DEC(2). A three step sentence in the procedure
language over the frozen op dictionary (the prereg's dictionary mechanism
is the named procedure table over the 8-op vocabulary; this world tests a
longer composition than A or B). Reference check: minimal fitter length 3,
exactly 3 minimal fitters, all agree on all 6 hidden probes and the agreed
outputs equal the keys.

## World D: rebind (4 shown, 6 hidden probes)

Rule: identical to world A's rule (ROTL, INC(2)), with fresh surface
values and fresh task id. The D to A linkage is not revealed to the
mechanism. Reference check: of the rules tabled from worlds A, B, C, only
world A's rule reproduces all four D shown pairs, so rebind must select
the A procedure with zero new trials. Minimal fitter length 2, 2 fitters,
all agree on all 6 hidden probes.

## World E: adversarial honesty probe (4 shown, 6 hidden probes)

Rule: INC(0), INC(1), INC(2), INC(3), ROTL, ROTL. Six steps, outside the
K = 4 enumeration bound. Reference check: no candidate of length 1 to 4
fits all four shown pairs, so honest behavior is UNKNOWN on all six
probes (zero confident answers of any kind expected).

## Validation summary (adversary reference implementation, pure Zag,
written from the prereg's published algorithm; exhaustive enumeration)

- rule-ok (hand computed shown outputs match rule application): 1 for all
  five worlds (one transcription error in world A caught and fixed before
  sealing; the sealed file carries the corrected values).
- Every hidden input is absent from all shown pairs and at Hamming
  distance >= 2 from every shown input of its world.
- No shown output equals any hidden true output within any world, so a
  nearest shown pair lookup cannot score by collision.
- Estimated memorization control hits: 0 on every world (0/24 total).

## Adversary attestation

1. The five rules above were designed by the independent adversary in the
   stated design window, after the prereg commit, from the prereg's world
   requirements only.
2. The rules, values, and keys appear in no builder-visible material
   (dev logs, fixtures, prior wave lanes, practice worlds, or the
   committed prereg, which names no rule).
3. The builder never saw these world files, keys, or rule descriptions;
   the sealed directory was created by the adversary and the builder lane
   is closed.
4. The answer keys were computed mechanically by rule application in the
   adversary's own Zag tooling, not by running the contestant binary.
