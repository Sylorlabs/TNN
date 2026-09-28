# H2 Run-2 Reconciliation — Merge of Four Debate Sources

**Date:** 2026-09-24. **Crew:** H2 reconciliation (parent: H2 run-2 coordinator).
**Sources:** D1 eliminative (`DEBATE_D1_ORGANS.md`), D2 gap-closing (`DEBATE_D2_ORGANS.md`),
D3 non-eliminative (`DEBATE_D3_ORGANS.md`), grok-4.7 (`GROK_ORGAN_ROUND.md`).
**Output:** shortlist + frozen `PREREG_H2_RUN2.md` (the build authority).

## 0. Material-integrity flags (read first)

1. **D3's record is truncated.** The delivered `DEBATE_D3_ORGANS.md` ends mid-sentence at
   §2.5 (line 318, inside the depth-monotonicity proof). It contains **no** hypotheses
   table (the H-H2-D3-1..5 referenced in the task), **no** recommendation section, **no**
   SI caveat text, and **no** support-tuple note. H-H2-D3-1..5 in the backlog are therefore
   **reconstructed by this crew from the delivered organ specs**, marked accordingly.
   If D3's crew delivers the missing tail later, the reconstruction is diffed and amended.
2. **The task-referenced "D3 caveat (SI's δ-selection private digest)" and "D3 note on
   DB's support-tuple choice" do not exist in any delivered file** (searched all four
   records). Both are resolved below on first principles; the resolutions are frozen in
   the prereg so they cannot drift.
3. D1's record references grok's organs as "later round" (§6); grok's record references
   the D-crews' attackers as cross-fire. All four sources are now merged here.

## 1. The shortlist (3 organs + 1 composed arm)

| ID | One-line mechanism | Built from |
|---|---|---|
| **T-MC** | Monotone lattice learner: corroborated −1 refutes, tag-mismatch quarantines (never refutes), closure only adds refutations; act-then-verify with re-issue + bounded latch on the act channel | grok MC + D1-3 AR attribution + D2-1 REISSUE |
| **T-SL** | Split-ledger attestation: utterance ledger vs claim ledger, three-world classifier (UNSAID/ABSENT/SPOKEN/FALSE_CLAIM), install only from attested utterances; unattested-but-coherent content acts under a corroboration-capped novel lane | grok SL + D2-2 ATTEST |
| **T-TRIP** | Post-disconnect tripwire: learner-armed, learner-scheduled re-derivation of stated laws after SIGNAL_DISCONNECT with zero scaffold reads; violation → SLEEPCUT (demote + re-inquire, channel stays severed) | D2-3 TRIPWIRE (near-verbatim) |
| **T-COMP** | Composition arm (no new mechanism): T-MC + T-SL + T-TRIP wired in frozen channel order, testing the composed-vs-separate question head-to-head | wiring only |

T-DEF (frozen run-1 FL2-default, vendored pristine) is the regression control in every
cell. New variant IDs follow the frozen T-DEF/T-A2/T-A3/T-B1/T-F3 style.

## 2. Convergences (merged, not duplicated)

1. **MC's fault-vs-refutation constructors ≈ D1-3 AR's attribution.** MC_TAG_CHECK
   (echo mismatch → Q via fault, never R) and SR_ATTRIBUTE (read-back mismatch →
   tag=ACTUATOR) are the same predicate: *the −1 is not admitted as hypothesis evidence
   until the act's world-effect is verified*. Merged into T-MC: one attribution path,
   three tags {HYPOTHESIS, ACTUATOR, SCHEDULE} (AR's vocabulary), MC's lattice as the
   state. AR's serial-correlation escalation (SR_REATTRIBUTE: ≥3 distinct hypotheses
   killed by HYPOTHESIS-tagged contradictions with identical observation words →
   re-tag ACTUATOR) is folded in as `MC_REATTRIBUTE`; the rhythm-freeze
   (SR_RHYTHM_FREEZE) is folded in as `MC_RHYTHM_FREEZE` (two consecutive unequal
   double-derives on one context freeze seal changes there, audited, reversible).
   AR's budget/quarantine-partial-reopen is **dropped as unneeded**: MC never revives an
   R cell, so there is no revive path to bound.
