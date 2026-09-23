# RUNLOG.md — T2-SELFTEST replication crew

## Inherited state (RESUME check)

- `~/workspace/scratch-crossref/T2/SELFTEST/clean/`: bare `git init` only
  (branch master, no commits, remote `origin=https://github.com/sylorlabs/TNN.git`
  pre-configured by predecessor). `git status` = "No commits yet";
  `git fsck` clean (nothing to check). No fetched objects.
- `~/workspace/scratch-crossref/T2/SELFTEST/crew/`: empty. No partial
  VERDICT.md/RUNLOG.md from predecessor. **Nothing valid to resume; started
  the clone fresh. Inherited state: remote URL only.**

## Timeline (all times PDT 2026-09-22/23)

- 04:2x — Inspected dirs; confirmed znc at
  `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  TMPDIR=`/home/hatch/workspace/tmp_commit` set for all commands.
- 04:3x — Read `~/workspace/AGENTS.md` (workspace rules), github skill.
- 04:4x — Started `git fetch origin tnn-native-lab --depth=50` in background
  (session proc_95a70f505568). Read-only orientation from the local
  working tree `~/workspace/tnn-lab/self-test/` (SELFTEST_PREREG.md,
  SELFTEST_VERDICT.md, oracle.py, selftest.zag — 566 lines) and the
  working-tree `crossref/PREREG_TIER2.md` T2-SELFTEST section (to know what
  to extract; authority reserved for the frozen commit).
- ~05:12 — Fetch completed (exit 0; ~463 MB objects). Verified branch tip.
- ~05:21 — **ANOMALY:** `clean/` directory vanished from the filesystem
  (not in Muse trash; disk 68 GB free). Cause unknown; no other crew
  contacted (non-interference). Decided to rebuild the clean checkout via a
  cheaper path rather than re-fetch 463 MB.
- 05:3x — Found both pins in T2/TQ crew's local clone object store
  (read-only inspection): `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (frozen prereg commit; on their `origin/tnn-native-lab`) and
  `334444eb94d8388bf79a1c54224c3405a27131a9` (claim commit; dangling in
  their pack, verified present). Confirmed `334444eb94d8` is NOT an ancestor
  of `7b2100d0` (branch rewritten between 2026-09-21 and 2026-09-22).
  Confirmed `git diff 334444eb94d8 7b2100d0 -- docs/lab/self-test/` touches
  ONLY `SELFTEST_VERDICT.md` (doc-sweep corrections: B6 GAP + T1 TRIPWIRE);
  `selftest.zag`, `oracle.py`, `SELFTEST_PREREG.md`, `runs_*` byte-identical.
- 05:4x — API verification via `gh-api` (GitHub REST, stored credential):
  `334444eb94d8` exists ("Self-test TNN: the TNN as its own test-runner",
  2026-09-22T02:20:55Z); branch tip `2f61ed6a` (2026-09-23T05:44Z) is 101
  commits ahead of frozen `7b2100d0` (compare API).
- 05:4x — Recreated `clean/`; `git fetch origin tnn-native-lab --depth=110
  --filter=blob:none` (1.4 MB, ~4 s). `git checkout 7b2100d0 --
  docs/lab/self-test docs/lab/crossref/PREREG_TIER2.md` (blobs fetched on
  demand from origin). `git fsck --no-dangling` clean.
- 05:5x — Extracted the T2-SELFTEST section verbatim from the frozen
  `PREREG_TIER2.md` (lines 131–137) → claims checklist + decision rule
  quoted in VERDICT.md §1.
- 05:52 — Copied frozen `selftest.zag` + `oracle.py` to `crew/build/`
  (md5 of copy == md5 of frozen blob materialization). Built:
  `znc_linux_x86_64_abed8aa1 selftest.zag -o selftest --no-analyze`
  (exit 0; 50776-byte binary; only warning: zagd unavailable).
- 05:53 — Ran s1 × 5 reps → `runs/rerun_s1_r{0..4}.log`, all exit 0;
  md5 5/5 identical: `3be14786893ae083ed4f3ede9a67024d` ==
  committed `runs_s1_r0.log` md5.
