# PREREG — ONE ENGINE vs DUAL ENGINE (frozen)

## 0. Question
Micah's bet: ONE ENGINE that does it all — hypothesis refereeing AND proof
derivation in a single adaptable mechanism — vs a DUAL ENGINE (separate
derivation engine + H5 referee, composed). Does the one engine match or beat
the dual, head-to-head? Architect: Fable 5.1, one deep batched round
(fable_response.txt, 2026-09-25). This prereg freezes Fable's 6 predictions
as kill bars.

## 1. Common ground (fairness — both engines)
- Same frozen knowledge store: docs/lab/math_logic/knowledge/KNOWLEDGE_STORE.md
  (25 items) PLUS the committed inference schemas (§2). Neither engine may
  ingest any other knowledge.
- Same claim representation: byte-encoded structured claims; schemas are
  antecedent patterns + consequent pattern with bound variables.
- Same depth bounds: primary bound 8; bound 16 for B6 scaling only.
- Pure Zag, zero RNG, deterministic given state; 3x byte-identical reruns
  asserted per problem; pinned toolchain znc_linux_x86_64_abed8aa1.
- Neither engine may contain problem-specific content, hardcoded answers,
  or domain tricks. Inference comes ONLY from the committed schemas (§2).
  Violation = build rejected, not a failed bar.

## 2. The commitment ceremony (auditable, once, frozen with this prereg)
Fable's design requires inference rules as structured schemas, not text.
The ceremony: encode as schemas ONLY what the frozen knowledge store gifts:
- K005 modus ponens: from P and (P=>Q), produce Q.
- K005 proof by contradiction: from (NOT-P => contradiction), produce P.
- Universal instantiation (needed by the battery; gifted implicitly by K001
  "for every positive integer n" phrasing — documented here as a judgment
  call, frozen).
The encoding (pattern bytes for each rule) is committed alongside this
prereg as COMMIT_SCHEMAS.md with the exact bytes. Both engines use these
identical schemas. If a schema mis-encodes its rule, that is a build defect
found by the audit bar (KB4), not a silent fix.

## 3. Engine ONE (Fable design a)
Single core operation: match-and-bind (pattern + ground state -> binding ->
new ground claim, with audit chain citing schema hash + premises + binding).
- Derivation = match-and-bind producing a claim not previously in memory.
- Refereeing = for each candidate hypothesis H, attempt to derive NOT-H;
  H survives iff NOT-H is not derivable within bound. No numeric scores.
- Search: deterministic breadth-first over applicable schemas per depth
  level, to bound 8 (16 for B6). Terminate on: target derived, fixpoint
  (no new claims), or bound reached.
- Withhold = derivation exhausted without producing the target; confidence
  is DERIVED (non-zero iff derived), never assigned.
- Output per problem: derived claim or WITHHELD, full audit chain,
  derivation count, confidence.

## 4. Engine DUAL (Fable design b)
- Engine D: theorem prover over the store (forward chaining; backward
  chaining on referee directive). Produces candidate claims + refutation
  candidates, each with full audit chain.
- Engine R: the REAL H5 referee (dlb_delib.zag imported verbatim), receiving
  D's candidates as hypotheses and D's audit chains as evidence; derivation
  depth + premise quality are the evidence scores (documented scoring rubric,
  frozen with the build — the rubric is itself audited under KB4).
- Interface: D->R: derived candidates + refutation candidates (standard
  claim format, no translation layer). R->D: bounded directives
  ("derive NOT-H to depth N") and deterministic priority signals
  (lowest-confidence hypothesis first — mechanical rule, frozen).
- Withhold owned by R. Productive disagreement: R may eliminate a
  D-endorsed candidate if NOT-H is derivable; R may sustain what D cannot
  prove only via other scored evidence (documented per case).
- Output per problem: verdict + confidence + audit chain (both engines'
  steps labeled), derivation count.

## 5. Batteries (all frozen before engines run)
- B1: the frozen 22 math problems (P01-P22), sealed solutions untouched.
- B2: 12 NEW harder math problems (test crew authors; sealed solutions
  committed BEFORE either engine runs; hardness bar: require >=4 derivation
  steps or a multi-lemma structure; same file format as B1).
- B3: 10 interleaved conjecture-test-revise problems (derive candidate,
  test against constraints, find flaw, revise, re-derive).
- B4: 15 non-math transfer problems (causal/temporal/semantic reasoning;
  solvable ONLY with the committed inference schemas, no domain rules).
- B5: false-rule injection: 1, 3, and 5 false inference rules injected
  into a COPY of the store; 20 problems per injection level.
- B6: scaling: problems requiring >=50 store items; measure derivation
  counts and wall time for both engines.

## 6. Kill bars (Fable's 6, frozen)
- KB1 interleaved (B3): if ONE solves >=7/10 more than DUAL, DUAL's
  interface is falsified as insufficient for revision loops. (Measured as
  pairwise wins: ONE win = ONE solves and DUAL does not.)
- KB2 P01-vs-P05 contrast (B1+B2, 20 easy/open pairs): DUAL must show
  conf(solvable) > conf(open) on >=18/20 pairs or its scoring rubric is
  falsified. ONE must show conf(solvable)>0 AND conf(open)=0 on every pair
  within bound, or its discriminating-withhold claim is falsified.
- KB3 transfer (B4): if ONE >=10/15 and DUAL <=6/15, DUAL's interface is
  falsified as domain-fragile.
- KB4 audit coherence: 3 independent grader subagents rate each solved
  problem's audit trail 1-5 (circularity, unwarranted steps, magic
  knowledge). Requires inter-rater alpha >0.8 or the bar is void. If ONE's
  mean exceeds DUAL's by >=1.0, DUAL is falsified as audit-hostile.
- KB5 false rules (B5): if DUAL produces >=50% more incorrect conclusions
  than ONE across injection levels, DUAL is falsified as more gullible; if
  ONE produces >=50% more, ONE is falsified as more fragile to contradiction.
- KB6 scaling (B6): DUAL's derivation count must be <=1/10 of ONE's, or
  DUAL's efficiency advantage is falsified as unnecessary. (A bar DUAL is
  predicted to win — included for honesty.)

## 7. Head-to-head verdict rule
Count kill bars won per engine (KB2 has two sub-bars, one per engine).
Most bars won = head-to-head winner. Ties or void bars reported honestly;
a tie is a finding, not a failure. The verdict states for each bar:
PASS/FAIL/VOID with the measured numbers.

## 8. Determinism and honesty
- 3x byte-identical reruns per problem per engine; any divergence voids
  that problem's result for that engine (reported, not silently rerun).
- Zero RNG in either engine or the test harness. Sealed solutions never
  read by engines (guarded reader, exit 3 on violation — same as attempt.zag).
- No bluffing: an engine may only output claims it derived (ONE) or that
  survived refereeing with scored evidence (DUAL). Fabrication = build
  rejected.

## 9. Commit protocol
This prereg commits ALONE first (frozen). Then COMMIT_SCHEMAS.md. Then one
build commit per engine (sources only; no binaries, no .zagd). Then
evidence + verdict commits. Incremental commits, never a giant final dump.
