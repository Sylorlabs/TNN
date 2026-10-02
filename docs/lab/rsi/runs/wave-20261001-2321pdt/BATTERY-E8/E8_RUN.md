# E8_RUN.md -- Orthogonal-signal ACT bandwidth probe execution report

Wave: wave-20261001-2321pdt, lane BATTERY-E8.
Prereg: PREREG_E8.md, frozen alone at commit 034ecbd35, SHA-256
aa5f09a9d02902c482d1108bc2c53ac9abf82bb916c203c5a6e7b184448d071b
(re-verified unchanged from git at run time: `git show 034ecbd35`
hashes to the same value; runner E8-K1 check HASH-OK). All work
pure Zag (pinned znc) and shell under PATH=$HOME/safebin; no Python
invoked (Step 0 verification in NAMECHECK.md: `which python3` and
`which python` both print nothing). TNN-2 frozen; no source edits.

## Process bars

- E8-K1 (prereg ordering): PASS. Prereg committed alone
  (034ecbd35) before implementation (eb854c45d) and before any
  run; SHA-256 re-verified unchanged by the runner.
- E8-K2 (determinism): PASS. 3/3 byte-identical transcripts per
  world; each transcript contains exactly one CHOICE line.
- E8-K3 (frozen binary): PASS. freeze_shim2_bin and tnn2.zag
  match section 0 hashes before the first run and after the last.
- E8-K4 (seal integrity): PASS. E8_MANIFEST.sha256:
  - 7e625dcbdcc27354c01356b02d092b5aeff8fb3499cc117adcf842498589ac34  e8_a_world.txt
  - 7c992e0a3b1e3c7f2e10dfc4cd0bc776aecf34335842653e9968dc7b1fb0f37f  e8_b_world.txt
  - 8c0222254050b10cc247418dfecc1424c6dd0326480b413632adad57bc380d87  e8_c0_world.txt
  - 427e592b69d30ea83628e510e0abce23e08a6feb3fadc149f8434698c0031c81  e8_c1_world.txt
- E8-K5 (block calibration): PASS. E8-C0 yields CHOICE 0,
  E8-C1 yields CHOICE 0, E8-A yields CHOICE 30 on all 3 runs each.
- E8-K6 (no leak): PASS. E8 id set returns zero matches in the
  frozen cognition sources (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS.
  (1) e8_worldgen.zag contains no id-conditioned or
  value-conditioned branching (grep for id-conditioned
  `if`/`while` returns zero matches); its if/while constructs are
  generic buffer, path, and argc helpers; world ids appear only
  as the exact prereg section 2 stream emissions.
  (2) e8_run.sh performs no transcript transformation and no
  logic keyed on world ids, subjects, relations, or CHOICE
  values beyond the byte comparison required by the prereg
  section 3 decision rule and the E8-K5 literal gates; world
  selection is a loop over the four world letters.
  (3) grep for python across the lane finds only the Step 0
  guard documentation in NAMECHECK.md; no invocation occurred.

Corroborating determinism note: e8_c0_r1.trans
(65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d)
is byte-identical to the E2 lane's e2_d_r1.trans (empty-state ACT
in a different id block and a different lane), confirming the
frozen binary is deterministic across lanes, not just within them.

## Per-run evidence (transcript SHA-256)

E8-A (content A: single miss on 84001/84101, ACT immediate):
- e8_a_r1.trans: ab3497b07e31be0e7d16db4385d293407cc666e732cbe3fecef8c7cc66d93509
- e8_a_r2.trans: ab3497b07e31be0e7d16db4385d293407cc666e732cbe3fecef8c7cc66d93509
- e8_a_r3.trans: ab3497b07e31be0e7d16db4385d293407cc666e732cbe3fecef8c7cc66d93509

E8-B (content B: miss on 84002/84102, three taught+hit pairs, ACT):
- e8_b_r1.trans: 7ebd471f19634b532896fa8c7de351f9ec054d5d65e39f7e3c23fce0e15746b3
- e8_b_r2.trans: 7ebd471f19634b532896fa8c7de351f9ec054d5d65e39f7e3c23fce0e15746b3
- e8_b_r3.trans: 7ebd471f19634b532896fa8c7de351f9ec054d5d65e39f7e3c23fce0e15746b3

E8-C0 (degenerate: ACT on empty state):
- e8_c0_r1.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d
- e8_c0_r2.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d
- e8_c0_r3.trans: 65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d

