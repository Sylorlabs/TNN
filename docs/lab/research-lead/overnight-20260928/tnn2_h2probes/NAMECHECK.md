# NAMECHECK: TNN-2 H2 masked verification probe design

Worker: H2 Masked Probe Designer (subagent, depth 1/2)
Task: Design H2 masked verification probes. Step 1 in the TNN-3 roadmap (commit `67a420cca`). Design only, no implementation.

## Step 0: Toolchain guard (mandatory)

Executed at startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no `python3`/`python` path printed. No forbidden executable resolves in PATH. Pure shell + git only. No code written or executed; design documents only.

Toolchain status: PASS. No Python, C, C++, JavaScript, or Rust invoked at any point.

## Source material consulted (read-only)

- `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` (frozen TNN-2 source, commit `f4de7ff46`): `t2_try_verify` (lines 497-510), `t2_trial` (lines 586-666), `mp_run` (lines 668-671).
- `docs/lab/research-lead/overnight-20260928/tnn3_roadmap/TNN3_ROADMAP.md` (commit `67a420cca`): H1/H2/H3 relation (section 2), Step 1 H2 probes, Risk 3 (H1-before-H2 treadmill).
- `docs/lab/research-lead/overnight-20260928/tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md` (commit `340e94e3e`): masked mode never engages in production (flags=0 always in freeze), verifier uses environment-supplied `expected`.

## Deliverables

- `H2_PROBE_DESIGN.md`: the probe design, with explicit NOT IMPLEMENTED header.
- This file (NAMECHECK.md).

Commit: explicit pathspecs only, under `docs/lab/research-lead/overnight-20260928/tnn2_h2probes/`.

## Constraints honored

- Owned path only: all writes inside `tnn2_h2probes/`.
- Roadmap and TNN-2 source treated as read-only; no edits.
- Design only; no Zag source written, no binaries built or run.
- No em dashes in documentation.
- Research paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
