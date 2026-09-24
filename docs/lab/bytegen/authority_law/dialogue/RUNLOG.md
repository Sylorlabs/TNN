# RUNLOG — dialogue plan-absolute instantiation

Date: 2026-09-24. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Source: `dialogue_plan_absolute.zag` (pure Zag, zero RNG). Full output: `dialogue_evidence.txt`.

## Build
- `znc dialogue_plan_absolute.zag -o dialogue_bin` — clean build, no errors
  (one A0102 lint fixed; zero warnings at ship).

## Probes (all PASS)

| Probe | Result |
|---|---|
| B1 learning-from-own-output | kb_write_rc=1 (KB_FROZEN), uc SELF-install rc=2 (refused), 8/8 forbidden ports refused, installs=0, uc_n=0 |
| B2 repeat-bias | 3 repeats winner=2,2,2, score vectors byte-identical; exact-tie query: last_fid=0→fid0, last_fid=3→fid3, scores byte-identical across both |
| VETO | clean turn veto=0; uc-override veto=1 (code 1 SRC_NOT_KB); subtle source-lie veto=1 (code 3); stale-fid veto=1 (code 2); recompose == direct-from-corrected-plan byte-identical (SHA `8d4e9d6a…b321` both); phrasing-A == phrasing-B re-composition (constant map) |
| RERUN | 8-turn mixed session ×3: SHA `72448e50…f17498ea` ×3, byte-identical |

## Notes
- Constructed-mode (`joke:`/`imagine:`) turns touch no store and never enter the checker.
- The checker never edits/blends: veto → `recompose_plan_pure` only.
- Frozen battery not run (needs Micah's signature; sibling crew drafting).
