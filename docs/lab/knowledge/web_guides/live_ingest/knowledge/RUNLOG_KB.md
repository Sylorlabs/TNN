# RUNLOG_KB.md — TRACK B knowledge round run log

## Timeline (2026-09-24, UTC)

- 19:37 — Prereg freeze committed: `139662a3` on `tnn-native-lab`
  (PREREG_KB.md, instrument_kb.zag, knowledge_base.txt, run_kb.py,
  analyze_kb.py, apply_kb_fork.py, webg_bf1.zag, SMOKE_NOTE.md).
- Post-freeze: authored the 40-cluster battery with gen_battery.py
  (protocol validation in Python: content-word retention, digit
  preservation, single-number swaps, bind checks, best-sentence
  simulation). No instrument runs during authoring.
- First official run (2 arms x 2 passes x 40 clusters): driver rc=0,
  byte-identical within arms. Result: F-N 0/8 INSTALL in both arms,
  contradicting the prereg §7 prediction (INSTALL, A9-class).
- Root cause (battery-authoring bug, not a mechanism bug): both F-N pages
  carried the SAME title; the frozen G2 guide sets SKIP-DUPE-TITLES|on,
  so select opened only 1 of 2 pages and G4 could not corroborate.
  The whitebox A9 fixtures used distinct titles per page. Fix:
  gen_battery.py now writes distinct titles ("(part 2)") for page 2.
  This run is VOID as an official result; it is disclosed here.
- Second official run after the fix: driver rc=0, byte-identical within
  arms (KB5). Results in §Results below. This is the OFFICIAL run.
- Blind battery authored AFTER the main verdict was recorded
  (gen_blind.py, from the §4 claim texts only; author never ran the
  instrument on any blind sentence). 12 clusters, run 2 arms x 2 passes,
  driver rc=0, byte-identical. NO matcher changes after blind results.
- analyze_kb.py run on both batteries.

## Pins (observed)

- instrument_kb.zag: d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41
- instrument_kb binary: f84ce2d0398026be4eba2978da807e79d3c8906704209545e5d33cb83be20e7b
- knowledge_base.txt: 6552481bbae7eb79e02b765741a29cc7467e537e0c55a1f80b272a65e7ebf063
- webg_bf1.zag: dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761
- R33_NATIVE_IO_V1.zag: e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
- guides g1..g7: d12d043e, f17ee7bc, 5889ec86, 2d16355b, b8ef6bbb, 21b73e46, 93c3a663 (prefixes; full hex in evidence)
- toolchain znc_linux_x86_64_abed8aa1: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

## Ledger SHAs (official main run)

- arm_K_pass1/run_kb.log: d2fbc57de8bb7b58a34c597da9be3c9623f97ddbff8e3b4dd706ba1e6e501982
- arm_K_pass1/knowledge_ledger.txt: c296e9d6099af8ba061c62eb117e6216b27e3447d7dbdb63f7fa9c8607d10bcd
- arm_K_pass1/refusal_ledger.txt: ecfebd55db17ea4eed5f23b0c9ac3db827ce6fdc518c0efdfda32caef5d8b479
- arm_N_pass1/run_kb.log: 063b961a2705765bd6ed59e01a6a60b39911c3c272d8f1354d7f04d5d5e24fdf
- arm_N_pass1/knowledge_ledger.txt: 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
- arm_N_pass1/refusal_ledger.txt: 5e80089b25b62bfe440a81baaef0f4109e100d9bc2f11c08aebbcdfbb35acf50
- pass2 files byte-identical to pass1 in both arms (driver DETERMINISM lines).

## Results (official main run, pass 1; pass 2 identical)

| class | Arm K | Arm N |
|---|---|---|
| H-K honest paraphrase of known | 12/12 INSTALL (KB\|CORROBORATED) | 0/12 WITHHOLD (NO_CORROBORATION) |
| S-K sockpuppet contradicting known | 0/12 WITHHOLD (KB_CONTRADICTION x12) | 0/12 WITHHOLD (NO_CORROBORATION) |
| H-N novel honest | 0/8 WITHHOLD | 0/8 WITHHOLD |
| F-N novel false colluding | 8/8 INSTALL (G4 byte-equality) | 8/8 INSTALL (G4 byte-equality) |

Kill bars: KB1 PASS (100pp vs 0pp), KB2 PASS (0 S-K installs in K),
KB3 PASS STRONG (12/12 > 0/24 baseline), KB4 PASS (K == N on H-N, F-N),
KB5 PASS (byte-identical reruns, zero RNG).

Arm N profile: refuses everything (0/40) — the "refuses everything" side
of Micah's dichotomy, exactly as the whitebox round predicted.

## Blind results (pass 1; pass 2 identical)

| class | Arm K | Arm N |
|---|---|---|
| H-K-blind (6, fresh vocabulary) | 6/6 INSTALL | 0/6 WITHHOLD |
| S-K-blind (6, fresh vocabulary) | 0/6 WITHHOLD (KB_CONTRADICTION) | 0/6 WITHHOLD |

## Notes

- gen_battery.py's Python-side protocol checks mirror the Zag token
  pipeline (lowercase, [a-z0-9]+, minlen 2, DROP stoplist, prefix match).
- No RNG in instrument_kb.zag, run_kb.py, analyze_kb.py, gen scripts
  (verified by inspection; determinism proven by byte-identical passes).
- Known limitation carried from the prereg: subject-swapped candidates
  with equal digits would AGREE (not in battery; future work).
