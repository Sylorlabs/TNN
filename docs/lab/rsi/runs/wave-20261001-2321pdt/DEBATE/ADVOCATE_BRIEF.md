# ADVOCATE_BRIEF.md: wave-20261001-2321pdt, the case for all 8 verdicts standing

Role: ADVOCATE. Method: read-only synthesis of the wave record, the
debate slate, the debate-prep brief, and the six synthesis lanes.
No experiments run. No em-dashes.

Standing principle, stated once: a verdict names the exact frozen
bars that governed it. A later, harder test that falsifies a broader
reading of a result does not retroactively move the bars that
governed the verdict. What the later test changes is the claim's
future citation boundary, not the verdict. That boundary is honest
only when carried as written qualifications. The skeptic's error in
this wave, repeated across questions, is to treat a sharper claim
boundary as a broken verdict. These are not the same thing.

---

## Q1. F1: UPHOLD BUILD-FAIL (not PARTIAL)

The verdict stands as BUILD-FAIL on the whole candidate as frozen.
The case:

1. The bar tripped as frozen. K-C0C-REG on R-W2 scored 0/30 hidden
   against an 80% threshold. The bar was not weakened. A BUILD-FAIL
   on a tripped frozen kill bar is the default, correct verdict.
   Commits: prereg 50de69403, implementation ba5ebbf8b (binary
   6f2b155b), sealed eval 3b159b401, judge-brief 14fdf441d.

2. The killing evidence is the strongest possible: it isolates the
   failure to a pre-existing constructor limitation. The prior
   wave's frozen binary, on the same sealed fixtures, converges to
   the byte-identical overfit structure (TRIGGER at ep 1, same 3
   constructs, 30/30, identical [4 4 4 2] structure) and scores
   0/30. The new binary reproduces the prior wave's W2 fixtures
   exactly. The trigger cannot be implicated. RT-EXEC verified
   this as PROVEN STRONGLY and independently reproduced
   byte-identical train states.

3. PARTIAL is not a defined verdict in the frozen rules. Creating
   it post hoc to rescue the trigger component would be
   bar-weakening, exactly the move Micah's red lines forbid. The
   procedural precedent question settles it: the frozen candidate
   was trigger plus constructor on the same fixtures; the
   trigger gets its proper channel, the NEW candidate path, which
   F1-FOLLOWUP Part 1 already used successfully (BUILD-PASS, all
   frozen bars on validated fixtures, byte-identical normalized
   CONSTRUCT sequence). That verdict document explicitly states it
   is NOT a change to the F1 BUILD-FAIL. The system worked as
   designed.

4. The worker's honest ownership of the bar-calibration mistake
   (unvalidated fresh seed conflating trigger regression with
   constructor seed-robustness) is a reason to keep the verdict,
   not soften it. Admitting a miscalibrated bar and keeping the
   fail teaches the right lesson: bars are calibrated or they
   are not. Narrowing to PARTIAL would reward the confusion.

Concession, stated plainly: the trigger component itself performs.
All trigger bars passed (fires on all 4 interleaved patterns, 0
false positives on 3 clean worlds, 30/30 learning, 57pp/57pp
ablations). The advocate does not dispute the component evidence.
The dispute is only procedural: component performance is filed as
a new candidate, never as a retroactive verdict edit.

Verdict: UPHOLD BUILD-FAIL.

---

## Q2. H-PI-REV2: BUILD-PASS with qualifications stands

The verdict stands with the RT-HPIREV2 qualifications attached.
The case:

1. Every frozen bar passed as frozen. K-SC-W1 5/5 (25/25 EW pairs),
   K-SC-W2 revision_evals 6/6/6/11/6 (all at or under 25), K-SC-W3
   reuse_correct=1 with zero new revision lines after the W3 probe,
   K-SC-W4 3/3 byte-identical, K-SC-W5 pure Zag and dash-free,
   K-SC-B bound-trip 3/3 (S1 fails=1, S2 COUNTEREXAMPLE_DETECTED at
   the held-out probe, S3 0 post-W3 lines, byte-identical to the
   step-7 transcript f56080d6), K-ARCH1/2 zero cognition source
   delta. All on 5 fresh sealed worlds A2/B1/B2/C2/D2. Commits:
   prereg 00b31af53 (alone), implementation ec52cf1ca (binary
   aee1b6f2). Commit-order self-check passes. RT-HPIREV2 Part 1
   independently reproduced 15 runs 3/3 byte-identical with bars
   verbatim. That is a BUILD-PASS.

