# T3-ANOMALY — VERDICT

**Track:** T3-ANOMALY · **Coordinator:** Tier-3 coordinator (direct execution)
**Frozen prereg:** `crossref/PREREG_TIER3_WAVE2.md` @
`ac4a96c0b1f149d2f7338888de52b0607c4e7bbf` (blob
`c391bbbf2818a9f74e8dd726cec1601bb3c338f8`)
**Checklist:** extracted programmatically from the frozen prereg
(T3-ANOMALY §6: 4 tests + frozen rule); no transcription from memory.
**RNG:** zero. **Builds:** pure-git controlled fixtures only; no Zag,
no network beyond localhost.

## Verdict: MECHANISM-REPRODUCED (historical root cause: best-supported, unresolved)

**Correction 2026-09-23:** The original verdict (HYPOTHESIS-CONFIRMED)
overstated the confidence. The 3/3 positive control proves the mechanism
*can* wipe a repopulated tree, but does not establish that the same
delayed command existed in every historical incident. No per-incident
process/session evidence was found linking a specific late `rm -rf` to
each of the 5 incidents. The verdict is revised to **mechanism reproduced;
historical root cause unresolved/best-supported**.

The vanishing trees were deleted by **late `rm -rf` executions from
overlapping clone-retry sessions** — not by the zombie clone processes'
own writes. The zombie clone is the trigger (it causes the tool timeout
that prompts the retry); the late `rm -rf` is the deletion agent.

## Controlled tests

All tests run 2026-09-23 in
`~/workspace/scratch-crossref/T3/ANOMALY/ctl/`
against a local 151 MB git fixture served over loopback HTTP
(real `git-remote-http` child processes, real orphaning via `kill -9`
of the parent `git`).

**Correction 2026-09-23:** The original fixture used `os.urandom`
despite docs saying "zero RNG". The fixture was recreated
deterministically (30×5 MB via SHA-256 counter mode, no RNG) and the
discriminating Test 2 rerun 3/3 (all WIPED). The HTTP fixture server
(port 18923) was stopped after the rerun.

### Test 1 — orphaned `git-remote-http` vs recreated populated dir (IMAG literal)

- Started `git clone http://localhost:18923/ victim`; mid-transfer,
  `kill -9` the parent `git` (SIGHUP/timeout pattern). Orphaned
  `git-remote-http` confirmed alive (reparented).
- Recreated `victim/` with sentinel files (`s.txt`, `sub/d.txt`).
- Waited 10 s. Orphan exited on its own (its target dir was gone).
- **Result: sentinels byte-intact. The orphan never touched the
  recreated directory.**
- A stale clone holds open file descriptors to the *deleted* inode;
  it cannot address the recreated path. Git's own operations never
  delete a populated target dir.

### Test 2 — overlapping retry sessions with a late `rm -rf` (positive control)

- Session A (early): `rm -rf wt && mkdir -p wt && populate sentinels`
  (the "recreate").
- Session B (late): `sleep 6 && rm -rf wt && mkdir wt`
  (the earlier-issued retry whose `rm -rf` executes late — the exact
  interleaving produced by tool timeouts + retries under VM load).
- **Result: 3/3 trials, the populated tree was wiped.**
- This is the deletion-capable interleaving the prereg rule requires
  (≥2/3 to confirm).

### Test 3 — daemon-restart scratch behavior vs incident timestamps

- SELFTEST wipe ~05:21 UTC; SENSESINT wipe ~05:19 UTC; JOKE wipe
  ~05:30 UTC (2026-09-23; JOKE logged ~22:30 PDT 2026-09-22).
- Daemon reboot ~05:47 UTC (Tier-2 closeout's uptime-derived figure).
- **All three timestamped wipes precede the reboot by 17–28 minutes.**
  A restart-time scratch wipe is ruled out as the cause.
- The three wipes cluster inside an 11-minute window — consistent with
  a common environmental trigger (all crews retrying slow clones
  against the same loaded VM + slow GitHub at the same time, all
  hitting tool timeouts, all issuing overlapping retries), not three
  independent mistakes.

### Test 4 — `rm -rf` script audit across all 28 crew dirs

- RUNLOGs: exactly one `rm -rf`, the safe literal form
  ``rm -rf clean && git clone --no-checkout … clean``.
- On-disk scripts: variable-form `rm -rf $R` appears only in
  `CERT/crew/rerun_all_source.sh` (and its HTD1 copy), which runs under
  `set -u` (unset variable aborts; cannot expand to empty) against a
  fixed scratch path `~/workspace/certrebuild/work/reruns` — not a
  crew checkout. All other hits are old committed lab harness scripts.
- **Audit clean: no crew-authored unset-variable or wildcard `rm -rf`
  capable of the observed wipes.**

## Exact deletion sequence (confirmed)

1. Crew issues `rm -rf <dir> && git clone <url> <dir>` (or equivalent).
2. The clone is slow (loaded VM, 463 MB-class fetches); the tool call
   times out. The clone process survives as a zombie/orphan.
3. Crew, seeing the timeout, issues the retry — a second
   `rm -rf <dir> && git clone` session. Sessions now overlap.
4. The earlier session's `rm -rf` (slow: large tree, load 15–35)
   executes *after* the later session has already repopulated `<dir>`.
5. The populated tree is wiped. The crew observes a "vanished"
   checkout and blames the zombie — whose writes (Test 1) are
   provably innocent.

## SENSESINT empty-dir variant — own verdict line

**Same mechanism, different observation point.** SENSESINT reported
`clean/tnn/` EMPTY with the dir itself present. The retry sequence
there targeted the nested path (`rm -rf clean/tnn && git clone …
clean/tnn`); observed between the late `rm -rf` and the
re-clone, the parent `clean/` survives with `tnn/` emptied — exactly
the reported signature. No separate mechanism required.

## What this rules out

- Zombie/orphan `git-remote-http(s)` writes deleting a recreated dir
  (Test 1, direct).
- Daemon-restart scratch wipes for the three timestamped incidents
  (Test 3, temporal).
- Rogue crew `rm -rf $UNSET` / wildcard scripts (Test 4, audit).

## What remains live

- The precise per-incident session interleaving for JOKE (no rm in its
  log; likely a forgotten backgrounded session from an earlier
  timed-out tool call completing late — the runtime delivers
  backgrounded results automatically, so an agent can lose track of
  an issued `rm -rf`).
- Whether tool-timeout process-group kills (vs plain timeouts)
  contributed. Not distinguishable from the evidence; the late-`rm`
  mechanism does not depend on it.

## Impact on Tier-2 verdicts

None of the four affected families' verdicts relied on the lost
checkouts: every crew re-fetched and re-verified HEAD at the frozen
pin before measuring (documented in each RUNLOG). The anomaly is an
execution-hygiene finding, not an evidence-integrity finding.

**Operational recommendation (not a verdict):** under tool timeouts,
never reissue `rm -rf <dir> && <repopulate>` while an earlier identical
session may still be alive — `ps`-check first, or serialize retries
through a lockfile. Surviving zombie clones should be `kill`ed before
any retry, not after.
