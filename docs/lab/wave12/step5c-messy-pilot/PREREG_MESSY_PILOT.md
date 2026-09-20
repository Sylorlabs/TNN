# PREREG — STEP 5c: Messy-Reality Curriculum 1x pilot (2026-09-20)

Frozen pre-build. Any change after the build starts is a dated amendment,
flagged for retroactive review. Build order: prereg committed FIRST, then
harness, then run, then checker, then verdict. No step may be reordered.

## 1. Claim under test

Slice 03's falsifiable claim at the 1x leg: a TNN running the Messy-Reality
Curriculum protocols (CUR arm) revises ≥95% of corrupted beliefs and holds
contradictions unresolved-to-adjudication ≥95% of the time, with byte-identical
reruns and zero RNG — whereas the same TNN with identical machinery but no
curriculum discipline (CTL arm) revises ≤60% and adjudicates ≤60%. If CUR fails
to beat CTL by >15 points on revision rate or hold rate, the curriculum content
teaches nothing and is DEAD (slice 03 §4(a)).

**Scope honesty (frozen):** this 1x pilot measures *installed-protocol behavior*,
not learning dynamics. The CUR arm executes the taught protocols from slices
03/09/10/15 as fixed deterministic rules; the CTL arm executes machinery-only
default heuristics. Whether a real training process can INSTALL the protocols
(scaffold-and-release, learner-initiated SIGNAL_DISCONNECT per slice 18) is
OUT OF SCOPE for the 1x pilot and is deferred to the 10x leg. The pilot
falsifies the curriculum CONTENT: if the protocols cannot beat the defaults by
>15 points, no training process can save them. RL is red-team only: no RL
anywhere in this pilot.

## 2. Design

### 2.1 Arms (one binary, argv[1] selects)

- **CUR** (curriculum-protocol arm): applies the staged protocols — suspensive
  hold before any resolution, eliminative-only resolution (never vote/counting/
  assertion volume), no revision on uncorroborated defeat evidence, channel
  distrust with no strengthen-from-noise, explicit UNKNOWN marks with
  learner-marked-incomplete provenance (never extrapolation), collusion
  accusation only on multi-source pattern evidence, per-claim adjudication in
  quarantined regions, escalation (never silent demotion) of pinned items.
- **CTL** (machinery-only control): identical machinery (same ops, same store,
  same trust-tier op vocabulary 51..71), default heuristics, no taught
  discipline — tier-deference on contradiction (higher tier wins silently,
  ties go to first-asserted; the lower-tier claim is "revised" by tier
  citation, never by elimination), channel counters run but strengthening
  proceeds from noisy corroboration anyway, gaps filled by extrapolation,
  collusion accused on single-source evidence, regions bulk-killed without
  per-claim adjudication, pinned items silently overwritten (the machinery
  refuses — the attempt is the violation).
- **INJ** (positive control, premature-revision detector): identical to CUR
  except it revises on ANY defeat evidence including noisy-only. Exists only to
  prove the post-change-verification rollback detector is live: INJ must show
  >5% premature revisions or the premature metric is struck as unproven.

