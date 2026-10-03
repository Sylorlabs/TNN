# DEBATE_BRIEF.md: wave-20261001-2321pdt (40-verdict slate)

For the wave's mandatory debate group (advocate, skeptic, judge).
Compiled by DEBATE-PREP from
docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md alone.
No new experiments were run for this brief. No position is advocated.
All verdicts below are marked [NEW] in the wave record (debate pending
where noted). Commits are local only, never pushed, on branch
tnn-native-lab.

## Verdict counts

| Outcome group | Count | Verdicts |
|---|---|---|
| BUILD-PASS | 12 | HPIREV2, CONTLEARN, TNN3H5R, ARENA-C8, ARENA2, ARENA3, DEVANG3, ARENA4, H7R, F2V3, ARENA5, F1-FOLLOWUP Part 1 (new candidate) |
| BUILD-FAIL | 2 | F1, H6R |
| Validated / instrumentation / analysis | 7 | FORK, H5R2-REPRO, CONSEQ, C174, C9BAT, ARENA-BLIND, BATTERY-CLUSTER |
| Battery v3 validation | 1 | BATTERY Part 1 (VALIDATED; its Part 2 sits below) |
| Discriminating-experiment results | 12 | BATTERY Part 2 (1/6), H5R2-BASELINE, H5R2-DECOY, F1-BUFFER, F1-REPAIR, F1-REPAIR2, BATTERY-E1, BATTERY-E2, BATTERY-E3, BATTERY-E4, BATTERY-E5, BATTERY-E6 |
| Red-team reviews | 6 | RT-EXEC, RT-INT, RT-GOV, RT-C174, RT-HPIREV2, RT-SENSE |
| Design-complete | 1 | TNN3-SUBSTRATE |

Total: 12 + 2 + 7 + 1 + 12 + 6 + 1 = 40. (The BATTERY bullet was split
into Part 1 validation and Part 2 sealed adversarial battery; the
F1-FOLLOWUP bullet carries Part 1 BUILD-PASS and Part 2 NOT-FOUND;
RT-HPIREV2 carries Part 1 QUALIFY and Part 2 adversarial results.)

## 1. The verdict slate

### 1a. BUILD-PASS (12)

**1. H-PI-REV2 narrowed single-conflict claim (step-7 bounding).**
Frozen bars (K-SC-W1..W5, K-SC-B, K-ARCH1/2) all PASS on 5 fresh sealed
worlds (A2/B1/B2/C2/D2): K-SC-W1 5/5 (25/25 EW pairs correct);
K-SC-W2 revision_evals 6/6/6/11/6 (all <= 25); K-SC-W3 reuse_correct=1
with zero new revision lines after the W3 probe; K-SC-W4 3/3
byte-identical; K-SC-W5 pure Zag, dash-free; K-SC-B bound-trip 3/3
(S1 fails=1, S2 COUNTEREXAMPLE_DETECTED at held-out probe, S3 0
post-W3 lines; byte-identical to step-7 transcript f56080d6);
K-ARCH1/2 zero cognition source delta, no architecture growth.
Revision measurements matched pre-freeze mechanical predictions exactly
on all five worlds. Commits: prereg 00b31af53 (alone), implementation
ec52cf1ca (binary aee1b6f2...); commit-order self-check passes.
Caveats in record: world design non-independent (disclosed in prereg);
three world-design slips fixed pre-freeze (disclosed); no L3,
representational-invention, or broad-generality claim; not SURVIVES
(transfer/reuse beyond the single probe, second independent red team,
governance audit remain). Step-5 PASS, step-6 PASS 13/13, step-7
FAIL-with-bounding untouched. [NEW] (debate pending)

**2. CONTLEARN learner-owned push: BUILD-PASS, LEARNOWN-DEMONSTRATED.**
Frozen kill bars K0-K6 all PASS. K3: 2021pdt cl_driver re-run 3/3,
stdout hash matches, REUSE_COUNT 30/30 retained (no regression).
K4a unsupervised store 13/13 (7 family-B + 6 family-C MAPs, zero
answer keys). K4b unsupervised reuse 20/20 masked probes across
3 task families. K4c ablation: in-arena deletion drops original-value
reuse to 0/20 while successor retrieval stays 20/20. K4d nostore
control 20/20 true misses. K5 UNCERT count 0. K6 3/3 byte-identical
per mode. K0/K1/K2: prereg frozen alone (408ffdcdc), implementation
(dfcd3caf1) strict descendant, frozen core untouched, pure Zag,
cognition-source delta 0/0/0, no new modes/bridges/handlers.
Honest bounds: does NOT claim learner agency (H2-v2/H3 stand),
procedure execution at query time, L3, or generality; workspace is the
single frozen arena (weak H10 sense). Two trivial incidents resolved
(git index.lock wait, one wrong relative path). [NEW] (debate pending)

**3. TNN-3 H5R2 trial-loop stale-provenance fix: BUILD-PASS, H5R2
ADVANCES.** All frozen kill bars pass: KB-W0 36/36, KB-S1 substrate
gate PASS, KB-W2R 12/12 (was 8/12 on H5R, the killed bar), KB-B2R
24/24, KB-W3 8/8 (new two-revision-then-revert provenance-chain
family), KB-B3 24/24, KB-G1R architecture PASS (13 added cognition
lines, budget <= 15, net +9; zero modes/bridges/routers/handlers;
zero ISA additions; cumulative diff net -4 vs TNN-2 base), KB-D1 3/3
byte-identical, KB-P1 pure Zag. Fix: 9-line t2_prov_ok helper in
t2_trial declines candidates whose licensing facts are not all live
tag-1 non-superseded; four promote sites gated in place. Commits:
prereg dc7df4aba, implementation 9db334bd4 (binary 19dcf2e4...),
sealed eval e20ba5402. Seal note: single worker as
coordinator/builder/evaluator; mitigations (seeds, ranges, patterns,
driver template hash f2d60568) frozen pre-implementation. Scope:
revision-provenance hypothesis on the frozen battery only; no broad
generality or L3 claim. [NEW] (debate pending)

**4. ARENA inquiry (C8): BUILD-PASS.** All 9 frozen kill bars pass.
C8 0.000 to 1.000; arena total 54/68 (0.794) to 58/68 (0.853); zero
regressions on the other 15 capabilities; 3/3 byte-identical reruns.
Mechanism: generic ask-observe-answer loop on the v6 base (+69/-3
lines, 0 new modes/bridges/routers/handlers/semantic cases, 0
hardcoded entities/values/answers); UNKNOWN reply plus observe
request naming the missing fact, absorb via learn_fact on
observe_result, exact answer on re-ask. Ablations: ask-off 0/4,
absorb-off 0/4 (both halves causal). L3 explicitly disclaimed (fails
C0-A through C0-D; L1/L2 infrastructure). Commits: prereg 1156add31,
implement 0ddb5e9ce, eval 0218296e0, judge-brief b9245751d.
Caveats: the "15 capabilities" count does not reproduce from sealed
records (16 capabilities, 68 items; flagged, not asserted); canonical
0.573 not moved; remaining sealed zeros C9 causal, C12 transfer, C15
goal; built on v6 base, not the TCNP binary (integration is a later
decision); disclosure: worker incidentally saw observe_result values
during protocol verification, never used (zero-hit grep audit).
[NEW] (debate pending)

**5. ARENA2 transfer-by-recoding (C12): BUILD-PASS.** All 8 frozen
kill bars PASS. C12 0.000 to 1.000; arena total 0.794 to 0.882
(60/68) on the v6 base; zero regressions on the other 15
capabilities; 3/3 byte-identical. Mechanism REMAP: composes the
learner's own exposure-learned Zem templates with the runtime-parsed
value permutation (no sealed values hardcoded; generalizes to any
permutation/template); 94 lines added, 0 changed, 0 new
modes/bridges/routers/gates/semantic cases. Ablations: prod-off and
class-off each zero exactly their half (both halves causal).
L3 explicitly disclaimed (researcher-authored recoding semantics; L2
transfer infrastructure). Commits: prereg 5a055b575 (alone),
implementation+eval 18309290c. C9 NEGATIVE FINDING (high value): the
worker examined causal first and rejected it with killing evidence:
all 12 causal observations satisfy x==y==z (chain permutation
observationally unidentifiable by design), zero intervention turns in
the battery, discrim items always list the true chain first with key
= chain[0]; the only 3/3 mechanism is question-format parsing
(gaming, rejected); the honest causal answer (UNKNOWN) scores 0.
Recorded with a world-generator fix recommendation (randomize
candidate order; add real intervention turns). C15 rejected (1 item,
narrow enumeration, ordering-fragile). Scope: REMAP is a CANDIDATE
only; canonical 0.573 unmoved; not cumulative with the inquiry
candidate (both built on the v6 base separately; integration is a
later decision). [NEW] (debate pending)

**6. ARENA3 transfer-by-relabeling (C12, on INQ base): BUILD-PASS.**
All 9 frozen kill bars PASS. C12 0.000 to 1.000 (6/6); total 0.853
to 0.941 (64/68); zero regressions on the other 15 capabilities;
3/3 byte-identical. Mechanism TRX: parse_remap helper parses the
4-value segment relabeling from the question (validates permutation
of [0,1,2,3]); remap_prod applies the learned class-A to class-B
position-wise rewrite then the parsed remap; remap_class answers
yes/no against the learned class-A template with remap applied.
Remap always from the question, never source/state. +80/-0 lines vs
INQ base; 0 new modes/bridges/routers/gates/semantic cases; reuses
exposure-induced A/B templates. Ablations: prod-off 3/6, class-off
3/6 (both halves causal). L3 explicitly disclaimed (L1/L2
template-relabeling). Commits: prereg 829208f99 (alone),
implementation 9191e71de, eval records in d51d8ef5b. SIBLING
COLLISION: ARENA2's dir was empty at this lane's start, so it
defaulted to C12 per instructions and recorded the assumption; both
lanes independently built C12 transfer candidates (ARENA2 REMAP on
v6 base: 0.794 to 0.882; ARENA3 TRX on INQ base: 0.853 to 0.941).
Per the frozen collision clause these are independent competing
runs, not duplication; the debate must compare/reconcile the two
mechanisms. Remaining sealed zeros: C9 causal, C15 goal. Canonical
0.573 unmoved. [NEW] (debate pending)

