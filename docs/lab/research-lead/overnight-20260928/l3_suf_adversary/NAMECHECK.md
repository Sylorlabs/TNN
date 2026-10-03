# L3-SUF-1-ADVERSARY NAMECHECK

Lane: `docs/lab/research-lead/overnight-20260928/l3_suf_adversary/`
Branch: `tnn-native-lab` (local only, never pushed)
Worker: L3-SUF-1-ADVERSARY (subagent, 2026-10-03, distinct instance from
designer, builder, red-team)
Task: non-ledger (claim minting paused). Design sealed worlds post-freeze,
hold the sealed key, run the evaluator. Do NOT modify the builder's frozen
code. Do NOT touch the builder's `src/` directory.

## Step 0 - Toolchain guard (adversary worker)

- `export PATH="$HOME/safebin"` at startup (verified 2026-10-03).
- `command -v python3 python` returns nothing under the safebin PATH
  (verified 2026-10-03; exit 1, no output).
- Pinned znc 2026.07.0-dev available at `$HOME/safebin/znc`.
- All research computation (world builders, evaluator, scoring) in pure
  Zag compiled only by the pinned safebin znc, honoring the pinned-znc
  workarounds in AGENTS.md (u8-backed cells, `_zag_malloc as *u8` alloc
  pattern, single output buffer + `_zag_raw_syscall`, shallow if-nesting,
  no `!(A && B)` in while conditions).
- If a forbidden interpreter is invoked in this lane, the wave is
  PROCESS-FAIL per the governance ruling; results stay exploratory until
  a clean safebin reproduction.

## Provenance

- Parent prereg: l3_suf_intermediate/PREREG.md (frozen 6c70c3198).
- Builder code-freeze: commit c973e88d6. Frozen world interface per
  l3_suf_intermediate/CODEFREEZE.md (learner-visible: w_observe, w_test,
  w_stakes; harness-only: w_truth, w_stakes_meta, w_undet).
- The builder's DEV worlds (W0, F-A..F-G) are NOT sealed and are NOT
  reused here. All worlds in this lane are designed post-code-freeze by
  this worker.

## Worker separation (frozen)

Designer, builder, adversary (this worker), red-team: four distinct
instances, blind except through the authorized evaluator. This worker has
not inspected the builder's sealed-ness assumptions beyond the frozen
public interface; the builder receives only per-arm PASS/FAIL, counts,
and digests from this lane.

## Constraints honored by this worker

- Pure Zag; safebin mandatory (Step 0 above).
- Commits local, never push, explicit pathspecs.
- Do NOT modify the builder's frozen code; do NOT touch the builder's
  `src/` directory. The evaluator links frozen learner sources read-only;
  sha256 recorded at build time, re-verified before every run.
- No ledger entries (non-ledger task).
- Sealed key (KEY.md) never leaves this lane except to the red-team
  worker under the same seal.

## Freeze record

- PREREG.md + NAMECHECK.md frozen in a commit containing ONLY these two
  files, added with explicit pathspecs. No .zag, no binary, no log, no key
  exists under this lane at freeze time. The prereg is never edited after
  freezing; any change requires a new prereg.
