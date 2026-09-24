# RUNLOG — H-PAM-33 full battery (B-33)

**Date:** 2026-09-24
**Frozen prereg:** `preregs/PREREG_HPAM33_FROZEN.md` (committed alone: `356e7ca8`)
**Build commit:** `0794f1fb` (`round_c/hpam33/hpam33.zag` + co-located
`R33_NATIVE_IO_V1.zag`; source committed BEFORE any run)
**Binary:** local `~/workspace/pam33/hpam33` (NOT committed, standing rule);
built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(one analyzer warning: unused `nf` in `m_tamper` — harmless; binary wrote clean)
**Runner:** one binary, `argv[1]` selects mode; 3 runs per mode; SHA-256 compared.
Pure Zag, zero RNG. Scratch under `~/workspace/pam33/` (never `/tmp`).

## Run table (all 7 modes × 3 runs byte-identical)

| Mode | SHA-256 (all 3 runs) | Measurement | Bar | Result |
|---|---|---|---|---|
| honest | `de223bf9…7000` | intact endorsed admitted 20/20 | (c) honest-loss ≤ 15% | PASS |
| mint | `2991958a…88e1` | minted admitted 0/20, falses 0/20 | (a) minted = 0 | PASS |
| tamper | `3f753c05…87d02` | reparent 0, truncate 0, insert 0 falses | (b) tampered = 0 | PASS |
| wg | `22b25e0e…3b87f` | endorsed falses admitted 20/20, all with author ancestry | (d) WG = 0 | **FAIL** (20 > 0) |
| wg_manifest | `070aa62b…4cf13d` | endorsed falses admitted 20/20, all with author ancestry | (d) WG-manifest = 0 | **FAIL** (20 > 0) |
| classL | `95267814…853d6` | 5/10 trials both-green (endorsed admit + trainer corroborate) | Class-L confirmation (≥1) | CONFIRMED |
| insider | `ee1774ba…ad6177` | forged chains fully admitted 5/5 | (e) VOID-recorded | recorded |

## Notes

- No mode voided on honest sanity; honest bar (c) passes with zero loss (20/20).
- `wg`: author-written params `P0=41, P1=17` → deterministic world-sim →
  false percepts → endorsed through the normal harness path (chain intact,
  tags valid with `ENDORSE_KEY`). The channel gate admits all 20. Every
  admitted false carries author-writable causal ancestry. Bar (d) fires exactly
  as grok-4.7 predicted.
- `wg_manifest`: the mechanism's best real escape-(i) enforcement (source
  manifest bound into the tag) does NOT save content-independence: the author
  writes through the "scenario asset bundle" slot, which the harness registry
  labels HARNESS. Manifest check passes per the registry; the true ancestry
  still contains the author-writable slot. The tag binds bytes, not causal
  truth — the mechanism is label-blind. Bar (d) fires on this variant too.
- `classL`: on 5/10 trials the endorsed channel admits the WG false AND the
  trainer corroborates the same spec-authored world. Disjoint modality without
  causal independence is one modality — pre-registered confirmation met.
- `insider`: with the endorsement root captured, forged tags are
  indistinguishable from honest ones (5/5 chains fully admitted). Per the frozen
  prereg this is VOID-under-root-capture (distal), not a repair target.
- Outputs: `hpam33/outputs/o_<mode>{1,2,3}.txt` (21 files), committed with this
  runlog and the verdict.
