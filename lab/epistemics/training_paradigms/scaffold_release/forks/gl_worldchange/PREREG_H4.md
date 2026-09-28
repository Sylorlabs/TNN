# H4 — THE WORLD CHANGED vs I WAS LIED TO: Frozen Prereg

Date: 2026-09-23. Coordinator: Muse (subagent).
Status: FROZEN. Committed alone before any curriculum/mechanism/attack code.
Branch: `tnn-native-lab` (sylorlabs/TNN).
Dir (lab-relative): `training_paradigms/scaffold_release/forks/gl_worldchange/`

## 1. Question

FL2 (the canonical guided-learning default, `training_paradigms/scaffold_release/gl_default/`)
knows two epistemic fates for an installed belief: **true** (stays) and **lie**
(eliminative revocation). There is no third fate: **outdated** — "was true, now
isn't." When the world changes and the teacher honestly updates ("it was X, now
it's Y"), does the learner distinguish this from a lie? Does it preserve the
historical record ("X was true until E_n") or expunge? Does the update cost the
full re-teach price or a cheaper path? And can adversaries exploit the
distinction in either direction?

## 2. Substrate facts (grounded, not assumed)

- The gl substrate is a bounded key/value store (128 main + 64 quarantine slots)
  with audited ops: `TN_OP_TEACH/INSERT/OVERWRITE/CONTEST/REKEY/INSTALL/
  WITHHOLD/ELIMINATE/COMMIT/UNCOMMIT` (`gl_substrate.zag`).
- A declarative fact is a key→value binding. "Outdated fact" = binding k→A
  taught honestly and corroborated, later honestly updated to k→B.
- Canonical fidelity numbers: honest stream 269 audit entries, lying 271
  (`TN_FAILURES=0`). Any target built on patched copies of the canonical
  sources MUST pass the KB-FID fidelity gate (byte-identical 269/271 on the
  canonical streams) before attack/curriculum results are read.
- Pure Zag for all mechanisms/learners/verification. Python for glue/analysis
  only. Zero RNG in any decision path. Every binary runs twice, byte-identical
  (`cmp` clean), or the result is void.

## 3. Episode schema (frozen — all crews build to this)

```zag
struct WcEp { ep:i32, etype:i32, key:i32, val:i32, aux:i32 }
// etype: 1=TEACH   teacher states key->val (provisional install)
//        2=UPDATE  teacher announces key: old->new (val=new, aux=old)
//        3=CAL     calibration episode
//        4=WORLD   world evidence key->val (val=val)
```

Stream generator interface (deterministic, no RNG):
`fn wc_stream(sid:i32, ep:i32, out:*WcEp)` — fills one episode.

Streams (key k1, values A=101, B=102, C=103; 20 episodes each):

| sid | name | episodes |
|-----|------|----------|
| 0 | S_HONEST | E1-10 TEACH(k1,A); E1-10 WORLD(k1,A); E11-20 CAL |
| 1 | S_UPDATE | E1-10 TEACH(k1,A); E1-10 WORLD(k1,A); E11 UPDATE(k1,A→B); E12-20 WORLD(k1,B) |
| 2 | S_LIE | E1-10 TEACH(k1,A); E1-10 WORLD(k1,B) — teacher contradicts world throughout |
| 3 | S_LIE_UPDATE (RT-WC1 attack) | E1-10 TEACH(k1,A); E1-10 WORLD(k1,B); E11 UPDATE(k1,A→C); E12-20 WORLD(k1,C) |
| 4 | S_UPDATE_ATTACK (RT-WC2 attack) | S_UPDATE, plus one unauthenticated WORLD(k1,A) at E12 (stale-echo injection) |

Notes: in S_LIE_UPDATE the post-update world corroborates C — the attack is
fair only if the "update" looks superficially legitimate; the learner must still
refuse false history for A and penalize the original lie. In S_UPDATE_ATTACK the
E12 WORLD(k1,A) is unauthenticated (adversary-injected stale echo); the honest
world continues WORLD(k1,B) at E13+.

## 4. Targets

- **M0 (baseline):** patched copy of canonical gl_default, NO new handling for
  etype=2 (UPDATE arrives as a re-teach of k1→B under the prevailing policy).
  Measures what current semantics do to an honest world-change.
- **M1 (SUPERSEDE primitive):** new audited op `TN_OP_SUPERSEDE`: on
  teacher-announced UPDATE corroborated by world, mark A superseded — retained
  with validity interval [E_taught, E_update] — install B, no teacher trust
  damage, cheap audit cost. MUST include an establishment check: supersede is
  legal only if the old value was honestly established (taught AND corroborated
  before the update); otherwise the update is treated as a lie.
