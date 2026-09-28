# W12 runlog — 2026-09-24

## Fixtures (frozen, inherited; byte-identical re-verified before build)
- `wild/w12/w12_stream.txt`: 1132 rows (1102 C in tape order + 30 wrong-set
  rows flagged `|1`), `wild/w12/w12_attack.txt`: 628 rows (500 junk + 1
  high-price true target at stream idx 500 + 127 trues).
- Generator `wild/w12/gen_budget.py` rerun -> byte-identical (recorded in
  `wild/RESUME_WILDB3.md`).

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`), cwd `pam/round4/wild/w12`.
- `w12_budget.zag` imports `R33_NATIVE_IO_V1.zag` (copied beside the source;
  already present in `wild/w12/`).
- `znc w12_budget.zag -o ~/workspace/scratch_wildb3/w12_budget --no-zagd`
  -> success. Binary is scratch-only (NOT committed).

## Battery (2x determinism per stream)
- stream: `./w12_budget w12_stream.txt` x2 -> byte-identical (`cmp` clean).
  SHA-256 `a892f4d97324a08a814ee8737053c9d40f8e8af16c95d5f377cf4db9c3090856`
- attack: `./w12_budget w12_attack.txt` x2 -> byte-identical (`cmp` clean).
  SHA-256 `389d557327e2d9f5bd109b864f5c1eaa9508908c4a874051473c4e24bc2cd9c1`

## Score
- `python3 score_w12.py <run> <stream>` -> exit 0 on both streams.
  Full mechanism mirror (frozen bar + §2 price + §3 episodes) matches every
  emitted row, episode summary, and summary line.

## Frozen-value notes (observations, not amendments)
- B: prereg freezes B=24814 with derivation "2x max per-episode total,
  max=12407". Recomputed from the frozen tape + frozen §2 mechanism
  (per-episode seen-set reset): max per-episode total = 10487 -> 2x = 20974.
  The derivation note does not reproduce; the PINNED VALUE B=24814 is used
  as frozen. (A larger B only makes the B1 prediction easier; all bars
  evaluated at the frozen value.)
- K1 first stage: prereg writes "(705,3588,1,1)" but its own K3 pins
  "bar passes 910/1102 (frozen 82.58%)", which requires the program-frozen
  (CT=705, MT=3588, ST=0, AT=0) variant (the (1,1) variant passes 671).
  The (0,0) variant is used, as K3 demands.
- K1 premise: "bar admits zero wrongs" is FALSE at item level for the W12
  fixture set: 2/30 wrong items (P rows idx 1124, 1126: conf=718,
  mrgF=6600, strong=agree=1) pass the frozen bar under every ST/AT variant.
  The Round-3 "zero" used pair-level accounting (9 CC1 pairs blocked via
  weakest member conf=704). W12 admitted exactly the bar's admit list
  (912 = 910 + 2); zero bar-rejected items re-admitted (no backdoor).
  See VERDICT_W12.md.
