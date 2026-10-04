# PREREG H-INTENT-UNIFIED3 RED TEAM (IU3-ADV): FROZEN

## Hypothesis

The H-INTENT-UNIFIED3 repair (verbatim-conflict guard, 16-cap WARN,
bridge_learn split sizing) leaves at least one of the following
exposed: (a) the verbatim-conflict guard is blind to genuine
training-data contradictions whenever the colliding input falls
outside the 16-input record cap, so the X-IU2-1 silent-resolution
failure mode persists for out-of-cap collisions; (b) bridge_learn's
split search has a second fixed-size buffer (distinct-value table)
that can overflow with more than 128 distinct byte values at one
position; (c) the committed raw evidence does not reproduce
byte-identically; (d) the audit finds a hardcoded literal, a missing
ce assignment, or intent-function divergence between the two files.

## Background

- H-INTENT-UNIFIED3 SURVIVES (8/8, 38/38), commit 7470c2b39,
  prereg e638bcb71.
- R1: intent_winner tracks em per candidate (ce[]); if top two both
  em=1, both answers are computed and compared byte-wise; on
  disagreement WITHHOLD AMBIGUOUS (kind -2) with an explicit
  "INTENT VERBATIM-CONFLICT" trace line. If answers agree, existing
  rules apply.
- R2: intent_record_inputs emits "INTENT WARN: record cap 16
  reached; ..." when npairs > 16; truncation behavior unchanged.
- R3: bridge_learn s1idx/s2idx sized z_alloc(npairs*4).
- Repair doc claims: "No heuristic term may silently resolve a
  verbatim-vs-verbatim conflict." Boundary doc notes: "Near-ties
  (em=1 vs em=0 with cf/lm deciding) are unchanged: only
  verbatim-vs-verbatim conflicts trigger the new guard."

## Attacks (frozen)

### X-IU3-1a: cap-times-verbatim composition (PRIMARY)

Setup (one workspace W1):
- Train proc D with 17 reverse pairs, the colliding input LAST
  (17th, unrecorded):
  "abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;
   vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;
   qrs>srq;tuv>vut;qab>baq"
- Train bridge B (5 pairs, all recorded), mirroring the G1 shape
  with condition byte 113 ('q'):
  "qab>zzz;qcd>zzz;abc>ccc;def>ccc;abcde>eeeee"
- Control workspace W1c: train ONLY the 17-pair proc string above.
- Query "qab" on W1 and on W1c.

Predicted mechanism behavior (to be verified, not assumed):
- On W1c: kind 0, answer "baq" (the proc genuinely learned pair 17;
  the contradiction is real training data).
- On W1: proc candidate em=0 (pair 17 unrecorded), bridge candidate
  em=1; the guard's both-em=1 precondition fails; the bridge wins
  (kind 1, answer "zzz") with NO "INTENT VERBATIM-CONFLICT" line.
- A "INTENT WARN" line appears at learn time (R2 working as
  documented).

Kill criterion: kind != -2 on W1 AND no VERBATIM-CONFLICT line in
the W1 query output AND W1c answers "baq" AND the W1 trace shows
proc exact_match=0 with bridge exact_match=1.
Verdict on success: DOWNGRADE (not kill: no frozen bar is broken).
What it narrows: "X-IU2-1 CLOSED" becomes "closed only for
collisions where both records are within the 16-cap"; the guard's
"no silent resolution" claim is falsified for out-of-cap collisions,
and the learn-time WARN does not restore query-time protection.
Setup-void condition: if the bridge does not learn as a bridge with
a firing condition on "qab" (trace must show a bridge candidate with
cond_fire=1), or if W1c does not answer "baq", the fixture is void
and the attack is not scored.

### X-IU3-1b: top-two agreement control (EXPECTED PASS)

Setup: proc A trained "qab>baq" (recorded), bridge C trained with
"qab" recorded answering "baq" as well (agreeing verbatim), plus a
third em=1 candidate disagreeing but ranked third on heuristics.
Concretely: A = "qab>baq;xcd>dcx" (reverse proc, 2 pairs);
C = bridge "qab>baq;qcd>dcq" hmm (must learn as bridge with both
em=1 and same answer "baq" as A, ranked above a disagreeing third).
This is a control: the repair's agree-refinement says the guard
must NOT fire when the top two agree. Expected: no VERBATIM-CONFLICT,
a winner is returned. This attack is scored as PASS-for-the-repair
if the guard stays silent; it becomes a DOWNGRADE only if the guard
fires on agreement (over-broad withholding) or if the documented
semantics are violated. If the fixture cannot be constructed to
spec (third candidate cannot be made em=1 and ranked third), it is
recorded informational and not scored.

