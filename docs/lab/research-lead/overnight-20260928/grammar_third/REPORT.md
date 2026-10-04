# REPORT: Grammar Third-System Worker

## Verdict: GRAMMAR-THIRD-COMPLETE (with breakage diagnosis)

## Claim tested

The transfer report made the induction machinery's world assumptions
explicit: (1) the verification lookup gi_trial_build2 references eval
relations 41/42; (2) the rubric gi_classify references decomp ids 43/44
and literal range 0..9; (3) pair decoding assumes P(a,b) = a*16+b.
EXL3 breaks exactly ONE of these, assumption (3), to find which stage
breaks first and whether the machinery fails closed or goes
silently wrong.

## EXL3: the third formal system

Literals 0..7, pair encoding P(a,b) = a*8+b (injective on 0..7:
8(a1-a2)=b2-b1 forces a1=a2 since |b2-b1|<=7<8, so P in 0..63 is unique
per pair; researcher-owned, taught via examples).

| EXL2 (prior)       | EXL3 (this probe)          |
|--------------------|----------------------------|
| SUB=41, DIV=42     | SUB=41, DIV=42 (unchanged) |
| DSUB=43, DDIV=44   | DSUB=43, DDIV=44 (unchanged) |
| BUILD=45           | BUILD=45 (unchanged)       |
| P(a,b) = a*16+b    | P(a,b) = a*8+b (BROKEN)    |
| literals 0..9      | literals 0..7 (inside 0..9)|

Constraint shapes identical to EXL2, taught via examples only:
SUB (P(a,b),41,a-b) only when a-b >= 0; DIV (P(a,b),42,a/b) only when
b>0 and a/b exact. TRAIN targets {1,3,5,7} with alternating
DIV-first/SUB-first canonical BUILD examples (4 BUILD facts, the only
BUILD supervision). TEST targets {0,2,4,6} (4 novel, disjoint). SUB/DIV
on literals 0..7 admits exactly 8 target values, so 4 TRAIN / 4 TEST is
the maximum-disjoint split.

## Machinery-identity proof

- g3_base.zag SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  identical to gt_base.zag (2 files share the digest).
- g3_patch.zag SHA-256 ae94800e0167d72aaba3879216699c3be2fbdc5d7c60eeea62428594c3db50d3,
  identical to gt_patch.zag (2 files share the digest). This file holds
  ALL induction, construction, ablation, and classification logic. Zero
  bytes changed.
- Driver: gi_report_grammar, gi_arm_induce, gi_arm_base,
  gi_arm_hardcode verified byte-identical per function to gt_driver.zag
  with cmp. The driver diff is confined to: the pair encoder
  (g3_P = a*8+b), teaching functions (literal loops 0..7), the
  world-specific test battery (gi_test_targets = {0,2,4,6}), and main
  (W1-W4 only; W5a/W5b contradiction arms dropped, already passed on
  byte-identical machinery in the transfer run).
- The /16 pair decode appears at exactly five sites in the
  byte-identical patch (g3_patch.zag lines): 53-54 (gi_induce part 1
  decode + sanity check), 89-90 (gi_induce part 2 range induction),
  174 (gi_trial_build2 decode + range check), 210 (gi_hardcode_build
  decode + range check), 250 (gi_classify decode + range check).

## Results (3/3 byte-identical, SHA-256 b1638370...)

Raw W1 output:
```
GI-INDUCED 1
GI-GRAMMAR nbuild=4 nlic=2 lic=44,43 a=[0,3] b=[0,15] maxlinks=1
GI-I 0 ans=9 class=1
GI-I 2 ans=16 class=1
GI-I 4 ans=32 class=1
GI-I 6 ans=48 class=1
GI-I-VALID 4/4
```

### The three-way question: SILENTLY WRONG grammar

Induction did NOT fail closed. gi_induce returned 1 and wrote a type-70
grammar node whose literal ranges are FALSE of the world:

- Induced: a=[0,3], b=[0,15] (from /16 decoding of decomp pair objects
  P in 0..63: a'=P/16 in 0..3, b'=P mod 16 in 0..15; extremes from P=0
  and P=63, both present as decomp objects).
- Truth: the world's components are a,b in 0..7 under P(a,b)=a*8+b.

