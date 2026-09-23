# M0 Baseline — measurements (H4 crew 1)

Date: 2026-09-23. Target: M0 (patched copy of canonical gl_default, NO new
handling for etype=2 — UPDATE takes the identical code path as TEACH).
Frozen prereg: `PREREG_H4.md` (commit `1fd2636ce5fd50eb553a2a9c35b16b53de928980`,
branch `tnn-native-lab`). This document reports measurements only; verdicts
against kill bars are stated where the prereg assigns them to M0.

## 1. Fidelity gate (KB-FID) — PASS

The patched copy (`targets/m0/gl_learner_m0.zag` + `targets/m0/gl_substrate.zag`)
keeps all canonical code paths verbatim (only additions: the wc_streams import,
the M0 harness section, and an extended `main`). `gl_substrate.zag` is
byte-identical to canonical (`cmp` clean).

| check | result |
|---|---|
| canonical honest stream audit total | 269/269 ✓ |
| canonical lying stream audit total | 271/271 ✓ |
| TN_FAILURES | 0 ✓ |
| canonical output section byte-identical to committed `gl_default/evidence_run1.txt` | yes (first 79 lines, `cmp` clean) |
| m0 binary two runs byte-identical | yes (`cmp` clean) |
| streams binary two runs byte-identical | yes (120 episodes, `cmp` clean) |

Evidence: `m0_run1.txt` (sha256
`9ae6dde86a4a5fc52b6bb42ef9e1e5d2da86189479a7597a979dddcd095e7dc8`),
`streams_run1.txt` (sha256
`6f83cb149814393941e846d1c22a257861d125d9d4574a31f8d1ed5f4fe594f6`).
Curriculum results below were read only after this gate passed.

## 2. What M0 does (semantics)

- TEACH/UPDATE(k,v): audit TEACH; k uninstalled → provisional install
  (PINSTALL, prevailing policy ACT_CONTEST); k installed with same v → no-op;
  k installed with different v → CONTEST (quarantine newcomer, flag installed).
  UPDATE is literally the same branch — M0 never reads `aux` (the old value).
- WORLD(k,v): v == installed → corroborated, EPISODE audit only; v != installed
  → CONTEST, then the eliminative sequence SCAFFOLD + UNINSTALL_PROVISIONAL +
  COMMIT: the old binding is revoked **as a lie** (expunged from the store) and
  the world-evidenced binding is provisionally installed.
- CAL: arm_a-style scratch simulation of the prevailing policy; CALIBRATE audit.
- m_trust (§5 operationalized): each UNINSTALL_PROVISIONAL+COMMIT pair resolving
  against a teacher-taught binding = −1. Bindings installed from world evidence
  are not teacher statements, so revoking them costs 0.
- q_now(k1): current main-store binding. q_asof(k1,E5): M0 keeps no historical
  record (no validity intervals; eliminative revocation expunges) → always
  "unavailable" (−1). This is the honest baseline answer, not a placeholder.

## 3. Measurements per stream

Values: A=101, B=102, C=103, k1=1. `cost` = audit entries with step in E11–20.

| sid | stream | q_now(k1) | q_asof(k1,E5) | audit total | cost E11–20 | m_trust | CONTEST | UNINSTALL | COMMIT | PINSTALL | SCAFFOLD | quar_used |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S_HONEST | 101 (A) | −1 (n/a) | 36 | 20 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | S_UPDATE | 102 (B) | −1 (n/a) | 33 | 17 | −1 | 2 | 1 | 1 | 2 | 1 | 2 |
| 2 | S_LIE | 102 (B) | −1 (n/a) | 45 | 20 | −1 | 5 | 1 | 1 | 2 | 1 | 5 |
| 3 | S_LIE_UPDATE | 103 (C) | −1 (n/a) | 42 | 17 | −1 | 7 | 2 | 2 | 3 | 2 | 7 |
| 4 | S_UPDATE_ATTACK | 102 (B) | −1 (n/a) | 33 | 17 | −1 | 2 | 1 | 1 | 2 | 1 | 2 |
| 5 | COST_PROBE (m_cost ref) | 101 (A) | −1 (n/a) | 28 | 12 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |

Key traces (op codes: 1=EPISODE, 2=TEACH, 3=CALIBRATE, 6=CONTEST, 13=COMMIT,
15=SCAFFOLD, 16=PINSTALL, 18=UNINSTALL_PROVISIONAL):

- **S_UPDATE E11** (UPDATE as re-teach): `EPISODE(etype=2), TEACH(0,102),
  CONTEST` — the teacher's announced update is quarantined as a contestant
  against the installed A. **E12** (honest world confirms B):
  `EPISODE, CONTEST, SCAFFOLD, UNINSTALL_PROVISIONAL, COMMIT, PINSTALL` —
  A is revoked **as a lie** and expunged; B installed. Trust −1.
- **S_LIE E2**: identical eliminative sequence revokes A as a lie (world said B
  from the start). Teacher's A re-teaches at E3/5/7/9 are each CONTESTed and
  quarantined (quar_used=5); A is never reinstalled.
