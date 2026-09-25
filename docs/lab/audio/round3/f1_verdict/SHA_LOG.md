# F1 Source/Plan/Render SHA Log
Date: 2026-09-25

## Sources
vowel_real.wav: 8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d
kidb.wav: 13285a0da02de5a830e289924ba4c9e5b831ac86bbd7de0002f033d7046682a3

## Plan
plan.bin: 1551226008b2f3ebd106926c34fd05a8ffade6ef8aa0d85313f66231f189de86
plan.txt: (see file; key values: fossil 0-392/785 marks, donor kidb 2573-2618, CV 1.2424008155672617%, F0 493.71903047640404 Hz, unique 1.0, reuse 1, G=1.0)

## Renderer
epochgraft.zag: afdb8c9afa8f60c0d0f268f4d5ffe80f980d08a1615432930bfd554a708d958c
epochgraft (binary): ebeca0f6402233d78a40c830b8d6b8b7a6e1dcc04527e7979e77e41fefb11b1b
Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Renders (3x byte-identical verified)
f1_a.wav: 14c7f43f40b51ec8ab2f12f521798bc704314b0e2e95f9b5c4e46e037905008f
f1_b.wav: 3bea9096bc24632d76319193e6eb3e68ffce137b251f57afc4a511fc5dddf630
f1_c.wav: 32150962a1ea0f9fcffe7ed9211f371c74e048687260a0bcffda765aef702f36
f1_freeze.wav: dfdce5d8e8ca985e824193b721f6286085009a9459fd1dff3543772fe30065d4
f1_control.wav: 43ded64586e705085c675d0df32bb35607cc300df8fbeba4e57b6ecb24059fad

Rerender verification (2026-09-25):
- a: 3x IDENTICAL (14c7f43f40b51ec8ab2f12f521798bc704314b0e2e95f9b5c4e46e037905008f)
- b: 3x IDENTICAL (3bea9096bc24632d76319193e6eb3e68ffce137b251f57afc4a511fc5dddf630)
- c: 3x IDENTICAL (32150962a1ea0f9fcffe7ed9211f371c74e048687260a0bcffda765aef702f36)
- freeze: 3x IDENTICAL (dfdce5d8e8ca985e824193b721f6286085009a9459fd1dff3543772fe30065d4)

## Provenance
prov_a.txt: de0e5f5eeaef72830379d6c152dfc3e2a002f7703c3536f1da23eb64b80d8c41
prov_b.txt: 4a1a3aae34304cd91c4486bb2d744bbd11ea44505a47b7a25032b1c82d04e48b
prov_c.txt: e97eb4adf51efbb99084eb221710220da3733ab648b5f1959a570effe59cb8bb
prov_freeze.txt: 072fa7aa39e09e511dc919fc0b847eadb6f785ee40e6d39d72fbc9a87c7c5430
prov_control.txt: 1068727d7bb9e053cc91539b97407630c3db659a74008ee52295ee415864b14c

## Zero-source test
All variants produce bit-exact zero output from zero PCM input:
- a: nonzero=0, sha=3c8a8c0591204fe6
- b: nonzero=0, sha=ad06548d002ee4f9
- c: nonzero=0, sha=92eb2434b679b653
- freeze: nonzero=0, sha=3c8a8c0591204fe6
