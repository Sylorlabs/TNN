# PREREG: L3-NIV2 CALR red team (K10 adjudication)

Status: REDTEAM-PREREG-FROZEN 2026-10-02, before any red-team attack
implementation exists. This document is never edited after freezing. Any
change requires a new prereg. The frozen design prereg (affe2c3eb), the
wave-3 prereg (754f33d1c), and REPORT_WAVE3.md (e61c9c50c, BUILD-PASS,
ledger C334) are untouched and still govern the artifact under test.

Commit-order self-check: the freeze commit contains PREREG.md and the
Step 0 update to NAMECHECK.md ONLY. No red-team .zag source, no attack
key file, no attack binary, no run log exists at freeze time. The
impl/ directory holds read-only copies of the frozen e61c9c50c sources
(extracted via `git show`, byte-verified against the commit) and the
binaries built from them; these are the artifact under test, not
red-team implementation.

Worker: L3-NIV2 CALR red-team worker (subagent, 2026-10-02). Replacement
for a completed worker (D3 policy redesign).

## 1. Target

CALR (Consequence-Anchored Lookahead Retention), the wave-3 search
mechanism that replaced the wave-2 beam for base construction
(transfer = 0). Frozen at commit e61c9c50c. Ledger C334 records
BUILD-PASS: T1 COMMITS on DEV-S1 (y = x^2 + x, refprog
[CPY r1,r0][MUL r0,r0][ADD r0,r1]), 6/6 held-out, 38,206 of 50,000 TESTs,
3/3 byte-identical.

CALR as frozen (PREREG_WAVE3.md section 4, lm_cons3.zag):

- Phase A (harvest): evaluates all 80 length-1 seeds (pool ids 1..80)
  and all 6400 length-2 appends (pool ids 81..6480) through the
  consequence channel via eval_prog (two-pass: first 3 training instances
  with early exit on first REJECT; remaining instances only if pass 1
  produced at least one ACCEPT). Every ACCEPT records fhat[train_idx] =
  output (cfg+256 values, cfg+320 known flags). No pruning.
- Phase B (potential, zero TESTs): for each depth-2 prefix, local
  4-register simulation on each training input; potential = max over the
  80 appends of agreement with fhat on known inputs.
- Phase C (ordered verification): verifies prefixes in (potential desc,
  score desc, id asc) order via bucket loops (pv 6..0, sv 6..0, plist
  order within a bucket, which is id order). For each prefix, recomputes
  the argmax append set (appends achieving max potential, byte order
  e = 0..79) and TESTs each through the consequence channel until one
  reaches full acceptance (score >= 6, hardcoded) or the argmax set is
  exhausted. Stops at the first full acceptance. Budget B_CONSTRUCT =
  50,000 TESTs enforced by do_test.
- Early return: if any seed or prefix fully accepts during Phase A
  (accn > 0), CALR returns immediately and the arm commits that short
  program.

Frozen assumptions under attack (load-bearing):

- H1 (fhat nonempty): PREREG_WAVE3.md section 8: "If fhat is empty (no
  ACCEPT in Phase A), potential is 0 for all and Phase C degrades to a
  score-ordered scan bounded only by the TEST budget. For DEV-S1, seeds
  alone guarantee fhat covers x = 0 and x = 1." The mechanism relies on
  seeds guaranteeing coverage; the degradation is claimed graceful.
- H2 (potential discriminates): D3: 1-step lookahead potential sees
  latent-state utility that score cannot (W3K3: PR <= SR/2).
- H3 (first acceptance is safe): Phase C stops at the first full
  acceptance (section 8 known limitation; interaction with genuine
  ambiguity deferred to wave 4).
- H4 (depth 3 suffices): CALR covers depth 3 only (section 8 known
  limitation; staged deepening is wave-4 work).

## 2. Red-team lemma R1 (analytical; constrains the attacks)

Claim: at depth 3, with nonempty fhat, the prefix of any fully-accepting
length-3 program ALWAYS has maximal potential (nk, the number of known
fhat inputs).

Proof: potential(P) = max over 80 appends of agreement(extend(P,app),
fhat on known inputs). Let S = P ++ [c] fully accept on training
(score >= 6, i.e., S(x_j) = refprog(x_j) for all 6 training inputs).
For each known input j, fhat[j] = refprog(x_j) (an ACCEPT records the
program output, and ACCEPT holds iff output == refprog(x_j)). Hence
agreement(S, fhat) = nk, the maximum achievable. So potential(P) = nk.

