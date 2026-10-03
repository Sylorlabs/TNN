# PREREG: Arena transfer-by-recoding mechanism (ARENA-REMAP, wave-20261001-2321pdt)

Status: FROZEN PREREG. Committed alone before any REMAP implementation,
binary, dev world, or evaluation run. Any change to the design below
requires a dated amendment committed alone before the changed code runs.
Commit-order rule: this file's commit must strictly precede every
implementation commit in this lane.

## 1. Objective

Raise C12 (transfer) from 0.000 on the sealed 68-item arena battery
(seed 71503461337030) with zero score regressions on the other 15
capabilities, 3/3 byte-identical reruns, and full architecture
accounting. Target: 60/68 = 0.882 with C12 at 1.000 (6/6).

Battery count note: the parent task says "15 capabilities" and "the
other 14". The sealed records (REFREEZE_RECORD.md, wave-20261001-1721pdt)
show 16 capabilities and 68 items. The count does not reproduce, so it
is flagged here rather than asserted. The frozen no-regression bar
covers all 15 non-target capabilities (C1-C11, C13-C16).

## 2. Capability pick justification

C12 (transfer, n=6) is picked. C8 (inquiry) is taken by the sibling
ARENA lane and is not duplicated here.

C9 (causal) was examined first per the recommendation and is REJECTED
as the pick, with the evidence recorded in NAMECHECK.md: the 12 causal
expo turns satisfy x==y==z in every observation (world_gen.zag CHECK 1),
so the chain permutation is observationally unidentifiable by design;
the battery contains zero intervention turns; the implemented
discrim|<chain>|<alt> items always list the TRUE chain first and the key
is chain[0], so the only 3/3 mechanism is "parse the first candidate,
emit its first variable", which uses zero experience and builds zero
causal structure. That is a benchmark-format exploit, rejected under
the no-gaming rule. The honest causal answer (UNKNOWN) scores 0. No
genuine causal mechanism can meet a C9=3/3 kill bar. Recorded here as a
negative finding with a world-generator fix recommendation (randomize
candidate order; add real intervention turns). It is not built.

C15 (goal, n=1, "listnames") rejected: single item, narrow enumeration
mechanism, ordering-fragile, low information gain.

C12 selected because: (a) genuinely zero in the v6 refreeze (0.000,
REFREEZE_RECORD.md); (b) genuinely passable without gaming: remap_prod
asks for the learned Zem transform output under a question-given value
permutation, remap_class asks whether a remapped triple matches the
learned template under the same permutation; both are solved by
composing the learner's own exposure-learned templates (the structures
behind v6's C10/C16 1.000 on this same world) with the permutation
parsed from the question at runtime; (c) no sealed values, entities, or
answers are hardcoded and the mechanism generalizes to any permutation
and any learned template; (d) 6 items make the gain material; (e) it is
the transfer-family instance of the composition shape (learned
structure times novel encoding), adjacent to the composition frontier.

## 3. Mechanism spec (REMAP)

Two question-type handlers in the existing test-turn dispatch, reusing
the existing learned Zem template slots (A template at W offsets
13888/13892/13896, B template at 13900/13904/13908, learned flags at
13912/13916). No part is gated on a capability number.

3.1 remap_prod|<r0,r1,r2,r3>|<t0,t1,t2>
  Parse the 4 permutation values from p1 (new helper parse_qsegs4,
  same shape as the existing parse_qsegs; each value must be 0..3 or
  the reply stays UNKNOWN). Parse the input triple from p2 with
  parse_qsegs. Require both Zem learned flags (same condition as the
  existing zemprod handler). Require the input triple to equal the
  learned A template (same match as zemprod); mismatch stays UNKNOWN.
  Map to the learned B outputs, then apply the permutation:
  a_i = perm[B_i]. Reply exactly "a0,a1,a2". Append one deterministic
  trace line to <statedir>/remap_trace.txt:
  "remap_prod t=<t> B=<b> perm=<p> out=<a>".

3.2 remap_class|<r0,r1,r2,r3>|<s0,s1,s2>
  Parse the permutation from p1 and the candidate triple from p2.
  Require the Zem A learned flag (same condition as the existing
  zemclass handler). Compute the expected triple e_i = perm[A_i] and
  reply "yes" iff the candidate equals it, else "no". (The generator's
  invalid item corrupts one position of the valid triple, so it
  compares unequal.) Trace line:
  "remap_class s=<s> exp=<e> yes|no".
  If the A template was never learned, the reply stays UNKNOWN,
  mirroring zemclass honesty.

3.3 Surgical implementation points (v6 base source
devint1_contestant_v6.zag, sha256
c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89):
  (a) add parse_qsegs4 next to parse_qsegs;
  (b) add the two handler blocks in the test dispatch immediately
  after the existing zemclass block;
  (c) no other handler logic is touched; no expo-path changes.

Architecture constraints (frozen): 0 new modes, 0 bridges, 0 routers,
0 task-specific admission gates, 0 hardcoded semantic cases, 0
hardcoded entities, values, permutations, templates, or answers. The
permutation is parsed from the question at runtime; the templates come
from exposure. Learner-state structures created: none new (the
mechanism composes existing learned state; the trace log is a
decision record, not cognitive state).

## 4. Why this scores on the sealed C12 items

