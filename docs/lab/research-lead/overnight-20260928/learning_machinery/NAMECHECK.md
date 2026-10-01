# NAMECHECK: Learning Machinery Specifier

## Step 0: Toolchain guard (mandatory)

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Guard check passed.
Safebin active for all subsequent shell operations.

## Scope

SPECIFICATION ONLY. Analysis and requirements. No implementation,
no variant built, no source modified, no experiment run.

## Input provenance (all read-only)

- Genuine state map `a5b66a376`:
  `docs/lab/research-lead/overnight-20260928/genuine_state/GENUINE_STATE.md`
- Consequence re-entry `7eab34ff2`:
  `docs/lab/research-lead/overnight-20260928/consequence_reentry/CONSEQUENCE_REENTRY.md`
- H3-lite frozen prereg `9084a7760`:
  `docs/lab/research-lead/overnight-20260928/h3lite_prereg/H3LITE_PREREG_FROZEN.md`
- Success criteria `04af42736`:
  `docs/lab/research-lead/overnight-20260928/success_criteria/SUCCESS_CRITERIA.md`
- Scaling analysis (`02804f782`, content in `bda26cf91`):
  `docs/lab/research-lead/overnight-20260928/scaling/SCALING.md`
- H3-lite Node 1 build `45c55ed83` (commit message and stat only;
  no source inspection beyond the recorded white-box summary)
- Weak K-LT-5 prereg (directory listing only; sealed world not opened)

## Constraints honored

- Zero em dashes in deliverables (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Frozen source (`tnn2_build/tnn2.zag`) read-only, never modified.
- Frozen prereg `9084a7760` read-only, never amended.
- No sealed worlds opened.
- Nothing pushed. Commit local only, explicit pathspecs on both
  `git add` and `git commit`.
- No new modes, bridges, handlers, or semantic cases proposed
  (this is a requirements specification, not a design).