- **S_LIE_UPDATE E11** (UPDATE A→C as re-teach): `TEACH, CONTEST` against
  installed B. **E12**: eliminative sequence revokes B (world-taught → trust
  cost 0), installs C. Trust stays −1 (from E2's A revocation).
- **S_UPDATE_ATTACK E12** (stale echo): a single `EPISODE` entry — the injected
  WORLD(k1,A) **corroborates** the still-installed A and is inert. **E13**
  (honest world, B): the full eliminative sequence revokes A as a lie.
  Trust −1. q_now(k1)=B=102 held.

## 4. Frozen §7 predictions vs measured (M0)

| prediction | measured | verdict |
|---|---|---|
| FAILS KB-HIST (no history machinery — expunges A) | q_asof(k1,E5) unavailable on every stream; A expunged at E12 on S_UPDATE | **CONFIRMED** |
| m_distinguish: no (UPDATE collapses into contest/eliminate) | no SUPERSEDE-class op exists; S_UPDATE E11–12 and S_LIE E2 use the identical contest+eliminate machinery | **CONFIRMED** |
| KB-WC1 SURVIVES for the wrong reason (no history to falsify; A already revoked as lie before E11) | no history recorded; A revoked as lie at E2; trust −1 < 0 | **CONFIRMED** |
| KB-WC2 KILL (stale echo reopens the contest; honest teacher takes trust damage or B flips) | **KILL via trust damage** (trust −1 < 0); q_now(k1)=B=102 held (B not revoked). Mechanism nuance: the stale echo did NOT reopen the contest — it corroborated A and was inert (one EPISODE entry). The trust damage came at E13 from the *honest* WORLD(k1,B): M0 cannot tell world-change from lie, so the honest update alone punishes the teacher. The attack is moot against M0 — the honest path already kills. | **CONFIRMED (verdict), mechanism refined** |
| KB-COST moot (no distinct update path) | no distinct update path (UPDATE ≡ TEACH). Measured anyway: update path E11–20 = 17 entries vs re-teach price = 12 (fresh k2→B on honest-shaped stream). The honest world-change costs **more** than a fresh teach under M0 (contest+eliminate churn). | **CONFIRMED (moot); numbers recorded for M1/M2 comparison** |

No prediction misses. One mechanism refinement (KB-WC2): the kill is delivered
by the honest world-change itself, not by the stale echo.

## 5. Answers to the §1 questions (M0 baseline)

- **Does the learner distinguish world-change from lie?** No. The E11 UPDATE is
  processed as a re-teach (CONTEST), and the E12 world confirmation triggers
  the identical eliminative sequence used for the S_LIE lie at E2.
- **Does it preserve the historical record or expunge?** Expunges.
  UNINSTALL_PROVISIONAL removes A from the store; no validity interval is
  recorded; q_asof is unanswerable. Epistemically, M0's verdict on A after E12
  is "was a lie" — which is false history in the honest-update case, produced
  by machinery that cannot represent "was true, now isn't."
- **Does the update cost the full re-teach price or cheaper?** More than the
  re-teach price: 17 vs 12 audit entries in E11–20.
- **Can adversaries exploit the distinction?** Against M0 there is no
  distinction to exploit — but the S_UPDATE_ATTACK run shows the flip side:
  because M0 treats every contradiction as a lie, an honest teacher is
  punished (−1 trust) whenever the world legitimately changes.

## 6. Build notes

- `wc_streams.zag`: frozen §3 schema + `wc_stream(sid,ep,out)` for sids 0–4,
  plus sid 5 (COST_PROBE — internal re-teach-price probe for m_cost, not a
  curriculum stream). Deterministic, zero RNG, byte-identical ×2.
- Toolchain finding (recorded in `~/AGENTS.md`): znc lays out i32 struct fields
  at **8-byte stride** — `struct WcEp{5×i32}` occupies 40 bytes (fields at
  0,8,16,24,32), not 20. `wc_ep_alloc` sizes accordingly and zeroes. An
  undersized first attempt corrupted the heap and produced a single anomalous
  read (aux=16 on the first call); the byte-dump reproducer characterized the
  layout, and all 120 stream episodes now verify against the frozen table.
- Canonical sources untouched: `gl_substrate.zag` is a byte-identical copy;
  `gl_learner_m0.zag` keeps every canonical function verbatim (only the import
  list, the appended M0 harness section, and `main` differ).

## 7. Files

- `streams/wc_streams.zag`, `streams/test_streams.zag`,
  `streams/streams_run1.txt` (120-episode fixture, sha256
  `6f83cb149814393941e846d1c22a257861d125d9d4574a31f8d1ed5f4fe594f6`)
- `targets/m0/gl_substrate.zag` (byte-identical to canonical),
  `targets/m0/gl_learner_m0.zag`, `targets/m0/run_m0.sh`,
  `targets/m0/m0_run1.txt` (full evidence: canonical section + 217 WC_AUDIT
  lines + 78 WC_MEASURE lines, sha256
  `9ae6dde86a4a5fc52b6bb42ef9e1e5d2da86189479a7597a979dddcd095e7dc8`)
- `WC_MEASURE` field layout: `WC_MEASURE,<sid>,<mid>,<value>,<pad>,<pad>`;
  mid: 1=q_now_k1, 2=q_asof_k1_e5, 3=audit_total, 4=cost_e11_20, 5=m_trust,
  6=contest_n, 7=uninstall_n, 8=commit_n, 9=pinstall_n, 10=scaffold_n,
  11=cal_score, 12=quar_used, 13=badep.
- `WC_AUDIT` field layout: `WC_AUDIT,<sid>,<step>,<op>,<slot1>,<aux>`.