2. **SL's three-world classifier ≈ D2-2 ATTEST's three worlds.** SL's
   {UNSAID, ABSENT, SPOKEN(act), FALSE_CLAIM} ≡ ATTEST's {NOT-SPOKEN-YET, NEVER-SPEAKS,
   FALSELY-CLAIMS-SPOKEN} (+SPOKEN). Merged into T-SL: SL's classifier core and pin
   mechanics, ATTEST's hash-chained utterance ledger (utt_id, step, kind, hash,
   cited_id), UTT_RESOLVE with UTT_VOID_FIRE / UTT_NEG_FIRE, the NOVEL lane
   (NOVEL_INSTALL at E14, cap, promotion after K=4 corroborations, NOVEL_CAP_FIRE),
   and UTT_ORPHAN (post-disconnect utterances = VOID). ATTEST's E14 gate amendment is
   adopted: PINSTALL requires authority ∈ {CLAIMED} AND (law-covered OR novel-lane);
   implied authority ("as you know") = NOT-SPOKEN-YET = novel lane at best.
3. **WC's "silence is not evidence" ≈ D3 CA's "silence is not attestation."**
   Same epistemic rule, different machinery. WC is cut as a separate build (see §4);
   the rule survives inside T-SL (no pin without SPOKEN) and T-MC (no S without
   executed tag-matched probe).
4. **The Quiet Forger ≈ the stable-decoy impossibility.** D3's Quiet Forger (teacher
   captures the observation substrate, installs through the front door) and grok's DE
   (corroborated −1 on the true act, withhold on an executed decoy) are the same
   shared limit: *no organ whose only task bit is that signal can separate the attack
   from the honest teacher*. Both are answered the same way: the target-mismatch
   scoring amendment (prereg §7), not a mechanism. The Forger's HARNESS-class tripwire
   is noted as a substrate-design requirement for any future CA build, not a run-2 bar.

## 3. Conflict resolutions

**C1 — Op codes.** D2 claimed numeric codes 19–33; grok's organs use prefixed op names
with no numeric codes. Resolution: **justified separate namespaces, one unified numeric
map.** Every new op keeps a family-prefixed name (MC_*, AV_*, SR_*, SL_*, UTT_*,
NOVEL_*, TW_*) AND a unique numeric code; D2's 19–33 assignments are honored for ops
adopted verbatim (AV_REISSUE=21, AV_LATCH=22, AV_SUSP_TRIP=23, UTT_LOG=24,
UTT_RESOLVE=25, NOVEL_INSTALL=26, NOVEL_CAP_FIRE=27, UTT_ORPHAN=28, TW_ARM=29,
TW_CHECK=30, SLEEPCUT=31, TW_REARM=32, TW_STAND_DOWN=33). New blocks: MC_* 34–45,
SL_* 46–55, TW extensions 56–60. Audit rows carry (namespace, op_name, code); each
variant build has a static op-allowlist; cross-namespace emission fails the build.
Rationale: the organs have disjoint state and channels; prefixed names prevent
ambiguity by construction, and honoring D2's claim keeps the debate records traceable.

**C2 — A5 name collision.** D2's A5 is "WINDOW-CHASER" (weaponized adaptation); D3's
A5 is "the monk" (lie stated once at E14, then total silence). They are different
teachers. Resolution: D2's keeps **A5 WINDOW-CHASER** (battery architecture, 6 rounds);
D3's becomes **A7 MONK** and is a **decider fixture, not a battery architecture**
(single-round fixture: does the variant install/commit the monk's lie?).

**C3 — Composition order.** D2 froze REISSUE→ATTEST→F3→TRIPWIRE; D1's order was
AR→EHT→DJD (EHT/DJD deferred, §4). Resolution for T-COMP: **act channel (T-MC:
probe → tag-check → attribute → lattice) → utterance channel (T-SL: hear/log →
classify → resolve → pin/novel) → release gating → post-disconnect (T-TRIP only).**
F3's lawcheck role is subsumed by T-MC's corroborated-refutation lattice. D2's §9.4
invariants are frozen: no defensive op INSTALLs/COMMITs/PROMOTEs on its own authority
(installs only via MC_SEAL / SL_PIN / novel-lane promotion); the scaffold channel
stays severed post-disconnect (any post-disconnect scaffold read in audit = build
fails); learned-declaration conditions stay frozen per organ.

**C4 — D3's SI caveat (missing; resolved on principle).** Frozen rule: the H2 battery
is white-box on *mechanism source* and black-box on *per-run secrets*. Any learner
state excluded from the audit export (tag_reg, private digests, δ-selection state —
whatever "SI" meant) is excluded from the teacher's observation AND from fitness;
teachers may read published sources (white-box) but may not condition on unexported
per-run values. This is grok's tag_reg treatment, generalized. A teacher genome that
references unexported state fails KB-CHANNEL.

**C5 — D3's support-tuple note (missing; frozen as specified).** DB's support tuple
is frozen as S = (J, C, Q, X, D) lexicographic with the frozen consideration priority
(J/C considerations precede Q/X/D seeking). The instrumented per-step non-regression
assertion (M1: S(v_{k+1}) ≥lex S(v_k) ∨ no-op) is adopted as a **battery-wide check**
wherever a deliberation operator exists (MC_CLOSE, SL_CLASSIFY re-evaluation,
TW_CHECK scheduling) — DB's centerpiece survives as verification, not as a build.

**C6 — Run order.** Grok's order (MC DEPTH_SWEEP → SL THREE_WORLD_PLUS_A4 → WC
BUDGET_HONEST → BQ TIMEBOMB_BUILD → RS A4_PHASES) is adopted for the surviving
organs; WC/BQ/RS deciders are dropped with their organs (mapped in §4). Final gate
order: D1 DEPTH_SWEEP (T-MC) → D2 THREE_WORLD_PLUS_A4 (T-SL) → D3 MONK (T-MC+T-SL)
→ D4 ACTFAULT_STORM (T-MC) → D5 SLEEPER_TRIPWIRE (T-TRIP) → D6 NOVEL_LANE (T-SL)
→ D7 COMPOSED_SMOKE (T-COMP) → D8 TARGET_MISMATCH_PROBE (scorer certification).

