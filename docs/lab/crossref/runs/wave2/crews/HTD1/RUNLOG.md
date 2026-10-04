# T2-HTD1 RUNLOG — HTD-1 Verdict Sheet Replication (Type C)

Crew: T2-HTD1 (REPLACEMENT; predecessor killed by daemon restart 2026-09-23)
Date: 2026-09-22/23 | Program: TNN cross-reference Wave 2 (Tier 2)
Authorization: Micah 2026-09-22 "run everything" ruling.

## Inherited state (from predecessor's RUNLOG.md, found in crew/ dir)

- Predecessor had: frozen-pin table (all PENDING), method note, a checklist of
  claims. Checklist text MATCHES the frozen prereg T2-HTD1 section (verified
  verbatim against the prereg below — no transcription drift).
- Predecessor's pin table recorded "RESULTS_VERDICT_SHEET.md pin: expected
  e7c5bcd6, observed pending" and a rule "Missing → STOP → UNREPLICABLE-AS-IS".
  INVESTIGATED: e7c5bcd6 does NOT exist in the first 200 commits of
  tnn-native-lab (checked pages 1-2 via API). The authoritative pin is the
  frozen prereg's: commit 8d74c47b5737 — which resolves cleanly. The e7c5bcd6
  expectation was an error (likely a transcription or a blob prefix from a
  different context). STOP condition did not trigger: the prereg's own pin
  was present and verified.
- Predecessor started a full clone into clean/t2-htd1-clean; daemon restart
  killed it mid-fetch (dir had ~285MB of objects, no refs). A SIGKILL (signal 9)
  also killed my first full `git fetch` retry (OOM during index-pack). The
  original partial clone dir was later gone (wiped); re-cloned shallow.

## PIN CORRECTION from coordinator (received 2026-09-22 23:37 PDT)

Coordinator confirms: `e7c5bcd6` was a transcription artifact (returns 422
"No commit found" in sylorlabs/TNN) — DISREGARDED per instruction. This
matches this crew's independent finding (recorded above: e7c5bcd6 searched
across 200 commits of tnn-native-lab, not found; the prereg's own pin
`8d74c47b5737` was used as authority throughout). No work depended on
e7c5bcd6; the verdict-sheet pin used was `8d74c47b5737743f4f2ff6eb807f05f2308358b0`,
resolved via both GitHub API and clean-clone `git show` (byte-identical
copies). No re-work required. Predecessor RUNLOG.md's "Missing → STOP →
UNREPLICABLE-AS-IS" note is formally retired by this correction.

## Frozen pins (recorded BEFORE work — verified, see §Evidence below)

| Item | Expected | Observed | Status |
|---|---|---|---|
| Frozen prereg commit | 7b2100d09911c5c10252c5756c7def288e70bd1f | full SHA 7b2100d09911c5c10252c5756c7def288e70bd1f, msg "crossref: scope + frozen preregs for the cross-reference / clean-environment replication program" | VERIFIED via API |
| Branch | tnn-native-lab | tnn-native-lab (tip 2f61ed6ac79a3f9571ef5b243d59330a8fe641f7) | VERIFIED |
| PREREG_TIER2.md blob @ frozen commit | — | b1178370036bffbda6eb68ea0989c0e427dc31b7 (38417 B) | VERIFIED |
| Verdict-sheet commit | 8d74c47b5737 (per prereg) | full 8d74c47b5737743f4f2ff6eb807f05f2308358b0, msg "htd-1: final results verdict sheet (closeout survey, 2026-09-21)"; adds docs/lab/htd-1/RESULTS_VERDICT_SHEET.md (blob 02c97bf9bedba8fd458b7425bc230ae1d44833b2) | VERIFIED |
| E-LG1 epclose R=5 | 1005582b5c (per prereg label) | 16a2574f3d01fed8b51f02de2b7a7ac6113de2de adds E-LG1-episode-close-R5.md — **PREREG LABEL SWAPPED** (see §Findings) | LABEL SWAPPED, evidence OK |
| G-CM1b evict rerun | 16a2574f3d (per prereg label) | 1005582b5c467e7dca554017bdc2f39573c39b6a adds G-CM1b-evict-rerun.md — **PREREG LABEL SWAPPED** | LABEL SWAPPED, evidence OK |
| Composition | 302796210b | 302796210b659925391cd98a5bd61c7844f4877d adds E-DE2-E-DE4-composition.md + builds/comp/ | VERIFIED |
| E-LG2 committed verdict | af6a22305ab9 | af6a22305a… msg "htd-1 RESULT: E-LG2 checkpoint+delta — verdict recorded (independently verified)"; adds builds/elg2/ | VERIFIED |
| E-DE3 committed verdict | 00984047f277 | 00984047f2… msg "htd-1 RESULT: E-DE3 lazy verification debt — KILLED (independently verified)"; adds builds/ede3/ | VERIFIED |
| znc binary | /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 | exists, 8337204 B, sha256 498abcb5ab346f8c… | VERIFIED |

