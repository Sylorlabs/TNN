# IMPLEMENTATION.md: Battery v2 (wave-20261001-2021pdt, lane BATTERY)

Worker: BATTERY-IMPL. Toolchain: safebin, `which python3` prints nothing,
pinned znc 2026.07.0-dev. Pure Zag for all research logic. No commits by
worker; coordinator commits. No em-dashes in documentation.

## 1. Prereg ordering (K-S1v2)

- Prereg commit d43fe32c5 (HEAD at implementation start), committed alone.
  SHA-256 of PREREG_BATTERY_V2.md:
  `ef0f2e6e7ba651a1d2f7d3d6e5dac69d9523bacff5b1e61a1ce75807348e3bf0`.
- Filesystem mtime order: prereg (1790912165) < world files and envelopes
  (1790912793) < WORLD_MANIFEST_V2.sha256 (1790912800).
- Implementation files first appear in the working tree after d43fe32c5.
  Commit-order self-check: PASS.

## 2. Generated artifacts (v2_worldgen.zag, seed 20261001)

World files (exact prereg section 3 streams), template, 3 sealed envelopes:

- m1w1v2_world.txt (600 B), m1w2v2_world.txt (348 B), m1w3v2_world.txt (378 B)
- m2w1v2_template.txt (78 B): 3 bias OBSERVEs
- m2w2v2_world.txt (340 B), m2w3v2_world.txt (340 B)
- m3w1v2_world.txt (1164 B), m3w2v2_world.txt (404 B), m3w3v2_world.txt (380 B)
- m2w1v2_envelope_run1.txt: PI 1 3 2 (1->A, 2->C, 3->B)
- m2w1v2_envelope_run2.txt: PI 1 2 3 (1->A, 2->B, 3->C)
- m2w1v2_envelope_run3.txt: PI 3 2 1 (1->C, 2->B, 3->A)

Permutations from LCG seed 20261001 + Fisher-Yates, deduped; all distinct.
Envelope hashes committed in WORLD_MANIFEST_V2.sha256 BEFORE any run
(manifest written 2026-10-02 03:46:40 UTC; first shim execution after).
Manifest verified with `sha256sum -c` before and after the battery: all OK.

Id sets: v2 uses 40000-49999, disjoint by sub-block (M1 40000-41999,
M3 42000-43999, M2 44000-46999). Numeric reuse across v1/v2 noted:
45101-45104 and 45111-45114 appear in both batteries but in different
roles (v1: objects/truths; v2: subjects/keys); harmless per prereg
section 2 (fresh state per block; K-S15v2 audits within v2 only).

## 3. Tool binaries (all pure Zag, pinned znc)

- v2_worldgen_bin (from v2_worldgen.zag)
- v2_sealed_score_bin (from v2_sealed_score.zag)
- v2_score_m2w1_bin (from v2_score_m2w1.zag)
- v2_inspect_state_bin (from v2_inspect_state.zag)
- v2_struct_check_bin (from v2_struct_check.zag)
- v2_m2w1_driver_bin (from v2_m2w1_driver.zag) + run_m2w1.sh (mechanical loop)
- v2_controls_bin (from v2_controls.zag)
- v2_audit_noleak_bin (from v2_audit_noleak.zag)

SHA-256 of sources and binaries recorded below (section 7).

Determinism: worldgen re-run byte-identical; all 8 fixed worlds
byte-identical across 3/3 block runs; M2-W1 per-run re-execution with its
envelope reproduces byte-identically (K-S2v2 PASS).

## 4. Frozen artifacts (K-S3v2)

- freeze_shim2_bin:
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  verified before each block run and after the battery.
- tnn2.zag:
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified after the battery.
- znc_linux_x86_64_abed8aa1:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- git status shows no modifications under frozen cognition paths.

## 5. Anti-smuggling (K-S4v2)

181 unique ids in 40000-49999 extracted from v2 world files; grep over
frozen tnn2.zag and freeze_shim2.zag finds zero matches. The benign 41024
constant is not in any v2 world id set. K-S4v2 PASS.

## 6. Deviations from prereg (implementation notes)

1. v2_sealed_score.zag accepts an optional third argv `BAR=<spec>` for
   world-specific bar checks and distractor verification. The specified
   two-arg form works for generic scoring; the third arg is a strict
   superset used by the driver. All bar parameters are prereg-fixed.
2. v2_inspect_state.zag takes argv [state.bin, worldfile]; the worldfile
   supplies the OBSERVE stream for (s,r,o) evidence matching, as required
   by the prereg's "source observation facts from the world's OBSERVE
   stream" semantics. Run on the final block state per prereg 5.2.
3. The M2-W1 interactive driver is split: v2_m2w1_driver.zag (all routing
   logic; step-indexed pure function of envelope+step+last_choice) plus a
   thin mechanical shell loop (run_m2w1.sh) that appends lines, invokes the
   frozen shim on snippets, and plumbs CHOICE values. Shell makes no
   routing decisions.
4. v2_struct_check.zag implements the K-S5v2(c)/K-S11v2(d) checks against
   inspector reports (the prereg names the inspector; the check itself is
   the bar logic).
5. v2_audit_noleak.zag implements K-S15v2; "novel-key" is interpreted as
   subject-novel (never observed as a subject in any v2 world), so that
   legitimate retention probes are not flagged as leaks.

## 7. File hashes (sources and binaries)

(Recorded for the coordinator's commit.)

```
9954282079114e98766265c69a18e626946acb01fe95021d34a4d37d0a995a34  v2_worldgen.zag
8f5bc00091ca1b3cddde18533aa5da3e97efc87c3bff830ac822a1d6ecc03bd1  v2_worldgen_bin
5f4fcc697bceacce66ec2be6d41a271ce94fcb6ff0bb973bd1895fbc53214075  v2_sealed_score.zag
e6c74bcd3b58072050c719376533575ef2e6aadf994414e2b4fdea289b3823e2  v2_sealed_score_bin
d65424df834df998b775b9ae36c87bb35048c4f99e847432eddb37af162c9b3e  v2_score_m2w1.zag
043d05550372cbc0b3cb43828514d86767d64e2727f265bc38683fa7d617b408  v2_score_m2w1_bin
3acd7119c5745525639bbb9b4eadcac93b4545c459371e1c17ab601d805c2dc1  v2_inspect_state.zag
ed6701b55f2375665e1fb50cbf1a144997ca2e0ee6b804ff495393fa7899ab65  v2_inspect_state_bin
5d85d30fa84838b6192b1ab05e229a83e0aa3e6ca6bf81a617b2b71415d94ab7  v2_struct_check.zag
1c4adb64e4020df509714a7b1006efdcb3e40189f19fcb65549922f67d0a8a1f  v2_struct_check_bin
fb3012538ac8a6dfe8b838d98b680f60734e107872d510e0256c106786da842a  v2_m2w1_driver.zag
f021676f8daca89eae72a08cee5dd4246525a6a6b077301bcd0fdaa7163cdaff  v2_m2w1_driver_bin
ffb1246ed1141c2b69549d0dedfe9b62aff4ec5acb4173b362c8153273cc148b  v2_controls.zag
b0dc2011112c4a8196bc808b4a215f8e93dd25259cebf48aa366131b44c66948  v2_controls_bin
699254b33759d64ceaf721c91d8818d408f534418e78b18985763195ca969d7b  v2_audit_noleak.zag
72f5c6969b3df10f4c4e70f39d8ed9834c29bd5d6eb519916346cb4f101f79b7  v2_audit_noleak_bin
```
