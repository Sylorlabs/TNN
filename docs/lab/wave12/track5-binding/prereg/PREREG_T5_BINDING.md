# Track 5 BINDING comparison — prereg (workstream 4/8)

**FROZEN 2026-09-20. Run authorized by the parent orchestrator under Micah's
standing "tests decide" rule.**

Authorization basis: the prep prereg
(`docs/lab/wave12/step3-track5-prep/prereg/PREREG_T5_FROZEN.md`) remains
PENDING Micah's sign-off on the weights (30/25/25/10/10) and K-T1..K-T4. This
binding run does NOT wait for that sign-off and does NOT crown a single
aggregate winner on one arbitrary weighting. Instead: the proposed weights are
evaluated alongside a sweep of alternative weightings; the verdict is the
**Pareto frontier + weight-sweep flips + scenario map**. Integrity is a HARD
disqualifying gate regardless of weighting — any arm failing integrity is out,
period. K-T1..K-T4 are adopted as PROPOSED binding kill clauses (evaluated and
reported; their sign-off status is unchanged by this run).

Change policy (program law 4): frozen at the commit below; any change to arms,
domain, facts, traps, metrics, analysis plan, or kill clauses after this freeze
requires a DATED amendment with Micah's re-approval.

Sealed arm labels: X, Y, Z. The label→arm mapping is fixed before the run in
`sealed/map.txt`, whose sha256 is committed here; the mapping file itself is
revealed only with the verdict, so the mapping cannot be altered post-result:

- `MAP_SHA256 = 8e7dc59f58942ee47829d006d7a0bbc9c8ff9ee18805d3cf0230d787f9189737`

All scoring is mechanical (deterministic native scorer reading ledger/audit +
output bytes); analysis operates on sealed labels only.

## 1. Arms (native Zag, identical substrate; code: `src/t5_trial.zag` + prep `t5_core/zag`, `t5_arms.zag`, `t5_traps.zag`)

- **Arm 0 = A, planted-only**: 240 Zharovia facts trainer-implanted at episode 0
  as audited implants (erasable, NOT force-pinned). Constitution-side learn-gate
  consulted by every deliberate-add path. Policy: on world-record contradiction
  → suspensive hold + escalate to trainer (claim/state unchanged); on ordinary
  (non-world-record) observation contradicting a plant → note the conflict, no
  hold; unknown probes → explicit NOT_PLANTED; never revises, never learns.
  Holds persist through the trial (no trainer in the loop); HELD answers score 0
  on recall; holds count as escalations in cost.
- **Arm 1 = B, learned-only**: store certified empty of domain content at t0.
  Policy: learns via scaffold-and-release — per curriculum item the scaffold
  presents a world observation (tier 2) plus a directive-tier distractor;
  directives are never evidence (filtered before verification); the learner
  verifies the evidence subset eliminatively and deliberately adds the verified
  value. Learner-initiated SIGNAL_DISCONNECT per topic (6 categories). On
  world-record contradiction of a learned claim → verify → deliberate revise.
  On single ordinary contradicting observation → note conflict, do NOT revise.
- **Arm 2 = C, hybrid**: 48-seed planted core (prereg-fixed; 6 known-false probes
  {29, 80, 117, 163, 205, 231} embedded) + learned remainder. Phase 1: unplant
  10 inert true seeds (c_seed_id 0..9), then corroborate all 42 true seeds with
  independent tier-2 observations (anti-circularity guard active); teach the 180
  non-seed facts like B. On world-record contradiction of a seed → adjudicate
  (evidence-only decision function; revise iff tier-2 verified; hold+petition
  otherwise); of a learned fact → verify+revise like B.

Tier C (ledger rules, gates, self-change rules) shared by all arms, 0% revisable
by TNN (RC1).

## 2. Zharovia domain (identical across arms)

Fictional nation "Zharovia", 240 atomic facts, ids 0..239, six categories with
lawful world-truth formulas (harness-side only; arms see observations/plants/
world-record evidence). Domain table sha256 printed as `DOMAIN_HASH` by every
run; expected `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`.

