# NAMECHECK: Learned Similarity Analyst

## Step 0: Toolchain Guard

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing (only "guard-check-done"
printed). Safebin active at `$HOME/safebin`. `znc` resolves to
`/home/hatch/safebin/znc`. Zero forbidden executables invoked during
this task.

## Scope

ANALYSIS ONLY. No implementation, no source edits, no binaries built,
no evaluators run.

## Input provenance

- Usability gap analysis `2c4ca4e3a`
  (`docs/lab/research-lead/overnight-20260928/usability_gap/USABILITY_GAP.md`):
  retrieval sub-problem, treadmill risk HIGH, "honest version is LEARNED
  similarity, which doesn't exist."
- Barrier-break design `f0f223029`
  (`docs/lab/research-lead/overnight-20260928/barrier_break/BARRIER_BREAK_DESIGN.md`):
  four barriers, barrier 3 is similarity retrieval.
- Xfer experiment `cbd7bc803`
  (`docs/lab/research-lead/overnight-20260928/xfer_experiment/XFER_EXPERIMENT.md`):
  zero transfer, domain A (subjects 1-5, relations 11/40) vs domain B
  (subjects 100-104, relations 61/60), isomorphic, disjoint namespaces.
- Barrier implementation `d7a62ea34`: visibility counters `hg(W,56)` /
  `hg(W,60)`; descriptors dead on arrival in `t2_gather`.
- Frozen `t2_sig` source read (read-only grep/sed):
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  lines 511-533. Records (tag, literal) per cell for tags 101-104,
  including literals for tags 101/102. Literal-contaminated.
- H2 evaluation void `72173fe11`: t2_sig calibration failed on
  literal-inclusion property.
- Micah's protected-core ISA ruling (2026-09-30, from standing context):
  forbidden as protected semantic operations include FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL. No core operation may encode a target-domain
  regularity detector.
- SUF criterion `7dddf3933` (from standing context): structural decision
  must read learner state, have exercised production write path, depend
  on learner history, change under ablation, produce non-enumerable form.

## Constraints honored

- Analysis only. Frozen source read, never modified (read-only
  grep/sed viewing).
- No sealed worlds opened (H2A/H2B/H2C untouched; FW worlds untouched).
- Zero em dashes (byte-verified before commit).
- Paper untouched:
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not read, not modified.
- Nothing pushed. Local commit only, explicit pathspecs, owned
  directory only.

## Verdict

LEARNED-SIMILARITY-COMPLETE.
