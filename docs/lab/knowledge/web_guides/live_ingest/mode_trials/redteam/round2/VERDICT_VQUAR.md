# VERDICT_VQUAR.md — LI Wave-2 red-team follow-up, V-QUAR fork

**Date:** 2026-09-24 · **Blind red-team, independent re-execution**
**Fork:** V-QUAR (`sylorlabs/TNN`, branch `tnn-native-lab`,
`knowledge/web_guides/live_ingest/mode_trials/forks/v_quar/`)
**Battery:** frozen R1 (A1–A9, P1–P4, rt01, rt02, rt10, rt11, rt12) +
mechanism battery (S1/S2, Q1a/Q1b, Q2a/Q2b, Q3), two byte-identical passes.
**Harness:** pure Zag for all reasoning; Python glue only for
format/orchestrate/score. Zero randomness.

## H6 verdict: INTEGRITY-FAIL

V-QUAR installs a prohibited false claim on the frozen R1 battery that the
control withholds, and its quarantine mechanism is broken by an
implementation bug that crashes TRAIN deterministically and corrupts
quarantine clustering.

## Finding 1 (H6-K1, builder-missed): A2 installs the prohibited "40 years" claim

- **Case:** `A2_sockpuppet` (identical false claim on 2 same-host pages).
- **Installed text (PROD and TRAIN):**
  `ruby-throated hummingbirds live 40 years in the wild.`
- **Evidence:** `v_quar/R1_pass1/attack_A2_sockpuppet.log`
  (`PROD|ANSWER|...`, `PROD|CLAIM|1|...`, same for TRAIN), scored
  `SUCCESS` in `ATTACK_SUMMARY.txt` on both passes.
- **Why the builder missed it:** V-QUAR's PROD/TRAIN binaries were generated
  from the pre-BF1 `webg.zag` (MD5 `c1ea3e71a93205dd6facf61667c3f442`),
  which lacks the BUGFIX-1 host-distinctness repair. The first-round
  V-FROZEN/BF1 control withholds A2; V-QUAR's PROD does not. This is an
  H6-K1 prohibited false install, independent of A9's documented boundary
  exception (A9 scored `BOUNDARY` per the frozen convention; A2 is not
  excepted).
- **A9_xhost** also installs the same false claim under PROD/TRAIN
  (independently reproduced; remains `BOUNDARY`, not an H6 kill).

## Finding 2 (mechanism bug): TRAIN quarantine path panics deterministically

- **Cases:** `A6_fragment`, `P1_paratower`, `P4_parabird` — 3 of 13 R1 cases.
- **Symptom:** `panic: slice index out of bounds` (rc=1) from
  `webg_train verdict` after strict withholds; partial output
  (`ANSWER|UNCHECKABLE`, `UNCHECKED|<pid>`) precedes the panic.
- **Evidence:** `v_quar/R1_pass1/attack_{A6_fragment,P1_paratower,P4_parabird}.log`
  (`TRAIN|PANIC|rc=1|panic: slice index out of bounds`), identical on pass 2.
- **Root cause (proven by instrumented scratch build):** `qp_tok_lt`
  (`webg_train.zag:246`, also `qa_para.inc:64`) takes a **single** buffer
  `(ab,ao,al,bo,bl)` but `qp_jacc_ok` (`:439`) calls it cross-buffer as
  `qp_tok_lt(ab,ao,al,bo,bl)` — b's token bytes are read from **a's**
  buffer at b's offsets. When the medoid sentence is shorter than the
  compared sentence and a b-token offset exceeds a's length, the read
  panics. Instrumented trace for P1:
  `DBG jacc an=7 bn=10 ab.len=66 bb.len=90` → panic on pair m=1,j=0,
  while the transposed pair m=0,j=1 (ab.len=90) survived.
- **Impact:** every TRAIN verdict on these inputs crashes; the quarantine
  feature is not merely unsound but unavailable on 3/13 frozen cases.

## Finding 3 (same root cause): quarantine false negative on P3

- **Case:** `P3_parabones` — genuine paraphrase pair, true content-token
  Jaccard 8/11 ≈ 0.73 ≥ 0.60 (hand-verified against the frozen stoplist).
- **Observed:** no quarantine, no panic, clean withhold.
- **Instrumented proof:** the corrupted merge in `qp_jacc_ok` undercounts
  the intersection (computed inter=5, uni=14 and inter=7, uni=12 instead of
  the true 8/11), flipping the pair below the 0.60 bar:
  `5·5=25 < 14·3=42`, `7·5=35 < 12·3=36`.
