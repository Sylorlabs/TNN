# WAVE-2 CROSSREF CLOSEOUT — 2026-09-23

**Coordinator:** resume coordinator (previous closeout coordinator died quiet ~3.6h before resume; no output since 08:06 UTC, no closeout artifacts left behind — did not stand down, verified tally and workdirs independently).
**Wave-2 frozen prereg:** `crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f`.
**Tally source:** `T2/_wave2_tally/VERDICTS.md` (28/28 crew VERDICT.md present in workdirs, cross-checked).

## FINAL: 28/28 resolved — 26 REPRODUCED, 2 PARTIAL

| # | Crew | Verdict | One-line |
|---|---|---|---|
| 1 | T2-WEBV2 | REPRODUCED | Every leg figure re-derived; R-CORR vs R-CONTRA holds |
| 2 | T2-RAWVSHUMAN | REPRODUCED | colordisc 505/506, pitchdisc 131/132; rescue forks dead |
| 3 | T2-RSI1 | REPRODUCED | Hash-verified committed blobs |
| 4 | T2-BUGREAD | REPRODUCED | KB-D1C 24/24, KB-D1 30/30, tripwire does not fire |
| 5 | T2-JOKE | REPRODUCED | All bars match; frozen PARTIAL stands; vanishing-tree incident |
| 6 | T2-PROSE | REPRODUCED | 25/25 run logs byte-identical; Q(4.7) quality-matters boundary |
| 7 | T2-TRACKR0 | REPRODUCED | B-T1 FAIL stands; repair root cause = index overflow |
| 8 | T2-DUEL | REPRODUCED | Scenario-fit, no champion; grok 104 decomposition identical |
| 9 | T2-HELLHOLE | REPRODUCED | Binding FAIL confirmed; vanishing-tree incident |
| 10 | T2-DIALOGUE | REPRODUCED | 370/370 PASS; response digest exact |
| 11 | T2-SELFTEST | REPRODUCED | 40/40 + 400/400 oracle fidelity; vanishing-tree incident |
| 12 | T2-INFORICH | REPRODUCED | 7/7 kill bars PASS; colluding-domain spoof installs 2/2 (boundary) |
| 13 | T2-SCALEDOWN | REPRODUCED | Mastery 1.0000 at all N; 30/30 logs byte-identical |
| 14 | T2-TQ | REPRODUCED | 10/10 checks; no knee at any corruption level |
| 15 | T2-IMAG | REPRODUCED | 36/36 both modes; Q1V pin amendment recommended |
| 16 | T2-TRACKB | **PARTIAL** | arm-3 identity ambiguity → governance call (see §3) |
| 17 | T2-PARAMS | REPRODUCED | 59/59 logs byte-identical; 16/19 configs byte-identical digest |
| 18 | T2-AUDIOCONT | REPRODUCED | All six dispositions match; raw render battery never committed (bounds replication) |
| 19 | T2-CERT | REPRODUCED | 0 flips re-derived; dirty1_urandom plant unreproducible (artifact limit) |
| 20 | T2-HTD1 | REPRODUCED | Every kill/survive entry re-derives; G-CO3 rests on weighted reading |
| 21 | T2-SENSESINT | **PARTIAL** | 10/140 evidence paths missing incl 3 P0 (see §3) |
| 22 | T2-CLASS3DEC | REPRODUCED | Ran on prereg authority (frozen section has zero pins) |
| 23 | T2-GOALB | REPRODUCED | B1 16/16, B3 16/16; committed scorer is destructive on re-run (detected+restored) |
| 24 | T2-TRACKA | REPRODUCED | I1=KILLED adjudicated (churn 22.1% > 20% bar); 16/20/13/3 body count |
| 25 | T2-SPEEDINTEL | REPRODUCED | Coding 18/18 at 4x; epistemic plateau confirmed 59/94 |
| 26 | T2-CHAMP | REPRODUCED | All class figures re-derived in pure Zag, 3x byte-identical |
| 27 | T2-PROSEV3 | REPRODUCED | KB3-VIABLE FAIL reproduced; 220/220 logs byte-identical |
| 28 | T2-SENSESH2H | REPRODUCED | A 72.6% PASS / B 54.0% FAIL; sense_b rebuilt md5-identical |

## PARTIAL dispositions (a PARTIAL never ends a track)

### T2-TRACKB — GOVERNANCE CALL #1 for Micah
All 11 frozen claims re-derived (25/25 independent Zag checks PASS, 3/3 byte-identical; pcodec FROZEN_DECODE_PASS re-derived). The PARTIAL comes solely from the frozen rule's named condition: the arm-3 rebuild produced **three PASS variants**, creating genuine ambiguity about which is "the" arm:
- **varA** `7d056be` — pure-Zag deliberative adaptive teacher: PASS
- **varB** `d7929bb` — phase-scheduler teacher: PASS
- **varC** `f0031d9` — engagement-meter teacher: PASS

**Follow-up (committed plan):** Micah selects the authoritative arm-3 (or rules the arm irreducibly multi-variant); a seal crew then records the decision against the three variant pins. PARTIAL stands until ruled. Nothing failed; no bar misapplied.

