# NAMECHECK_ADVERSARY.md - wave-20261001-2021pdt / F2v3-ADVERSARY (sealed World C-prime)

## Step 0: Toolchain guard (mandatory, before any other work)

Date: 2026-10-01 21:19 PDT (Thu)
Worker: independent adversary (depth 2/2), lane F2v3-ADVERSARY. Independent
of the F2v3 builder worker and the F2v3-IMPL worker. Working from the
committed frozen prereg PREREG_F2V3.md only.

Actions taken:
1. Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   (resolved under the working copy; the bare relative path from the task
   does not exist under $HOME).
   - Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   - znc pinned toolchain present and verified by the script
   - Safebin verify reported: python3 absent from safebin PATH (OK),
     python absent (OK)
2. Exported PATH="$HOME/safebin" (safebin only, no other entries) for
   every subsequent shell invocation in this task.
3. `which python3` -> prints nothing (exit 1) (OK)
4. `which python` -> prints nothing (exit 1) (OK)

Toolchain status: PURE-ZAG PATH active. No forbidden executable has been
invoked at any stage (setup, reads, builds, runs, log handling). Any
forbidden invocation would be automatic PROCESS-FAIL; none occurred.

## Learner source verification (before building the sealed binary)

- f2v3_learner.zag sha256 (working copy):
  91c9390f9567e3c99fbfbdcf0129d709d954a628c8d604b3139ea762f50f8900
- Build-chain check: rebuilt learner + f2v3_world_a.zag with the safebin
  pinned znc; output binary sha256 =
  62ee648f5d31d67b0877e77f1fe7dfe3e40740d39001015caaa71beb47d8dc40,
  byte-identical to the builder-recorded /tmp/f2v3_a hash in
  IMPLEMENTATION.md. The sealed binary is therefore built from exactly
  the builder's frozen learner source via a bit-reproducible chain.

## Independence statement

The adversary designed World C-prime from the frozen prereg family spec
(section 5) only. The implementer's dev worlds were not used as design
input; the committed world files were read solely to learn the exact
w_* interface the sealed world must implement (the interface is
prereg-disclosed). C-prime's sealed specifics (delays, gate polarities,
pulse schedule, passive length, goal setup) were chosen independently
and differ materially from every previously seen instance. The
implementer never sees C-prime: world files live in F2v3/sealed/, which
the builder never reads, and the sealed binary is built by the adversary.

## Write scope

New files only inside docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/:
NAMECHECK_ADVERSARY.md (this file), SEALED_CPRIME.md, SEALED_EVAL.md,
sealed/ (world sources). No commits by this worker; the coordinator
commits. No pushes. No em dashes in wave documentation.
