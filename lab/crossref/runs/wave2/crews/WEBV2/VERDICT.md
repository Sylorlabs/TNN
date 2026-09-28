# T2-WEBV2 — web-search sense v2: live web works — REPLICATION VERDICT

**Crew:** T2-WEBV2 (independent replication session; different agent session from the original crew).
**Replication type:** C (evidence re-derivation; live web not re-hit).
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` §T2-WEBV2 (authoritative), read from a fresh clone.
**Evidence commit:** `ff97c7a08fcb` — "web-search sense v2: live transport, forced install-mode choice, R-CORR vs R-CONTRA".
**Date:** 2026-09-22.

## Verdict: REPRODUCED

Every leg figure re-derives exactly from committed evidence with independent Zag
code written by this crew; the R-CORR vs R-CONTRA distinction holds in the
evidence; the unanimous-spoof residual instances are exactly as described.
One evidence caveat is documented below (probe-bar raw battery).

## Committed vs re-derived figures

| Claim (commit ff97c7a08fcb) | Re-derived (independent Zag) | Match |
|---|---|---|
| search.lumy.live SearXNG JSON 10/10 probe bar | **Caveat:** no committed machine JSON for the 10-query lumy battery (`probe_results.json`, `reprobe_results.json` contain no lumy.live endpoint; the 10/10 rests on the prose table in `TRANSPORT_PROBE.md`). Corroborated operationally: **22/22** recorded lumy queries (21 `live/` envelopes + `LIVE_SMOKE.json`) return ≥6 usable results each (bar: ≥3), so KB-LIVE's bar (≥8/10 queries with ≥3 usable) is satisfied by committed machine data. | partial-evidence |
| Leg A 20/20 (10/10 unknowns searched; no-search baseline 0/10) | 10/10 known held (G0/D0), 10/10 unknowns searched (G1), 10/10 baseline lines `ans=unknown`, SUMMARY 20/20, installs=0 | ✓ exact |
| Leg B 6/6 dispositions | dispositions 2,2,4,1,2,6 vs expected 2,2,4,1,2,6; 0 installs, 0 false provisionals | ✓ exact |
| Leg C 12/12 teacher falsehoods caught | 12/12 lines D5 (catch), 0 installs | ✓ exact |
| Leg D 12/12 gate decisions | 6 required issued + correct (G1=E1), 6 unneeded not issued (G0=E0) | ✓ exact |
| Leg M 24/24 (12 cases × 2 modes) | 24/24 MC lines P1; full outcome matrix verified | ✓ exact |
| Leg R 24/24 (12 cases × 2 rules) | 24/24 MC lines P1; full outcome matrix verified | ✓ exact |
| Leg S 4/4, exactly 2 transport fires | 4 cycles, `transports=2` on both the S line and SUMMARY | ✓ exact |
| N=5 byte-identical replays per leg | all 5 run files byte-identical for all 7 legs; sha256 digests recomputed by independent Zag match `hash_manifest.txt` 7/7 | ✓ exact |
| R-CORR: 0 false installs outside the preregistered unanimous-spoof residual | installs under rule1/mode2: M5,M6 (residual) + M7,M8 (true) + M12 (audited override) only; M1–M4 withheld, M9–M11 refused | ✓ exact |
| R-CORR installs all true claims | M7,M8 → R7/NI1 under rule1 | ✓ exact |
| R-CORR withholds all single-source falsehoods | M1–M4 → R8/NI0 under rule1 (4/4) | ✓ exact |
| Read-only mechanically install-free (0 install ops) | 0 install ops in every mode-1 context: all 12 legM mode1 rows NI0/R8; legs A/B/C summaries `installs=0`; no D7 disposition anywhere; legs D/S have no install path | ✓ exact |
| R-CONTRA installs single-source falsehoods 4/4 (negative control) | M1–M4 → R7/NI1 under rule2 (4/4); also installs 1v1 first-seen M9–M10 (2/2), as predicted unsafe | ✓ exact |
| Honest residual: unanimous two-source spoof still fools | M5, M6 → R7/NI1 under BOTH rule1 and rule2 (mode2); exactly the two preregistered instances, no others | ✓ exact |

## What changed

Nothing. No figure moved, no bar flipped, no anomaly found. The verifier is
independent code (this crew's `verify_webv2.zag`, ~560 lines, pure Zag, zero
RNG) reading only committed evidence files; it re-derives each number from the
run-log line records rather than trusting the SUMMARY/VERDICT lines (those are
checked separately as consistency assertions).

## Evidence caveat (not a replication failure)

The committed "10/10 probe bar" for `search.lumy.live` is asserted in the prose
summary table of `transport/TRANSPORT_PROBE.md`, but the raw 10-query × lumy
machine battery is not in the commit: `probe_results.json` (first battery, with
the documented `usable`-flag script bug) and `reprobe_results.json` (fixed
re-probe) both lack any lumy.live endpoint. The live transport demonstrably
works on committed machine evidence — 21 recorded `live/` envelopes + 1
`LIVE_SMOKE.json`, all `"backend": "lumy"`, all with ≥6 usable results (bar: ≥3)
— which satisfies the prereg's KB-LIVE bar (≥8/10 queries with ≥3 usable).
The exact "10/10" number is therefore corroborated operationally but not
machine-re-derivable. This does not affect any leg score: legs A–D were scored
by replay over the recorded envelopes, whose provenance (lumy, hashes) is
committed.

## Frozen pins (SHA-256, recorded before work began)

- Prereg (SCOPE + TIER2): `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Evidence: `ff97c7a08fcbac3f832498456c51d28e82146d5d`
- `docs/lab/senses/web-search/v2/VERDICT.md`: `b3d7012fe78cf1ee24617837e7a5d0f988a4ff419ad6f30505952bbe291c54f1`
- `docs/lab/senses/web-search/v2/PREREG.md`: `de10ab221ea7e87ad19b740be659dbe7fded70325e3d25131e46a346b55566dd`
- `runs/20260922_020800/hash_manifest.txt`: `85f3b00706da6242218c001e0296f74d2b477810a64e97fde4f854ce06eb9042`
- `transport/TRANSPORT_PROBE.md`: `79a9157f6c73382910ce8e2f5678fbab4276930007309a24405503f5c27ffc13`
- znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- This crew's verifier outputs (3 runs, byte-identical): `6e192508db0ffce31c42e28c81f365a7d6f1848b6fe1d5f8aecbeb2663348bba`

