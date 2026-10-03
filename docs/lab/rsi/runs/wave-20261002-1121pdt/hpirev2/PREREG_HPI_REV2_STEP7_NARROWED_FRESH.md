# PREREG: H-PI-REV2 step-7 narrowed claim, fresh freeze (FROZEN)

Status: FROZEN (drafted wave-20261002-1121pdt, HPIREV2 lane; the lane
worker commits this document alone before any step-7 narrowed
implementation file, transcript, binary, or build log exists in the
lane; commit-order self-check applies; UNVERIFIABLE ORDERING voids
this prereg). The eight fresh world files (40 files: TW/FW/RW/EW/
CONFLICT per world) were designed and mechanically validated during
prereg preparation; their sha256 hashes are frozen in this document
and the executor verifies them at load time before any run. No
implementation, no execution follows this freeze in this wave beyond
what this text specifies; any further amendment must be committed
transparently and re-frozen before execution; no bar may be altered
after seeing results. Builders report BUILD-PASS/BUILD-FAIL only.

## Provenance and why this is a fresh freeze

Step-7 (wave-20261001-2021pdt) returned FAIL with bounding on the
bounded-L2 revision claim: the claim BOUNDED to single-conflict
revision (family B trips K-OOD-W1/W3); it was not killed and not
voided. The wave-20261001-2321pdt follow-up froze a narrowed
single-conflict prereg (00b31af53), executed it (ec52cf1ca:
BUILD-PASS on 5 worlds A2/B1/B2/C2/D2), and received independent
review (5f53f1c7a: RT-HPIREV2 QUALIFY with Q1 certification erratum
and Q2 rank-bias accommodation qualifier). The RT adversarial family
then CONFIRMED two load-bearing facts: ADV-S4 (a valid
single-conflict world the procedure fails, fails_total=1) and
ADV-M1 (masked second conflict, silent success). The wave debate
ruled OVERTURN (further narrowing) on Q2: the bound holds only on
rank-diagnosable single conflicts, with probe-dependent trip;
citation must carry both qualifiers. The wave-20261001-2321pdt
prereg is therefore SUPERSEDED by this fresh freeze, not amended:
the claim below is strictly narrower, and the killed parts are not
smuggled back.

Killed parts (must not reappear): the unqualified "revises
correctly on every single-conflict world" (killed by ADV-S4); the
unqualified "never silent wrong convergence" (killed by ADV-M1).
This prereg does not re-litigate them.

## The narrowed claim (one mechanism, one question)

The frozen revision procedure (proc_revise2.zag at 847a8f10f,
sha256
dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12;
machinery lines 1-606 sha256
8d2b16ab31184758b2b724e19cb1fa9f96d5ff008a0674b6c95c1da8e227f712)
revises correctly and cheaply on sealed single-conflict worlds
whose conflict coincides with the frozen rank-1 diagnosis
(position-ascending (pos,byte) over the failing FW record), across
novel base programs, consequents, bytes, positions, and lengths; on
multi-conflict worlds it flags the uncovered conflict explicitly
when that conflict is independently probed, but can report silent
success when the uncovered conflict is masked in all probed pairs.

Question: does the frozen procedure meet the frozen bars below on
four fresh sealed rank-diagnosable single-conflict worlds (R1-R4),
does it produce the frozen explicit-trip signal on two fresh sealed
probed two-conflict worlds (P1/P2), and do the two boundary worlds
(X1 rank-invisible single conflict, X2 masked two-conflict) behave
as the qualifiers predict (loud fail on X1, silent success on X2)?

## Frozen reference points (not re-decided here)

- Frozen mechanism: proc_revise2.zag at 847a8f10f (hashes above).
  Cognition source delta must be 0.
- Frozen executor lineage: the step-7 harness approach (frozen
  machinery lines 1-606 byte-verbatim plus a new staging main) is
  reused; harness code is recorded separately from cognition source.
- Ceiling: bounded L2, not L3. A BUILD-PASS here means the narrowed
  claim holds on the tested worlds; it is not evidence toward L3
  and must not be claimed as such. It is never SURVIVES.
