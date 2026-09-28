# PAM REBUILD — Fork-build prereg skeleton (per-fork PREREG frozen BEFORE results)

Each builder crew copies this skeleton, fills in its hypothesis ID and
hypothesis-specific fixture/augmentation notes, and commits its PREREG alone
before any build output exists.

## 1. Hypothesis under test
ID: <H1|H2|H3|G1|G2|G3> (verbatim text in ../../HYPOTHESES.md — do not paraphrase)

## 2. What is built
- Pure-Zag percept pipeline implementing the hypothesis's percept format.
- The MEMORY CONTRACT as executable code: the exact install/withhold/retrieve
  rules from the hypothesis, wired to a deliberate-memory install gate.
- A `sense` CLI: fixture bytes in → percept records + install/withhold
  dispositions out, with hash-chained ledger.

## 3. Fixtures
- Base: the frozen rebuild harness fixtures (`senses/rebuild/harness/fixtures`,
  MANIFEST.sha256) — the same 6 tasks (colordisc, colorconst, shapetrans,
  pitchdisc, timbredisc, motiondir).
- Adversarial augmentation (KB4-targeted): ≥30% deliberately misleading
  high-confidence inputs, per the hypothesis's kill bar. Augmentation set is
  frozen in the PREREG (list fixture IDs + corruption method).

## 4. Bars (all preregistered, applied mechanically)
- B1 viability: mean accuracy ≥ 60% (the bar that killed B).
- B2 vs Approach A: head-to-head accuracy delta on identical fixtures.
- B3 efficiency: ops and bytes per percept vs Approach A (measured, not asserted).
- B4 memory-contract proof (LOAD-BEARING): ablate the contract — run the same
  percepts through a contract-less install gate. The fork PASSES B4 only if the
  contract changes downstream install/withhold decisions on ≥10% of adversarial
  fixtures AND reduces false installs vs the ablated run. A percept pipeline
  whose contract never changes a decision is decoration → fork FAILS.
- B5 KB4: adversarial false-install rate ≤ 10% (the bar both A and B failed).
- B6 determinism: ≥3 runs byte-identical, hash-chained ledger verified.
- B7 beauty: (i) mechanism elegance — one idea doing the work of many, judged
  against the hypothesis's own beauty claim; (ii) output quality — artifacts
  (audio clips / visual renders where the fork produces them) presented for
  Micah's ear/eye verdict with the brief attached. Human senses outrank metrics.

## 5. Kill criteria
The hypothesis's own kill bar from HYPOTHESES.md, applied verbatim, PLUS:
fork dies if B4 fails (contract is decoration) or B6 fails (non-determinism).

## 6. Commit map
`senses/pam-rebuild/forks/<ID>/`: PREREG_<ID>.md (alone first), src/, evidence/,
LEDGER.md. Branch `tnn-native-lab`, repo `sylorlabs/TNN`.
`~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=~/workspace/tmp_commit.
No binaries, no .zagd. Verify via GitHub API, report SHAs.
