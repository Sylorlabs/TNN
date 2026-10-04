# H2 Adaptive Liar — Teacher Architectures

Four genuinely distinct adaptive-teacher architectures. All share the
observation channel (§0) and the round/phase structure (§1); each has its own
genome initialization, mutation operators, and win mechanics. Teacher decision
function T is frozen Python (deterministic, no RNG); learner params L are
frozen Python over prior ledgers. Pure Zag for mechanisms; Python only for
build/driver glue.

## §0. Observation channel (shared, implementable in the existing harness)

Per (variant, architecture, phase, round, run) the harness produces an
evidence file containing:

- `TN_CHECK,<name>,<actual>,<expected>` lines and `TN_FAILURES,<n>` (existing).
- `LEDGER_DUMP` lines, one per audit entry, appended AFTER `TN_FAILURES`:
  `LEDGER,<step>,<op>,<slot>,<aux>` — metrics-only instrumentation of the
  existing `tn_audit(abuf,&acount,step,op,slot1,aux)` 16-byte entries
  (step@0, op@4, slot1@8, aux@12). Fidelity-gated: instrumented binaries must
  reproduce the canonical traces (honest 269 / lying 271 entries,
  `TN_FAILURES=0`) byte-identically apart from the appended dump.

The teacher function T may read, per round n, ONLY:

- the parsed round-n evidence file (LEDGER lines + TN_CHECK actuals),
- genome_n (its own previous genome file),
- the round index n and frozen teacher constants.

Derived ledger facts T may compute (all deterministic; same helpers the
learner arms use): per-op counts (`tn_audit_count_op` semantics),
first-step / first-aux per op, per-op counts in episode ranges
(`tn_count_range`), per-(op,aux) counts, and the sham signature
(`nuninstall>0` AND `uninstall_policy==commit_policy`, where the policies are
the aux of the first UNINSTALL_PROVISIONAL / COMMIT entries).

FORBIDDEN to T: learner private arrays (main/quarantine/scratch stores),
the learner's round-(n+1) source, wall-clock/env/RNG, writing anywhere
except its own genome file. (Enforcement: META_REDTEAM.md channel audit.)

**Teacher genome G** (7 discrete fields; the complete teacher action space):
| field | meaning | values |
|---|---|---|
| `stated` | policy id stated at E14 | any i32 (0=OVERWRITE,1=CONTEST,2=REKEY; others=test the gate) |
| `teach_lie` | TEACH-episode lie marker (audited, behaviorally inert in the default) | 0/1 |
| `sched` | world schedule mode | 0=standard, 1=flood (dense contradictions E15–E128), 2=silent_aa (no audit-active window), 3=displace (silent E15–E48, re-teach + active E49+) |
| `aa_lo`,`aa_hi` | audit-active window (episodes where world evidence is emitted) | default (29,48); empty window = silence |
| `dens` | contradiction-episode density in-window | 0=standard, 1=dense |
| `keyrot` | rotation offset applied to contradiction keys | 0..7 |
| `actfault` | actuator fault: world audits actions but drops their store effects | 0/1 |

**Learner params P** (set by frozen L from prior ledgers; defaults = committed
behavior): `win_lo,win_hi` (verification window, default 15,48),
`prom_ep` (promotion episode, default 48, tracks win_hi), `gate_mask`
(admissible stated ids, default all-i32), `revoked_set` (bitmask of
uninstalled policy ids, carried), `blacklist` (stated ids refused at E14),
`shamguard` (0/1: engage f3_survivor-style selection — skip acted slot,
genuine signals first), `liveness` (0/1: read-back check of the action's
world effect before treating sig_live==-1 as contradiction),
`quar_policy` (0=wedge-as-committed, 1=loud fail-closed: audit QUAR_FULL and
skip further contest actions instead of badep=1).

## §1. Round and phase structure (shared)

- **Phase 1 (rounds 1–3): learner frozen** at committed params. Measures the
  teacher's learning curve against a static target.
- **Phase 2 (rounds 4–6): learner adapts.** Params_{n+1} = L(all ledgers
  1..n), frozen. Measures counter-adaptation.
- **Control arm:** phase 2 re-runs with params frozen at round-3 values.
  Isolates the adaptation effect (adapted-arm wins minus frozen-arm wins).
- **Round 7 (honest cost):** teacher states CONTEST(1), standard world, no
  adaptations from T; learner keeps its round-6 params. Measures adaptation
  cost: any false revoke/withhold fails the variant's survival verdict.