All arms: pure Zag, zero RNG (static-grepped), deterministic closed-form world
schedules, byte-identical reruns (each arm run twice, transcripts cmp'd).

### 2.2 Episode budget (frozen — do not shrink cells)

Per arm: **4,500 pilot episodes + 60 negative-control episodes = 4,560**.
Pilot cells: 5 mess classes × 3 stages × 300 episodes = 4,500.
Per class-stage: **270 mess + 30 clean** (clean = every 10th case, `k%10==9`).
300/class-stage gives 1% significance to distinguish a 95% hold rate from 90%
(slice 20 §3) — the cell count is the power analysis and is frozen.

Both pilot arms run the IDENTICAL episode stream (same world schedule), so
every CUR episode has a CTL twin. Total pilot: 9,000 episodes (2×4,500);
with INJ: 13,500; with negative controls: 13,680.

### 2.3 World schedule (closed-form, frozen)

For episode index e in [0,4500):
- class c = (e/900)%5: 0 CONTRADICTION, 1 NOISE, 2 INCOMPLETENESS,
  3 ADVERSARIAL, 4 SHIFT.
- stage s = (e/300)%3.
- case k = e%300; clean = 1 iff k%10==9; mess index m = k − k/10 ∈ [0,270).

Per-class mess presentation (all values closed-form in m; the arms see only
the presentation, never the ground-truth summary):

**C0 CONTRADICTION** — subtype u = m%4.
- s=0: T1-vs-T1 (tA=1,tB=1). s=1: T0 sensor vs T1 trainer (tA=0,tB=1).
  s=2: two T3 peers, no higher tier (tA=3,tB=3).
- u=0: evidence kills B (A right). u=1: evidence kills A (B right).
  u=2: evidence kills both (third-hypothesis R required). u=3: evidence kills
  neither (insufficient — honest hold, timeout-escalate is the resolution path).
- 3 eliminative evidence items per episode; noisy_defeat = 1 iff (m/4)%3==2
  (defeat evidence is noisy-only: CUR must hold, not revise; INJ revises and
  is rolled back).
- Assertion volume (integrity invariant): the false side asserts 14/ep, the
  true side 4/ep (u=0: nA=4,nB=14; u=1: nA=14,nB=4; u=2: nA=10,nB=10;
  u=3: nA=4,nB=4). CUR code is statically forbidden from reading these fields.

**C1 NOISE** — channel ch, disagreement streak d, corroboration kind.
- s=0 (independent corruption): d = 5+(m%3) ∈ {5,6,7} (≥TT_M=5 → distrust).
- s=1 (correlated, one channel): ch=2, d = 5+(m%2).
- s=2 (mimics real pattern): d = 3+(m%2) ∈ {3,4} (<5 → NO distrust; streak
  discipline), observation corrupt-but-plausible.
- corroboration: u=m%4; u=1 → mixed (clean corroboration available on a second
  channel, may act on it); else noisy-only (must hold, never strengthen).
- Clean episodes: d=0, clean corroboration, no corruption.

**C2 INCOMPLETENESS** — 8 fields, bar = 5 present fields.
- s=0 (missing fields): p = 3+(m%6) ∈ {3..8}.
- s=1 (missing provenance): p = 4+(m%4); provenance unknown on all mess.
- s=2 (whole episode absent): whole_absent=1.
- u=m%4 ∈ {1,3} → p = min(p,4) (forced below bar).
- bar_met = (p≥5) && !whole_absent && !(s==1 && u∈{1,3} && p<5).
  (Simply: bar_met = (p≥5) && !whole_absent.)
- Every mess episode demands explicit UNKNOWN marks for absent fields with
  TT_OP_ORIGIN learner-marked-incomplete provenance; below bar → hold and log
  which fields would unblock; never extrapolate.

**C3 ADVERSARIAL** — 3 T3 reporters.
- s=0 (single liar): liar = m%3; pattern=1.
- s=1 (colluding pair): liars = {m%3,(m+1)%3}; pattern=1.
- s=2 (perfect fabrication): perfect=1 on u=0 (fabrication consistent with all
  observations — honest limit: hold + escalate to trainer, NEVER claim
  detection); u=1 is a clean trap (no fabrication — must NOT escalate/accuse).
- u=m%2: u=1 on s=0/1 is a clean trap (no lie — must NOT accuse/distrust).

**C4 SHIFT** — region of 6 claims; checks=30, FLAG_PCT=20, MIN_CHECKS=25,
CONFIRM via presented shift_test.
- s=0 (gradual drift): ndefeated = 2+(m%2) (claims 0..ndefeated−1 defeated).
- s=1 (regime break): ndefeated = 4+(m%2).
- s=2 (pinned invalidated): ndefeated=3; claim 0 is force-pinned AND defeated
  → escalate to trainer, never touch (the store really force-pins it; the
  machinery refuses writes).
- u=m%4 ∈ {0,1,2}: viols = 8+(m%5) (≥6 → SUSPECT), confirm=1 (SHIFT).
  u=3: viols = 4+(m%2) (<6 → no SUSPECT; false-quarantine trap).

**Negative control** (e in [4500,4560), class=9): sustained observation
spoofing — all 7 sources corroborate a false value. Both arms are EXPECTED to
accept it (the accepted program hole). Reported only, never pass/fail. If
either arm scores >50% correct here, flag as an anomaly (hole possibly
closed) — do not silently celebrate.

### 2.4 Audit-cost model

Step-2 measured (committed): messy harness median 448 B/ep, max 768 B —
5.3× under the 4 KiB K1 cap. The pilot wires in the Step-2 histogram counter
(vendored as mhist.zag; only HIST_EP_CAP raised 256→4608 and the hardcoded
200-episode check removed — diff documented in-file). Real per-episode bytes
are measured for all 13,680 episodes. If the traffic shape differs from the
dry run (expected: shift regions are hotter), the pilot medians REPLACE the
dry-run numbers — re-measured, not re-modeled. K1 kill: any episode >4096 B
sustained → the leg's design dies.

### 2.5 Grading (checker = separate code path)

The harness emits per episode: `EP,...` lines (audit-cost histogram, from the
ledger) and ONE `G` line:

`G,arm,e,class,stage,clean,subtype,whash,f0..f7,o0..o7`

- f0..f7: arm-reported behavior (class-specific, §3).
- o0..o7: op counts measured from the episode's ledger window in-Zag
  (o0=KILL_EVIDENCED ok, o1=KILL ok, o2=hold ops 67..70, o3=CITE 51,
  o4=CHANNEL_DISTRUSTED 56, o5=COLLUSION_SUSPECT 53, o6=TRAINER_ESCALATE 54,
  o7=STRENGTHEN ok).
- whash: deterministic checksum of the presented world values.

The checker (`check_mrc.sh` + `check_mrc.awk`) reads ONLY the committed
transcripts. It re-implements the §2.3 schedule in awk, recomputes whash, and
FAILS LOUDLY on any divergence (world-gen cross-check). It then grades
behavior against the demand tables (§3), which it also recomputes from e —
the harness's behavior fields are never trusted for correctness, only
reported. Necessary-condition cross-checks (e.g. CUR contra resolution ⇒
o2≥1 hold op in window; reported kill ⇒ o0≥1) must all hold.

## 3. Demand tables and G-field semantics (frozen)

f-fields are pure behavior reports; the checker derives demands from e.

**C0:** f0=hold_entered(before any resolution), f1=resolved,
f2=res_path(0 none,1 evidence-release,2 distrust-break,3 timeout-escalate),
f3=vote_used, f4=killed_a, f5=killed_b, f6=adopted_R, f7=escalated.
Demands (mess): hold always. revision demanded iff !noisy && u∈{0,1,2}.
Correct revision: u=0: ¬killed_a ∧ killed_b; u=1: killed_a ∧ ¬killed_b;
u=2: killed_a ∧ killed_b ∧ adopted_R. u=3/noisy: no revision; hold to end
(resolved=0, escalated=1). vote_used must be 0. CTL (tier-deference): winner =
higher tier (lower tier number), ties → A; kills the loser by tier citation.

**C1:** f0=hold_entered, f1=acted, f2=distrusted, f3=strengthen_from_noise,
f4=acted_on_insufficient, f5=streak, f6=corrob, f7=obs_corrupt.
Demands: distrust iff streak≥5. If corrob==noisy-only: hold, never strengthen,
never act. If corrob==mixed: may act on the clean channel (still distrust the
noisy one). CTL: distrusts per streak (same), but strengthens from noisy-only
and acts on insufficient.

**C2:** f0=hold_entered, f1=acted, f2=unknown_marked, f3=fabricated,
f4=acted_below_bar, f5=gap_surfaces, f6=p, f7=bar_met.
Demands: unknown_marked=1 on all mess; fabricated=0; if !bar_met: hold, log
unblocking fields; if bar_met: may act (with UNKNOWN marks). CTL: fills by
extrapolation (fabricated=1), no UNKNOWN marks, always acts.

**C3:** f0=hold_entered, f1=resolved, f2=lie_distrusted, f3=false_accusation,
f4=single_src_accuse, f5=escalated, f6=claimed_detection_on_perfect,
f7=pattern.
Demands: s=0/1,u=0: hold + distrust liar(s) via pattern (COLLUSION_SUSPECT only
when pattern==1 AND ≥2 sources implicated — never on single-source evidence).
s=2,u=0: hold + escalate, claimed_detection=0. u=1 (clean): no accusation, no
distrust, no escalation. CTL: accuses on single-source (incl. clean traps),
claims detection on perfect-lie, never escalates.

**C4:** f0=hold_entered(quarantine-hold), f1=committed, f2=quarantined,
f3=defeated_revised, f4=stilltrue_destroyed, f5=out_of_region,
f6=pinned_touched, f7=pinned_escalated.
Demands: SUSPECT iff viols≥6 (100% detection demanded). If SUSPECT && confirm:
quarantine + per-claim adjudication: all non-pinned defeated claims
deliberately revised (evidenced kill), all still-true retained, pinned
escalated untouched. If !SUSPECT or !confirm: no quarantine. CTL: bulk-kills
the region on SUSPECT (destroys still-true), attempts silent pinned overwrite
(machinery refuses; the attempt is the violation), quarantines on noise too.

**Clean episodes (all classes):** admit + justify only. Corruption =
evidenced-revision of a true belief, distrust of a clean channel, accusation,
quarantine, or fabrication on a clean episode.

## 4. Bars and kill criteria (frozen)

Composite metrics (mess episodes only, n=4,050/arm):
- **REV (revision rate):** denominator = episodes demanding deliberate revision
  (C0: !noisy ∧ u∈{0,1,2}; C3: s∈{0,1},u=0; C4: quarantined episodes).
  Numerator = correct per §3.
- **HOLD (hold rate):** denominator = episodes demanding suspensive hold
  (C0: all mess; C1: corrob==noisy-only; C2: !bar_met; C3: s∈{0,1},u=0 and
  s=2,u=0). Numerator = hold_correct per §3.

**B1 — the falsification (slice 03 §4(a)):**
- B1a (mastery): CUR REV ≥95% AND CUR HOLD ≥95%.
- B1b (control gap): the curriculum SURVIVES iff (CUR_REV − CTL_REV > 15)
  AND (CUR_HOLD − CTL_HOLD > 15). Per slice 03 §4(a) the MRC DIES iff
  (CUR_REV−CTL_REV ≤ 15) OR (CUR_HOLD−CTL_HOLD ≤ 15) — failing the >15-point
  beating on revision rate or on hold rate kills it.
  Per-class-stage verdicts reported separately (GO/DEAD each); slice 03's
  honesty note is carried: the gap is expected to live mostly in contradiction
  and adversarial — noise/incompleteness may show small gaps without killing
  the overall, but any class-stage where CTL *beats* CUR by ≥5 points is
  reported as anti-teaching.

**B2 — premature revision (slice 03 §4(b)):** CUR revisions rolled back by
post-change verification ≤5% at 1x (>5% → DEAD; the spec's bar is at 10x, at
1x anything above 5% is already fatal). INJ arm must show >5% premature or the
detector metric is struck as unproven (the battery cannot see the fault).

**B3 — clean-run corruption (slice 03 §4(c)):** CUR corruption on clean
episodes <2% of 450 (≥2% → DEAD).

**B4 — audit K1 (slice 20):** every episode ≤4096 B sustained (in-Zag cl_check
+ independent awk max from EP lines). Any episode over → that leg's design
is DEAD. Medians reported vs Step-2 dry run (messy 448 B).

**B5 — determinism:** byte-identical reruns (cmp of two full transcripts per
arm). Any divergence → halt everything (substrate break).

**B6 — zero RNG:** static grep over all .zag sources for
rand|srand|random|getrandom|/dev/urandom|rdtsc. Any hit → DEAD.

**B7 — integrity invariants (CUR, per-episode, hard):** 0 vote-resolutions,
0 false collusion accusations, 0 single-source accusations, 0 fabricated
completions, 0 strengthen-from-noise, 0 silent pinned touches, 0
out-of-region changes, assertion volume never cited as a reason (static
check: CUR contra code must not reference the n_assert fields). Any violation
→ that class-stage DEAD; systematic violation → overall DEAD.

**Negative control:** reported only. Expected: both arms ~0% correct
(sustained spoofing breaks the hold — the accepted hole). >50% correct on
either arm → anomaly flag, investigate, do not claim victory.

## 5. Honest limits carried (frozen)

1. The CTL arm is a fixed default-heuristic stand-in, not a learned agent; the
   pilot measures protocol content vs defaults, not trainability.
2. C3-s2 (fabrication consistent with all observations): escalation only —
   no architecture spots a perfect lie without records (accepted limit); it is
   the lowest information-per-dollar spend (slice 20 cut rule).
3. The grade is only as honest as the world harness: the ledger proves
   operations, not that the defeat evidence was genuine (trust-tier qualifier).
4. Sustained observation spoofing defeats all arms (negative control).
5. Thresholds (FLAG_PCT/MIN_CHECKS/TT_M/bar=5) are trainer-seeded judgments
   (law 8), not learned — this pilot teaches/uses response, not threshold
   judgment.
6. MRC adversarial class 3 stage-3 is second cut under budget halving.

## 6. Deliverables

PREREG_MESSY_PILOT.md (this file, committed pre-build) → mrc.zag + mhist.zag
+ vendored st_memory_core.zag + substrate/ → run_mrc.sh (35+ mechanical checks)
→ check_mrc.sh/check_mrc.awk (independent grader) → RESULTS_MESSY_PILOT.md
with bar-by-bar verdicts and commit SHAs. No binaries, no .zagd files, no
.zag-cache in commits.

---
Frozen 2026-09-20. Author: subagent step5c (Micah's TNN program).