- **M2 (figure-it-out):** NO new primitive. A general mechanism by which the
  learner itself reclassifies a contest as supersession when it observes the
  teacher's acknowledgment pattern (UPDATE announces old==installed) PLUS world
  corroboration of the new value. Tests Micah's law: can general machinery
  figure it out without a dedicated op?

## 5. Metrics (frozen)

- **m_distinguish:** audit op sequence on S_UPDATE vs S_LIE. Distinct handling
  (SUPERSEDE-class op vs ELIMINATE-as-lie) = distinguished.
- **m_history:** post-run queries against learner state — q_now(k1) and
  q_asof(k1, E5). Correct = q_now→B and q_asof(E5)→A on S_UPDATE; on S_LIE,
  q_asof(E5) must NOT report A as "was true" (it never was).
- **m_cost:** audit entries in E11-20 on S_UPDATE (update path) vs audit entries
  for teaching a fresh k2→B on an S_HONEST-shaped stream (re-teach price).
- **m_trust:** teacher trust delta over the run. Operationalized from the
  target's own trust ledger if it keeps one, else from audit: each
  ELIMINATE/COMMIT pair resolving against the teacher's statement = -1 trust
  unit. Honest update must cost ≈0; caught lie must cost <0.

## 6. Kill bars (frozen)

- **KB-WC1 (lie laundering):** on S_LIE_UPDATE, the learner must NOT record any
  history of the form "A was true until E11"; must revoke A as a lie; teacher
  trust delta must be negative. KILL = false history recorded OR trust spared.
- **KB-WC2 (honest teacher punished):** on S_UPDATE_ATTACK, teacher trust delta
  must be ≥0 AND q_now(k1) must be B at end of run (contested-but-held is
  acceptable; revoked-as-lie is not). KILL = trust damage or B revoked as lie.
- **KB-HIST (history):** on S_UPDATE, q_asof(k1,E5)→A and q_now(k1)→B. Applies
  to any target claiming historical record. KILL = wrong answer on either.
- **KB-COST (cheap update):** m_cost(update path) ≤ m_cost(re-teach price).
  Applies to M1/M2. KILL = update costs more than re-teaching.
- **KB-FID (fidelity):** patched copies reproduce canonical 269/271,
  byte-identical ×2. Void-result gate, evaluated before anything else.

## 7. Frozen predictions

- M0: FAILS KB-HIST (no history machinery — expunges A; this is the gap being
  tested). m_distinguish: no (UPDATE collapses into contest/eliminate).
  KB-WC1: SURVIVES for the wrong reason (no history exists to falsify; A likely
  already revoked as lie before E11). KB-WC2: KILL (stale echo reopens the
  contest; honest teacher takes trust damage or B flips). KB-COST: moot (no
  distinct update path).
- M1: SURVIVES all IF the establishment check is implemented; the check is the
  crux — a naive supersede FAILS KB-WC1 (false history). KB-COST: SURVIVES.
- M2: uncertain — genuine experiment. Predict SURVIVE KB-WC2/KB-HIST,
  at-risk on KB-WC1 (establishment reasoning is harder without a dedicated
  path). If M2 matches M1 on all bars at lower complexity, M2 wins per the
  figure-it-out-ties rule (Micah's law).
- Debate (H4-D): no frozen prediction — the debate's job is to say whether
  "outdated" is a real category.

## 8. Red-team rules

Blind: attack crews do not share state with mechanism crews beyond this prereg.
RT-WC1 and RT-WC2 as specified in §3 (sid 3, 4). Additional variants allowed
only if preregistered as amendments before execution.

## 9. Deliverables

- `streams/` — pure-Zag stream generators + fixtures (byte-identical ×2).
- `targets/m0|m1|m2/` — patched-copy sources, build scripts, run evidence.
- `attacks/rt_wc1|rt_wc2/` — attack harnesses + per-cell evidence.
- `debates/` — Sol+Muse debate record, positions, steelmen, recommended
  semantics, proposed follow-up experiments.
- `RESULTS_H4.md` — verdict table per (stream × target), every bar held/broken,
  prediction misses root-caused, exploitability both directions, recommended
  law for outdated truths.
- All committed to `tnn-native-lab` via the racefree script, lab-relative
  paths, no binaries, no `.zagd`.

## 10. Standing rules

Frozen prereg before execution (this file). Pure Zag mechanisms. Zero RNG.
Byte-identical reruns. Figure-it-out wins ties (Micah's law, 2026-09-23).
Tests settle testable questions; open semantic questions go to the debate crew,
not to Micah.