Verified preconditions from committed sources (not from the key):
the v6 refreeze scores C10 2/2 and C16 6/6 on this exact sealed world,
so the learned A and B templates are exactly the true templates; the
generator (world_gen.zag) defines the remap_prod key as
perm[true-B-output] and the remap_class valid triple as
perm[true-A-triple]. REMAP computes exactly these quantities from the
learned templates and the runtime-parsed permutation, so all 6 items
score 1000 by exact match. The 3 remap_prod questions are identical,
and the 3 remap_class questions are valid/invalid/valid; the mechanism
treats each independently (no cross-item state), so repetition is
handled uniformly.

## 5. Kill bars (frozen; never move after this commit)

K1 (C12 transfer): C12 = 6/6 = 1.000 on the sealed 68-item battery.
K2 (no regression): per-capability scores on C1-C11 and C13-C16
byte-identical to the v6 refreeze record; total 60/68. Zero score
regressions on all 15 non-target capabilities.
K3 (determinism): 3/3 full sealed runs produce byte-identical stripped
reply streams (ms and rss_kb excluded, the v6 K6 exclusion class) and
byte-identical remap_trace.txt files.
K4 (pure Zag): zero non-safebin executable invocations in this lane;
`which python3` prints nothing at lane start and lane end. Any
forbidden invocation is PROCESS-FAIL and voids the verdict.
K5 (sealed validity): world_gen and arena rebuilt from committed
sources with hashes matching the refreeze record (world_gen
c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211,
arena 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076);
regenerated turns.jsonl hash matches the sealed world
(0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469);
pre-run hashes of turns.jsonl and the key file recorded before the
contestant runs; the contestant never opens key/idmap/proof files
(worlddir arg-presence-checked only); grep audit of the mechanism
source for the sealed remap permutation string and the sealed template
value strings returns zero hits. Disclosure: while verifying the turn
protocol from the committed sealed world, the worker saw the sealed
C12 question strings (contestant-visible content); the mechanism parses
them at runtime and hardcodes none of them, and the grep audit is the
evidence.
K6 (negative controls, both halves causal):
K6a ablation REMAP_PROD_OFF (remap_prod handler block disabled,
surgical source delta): the 3 remap_prod items reply UNKNOWN, C12
prod half = 0/3.
K6b ablation REMAP_CLASS_OFF (remap_class handler block disabled,
surgical source delta): the 3 remap_class items reply UNKNOWN, C12
class half = 0/3.
K7 (architecture): delta accounting recorded (source lines
added/changed; 0 new modes, 0 bridges, 0 routers, 0 task-specific
admission gates, 0 hardcoded semantic cases); keyword scan of added
lines for mode/bridge/router/gate finds only benign hits; learner
state adds no new structures (existing Zem slots reused; trace log
only).
K8 (no L3 claim): explicit disclaimer in the evaluation report. This
mechanism does not meet Criterion 0: the "apply the question-given
permutation to the learned template output" semantics is
researcher-authored handler logic (fails C0-A runtime-defined
semantics); the recoding form is fixed, not incrementally constructed
from experience (fails C0-B); no unforeseen representational forms are
produced (fails C0-C); no new representation is invented, only an
existing template reused under a recoding (fails C0-D). Plainly:
REMAP is L2 transfer infrastructure (composition of learned structure
with a given recoding), not L3 representational invention. No L3 claim
is made.

BUILD-PASS requires K1, K2, K3, and K4 all PASS. K5 through K8 must
also PASS for the verdict to stand; any bar failing yields BUILD-FAIL
with the killing evidence named. Kill bars never move after freezing;
a broken prereg is amended transparently and re-frozen, never salvaged.

## 6. Evaluation protocol (frozen)

6.1 Rebuild world_gen and arena from committed competitive_arena
sources with the pinned znc; verify hashes against the refreeze
record; abort on mismatch.
6.2 Regenerate the world (deterministic seed inside world_gen.zag);
verify turns.jsonl sha256 equals
0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469.
6.3 Record pre-run sha256 of turns.jsonl and the key file. Build the
REMAP contestant from the committed implementation source; record its
sha256.
6.4 Dev smoke test (in /tmp, never sealed): hand-crafted mini turn
streams exercising remap_prod (known template + permutation),
remap_class yes, remap_class no, malformed permutation (UNKNOWN),
and no-template (UNKNOWN). Must pass before the sealed run.
6.5 Sealed run: fresh state dir, per-turn invocation
`remap <turn.json> <statedir> <worlddir>`, replies appended, over all
turns; score with the rebuilt arena binary. Repeat twice more (3/3)
for K3.
6.6 Ablations K6a/K6b: surgical source deltas, rebuilt, one sealed run
each on the same world, C12 halves scored.
6.7 Audits: grep for sealed remap/template strings in mechanism
source (K5); keyword scan for mode/bridge/router/gate in added lines
(K7); byte scan for em-dash in lane docs.

## 7. Scope reminders (frozen)

REMAP is a CANDIDATE mechanism only. No L3 claim (K8), no TNN-2
substrate claim, no TNN-beats-LLM claim. The canonical 0.573 is not
moved by this result (only a clean refreeze reproducing composition
without contamination can move it). The LLM baseline comparison
remains pending credentials and is out of scope for this lane.

FROZEN 2026-10-01 PDT. Lane: wave-20261001-2321pdt/ARENA2.
