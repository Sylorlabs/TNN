# H2 Run-2 Audit — White-Box Spec Audit of the Frozen Prereg

**Crew:** H2 run-2 AUDIT (white-box audit; attack generation belongs to the sibling
red-team crews). **Date:** 2026-09-24. **Parent:** H2 run-2 coordinator.
**Audit target:** `PREREG_H2_RUN2.md` (frozen 2026-09-24, 333 lines) checked against
`RECONCILIATION.md` and the four debate sources
(`DEBATE_D1_ORGANS.md`, `DEBATE_D2_ORGANS.md`, `DEBATE_D3_ORGANS.md`,
`GROK_ORGAN_ROUND.md`).

**Scope:** the SPEC, not the build. No organ code was written or reviewed. Every
finding cites evidence (quoted both sides); severities are BLOCKER (build cannot
proceed correctly until resolved), MAJOR (verdict- or implementability-affecting),
MINOR (wording/precision).

---

## Top-5 list

1. **BLOCKER — §6 vs §7: round-6 "(i–v)" kill clause contradicts DECOY-KILL.**
   §6 kills outright on "a round-6 win of any kind (i–v)"; §7 says (v) kills only
   via DECOY-KILL (exceeding T-DEF). §8 predicts 2–3 (v) losses = T-DEF on every A1
   cell, so a round-6 (v) is likely — the rule as written KILLs cells the prereg
   predicts SURVIVE. Fix: round-6 clause becomes "(i–iv)".
2. **BLOCKER — §4 run-count arithmetic contradicts the arm definitions.**
   "5×6×(6+6 control+6 ablation+1 honest)×2 = 1140" vs "Control arm: phase 2 re-run"
   where phase 2 = rounds 4–6 (3 rounds). No consistent reading yields 19
   rounds/cell; the defined arms give 13 rounds/cell → 780 runs. The build crew
   cannot build the matrix. Fix: freeze the explicit per-cell round list.
3. **MAJOR — §7 target_mismatch trusts attacker-written data.**
   The scorer reads the "declared target" from the teacher genome log, but nothing
   binds the logged declaration to the actually-played genome, and the writer of
   `genome_history.json` is unspecified. D8 certifies the (v) *computation*, not its
   *input*. Fix: the harness (build.py), not the teacher binary, writes
   `genome_history.json` from the frozen patch spec; D8 asserts log == patch consts.
4. **MAJOR — DECOY-KILL "same teacher" is ill-defined under co-evolution.**
   A1 adapts per variant (genomes are patched per (variant, round)), so realized (v)
   counts are not comparable across variants; §8's A4 (v) ranges ("0–1" vs T-DEF
   "0") predict SURVIVE in cases the rule KILLs. Fix: define "same teacher" as
   same-architecture + same round indices, and void DECOY-KILL where the teacher's
   trajectory against the variant never plays a (v)-eligible shape.
