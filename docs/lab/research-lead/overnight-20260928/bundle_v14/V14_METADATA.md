# Bundle v14 Metadata

## Bundle

- File: `~/workspace/tnn-native-lab-20260930-v14.bundle`
- Created: 2026-09-30 (UTC)
- Size: 2.0G
- SHA-256: `06b43ac8db876447237da11e3e33d5f44e50e7d5277429deccf9396d89759481`
- HEAD captured: `d5e3222b608c358b92332f0cad4020d00be71741`
- Refs: 69
- Commits on HEAD: 3279
- Verification: `git bundle verify` reports complete history.

## HEAD commit

`d5e3222b6` Ledger cycle 13: append C125-C133 (133 claims; zero new SURVIVES; L3 still zero).

## Major work since v13 (HEAD `ad7d3ac1cb98`)

- COMP-1 build (`170e39424`)
- DEVINT-CLA2 build (`35f9500b2`) + red team (`a5ccb100d`, 4 ATTACK-SUCCESS vectors)
- Integration prereg (`7fc7148ac`) + TNN-1 build (`0323b97d5`, 1090 lines, 35/35 tests) + TNN-1 red team (`cbde38737`)
- Inquiry prereg (`04ac028fb`) + inquiry build (`396ecafa4`, PROCESS-FAIL per guard, 9th Python incident) + clean re-freeze (`18ed3331c`)
- MUL-1 build (`fbf14f73a`, 4-cell PROC, 4297 rejections) + MUL red team (`44f22979b`, 6 vectors ATTACK-PASS)
- ACT bid alignment (`75a9b0e04`)
- C1 harness fix (`fac9875b0`)
- Guard audit (`e0a842962`) + Python incident audit 2 (`4a97c985c`)
- Record correction (`67f92ed4f`)
- Compression tracker (`f46a89e99`)
- Ledger cycles 12 (`b81ca69ed`, 124 claims) and 13 (`d5e3222b6`, 133 claims)

## Supersession

This bundle supersedes v13 (`~/workspace/tnn-native-lab-20260930-v13.bundle`).

## Governance

- Working tree verified clean (no modified tracked files) before bundle creation.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff verified.
- Zero Python invocations in this wave (Step 0 guard recorded in NAMECHECK.md).
- Bundle HEAD matches repo HEAD at creation time (verified via list-heads).
