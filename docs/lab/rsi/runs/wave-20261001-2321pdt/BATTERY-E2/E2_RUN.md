# E2_RUN.md -- Single-guide content discrimination execution report

Wave: wave-20261001-2321pdt, lane BATTERY-E2.
Prereg: PREREG_E2.md, frozen alone at commit 229cf5263, SHA-256
bdb6eddce83d72a3273cf6e829cd56fab457a7cc98fffafa882b6c45746abd83
(re-verified unchanged from git at run time: `git show 229cf5263`
hashes to the same value). All work pure Zag (pinned znc) and
shell under PATH=$HOME/safebin; no Python invoked. TNN-2 frozen;
no source edits.

## Process bars

- E2-K1 (prereg ordering): PASS. Prereg committed alone
  (229cf5263) before implementation (4900c177d) and before any
  run; SHA-256 re-verified unchanged.
- E2-K2 (determinism): PASS. 3/3 byte-identical transcripts per
  world; each transcript contains exactly one CHOICE line.
- E2-K3 (frozen binary): PASS. freeze_shim2_bin and tnn2.zag
  match section 0 hashes before the first run and after the last.
- E2-K4 (seal integrity): PASS. E2_MANIFEST.sha256:
  - 5f38eca7699dccaee0c3761e8440742a824eabcdf6e22b17551059ec4949fec9  e2_a_world.txt
  - 1b993da2a3210a6123a6d6ff433ac2fe3436e300f302a7f0482581fe437caf2b  e2_b_world.txt
  - 8c0222254050b10cc247418dfecc1424c6dd0326480b413632adad57bc380d87  e2_d_world.txt
- E2-K5 (block calibration): PASS. E2-D degenerate control yields
  CHOICE 0 on all 3 runs (presence bit reads in this id block).
- E2-K6 (no leak): PASS. E2 id set returns zero matches in the
  frozen cognition sources (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS.
  (1) e2_worldgen.zag contains no id-conditioned or
  value-conditioned branching; its if/while constructs are
  generic buffer, path, and argc helpers; world ids appear only
  as the exact prereg section 2 stream emissions.
  (2) e2_run.sh performs no transcript transformation and no
  logic keyed on world ids, subjects, relations, or CHOICE
  values beyond the byte comparison required by the prereg
  section 3 decision rule and the E2-K5 gate; world selection
  is a loop over the three world letters.
  (3) grep for python across the lane finds only guard
  documentation; no invocation occurred.

## Per-run evidence (transcript SHA-256)

E2-A (content A: single miss on 81001/81101, then ACT):
- e2_a_r1.trans: 27544c0803beb8c70d0611a8724af431d8b07313737b5f43d4fea3a05ec9112f
- e2_a_r2.trans: 27544c0803beb8c70d0611a8724af431d8b07313737b5f43d4fea3a05ec9112f
- e2_a_r3.trans: 27544c0803beb8c70d0611a8724af431d8b07313737b5f43d4fea3a05ec9112f

E2-B (content B: taught 82002/82102, single miss on 82001/82101, then ACT):
- e2_b_r1.trans: 5229a8c213e7349045a5388321b6494ab0bfa2050535d9b1a46c2b502283f02b
- e2_b_r2.trans: 5229a8c213e7349045a5388321b6494ab0bfa2050535d9b1a46c2b502283f02b
- e2_b_r3.trans: 5229a8c213e7349045a5388321b6494ab0bfa2050535d9b1a46c2b502283f02b

E2-D (degenerate: ACT on empty state):
- e2_d_r1.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d
- e2_d_r2.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d
- e2_d_r3.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d

## Transcripts (run 1 of each; runs 2 and 3 byte-identical)

E2-A:
```
WORLD_BEGIN
ANSWER 81001 81101 -2
CHOICE 30
WORLD_END events=2 answers=1
STATE_SAVED
```

E2-B:
```
WORLD_BEGIN
OBSERVED 82002 82102 82012
ANSWER 82001 82101 -2
CHOICE 30
WORLD_END events=3 answers=1
STATE_SAVED
```

E2-D:
```
WORLD_BEGIN
CHOICE 0
WORLD_END events=1 answers=0
STATE_SAVED
```

## Decision rule outcome (prereg section 3, frozen)

Observation channel: the single CHOICE line per transcript.
CHOICE(E2-A) = "CHOICE 30"; CHOICE(E2-B) = "CHOICE 30",
byte-identical across all 3 runs of each world.

Signature: SIGNATURE-CONTENT-BLIND.
Verdict: E2-CONTENT-BLIND.

Reading: two single guides with materially different content
(different missing facts, different resolution-state context)
produce byte-identical actions with no concurrency anywhere.
The constant-guide story is not a concurrency phenomenon.
This confirms H2a (absent content channel at the guide-to-ACT
interface) as the root cause of Cluster 2 and kills H2b (the
concurrency-collapse alternative) for this instrument. The
action selection reads guide presence only; guide content,
count of distinct content, and resolution state have no write
path into ACT.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2/PREREG_E2.md
- Tools: e2_worldgen.zag, e2_worldgen_bin, e2_run.sh
- Worlds and manifest: e2_worlds/ (E2_MANIFEST.sha256)
- Transcripts: e2_runs/ (per-world per-run .trans, per-run .bin state)
- Transcript hashes: e2_runs/E2_TRANS_SHA256.txt
