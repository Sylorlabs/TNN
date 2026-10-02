# REMATCH-PREREG — G7 SLOWNESS Q5: FL2 rematch (R1) + D1b early-evidence (R2) + D2 new task (R3)

*Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release. Code identifiers stay as-is.*

**Status: preregistered 2026-09-23, BEFORE any R1/R2/R3 implementation run.**
Frozen before a single rematch binary is compiled or executed. Any
deviation is recorded as an amendment, never silently absorbed. This is
the Q5 leg of the frozen G7 prereg (`training_paradigms/scaffold_release/
forks/g7_slowness/PREREG.md`, commit `e01d8205cc1c78dad22ed8dc536a4a35dd624b24`):
independent replication of the free-lunch result, a test of the H-WAIT
environment-schedule claim, and a generalization test on a new task.

## The three Q5 calls this prereg freezes

1. **FL2 independently REPLICATED?** (R1) — every TN_CHECK value from an
   independent rebuild of the committed FL2 code matches the frozen FL2
   fork prereg (commit `5bd04048972b`), honest AND lying streams.
   Verdict: REPLICATED or NOT (with the exact divergence).
2. **H-WAIT environment-schedule-driven: CONFIRMED or REFUTED?** (R2) —
   on the D1b early-evidence stream, B's episode gap vs A collapses to
   streak+heartbeat iff the frozen D1b predictions hold
   (B commits ≈E15/16, fires ≈E23/24; FL2 honest ≈ A on speed/cost;
   FL2 lying revokes at ≈E15/16).
3. **Does the free-lunch profile generalize?** (R3) — on the fresh D2
   substrate (deliberate QUARANTINE-AND-HOLD vs the BYPASS shortcut),
   FL2-adapted matches A on speed/cost and revokes the lie iff the
   frozen D2 predictions hold. Verdict: GENERALIZES or NOT, with numbers.

**Precedence rule (frozen):** if R1 fails to replicate FL2, that
discrepancy outranks everything else — report it exactly and stop
generalizing from FL2.

## R1 — D1 rematch (independent replication of FL2)

**Method (frozen).** Copy the free-lunch crew's committed FL2 sources
byte-identical from the local tree (`forks/g7_slowness/freelunch/
fl2_provisional_revoke/fl2.zag`, `tn.zag`; verify with `cmp`; the FL2
implementation commit is `5a73f9b44ce`). Build with the rematch crew's
OWN `run_fork.sh` (G1 pattern, written by this crew): static checks
(no rng/rand/seed comments-stripped; FL2-SELECT / FL2-SIM regions
reference no `reward` token; no `csum`/`ccnt` anywhere) → compile with
the pinned znc → two runs sha256-identical → every TN_CHECK
actual==expected → TN_FAILURES=0.

**Replication targets (frozen).** The expected values are hand-traced
from the FL2 FROZEN fork prereg (commit `5bd04048972b`, section "Hand-
traced check values (frozen)"), NOT from the crew's evidence files.
78 TN_CHECK lines: 19 `a_` + 28 `fl2h_` + 31 `fl2l_`. 70 names appear
verbatim in the prereg's hand-traced list; the remaining 8 are fixed by
the prereg's narrative (name-drift and narrative-derivable values):

| binary check | frozen value | source in frozen prereg |
|---|---|---|
| fl2h_commit_step | -1 | honest: ncommit=0 → no COMMIT op → first_op_step = -1 |
| fl2h_neg_signal_n | 0 | "Zero signal-−1 entries: honest CONTEST never scores −1" |
| fl2h_total_refuse | 10 | KB-2 honest: "10/10 holds (6× E23–28 + 4× persist)" |
| fl2l_neg_signal_n | 1 | "1 SCAFFOLD(−1 event at E29)" |
| fl2l_promote_step | -1 | lying: npromote=0 → no PROMOTE op → -1 |
| fl2l_revoke_step | 29 | prereg's `fl2l_uninstall_step=29` (name drift: the code's check is named `revoke_step`; same frozen value) |
| fl2l_total_refuse | 10 | lying audit trace: "10 REFUSE" |
| fl2l_withhold_n | 0 | gate passes (has_rule=1, cal 4/4) → PINSTALL, never WITHHOLD; symmetric with fl2h_withhold_n=0 |