The GI-GRAMMAR line reports the wrong ranges with the same confidence
as EXL2's correct ones. The battery then reports 4/4 valid, so the
wrongness is invisible in the headline score. This is the silent-wrong
outcome: a confident wrong grammar, no alarm anywhere.

Hand verification that every W1 construction is semantically valid
under the WORLD encoding (a=ans/8, b=ans-a*8):

| t | ans | world (a,b) | check        | machinery (/16) (a',b') | class |
|---|-----|-------------|--------------|--------------------------|-------|
| 0 | 9   | (1,1)       | 1-1=0 = t    | (0,9)                    | 1     |
| 2 | 16  | (2,0)       | 2-0=2 = t    | (1,0)                    | 1     |
| 4 | 32  | (4,0)       | 4-0=4 = t    | (2,0)                    | 1     |
| 6 | 48  | (6,0)       | 6-0=6 = t    | (3,0)                    | 1     |

Each ans is licensed by a true DSUB fact ((0,43,9), (2,43,16),
(4,43,32), (6,43,48)) and verifies against the true SUB eval table.
The machinery's (a',b') column is what the rubric checked; it agreed
because it uses the same wrong decode (self-consistent wrongness).

The 4 TRAIN BUILD facts the teacher actually taught, with their true
licensors (all found by induction):
(1,45,9) via DIV (1,1), licensor (1,44,9); (3,45,24) via SUB (3,0),
licensor (3,43,24); (5,45,41) via DIV (5,1), licensor (5,44,41);
(7,45,56) via SUB (7,0), licensor (7,43,56).

### Stage-by-stage: which breaks first

1. Licensor discovery (gi_induce part 1, relational): CORRECT.
   {44,43} discovered from the BUILD examples, not hardcoded.
2. The designated encoding guard (part 1 sanity check): VACUOUS.
   With a=P/16, b=P-a*16, the check `a*16+b!=P` is a tautology and
   b is always in [0,15]; the whole condition reduces to P>255.
   EXL3's P values are all <= 63 (EXL/EXL2: <= 159), so the guard
   cannot fire on any of the three systems run to date. It is not a
   check; it is a restatement of integer division. This is where
   fail-closed SHOULD have happened, and structurally cannot.
3. Range induction (gi_induce part 2): SILENTLY WRONG. a=[0,3],
   b=[0,15] written to learner state as fact.
4. Construction (gi_trial_build2): WORKS. 4/4 valid outputs, because
   verification (gi_eval_known) keys on the RAW pair value P, never on
   decoded components, and the range check is self-consistent with the
   machinery's own wrong decode.
5. Classification (gi_classify): AGREES. Same wrong decode, so the
   rubric confirms the wrong grammar's constructions. 4/4 masks the
   breakage.

The encoding assumption therefore breaks first at RANGE INDUCTION
(stage 3), while the guard meant to catch it (stage 2) is vacuous.
The relational induction (licensors) is codec-independent and
unaffected; the codec-dependent part (ranges) is where the wrongness
enters learner state.

### ABLATE arm (W2): 0/4 (class 2 throughout)

Grammar induced, then DELETED via gi_ablate. Base trial produces 0/4
valid (all class 2 multi-dep invalid forms, the same failure mode as
the EXL and EXL2 controls). Nuance worth recording: the wrong grammar
is still causally load-bearing for construction. Removing it returns
the errors, because the CORRECT part of the induction (the licensor
set {44,43}) is what does the work in trial_build2; the wrong ranges
are along for the ride. Wrong does not mean useless here; it means
the grammar asserts false literal ranges while its relational core
is right.

### HARDCODE arm (W3): 4/4

The researcher-authored restriction also passed, but this is fragile:
its hardcoded 0..9 range check (line 210) admits only constructions
whose /16-decoded b' <= 9. The gather order happened to surface such
pairs first for all 4 TEST targets. On a world where the first-found
valid construction decodes to b' > 9, this arm would report class 0
for a semantically valid construction. Not load-bearing for the
diagnosis, recorded as a fragility.

### FRESH arm (W4): 0/4 (class 2 throughout)

No induction, base trial: 0/4. Induction is necessary, same as EXL2.

