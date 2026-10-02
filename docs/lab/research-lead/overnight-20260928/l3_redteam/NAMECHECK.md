# NAMECHECK: L3 Red Team vs C281/C284 (L3-REDTEAM)

Worker: L3 Red-Team Worker (subagent, 2026-10-02).
Prereg: PREREG.md, frozen and committed BEFORE any attack
implementation (commit-order self-check per loop governance).

## Step 0: Worker toolchain guard (MANDATORY, recorded)

Setup executed at worker start, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp \
    sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty), then
"guard-check-done". safebin contains 36 symlinks (coreutils, git,
pinned znc); python3/python do not resolve under the worker PATH.
No forbidden executable invoked at any point (verified again at
report time). Pure Zag for all research logic. Shell only for:
invoking znc, running binaries, git ops, file moves/copies,
checksums, text search.

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make the current scientific wave PROCESS-FAIL.
None occurred.

## Step 1: Scope check

- Target: C281/C284 L3 claim (learner-created intermediate M).
- Do NOT modify xdomain_grammar_l2m/ or l3_repro_transfer/.
  All attack variants are COPIES under l3_redteam/.
- Deliverables: PREREG.md (frozen first), NAMECHECK.md, REPORT.md,
  attack sources, binaries, run outputs. Commit with EXPLICIT
  pathspecs. Paper untouched. Nothing pushed.

## Step 2: Pre-registration

PREREG.md written and committed before any attack source, binary,
or run log was created. Frozen attack battery: audits A1-A4,
empirical variants V0-V6 (H1 stack). Predictions recorded per
attack; deviation is evidence, not a tuning opportunity.

## Step 3: Implementation (post-prereg)

- V0: byte copies of committed glm_learner.zag + gl2m_h1.zag.
- V1: learner copy, op search bound 5 -> 4.
- V2/V2S: driver copy, G1b rule (r in [2,8]), 18 labels, targets
  26/34; V2S installer writes [INC,INC].
- V3: driver copy, G1c rule (r in [0,7]), labels with D+1 and 2D
  valid.
- V4: learner copy, SET1/INC op codes swapped in m_exec.
- V5: driver copy, fact insertion order 73 before 74.
- V6: driver copy, g1_labels insertion order reversed.
- Build: cat learner+driver, pinned znc, 3 runs each, sha256.

## Step 4: Reporting

REPORT.md records every attack as SUCCEEDED or FAILED with
evidence (traces, digests, source line references). Verdict:
L3-REDTEAM-COMPLETE with the attack ledger.

## Constraints honored

Pure Zag; zero Python; safebin mandatory; no em/en dashes in loop
documentation; paper untouched; nothing pushed (commits local on
tnn-native-lab); 0 modes/bridges/handlers.