### T2-SENSESINT — EVIDENCE RECOVERY PLAN
10/140 manifest evidence paths absent from the frozen commit, re-verified missing at current head `fa29b249` (genuine HTTP 404s, 2026-09-23; `v2/src/` listing shows only `ws2_*` files — no `gk*`):
- `senses/web-search/v2/src/gk1_trial.zag` (P0, PASS, size 5285)
- `senses/web-search/v2/src/gk2_trial.zag` (P0, PASS, size 6329)
- `senses/web-search/v2/src/gk3_trial.zag` (P0, PASS, size 4235)
- 7× `senses/web-search/internet-trial/evidence/phase1/*.jsonl` (P2, review-note)

The 3 missing P0 files are the GK1/GK2/GK3 trial sources — the load-bearing HTRF batteries behind "H1, H2, H3 all SUSTAINED" and headline digests `488af9ab…` / `7f351a53…` / `94575a9a…`. The digests cannot be re-derived from the committed record. Real evidence gap.

**2 size mismatches EXPLAINED (not corruption):** manifest recorded kb5.py 2189 / run_all.py 4302, but committed `docs/lab/senses/rematch/code/kb5.py` is 2731B and `run_all.py` is 5801B — and the independent T2-REMATCH heavy crew fetched and successfully used those exact sizes from the pinned rematch commit `1c01a1ad`. The manifest recorded stale sizes; the committed bytes are the live revisions.

**Follow-up (committed plan):**
1. Regenerate or re-run the GK1/GK2/GK3 trials from frozen specs; commit the sources under the manifest paths.
2. Recover the 7 P2 internet-trial phase1 jsonl, or formally downgrade the P2 items.
3. Correct the 2 manifest sizes (kb5.py 2731, run_all.py 5801).
4. Commit recovered evidence + amended verdict; on completion SENSESINT upgrades to REPRODUCED.

## Heavy-family orphans — adopted, not redone
- **T2-REMATCH** (senses long-horizon rematch): ALIVE and working as of 2026-09-23 ~15:05 UTC. Binary-evaluation pipeline running post-second-reboot (TRAIN_T3 at 18,000/37,000 records); TRAIN_T1 (740 rec) and TRAIN_T2 (7,400 rec) caches BYTE-IDENTICAL to the original crew's. VERDICT.md still open ([TO BE FILLED] results section). Adopted: results incorporated on completion. Not part of Wave-2's 28.
- **T2-LHADV** (coding LH-ADV-2): COMPLETE — REPRODUCED. Committed `102199e8` (VERDICT.md, RUNLOG.md, 3 ledgers under `docs/lab/crossref/runs/heavy/T2-LHADV/`). 3/3 byte-identical battery runs; fabrication 0.

## Anomalies carried (verdict-neutral, recorded)
- **Vanishing-tree incidents:** JOKE, HELLHOLE, SELFTEST, SENSESINT (×3) — clean/clone trees vanished mid-run, not in trash, disk healthy. Best hypothesis: zombie `git clone` processes from timed-out attempts racing recreated checkouts. All recovered; no verdict affected.
- **13 transcription-artifact brief pins** (all from replacement-batch briefs, e.g. `e7c5bcd6`, `02ffbc1be27a`, `8d0d6b9e9c9c`): every affected crew correctly fell back to the prereg's own pins per §1 authority.
- **T2-AUDIOCONT evidence gap:** the raw Type-A render battery (r2g.zag/r2b harness, patch/analysis scripts, renders) was never committed despite the frozen prereg promising "fixed sources committed after" — replication = independent re-measurement + exact statistical re-derivation. This bounds (not breaks) the replication strength.
- **T2-GOALB destructive scorer:** committed `score_b2_combined.py` CLOBBERS `clean/evidence/b2_combined.md` on re-run; crew detected it, restored the blob from API, re-swept 32 files clean.
- **T2-CERT artifact limit:** `dirty1_urandom` plant source calls `nio_open_readonly` + `_zag_rand` (unknown to the pinned toolchain) — that binary is unreproducible from frozen evidence.
- **Infra pattern:** full git clones infeasible on this VM under load (SIGKILL/OOM); crews used blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches with identical bytes.

## What remains open
1. T2-TRACKB governance call → **Micah's decision** (varA vs varB vs varC).
2. T2-SENSESINT evidence recovery (plan in §3).
3. T2-REMATCH final verdict (heavy-family; pipeline in progress).
4. `docs/lab/crossref/VERDICT_TABLE.md` not yet updated with Wave-2 rows (left for parent — table format/ownership).
5. **TIER 3 NOT LAUNCHED** — not claimed, not started.

## Files committed with this closeout
- `docs/lab/crossref/runs/T2/<28 crew names>/VERDICT.md` + `RUNLOG.md` (56 files)
- `docs/lab/crossref/runs/T2/_wave2_tally/VERDICTS.md` (full tally)
- `docs/lab/crossref/runs/T2/_closeout/CLOSEOUT_WAVE2.md` (this report)

All committed evidence is text; zero RNG in any decision path; pure-Zag verification where mechanisms were re-derived.