- The wave-20261001-2321pdt narrowed prereg (00b31af53) and its
  BUILD-PASS (ec52cf1ca) stand as historical records under their
  own qualifiers; this freeze supersedes them for forward citation.
  Every citation of the H-PI-REV2 result must carry the debate Q2
  qualifiers: bound holds only on rank-diagnosable single
  conflicts, with probe-dependent trip.

## The eight fresh worlds (step-7 worlds are regression only)

Each world has five files: TW.txt (3 base pairs), FW.txt (1
counterexample pair), RW.txt (1 held reuse pair, sealed from the
revision phase until revision completes), CONFLICT.txt (declared
conflict set), EW.txt (intended rule R_w in words). Pair notation:
one pair per line as key=value. All bytes are from the fresh
alphabet {f,g,=,<,>,?,@,[,],{,|,}} disjoint from all prior world
bytes (verified by grep over all prior world files).

Design seeds (committed here):

- R1 (novel base): single conflict (0,61); base program 39
  (repeat input[n-2]); trigger byte '='; predicted V0=39, DIAG
  (0,61), ALT=4 (const 2), revision_evals=5.
- R2 (novel consequent): single conflict (0,60); base program 4
  (const 2); trigger byte '<'; FW consequent is the non-const
  program 50 (2-k); predicted V0=4, DIAG (0,60), ALT=50,
  revision_evals=5.
- R3 (longer inputs): single conflict (0,62); base program 2
  (const 0); TW lengths 9/11/8, FW/RW lengths 8/9; trigger byte
  '>'; predicted V0=2, DIAG (0,62), ALT=4, revision_evals=10.
- R4 (novel base shape): single conflict (0,63); base program 629
  (n-4, smallest benum index for that function); trigger byte '?';
  predicted V0=629, DIAG (0,63), ALT=4, revision_evals=6.
- P1 (probed two-conflict): conflicts (0,61)/alt1=4 and
  (2,62)/alt2=2; base 39; FW probes conflict 1, RW probes conflict
  2; explicit trip expected (S1-S3).
- P2 (probed two-conflict): conflicts (0,63)/alt1=4 and
  (1,64)/alt2=3; base 2; FW probes conflict 1, RW probes conflict
  2; explicit trip expected (S1-S3).
- X1 (boundary: rank-invisible single conflict): true trigger
  (2,62), diagnosed (0,60); base 39; the rank-1 diagnosis does not
  select the true conflict; loud fail expected (fails_total=1),
  confirming the rank-diagnosability qualifier is load-bearing.
- X2 (boundary: masked two-conflict): conflicts (0,61)/alt1=4 and
  (2,62)/alt2=3; base 2; the second conflict byte never appears at
  position 2 in FW or RW; silent success expected, confirming the
  probe-dependent trip qualifier.

Frozen sha256 hashes (executor verifies at load time; any mismatch
aborts the run, no verdict). All hashes are 64 hex characters
(verified mechanically; lesson of the Q1 erratum).

