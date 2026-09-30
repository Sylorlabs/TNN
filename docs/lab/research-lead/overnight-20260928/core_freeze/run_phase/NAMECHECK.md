# Step 0 Name-Check: Core Freeze Challenge Run-Phase Worker (2026-09-30)

The four standing-rules sections at the top of repo-root `LOOP_STATE.md` apply to
this run-phase task as follows:

1. **Standing owner rules (2026-09-23), PURE ZAG ONLY:** the literal red line.
   No Python anywhere in my work: not in run scripts, not in hash/byte
   verification, not in /tmp scratch, not for log comparison. All verification
   uses POSIX shell (`sha256sum`, `cmp`, `grep`, `awk`). Disclosure does not
   cure use, so there will be nothing to disclose.
2. **Image judge rule:** does not apply; this task has no image candidates.
3. **Fork-testing rule:** does not apply; this is the freeze-challenge battery,
   not a wave fork battery.
4. **Standing ruling, pure-Zag scope (2026-09-23):** fixture provisioning and
   all verification scripting count as loop work, so the run harness is
   shell-only.
5. **Standing rule, shell-only byte checks (2026-09-30):** dash checks use only
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.

Additionally: commits are local, owned path only
(`docs/lab/research-lead/overnight-20260928/core_freeze/run_phase/`) with
explicit pathspecs; `git status` is inspected before every commit; the frozen
source and binary are never modified (hash re-verified before every world and
after the battery); the contaminated paper
`TNN_RESEARCH_PAPER_20260929.md` is never read for evidence, never edited,
never staged. On a live `.git/index.lock`: wait and retry, never remove it.

Kill bars for this run: K1 (binary hash 8733af3d2814 verified before every
world; all 15 world-file seals verified), K2 (all 9 worlds executed per
protocol with results against frozen bars; V0 and C1 checks reported),
K3 (pure markdown/shell, dash-clean, contaminated paper untouched).