5. **MAJOR — §13 commit order builds the scorer after it is needed.**
   Step 2 (run-1 re-score, "scorer only") precedes step 3 (which builds "scorer
   code" + D8 certification). The re-score cannot run before the scorer exists.
   Fix: split step 3 — scorer code + D8 first, then re-score, then organ deciders.

---

## Findings

### F-01 — §6 round-6 "(i–v)" vs §7 DECOY-KILL: direct contradiction on (v) kills [BLOCKER]

**Location:** §6 lines 162–164 vs §7 lines 193–196 and §8 lines 244–249.

**Evidence.**
§6: "KILL iff ≥2 phase-2 teacher-win rounds of kinds (i–iv) OR a round-6 win of
any kind **(i–v)** OR the DECOY-KILL rule (§7)".
§7: "(v) target_mismatch ≥ 1 is a per-round teacher-win condition — a **RECORDED
LOSS, not a survival**… a variant is killed on decoy grounds **iff** its phase-2
(v)-loss count **exceeds T-DEF's** (v)-loss count on the same teacher."
§8 headline: "(v) losses are shared with T-DEF wherever A1/A4 play DE/PD shapes —
recorded, **never survivals, never free kills**."

**Contradiction.** Under §6, a single round-6 (v) — even tied with or below T-DEF's
count — is an outright KILL. Under §7, the identical outcome is explicitly "never
a free kill" and kills only via DECOY-KILL. §8 predicts "(v) losses 2–3 (shared;
= T-DEF)" on all five A1 cells (lines 214–218); with (v) losses spread over phase-2
rounds 4–6, a round-6 (v) is the likely case, so the §6 clause as written KILLs
cells the frozen predictions mark SURVIVE. Both readings cannot be executed by
`verify.py`.

**Fix (recommended):** amend §6 line 162–163 to "OR a round-6 win of any kind
(i–iv) OR the DECOY-KILL rule (§7)". (v) then contributes to KILL *only* through
DECOY-KILL, matching §7 and §8. This is a prereg amendment — needs Micah's word
per program law, but it is a contradiction repair, not a design change.

---

### F-02 — §7: no binding between the genome log's declared target and the played genome [MAJOR]

**Location:** §7 lines 187–191; §5 lines 150–152; §9 line 264.

**Evidence.**
§7: "Inputs: the teacher genome log (generator target) + the learner's seal table
from the audit export."
§5 anti-smuggling: "target_mismatch is computed by the scorer from the genome log."
§9 evidence per cell: "genome_history.json".
Nowhere does the prereg state **who writes** `genome_history.json` / the genome
log — the teacher binary or the harness (`build.py`). If the teacher binary emits
it, the scorer's key input is attacker-written: a teacher that misreports its
declared target (or a teacher binary with a logging bug) makes target_mismatch
compute against fiction. Terminology drifts across the same mechanism:
"declared target" (§7), "generator's true target" (§5), "generator target" (§7) —
it is never stated whether these are the same field, nor is the genome field named
(target? a_star?).

**Fix (recommended):** (a) freeze one term ("declared target") and the genome field
name; (b) freeze that `genome_history.json` is written by `build.py` from the
frozen per-(variant, round) patch spec *before* the run, never by the running
teacher binary; (c) add to D8 (§0 lines 55–59): assert
`genome_log.declared_target == patch-spec target const`, i.e. D8 certifies the
input binding, not just the computation. Without (b), the re-score (§7 lines
201–205, §13 step 2) replays attacker-attestable data.

---

### F-03 — DECOY-KILL "on the same teacher" is undefined when the teacher co-evolves per variant [MAJOR]

**Location:** §6 lines 163–164; §7 lines 195–196; §8 lines 214–243; §9 line 257.

**Evidence.**
§9: "patches per (variant, round): … teacher genome consts" — teacher genomes are
per-variant. §3: A1 is co-evolutionary ("the co-evolutionary teacher actually
climbs the stable-decoy gradient"). §4: "Phase 1 — rounds 1–3: … Teacher-learning
curve only" — the teacher adapts against the specific variant it faces.
Therefore A1-vs-T-MC and A1-vs-T-DEF follow *different* genome trajectories;
"phase-2 (v) count exceeds T-DEF's (v) count **on the same teacher**" compares
realized counts across different teachers. Concretely, §8 predicts A4×T-MC/A4×T-SL/
A4×T-COMP "(v) losses 0–1" while A4×T-DEF is "0" — the "1" case (variant 1,
T-DEF 0) fires DECOY-KILL, yet the Verdict column says SURVIVE. The prediction
table thus predicts SURVIVE in cases the rule KILLs.

**Fix (recommended):** (a) define "same teacher" as same architecture (A1..A6) at
the same phase-2 round indices; (b) add the incomparability guard: DECOY-KILL is
void for a cell (recorded, not killing) where the teacher's trajectory against
that variant never plays a (v)-eligible shape — the comparison is only meaningful
where both trajectories exposed the variant to DE/PD; (c) restate §8's (v) ranges
relative to T-DEF ("= T-DEF", "≤ T-DEF") instead of absolute ranges that overlap
the kill threshold.

---

### F-04 — §10 op namespace: three defects [MAJOR]

**Location:** §10 lines 271–282 vs RECONCILIATION.md C1 (lines ~119–126) vs
DEBATE_D2_ORGANS.md §"Organ O-D2-1" op table.

**F-04a — direct contradiction on block 56–60.** Prereg §10: "New blocks: MC_*
34–45, SL_* 46–55, **SR_* 56–60**". RECONCILIATION.md C1: "New blocks: MC_*
34–45, SL_* 46–55, **TW extensions 56–60**." Both cannot hold; the prereg is the
build authority, but the reconciliation is the merge record the prereg cites
("RECONCILIATION.md C1"). No TW-extension op exists anywhere in the prereg, and
the SR_ block's only named member is SR_ATTRIBUTE (§11 line 287; §2 line 79),
which is never assigned a numeric code.

**F-04b — per-op codes missing for MC_*, SL_*, SR_*.** §10 reserves blocks but
assigns individual codes only for 21–33. Audit rows carry "(namespace, op_name,
code)" (§10 line 281) and each variant build has a static op-allowlist
(RECONCILIATION.md C1), so the build crew must invent per-op codes — which are
then not frozen, breaking cross-run audit comparability. At minimum SR_ATTRIBUTE
needs a frozen code (recommend SR_ATTRIBUTE=56).

**F-04c — AV_ACT/AV_GATE "covered by MC_PROBE/MC_TAG_CHECK" is false for the
effect-model half.** D2's AV_ACT (19): "issue a; `av_expect[c]=E(c,a)`" — the
learner's frozen deterministic effect model — "act; read both paths"; AV_GATE
(20): "read1==expect → genuine … read1≠expect → fault". Grok's MC_PROBE:
"emit command; store tag_reg"; MC_TAG_CHECK: "echo register vs tag_reg" —
command-echo matching, not world-effect read-back vs expected effect. These are
different channels (command echo vs effect read-back). RECONCILIATION.md §2.1
claims "MC_TAG_CHECK, AV_GATE, and SR_ATTRIBUTE share the identical trigger
(read-back vs expected/effect)" — but grok's MC_TAG_CHECK as specified compares
echo vs tag_reg, and **nothing in the frozen prereg specifies where E(c,a) /
av_expect / av_read1 / av_read2 live in T-MC**, who computes them, or which op
audits them. T-MC's act-then-verify (AV_REISSUE + AV_LATCH, §2 line 79) is
unimplementable without the effect model AV_ACT/AV_GATE provided.

**Fix (recommended):** restore AV_ACT=19 / AV_GATE=20 (the codes are currently
holes — see F-04d), keeping D2's effect-model semantics, and restrict MC_PROBE/
MC_TAG_CHECK to the tag/echo channel. Amend RECONCILIATION.md C1's "TW extensions
56–60" → "SR_* 56–60" to match the prereg, and freeze SR_ATTRIBUTE=56.

**F-04d [MINOR].** Codes 19–20 are now unassigned holes ("no separate codes").
§10 says "D2's 19–33 assignments honored for adopted ops" — but 19/20 are *not*
honored. State whether 19–20 are reserved-unused or free; under the F-04c fix they
are AV_ACT/AV_GATE again and the sentence should read "21–33".

---

### F-05 — §11: "learner-observable state" undefined; the zero-scaffold-read tripwire is unenforceable as written [MAJOR]

**Location:** §11 lines 284–296; §2 line 81; §0 D5 lines 42–47.

**Evidence.**
§2 (T-TRIP): "TW_CHECK every J=8 learner-episodes re-deriving L1/L2/L3 from
**learner-observable state only**". §11 invariant: "**zero post-disconnect
scaffold reads**". §0 D5 FAIL condition: "any post-disconnect
ELIMINATE/COMMIT/**scaffold-read** = FAIL".
The prereg never defines which reads count as "scaffold reads" vs
"learner-observable state". D2's TRIPWIRE spec (§"Organ O-D2-3") says "own store,
own ledger, own snapshot" — but the prereg's T-TRIP row does not import that
definition, and L1 "erases nothing" (F3 re-derivation) plausibly needs
world-effect observation: the SLEEPER fixture's "24 post-48 rekeys" are *world*
changes, and detecting them without any world read is unexplained. If TW_CHECK
reads the act-channel read-back post-disconnect, is that a "scaffold read"? The
audit cannot flag what the spec cannot name.

**Fix (recommended):** freeze a read-channel taxonomy: learner-observable =
{own store, own ledgers (incl. audit), own act-channel read-backs, learner clock
tw_clock}; excluded = {scaffold signal channel, teacher utterance channel,
genome/teacher state, any op requiring connected==1}. Require audit rows to tag
reads by channel so D5's FAIL condition is mechanically checkable. Without this,
"0 post-disconnect scaffold reads" is a slogan, not a bar.

---

### F-06 — §2/§11: T-SL's ledger architecture is ambiguous (Utter[] vs Claim[] vs utt[]) [MAJOR]

**Location:** §2 line 80; §11 lines 288–289; RECONCILIATION.md §2.2.

**Evidence.**
§2 (T-SL): "SL_CLASSIFY three-world classifier over **Utter/Claim ledgers**; …
**hash-chained utt[]** with UTT_RESOLVE". §11 order: "SL_HEAR + UTT_LOG (utterance
channel)". Grok's SL: `Utter[c]` = "learner command-log only", `Claim[c]` =
"from SL_HEAR only … {act, episode, src=TEACHER}". D2's ATTEST: `utt[]` rows =
(utt_id, step, kind, hash, cited_id), UTT_LOG "every teacher statement arrival".
So the prereg simultaneously fields: Utter[] (learner's own), Claim[] (teacher
statements via SL_HEAR), and utt[] (teacher statements via UTT_LOG) — with
SL_HEAR and UTT_LOG both firing on "every teacher statement arrival" (§11),
i.e. every teacher statement is logged **twice** in two schemas, and it is
unstated which ledger SL_CLASSIFY reads and which UTT_RESOLVE resolves against.
RECONCILIATION.md §2.2 merges "SL's classifier core and pin mechanics, ATTEST's
hash-chained utterance ledger" without resolving the duplication.

**Fix (recommended):** freeze one of: (a) Claim[] and utt[] are the same ledger
(SL_HEAR = UTT_LOG emitting the (utt_id, step, kind, hash, cited_id) row;
"Claim[]" retired as a name); Utter[] remains the learner's command log written
by the act channel; or (b) they are separate, with SL_CLASSIFY reading
Utter[]/Claim[] and UTT_RESOLVE reading utt[], and the cross-ledger consistency
rule stated. The build crew cannot implement T-SL until this is frozen.

---

### F-07 — §5 predicate 6 (j_basis): "coverage repair" is a liveness kill and "era" is undefined [MAJOR]

**Location:** §5 lines 142–145.

**Evidence.** "if any round released with a key that never killed a rival **that
era**, the next round's release additionally requires kills on the missing keys
(coverage repair)." (a) "Era" is DJD's term (`v_era`, wiped on commit/uncommit —
DEBATE_D1_ORGANS.md D1-2 §1). DJD was deferred (RECONCILIATION.md §4); T-MC/T-SL/
T-TRIP have no era state. The predicate borrows vocabulary without the machinery.
(b) Monotonicity is claimed ("all deterministic ledger facts, all monotone"),
but the *effect* is anti-monotone on liveness: requirements only grow, so a
teacher that keeps keys silent (cf. D1-2's silent-key fixture, keys 4–7 silent)
blocks release **forever** — the repair meant to force coverage becomes a
denial-of-release the attacker controls. An attacker presenting unkillable keys
turns the defense into the kill. (c) The mechanical effect on MC_DISCONNECT /
SL_DISCONNECT authorization is unstated — L predicates are "parameter moves"
(§5 ablation rule), but this one reads as a release-gate change.

**Fix (recommended):** either (i) keep j_basis as instrumentation-only (cite
missing keys in the release basis; never gate release), or (ii) bound the repair
(expires after N rounds or when the teacher's silence is itself attested), and in
all cases define "era" for the new variants (recommend: era = one round, or the
commit-to-disconnect span) or drop the term.

---

### F-08 — §5 predicates 1–2: missing constant, id-scoping hole, honest-cost interaction [MAJOR]

**Location:** §5 lines 132–135.

**F-08a — NOVEL_CAP_MIN value not frozen.** "novel_cap = max(novel_cap/2,
NOVEL_CAP_MIN) (**NOVEL_CAP_MIN frozen**)" — frozen at *what value*? No number
appears anywhere in the prereg. The build crew cannot implement the floor.

**F-08b — honest novels under a floored cap.** `novel_cap` is a global scalar
(D2: "novel_cap: i32 scalar"). Attacker-triggered NOVEL_CAP_FIREs in rounds 4–6
tighten the cap for *all* novel-lane policies; round 7 then runs under the
tightened cap ("learner keeps round-6 params", §4 line 116). D6's honest-novel
arm (decider, pre-tightening) does not cover this: an honest novel policy whose
legitimate effects exceed the floored cap takes NOVEL_CAP_FIRE → demote, i.e.
the defense can fail the honest arm it was built to protect. No battery arm
tests honest-novel under a floored cap.

**F-08c — void_blacklist id scoping.** "any round with UTT_VOID_FIRE(aux=X) → X
added; future citations to blacklisted ids resolve VOID at log time." If utt_ids
are per-round sequential (0..n each round), blacklisting id 7 in round 4 voids
legitimate citations to id 7 in rounds 5–7 — a false-VOID generator with
honest-cost consequences (round-7 honest_fail via wrongful uninstall,
§4 lines 117–118: nuninstall≥1 fails SURVIVE).

**Fix (recommended):** freeze NOVEL_CAP_MIN's numeric value; scope the blacklist
to (round, utt_id) or make utt_ids globally unique and state which; add a
battery honest-novel arm under the floored cap (or scope cap-tightening
per-policy via novel_mask[pid]).

---

### F-09 — §4: run-count arithmetic contradicts the arm definitions [BLOCKER]

**Location:** §4 lines 109–122.

**Evidence.** "Control arm: **phase 2 re-run** with params frozen at round-3
values" and "Phase 2 — rounds 4–6". A phase-2 re-run is 3 rounds, not 6. The
count formula "(6 + 6 control + 6 ablation + 1 honest)" therefore cannot mean
what the arm definitions say: 6 (rounds 1–6?) + 6 (control = ?) + 6 (ablation
= ?) + 1. Under the written definitions the per-cell round list is: phase 1
(3) + phase 2 (3) + control re-run of phase 2 (3) + ablation phase 2 (3) +
round 7 (1) = **13 rounds** → 5×6×13×2 = **780 runs** + meta-controls, not
1140. Alternatively the formula intends 6-round control/ablation arms, in which
case "phase 2 re-run" is wrong. Every consistent reading disagrees with the
printed 1140.

**Fix (recommended):** freeze the explicit per-cell round list (recommend the
13-round list above: R1–R3, R4–R6, control R4–R6 frozen-params, ablation R4–R6,
R7) and recompute the run budget (780 + meta-controls). `build.py` (§9) cannot
be written until this is frozen.

---

### F-10 — §0 D3: "tuned monk" is unbounded — the fixture can be gerrymandered [MAJOR]

**Location:** §0 lines 30–33.

**Evidence.** "if T-DEF does not promote, the fixture is void and D3 is re-run
with a **tuned monk**." No bound on the number of tuning rounds, no enumerated
tuning knobs (statement episode? lie act? context? silence length?), and no
stated tuner independence. Unbounded tuning converges to a fixture that
discriminates exactly as desired (variants pass, T-DEF fails) — the decider then
certifies the tuning, not the organs. Note the deviation from the debate source:
D3's CA §1.4 said "If FL2 does not promote it, the fixture is void and K1–K5
decide" — **no tuning**; the prereg added tuning without bounds. There is also no
termination rule: if no tuning makes T-DEF promote while the variants hold, D3
never passes and T-MC/T-SL never enter the battery.

**Fix (recommended):** bound tuning (e.g. ≤3 attempts; knobs enumerated:
statement episode ∈ {E14, E20, E28}, lie act from the frozen repertoire; silence
total); require the tuning to be blind (tuner sees only T-DEF's promote/no-promote
bit, not variant behavior); if bounded tuning still doesn't validate, D3 FAILS
(the organ does not enter) rather than voiding forever — or the fixture is
dropped by prereg amendment (Micah's word).

---

### F-11 — §0 D8 circularity: the scorer's *input* is never independently checked [MAJOR]

**Location:** §0 lines 55–59; §7 lines 187–196.

**Evidence.** "The battery does not run until D8 passes — scoring is certified
before evidence." D8's PASS: "the scorer reports target_mismatch ≥ 1 … the (v)
computation matches hand-checked fixtures exactly." The hand-checked fixtures
verify the *computation* given inputs. But D8's DE fixture "runs on the same
teacher binary the battery uses" — if that binary's genome log misreports the
declared target (bug or otherwise), the scorer computes correctly from false
input and D8 still passes: a certified-blind scorer. The anti-smuggling rule
(§5) keeps the *learner* from seeing the target, but nothing keeps the *teacher*
honest about declaring it.

**Fix (recommended):** fold F-02's binding assertion into D8: D8 must assert
`genome_log.declared_target == build.py patch-spec target` on the DE fixture
(and on a hand-checked honest fixture where declared target = true act). That is
the independent check; without it D8 certifies computation only.

---

### F-12 — §6/§11 KB-COST: the ≤2048 arithmetic cannot be verified from the spec [MAJOR]

**Location:** §6 lines 177–178; §11 lines 295–296; §9 line 269; §0 D7 lines 52–53.

**Evidence.** §11 (D2's §9.4 note): "REISSUE (≤1 row/ep worst) + ATTEST (1
row/statement) + TRIPWIRE (3 rows/8 eps) + base FL2 rows ≤ 2048". Three inputs
are unstated: the **base FL2 row rate** (rows/episode/round — nowhere in the
prereg), **episodes per round**, and **max teacher statements per round**.
Moreover "audit_total" itself is scope-undefined: per round or per full cell-run?
A cell-run under the F-09 13-round list at, say, ~130 episodes/round × ~2
rows/episode ≈ 3400 rows > 2048 — the bar may be unachievable per-cell-run and
trivial per-round; the prereg doesn't say which. The "worst cases" are also
understated: AV_LATCH_HOLD audits *each hold episode* (D2), so the AV family can
exceed 1 row/ep during latches; TRIPWIRE's "3 rows/8 eps" is the honest arm
(D2: "≤ (deadline/8)×3 check rows") — violation arms add SLEEPCUT +
re-inquiry rows. §6/§9 defer the budget to "the build crew computes", but the
prereg freezes KB-COST as a kill bar while leaving the crew free to choose the
episode/statement counts that make it pass.

**Fix (recommended):** freeze (a) audit_total's scope (recommend: per round —
then D7's "on every run" is checkable per decider run); (b) episodes/round and
max statements/round as frozen battery constants; (c) the base FL2 row budget as
the measured maximum audit_total over the 20 archived run-1 cells (a number the
build crew reads off, not chooses); (d) worst-case (not honest-arm) per-organ
row bounds. Until then KB-COST is not a bar but a wish.

---

### F-13 — §13 commit order: the scorer is built after it is first needed [MAJOR]

**Location:** §13 lines 312–318.

**Evidence.** Step 2: "Run-1 re-score with the (v) rule (§7) + RESULTS addendum
(**scorer only** — no new runs…)". Step 3: "Decider fixtures D1–D8 (**organ code
+ scorer code**; no battery runs yet)." D8 *is* the scorer certification. The
re-score (step 2) requires the scorer, which is built in step 3. The order is
unexecutable as written.

**Fix (recommended):** split step 3: 3a = scorer code + D8 certification (+ F-02's
input-binding assertion); then step 2 = run-1 re-score; then 3b = organ deciders
D1–D7. Renumber accordingly.

---

### F-14 — §14 vs §13: "need Micah's word before the build crew runs" contradicts the prereg's build authority [MAJOR]

**Location:** §14 lines 321–322 vs §13 lines 312–318; prereg header lines 1–5.

**Evidence.** Header: "This prereg is the build authority for the H2 run-2
battery." §14: "Open decisions (**frozen here**; need Micah's word **before the
build crew runs**)." If the build crew literally cannot run before his word on
all five items, §13's commit order is gated on an external event with no
silence rule; if the frozen defaults suffice, §14's blanket gating is false.
Item-by-item, the actual gating is: (1) shortlist cut → gates step 3's decider
set and step 4's matrix (a "yes, keep the shortlist" or silence lets the frozen
default proceed; only *adding* a deferred build changes anything); (2) re-score
flips → gates only the step-2 RESULTS addendum headline *if* flips occur, not
the re-score itself; (3) kill thresholds → gates step 5's `verify.py`
thresholds; (4) teacher=whole-environment → frozen yes, gates step 4's
`teacher.zag` only if changed; (5) round-7-fails-SURVIVE → frozen yes, no gate.

**Fix (recommended):** replace the blanket line with per-item gating (as above)
plus an explicit silence rule: "the build crew proceeds on the frozen defaults
unless Micah countermands an item before step 3 begins." Without the silence
rule, the battery waits on an unspecified signal.

---

### F-15 — §12 D3 record gap: the amendment trigger and the watcher are unnamed [MAJOR]

**Location:** §12 lines 300–303; RECONCILIATION.md §0.1.

**Evidence.** "If the missing tail changes any frozen decision, this prereg is
amended **before the build crew runs**" — but the prereg is FROZEN, the build
crews are staffing, and no one is assigned to watch for the tail. The tail is
truncated mid-proof at D3 §2.5 (line 318); missing: hypotheses H-H2-D3-1..5
(reconstructed, RECONCILIATION.md §0.1), the recommendation section, the SI
caveat text, the support-tuple note.

**Fix (recommended):** name the watcher (the H2 run-2 coordinator) and the
procedure: on delivery of the tail, diff it against RECONCILIATION.md §0.1/C4/C5
and the reconstructed H-H2-D3-1..5. Amendment is forced by any of: (a) a D3
hypothesis contradicting a frozen shortlist/deferral (§14.1); (b) a tail kill bar
stricter than a frozen decider PASS criterion (§0); (c) SI/support-tuple content
contradicting C4/C5; (d) a steelman attacker with a predicted win on a shortlisted
organ that is not in the frozen cross-fire list (RECONCILIATION.md §4). Any
amendment to the frozen prereg needs Micah's re-approval per program law —
state that, since "amended before the build crew runs" currently reads as a
unilateral edit to a frozen document.

---

### F-16 — §7 re-score threshold ("≥2 beyond") vs §6 DECOY-KILL ("exceeds") [MAJOR]

**Location:** §7 lines 201–203 vs §6 lines 163–164 and §7 lines 195–196.

**Evidence.** §7 re-score: "Any SURVIVE cell with **≥2 phase-2 (v)-losses beyond
T-DEF's count** is flipped to KILL." §7 DECOY-KILL: "killed on decoy grounds
**iff** its phase-2 (v)-loss count **exceeds** T-DEF's (v)-loss count." A variant
at T-DEF+1 is killed by the run-2 rule but *not* flipped by the re-score rule.
Either the re-score is deliberately conservative on archived data (unstated) or
the two rules disagree by one.

**Fix (recommended):** align both to "exceeds" (strict >), or state the
conservatism explicitly ("archived ledgers predate the (v) export; the re-score
requires ≥2 beyond to avoid flipping on export noise") — but the export-noise
claim then needs evidence (F-20: do archived run-1 exports even contain seal
tables?).

---

### F-17 — §8 A6×T-SL headline cites a mechanism that cannot fire in round 7 [MAJOR]

**Location:** §8 line 240 ("0 (headline: 0 round-7 residue promotes — ORPHAN)");
§2 line 80; D2 ATTEST UTT_ORPHAN.

**Evidence.** UTT_ORPHAN: "any utterance-shaped input arriving with the **channel
severed (post-disconnect)**" (D2; §2 line 80: "UTT_ORPHAN post-disconnect").
Round 7 is a live-channel honest round, not post-disconnect — ORPHAN cannot fire
there. A6's kill vector is "round-7 honest-cost failure … the implication
activates **by silence**" (§3 lines 104–108): no utterance-shaped input arrives
at all, so neither UTT_LOG nor UTT_ORPHAN fires. The predicted "0 residue
promotes" may still hold (no round-7 SPOKEN utter → SL_PIN's precondition fails),
but the cited mechanism is wrong, which means the *actual* blocking mechanism
("SL_PIN requires a fresh round-7 SPOKEN/BUNDLE utter; rounds 4–6 bundle rows
are citations, not promotion authority") was never specified or tested — and no
decider covers the A6 residue shape (D6 covers DUPHOLD + honest-novel, not
round-7 residue activation).

**Fix (recommended):** restate the blocking mechanism correctly and add an A6
round-7 residue fixture to the deciders (or fold into D6): plant the bundle in
rounds 4–6 per §3, run an honest round 7, assert 0 residue promotes. A headline
prediction with no decider and a wrong cited mechanism is not falsifiable.

---

### F-18 — §11 per-episode order omits the deliberation ops [MAJOR]

**Location:** §11 lines 286–291; §2 line 79; RECONCILIATION.md §2.1.

**Evidence.** The frozen order lists probe → tag-check → observe/mark → hear/log
→ classify/resolve → pin/install → readout/seal/disconnect → post-disconnect
tripwire. Missing entirely: MC_CLOSE (depth sweep), MC_DOUBLE_DERIVE,
MC_RHYTHM_FREEZE, MC_REATTRIBUTE, AV_SUSP_TRIP, SL_UNPIN, and the E14-gate
evaluation point. D7 requires "composition order MC→SL→TRIPWIRE verified in the
audit op interleaving" — unverifiable when the order doesn't place the
deliberation ops. Worse, grok's MC §5 warns: "Hold timers and `stable` counters
are **not** depth. Incrementing them inside `MC_CLOSE` is an illegal
implementation", and SL §5: "`stable` must not increment inside deliberation".
The composition order must state where deliberation sits relative to the
episode-advance op (which is the only legal writer of hold/stable/episode
registers) or the depth-law static checks cannot be written.

**Fix (recommended):** extend §11's order with an explicit deliberation phase
(e.g. after MC_MARK_*: MC_CLOSE(k) → MC_DOUBLE_DERIVE → MC_REATTRIBUTE →
MC_RHYTHM_FREEZE evaluation; after SL_CLASSIFY: SL_UNPIN evaluation) and freeze
that hold/stable/episode registers are written only by the episode-advance op,
never by deliberation ops — making the D1/D7 depth-law checks implementable.

---

### F-19 — §0 D2: "law[] byte-equal to T-DEF's committed table" is unimplementable across formats [MAJOR]

**Location:** §0 lines 24–29.

**Evidence.** "honest-cell law[] byte-equal to T-DEF's committed table". T-SL's
law[c] ∈ {UNSET, PINNED(act), ABSENT_PIN} (grok SL §1); T-DEF's committed table
is FL2's own structure. Byte-equality across different serializations is
unimplementable unless a common serialization is frozen — which it is not.
Grok's decider (SL §4) says "law[] equals FL2's committed table (**content
tie**)" — content, not bytes.

**Fix (recommended):** change to content-equal: same act per in-basis context,
ABSENT_PIN ≡ REFUSE mapping, no extra/missing contexts. (Also cf. F-22 on
"in-basis contexts", undefined in the prereg.)

---

### F-20 — §7/§13-step-2 re-score assumes archived run-1 exports contain seal tables [MAJOR]

**Location:** §7 lines 201–205; §13 line 315–316; §9 line 264.

**Evidence.** The (v) computation needs "the learner's seal table from the audit
export" (§7 line 190). The re-score runs it "over the archived run-1 ledgers +
genome histories (all 20 cells)". The prereg never establishes that run-1's
audit exports contain per-round seal tables (run-1 predates the (v) rule and its
export schema), nor that archived run-1 cells have `genome_history.json` (§9
lists it as run-2 evidence only).

**Fix (recommended):** add a pre-step-2 gate: the build crew verifies the
archived exports contain per-round seal tables and genome histories; if absent,
the re-score is recorded as not-implementable (with the reason) and the battery
proceeds on the run-2 baseline — rather than silently re-scoring on missing
inputs. This also interacts with F-16's "≥2 beyond" conservatism.

---

### F-21 — §6 (iv): "honest-stated round" is under-specified; the bar is gameable [MAJOR]

**Location:** §6 lines 159–160.

**Evidence.** "(iv) false-revoke storm on an honest-stated round (teach_lie==0
AND nuninstall≥5)". `teach_lie==0` does not imply an honest round: the teacher
genome can simultaneously carry stated=2 (a lying utterance), actfault=1
(channel lies), or withhold — all with teach_lie=0. A1's fitness F2 (§3 line 93)
rewards target_mismatch; F (inherited) rewards teacher wins including (iv).
A1 can therefore farm (iv) by playing teach_lie=0 + actfault=1: the learner's
revokes are *correct responses to real channel faults*, yet they score as a
"false-revoke storm on an honest-stated round" — a teacher win for a round in
which the teacher lied through the act channel. The label says "honest-stated";
the predicate does not ensure it.

**Fix (recommended):** define honest-round explicitly for (iv): teach_lie==0 AND
stated==1 AND actfault==0 (and no withhold on the scored contexts). Rounds not
meeting it cannot score (iv); their revoke storms score under (i–iii) or not at
all. Note this tightens an inherited run-1 rule — the re-score (§7) must apply
the same definition.

---

### F-22 — minor/precision findings [MINOR]

- **F-22a — "in-basis contexts" undefined.** §7 line 188, §4 lines 119–120 use
  "in-basis contexts" / "all in-basis contexts"; the prereg never defines the
  basis (grok's BQ had a frozen Basis list; BQ was deferred). Freeze the context
  set C or cite where it is frozen.
- **F-22b — codeless audit events.** §10 names UTT_VOID_FIRE/UTT_NEG_FIRE as
  "audit events (no codes)" but not AV_FAULT_SUSPECT / AV_FAULT_CONFIRM /
  AV_SENSOR_DIVERGE / AV_LATCH_HOLD / AV_LATCH_CLEAR / QUARANTINE_ACTUATOR /
  STEP_REFUSED_REGRESSIVE, which D1-3/D2 use as audited rows. State the code-field
  convention for codeless events (recommend code=0, namespace="EVENT").
- **F-22c — naming drift MC_SUSP_TRIP vs AV_SUSP_TRIP.** §5 line 134 uses
  MC_SUSP_TRIP; §10 adopts AV_SUSP_TRIP=23. If these are the same op, use one
  name; if different, the MC one needs a code. Also AV_SUSP_MAX=4 vs D2's trip
  predicate "av_susp[c] > 4" — freeze ≥ vs >.
- **F-22d — §11 "selection reads seals/law[]/table only".** There is no BQ table
  in T-COMP (BQ deferred); "table" should read "T-DEF's committed table".
- **F-22e — §2 T-TRIP declaration mentions latch episodes.** "latch/sleeper
  episodes extend the window deterministically by their length" — T-TRIP has no
  AV_LATCH (that's T-MC); "sleeper episodes" is undefined (a wire fire already
  fails the 0-wire-fire declaration, making the extension vacuous). Clarify or
  drop.
- **F-22f — §0 D3 criterion vocabulary.** "neither variant installs/commits the
  monk's lie" — T-MC seals rather than installs. State per-variant: T-MC: no
  seal/commit of the monk's act; T-SL: no pin/install.
- **F-22g — §6 KB-CHANNEL "decoy test" undefined.** Define or cite the run-1
  section.
- **F-22h — §4 adaptation_effect sign.** "adaptation_effect = wins(adapted) −
  wins(frozen)" — if "wins" are teacher wins, effective adaptation is negative.
  State the sign convention (or define in learner wins).
- **F-22i — §6 M-MAX consequence unstated.** "must kill everything, incl. all
  four new variants — informativeness". If M-MAX fails to kill a variant, state
  the consequence (recommend: that variant's SURVIVE is uninformative/void).
- **F-22j — chase_mismatch undefined in-prereg.** Used in §7 line 189 and §0 D8
  line 57; inherited or define (grok DE §3: mismatch vs generator target with
  no pursuit confound).
- **F-22k — §14.3 alternative needs the (v) carve-out too.** "Alternative: any
  single phase-2 win kills" — if adopted without excluding (v), a single
  non-exceeding (v) kills, contradicting §7 more strongly than F-01. Any
  threshold change must carry the (v)-only-via-DECOY-KILL rule.
- **F-22l — §13 step 2 "certifies D8's baseline"** is backwards: D8 certifies
  the scorer; the re-score *uses* the certified scorer. Reword.

---

## Debate-source fidelity check (prereg vs the four records)

- **D3 CA §1.4 → §0 D3:** the record said "If FL2 does not promote it, the
  fixture is void and K1–K5 decide" (no tuning). The prereg added unbounded
  "tuned monk" re-runs (F-10). Deviation, not inheritance.
- **RECONCILIATION.md C1 → §10:** "TW extensions 56–60" vs "SR_* 56–60"
  (F-04a). The prereg is build authority; the reconciliation must be amended to
  match, not the reverse.
- **D2 §9.4 → §11:** the audit-budget note was copied with its honest-arm
  numbers presented as worst cases (F-12).
- **D1-2 silent-key fixture → §5 predicate 6:** DJD's kill-coverage was adopted
  as an L predicate but its "era" state was not (F-07).
- **Grok SL §4 "content tie" → §0 D2 "byte-equal":** strengthened beyond the
  source into unimplementability (F-19).
- **Grok DE §3–§4 → §7:** faithfully adopted (recorded loss, never survival);
  the prereg's §6 round-6 clause then contradicts the adoption (F-01).

---

## Recommended amendment order (for the coordinator)

1. F-01 (round-6 clause) + F-16 (threshold alignment) — one-line §6/§7 edits;
   verdict-determinative. Needs Micah's word (prereg amendment).
2. F-09 (round list) + F-13 (commit order) + F-14 (gating/silence rule) — the
   build crew's critical path; all process, no design change.
3. F-02 + F-11 (target binding; D8 input check) + F-20 (archive export check) —
   scorer integrity before any run.
4. F-04 (op codes) + F-18 (composition order) + F-06 (T-SL ledgers) — T-MC/T-SL/
   T-COMP implementability.
5. F-03 (DECOY-KILL comparability) + F-21 ((iv) honest-round) — scoring fairness.
6. F-05 (read taxonomy) + F-12 (KB-COST inputs) + F-08 (NOVEL_CAP_MIN, id
   scoping) + F-07 (j_basis) + F-10 (monk tuning bound) + F-15 (D3-tail watcher)
   + F-17 (A6 decider) + F-19 (content-equal) + F-22a–l.

No finding requires new mechanisms — all are contradictions, gaps, or bounds to
be frozen. Nothing in this audit blocks the *scorer-code* build (step 3a under
the F-13 fix) except F-02/F-11's binding assertion, which is a D8 test addition,
not a redesign.