2. The red team's findings bound the claim; they do not falsify the
   bars. Q1 (certification defect, 24/25 hashes, the 62-char
   truncated D2_FW.txt line) is a transcription typo in the prereg
   document: same file committed, staged, run. It changes nothing
   experimental. Q2 (the five worlds accommodate the rank-biased
   diagnosis by disclosed pre-freeze design) is load-bearing but
   honest: the non-independence was disclosed in the prereg, not
   hidden. The narrowed claim as stated was never tested against a
   conflict the rank bias does not select, and that is why the
   qualifier exists.

3. Part 2 adversarial results confirm the bound's content, not its
   death. ADV-S1/S2/S3 PASS (the bound generalizes to fair
   structures). ADV-S4 BREAK CONFIRMED is a valid single-conflict
   world whose true trigger (2,66) the rank bias cannot select.
   ADV-M1 is silent success; ADV-M2 is an explicit trip. The
   probe-dependence of the trip signal is a measured property of
   the mechanism, and the reviewer recommends exactly the two
   qualifiers the advocate attaches: rank-diagnosability on the
   narrowed claim, probe-dependence on the bound-trip half.

4. Further narrowing (to "the bound holds only on
   rank-diagnosable single conflicts with probe-dependent trip
   signaling") is not a verdict change; it is the same qualified
   claim restated. ADV-S4 bounds the qualified claim rather than
   falsifying the bars. The adversarial family ran the frozen
   mechanism byte-verbatim (cognition delta 0); nothing about the
   frozen-bar evidence moved. If the skeptic wants ADV-S4 to
   falsify "the narrowed claim as originally stated," the advocate
   agrees, and notes that is precisely why the rank-diagnosability
   qualifier is attached. The verdict that stands is
   BUILD-PASS-with-qualifications, not BUILD-PASS-as-bare-slogan.

Concession: citing the claim without both qualifiers is disallowed
under the advocate's own position. The certification defect is
recorded. The non-independence was disclosed and remains a bound
on generality, honestly stated.

Verdict: UPHOLD BUILD-PASS with the rank-diagnosability and
probe-dependence qualifiers carried verbatim.

---

## Q3. ARENA2 vs ARENA3: both stand as independent runs

Both BUILD-PASS claims stand. The case:

1. Each met its own frozen bars independently. ARENA2 REMAP:
   C12 0 to 1, arena total 0.794 to 0.882 (60/68) on the v6 base,
   all 8 kill bars PASS, +94/-0 lines, zero new
   modes/bridges/routers/gates/semantic cases, ablations zero
   exactly each half (both halves causal), no sealed values
   hardcoded (composes exposure-learned Zem templates with the
   runtime-parsed permutation; claims generalization to any
   permutation/template). Prereg 5a055b575 (alone),
   implementation+eval 18309290c. ARENA3 TRX: C12 0 to 1 (6/6),
   total 0.853 to 0.941 (64/68) on the INQ base, all 9 kill bars
   PASS, +80/-0 lines, ablations 3/6 each half (both halves
   causal), remap always from the question, never source/state
   (validates permutation of [0,1,2,3]). Prereg 829208f99 (alone),
   implementation 9191e71de, eval records in d51d8ef5b. Both
   disclaim L3.

2. The frozen collision clause governs and it was satisfied:
   ARENA2's directory was empty at ARENA3's start, the assumption
   was recorded pre-build, and the clause names these independent
   competing runs, not duplication. Overriding the clause now
   would be the same post-hoc bar-weakening the advocate rejects
   in Q1.

3. Subsumption is premature. The two mechanisms have different
   generality profiles: REMAP claims any-permutation generality
   from exposure-learned templates; TRX validates parsed
   [0,1,2,3] relabeling with position-wise rewrite. Neither is
   cumulative with the inquiry candidate; canonical 0.573 is
   unmoved by both. Retiring one without the composition
   experiments (REMAP on the INQ base, TRX generalized beyond
   [0,1,2,3]) would destroy information the collision clause
   exists to preserve.

4. The scores are not directly comparable (different bases: v6
   vs INQ), so no ranking claim is made. Both stand; the debate
   compares generality and scopes integration later.

Independent value preserved: ARENA2's C9 negative finding stands
as a genuine contribution regardless of the transfer comparison.
The causal battery is observationally unidentifiable by design
(all 12 observations satisfy x==y==z; zero intervention turns;
the only 3/3 mechanism is question-format gaming, rejected).
Honest UNKNOWN scores 0. That finding, with the generator fix
recommendations (randomize candidate order, add real
intervention turns), survives any reconciliation of the two
transfer mechanisms.

Verdict: UPHOLD both as independent competing runs; no
subsumption until the composition experiments exist.

---

## Q4. E3 mandate: scope is correct (broad)

The broad mandate stands: every wave construction claim resting
on unmasked QUERY evidence must be re-examined blind. The case:

1. E3B blind is a clean discriminating result, not a methods
   quibble. Blind: 0/2, outputs exactly the pre-registered
   spurious composites [80971, 80972] vs sealed targets
   [80921, 80922]. Oracle-present: 2/2. The white-box inspector
   confirms the blind trial runtime-assembled GUARD/SETREG chain
   graphs with ET_DEP provenance to the taught spurious facts,
   promoted them as MAP nodes, and executed them. ASSEMBLY WORKS
   BLIND; SELECTION DOES NOT. Commits: prereg a17a276c8 (alone),
   implementation ce46b327a, 12 sealed runs 4f49f8b66.

2. The interpretation is load-bearing and was recorded honestly:
   correct compositions depended on the unmasked verifier
   (t2_try_verify: accept iff output equals the QUERY-carried
   expected value) to SELECT among multiple executable BFS
   chains. Without the oracle, masked mode emits the
   first-executable chain. This REFRAMES EVERY PF CONSTRUCTION
   OBSERVATION as BFS enumeration plus oracle selection, not
   selective construction. That reframing is a positive result,
   not a voiding: it tells the program exactly what to build
   next (learner-side selection machinery, per CLUSTER-FINAL
   property 3).

3. The narrow reading ("only claims with a structural selection
   step among multiple candidates") would exempt mechanisms on a
   technicality that E3 already closed. Any masked-trial
   mechanism that emitted correct compositions on unmasked
   QUERY runs is inside the blast radius, because the
   first-executable-chain behavior is what the trial does when
   the oracle is withheld. The mandate is a re-examination
   requirement, not a guilty verdict: ARENA-BLIND is the proof
   that mechanisms survive it. The ROSTER audit (prereg
   0b95a6601, audit c2eb08c2a) passed all six frozen criteria
   A1-A6: the 72 sealed test turns carry exactly
   {turn, kind, item, cap, q}, the frozen ROSTER source parses
   only item/cap/q, there is no candidate set and no selection
   step (exactly one candidate: the roster enumeration), and
   ROSTER never emits OBSERVE requests. Per the frozen decision
   rule, ORACLE-FREE means the masked re-test branch is not
   triggered. That audit is the template; it answers the
   mandate per mechanism rather than exempting mechanisms by
   category.

4. PF-A2's 2/2 valid-composition result is re-described, per
   CLUSTER-FINAL, as BFS enumeration plus oracle selection. E3's
   own confound note (BATTERY-E1's W4 behavioral leg:
   structure-driven answers vs oracle-verified BFS traversal
   indistinguishable) marks the scope honestly.

Concession: the mandate is work, and it applies to prior-wave
evidence too. That is the point. The broad mandate is the
correct price for having discovered that the verifier was doing
the selecting.

Verdict: UPHOLD the broad mandate; ARENA-BLIND is the per-mechanism
template for satisfying it.

---

## Q5. H5R2: BUILD-PASS stands within frozen scope

The verdict stands. The case:

1. BUILD-PASS was awarded against frozen bars, and every bar
   passed. KB-W0 36/36, KB-S1 substrate gate PASS, KB-W2R 12/12
   (recovering the killed 8/12 bar), KB-B2R 24/24, KB-W3 8/8 (new
   two-revision family), KB-B3 24/24, KB-G1R architecture PASS
   (net +9 cognition lines against a 15-line budget; zero
   modes/bridges/routers/handlers; zero ISA additions; cumulative
   diff net -4 vs the TNN-2 base), KB-D1 3/3 byte-identical, KB-P1
   pure Zag. Commits: prereg dc7df4aba, implementation 9db334bd4
   (binary 19dcf2e4), sealed eval e20ba5402. H5R2-REPRO:
   REPRO-PASS independently (commit 8b30769de), every number in
   SEALED_EVAL_H5R2.md reproduced exactly, SHA-256 matches the
   frozen binary bit for bit.

2. SEPARATED does not retroactively move those bars. A verdict
   names the exact bars that governed it. The re-teach family
   lies outside the frozen battery's event sequences: the battery
   never leaves two live facts on one key. On every frozen
   family, the gate's promoted candidate coincides with
   NEWEST-LIVE-ON-KEY's (baseline lane, decoy lane, chained
   lane all show agreement). The coincidence was constructed to
   be broken by a later lane, precisely because it was a
   coincidence, and that lane succeeded. That is the
   discriminating-experiment program working, not a verdict
   failing.

3. The four-lane arc is coherent and strengthens, not weakens,
   the gate's standing. BASELINE-MATCHES: recency matches on the
   four worlds because there the newest fact happened to be the
   live one; disclosed cost, recency regresses the built-in
   battery to 45/46 (F2 masked-query disambiguation breaks)
   while H5R2 holds 46/46. DECOY-DISCRIMINATES: on 8 decoy probes
   where the newest fact is NOT live, H5R2 anchors every revert
   MAP's DEP edges to the live older fact 8/8 while
   REVERT-TO-LATEST anchors to the decoy 8/8; necessity vs
   recency PROVEN. SKEPTIC2: the stronger skeptic
   NEWEST-LIVE-ON-KEY matches 8/8 byte-identically on chained
   decoys; necessity still unproven there. SEPARATED: on the
   re-teach family the gate picks SEP-OLD 8/8 and the skeptic
   picks SEP-NEW 8/8, with NEWEST pre-registered as the favored
   arm under the standard belief-revision reading. Every arm
   failure across all four lanes is provenance-only (D-ANS/VAL
   8/8 on all arms everywhere).

4. The honest scope: the gate is a stale-provenance filter, not
   a uniquely-correct promotion policy. It refuses to anchor DEP
   edges to superseded or dead facts; it does that job on all
   frozen families and on the decoy families. Its oldest-first
   tie-breaking is a creation-order artifact of forward node-id
   enumeration, unjustified by any lane's evidence, and the
   re-teach world is a genuine counterexample to any reading of
   the claim as "stale provenance is fixed" in full generality.
   That gap is named explicitly as an open gap: any next gate
   must pass the union of the frozen families and the separator
   family, or the scope is narrowed publicly. The synthesis
   names the buildable next hypothesis: provenance filter plus
   newest-live tie-breaking among all live licensing facts.
   None of the four lanes built it; that is future work, not a
   reason to unbuild the current verdict.

Concession: the skeptic's reading that SEPARATED falsifies the
broadest slogan of the claim is correct about the slogan. The
advocate's position is that verdicts certify bars, not slogans,
and the citation boundary going forward must name the re-teach
gap. BUILD-PASS within frozen scope; open gap acknowledged;
scope narrowing required for any broader claim.

Verdict: UPHOLD BUILD-PASS within its frozen scope, with the
re-teach gap named as an explicit open gap.

---

## Q6. ARENA5: BUILD-PASS stands within bounded scope

The verdict stands. The case:

1. All 8 frozen kill bars passed on the fresh sealed 68-item
   battery (seed 71503461337032). K1: C15 0.947 on all 3 runs,
   the honest experience-based ceiling (Momado never appears in
   expo turn events on any seed, verified from the frozen
   world_gen source; 2000*9/(10+9) = 947). K2: 54.947/68 = 0.808
   with all 15 non-target capabilities byte-identical to the v6
   fresh baseline; zero regressions. K3: 3/3 byte-identical. K4:
   pure Zag. K5: sealed validity holds (arena rebuilt to the
   refreeze hash; zero hits on all 10 sealed names). K6:
   ablation causal (roster off yields C15 0.000, others
   unchanged; default-action-disabled with roster on yields
   0.000, proving the default action is the goal-completion
   path). K7: 174 lines added, 0 changed, zero dedicated goal
   handlers, zero modes/bridges, zero "listnames" hits in the
   mechanism source. K8: explicit L3 disclaimer. Commits:
   prereg b63f80289, Amendment 1 f3320caf8 (seed validity rule),
   implementation 2320c3454, sealed eval + judge brief
   6582398e9. CANDIDATE only; L3 disclaimed; canonical 0.573
   unmoved. RT-ARENA5: QUALIFY, BUILD-PASS stands; the reviewer
   independently reproduced the load-bearing evidence.

2. NARROW tests a bar the lane never froze. ARENA5's prereg K7
   demanded only no goal handlers, and that bar is clean:
   intensionally, DEFRECALL is not a handler (zero goal-string
   branches, proven by source grep and by firing on content-free
   bare prompts like "x"). Judging BUILD-PASS by a
   discriminating-generality bar the lane never preregistered
   would itself be a governance violation. ARENA-GEN ran the
   test ARENA5 did not: AG-1 PASS (0.947 reproduced on fresh
   seed 71503461337033), AG-2 FAIL at 5/7, AG-3/AG-4/AG-5 PASS,
   verdict NARROW, recount-verified by ARENA-GEN-VERIFY. What
   NARROW refutes is the advertising language "general default
   action," not any frozen bar and not the intensional claim.

3. The bounded claim that survives is real infrastructure:
   DEFRECALL is a content-blind structural trigger (dispatch
   miss AND bare prompt AND non-empty roster) that volunteers
   persistent knowledge, causally tied to the experience-built
   roster (K6), honest about absence (empty roster yields
   UNKNOWN, no hallucination), zero regressions, L2 goal
   infrastructure. That is worth having: the arena went from
   zero bare-prompt goal completion to handler-free roster
   volunteering with no regressions and no architecture growth.

4. RT-ARENA5 had already named the exact bound: on the sealed
   battery the default action is extensionally equivalent to a
   listnames handler, because exactly one of the 68 items is a
   bare prompt. The battery could not discriminate; the source
   could. ARENA-GEN narrowed it further: across a diverse
   bare-prompt battery the mechanism is extensionally a
   bare-prompt handler, generality real in scope (all bare
   prompts, not one goal string) but shallow in content (no
   discrimination between appropriate and inappropriate
   enumeration). The advocate accepts this full progression:
   PASS on the bars as preregistered, to the bars cannot
   discriminate generality, to the generality tested directly
   is indiscriminate.

Concession, stated without hedging: the mechanism answers
"whattime" with a list of names and answers a bare "invent"
with a list of names. The claim on the words "general default
action" is untenable without a discriminating trigger. The
dev-probe demonstration was one-sided by design. The supported
bounded claim is a content-blind structural trigger that
volunteers persistent knowledge. The debate's open question
(whether that bounded claim is the thing worth promoting, or
the sign that the direction needs a discriminating trigger
first) is a research-direction question, not a verdict
question. DEFRECALL may not be cited as general default-action
evidence until a discriminating trigger is demonstrated via
general machinery or learner-created discrimination, with
adversary-supplied negatives, preserving K2/K6/K7 quality.

Verdict: UPHOLD BUILD-PASS within bounded scope. Not
retroactively re-graded; citation carries the NARROW.

---

## Q7. CONTLEARN: BUILD-PASS stands in machinery-enabled scope

The verdict stands. The case:

1. The frozen bars measured exactly what the prereg froze, and
   all passed. K4a unsupervised store 13/13 (7 family-B + 6
   family-C MAPs, zero answer keys). K4b unsupervised masked
   reuse 20/20 across 3 task families. K4c in-arena deletion
   ablation: original-value reuse drops to 0/20 while successor
   retrieval stays 20/20. K4d nostore control 20/20 true misses.
   K3: 2021pdt cl_driver 3/3 re-run, REUSE_COUNT 30/30 retained,
   no regression. K5 UNCERT count 0. K6 3/3 byte-identical.
   K0/K1/K2: prereg 408ffdcdc frozen alone, implementation
   dfcd3caf strict descendant, frozen core untouched, pure Zag,
   cognition-source delta 0/0/0, no new modes/bridges/handlers.
   RT-INT: EVIDENCE-HOLDS on CONTLEARN with the weak/strong
   qualifier carried. Those measurements are true of the
   machinery-enabled core and no later lane disputes them.

2. CONTLEARN's own verdict document stated the scope explicitly
   and the strong sense was never claimed: the workspace is
   owned in the weak H10 sense (resident in the learner's
   arena, manipulated only through the frozen event interface).
   The machinery-disabled lanes upgrade that scope statement
   to a measured fact: CONTLEARN-OWNED (0/6 vs 6/6 on the fixed
   disclosed battery of fresh 2-hop chains; STORE_OK 0/6 vs
   6/6, REUSE 6/12 vs 12/12, DELAYED 6/12 vs 12/12, zero MAP
   nodes at every phase) and CONTLEARN-OWNED2 (independent
   replication; MAPC=0 at all three censuses; DEPC equals
   GUIDEC at 6/12/18, proving the only learner-side edges ever
   written were guide-to-UNCERTAINTY links). Standing retrieval
   of taught 1-hop facts stayed intact in TREAT (6/6) in both
   lanes, so the variant is functional and the gap is a
   capability gap, not breakage. LEARNER-MECH gives the root
   cause, verified against the frozen bytes by MECH-VERIFY
   CONFIRMED x3: initiation is event-only (nothing in learner
   state can gate, enable, defer, retry, or redirect the trial
   loop), control parameters bypass learner state entirely
   (mp_run never reads the mp slot), and the miss path
   hardcodes escalation. Per CONTLEARN-OWNED's own verdict:
   "the strong sense (the learner decides or authors) is now
   measured absent, not merely unclaimed."

3. The discrimination falsifies the strong reading, which
   CONTLEARN never claimed. That is a supersession of the claim
   boundary, not a retraction of the evidence. The 13/13 and
   20/20 measurements remain true. Retiring or renaming the
   verdict would erase a real, measured, determinism-verified
   result (unsupervised store and masked reuse without
   per-query answer keys, killing the key-matching confound)
   because of a reading its own authors disclaimed. The
   correct outcome is citation discipline.

4. The required citation form going forward:
   "LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong
   sense measured absent, CONTLEARN-OWNED/OWNED2)." It evidences
   learner-owned responsiveness and storage within the frozen
   interface (weak H10), not learner-authored integration. The
   K3 regression check (REUSE_COUNT 30/30 retained) is cited
   unconditionally. Any citation of the label as learner-authored
   integration is a category error under the advocate's own
   position.

