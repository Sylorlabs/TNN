# NAMECHECK: Full Theater Ablation Experimenter

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

Empirical ablation of theater audit instances T1, T2, T3, T4, T6
(`e0423538a`). T5 (UNCERTAINTY) already confirmed by `408bcfaa5`; not
re-tested here.

## UNFROZEN VARIANT declaration

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  verified before copying and verified unmodified after (same hash; frozen
  binary `tnn2_bin` also unmodified).
- `theater_base.zag`: verbatim copy of frozen source (SHA-256 identical).
- `theater_full.zag`: `theater_base.zag` with the original test `main`
  (line 1357) removed and `theater_driver.zag` appended. Cognition code
  untouched.
- `theater_bin`: compiled from `theater_full.zag` with the pinned znc.

## Ablation methods (per instance)

- **T1 (MISS_POLICY node 1, tag 901, DEAD):** `t1_ablate` zeroes tag
  (field 0) and field 20 of node 1 in place. Slot kept occupied (live=1)
  so allocation order is unchanged. Tests: does any production behavior
  depend on the MISS_POLICY node?
- **T2 (P-INV threshold tag 903, READ-ONLY):** No destructive ablation;
  the theater is the absent write path. `t2_check` reads the tag-903
  node's field 20 after a battery containing bootstrap events. Expect 3
  (unchanged). Additionally verifies bootstrap actually ran (threshold was
  consulted), proving the read path is real and the classification is
  READ-ONLY (not DEAD).
- **T3 (trial stats header 16, WRITE-ONLY):** `t3_ablate` zeroes header
  field 16 (`hs(W,16,0)`). Tests: does any production behavior depend on
  recorded trial statistics?
- **T4 (event log header 28 + ls storage, WRITE-ONLY):** `t4_ablate`
  resets the log count (`hs(W,28,0)`). Old entries beyond the count are
  never read. Tests: does any production behavior depend on the event
  log contents?
- **T6 (eviction history tag 3 + header 12, WRITE-ONLY):** `t6_ablate`
  resets the chain head (`hs(W,12,-1)`, the init value) and zeroes any
  live tag-3 nodes in place. Also records whether the chain was empty
  before ablation. Tests: does any production behavior depend on eviction
  history?

## Battery design

Six learners (WA control, WB T1, WC T2, WD T3, WE T4, WF T6) in one
deterministic binary. Identical call sequence; ablations applied at the
midpoint. Battery covers: teaches, exact query hits, masked misses (trial
path), chain promotion (MAP), action selection, guide queries,
contradiction + revision, observations, and bootstrap scenarios (3+
unanimous facts with same r/o, then masked query on new subject).
Every return value emitted with learner prefix. Comparison strips prefix
and ablation-diagnostic lines, diffs the streams.

## Input provenance

- Theater classifications: `theater_audit/THEATER_AUDIT.md` (commit
  `e0423538a`), instances T1-T6.
- T5 precedent: `t30_ablation/T30_ABLATION.md` (commit `408bcfaa5`),
  62/62 identical, theater CONFIRMED.
- Battery patterns follow `t30_ablation/t30_driver.zag` and
  `state_dynamics/sd_driver.zag` (commit `ee238d8d4`).
- Unsealed synthetic subjects only. No sealed H2/FW/W content opened,
  listed, or hashed.

## Constraints honored

- Frozen source and binary untouched (hashes re-verified at end).
- UNFROZEN VARIANT ONLY for the experiment.
- Determinism: 3/3 byte-identical runs required.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commit only, explicit pathspecs.
