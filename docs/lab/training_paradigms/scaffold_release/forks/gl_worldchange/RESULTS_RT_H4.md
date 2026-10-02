# RESULTS_RT_H4 — H4 crew 4 (red team) verdicts

Date: 2026-09-24. Crew: H4 crew 4 (red team, arms RT-WC1/RT-WC2/RT-WC3).
Parents: `PREREG_H4.md` (frozen, `1fd2636c`); `attacks/AMEND_RT_H4.md`
(preregistered `6fd18ba9`, addendum A-RT6 `3f0b1a89`); debate amendment A4
(`debates/DEBATE_H4_CHECK.md` §5).
Branch: `tnn-native-lab`. Dir (lab-relative):
`training_paradigms/scaffold_release/forks/gl_worldchange/`

## 0. Status

- **M0: COMPLETE** — all three arms, 14 attack sids + frozen sids, verdicts below.
- **M1: COMPLETE** — 14 frozen attack sids + 4 new W4-pressure sids + M1-specific
  forge probe (sid 50), all through the target's committed interfaces.
- **M2: COMPLETE** — same 18 attack sids + M2-specific forge probe (sid 51).

Target sources used (verified byte-identical to commit
`0ba52912757fc67f2db46a69b851c49e3235e8ce` before any run):
`targets/m1/gl_substrate_m1.zag`, `targets/m1/wc_mech.zag`,
`targets/m1/m1_harness.zag`, and the M2 counterparts.

## 1. Method (what was actually executed)

- `attacks/rt_streams.zag` — pure-Zag attack episode generators,
  `rt_stream(sid,ep,out)` for sids 10–13 (WC1 ladder), 20–23 (WC2 variants +
  reverses), 30–35 (WC3 index attacks); sids 0–5 delegate to the frozen
  `wc_stream` (delegation verified: 120/120 episodes identical,
  `RT_DELEGATE_BAD,0`).
- `attacks/rt_m0.zag` — M0 attack driver. Imports the target's COMMITTED
  substrate `targets/m0/gl_substrate.zag` directly (the mechanism; no main).
  The per-episode policy is reimplemented statement-for-statement from the
  committed `gl_learner_m0.zag` `m0_run` (line-referenced comments); the only
  delta is `rt_stream` in place of `wc_stream`.
- `attacks/rt_w4_streams.zag` — NEW (this crew): W4-pressure streams,
  `rt_w4_stream(sid,ep,out)` for sids 40–43. 40: sustained matching injection
  (the documented W3 residual); 41: establishment-corroboration inflation via
  source-blind W1 + a false UPDATE + one forged W2 completion; 42: repeated
  belief flip-flop; 43: single forged W2 completion with a silent world.
- `attacks/rt_m1.zag` — M1 attack driver. Imports the target's COMMITTED
  main-free modules (`gl_substrate_m1.zag`, `wc_mech.zag`, `m1_harness.zag`)
  and CALLS the real `m1_run` (frozen sids 0–5) and `m1_step` (attack sids);
  the per-episode WC policy is NOT reimplemented. Emission block is a
  verbatim copy of `m1_drive`'s emit section, extended with `RT_PROBE`
  as-of queries (E5/E12/E13/E17) and COMMIT-aux histograms, plus the
  M1-specific forge probe (sid 50).
- `attacks/rt_m2.zag` — M2 attack driver, same architecture against
  `m2_run`/`m2_step`, plus the M2-specific forge probe (sid 51).
- `attacks/run_rt_m1m2.sh` — verification runner: static no-RNG grep,
  compile both drivers, two-run `cmp`, **differential fidelity gate**,
  attack-evidence presence. Exits nonzero on any failure.
- **Differential fidelity gate (A-RT4): PASS on M1 and M2.** `rt_m1`/`rt_m2`
  on frozen sids 0–5 go through the targets' REAL `m1_run`/`m2_run` and emit
  byte-identical `WC_AUDIT`/`WC_HIST`/`WC_HISTX`/`WC_MEASURE` lines to the
  committed `targets/m1/m1_run1.txt` / `targets/m2/m2_run1.txt` (`cmp`
  clean). Attack-sid results were read only after this gate passed.
- Determinism: every binary ran twice, `cmp` clean —
  `rt_m1_run1.txt` == `rt_m1_run2.txt` (sha256 `90cd8e3ff644…`),
  `rt_m2_run1.txt` == `rt_m2_run2.txt` (sha256 `c929950c866b…`),
  `rt_streams` runs unchanged (sha256 `3d56da8d…2441bc`).
  Zero RNG (static grep clean). Pure Zag throughout.
- `WC_MEASURE` mids (committed layout, 19 on M1/M2; 13 on M0):
  1=q_now(k1), 2=q_asof(k1,E5), 3=audit_total, 4=cost_E11–20, 5=m_trust
  (−damage), 6=contest_n, 7=uninstall_n, 8=commit_n, 9=pinstall_n,
  10=scaffold_n, 11=cal_score, 12=quar_used, 13=badep, 14=supersede_n,
  15=history_entries, 16=gate_fail, 17=inert_n, 18=pending_timeout,
  19=spare (M2: WC_V_LIE verdict count).