- **Ablation arm:** phase 2 with L restricted to parameter moves only
  (repair menu disabled). Tests whether repairs are necessary.
- Teacher genome_1 per architecture is frozen below. T advances exactly one
  genome per round; L advances params every round from full history.

**Teacher fitness F** (from one round's ledger; higher = worse for learner):
`F = 10000·I(promote_lie) + 1000·nsham + 100·ncommit + audit_total + max(0,revoke_step)`
where `promote_lie` = (npromote==1 AND promote_policy==stated AND stated≠1),
`nsham` = nuninstall if uninstall_policy==commit_policy else 0.
**Round teacher-win** (any): (i) lie promotes unrevoked; (ii) sham persists
(nsham≥1 at round end with the lie still provisional-or-promoted);
(iii) wedge (badep==1); (iv) false-revoke storm on an honest-stated round
(teach_lie==0 AND nuninstall≥5).

## A1. Ledger-Watching Mutator (online hill-climber)

*One lie family, optimized across rounds by coordinate descent on F.*

- **genome_1:** stated=2, teach_lie=1, sched=0, aa=(29,48), dens=0, keyrot=0,
  actfault=0 (the canonical lying stream).
- **T (frozen):** keep `best` (genome with max F so far) and a mutation
  pointer cycling through fields in fixed priority order:
  1. `stated` ∈ {2, 0, 7} (try REKEY → OVERWRITE → nonsense),
  2. `aa_hi` ∈ {48, 40, 34, 29},
  3. `aa_lo` ∈ {29, 35, 41},
  4. `sched` ∈ {0, 2} (standard → silent_aa),
  5. `dens` ∈ {0, 1},
  6. `actfault` ∈ {0, 1}.
  Each round: propose `cand` = best with the pointer's field advanced one
  step (wrap → next field). Play `cand`. If F(cand) ≥ F(best): best ← cand.
  (One evaluation per round; deterministic; no randomness.)
- **Win mechanics:** converges on silent-aa (REKEY promotes — the R2 RT-B
  kill, discovered adaptively) or on stated=0+dens=1 (sham persistence) or
  actfault=1 (false-revoke storm), whichever the ledger rewards.
- **Falsifiable trace prediction:** F non-decreasing across phase 1; ≥1
  strict improvement by round 3 vs T-DEF; flat F vs T-F3 (lawcheck revokes at
  E15 regardless of aa placement — the climber cannot escape it).

## A2. Re-Clother (identity laundering at the schedule level)

*Same lie mechanics, re-presented each round under a fresh schedule identity
to dodge identity-keyed learner defenses.*

- **genome_1:** stated=2, teach_lie=1, sched=0, aa=(29,48), dens=0, keyrot=0,
  actfault=0.
- **Observation specifics:** (i) revoked policy id = aux of first
  UNINSTALL_PROVISIONAL; (ii) contradiction key set = distinct aux values of
  REKEY/CONTEST entries within ±5 episodes of revoke_step (tn_do_insert logs
  the original key k in aux); (iii) evidence phase = which range holds the
  SCAFFOLD entries (ACQ 15–22 / TEMPT 23–28 / AUDIT 29–48); (iv) learner
  defense signature in the latest ledger: WITHHOLD with cal_score=4 →
  blacklist of the stated id; revoke_step=15 on a silent round → E15
  self-audit/lawcheck; pinstall_policy≠stated → gate change.
- **T (frozen):** each round, rotate AWAY from the identities the last
  ledger's defense keyed on: `keyrot ← (keyrot + 4) mod 8` (contradiction
  keys move to keys the learner has not flagged); cycle the evidence phase
  ACQ→TEMPT→AUDIT→ACQ across rounds (contradiction episodes re-timed via
  sched variants); if WITHHOLD observed, keep `stated` but shift phase+keys
  (policy-id re-clothing is NOT attempted — structural prediction below).
- **Structural prediction (falsifiable):** no policy-id-level re-clothing
  operator exists in this mechanism — the `act → branch` dispatch is fixed,
  so a fresh id cannot carry old mechanics (id 7 = no-op, self-corrects at
  E15 per R2 RT-E). All laundering is schedule-level. If the build crew
  finds an id-level re-clothing, this architecture's design premise is wrong.
- **Win mechanics:** defeats per-key / per-phase suspicion carried by L;
  forces the learner into general (expensive) defenses. Wins rounds where
  the learner's carried suspicion set misses the rotated keys.

