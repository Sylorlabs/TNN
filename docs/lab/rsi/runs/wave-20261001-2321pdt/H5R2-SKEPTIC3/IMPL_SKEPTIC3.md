# H5R2-SKEPTIC3 Implementation Record

Lane H5R2-SKEPTIC3, wave-20261001-2321pdt. Implements the frozen prereg
PREREG_SKEPTIC3.md (freeze commit 6bf257048 on branch tnn-native-lab,
2026-10-02 ~07:34 UTC). Pure Zag, safebin toolchain, `which python3`
prints nothing (exit 1) at every check. Zero forbidden-executable
invocations.

## 1. Arms: extracted read-only, hash-verified, not rebuilt

- H5R2 substrate: extracted via git show from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (matches the frozen substrate hash; verified before use).
- NEWEST-LIVE-ON-KEY (bl_newest.zag): extracted via git show from
  f461e812d, SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649
  (matches the frozen skeptic hash; verified before use).

No working-tree file was used as a build input for either arm.

## 2. Separator fragment (SEP_FRAG.zag)

Written post-prereg to the frozen spec in PREREG_SKEPTIC3.md section
2: sep_fact_live_id (single live tag-1 fact on a key),
sep_two_live_old (SC-4: exactly two live tag-1 non-superseded facts
on K with objects c_old on the older id and c_new on the newer id;
emits TWOLIVE markers and returns the older id),
sep_fact_newer (the other live id), sep_probe (the re-teach event
sequence, SC-4 check, masked separator query flags=1, arm-neutral
SEP-check emitting SEP-OLD / SEP-NEW / SEP-DEP-FAIL / SEP-MAP-FAIL /
SEP-VAL-FAIL / SEP-MISS / SEP-AB-FAIL / SEP-TWOLIVE-FAIL),
sealed_main_s1 / sealed_main_s2 with the frozen seeds, key ranges,
and object values (s1 vo=2, s2 vo=6).

One fix during implementation (pre-commit, smoke-caught): the first
draft carried a leftover pn parameter on sep_probe; znc reported an
arity error at compile time. The pn parameter was removed (the tag
already identifies the probe); the fragment then compiled with exit
0 and only the pre-existing A0102 warnings shared by the substrate.

SHA-256 of SEP_FRAG.zag:
65875ee5ea47dbb0866e9611204739c3d8b3c494f84e1f93d84a1327221447c2

## 3. Pre-sealed smoke verification (in /tmp, discarded, not committed)

Assembled smoke worlds per the frozen 7.1 rule on world s1 for both
arms and ran each twice:

- H5R2: 4/4 "SEP-TWOLIVE ok", 4/4 "SEP ok", 4/4 "SEP-OLD"
  (v = c_old on every probe), DONE-OK. White-box: live MAP DEP
  edges to the a-link fact and to F_old (the older live fact on K,
  e.g. S1P1 dep->2 o=91301 and dep->3 o=91403).
- NEWEST-LIVE-ON-KEY: 4/4 "SEP-TWOLIVE ok", 4/4 "SEP ok", 4/4
  "SEP-NEW" (v = c_new on every probe), DONE-OK. White-box: live MAP
  DEP edges to the a-link fact and to F_new (the newest live fact on
  K, e.g. S1P1 dep->2 o=91301 and dep->4 o=91404).
- Both arms byte-identical across the two smoke runs (full-stdout
  SHA-256 stable).

The smoke assemblies are discarded. The sealed evaluation
re-assembles all worlds from the committed sources per PREREG 7.1.

## 4. Deviations from the prereg

None, except the arity fix above (caught by the compiler before any
sealed assembly; the frozen spec is unchanged). Ordering: prereg
freeze commit 6bf257048 strictly precedes this implementation commit.
