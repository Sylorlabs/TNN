# NAMECHECK_ADVERSARY.md (DEVANG3-ADVERSARY, wave-20261001-2021pdt)

Independent adversary worker for lane DEVANG3 sealed Families B/C design and
sealed evaluation. Independent of the DEVANG3 builder and DEVANG3-IMPL
workers. All family designs derive from the frozen prereg
(PREREG_DEVANG3.md, committed alone at 8197c294c) only. The builder's dev
files (dev_segb.txt, dev_segb_key.txt, dev_sealc.txt) were NOT opened or
inspected at any point. Sealed files live in DEVANG3/sealed/ and are written
by this worker only; the builder never reads them.

## Step 0: toolchain guard (mandatory, before any other work)
- Ran `/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` at 2026-10-01 21:05 PDT: SAFEBIN-READY, 36 tools linked, znc OK (`/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- `export PATH="$HOME/safebin"` applied for every command in this worker.
- `which python3` returns nothing (exit 1); `which python` returns nothing (exit 1). Verified before any other work.
- PURE ZAG ONLY: shell invokes pinned znc, runs binaries, git ops (read-only status/log/show/diff), file moves/copies. No forbidden executable invoked. Any forbidden invocation is automatic PROCESS-FAIL; none occurred.

## Step 0b: frozen binary verification (before any run)
- Implementation binary: `docs/lab/rsi/runs/wave-20261001-2021pdt/DEVANG3/devang3`.
- `sha256sum` verified against task value `7006ce4d23bdacf5f0c8fed1362e92451822b14ee3204ed23cb35027434e354e`: MATCH. (Had it not matched, work would have stopped as BLOCKED.)

## Step 0c: commit-order verification (before sealed evaluation)
- Prereg freeze commit 8197c294c: contains PREREG_DEVANG3.md + NAMECHECK.md only; committed 2026-10-02 03:29:32 +0000 (2026-10-01 20:29:32 PDT).
- File mtimes corroborate builder's BUILD-LOG ordering claim: PREREG_DEVANG3.md 03:28:39 UTC < commit 03:29:32 UTC < NAMECHECK.md (Step 0b) 03:30:02 UTC < devang3.zag 03:58:37 UTC < devang3 binary 03:59:54 UTC < BUILD-LOG.md 03:59:40 UTC < IMPLEMENTATION.md 04:00:03 UTC.
- No implementation file predates the prereg freeze commit. No ordering violation. Not VOID on ordering grounds.
- Note: implementation files are currently uncommitted (coordinator commits; this worker does NOT git commit per task). Sealed files are written with sha256 recorded in SEALED_B.md/SEALED_C.md BEFORE any sealed run; the coordinator must verify the committed sealed files match these hashes.

## Step 1: independence declaration
- This worker did not spawn the builder, did not read builder implementation notes beyond the prereg and the sealed-interface usage line, and designed Families B/C from prereg section 5 requirements only.
- K_AUD (code audit of committed devang3.zag source) was performed AFTER family design and sealed file generation, and only the audit-relevant sections were read; audit findings did not alter the sealed families.

## No em dashes
- Documentation rule honored: no em dashes in any file written by this worker.
