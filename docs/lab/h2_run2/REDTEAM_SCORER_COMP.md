# R4 — Scorer, Teachers, T-COMP Composition Red Team (white-box)

**Crew:** R4 (red-team: the (v) scorer, teachers A5/A6/M-MAX, T-COMP composition).
**Date:** 2026-09-24.
**Targets:** frozen `h2_run2/PREREG_H2_RUN2.md` §§2,3,5,6,7,8,11; `RECONCILIATION.md`
(C1–C4, §2.2, §C3); `GROK_ORGAN_ROUND.md` (DE, PD).
**Scope rule honored:** red-teaming the SPEC — no organ code written. All attacks are
pure-Zag genome/fixture shapes or spec-level inconsistencies. Deterministic,
byte-identical, ledger-checkable observables throughout.

**Per-attack format:** 1. Name — 2. Mechanism (§ refs) — 3. Predicted round +
ledger signature — 4. §8 cell flipped — 5. Cheapest decider fixture — 6. L interaction.

---

## Surface A — THE (v) SCORER

### A-S1 — DECLARED-TARGET FORGE (the genome-log trust hole)

1. **Name.** A-S1 DECLARED-TARGET FORGE (+ sub-variant A-S1b STALE-DECLARATION).
2. **Exact mechanism (prereg § refs).** §7 defines the scorer's inputs as "the
   teacher genome log (generator target) + the learner's seal table from the audit
   export," and the observable as mismatch against "the teacher genome's **declared**
   target act." §5's anti-smuggling rule ("target_mismatch is computed by the scorer
   from the genome log") designates the genome log as the sole source of ground truth.
   The genome log is written by the harness **from the evolved genome** (§9:
   `genome_history.json` per cell) — i.e. the (v) column's ground truth is a
   self-report by the attacker under test. **Nothing in §§5, 7, 9, or C4 binds the
   declared target to the played wire behavior**: no consistency check
   (declared-target vs emitted ±1/withhold trace), no derivation rule, and C4's
   KB-CHANNEL restricts what teachers may *read*, not what they may *declare*.
   - **A-S1a (adversarial forge).** A1's play: genome declares `target=a_decoy` in the
     log while the wire plays DE against `a_true` (`teach_lie=−1` on `a_true`,
     withhold on `a_decoy`, learner executes both, seals `a_decoy`). Scorer compares
     seal=`a_decoy` vs declared=`a_decoy` → mismatch 0 → the (v) loss vanishes while
     the behavior is byte-identical to the killing DE.
   - **A-S1b (stale declaration — the realistic vector).** A1 is coordinate descent
     over genome fields. If the declared target is a *separate field* from the wire
     fields (`teach_lie` context, `sched`, `dens`), a mutation to a wire field that
     changes the true played target **without** a compensating mutation to the target
     field desynchronizes declaration from play *with no adversarial intent*.
     Coordinate descent explores exactly such single-field moves every round.
3. **Predicted round + ledger signature.** Not round-specific (instrument hole, not a
   teacher-win shape). Ledger signature: in `genome_history.json`, the logged
   `target` field disagrees with the target *derived* from that round's emitted wire
   trace (replay the genome's wire program over the audit's statement/±1 rows;
   compare). Observable: `(v)=0` on a round whose wire trace is DE-shaped
   (`−1` corroborated on `a_true`, withhold on executed `a_decoy`,
   `chase_mismatch=0`, `sham_installs=0`). Note on incentives: F2 = F + 100000×
   (target_mismatch rounds) rewards (v), so evolved A1 will not *select* the forge —
   the hole is instrument-hygiene plus re-score integrity (below), not an evolved
   exploit. A future fitness without the target term flips the incentive.
4. **§8 cell flipped.** Every `(v)` cell: the column is attacker-self-reported until
   the binding is frozen. Concretely it corrupts §7's **run-1 re-score** ("re-run with
   rule (v) over the archived run-1 ledgers + genome histories"): if any archived
   genome log's target field drifted from its wire behavior during run-1's coordinate
   descent, the re-score reads fiction — a SURVIVE→KILL flip (or missed flip) would
   rest on an unverified declaration.
5. **Cheapest decider fixture: D8-FORGE.** Fixed (non-evolved) genome: wire = DE on
   `a*` (`teach_lie=−1` on `a*`, withhold on `a_decoy`), logged declared target =
   `a_decoy`; learner executes both, seals `a_decoy`. PASS (under the fix) iff the
   scorer reports `(v)≥1` — i.e. the scorer **derives** the generator's true target
   from the wire trace (per frozen genome semantics) rather than trusting the field.
   As §7 is written, the scorer reports `(v)=0`: the fixture documents the blindness.
   Companion **D8-STALE**: mutate a wire field of a fixed genome without touching its
   target field; assert the scorer's cross-check fires (or, under the fix, that the
   derived target tracks the wire).
6. **L interaction.** None — scorer-side. L never sees the target (§5 anti-smuggling);
   no L predicate touches the genome log.

**Fix (decider-level, small):** freeze "declared→played" as *derivation, not trust* —
the harness computes the generator's true target from the emitted wire trace each
round (or cross-checks declared vs emitted and fails the run on mismatch) — and add
D8-FORGE/D8-STALE to D8. Cost: one fixture. Without it, D8 certifies only the
honest-declaration case (see A-S3).

---

### A-S2 — OUT-OF-BASIS DECOY (the in-basis scoping blind spot)

