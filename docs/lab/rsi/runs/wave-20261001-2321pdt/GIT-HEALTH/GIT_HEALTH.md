# GIT HEALTH: wave-20261001-2321pdt working copy

Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Checked 2026-10-02 ~00:50 PDT. HEAD moved twice during the check (concurrent workers committing); final HEAD d9751df2d FINAL-SUMMARY.

## Verdict: INDEX DEGRADED, not corrupted

The git object store is healthy and no tracked file is missing or modified.
But the index (the tracked file set) lost ~55,500 files: only `docs/` (6,369 files)
is tracked now. Everything else in the working tree (src/, archive/, artifacts/,
data/, .github/, .gitignore, LICENSE, README.md, LOOP_STATE.md, units, and more)
is untracked. Cause identified below. The repair is a coordinator decision; this
lane changed nothing.

## Findings

1. Status breakdown: `git status --porcelain` shows 282 entries, all `??`
   (untracked), zero modified, zero staged, zero deleted. `git status --porcelain
   -uall` counts 140,546 untracked files. Tracked files: 6,369, all under docs/.

2. Root commit (48bc97c30) tracked 61,901 files across .github, .gitignore,
   LICENSE, README.md, archive, artifacts, data, docs, src, units. So the
   shrink from 61,901 to 6,369 tracked files happened inside this branch's history.

3. The deleting commit is f461e812d (H5R2-SKEPTIC2 implementation,
   wave-20261001-2321pdt): it deleted essentially the whole tracked tree outside
   docs/. WAVE_RECORD.md already notes this incident: that worker's commit
   accidentally deleted BATTERY-E4/PREREG_E4.md and NAMECHECK.md (411 deletions,
   restored byte-identical), but the same commit also dropped the top-level
   non-docs entries from the index. `git diff --stat f461e812d^ f461e812d`
   shows 147,298 files changed with 39,880,155 line deletions: a mass deletion,
   not a handful of files. Likely cause: the worker ran `git add -A`
   from a subdirectory or a staging operation that recorded deletions for
   everything it did not re-add.

4. Working-tree data is intact. The deleted-from-index files still exist on disk:
   src/zag, src/tools/toolchain, archive, artifacts, data all present and readable.
   Because they show as untracked rather than deleted, nothing needs recovery
   from objects; the content is where it was.

5. WAVE_RECORD.md: tracked at docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md,
   byte-identical to HEAD (git diff shows no change). It carries the verdict
   bullets: 55 bullet lines in the Verdicts section, matching the FINAL-SUMMARY
   count of 47 verdicts plus housekeeping notes. Not affected by the incident.

6. Recent commits in HEAD: cad168d3a (DEBATE.md, 8 rulings) and f90cdd8a0
   (Queued next, 12 items) are both ancestors of HEAD. Confirmed by merge-base
   check. The debate and queue records are safe.

7. No silent data loss beyond the index. `git fsck` not run (not needed for this
   diagnosis); the object store serves every requested object normally.

## Impact

- Any lane that assumes the full tree is versioned (freeze provenance, sealed
  evaluators referencing src/ paths via git show, reproducibility from committed
  sources) now references files git does not track. The frozen-binary
  provenance claims cite commit hashes of implementation sources; those sources
  are on disk but no longer under version control.
- Future `git add -A` runs by workers could either re-add 140k files (index
  bloat) or, worse, a worker that does `git commit -a` in the wrong directory
  could repeat the mass deletion.

## Recommendation to the coordinator

1. Do not let workers repair this ad hoc. Decide the intended tracked scope:
   (a) restore the pre-incident scope (re-add the non-docs top-level entries
   that still exist on disk), or (b) formally narrow the repo to docs/ with a
   recorded ruling and move src/ and other code trees to their own repo or
   bundle. Given the freeze/provenance requirements, option (a) is the safer
   default until a ruling says otherwise.
2. The repair commit should be made by one trusted operator, verified with
   `git ls-tree` before and after, and recorded in the wave ledger.
3. Add a standing guard: workers commit only under their lane directory with
   explicit pathspec (already the rule); add a pre-commit sanity check that
   refuses commits deleting more than a small threshold of files without an
   explicit override flag.
4. The H5R2-SKEPTIC2 worker's git workflow needs review (already flagged in
   WAVE_RECORD.md); extend that review to how the mass deletion happened so the
   guard targets the actual mechanism.

Lane performed no git reset, no git clean, no destructive command. Diagnostics
only, shell git/file ops, pure safebin toolchain, no python3 present.
