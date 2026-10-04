# NAMECHECK: Mini-Lifetime Designer

## Step 0: Toolchain guard (mandatory)

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

Result: `which python3 python` returned empty. No Python or forbidden
interpreter in PATH. Guard PASS.

Scope: DESIGN ONLY. No Zag code written, no binary built, no experiment
run, no sealed worlds opened or created. All shell use was read-only
file inspection (`sed`, `grep`, `ls`) plus git operations.

## Step 1: Input provenance

This design is derived from, and cites exactly:

- Micah directive 2026-10-01 (mini-lifetime instruction, consequence-driven
  adaptation target, H3-lite separation, weak/strong K-LT-5 split).
- `lifetime_protocol/LIFETIME_PROTOCOL_V2.md` (DRAFT-NOT-FROZEN, 1225
  lines): two-track structure (Sec 3), world designs A/B/C (Sec 4),
  trial-must-run rule (Sec 4.1), procedure (Sec 5), instrumentation
  (Sec 6), eight measures (Sec 7), E() rules (Sec 9), kill bars (Sec 11),
  honest TNN-2 assessment (Sec 13), freeze requirements (Sec 16),
  banked decisions D1-D5 (Sec 19).
- `lifetime_scope/LIFETIME_SCOPE.md` (commit dffbdbbe7): saturation
  arithmetic, per-world node budgets, the three-world mini proposal
  (Sec 3), TNN-3 requirements (Sec 4), D3 reuse-path note (Sec 5).
- `tnn2_reusepath/REUSE_PATH_DESIGN.md` (NOT IMPLEMENTED): the minimal
  reuse path (MAP-first query, shadow-teach deletion, liveness,
  contradiction retargeting, most-recent selection), honest prediction
  of unchanged scores (Sec 6.3), draft K-REUSE-1/K-REUSE-2 bars (Sec 7).
- Frozen TNN-2 build identifier f4de7ff46 (per protocol Sec 19 D3).

## Step 2: What this task does and does not do

DOES: produce a complete, freezable design for the mini-lifetime causal
experiment: builds, worlds, procedure, controls, measures, kill bars,
the A-vs-B primary comparison, and the two-part reporting structure
(MINI-LIFETIME RESULT vs FULL-LIFETIME FEASIBILITY).

DOES NOT: implement the reuse-path variant, generate or seal any world,
run any learner, freeze the protocol, amend any frozen prereg, or touch
the research paper.

## Step 3: Constraints honored

- Design only. Zero em dashes and zero en dashes in both files
  (verified by byte scan before commit).
- Paper untouched:
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not read, not modified.
- Nothing pushed. Commit stays local on branch tnn-native-lab.
- No sealed worlds opened or created.
- Explicit pathspecs on both `git add` and `git commit`
  (the post-collision convention).