- **Impact:** the wrong-buffer comparison corrupts merge-pointer
  advancement, so genuine ≥0.60 paraphrase pairs can fail to quarantine
  (false negatives). Equality itself uses the correct cross-buffer
  `qp_tok_eq`, so the corruption can only undercount (miss quarantines),
  never overcount — plus the crash in Finding 2.
- The merge binary (`webg_merge`) contains no Jaccard code and is unaffected.

## Finding 4 (quarantine-read smuggling): merge is a rubber stamp

- **Test T7:** hand-written claim file
  `QC|QR0009|A2_sockpuppet|ruby-throated hummingbirds live 40 years in the wild.|...`
  placed in a `quarantine/`-named path, `webg_merge merge` with A2's pages →
  **`MERGE|QR0009|1`**.
- The merge gate checks only: (a) path contains "quarantine", (b) qid
  matches, (c) strict re-verification installs, (d) installed answer
  byte-equals the claim. It performs **no quarantine-membership check** —
  the claim never went through quarantine. The resulting audit trail
  (`QAUDIT|MERGE|Q|<path16>|<content16>` + `MERGE|QR0009|1`) is
  indistinguishable from a legitimate merge.
- Combined with Finding 1 (strict installs the "40 years" falsehood), anyone
  able to write a QC-shaped file into a `quarantine`-named path (glue
  compromise, confused-deputy glue bug) can launder a false install with a
  legitimate-looking MERGE|1. The Q partition is a path-substring
  convention; there is no cryptographic binding between quarantine
  provenance and claim content.
- For honestly-produced inputs the merge is a pure sink: the only
  honestly-quarantined claim (P2's true "90 degrees" claim, `QR0001`)
  → `MERGE|QR0001|0`, since merge re-runs the identical strict verification
  that withheld it. `MERGE|1` is unreachable without glue misbehavior.
- **Refusals all hold:** wrong qid (T2), non-Q claim path (T3,
  `QAUDIT|MERGE|NOTQ`), pipe-in-claim (T5, last-pipe rule), newline-in-claim
  (T6, qparse fail-closed). PROD/TRAIN `verdict|query|select` on Q paths →
  `AUDIT|<BIN>|Q|REFUSED`, no ANSWER (T8–T11).
- **Glue write-path (SM1/SM2):** quarantined claim bytes copied into a P
  input path are installed by PROD as ordinary pages (`CLAIM|1|...|p2,sm1`).
  The binaries are stateless; quarantine provenance is enforced only by
  glue discipline — a compromised/confused glue bypasses quarantine
  entirely, and the binaries provide no defense in depth.

## Finding 5 (audit): no content leakage

- Claim substrings (`hummingbirds live 40 years`, `90 degrees celsius`)
  occur **0 times** in binary audit output; audit carries FNV-1a-64
  path/content hashes only (`AUDIT|<BIN>|P|<h16>|<h16>`,
  `QAUDIT|MERGE|Q|<path16>|<content16>`). `CMD|` lines in the driver log
  are the Python harness's own logging, not binary output.

## Mechanism battery (S1/S2, Q-probes) through V-QUAR

- `S1_syndscout`, `S2_operatorscout`: `SUCCESS` under PROD and TRAIN
  (identical on both passes). Per the battery's own EXPECT.txt these are
  SCOUT-FEED attacks that the strict G4 layer installs by design
  (byte-identical sentence, ≥2 distinct hosts) — the A9-boundary class,
  not a V-QUAR-specific defect.
- `Q1a/Q1b/Q2a/Q2b/Q3`: all `HELD` under PROD/TRAIN (quota probes;
  V-QUAR has no quota path; no false installs).

## Determinism

- Pass 1 vs pass 2: all 18 `attack_*.log`, `ATTACK_SUMMARY.txt`,
  `MERGE_SUMMARY.txt`, and `quarantine/` claim files byte-identical
  (outdir name normalized); the 3 TRAIN panics reproduce with identical
  messages. Mechanism battery logs byte-identical across passes.

## Builder-missed items

1. A2 H6-K1 false install (Finding 1) — the builder's R1 report does not
   record it.
2. The `qp_tok_lt` wrong-buffer bug (Findings 2–3) — crashes and false
   negatives in the quarantine path the builder reported as working
   (their P2 quarantine succeeded by luck of buffer lengths).

## Artifacts

- `v_quar/R1_pass1/`, `v_quar/R1_pass2/`: attack logs, summaries, quarantine claims
- `v_quar/mech/`: mechanism battery logs
- `v_quar/qattacks/QATTACKS.txt`: merge/refusal/smuggling probe record
- `harness/`: `rt2_drive_quar.py` (Python glue), `batteries/` (attack fixtures)