R1_CONFLICT.txt 19f022273ccc327c5ea0b6d12593fc4dbad4c3eb0b96cb3b93b21a5681f5bd94
R1_EW.txt 02a369c36cc03a9e5846e91f2ae4fab2d48df09b876f4089ddfae3b66157cf46
R1_FW.txt cab41140a20706cd22761ed5d4b7a41c28b4c8fc0f8513f124084b6b9a095ece
R1_RW.txt 8322ef400524dd1f46eb9ca9ffaf12c701d25f0835e40bbfda9f9eb2ee640322
R1_TW.txt 7c8c917577415832791014ecc73528d85f67cd2f3e2717f1755e21b24d4d1876
R2_CONFLICT.txt 28bee01ee9edb05c38ee14b6a21d9ca4082abc8c72f169b0cead5bbe51b0d49e
R2_EW.txt 846dba18dd74c3daac688000fac3101ef5ba9bf6fdd3c6dd737b4852ff8812de
R2_FW.txt 3039d23ae9d3675ba40d23562c9ce9ac56caa9c354040b01fa1ffd2fd69a047a
R2_RW.txt 44fe960dd1f22f912450c19d30ee78a6de3465e1e15fa705abf22bc143306fc2
R2_TW.txt d95909d6c0a1008c107c9b4b0fa523639b4b70d015409a6f29452314466f1f94
R3_CONFLICT.txt f7f5346a7b1a23d77571c346121e8bc94f21d0cd8bdc98d801be7b2498295a85
R3_EW.txt 289b89bcf64d7d5d945b97a0b43e3040c78feed2f09a4d6fae5e7649fc67bc41
R3_FW.txt f88c6230dc4069d0bece07615e94f971dcfbc8a3fbf002626736e1415881fe88
R3_RW.txt 426a8c0c2f9083ff706ab62943268e0477ac51146e255e4c14062c74013256a6
R3_TW.txt 1db664a10b8cca098609a1e2183562dd43301735a5dc2f39cc2f11ddcc4f39cd
R4_CONFLICT.txt e1c1098c2f8295a6055cd3c35240a2e0ee3d3366c271e9ecbe79a5fda5e40bc2
R4_EW.txt be580d485cdf42dab908b8ba0234e149f8a456e750d1dae53acf60192078478f
R4_FW.txt 7710d2aa7d8ceee9d02c64f55eae2a506b0fcfc0ff5c361f513edf026d38ed24
R4_RW.txt 1a99b812d9eb31bec1791a02ea3a9d2643d911bc8afa79d0b8460bbea036621a
R4_TW.txt 3122cd54ec69ea49a57a7295879076eaf158a01d4a980e7007f330b1dfa14a10
P1_CONFLICT.txt cf3003d85463e73f4904844377f148a4038867814f46a6e00fed9c3e94ef9581
P1_EW.txt 96a8e99813d65b6385dfb9d72661352701dc410c45996d7f9c548d357d0f8e8d
P1_FW.txt 1fe62cb1659c8be3f010762a5d458def4bd9fc58e49330310086312c4b0d891a
P1_RW.txt 2be9c4276b5c81b36c5a599efcc4dae3c2c44764f49a0f01ccaff1dcb99c71dd
P1_TW.txt 7c8c917577415832791014ecc73528d85f67cd2f3e2717f1755e21b24d4d1876
P2_CONFLICT.txt 32e1909a6cb70208203b3b450563c6a060b516a1ba6af37db5f692f06150fad2
P2_EW.txt b1c2c003f74d1f28f66b2c2e655c76c3fcc6243d1ce928627855a8fd1cb76a2f
P2_FW.txt 6c0e6bda47d5ccd6f286bc89fe7791e81b73d256e4c8679b970eb3f587805153
P2_RW.txt 480e566eda3155d1f6d969718796efc33832950ce35aee74c296b92751294a96
P2_TW.txt c36c658ecb9807a5242a384a5d764589c29d6b5d831e859e87b95d8501570d52
X1_CONFLICT.txt 943b7f879c06945d2cf72a77de2747f2bfd255068c3ac92d305fe2fcf7d52ab4
X1_EW.txt 6961ed274d0f1ea62ea9ab454fb8fddc3cea1a0fc5f554b9f5df18616f5d05b6
X1_FW.txt 353ed166ff16a5b2e74db6573e24ae773902d29ab1d158899de13b397f18935e
X1_RW.txt cf826fb0647265af977f3fe07954bfb410ce6d4ad0b0e293c9ef45ffe4e2888d
X1_TW.txt 7c8c917577415832791014ecc73528d85f67cd2f3e2717f1755e21b24d4d1876
X2_CONFLICT.txt be9637693d82e9ff398751dbddbac67c6d0c9adea7a091f245ac0492731b291d
X2_EW.txt 318048ab5b5b81d225469f4cf3d2f684ca0bc1058c749ca589c304a8d0b44a2a
X2_FW.txt 1fe62cb1659c8be3f010762a5d458def4bd9fc58e49330310086312c4b0d891a
X2_RW.txt 32f61d15f5017d27623a4a7955a232ca7b3e2c0dc9bed4610a6a2f534033f7c3
X2_TW.txt c36c658ecb9807a5242a384a5d764589c29d6b5d831e859e87b95d8501570d52

## World validity prechecks (void, never a verdict)

The executor runs these mechanically before any revision execution,
using only frozen baseline code; any failure voids that world and
the whole narrowed run: no verdict is recorded, and the remedy is a
transparent amendment with a redesigned world, re-frozen. A malformed
world must never be laundered into a FAIL.

