# NAMECHECK.md: TNN3H10 (H10 prereg: writing only)

Lane: TNN3H10, wave wave-20261001-2021pdt. Worker: subagent (depth 2/2).
Task: verify substrate in frozen tnn2.zag and write PREREG_H10.md (writing only; no computation, no binaries).

## Step 0: toolchain guard (mandatory before any work)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  - Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- Ran: `export PATH="$HOME/safebin"` then `which python3` -> printed NOTHING (exit 1).
  Also `which python` -> printed NOTHING.
- All subsequent commands run with safebin PATH. Any `muse.exec` uses the exported PATH above.

## Step 1: work order confirmed

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (verified `git rev-parse --abbrev-ref HEAD`).
- No git reset, no rebase, no commit (coordinator commits), no push.
- Writing ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H10/.
- Task is writing only: no implementation files, no binaries, no forbidden executables.
- Documentation rule: no em-dashes anywhere in lane files. Checked by grep before done.

## Step 2: frozen source identity

- Frozen source: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
- SHA-256 verified by worker: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (matches task instruction; 1591 lines).

## Step 3: substrate verification outcome (recorded in PREREG_H10.md)

- (a) Per-format selectors enumerated with quoted code and line numbers. Store
  already unified (one allocator, one node table, one edge table); readers are
  per-format. Load-bearing: cell ISA fields read by execute (192-215), fact
  (f20/f24/f28) keys read by the activate family, MAP (f4/f8/f20/f28) fields
  read by the revise path. Confirms H3's finding: three genuinely different
  structures, each read by the code that created them.
- (b) FAIL. No generic graph query mechanism exists; every content selector
  hardcodes its tag literal; zero-added-lines claim false.
- (c) FAIL, exhaustively. Event interface takes scalar payloads only
  (ev_teach/teach_in/query/observe/act); no node index, tag, field, or edge
  type accepted or exposed; link types are a fixed 13-value enum; the 4-op ISA
  has no alloc/link/edge ops; no learner entity exists in the frozen build.
- (d) Deletion set measured: about 371 body lines of format-specific
  selector/reader/writer code, all load-bearing per (a). The H10 "deletion
  set" (delete with zero added) is empty, same as H3 measured.
- Verdict: SUBSTRATE-ABSENT (fifth consecutive: H2, H3, H4, H6, H10).
  PREREG_H10.md is NOT-FROZEN. No bars frozen, no implementation authorized.
- Em-dash check: grep found none in lane files.