Consequence: attack design (a) "a problem where the 1-step lookahead
potential is misleading (the crucial prefix has low potential but is
necessary)" is IMPOSSIBLE as stated at depth 3 with nonempty fhat. The
only channels by which potential can mislead are: (i) fhat EMPTY
(potential vacuous, all zero) -> Attack A1; (ii) fhat SPARSE (potential
takes few values, dense ties, and the (score,id) tie-break dominates;
score is exactly the wave-2 criterion proven blind to latent state by
D1) -> Attack A2. This lemma is itself a red-team result: it
characterizes precisely when CALR's core signal can and cannot mislead.

## 3. Attack designs

All attacks use newly authored unsealed REDTEAM key files (REGIME
REDTEAM-A*, TRAIN 6 distinct inputs in key order, HELDOUT 6, REFPROG =
the exhibited solution). T1 arm only (OBSERVE 6 key order, construct
budget 50000, transfer 0). The artifact under test is the frozen
e61c9c50c learner binary; the world binary is the frozen e61c9c50c
world. No sealed content is touched.

### Attack A1: EMPTY-FHAT (the consequence channel goes silent)

Design: a key with 6 distinct training inputs X, true program T of
length 3 (REFPROG = T's bytes), such that NO length-1 or length-2
program ACCEPTs on train[0] = X[0]. By eval_prog's early-exit
structure, no ACCEPT can then be recorded at any training index, so
fhat is EMPTY (nk = 0). This directly breaks H1: the prereg's claim
that seeds guarantee fhat coverage holds only for training sets
containing inputs like 0/1 where short programs coincide with the
target; the red team chooses X where they never do.

Predicted CALR behavior (analytic, forced): Phase A burns exactly 6480
TESTs (each of the 6480 programs REJECTs at instance 0, one TEST each),
fhat empty, all potentials 0, all scores 0. The Phase-A early return
does not trigger (accn = 0). Phase C scans all 6400 prefixes in id
order (bucket (0,0), plist order); argmax = all 80 appends per prefix;
each prefix costs at least 80 TESTs (one per append, instance-0
REJECT). Reachable prefixes: floor((50000 - 6480) / 80) = 544, i.e.,
prefix ids 81..624. If the verifier (section 4) confirms that no
length-3 program with prefix id <= 624 fully accepts on X, then no
COMMIT is possible (Phase A programs cannot fully accept either: they
score 0), the budget exhausts, disambiguate sees zero reps, and the
arm DEFERS. The exhibited solution T (prefix id >= 2000, verified)
exists and needs only 6 TESTs to verify, but is unreachable in the
blind id-order scan.

Kill criterion: CALR DEFERS (trace shows CALR-DONE with accn = 0, then
DEFER, world TALLY 0 0 FAIL) while the solvability bar (section 4, A1)
holds. A wrong commit (COMMIT followed by SCORE <= 4 / FAIL) also
counts as a kill.

Assumption broken: H1 and the "graceful degradation" claim. The
degradation is not graceful: with empty fhat CALR becomes a blind
id-ordered scan that burns the full 50,000 TEST budget and defers on a
problem whose solution is 6 TESTs away.

### Attack A2: TIE-FLOOD (sparse fhat drowns potential in ties)

Design: a key with 6 distinct training inputs X, true program T of
length 3, such that fhat covers exactly nk in {1,2} inputs (sparse but
nonempty). By Lemma R1 the true prefix has potential = nk = max, but
potential takes only nk+1 distinct values, so the (potential desc,
score desc, id asc) order is dominated by the (score,id) tie-break.
Score is the wave-2 criterion that D1 proved blind to latent register
state. CALR therefore silently degenerates to the mechanism wave 2
already falsified.

Construction: simulator-guided search. A faithful pure-Zag simulator
of CALR Phases A/B/C (exact two-pass eval_prog scoring with early
exit, exact fhat derivation, exact potential computation, exact bucket
order, exact argmax byte order, exact TEST counting with the 50,000
budget) is validated FIRST on DEV-S1: it must reproduce the wave-3
trace numbers tid = 433, PR = 229, SR = 453, pmax = 2, nk = 2, first
full acceptance at verification 229 with parent 433 and program bytes
000100020000010001. The simulator then scans the frozen candidate
families F1 (T_a(x) = x^a, a in {3,4,5,6,7,8}; X in
{{2,3,4,5,6,7},{3,4,5,6,7,8},{0,1,2,3,4,5}}) and F2 (T(x) = x^3 + c,
x^2 + x + c, c in {1,2,3}; X in {{0,1,2,3,4,5},{2,3,4,5,6,7}}).
Selection rule (frozen): the first candidate in enumeration order for
which the simulator predicts DEFER and the true prefix's rank is at
least 2x the simulator's reachable-prefix count. If no candidate
qualifies, A2 is reported FAILED-ATTACK (honest negative).

Kill criterion: CALR DEFERS while the solvability bar (section 4, A2)
holds. The trace must show CALR-HARVEST with nk in {1,2} (confirming
the sparse-fhat regime was actually hit).

Assumption broken: H2. Potential does not discriminate when fhat is
sparse; the tie-break reinstates the falsified score criterion.

### Attack A3: DECOY (the first full acceptance is a dead end)

Design: a key with 6 distinct training inputs X, 6 held-out H, true
program T of length 3, decoy program D of length 3, D != T as bytes,
with D|_X = T|_X (D fully accepts on training), T|_H = refprog|_H
(T scores 6/6 held-out), D|_H != T|_H with SCORE(D) <= 4 on H, and
rank_CALR(prefix(D)) < rank_CALR(prefix(T)) such that the validated
simulator predicts CALR's Phase-C scan commits D (or another
held-out-failing program) before any held-out-passing program.

