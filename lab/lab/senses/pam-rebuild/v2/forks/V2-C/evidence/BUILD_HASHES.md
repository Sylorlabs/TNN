# Build hashes — V2-C pure-Zag battery

**Date:** 2026-09-24
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned). Imports resolved with cwd=buildsrc (znc resolves `@import`
  relative to cwd).
**Sources:** fetched from branch `tnn-native-lab` via GitHub API
  (`senses/pam-rebuild/v2/forks/V2-C/src/`). `vsense_c_zag.zag` verified
  byte-identical to Crew A's local `build/src/vsense_c.zag` (`cmp` clean);
  `memgate.zag` SHA matches the R2-4 byte-identical value in the frozen
  amendment (f7fa8db127b0def8f481c66b86f78b719ae26b4d0a6e549a9f82fc15566e9774).

## Source SHAs (branch-committed)

| File | SHA256 |
|------|--------|
| vsense_c_zag.zag | 59c8bf4aa7625c8a0e6f6d1e5a82ef3d325cc74e48ff55572d4b5564f78f00a3 |
| vknow.zag | 5bd506be9942737f322ec906fc34af842fa30d724e5a6d2e791d3942e7c67372 |
| vknow_structural.zag | 4840bb4ad5f66c42e5157e24ca78cba5bee22ea90660826c764fa91c8c0b4471 |
| memgate.zag | f7fa8db127b0def8f481c66b86f78b719ae26b4d0a6e549a9f82fc15566e9774 |
| lut.zag (R2-4) | 9379d9880fd47a47557a0e619ba56d256d7a6e1f47e5584deba434f1db46a006 |
| gcheck.zag (R2-4) | 8cae32a86a3c4dbfe93026beb26d6361e37470b6eb3112fbd277ae3efb58b51b |
| deliberate.zag (R2-4) | 63228c648f4a87a37c7beeb5eb30f828d21b97663b6e1f47e5584deba434f1db46a006 |
| CALIBRATION_C_ZAG.md | 535021e05eae889a651a2176eeb0af6bea28df9c9deb1111edb6de55db2ed496 |

## Binary SHAs (reused for all 3 runs)

| Binary | SHA256 |
|--------|--------|
| bin/vsense_c | d6d0bc95404ac55887c3f9a540d7db0e466650624bcc1de16f4660ffd1e897c1 |
| bin/deliberate | ab185ba2d13a31c6afdecc3409f71801df37af32f69d04304774eaea234a144d |
| bin/memgate | 0314033408d2fbf121db72595c6d8d02f50a29a279b2fa9839e5e104e2e40040 |

dmask=4095 for all runs. Binaries are NOT committed (per lab rule).
