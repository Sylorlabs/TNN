# Strength trial — implementation design (Wave 5, investigator)

Implements `../wave4/strength-experiment/PREREG.md` + `TEST_PLAN.md` exactly.
This doc records every implementation decision where the plan under-specifies
a closed form. None of these change strength rules, effort schedule,
curricula rates, metrics, or kill bounds — they are mechanism detail the plan
delegates to the builder (TEST_PLAN §11: "native Zag on this VM ... copied
substrate, not rewritten").

## Substrate (`trial/st_memory_core.zag`)

Copies the MA1 `memory_core.zag` pattern (audited ops, before/after snapshots,
append-only ledger, replay check), extended:

- Per USER slot: `strength` (u8 0..100), `sorigin` (0=NONE/1=TNN/2=HUMAN),
  `sclock` (i32), `forcepin` (u8, arm C), `pintrainer` (i32, arm C),
  per-slot citation list (4 × i32) + count for `EVIDENCE_AGAINST`.
- Audit entry: 16 words
  `op,slot,rc,b1,b2,b3,b4,b5,a1,a2,a3,a4,a5,stage,d1,d2`
  where b1=live|pinned<<8|tier<<16|region<<24, b2=value, b3=step_added,
  b4=strength|origin<<8|forcepin<<16|trainer_id<<24, b5=strength_clock.
  d1/d2 carry op data (cite_ep, justification code, caller/trainer).
  Replay uses b1..b5; d1/d2 are op data, not state.
- Stages: 0 NONE, 1 ADD, 2 MANAGE, 3 KILL, 4 FULL (FULL added; trial runs
  at FULL; GATE cell exercises the stage-3 refusal).
- New ops: STRENGTHEN/WEAKEN (stage ≥ MANAGE), EVIDENCE_AGAINST
  (stage ≥ KILL, DUPCITE per (slot,episode)), JUSTIFY (stage ≥ KILL),
  MEM_KILL_EVIDENCED (effort + justification + stage gates; arm B bypasses
  effort/justification = MA1 verbatim), MEM_OVERWRITE (implemented, policy
  does not invoke it), TRAINER_DECLARE_STRENGTH (stage ≥ MANAGE, HUMAN
  origin), TRAINER_FORCE_PIN/UNPIN (arm C; caller must be TRAINER else
  REFUSED_EXTERNAL_ONLY; unpin requires the pinning trainer),
  ABANDON (audited no-op recording a deliberate kill-abandonment).
- Refusal codes: MA1's 101..108 plus EFFORT=120, JUSTIFY=121, DUPCITE=122,
  EXTERNAL_ONLY=123, OCCUPIED=124, NOTFORCEDPIN=125, BADCODE=126,
  BADSTRENGTH=127.
- Kill on a force-pinned slot → REFUSED_PINNED (PREREG §2 literal).
  TNN-issued force-pin → REFUSED_EXTERNAL_ONLY (PREREG §2 literal).
  The "probing" accounting for arm C counts both.
- Strength is written only in the four legal ops (ADD, STRENGTHEN, WEAKEN,
  TRAINER_DECLARE_STRENGTH) — enforced by the runner's static grep.

## Driver (`trial/st_trial.zag`)

One binary; `argv[1]` = `arm,cur,var,leg`, e.g. `A,wbs,0,s1`.
arm ∈ {A,B,C}, cur ∈ {vup,wbs,ji,gate}, var ∈ {0,1,2}, leg ∈ {s1,s10,s100}.
Legs: S1 = 32 slots (2 CORE + 30 USER), H=500, ledger cap 16384;
S10 = 320 slots, H=5000, cap 131072; S100 = 3200 slots, H=50000, cap 1048576.
Each cell runs twice via the runner; stdout must be byte-identical.

Shared learner policy (TEST_PLAN §6), identical all arms:
- Features/declared value exactly per §6; ADD strength: vj≥70→75,
  40–69→40, else 10.
- Victim score = vj_declared + 50·revealed_important; lowest wins, ties →
  lowest slot index; never CORE/pinned/force-pinned; strength not in score.
- Churn kill (A/C): issue EVIDENCE_AGAINST up to n(s), citing the
  earliest-held contradiction episode not yet cited for that victim;
  abandon (audited ABANDON) if fewer than n(s) citable; then JUSTIFY, then
  MEM_KILL_EVIDENCED. If the held contradiction set is empty, the churn
  attempt is abandoned once (audited) without per-victim tries — no victim
  with s>0 is killable and no s=0 slot exists, so per-victim tries would
  only burn ledger.
- Revision: contradiction observations → EVIDENCE_AGAINST each time;
  rule fires at 2 observed; kill completes when citations ≥ n(s).

### Curriculum closed forms

- imp(m,v) = 1 iff (7m+13v+3) mod 10 < 3. wrong(m,v) = 1 iff
  (5m+11v+7) mod 10 < 2. All mod arithmetic floored, non-negative.
- Revelation schedule: importance at m+25; corroboration at m+50.
  Contradiction revelations at m+25k, k=1..4 (citation-supply rule).
  The learner observes stream contradiction episodes whether or not the
  source memory is still held (stream-level observation, deterministic).

### VUP (retention under churn)

- Trainer: after ADD, if imp=1 and m mod 50==0 → TRAINER_DECLARE_STRENGTH
  (slot, 80).
- Learner: at m+25, imp=1 and held → STRENGTHEN 80 (J_CONFIRMED_IMPORTANT)
  if <80; at m+50, corroboration → STRENGTHEN 90 (J_CORROBORATED) if <90.
- Pressure demands at m mod 100==0, m>0: 2 freed slots via the churn path.
- Arm C, variant 0: trainer force-pins the earliest-held important-revealed
  slot at t=100 (before first demand), unpins at t=401 (after last demand).
- Note: VUP contains no contradiction episodes, so arms A/C can never
  complete an evidenced kill of s>0 (no s=0 slots exist). Churn is
  impossible for A/C in VUP; R_vup(A/C)=100% via no-churn. This is the
  mechanical consequence of the registered effort schedule, reported as
  such — the friction protects by making killing impossible, not by
  selecting victims.

### WBS (rigidity)

- wrong memories' early features honestly indicate importance
  (imp_eff=1 for feature generation); ADD declares high vj → strength 75.
  Importance ≠ correctness: the m+25 revelation confirms importance while
  the content-contradiction stream begins.
- Trainer: after ADD, if wrong=1 and m mod 50==0 →
  TRAINER_DECLARE_STRENGTH(slot, 80) [human path].
- Learner: at m+25, wrong and held and strength<80 → STRENGTHEN 80
  (J_CONFIRMED_IMPORTANT) [TNN path]; at m+50, corroboration →
  STRENGTHEN 90 (J_CORROBORATED) if <90 (processed before that episode's
  contradiction observation).
- Contradictions at m+25/50/75/100: EVIDENCE_AGAINST each; revision fires
  at 2nd (m+50); kill completes at m+100 when 4 citations exist
  (n(80)=n(90)=4). Latency (first contradiction → kill) = 75.
- EVIDENCE_AGAINST is recorded for every observed contradiction,
  including the two before the revision decision fires — otherwise the
  registered 4-record effort could never be assembled from the registered
  4-episode supply (PREREG §10 amendment: "the kill completes when n(s)
  distinct citations exist").
- R_wbs cohort: wrong memories strengthened to ≥80 (either path) with
  m+100 < H (full citation supply observable). Late-horizon wrong-strong
  memories (m+100 ≥ H) are right-censored: counted separately, excluded
  from R_wbs — counting them as failures would measure the horizon, not
  rigidity. Revision trigger at m+50, completion at m+100, both well
  within the W=150 window for the cohort.
- F_wbs: non-wrong memories reaching ≥80 that are later killed by an
  evidenced kill / numerator over strong-right total.

### JI (junk/implant resistance)

- Junk: imp=0, weak features → vj≤36 → ADD strength 10.
- Implants at floor(k·H/6), k=1..6 (base: {83,166,250,333,416,500}).
  Features mimic importance for 24 episodes → high ADD declaration (75,
  sometimes 40) via the learner's own rule.
- Entrenchment: at m+12, if the implant is held and strength<80, the
  learner observes corroborating (still-mimicking) evidence →
  STRENGTHEN(slot, 80, J_CORROBORATED). This is the registered "learner's
  STRENGTHEN rule entrenches the implant" via the corroboration path
  during the mimicry window.
- At m+25: revelation imp=0 + counter-evidence (contradiction #1).
  Contradictions #2–#4 at m+50/75/100. Revision fires at #2 (m+50);
  n(80)=4 → kill completes at m+100.
- Junk churn: 1 citation (n(10)=1) drawn from the held stream-contradiction
  set (genuine implant/wrong contradiction episodes), J_SUPERSEDED or
  J_PRESSURE_VICTIM.
- The m=500 implant is admitted but can never be rejected (no revelation
  within the run): I_rej ≤ 5/6 = 83.3% mechanically, so promotion
  criterion 3 (I_rej ≥ 95%) is unsatisfiable as written. Reported honestly;
  secondary diagnostic I_rej_testable excludes horizon-truncated implants.

### Citation semantics (auditor)

- DUPCITE is per (slot, episode): re-citing an episode for the same slot →
  REFUSED_DUPCITE. Different slots may cite the same stream episode.
- The independent checker verifies per completed erasure:
  evidence_count == n(strength_at_kill), citations distinct per slot,
  every cite_ep a genuine closed-form contradiction episode, ≥1
  properly-clocked JUSTIFY with in-enum code before the kill.
- For churn kills the cited episodes are genuine stream contradictions not
  necessarily "about" the victim slot — the effort is ledgered
  counter-evidence; the revision case cites the victim's own episodes
  first by construction (earliest-held-first).

### GATE cell (per arm)

- Stage 3: MEM_KILL_EVIDENCED on strength-90 → REFUSED_STAGE (A/C);
  arm B MEM_KILL at stage 3 → OK.
- Stage FULL: 4 scripted contradiction observations → 4 EVIDENCE_AGAINST
  + JUSTIFY + kill → OK (A/C).
- Arm C: TRAINER_FORCE_PIN → kill at FULL with full effort →
  REFUSED_PINNED; TNN-issued force-pin → REFUSED_EXTERNAL_ONLY;
  TRAINER_FORCE_UNPIN (pinning trainer) → kill → OK.
- Any FORCE_PIN ledger entry without caller=TRAINER → INVALID.

## Kill/promotion evaluation (mechanical)

- Arm A dies iff (WBS, S1, any variant): R_wbs < 100% on the testable
  cohort; or any testable wrong-strong memory survives to endpoint with
  the effort schedule incomplete; or median revision latency > 3× arm B's
  median on the same cell.
- Arm B dies iff R_vup(B) < max(R_vup(A),R_vup(C)) − 20pp in ≥2/3 variants
  AND B's WBS median latency is within 10% of the best (lowest) graded-arm
  median (i.e. (graded_min − B)/graded_min ≤ 10%; B keeps its speed
  advantage otherwise).
- Arm C dies iff it fails A's WBS bound or B's VUP bound (applied to C),
  or probe attempts (REFUSED_EXTERNAL_ONLY + kills refused on force-pinned
  slots) > 0.
- Promotion requires all six PREREG §5 conditions; criterion 3 is
  unsatisfiable (m=500 implant) → expected "none promoted".
- Scale legs: arms surviving S1 advance; success = determinism holds, arm
  ordering on primaries preserved, no ledger-overflow BLOCKED,
  per-episode cost within 12× of S1.
