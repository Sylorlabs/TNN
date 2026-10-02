# NAMECHECK_S6C: H-PI-REV2 step-6 re-execution under amendment K-AX2 (lane HPIREV2-S6C)

Worker: HPIREV2-S6C (B4b implementer and re-execution worker).
Independence: this worker is distinct from the step-6 implementer
(HPIREV2-S6-IMPL) and from the amendment authors (the S6 and S6B
amendment-author workers). All implementation below is from the frozen
amendment text only: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
AMENDMENT_KAX2.md as committed at 3c93a737b.

## Step 0: safebin activation (own activation, recorded here)

1. Ran the lane's safebin setup script:
   bash /home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
   (the task's literal path ~/docs/lab/... does not exist; the
   identical script lives under the working copy at
   /home/hatch/workspace/tnn-rsi/docs/lab/research-lead/
   overnight-20260928/safebin_setup/setup_safebin.sh, the same file the
   S6 worker used). Setup output: "SAFEBIN-READY: /home/hatch/safebin
   (36 tools, no python)".
2. `export PATH="$HOME/safebin"` before every subsequent command.
3. Toolchain verification: `which python3` prints NOTHING (exit 1);
   `which python` prints NOTHING (exit 1). If either had resolved,
   work would have stopped here with BLOCKED.
4. Safebin contents include bash, cat, cmp, cut, date, diff, git, grep,
   sed, sha256sum, stat, wc, znc (pinned), and coreutils; python3 and
   python are absent.
5. Rule honored throughout: shell invokes only pinned znc, runs built
   binaries, git read ops, and file copies. No python3, python, gcc,
   cc, perl, ruby, or node invoked at any stage. Any forbidden
   invocation would be reported as automatic PROCESS-FAIL.

## Commit-order self-check (binding, per the amendment)

- `git log --format=%H -- AMENDMENT_KAX2.md` shows exactly one commit:
  3c93a737b (the frozen amendment).
- At this worker's start, `git rev-parse HEAD` was 3c93a737b. While
  this worker read the frozen documents, the coordinator advanced HEAD
  to 6b4ed149e (wave H5 sealed evaluation, a different lane; no
  HPIREV2 files touched). 3c93a737b is an ancestor of HEAD. The
  amendment still strictly precedes every S6C_ artifact: no S6C_ file
  existed in the working tree or in git before this worker's first
  write (verified: `git ls-files S6C_*` = 0 and lane listing showed no
  S6C_ files). UNVERIFIABLE ORDERING does not apply; ordering is
  verifiable.
- This worker performs no commits, no pushes, no git reset, no rebase.
  All S6C_ files are new files in the lane only; no existing lane file
  is modified.

## Scope

- Build B4b exactly per the frozen B4b specification (nested two-branch
  template stream, 590879 candidates, alt and v_old computed by frozen
  dsearch, no Section B revision-machinery code in B4b).
- Run the amended step-6 matrix: 12 runs (M x3, B3 x3, B4b x3, D1 x3);
  M, B3, D1 expected byte-identical to S6 transcripts.
- Score the amended K-AX2 bar and all other bars unchanged; report
  cost-accounting fields per the amendment.
- Deliverables: S6C_EXECUTION_LOG.md, S6C_VERDICT.md, S6C_b4b.zag,
  S6C_b4b_bin, S6C run transcripts. No verdict beyond the re-execution
  semantics; verdicts are never SURVIVES.

## Documentation and determinism rules

- No em-dash or en-dash bytes in any lane file (byte-checked at the
  end).
- Determinism: 3/3 byte-identical reruns per binary; zero randomness
  in any decision path.

No em-dashes in this documentation.
