# NAMECHECK: MULTI-OWNER-CHURN probe

## Step 0: Toolchain Guard

- Safebin activated at startup: `$HOME/safebin` (verified present).
- `export PATH="$HOME/safebin"` applied for all subsequent work.
- `which python3` returned NOTHING. `which python` returned NOTHING.
- `which znc` returns `/home/hatch/safebin/znc`, a symlink to the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`).
- No Python, C/C++, JavaScript, or Rust invoked at any point. Work so far:
  shell only (mkdir, ls, git branch/status, file writes of prereg documents).
- Any forbidden-executable invocation in later steps = automatic
  PROCESS-FAIL for the current scientific wave.

## Scope

Lane directory (owned path only):
`docs/lab/research-lead/overnight-20260928/multiowner_churn/`

Contents: PREREG.md (frozen first), NAMECHECK.md (this file),
multiowner_churn.zag (implementation, after prereg commit), build
outputs, raw run logs (run1/2/3.txt), REPORT.md (after 3/3 runs).

## Environment notes

- Repo ~/workspace/tnn-rsi-gpi3; branch tnn-native-lab. Working directly
  in the checkout; the pinned znc is already present at
  src/tools/toolchain/.
- Commits local only, never pushed. Explicit pathspecs on every commit.
- No `git reset`. No amend of shared history. Per the 2026-10-03 shared
  workspace lesson, git writes go through /usr/bin/git directly (the
  safebin git symlink has failed with EPERM on object writes); on
  index.lock contention, retry with sleep backoff and never remove the
  lock while other workers are active.
- Substrate is the frozen EVICTION-POLICY mechanism
  (`../eviction_policy/`, VERDICT=PASS, 2026-10-03): identical header
  layout, pool geometry, conflict path, owner-scoped reads, A family,
  benign B writer, PART classification, 16/16 split, PIN scan+drop.
  The only new code is teach_churn_multi; teach_churn (single-owner)
  is carried over unchanged so the 9 baseline conditions can reproduce
  the frozen table bit for bit.
- Non-ledger task: claim minting paused; no ledger entries are made.
- Sealed worlds: none used. No sealed-world contents inspected.
- Documentation style: no em or en dashes in lane documents (verified
  before commit).

## Design lineage

Follow-up to EVICTION-POLICY (VERDICT=PASS, 8/8 kill bars). Its own
report caveated the money result: the churn adversary was single-owner
(key 3999, B-owned), so every churn victim was class B and PART's win
partly aligned with the class boundary. This lane is the caveated
probe it ordered: 2 and 3 churn owners, with at least one churner
carrying an A-family owner (owner 8 on key 3998; owner 4 on key 3997)
so the churn crosses the class boundary. The parent questions: does
owner-partitioned still win (preregistered answer: no, ret 77 -> 0)
and does pinning still survive (preregistered answer: yes, ret 100,
drop 28/48). This lane is an adversary extension on a frozen
mechanism, not a repair lineage; it canonizes no policy fix.
