# T2-BUGREAD — RUNLOG.md

**Crew:** T2-BUGREAD (REPLACEMENT — predecessor killed mid-run by runtime daemon restart 2026-09-22/23)
**Session:** 643929b3-35e7-4ea3-b395-f6c80222bd94
**Started:** 2026-09-22 21:38 PDT (task received)
**Run dir:** `~/workspace/scratch-crossref/T2/BUGREAD/crew/`
**Clean dir:** `~/workspace/scratch-crossref/T2/BUGREAD/clean/`
**Type:** A (full independent rerun)
**Toolchain:** `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Inherited state (predecessor)

- Predecessor left NO RUNLOG.md / VERDICT.md in `crew/` (dir empty).
- `PREREG_TIER2.md` (38,417 B) + `SCOPE.md` copies at BUGREAD dir root — placed by parent/orchestrator. Byte-verified against frozen commit (see below).
- `clean/` contained a partial (`blob:none`) clone of sylorlabs/TNN @ `ec9f588135176d37507684f493daab3ff177fa8f` with an EMPTY worktree and 61,078 staged deletions (`D .github/scripts/...`) — residue of an interrupted partial-clone checkout (a later-finishing background `git status` from the predecessor era confirmed the count; its stderr also showed a promisor fetch failure `could not fetch 3c06f5b4920c780ba9f97dea830cd1373ef9aad4`). `git fsck --no-dangling`: clean (object store intact).
- Remote `https://github.com/sylorlabs/TNN.git`; remote branch head at the time: `8f89741cdb0facbee6ca294027e18d5ecb6a396f`.

## Pin freeze (before running)

| Pin | Expected | Result |
|---|---|---|
| Evidence pin | `a978fdc90638` | Short-SHA `git fetch` failed ("couldn't find remote ref"); **full-SHA fetch `a978fdc90638839c9f8eaf64e3c4d029696e79a2` succeeded**. GitHub API confirms: "bug-blindness: final verdict — 24/24 compiler parity, curriculum gap, crutch-not-learning (Micah 2026-09-21)", 2026-09-22T04:00:10Z. **Pin EXISTS — no STOP.** |
| Frozen prereg | `7b2100d09911c5c10252c5756c7def288e70bd1f` | API-verified ("crossref: scope + frozen preregs…", 2026-09-22T22:54:44Z). Local PREREG_TIER2.md `git hash-object` = `b1178370036bffbda6eb68ea0989c0e427dc31b7` == API blob SHA for `docs/lab/crossref/PREREG_TIER2.md` @ frozen commit, size 38417 — **byte-identical to frozen prereg**. T2-BUGREAD section extracted and quoted in VERDICT.md. |

## Environment build-up

1. Sparse checkout (non-cone) in `clean/`: `docs/lab/coding/bug-blindness/*` minus `battery/parity/.zag-cache/*`, plus `docs/lab/coding/driver.py`, `run_full.py`, `src/learner.zag`, `PREREG.md`, `CODING_REPORT.md`. Then `git checkout -q a978fdc90638839c9f8eaf64e3c4d029696e79a2` → detached HEAD at pin, worktree materialized. (`sparse.log`, `sparse2.log`, `checkout.log` in crew/.)
2. Battery inventory: 136 files under `docs/lab/coding/bug-blindness/` (`bb_tree.txt`). 24+6 battery = `battery/parity/` (p01–p24, s01–s06, c01–c08, `answer_key_parity.txt`); instrument `inspect.zag` (1823 lines, no `@import`); runner `run_bb1_parity.py`; oracle `verify_bb.py`.
3. Full pin tree listing saved to `pin_tree.txt` (for locating `docs/lab/coding/src/learner.zag`, `docs/lab/coding/driver.py`).

## Replication runs