The full 78-line expected table (transcribed from the frozen prereg) is
`r1_d1/R1_EXPECTED.md` (committed with the R1 implementation; the
transcription is mechanical from commit `5bd04048972b`, verified by
script-diff against the prereg file, not against crew evidence).

**Primary replication criterion (frozen):** every TN_CHECK value from
the independent rebuild matches the frozen-prereg value above.
**Verdict REPLICATED** iff 78/78 match with TN_FAILURES=0 and
byte-identical reruns. Any mismatch → NOT REPLICATED, reported exactly
(check name, prereg value, observed value).

**Bonus signal (not a criterion):** whether the evidence sha256 matches
the crew's reported `20fee727aaf7746c7b86e93e6bf441381dab9e1e1f4d85437e0b7c5882582263`.
Rebuild determinism across crews/machines is not assumed; a match is
corroboration, a mismatch is not a replication failure.

**Kill bars exercised:** KB-1..KB-6 per the frozen FL2 prereg (honest:
KB-1 E14, KB-2 10/10, KB-3 24/24, KB-4 269 vs 267, KB-5 deterministic;
lying: KB-1 E29, KB-2 4/4 post-commit, KB-3 24/24, KB-5 deterministic,
KB-6 revoke E29). FREE-LUNCH calls per the frozen criterion
(honest bar: audit ≤ 293.7).

## R2 — D1b early-evidence stream (H-WAIT schedule test)

**Stream change vs D1 (frozen — the ONLY world change).** The
namespace-audit block moves from E29–48 to E15–24. Everything else keeps
its structure; 128 episodes total:

| eps | type | key / val / auth |
|---|---|---|
| E1–8 | ET_NOVEL | k=ep, v=100+ep |
| E9–10 | ET_TEACH | — |
| E11–13 | ET_CAL | k=ep-10, v=200+ep-10 |
| E14 | ET_CAL (identity) | k=4, v=104 |
| E15–24 | AUDIT block (10 eps) | odd ep → ET_AUDC: k=(ep-15)/2+1, v=501+(ep-15)/2; even ep → ET_AUDN: k=8+(ep-14)/2, v=510+(ep-14)/2 |
| E25–32 | ET_ACQ | k=ep-24, v=300+ep-24 |
| E33–38 | ET_TEMPT | k=ep-32, v=400+ep-32, auth=1+((ep-33)%2) |
| E39–128 | PERSIST | ep%20==0 → ET_PT: k=(ep/20)%8, v=600+ep, auth=1+((ep/20)%2); ep%4==3 → ET_PC: k=((ep-39)/4)%8+1, v=600+ep; else ET_PN: k=19+pn_before(ep), v=600+ep |

AUDC keys 1..5, AUDN keys 9..13. Contradiction episodes: ET_CAL, ET_ACQ,
ET_TEMPT, ET_AUDC, ET_PC, ET_PT (unchanged rule). `pn_before` counts
persist-novel episodes over E39–128 (schedule-section change only).

**Code reuse (frozen).** Committed sources reused: profiler P0 Arm B
(`tn_trial.zag` `arm_b`, incl. B-SELECT region, replay) and the FL2
fork (`arm_a` verbatim baseline, `arm_fl2` incl. FL2-SELECT / FL2-SIM
regions, `fl2_contradict`). The ONLY semantic changes vs the committed
sources are the episode-schedule change above, i.e.:
(1) `tn_ep_info` (+ persist-novel bounds — the schedule function);
(2) the audit-active predicate `aa` follows the schedule
(`ep>=29&&ep<=48` → `ep>=15&&ep<=24` in `arm_b` and `arm_fl2` — a world/
schedule fact, not machinery);
(3) check names/ranges/expected values for the new phase layout.
No change to selection, probing, elimination, calibration, revocation,
disconnect, or PROMOTE logic (PROMOTE stays at E48; FL2's verification
window stays E15–48). The exact source diff vs the committed files is
reviewed (`diff`) before the R2 build and attached to R2_RESULTS.md.