Concession: the machinery-disabled discrimination is the most
consequential negative result in this wave's integration story.
Learner authority over integration is effectively zero on
frozen TNN-2; the TNN-3 open question (initiation-from-state,
control-from-state, trigger-from-state, white-box visibility of
the initiation act) is genuine new work. The advocate does not
soften that. It does not overturn the bars CONTLEARN froze.

Verdict: UPHOLD BUILD-PASS within the machinery-enabled scope;
LEARNOWN-DEMONSTRATED cited only in the bounded form.

---

## Q8. CONSEQ and CONTLEARN: qualified citation is honest

Both results stand with their carried qualifications. The case:

1. CONSEQ is VALIDATION-PASS on an independent re-execution of
   the frozen Node2-v2 K-H3 prereg (4b05c8011): 5/5 kill bars
   PASS, 3/3 byte-identical, hashes match bit for bit, causal
   ablations on Link 1 (consequence record disabled: default
   reverts to fixed 30) and Link 3 (production read disabled:
   guide stays 30) both NECESSARY. Commits e068ac9a4. That is
   what the verdict certifies: reproduction fidelity of the
   consequence re-entry template. C174 graduates the shared
   tag-61 consequence store from EMERGES to validated-on-frozen-bars
   as infrastructure (STORE-SERVES-TWO, BEHAVIOR-CHANGE,
   ABLATION-CAUSAL, MIGRATION-COMPAT, DETERMINISM; prereg
   134af1cb2, implementation b5e0274f7, seal 0096b30ca, eval
   3028240e4), with honest dev-harness scope: not TNN-2/TNN-3
   integration, thresholds/weights are researcher scaffolding,
   broader worlds untested. RT-INT and RT-C174: EVIDENCE-HOLDS,
   no dissent, qualifications carried.