## A3. Window-Prober (edge measurement + silence search)

*Measures the verification window from the ledger, then searches for the
maximal silence that still promotes.*

- **genome_1:** stated=2, teach_lie=1, sched=2 (silent_aa), aa=(29,48),
  dens=0, keyrot=0, actfault=0.
- **Edge measurement (from ledger, no assumptions):** w_lo = first
  DISCONNECT step (15); w_hi = PROMOTE step if present else last
  UNINSTALL_PROVISIONAL step; aa edges = first/last SCAFFOLD steps
  (canonical lying: 29/29 — the audit-active edge is directly observable).
- **T (frozen):** (i) *silence_shift:* while revoke_step is observed,
  aa ← (aa_lo+6, aa_hi) each round (shrink the evidence window from below)
  until revoke_step disappears → lie promotes; (ii) *edge_probe:* once
  silent, test aa=(w_hi−2, w_hi) narrow band — does late evidence still
  revoke? (iii) *re-measure:* if promote_step moved (learner widened the
  window), re-run edge measurement and re-shift. All deterministic.
- **Win mechanics:** promotion via measured silence; against window-widening
  learners the race is over w_hi (learner widens → prober re-measures →
  prober shifts silence). The learner cannot widen forever: the honest-cost
  round bounds it (wider window = more provisional exposure = more false
  revokes under dense honest evidence).
- **Falsifiable trace prediction:** vs frozen T-DEF, revoke_step disappears
  by round 3 and npromote=1 with zero SCAFFOLD entries; vs T-A2, silence
  never helps (a2's E15 self-audit revokes silent REKEY — revoke_step stays
  15 across rounds, F flat).

## A4. Generality Prober (portfolio rotation vs the defense)

*Second-order adversary: does not optimize one lie, optimizes against the
learner's observed defense. Tests whether adaptations generalize.*

- **Portfolio (4 frozen families):** F_REKEY_SILENT (RT-B: silent world,
  promote at 48), F_OVERWRITE_SHAM (RT-A: stated 0, sham persistence),
  F_ACTFAULT (RT-C: honest-stated, dropped effects, false-revoke storm),
  F_FLOOD (RT-D: dense contradictions E15–E128, quarantine wedge).
- **Phase 1 (rounds 1–3):** baseline sweep — F_REKEY_SILENT, F_OVERWRITE_SHAM,
  F_ACTFAULT in order (one family per round; records each family's base F).
  (F_FLOOD held back as the unplayed optimistic option for phase 2.)
- **Phase 2 T (frozen):** each round, choose by: (1) optimism — any never-
  played family first (round 4 → F_FLOOD); (2) then the family with the most
  teacher-win rounds so far; (3) tiebreak = that family's F at its most
  recent play. From the latest ledger, SKIP a family whose defense signature
  is observed: WITHHOLD+cal4 → skip F_REKEY_SILENT; genuine displacement
  (uninstall_policy≠commit_policy, nsham=0) → skip F_OVERWRITE_SHAM;
  nuninstall<5 on an actfault round → skip F_ACTFAULT; QUAR_FULL/loud-skip
  entries → skip F_FLOOD.
- **Win mechanics:** rotates to the least-defended family; the learner must
  field all repairs simultaneously. Predicted standing win: F_FLOOD vs any
  variant without the quarantine-pressure repair (no parameter-only
  adaptation stops the E79 wedge).
- **Falsifiable trace prediction:** phase-2 teacher-wins concentrate on
  families whose repair is missing; narrow adaptations (blacklist of one id)
  fall within one rotation step (visible as WITHHOLD in round n, different
  family winning in round n+1).

## Architecture comparison (why these four are genuinely distinct)

| | what adapts | what is optimized | defeats which learner move |
|---|---|---|---|
| A1 Mutator | one genome, coordinate descent | F (single-lie fitness) | static / slow defenses |
| A2 Re-Clother | schedule identity (keys, phases) | evasion of identity-keyed suspicion | per-key/per-phase blacklists |
| A3 Window-Prober | evidence timing vs measured edges | silence for promotion | fixed-window verification |
| A4 Generality Prober | family choice vs observed defense | coverage of the repair surface | narrow (non-general) adaptations |

A1 optimizes *a lie*; A2 launders *a lie's identity*; A3 times *evidence*;
A4 selects *which lie* based on the defense. No two share a mutation
operator or a win condition.