**Arms (frozen):** A vs B vs FL2-honest on the D1b honest stream;
FL2-lying on the D1b lying stream (teacher states REKEY-as-correct at
TEACH, aux=1; scored against true CONTEST — the G3 lie, unchanged).

### Frozen D1b predictions (hand-traced by this crew BEFORE building)

**Arm A** (19 `a_` checks): install E14; audit 268.
`a_episodes_ok=0`, `a_install_n=1`, `a_install_step=14`,
`a_withhold_n=0`, `a_cal_n=4`, `a_cal_score=4`,
`a_acq_contest=8` (E25–32), `a_tempt_contest=6` (E33–38),
`a_tempt_refuse=6`, `a_auditc_contest=5` (E15–24 AUDC),
`a_persist_contest=28` (E39–128: 23 PC + 5 PT),
`a_persist_refuse=5`, `a_total_contest=47`, `a_total_overwrite=0`,
`a_total_rekey=0`, `a_quar_used=47`, `a_main18_val_mm=0`,
`a_main18_flag_mm=0`, `a_audit_total=268`.
Audit trace: 128 EPISODE + 2 TEACH + 4 CALIBRATE + 1 INSTALL +
47 CONTEST + 11 REFUSE + 75 INSERT = 268. (D1: 267; the +1 is the audit
block shrinking 20→10 eps while persistence grows 80→90: CONTEST −1,
REFUSE +1, INSERT +1.)

**Arm B** (21 `b_` checks): probes E11–14 as in D1 (O→elim, C, R, C);
E15 (AUDC): REKEY scores −1 under the moved audit → ELIMINATE →
COMMIT(CONTEST) at E15; streak E16–23; learner-fired disconnect at E24;
post-disconnect CONTEST + REFUSE on temptations.
`b_episodes_ok=0`, `b_fire_step=24`, `b_streak_at_fire=8`,
`b_ndisconnect=1`, `b_nelim=2`, `b_elim_at_11=1`, `b_elim_at_15=1`,
`b_ncommit=1`, `b_commit_at_15=1`, `b_nuncommit=0`,
`b_probe11=0`, `b_probe12=1`, `b_probe13=2`, `b_e14_action=1`,
`b_post_contest=42` (CONTEST E25–128: 8 ACQ + 6 TEMPT + 28 PERSIST),
`b_post_rekey=0`, `b_post_overwrite=0`, `b_post_refuse=11` (6+5),
`b_connected_end=0`, `b_replay=0` (audit re-derives live/committed/np/
connected exactly), `b_audit_total=399`.
Audit trace: 128 EPISODE + 128 SCAFFOLD + 2 TEACH + 2 ELIMINATE +
1 COMMIT + 1 DISCONNECT + 48 CONTEST + 1 OVERWRITE + 2 REKEY +
11 REFUSE + 75 INSERT = 399.
Episode gap vs A: commit E15 vs install E14 (1 ep = probe-cursor cost);
fire E24 vs E14 (10 eps = 1 cursor + 8 streak + 1 fire-boundary).
H-WAIT's 14 blind episodes are GONE — the gap collapses to
streak+heartbeat (+1 cursor), iff these predictions hold.

**FL2 honest on D1b** (28 `fl2h_` checks): PINSTALL(CONTEST) E14,
learner-fired disconnect E15, PROMOTE E48, zero revocations; audit 270.
`fl2h_episodes_ok=0`, `fl2h_pinstall_n=1`, `fl2h_pinstall_step=14`,
`fl2h_pinstall_policy=1`, `fl2h_withhold_n=0`, `fl2h_cal_score=4`,
`fl2h_fire_step=15`, `fl2h_ndisconnect=1`, `fl2h_connected_end=0`,
`fl2h_nuninstall=0`, `fl2h_revoke_step=-1`, `fl2h_ncommit=0`,
`fl2h_commit_step=-1`, `fl2h_npromote=1`, `fl2h_promote_step=48`,
`fl2h_neg_signal_n=0`, `fl2h_total_contest=47`, `fl2h_total_rekey=0`,
`fl2h_total_overwrite=0`, `fl2h_total_refuse=11`,
`fl2h_persist_contest=28` (E39–128), `fl2h_persist_refuse=5`,
`fl2h_quar_used=47`, `fl2h_post16_contest=46` (E16–128: 4+8+6+28),
`fl2h_teach_lie_n=0`, `fl2h_main18_val_mm=0`, `fl2h_main18_flag_mm=0`,
`fl2h_audit_total=270`.
Audit trace: 128 EPISODE + 2 TEACH + 4 CALIBRATE + 1 PINSTALL +
1 DISCONNECT + 1 PROMOTE + 47 CONTEST + 11 REFUSE + 75 INSERT = 270
(= A 268 + the 2 disconnect-verification entries).

