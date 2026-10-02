# NAMECHECK: sequential_revision (Sequential Revision Worker)

## Step 0: toolchain guard (mandatory, recorded)

Executed at worker start, 2026-10-02:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned NOTHING (no output before
"guard-check-done"). PATH restricted to $HOME/safebin only (49 tools).
No forbidden executable invoked at any point in this lane. build.sh
re-verifies the guard at build time (exits 1 if python3/python resolve).

Toolchain lessons honored (AGENTS.md): u8-backed state cells with
little-endian get32/set32 (no `as *i32` slice construction); all dynamic
output formatted into ONE preallocated buffer via cursor-returning emit
helpers with a single `_zag_raw_syscall(1,1,ptr,len,0,0,0)` write
(no _zag_print for dynamic content, 7-arg form per compiler); no
`as []f64` casts; no WAV reads. Recursion verified working in this znc
build (scratch test) before use in the nested rule renderer.

## Step 1: prereg frozen alone

PREREG.md (K-SR-1..K-SR-5, frozen predictions P1..P12) committed ALONE
strictly before any implementation source existed. Commit-order
self-check: the prereg commit is an ancestor of the implementation
commit and its tree contains exactly one file
(docs/lab/research-lead/overnight-20260928/sequential_revision/PREREG.md),
verified by `git show --stat` on the prereg commit.

Shared-repo index caution (learned from rule_revision lane): after every
commit, verify `git show --stat HEAD` holds only this lane's files;
use explicit single-file pathspecs for the prereg commit.

## Step 2: implementation (pure Zag, safebin only)

- sr_mech.zag: output helpers, u8 state cells, world facts (D_true,
  two kind laws W1/W2, world_change switch), obs log, tree node pool,
  rule_induce (generic CONSTANT induction), rule_pred (tree walk),
  learner_refute (generic chain blame walk), boundary_search (generic
  downward active inquiry), learner_refine (generic smallest-mispredicted
  leaf re-split), rule rendering (recursive, depth-capped), TREE-DUMP.
- sr_main.zag: driver; phases TEACH, Z2, REFUTE-1, REVISE-1, RETEST-1,
  REGRESS-1, GENERALIZE-1, WORLD-CHANGE, Z3, REFUTE-2, REVISE-2,
  RETEST-2, REGRESS-2, GENERALIZE-2, PRESERVE-CHECK; main().
- sr_full.zag: assembled (cat mech main).
- build.sh: guard + kill-bar source checks + compile + 3x run.

## Step 3: build

`znc sr_full.zag -o sr_bin`, exit 0 (compile.txt). Build notes: the
first build rendered nested leaves as ALWAYS(kind)
(IF(in<33,ALWAYS(NODE),ALWAYS(NUM))), mismatching the frozen notation;
fixed as a display-only change in the recursive renderer (nested
leaves render as bare kinds; root leaf still ALWAYS(kind)). No logic
change. The one `as *i32` grep hit was a code comment; reworded.
sr_bin sha256:
22229d61bfc343545346e6a23954f9ad6bc30203b8d1f4caae949447a56deeb0.
sr_full.zag sha256:
065dd7ed83ddd5d70f88cc9d9a4229a1d2fd2a9120fdeb1f195ea7bfd286e57f.

## Step 4: runs

run1.txt, run2.txt, run3.txt all exit 0. sha256 (all three):
025f3b6a78a8cca7652d4016ed57c47081a4a86a62d270dc30cc2ce872022921.
cmp pairwise: identical. DETERMINISM-OK: 3/3 byte-identical.
12/12 frozen predictions matched (see REPORT.md). 40 transcript
lines, 15 MATCH, 0 MISMATCH.

## Step 5: kill-bar source checks (from build log)

- grep -ci 'expected' over both sources: 0, 0.
- gate/E write sites: 2 (world_init init + world_downstream latch);
  0 set32(E inside learner_refute/boundary_search/learner_refine.
- `fn learner_refute`, `fn boundary_search`, `fn learner_refine`,
  `fn rule_induce`, `fn rule_pred`: 1 definition each.
- node-cell writes (nset): 11 total = 1 definition + 2 inside
  rule_induce + 8 inside learner_refine; 0 in the driver.
- learner_refute / boundary_search / learner_refine bodies contain
  none of the literals 31,32,33,34,40,50,60,66,67,70,80 (build.sh
  sed-scoped grep returns 0,0,0); revision content comes only from
  the ce cells and the observation log; driver calls pass no values
  (learner_refute(L,E), boundary_search(L,E), learner_refine(L)).
- exception machinery occurrences: 0, 0. No lookup list exists.
- mode/bridge/handler occurrences: 0, 0.
- `as *i32` occurrences in code: 0, 0.
- Unseen-input check: zero probe lines (OBS, REFUTE link, SEARCH
  trail) mention 40, 60, 50, or 80 (build.sh check returns 0).
- Preservation text checks: [0:split T=33 L=1 R=2] and [1:leaf NODE]
  in both TREE-DUMP lines (2, 2); REVISE-2 after-rule exact (1).

## Step 6: commits (explicit pathspecs, local only, never pushed)

- 8d54c2d7e: PREREG.md alone (frozen before implementation).
- dc4bf7d3f: implementation: NAMECHECK.md, REPORT.md, sr_mech.zag,
  sr_main.zag, sr_full.zag, build.sh, sr_bin, compile.txt,
  run1/2/3.txt, sha256sums.txt (12 files, explicit pathspecs).
