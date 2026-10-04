# VERDICT — T2-TRACKB (replacement crew, 2026-09-22)

**Family:** T2-TRACKB — representation Track B closeout (Type C: committed-evidence re-derivation; no live-web recapture; no new data collection).

## Frozen claims checklist (quoted verbatim from the frozen prereg)

Source: `sylorlabs/TNN`, branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`,
file `docs/lab/crossref/PREREG_TIER2.md`, §T2-TRACKB (line 89). Extracted by this crew via
`git show` and byte-compared against the predecessor's frozen copy: **identical**.

> ## T2-TRACKB — Track B: arm-1 DONE, arm-3 FAIL, arm-4/5 PASS (Type C)
>
> **Claims:** closeout head `47c48d3e7cf9f`: arm-1 DONE (`89745ce1117c`); arm-3 FAIL (verdict committed, rebuild parked); arm-4 PASS; arm-5 PASS; C3 FORCE-PIN B.6 PASS (`d921459a`); C4 W9 head-to-head BLOCKED honestly — no blowout winner, scenario-fit map instead; W5 learner/harness B.4 FAIL (blocked)/B.5 PARTIAL; W8 cost comparison BLOCKED, accounting verified; pcodec frozen-§B.3 fix (`4a6d898c1e66` + `6adb2fa5930c`; FROZEN_DECODE_PASS, learner 5/5 determinism, tripwire 15/15); B.6 force-pin implemented; arm-3 rebuilt three ways all PASS (which becomes the arm = governance call).
> **Method:** Type C — re-derive from committed evidence; verify the W9 BLOCKED honesty (no winner named) and the arm-3 FAIL→rebuild-PASS×3 record.
> **Rule:** REPRODUCED if all arm verdicts re-derive; PARTIAL if the arm-3 rebuild's three PASS variants create ambiguity about which is "the" arm (name it).

## Verdict: PARTIAL

Every committed claim re-derived (25/25 independent mechanical checks PASS; pcodec
`FROZEN_DECODE_PASS` re-derived by rebuilding the W5 verifier from committed sources and
running it 3× byte-identically). The PARTIAL verdict comes solely from the frozen rule's
own named condition: the arm-3 rebuild's three PASS variants create genuine ambiguity
about which is "the" arm, and the closeout parks that choice as governance call #1 for
Micah. Nothing failed; no bar was misapplied; the ambiguity is the committed state,
accurately recorded — and it is exactly what the frozen rule instructs to name.

The three variants (named per the rule):
- **varA** — pure-Zag deliberative adaptive teacher (`7d056be`): "Verdict: PASS."
- **varB** — phase-scheduler teacher (`d7929bb`): "Verdict: PASS — arm-3 bar (3) 'shows adaptive judgment' is met"
- **varC** — engagement-meter teacher (`f0031d9`): "Verdict: PASS"

## Claim-by-claim vs measured

| # | Frozen claim | Measured (re-derived) | Result |
|---|---|---|---|
| 1 | closeout head `47c48d3e7cf9f` | commit present; "Track B closeout: finalize verdict sheet…"; all claim commits are its ancestors (arm-1, force-pin, pcodec ×2); rebuild commits on `origin/tnn-native-lab` | holds |
| 2 | arm-1 DONE (`89745ce1117c`) | commit present ("parent-wired teacher in pure Zag, verified byte-identical", holds `arm1/teacher.zag`); `ARM1_VERDICT.md` records "## Verdict: **PASS** (no §4 kill bar fired)"; sheet records arm-1 verdict commit `bdffce301a5a7800f17f8a24ff63443b476d34e0` | re-derived |
| 3 | arm-3 FAIL (verdict committed, rebuild parked) | `ARM3_VERDICT.md`: "## Verdict: FAIL — one arm-3 bar unmet (adaptive judgment not demonstrated)"; closeout: "FAIL — B.1 arm-3 criterion (3) not demonstrated… rebuild path parked for Micah" | re-derived |
| 4 | arm-4 PASS | `ARM4_VERDICT.md`: "**Verdict: PASS** — per the frozen PREREG_FREEZE.md §4 kill criteria (B.1/B.4)" | re-derived |
| 5 | arm-5 PASS | `ARM5_VERDICT.md`: "## VERDICT: PASS" | re-derived |
| 6 | C3 FORCE-PIN B.6 PASS (`d921459a`) | commit present, holds `FORCE_PIN_VERDICT.md`: "## VERDICT: PASS — B.6 implemented to the frozen spec text" | re-derived |
| 7 | C4 W9 head-to-head BLOCKED honestly — no blowout winner, scenario-fit map instead | sheet headline: "The frozen §4 B.1 identical-slice head-to-head is BLOCKED"; "§7 BLOWOUT RULE APPLIED" → "Result: NO BLOWOUT. No manufactured winner."; mechanical §7 application verified ("0 complete scorecards exist for any arm"); negative check: no "WINNER IS" string anywhere in the sheet | re-derived |
| 8 | W5 learner/harness B.4 FAIL (blocked) / B.5 PARTIAL | `LEARNER_HARNESS_VERDICT.md`: "B.4 TST-1 tape / replay rule — **FAIL (blocked)**"; "B.5 Learner's rights (§L) — **PARTIAL**" (closeout notes the footer gap was later CLOSED by repair crew `afb32918809b` — consistent, not contradictory) | re-derived |
| 9 | W8 cost comparison BLOCKED, accounting verified | `W8_CLOSEOUT.md`: "UNCHANGED: still BLOCKED for the same-slice comparison"; "*accounting* remains IMPLEMENTED AND VERIFIED" | re-derived |
| 10 | pcodec frozen-§B.3 fix (`4a6d898c1e66` + `6adb2fa5930c`; FROZEN_DECODE_PASS, learner 5/5 determinism, tripwire 15/15) | commits present with matching messages; rebuilt `verify/w5_pcodec_frozen.zag` from `4a6d898c1e66` sources → `p_decode rc=0`, `FROZEN_DECODE_PASS`, 3/3 byte-identical (sha256 `395111cc…55882`); sheet records "test_determinism: 5/5 byte-identical — PASS", "test_tripwire: 15/15 frozen B.8 cases — PASS"; sheet records both pcodec commit SHAs | re-derived |
| 11 | B.6 force-pin implemented | `FORCE_PIN_VERDICT.md` contains "B.6 implemented"; closeout: "B.6 force-pin: implemented and tested PASS by C3" | re-derived |
| 12 | arm-3 rebuilt three ways all PASS (which becomes the arm = governance call) | varA/varB/varC verdict files each record PASS (see above); closeout "PARKED FOR MICAH #1: Arm-3 rebuild — options (a)/(b)/(c)… needs his decision — nothing here is approved" | re-derived as stated — **and this is the PARTIAL trigger** |

## Method note (Type C compliance)

- Independent Zag verifier `crew/work/verify_trackb/verify_trackb.zag` (pure Zag, zero RNG):
  25 mechanical checks (substring + sha256 re-derivation, incl. wiring-spec digest
  `d333bc45…f32` recomputed with `ns_sha256` and matched to the pinned hash in committed
  `WIRING_HASHES.txt`). Built with pinned znc; **3/3 runs byte-identical**
  (sha256 `67c9d1207f6a8c2fd79bea2a35557f004e2edf7eff8495c30a08b2e711e01503`), exit 0,
  `fails=0`, `TRACKB_REDERIVED_ALL_PASS`.
- pcodec mechanism re-derivation: rebuilt the W5 verifier from committed sources;
  3/3 byte-identical `FROZEN_DECODE_PASS` (see RUNLOG).
- Evidence extracted fresh from git objects at the pinned commits (predecessor's two
  evidence copies byte-compared identical, then re-extracted anyway — never trusted).
- No live-web recapture, no new data collection, no repo writes, no commits by this crew.

## Frozen pins (recorded BEFORE running)

| Item | Pin | Status |
|---|---|---|
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | OK (object present) |
| Closeout head | `47c48d3e7cf9f` | OK |
| arm-1 | `89745ce1117c` | OK |
| C3 force-pin | `d921459a` | OK |
| pcodec fix | `4a6d898c1e66` + `6adb2fa5930c` | OK |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | OK (used for both builds) |

**Dispatch-pin discrepancy (recorded, did not stop the run):** the dispatch text named an
"Expected" pin `8d0d6b9e9c9c` ("Missing → STOP → UNREPLICABLE-AS-IS"). Exhaustive check —
local git objects, `git ls-remote`, `git fetch`, GitHub API
(`GET /repos/sylorlabs/TNN/commits/8d0d6b9e9c9c` → 422 "No commit found"), full-SHA
substring search of every prereg pin, and `git grep` over the closeout tree — found
nothing. It appears nowhere in the authoritative frozen prereg §T2-TRACKB (extracted
byte-identical by this crew). Per frozen SCOPE §2.2 the STOP condition is "a pin listed
in the tier prereg doesn't hold" — every listed pin holds. Treated as a dispatch
transcription error per AGENTS.md ("verify EVERY task's spec text programmatically
against the source document"); run proceeded on the authoritative pins. Full evidence
in RUNLOG.md.

## Open items / follow-ups for the parent

1. The arm-3 "which becomes the arm" governance call is still parked for Micah
   (varA vs varB vs varC) — unchanged by this replication.
2. The dispatch pin `8d0d6b9e9c9c` should be corrected or explained in the dispatch table
   to avoid future crews hitting the spurious STOP gate.
3. Suggested verdict-table entry: **T2-TRACKB — PARTIAL** (all claims re-derived; arm-3
   rebuild three-way ambiguity named per the frozen rule).
