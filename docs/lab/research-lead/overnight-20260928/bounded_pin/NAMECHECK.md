# NAMECHECK: BOUNDED-PIN-LIFETIME comparison

## Step 0: Toolchain Guard

- Safebin activated at startup: `$HOME/safebin` (verified present).
- `export PATH="$HOME/safebin"` applied for all subsequent work.
- `which python3` returned NOTHING. `which python` returned NOTHING.
- `which znc` returns `/home/hatch/safebin/znc`, a symlink to the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`).
- No Python, C/C++, JavaScript, or Rust invoked at any point. Work so far:
  shell only (mkdir, file writes of prereg documents).
- Any forbidden-executable invocation in later steps = automatic
  PROCESS-FAIL for the current scientific wave.

## Scope

Lane directory (owned path only):
`docs/lab/research-lead/overnight-20260928/bounded_pin/`

Contents: PREREG.md (frozen first), NAMECHECK.md (this file),
bounded_pin.zag (implementation, after prereg commit), build outputs,
raw run logs (run1/2/3.txt), REPORT.md (after 3/3 runs).

## Environment notes

- Repo ~/workspace/tnn-rsi-gpi3; branch tnn-native-lab. Working directly
  in the checkout; the pinned znc resolves via the safebin symlink.
- Commits local only, never pushed. Explicit pathspecs on every commit.
- No `git reset`. No amend of shared history. Per the 2026-10-03 shared
  workspace lesson, git writes go through /usr/bin/git directly (the
  safebin git symlink has failed with EPERM on object writes); on
  index.lock contention, retry with sleep backoff and never remove the
  lock while other workers are active.
- Substrate is the frozen MULTI-OWNER-CHURN mechanism
  (`../multiowner_churn/`, VERDICT=PASS 8/8, 2026-10-03): identical
  header layout (offsets 0..28), pool geometry, conflict path,
  owner-scoped reads, A family, benign B writer, multi-owner churn
  routine (M2/M3, w=21 per key). Frozen additions only: header offsets
  32 (pin_ttl_N) and 36 (clock), the 32x4 side table at base 2624,
  policies 3..7 in relocate(), and the per-round unpin(3999,16) call
  active under policy 7 only.
- Non-ledger task: claim minting paused; no ledger entries are made.
- Sealed worlds: none used. No sealed-world contents inspected.
- Documentation style: no em or en dashes in lane documents (verified
  before commit).

## Design lineage

Follow-up to MULTI-OWNER-CHURN (VERDICT=PASS 8/8). Its report left the
sharp next question preregistered: "pinning's drop leak (48 of 32
slots at M3) makes bounded-pin-lifetime/unpin reclamation the sharp
next preregistered comparison." This lane runs it, holding the M2/M3
adversary fixed. It also generalizes PINNING-RECLAMATION's consent
result (VERDICT=PASS 7/7, single-owner adversary): the unpin arm
covers only owner 16 under a 2-3 owner churn, testing whether the
mechanism survives a commons shared with non-consenting churners.
The preregistered structural prediction is that under this protocol
pin age order equals placement order, so no lifetime N can achieve
ret=100 with drop=0: the N landscape is a strict Pareto frontier, and
explicit unpin is predicted to sit off it (ret=100, partial
reclamation, dose-sensitive). This lane proposes and canonizes no
repair; per the no-patch-treadmill rule it records measured prices.