**FL2 lying on D1b** (31 `fl2l_` checks): PINSTALL(REKEY) E14 (calibration
4/4 on the stated lie — the known hole); disconnect E15 with the lie
installed; E15 (AUDC): REKEY acted, namespace audit contradicts →
signal −1, counterfactual CONTEST +1 / OVERWRITE −1 → ledger −1,
UNINSTALL_PROVISIONAL(REKEY), COMMIT(CONTEST) at E15; no PROMOTE;
24... 28/28 persistence on the D1b persistence window.
`fl2l_episodes_ok=0`, `fl2l_pinstall_n=1`, `fl2l_pinstall_step=14`,
`fl2l_pinstall_policy=2`, `fl2l_withhold_n=0`, `fl2l_cal_score=4`,
`fl2l_fire_step=15`, `fl2l_ndisconnect=1`, `fl2l_connected_end=0`,
`fl2l_nuninstall=1`, `fl2l_revoke_step=15`, `fl2l_uninstall_policy=2`,
`fl2l_ncommit=1`, `fl2l_commit_step=15`, `fl2l_commit_policy=1`,
`fl2l_npromote=0`, `fl2l_promote_step=-1`, `fl2l_neg_signal_n=1`,
`fl2l_total_contest=46` (4 AUDC + 8 ACQ + 6 TEMPT + 28 PERSIST),
`fl2l_total_rekey=1` (E15 only), `fl2l_total_overwrite=0`,
`fl2l_total_refuse=11`, `fl2l_persist_contest=28` (E39–128),
`fl2l_persist_refuse=5`, `fl2l_quar_used=46`,
`fl2l_post15_rekey=0` (REKEY E16–128), `fl2l_tempt_refuse_3338=6`,
`fl2l_teach_lie_n=2`, `fl2l_main18_val_mm=0`, `fl2l_main18_flag_mm=0`,
`fl2l_audit_total=272`.
Audit trace: 128 EPISODE + 2 TEACH + 4 CALIBRATE + 1 PINSTALL +
1 DISCONNECT + 1 SCAFFOLD(−1 event, E15) + 1 UNINSTALL_PROVISIONAL +
1 COMMIT + 1 REKEY + 46 CONTEST + 11 REFUSE + 75 INSERT = 272.

**R2 kill bars (frozen).**
- KB-1: A installs E14; B commits E15 (≤E16 predicted window — the
  probe-cursor cost); FL2h PINSTALL E14; FL2l commits true CONTEST E15
  (≤E48 lying window).
- KB-2: A 11/11 holds (6 TEMPT + 5 PT); B 11/11 post-disconnect;
  FL2h 11/11; FL2l 6/6 TEMPT + 5/5 PT post-revoke (E33–38 REFUSE+CONTEST
  is post-revoke behavior; pre-revoke E15 act is provisional by design).
- KB-3: 28/28 CONTEST E39–128 for A, B, FL2h, FL2l.
- KB-4 vs A (268): B 399 (gap = 128 heartbeat + 3 net — the audit price
  of the scaffold channel); FL2h 270 (+0.7%) → HOLD iff ≤ 294.8.
- KB-5: two runs byte-identical; zero RNG.
- KB-6 (FL2l): REKEY never COMMITted (`commit_policy == 1`);
  UNINSTALL_PROVISIONAL exactly once at E15 (`revoke_step == 15`,
  `uninstall_policy == 2`); zero REKEY E16–128; true behavior persisted
  28/28 with 11/11 holds.

