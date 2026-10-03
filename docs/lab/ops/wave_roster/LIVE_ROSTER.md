# Wave Live Roster — TNN native-lab audit

Audited 2026-09-24 ~06:05 UTC (2026-09-23 ~23:05 PDT) by wave-audit subagent.
Method: 500 most recent commits on `tnn-native-lab` (spanning 2026-09-23T06:48Z → 2026-09-24T05:22Z),
local workdir mtimes, and live `ps` process list. Daemon restart 2026-09-23 wiped subagent handles;
status below is verified from live evidence, not vibes.

Statuses: RUNNING = live commits or processes within the audit window. STALLED = no commits/processes
and no done-verdict. DONE = verdict committed. BLOCKED-ON-MICAH = needs his word/signature, not a crew.

## Flagship lines (must stay visibly alive)

| wave | status | last evidence | crew/agent | next action |
|---|---|---|---|---|
| PAMs | RUNNING | 05:00Z SELF-PAM R2 Fork C commit `0a2e006c`; fs-e4b judge procs live | self-pam R2, PAM rebuild FS-E1/E4b crews | none; V4 next round HELD (see blocked list) |
| video | RUNNING (rewoken 2026-09-24) | MOTION4 round: prereg `f69f5653`, impl `ea94ab9e`, fixtures `da343904`, RM2 `c86c9182`, VERDICT `ff452f8f` — FAIL on K2 only, 6/7 pass | kill-battery crew done | repair round needs Micah's sign-off (prereg amendment) |
| audio | RUNNING | 05:14Z V11 fork P prereg `c1d57a2a`; voice_sig procs on fork_p live | V11 coordinator + forks G/P/R/W | none |
| image | BLOCKED-ON-MICAH | r10 beauty round + finalized oracle brief 09:24Z | — | Micah's eyes on r10 oracle brief |
| text | RUNNING | 18:29Z gap-closure fixes commit | gap-closure crew | monitor; 11h quiet is within tolerance |
| 1GB ingestion | RUNNING | 05:14Z 10GB crew-4 STATUS `e67d193e`; split_wiki.py live | 10GB phase-2 crew-4 | none |
| hell-hole | RUNNING | V4 red-team prereg frozen 20:50Z; local hh active ~2h ago (k1/k2/k3/k5 runs) | V4 red-team crew | none; verdict expected on completion |
| RSI | DONE | RSI-4 verdict 2026-09-23T00:00 (Grade A, open-ended invention) | — | RSI-5 is Micah's call (rounds 1–4 complete) |

## Other waves

| wave | status | last evidence | crew/agent | next action |
|---|---|---|---|---|
| r12_v4 round-3 fix | RUNNING | `znc r12_v4_r3.zag` compiling at 05:50Z (rt2fix3) | round-3 fix crew | none; verdict + fresh re-attack pending |
| H2 revival (adaptive liar) | DONE (round 1) | prereg `6bb794a8`, evidence `2ee2b09a` (216 files); 630 runs byte-identical | H2 revival crew done | PROVISIONAL — §11 unsigned, no verdict language; successor prereg (A5/A7/C1, ROW-ATTEST, D-COST, D-ESCROW) not started |
| live-ingestion hardening | RUNNING | 05:00Z LI-HARDEN-GLUE `9c959cd4` | LI-HARDEN crews | none |
| bytegen deep investigation | RUNNING | 04:46Z `1d97706d`; local bytegen active 0h | bytegen crew | none |
| memory self-org (MORG) | RUNNING | 05:02Z `03a1f171` fixtures+scorer | MORG crew 1 | none |
| H7 conscious swarm | RUNNING | grok47 round-1 debate prompt proc live 05:47Z | H7 swarm coordinator | none |
| H5 resolution | RUNNING | grok47 Q1 (knee) proc live 05:49Z in h5_resolution | H5 second-opinion follow-up | none |
| conscious perception | RUNNING | 03:45Z `8d53b18b`; local active 1h | perception crew | none |
| KB control | RUNNING | 02:55Z root-cause+redteam preregs; local active 0h | crews A–D | none; C1 build needs Micah greenlight |
| self-PAM R2 | RUNNING | 04:59Z `0a2e006c`; gh-api fetch proc live | selfpam R2 crew | none |
| FL2 other-kills | RUNNING | 01:26Z RT-F; fl2other local active 3h | FL2 RT crew | none |
| onebrain seam red-team | RUNNING | 02:12Z; local active 3h | onebrain crew B | none |
| threeworlds | RUNNING | 03:38Z; local active 1h | threeworlds crews | none |
| H4 deep audit | RUNNING | 04:04Z C3 verdict; local active 0h | H4 workstream A | none |
| H3 fixes | RUNNING | 04:41Z final report `01df1f47` | H3 fixes crew | none |
| H3 crew (novelty) | RUNNING | local h3_crew active 4h | H3 crew | none |
| H2 scratch co-evolution | RUNNING | local h2_scratch active 3h | H2 crew | none |
| fair-fight | RUNNING | 03:58Z `1b4df5de` | fair-fight crew | none |
| source-trust | RUNNING | 04:50Z `3f3a7a6b` (done) + 04:26Z synthesis | — | synthesis done; monitor |
| LI mode trials | RUNNING | 23:49Z Sep 23 cross-check | LI modes crew | none |
| T2-REMATCH (wave-2 heavy) | RUNNING | pipeline procs live since 04:36Z | rematch crew | none; final verdict on completion |
| wave-2 crossref | DONE | Tier-3 synthesis 21:43Z Sep 23; SENSESINT recovery committed 18:39Z | — | 3 open items (below) |
| trackb | RUNNING→wrapping | 21:40Z addendum; brief drafted | trackb crew | monitor; likely done |
| H7 broader-fix swarm | DONE | `508c19cb` (known completion) | — | — |
| PAMs v2 counsel | DONE | `81710b47` (known completion) | — | — |
| H5 second opinion | DONE | `73d883f0` (known completion) | — | resolution round running separately |
| H2 investigation | DONE | `7bd828b4` (known completion) | — | — |
| source-trust L+S review | DONE | `3f3a7a6b` (known completion) | — | — |
| PAMs v2 follow-ups | DONE | all 7 crews, clean commits (2026-09-24) | — | next round HELD |
| KB4 F2 appeal | DONE | binding verdict WRAPS 17:04Z Sep 23 | — | — |
| motion3 | DONE | VERDICT_MOTION3.md committed | — | — |
| senses-rematch | DONE | VERDICT: B STAYS DEAD | — | — |
| teacher-showdown Leg C | DONE | ran COMPLETE 2026-09-22 (audit window artifact); missing local evidence committed `ccd06d3e` 2026-09-24 | — | grok-4.7 champion teacher; Leg C +10.5pp clean, +26/−0 probes |