E8-C1 (post-hit control: OBSERVE then QUERY hit, ACT):
- e8_c1_r1.trans: 839697984f57b3e4b4df366a749bda1955b4965f5b1f2eff5895e888bf6f705a
- e8_c1_r2.trans: 839697984f57b3e4b4df366a749bda1955b4965f5b1f2eff5895e888bf6f705a
- e8_c1_r3.trans: 839697984f57b3e4b4df366a749bda1955b4965f5b1f2eff5895e888bf6f705a

## Transcripts (run 1 of each; runs 2 and 3 byte-identical)

E8-A:
```
WORLD_BEGIN
ANSWER 84001 84101 -2
CHOICE 30
WORLD_END events=2 answers=1
STATE_SAVED
```

E8-B:
```
WORLD_BEGIN
ANSWER 84002 84102 -2
OBSERVED 84003 84103 84013
ANSWER 84003 84103 84013
OBSERVED 84004 84104 84014
ANSWER 84004 84104 84014
OBSERVED 84005 84105 84015
ANSWER 84005 84105 84015
CHOICE 0
WORLD_END events=8 answers=4
STATE_SAVED
```

E8-C0:
```
WORLD_BEGIN
CHOICE 0
WORLD_END events=1 answers=0
STATE_SAVED
```

E8-C1:
```
WORLD_BEGIN
OBSERVED 84021 84121 84031
ANSWER 84021 84121 84031
CHOICE 0
WORLD_END events=3 answers=1
STATE_SAVED
```

## Decision rule outcome (prereg section 3, frozen)

Observation channel: the single CHOICE line per transcript.
CHOICE(E8-A) = "CHOICE 30"; CHOICE(E8-B) = "CHOICE 0",
byte-identical across all 3 runs of each world. The two CHOICE
lines differ as byte strings.

Signature: SIGNATURE-BANDWIDTH-SUFFICIENT.
Verdict: E8-BANDWIDTH.

Reading per the frozen task mapping: with guide presence held
constant (exactly one live guide, no concurrency, no resolution in
either world), the actions differentiate by guide content when the
output channel can express the correct-action difference (30 for
the actionable in-context guide vs 0 for the non-actionable aged
guide; the {0, 30} repertoire demonstrably expresses both per the
E8-K5 calibration). H2d is confirmed as a contributing cause:
output bandwidth is in the causal chain of whether guide-content
differences manifest behaviorally.

## Mechanistic interpretation (separate from the verdict)

Read-only white-box reading of the frozen shim (no source edits;
this is interpretation, not the verdict, which follows the frozen
rule above):

- The ACT operator returns the winning candidate's stored action
  code; guide nodes are constructed with that code fixed at 30;
  candidacy requires the guide's content key (the missing
  subject) to match the current 4-context. The
  protocol-reachable vocabulary is therefore {0, 30}, and E8's
  30-vs-0 difference was carried by the candidate-selection
  stage, not by a richer emission vocabulary.
- Guide presence cannot explain the E8-A/E8-B difference: both
  worlds hold exactly one live guide with no concurrency and no
  resolution, so the presence bit is identical. The difference is
  content-driven (the guide's contextual actionability).
- This refines E2's H2a rather than contradicting it: E2's
  instrument (two single guides, both actionable and in-context,
  differing only in missing subject and surrounding resolved
  facts) showed no content reaching; E8's instrument shows
  content in the form of contextual actionability does reach
  action selection. H2a's strong form ("content never reaches
  action selection in any form") does not survive E8; the
  precise surviving claim is that subject-identity content of an
  actionable guide does not differentiate the emitted action.
- On H2d's literal form ("the operator lacks the bandwidth"):
  the {0, 30} channel proved sufficient for this content
  difference, so output coarseness did not suppress it here.
  The frozen-rule verdict (E8-BANDWIDTH) stands as specified;
  the mechanism says bandwidth sufficiency, not bandwidth lack,
  is what the experiment demonstrated.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8/PREREG_E8.md
  (commit 034ecbd35, SHA-256
  aa5f09a9d02902c482d1108bc2c53ac9abf82bb916c203c5a6e7b184448d071b)
- Tools: e8_worldgen.zag, e8_worldgen_bin, e8_run.sh (commit eb854c45d)
- Worlds and manifest: e8_worlds/ (E8_MANIFEST.sha256)
- Transcripts: e8_runs/ (per-world per-run .trans, per-run .bin state)
- Transcript hashes: e8_runs/E8_TRANS_SHA256.txt