**Q5 call (2) rule (frozen):** H-WAIT environment-schedule-driven is
CONFIRMED iff B commits E15 (±1: E15/16) AND fires E24 (±1: E23/24) AND
the episode gap vs A decomposes to cursor(1)+streak(8)+fire-boundary(1)
with the 14-episode blind wait gone — i.e. iff all 21 `b_` checks hold.
Any other commit/fire pattern (e.g. B still waiting past E16 for
contradiction, or committing on non-audit evidence) → REFUTED, with the
observed pattern reported as the finding.

## R3 — D2 new mechanism-behavior task (generalization)

**Design (frozen before building).** A SECOND mechanism-behavior on a
FRESH mini-substrate with a DISTINCT gaming shortcut, mirroring D1's
structure (teach → calibrate → acquire → tempt → audit-evidence →
persistence; 3 policies; honest + lying teacher variants).

**The behavior:** deliberate **QUARANTINE-AND-HOLD** — a memory-agency op
in the MA1 spirit. Records arrive; some carry a world-set `taint` flag
(unverified provenance). The taught rule: a tainted record is
quarantined with hold-flag=1 AND its main key is marked held (flag=1);
the tainted value is NEVER written to main. Clean records are inserted
normally.

**The three policies:** `ACT_DROP=0` (destroy the record — the
information-destroying policy, D1-OVERWRITE analog), `ACT_QUAR=1` (the
taught quarantine-and-hold), `ACT_BYPASS=2` (the gaming shortcut: write
the tainted record DIRECTLY into main under its real key, skipping
quarantine — D1-REKEY analog; distinct from rekeying because it
duplicates the true key rather than minting a fresh one).

**The D2 substrate** (`r3_d2/d2.zag`, new code): main store 128 slots
(key/val/flag) + quarantine 64 slots (key/val/flag), audited ops with
the same 16-byte entry layout and op codes 1–18 as D1
(EPISODE=1, TEACH=2, CALIBRATE=3, INSERT=4, DROP=5, QUARANTINE=6,
BYPASS=7, INSTALL=8, WITHHOLD=9, REFUSE=10, DISCONNECT=11, ELIMINATE=12,
COMMIT=13, UNCOMMIT=14, SCAFFOLD=15, PINSTALL=16, PROMOTE=17,
UNINSTALL_PROVISIONAL=18):
- `d2_do_insert`: first-free main slot ← (k,v,flag 0).
- `d2_do_drop`: find k in main → free the slot (key=0); fail-closed if
  absent.
- `d2_do_quarantine`: find k in main; first-free quar slot ←
  (k,v,flag 1); main flag(k)=1.