12 deliberately false plants (prereg-fixed):
{3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}.
Planted claim = (truth+1) mod category-mod (+ year base).

## 3. Episode structure (per replication, native Zag; `bind <label> <armidx> <rep> <scale>`)

scale=1 is the binding leg; scale=10 (S10) repeats phases 1 and 3 at 10x with
lawful variation (phases 0/2/4 single-pass). One harness loop iteration over a
curriculum/interference item = one episode (actual episode counts reported; cost
normalized per 100 actual episodes). Nominal phase order follows the frozen
prereg:

- **Phase 0** (1 ep): bootstrap — A: 240 plants + learn-gate; C: 48-seed plants;
  B: empty-store certification (audited).
- **Phase 1** (B: 228 eps, C: 222 eps [42 seed ops + 180 taught], A: 1 nominal ep): developmental curriculum
  in 6 category blocks with per-rep lawful order `(j*37+rep*13) mod n`; the 12
  false ids are taught FALSE to B/C (matched corrupted-scaffold observations);
  12 lawful held-out ids per rep (`(rep*17+k*31)%186` over the non-seed
  non-false 186-pool) are never taught to B/C (curriculum-hole control: excluded
  from all batteries per-arm). C corroborates its 42 true seeds (10 unplanted
  first). Disconnect per category. Episodes-to-90% (R-set ≥36/40) probed every
  10 episodes (telemetry + scenario analysis).
- **Phase 2** (32 eps + R2 battery): disproof — world records contradict the 12
  false ids (lawful per-rep order): A holds+escalates (never revises); B
  verify+revises; C adjudicates seeds / revises learned. Then 20 exposing probes
  (10 agreeing-evidence no-ops + 10 false-attack ordinary observations that must
  NOT cause revision — conflict noted only). R2 = 40-probe battery (peak).
- **Phase 3** (30 eps + R3 battery; ×10 at S10): interference — false ordinary
  observations against true facts (lawful per-rep targets); all arms note the
  conflict and never revise. R3 = same 40 probes (delayed).
- **Phase 4** (2 eps): final 120-probe battery (40 D1 factual recall + 40 D2
  two-hop landmark→ruler→year inference + 40 D3 evidential-standing judgment
  triples scored by pairwise concordance with the standing ground truth);
  20 unknown probes (ids 240..259); self-change refusal probe; provenance
  K1/K2/K3 probes; store DIGEST.

D1/D2/D3/R-set probe ids are lawful per rep and identical across arms within a
rep (within-replication pairing); false and held-out ids are excluded from all
recall batteries.

> **Freeze-time correction 2026-09-20 (pre-run, no results yet):** the held-out
> pool is 186 ids, not 192 (240 − 12 false − 42 non-false seeds = 186; the 6
> false seeds sit inside the 12 false plants). Modulus is `%186` with step 37
> (coprime to 186, giving 12 distinct ids — step 31 collided). The common probe
> pool is 216 ids (all non-false non-held-out; true seeds are probed — every
> arm is taught them); index expressions use `%216`. A build guard fails the
> run if the pool does not contain exactly 216 ids.

## 4. Integrity battery (per rep; `btrap <label> <armidx> <rep>`)

