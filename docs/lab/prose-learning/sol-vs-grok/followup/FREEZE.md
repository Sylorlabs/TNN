# BUILD FREEZE — Sol-vs-Grok follow-ups (FROZEN 2026-09-22)

Sources frozen as committed. No source changes after this point except
crash fixes (documented, rebuilt, full rerun). Sealed battery
(`followup/gen/followup/`) generated after this freeze; builders do not
inspect it before scoring.

## Toolchain

`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Built with cwd=`followup/src` (@import resolves relative to cwd).
Only warning: analyzer A0101 off-by-one note (`k2 <= N` with indexing) —
the same known-benign warning the duel builds carried; no new warnings
(KB-F-TOOL satisfied).

## Frozen binary SHA256 (built 2026-09-22 from the committed sources)

- sg_verify: be9d5b8bbaffcec828a089da70b3c3b5c86c7d0bab83f52785395bd345b83ded
- sg_coref1: 17b4ee1ef2a8996dc0699d262fdfeee3b1c4fb7e1ea0169e9a81f5265c76dde1
- sg_coref2: a9d1c9b333cdb88d82dd1214e625b07a3fc83e16693126388a37f4356a85f0d9
- sg_gated: e208302fd85fe67640cac688d971c227666b0dcc219e14e2dc1b0a8eb3608d6a
- sg_sol (duel frozen source rebuild): 67729f4885649fa65302444c8f42a2da0e61b643b3ced30ce118f6d17b930334
- sg_grok (duel frozen source rebuild): 9d3682be29c483d59c3cf605abefe85e5c766c77e43f833c203c6c6e507ddc62

## Calibration (visible calib battery — sanity only, not evidence)

| build | SG-PARA | SG-SAFE | SG-PREC | SG-COMP | SG-WRONG |
|---|---|---|---|---|---|
| sol | 0.5000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| grok | 0.9583 | 0.9167 | 0.8490 | 0.1667 | 0.2315 |
| verify | 0.8958 | 1.0000 | 1.0000 | 0.1667 | 0.0000 |
| coref1 | 0.9583 | 0.9167 | 0.9010 | 1.0000 | 0.1852 |
| coref2 | 0.9583 | 0.9167 | 0.9010 | 1.0000 | 0.1852 |
| gated | 0.9583 | 1.0000 | 0.9744 | 1.0000 | 0.0185 |

Veto/gate distributions on calib match design: verify attestation=48
(neg+hedge), subject=44, tie=20; gated attestation=48, subject-excluded=20.

Determinism: rerun of sg_gated byte-identical (stdout + proof SHA256 match).
The 5-run byte-identical protocol runs on the sealed battery.

## FROZEN 2026-09-22.