**7. DEVANG3 better segmenter: BUILD-PASS.** Both killing bars
cleared on fresh sealed worlds: K_SEG 12/12 (>= 9/12), K_SEAL 20/20
(>= 12/20); all supporting bars pass (K1 10/10, K_AUD PASS, K_ABL
4/12, K-C0 35pp/7 words, K8 20/20 vs 17/20, K2-K7/K9 7/7, K10-K12
audits + 3/3 identical). Regression on 2021pdt worlds: Family B
12/12 (was 8/12), Family C 11/20 (unchanged, no regression). Root
cause: the novel-segment score -50 + ilog(L+1)*5 contained a length
bonus rewarding novel+known merges (probe 9 exact tie); flipped to
linear length penalty -50 - 1*L. Exactly ONE cognition line changed
(plus comments); no new tables, modes, bridges, handlers, semantic
cases; C0 control untouched. Commits: prereg 5b7e55706 (alone),
implementation 126ef2600 (binary 36f5047d...), sealed package
ead6f006c, eval 11026f43b, judge-brief a29d4088c. Caveats: single
worker, no independent adversary (mitigated: fresh vocab/episodes,
blind generation, hashes pre-run, no inspection between); C2
fixed-width-3 also scores 20/20 on fresh Family C (discrimination
via K_SEG 12/12 vs 4/12 and K8); pre-prereg tuning explored and
dropped (confined to /tmp). [NEW] (debate pending)

**8. ARENA4 C15 roster: BUILD-PASS.** C15 is genuinely achievable,
NOT broken by design. The ARENA2 rejection reason
"ordering-fragile" is factually wrong: the frozen scorer (hash
matches refreeze) scores cap 15 as order-insensitive set F1 (sc =
2000*inter/(ne+nr) over comma-split names), not exact match. 9 of
10 entities are observable in exposure turns (verified: "Segunu"
occurs 0 times in exposure.jsonl); an experience-based roster
scores 2000*9/19 = 0.947 in any order. Unlike C9 (only gaming
passes), C15 is passable by a general mechanism: a persistent
entity roster in learner state enumerated to satisfy the stated
goal. Built on the v6 base (roster orthogonal to TRX/INQ): ROSTER =
entity roster (12x16B slots) populated from learn_fact/learn_rel
exposure events only (no briefing reads, no sealed strings), plus a
listnames question handler in the existing test-turn dispatch, plus
a white-box decision trace. Sealed results (68-item battery, seed
71503461337030), all 8 kill bars PASS: K1 C15 0.947 >= 0.900 (was
0.000); K2 zero regressions (all other 15 capabilities
byte-identical; total 54.947/68 = 0.808); K3 3/3 byte-identical; K4
pure Zag; K5 tool/world/key hashes all match refreeze; K6 ablation
causal (roster off -> C15 0.000, others unchanged); K7 164 lines
added, 0 changed, zero new modes/bridges/routers/gates/semantic
cases; K8 L3 disclaimed. Commits: 19d9edc87 (prereg freeze + audit,
no implementation) -> 171c45101 (implementation) -> f8d7b9b2e
(sealed eval + judge brief); commit-order self-check satisfied.
Flags: (1) 15-vs-16 discrepancy (sealed records govern: 16
capabilities, 68 items); (2) battery limitation: 0.947 is the honest
experience-based ceiling (Segunu never observed); the implemented
C15 is a single probe while the prereg spec described autonomous
goal completion with tools (future battery work). [NEW]

**9. H7R substrate re-attempt (contradiction-driven re-derivation):
BUILD-PASS.** The trigger + construction service suffice for genuine
contradiction-driven re-derivation; no SUBSTRATE-INSUFFICIENT gap
encountered. The learner-side REDERIVE consumer identifies
superseded vs new fact via the substrate's own ET_CON signal, finds
the stale BUILD ticket, and authors a copy of the stale ticket's
steps with literal re-resolution (superseded value -> new value);
the sealed driver never authors tickets (literal grep = 0). Numbers
vs frozen bars (12 contradiction cases, 3 sealed worlds x 4, values
chosen post-freeze): B1 PASS (exactly one REDERIVE ticket per
contradiction, linking superseded + new fact); B2 PASS (held-out
probe: 12/12 re-derived roots return the corrected answer, 100pp
margin over stale); B3 non-treadmill PASS (t2_sig differs 12/12);
B4 ablation PASS (stale roots stay stale 12/12 without the rebuilt
graph); B5/B6 PASS (confirms trigger zero tickets/authoring; 6/6
distractor contradictions consumed with zero BUILD tickets); P1 PASS
(3/3 byte-identical); P2 K-C0A PASS (zero new semantic cases; no
world constant in any conditional test outside scoring; no new
node/edge/relation types). Commits: 144deb24a (prereg alone) ->
11eb54f6f (implementation + sealed eval) -> f1cd443fa (judge brief).
Cosmetic issue handled transparently (driver header comment tripped
the authorship grep; reworded, rebuilt, re-ran 3x byte-identical).
No L3 authorship claim made. The H7R record states "Substrate halves
now 3/3 passing (H2R, H6R, H7R)". [NEW]

**10. F2V3 (F2 v4 depth-9 candidate): BUILD-PASS.** All eight frozen
kill bars (K4-R1 through K4-R7, D2=9 restated in PREREG_F2V4.md)
PASS in both fresh sealed worlds (A-prime confounded chain,
C2-prime dual contextual delay), 3/3 byte-identical reruns per
world, no regressions on the retired 2021pdt worlds. The fix from
the v3 BUILD-FAIL: raising the DPDS discrimination bound from 8 to
9 (one constant plus the buffer capacity it requires:
discrimination sequence buffers 8 -> 10 slots, ledger record
48+nhyp -> 50+nhyp; no mechanism change). Non-vacuity confirmed on
the v3-frozen binary (C2-prime yields genuine depth-9 candidates; v3
terminates by exhaustion with the D2 certificate for the crossed
pair). Commits: 5e4e56a5f (prereg) -> b5fcf9ae3 (implementation) ->
30a1ff7e0 (sealed eval + judge brief restoration) -> d0846df90
(judge brief). Sealed binaries sha256-verified. Pure Zag throughout.
[NEW]

**11. ARENA5 autonomous C15 goal completion (DEFRECALL): BUILD-PASS.**
All 8 frozen kill bars pass on the fresh 68-item battery (seed
71503461337032). DEFRECALL removes ARENA4's dedicated listnames
handler and replaces it with a generic default action at the v6
fallback position: when no specific question handler matches AND the
question is a bare prompt (no | parameters), the learner volunteers
its persistent knowledge state (the experience-built entity roster,
comma-joined); parameterized questions with no handler keep
replying UNKNOWN (preserving frozen scorers that reward honest
abstention). Zero references to the goal string "listnames"
(grep-verified); zero branches keyed on any question/goal string;
roster extracted verbatim from ARENA4's recorded commits. K1 C15
0.947 >= 0.900 (all 3 runs); K2 zero regressions (54.947/68 =
0.808); K3 3/3 byte-identical; K4 pure Zag; K5 hashes match refreeze;
K6 ablation causal (roster off -> 0.000; default-action-disabled
with roster on -> 0.000, proving the default action is the
goal-completion path); K7 174 lines added, 0 changed, zero dedicated
goal handlers, zero modes/bridges; K8 L3 disclaimed. Dev generality:
novel bare prompts ("recall", "who") enumerate the roster; novel
parameterized prompts reply UNKNOWN. Honest caveats: (1) on this
battery the default action is extensionally equivalent to a
listnames handler (C15 probe is the only bare prompt); generality
rests on intension, flagged for the judge; (2) the battery still
expresses the goal as a test-turn bare prompt; multi-step tool
protocol remains unimplemented; autonomy demonstrated is
handler-free goal completion, not tool use. Commits: b63f80289
(prereg) -> f3320caf8 (Amendment 1: seed validity rule) ->
2320c3454 (implementation) -> 6582398e9 (sealed eval + judge brief).
[NEW]

**12. F1-FOLLOWUP Part 1 (narrowed re-test + constructor
seed-sensitivity): BUILD-PASS (new candidate; explicitly NOT a
verdict change to the F1 BUILD-FAIL).** Windowed trigger passes all
frozen bars on validated fixtures; K-C0C-REG Leg W2: new binary
reproduces old binary's behavior EXACTLY on the prior wave's W2
fixtures (same TRIGGER episode 1, byte-identical normalized
CONSTRUCT sequence via pure-Zag cmp_events, identical [4 4 4 2]
structure, hidden 30/30 both, byte-identical hidden preds); zero
trigger regression; 24 invocations x 3 reps byte-identical.
Commits: 001fcfaca (Part 1 prereg) -> 6dee24671 (Part 2 prereg) ->
34960a9bc -> 63922a500 -> 27116eb12 -> 728e114f2; commit-order
holds. Disclosure: awk used only for mechanical text extraction
(safebin-allowlisted); all research logic in frozen pure-Zag tools.
Bounded L2+ ceiling stands; no L3 claim. Part 2 verdict: NOT-FOUND
(separate outcome group below). [NEW] (debate pending)

### 1b. BUILD-FAIL (2)

**13. F1 interleaved-error trigger: BUILD-FAIL.** Tripped bar:
K-C0C-REG on R-W2 (0/30 hidden < 80% frozen threshold); bar not
weakened. Built: generic windowed failure-density trigger (fire when
>= 2 of last 8 truth-episodes are prediction failures; strict
superset of the old K1=2 consecutive trigger; zero researcher-authored
semantic cases per K-C0A audit). Trigger bars all PASS: fires on all
4 interleaved patterns (old trigger: 0 fires), 0 false positives on
3 clean worlds, 30/30 learning on interleaved streams, ablations
57pp/57pp. Killing evidence: R-W2 trip is a PRE-EXISTING constructor
limitation, not a trigger regression: the prior wave's frozen binary
on the same sealed fixtures converges to the byte-identical overfit
structure and scores 0/30; the new binary on the prior wave's exact
W2 fixtures reproduces it perfectly (TRIGGER at ep 1, same 3
constructs, 30/30, identical [4 4 4 2] structure). Worker honestly
owns a bar-calibration mistake: its K-C0C-REG bar used an unvalidated
fresh seed, conflating trigger regression with constructor
seed-robustness. Commits: prereg 50de69403, implementation ba5ebbf8b
(binary 6f2b155b...), sealed eval 3b159b401, judge-brief 14fdf441d.
Debate to adjudicate: BUILD-FAIL vs PARTIAL-narrowed (trigger re-test
on validated seeds; constructor seed-sensitivity as separate
finding). [NEW] (debate pending)

**14. H6R substrate re-attempt (standing/accumulation): BUILD-FAIL.**
B1 (trajectory discrimination) PASS; B2 (integration) PASS; B3
(sealed probe prediction, 4 worlds x 20 probes = 80) KILL FIRES:
accT = 50/80, accC = 50/80, margin = 0 points (bar >= 15), exactly
as the frozen H6R-B3-nil theorem predicted; B4 (retention)
SUBSTRATE-INSUFFICIENT with the exact gap: standing values live on
kind-904 record nodes that are never protection-pinned (no ref_prot
call in ls_touch; only facts and roots are pinned) and carry lbid 0
(value in field 24, invisible to the lbid selector; only in-edge is
the type-10 root link, which bid does not count); the adopted
evict_node selects argmin lbid over unprotected live nodes, so it
always evicts standing records before any fact node (sealed
evidence: B4-W1 first real eviction = node 6, nH's standing record,
not nF); evicting a record destroys that node's standing, so no
world can express "high-standing nodes survive preferentially"; the
package pins roots but not records. P3 3/3 byte-identical; P4 K-C0A
zero new semantic cases. Kill bars KB-H6R not weakened. The standing
package unblocks H6's accumulation and integration bars but cannot
beat the no-standing baseline on probe prediction and cannot
express preferential retention. Recorded as a crisp substrate design
gap for the governance record (TNN3-SUBSTRATE adoption pending).
[NEW]