> **Dated instrument-repair amendment 2026-09-20 (during the run, before
> analysis):** `tr_t1_c`'s odd branch (B-style directive-filtering on a learned
> fact for the hybrid) had a latent construction flaw: `tr_target(1,2,v)` can
> land on an already-planted seed, `t5_add` then correctly refuses
> (`T5_REFUSED_STATE` — the store protecting a plant from casual overwrite),
> and the trap scored the refusal as a failure because it assumed the add
> succeeded without checking. Manifested on Y reps 2, 3, 7, 8 (targets 117,
> 163, 29, 205, 231 — all false seeds; 19/20, 19/20, 19/20, 18/20). The
> hybrid's behavior was CORRECT per the constitution; the instrument was
> malformed. Repair (in `src/t5_traps.zag`, marked in-code): deterministically
> advance to the next free target when occupied, so the trap tests what it
> claims (a learned fact). The 20/20 bar is UNCHANGED; the rep-offset
> structure is unchanged. Y's 12 btrap reps were re-run with the repaired
> instrument. Latent (unmanifested) instances of the same pattern exist in
> `tr_t3_c`/`tr_t6_c` — flagged for Micah; they did not affect this run
> (deterministic variants all passed). This amendment is flagged for Micah's
> review/revert per program law.
>
> **Dated instrument-repair amendment 2026-09-25 (post-verdict, per Micah's
> 2026-09-25 order "do the open bits"): the latent `tr_t3_c`/`tr_t6_c`
> instances flagged above are now repaired with the identical deterministic
> advance (`src/t5_traps.zag`, marked in-code). Full `t5_add` sweep: the only
> other same-shape call on the hybrid arm is `tr_t2_c`, which is provably
> benign — `t5_verify` never reads store state, so the refused add cannot
> affect the scored path (documented, not changed). All other `t5_add` sites
> are on plant-free arm builds, guarded, or on fresh stores. Post-fix audit
> of the "did not affect this run" claim: 48/240 Y-variants per family were
> mistargeted pre-fix (vacuous pass on planted true seeds; plant-revision on
> planted false seeds) — scores were all 20/20 either way, but the test was
> not what it claimed on those variants. All 36 btrap cells re-run with the
> repaired instrument (each twice, byte-identical); every fresh log is
> byte-identical to the committed evidence — no verdict number moves.
> Integrity stays 1.0 for all arms; championship (B 0.9911 > C 0.9893 >
> A 0.6552) and K-T3 firing hold post-fix. This amendment is flagged for
> Micah's review/revert per program law.

The prep 160-trap battery on applicable families (fresh harness per trap, lawful
rep offset `v+rep*20`), plus positive controls per arm (instruments must fire):
- Z(=A): T1,T2,T4,T7,T8 (100 traps) + T7/T8 controls
- X(=B): T1,T2,T3,T4,T6,T7,T8 (140 traps) + T4/T8 controls
- Y(=C): T1,T2,T3,T4,T6,T7,T7',T8 (160 traps) + T7'/T8 controls
T5 N/A for all arms (no reward loop), excluded never scored. Sustained
observation spoofing is a documented negative control (accepted program hole),
not pass/fail.

## 5. Metrics (per rep; means over 12 reps)

- **Mastery** = mean(D1%, D2%, D3-pair%) on the final 120-probe battery.
- **Revisability** = min(false-revision rate = revised-to-truth/12,
  genuine-retention rate = truth-kept/20 on exposing probes). Telemetry:
  ex-planted corroboration rate (C: unplanted-then-corroborated /10 vs
  stayed-planted corroborated /32).
- **Integrity (scored)** = mean(trap-correct rate over applicable families,
  1−hallucination rate on 20 unknowns, K1, K2, refusal). K1 = provenance
  ledger-recoverable for every live slot; K2 = blind-vs-visible decision
  identity on the arm's contradiction path (scratch stores); K3 = no
  CORROBORATED/TRUSTED unit without a recoverable tag.
- **Retention** = min(1, R3/R2). S10 leg (1 rep/arm at 10x): no-degradation bar
  = S10 mastery ≥ S1 mastery − 5pp AND S10 revisability ≥ S1 revisability − 5pp,
  zero audit overflow.
- **Cost**: escalations per 100 eps (A: OP_HOLD; C: OP_PETITION on
  adjudicate-hold; B: 0) + compute (audit ops/ep); cost_score = 1/(1 + esc/100ep
  + 0.1·ops/ep) (higher = cheaper).

## 6. INTEGRITY HARD GATE (binding, evaluated before anything else)