## Method

Type C: re-derive the verdict sheet from committed build evidence with
independent checks; verify each kill/survive bar was applied per the frozen
preregs (HTD1_PREREG_FROZEN_2026-09-21.md + COST_MODEL_FROZEN.md +
AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md); confirm the G-CO3
contract-dependence caveat is as stated.

## Evidence gathered (all at the frozen pins, via GitHub API at commit SHAs)

- evidence/PREREG_TIER2_frozen.md (b1178370…): T2-HTD1 section quoted in VERDICT.md
- VERDICT_SHEET_8d74c47b5737.md (02c97bf9…): the verdict sheet under replication
- evidence/HTD1_PREREG_FROZEN.md (76b5d3c5…), AMENDMENT_CONSTRUCTED_MODE.md (661c0f6f…), COST_MODEL_FROZEN.md (e4064f35…)
- evidence/E-DE2-E-DE4-composition.md (5eda984a…), E-LG1-episode-close-R5.md (df59e5cc…), G-CM1b-evict-rerun.md (63b1dfa2…)
- evidence/VERDICT_ELG2.md (d72bd0f8…) from builds/elg2 at frozen commit
- builds/ dir listing at frozen commit: comp, ede3, elg2, esp-research, ref-baselines (no ede1/ede2/ede4/ede5/gco2/gco3/gcm1 builds — local-only per the sheet)

## Independent verification (pure Zag, zero RNG)

Built htd1_barcheck.zag with the pinned znc (binary htd1_barcheck_bin, not
committed). It recomputes every bar-application arithmetic from the frozen
bars and the sheet's numbers (tenths-of-percent integer math) and emits the
kill/survive verdict per entry. Run 3×:

- run1/run2/run3 SHA-256: 68f6ae67d87794b0d28d41165eeb22bd1e4928db29903c5c1568ea0b1f9a1611 — BYTE-IDENTICAL (3/3).

All 14 entry verdicts re-derived; every bar application trips/not-trips
exactly as the sheet states. Full per-entry table in VERDICT.md.

## Clone status

- Full clone failed: git-remote-https SIGKILL (OOM in index-pack) at ~285MB.
- Re-cloned: `git clone --depth 300 --branch tnn-native-lab` into
  clean/t2-htd1-shallow (TMPDIR=~/workspace/tmp_commit). HEAD
  `2f61ed6ac79a3f9571ef5b243d59330a8fe641f7` = API branch tip.
- `git status --short`: clean (empty). `git fsck --full`: rc=0, no errors.
- Frozen prereg @ 7b2100d0, verdict sheet @ 8d74c47b5737, composition @
  302796210b, E-LG1 doc @ 16a2574f3d, G-CM1b doc @ 1005582b5c — all fetched
  (per-commit depth-1 fetches for objects beyond the depth-300 window) and
  byte-compared against the API copies: all `cmp`-clean.
- The 8d74c47b5737 commit is NOT in the depth-300 window (per-commit fetch
  confirmed its SHA/message/tree match the API).

## Environment notes

- Scratch only; nothing in /tmp; TMPDIR=/home/hatch/workspace/tmp_commit.
- No .zagd caches, no binaries committed (htd1_barcheck_bin stays in crew/ scratch).
- No live-web recapture: all content fetched at frozen commit SHAs via the
  GitHub API (committed evidence, not web facts). No outward sends.
- NON-INTERFERENCE: read-only API + scratch builds only.