### X-IU3-2: distinct-value table overflow (SECONDARY)

Setup: build a 150-pair training string in Zag code (no literals
beyond the generator): for byte values v in 33..182, input bytes
[v,'a','b'], output "xxx" for v in 33..172 (140 pairs) and "yyy"
for v in 173..182 (10 pairs). Train as one T LEARN. Rationale: all
pairs extractable (allok=1), no single program covers both output
classes (direct discovery fails, as in the G3 fixture), so the
split search runs; at position 0 there are 150 distinct byte values,
but dvals is z_alloc(128) in bridge_learn. Predicted: slice-index
panic (if bounds-checked) or corrupted output.
Kill criterion: the process panics, exits nonzero, or 3 runs differ
byte-wise.
Verdict on success: DOWNGRADE (new latent crash in the repaired
function; R3's crash-safety is incomplete). This bug predates IU3;
the finding is that the repair's crash hardening missed it.
Setup-void: if direct discovery succeeds (no split search; check
for the "bridge: direct failed" emit line), the fixture is void.

### X-IU3-3: evidence reproduction (VERIFICATION)

Rebuild iu3_fix.zag, intent_learn.zag, and unified_learn.zag with
the pinned toolchain (znc 2026.07.0-dev, edition 2026), run each
binary 3 times, md5 each run, and cmp byte-for-byte against the
committed IU3_FIX_RAW.txt, IU3_INTENT_REG_RAW.txt, and
IU3_UNIFIED_REG_RAW.txt.
Kill criterion: any run differs from the committed raw file, or
any of the 3 runs differ from each other.
Verdict on success: KILL (frozen K-IU3-5 determinism/reproducibility
is broken; the repair's evidence does not reproduce). This is the
only attack that can kill.

### X-IU3-4: source audit (VERIFICATION)

(a) Diff the 7 intent functions (intent_record_inputs,
intent_record_proc, intent_record_br, intent_exact_match,
intent_qscore, intent_winner, intent_trace_emit) between
intent_learn.zag and unified_learn.zag: must be byte-identical
(X-IU4 faithfulness invariant).
(b) Grep the mechanism regions (everything above main()) of both
files for test-answer literals ("qab", "xab", "tuv", "wqx",
"baq", "zzz", "xxx", "ccc", "ddd"): none may appear outside
main() and comments.
(c) Verify ce[] is assigned for every candidate in both the proc
loop and the bridge loop of intent_winner in both files.
(d) Verify the guard dispatches proc_apply/bridge_apply by kind
for both top and second.
(e) Count "INTENT WARN" emissions on the X-IU3-1a fixture: exactly
1 (proc record), 0 for the 5-pair bridge.
Kill criterion: any literal in mechanism code, any missing ce
assignment, any function divergence, or WARN count != expected.
Verdict on success: DOWNGRADE (audit failure). A missing WARN on
the frozen G2 fixture would additionally break K-IU3-2 (kill);
the audit checks the frozen fixture output too.

## What does NOT count

- Breaking a frozen bar with a fixture identical to a frozen one
  but a different verdict expectation than the prereg (that would
  be re-litigating, not attacking).
- The documented 16-cap truncation itself (X-IU2-3 was already a
  confirmed boundary); only its interaction with the NEW guard
  (X-IU3-1a) counts.
- dvals overflow requiring more than 256 distinct byte values
  (impossible for bytes) or non-extractable pairs (voids the
  fixture by the setup-void condition).
- Any Python at any stage (voids the whole red team).

## Test design (frozen)

Pure Zag. Pinned znc 2026.07.0-dev (edition 2026). No Python
anywhere: no generators, no verifiers, no analysis scripts.

- iu3_adv.zag: byte-copy of the repaired unified_learn.zag
  mechanism (verified by diff), main() replaced by the X-IU3-1a,
  X-IU3-1b, and X-IU3-2 fixtures plus setup diagnostics.
- X-IU3-3 runs the three committed sources unmodified.
- X-IU3-4 is diff/grep over the committed sources.
- Raw outputs committed: IU3_ADV_RAW.txt (md5 over 3 runs).
- Only adversary-owned files staged and committed. No other
  agent's files touched. No em dashes in new docs.

## Commit order

This prereg commit strictly precedes the attack implementation
commit.