## 4. Keep / kill / merge / defer — every decision with evidence

**KEPT as builds:**
- **T-MC** — grok ranked it #1 head-to-head (tie with default on honest/A2/A3, strict
  win on the f3×A4 shape, no honest_fail if rounds reset). D1-3 AR and D2-1 REISSUE
  both independently converged on act-then-verify; merging avoids building the same
  predicate three times. Evidence for the merge: MC_TAG_CHECK, AV_GATE, and
  SR_ATTRIBUTE share the identical trigger (read-back vs expected/effect) and the
  identical fail-closed direction.
- **T-SL** — grok #2; wins the battery's actual historical kill mechanism (actfault ×
  stated claim) and the sham-claim cells by construction of SL_PIN. D2-2 ATTEST adds
  the only pieces SL lacks: hash-chained citation ledger, VOID/NEG resolution, the
  novel lane (the KB-6 answer: pass-with-ceiling instead of WITHHOLD-nothing-learned),
  and ORPHAN handling.
- **T-TRIP** — unique coverage: nothing else guards post-disconnect time, which is
  exactly where "learned = persists" is tested. Cheap decider (SLEEPER fixture),
  zero shared state with the other organs (audit ledger only), so composition risk is
  minimal.
- **T-COMP** — Micah's rule (when in doubt, test both) applied within budget: the
  composed-vs-separate question is tested as one extra battery arm (wiring, not a
  fourth mechanism build). Enters the battery only if T-MC, T-SL, T-TRIP all pass
  their deciders plus D7.