- V0 (base learnable): frozen dsearch over the 1055 benum programs
  on TW alone achieves first_fit >= 0 with fails-on-TW=0. Record
  w_first_fit_tw. Must equal the design seed base (R1:39, R2:4,
  R3:2, R4:629, P1:39, P2:2, X1:39, X2:2).
- V1 (disjointness and placement): bytes(FW input) disjoint from
  bytes(TW inputs); the declared conflict bytes are a subset of
  bytes(FW input); bytes(RW input) disjoint from bytes(TW inputs)
  except for declared conflict bytes; RW's input matches each
  declared conflict at its declared position (P1: (0,61) and
  (2,62); P2: (0,63) and (1,64); X2: (0,61) only, conflict 2
  masked by design).
- V2 (problem real): v1w (the V0 first fit) mispredicts FW.
- V3 (impossibility recheck): dsearch over TW+FW evaluated against
  EW restricted to TW+FW enumerates all 1055 benum programs with
  first_fit=-1.
- V4 (expectation consistency): EW equals R_w applied to the check
  inputs, where R_w is the declared rule (single IF for R1-R4/X1,
  two-level IF for P1/P2/X2).
- V5 (rank-diagnosability, new): for R1-R4 only, the frozen
  diagnose on the FW record returns the declared conflict
  (pos,byte) exactly. Void if the diagnosis does not coincide with
  the declared conflict. (P1/P2/X1/X2 are exempt: they test the
  multi-conflict and boundary regimes, not the rank-diagnosable
  single-conflict claim.)

## Frozen kill bars

Per world w in {R1, R2, R3, R4}; BUILD-PASS requires all of them.

- K-RW1 (correctness, accuracy floor 100 percent): the revised
  procedure achieves fails=0 on all EW pairs. Kill: any
  w_fails_total > 0. A trip KILLS the narrowed claim: the bound is
  exactly rank-diagnosable single-conflict, so a failure there
  falsifies even the narrowed claim.
- K-RW2 (revision-eval ceiling): revision_evals <= 25, strict.
  Kill: revision_evals > 25.
- K-RW3 (reuse): RW is predicted correctly with zero new
  DIAGNOSIS, PRIMITIVE-CONSTRUCTED, or VERSION lines after the
  reuse check. Kill: any misprediction or any new revision marker.
- K-RW4 (determinism): per world, 3/3 runs byte-identical
  (sha256 match), exit 0, zero stderr bytes. Run matrix: 24 runs
  (8 worlds x 3). Kill: any divergence, nonzero exit, or any
  stderr byte.
- K-RW5 (purity and docs): pure Zag only at every stage; zero
  Python; zero em-dash and zero en-dash bytes in all new lane
  files (byte-checked). Kill: any Python use or any forbidden
  byte.

Probed two-conflict bars (the flagging half of the narrowed claim):

- K-PB (explicit trip on probed multi-conflict, never silent wrong
  convergence): on P1 and P2, 3/3 runs exhibit ALL of: (S1)
  w_fails_total > 0, the run reports failure on EW and does not
  claim success; (S2) the transcript contains
  COUNTEREXAMPLE_DETECTED at the W3 reuse probe for the held-out
  RW, the uncovered conflict is explicitly flagged when probed;
  (S3) zero new DIAGNOSIS, PRIMITIVE-CONSTRUCTED, or VERSION lines
  appear after the W3 marker, the mechanism does not silently
  re-revise into a wrong stable state. Kill (silent wrong
  convergence): w_fails_total=0 on P1 or P2, or no
  COUNTEREXAMPLE_DETECTED at the reuse probe. A trip KILLS the
  flagging half of the narrowed claim.

Boundary-honesty bars (HOLD on mismatch, never a claim-kill):

- K-X1 (rank-invisibility boundary): on X1, the expected outcome
  is loud fail (w_fails_total=1), confirming the
  rank-diagnosability qualifier is load-bearing. If X1 instead
  reports w_fails_total=0, that is a HOLD (the mechanism exceeded
  the claim; investigate, do not kill). If X1 fails loudly as
  expected, the qualifier stands confirmed.