## Diagnosis: the load-bearing assumption

Assumption (3), the pair codec P(a,b)=a*16+b, is load-bearing at all
five decode sites, and the machinery has NO working guard on it:

- The part-1 sanity check is tautological under any fixed divisor
  (proved above: reduces to P>255). It can never contradict the
  encoding assumption, so induction cannot fail closed on codec
  mismatch. It will always either succeed-wrong (as here) or, for
  P>255 worlds, refuse for the wrong reason.
- Verification and classification both operate on raw P or on the
  same wrong decode, so a codec mismatch never surfaces as a
  construction failure or a rubric failure. The wrongness is
  self-consistent end to end, which is exactly why it is silent.

What does NOT need to change: licensor discovery (codec-independent,
correct here), the nlic<=2 guard (not exercised), verification keyed
on raw P (already codec-independent and the reason construction
survived).

## Minimal machinery change (diagnosed, NOT implemented)

Promote the pair codec from hardcoded constant to induced grammar
state:

1. Add an encoding parameter (divisor D, or an explicit
   decode/encode pair) to the type-70 grammar node as a new field.
2. Induce D in gi_induce from the example stream instead of assuming
   16, and thread it through all five decode sites (lines 53-54,
   89-90, 174, 210, 250).
3. Replace the tautological sanity check with a real one: the
   candidate codec must be cross-consistent with the fact structure
   in a way that discriminates D (re-encoding decoded components
   reproduces P under ANY divisor, so the discriminator has to come
   from elsewhere, e.g. consistency of decoded components with the
   literal co-occurrence structure across the eval/decomp tables).
   Defining that discriminator is the follow-up's hard part; D is
   only weakly identified by the current fact stream.
4. Honest fallback: if no codec is established from the stream,
   refuse induction (return 0, write nothing) rather than writing
   ranges under an assumed codec. Fail-closed is the correct behavior
   for an unidentified codec; silent-wrong is the current bug.

Deliberately not implemented here per the tasking; this report is the
diagnosis the follow-up builds on.

## Researcher-owned vs learner-owned (EXL3)

Researcher-owned: EXL3 definition, the a*8+b encoding, teach order,
TRAIN/TEST split, classification rubric, the induction procedure.
Learner-owned: all SUB/DIV eval facts, all DSUB/DDIV decomp facts, the
4 BUILD facts, the induced licensor set {44,43} (correct), the promoted
MAPs. The induced literal ranges a=[0,3], b=[0,15] sit in learner state
but are an artifact of the researcher's hardcoded codec, not of the
data: the data never supported them and no check could have rejected
them.

## Metrics

- Cognition lines added: 0 to patch/base (byte copies). Driver:
  teaching section rewritten for EXL3 (pair encoder, 0..7 loops);
  arms byte-identical per function.
- Modes/bridges/handlers: 0. New semantic cases: 0. Base
  modifications: 0.
- Determinism: 3/3 byte-identical runs
  (SHA-256 b16383700c8acb696542bdda9d17ee7d3f0582753160b991e67fc20866a1ed5c).
- Induction: 4/4 BUILD examples yielded a grammar (wrong ranges,
  right licensors). Construction: 4/4 novel targets valid under the
  world encoding; ablation 0/4; fresh 0/4.
- Assumption verdict: (3) pair codec is load-bearing and unguarded;
  (1) and (2) held throughout (ids 41/42/43/44/45 behaved exactly as
  in EXL2; world literals 0..7 never touched the 0..9 rubric bound).

## Follow-ups (not started)

1. Implement the codec-induction follow-up per the minimal-change
   diagnosis above; re-run EXL3 and require either correct ranges
   a=[0,7], b=[0,7] or a fail-closed refusal. The current silent-wrong
   must become impossible.
2. The remaining untested assumption breaks are still open probes:
   3 genuine licensors vs the nlic<=2 guard (known from the transfer
   report to refuse; untested with genuine licensors), literals beyond
   0..9 vs the rubric's hardcoded range (expected to break
   measurement, not learning), and ternary operators (arity break;
   messiest, likely needs base-level representation work).
3. Audit other "sanity checks" in the machinery for the same
   tautology pattern: a guard that cannot fire on any reachable input
   is a comment, not a guard.
