# NAMECHECK — p1falsifier

Claim ids used: **C660-C699** (the C5xx-or-higher block required by brief 10.4;
C377-C466 are contested and untouched; redteaw4 used C620-C647, p1mech used
C600-C651 — no overlap with C660-C699).

Files created by this lane, all under
`docs/lab/research-lead/overnight-20260928/p1falsifier/`:

* `PREREG.md` — preregistration, frozen kill bars K1-K13, V0-V3.
* `NAMECHECK.md` — this file.
* `frz.zag`, `sup.zag`, `wld.zag`, `life.zag`, `hlp.zag` — **copies, byte-identical**,
  of `lane/p1mech` @ `2162252f2` `p1_mech/{frozen_prefix,lt3_support,lt3_world,lt3_life,lt3_helpers}.zag`.
  Not edited. sha256 asserted by `run.sh`.
* `fx_main.zag` — all new code (this lane's only original source file).
* `run.sh` — build + watchdog + determinism + sha assertions.
* `REPORT.md`, `ERRATA.md` — written after the run.

No file of any other lane or worktree is created, modified or deleted.
