# VERIFY — T2-GOALB (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** `sylorlabs/TNN`, branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, file `docs/lab/crossref/PREREG_TIER2.md`, section T2-GOALB (extracted programmatically; never from memory).
**Tier-2 crew verdict under test:** REPRODUCED.

## Pins (all verified before running)
- Tier-2 prereg: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Evidence commit: `5c1bf2a8babe2197160d5c092298bdb946d8bc67`
- `docs/lab/GOALB_STORY/evidence/b2_combined.md` blob `7cc578f7935effcf5550378f9bd48937d40b761f` ✓ matches the recorded pre-clobber SHA (the destructive `score_b2_combined.py` was NEVER executed by this re-verifier).
- `docs/lab/dialogue/kb.txt` blob `68c86046277ecaf0b358bad30f474692d508d381`, SHA256 `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1` ✓ matches kb_before.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Zero RNG.

## Type A — mechanical bars (fresh rebuild from committed sources)
- `story_all.zag` (blob `69ee6052522c2344a0bee8d65c2c5c1a5f5941fd`) rebuilt with pinned znc: `wrote native binary story_bin (137217 bytes main)`.
- 3 fresh-process runs, cwd with `inputs/words.txt` + `inputs/classes.txt`: all exit=0, byte-identical, SHA256 `9dd1c20c25684a305887148dcd80768b8d208309aa1eb31fa070439e47870dd7` — EXACT match to the committed `runs/rep1.log`.
- **B1 coverage 16/16** (POS 8/8, DEL 8/8): every story contains all words assigned to its set.
- **B3 novelty 16/16**: no story sentence (≥6 words) appears verbatim in the corpora.
- **B4 leakage PASS**: kb.txt SHA256 identical before/after; 0/16 story substrings (≥16 bytes) in kb.txt; source audit: sole file open is `open(2)` flags=0 (O_RDONLY); only read(0)/close(3); no write-to-file path; all output via stdout.
- **B5 determinism PASS**: 3/3 byte-identical + byte-identical to committed log.
- Negative control: deleted-word story flagged correctly (checker live).

## Type C — B2 two-judge re-derivation (independent parser, committed records)
- 17/17 items parsed on both judges; key T01–T16 → S1–S8 × POS/DEL, T17 → CTRL.
- Two-judge means ≥3.5: **DEL 4/8** (S2 3.5, S4 4.0, S6 3.5, S8 4.0), **POS 0/8** (all 1.5) → bar ≥6/8 **FAILED both variants** ✓.
- Per-judge: sol DEL 6/8 / POS 0/8 / CTRL 5; grok DEL 0/8 / POS 0/8 / CTRL 5 ✓.
- Every DEL story > its set-pair POS on both judges (8/8 pairs) ✓; max inter-rater |diff| = 2 ✓.

## Verdict: REPRODUCED
All four mechanical bars match on a fresh rebuild; the two-judge B2 FAIL re-derives exactly with DEL 4/8 / POS 0/8. No mechanical bar flipped.

## 2026-09-24 — verifier fix (follow-up)
The `evidence/verify_goalb.py` committed in b7e8fa3391e8e0cfbe9a39f14c328b6e21f04087
had a faulty B1 parser: it read words.txt as a flat word list and chunked it
`words[(n-1)*per : n*per]`, treating each whole `S<n>: word,word,...` line as one
"word" — reporting B1 0/16 on the same log. It has been REPLACED with a faithful
mirror of the frozen `GOALB_STORY/src/verify_goalb.py`:
`S<n>: word,word,...` per-set parsing, word-boundary regex against STORY lines
only, frozen B3 corpus (dialogue/kb.txt + battery.txt + prose-learning/v3/inputs3*),
frozen B4 sliding-16-byte-window check. Re-run on the committed fresh rep1.log:
B1-COVERAGE 16/16, B3-NOVELTY 16/16, B4-SUBSTRING 16/16 clean,
kb-sha256=3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1.
B5: rep1/rep2/rep3 byte-identical (9dd1c20c25684a305887148dcd80768b8d208309aa1eb31fa070439e47870dd7).
The mechanical bars now reproduce END-TO-END through the committed verifier.