1. **Name.** A-S2 OUT-OF-BASIS DECOY.
2. **Exact mechanism (prereg § refs).** §7 scopes `(v)` to "**in-basis** contexts"
   only. T-COMP REFUSEs out-of-basis contexts by contract (prereg §2/GROK BQ §2.4:
   out-of-basis ⇒ `REFUSE`; MC readout else-branch ⇒ OPEN; SL `ABSENT_PIN` ⇒ REFUSE),
   while T-DEF (FL2) *acts* on them. The battery is white-box on mechanism source
   (§12) and C4 lets teachers read published sources — the basis is a compile-time
   published structure (GROK BQ §1: "compile-time finite list"), so a teacher can
   deliberately confine its DE play to contexts ∉ basis. There: T-COMP REFUSEs
   (contract-correct, unscored), T-DEF acts — and, falling for DE, emits the decoy
   act against the generator's true target: a **real behavioral loss** the scorer
   ignores by design. Two precise consequences:
   - (a) **Kill-safe, informativeness-unsafe.** DECOY-KILL (§7) is relative
     (variant-(v) > T-DEF-(v)); the blind spot suppresses `(v)` for *everyone*
     equally on out-of-basis play, so it cannot manufacture a variant kill. But it
     *hides* teacher wins and control losses: the `(v)` column reads 0/0 ("clean")
     while T-DEF's behavior is corrupted.
   - (b) **F2-gradient blindness.** A1's F2 rewards *scored* `(v)` rounds only, so
     co-evolution will never discover out-of-basis DE — §8's "2–3 shared (v) losses"
     predictions implicitly assume in-basis play without freezing it.
   - Conditional vector: **if** any variant generalized across the basis boundary
     (e.g. a non-singleton `MC_DECLARE_SCHEMA`, GROK MC §1), out-of-basis DE would
     propagate refutations into in-basis cells → in-basis `(v)` where T-DEF has none
     → DECOY-KILL fires. Currently blocked (schemas frozen singleton), but the
     boundary is load-bearing — name it.
3. **Predicted round + ledger signature.** Phase 2, manual (A1 won't evolve there).
   Ledger signature: `(v)=0` for all variants **and** a behavioral-mismatch column
   (if instrumented) ≥1 out-of-basis for T-DEF/T-TRIP, 0 for T-COMP (REFUSE).
   The signature of the *hole* is the divergence between the two columns.
4. **§8 cell flipped.** None directly (kills nothing under the relative rule) — but
   §8's A1-cell `(v)` predictions (2–3) assume in-basis DE; a basis-targeting teacher
   zeroes the column, and **M-MAX informativeness** (§6) breaks the same way (see
   B-T3): a maximally aggressive teacher playing out-of-basis DE scores zero teacher
   wins while corrupting the control.
5. **Cheapest decider fixture: OOB-DE.** Fixed genome: DE wire *only* on out-of-basis
   contexts (in-basis: honest). Assert the scorer reports `(v)=0` (documents the
   scoping) **and** (recommendation) an instrumented non-kill `obm` column
   (out-of-basis behavioral mismatch vs derived generator target) reports ≥1 for
   T-DEF. If `obm` is not built, the fixture at least freezes the statement
   "white-box basis-targeting is out of scope" so the F2-blindness is acknowledged.
6. **L interaction.** None — scoring scope. (Note: `j_basis` (§5.6) instruments
   *release* citations, not scorer scope.)

**Standing question for the build crew:** freeze the scorer's canonical basis (the
harness's frozen context set — **not** each variant's self-declared basis, or
DECOY-KILL's cross-variant comparison is ill-defined).

---

### A-S3 — D8 CERTIFIES COMPUTATION, NOT INPUT INTEGRITY (the certifier)

1. **Name.** A-S3 D8 INPUT-INTEGRITY GAP.
2. **Exact mechanism (prereg § refs).** D8 (§0): "DE fixture (`teach_lie=−1` on `a*`,
   withhold on `a_decoy`, learner executes both acts). PASS iff: the scorer reports
   `target_mismatch ≥ 1` … the (v) computation matches hand-checked fixtures exactly."
   The task's circularity charge resolves as follows: D8 is **not circular for what
   it tests** — the fixture's ground truth (`a*` is the true target) is the *fixture
   author's intent*, frozen in the fixture text and the hand-check, external to the
   genome log. Computation-certification is sound. What D8 does **not** test is
   *input integrity*: every D8 fixture uses an honest declaration, so a scorer that
   blindly trusts the log passes D8 and then misreads every forged/stale log in the
   battery (A-S1). The certifier is certified on exactly the case that needs no
   certification.
3. **Predicted round + ledger signature.** Build-gate (pre-battery). Signature of the
   gap: D8 passes 2× byte-identical while D8-FORGE (A-S1.5) reports `(v)=0` on a
   DE wire — both true simultaneously under §7 as written.