## Method notes

- Fresh clone of `sylorlabs/TNN` branch `tnn-native-lab` into
  `~/workspace/scratch-crossref/T2/WEBV2/clean/`. (Bandwidth was saturated by
  parallel sibling-crew clones, so: `--depth 1 --filter=blob:none --no-checkout`
  partial clone, then `git fetch --deepen` to reach the pins; evidence paths
  checked out at `ff97c7a08fcb`, crossref docs at `7b2100d0`. `git diff` against
  both pins confirms every read file byte-matches its pin.)
- No `.zagd`/binary copies; verifier built from source with the pinned znc.
- Scratch only under `~/workspace/scratch-crossref/T2/WEBV2/`; `TMPDIR=/home/hatch/workspace/tmp_commit`.
- No live web touched (Type C). No live workstreams touched; only committed evidence read.
- Determinism: verifier run 3×, byte-identical stdout (sha256 above), exit 0.

## Artifacts

- `~/workspace/scratch-crossref/T2/WEBV2/crew/VERDICT.md` (this file)
- `~/workspace/scratch-crossref/T2/WEBV2/crew/RUNLOG.md`
- `~/workspace/scratch-crossref/T2/WEBV2/crew/verify/verify_webv2.zag` (independent verifier source)
- `~/workspace/scratch-crossref/T2/WEBV2/crew/verify/run{1,2,3}.out` (byte-identical outputs)