- 05:54 — Ran s10 × 5 reps → `runs/rerun_s10_r{0..4}.log`, all exit 0;
  md5 5/5 identical: `6ffead6686871b4191fe6e5927c354ce` ==
  committed `runs_s10_r0.log` md5.
- 05:55 — Ran committed `oracle.py`: `s1 1` → ALL KILL BARS HOLD
  (overhead 40/3144 = 0.0127; 5/5 byte-identical); `s10 10` → ALL KILL BARS
  HOLD (overhead 400/31440 = 0.0127; 5/5 byte-identical). Both exit 0, zero
  OBS/VERDICT/BAR/COVERAGE failures → 40/40 and 400/400 per oracle procedure.
- 05:56 — Fault injection: copied source to `selftest_fault.zag`, added
  labeled `if(batt!=5)` guard around the orchestrator's inner loop (silently
  skips battery 5 / B5). Built `selftest_fault` (exit 0). Ran s1:
  7 ST_VERDICT lines, `ST_BLOCKED,emitted=7,expected=8`, NO ST_DONE,
  NO ST_MANIFEST — binary layer blocks exactly as the original verdict
  describes.
- 05:57 — Ran `oracle.py s1 1` on the fault log → exit 1:
  COVERAGE missing=[('B5',0)], COUNT 7 vs 8, ST_DONE missing, ST_BLOCKED
  present, ST_MANIFEST missing. Oracle layer blocks independently.
- 05:58 — Gathered pin evidence (blob SHAs, fsck); wrote VERDICT.md,
  RUNLOG.md.

## Commands of record

```
# clean checkout (rebuilt after anomaly)
git init && git remote add origin https://github.com/sylorlabs/TNN.git
git fetch origin tnn-native-lab --depth=110 --filter=blob:none
git checkout 7b2100d09911c5c10252c5756c7def288e70bd1f -- docs/lab/self-test docs/lab/crossref/PREREG_TIER2.md

# build (crew/build/)
znc_linux_x86_64_abed8aa1 selftest.zag -o selftest --no-analyze
znc_linux_x86_64_abed8aa1 selftest_fault.zag -o selftest_fault --no-analyze

# runs
for r in 0 1 2 3 4; do ./build/selftest s1 $r  > runs/rerun_s1_r$r.log; done
for r in 0 1 2 3 4; do ./build/selftest s10 $r > runs/rerun_s10_r$r.log; done
./build/selftest_fault s1 0 > runs/fault_s1_r0.log

# oracle (committed oracle.py, unmodified)
python3 build/oracle.py s1 1   runs/rerun_s1_r*.log
python3 build/oracle.py s10 10 runs/rerun_s10_r*.log
python3 build/oracle.py s1 1   runs/fault_s1_r0.log   # expect exit 1
```

## Evidence inventory (crew/)

- `build/selftest.zag` — frozen source copy (md5 800a23ab636f81cdeafc83bb1b2c107d)
- `build/oracle.py` — frozen oracle copy (unmodified)
- `build/selftest`, `build/selftest_fault` — fresh znc builds (scratch only)
- `build/selftest_fault.zag` — labeled fault-injection variant (pristine source untouched)
- `runs/rerun_s1_r{0..4}.log`, `runs/rerun_s10_r{0..4}.log` — 10 clean reruns
- `runs/fault_s1_r0.log` — fault-injection run
- `VERDICT.md`, `RUNLOG.md` — deliverables

## Zero-RNG / purity notes

- `selftest.zag` contains no RNG or seeded PRNG: data comes from closed-form
  `truth(f,salt) = (((f+salt)*7919+13) % 100003)` and `flie`; the rep argv is
  accepted but never printed (rep-invariant output by construction).
- Python used only as glue (running the committed oracle, md5, file copies).
  All reasoning/verification logic is the frozen Zag binary + frozen oracle.
- Slices all far below 2^25 bytes (largest: 80×64 = 5120-byte audit ledger).
- Scratch only (`~/workspace/scratch-crossref/T2/SELFTEST/`); nothing written
  to `/tmp`; no commits made; no live workstreams touched.