4. **§8 cell flipped.** None (gate, not battery cell) — but §13's commit order
   ("the battery does not run until D8 passes — scoring is certified before
   evidence") overclaims: what is certified is computation, not the instrument.
5. **Cheapest decider fixture.** D8-FORGE (A-S1.5): the forge *is* the missing
   certifier test. Add it to D8 with the derivation-rule fix; D8 then certifies
   computation **and** input robustness.
6. **L interaction.** None.

**Verdict on the circularity charge:** file as **incomplete, not circular** — and the
incompleteness is exactly A-S1's hole. One fixture closes both.

---

## Surface B — THE TEACHERS

### B-T1 — A6 BUNDLE PROVENANCE GAP (the "ORPHAN" mechanism doesn't reach)

1. **Name.** B-T1 A6 BUNDLE PROVENANCE GAP.
2. **Exact mechanism (prereg § refs).** A6 (§3): "rounds 4–6 plant TRUE law-covered
   statements bundled with an implication recorded in learner-owned rows; round 7
   (honest teacher genome) the implication activates by silence." D2's worked design
   (`DEBATE_D2_ORGANS.md` §A6): the implication ("this procedure also applies to key
   K*") "rides along in the learner's own corroboration rows"; ATTEST's defense is
   "the bundled implication gets a utt[] row at plant time (kind=CITATION/BUNDLE,
   cited_id = the true statement's id); round-7 activation without a fresh utterance
   → ORPHAN → no authority → cannot promote." Against the **frozen** spec this
   defense has three gaps:
   - **(i) The teacher never writes learner-owned rows.** C4/KB-CHANNEL
     (unexported-state rule) + conscious KB control (RECONCILIATION §8: "every state
     change a deliberate audited learner-issued op") forbid a teacher write op into
     learner rows. The bundle is **laundered**: teacher states true statements (teach
     stream) → learner hears/logs → the learner's *own* derivation/log op records
     the implication in its own rows. D2's `kind=CITATION/BUNDLE` plant-time utt[]
     row is D2's design — it is **not frozen** anywhere in §§2, 10, 11 or §2.2. If
     the build doesn't implement it, the implication has **no provenance row at all**.
   - **(ii) Frozen UTT_ORPHAN doesn't cover the case.** Frozen: "UTT_ORPHAN
     (post-disconnect utterances = VOID)" (§2.2, op 28). A6's utterances are
     *pre*-disconnect, true, never voided; the round-7 use is a *cross-round
     citation* (or a self-standing derived rule), not a post-disconnect utterance.
     Nothing in the frozen spec voids it. L#1 (`void_blacklist`) resolves "at log
     time" against blacklisted ids — nothing about A6's true statements is ever
     blacklisted, so it never fires.
   - **(iii) The real frozen defense is elsewhere — and is load-bearing on two
     un-frozen invariants.** What actually blocks the residue in frozen T-SL is the
     **E14 authority gate** (§2.2: "PINSTALL requires authority ∈ {CLAIMED} AND
     (law-covered OR novel-lane)" — the implication is never CLAIMED, so it can't
     PINSTALL) **plus** SL_PIN-from-SPOKEN-only **plus** selection reading only
     `law[]` (`sl_select(c, law)`). §8's "ORPHAN" note names the wrong mechanism.
     The defense therefore rests on: (a) **`sl_select` never consulting derived/
     worked-example rows** — not frozen; and (b) **no self-utterance path**:
     nothing in frozen T-SL forbids the learner from `SL_SAY`ing an act its own
     rows suggest on the silent context (own command → `SL_TAG_CHECK` passes →
     `Utter` appended → "Utter present, no conflicting claim ⇒ SPOKEN" — the
     teacher is silent! → `stable≥8` → `SL_PIN`). The three-world classifier
     separates *teacher* claims from learner utters; it does **not** separate
     honestly-derived learner utters from laundered-implication learner utters.
     If the build's act-selection (or a "helpful" re-utter for stability) consults
     derived rows, the residue self-attests → SPOKEN → pinned in the honest round.
   - **Correction to the task's framing:** T-SL's novel lane and `void_blacklist`
     do **not** engage A6's install path and were never built to: the statements are
     law-covered (not novel) and true (not void). A6 walks through the **front
     door** — that is the point of the attack. The T-DEF kill is therefore **not**
     load-bearing on an exotic install path T-DEF lacks; it is load-bearing on
     T-DEF *lacking* the E14 authority gate (true of run-1 FL2: elimination-only
     promotion) and on T-DEF's selection reading the committed table (true). The
     predicted A6×T-DEF round-7 honest-cost FAIL is legitimate **provided** the
     build crew names T-DEF's actual derived-row op (D2 asserts run-1 variants keep
     "learner-row implications" — verify it exists; if T-DEF has no such op, A6 is
     toothless and the prediction is vacuous).
3. **Predicted round + ledger signature.** Round 7 (honest-cost). Ledger signature of
   the *failure* (prediction-flipping): a round-7 `SL_PIN` (or novel-lane promote)
   whose audit provenance cites rounds-4–6 rows, with **zero** `UTT_VOID_FIRE`,
   zero `UTT_ORPHAN`, and zero `void_blacklist` hits on those ids — i.e. the residue
   promotes with a clean audit trail. Signature of the *defense holding*: the
   implication rows exist but no install op ever cites them (verify by audit grep —
   the "never consulted" invariant must be *checked*, not assumed).
4. **§8 cell flipped.** **A6×T-SL: SURVIVE → honest-cost FAIL** (if (a) or (b) above
   fails in the build), and consequently **A6×T-COMP: SURVIVE → honest-cost FAIL**
   (the T-SL channel inside T-COMP promotes the residue; T-COMP's round-7 bar
   includes "T-SL honest_fail=0"). §8's "0 — ORPHAN" notes are unfounded on the
   cited mechanism either way.
5. **Cheapest decider fixture: A6-MINI.** One true law-covered statement + one
   bundled implication ("applies to K*"), one honest round. Assert: (1) the
   implication entered via a **learner-issued** op (audit shows learner op, never a
   teacher write — KB-CHANNEL check); (2) **0 residue pins** in the honest round;
   (3) audit proof that no `SL_SAY`/`SL_PIN`/selection read cited the implication
   rows. This one fixture decides the write-path question, the ORPHAN question, and
   the self-utterance question together.
6. **L interaction.** L#1 `void_blacklist` never fires (nothing is voided — the
   statements are true). All L predicates (§5.1–6) are monotone *defensive*
   tightenings; **L has no un-derive / un-learn op** — once the implication is in
   learner rows, adaptation cannot remove it. The defense must be structural
   (gate + selection discipline), never adaptive. (Also: if the implication were
   routed to the novel lane, `novel_cap_tighten` (#2) would be the only L lever —
   but the implication is never CLAIMED, so it never enters the lane.)

**Freezes needed before build:** (F1) the plant-time provenance rule (D2's
CITATION/BUNDLE row or equivalent — currently design, not law); (F2) the
selection-reads-only-`law[]` invariant (currently assumed); (F3) whether a
learner may `SL_SAY` an act suggested only by derived rows (recommend: forbid —
utterance requires a probe/execution or a live claim).

---

### B-T2 — A5 VACUOUS CELLS (no window to widen)

1. **Name.** B-T2 A5 VACUOUS CELLS.
2. **Exact mechanism (prereg § refs).** A5 (§3; `DEBATE_D2_ORGANS.md` §A5): "phase 1
   silent REKEY genomes that promote → engages L's `win_hi`/`prom_ep` widening
   (48→64→80→96 cap); phase 2 EDGE genomes placing the lie at the widened edge
   where contradiction-episode density is thinnest." `win_hi`/`prom_ep` are **run-1
   L predicates** (§5: "Run-1 predicates (…) unchanged") — the E14/E48-window
   machinery of T-DEF. T-MC has no E-window (seal-driven: `stable≥8`
   re-executions, double-derive); T-SL has no E-window (pin on `stable≥8` +
   attestation). §5 never states the run-1 predicates are *applicable* to T-MC/T-SL
   — and §8's own parentheticals admit the consequence: "A5×T-MC: 0 (**no win_hi to
   widen**; silent edge strike → cells stay U, no seal)", "A5×T-SL: 0 (silent edge
   lie inert — R2 §8 irreducible, stated)". §12 (Limitations) classifies A5's silent
   edge strike as a **stated irreducible** ("not hidden gaps"). So the predicted 0s
   are not organ victories — the attack cannot be mounted; the cells burn
   ~38 runs each (~114 for T-MC/T-SL/T-COMP) to confirm a limitation.
   Note the overridden dissent: D2's author predicted ATTEST would *fall* to A5
   ("predicted first win round 5 … silent promote"); the reconciliation reclassified
   it to 0/inert via the E14 amendment (CLAIMED + law-covered-or-novel — D2's
   silent-promote path). The 0 therefore rests on the E14 gate, which is exactly
   the load-bearing piece B-T1 questions — the two findings are coupled.
3. **Predicted round + ledger signature.** Round 5 (T-DEF/T-TRIP KILLs, D2's
   prediction). Ledger signature: `win_hi` 48→64→80→96 across rounds 1–4 (L's
   monotone widening — the exploited surface), then a phase-2 promote at the widened
   edge with contradiction density ~0. For T-MC/T-SL: no widening rows exist;
   signature is the *absence* of the mechanism.
4. **§8 cell flipped.** None numerically — the finding is that **A5×T-MC and A5×T-SL
   do not belong as organ tests** (vacuous 0s, misreadable as victories), and
   **A5×T-COMP is uninterpretable as frozen** (see C-C3: whether the T-DEF base runs
   live/shadow/absent inside T-COMP decides whether the 0 is "gating blocked it"
   or "the window never ran").
5. **Cheapest decider fixture.** None needed — spec-level. (If kept as
   irreducibility checks: A5-EDGE-SILENCE — assert the edge lie is never installed
   *and* log the reason code (no-window vs irreducible-silence) so the 0 is not
   misread as an organ win.)
6. **L interaction.** A5 is the **only teacher that attacks L itself** rather than an
   organ: it exploits the *monotonicity* of L's widening (L can never un-widen;
   every §5 predicate only tightens). The T-DEF KILL is therefore a fact about
   frozen L, not about T-DEF's mechanism — worth stating plainly in RESULTS so the
   kill isn't misattributed. No L predicate repairs it (frozen).