### 1c. Validated / instrumentation / analysis (7)

**15. Fork battery: 59 refs (53 local, 6 remote); 2 FRESH PASS
(tnn-native-lab @ 3dceac9cc moved tip; new archive ref
tnn-native-lab-wave-archive-wave-20261001-2021pdt @ a272a8f6); 55
RE-CERT PASS; 2 RE-CERT UNTESTABLE (rh-pull-1-head, rh-pull-2-head,
standing cause); 0 FAIL.** Archive immutability: 47/47 pre-existing
tips byte-identical, plus 1 new ref fresh-tested PASS (48/48).
Frozen pins verified (znc 498abcb5..., probe 3b29aa06..., b1_run
5dfe3c16..., b2_bin 75b85d3c...). Commit 668ae8d8f. [NEW] (debate
pending)

**16. H5R2-REPRO (independent reproduction from committed source):
REPRO-PASS.** Every number in SEALED_EVAL_H5R2.md reproduces exactly:
sources extracted via git show match lane hashes (tnn3_h5r2.zag
04f8e213..., DRIVER_TMPL.zag f2d60568... matches prereg hash);
independent rebuild 3x byte-identical, SHA-256 19dcf2e4... matches
the frozen binary bit for bit (lane .bin never copied); all four
sealed world hashes match SEALED_H5R2.md; 12 re-runs byte-identical
within worlds, all full-stdout hashes match KB-D1 exactly.
Comparison table: KB-W0 36/36, KB-W2R 12/12, KB-B2R 24/24, KB-W3
8/8, KB-B3 24/24, KB-S1/KB-G1R PASS re-verified on extracted files
(9-line helper + 4 gate sites, no modes/bridges/handlers/ISA
additions), negative controls none fired. Commit order: prereg
dc7df4aba < implementation 9db334bd4 < sealed e20ba5402, strict
ancestor chain, no UNVERIFIABLE ORDERING. Commit 8b30769de. The
H5R2 BUILD-PASS verdict survives independent re-execution (pipeline
step 4). [NEW]

**17. CONSEQ shared consequence substrate (Node2-v2 K-H3):
VALIDATION-PASS.** Independent re-execution of frozen Node2-v2 K-H3
prereg (4b05c8011): 5/5 frozen kill bars PASS, 3/3 byte-identical
reruns, hashes match committed records bit for bit. Causal ablation
Link 1 (consequence record disabled): default reverts to fixed 30,
NECESSARY confirmed. Causal ablation Link 3 (production read
disabled): write fires but guide stays 30, NECESSARY confirmed.
K-H3 disambiguation: single lineage (H3LITE_DESIGN.md Sec 6 draft ->
frozen H3-lite Node 2 unreachable -> Node2-v2 prereg), no conflict.
Scope honestly held: validates the consequence re-entry template,
not the shared tag-61 substrate itself (C174 remains EMERGES,
exploratory). Commits e068ac9a4 (+ lane files). [NEW] (debate
pending)