## Open wave-2 items (not stalls, tracked for parent)

1. T2-TRACKB governance → Micah's decision (varA vs varB vs varC).
2. T2-REMATCH final verdict → running (above).
3. `docs/lab/crossref/VERDICT_TABLE.md` wave-2 rows → left for parent (table ownership).

## Blocked on Micah (signature/word needed, NOT crew dispatches)

1. Imagination r10 oracle judgment — finalized oracle brief committed 09:24Z; his eyes.
2. PAMs v2 next round (V4 confirmatory trial + front-end red-team) — held unless he says go.
3. KB4 C1 six-task build greenlight.
4. RSI-5 frontier decision (rounds 1–4 complete, all Grade A/A−).
5. H7 Phase-2c sincere-discourse calibration corpus — awaits human sign-off.

## Re-dispatch briefs

### Brief #1 (TOP PRIORITY — flagship): video line coordinator — RESOLVED 2026-09-24, MOTION4 round complete

**What ran:** rematch verdict verified clean (B STAYS DEAD, branch copy byte-identical, 5 rematch commits resolve); caught the M3 source gap (motion3.zag never committed — closed as `9d8b7edc`, rebuilt byte-identical). Frozen prereg MOTION4 (`f69f5653`): coarse-to-fine coherence-field extension of M3, ≤1.5M ops. Implementation `ea94ab9e` (K6 determinism proven, 973,568 ops). RM1 fixtures `da343904` (252 clips), RM2 labels `c86c9182` (committed before any motion4 run). M3 baseline on RM1: 1/96 on 6px (≈0%), 0 false.
**Verdict (`ff452f8f`): MOTION4 FAILS — K2 only, 6/7 kill bars pass.** K3 blew past its bar (81.3% vs 40% on 6px fast motion, 0 false on 204 clips). K2 failed on both clauses: 1 false-STILL (p006, sub-E_FLOOR evidence let S2's STILL claim pass unchallenged through frozen P5) and moving-catch 7/26 < 25/26 (18 forced withholds via frozen still_dir_conflict rule). Fable audit: CONFIRM.
**Next:** repair round is a prereg amendment — revise frozen P5 so a scale blind to displacement d cannot claim STILL at d (kills both the 18 withholds and the p006 false-STILL), or rewrite K2's bar to scope 1px/frame out. Needs Micah's sign-off before any source is touched.

**Inherited state:** senses-rematch VERDICT committed (B STAYS DEAD: A 83.8% vs B 56.6% at T4; B never crossed A).
H3ADV video fixtures committed 07:52Z (part of Fork H3 counterfactual-predictive-state work).
Local video workdirs (senses-rematch, scratch_dvid1, tmp_vid, senses-v2) quiet 18–41h; no live video processes.
No video-specific commits since 07:52Z (~22h).
**Verify first:** `ps` for video processes (none found in audit); confirm senses-rematch VERDICT.md is
committed and clean; confirm no orphaned video crew workdir newer than 2026-09-23T12:00Z.
**Task for fresh crew:** video-flagship coordinator — (a) verify the rematch verdict landed cleanly on the
branch with no open items; (b) per the standing flagship-alive rule, draft the next preregistered video
experiment (what comes after the rematch verdict — e.g. motion-coherence fork or a V11-style coordinator
round), frozen BEFORE any implementation; (c) commit the prereg. Do NOT re-run the rematch.

### Brief #2: teacher-showdown Leg C verification — RESOLVED 2026-09-24

**Resolution:** the audit's "STALLED?" classification was an artifact of the 500-commit window
(2026-09-23T06:48Z → 2026-09-24T05:22Z), which did not reach back to the Leg C commits of 2026-09-22.
Leg C ran COMPLETE 2026-09-22; verdict `docs/lab/GROK47_OVERNIGHT/teacher/LEGC_VERDICT.md` (blob
`56dae906`) was already on branch. A verify crew independently re-verified: corpus SHA256 matches,
5/5 prose runs byte-identical, oracle cross-check 0-diff, Δ_clean = +24/228 (+10.5pp, z≈3.5), 26
probes gained / 0 lost. The only gap — primary prose evidence existed only locally — was committed
2026-09-24 as `ccd06d3e` (binaries/.zagd excluded). grok-4.7 is the champion teacher (Leg B
faithfulness blowout + Leg C prose win). Audit lesson: recursive-tree queries against
`tnn-native-lab` can silently truncate (~26k files); a 0-path filter result is not evidence of
absence — use the contents API at a commit ref.

---
Roster maintained at `docs/lab/ops/wave_roster/LIVE_ROSTER.md` (lab-relative `ops/wave_roster/LIVE_ROSTER.md`).
