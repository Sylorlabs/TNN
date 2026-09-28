# Independent verification — Workbuddy Round 2 repair (parent agent, 2026-09-27)

Performed directly by the coordinator on Crew D's frozen deliverables
(`~/workspace/wb2/crewD/`), using the pinned toolchain, Crew A's frozen
battery + scorer, and Crew C's kill probes. No Crew D outputs were trusted
without re-derivation.

## Binary provenance

| Check | Result |
|---|---|
| Source SHA-256 | `0bec5459b2959ec056c6c8771de7de009d7fd9406d7029d98fa97faa1a9d531b` — matches Crew D manifest |
| Clean rebuild from that source (pinned znc) | `7636a577fff29de6eae10fe238e33514083a3059aa9df8f64784a9601a684a09` — **byte-identical to Crew D's validated binary** |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (clean build dir, only analyzer warnings) |

## Kill-probe re-derivation (on my independently built binary)

| Probe (Crew C id) | Turns | Output | Verdict |
|---|---|---|---|
| c_c5 | `quinn was promoted.` / `quinn was praised.` / `was quinn promoted?` / `was quinn praised?` / `how many facts did i teach you?` | `Noted.` / `Noted.` / `yes.` / `yes.` / `2 facts.` | **FIXED** — both facts coexist, both retrieved, count correct |
| c_h1 | `quinn was promoted.` / `no, quinn resigned.` / `was quinn promoted or demoted?` | `Noted.` / `Noted.` / `I don't know.` | **FIXED** — stale fact no longer served; honest withhold (question's options don't include "resigned") |
| c_c2 | `the door code is 4321.` / `actually, the door code is 9876.` / `what is the door code?` | `the door code is 9876.` | **FIXED** — `actually,` now recognized as a correction marker; single period |
| c_c6 | `the vault code is 7760.` / `what is the vault code?` | `the vault code is 7760.` | **FIXED** — single period on plain-taught facts |

## Full battery re-derivation

- All 20 Crew A sessions run via `run_session.sh` recipe (fresh process each,
  2× byte-identical): all OK.
- Scored with Crew A's strict `score_battery.py`:
  **TOTAL: 24 PASS / 0 WEAK / 0 FAIL (n=24)**

## Regression gates re-derivation

- S1 frozen answer stream: **PASS** `3d60c4e33c0259b12fd7d27363aed6e8eca095a75bbc8a4daadcc2b6bbcf418f`,
  3/3 (plain + `MALLOC_PERTURB_=165` + `MALLOC_PERTURB_=90`).
- Confident-wrong scan across all kill probes: none found.

## One harness trap noted

`verify_s1.sh` runs the binary with the caller's cwd; the binary reads
`kb.txt`/`gaz.txt` from its cwd, so running from the wrong directory changes
behavior silently (first attempt FAILed). Same trap Crew C caught. Always run
from the build directory.

## Conclusion

Crew D's claims re-derive exactly. The red-team kill is resolved: the
`(subject, verb)`-keyed upsert is replaced by complement-aware identity plus
subject-level correction retractions, with no regression on the 24-probe
battery or the frozen gates.
