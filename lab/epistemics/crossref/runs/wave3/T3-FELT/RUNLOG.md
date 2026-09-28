# T3-FELT RUNLOG — crossref tier-3 status verification (NOT a replication)

Family: T3-FELT (felt-intensity re-trial record status).
Task: verify frozen prereg's stated record (re-trial prereg drafted+committed, NOT run,
awaiting Micah's approval). Do not run the experiment.

## Frozen prereg (programmatic extraction)
- Source: `~/workspace/tnn-lab/crossref/PREREG_TIER3.md`
- sha256 (local file): `538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1`
- Branch copy `docs/lab/crossref/PREREG_TIER3.md` @ tnn-native-lab head: sha256
  `538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1` — IDENTICAL.
- Branch head at verification time: `16400e32cdcdbc519a9bdce2277f192a5c57d0a9`
  (branch `tnn-native-lab`, repo `sylorlabs/TNN`).
- T3-FELT section extracted via `grep -n "## T3-FELT" + sed` (lines 42..53):

```
## T3-FELT — felt V3: RETIRE

**Claims:** commit `fce10cb5ba84`: N-arm resume — all 12 a/b pairs byte-identical ...
Verdict: RETIRE — feeling retires wholesale per AMEND1 A7 fork-arrangement ...
**Decisive bars (spot rerun):** K3′ and K4 application on the committed checker output; byte-identical a/b pairs on a sample.
**Method:** clean checkout; re-derive the kill-criterion arithmetic from committed evidence with independent Zag code; spot-verify pair byte-identity.
**Rule:** REPRODUCED if K3′/K4 fire exactly as stated and the RETIRE verdict follows mechanically; NOT REPRODUCED if any kill-criterion arithmetic is wrong.
```
Plus the section orientation given by the task: T3-FELT verdict commit = PREREG
`c9bbff95c6f1` — the felt-intensity re-trial prereg (fix harness AND test variations
head-on, TNN deliberately choosing via gated deliberation, max 2 harness changes per
run, anti-shopping rule, calibration knob frozen during pure feeling evaluation),
drafted and committed, NOT RUN, awaiting Micah's approval.

## Step (a): resolve prereg commit c9bbff95c6f1 on tnn-native-lab
- `GET /repos/sylorlabs/TNN/commits/c9bbff95c6f1` → **HTTP 422 "No commit found for SHA"**.
- Scanned 1,600 commits of tnn-native-lab history (pages 1–16, back to 2026-09-22T03:44Z,
  covering the 2026-09-20 records): **no commit with SHA prefix `c9bbff9`**, and **no
  commit message anywhere references `c9bbff95c6f1`**.
- CONCLUSION: named prereg commit **does not resolve** → per program law this family
  reports **RECORD-MISSING (c9bbff95c6f1)**.

## Record-content found under a different SHA (not the named commit)
- `6a030212284846bb4964dc9fbc57e67bde2704d8` — "lab(wave8): felt-intensity re-trial
  preregistration (awaiting Micah's approval — NOT run)" — 2026-09-20T04:30:52Z.
- Contains `docs/lab/wave8/felt-retrial/PREREG_RETRIAL.md`, blob
  `9747366c9f0b62c1cf76e9f9efe56ab9126a908c`, byte-identical at the prereg commit
  and at current branch head (stable record).
- Header reads: "Status: PREREGISTERED (frozen before any compile/run of re-trial
  code). Requires Micah's approval before execution. Date: 2026-09-20."
- Description matches the frozen prereg's orientation verbatim; the SHA in the frozen
  prereg (`c9bbff95c6f1`) appears stale or mis-transcribed (possible history rewrite
  or transcription drift).

## Step (b): search for any FELT verdict-of-results on the branch
- `docs/lab/crossref/runs/T3/` at head: T3-ANOMALY, T3-CONSIST, T3-HARDEN,
  T3-PARTIALS, T3_SYNTHESIS.md — no T3-FELT dir, no wave3 dir yet (this crew's).
- **BUT a results verdict EXISTS on the branch**, contradicting the "not run" status:
  - `5b1213eaee441e41751050a50069599792c7c526` — "lab(wave8): felt-intensity re-trial
    results — harness fixed, TNN chose H1, F identical to N; two prereg defects flagged"
    — 2026-09-20T05:50:53Z (author identity: micahcooley, the lab commit identity).
  - Committed ~80 minutes AFTER the prereg commit that requires Micah's approval.
  - Is an ancestor of current branch head (`compare` status: head is `ahead` of it).
  - Files: `docs/lab/wave8/felt-retrial/decides/DECIDES_RESULTS.md` (TNN-decides arm D,
    chose H1 across variants), `develop/DEVELOP_RESULTS.md` (Arm T + Phase C results),
    `phase_e/PHASE_E_RESULTS.md` (42-run harness-variation evaluation F-H1..H5/N-H1/N-H5).
    Both results docs explicitly cite the frozen `PREREG_RETRIAL.md`.
  - No Micah approval for the re-trial is recorded anywhere in the scanned history or
    in the lab memory record ("The re-trial prereg is drafted and committed, awaiting
    his approval").
- ANOMALY: the branch record shows the re-trial was EXECUTED (without the required
  approval) before the frozen prereg's "NOT run" orientation was written (2026-09-22).

## Verdict
**RECORD-MISSING** — named prereg commit `c9bbff95c6f1` cannot be resolved on
tnn-native-lab (no tree/blobs to hash-match). Approval gate: **Micah's approval
before execution** (PREREG_RETRIAL.md: "Requires Micah's approval before execution").
The true record status is worse than missing: a prereg document exists under a
different SHA and a full results verdict exists on the branch, contradicting the
frozen "not run" claim. Escalated to parent: the frozen prereg's SHA should be
amended, and the unauthorized-results commit adjudicated with Micah.