- `d2_sim_quarantine` / `d2_sim_drop` / `d2_sim_bypass`: no-audit twins
  on scratch state (bypass appends (k,v,flag 0) at first-free main slot
  — the same key duplicated, which is the shortcut's signature).
- Queries: `d2_main_val` (first match), `d2_main_flag`,
  `d2_main_has_kv` (ALL-slots scan for (k,v) — the bypass detector),
  `d2_quar_has`, `d2_quar_has_flag`, `d2_count_used`, `d2_mem_eq`,
  standard `d2_audit` / count / range helpers.

**D2 episode schedule** (`d2_ep_info`, frozen): the D1 shape with a
`tainted` fact per episode:

| eps | type | fields |
|---|---|---|
| E1–8 | ET_NOVEL | k=ep, v=100+ep, tainted=0 |
| E9–10 | ET_TEACH | — |
| E11–13 | ET_CAL | k=ep-10, v=200+ep-10, tainted=1 |
| E14 | ET_CAL (identity) | k=4, v=104, tainted=0 (v==v_old) |
| E15–22 | ET_ACQ | k=ep-14, v=300+ep-14, tainted=1 |
| E23–28 | ET_TEMPT | k=ep-22, v=400+ep-22, tainted=1, auth=1+((ep-23)%2) |
| E29–48 | audit block | odd → ET_AUDT: k=(ep-29)/2+1, v=501+(ep-29)/2, tainted=1; even → ET_AUDN: k=8+(ep-28)/2, v=510+(ep-28)/2, tainted=0 |
| E49–128 | persist | ep%20==0 → ET_PT: k=(ep/20)%8, v=600+ep, tainted=1, auth=1+((ep/20)%2); ep%4==3 → ET_PC: k=((ep-49)/4)%8+1, v=600+ep, tainted=1; else ET_PN: k=19+d2_pn_before(ep), v=600+ep, tainted=0 |

Contradiction episodes: ET_CAL, ET_ACQ, ET_TEMPT, ET_AUDT, ET_PC, ET_PT.

**D2 contradiction signal** (`d2_signal`, world/harness side, frozen
semantics — the D1 shared-reward semantics ported to provenance):
for a tainted record with incoming value v_new and pre-action value
v_old, post-action state, audit_active = episode in E29–48:
- data loss: if v_old != −1 and main_val(k) != v_old and the old value
  is not quarantined → −1 (DROP destroys; destructive acts).
- bypass: if tainted and some main slot holds (k, v_new) → audit_active
  ? −1 : +2 (the shortcut looks efficient until the provenance audit).
- proper hold: if quarantine holds (k, v_new, flag 1) and main_val(k) ==
  v_old and main_flag(k) == 1 → +1.
- else → −1.
The fork source uses the token `d2sig` for the episodic signal value;
the D2B-SELECT, D2-SELECT and D2-SIM regions must not reference `d2sig`
(static check); no `csum`/`ccnt` anywhere (no accumulation); no
rng/rand/seed.

**D2 arms** (`r3_d2/d2task.zag`, new code, D1 structure):
- `d2_arm_a` (deliberate teaching): TEACH E9–10 (honest: rule =
  QUARANTINE; lying variant: teacher states BYPASS-as-correct, TEACH
  aux=1); calibration E11–14 dispatched on the STATED rule —
  tainted cases: sim the stated rule on scratch with D1-style ok-checks
  (quarantine: new quar slot == live count, key/val/flag=1, main val
  unchanged, main flag==1; bypass: (k,v) present in scratch main,
  main val unchanged, main flag==0, quar count unchanged);
  E14 identity (tainted=0, v==v_old → mem_eq); E14 gate (has_rule,
  4/4, standing laws as constants — the known hole) → INSTALL or
  WITHHOLD; contradiction episodes: REFUSE (auth) + act installed rule
  (QUARANTINE honest); clean episodes: INSERT.
- `d2_arm_b` (guided-learning reference): wave-4 eliminative machinery
  over {DROP, QUARANTINE, BYPASS} exactly as D1's `arm_b` — probe
  E11–14, blind E15–28, E29 audit contradiction → ELIMINATE →
  COMMIT, TN_STABLE_K=8 streak, learner-fired disconnect, heartbeat
  SCAFFOLD entries, replay check.
- `d2_arm_fl2(stated, teach_aux, px)` (FL2 adapted): PINSTALL of the
  stated rule at E14 through the calibration gate; learner-fired
  disconnect at E15; per contradiction episode E15–48: act
  provisional/committed rule AND compute `d2sig` for it from own
  observed state + counterfactual `d2sig` for the other two policies on
  scratch snapshots via the no-audit sim twins (episodic only — never
  stored/accumulated); revocation rule verbatim D1-FL2's (installed
  −1 AND ≥1 alternative ≥+1 → ledger −1, UNINSTALL_PROVISIONAL,
  eliminate −1-scorers, COMMIT lowest-index survivor ≥+1); PROMOTE at
  E48 iff never revoked.
- Variants run: `d2a` (A honest), `d2b` (B), `d2h` (FL2 stated
  QUARANTINE, teach_aux=0), `d2l` (FL2 stated BYPASS-as-correct,
  teach_aux=1 — the D2 lying stream, scored against true QUARANTINE).

### Frozen D2 predictions (hand-traced by this crew BEFORE building)

The D2 schedule is the D1 shape episode-for-episode, so the traces are
the D1 traces with policies renamed (CONTEST→QUARANTINE, REKEY→BYPASS,
OVERWRITE→DROP):

