# WILD-B RESUME — THIRD GENERATION (2026-09-24)

Two predecessor generations died in daemon restarts before producing
anything. No build progress existed on disk beyond the original fixtures.

## Inherited state (verified on-VM 2026-09-24 by the third generation)

- Frozen preregs read: `PREREG_ROUND4.md`, `PREREG_W4/W5/W7/W10/W11/W12/W13/W15`,
  `PREREG_AMEND1.md`; shared tape `TAPE.md`; `TAPE_W7_ADDENDUM.md`.
  No prereg was modified. (PREREG_W1/W2/W3/W6/W8/W9/W14 are WILD-A — not read
  in full; only `TAPE_WILDA_ATTACKS.md` was skimmed to note its existence.)
- `m1_cases.txt`: sha256 `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611`
  (matches TAPE.md), counts 1102 C / 12 W / 18 P / 1109 B (exact).
- Frozen sources: sweep.jsonl `4163fffa…83f2`, rec_install.records
  `c26ac974…17c4ad`, gen_guard.py `49eef7b1…ae2c` — all match TAPE.md §2.
- W7 addendum: signals `9024f08e…10ce2b`, truth `5adc617c…3a34a` — match.
- All six fixture generators re-run into scratch; outputs BYTE-IDENTICAL
  to on-disk fixtures (cmp clean): w7 (200/200 rows), w10 (2291 rows,
  kinds C=1102 B=1109 W=12 P=18 F=50), w11 (370 chains), w12 (1132-row
  stream, 628-row attack, target idx 70), w13 (10050 events), w15 (5250 events).
- Preregistered predictions re-verified from the tape by an independent
  Python mirror: W confs
  764,774,788,798,798,799,800,806,806,819,830,832; P weaker-member confs
  704×8,840; CT*(0)=841; correct-admit at 841 = 433/1102 = 39.29%;
  M1 bar (705,3588,0,0) = 910/1102 = 82.58%; W12 max per-episode price
  total = 10487 → B = 20974 (AMEND1 confirmed; an initial recompute that
  used a global seen-set instead of the per-episode seen-set gave 9167
  and was discarded — the per-episode rule is the frozen one);
  W5 distinct signatures = 207 (< 4096 capacity).
- W11 C3 construction audit (`w11/C3_AUDIT.md`, pre-fixture-use) present.
- No Zag instruments, batteries, verdicts, or w4/w5 dirs exist yet —
  builds begin from this commit.

## Coordinator follow-ups (received by dead predecessors; applied now)

1. K6/K7/K8 kill-bar types ADOPTED as add-only bars (K6 = staleness;
   K7 = calibration-sensitivity audit; K8 = classification audit via
   dual-run verification). K6 and K7 are used in W13/W11; K8 is not
   invoked by any WILD-B design (none classifies admits into ranked
   classes requiring dual-run verification — recorded, not evaded).
2. Fable F-P3 ↔ W11 mapping: W11 kept as assigned; F-P3's
   calibration-poisoning bar ADOPTED as W11's K7 (0/40 drifted admits at
   exact-match threshold). Recorded in PREREG_W11 §7, restated in
   VERDICT_W11. W10/W7 forger non-sharing decision honored
   (PREREG_W10 §7, PREREG_W7 §7). W12/W8 non-convergence recorded
   (PREREG_W12 §7).
3. Micah 2026-09-24 standing law (no arbitrary hard limits): every frozen
   numeric cap classified load-bearing vs arbitrary at verdict time.
4. Hands-off §5 unchanged: M1 bar (0,0,705,3588) as-is; fable's 4 repairs
   not applied; 3 HELD items not run.

## Work plan

Build w4_selftrain.zag, w5_memory.zag, w7_hunter.zag, w10_duel.zag,
w11_chain.zag, w12_budget.zag, w13_lease.zag, w15_quarantine.zag (pure Zag,
[]u8 arenas + LE accessors, zero RNG), Python scorers as mirrors, batteries
≥2× byte-identical, kill bars applied mechanically, per-design verdicts
`VERDICT_W{4,5,7,10,11,12,13,15}.md`, committed stage by stage.