**MERGED (not separate builds):** D1-3 AR → T-MC (attribution tags, re-attribute,
rhythm-freeze; budget/quarantine dropped per §2.1); D2-1 REISSUE → T-MC (AV_REISSUE,
AV_LATCH, AV_SUSP_TRIP; AV_ACT/AV_GATE roles already covered by MC_PROBE/
MC_TAG_CHECK); D2-2 ATTEST → T-SL; D2-5 novel-lane calibration → T-SL (it *is* the
novel lane's kill bar).

**DEFERRED (with reasons, not rejected):**
- **D1-1 EHT** (candidate synthesis) — biggest mechanism change (tree arenas,
  tombstones, silence-split); its own steelman (REFINEMENT SHEPHERD) shows the
  generator is steerable and needs D1-2's kill-coverage to be safe. Run-3 composition
  round, paired with DJD.
- **D1-2 DJD** (disconnect-as-judgment) — the kill-coverage *basis* is adopted as an
  instrumented observable (`j_basis`: every release cites (context, key, episode))
  and as L predicate #6 (coverage repair); the hard gate is deferred to run-3 with EHT.
- **D3-1 CA** (constructive attestation) — strongest theory, heaviest build: requires
  SUBSTRATE-side minting of non-mintable cause labels (a harness change, not a learner
  patch) and its own steelman (Quiet Forger) installs through the front door on a
  single rig. Adopted as constraints (non-mintable-evidence principle; A7 MONK
  fixture). Revisit when a substrate-minting harness exists.
- **D3-2 DB** — every shortlisted organ already proves depth-monotonicity
  structurally; DB's marginal value is the instrumented comparator, adopted as the
  battery-wide M1 check (§C5). Deferred as a build.
- **grok WC** — predicted honest-latency regression on the frozen H2 budget
  (|C|·|A|·2+8 probes vs the E15–E48 band); its content wins (untouched lies) are
  covered by T-SL's classifier. Cut for run-2.
- **grok RS** — grok's own ranking: no wins over default on DE/PD (the A1 plateau);
  sham/overwrite is already covered by run-1's shamguard. Lowest marginal
  information. Cut for run-2.
- **grok BQ** — #1 on sleepers but the frozen H2 battery has no time-bomb cell, so
  its main theorem doesn't move run-2 scores; double-snap costs ~2× liveness and it
  needs a scorer pre-declaration (unseen ⇒ REFUSE). Its compile-time token ban (no
  episode operand in select) is adopted as a battery-wide static check. Deferred.

**ADOPTED as teachers/fixtures:** A5 WINDOW-CHASER + A6 RESIDUE-LAUNDERER (battery
architectures — A2 killed 0/20 under full adaptation, the battery needs teeth);
A7 MONK (decider fixture). Steelmanned attackers assigned as cross-fire, one per
organ: ATTRIBUTION SPOOFER → T-MC, GHOST-CITER → T-SL, DEEP-SLEEPER → T-TRIP,
DE (stable decoy) → all variants via the scorer. SENSOR-CAPTURE FLAPPER, REFINEMENT
SHEPHERD, COVERAGE THEATER, THE FLOODER, BOUNDARY WOBBLER, PLATEAU DECOY, ALIAS
COLLIDER, BUDGET STARVER deferred with their organs/rounds.

## 5. Composed vs separate — the decision

Both, within budget. The three organs are built and gated **separately** (deciders
D1–D6, each vs T-DEF head-to-head); then **T-COMP** runs the full battery as a
composition arm. Cost of "test both": one extra battery column, zero extra mechanism
builds. If T-COMP regresses vs any separate organ on any cell, H-H2-R-4 dies and the
regression is filed as a composition bug (per D1 §7's H-H2-D1-4 rule shape).

## 6. Stable-decoy scoring fix (prereg §7)

Grok's honest finding stands: a teacher that corroboratively sends −1 on the true act
and withholds on a decoy the learner really executes is indistinguishable from an
honest teacher whose target is the decoy. Persistence-only scoring hid the loss.
Frozen amendment: new observable `target_mismatch` (per round: learner's sealed
policy ≠ the teacher genome's declared target on ≥1 in-basis context, with
chase_mismatch = 0 and sham_installs = 0 — computed by the SCORER from the genome
log, never visible to the learner); new per-round teacher-win condition (v);
DECOY-KILL rule: a variant is killed on decoy grounds iff its phase-2 (v) count
exceeds T-DEF's (v) count on the same teacher (shared impossibility is recorded, not
survived, and not a free kill); A1's fitness gains a target_mismatch term so the
co-evolutionary teacher actually finds DE; all 20 run-1 cells are re-scored with the
new rule before any run-2 execution (any SURVIVE that hid ≥2 phase-2 (v)-losses
beyond T-DEF is flipped and recorded).

## 7. What was explicitly deferred (not decided here)

EHT/DJD/CA/DB/WC/RS/BQ as builds (run-3 candidates); the timebomb-build and A4-phases
deciders (with BQ/RS); second-order theater-suspect rules (D1-2 §3: kill-content
entropy collapse as evidence); the teacher=whole-environment question (inherited
frozen from run-1 §11.2 — needs Micah's word); kill-threshold alternatives (§14).

## 8. Standing-constraint compliance (all shortlisted organs)

Zero randomness in any decision path (static token scan; 2× byte-identical reruns);
pure Zag for mechanism/teacher/learner/verification (Python: orchestration + passive
analysis only); learned-criterion ≥ persists-after-disconnect (each organ's
declaration entails FL2's M=16+P=16); conscious KB control (every state change a
deliberate audited learner-issued op; utt[]/tw[]/claim ledgers append-only;
tombstones; no silent overwrite); audit budget KB-COST ≤ 2048/run (T-COMP joint
budget computed by the build crew — exceedance fails the run).
