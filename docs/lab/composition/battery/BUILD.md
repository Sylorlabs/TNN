# BUILD.md — D1 full battery build record (Crew B)

Frozen source: `~/workspace/comp_b4/ref/PREREG.md` §§1–8 (commit
`6ca9e042110ca`). Nothing from `AMENDMENT_PROPOSAL.md` enacted. D2 excluded.
No commit made by this crew; the coordinator commits.

## Toolchain (pinned, pure Zag, zero RNG)

| Artifact | SHA-256 |
|---|---|
| `znc_linux_x86_64_abed8aa1` | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| `battery.zag` (this battery) | `8b75e3ce5438b6137fc1f3e9490db0feced48b052a89159e8dd65ccb62fe1e51` |
| `battery` (compiled binary) | `6c9d2b06f9526965b1a56b592ec966e72562e00743003c77cc71b254f429b89e` |
| `work/wb_dialogue_bin` (real learner) | `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09` |
| `drive.py` | `08332a2a6f38f70bf026ff2e7fc2a2d78d66679ba72b55b8829e9ade030bfa3e` |
| `audit.py` | `7b8931dd2559e76c5d8dd932f236695d82f5d7341c5e70db64a04c41c5a01ba6` |
| `kbars.py` | `9a7030710e606bf51c87c12b05bfa7cdec24153a793f35483fb775a2e0a25a3e` |

The znc SHA matches the pinned toolchain fingerprint on record
(`498abcb5…`). `battery.zag` uses no `@import`, no RNG primitives, no phase
salt. The Python driver/auditor use no randomness (fixed protocol, fixed
arithmetic); Python's `set` iteration order is the only nondeterminism and
it does not touch any scored output (all scored bytes come from the Zag
binary and the learner binary).

## Real learner provenance

- Source: workbuddy round-2 dialogue learner,
  `docs/lab/workbuddy/round2/wb2_dialogue.zag` at commit
  `3cd24f11d119a17d14d9637e43ebdc8918b41e92`.
- Compiled 2026-09-27 with the pinned znc into `work/wb_dialogue_bin`
  (752,870 bytes). Build note: the archived Darwin-flavored
  `R33_NATIVE_IO_V1.zag` referenced `_zag_darwin_syscall` and failed; the
  build used `~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag` +
  `R33_NATIVE_SHA256_V2.zag` (same-directory native files) instead.
- Run in `chat` mode against `work/kb.txt` + `work/gaz.txt`. 8 sessions per
  driver run (6 P0 + 1 P3 + 1 samples), each a fresh process.

## Generator output (`./battery gen`)

| Section | Count | Content |
|---|---|---|
| TEACH | 36 | 6 rules × 6 examples, tok 0–5 |
| P0 | 48 | 6 rules × 8 probes, tok 6–13 |
| P1 | 150 | 30 pairs × 5 retrieval rows (4 inputs + 1 expected) |
| P2 | 600 | 120 pair-items (30 pairs × 4) + 480 triple-items (120 triples × 4) |
| P3 | 8 | distractors, tok 614–621 |

Sample pair row: `P2 pair 0,1 14 uiyq qqyiu` (REVERSE→DUP-FIRST on `uiyq`).

## Build defect found and fixed (before any valid run)

The pair enumerator was copied from the 4-rule pilot (`pi=p/3`, `q=p%3`),
which yields rule indices up to 8 for the 6-rule battery and panicked with
`slice index out of bounds` (exit 1) on `./battery null`/`singlerule`.
Fixed to `pi=p/5`, `q=p%5`, `pj=q+(q>=pi?1:0)`; triple enumerator verified
structurally (6×5×4=120 ordered distinct). The earlier `null.out` from the
broken build was discarded. All reported outputs come from the fixed binary
(SHA `6c9d2b06…`).

## Determinism record

| Arm | Runs | Result |
|---|---|---|
| NULL (scripted) | 2 | byte-identical (`null.out` = `null2.out`) |
| SINGLE-RULE (scripted) | 2 | byte-identical (`singlerule.out` = `sr2.out`) |
| Learner sessions (drive.py) | 2 + 1 perturbed | byte-identical all 5 files (`run1` = `run2` = `run_pert` under `MALLOC_PERTURB_=165`) |
| Learner scoring (`battery learner`) | 1 per transcript set | transcripts identical ⇒ scoring identical |

No phase salt anywhere. No RNG anywhere in the battery or the driver.