Construction: computational collision search. Enumerate all 512,000
length-3 programs; compute training signatures on X =
{0,1,2,3,4,5}; group by signature; collect pairs (D,T) with identical
training signatures but different held-out signatures on H =
{6,7,8,9,10,11}. For the first 20 such pairs in enumeration order,
run the validated simulator to predict CALR's committed program.
Selection rule (frozen): the first pair for which the simulator
predicts a commit with held-out score <= 4. Honest caveat
(preregistered): all ISA programs compute polynomials with
nonnegative coefficients (degree <= 8 at length 3), so a training
collision with held-out divergence needs a degree 6..8 vanishing
polynomial on X; the search may find none, in which case A3 is
reported FAILED-ATTACK (an informative negative about Phase-C
robustness at depth 3).

Kill criterion: CALR COMMITs a program that scores <= 4 on held-out
(SCORE ... FAIL in the trace) while the solvability bar (section 4,
A3) holds, i.e., the true solution T exists and passes held-out.

Assumption broken: H3 (stop-at-first-acceptance). Would confirm the
deferred section-8 ambiguity problem is real and exploitable now, not
just in wave 4.

### Attack A4: DEPTH-4 (the depth-3 bound is a cliff)

Design: a key with 6 distinct training inputs X, true program T of
length 4 (REFPROG = T's bytes, minimally length 4: the verifier
confirms no length <= 3 program fully accepts on X), e.g. T =
[MUL r0,r0]^4 (x^16) with X = {2,3,4,5,6,7}; frozen fallback X =
{3,4,5,6,7,8} if the verifier rejects the primary.

Predicted CALR behavior: Phase A finds no full acceptor (verified);
Phase C verifies only length-3 programs (prefix length 2 + 1 append),
so the length-4 solution is unreachable by construction; the budget
exhausts; the arm DEFERS. This targets the DISCLOSED limitation H4,
so a kill is recorded as CONFIRMED-KNOWN-LIMITATION (not a surprise),
with two novel contributions: (a) demonstrating the cliff is sharp
(no partial credit, no graceful handoff), and (b) quantifying the
naive fix cost: extending Phase A to depth 3 requires harvesting
512,000 length-3 prefixes (80x), each costing >= 1 TEST, i.e.,
>= 512,000 TESTs, over 10x the 50,000 budget (computed analytically,
not run).

Kill criterion: CALR DEFERS while the solvability bar (section 4, A4)
holds (length-4 solution exhibited and verified; no length <= 3
program fully accepts on X).

## 4. Solvability bars (frozen; checked by an independent pure-Zag verifier BEFORE any binary run)

The verifier is a separate pure-Zag program (no learner code, no
channel): it parses the attack key, evaluates programs with its own
isa_exec copy, and checks the bars below exhaustively. Its output is
committed with the attack. No binary run may be claimed as a kill
unless its key passed the verifier.

