# NAMECHECK: Integration Adaptive Policy Worker

## Step 0: Toolchain guard (mandatory)

Activation:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing (empty output before
`guard-check-done`). Safebin contains 36 tools including the pinned znc;
python3 and python do not resolve. Guard check recorded 2026-10-02.
Zero forbidden executables invoked in this wave.

## Provenance

- Worker: Integration Adaptive Policy Worker (depth 1 subagent).
- Mission: Micah Priority 7. Learn decision policy from consequences, not
  hardcoded AND/OR. Answer the RSV redteam bound (AND gate too conservative:
  withholds despite perfect predictor when source adversarial).
- Parent task: consequence-driven decision policy with context adaptation
  (stakes, source history, regime shift), 3/3 deterministic.
- Base: none (fresh UNFROZEN variant, self-contained). Frozen TNN-2
  read-only; not modified or linked.

## Inputs (commits verified via git log)

- RSV integration: `b755e33ff` (shared tag-61 substrate; integrated arm 3/3).
- RSV redteam bound: `98f68d6a3` (AND gate withholds on perfect
  predictor + adversarial source; 100% prediction-only vs 0% answered).
- Constitution: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_CONSTITUTION_20261001.md`.

## Constraints honored

- Pure Zag for all computation, generation, scoring, diagnostics.
- Shell only: znc invocation, binary runs, git ops, file moves.
- Safebin PATH from startup; `which python3`/`which python` return nothing.
- 0 modes, 0 bridges, 0 handlers, 0 semantic cases in the experiment code.
- No hardcoded AND/OR (or any threshold gate) in the adaptive decision path.
- Frozen artifacts untouched; research paper untouched; nothing pushed.
- Explicit pathspecs on every git add/commit.
- No em/en dashes in loop documentation.
- Preregistration (PREREG.md) committed strictly before implementation.