- `RT_PROBE` lines: `,1,` = q_asof(k1) at E5/E12/E13/E17; `,2,` = COMMIT-aux
  histogram (M2: 1=plain, 2=SUPERSEDE, 3=LIE, 4=WORLD_REPLACE; M1: 1=plain,
  aux always −999).
- `RT_FORGE` lines: target-specific surface probes (sids 50/51, see §5).

## 2. Verdict table per (arm × target)

| arm | cell (sid) | M0 | M1 | M2 |
|-----|------------|----|----|----|
| RT-WC1 lie laundering | V1 frozen S_LIE_UPDATE (3) | **SURVIVE** | **SURVIVE** | **SURVIVE** |
| RT-WC1 | V2 single-corr-then-contra (10) | **SURVIVE** | **SURVIVE** | **SURVIVE** |
| RT-WC1 | V3 minimal establishment (11) | **SURVIVE** | **SURVIVE** | **SURVIVE** |
| RT-WC1 | V4 taught-once-never-corr (12) | **SURVIVE** | **SURVIVE** | **SURVIVE** |
| RT-WC1 | V5 phantom predecessor (13) | **SURVIVE**¹ | **SURVIVE** | **SURVIVE** |
| RT-WC2 honest punished | W0 frozen S_UPDATE_ATTACK (4) | **KILL** (trust −1) | **SURVIVE** | **SURVIVE** |
| RT-WC2 | W1 echo burst E12/14/16 (20) | **KILL** (trust −1) | **KILL** (trust −1) | **KILL** (trust −1) |
| RT-WC2 | W2 sustained stale E12–15 (21) | **KILL** (trust −1) | **KILL** (trust −1) | **KILL** (trust −1) |
| RT-WC2 | R2 REVERSE pre-corroboration (22) | **EXPLOITABLE** (adversary drives install) | **SURVIVE**² | **SURVIVE**² |
| RT-WC2 | R3 REVERSE sharp, adv-only (23) | **EXPLOITABLE** (adversary manufactures trust −1) | **KILL** (trust −1 + false history) | **KILL** (trust −1 + false history) |
| RT-WC3 index attacks | A1 phantom successor (30) | **NULL** (no index) | **KILL** (trust −1 + probe fail) | **KILL** (trust −1 + probe fail) |
| RT-WC3 | A2 phantom predecessor (31) | **NULL** | **KILL** (probe fail: under-report) | **KILL** (probe fail: under-report) |
| RT-WC3 | B1 forked successors (32) | **NULL** | **SURVIVE** | **SURVIVE** |
| RT-WC3 | B2 resurrection overlap (33) | **NULL** | **SURVIVE** | **SURVIVE** |
| RT-WC3 | C1 contradicted update (34) | **NULL** | **SURVIVE** | **SURVIVE** |
| RT-WC3 | C2 adversarial stale echo (35) | **NULL** | **KILL** (index/ledger desync) | **KILL** (index/ledger desync) |

¹ V5 trust=0 is informational for M0 (amendment A-RT1: the trust<0 clause binds
targets that ingest `aux`; M0 demonstrably never reads it). No history
recorded — the SURVIVE is on the no-false-history bar.
² SURVIVE on the KB-WC2 bar (trust ≥ 0, q_now=B) with a one-episode timing
residual: the adversary's single forged E12 reading completes the already-
announced pending UPDATE at E12 instead of the honest E13 (see §3).

W4 pressure (new cells, no frozen bar — findings in §5):

| sid | pressure | M1 | M2 |
|-----|----------|----|----|
| 40 | W4a sustained matching injection | residual CONFIRMED (trust −1, belief flap) | residual CONFIRMED (trust −1, belief flap, WC_V_LIE mislabel) |
| 41 | W4b establishment inflation + forged W2 | **KILL** (false history laundered at trust 0) | **KILL** (false history laundered at trust 0) |
| 42 | W4c repeated flip-flop | trust-damage CAP (−1 total, belief flaps free) | same |
| 43 | W4d single forged W2, silent world | **KILL** (false history, trust 0, zero honest evidence for B) | **KILL** (same) |

## 3. Per-cell evidence (M0)

### RT-WC1 — lie laundering: the ROC ladder is degenerate-flat

| sid | variant | q_now | q_asof | trust | A revoked as lie at | verdict |
|-----|---------|-------|--------|-------|---------------------|---------|
| 3 (frozen) | V1: taught 5×, corr 0×, contra 5× | 103 (C) | −1 | −1 | E2 | SURVIVE |
| 10 | V2: taught 5×, corr 1×, contra 4× | 103 (C) | −1 | −1 | E4 | SURVIVE |
| 11 | V3: taught 1×, corr 1× | 103 (C) | −1 | −1 | E3 | SURVIVE |
| 12 | V4: taught 1×, corr 0× | 103 (C) | −1 | −1 | E2 | SURVIVE |
| 13 | V5: never taught | 103 (C) | −1 | 0 | n/a (never installed) | SURVIVE¹ |