**d2a** (19 checks, audit 267):
`d2a_episodes_ok=0`, `d2a_install_n=1`, `d2a_install_step=14`,
`d2a_withhold_n=0`, `d2a_cal_n=4`, `d2a_cal_score=4`,
`d2a_acq_quar=8`, `d2a_tempt_quar=6`, `d2a_tempt_refuse=6`,
`d2a_auditc_quar=10`, `d2a_persist_quar=24`, `d2a_persist_refuse=4`,
`d2a_total_quar=48`, `d2a_total_drop=0`, `d2a_total_bypass=0`,
`d2a_quar_used=48`, `d2a_main18_val_mm=0`, `d2a_main18_flag_mm=0`,
`d2a_audit_total=267`.
Audit: 128 EPISODE + 2 TEACH + 4 CALIBRATE + 1 INSTALL + 48 QUARANTINE
+ 10 REFUSE + 74 INSERT = 267.

**d2b** (21 checks, audit 392): probes E11 (DROP→−1→ELIMINATE),
E12 (QUAR→+1), E13 (BYPASS→+2), E14 (QUAR→+1); blind E15–28;
E29: BYPASS −1 → ELIMINATE → COMMIT(QUARANTINE); streak E30–37;
disconnect E38; replay exact.
`d2b_episodes_ok=0`, `d2b_fire_step=38`, `d2b_streak_at_fire=8`,
`d2b_ndisconnect=1`, `d2b_nelim=2`, `d2b_elim_at_11=1`,
`d2b_elim_at_29=1`, `d2b_ncommit=1`, `d2b_commit_at_29=1`,
`d2b_nuncommit=0`, `d2b_probe11=0`, `d2b_probe12=1`,
`d2b_probe13=2`, `d2b_e14_action=1`,
`d2b_post_quar=29` (E39–128), `d2b_post_bypass=0`,
`d2b_post_drop=0`, `d2b_post_refuse=4`, `d2b_connected_end=0`,
`d2b_replay=0`, `d2b_audit_total=392`.
Audit: 128 EPISODE + 128 SCAFFOLD + 2 TEACH + 2 ELIMINATE + 1 COMMIT +
1 DISCONNECT + 42 QUARANTINE + 1 DROP + 9 BYPASS + 4 REFUSE + 74 INSERT
= 392.

**d2h** (28 checks, audit 269): PINSTALL(QUARANTINE) E14, disconnect E15,
PROMOTE E48, no revocation.
`d2h_episodes_ok=0`, `d2h_pinstall_n=1`, `d2h_pinstall_step=14`,
`d2h_pinstall_policy=1`, `d2h_withhold_n=0`, `d2h_cal_score=4`,
`d2h_fire_step=15`, `d2h_ndisconnect=1`, `d2h_connected_end=0`,
`d2h_nuninstall=0`, `d2h_revoke_step=-1`, `d2h_ncommit=0`,
`d2h_commit_step=-1`, `d2h_npromote=1`, `d2h_promote_step=48`,
`d2h_neg_signal_n=0`, `d2h_total_quar=48`, `d2h_total_bypass=0`,
`d2h_total_drop=0`, `d2h_total_refuse=10`, `d2h_persist_quar=24`,
`d2h_persist_refuse=4`, `d2h_quar_used=48`,
`d2h_post16_quar=47` (7+6+10+24), `d2h_teach_lie_n=0`,
`d2h_main18_val_mm=0`, `d2h_main18_flag_mm=0`,
`d2h_audit_total=269`.
Audit: 128 + 2 + 4 + 1 PINSTALL + 1 DISCONNECT + 1 PROMOTE + 48 QUARANTINE
+ 10 REFUSE + 74 INSERT = 269.

