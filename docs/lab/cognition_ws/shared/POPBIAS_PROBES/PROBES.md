# POPBIAS_PROBES — shared popularity-bias probe fixtures + scorer

Owner: WS3-A (mechanism + retune). Consumer: WS3-B's adversarial battery may
extend these. All deterministic, pure Zag, zero RNG.

## What this is

A probe set for the claim-judgment popularity-bias mechanism in
`tnn-lab/info-source/src/ws2_sense.zag` (the sense wire: `ws_decide` verdicts
+ `ws_install` deliberate-install path), and for its WS3-A retune
(`ws3/src/sense_after.zag`).

## Files

- `probes_table.json` — machine-readable fixture table (ids, families, ground
  truth, phases, verified flags, warrants) + the RESULT line format +
  disposition codes. Extend by adding fixtures here and regenerating.
- `score_popbias.py` — mechanical scorer: reads
  `ws3/runs/{before,after,control}_r{1,2,3}.log`, checks K7 determinism,
  applies kill bars K1–K7, prints the before/after table. Exit 0 = all hold.
- Fixture sources: `ws3/src/gen_drivers.py` (single table → 3 Zag drivers),
  `ws3/src/sense_before.zag` (byte-identical frozen original),
  `ws3/src/sense_after.zag` (retuned).

## Probe families (13 fixtures, 14 RESULT rows)

- **never-lie** (A2/A3/A5/A10): false claim "Poseidonia", unanimous agreement
  at 2/3/5/10 domains, unverified. A2V: same + verified=1 (TEACHER-CONFIRM).
- **sleeper** (B1/B1V/B2): true claim "Ouagadougou", 1 domain (B1),
  1 domain + verified=1 WORLD-SETTLE (B1V), 2 domains (B2).
- **reversal** (C1/C2a/C2b): C1 = 3× false "Lyon" + 1 live contradictor "Paris";
  C2a = 3× "Lyon" unanimous; C2b = same handle after a reliable contradicting
  belief ("Paris" @ conf 80) is installed.
- **sanity** (D1/D2/D3): warranted install of true "W"; zero results; tampered
  envelope (disp 9 path).

RESULT line:
`RESULT|<arm>|<fid>|<family>|D<disp>|C<chosen>|N<nudge>|F<conf>|I<install_rc>|V<verified>|S<stored_value>`

Arms: BEFORE (frozen original — exhibits the bug), AFTER (retuned, popcap=5),
CONTROL (retuned, popcap=0 — bias-free control).

## The retuned rule (summary)

Popularity (repeat count) is a bounded confidence annotation only
(`nudge=min(topc-1,popcap)`, `conf=50+nudge`, cap 55): it never changes a
disposition, never picks a winner among disagreeing claims (disp 6 retired —
any disagreement → WITHHOLD), is zeroed by any single contradiction (live or
installed conf≥50), and never qualifies an install (install needs
`verified==1` non-popularity warrant). Popularity is ledger-tagged POP as
evidence-not-truth.

## How to extend

1. Add fixtures to the `FIXTURES` table in `ws3/src/gen_drivers.py`.
2. Regenerate: `python3 gen_drivers.py` (writes `ws3/build/drv_*.zag` +
   this dir's `probes_table.json`).
3. Rebuild with the pinned toolchain
   (`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
4. Run each arm 3× into `ws3/runs/`, run `score_popbias.py`.

Note: the sense module stores at most 6 results per fact — popularity beyond
6 agreeing domains is not representable (nudge saturates at its cap first).
