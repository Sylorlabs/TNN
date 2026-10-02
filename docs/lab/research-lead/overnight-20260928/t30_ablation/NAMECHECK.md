# NAMECHECK: T30 Ablation Experimenter

## Step 0: Toolchain guard (mandatory, recorded)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
  git-receive-pack git-upload-pack).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returned NOTHING. Zero forbidden executables invoked
  in this wave. All computation in Zag (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`); shell used only to invoke
  znc, run the binary, git ops, move/copy files.

## Scope

Empirical test of the ignorance-dedup prediction (`8510e327b`): ablating
every T30 UNCERTAINTY node changes zero production behavior.

## UNFROZEN VARIANT declaration

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  verified before copying and verified unmodified after (same hash; frozen
  binary `tnn2_bin` also unmodified).
- `t30_base.zag`: verbatim copy of frozen source (SHA-256 identical).
- `t30_full.zag`: `t30_base.zag` with the original test `main` (line 1357)
  removed and `t30_driver.zag` appended. Cognition code untouched.
- `t30_bin`: compiled from `t30_full.zag` with the pinned znc.

## Ablation method

`t30_ablate`: for each live node with tag 30, zero tag and fields
4/20/24/28/32 in place; slot kept occupied (live=1) so later
`alloc_node` order and node indices are unchanged across both learners.
This is the "zero them" form named in the task. Rationale: it removes
the nodes from every production scan while holding allocation order
constant, so any behavioral divergence would be a real causal effect
of the T30 nodes, not an index artifact.

## Input provenance

- Prediction under test: `ignorance_dedup/IGNORANCE_DEDUP.md` (commit
  `8510e327b`), Section 2d: "ablating every T30 node from a live
  learner would change zero production behavior."
- Theater classification: `theater_audit/THEATER_AUDIT.md` (commit
  `e0423538a`), T5: UNCERTAINTY nodes are write-only.
- Battery call sequences follow the proven patterns in
  `state_dynamics/sd_driver.zag` (commit `ee238d8d4`).
- Unsealed synthetic subjects only (1000s, 2000s, 7000s, 9100s, 9200s).
  No sealed H2/FW/W content opened, listed, or hashed.

## Constraints honored

- Frozen source and binary untouched (hashes re-verified at end).
- UNFROZEN VARIANT ONLY for the experiment.
- Determinism: 3/3 byte-identical runs
  (`ac9576f78363062f41697f89d3a2db9e51c9ee93be05cad3b8737dcb8d66c744`).
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commit only, explicit pathspecs.