4. **Seal check:** `logs/bb1_parity_key_sealed.sha` = `2bccc18e…361b`; `sha256sum battery/parity/answer_key_parity.txt` identical → seal intact.
5. **Build 1:** `znc inspect.zag -o inspect` → exit 0, 134,552 B binary (59 analyzer warnings, non-fatal). Source `inspect.zag` sha256 `76d44cd3c40…` == `MANIFEST_A.sha` record.
6. **Smoke:** p01→`BUG E0001 4`, c01→`CLEAN`, s01→`BUG UNINIT-VAR 3` — all match sealed key.
7. **Full battery (build 1):** `python3 run_bb1_parity.py` → 5 reps; digests `2bccc18e…` ×5 == committed `logs/bb1_parity_digests.txt`; rep1 bytes == sealed key bytes (`cmp` clean). Scores: KB-D1C 24/24 PASS, KB-D1 30/30 + 0/8 PASS, KB-D2 30/30 PASS, stretch 6/6, zero misses/false-alarms/class-errors. (`run_parity.log`)
8. **Build 2 (independent):** `znc inspect.zag -o inspect2` → sha256 `fc1e7ec7a45…` identical to build 1. Single-rep battery digest with build 2 = `2bccc18e…`. Toolchain + source deterministic.
9. **Oracle:** `python3 verify_bb.py` → 13/13 PASS, exit 0 (Q1 from rerun logs; Q3/Q4 from committed logs). (`oracle.log`)
10. **Worktree diff:** `git diff` empty after rerun — rerun logs byte-identical to committed logs.

## Curriculum-gap verification (committed code @ pin)

11. `grep -i bug src/learner.zag` → 0; `grep -c _zag_raw_syscall` → 0; `grep -c teach` → driver.py:0, run_full.py:0.
12. `do_teach` (1306–1320) read: prints AUDIT lines only, installs nothing.
13. `ALL_PATTERNS` (driver.py:12) = 11 IDs as VERDICT-BB.md lists; emitter spot-checks (`installed_has`:131, `emit_t1_slice`:289, `emit_t2_math`:622) match AUDIT.md.
14. `eclass_of`/`details_of` (driver.py:19–38): Python regexes on compiler stderr; `repair` receives only `(eclass, details, src)`; `run_learner` = fresh subprocess per call (stateless); test failures end loop undiagnosed (driver.py:~66).
15. 8 `patch_*` fns at exact cited lines (1155/1184/1442/1463/1490/1596/1733/1784); dispatch calls 7; `patch_type_a` zero call sites → dead code confirmed.
16. Tripwire check: `run_bb1_parity.py` passes only the program path to `inspect`; `inspect.zag` reads only `_zag_arg(1)` (+ optional "trace" flag); zero references to answer key or battery filenames; verdicts from table-unification checks. **Battery is NOT testing pre-labeled repairs.**

## Cleanup

17. Removed `inspect`, `inspect2` binaries and build-created `.zag-cache` from the clean worktree. Nothing committed. `git status` clean; `git diff` empty.
18. Run artifacts copied to crew/: `run_parity.log`, `oracle.log`, `build1.log`, `build2.log`, `bb1_parity_digests.txt`, `bb1_parity_score.txt`, `bb_tree.txt`, `pin_tree.txt`, `sparse.log`, `sparse2.log`, `rep_inspect2.txt`.

## Incidents / notes

- Exec tool had transient "failed to store metadata for session" flakes; worked around by redirecting output to files.
- My `pkill -f "git checkout"` matched my own shell — killed it; switched to `ps`-based inspection. No sibling processes harmed.
- Sibling Wave-2 crews (DIALOGUE, HTD1, SENSESH2H, CLASS3DEC, SELFTEST) observed active on this VM (ps); no shared state touched (non-interference held).
- `~/MEMORY.md` gained an audio line mid-run (v6 opus verdict) — irrelevant to this task, noted only.

## Result

**REPRODUCED** — see VERDICT.md. Final message to parent restates the complete verdict, battery-vs-measured, and frozen pins.
