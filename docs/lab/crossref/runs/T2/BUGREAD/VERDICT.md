# T2-BUGREAD — VERDICT.md

**Crew:** T2-BUGREAD (REPLACEMENT — predecessor killed mid-run by runtime daemon restart; no predecessor artifacts existed)
**Type:** A — full independent rerun from committed sources + sealed key in a clean checkout
**Date:** 2026-09-22/23 PDT
**Verdict: REPRODUCED**

## 1. Frozen prereg (authoritative — quoted verbatim from the byte-verified copy)

Source: `docs/lab/crossref/PREREG_TIER2.md` §T2-BUGREAD, frozen at commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`. Local copy blob SHA
`b1178370036bffbda6eb68ea0989c0e427dc31b7` == frozen commit's blob SHA
(API-verified) — byte-identical to the frozen prereg.

> ## T2-BUGREAD — bug-reading: 24/24, no rearchitect (Type A)
>
> **Claims:** commit `a978fdc90638`: TNN 24/24 on compiler-parity bug detection (programs as facts) + 6/6 on bugs the compiler cannot see (uninit vars, off-by-ones, wrong comparisons); byte-identical reruns; sealed answer key. Earlier failure = curriculum gap, not logic gap: zero bug knowledge taught (11/11 installed items all correct-code), learner never saw compiler output (Python driver regexes pre-labeled repairs), no memory (teach hook no-op, stateless), 8 repair rules authored not taught. Rearchitect trigger did NOT fire → decision: no TNN rearchitect; teach bug knowledge deliberately, move error classification into TNN (stderr as untrusted observation), real teach hook + persistent store, fix brace-patcher doubling, extend op inventory (first-attempt generation on unseen ops only 1/6).
> **Method:** rerun the 24+6 battery from committed sources/sealed key in clean checkout; verify the curriculum-gap root causes are as described in the committed code.
> **Rule:** REPRODUCED if 24/24 + 6/6 and the no-rearchitect decision's premises check out; NOT REPRODUCED if the battery was actually testing pre-labeled repairs (curriculum-gap claim wrong).

## 2. Pins frozen (before running)

| Pin | Expected | Found | Status |
|---|---|---|---|
| Evidence commit | `a978fdc90638` | `a978fdc90638839c9f8eaf64e3c4d029696e79a2` — "bug-blindness: final verdict — 24/24 compiler parity, curriculum gap, crutch-not-learning (Micah 2026-09-21)", 2026-09-22T04:00:10Z, API-verified on sylorlabs/TNN | HELD (fetched by full SHA; short-SHA fetch failed, full SHA succeeded — pin EXISTS, no STOP) |
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | API-verified; local PREREG_TIER2.md blob `b1178370036bffbda6eb68ea0989c0e427dc31b7` == frozen blob | HELD |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | present, used for both builds | HELD |
| Clean checkout | `~/workspace/scratch-crossref/T2/BUGREAD/clean/` @ pin (detached HEAD `a978fdc90638`), sparse (bug-blindness + coding sources only; `.zag-cache` excluded) | `git fsck` clean; worktree at pin | HELD |

## 3. Battery vs measured

Battery: `docs/lab/coding/bug-blindness/battery/parity/` — 38 items
(p01–p24 compiler-parity buggy, s01–s06 beyond-compiler buggy, c01–c08 clean),
instrument `inspect.zag` (pure Zag, zero RNG) built from source with the pinned
znc, scored by `run_bb1_parity.py` against sealed key
`battery/parity/answer_key_parity.txt` (38 entries).

Seal check: `logs/bb1_parity_key_sealed.sha` records
`2bccc18e7d086d77d243b97d471fad9dbf96dbf86f4c26d63e01b73ee03e361b`;
current key file hashes to the identical value — seal intact, key unmodified.

| Committed bar | Committed | This rerun | Match |
|---|---|---|---|
| KB-D1C compiler parity (24 items, 12 classes ×2), bar ≥0.85 | 24/24 = 1.0000 PASS | **24/24 = 1.0000 PASS** (all 12 classes 2/2) | ✅ |
| KB-D1 detection (30 buggy), bar ≥0.70 | 30/30 | **30/30** | ✅ |
| KB-D1 false alarms (8 clean), bar ≤0.25 | 0/8 | **0/8** | ✅ |
| KB-D2 class+line precision, bar ≥0.60 | 30/30 | **30/30** | ✅ |
| Stretch: UNINIT-VAR / OFF-BY-ONE / WRONG-COMPARISON | 2/2 each (6/6) | **2/2 each (6/6)** | ✅ |
| 5-rep byte-identical digests | `2bccc18e…` ×5 | **`2bccc18e…` ×5** (== committed digests; rep output bytes == sealed key bytes) | ✅ |
| Two independent source builds byte-identical | n/a (new check) | `fc1e7ec7a4525043854ce8b88273bf0ecac0d44aa605f9058509f26a36f72dd5` both builds; 2nd build's battery digest also `2bccc18e…` | ✅ |
| Independent oracle `verify_bb.py` | exit 0 (original) | **13/13 PASS, exit 0** (Q1 from rerun logs, Q3/Q4 from committed logs) | ✅ |

Rerun log outputs are byte-identical to the committed logs (`git diff` empty
after the run) — the committed evidence reproduced exactly.

## 4. Curriculum-gap premises — verified against committed code

All at pin `a978fdc90638`, files `docs/lab/coding/src/learner.zag` (2050 lines),
`docs/lab/coding/driver.py` (130 lines), `docs/lab/coding/run_full.py`.

| Frozen premise | Committed-code evidence (this crew) |
|---|---|
| Zero bug knowledge taught; 11/11 installed items all correct-code | `ALL_PATTERNS` (driver.py:12) = `p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill` (11 IDs); passed straight to learner `gen` mode, never through `teach`. Emitter spot-checks match AUDIT.md line numbers (`installed_has`:131, `emit_t1_slice`:289, `emit_t2_math`:622). `grep -i bug` in learner.zag → **0 hits**. `grep -c teach` → driver.py:0, run_full.py:0 (`teach` mode never invoked by either driver). |
| Learner never saw compiler output (Python driver regexes pre-labeled repairs) | `eclass_of`/`details_of` (driver.py:19–38) classify via Python regexes on raw compiler stderr; learner `repair` mode receives only `(eclass, details, src)` (driver.py:42–45, `gen_task`/`repair_task`). The TNN never sees compiler output. |
| No memory (teach hook no-op, stateless) | `do_teach` (learner.zag:1306–1320) prints `AUDIT op=INSTALL …` lines and returns — no store, no table, no mutation. `grep -c _zag_raw_syscall` in learner.zag → **0** (no file writes possible). `run_learner` spawns a fresh subprocess per call (driver.py:42–45). |
| 8 repair rules authored not taught | All 8 `patch_*` fns defined at the exact lines VERDICT-BB.md cites (`patch_unknownfn`:1155, `patch_type_a`:1184, `patch_ret_word`:1442, `patch_arg_unquote`:1463, `patch_del_badassign`:1490, `patch_arity`:1596, `patch_brace`:1733, `patch_dupfn`:1784). Dispatch (do_repair, 2006–2039) calls 7; `patch_type_a` has **zero call sites** — dead code, confirmed. |
| Rearchitect trigger did NOT fire (first condition: knowledge installed via teaching path — not met) | Q2 audit finds no bug knowledge was ever installed through any deliberative/teaching path (above). Trigger correctly not fired → curriculum gap is the primary verdict. Decision (no TNN rearchitect; deliberate teaching rearchitect) rests on verified premises. |

## 5. NOT-REPRODUCED tripwire — checked, does NOT fire

Tripwire: "the battery was actually testing pre-labeled repairs."
Evidence it is not:
- `run_bb1_parity.py` invokes `[INSPECT, <battery .zag path>]` — the program
  file only; no labels, no key, no extra args (the optional 2nd arg is a
  "trace" flag, never passed by the driver).
- `inspect.zag` `main` reads `_zag_arg(1)` (program path) only; the single
  file it opens is that path. Zero references to `answer_key` or any battery
  filename (`grep -c` for `p01|p02|s01|c01|answer_key` → 0).
- Verdicts are computed by table-unification checks over authored fact tables
  (DEF/CALL/ARITY/DECL/ASSIGN/USE/LOOP/COND/SPEC/BRACE), not by lookup.
- The sealed key is loaded by the driver only for post-run scoring.

The battery genuinely tests reading-by-inference. The curriculum-gap claim stands.

## 6. Verdict

**REPRODUCED.** 24/24 compiler-parity + 6/6 compiler-invisible, 5/5
byte-identical reruns with digests matching the committed values, sealed answer
key intact (seal SHA == key bytes; rerun output bytes == key bytes), and every
curriculum-gap root cause verified line-by-line in the committed code. The
no-rearchitect decision's premises check out; the pre-labeled-repairs tripwire
does not fire.

## 7. Notes / caveats

- Predecessor left no artifacts; clean/ clone was in a degraded state (empty
  worktree, 61,078 staged deletions from an interrupted partial-clone
  checkout, one promisor fetch failure in its history). Resolved via
  `git reset` + sparse checkout at the pin; `git fsck` clean; evidence pin
  fetched by full SHA from origin and verified via GitHub API.
- The `.zag-cache` committed under `battery/parity/` was excluded from the
  checkout; both `inspect` binaries were built from source (byte-identical
  across two builds) and removed afterwards, as was the build-created
  `.zag-cache`. Nothing was committed.
- Q3/Q4 metrics were re-derived by the independent oracle from committed logs
  (13/13 PASS); Q3/Q4 batteries were not re-executed (outside the T2-BUGREAD
  bar, which covers the 24+6 battery + curriculum-gap premises).
- Build emitted 59 znc analyzer warnings (non-fatal); build succeeded.
- Non-interference: sibling Wave-2 crews (DIALOGUE, HTD1, SENSESH2H,
  CLASS3DEC, SELFTEST) observed active on this VM; no shared state touched.

**Artifacts (this run):** `~/workspace/scratch-crossref/T2/BUGREAD/crew/` —
[RUNLOG.md](sandbox://workspace/scratch-crossref/T2/BUGREAD/crew/RUNLOG.md),
[VERDICT.md](sandbox://workspace/scratch-crossref/T2/BUGREAD/crew/VERDICT.md)
(this file), `run_parity.log`, `oracle.log`, `build1.log`, `build2.log`,
`bb1_parity_digests.txt`, `bb1_parity_score.txt`, `bb_tree.txt`,
`pin_tree.txt`, `sparse.log`, `rep_inspect2.txt`.