- K-X2 (masking boundary): on X2, the expected outcome is silent
  success (w_fails_total=0), confirming the probe-dependent trip
  qualifier. If X2 instead trips explicitly (w_fails_total > 0
  with COUNTEREXAMPLE_DETECTED), that is a HOLD (the mechanism
  was more conservative than the claim requires; investigate, do
  not kill). If X2 reports silent success as expected, the
  qualifier stands confirmed.

Architecture bars (preserved):

- K-ARCH1 (zero cognition source delta): the frozen mechanism
  source is byte-identical before and after; cognition source
  delta = 0 exactly. World files, validator, and test harness code
  are recorded separately. Kill: any nonzero cognition source
  delta.
- K-ARCH2 (no architecture growth): new_semantic_cases=0,
  new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
  protected-core changes. Kill: any nonzero value.

## Verdict semantics

BUILD-PASS: every kill bar above holds; both boundary bars behave
as expected (or HOLD with documented investigation); cost
accounting complete.
BUILD-FAIL: names every tripped kill bar. A K-RW1/W2/W3 trip on
any R world, or a K-PB trip, KILLS the narrowed claim as stated
(it is already the narrowed residue; there is no further honest
narrowing without changing the question). A K-RW4, K-RW5,
K-ARCH1, or K-ARCH2 trip is FAIL with cause named (determinism,
purity, or architecture): no claim about the mechanism follows
because the failure is in the run's premises, recorded as
information gained. A HOLD on K-X1 or K-X2 is not a FAIL: it is
recorded as information gained and triggers investigation, never
a verdict change. Any validity precheck failure: VOID, never a
verdict; transparent amendment with a redesigned world,
re-frozen. No outcome here weakens, reinterprets, or re-scores
any frozen bar from steps 5, 6, or 7; the step-7 FAIL-with-bounding
record stands, as do the wave-20261001-2321pdt records under
their own qualifiers.

## Sealed evaluation protocol and disclosure

- The eight worlds were designed and mechanically validated by the
  lane worker (non-independent: no separate adversary or red team
  was available in this wave). Mitigations, frozen here: the
  world designs and the sha256 of all 40 world files are committed
  in this prereg before any execution; the executor verifies
  hashes at load time; the executor re-runs V0-V5 mechanically
  and any void triggers transparent amendment and re-freeze,
  never silent repair; no world may be tuned after seeing
  execution results.
- The pre-freeze mechanical validation ran the frozen dsearch,
  diagnose, and scoring logic over the world designs: V0 first
  fits (39/4/2/629/39/2/39/2), V1a-e, V2 det=1 on all eight, V3
  first_fit_twfw=-1 on all eight, predicted DIAG winners
  (0,61)/(0,60)/(0,62)/(0,63)/(0,61)/(0,63)/(0,60)/(0,61),
  predicted ALT first fits (4/50/4/4/4/4/4/4), predicted
  revision_evals (5/5/10/6), V4 EW consistency, V5
  rank-diagnosability on R1-R4: ALL-WORLDS-VALID, exit 0. Design
  slips found and fixed pre-freeze (R1/P1/X1 TW did not
  discriminate base 39 from program 3; R2/R3 TW violated the
  extract_seq uniqueness requirement; R4 base 979 was not the
  smallest index for n-4, corrected to 629; R4 FW consequent
  changed from reversal to const for clean generalization; R4 RW
  length miscount); the frozen hashes above are of the corrected
  files.
- Per world execution order: load-time hash verify, V0-V5
  prechecks, train v1w, present FW, run the frozen revision
  (record revision_evals), score against EW (W1, W2), present RW
  after revision ACTIVE (W3). Repeat 3x per world (W4). 24 runs.
- The executor uses only the frozen mechanism machinery and
  frozen baseline code; the harness stages world literals
  transcribed from the sealed files, verified byte-exact (STAGE
  lines diffed); no world-specific branching, no new semantic
  cases, no modes, no bridges, no routers, no handlers. RW is
  never observed before the W3 phase.
- Code-sharing disclosure is mandatory in the result doc.

## Cost accounting (required in the result doc)