2. The carried qualifications are already the honest form.
   CONSEQ: the independent-adversary clause was never met
   (builder-sealed worlds); this wave confirms reproduction
   fidelity, not adversarial validation. The consequence record
   is a researcher-written 3-revelation counter, inside the
   frozen claim bounds but still researcher-authored. Scope is
   honestly held: it validates the template, not the substrate
   itself. CONTLEARN: masked queries remain researcher
   scaffolding, honestly disclosed; the weak/strong distinction
   stays attached whenever cited.

3. Stripping the advancement claims would misprice what was
   actually achieved. CONSEQ advances the
   shared-consequence-substrate hypothesis toward the adversary
   clause: independent re-execution with byte-identical hashes
   and two NECESSARY ablations is the prerequisite step the
   clause requires before an adversary can be trusted to test
   anything. To call it "reproduction fidelity only" as a
   demotion is to forget that the fidelity step was the
   missing one. C174's STORE-SERVES-TWO (one store serving
   reorder and retention via sub_consec) plus the ABLATION-CAUSAL
   byte-for-byte reversion to the fixed baseline is genuine
   infrastructure validation, not a bare re-run. The adversary
   clause defines the next experiment; it does not erase the
   evidence the qualification carries.

4. Qualified citation is the mechanism by which the wave's
   claims stay honest, and it works: the qualifications are
   specific, checkable, and already recorded (adversary clause
   unmet; weak H10 only; machinery-enabled scope; dev-harness
   scope for C174; shared-code fallback noted for C174 bar
   (c); K-H3-world compat bound for bar (d)). The stripped
   alternative (verdicts stand as measurements but may not be
   cited as advancing their parent hypotheses) would turn
   every qualified verdict into a private number, which is
   indistinguishable from discarding the wave's work while
   keeping its paperwork.