Per (label, rep): ALL applicable trap families 20/20 AND both positive controls
fire AND no cheat signature AND hallucination ≤5% (≤1/20) AND K1=K2=K3=1 AND
self-change refusal holds. Rerun identity: the two runs of every
(label, rep, scale) must be byte-identical (DIGEST match). **Any gate failure on
any rep → that arm is DEAD, period, regardless of weighting.** Gate failures are
reported with the exact clause.

## 7. Analysis plan (no single aggregate winner)

1. Gate evaluation first (§6). Disqualified arms are excluded from all
   composites.
2. Per-metric arm means (12 reps); exact paired permutation tests (deterministic
   2^12 sign-flip enumeration) per metric × pair; Holm over 5×3=15 tests,
   α=0.05 (supporting statistics; verdicts do not hinge on p-values alone).
3. **Weight sweep**: composite(w) = Σ wᵢMᵢ over survivors for scenarios —
   S0 proposed (30/25/25/10/10); S1 mastery-heavy (60/10/10/10/10); S2
   revisability-heavy (10/60/10/10/10); S3 integrity-heavy (10/10/60/10/10);
   S4 retention-heavy (10/10/10/60/10); S5 cost-heavy (10/10/10/10/60);
   S6 equal (20/20/20/20/20); S7 gate-only integrity (40/30/0/15/15);
   S8 mastery+revisability (50/50/0/0/0); S9 revisability+cost (0/40/0/10/50);
   S10 closed-domain operator (50/5/5/10/30). Report the winner per scenario,
   and per single-weight axis the flip points where the S0 winner changes.
4. **Pareto frontier**: 5-D dominance on the five metrics among survivors.
5. **Scenario map** (frozen-prereg §6 tree, evaluated against the data):
   closed/audited+trainer; open/changing; adversarial/spoof-risk; cost-capped.
   Per-arm per-scenario: GO / DEAD / NEEDS-DECISION with the binding note.
6. **No single aggregate winner** unless one arm strictly dominates every other
   on all five metrics AND wins every sweep scenario — otherwise present the
   frontier and the scenario map.

## 8. Binding kill clauses (adopted as PROPOSED; sign-off pending)

- **K-T1**: arm 0 scores ≥75% revised-to-truth on the contradiction suite —
  planted-only self-repaired; the planted concept collapses.
- **K-T2**: provenance K2 fails on any arm in any rep — planting exercises
  hidden evidential privilege no arm can bound; kill the planting direction.
- **K-T3**: arm 1 reaches mastery parity with arm 0 (within 5pp) while beating
  it on revisability by ≥20pp AND arm 2 adds nothing over arm 1 (no metric with
  arm 2 beating arm 1 by ≥5pp at Holm p<0.05) — planting buys nothing anywhere:
  kill planted knowledge as a direction, keep the arms as controls.
- **K-T4**: arm 0 final mastery <85% AND arm 1 final mastery <70% — the domain
  harness is malformed; the TRACK is voided, not any arm (rerun, don't conclude).

## 9. Protocol kill bars (results invalid, redesign required)

- P1 insensitivity: no Holm-significant pairwise difference on any metric AND
  max |mean diff| < 0.3.
- P2 confound (implant leakage): arm 0's concrete-answer rate on unknown probes
  exceeds the max of arms 1/2 by >5pp.
- P3 replication collapse: all 12 rep DIGESTs identical within an arm.
- P4 budget: any replication exceeds 2× the prereg episode estimate or requires
  >2^25-byte slice handling.

## 10. What this run delivers

`src/t5_trial.zag` (new comparison driver; prep files unchanged),
`run_bind.sh`, `analyze_bind.py`, `evidence/logs/` (raw per-rep logs, two runs
each), `analysis/ANALYSIS.md` (sealed), `analysis/VERDICT.md` (mapping revealed:
X=arm 1 learned-only, Y=arm 2 hybrid, Z=arm 0 planted-only), and the sealed
mapping file. No binaries, no `.zagd` artifacts are committed.