**18. C174 shared tag-61 consequence store: VALIDATION-PASS.**
All 5 frozen kill bars pass; the store graduates from EMERGES
(exploratory) to validated-on-frozen-bars as infrastructure. (a)
STORE-SERVES-TWO PASS: W-REORDER 121 writes / 294 reorder reads,
W-RETIRE 28 writes / 10 retention + 15 utility reads, same store,
consumers only via sub_consec. (b) BEHAVIOR-CHANGE PASS: reorder S
[0 5 1 2 3 4] vs fixed [3 0 5 1 4 2] (63 vs 103 attempts); retention
victims S [7 0 1 6 5] vs F [4 8 3 9 7], held-out answerability 6/6
vs 3/6. (c) ABLATION-CAUSAL PASS: A == F byte-for-byte (de193b84,
3x each), S differs (6c33f7c4); disabling the store reverts every
judgment to the fixed baseline, mirroring CONSEQ Link 1. (d)
MIGRATION-COMPAT PASS: M1 reproduces the CONSEQ K-H3 trace exactly
(30 30 30 30 30 45, guide 45); M2 byte-identical; MIGRATION_MATCH 1.
(e) DETERMINISM PASS: 3/3 byte-identical all six binaries. Commits:
prereg 134af1cb2 -> implementation b5e0274f7 -> seal 0096b30ca
(world_sealed.zag e66dab44, before any eval) -> eval 3028240e4;
prereg-first order honored. Disclosed fix (not a bar move): after
the seal, removed the C174_EVAL arm= metadata line from eval stdout
(it made bar (c)'s whole-output SHA comparison vacuous); no
prereg/world/logic changes; documented in EVAL_RESULTS.md. Honest
scope: dev-harness validation of the store as infrastructure, not
TNN-2/TNN-3 integration; reclamation exercised only in selftest;
thresholds/weights are researcher scaffolding; migration boundary
documented (per-value counters and shift register coincide only on
non-interleaved worlds); no L3/FW1-FW9/generality claims; broader
worlds untested. [NEW] (debate pending)

**19. C9BAT corrected causal battery generator: GEN-PASS.** All 8
frozen kill bars pass on the dev battery (SEED_DEV=777001337, N=24
worlds): G1 gamer old-exploit 0/24; G2 reference experimenter
(two-stage interventional protocol) 24/24; G3 3/3 byte-identical
generation; G4 genericity (0 chain-string literals in c9gen.zag); G5
pure Zag; G6 positional rules 11/24 and 13/24 (true chain first in
11 items, second in 13; no positional rule hits 24/24); G7 honest
UNKNOWN 0/24; G8 scope honesty documented. Generator: 24 worlds/seed,
uniform true chain from all 6 permutations of (X,Y,Z), 400 noisy
observational turns (edge flip p=0.05), 120 do() turns (60 on X, 60
on Z) each followed by intervened-outcome turn, one discrim question
with true chain + uniform random alternative in seeded coin-flip
order. Two bugs found and fixed pre-validation (arena LCG bit-0
degeneracy on binary draws: fixed via rng_bit; Fisher-Yates reaching
only 3/6 permutations: fixed via transparent prereg amendment A1,
mod-6000 uniform index; no kill bar moved). Commits: fd3d23c3a
(NAMECHECK) -> 9e2ea47fc (prereg alone) -> 4dc4a6d02 (implementation)
-> c2448aa0b (amendment A1 + RNG fixes) -> 3e66b3409 (validation).
Frozen arena battery never touched. Scope honesty: C9GEN is a
CANDIDATE instrument for a future wave's governance decision, not a
replacement; the 24/24 is evidence about the instrument (admits a
genuine experiment-driven solution), not evidence any learner is
causal in general; no L3/substrate/score claims. [NEW] (debate
pending)

**20. ARENA-BLIND (E3-mandated blind re-examination of ROSTER):
ORACLE-FREE (ARENA4 BUILD-PASS stands).** Executed the BATTERY-E3
mandate for the ARENA4 ROSTER mechanism (C15 0.947). Froze a prereg
alone first (0b95a6601), then audited the arena battery's query
mechanism against six frozen criteria (A1-A6) using only committed
sources. Findings, all PASS: A1 the 72 sealed test turns carry
exactly {turn, kind, item, cap, q}; zero carry any exp/answer/key/
oracle/expected field (the listnames turn is
{"turn":117,"kind":"test","item":63,"cap":15,"q":"listnames"}); A2
the run driver passes the contestant one turn JSON + state dir per
turn; the answer key goes to the scorer only; A3 the frozen
turn-protocol contract defines test turns as (item, cap, q) with no
expected-answer field; A4 the frozen ROSTER source (171c45101)
parses only item/cap/q (item/cap echoed into the reply envelope for
scorer mapping, never cognition inputs; the listnames handler reads
only the learner-state roster); A5 zero verifier-with-expected hits;
no candidate set and no selection step exist, so the E3 failure mode
(oracle selection among multiple executable chains via a
QUERY-carried expected value) has no structural analogue: ROSTER
generates exactly one candidate (the roster enumeration); A6 ROSTER
never emits OBSERVE requests. Per the frozen decision rule,
ORACLE-FREE means the masked re-test branch is not triggered: the
C15 claim never rested on unmasked QUERY evidence. The E3 mandate is
satisfied for ROSTER by this audit. Commits: 0b95a6601 (prereg) ->
c2eb08c2a (audit + verdict). Pure Zag throughout. [NEW]

**21. BATTERY-CLUSTER shared-cause analysis of the post-freeze 1/6:
COMPLETE.** Two clusters cover all 8 failure signatures; nothing
unclusterable (PF-A2 caveat recorded as a methods note, no verdict
weight). Cluster 1 DERIVATION SUBORDINATION ("the flat layer always
wins"): PF-A1, PF-C1, PF-C2, v3-M1, v3-M3. Shared cause: frozen
TNN-2's answer/revision operators resolve through a flat
instance-fact layer with no privileged standing layer for derived
structures (taught fact preempts traversal; direct-fact contradiction
shadows instead of revising; revisions patch instances only so shift
patterns cannot transfer; v3 M1 0/8 composition with EVIDENCE
count=0; v3 M3 per-instance structures, generalization 0/2).
Cluster 2 GUIDE CONTENT DECOUPLING ("the presence bit"): PF-B1,
PF-B2, v3-M2. Shared cause: ACT reads uncertainty guides only as a
presence/absence bit (baseline 0 becomes 30 with a live guide); guide
content, count, and resolution state have no write path into action
selection. 8 hypotheses (4 per cluster), each with H/E/D; at least
one general-substrate hypothesis per cluster. A possible deeper
cross-cluster root (no derived learner representation has a
privileged channel into behavior operators) stated as a falsifiable
hypothesis, not assumed. Top-3 discriminating experiments by
information gain: E1 licensed-structure inspector for
composition/law (tests H1c: "derived structure absent" vs "present
but subordinated" across all of Cluster 1 in one run); E2
single-guide content discrimination (tests H2a vs H2b); E3 blind
composition probe with oracle withheld (tests H1d; a collapse to 0/2
reframes every construction claim). Then E4-E8 within-cluster
discriminators. All frozen-binary compatible, pure Zag,
prereg-first. No patches proposed (no-patch-treadmill rule honored);
Criterion 0 not met, no L3 language. Commits: 55ee13a1c (NAMECHECK
+ CLUSTER_ANALYSIS.md), 335b169ae (JUDGE_BRIEF.md). Next: E1
execution dispatched as BATTERY-E1. [NEW]

### 1d. Battery v3 validation (1)

**22. BATTERY Part 1 (v3 validation): VALIDATED.** Battery v3 (6
triviality-review corrections as base invariants; K-S11v3(d)
tightened; v2 M2-W2 fresh-state protocol) VALIDATED on frozen TNN-2:
all process bars PASS, all calibration gates pass, all 9 mechanism
bars FAIL with the predicted degenerate signatures (M1 0/8
composition; M2 constant CHOICE 30; M3 stale 53209/53803). No
defects; v1/v2 kills corroborated on fresh instances. Commits:
prereg f7f8f5e3b, impl+validation a42a113aa. [NEW] (debate pending)

### 1e. Discriminating-experiment results (12)

**23. BATTERY Part 2 (post-freeze sealed adversarial battery):
1/6 PASS.** Owner's standing order; six worlds 60000-69999,
materially different from FW1-FW9/v3, each adversarial to its
mechanism; prereg 59e029102, impl+runs e7a1d4217. PF-A1 FAIL
(retrieval shadows construction: returned taught wrong answer 60999
over constructed 60902); PF-A2 FAIL (bar; caveat: world weakly
discriminates, 2/2 via BFS+oracle traversal not selective
abstraction); PF-B1 FAIL (no selective resolution under concurrent
guides; pre=post=30); PF-B2 FAIL (no discrimination under guide
flood; 30,30,30); PF-C1 PASS (1/1, but via direct-fact shadowing,
not graph revision: recorded); PF-C2 FAIL (revision does not transfer
across relations: revised 1/1, transfer 0/1). Mechanism verdicts:
(a) runtime executable-graph construction FAILS; (b)
learner-originated uncertainty to guide to action FAILS; (c)
counterexample-driven revision FAILS. Mechanism-targeted evidence
only; no L3 claim (Criterion 0 not met); FW1-FW9 stays
regression-only. Per the no-patch-treadmill rule this is NOT six
patch requests: failures go to shared-cause clustering with 3+
structurally different hypotheses per bottleneck before any repair
lineage (BATTERY-CLUSTER lane dispatched). [NEW] (debate pending)

**24. H5R2-BASELINE (pipeline step 5, simple-baseline comparison):
BASELINE-MATCHES via (a) REVERT-TO-LATEST.** Honest informative
result, not hidden. Per-baseline per-bar on the same four sealed
worlds (3/3 byte-identical): (b) NO-GATE reproduces the H5R kill
exactly (KB-W2R 8/12, KB-W3 0/8; byte-identical to the killed H5R
base d98d08f0; the fix matters for provenance, not answers); (c)
RANDOM-ANCHOR chance-level (W2R 8/12, W3 4/8; arbitrary anchoring
does not suffice, discipline must be systematic); (a)
REVERT-TO-LATEST (recency heuristic, no provenance gating) matches
H5R2 on EVERY bar (W0 36/36, W2R 12/12, B2R 24/24, W3 8/8, B3
24/24), violating CB-2. So the t2_prov_ok gate is NOT shown
necessary by these four worlds. Honest cost of (a) disclosed:
built-in battery regresses to 45/46 (F2 FAIL: masked-query
disambiguation now prefers the most recently taught chain); H5R2
holds 46/46. This bounds the H5R2 claim: it beats no-gate and
random, but recency matches it here. Recommended next experiment
(dispatched as H5R2-DECOY): the battery lacks the discriminating
world, one where the newest fact is NOT the live one (decoy OBSERVE
on an unrelated key after the revert); the gate should anchor
correctly there while recency anchors to the decoy. Commits: prereg
28cbe5877 (alone), implementation 1203b865d, sealed eval 6a7c73816,
judge-brief fc2f910e5; commit order strict. Git-race disclosure:
fc2f910e5 swept in six F1-BUFFER files staged by a concurrent
worker (safely committed; attribution blurred, no data lost). [NEW]
(debate pending)

**25. H5R2-DECOY (decoy-OBSERVE discrimination): DECOY-DISCRIMINATES.**
All five frozen kill bars hold. The t2_prov_ok provenance gate is
shown NECESSARY against the recency heuristic: on 8 decoy probes (2
worlds x 4) where the newest fact is NOT the live one, H5R2 anchors
every revert MAP's DEP edges to the live (older) fact 8/8, while
REVERT-TO-LATEST anchors to the decoy on 8/8 (the pre-registered
failure signature; white-box sample: H5R2's DEP lands on node 36,
the live reverted fact on K, sup=0; recency's lands on node 28, the
decoy fact on K2, sup=0). Controls: NO-GATE 0/8 (stale-anchor
D-DEP-FAIL, its baseline failure mode), RANDOM-ANCHOR 2/8. Decoy
fact itself answerable on all arms (DB-5: no adversarial-by-brokenness).
Value answers correct on all arms everywhere: the discrimination is
provenance-only, exactly as predicted. 3/3 byte-identical per world.
Interpretation: BASELINE-MATCHES is RESOLVED, not contradicted.
Recency explained the four-world battery only because there the
newest fact happened to be the live one; the gate's necessity was
untestable there and holds here. Commits: prereg 51a4fe8e1 (alone)
-> 4511f5c64 (implementation) -> 12d69043f (sealed eval + judge
brief) -> 2a4c0ff3f (RENDER_SHA fill). Arm sources extracted
read-only and hash-verified; key ranges 87xxx-88xxx disjoint from
all prior batteries. Recommended next (dispatched as
H5R2-SKEPTIC2): a stronger skeptic baseline (gates on liveness but
not supersession, or "newest live fact") and scaling the decoy
family to W3-style chained decoys. [NEW]

**26. F1-BUFFER (trigger-time-buffer prediction test):
BUFFER-NOT-PREDICTIVE.** 24 fresh sealed sum2 worlds (8100-series
seeds), 3/3 byte-identical per seed, frozen F1 binary hash-verified.
Overfit rate 8/24 = 33 percent with the same catastrophic signature
as the 5100-series (overfit seeds score 0 to 10 percent hidden
accuracy). Frozen rule (predict OVERFIT iff T(B) >= 12)
misclassifies 7/24 fresh seeds against the frozen bar of at most 2:
the rule has no predictive power out of sample (worse than the 5/24
on the training series). This is the informative reference outcome
named in the prereg, reported fully. Mechanistic refinement: the
first-trigger buffer fully determines the greedy burst's second
construct (verified: 5100-series seeds 6 and 18 share the exact
first-trigger buffer multiset and take identical first two
constructs, including the degenerate re-add), but the final OVERFIT
vs CORRECT outcome is decided by later-trigger repair dynamics over
the subsequent episode sequence (seed 6 repaired by a later
full-buffer trigger; seed 18 stalls). The F1-FOLLOWUP hypothesis is
therefore refined, not confirmed: trigger-time buffer mass predicts
the greedy second step, not the final overfit. A trigger-time policy
that only sees buffer mass cannot fix the failure; any fix must
address the later repair dynamics or the greedy depth-1 trial itself.
Dispatched as F1-REPAIR. Commit 451823613 (also swept in this record
line via the standing staging race; no data lost). [NEW]

**27. F1-REPAIR (repair-dynamics discrimination): GREEDY-CONFIRMED
per the frozen decision rule, WITH a trace-verified nuance that
strengthens the repair story.** 24 fresh 6100-series sum2 worlds
(frozen binary hash-verified, 3/3 byte-identical, 0 NOTRIG):
overfit 6/24 = 25 percent, all 6 D-seeds (degenerate-path:
first-trigger burst's second construct adds no complementary
feature). Frozen signature (REPAIR-BURST = TRIGGER at t > T1 with
buf=8 whose burst drives trial-buffer error to zero): S=1 on seeds
12, 15, 17, 20 (all CORRECT). 6 counterexample pairs (seed 10:
deg=1, S=0, CORRECT 30/30, vs seeds 3, 4, 5, 11, 13, 22: S=0,
OVERFIT) force GREEDY-CONFIRMED per the frozen rule. The crucial
nuance (post-hoc, trace-verified): the counterexample refutes the
frozen signature's buf=8 clause, NOT the repair story. Seed 10's
trace shows TRIGGER 3 on a PARTIAL buffer (buf=4) running a burst to
err_after=0 (16->12->6->0), revising its degenerate doubling into a
correct structure; none of the 7 S=0 OVERFIT D-seeds has any later
burst reaching zero on any buffer size; no non-degenerate seed has
any later to-zero burst. Under the relaxed signature S-prime (later
burst to zero, any buffer size): 11/11 on fresh 6100 + 9/9 on 5100
training = 20/20 degenerate-path seeds, repair-to-zero iff CORRECT.
H-GREEDY's gloss ("repair is epiphenomenal") is UNSUPPORTED: seed
10's first two constructs are the degenerate doubling, identical in
form to OVERFIT seeds 3/4/22; the later repair burst, not the greedy
trial, explains its CORRECT outcome. The buf=8 clause was overfit to
5100 calibration (all training repairs happened to be full-buffer).
Recommended next (dispatched as F1-REPAIR2): fresh prereg on the
relaxed repair signature S-prime, then a repair-time policy
experiment (what makes a later burst run to zero vs stall); NOT an
attack on the depth-1 trial. Commits: b4afb6236 (prereg alone) ->
fadaee3fb (implementation) -> cbded055d (fixtures) -> 5935c5169
(sealed runs) -> 4c253fb36 (judge brief). [NEW]

**28. F1-REPAIR2 (S-prime confirmation + repair-time policy):
REPAIR2-CONFIRMED.** 24 fresh sealed 7300-series sum2 worlds (frozen
F1 binary hash-verified, 3/3 byte-identical, 0 NOTRIG). Overfit rate
4/24 = 17 percent. Part A (S-prime on degenerate-path seeds): D = 7
seeds; S-prime=1 on 4 (all CORRECT), S-prime=0 on 3 (all OVERFIT);
misc_D = 0 <= 2: PASS. S-prime now holds on 27/27 degenerate-path
seeds across three series (9/9 5100, 11/11 6100, 7/7 7300). Part B
(POLICY-R repair-time policy): mispredicted on 2 seeds (11, 19),
misc_B = 2 <= 4: PASS; both violations on non-degenerate seeds,
precisely bounding the policy's scope (seed 11: clean inherited
accumulator completes without a doubling; seed 19: a doubling-first
burst stalls when the post-reset buffer favors the degenerate second
move). K-C0A PASS; commit order strict (prereg b4dfa3f32 ->
implementation 6bc6483c3 -> fixtures fed95fc76 -> sealed eval
466bcee03). Decided: S-prime confirmed as the repair signature on
fresh worlds; POLICY-R characterizes typical degenerate-path repair
dynamics within its stated boundary. Not decided: no fix proposed
for the F1 line; POLICY-R is a mechanism characterization, not a
repair patch. [NEW]

**29. BATTERY-E1 licensed-structure inspector: E1-FIRSTCLASS (H1c
killed).** The inspector found licensed derived structures in frozen
TNN-2's white-box state: E1-W2 (derived-fact contradiction) shows
DERIVED=1, BYPASS=1 (one persistent structure with both chain hops
licensed and an answer never taught; it survives the contradiction
untouched while the bar probe returns the flat fact: the clean
"present but subordinated" signature); E1-W4 (clean composition)
shows DERIVED=1, FIRSTCLASS=1 (two licensed structures with answers
never taught; probes return them). E1-W1 (construction vs retrieval)
shows STRUCTURES 0 (the flat layer answers with no persistent
structure at all); E1-W3 (cross-relation transfer) shows two
single-evidence per-instance structures and no law-level derived
structure (DERIVED=0). Per the frozen rule (D={W2,W4}, W4
FIRSTCLASS=1), verdict E1-FIRSTCLASS. This was a prereg prediction
miss (predicted E1-ABSENT), reported plainly. What it decides: H1c
as stated ("no standing derived structure exists at all") is KILLED
by white-box evidence. Cluster 1's shared cause refines from "no
derived structures" to "derived structures exist but have no
privileged standing in the read path; the flat instance-fact layer
is consulted first and wins"; the DERIVATION SUBORDINATION cluster
name is vindicated as the deeper cause. H1a (read-path precedence
inversion) wins for W1/W2; W3 supports H1b (instance-only write
path). One recorded confound: W4's behavioral leg cannot distinguish
structure-driven answers from oracle-verified BFS traversal (PF-A2
caveat property), reserved for E3/H1d. No repair proposed; Criterion
0 not met, no L3 language. Commits: 793abbf65 (prereg alone) ->
aa38427b8 (worlds) -> 4afcd9f3b (inspector/controls; v3 cross-check
identical) -> f5b1bab41 (runs + judge brief). Dispatched BATTERY-E4
as the within-cluster discriminator for the refined cause. [NEW]

**30. BATTERY-E2 single-guide content discrimination:
E2-CONTENT-BLIND.** Two materially different single guides, each run
in isolation with zero concurrency, produce byte-identical CHOICE 30
actions on frozen TNN-2 (E2-A transcript hash 27544c08, E2-B
5229a8c2; 3/3 byte-identical per world). The degenerate control (ACT
on empty state) yields CHOICE 0, so the presence bit reads correctly
and the A/B comparison is calibrated. The constant-guide story is
NOT a concurrency phenomenon: this confirms H2a (absent content
channel at the guide-to-ACT interface) as the root cause of Cluster
2 and kills H2b (concurrency collapse) for this instrument. Process
bars all PASS (prereg alone 229cf5263, commit order strict,
determinism, frozen-binary hashes, seal integrity, block
calibration, anti-smuggling, K-C0A zero new semantic cases).
Commits: 229cf5263 -> 4900c177d -> 6c9d96cef -> 524eca821. No patch
proposed; decided evidence for the BATTERY-CLUSTER analysis.
Recorded limitation: the QUERY oracle value is present per PF
protocol but the ACT channel has no answer path, so oracle echo is
structurally excluded as an explanation. Remaining within-cluster
discriminators: E6 (guide-store lifecycle inspector, H2c) and E8
(ACT output bandwidth probe, H2d); E7 loses its H2b rationale given
this result. Dispatched as BATTERY-E6. [NEW]

**31. BATTERY-E3 blind composition probe, oracle withheld:
E3-ORACLE-DEPENDENT (debate priority).** The refined H1d is
SUPPORTED; the naive H1d is false. Blind E3B (discriminating,
spurious-first adversarial): 0/2, outputs exactly the pre-registered
spurious composites [80971, 80972] vs sealed targets [80921, 80922];
the white-box inspector confirms the blind trial runtime-assembled
GUARD/SETREG chain graphs with ET_DEP provenance to the taught
spurious facts, promoted them as MAP nodes, and executed them.
ASSEMBLY WORKS BLIND; SELECTION DOES NOT. Oracle-present E3B: 2/2.
Blind E3A bar probes: 2/2 (calibration: blind graph assembly
intact); distractor probes spuriously composed (the trial enumerates
chains relation-agnostically). Interpretation: the trial's correct
compositions depended on the unmasked verifier (t2_try_verify:
accept iff output equals the QUERY-carried expected value) to SELECT
among multiple executable BFS chains; without the oracle, masked
mode emits the first-executable chain. This REFRAMES EVERY PF
CONSTRUCTION OBSERVATION as BFS enumeration plus oracle selection,
not selective construction; every wave construction claim resting on
unmasked QUERY evidence must be re-examined blind. No repair
proposed. Commits: a17a276c8 (prereg alone) -> ce46b327a
(implementation) -> 4f49f8b66 (12 sealed runs + judge brief).
Dispatched BATTERY-E5 as the remaining Cluster 1 discriminator.
[NEW]

**32. BATTERY-E4 precedence-reversal world: E4-PRECEDENCE.** H1a
confirmed as pure read-path precedence (an ordering phenomenon), not
deeper suppression. E4-W0 (control, no flat wrong fact): DERIVED=1,
FIRSTCLASS=1; the licensed derived structure forms cleanly and
drives probes. E4-W1 (precedence-reversal): DERIVED=1, PREFLAT=1,
POST=1; the flat wrong fact 72299 wins pre-contradiction while the
derived structure exists underneath (subordination replicated); after
the licensed contradiction teaches 72295, the decision probe returns
72295 (supersession per the frozen protocol). The inspector confirms
the SAME licensed derived structure (id=13, both-hop evidence)
persists through flat-fact teaching and contradiction with no
degradation; the flat wrong-fact triple leaves no trace in its
evidence. The derived layer is fully intact through the entire
sequence, so its non-use pre-contradiction is attributable only to
read-path ordering (activate before trial); the deeper-suppression
alternative is disfavored. All process bars PASS (prereg b63f80289
strictly first; 3/3 byte-identical; frozen binary hashes; manifest
2/2; K-C0A). Design honesty note (preregistered): the behavioral
SUPPRESSION signature is unobservable because the frozen
contradiction protocol supersedes rather than deletes; the honest
discriminator is the white-box DERIVED leg. Commits: b63f80289
(prereg) -> 5a2c7c91c (prereg restore after incident) -> f26ddb294
(worlds) -> 67680ebb1 (tools) -> 61df738fe (runs + verdict).
Incident: H5R2-SKEPTIC2 worker commit f461e812d accidentally deleted
BATTERY-E4/PREREG_E4.md and NAMECHECK.md (411 deletions); restored
byte-identical before any implementation commit; E4-K1 holds.
Flagged for parent: that worker's git workflow needs review. [NEW]

**33. BATTERY-E5 double-revision law world: E5-INSTANCE-ONLY (H1b
confirmed).** Contradicting two instances of a two-hop derived law
leaves the unseen third instance on the old law (72323) and the
analogous relation untouched (72421), unanimous across 3 fresh-state
runs in both driver conditions. The white-box inspector shows the
contradiction writes landing only in the flat instance-fact layer,
with the per-instance derived structures unrevised and zero
cross-instance aggregation. H1b (instance-only write path) confirmed
at both the behavioral and state levels. All process bars PASS
(prereg ordering, determinism, frozen binary, seal integrity,
no-leak, calibration, K-C0A). Commits on lane-battery-e5 branch:
282c8301e (prereg alone) -> c8d9f14e1 (tools + worlds) -> 8510feee6
(runs + verdict). Process note: worker used a worktree with its own
branch instead of committing to tnn-native-lab; merging to the wave
branch. [NEW]

**34. BATTERY-E6 guide-store lifecycle inspector: E6-CONTENT-READ,
with H2C-STICKY.** Pure-Zag inspector dumped the 110656-byte
workspace across a staged guide-event sequence (2 guides with
distinguishable content, create -> ACT -> resolve -> ACT -> resolve
-> ACT), plus a field-ablation probe (5 classes x 3 chains) mutating
guide-store fields in dumped state and replaying ACT. 3/3
byte-identical reruns; all 5 world files hashed to prereg-pinned
values. Writes: each miss writes one type-30 UNCERTAINTY node
(f20=subject, f24=relation, f28=2) and one type-1 guide node
(f4=subject, f20=30, f24=-999) with DEP guide->uncertainty and MEM
POLICY_ROOT->guide edges. Lifecycle: both resolution OBSERVEs leave
every guide/uncertainty record byte-identical (no retire, update,
unlink, aging, or eviction; only the taught fact node and log
change) on all 3 chains: H2C-STICKY confirmed as decided evidence.
Reads (ablation-established): guide subject field F4 30->0 (read as
recency gate); guide action-value F20 30->0 (read as emitted choice);
uncertainty content UC 30->30 (the (s,r) uncertainty content is NEVER
observably read); presence removal PRES 30->0 (positive control).
Frozen decision rule fired SIGNATURE-CONTENT-READ: the distinguishing
uncertainty content has no read path into ACT; the only content
reaching ACT is the subject tag (gate) plus a construction-constant
action value (30). This REDIRECTS Cluster 2 toward H2d (output
bandwidth); H2a-as-literally-stated ("content never reaches action
selection") is refined, not just confirmed. All process bars PASS
(E6-K1..K6, K-C0A). Prereg erratum handled transparently
(POLICY_ROOT index gloss corrected to the frozen source before any
run; predicate and bars unaffected). Commits: 58811f3a5 (prereg
alone) -> fbe5ab33e (implementation) -> 486c13c5c (verdict) ->
a95e8b05b (RENDER_SHA). BATTERY-E8 (H2d probe) already running as
the follow-up. [NEW]

**35. F1-FOLLOWUP Part 2 (constructor seed-sensitivity, 24 fresh
sealed sum2 worlds, 5100-series seeds): NOT-FOUND.** Overfit rate
6/24 = 25%, cleanly bimodal (overfit seeds score 5,0,2,0,1,0 of 30;
18 correct at 30/30); NO pre-registered whole-fixture property
(F1-F6) separates overfit from correct within the frozen <= 2
misclassification bar (best F6 misc=4); F1's 2301 fixture shares no
cleanly separating property either. Post-hoc mechanistic
explanation (explicitly not the frozen-rule pattern): all 6 overfit
seeds show the greedy second construct re-adding the same feature
(or doubling the accumulator) instead of the complementary feature,
locking into degenerate compositions (3x0+x1, 3x0+2x1, 4x0+x1,
3x1+2x0, 4x1+x0, 3x1+2x0); the trigger fires at episode 1 on all 6,
so the greedy path is decided by the first-trigger buffer's x0/x1
error-mass balance, which whole-fixture features cannot see.
Natural next prereg: trigger-time-buffer features, frozen before
runs. (Note: this led to the F1-BUFFER/F1-REPAIR/F1-REPAIR2 line,
which refined the hypothesis further.) [NEW]

### 1f. Red-team reviews (6)

**36. RT-EXEC (red team: F1, TNN3H5R): EVIDENCE-HOLDS on both.**
Prereg commit-order PASS both lanes (F1 50de69403 < ba5ebbf8b;
TNN3H5R dc7df4aba < 9db334bd4). F1: constructor-limitation
attribution PROVEN STRONGLY (prior wave's frozen binary and new
binary produce byte-identical train states on sealed rW2, same
4-construct all-ADD overfit; trigger cannot be implicated).
Recommendation: UPHOLD BUILD-FAIL (PARTIAL-narrowed rejected: not a
defined verdict in the frozen rules; inventing one post-hoc would be
bar-weakening); accept the windowed trigger per the lane's
judge-brief actions and file greedy-trial seed-sensitivity as a
separate constructor finding (the F1-FOLLOWUP lane is already doing
both as a NEW candidate, not a verdict change). TNN3H5R: H5R2
ADVANCES stands; seal integrity verified (prereg-frozen mitigations
all hold; one procedural blemish: DRIVER_TMPL.zag committed with
the implementation commit, but content binding holds via the prereg
hash f2d60568); mechanism genuine (independent compile+run
byte-identical to frozen KB-D1 record 76e5794c); KB-G1R honest (net
+9, zero modes/bridges/handlers/ISA). Review commit 76b9ee229.
[NEW]

**37. RT-INT (red team: CONSEQ, CONTLEARN): EVIDENCE-HOLDS on both,
no dissent.** Independent verification: CONSEQ re-hashed all reruns
(kh3 74c48d5a 3/3, L1 d67cecf5, L3 0d25a574, all match committed
originals), re-ran committed n2v2_test_bin byte-identical, kill bars
verbatim vs frozen prereg 4b05c8011 (unweakened), prereg precedes
build by 81s. CONTLEARN prereg 408ffdcdc strictly precedes
implementation dfcd3caf, frozen core hash a29972ca verified, driver
audit clean (0 switch/match, 0 alloc/link), re-ran lo_driver
byte-identical both modes, K3 cl_driver re-run 53ff2c99 3/3.
Strongest attacks held: CONSEQ consequence record is a
researcher-written 3-revelation counter but inside frozen claim
bounds; ablations genuinely causal. CONTLEARN masked queries still
researcher scaffolding, honestly disclosed; removing answer keys
kills the key-matching confound but does not escape scaffolding.
Carried qualifications: CONSEQ independent-adversary clause never
met (builder-sealed worlds; this wave confirms reproduction
fidelity, not adversarial validation); CONTLEARN
"LEARNOWN-DEMONSTRATED" label hazard, keep the weak/strong
distinction attached when cited. Review commits f70c676f4,
6c8485fdc. [NEW]

**38. RT-GOV (architecture/governance review of TNN3-SUBSTRATE):
HOLDS on all three axes, one QUALIFY.** Axis 1 ONE-SYSTEM RULE
HOLDS: full 197-line PKG block read; no modes/bridges/routers/
task-specific handlers; ticket admission gates on structural
vocabulary (-41 + pending), one two-pass code path for all tickets,
data-driven spec decode with zero semantic validation;
BUILD_ROOT/STAND_ROOT follow frozen POLICY_ROOT conventions.
Axis 2 ISA RULING HOLDS: frozen tnn2.zag hash a29972ca re-verified;
PKG calls only pre-existing functions; 0 new opcodes;
forbidden-class audit of all 14 functions clean; 197-line count
honest. Two disclosed residuals: (a) ls_bump +1/-1 polarities are
researcher constants; (b) lbid record-wins-else-bid default may need
H6R override. Axis 3 GOVERNANCE HOLDS with one QUALIFY: commit
order holds (be112b78f < a11dde4b9), PKG block byte-identical
prereg vs prototype (be4e5867), committed binary re-run reproduces
proto_run.log byte-identically; QUALIFY: Amendments 1-2 applied in
place and committed inside the prototype commit, not re-frozen
alone (flagged for Micah's amendment-discipline decision).
Recommendation scope honest (cognition layer only, baseline change
named as Micah's decision). Doc fix requested: "904 ticket nodes"
should read "type-904 ticket nodes". Five verbatim-ready Micah
decisions in RT-GOV_REVIEW.md ESCALATION (see section 2, debate 7).
Review commit 7a1ebe002. [NEW]

**39. RT-C174 (red team: C174 shared-store validation):
EVIDENCE-HOLDS, no dissent.** All 7 attacks failed: (1) post-seal fix
did not weaken bar (c): diff is exactly one emit line, prereg
section 4 anticipated format-identical decision channels;
independently rebuilt arms reproduce A==F de193b84 and S 6c33f7c4;
(2) A==F not vacuous (a routing bug would have broken equality);
nuance: disabled-store fallback routes via shared code by
construction, so bar (c) proves "reverts to fixed rules," not
independent convergence; (3) S != F is genuine store-driven
reordering (orders, attempts 63 vs 103, victims, answerability 6/6
vs 3/6 all differ on decision channels); (4) seal not hand-tuned:
committed generator reproduces world_sealed.zag bit-for-bit from
frozen seed; (5) no overclaim toward TNN-2/TNN-3; verdict stays in
dev-harness scope; (6) migration boundary was pre-registered before
the run; bar (d) properly bounded to K-H3-world migration compat
(independently verified against the CONSEQ K-H3 record); (7) commit
order strict: prereg 134af1cb2 -> impl b5e0274f7 -> seal 0096b30ca
-> eval 3028240e4. Minor nits (non-kills): arithmetically loose
parenthetical in EVAL_RESULTS bar (a); residual self-attestation on
the pre-fix claim (corroborated, not independently falsifiable);
cosmetic znc warning E0101. Review commit 89b27a9ce. Carried
qualifications: bar (c) = shared-code fallback; bar (d) =
K-H3-world compat. [NEW]

**40. RT-HPIREV2 (reviewer + adversary on H-PI-REV2 narrowed
claim): Part 1 QUALIFY, Part 2 bound PARTIALLY survives.** Part 1:
BUILD-PASS stands on the five tested worlds under the frozen bars as
written (commit order holds; binary/mechanism/prefix hashes match;
15 runs 3/3 byte-identical; bars verbatim, none weakened). Two
findings: Q1 certification defect (24/25 sealed files match prereg
hashes; D2_FW.txt has a 62-char truncated hash line in the prereg,
a transcription typo, so the lane's "25/25 verified, all match"
sentence is not literally true; certification defect, not
experimental: same file committed, staged, run); Q2 LOAD-BEARING:
all five lane worlds accommodate the frozen rank-biased diagnosis by
disclosed pre-freeze design (D2's design note admits tuning RW to
match both declared and diagnosed conflicts); the narrowed claim as
literally stated was never tested against a conflict the rank bias
does not select. Part 2 (post-freeze adversarial family, seal
8b86b27d2 committed alone pre-execution; lane binary hardcodes its
five fixtures, so adversarial runs execute the frozen mechanism
byte-verbatim, cognition delta 0): ADV-S1/S2/S3 PASS (bound
generalizes to fair structures); ADV-S4 BREAK CONFIRMED (valid
single-conflict world per V0-V3 whose true trigger (2,66) the rank
bias cannot select: fails_total=1); ADV-M1 SILENT SUCCESS CONFIRMED
(masked second conflict: fails=0, zero detection, uncovered
conflict never flagged); ADV-M2 explicit trip CONFIRMED (probed
second conflict: COUNTEREXAMPLE_DETECTED at W3). The bound-trip
signal is PROBE-DEPENDENT: explicit when the uncovered conflict is
probed alone, silent when masked. Reviewer recommendation: restate
the narrowed claim with an explicit rank-diagnosability qualifier,
and the bound-trip half with a probe-dependence qualifier. Debate
must adjudicate: BUILD-PASS-with-qualifications vs further
narrowing. Commits: seal 8b86b27d2, erratum 1c40232af
(pre-execution), review 5f53f1c7a. Pure Zag throughout. [NEW]

**41. RT-SENSE (red team: DEVANG3): QUALIFY (not dissent, not clean
holds).** BUILD-PASS stands on the frozen kill bars as written;
every reported number independently reproduced from committed
sources. Qualification: the K_SEAL leg (learner 20/20 on fresh
Family C) does NOT discriminate the learner from the trivial
fixed-width-3 control C2, which also scores 20/20 on the fresh
family (reviewer re-ran all variants: learner 20/20, c2 20/20, c0
13/20, c1/c3 10/20). The fresh Family C was specified in the frozen
prereg, informed by the lane's own disclosed /tmp tuning, to the
segmenter's known 3-char comfort zone; the judge brief's "K_SEAL
11/20 to 20/20" framing compares the 2021pdt sealed C against a
differently structured fresh family, not a same-set improvement.
What the wave establishes is the merge-pathology fix on ambiguity
probes (K_SEG 12/12 fresh; 12/12 on the 2021pdt regression set where
the baseline scored 8/12). Post-freeze generalization beyond a
trivial control is not demonstrated by Family C;
segmentation-specific discrimination rests on K_SEG (12/12 vs
ablation 4/12) and K8 (20/20 vs 17/20, exactly at the 15pp
threshold). Verification: no weakened bars (all match frozen prereg
verbatim); commit order strict (prereg 5b7e55706 contains only
prereg+NAMECHECK, then 126ef2600, ead6f006c, 11026f43b, a29d4088c);
one-line fix confirmed (sc=-50+ilog(L+1)*5 to sc=-50-1*L, plus
comments); root cause corroborated behaviorally (2021pdt baseline
reproduces the four documented failures; fixed binary 12/12 on old
and fresh sets); binary rebuilt byte-identical (36f5047d...); seal
integrity holds (all five pre-run hashes match; generator reproduces
sealed files byte-identically); K_AUD/K10/K11 verified by
inspection; no tuning leakage into the lane dir (residual
attestation-based risk disclosed: no independent adversary worker).
Minor nits (non-material): IMPLEMENTATION.md line count 1571 vs
committed 1574; SEALED_B.md probe-2 gloss slightly loose; fresh
Family B reuses word form tema from the 2021pdt set. Review commit
6ea7f42f9. SENSORY lane still running; needs red-team coverage when
it lands. [NEW]

### 1g. Design-complete (1)

**42. TNN3-SUBSTRATE (substrate addition package):
DESIGN-COMPLETE.** 197-line, zero-new-opcode package (learner
construction service + contradiction trigger + learner-writable
standing) closing the three gaps that stopped H2/H4/H6/H7.
Architecture accounting: 197 cognition lines added; 0 hardcoded
semantic cases; 0 modes; 0 bridges; 0 routers; 0 task-specific
handlers; 0 protected-core ops. Learner-state structures: 904
ticket nodes (-41 BUILD, -43 REDERIVE, -44 STAND),
topology-identified step nodes, BUILD_ROOT/STAND_ROOT; all existing
edge types. Verification on dev prototype (frozen tnn2.zag
untouched, hash re-verified): R0 46/46 frozen self-tests pass
(behavior-preserving), V1 construction (BUILD ticket with inverted
guard slot builds through one generic service, executes on frozen
ISA, fails closed; assembler-shaped ticket proves content-neutrality),
V2 trigger (every ev_observe contradiction yields exactly one
REDERIVE ticket), V3 standing (confirm/contradict accumulate +1/-1,
persist across queries). Frozen kill bars KB-H2R/H4R/H6R/H7R for the
re-attempts. Unblocks H2R/H6R/H7R and H4R's construction half;
H4R's closed loop still gated on Micah's pending EXECUTE placement
ruling. Commits: prereg be112b78f (Amendments 1-2 transparent),
prototype a11dde4b9, recommendation f77b7c7d5. RECOMMENDS but does
NOT adopt: adoption into the TNN-2 cognition layer, and any
protected-core change (none requested), are Micah's governance
decisions. ESCALATION ITEM recorded. [NEW]

(Note on numbering: entries 1-42 above correspond to the wave
record's 40 verdict bullets, with BATTERY split into two entries
and F1-FOLLOWUP and RT-HPIREV2 each carrying two sub-verdicts.)

## 2. Key debates for the group

### Debate 1: F1 BUILD-FAIL, uphold vs PARTIAL-narrowed

The question: should the F1 verdict stand as BUILD-FAIL (whole
candidate), or should it be narrowed to a PARTIAL verdict covering
the trigger component with the constructor seed-sensitivity filed
as a separate finding?

For UPHOLD: RT-EXEC recommends UPHOLD. PARTIAL is not a defined
verdict in the frozen rules; inventing one post-hoc would be
bar-weakening, exactly the move Micah's red lines forbid. The
frozen candidate was trigger plus constructor on the same fixtures,
and the frozen bar K-C0C-REG tripped at 0/30 on R-W2. The F1-FOLLOWUP
lane is already proceeding as a NEW candidate (Part 1 BUILD-PASS),
which is the correct procedural channel for the trigger re-test, not
a verdict change. Verdicts name the frozen bars that governed them;
the bar existed before the results.

For PARTIAL-narrowed: the trigger itself passed every trigger bar
(fires on all 4 interleaved patterns where the old trigger fired 0
times, 0 false positives, 30/30 learning, 57pp/57pp ablations). The
killing evidence is PROVEN STRONGLY to be a pre-existing constructor
limitation (the prior wave's frozen binary converges to the
byte-identical overfit structure on the same fixtures), so the FAIL
label attaches to a component the lane did not change. The worker
owns a bar-calibration mistake (unvalidated fresh seed conflating
trigger regression with constructor seed-robustness). F1-FOLLOWUP
Part 1 then passed all frozen bars on validated fixtures with zero
trigger regression. Recording the candidate's trigger as
narrowed-PASS would localize the failure where the evidence says it
lives.

The group must also weigh: does "uphold" overclaim nothing while
leaving the working trigger unpromoted, and does "narrow" risk the
bar-weakening precedent RT-EXEC warns about?

### Debate 2: HPIREV2 BUILD-PASS vs RT-HPIREV2 QUALIFY

The builder verdict: BUILD-PASS on five fresh sealed worlds, all
frozen kill bars, commit-order clean, 15 runs byte-identical,
revision measurements matching pre-freeze mechanical predictions
exactly.

The red team does not dissent on the five worlds but carries two
findings plus an adversarial family. Q1 is a certification defect
(24/25 hashes; a 62-char truncated hash line for D2_FW.txt in the
prereg), not experimental. Q2 is load-bearing: all five worlds
accommodate the frozen rank-biased diagnosis by disclosed pre-freeze
design (D2's design note admits tuning RW to match both declared and
diagnosed conflicts), so the narrowed claim as literally stated was
never tested against a conflict the rank bias does not select. The
adversarial Part 2 then ran the frozen mechanism byte-verbatim
against post-freeze worlds: ADV-S1/S2/S3 pass (the bound generalizes
to fair structures), but ADV-S4 is a CONFIRMED BREAK (a valid
single-conflict world whose true trigger (2,66) the rank bias
cannot select, fails_total=1), and ADV-M1/M2 show the bound-trip
signal is PROBE-DEPENDENT (explicit when the uncovered conflict is
probed alone, silent when masked).

The question: BUILD-PASS-with-qualifications, or further narrowing?
The reviewer recommends restating the claim with an explicit
rank-diagnosability qualifier and the bound-trip half with a
probe-dependence qualifier. The group must decide whether the
qualifiers attach to the verdict, whether the verdict is narrowed
to "bound holds on rank-diagnosable single conflicts with
probe-dependent trip signaling," and whether the ADV-S4 break
falsifies the narrowed claim as originally stated or bounds it.
Note the non-independence of the original five worlds is disclosed,
not hidden; the question is how much weight that disclosure carries.

### Debate 3: ARENA2 vs ARENA3, sibling collision on C12

Two independent lanes both built C12 transfer candidates after
ARENA2's directory was empty at ARENA3's start (assumption recorded
pre-build; per the frozen collision clause these are independent
competing runs, not duplication). The debate must reconcile the
mechanisms, not just the scores.

ARENA2 REMAP (on v6 base): C12 0 to 1, total 0.794 to 0.882
(60/68), +94/-0 lines, composes exposure-learned Zem templates with
the runtime-parsed value permutation, no sealed values hardcoded,
generalizes to any permutation/template. Ablations zero each half
exactly. L3 disclaimed. Also produced the C9 negative finding (the
causal battery is observationally unidentifiable; only gaming
passes; fix recommendations recorded).

ARENA3 TRX (on INQ base): C12 0 to 1 (6/6), total 0.853 to 0.941
(64/68), +80/-0 lines, parses the 4-value relabeling from the
question, applies learned class-A to class-B position-wise rewrite
plus parsed remap. Remap always from the question, never from
source/state. Ablations 3/6 each half (both causal). L3 disclaimed.

Comparison points the group should settle: the scores are not
directly comparable (different bases: v6 vs INQ; REMAP's denominator
includes no inquiry gain). Which mechanism is more general (REMAP
claims any permutation/template; TRX validates permutations of
[0,1,2,3] parsed from the question)? Do they compose (REMAP on the
INQ base, or TRX generalized)? Is one subsumed by the other? And the
integration question neither answers: neither is cumulative with
the inquiry candidate, both leave canonical 0.573 unmoved, and
integration across INQ/REMAP/ROSTER/DEFRECALL is an open later
decision.

### Debate 4: H5R2, is the gate necessary?

The arc across three verdicts: (a) TNN3H5R BUILD-PASS, H5R2 ADVANCES
(KB-W2R 12/12, the killed bar now passing; KB-W3 8/8 new family),
reproduced independently (H5R2-REPRO REPRO-PASS, pipeline step 4).
(b) H5R2-BASELINE: REVERT-TO-LATEST, a recency heuristic with no
provenance gating, matches H5R2 on every bar of the same four sealed
worlds, violating CB-2; the gate is NOT shown necessary there.
Honest cost disclosed: the recency arm regresses the built-in
battery to 45/46 (F2 FAIL) while H5R2 holds 46/46. (c) H5R2-DECOY:
DECOY-DISCRIMINATES; on 8 decoy probes where the newest fact is not
the live one, the gate anchors 8/8 to the live fact while recency
anchors 8/8 to the decoy. The record's interpretation:
BASELINE-MATCHES is RESOLVED, not contradicted; recency explained
the four-world battery only because newest happened to be live
there.

The question for the group: what is the H5R2 claim now? The
skeptic's case: a mechanism whose necessity is demonstrated only on
worlds designed to discriminate it, while a one-line heuristic
matches it on the original battery, has a narrow demonstrated
advantage; the 46/46 vs 45/46 built-in difference is one item.
The advocate's case: the decoy battery was the pre-registered
discriminating experiment the baseline lane itself recommended; the
gate beats no-gate and random everywhere and beats recency exactly
where recency must fail; necessity was never claimed on the four
worlds, only bounded. The group should also note what is still
open: H5R2-SKEPTIC2 is running a stronger skeptic baseline (gates on
liveness but not supersession; "newest live fact") and W3-style
chained decoys, which could move this again.

### Debate 5: E3-ORACLE-DEPENDENT, does it reframe the construction claims?

BATTERY-E3 is the wave's most consequential negative result. Blind
E3B (spurious-first, adversarial): 0/2, emitting exactly the
pre-registered spurious composites; oracle-present E3B: 2/2. The
white-box inspector confirms blind assembly of GUARD/SETREG chain
graphs with ET_DEP provenance, promotion as MAP nodes, execution:
ASSEMBLY WORKS BLIND, SELECTION DOES NOT. The trial's correct
compositions depended on the unmasked verifier (accept iff output
equals the QUERY-carried expected value) to select among multiple
executable BFS chains; masked mode emits the first-executable chain.
The record's own interpretation: this REFRAMES EVERY PF CONSTRUCTION
OBSERVATION as BFS enumeration plus oracle selection, not selective
construction; every wave construction claim resting on unmasked QUERY
evidence must be re-examined blind.

The debate questions: (1) Scope: which claims rest on unmasked
QUERY evidence? E3's confound note already flags BATTERY-E1's W4
behavioral leg (structure-driven answers vs oracle-verified BFS
traversal indistinguishable). What about the PF-A/PF-C battery
results, and any prior-wave construction claims built on the same
verifier? (2) The ARENA-BLIND audit answered the mandate for ROSTER
(ORACLE-FREE: single candidate, no oracle fields, no selection
step), a clean template for answering it; which other mechanisms
need the same audit? (3) Does the reframing strengthen or weaken
the DERIVATION SUBORDINATION cluster story (E1/E4/E5)? Assembly
works; selection and standing do not: that is consistent with the
cluster but reframes what "construction" meant in PF-A1 and v3-M1.
(4) What would a genuinely selective construction look like, and
can it be built without an oracle channel? No repair was proposed;
the group should decide whether the next experiments are audits of
old claims or new blind-first designs.

### Debate 6: CONSEQ / CONTLEARN qualifications

Both survived red team with EVIDENCE-HOLDS and no dissent, but each
carries a qualification the group should weigh when citing them.

CONSEQ (VALIDATION-PASS): the wave confirms reproduction fidelity
of the frozen Node2-v2 K-H3 prereg (5/5 bars, 3/3 byte-identical,
causal ablations on Link 1 and Link 3 both NECESSARY), not
adversarial validation: the independent-adversary clause was never
met (builder-sealed worlds). The consequence record is a
researcher-written 3-revelation counter, inside the frozen claim
bounds but still researcher-authored. Scope honestly held: it
validates the consequence re-entry template, not the shared tag-61
substrate (C174 validated separately as infrastructure, in
dev-harness scope only). The question: how much does this advance
the shared-consequence-substrate hypothesis (Micah's fifteen-question
agenda item), and what experiment would meet the adversary clause?

CONTLEARN (BUILD-PASS, LEARNOWN-DEMONSTRATED): the unsupervised
store/reuse bars (K4a 13/13, K4b 20/20, K4c ablation to 0/20,
K4d 20/20 true misses) remove the answer-key confound, but the
masked queries remain researcher scaffolding, honestly disclosed;
removing keys does not escape scaffolding. The
"LEARNOWN-DEMONSTRATED" label is a hazard: the weak/strong
distinction must stay attached when cited (weak H10 sense: the
workspace is the single frozen arena; no learner-agency claim).
The question: is this a genuine step toward the continuing-learner
goal, or machinery integration demonstrated under supervision,
exactly as the prior red team qualified it? The K3 regression check
(REUSE_COUNT 30/30 retained) is solid either way.

### Debate 7: The 5 RT-GOV governance decisions for Micah

RT-GOV HOLDS on all three axes (ONE-SYSTEM RULE, ISA RULING,
GOVERNANCE) with one QUALIFY (Amendments 1-2 applied in place
inside the prototype commit, not re-frozen alone). The substrate
package RECOMMENDS but does NOT adopt; adoption and any
protected-core change are Micah's decisions. The five
verbatim-ready decisions from RT-GOV_REVIEW.md ESCALATION:

1. Adopt the 197-line package into the TNN-2 cognition layer?
   (Evidence: R0 46/46 self-tests behavior-preserving; V1/V2/V3
   verification; H7R BUILD-PASS built on it; H6R BUILD-FAIL shows a
   standing-gap the package does not close.)
2. Accept the frozen-baseline change? (Soft irreversibility once
   the re-attempts freeze their bars against the new baseline.)
3. Accept lbid's record-wins-else-bid default? (Residual (b);
   flagged as possibly needing H6R override.)
4. Accept the +1/-1 polarities as fixed machinery, or require
   learner ownership before H6R? (Residual (a): researcher
   constants in the standing accumulator.)
5. Accept Amendments 1-2 as committed, or require future
   amendments to re-freeze alone? (The QUALIFY; an
   amendment-discipline decision with precedent value.)

The group should prepare, for each: the evidence for, the evidence
against, and what changes in the research program if Micah says
yes vs no. Note the interaction with H6R's BUILD-FAIL: the
standing-record eviction gap (records never protection-pinned,
lbid 0, always evicted before fact nodes) is a crisp substrate
design gap that adoption would inherit; the group should say
whether that gap is a reason to delay adoption or the first repair
target after adoption.

## 3. Provenance: what is new vs inherited (per BUILD-PASS)

Prepared answers for the skeptic's verbatim provenance probe.
"Inherited" means taken from prior waves, the frozen base, or
shared instruments; "new" means created and evidenced this wave.

**HPIREV2.** New: the narrowed step-7 single-conflict bound as a
frozen claim; 5 fresh sealed worlds; the bound-trip 3/3 evidence;
the certification (minus the Q1 transcription defect); zero
cognition source delta on this lane. Inherited: the frozen TNN-2
base; the rank-biased diagnosis machinery and the step-5/6 results
from the prior wave; the step-7 FAIL-with-bounding frame itself.
Not claimed: L3, generality, SURVIVES status.

**CONTLEARN.** New: the learner-owned push evidence (unsupervised
store 13/13, masked reuse 20/20, in-arena deletion ablation,
nostore control), the 2021pdt cl_driver 3/3 re-run with REUSE_COUNT
30/30 retained. Inherited: the frozen arena and core; the prior
wave's INTEGRATION-DEMONSTRATED result (which the prior red team
qualified as machinery integration under per-query supervision);
the weak-H10 framing. Researcher scaffolding remains disclosed.

**TNN3H5R (H5R2).** New: the 9-line t2_prov_ok helper and 4 gated
promote sites; the KB-W2R 12/12 recovery (was the 8/12 kill); the
new KB-W3 two-revision family 8/8; the net +9 architecture delta.
Inherited: the frozen battery worlds; the TNN-2 base (cumulative
diff net -4); the H5R kill it repairs. Seal note disclosed: single
worker as coordinator/builder/evaluator with pre-frozen mitigations.

**ARENA inquiry (C8).** New: the ask-observe-answer loop mechanism
(+69/-3 lines, both halves ablated); C8 0 to 1; arena 54/68 to
58/68. Inherited: the arena battery and v6 base; the learn_fact /
observe_result protocol it rides on. L3 disclaimed; canonical
0.573 unmoved; not built on the TCNP binary.

**ARENA2 (REMAP).** New: the REMAP mechanism (exposure-learned Zem
templates composed with runtime-parsed permutation); C12 0 to 1;
60/68. Inherited: the v6 base and the exposure templates it
composes. Bonus new this wave: the C9 negative finding with killing
evidence and generator fix recommendations (a genuine contribution
independent of the transfer claim).

**ARENA3 (TRX).** New: the TRX mechanism (question-parsed 4-value
relabeling applied to learned A/B templates); C12 6/6; 64/68 on the
INQ base. Inherited: the INQ base and A/B exposure templates; the
C12 target itself (born of the sibling collision, assumption
recorded). L3 disclaimed; canonical 0.573 unmoved.

**DEVANG3.** New: the one-line score fix (sc=-50-1*L, length bonus
to linear penalty) with behavioral root-cause evidence; K_SEG
12/12; K_SEAL 20/20 on the fresh family. Inherited: the segmenter
machinery; the Family B/C instruments. RT-SENSE qualification
stands: the fresh Family C does not discriminate the learner from
the trivial C2 control; discrimination rests on K_SEG and K8.

**ARENA4 (ROSTER).** New: the experience-built entity roster
mechanism and the falsification of ARENA2's "ordering-fragile"
rejection (frozen scorer is order-insensitive set F1); C15 0 to
0.947. Inherited: the v6 base; the exposure events the roster reads.
ARENA-BLIND's ORACLE-FREE audit is new evidence this wave that the
claim never rested on oracle selection. Caveat: 0.947 is the honest
experience ceiling (Segunu never observed).

**H7R.** New: the learner-side REDERIVE consumer (12/12 corrected
roots, 100pp margin; B1-B6 + P1/P2 all PASS); built on the
TNN3-SUBSTRATE construction service and contradiction trigger.
Inherited: the substrate package (DESIGN-COMPLETE, pending
adoption); the contradiction protocol. Flag for the debate: the
H7R record states "Substrate halves now 3/3 passing (H2R, H6R,
H7R)" while this same wave's H6R lane verdict is BUILD-FAIL; the
group should establish whether the parenthetical refers to this
wave's H6R (a contradiction needing resolution) or a prior H6R
result (a naming collision needing disambiguation).

**F2V3.** New: the D2 8 to 9 bound raise (one constant plus buffer
8 to 10 slots and ledger 48+nhyp to 50+nhyp); depth-9 distinguishing
sequences passing all eight frozen bars on two fresh worlds.
Inherited: the DPDS mechanism and the v3 BUILD-FAIL it repairs; the
retired 2021pdt worlds (no regressions).

**ARENA5 (DEFRECALL).** New: the generic default action replacing
ARENA4's dedicated listnames handler (174 lines; zero goal-string
references; roster-on/action-off ablation proves the default action
is the goal-completion path). Inherited: ARENA4's roster verbatim;
the v6 base; the battery (seed 71503461337032). Caveat disclosed:
on this battery the default action is extensionally equivalent to a
listnames handler; generality rests on intension.

**F1-FOLLOWUP Part 1.** New: the corrected-bar re-test (trigger
reproduces old binary byte-exactly on validated fixtures; zero
trigger regression). Inherited: the F1 windowed trigger; the prior
wave's W2 fixtures. Explicitly NOT a verdict change to the F1
BUILD-FAIL; filed as a new candidate.

## 4. Open questions (what the running lanes may still decide)

- **SENSORY** (running): new bigger-lever realism candidate H2v1;
  fresh frozen prereg; sealed blind A/B for Micah if READY. When it
  lands it needs red-team coverage (RT-SENSE flagged this in
  advance). Could move the realism frontier or confirm H1v2's
  BUILD-FAIL stands.
- **H5R2-SKEPTIC2** (running): the stronger skeptic baseline (gates
  on liveness but not supersession, or "newest live fact") plus
  W3-style chained decoys. This is the direct follow-up to Debate 4;
  it can shrink or extend the demonstrated necessity of the
  t2_prov_ok gate. Process flag: this worker's commit f461e812d
  accidentally deleted BATTERY-E4 files (restored byte-identical);
  its git workflow needs review.
- **BATTERY-E8** (running): the H2d ACT-output-bandwidth probe,
  follow-up to E6's redirect of Cluster 2. Decides whether the
  "content reaches ACT as subject tag plus constant 30" story ends
  at bandwidth limits.
- **LANE-AUDIT** (early): only NAMECHECK committed so far; scope
  and findings pending.
- **TNN3-SUBSTRATE adoption**: pending Micah's five governance
  decisions (Debate 7). H2R/H6R/H7R re-attempts are frozen against
  bars that assume the package; H6R's BUILD-FAIL already records a
  standing-gap the package does not close.
- **F1 line**: F1-REPAIR2 confirmed S-prime (27/27 across three
  seed series) and characterized POLICY-R within its boundary; no
  fix proposed for the greedy depth-1 trial or the repair-time
  policy. The F1 BUILD-FAIL vs PARTIAL question (Debate 1) is
  independent of this.
- **Integration debt**: INQ, REMAP, TRX, ROSTER, DEFRECALL were
  built on separate bases (v6 vs INQ); none is cumulative with the
  others; canonical 0.573 is unmoved by all of them. Integration is
  an explicit later decision the debate should scope.
- **E3 audit backlog**: ARENA-BLIND answered the mandate for
  ROSTER; the group should list which other construction claims
  (PF-A/PF-C battery results, E1-W4 behavioral leg, prior-wave
  construction evidence on unmasked QUERY) owe the same blind
  audit.
- **The debate itself**: DEBATE.md not yet committed; this brief
  is the input, not the verdict. Verdicts above marked "debate
  pending" remain the lanes' claims until the debate group rules.

## Evidence paths

- Wave record: docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md
- Lane dirs: docs/lab/rsi/runs/wave-20261001-2321pdt/<LANE>/ (each
  with PREREG, implementation, sealed eval, JUDGE_BRIEF.md)
- Red-team reviews: docs/lab/rsi/runs/wave-20261001-2321pdt/RT-*/
  (RT-GOV_REVIEW.md carries the 5 verbatim Micah decisions)
- This brief: docs/lab/rsi/runs/wave-20261001-2321pdt/DEBATE-PREP/
  DEBATE_BRIEF.md + JUDGE_BRIEF.md

Swarm note: DEBATE-PREP is synthesis-only and consumed no build
capacity; all running lanes (SENSORY, H5R2-SKEPTIC2, BATTERY-E8,
LANE-AUDIT) continue undisturbed.
