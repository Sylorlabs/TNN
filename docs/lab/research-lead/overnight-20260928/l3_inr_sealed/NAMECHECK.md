# NAMECHECK: L3-INR-SEALED adversary worker (sealed battery + L3 verdict)

Worker: L3-INR-SEALED (subagent, depth 2/2, 2026-10-03). Task: design the
sealed worlds S1/S2/S3/S1p post-implementation-freeze under prereg G1-G8,
run the sealed battery via the two-process protocol (learner never opens
a world file), 3/3 byte-identical runs, verdict against K1-K12/KC0A-D.
This worker is the ADVERSARY: it tries to break the implementation.

Work directory: `l3_inr_sealed/` (this directory). The frozen
implementation `l3_inr_impl/` is NEVER modified by this worker
(read-only). The frozen prereg `l3_interm_repr_reuse/` is never touched.

## Step 0: Worker toolchain guard (MANDATORY, recorded)

Safebin activated at startup: `export PATH="$HOME/safebin"`.
Verification performed under the safebin PATH before any sealed work
(2026-10-03, ~07:26 UTC):

- `which python3` returns nothing.
- `which python` returns nothing.
- `which znc` returns /home/hatch/safebin/znc (pinned compiler).

All scientific computation is pure Zag executed via the pinned znc, or
via the FROZEN implementation binaries (learner_bin/world_bin/spearman)
which are themselves pure-Zag builds. Shell is used only for: invoking
binaries, file moves/copies, sha256sum digesting, git operations, and
text plumbing in the file-mediated driver (no computation). No Python or
other interpreter is invoked at any point. Per Micah's 2026-09-30
governance ruling, any forbidden executable invocation would make this
wave PROCESS-FAIL. None occurred.

Pinned-znc defect workarounds: no new Zag code is written by this worker
(world files are data, not code; the driver scripts are copied verbatim
from the frozen implementation's protocol).

## Step 1: Scope check

- Design sealed worlds S1/S2/S3a/S3b/S1p AFTER the implementation code
  freeze (commit 106c8e99c, 2026-10-03 07:15:15 UTC). World design began
  2026-10-03 ~07:26 UTC, strictly post-freeze. Materially different from
  DEV worlds; S1 is an adversarial family targeting the implementation's
  construction approach (see SEALED_KEY.md).
- The learner process never receives a world path: all runs go through
  the frozen `run_arm.sh` two-process protocol (driver passes the world
  path only to `world_bin`). The implementation worker (L3-INR-IMPL,
  a different subagent instance) never sees sealed contents; this worker
  holds the sealed key and releases only per-arm PASS/FAIL, accept
  counts, TEST counts, and digests.
- Sealed battery: full arm set (T1-T5b, C0-C5) on sealed worlds,
  3/3 byte-identical runs per arm, sha256 digests.
- Verdict computed against the frozen bars K1-K12 and KC0A-D. K10
  (independent red team) requires a follow-up worker (a different
  instance); this worker does NOT perform K10 and records it as PENDING.

## Step 2: Commit-order self-check (prereg strictly precedes sealed worlds)

- Prereg freeze: commit ca7cfca77 (2026-10-02, PREREG.md + NAMECHECK.md
  only under l3_interm_repr_reuse/).
- Implementation code freeze: commit 106c8e99c (2026-10-03 07:15:15 UTC,
  "L3-INR implementation: frozen prereg C363, DEV validation 3/3
  byte-identical"), descendant of ca7cfca77.
- Sealed world design: began 2026-10-03 ~07:26 UTC, after 106c8e99c.
  The sealed worlds and key are committed in l3_inr_sealed/ in commits
  dated after 106c8e99c. The frozen prereg therefore strictly precedes
  both the implementation and the sealed worlds. Verified via
  `git log --format='%H %ad' --date=iso` ordering at report time.
- The committed PREREG.md/NAMECHECK.md blobs and the entire
  l3_inr_impl/ tree are untouched by this worker (verified:
  `git diff 106c8e99c HEAD -- <l3_inr_impl/>` empty at report time).

## Step 3: Adversary stance (procedural firewall, prereg G8)

- This worker (L3-INR-SEALED) is a different subagent instance than the
  implementation worker (L3-INR-IMPL). The red-team worker (K10) must be
  a third, different instance (pending follow-up).
- The sealed key (SEALED_KEY.md) exhibits: hop counts, the reference
  edge sets, the C2/C3 training failures (run with the frozen control
  arms on sealed S1), attribute correlations, and the S3 resolvability
  analysis. The key is held in this lane; only digests/counts leave it.
- Candidate-world calibration runs (running frozen arms on draft worlds
  during design) are adversary-side verification, not the sealed
  battery. The sealed battery is the final 3/3 runs on the finalized
  worlds, recorded in runs/ with digests.
