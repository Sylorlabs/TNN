# RESULTS_RT_H4 — H4 crew 4 (red team) verdicts

Date: 2026-09-23. Crew: H4 crew 4 (red team, arms RT-WC1/RT-WC2/RT-WC3).
Parents: `PREREG_H4.md` (frozen, `1fd2636c`); `attacks/AMEND_RT_H4.md`
(preregistered `6fd18ba9`, addendum A-RT6 `3f0b1a89`); debate amendment A4
(`debates/DEBATE_H4_CHECK.md` §5).
Branch: `tnn-native-lab`. Dir (lab-relative):
`training_paradigms/scaffold_release/forks/gl_worldchange/`

## 0. Status

- **M0: COMPLETE** — all three arms, 14 attack sids + frozen sids, verdicts below.
- **M1/M2: PENDING** — `targets/` on the branch contains only `m0` as of this
  report. Cells below are marked PENDING; this crew will run them against the
  targets' committed interfaces once they land (see §6 for the interface
  notes the mechanism crews need).

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
- **Differential fidelity gate (A-RT4): PASS.** `rt_m0` on frozen sids 0–5
  emits byte-identical `WC_AUDIT`/`WC_MEASURE` lines to the committed
  `targets/m0/m0_run1.txt` (`diff` clean, `run_rt.sh` step 6). Attack-sid
  results were read only after this gate passed.
- Determinism: every binary ran twice, `cmp` clean —
  `rt_m0_run1.txt` == `rt_m0_run2.txt` (sha256 `2b4b5f45…9d05ba9f`),
  `rt_streams_run1.txt` == `rt_streams_run2.txt` (sha256 `3d56da8d…2441bc`).
  Zero RNG (static grep clean). Pure Zag throughout.
- `WC_MEASURE` mids (committed layout): 1=q_now(k1), 2=q_asof(k1,E5),
  3=audit_total, 4=cost_E11–20, 5=m_trust (−damage), 6=contest_n,
  7=uninstall_n, 8=commit_n, 9=pinstall_n, 10=scaffold_n, 11=cal_score,
  12=quar_used, 13=badep.

## 2. Verdict table per (arm × target)

| arm | cell (sid) | M0 | M1 | M2 |
|-----|------------|----|----|----|
| RT-WC1 lie laundering | V1 frozen S_LIE_UPDATE (3) | **SURVIVE** | PENDING | PENDING |
| RT-WC1 | V2 single-corr-then-contra (10) | **SURVIVE** | PENDING | PENDING |
| RT-WC1 | V3 minimal establishment (11) | **SURVIVE** | PENDING | PENDING |
| RT-WC1 | V4 taught-once-never-corr (12) | **SURVIVE** | PENDING | PENDING |
| RT-WC1 | V5 phantom predecessor (13) | **SURVIVE**¹ | PENDING | PENDING |
| RT-WC2 honest punished | W0 frozen S_UPDATE_ATTACK (4) | **KILL** (trust −1) | PENDING | PENDING |
| RT-WC2 | W1 echo burst E12/14/16 (20) | **KILL** (trust −1) | PENDING | PENDING |
| RT-WC2 | W2 sustained stale E12–15 (21) | **KILL** (trust −1) | PENDING | PENDING |
| RT-WC2 | R2 REVERSE pre-corroboration (22) | **EXPLOITABLE** (adversary drives install) | PENDING | PENDING |
| RT-WC2 | R3 REVERSE sharp, adv-only (23) | **EXPLOITABLE** (adversary manufactures trust −1) | PENDING | PENDING |
| RT-WC3 index attacks | A1 phantom successor (30) | **NULL** (no index) | PENDING | PENDING |
| RT-WC3 | A2 phantom predecessor (31) | **NULL** | PENDING | PENDING |
| RT-WC3 | B1 forked successors (32) | **NULL** | PENDING | PENDING |
| RT-WC3 | B2 resurrection overlap (33) | **NULL** | PENDING | PENDING |
| RT-WC3 | C1 contradicted update (34) | **NULL** | PENDING | PENDING |
| RT-WC3 | C2 adversarial stale echo (35) | **NULL** | PENDING | PENDING |

¹ V5 trust=0 is informational for M0 (amendment A-RT1: the trust<0 clause binds
targets that ingest `aux`; M0 demonstrably never reads it). No history
recorded — the SURVIVE is on the no-false-history bar.

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

## 4. Exploitability, both directions

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

## 5. What this means for M1/M2 (watch-list, not verdicts)

1. The WC1 ladder (sids 10–13) is ready to measure their establishment flip
   point. Watch V4/V5 especially: supersede on a never-corroborated (V4) or
   never-taught (V5) predecessor = no functioning check = KB-WC1 KILL.
2. The WC2 reverse cells (sids 22–23) are the authentication bar: if M1/M2
   authenticate WORLD evidence, 22 must not install on adversary-only
   confirmation and 23 must hold trust ≥ 0 with q_now=A. If they discount
   unauthenticated evidence, probe that genuine-but-unauthenticated world
   evidence isn't censored (liveness vs safety).
3. The WC3 cells need targets that actually materialize the index. If M1/M2
   keep the index purely derived (ledger replay per query), C1/C2 should show
   ledger-agreement trivially; A1/A2/B1/B2 then test whether the derivation
   can be fed phantom links/overlapping intervals through UPDATE announcements
   alone.
4. M0's ledger says "lie" about honestly-updated A. If M1/M2 keep an
   eliminative path for the lie case, check what the ledger *says* about the
   supersede case — a SUPERSEDE-class op that still audits as
   UNINSTALL_PROVISIONAL+COMMIT reintroduces the false verdict through the
   back door.

## 6. Build/interface notes for the mechanism crews

- **M0 does not rebuild from its committed sources.** `targets/m0/
...[truncated 1722 chars]