Concession: CONSEQ does not establish that the shared
consequence substrate generalizes, survives adversaries, or
integrates into TNN-2/TNN-3. CONTLEARN's "learner-owned"
framing without the bounded citation form is a hazard, as
RT-INT named it. The advocate's position makes the bounded
citation form mandatory, not optional.

Verdict: UPHOLD both as qualified evidence; the qualifications
are carried verbatim in every future citation.

---

## Closing: what the advocate concedes and what the advocate holds

Conceded, without reservation: five slogans died or narrowed in
this wave. The F1 trigger's component success does not soften
its BUILD-FAIL. H-PI-REV2's claim carries a
rank-diagnosability qualifier it cannot shed. DEFRECALL is a
bare-prompt handler, not a general default action.
LEARNOWN-DEMONSTRATED is machinery-enabled, strong sense
measured absent. H5R2's gate is a filter with an unjustified
tie-break direction and a known re-teach gap. E3 reframed every
PF construction observation as BFS enumeration plus oracle
selection. These are the wave's hard-won findings, and the
advocate defends them as findings.

Held: none of that overturns a verdict, because verdicts
certify frozen bars and every cited bar was met as frozen.
The skeptic's program across all eight questions is the same
move: take a sharper, honestly-earned claim boundary and call
it a broken verdict. The advocate's answer is the same in all
eight: carry the boundary as written qualification, and let
the verdict stand on the bars that governed it.