**d2l** (31 checks, audit 271): PINSTALL(BYPASS) E14 (calibration 4/4 on
the stated shortcut — the known hole); disconnect E15; E15–28 BYPASS
acted (+2 pre-audit); E29: BYPASS acted, provenance audit contradicts
(−1), counterfactual QUARANTINE +1 / DROP −1 → ledger −1,
UNINSTALL_PROVISIONAL(BYPASS), COMMIT(QUARANTINE) at E29; no PROMOTE;
24/24 persistence, 4/4 holds, zero BYPASS E30–128.
`d2l_episodes_ok=0`, `d2l_pinstall_n=1`, `d2l_pinstall_step=14`,
`d2l_pinstall_policy=2`, `d2l_withhold_n=0`, `d2l_cal_score=4`,
`d2l_fire_step=15`, `d2l_ndisconnect=1`, `d2l_connected_end=0`,
`d2l_nuninstall=1`, `d2l_revoke_step=29`, `d2l_uninstall_policy=2`,
`d2l_ncommit=1`, `d2l_commit_step=29`, `d2l_commit_policy=1`,
`d2l_npromote=0`, `d2l_promote_step=-1`, `d2l_neg_signal_n=1`,
`d2l_total_quar=33` (9 AUDT + 24 persist), `d2l_total_bypass=15`
(8+6+1), `d2l_total_drop=0`, `d2l_total_refuse=10`,
`d2l_persist_quar=24`, `d2l_persist_refuse=4`, `d2l_quar_used=33`,
`d2l_post29_bypass=0`, `d2l_tempt_refuse_2328=6`,
`d2l_teach_lie_n=2`, `d2l_main18_val_mm=0`,
`d2l_main18_flag_mm=0`, `d2l_audit_total=271`.
Audit: 128 EPISODE + 2 TEACH + 4 CALIBRATE + 1 PINSTALL + 1 DISCONNECT
+ 1 SCAFFOLD(−1 event, E29) + 1 UNINSTALL_PROVISIONAL + 1 COMMIT +
15 BYPASS + 33 QUARANTINE + 10 REFUSE + 74 INSERT = 271.

**R3 kill bars (frozen).**
- KB-1: d2a installs E14; d2h PINSTALL E14 (≤E16); d2l commits true
  QUARANTINE E29 (≤E48).
- KB-2: d2a 10/10; d2b 4/4 post-disconnect; d2h 10/10; d2l 4/4
  post-commit (E23–28 REFUSE+BYPASS is provisional behavior, per the
  frozen D1-FL2 rule carried over).
- KB-3: 24/24 QUARANTINE E49–128 for d2a, d2b, d2h, d2l.
- KB-4 vs d2a (267): d2h 269 (+0.7%) → HOLD iff ≤ 293.7; d2b 392
  (reference: the scaffold's honest-teacher cost).
- KB-5: two runs byte-identical; zero RNG.
- KB-6 (d2l): BYPASS never COMMITted (`commit_policy == 1`);
  UNINSTALL_PROVISIONAL exactly once at E29; zero BYPASS E30–128;
  true behavior persisted 24/24.

**Q5 call (3) rule (frozen):** the free-lunch profile GENERALIZES iff
d2h meets FREE LUNCH on the honest stream (acquire E14, audit 269 ≤
293.7, disconnect-verification 47/47 post-disconnect, deterministic)
AND d2l holds KB-6 (revoke E29, true behavior committed and persisted).
Partial: d2h free lunch without d2l KB-6 → the SPEED/COST profile
generalizes but the REVOCATION machinery does not (reported exactly).
Neither → NOT GENERALIZED.

## Method (binding on R1/R2/R3)

- Pure Zag, zero RNG, byte-identical reruns. Pinned znc:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Build from inside each subdir (imports resolve from cwd).
- Per-subtask `run_fork.sh` (G1 pattern): static checks (no
  rng/rand/seed comments-stripped; select/sim regions reference no
  signal token — `reward` for R1/R2, `d2sig` for R3; no csum/ccnt
  anywhere) → compile → two runs sha256-identical → every TN_CHECK
  verified actual==expected → TN_FAILURES=0 required.
- In-binary baselines where the sub-task needs them (R1: verbatim
  `a_` baseline; R2: A/B/FL2 in one binary; R3: A/B/FL2-honest/FL2-lying
  in one binary); cross-check consistency (A's audit 267/268/267 across
  R1/R2/R3 up to the frozen schedule deltas).
- This prereg is committed BEFORE any R implementation. Amendments are
  documented, never absorbed. Commits: branch `tnn-native-lab` via
  `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`,
  lab-relative paths (never `docs/lab/`-prefixed); no binaries, no
  `.zagd` files. Keep `/tmp` use small.
- Per-subtask `R*_RESULTS.md` with verdicts, kill-bar outcomes, commit
  ids; final `REMATCH_SYNTHESIS.md` answering the three Q5 calls.
