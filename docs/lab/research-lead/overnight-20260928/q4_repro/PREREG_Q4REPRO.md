# Preregistration: Q4 F-PARCOND Independent Reproduction

## Objective
Independently reproduce the F-PARCOND BUILD-PASS result from committed source (commit 5f56cc491), per promotion pipeline step 4.

## Source
- Commit: 5f56cc491
- File: docs/lab/research-lead/overnight-20260928/q4_parcond/q4_parcond.zag
- Method: `git show 5f56cc491:<path>` to extract source; do NOT copy from working tree.

## Protocol
1. Extract source from commit 5f56cc491 via git show.
2. Compile with znc toolchain.
3. Run 3 times, capture stdout/stderr.
4. Verify: exit 0, 3/3 byte-identical, md5 matches reported e9be97dd8a0c8428ce4f616e087a6433.
5. Verify: content matches committed Q4PARCOND_RAW_1.txt.

## Kill Bars
- K1: Source checked out from commit (not working tree).
- K2: Reproduction matches (md5, results, content).
- K3: Pure Zag (znc, shell only), no Python, no em dashes.

## Expected Results (from 5f56cc491)
- md5: e9be97dd8a0c8428ce4f616e087a6433
- Content: Q4-PARCOND header, P1 64/64 true, P2 reuse 0 vs scratch 24, KB3 1, DONE.
- Exit 0, zero stderr, 3/3 byte-identical.

## Governance
- Pure Zag only. No Python anywhere.
- No em dashes in committed files.
- Commits local, owned path q4_repro/ only.
- Use pathspec commits: `git commit -- <path>`.