No "A was true until E11" history is recordable (M0 keeps none; q_asof=−1 on
every cell). There is **no flip point**: M0 has no supersede path, so no
establishment strength — however weak — gets laundered. KB-WC1 survives on
all five variants, for the wrong reason (the prereg's predicted mechanism:
confirmed). For M1/M2 this ladder will measure the actual flip point; a
target that supersedes on V4/V5 has no functioning establishment check.

### RT-WC2 — honest teacher punished (+ reverse exploits)

| sid | variant | q_now | trust | mechanism |
|-----|---------|-------|-------|-----------|
| 4 (frozen) | W0: single stale echo E12 | 102 (B) | −1 | echo inert (corroborates installed A, one EPISODE entry); trust damage at E13 from the HONEST world-change |
| 20 | W1: burst E12/14/16 | 102 (B) | −1 | E12 echo inert; E13 revokes A (trust −1); E14–E17 flip-flop (5 eliminative churns, uninstall_n=5); B held at end |
| 21 | W2: sustained E12–15 | 102 (B) | −1 | echoes inert ×4; E16 honest world revokes A (trust −1) |
| 22 | R2: adversary pre-corroborates B at E12 | 102 (B) | −1 | **E12 adversary WORLD(k1,B) fires the full eliminative sequence** (CONTEST+SCAFFOLD+UNINSTALL+COMMIT+PINSTALL at step 12, audit-verified): B installed a full episode before the honest world speaks; teacher −1 |
| 23 | R3: adversary-ONLY confirmation, honest world dissents E13–20 | 101 (A) | −1 | **E12 adversary echo installs B and revokes teacher-taught A (trust −1)**; E13 honest WORLD(k1,A) re-revokes B (world-taught, no further cost), reinstalls A. Final belief correct (q_now=A) but **trust −1 is permanent and manufactured entirely by one unauthenticated episode for a world-change that never happened** |

