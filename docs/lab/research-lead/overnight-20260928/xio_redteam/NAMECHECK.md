# NAMECHECK.md -- XIO Adapter Red-Team Worker

## Step 0: Worker toolchain guard (mandatory, recorded at startup)

Executed before any other work, 2026-10-02 ~07:32 PDT:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING under the safebin PATH
(`guard-check-done` printed, no paths listed). No Python, no forbidden
interpreter was invoked at any point in this task. All computation is
pure Zag (znc 2026.07.0-dev) plus POSIX shell for file assembly,
compilation, hashing, and comparison. PROCESS-FAIL was not triggered.

## Scope and frozen-boundary discipline

- Read-only: `docs/lab/research-lead/overnight-20260928/xio_adapters/`
  (PREREG.md, xio_core.zag, xio_driver.zag, xio_full.zag, REPORT.md,
  binaries, run outputs). Verified untouched after the run via
  `git status` (no modifications under `xio_adapters/`).
- New, unfrozen, mine: everything under
  `docs/lab/research-lead/overnight-20260928/xio_redteam/`.
- Assembly method: `rt_full.zag` = first 1924 lines of `xio_full.zag`
  (frozen base + xio_core, ending at the close of `xio_query`) with the
  original driver section cut off, plus the new red-team driver
  `rt_driver.zag` appended. The base's internal battery symbol
  `ev_query` is provided once, by the red-team driver, as
  `xio_query(...,xio_on=1)`; the battery itself is never invoked.
- No modes, bridges, handlers, or core semantic cases added. No paper
  touched. Nothing pushed (commit stays local, explicit pathspecs only).

## Adversarial-battery provenance (commit-order equivalent)

This is an adversarial battery, not a hypothesis test, so there is no
frozen prereg. The honest equivalent is documented here: every attack's
PREDICTED outcome was fixed in the driver source (`rt_driver.zag`,
written before the first run) and is quoted in REPORT.md alongside the
OBSERVED outcome. Three attacks (A4b, A4c, A5) had their predictions
revised after the first run exposed design flaws in the attack itself
(decoy-count coincidence, id-recycling nondeterminism, rebind solving
the reverse query); the revisions are documented in REPORT.md with the
probe evidence that forced them. The final binary's outputs
(`rt_run1/2/3.txt`) are 3/3 byte-identical,
sha256 `d22cab6cafe0759003a872a11359096a544a83ee97a375a83fde5912728e35c4`.

## Zag toolchain notes (per AGENTS.md)

- Output path reuses the proven `emit`/`e64` helpers from the frozen
  base (byte-identical 3/3 in the H-XIO-1 runs); every binary's stdout
  bytes were verified before trusting them (3/3 identical here).
- No `as *i32` + slice construction in new code; all cell access is
  through the base's `get32`/`set32` over u8-backed buffers.
- No Python or other forbidden executable was used for analysis:
  all result inspection was done by reading the run outputs.
