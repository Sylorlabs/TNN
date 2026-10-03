# NAMECHECK: BELIEF-PROVENANCE 1 (evidential adjudication)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance/`
Worker: BELIEF-PROVENANCE subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-1: the learner adjudicates
between two conflicting grounded structures using a learned
evidential meta-table, with STANDARD/REVERSED/NOMETA arms.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: the documented setup script path
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  did not exist; `~/safebin` was already provisioned with the 36
  allowed tools (awk basename bash cat chmod cmp comm cp cut date
  diff dirname echo file find git git-receive-pack git-upload-pack
  grep head join ln ls mkdir mktemp mv nl od paste printf rm sed
  sh sha256sum sleep sort stat strings tail tee timeout touch tr
  uname uniq wc which xargs znc). `export PATH="$HOME/safebin"`.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc resolves via the safebin symlink to the pinned toolchain:
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path).
- Shell used only for: znc invocation, binary execution, git ops,
  file movement, sha256 checks. All scientific computation in pure
  Zag.
- Git discipline: explicit pathspecs only; commits local, never
  push; never `git reset`; never amend shared history; never
  modify other lanes. Other workers have staged/unstaged changes
  on this branch; this worker touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance/`.
  If git writes fail with EPERM through the safebin symlink,
  retry via `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03).
- Zag pitfalls honored: no `as *i32` + slice construction in
  functions (u8-backed state, get32/set32 helpers); no
  `_zag_print` for dynamic output (single preallocated output
  buffer + one `_zag_raw_syscall` write, `_zag_slice_ptr` for the
  pointer); no reliance on `.len` of `as []f64`/`as []i64` casts;
  `if` nesting at most 3; no `!(A && B)` in while conditions
  (De Morgan form); hash-only dedup then linear scan if any
  table is needed; `[]u8 as *u8` never used (thread
  `_zag_malloc as *u8` via z_alloc).
- No em/en dashes in any lane file (byte-verified with grep -P
  before each commit).

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation file
  exists in this lane. This NAMECHECK.md Step 0/1 recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this file).
- Implementation (bp_learner.zag, bp_world.zag, bp_driver.zag)
  comes in a LATER commit, strictly after this one.

## Step 2: implementation (done, commit follows prereg commit 21dce2653)

- Files: bp_learner.zag (461 lines: state, facts, MAPs with
  corr/rev, bp_observe, edges 14/15/16, meta-table,
  bp_adjudicate, bp_explore, bp_confirm, bp_deliver),
  bp_world.zag (10 lines: schedule constants), bp_driver.zag
  (333 lines: 3 arms + in-driver bars K-2..K-6, K-8).
- Built: `cat bp_learner.zag bp_world.zag bp_driver.zag >
  bp_full.zag`; pinned znc by absolute path, build exit 0, no
  warnings -> bp_bin (90573 bytes; log: bp_compile.txt).
- No Python/C/JS/Rust invoked at any point. Safebin PATH held
  for the whole session. `which python3` / `which python` still
  empty.
- No em/en dashes in any lane file (byte-verified with grep).

## Step 3: runs + REPORT.md (done)

- 3/3 runs byte-identical: sha256
  e6de43ad657a826243b9ca86f70cb9a329b7813088c234347cdceb152b3b39e0
  for bp_run1/2/3.txt (K-1 PASS).
- In-driver bars K-2, K-3, K-4, K-5, K-6, K-8 all PASS=1.
- Shell K-7: 2 total ANS lines (via=20 val=202 line 197,
  via=21 val=204 line 399); 0 ANS in NOMETA section; ADJ-WIN
  win=20 once, win=21 once; STANDARD ep0 EXPLORE-TRY HIT (17)
  before META-ROW r=0 (18); REVERSED ep0 MISS (218), HIT (219),
  META-ROW (220).
- REPORT.md written with verdict BP-1-PASS.
- Committed with explicit pathspecs, local only, never pushed.
- Ledger: to be recorded as C397 (ledger file untouched;
  another worker has staged changes there).