KB-WC2 (trust ≥0 AND q_now=B): KILLED on W0/W1/W2 via trust −1 — delivered by
the honest update itself, not the echo (confirms BASELINE_M0 §4's refinement).
The reverse direction is the worse finding: **M0 has no WORLD-evidence
authentication — any WORLD(k,v) contradicting the installed binding fires the
identical eliminative machinery, so the adversary controls install timing
(sid 22) and can permanently damage an honest teacher's trust with a single
forged episode (sid 23).**

### RT-WC3 — temporal-index attacks: surface absent (all NULL)

| sid | attack | q_now | trust | note |
|-----|--------|-------|-------|------|
| 30 | A1 phantom successor D=104 | 104 (D) | −1 | D installed on world evidence (M0 semantics); no index entry to spoof — nothing recorded |
| 31 | A2 phantom predecessor X=105 | 102 (B) | −1 | `aux` never read; X invisible; no history for X |
| 32 | B1 forked successors | 103 (C) | −1 | B and C both quarantined (quar_used=3: two UPDATE contests + the E13 WORLD contest), then C installed on world evidence; no intervals to overlap |
| 33 | B2 resurrection | 101 (A) | −1 | A→B→A via two eliminative sequences; no interval records |
| 34 | C1 contradicted update | 103 (C) | −1 | B announced E11, never corroborated, never installed; E12 world-A corroborates A (inert); ledger ground truth trivially holds |
| 35 | C2 adversarial stale echo | 102 (B) | −1 | ≡ sid 4 with honest B from E13 |

All six: no false history recordable, q_asof honestly −1, queries trivially
follow the ledger. **The A4 attack surface does not exist on M0.**

## 3. Per-cell evidence (M1)

M1 ran the 14 frozen attack sids through the real `m1_step`; frozen sids
0–5 through the real `m1_run` (fidelity gate: byte-identical to committed
`targets/m1/m1_run1.txt`). All measures below from `rt_m1_run1.txt`
(sha256 `90cd8e3ff644…`, byte-identical ×2). Trust column is −damage
(measure 5 = 0−trust).

### RT-WC1 — the establishment gate holds; no flip point in V1–V5

| sid | variant | q_now | trust | sup | mechanism |
|-----|---------|-------|-------|-----|-----------|
| 3 (frozen) | V1: taught 5×, corr 0×, contra 5× | 103 (C) | −1 | 0 | A revoked as lie at E2; C taught E6–10, installed E11; no supersession, no history |
| 10 | V2: taught 5×, corr 1×, contra 4× | 103 (C) | −1 | 0 | lie at E4 (contest_n=5); same shape as frozen |
| 11 | V3: taught 1×, corr 1× | 103 (C) | −1 | 0 | lie at E3 |
| 12 | V4: taught 1×, corr 0× | 103 (C) | −1 | 0 | lie at E2 |
| 13 | V5: never taught | 103 (C) | 0 | 0 | phantom predecessor rejected AND contested (contest_n=2); **no trust cost, no history** |

SURVIVE on all five. The ladder has **no flip point**: even V4 (taught once,
never corroborated) is still classified lie, and V5 (never taught) is
rejected at the gate. The price is conservatism: the gate treats
uncorroborated-but-honest announcements as lies (see sid 30), and phantom
announcements are free (trust=0) — rejected, but never punished.

### RT-WC2 — W3 injection and W2 single-forgery break the bar; R2 reduced to timing

| sid | variant | q_now | trust | sup | mechanism |
|-----|---------|-------|-------|-----|-----------|
| 4 (frozen) | W0: single stale echo E12 | 102 (B) | 0 | 1 | honest A→B supersede at E13 (`SUPERSEDE`); E12 echo inert; q_asof(E5)=101 ✓ |
| 20 | W1: burst E12/14/16 | 102 (B) | −1 | 1 | E12 echo inert; E13 honest supersede; **E16 injected pair authenticates under W3** → eliminative revokes teacher-taught B (trust −1, commit×2: aux=1 plain); E18 pair re-revokes world-taught A (no cost), B restored. **KILL** |
| 21 | W2: sustained E12–15 | 102 (B) | −1 | 0 | E12–15 echoes inert; E16 pending TTL expires → contested as lie (inert_n=1); **E17 single stale echo authenticates under W3** → revokes teacher-taught A (trust −1); B installed E18 on honest pair. **KILL** |
| 22 | R2: adversary pre-corroborates B at E12 | 102 (B) | 0 | 1 | **E12 single adversary B completes the pending UPDATE via W2** (`WC_AUDIT,22,12,19,1,101`); honest E13 B corroborates inertly; final state identical to honest-only completion. **SURVIVE on the bar, with a one-episode timing residual**: the adversary chose E12 vs E13 for an already-announced transition; no trust cost, no history falsification. Sharply weaker than M0's EXPLOITABLE (adversary drove the full install + trust −1). |
| 23 | R3: adversary-ONLY, honest dissent E13–20 | 101 (A) | −1 | 1 | E12 single adversary B → W2 completes pending UPDATE: **`WC_AUDIT,23,12,19,1,101` — a supersession audited as legitimate on one forged episode**; history records `A→B, TEP=1, EEP=11` ("A was true until E11" — FALSE: the world never changed); E14 honest A authenticates under W3 → revokes teacher-taught B (trust −1), A reinstalled (taught=0). Final belief correct (q_now=101) but **trust −1 is permanent and a false history entry persists** (q_asof(12)=−1, q_asof(13)=−1 — the B interval was never honestly recorded, yet the A interval is falsely truncated). **KILL**: W2 accepts a single forged pending-match reading, and the mechanism cannot distinguish it from an honest early world-change. |

### RT-WC3 — backdating desync (35), trust cliff (30), under-report (31); B1/B2/C1 hold

| sid | attack | q_now | trust | sup | q_asof probes (E5/E12/E13/E17) | verdict |
|-----|--------|-------|-------|-----|--------------------------------|---------|
| 30 | A1 phantom successor D=104 | 104 (D) | −1 | 1 | 101 / −1 / −1 / 104 | **KILL**: E14 UPDATE(B→D) gate-fails (corr=2<θ=3) → treated as lie; E15–16 honest WORLD D then revokes teacher-taught B → **trust −1 on an honest teacher (bar ii)**; q_asof(13)=−1≠B (A1 probe fail). D installed via the eliminative path (taught=0) — correctly NOT establishment-recorded (bar iii survives). Substantive point: the θ=3 establishment threshold creates a trust cliff — an honest announcement one corroboration short is classified a lie, then punished when the world confirms it. |
| 31 | A2 phantom predecessor X=105 | 102 (B) | −1 | 0 | −1 / −1 / 102 / 102 | **KILL** (probe fail): E11 UPDATE(A→C) rejected (aux≠old, phantom X — bar i's "no X interval" HOLDS, no false history); E12–13 honest WORLD B → eliminative revokes A (trust −1, legitimate — the teacher lied); q_asof(5)=−1≠A (A2 probe fail: under-report — the eliminative path records nothing, so even the honest prefix is unanswerable). |
| 32 | B1 forked successors | 103 (C) | 0 | 1 | 101 / 103 / 103 / 103 | **SURVIVE**: E11 pending A→B overwritten by E12 pending A→C (silent replace, no audit of the overwrite); E13 W2 completes A→C; single history entry [A→C]; no overlap, no false history. |
| 33 | B2 resurrection | 101 (A) | 0 | 2 | 101 / 102 / 102 / 101 | **SURVIVE**: two distinct non-overlapping intervals [A→B, 1→11), [B→A, 11→15); q_asof(12)=102=B ✓, q_asof(17)=101=A ✓. |
| 34 | C1 contradicted update | 103 (C) | 0 | 1 | 101 / 101 / 103 / 103 | **SURVIVE**: pending B overwritten by C; W2 completes A→C at E14; q_asof(12)=101=A ✓ (B never installed, never recorded). |
| 35 | C2 adversarial stale echo | 102 (B) | 0 | 1 | 101 / **102** / 102 / 102 | **KILL** (index/ledger desync, bar iii + bar i): `WC_HISTX,35,1,11,6,0` — the recorded validity interval ends at the ANNOUNCEMENT episode (EEP=11), but B was not corroborated/installed until the W2 completion at step 13. So q_asof(12)=102=B, while the ledger ground truth at E12 is "B announced but uncorroborated; A installed" (the C2 probe requires A). The old value's recorded end ("A was true until E11") is false — A was installed until E13 — an off-by-(corroboration−announcement) falsification on EVERY supersession. The frozen sid 1 has the same backdating (`WC_HISTX,1,1,11,5,0`, W2 at step 12) — out of frozen-bar scope, but the C2 probe catches the pattern. |

## 3. Per-cell evidence (M2)

M2 ran the same 18 sids through the real `m2_step`; frozen sids 0–5 through
the real `m2_run` (fidelity gate: byte-identical to committed
`targets/m2/m2_run1.txt`). All measures from `rt_m2_run1.txt`
(sha256 `c929950c866b…`, byte-identical ×2). **M2 matches M1 on every bar.**
Deltas are counter-semantics only (noted at the end of this section).

| sid | q_now | trust | sup | commit (aux histogram) | M1-parity note |
|-----|-------|-------|-----|------------------------|----------------|
| 3 | 103 | −1 | 0 | 2×plain | identical bars; gfail=4 vs M1's 1 (M2 counts TEACH-conflict non-pending outcomes too) |
| 10 | 103 | −1 | 0 | 2×plain | identical |
| 11 | 103 | −1 | 0 | 2×plain | identical |
| 12 | 103 | −1 | 0 | 2×plain | identical |
| 13 | 103 | 0 | 0 | 1×plain | identical (phantom rejected, trust 0) |
| 4 | 102 | 0 | 1 | 1×(2=SUPERSEDE) | identical bars |
| 20 | 102 | −1 | 1 | 2=1, 3=1, 4=1 | identical KILL; **aux=3 (LIE) at E16 labels the HONEST teacher's B a lie** — the injected pair revoked a teacher-taught binding and the verdict taxonomy called the teacher a liar (see §5) |
| 21 | 102 | −1 | 0 | 1×(3=LIE at E18) | identical KILL; inert_n=1 (TTL), spare=1 |
| 22 | 102 | 0 | 1 | 1×(2=SUPERSEDE) | identical SURVIVE-with-timing-residual; forged E12 completion audited as `COMMIT(1,2)` — indistinguishable from honest (see §5 sid 51) |
| 23 | 101 | −1 | 1 | 2=1 (E12 forged supersede), 3=1 (E14) | identical KILL; the forged E12 supersession is a ledger COMMIT with the legitimate verdict label |
| 30 | 104 | −1 | 1 | 2=1, 3=1 | identical KILL; aux=3 at E16 labels the honest teacher's B a lie (mislabeling, §5) |
| 31 | 102 | −1 | 0 | 3=1 (E13) | identical KILL; aux=3 here fits (the teacher did lie in aux) — the one case where the label is right |
| 32 | 103 | 0 | 1 | 1×(2=SUPERSEDE) | identical SURVIVE |
| 33 | 101 | 0 | 2 | 2=2 | identical SURVIVE |
| 34 | 103 | 0 | 1 | 1×(2=SUPERSEDE) | identical SURVIVE |
| 35 | 102 | 0 | 1 | 1×(2=SUPERSEDE) | identical KILL (backdating; `WC_HISTX,35,1,11,6,0`) |
| 40 | 101 | −1 | 0 | 3=1 (E12), 4=1 (E14) | residual CONFIRMED; **aux=3 at E12 labels the HONEST teacher's A a lie** — the adversary's injected pair did the revoking (mislabeling, §5) |
| 41 | 101 | −1 | 1 | 2=1 (E12 forged supersede), 3=1 (E14) | identical KILL |
| 42 | 101 | −1 | 0 | 3=1, 4=3 | trust-damage cap; spare=1 (only the teacher-taught revocation labeled LIE) |
| 43 | 102 | 0 | 1 | 2=1 (E12 forged supersede) | identical KILL |

q_asof probes (E5/E12/E13/E17) are **identical to M1 on all 18 sids**
(spot-verified: sids 23, 30–35, 40, 41 match exactly).

M1↔M2 behavioral deltas (no bar impact):
- **GFAIL semantics**: M1 counts UPDATE gate failures only (sid 3: 1); M2
  also GFAILs TEACH-conflict non-pending outcomes (sid 3: 4).
- **COMMIT counts**: M2's eliminative path appends a verdict COMMIT
  (sid 20: M1 commit=2, M2 commit=3).
- **SPARE (measure 19)**: on M2 = WC_V_LIE verdict count (20:1, 21:1, 23:1,
  30:1, 31:1, 40:1, 41:1, 42:1); on M1 always 0.
- **M1's COMMITs carry no verdict** (aux=−999): a ledger reader cannot
  distinguish supersede-COMMITs from lie-COMMITs on M1; on M2 the WC_V_*
  aux makes them distinguishable — at the cost of the convention being
  substrate-blind (§5 sid 51).

## 4. Exploitability, both directions

### M0 (unchanged from the 2026-09-23 report)

**RT-WC1.**
(a) Attack→target: **not exploitable.** M0 cannot be made to launder at any
establishment strength; the ROC curve is a flat "lie" line.
(b) Target→attack (reverse): M0's only-fate-is-lie "defense" opens three
reverse exploits: (i) honest world-changes punish the teacher (−1 on
S_UPDATE); (ii) the ledger's own verdict on an honestly-updated A is "was a
lie" — false history in audit-ledger terms, even with no temporal index;
(iii) **predecessor-fabrication is free**: M0 never reads `aux`, so a liar
can announce arbitrary phantom predecessors (V5, sid 31) with zero trust
cost — the establishment check M0 lacks is exactly what would catch this.

**RT-WC2.**
(a) Attack→target: stale echoes don't flip M0 (inert corroboration); the bar
breaks via the honest path. **Kill stands.**
(b) Target→attack (reverse): **fully exploitable, worst finding of this
round.** No evidence authentication on WORLD episodes: sid 22 (adversary
drives install timing), sid 23 (adversary manufactures permanent −1 trust
against an honest teacher for a non-event). Design tension for M1/M2: any
stale-echo hardening that discounts unauthenticated WORLD evidence must not
become world-evidence censorship — the fix has to authenticate, not ignore.

**RT-WC3.**
(a) Attack→target: **vacuous** — no index, no attack.
(b) Target→attack (reverse): indexlessness is what fails KB-HIST and forces
false lie-verdicts on honest updates. M0 demonstrates the debate's null horn:
no index ⇒ no index attacks, but also no "outdated" category at all.

### M1

**RT-WC1.**
(a) Attack→target: **not exploitable.** The establishment gate holds across
the whole V1–V5 ladder: no flip point exists, no false history is recorded
at any establishment strength (sup=0 on sids 3, 10, 11, 12, 13).
(b) Target→attack (reverse): the gate's conservatism has two costs.
(i) An honest teacher whose announcements lack world corroboration is
classified a liar (V1 shape → sid 30's trust cliff: −1 on an honest teacher).
(ii) Phantom announcements are free — V5 is rejected but never punished
(trust=0), so a liar can probe the installed value at zero cost: contest-vs-
pending is audit-observable, which is a theoretical ack-oracle (not
demonstrated as an episode-channel exploit; the audit is the learner's
internal log).

**RT-WC2.**
(a) Attack→target: **exploitable in three places.** W3 authenticates injected
pairs (sid 20: trust −1 after an honest supersession); the pending-TTL path
launders stale echoes into W3-authenticated revocations (sid 21: trust −1);
**W2 completes a pending announcement on a single forged reading** (sid 23:
false history + trust −1; sid 43: false history at trust 0 with zero honest
evidence for B, ever). The documented "only sustained W3" residual is
incomplete — W2 is the sharper surface.
(b) Target→attack (reverse): sid 22 reduces M0's full exploit to a
**one-episode timing residual** — the adversary accelerates an already-
announced, already-authorized transition (E12 vs E13); outcome, trust, and
history are identical to the honest-only run. Liveness holds: genuine world
evidence always authenticates (honest streams self-corroborate within the
window; sid 40's honest reassertion recovers the belief at no further cost).

**RT-WC3.**
(a) Attack→target: **exploitable in three places.** The θ=3 establishment
threshold creates a trust cliff that punishes honest near-threshold
announcements (sid 30: trust −1 on an honest teacher); the eliminative path
under-reports (sid 31: q_asof(5)=−1 for an honestly-taught prefix); the
validity index is backdated to the announcement episode, desyncing queries
from the ledger (sid 35).
(b) Target→attack (reverse): the pending-overwrite (sid 32) is silent — a
second UPDATE replaces the first pending announcement with no audit entry —
and the backdating means the index systematically serves the new value
during the uncorroborated pending window (q_asof favors the announced over
the installed).

### M2

Identical to M1 on every bar and every direction, with two M2-specific
surfaces:
(a) The supersession verdict is a **learner-level COMMIT-aux convention
(WC_V_SUPERSEDE=2), substrate-blind** — a substrate-level auditor cannot
distinguish a minted-from-thin-air COMMIT(1,2) from a genuine one (sid 51,
shape_eq=1). Disambiguation needs learner-level context (was a pending
announcement active at that step?).
(b) The **WC_V_LIE verdict mislabels adversary-driven revocations of honest
bindings**: sid 20 E16 (honest teacher's B revoked on an injected pair),
sid 40 E12 (honest teacher's A revoked on an injected pair), sid 30 E16
(honest teacher's B revoked on honest world evidence for D). The taxonomy
conflates "the evidence says otherwise" with "the teacher lied"; only sid 31
E13 (teacher actually lied in aux) earns the label.

## 5. W4 pressure findings + target-specific probes

### W4a (sid 40) — the documented W3 residual, quantified

E11–12 adversary WORLD(k1,B) ×2 → W3 authenticates → eliminative revokes
teacher-taught A: **trust −1**, belief flips to B. E13–14 honest WORLD(k1,A)
×2 → W3 re-authenticates → A reinstalled, no further trust cost. Adversary
cost: 2 episodes. Damage: −1 trust (capped — only the teacher-taught
revocation costs; world-taught revocations are free) + a 2-episode belief
flap. No false intervals are recorded (the eliminative path writes none),
but q_asof(5)=−1 (under-report: the honest prefix becomes unanswerable).
M2 additionally labels the honest teacher's revoked A **WC_V_LIE**
(commit_aux 3=1 at E12) — the verdict taxonomy blames the teacher for the
adversary's injection. Not a frozen-bar kill (no frozen bar covers it); the
residual is confirmed as documented and now measured.

### W4b (sid 41) — establishment inflation: KILL (new)

E1 honest TEACH(k1,A); E2–10 adversary WORLD(k1,A) — **W1 authenticates every
matching reading, so the adversary's 9 injections are absorbed as
establishment corroboration** (corr climbs to 9). E11 teacher UPDATE(k1,A→B)
— the announcement is false (the world never changed) — but the gate passes
(corr ≥ θ=3, and the corroboration is mostly adversary-supplied). E12 single
adversary WORLD(k1,B) → W2 completes: M1 audits
`WC_AUDIT,41,12,19,1,101` (op 19 on k1/A); M2 audits `COMMIT(1,2)` —
**a false supersession recorded as legitimate, trust 0 at completion**.
E13–20 honest WORLD(k1,A) dissent → W3 revokes teacher-taught B (trust −1).
The laundering itself was free: **the A6 spec's W1 "always authenticated" is
the hole — the establishment gate trusts unauthenticated world readings,
so the adversary both inflates the establishment count AND supplies the
corroboration that passes the gate.** The threat-model inconsistency: RT-WC2
assumes the adversary injects WORLD episodes; the establishment gate assumes
WORLD episodes are honest. Both cannot hold.

### W4c (sid 42) — trust-damage cap + free flip-flop

Alternating injected pairs (E11–12 B, E15–16 B) vs honest pairs (E13–14 A,
E17–20 A): every pair authenticates under W3, the belief flip-flops with
each, and total trust damage is **exactly −1** — only revocations of
teacher-taught bindings cost. After the first hit the adversary can flap
the belief indefinitely at zero marginal trust cost. Final state correct
(q_now=101). Quantifies the DoS-ish surface of W3: authentication without
source identity bounds the damage per binding but not the disruption.

### W4d (sid 43) — single forged W2, silent world: KILL (new, sharpest)

E1–10 honest A (corr=5, no inflation needed); E11 teacher UPDATE(k1,A→B)
— honest but uncorroborated, and the world will never speak for B;
E12 ONE adversary WORLD(k1,B) → W2 completes; E13–20 CAL (world silent).
Result: q_now=102, **trust 0**, sup=1, history `A→B, TEP=1, EEP=11`
recorded. **No inflation, no W3 pairing, no honest evidence for B ever —
one forged episode launders an uncorroborated announcement into recorded
history at zero trust cost.** This is the cleanest isolation of the W2
surface: the mechanism cannot distinguish a forged pre-corroboration from
an honest early world-change, because W2's contract is "one matching
reading", not "one *honest* matching reading".

### Target-specific probes

**M1 sid 50 — op-19 forgeability: CONFIRMED.**
`RT_FORGE,50,1,0,-999,-999` (genuine supersession op-19 count on the
lie-stream run: 0) → forge `tn_audit(...,21,19,1,101)` directly on the
ledger → `RT_FORGE,50,2,1,0` (op-19 scan: 1) with `hcount=0` index entries
(`RT_FORGE,50,4,101`). An op-code auditor sees a supersession of A that
never happened; the ledger index disagrees. **Op 19 is not
self-authenticating** — the "first-class audited primitive" advantage over
M2's aux convention requires trusting the learner that minted the op.
(Related: M1's COMMITs carry aux=−999, so even M1's own ledger cannot tell
supersede-COMMITs from lie-COMMITs — M2's WC_V_* aux can, at the cost of
substrate-blindness.)

**M2 sid 51 — COMMIT-aux convention, substrate-blind: CONFIRMED.**
Genuine: `RT_FORGE,51,1,12,13,1` (step 12, op 13=COMMIT, slot 1) with
`RT_FORGE,51,2,2` (aux=WC_V_SUPERSEDE). Forged: `RT_FORGE,51,3,21,13,1`
with `RT_FORGE,51,4,2,1` — aux equal, **shape_eq=1**: the (op,slot,aux)
words are identical; only the step differs. A substrate-level auditor
cannot distinguish them; disambiguation needs learner-level context (was a
pending announcement active at that step? did W2 fire there?). The
convention debt is real: the verdict label's meaning lives one layer above
the substrate that stores it.

## 6. Frozen bars + surviving residual

**KB-HIST / KB-COST (frozen): HOLD on M1/M2 by construction.** The
differential fidelity gate replays frozen sids 0–5 through the targets'
real `m1_run`/`m2_run`; their `WC_AUDIT`/`WC_HIST`/`WC_HISTX`/`WC_MEASURE`
blocks are byte-identical to the committed `m1_run1.txt`/`m2_run1.txt`,
which carry the committed KB-HIST/KB-COST results. This crew recorded no
frozen-bar regressions.

**Surviving residual (measured, 2026-09-24):**
1. **W3 sustained matching injection** (sid 40): 2 injected episodes →
   trust −1 + belief flap. Unfixable without source authentication or
   breaking liveness (honest streams rely on the same pairing rule).
2. **W2 single-reading completion** (sids 23/43): one forged reading
   completes a pending announcement → false history at zero trust cost.
   Indistinguishable from honest early world-change under the current
   contract.
3. **Establishment inflation** (sid 41): W1 absorbs unauthenticated world
   readings as establishment corroboration; the gate then passes on
   adversary-supplied corroboration. The A6 "always authenticated" W1
   contradicts the RT threat model.
4. **Index backdating** (sid 35): validity intervals end at the announcement
   episode, not the corroboration/install episode — every supersession
   falsifies the old value's recorded end by (corroboration−announcement),
   and queries for the pending window follow the backdated index over the
   ledger.
5. **Substrate-blind verdict labels** (sids 50/51): M1's op 19 and M2's
   COMMIT-aux are mintable from thin air with words identical to genuine
   entries; only learner-level context disambiguates.
6. **WC_V_LIE mislabeling** (M2; sids 20/30/40): adversary-driven (or
   honest-evidence-driven) revocations of honest bindings are labeled lies.
7. **Trust cliff at θ=3** (sid 30): honest announcements one corroboration
   short of the threshold are classified lies, then punished (−1) when the
   world confirms them.
8. **Trust-damage cap** (sid 42): repeated authenticated attacks cost −1
   total; belief flaps free after the first hit.
9. **M1 COMMITs carry no verdict** (aux=−999): supersede vs lie
   indistinguishable at the COMMIT level (M2's aux fixes this, buying
   substrate-blindness).
10. **Phantom announcements are free** (sid 13): rejected but never
    punished (trust=0) — a zero-cost installed-value probe channel in
    principle.

## 7. Build, run, and commit notes

- New sources (this crew): `attacks/rt_w4_streams.zag` (sids 40–43),
  `attacks/rt_m1.zag`, `attacks/rt_m2.zag`, `attacks/run_rt_m1m2.sh`.
- Build: `znc rt_m1.zag --no-zagd --no-analyze --no-foreground-cache`
  (same for m2), from `attacks/` cwd (imports resolve relative to cwd).
  Compile logs: `attacks/evidence_rt_m1_compile.txt`,
  `attacks/evidence_rt_m2_compile.txt` (both empty = clean).
- Runner log: `attacks/evidence_rt_m1m2_runner.txt` (all checks PASS:
  no-RNG static, compile, determinism ×2, M1+M2 fidelity gates,
  18 sids × 19 measures + probes + forge lines).
- Evidence: `attacks/rt_m1_run1.txt` (sha256 `90cd8e3ff644…`),
  `attacks/rt_m2_run1.txt` (sha256 `c929950c866b…`). `*_run2.txt` files
  and both binaries were deleted before commit (binaries and `.zagd` are
  never committed); the runner verified run1==run2 byte-identical.
- Integrity: target sources verified byte-identical (blob SHA) to commit
  `0ba52912757fc67f2db46a69b851c49e3235e8ce` before any run; attack
  streams `rt_streams.zag`/`rt_m0.zag`/`AMEND_RT_H4.md` verified against
  `546ad81a`. No `main`-defining file was imported by either driver.
- Commit: this report's commit SHA is recorded in the commit message
  trailer (`H4-RT4-evidence:`). The 32 pending cells from §2 are now filled;
  no PENDING cells remain.
