# PAM Survivor Re-verification — Evidence (2026-09-25)

Independent re-verification: every arm below was rebuilt from frozen sources
with the pinned toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
batteries re-run ≥2×, outputs compared byte-for-byte against frozen evidence.
Pure Zag, zero RNG. Five independent crews; no crew trusted the old verdicts.

## X3 composition — RE-VERIFIED, DEMOTED holds

- full ×3: `b1e6b4e3e92534127d3e385b8506e9fcabbaa81d77670a5a2a2a19a264b6ff5b` (matches frozen)
- nop ×3: `e55889eb3fd3e22c98f1ffa03a9e5e4e762fd7506fe219f00722b2671eef9c3c` (matches frozen)
- Kill bars re-scored from fresh runs: zero safety-row failures, honest bars pass,
  anti-stub moves 120/120 on all 7 required classes. No kill, no earned survival.

## Individual PAMs — 6/6 RE-VERIFIED

- H-PAM-35: 7 output SHAs match frozen (`60cd2abe…4280b`, `c195f1e2…aa4`, `0b20426d…039c1`, `46166108…2ac3`, `e71df6ff…e19`, `bf148b44…5558`, `d71bb9be…d1af3`). SURVIVED unforgeability-only.
- H-PAM-36: `8c75d667…44f3`, `d43b6d39…76f`, `c2c36062…7b3` match. SURVIVED temporal game.
- H-PAM-33: 7 mode outputs byte-identical to frozen. KILLED as gate, RETAINED as channel-integrity check.
- H-PAM-30: 12 mode SHAs match frozen. DEMOTED to composition-only.
- H-PAM-34: 13 mode SHAs match frozen. Coarse KILLED, full-pin DEMOTED.
- H-8: SHA `0ed3de64…920` matches; AUDIT line reproduced exactly. Tripwire/audit only.

## WILD W1–W12 — re-verified; W5/W10 stay dead

- W1 `5ed1e464…a67b841` · W2 `bd4e3bd8…5de9665` · W3 `8b1f2896…af47` · W4 `8928815c…d21860`
  · W6 `db18b7fc…5d745` · W7 `fa922499…01ca76` · W8 `27fa3976…3e196a` · W9 `eb7934ad…4485a1`
  · W11 `690543d0…b789` · W12 stream `a892f4d9…d85a1`, attack `389d5573…c2cd9c1` — all match.
- W5 `0e630c0c…cd1a4ee` matches: KB-W5-M fired (27/2035) — CONFIRMED DEAD.
- W10 mu=1000 `be483f1e…6e90e4`, mu=500 `efd48b92…dd85a5c` match: D1 fired (573/1102) — CONFIRMED DEAD.
- W12: K1 premise failure reproduced exactly (items [1124, 1126]).

## WILD W13–W23 + wildc — re-verified; W14 stays dead; W13 HOLD

- W13 `e5c3ef14…8a6451b` — HOLD (LIVE 66.50% < 90% bar; K1 0/50, K6 max staleness 0).
- W14 `d37a4ea5…35bc` — CONFIRMED DEAD (4/12 admits; 392/392 false percepts margin>0).
- W15 `de044f42…2fb2` · W16 `c5f562a7…bab0c` · W17 `e674a7a2…26a67` · W18 `3c0755c4…857e` ·
  W19 `98eacc5d…831c0` · W20 `ecee5230…0066` · W21 `fe099d6f…2985` · W22 `a7fd9827…75ac` ·
  W23 `da8204fc…0ec82` — all match. W23: C 1065/1102 = 96.64%, 274 SINGLETON promotions, 0/14 attacks.
- W20 prereg inconsistency reproduced (R-AUTH vs K-ETB-4) — needs frozen-prereg amendment.

## CU track — RE-VERIFIED

- 12 rerun outputs match `evidence/DIGESTS.txt` (`9aa02241…`, `6ce44acc…`, `41c01194…`,
  `385fb630…`, `49b225a5…`, `a342440f…`); fixtures `0939bbd2…`, `c89d6acc…`, `e6379ddb…` match.
- P-UNC holds (G +0.0, K1 GREEN, agreement 0.0 < 0.90); P-CON falsified (three independent
  failures); P-HYB fails cost bar (2.434x > 1.3x); both arms catch 100/100 laundering probes.

## Method notes

- No crew had a local git repo on the VM (box-backed working copy); source identity was
  established by file SHAs + rebuild→byte-identical-to-frozen-evidence.
- All binaries were built to /tmp scratch; no binaries or `.zagd` files were committed.
- Killed arms that still fail identically are confirmed dead, not resurrected.