Machine-greppable fields, per world w in
{R1,R2,R3,R4,P1,P2,X1,X2}: w_first_fit_tw, w_b1w_enumerated,
w_revision_evals, w_fails_total, w_reuse_correct,
w_reuse_new_revision_lines, w_wall_ms; plus binary_bytes (each
binary), source_delta_lines (harness and validator only),
cognition_source_delta (must be 0), new_semantic_cases,
new_modes, new_bridges, new_routers, new_handlers. Kill: any
missing field; any nonzero architecture-growth field; any nonzero
cognition_source_delta.

## Honest boundaries: bounded L2 ceiling, NOT L3, never SURVIVES

This follow-up does not test representational invention, template
invention, or any L3 criterion. A BUILD-PASS means the narrowed
claim holds on the eight tested worlds; it is not evidence toward
L3 and must not be claimed as such. It is never SURVIVES:
remaining pipeline steps (transfer/reuse beyond the single probe,
second independent red team, governance audit) are untouched.
Nothing here alters the step-5 PASS, step-6 PASS, or step-7
FAIL-with-bounding records, nor the wave-20261001-2321pdt
BUILD-PASS/QUALIFY records under their qualifiers.

## Skeptic self-attack (and answers)

Attack 1: the worlds were designed and validated by the same
worker that executes, so the seal is theater.

Answer: the pre-freeze fixes are disclosed above, and tuning
pre-freeze is the legitimate role of design plus certification.
The seal binds post-freeze: hashes are frozen here, the executor
re-verifies V0-V5, and any void forces transparent amendment and
re-freeze rather than silent repair. The non-independence is a
stated limitation, not a hidden one, and it caps the claim: this
is a narrowed re-test, never SURVIVES, and a second independent
red team remains a pipeline requirement.

Attack 2: the narrowing is just relabeling the ADV-S4 and ADV-M1
kills as qualifiers; the claim now says "it works where it works."

Answer: the qualifiers are operational, not tautological. V5
(rank-diagnosability) is a mechanical precheck on the world, not
on the outcome: a world either has its conflict at the rank-1
diagnosis or it does not, decidable before execution. X1 tests
the boundary directly: if the mechanism passed X1, the qualifier
would be shown unneeded (HOLD, investigated). The probe-dependent
trip is likewise operational: P1/P2 vs X2 differ only in whether
the second conflict is probed, decidable from the world files.
The claim predicts different outcomes for P1/P2 (trip) vs X2
(silent success) on mechanically distinguishable inputs; that is
a falsifiable prediction, not a tautology.

Attack 3: eight worlds cannot establish even a bounded claim; a
PASS here is eight anecdotes.

Answer: the claim is already bounded to rank-diagnosable
single-conflict revision plus the two probe regimes, and the
eight worlds span the dimensions the step-6 ablation pinned as
load-bearing (bytes, position, length, template shape) plus the
probed/masked multi-conflict boundary. The verdict claims only
the tested regimes, never broad generality, and the
never-SURVIVES rule caps inflation.

Attack 4 (red-team of the narrowing): did the fresh prereg
accidentally re-broaden the claim? Check each phrase against the
killed parts. "Revises correctly and cheaply on sealed
single-conflict worlds whose conflict coincides with the frozen
rank-1 diagnosis": the qualifier "whose conflict coincides with
the frozen rank-1 diagnosis" is the ADV-S4 exclusion, present and
load-bearing (X1 tests it). "Flags the uncovered conflict
explicitly when that conflict is independently probed, but can
report silent success when the uncovered conflict is masked in
all probed pairs": the "can report silent success" is the ADV-M1
accommodation, present and load-bearing (X2 tests it). No phrase
promises correctness on non-rank-diagnosable single conflicts; no
phrase promises never-silent convergence. The K-X1/K-X2 bars are
HOLD-on-mismatch, not kill bars, so they cannot launder a
boundary exceedance into a claim expansion. The narrowing holds.

## Commit-order self-check (binding)

This prereg must be committed ALONE before any step-7 narrowed
implementation file (validator source beyond this commit,
executor harness source, binary, transcript, or build log) exists
in the lane. Verification: `git log --format=%H -- <this file>`
must show exactly one commit for this file, and that commit must
strictly precede the first commit adding any narrowed-step
implementation artifact. The world files in worlds/ are design
artifacts whose hashes are frozen here; they are committed after
this prereg. UNVERIFIABLE ORDERING voids this prereg. No bar may
be altered after results are seen.

No em-dashes in this documentation.