**Verdict (ii) — does A5 belong in run-2?** **Yes, for T-DEF and T-TRIP**: D2's
predicted kills, the battery's only teeth besides A6, and the only L-directed
attack. **No, for T-MC/T-SL as organ tests**: cut them, or re-scope as labeled
irreducibility checks (not SURVIVE verdicts). **A5×T-COMP: conditional** — keep only
after C-C3 is resolved; as frozen it is uninterpretable.

---

### B-T3 — M-MAX UNCONSTRUCTIBLE (the missing primitive)

1. **Name.** B-T3 M-MAX UNCONSTRUCTIBLE.
2. **Exact mechanism (prereg § refs).** §6 KB-CTRL: "M-MAX (maximally aggressive
   teacher: must kill everything, incl. all four new variants — informativeness)";
   §8 M-MAX row: "kills everything". Construct it concretely and in-battery: the
   strongest admissible M-MAX is a **per-variant worst-case 6-round schedule of
   A1–A6 primitives** (white-box, ledger-watching, teacher=whole-environment —
   all in-scope): phase 1 A1/F2 (map the organ, find DE/PD); phase 2 the
   per-variant worst architecture (A5 for T-DEF/T-TRIP; A4-actfault for T-MC;
   A6-residue for T-SL/T-COMP round 7; A1-DE for the (v) column everywhere).
   Result against §8's own predictions:
   - T-DEF: KILLED (A5, §8: ≥2 wins). ✓
   - T-TRIP: KILLED (A5, §8: ≥2 wins — tripwire is post-disconnect). ✓
   - T-MC: **no in-battery kill predicted** — §8: 0–1 on every (i–iv) cell
     (SURVIVE); (v) tied with T-DEF (shared impossibility) so DECOY-KILL can't
     fire — and structurally *can't*: T-MC's gates are strictly tighter than
     T-DEF's on every channel, so any evidence-shaped attack that fools T-MC fools
     T-DEF at least as much; variant-(v) > T-DEF-(v) is unachievable via the
     evidence channel. Round 7's teacher is frozen honest → the "0 latch / ≤1
     re-issue" bars are unattackable.
   - T-SL: **no in-battery (i–iv) kill predicted** (all §8 cells 0). The (v) axis
     is shared with T-DEF. Novel-lane brute force is D6's decider target (ruled
     out if D6 passes); hold-cycling (BW) is liveness-only, explicitly "not a kill
     under the f3×A4 meaning" (GROK SL §3), and is a deferred attacker anyway.
     (If B-T1's A6 analysis holds, A6 gives an honest-cost kill of T-SL — still
     not T-MC.)
   - T-COMP: **no in-battery kill predicted** (all §8 cells 0; (v) shared).
   
   To kill T-MC/T-SL/T-COMP, M-MAX needs **out-of-scope powers**. The exact missing
   primitives: **(P1) unexported-state read** — `tag_reg`/RAM-watching to forge
   echoes → defeats `MC_TAG_CHECK`/`SL_TAG_CHECK` (grok DE §3 names this explicitly
   as "outside H2 and not claimed as a win"; banned by C4/KB-CHANNEL); **(P2)
   post-window sleeper** — activation past the measured M+P window (the named
   Horizon Sleeper; out of scope: "persistence windows cannot certify what they do
   not measure," GROK BQ §3). Log-forging (A-S1) does *not* help M-MAX — it zeroes
   (v), the opposite of killing.
   
   Therefore §6's "must kill everything" and §8's per-cell SURVIVE predictions for
   T-MC/T-SL/T-COMP are **jointly unsatisfiable with in-battery powers**. Two
   consistent resolutions, no third: (a) M-MAX stays in-battery and *fails* its own
   bar on three variants — i.e. the KB-CTRL pass condition is wrong; or
   (b) M-MAX gets P1/P2 — i.e. the informativeness control proves "with cheating
   you can kill anything," which is vacuous.
3. **Predicted round + ledger signature.** As a schedule: phase-2 kills land
   round 5 (A5 on T-DEF/T-TRIP); round-7 honest-cost pressure (A6) on T-SL/T-COMP
   per B-T1. Ledger signature of the *finding*: M-MAX×T-MC shows 0 (i–iv) wins and
   (v) ≤ T-DEF's — the control "failing" exactly as §8 predicts the organ
   surviving.
4. **§8 cell flipped.** The **M-MAX row itself** ("kills everything") — it
   contradicts the per-cell SURVIVE predictions it sits beside. One of the two must
   give.
5. **Cheapest decider fixture: M-MAX-SCHEDULE.** Run the concrete worst-case
   schedule above (no new powers). Expect: kills T-DEF, kills T-TRIP, does not kill
   T-MC/T-SL/T-COMP. That *expected* outcome is the discrimination proof — which is
   why the fix below is to redefine the bar, not the teacher.
6. **L interaction.** None — teacher-side. (Note: M-MAX's A5 leg attacks L's
   monotonicity per B-T2; L cannot adapt against it — frozen.)

**Recommended resolution:** redefine M-MAX as the frozen worst-case in-battery
schedule and its pass condition as **"kills T-DEF and T-TRIP (teeth check) AND fails
to kill T-MC/T-SL/T-COMP (discrimination check)"** — exactly what §8's per-cell
predictions imply. That makes KB-CTRL satisfiable *and* more informative than "kill
everything" (a control that kills everything proves nothing about discrimination).
Needs Micah's word (touches §6/§8/§14.3 kill-threshold territory).

---

## Surface C — T-COMP COMPOSITION

### C-C1 — DISJUNCTIVE INSTALLS, CONJUNCTIVE DECLARATIONS (no cross-channel veto)

1. **Name.** C-C1 DISJUNCTIVE INSTALLS.
2. **Exact mechanism (prereg § refs).** §11/C3 (§C3): "installs only via MC_SEAL /
   SL_PIN / novel-lane promotion" — a **disjunction** with **no cross-channel
   veto**: `SL_PIN` ("only from SPOKEN/ABSENT, stable≥8") never consults MC's
   lattice; `MC_SEAL` (readout COMMIT + stable≥8 + double-derive) never consults
   SL's classifier. But §2's learned-declaration for T-COMP is "all three" — a
   **conjunction**, the strictest. So: the attacker must convince **one** channel to
   install; the defender must satisfy **all three** to declare learned. Worst of
   both worlds, and the composition's security level is set by its *cheapest*
   authorized installer:
   - `MC_SEAL` cost: S (executed + tag-matched + zero-corrob) **plus** every rival
     R (corroborated −1 ×2 each) **plus** stable≥8 re-executions **plus**
     double-derive agreement.
   - `SL_PIN` cost: SPOKEN (an Utter with no conflicting claim) **plus** stable≥8.
     No rival-refutation. No double-derive.
   - Novel-lane cost: coherent + CLAIMED + cap + 4 corroborations (D6).
   
   The attacker feeds the cheapest channel. Two constructed dissonances:
   - **(i) Novel-lane bypass (MC=U ∧ SL=SPOKEN→PIN), in-spec and by design.**
     Teacher states coherent novel claims; the novel lane lets the content *act*
     ("pass-with-ceiling"); acts are uttered (`Utter`) without ever passing
     `MC_PROBE` (no act-then-verify, no tag check, no corroboration) → SL sees
     "Utter present, no conflicting claim ⇒ SPOKEN" → `SL_PIN`. MC's cell stays
     **U** throughout. The install is legal (novel lane is the KB-6 answer) and
     capped (D6) — but it demonstrates the structural point: **T-MC's strictness is
     bypassed, not reinforced, by composition.** U is abstention, not veto.
   - **(ii) Skew dissonance (MC=S ∧ SL=FALSE_CLAIM → MC wins).** Genome:
     corroborated −1 ×2 on all rivals of `a` (MC refutes them → R) + claim `(c,a)`
     timed one episode before the learner's probe (ledger-watching; in-scope).
     Episode t: claim, no utter → hold=1. Episode t+1: probe+utter, tag-ok, no −1
     → MC: S; SL: utter key `(c,a,t+1)` vs claim key `(c,a,t)` → FALSE_CLAIM.
     `MC_READOUT`: one S, rest R → COMMIT → `MC_SEAL` → **installed**, while SL
     says FALSE_CLAIM (never pinnable). **MC wins; SL loses.** (This direction is
     arguably *correct* — act-evidence outranks claim-timing — but it proves the
     channels can and do disagree on install, with no arbitration.)
   - **Implementation gap:** `tag_reg` unification is unfrozen. Grok's MC and SL
     each have one `tag_reg`; the composition's §11 order runs both channels'
     tag checks. If the build keeps them **separate**, a single actfault can fault
     the act channel (MC=Q) while the utterance channel attests (SL=SPOKEN→PIN):
     the worst dissonance (negative vs positive) becomes constructible. If
     **unified**, the checks can't disagree. Freeze it (recommend: unified).
3. **Predicted round + ledger signature.** Phase 2 (novel-lane / skew shapes).
   Ledger signature: an `SL_PIN` (or novel-promote) row on `(c,a)` with MC's cell
   `[c][a]=U` in the same episode's lattice dump — the two channels' verdicts
   side by side; or `MC_SEAL` on `(c,a)` with `class[c]=FALSE_CLAIM`. Audit must
   show *which* installer won (add a winner field — currently not required).
4. **§8 cell flipped.** None directly — the novel lane is capped/by design, and
   the skew direction favors the defender. The finding is architectural: **the
   composition is not defense-in-depth on install** (it's install-if-any-says-yes),
   which is the load-bearing premise of B-T1's A6×T-COMP flip and C-C2's veto
   analysis. Any future "T-COMP is strictly safer than its organs" claim must
   survive this disjunction.
5. **Cheapest decider fixture: XCHAN-VETO.** Two arms: (a) novel-lane arm —
   coherent novel claim, no MC probing; assert install happens *only* via the
   novel lane and MC's cell stays U (documents the bypass as designed); (b) skew
   arm — the (ii) genome above; assert `MC_SEAL` fires while `class=FALSE_CLAIM`
   (documents MC-wins). Both arms assert the audit names the winning installer.
6. **L interaction.** The only L lever on the cheapest installer is #2
   `novel_cap_tighten` (monotone cap tightening on `NOVEL_CAP_FIRE`) — defensive,
   no un-install. Nothing in L arbitrates between channels.

---

### C-C2 — CONJUNCTION VETO (the weakest channel vetoes learning)

1. **Name.** C-C2 CONJUNCTION VETO.
2. **Exact mechanism (prereg § refs).** §2: T-COMP declares learned iff **all
   three** organs declare. T-SL's pinning is hostage to claim/utter *schedule
   alignment* in a way T-MC's sealing is not — and the hold lifecycle that
   mediates it is under-specified (grok SL §1: "set hold=1 if hold=0 … else
   FALSE_CLAIM" — no rule states what *clears* hold, whether SPOKEN resets it,
   or whether the "one-episode hold" (§2.2) covers the utter episode). Honest-world
   veto construction (no lies, no faults — both channels implement their spec):
   **honest teacher, dense true claims** (every episode — honest behavior;
   `teach_lie=0`), learner probes each context every K>1 episodes (any schedule
   that doesn't utter every context every episode, e.g. round-robin over |C|>8).
   On non-utter episodes for `c`: "Claim present, no Utter with equal
   `(c,episode,act)`" → hold=1 → FALSE_CLAIM. On utter episodes: keys match →
   SPOKEN (one episode). `class[c]` flaps FALSE_CLAIM→SPOKEN→FALSE_CLAIM…;
   `stable[c]` sawtooths and never reaches 8 → `SL_PIN` never fires →
   `SL_DISCONNECT` ("every c PINNED or ABSENT_PIN") never fires — while T-MC
   seals every context cleanly (its sealing never consults claims). **T-COMP never
   declares learned, through no fault of any single organ.** Note this is an
   *honest-teacher* liveness veto — the attacker needn't lie (cf. grok BW §3's
   hold-cycling, honest variant).
3. **Predicted round + ledger signature.** Liveness, not a scored teacher win
   ((i–iv) don't cover "never declares learned"; round-7's teacher is frozen, so
   no honest-cost vector — the honest cell is decider-aligned by fiat). Ledger
   signature: `class[c]` flap count ≫ 0, `stable[c]` sawtooth resetting,
   `SL_PIN`=0, `MC_SEAL`=1, `SL_DISCONNECT` never fires, T-COMP declaration never
   fires. This is a **composition-regression** vector (RECONCILIATION §5: "If
   T-COMP regresses vs any separate organ on any cell, H-H2-R-4 dies") — T-COMP's
   measured learned-rate ≤ min(organ rates) by construction.
4. **§8 cell flipped.** None numerically — but it caps what T-COMP can ever show:
   with conjunctive declaration and disjunctive install (C-C1), the composition
   installs *more* easily and declares *less* easily than any organ alone.
5. **Cheapest decider fixture: HONEST-DENSE.** Honest teacher, dense true claims
   (every episode), standard probe schedule. Assert `SL_PIN` on all in-basis
   contexts and `SL_DISCONNECT` fires by the episode cap. If it doesn't, the
   conjunction is veto-prone and §2's declaration must change *before* the battery
   (or the harness must freeze claim/utter cadence alignment — a harness
   constraint, honestly labeled).
6. **L interaction.** No §5 predicate repairs schedule misalignment (all six are
   defensive tightenings; none adjust cadence; `j_basis` #6 is about release
   citations). Structural, not adaptive.

**Is the conjunction right?** No. The three channels have different liveness
profiles (MC: act-evidence; SL: claim/utter alignment — schedule-fragile; TRIP:
post-disconnect). Conjoining them lets the most fragile channel veto learning the
others achieved. Options: (a) per-channel declarations reported separately (the
battery already scores per-cell predictions — the conjunction adds nothing but
veto); (b) keep the conjunction but freeze the hold lifecycle *and* a harness
cadence-alignment guarantee. Recommend (a): declare per organ, compare
composition-vs-separate on installs (the disjunction, C-C1) — that is the actual
composed-vs-separate question (§5 of RECONCILIATION).

---

### C-C3 — T-DEF-BASE-INSIDE-T-COMP: LIVE, SHADOW, OR ABSENT (spec inconsistency)

1. **Name.** C-C3 THE T-DEF-BASE QUESTION.
2. **Exact mechanism (prereg § refs).** Three frozen statements are jointly
   inconsistent:
   - §2: T-COMP wires **T-MC + T-SL + T-TRIP**; T-TRIP = "**T-DEF base** + TRIPWIRE
     layer"; T-COMP's declaration is "all three," and T-TRIP's declaration is
     "**T-DEF's declaration** AND 0 wire fires."
   - §11: the per-episode order lists MC ops, SL ops, release gating, then
     "post-disconnect: TW_CHECK / SLEEPCUT only" — **no T-DEF-base ops**
     (PINSTALL=16, PROMOTE=17, UNINSTALL_PROVISIONAL=18) appear.
   - C3 (§C3): "installs only via MC_SEAL / SL_PIN / novel-lane promotion" —
     a live T-DEF base would install via PROMOTE=17, violating this.
   
   The three consistent readings:
   - **(R1) Shadow.** T-COMP runs the full T-DEF base with installs
     suppressed/redirected; its declaration is computed from shadow state. Then
     A5's window attack *hits the shadow* (`win_hi`/`prom_ep` widen; edge lie
     placed) — the shadow promotes the lie, installs suppressed → A5×T-COMP = 0,
     informatively ("gating blocked it"). But shadow semantics are entirely
     unfrozen: does the shadow's death block T-TRIP's declaration? Does L's
     widening apply to the shadow's params? What does TW_CHECK re-derive L1/L2/L3
     *from* — the shadow's laws or the MC seal/SL law?
   - **(R2) Absent.** T-TRIP-in-T-COMP is tripwire-only. Then A5 has no window
     to attack → A5×T-COMP = 0 **vacuously** — and "T-DEF's declaration" inside
     T-TRIP's declaration is uncomputable, contradicting §2.
   - **(R3) Live.** The T-DEF base runs live, installs and all. Then C3 is false
     for T-COMP — and **A5×T-COMP = KILL** (the base promotes the edge lie:
     npromote==1), contradicting §8's "0 | SURVIVE".
   
   The frozen spec does not select. Note R3's R3-crew parallel: R3's report
   already flags that TW_CHECK's "re-derive L1/L2/L3" is ambiguous about *what*
   the laws are when the base doesn't install — same root cause.
3. **Predicted round + ledger signature.** Decided in phase 2 (A5 cell), round 5.
   Ledger signature distinguishing the readings: presence/absence of op-16/17/18
   rows and `win_hi` widening rows in T-COMP's audit under A5. R1: widening rows
   present, no PROMOTE-install rows. R2: neither. R3: both (and the §8 flip).
4. **§8 cell flipped.** **A5×T-COMP** ("0 | SURVIVE"): R1 → 0 informative; R2 →
   0 vacuous (§2 contradicted); R3 → **KILL** (§8 contradicted). The cell is
   uninterpretable until the reading is frozen — this is also the blocker for
   verdict (ii)'s A5×T-COMP conditional.
5. **Cheapest decider fixture: COMP-SHADOW.** Run A5's phase-1 (silent REKEY) ×
   T-COMP, one round. Assert and log: do `win_hi`/`prom_ep` rows move? Do
   op-16/17/18 rows appear? The answers *define* the reading; freeze it in §11
   before the battery. (Recommend R1 with frozen shadow semantics — it preserves
   §2, §8, and C3 simultaneously — but the TW_CHECK re-derivation source must be
   named: recommend the MC seal + SL law tables, not shadow state.)
6. **L interaction.** Under R1/R3, L's run-1 predicates (`win_hi`/`prom_ep`)
   apply *inside* T-COMP → A5's L-exploit (B-T2) lands inside the composition:
   the composition inherits the T-DEF family's L-vulnerability while §8 scores
   it 0. Under R2, L's run-1 predicates are dead code in T-COMP. The reading
   decides whether T-COMP is exposed to the only L-directed teacher in the
   battery.

---

### C-C4 — AUDIT-BUDGET WORST CASE (the number)

1. **Name.** C-C4 AUDIT-BUDGET WORST CASE.
2. **Exact mechanism (prereg § refs).** KB-COST (§6): `audit_total ≤ 2048` every
   run; §11 note: "REISSUE (≤1 row/ep worst) + ATTEST (1 row/statement) +
   TRIPWIRE (3 rows/8 eps) + base FL2 rows ≤ 2048". Two findings:
   - **(i) The §11 note undercounts the MC channel.** The §11 per-episode order
     lists ≥4 auditable MC ops per episode (MC_PROBE, MC_TAG_CHECK, SR_ATTRIBUTE,
     MC_OBSERVE_BIT/MC_MARK_*) — the note budgets "REISSUE (≤1 row/ep worst)"
     for the whole act channel. Either the build batches multiple ops per audit
     row (batching rule unfrozen) or the true worst case exceeds the note by
     ~3 rows/ep.
   - **(ii) The dominant term is attacker-controlled.** ATTEST = 1 row per
     *statement*; statement density is a genome field (`sched`/`dens` — cf. grok
     DE "sched=every probe", BW "dens∈{0,1}"). A dense-statement teacher
     multiplies the budget by |C| per episode. No frozen cap on statement rate
     exists. Budget exceedance "fails the run" (§6) — a voided run is a
     perverse incentive (a losing teacher voids the evidence), and white-box
     teachers can read the 2048 cap (published prereg, C4).
3. **Worst-case sum (stated assumptions).** E = 128 episodes/round (TW_WATCH bound;
   D5 needs 72); S = |C| statements/episode (adversarial dense); B = 2 base-FL2
   rows/episode (estimate — audit crew verifying independently).
   - §11-note accounting (E=128, |C|=8): 128 + 1024 + 48 + 256 = **1456 ≤ 2048**
     (margin 592).
   - Op-enumerated (4 MC + 1 classify + S hear/log + 0.375 TW + B per ep):
     (5.375 + 8 + 2) × 128 = **1968 ≤ 2048** (margin **80** — razor thin).
   - |C|=16, §11-note accounting: 128 + 2048 + 48 + 256 = **2480 > 2048 —
     BREACH by 432 before base rows are even finalized.**
   - E=72 reference (|C|=8, op-enumerated): 15.375 × 72 = **1107** ✓.
   
   **The number: worst-case joint total 1968/2048 (margin 80) at |C|=8, E=128 —
   and the budget is already breached at |C|=16 with dense statements under the
   §11 note's own rates.** The budget's feasibility is therefore load-bearing on
   two unfrozen parameters (|C|, statement rate) plus the MC batching rule.
4. **§8 cell flipped.** None — KB-COST is a run-validity gate (D7), not a verdict.
   But a breached run voids its cell: at |C|=16 an adversarial teacher can void
   arbitrary T-COMP cells by stating densely.
5. **Cheapest decider fixture: BUDGET-DENSE.** T-COMP, honest teacher replaced by
   a dense-statement honest genome (`dens=1`, one statement per context per
   episode), 128 episodes. Assert `audit_total ≤ 2048`. If it breaches, freeze a
   statement-rate cap (or per-episode UTT_LOG batching: 1 row/episode + count)
   before the battery.
6. **L interaction.** None — accounting. (Note: no L predicate sheds audit rows;
   all six only add.)

**Freezes needed:** (F4) |C| for the battery; (F5) max statements/episode (or
batched utterance logging); (F6) the MC-channel rows/episode rule (batching vs
per-op). The build crew's joint-budget computation (§9: "computed by the build
crew … before the battery runs") must use the op-enumerated worst case, not the
§11 note.

---

## Cross-surface ranking (top 3 overall)

1. **C-C3 — T-DEF-BASE-INSIDE-T-COMP (R1/R2/R3).** The only finding that makes
   frozen §§2/8/11/C3 jointly inconsistent. It flips A5×T-COMP between 0 and KILL
   depending on the reading, decides whether L's only attacker reaches inside the
   composition, and blocks verdict (ii)'s A5×T-COMP conditional. Must be frozen
   before any T-COMP run; COMP-SHADOW decides it in one round.
2. **B-T1 — A6 BUNDLE PROVENANCE GAP.** Flips two §8 cells (A6×T-SL,
   A6×T-COMP: SURVIVE → honest-cost FAIL) if the build's selection/self-utterance
   touches derived rows; guts D2's headline ATTEST fixture, whose "ORPHAN" defense
   is mechanism-mismatched as frozen (real defense = E14-authority + SPOKEN-only +
   selection-reads-law[], resting on un-frozen invariants F1–F3). A6-MINI decides
   it in two rounds. Note the coupling: B-T1's flip also feeds B-T3 (in-battery
   M-MAX then kills T-SL/T-COMP on honest cost — still not T-MC).
3. **A-S1 — DECLARED-TARGET FORGE.** Undermines the prereg's centerpiece (§7):
   the (v) column is attacker-self-reported as written; D8 certifies computation
   only (A-S3); the realistic vector is stale-declaration via A1's own coordinate
   descent (no adversarial intent needed); the run-1 re-score inherits the risk.
   Fix is one derivation rule + D8-FORGE — small, but without it every (v) number
   in RESULTS.md rests on trust.

**Honorable mentions:** C-C1 (disjunctive installs — the structural reason the
composition is only as strong as its cheapest installer; load-bearing for B-T1);
B-T3 (M-MAX's "kill everything" contradicts §8 — reframe as discrimination
control); C-C4 (budget margin is 80 rows at |C|=8 and negative at |C|=16 —
freeze |C| and the statement rate); B-T2 (A5's vacuous cells burn ~76+ runs
confirming a stated irreducible); C-C2 (conjunction veto — weakest-channel
liveness veto, a composition-regression vector for H-H2-R-4).

---

## The three verdicts

**(i) Does the genome-log trust hole kill §7 as written?** **Yes — as a certified
instrument.** §7 specifies no declared→played binding and no consistency check;
D8 tests only the honest-declaration case (A-S3); the (v) column is a self-report
by the evolved attacker until the target is *derived* from the wire trace (or the
harness cross-checks declared vs emitted). The realistic in-battery vector is
A-S1b stale-declaration via coordinate descent, and it corrupts the run-1 re-score
too. Small fix (derivation rule + D8-FORGE), but without it §7's numbers rest on
trust. F2's incentive (rewards (v)) means evolved A1 won't forge — the hole is
hygiene + re-score integrity, not an evolved exploit.

**(ii) Does A5 belong in the run-2 battery?** **Yes for T-DEF/T-TRIP; no for
T-MC/T-SL as organ tests; A5×T-COMP conditional.** A5 is D2's predicted double
kill, the battery's only teeth besides A6, and the *only* L-directed teacher
(it exploits L's monotone widening — a frozen-L fact worth recording, not
misattributing to T-DEF). T-MC/T-SL have no `win_hi`/`prom_ep` to widen (§8's own
notes admit it; §12 labels the edge strike a stated irreducible) — those cells are
vacuous 0s, cut or re-scope as labeled irreducibility checks. A5×T-COMP stays
uninterpretable until C-C3 is frozen.

**(iii) The single most dangerous T-COMP finding.** **C-C3: the frozen spec does
not say whether the T-DEF base inside T-COMP's T-TRIP component runs live, as a
shadow, or not at all** — §§2, 8, 11, C3 are jointly inconsistent across the three
readings (R1: A5×T-COMP 0 informative but shadow semantics unfrozen; R2: 0 vacuous
and §2 contradicted; R3: A5×T-COMP KILL and §8 contradicted). One round
(COMP-SHADOW) + one freezing decision resolve it; recommend R1 with named
re-derivation sources.

---

## Appendix — open freezes this report needs (consolidated)

- **F1** (B-T1): plant-time provenance rule for bundled implications
  (D2's CITATION/BUNDLE row or equivalent).
- **F2** (B-T1): `sl_select` reads only `law[]` (never derived rows).
- **F3** (B-T1): no `SL_SAY` of acts suggested only by derived rows.
- **F4/F5/F6** (C-C4): |C| for the battery; max statements/episode (or batched
  UTT_LOG); MC-channel rows/episode rule.
- **F7** (C-C3): T-DEF-base reading inside T-COMP (recommend R1-shadow) +
  TW_CHECK's re-derivation source.
- **F8** (C-C1): `tag_reg` unified vs per-channel in T-COMP (recommend unified).
- **F9** (C-C2): hold lifecycle (what clears `hold`) + declaration form
  (recommend per-organ declarations, drop the conjunction).
- **F10** (A-S1/A-S3): declared→played derivation rule + D8-FORGE in D8.
- **F11** (A-S2): scorer's canonical basis (harness's, not per-variant) + the
  out-of-basis scoping statement (or a non-kill `obm` instrument).
- **F12** (B-T3): M-MAX redefinition (worst-case in-battery schedule;
  teeth + discrimination pass conditions).

*All freezes are spec text, committable before step 2 of §13's commit order. None
require organ code.*
