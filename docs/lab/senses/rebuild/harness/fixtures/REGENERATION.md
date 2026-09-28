# Fixture regeneration

The 1850 fixtures + 925 truth files + 170 photos are NOT stored in this
commit (42MB). They are byte-regenerable:

1. Photos: download per `../FIXTURE_SOURCES.md` URLs into
   `harness/fixtures/_photos/` as ph000.jpg ... (170 files).
2. Run `harness/gen.py` (fixed master seed 20260921, deterministic
   splitmix64 noise) from `harness/`.

Verify with: `cd harness/fixtures && sha256sum -c MANIFEST.sha256`
(all 2020 entries must report OK).
