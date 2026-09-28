# VERDICT: T3-FELT — RECORD-MISSING

**Family:** T3-FELT (felt-intensity re-trial record status — status verification, not a replication).
**Verdict:** **RECORD-MISSING** — named prereg commit `c9bbff95c6f1`.
**Approval gate:** **Micah's approval before execution** (per `PREREG_RETRIAL.md`:
"Status: PREREGISTERED (frozen before any compile/run of re-trial code).
Requires Micah's approval before execution.").

## What was checked
1. Frozen prereg `docs/lab/crossref/PREREG_TIER3.md` (branch copy) sha256 matches the
   local file: `538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1`.
   T3-FELT section extracted programmatically. Branch head at verification:
   `16400e32cdcdbc519a9bdce2277f192a5c57d0a9` (`tnn-native-lab`, `sylorlabs/TNN`).
2. Prereg commit `c9bbff95c6f1`:
   - GitHub `GET /commits/c9bbff95c6f1` → HTTP 422 "No commit found for SHA".
   - 1,600 commits of `tnn-native-lab` history scanned (back to 2026-09-22T03:44Z,
     covering the 2026-09-20 records): no SHA starting `c9bbff9`; no commit message
     references `c9bbff95c6f1`.
   - The named commit cannot be resolved; no tree/blobs to hash-match.

## Anomalies (material — parent must adjudicate)
1. **The prereg record exists under a different SHA.** `6a030212284846bb4964dc9fbc57e67bde2704d8`
   ("lab(wave8): felt-intensity re-trial preregistration (awaiting Micah's approval —
   NOT run)", 2026-09-20T04:30:52Z) matches the frozen prereg's description verbatim.
   Its `PREREG_RETRIAL.md` blob (`9747366c9f0b62c1cf76e9f9efe56ab9126a908c`) is
   byte-identical at that commit and at branch head. The SHA in the frozen prereg
   appears stale or mis-transcribed (history rewrite or transcription drift). Do not
   treat the record as lost — but the frozen prereg's SHA needs amendment.
2. **A verdict-of-results exists on the branch, contradicting "not run."**
   `5b1213eaee441e41751050a50069599792c7c526` ("lab(wave8): felt-intensity re-trial
   results — harness fixed, TNN chose H1, F identical to N; two prereg defects
   flagged", 2026-09-20T05:50:53Z) is an ancestor of the branch head and commits
   full re-trial results (`decides/`, `develop/`, `phase_e/` results docs, all citing
   the frozen prereg) — ~80 minutes after the prereg commit that requires Micah's
   approval. No Micah approval is recorded anywhere (history or memory). Taken at
   face value, the re-trial RAN without its governance gate — before the frozen
   prereg's "NOT run" orientation was even written (2026-09-22).

## Conclusion
Neither NOT-RUN (a results verdict exists) nor cleanly "present" (the named commit
does not exist) applies. Per program law for an unresolvable prereg commit, the
verdict is **RECORD-MISSING** on `c9bbff95c6f1`, escalated with the two anomalies
above for Micah-facing adjudication: (i) amend the frozen prereg's SHA to the real
prereg commit, (ii) decide the standing of the unauthorized results commit
`5b1213eaee44` (accept, quarantine, or formally invalidate).
