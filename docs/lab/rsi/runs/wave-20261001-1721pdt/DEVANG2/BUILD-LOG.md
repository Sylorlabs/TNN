# BUILD-LOG.md (DEVANG2, wave-20261001-1721pdt)

File creation order, recorded so the coordinator can commit the prereg
before the implementation. No git commits were made by this worker.

1. `NAMECHECK.md` (17:24 PDT): Step 0 toolchain guard. Ran
   `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   (SAFEBIN-READY, 36 tools, python3/python absent), exported
   `PATH="$HOME/safebin"`, confirmed `which python3` returns nothing.
   Recorded BEFORE any prereg read or implementation.

2. Prereg analysis (no new files; read-only work):
   a. Frozen retry prereg: `git show a2b567de5` (full read of
      `PREREG_DEVANG2.md`, 225 lines), including crash diagnosis grounded
      in devlang/ DEVANG1 records, narrow scope (crash fix plus ONE
      mechanism change: cold-start tie-break, section 4.2), and frozen
      numeric bars (KR0 crash-regression gate, K1..K12, verdict rule,
      architecture accounting expectations).
   b. Frozen DEVANG1 prereg: `git show e23627a40` (inherited design:
      world, phases, online protocol, grounding, negator/comparative
      detection, interpretation passes, controls C1/C2/C3).
   c. Overnight DEVANG2 implementation and result: commit 153e2af8e
      (`devang2.zag`, 1065 lines; `RESULT_DEVANG2.md`). Verified its
      failure mode (memory-safe, 13/20 vs C2 17/20, K1 3/10) and its
      disclosed scoring deviation (length-averaged, retained per retry
      prereg section 3).

3. `devang2.zag` (17:26 PDT): implementation. Copied the memory-safe
   overnight baseline, updated the header comment to cite prereg
   a2b567de5, added `bigram_total` + `seg_online` (cold-start tie-break,
   prereg section 4.2, ~35 new/changed lines), switched both
   segmentation call sites (training and test) from `seg_dp` to
   `seg_online`. No other changes. No em dashes in source.

4. `devang2` (17:27 PDT): compiled binary via pinned znc
   (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`, exit 0, warnings
   only). `.zag-cache/` build artifact created alongside (compiler
   scratch, not a source file).

5. `RUN1.out`, `RUN2.out`, `RUN3.out`, `RUN1.err`, `RUN2.err`,
   `RUN3.err` (17:27 PDT): three runs, exit 0 each, stderr 0 bytes each,
   outputs byte-identical (sha256
   94856b34dfa590e1b2fee9aed5c34f253068c5b0915dffeb312edc26896ac564).

6. Debug verification (ephemeral, /tmp only, deleted after): a
   temporary instrumented build confirmed the cold-start branch fires
   exactly once (at t=0) and that its mechanism numbers are identical
   to the frozen binary's. Not part of the frozen artifact set.

7. `RESULT_DEVANG2.md` (17:28 PDT): build record with per-bar numbers,
   determinism evidence, crash-regression evidence, online audit,
   architecture accounting actuals, BUILD-FAIL verdict with killing
   evidence.

8. This `BUILD-LOG.md` (17:28 PDT).

Commit-order statement for the coordinator: the prereg (a2b567de5) was
committed long before this worker's implementation files existed; this
lane's implementation files (`devang2.zag`, `devang2`, run outputs,
records) were all created after the prereg analysis above. Safe to
commit prereg before implementation.