- A1 bars: (a) REFPROG parses to a length-3 program T; (b) no
  length-1 or length-2 program (all 6480) outputs T(X[0]) [hence fhat
  empty is forced]; (c) id(prefix(T)) >= 2000 under the frozen
  id-assignment rule (seeds 1..80 in (o,d,s) order, prefixes
  81..6480 in (si,e) order); (d) no length-3 program (all 512,000)
  with prefix id <= 624 fully accepts on X [hence DEFER is forced,
  not lucky]. Keygen tries candidates in frozen order: (x^8,
  {3,4,5,6,7,8}), (x^6, {3,4,5,6,7,8}), (x^8, {4,5,6,7,8,9}); the
  verifier selects the first satisfying (a)-(d).
- A2 bars: (a) REFPROG is length 3; (b) the simulator's fhat
  computation on the key gives nk in {1,2}; (c) the simulator
  predicts DEFER with true-prefix rank >= 2x reachable; (d) no
  length <= 2 program fully accepts on X (else Phase A would commit
  it and the attack would not test Phase C).
- A3 bars: (a) REFPROG is length-3 T; (b) exhibited D is length 3,
  D != T bytes, D|_X = T|_X, T scores 6/6 on H, D scores <= 4 on H;
  (c) the simulator predicts CALR commits a program scoring <= 4 on
  H; (d) no length <= 2 program fully accepts on X.
- A4 bars: (a) REFPROG is length-4 T; (b) no length <= 3 program
  (all 6480 + 512,000) fully accepts on X; (c) T is minimally
  length 4 (implied by (b)).

## 5. Controls

- C0 (harness fidelity): run the frozen e61c9c50c learner + world
  binaries on the unsealed DEV-S1 key (copied read-only), T1 arm.
  Expected: CALR-FOUND with parent 433, COMMIT of
  000100020000010001, SCORE 6 6 PASS, 3/3 byte-identical decisive
  lines. If C0 fails, every attack verdict is VOID (harness broken),
  and the worker reports the harness failure instead of attack
  verdicts.

## 6. Frozen kill bars

- K1 (determinism): 3/3 runs per attack with byte-identical decisive
  trace lines (CALR-HARVEST, CALR-RANK, CALR-DONE, CALR-FOUND if any,
  COMMIT, SCORE, DEFER/TALLY). Full-log sha256 recorded per run.
- K2 (solvability): the section-4 verifier output for the attack's
  key is committed and shows all bars green BEFORE the binary runs.
- K3 (kill): CONFIRMED-KILL iff K1 and K2 hold and the binary either
  (i) DEFERS (DEFER in trace, world TALLY 0 0 FAIL, no COMMIT), or
  (ii) COMMITs a program scoring <= 4 on held-out (SCORE ... FAIL).
  A4 kills are labeled CONFIRMED-KNOWN-LIMITATION. FAILED-ATTACK iff
  K1 and K2 hold and the binary COMMITs a program scoring >= 5 on
  held-out (CALR solves the attack problem). A kill must name the
  exact assumption (H1-H4) it breaks.
- K4 (terminality): VOID is terminal per attack. C0 failure voids all
  attacks. Any forbidden-executable invocation voids the whole wave
  (PROCESS-FAIL per governance). Kill bars are never weakened; a
  missed bar is reported as missed.

## 7. Verdict logic

Per attack: CONFIRMED-KILL (naming the broken assumption) /
CONFIRMED-KNOWN-LIMITATION (A4 only) / FAILED-ATTACK (with the
reason: e.g., CALR solved it, or no candidate satisfied the frozen
selection rule) / VOID (with the cause). The REPORT lists, per
attack: the key, the verifier output, the 3 run digests, the decisive
trace lines, and the verdict. Honest negatives are reported as
information, not buried.

## 8. Implementation plan (not yet existing at freeze)

- rt.zag (pure Zag, compiled with the pinned znc): modes keygen,
  verify, sim, collide, as specified above. One program, argv-selected
  mode. No learner/world code reused; isa_exec semantics copied from
  the frozen isa.zag (read-only reference).
- battery_rt.sh: shell only (FIFO plumbing, timeouts, sha256). Runs
  the frozen learner_bin/world_bin on each attack key 3x (T1 arm).
- REPORT.md with per-attack verdicts.

## 9. Governance restated

Pure Zag for all scientific computation. Commits local only, explicit
pathspecs, never push, never amend shared history, never git reset.
Do not modify l3_novel_intermediate_v2/. Do not touch sealed worlds;
attack fixtures are unsealed REDTEAM keys. No em/en dashes in
documentation.
