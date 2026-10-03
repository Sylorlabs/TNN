# T6 Sealed Task Specification: Draft

Status: DRAFT ONLY. This document is a draft specification for the sealed T6
capstone task of Battery v2. It is not the sealed spec. It authorizes no
implementation and no evaluation. The sealed T6_SPEC.md will be written later
by an independent adversary worker per the sealing protocol in section 7,
strictly after the section 1 gate is satisfied. This draft contains no T6
implementation, no frozen episode lists, no hidden answers, and no code.

Ancestry: Battery v2 prereg `d2a69d512` (frozen); design `611e8fa1f`.
Authoring: pure text edit, no Python used.

## 1. Role and gating

T6 is the sealed adversary capstone of Battery v2. Canonical name stays T6
under the "Battery v2" version.

Gate (v2 prereg section 3.7, frozen): T6 evaluation launches only after ALL
of: (i) freeze commits of every hypothesis evaluated under v2 (B, C2, and
D's K4-clean rerun commit) are in ancestry; (ii) the Battery v2 prereg is
frozen (`d2a69d512`, satisfied); (iii) the sealed T6 spec commit strictly
follows (i) and (ii). A and C were falsified under v1 and do not gate T6.

This draft is a prerequisite work product, not a gate item. The draft commit
does not count as the seal.

## 2. VM variant

Recommendation: T6 targets GENEXEC2-P (the restricted VM: jumps, calls,
arithmetic, and stack operations; DIV, MOD, LT, EQ, GT removed).

Rationale:

(a) The P-VM conditional line T1/T4/T5 is the battery's key discriminator,
and T6 as capstone should extend that line rather than open a new VM axis.

(b) On the full VM, DIV and MOD admit arithmetic shortcuts that bypass
intended control flow (the v1 D lesson: a straight line ABS program via
MOD). On GENEXEC2-P, any non straight line target forces jumps, and any
jump free solve of a conditional T6 fires F-TRICK, so the kill switch acts
as a true anomaly detector instead of a routine audit.

(c) The retained jumps are exactly the machinery T6 is meant to probe.

The sealed spec states the final VM choice. If the adversary chooses the
full VM instead, it must record why in the sealed spec, and the V2 audit
burden on any straight line solve is heavier.

## 3. Validity constraints (v2 restatement)

Carried over from v1, restated for v2. All mandatory.

- V1 computability: a target program exists in the frozen op set of the
  chosen VM variant. The adversary exhibits it and logs its exact outputs
  on all train and held-out episodes of the sealed spec.
- V2 material difference: T6 must require a structure materially different
  from T0..T5. It must not be a straight line arithmetic map, a single kink
  absolute value, a periodic mod, or a two input parity. The exhibited
  target program must contain at least one of JZ, JNZ, JMP, CALL.
- V3 budget adequacy: the exhibited target program has at most 40 ops
  total (main program plus all called fragment bodies), the same envelope
  as v2-SOLVE.
- V4 episodes: at least 9 train episodes and at least 8 held-out episodes,
  held-out disjoint from train, both fixed in the sealed spec.
- V5 no reverse engineering: the adversary records which conditional
  predictions T6 is intended to discriminate, but T6 must satisfy V2 on its
  own structural merits, independent of the predictions.

v2 additions that apply to T6:

- v2-SOLVE: exact integer equality of top of stack with the target on ALL
  train episodes AND total program ops (main plus all called fragment
  bodies) at most 40.
- F-TRICK: any jump free GENEXEC2-P program achieving v2-SOLVE on T6 voids
  the task pending re-investigation.
- F-SMUG: DIV, MOD, LT, EQ, or GT anywhere in the final program (main plus
  all called fragment bodies) voids the exhibiting result.
- F-MEM: a memorization style solve over the 40 op cap is not SOLVE.
- Confirmation rule (prereg section 3.6): a prediction is CONFIRMED iff the
  observed outcome matches under v2-SOLVE and the committed construction
  trace shows the predicted mechanism via the mandatory trace events.
  Outcome match without mechanism trace is UNCONFIRMED.

## 4. Task family

Primary recommendation: kinked polynomial piecewise (the "quadratic kink"
family). Parametric form: a piecewise integer function with at least 3
regions, at least one nonlinear region (quadratic via MUL; no DIV needed),
and at least one constant or linear region, with region boundaries at small
integer kinks. Illustrative shape only, not sealed: quadratic on the left,
flat in the middle, linear on the right.

Why it satisfies V2: no T0..T5 task contains any nonlinear region. Every
piecewise task so far (T1, T4, T5) is linear pieces. A quadratic region is
a new structure class, and the exhibited target needs at least two boundary
tests, hence JZ or JNZ in the target program.

Difficulty: strictly harder than T5 (3 linear pieces via fragment
composition) along a new axis. A solver must both partition the input
(control flow) and synthesize a non affine region map (MUL). Exhibited
targets are under 20 ops, inside the 40 op envelope.

Alternates the adversary may choose instead. Each must still pass V1..V5
on its own structural merits:

- Alt 1, bounded iteration (triangular accumulation): f(x) = 1 + 2 + ...
  + x. Forces a loop (JMP/JNZ) with an accumulator. Unambiguously
  materially different: no prior task requires iteration. Predicted outcome
  is FAIL for all three hypotheses, so this alternate marks the loop
  frontier rather than discriminating. Choose it if the capstone goal is
  frontier marking over discrimination.
- Alt 2, nested conditional with a trap region: 4 or more linear regions
  where one region is a constant trap that punishes over splitting (a
  C-F3 style guard). This is closer to T4, so the adversary must defend V2
  material difference explicitly in the sealed spec if choosing it.

This draft does not fix the family. The adversary selects one, defends V2
in the sealed spec, and records the intended discriminations per V5.

## 5. Difficulty calibration

- Episode budget: train at least 9, held-out at least 8, disjoint (V4).
  Recommended scale: 13 train and 8 to 12 held-out, matching T4/T5, so
  difficulty comes from structure rather than episode count.
- Op envelope: exhibited target under 20 ops, hard cap 40 (V3, v2-SOLVE).
- Harder than T4/T5: T4 has 4 linear pieces; T5 composes 2 conditional
  fragments. The primary family adds a nonlinear region and 3 or more
  regions, so a solver needs partitioning plus non affine synthesis.
- Not harder than the envelope: a sealed task no hypothesis could touch
  even in principle is a bad capstone. V1 requires the adversary to prove
  solvability within budget by exhibiting the target program.

## 6. Discrimination goal

Hypotheses evaluated under v2: B (fragment retrieval), C2 (counterexample
guided splitting with lookahead and bounded backtracking), D (MAP-Elites
straight line synthesis). A and C are not evaluated.

Staked conditional predictions for the sealed T6, to be restated in the
sealed spec per V5:

- D: predicted FAIL. D is straight line only on the polynomial VM (Lemma 2
  carried over); a conditional or nonlinear piecewise target is out of
  reach. A D v2-SOLVE on T6 triggers a V2 audit: either the sealed function
  admitted a straight line shortcut (adversary error, task void) or D
  gained control flow (smuggling audit under F-SMUG/F-TRICK).
- B: predicted FAIL unless B's prereg was transparently amended with a case
  capable base constructor before any v2 evaluation (prereg section 4, star
  condition). If amended, B must show the section 3.6 trace events: at
  least 2 retrieval events with behavioral match recorded before each CALL,
  and at least 2 CALLs to the same P-VM valid fragment id. An unamended B
  SOLVE on a conditional T6 fires an F-SMUG/F-TRICK audit.
- C2: conditional SOLVE. C2's predicted path: split events tracking the
  true region count (C-F3 guards over splitting), each region repaired, 0
  CALLs in the final program. The key discriminator on the primary family
  is whether C2's repair synthesizes the nonlinear region. C2 SOLVE with a
  trace showing region count tracking is the CONFIRM path. C2 FAIL on the
  quadratic region while solving the linear regions localizes the repair
  boundary precisely.

Sharpest signals:

(a) C2 SOLVE with B FAIL and D FAIL on the primary family confirms the
split and repair mechanism beyond linear pieces, and gives B its sharpest
C0-C signal: no novel primitive required, still FAIL.

(b) An all FAIL outcome on Alt 1 marks the iteration frontier and redirects
the program toward loop synthesis.

(c) Any D SOLVE or any jump free SOLVE on a P-VM T6 voids or audits per
F-TRICK and V2. No quiet patch is permitted.

## 7. Sealing protocol

Who: an independent adversary worker, independent of the B, C2, and D
implementers and of this draft's author. The adversary must not have
implemented or debugged any hypothesis evaluated under v2. Exactly one
worker is named in the seal commit message.

When: strictly after the section 1 gate. Verify with git ancestry: every
hypothesis freeze commit and `d2a69d512` are ancestors of the seal commit,
and no T6 evaluation commit exists yet.

How:

- S1: the adversary writes T6_SPEC.md (function definition, exact train and
  held-out episode lists, exhibited target program with op count,
  verification run log showing exact outputs on all episodes) into
  `battery_v2/sealed/`. The sealed spec states the VM variant (section 2),
  defends V2 material difference, and records intended discriminations
  (V5).
- S2: the adversary commits T6_SPEC.md alone (no other files in that
  commit) and records the sha256 of T6_SPEC.md in the evaluation log. The
  commit message tags the seal.
- S3: at evaluation time the harness exposes ONLY the train episodes to
  each frozen hypothesis. Held-out episodes and the target program are
  revealed only after all hypotheses report on T6. No hypothesis code
  changes between seal and reporting; any change voids that hypothesis's T6
  run. A re freeze would require a new sealed spec, because the old train
  episodes are then seen.
- S4: any T6 evaluation run whose ancestry does not show the seal commit
  after all implementation freeze commits is void. Verify with
  `git merge-base --is-ancestor` before accepting results.

Void conditions: F-TRICK firing on T6 voids the task pending
re-investigation (prereg section 3.6). F-SMUG voids the exhibiting result.
A post seal contestant change voids the run per S3. A broken gate (seal
before all freezes) voids the seal itself.

Aftermath: once all hypotheses report, the held-out episodes and the
exhibited target are published with the battery results, and the sealed
directory becomes ordinary committed history. No L3 claim follows from
battery success alone (prereg section 3.6). After a CONFIRMED battery, the
mandatory Criterion 0 sequence applies: source audit, persistence, reuse,
transfer, revision, adversarial unseen structure.

## 8. Kill bars for this draft

- K1 draft complete: this document specifies the task family (section 4),
  difficulty (section 5), and discrimination goal (section 6).
- K2 sealing protocol specified: section 7 names who generates the sealed
  spec, when (gate plus ancestry verification), and how (S1..S4, sha256
  recording, harness exposure rules, void conditions).
- K3 no implementation: this draft contains no T6 implementation, no frozen
  episode lists, no hidden answers, and no code. The exhibited target
  program does not exist yet; the adversary writes it at seal time.

Builder label: T6-DRAFT-COMPLETE.
