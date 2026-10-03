# REPRO RESULT: OpScope Step 4 (Independent Reproduction)

## Verdict: OPSCOPE-REPRO-PASS

## Kill bars

- K1 PASS. Independent rebuild: source extracted from committed
  commit `7ca508cd0` only (no sealer/builder working files touched),
  compiled fresh with the repo `znc` on this machine.
- K2 PASS. Results match: 3/3 run outputs byte-identical to the
  committed sealed runs; scored values S1 14/14, S2 7/7, S3 1;
  VERDICT line reads SEALED-PASS in my runs.
- K3 PASS. Pure Zag at every stage: extraction (git), build (znc),
  runs, byte checks (md5sum, sha256sum, diff, grep, sed, cmp),
  committing (git). Zero Python anywhere, including scratch and
  verification. 3/3 byte-identical runs, exit 0, zero stderr bytes.
  No em or en dash bytes in any new file (shell-only check).

## Extraction fidelity

- `opscope_sealed.zag` extracted via
  `git show 7ca508cd0:.../opscope_sealed/opscope_sealed.zag`;
  sha256 of extracted content
  `365a7d1bc7d9008b7b00728f5170ce19618e8c8c87478b22df6b31429deaa839`
  matches `git cat-file -p` of the committed blob byte for byte.
- No modification of the extracted source: the build ran against
  the committed text verbatim.

## Independent rebuild

- `znc opscope_sealed.zag -o repro_bin`:
  `znc: wrote native binary repro_bin (147760 bytes main, 0 external tools)`.
  147760 bytes main matches the sealed result doc claim exactly.
- Build warnings: same E0101 `+ 0` notes as the sealer's
  committed `sealed_build.err`.

## Runs (this machine, fresh binary)

| Run | exit | stderr bytes | md5 |
|-----|------|--------------|-----|
| repro_run1.txt | 0 | 0 | 88524b3ec6181c60411fa09b09c6d744 |
| repro_run2.txt | 0 | 0 | 88524b3ec6181c60411fa09b09c6d744 |
| repro_run3.txt | 0 | 0 | 88524b3ec6181c60411fa09b09c6d744 |

Committed `sealed_run1/2/3.txt` (from `7ca508cd0`) all have md5
`88524b3ec6181c60411fa09b09c6d744`. All six hashes identical:
my 3 runs are byte-identical to the sealer's 3 runs.

## Scored values (from my runs)

- `S1_SEALED_NEG: 14/14` (bar >= 12/14) PASS
- `S2_CONTROLS: 7/7` (bar == 7/7) PASS
- `S3_WHITEBOX: 1` (OPREC trig=1/sig=0, sup 12/12/12/12/12/14/16,
  created 40..100, 7 active entries) PASS
- `VERDICT: SEALED-PASS`

## Training fidelity (learner identity)

The reproduced run's training section (through TRAIN_DONE) is
byte-identical to the committed builder `run1.txt` from `837c02c59`,
after accounting for exactly one sealer-added line in the sealed
harness: `VERIFY_U_ROUNDTRIP_SEALED_21: 1` (line 3, the sealed-world
round-trip verification). Dropping that one line, lines 1-2 + 4-104
of my run diff empty against lines 1-103 of the builder's committed
run. The evaluated learner is exactly the committed K=2 rebuild
learner.

## Sealed-item cross-check (world identity)

All 21 sealed items in my runs were compared field by field against
the committed `sealed_episodes.txt` from `7f24f2f9d`: ids, U
sequences, and pred==tgt all match, 21/21. The world scored is the
committed sealed world (seed 987654321).

## Artifacts (this commit)

- `opscope_sealed.zag` (extracted committed source, unmodified)
- `repro_bin` (independently built native binary)
- `repro_build.err` (compiler warnings)
- `repro_run1.txt`, `repro_run2.txt`, `repro_run3.txt`
  (byte-identical raw outputs)
- `repro_run1.err`, `repro_run2.err`, `repro_run3.err` (empty)
- `REPRO_RESULT.md` (this file)

## Source commits reproduced

- `837c02c59` builder (learner identity proven via training fidelity)
- `7f24f2f9d` sealed world (item cross-check 21/21)
- `7ca508cd0` sealed harness + sealed runs (md5-identical outputs)

## Honest scope

OPSCOPE-REPRO-PASS is pipeline step 4 of 11. It independently
confirms the sealed-evaluation evidence: from committed source
alone, a fresh build on this machine reproduces the sealer's runs
byte for byte and the same SEALED-PASS verdict. No L3 claim, no
SURVIVES. Steps 5-11 (baseline, alternative-explanation attack,
OOD beyond this sealed set, ablation, transfer/reuse, independent
red team, governance audit) remain open. BUILD-PASS stands.
