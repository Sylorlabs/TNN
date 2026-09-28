# RUNLOG_B3536

2026-09-24 ~12:15 PDT — crew start (second replacement; fresh start).
- Checkpoint first: PREREG_B3536.md drafted, committed ALONE: `abbc35b29a3`.
- Amendment 1 (self-contradiction fix + J-36 carry scoping): `fed0d98e`.

2026-09-24 ~12:20 — sources extracted by script from 1fa4ae58 + 6a30f5f9;
13 shared helpers asserted byte-identical, deduped; 51 fns in b3536_lib.zag.
Composition driver comp_drive.zag written (new test code); class identity
verified 25/25 against ec8d5d13 (no drift).

2026-09-24 ~12:30 — build: b3536.zag `c650450a…` compiled OK. Smoke tests:
comp 0/120 everywhere except C36J 120/120 carry; b2b3 all bars green.
Build committed BEFORE any run: `7fe177ae`.

- Anti-interaction audit found stale hardcoded seeds in dead h35 m36 →
  removed by script (build v2); audit CLEAN (1 ns_sha256 site; old seed only
  in marked attacker fixture; no attacker-side seed/world channel).
- Build v2 committed: `7a1a8422` (b3536.zag `1602247d…`).

2026-09-24 ~12:40 — full battery: comp 3× byte-identical
(`a321d59d…`), b2b3 3× byte-identical (`007aa9c6…`). 17/17 bars PASS.
VERDICT: SURVIVED. Seed-reuse detector exercised (refuses on used ledger).

Evidence commit: <to fill>.
