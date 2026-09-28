# N5 sealed-battery recovery — run manifest

Recovery agent: independent (not the N5 crew). Date: 2026-09-26 UTC.
Prereg: PREREG_MATH_R4.md (frozen, commit 84ed45077a554f9897ec55c2ca1430273c79eb69).

## Binary
- Source: `n5.zag` (this package; frozen engine source from
  `math_logic/round4/engines/n5/n5.zag`)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Binary SHA-256: `c13243cb7834fb4c044143277b33ba65fa7ee975a20739cd2359f92c6205a219`
  (byte-identical to the crew's build; binary itself NOT committed)
- Source SHA-256: `c2c105d8d14799fa0655b80f4391a1e083ce47d07d9e98d3f3ed922e63817598`

## Knowledge store (prereg §2, R4 wording)
- `math_logic/round4/batteries/knowledge/KNOWLEDGE_STORE_NL.md`
- SHA-256: `e8846333ff4a97a4224d6d262aef1cb021ea09e24b39cb1ecbfb4692f49c3c1d`

## Battery verification (before runs)
- `verify_battery.py` on round4 batteries: ALL CHECKS PASS
  (byte-identical regen, counts, sealed trace validation, CHAIN50 linkage,
  paraphrase/nonce checks, knowledge-store checks, no sealed leakage,
  manifest verification, exit-3 sealed-write guard)

## Run protocol
- 3× reruns per problem, `cmp`-verified byte-identical; clean cache snapshot
  per run (`/tmp/<pfx>_cache_clean.txt` → per-run copy); pure Zag; zero RNG.
- Timeouts: 180 s/run for para, PB1, PB2, PB4, CHAIN50. Three PB3 problems
  (B5X_NL_L2_15, B5X_NL_L3_05, B5X_NL_L4_05) exceeded 180 s with the full R4
  store and were re-run at 600 s/run (all completed; e.g. L2_15 → WITHHELD
  in ~179 s). No reported verdict is a timeout artifact.
- CWD for all runs: `math_logic/round4/engines/n5` (B5X store paths resolve
  relative to tnn-lab root per n5.zag `n5_load_stores`).

## Coverage
- 183 problems × 3 runs = 549 output files, all non-empty, all r1/r2/r3
  byte-identical (independent re-verification: 0 mismatches).
- para: 36 (12 bases + 12 paraphrases + 12 nonces)
- pb1: 24 R3N (9 engine errors rc=-2/exit-4, documented in verdict §3)
- pb2: 37 twins · pb3: 60 B5X-NL · pb4: 20 CHAIN-NL · chain50: 6 CHAIN50-NL

## Results (from score.py + independent audit — identical)
- PARA-INV gate: PASS (no flips; all-WITHHELD stability)
- PB1: 10/24 correct, fd=0, fw=5 → MISS (need 12/24)
- PB2: 33/37 correct, fd=0, fw=4 → CLEAR (need 30/37)
- PB3: 42/60 correct, fd=14, fw=4 → MISS (need ≥45/60, fd<10, fw<10)
- PB4: 0/20 → MISS (need 12/20)
- H-CHAIN: 6/6 derived, trace depths 56–72 → HOLDS
- **Bars cleared: 1/4.** R3 verdict (DUAL wins) stands for N5.

## Files
- `VERDICT_N5.md` — the verdict
- `SCORES.txt` — scorer output
- `run_all.sh` — main runner (batteries selectable; 180 s timeout)
- `run_pb3_slow.sh` — PB3 600 s-timeout runner (separate file; see verdict §1)
- `score.py` — scorer (sealed keys read from round3/batteries/sealed/, never
  by the engine)
- `n5.zag` — frozen engine source
- `runs/para|pb1|pb2|pb3|pb4|chain50/` — 549 3×-verified outputs
- `runs/RUNLOG.txt`, `runs/RUNLOG_PB3SLOW.txt` — run logs (binary+store SHAs)
- `logs/` — per-runner logs (g1/g2/g3 slow-PB3, chain50, pb4, superseded attempts)

## Provenance
Supersedes the N5 crew's `~/workspace/n5_certified/` runs (wrong R3 store
path + mid-run store corruption; see VERDICT_N5.md §6). Crew outputs preserved
in workspace for audit, not cited as evidence.
