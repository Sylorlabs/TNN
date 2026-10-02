# Zombie-Lane Investigation: wave-20261001-1721pdt GOV lane

Date: 2026-10-01 (17:21 PDT wave). Worker: GOV lane (subagent).
Question: did a still-alive rogue worker ("zombie lane") commit to
tnn-native-lab outside the coordinator's knowledge, or were the seven
commits legitimate direct handoffs?

## Commits under investigation

| commit | time (UTC 2026-10-01) | subject |
|---|---|---|
| 1963e994d | 21:22:32 | Mini-lifetime integration: 3-arm persistent comparison |
| 02a338dbf | 21:26:46 | substrate expansion: 5 behaviors from one consequence substrate |
| 105e9ee8b | 21:30:24 | Persistent cross-domain connections |
| ff0d91691 | 21:36:54 | Utility integration: Test 6 redundancy + predictive utility |
| 0509fd116 | 21:39:35 | rebinding hardening: scale/deception/adaptation |
| 293cf0672 | 21:41:22 | Governance wave 2: ledger C181-C188 |
| eb19a4f3c | 22:13:26 | Protect-the-how: retry complete (tip of tnn-native-lab) |

All seven sit in one linear first-parent chain on tnn-native-lab. The
reflog shows one straight line of commits, no branch switches, no
rebases. Author and committer are identical on all seven:
tnn-rsi-loop <rsi-loop@localhost>, the standing loop identity used by
every other wave commit.

## Finding 1: NAMECHECK.md records present on all seven

- 02a338dbf, 105e9ee8b, ff0d91691, 0509fd116, 293cf0672, 1963e994d each
  add a fresh NAMECHECK.md in their own lane dir, each recording a
  Step 0 toolchain guard (safebin activation, which python3 returning
  nothing) executed before any research work.
- eb19a4f3c adds no new NAMECHECK.md but inherits the lane's record:
  docs/lab/research-lead/overnight-20260928/protect_how/NAMECHECK.md
  exists in the tree (first committed in the fold-in 249a1b85e).
  GAP: the protect-how retry worker did not record its own Step 0 in
  eb19a4f3c. The report text states safebin was active and zero
  forbidden executables were invoked, but the Step 0 record itself is
  the previous worker's, not the retry's.

No commit is missing a NAMECHECK.md record entirely.

## Finding 2: the commits were expected by a sibling worker, unrecognized by the coordinator

- The governance worker's own NAMECHECK.md (committed in 293cf0672)
  states its mission as: "Wait for 8 new priority workers +
  protect-how retry to complete." It then recorded those workers'
  claims C181-C188 as exploratory BUILD-PASS. The governance worker
  knew this batch existed and was waiting on it. This is coordination,
  not a rogue lane.
- The wave-20261001-1421pdt wave record (f52ab3aa1, committed 21:59
  UTC) tells the other half: its debate group listed five of the
  commits (02a338dbf, 105e9ee8b, ff0d91691, 0509fd116, 293cf0672) as
  "undebated arrivals" from "an unidentified lane (not produced by any
  of this wave's 11 workers, not debated)", ruled NO VERDICT, and
  recommended the parent investigate the possible zombie lane as a
  process anomaly and standing risk to prereg ordering and seal
  integrity.
- Interpretation: the batch was spawned above the wave coordinator
  (direct handoffs, consistent with the Micah 10-priorities push
  visible in the content), and the 1421pdt coordinator was never told.
  The "unidentified lane" label in the wave record is accurate from
  the coordinator's vantage but does not imply a rogue worker.

## Finding 3: no live worker evidence on this machine

- Process scan of /proc for znc/tnn/rsi/agent processes: no znc
  builds running. The only research-looking processes are sibling
  lanes of the current wave (1721pdt) doing grep searches (K-LT-5,
  arena v6, H-EXP2).
- File mtime scan: every file modified after the last commit
  (22:13:26 UTC) sits inside the current wave's run dirs
  (wave-20261001-1721pdt); nothing outside wave dirs was written
  after the last commit.
- git fsck unreachable objects: all unreachable commits are dated
  2026-09-22 through 2026-09-30 (old worktree/stash/index
  artifacts). None is from 2026-10-01. No recent orphaned work.
- Message style across the seven commits matches loop norms
  (-COMPLETE verdict tags, determinism claims, "Local only." on four
  of the seven).

## Finding 4: content claims of 1963e994d and eb19a4f3c sample-checked

- 1963e994d REPORT.md supports the commit message: 3-arm persistent
  comparison (frozen baseline vs rebind vs integrated), results table
  per arm, verdict MINI-LIFETIME-INTEGRATION-COMPLETE, "3/3
  byte-identical per arm" with sha256 prefixes, pure Zag via pinned
  znc, architecture accounting recorded. GAP: only run1 transcripts
  per arm (mli_run_A1/B1/C1) are committed; runs 2 and 3 are not in
  the commit despite the 3/3 determinism claim (hashes are asserted
  in the report only).
- eb19a4f3c REPORT.md supports the commit message: PROTECT-HOW-
  COMPLETE: SAVES-HOW-BY-ORDER, control and treatment 3/3
  byte-identical with SHA-256 hashes, analysis completed, honest
  boundary stated ("The 3-tier policy is researcher-authored, not
  learner-derived"). The commit adds ph_ctl_run2.txt and
  ph_ctl_run3.txt, completing the transcript set (all six runs now
  present). GAP: ledger C189 was never appended; the governance
  report anticipated "Will be C189 when committed" but eb19a4f3c
  does not touch the ledger.

## Verdict

No evidence of a live zombie lane. The seven commits are best
explained as legitimate direct handoffs: a coordinated batch of
workers on Micah's 10 priorities (learner verification, adaptive
threshold, provenance learning, mini-lifetime integration, substrate
expansion, persistent connections, utility integration, rebind
hardening, protect-how retry) plus their governance worker, spawned
above the 1421pdt wave coordinator, which is why the coordinator's
debate group saw them as an unidentified lane. The governance worker's
own records prove the batch was expected and internally coordinated.

## Known

- Provenance chain: all seven commits linear on tnn-native-lab, same
  loop identity, consistent timestamps 21:22-22:13 UTC inside the
  1421pdt wave window.
- NAMECHECK.md records exist for all seven lane dirs; Step 0 guard
  recorded for six commits plus the inherited protect_how record.
- No live rogue processes, no uncommitted recent file writes outside
  current wave dirs, no recent orphaned commits.
- The 1421pdt fork battery FRESH PASSed two of the five at the time;
  this wave's battery FRESH PASSes all seven (see FORK_BATTERY.md).

## Unknown (cannot be settled from this machine)

- Who exactly spawned the batch (parent orchestrator vs root is the
  inference; no spawn record is visible to this lane).
- Independent re-verification of the experiment results themselves
  (the battery confirms toolchain integrity at each commit, not the
  experiments' claims).
- Runs 2 and 3 transcripts for mini_lifetime_integration; the retry
  worker's own Step 0 record; the missing C189 ledger entry.

## Follow-ups recommended

1. Retrospective charter or frozen-bar review plan for C181-C188
   before any claim is adopted beyond exploratory (the 1421pdt wave
   record already queues this).
2. Append C189 for the protect-how retry to the canonical ledger, or
   record why it stays unledcoded.
3. Commit the missing mli_run_A2/A3/B2/B3/C2/C3 transcripts if they
   exist, or downgrade the determinism claim to the evidence on disk.
4. Process fix at the parent level: direct-handoff batches should
   announce themselves to the active wave coordinator so "unidentified
   lane" does not recur.
